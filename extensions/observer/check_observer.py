#!/usr/bin/env python3
"""Independent checker for minimal target-observer certificates (observer-closure-v2).

It never imports or calls the compiler. It recomputes, with its own exact rational
arithmetic, every identity that the theorem in programmes/TARGET_OBSERVERS.md needs:

  provenance  each basis row Q_i equals G_{t_i} A_{w_i} for its declared word w_i
  rank        the rows of Q are linearly independent (Q has full row rank r)
  invariance  Q A_a = B_a Q for every action a
  target      G = C Q
  panel       either K H = Q (static recovery) or a hidden state v with H v = 0,
              Q_i v != 0 and the lost word's output G_t A_w v != 0

Invariance plus target containment proves sufficiency for every future word and
initial state; provenance plus rank proves that no linear summary of smaller rank
is sufficient. Usage: check_observer.py CERT.json [--input MODEL.json]
"""
from __future__ import annotations
import argparse
import hashlib
import json
import sys
from fractions import Fraction as F
from pathlib import Path

FORMAT = 'observer-closure-v2'


def _rat(x):
    if type(x) not in (int, str) and not isinstance(x, F):
        raise ValueError('coefficients must be exact integers or rational strings')
    return F(x)


def _mat(rows, cols, nrows=None):
    if not isinstance(rows, list) or (nrows is not None and len(rows) != nrows):
        raise ValueError('wrong matrix row count')
    if any(not isinstance(r, list) or len(r) != cols for r in rows):
        raise ValueError('wrong matrix column count')
    return [[_rat(x) for x in r] for r in rows]


def _str(rows):
    return [[str(F(x)) for x in r] for r in rows]


def canonical_model(model):
    """The canonical exact form that the model hash binds to."""
    n = model['dimension']
    if type(n) is not int or n < 1:
        raise ValueError('dimension must be a positive integer')
    acts = model['actions']
    if not isinstance(acts, dict) or any(not isinstance(k, str) or not k for k in acts):
        raise ValueError('actions must be a map with nonempty string names')
    out = {'dimension': n,
           'actions': {k: _str(_mat(v, n, n)) for k, v in sorted(acts.items())},
           'target': _str(_mat(model['target'], n))}
    if 'observation' in model:
        out['observation'] = _str(_mat(model['observation'], n))
    return out


def model_digest(model):
    raw = json.dumps(canonical_model(model), sort_keys=True, separators=(',', ':'), ensure_ascii=False)
    return hashlib.sha256(raw.encode()).hexdigest()


def _mul(a, b, cols):
    return [[sum((x * b[k][j] for k, x in enumerate(r)), F(0)) for j in range(cols)] for r in a]


def _rank(rows, cols):
    a = [r[:] for r in rows]
    rk = 0
    for c in range(cols):
        piv = next((i for i in range(rk, len(a)) if a[i][c]), None)
        if piv is None:
            continue
        a[rk], a[piv] = a[piv], a[rk]
        for i in range(rk + 1, len(a)):
            if a[i][c]:
                f = a[i][c] / a[rk][c]
                a[i] = [x - f * y for x, y in zip(a[i], a[rk])]
        rk += 1
    return rk


def _word_row(row, word, acts):
    # Chronological word [a1,...,ak] acts by A_ak ... A_a1, so the row is G A_ak ... A_a1.
    for a in reversed(word):
        m = acts[a]
        row = [sum((row[i] * m[i][j] for i in range(len(row))), F(0)) for j in range(len(m))]
    return row


def check(cert, expected_model=None):
    if cert.get('format') != FORMAT:
        raise ValueError('unknown certificate format')
    if cert.get('coefficient_domain') != 'Q':
        raise ValueError('coefficient domain must be Q')
    if cert.get('word_convention') != 'chronological: [a1,...,ak] acts by A_ak...A_a1':
        raise ValueError('undeclared or unsupported word convention')
    model = canonical_model(cert['model'])
    if model != cert['model'] or model_digest(model) != cert['model_sha256']:
        raise ValueError('model is not canonical or its hash does not match')
    if expected_model is not None and model != canonical_model(expected_model):
        raise ValueError('certificate belongs to a different input model')
    n = model['dimension']
    acts = {k: _mat(v, n, n) for k, v in model['actions'].items()}
    g = _mat(model['target'], n)
    q = _mat(cert['basis'], n)
    r = len(q)
    if _rank(q, n) != r:
        raise ValueError('basis rows are dependent')
    words = cert['basis_words']
    if not isinstance(words, list) or len(words) != r:
        raise ValueError('wrong provenance count')
    for row, w in zip(q, words):
        t, word = w.get('target_row'), w.get('word')
        if type(t) is not int or not 0 <= t < len(g):
            raise ValueError('invalid target-row provenance')
        if not isinstance(word, list) or any(not isinstance(a, str) or a not in acts for a in word):
            raise ValueError('invalid word provenance')
        if row != _word_row(g[t], word, acts):
            raise ValueError('basis row is not its declared target word')
    if _mul(_mat(cert['target_factor'], r, len(g)), q, n) != g:
        raise ValueError('target factorization G = C Q fails')
    if set(cert['quotient_actions']) != set(acts):
        raise ValueError('action alphabet mismatch')
    for k, a in acts.items():
        if _mul(q, a, n) != _mul(_mat(cert['quotient_actions'][k], r, r), q, n):
            raise ValueError('intertwining Q A = B Q fails for action ' + k)
    panel = None
    if 'observation' in model:
        h = _mat(model['observation'], n)
        p = cert['panel']
        if p['status'] == 'recoverable':
            if _mul(_mat(p['recovery'], len(h), r), h, n) != q:
                raise ValueError('sensor recovery identity K H = Q fails')
        elif p['status'] == 'impossible':
            v = [_rat(x) for x in p['invisible_state']]
            i = p['lost_basis_row']
            if len(v) != n or type(i) is not int or not 0 <= i < r:
                raise ValueError('malformed invisible-state witness')
            dot = lambda row: sum((x * y for x, y in zip(row, v)), F(0))
            if any(dot(row) for row in h) or not dot(q[i]):
                raise ValueError('invisible-state witness fails')
            if p['lost_target_word'] != words[i]:
                raise ValueError('lost output word mismatch')
            if F(p['output_difference']) != dot(q[i]):
                raise ValueError('declared output difference is wrong')
        else:
            raise ValueError('unknown panel claim')
        panel = p['status']
    if cert.get('rank') != r:
        raise ValueError('declared rank mismatch')
    return {'status': 'passed', 'format': FORMAT, 'minimal_linear_state_dimension': r, 'panel': panel,
            'input_bound': expected_model is not None,
            'scope': 'all finite action words, all initial states and all linear state summaries of the '
                     'encoded finite rational model'}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('certificate', type=Path)
    ap.add_argument('--input', type=Path)
    a = ap.parse_args()
    try:
        exp = json.loads(a.input.read_text()) if a.input else None
        print(json.dumps(check(json.loads(a.certificate.read_text()), exp), indent=2))
    except (ValueError, KeyError, TypeError, IndexError, ZeroDivisionError) as e:
        print(json.dumps({'status': 'rejected', 'reason': str(e)}))
        sys.exit(2)


if __name__ == '__main__':
    main()
