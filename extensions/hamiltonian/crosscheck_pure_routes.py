#!/usr/bin/env python3
"""Cross-check the two independent pure-top classifications on the same inputs.

check_two_root.classify(H, routes='gauge') uses only the check_gauge.py line
(K1, K1', K2, K1+K2, extended K3, K4, NA/NE/NB/NT/NV/NQ, RS, TP, TE);
routes='core_overlap' uses only research/core_overlap (PP, QC, SC, SS, SO, SCP,
QF, QR, HR, CP). For every sampled pure top on which both answer with a proved
core, the predicted core dimensions in each degree <= N must agree. A
disagreement, or a case only one side proves, is reported; with --direct every
proved prediction is also compared with the direct filtered kernel
{G : deg G <= N, C_k D^r G = 0, r <= R}.

The samples are triangular normal forms tau*h(Q, P), P = p + w(q), with random
h and w, perfect-power and linear transverse tops, and random affine images.
Agreement on samples is evidence of consistency, not a proof of either line.

Usage: crosscheck_pure_routes.py [--count N] [--seed S] [--direct] [--out FILE]
"""
from __future__ import annotations
import argparse
import json
import random
import sys
import time
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parent)]
import check_two_root as TR          # noqa: E402
import check_triangular as CT        # noqa: E402
import weyl_receipts as W            # noqa: E402
from test_two_root import predicted_res, linmap   # noqa: E402


def sample(rng):
    kind = rng.choice(['tri', 'tri', 'tri', 'transverse', 'affine'])
    if kind in ('tri', 'affine'):
        e = rng.choice([2, 2, 2, 3])
        w = {e: F(1), 1: F(rng.randint(-1, 1))}
        s = rng.choice([2, 3, 4])
        h = {(0, s): F(1)}
        for _ in range(rng.randint(1, 4)):
            i, j = rng.randint(0, 3), rng.randint(0, s - 1)
            if i * e + j < s * e:                    # stay below the pure top
                h[(i, j)] = F(rng.randint(-2, 2))
        H = CT.tri(h, w)
        if kind == 'affine':
            H = linmap(H, 1, rng.randint(-1, 1), 0, 1, rng.randint(-1, 1), rng.randint(-1, 1))
        return W.tidy(H)
    # transverse tops: q^k (p + v(q))^s + lower, s >= 2
    k, s = rng.randint(0, 3), rng.choice([2, 3])
    v = {(rng.randint(2, 4), 0): F(1)}
    G = TR.add({(1, 1): F(1)} if rng.random() < 0.5 else {(0, 1): F(1)}, v)   # qp + v or p + v
    H = TR.mul(TR.power({(1, 0): F(1)}, k), TR.power(G, s))
    for _ in range(rng.randint(0, 3)):
        H = TR.add(H, {(rng.randint(0, 3), rng.randint(0, 1)): F(rng.randint(-2, 2))})
    return W.tidy(H)


def predictions(H, N):
    out = {}
    for side in ('gauge', 'core_overlap'):
        try:
            r = TR.classify(H, routes=side)
        except ValueError as exc:
            return None, str(exc)
        if r.get('top') != 'pure':
            return None, 'not pure'
        want = predicted_res(r, N) if r.get('proved') else None
        out[side] = {'route': r['route'], 'proved': bool(r.get('proved')), 'core': r['core'],
                     'dim': want, 'degree': r['degree']}
    return out, None


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--count', type=int, default=400)
    ap.add_argument('--seed', type=int, default=7)
    ap.add_argument('--direct', action='store_true')
    ap.add_argument('--out', type=Path)
    a = ap.parse_args()
    rng = random.Random(a.seed)
    tally = {'pure_samples': 0, 'both_proved': 0, 'agree': 0, 'gauge_only': 0,
             'core_overlap_only': 0, 'neither': 0, 'disagree': 0, 'direct_checked': 0,
             'direct_mismatch': 0}
    routes, issues = {}, []
    t0 = time.perf_counter()
    seen = set()
    while tally['pure_samples'] < a.count:
        H = sample(rng)
        key = tuple(sorted(H.items()))
        if key in seen or not H:
            continue
        seen.add(key)
        try:
            d = max(i + j for i, j in H)
        except ValueError:
            continue
        if d < 3:
            continue
        N = d + 2
        pr, why = predictions(H, N)
        if pr is None:
            continue
        tally['pure_samples'] += 1
        g, c = pr['gauge'], pr['core_overlap']
        pair = f"{g['route']} | {c['route']}"
        routes[pair] = routes.get(pair, 0) + 1
        if g['dim'] is not None and c['dim'] is not None:
            tally['both_proved'] += 1
            if g['dim'] == c['dim']:
                tally['agree'] += 1
            else:
                tally['disagree'] += 1
                issues.append({'H': TR.ser(H), 'N': N, 'gauge': g, 'core_overlap': c})
        elif g['dim'] is not None:
            tally['gauge_only'] += 1
        elif c['dim'] is not None:
            tally['core_overlap_only'] += 1
        else:
            tally['neither'] += 1
        if a.direct and d <= 6:
            from test_root_rigidity import filtered_dim
            dims = {x['dim'] for x in (g, c) if x['dim'] is not None}
            if dims:
                actual = filtered_dim(H, N, 8)
                tally['direct_checked'] += 1
                if dims != {actual}:
                    tally['direct_mismatch'] += 1
                    issues.append({'H': TR.ser(H), 'N': N, 'direct': actual, 'gauge': g,
                                   'core_overlap': c})
    result = {'status': 'passed' if not issues else 'issues', 'seed': a.seed, 'tally': tally,
              'route_pairs': dict(sorted(routes.items(), key=lambda kv: -kv[1])),
              'issues': issues, 'seconds': round(time.perf_counter() - t0, 1)}
    text = json.dumps(result, indent=1)
    if a.out:
        a.out.write_text(text + '\n')
    print(text)
    return 0 if not issues else 1


if __name__ == '__main__':
    sys.exit(main())
