#!/usr/bin/env python3
"""Minimal target-observer compiler, certificate format observer-closure-v2.

Input model (exact integers or rational strings; floats rejected):
  {"dimension": n, "actions": {"name": n x n}, "target": m x n, "observation": k x n (optional)}

Output: basis Q with word provenance, quotient actions B_a with Q A_a = B_a Q,
target factor C with G = C Q, and for a static panel H either K with K H = Q or an
invisible initial state v (H v = 0) together with a future word whose output changes.
The result is replayed by the independent check_observer.py before it is returned.

Commands: compile MODEL.json [--output CERT.json] [--max-dimension N]
"""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parent)]
import qlinalg as L                       # noqa: E402
import check_observer                     # noqa: E402

CONVENTION = 'chronological: [a1,...,ak] acts by A_ak...A_a1'


def compile_model(model, max_dimension=None):
    model = check_observer.canonical_model(model)
    n = model['dimension']
    acts = {k: L.mat(v, n, n) for k, v in model['actions'].items()}
    g = L.mat(model['target'], n)
    if max_dimension is not None and n > max_dimension:
        return {'status': 'unknown', 'reason': f'dimension {n} exceeds declared budget {max_dimension}'}
    q, words = [], []
    for i, row in enumerate(g):
        if L.rank(q + [row], n) > len(q):
            q.append(row)
            words.append({'target_row': i, 'word': []})
    history = [len(q)]
    frontier = list(range(len(q)))
    # Breadth-first over newly added rows: W_{k+1} = W_k + sum_a W_k A_a needs only new rows.
    while frontier:
        new = []
        for i in frontier:
            for name, a in acts.items():
                cand = L.row_times(q[i], a)
                if L.rank(q + [cand], n) > len(q):
                    q.append(cand)
                    words.append({'target_row': words[i]['target_row'], 'word': [name] + words[i]['word']})
                    new.append(len(q) - 1)
        frontier = new
        if new:
            history.append(len(q))
    r = len(q)
    cert = {
        'format': check_observer.FORMAT, 'coefficient_domain': 'Q', 'word_convention': CONVENTION,
        'model': model, 'model_sha256': check_observer.model_digest(model), 'rank': r,
        'basis': L.strs(q), 'basis_words': words,
        'quotient_actions': {k: L.strs([L.left_solve(q, L.row_times(row, a), n) for row in q])
                             for k, a in acts.items()},
        'target_factor': L.strs([L.left_solve(q, row, n) for row in g]),
        'diagnostics': {'closure_dimensions': history,
                        'stabilization_bound': n - history[0],
                        'note': 'diagnostic only; the proof objects are the identities above'},
        'theorem': ('z = Q x evolves by z -> B_a z and reproduces G A_w x for every word w and every x; '
                    'every linear summary R with that property satisfies rank R >= rank Q.'),
    }
    if 'observation' in model:
        h = L.mat(model['observation'], n)
        rec = [L.left_solve(h, row, n) for row in q]
        if all(x is not None for x in rec):
            cert['panel'] = {'status': 'recoverable', 'recovery': L.strs(rec)}
        else:
            v = next(v for v in L.null_basis(h, n) if any(L.dot(row, v) for row in q))
            i = next(i for i, row in enumerate(q) if L.dot(row, v))
            cert['panel'] = {'status': 'impossible', 'invisible_state': L.vstr(v), 'lost_basis_row': i,
                             'lost_target_word': words[i], 'output_difference': str(L.dot(q[i], v)),
                             'meaning': 'initial states x and x+v give identical panel readings but differ '
                                        'in target row target_row after the chronological word'}
    check_observer.check(cert, model)
    return cert


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)
    c = sub.add_parser('compile')
    c.add_argument('model', type=Path)
    c.add_argument('--output', type=Path)
    c.add_argument('--max-dimension', type=int)
    a = ap.parse_args()
    try:
        cert = compile_model(json.loads(a.model.read_text()), a.max_dimension)
    except (ValueError, KeyError, TypeError) as e:
        print(json.dumps({'status': 'invalid_model', 'reason': str(e)}))
        sys.exit(2)
    text = json.dumps(cert, indent=2, ensure_ascii=False) + '\n'
    if a.output:
        a.output.write_text(text)
        print(json.dumps({'status': 'written', 'path': str(a.output), 'rank': cert.get('rank')}))
    else:
        sys.stdout.write(text)


if __name__ == '__main__':
    main()
