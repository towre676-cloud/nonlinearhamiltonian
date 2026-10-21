#!/usr/bin/env python3
"""Supplied-unit orbit compiler for x^2 - D y^2 = N (A1 producer, pell-orbits-v1).

Seeds come from the proved reduction window (see check_pell.py); modular filters are
full-state cycles of the unit map mod q (a permutation, det = 1, so no transient tail);
height populations use the closed residue-count formula with an exact M(Y) found by
exponential bracketing and binary search on the orbit index (integer comparisons only).
The certificate is replayed by check_pell.py, which recounts by direct iteration.

Model: {"D": 2, "N": -7, "unit": [3, 2], "filter": {"modulus": 3, "accept": [[x, y], ...]},
        "height": 1000}            (filter and height optional)
Usage: pell.py MODEL.json [--output CERT.json] [--max-states N] [--max-window N]
"""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import check_pell as C  # noqa: E402


def mat_pow(D, a, b, j):
    """eps^j as (u, v) with eps^j = u + v sqrt D, by binary powering."""
    ru, rv, bu, bv = 1, 0, a, b
    while j:
        if j & 1:
            ru, rv = ru * bu + D * rv * bv, ru * bv + rv * bu
        bu, bv = bu * bu + D * bv * bv, 2 * bu * bv
        j >>= 1
    return ru, rv


def orbit_point(D, seed, a, b, j):
    u, v = mat_pow(D, a, b, j)
    x, y = seed
    return x * u + D * y * v, x * v + y * u


def last_index(D, seed, a, b, Y):
    """Largest j >= 0 with y_j <= Y (y_j strictly increasing for j >= 1 on this branch), or -1."""
    if orbit_point(D, seed, a, b, 0)[1] > Y:
        return -1
    hi = 1
    while orbit_point(D, seed, a, b, hi)[1] <= Y:
        hi *= 2
    lo = hi // 2                      # y_lo <= Y < y_hi
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if orbit_point(D, seed, a, b, mid)[1] <= Y:
            lo = mid
        else:
            hi = mid
    return lo


def compile_model(model, max_states=10 ** 6, max_window=10 ** 7):
    D, N, a, b = C.read(model)
    bound = b * b * N if N > 0 else a * a * (-N) // D + 1
    if bound > max_window ** 2:
        return {'status': 'unknown', 'reason': 'seed window exceeds the declared budget'}
    seeds, end = C.window(D, N, a, b)
    cert = {'format': C.FORMAT, 'model_sha256': C.digest(model), 'order': 'Z[sqrt D], integer coordinates',
            'unit_identity': f'{a}^2 - {D}*{b}^2 = 1',
            'seed_bound': ('y^2 < b^2 N, x > 0, y >= 0' if N > 0 else 'D y^2 < a^2 |N|, x >= 0, y > 0'),
            'seeds': seeds, 'window_end_exclusive': end}
    flt = model.get('filter')
    if flt:
        q = flt['modulus']
        cert['cycles'] = []
        for x, y in seeds:
            st, s = [], [x % q, y % q]
            while not st or s != st[0]:
                st.append(s)
                if len(st) > max_states:
                    return {'status': 'unknown', 'reason': 'modular state budget exhausted'}
                s = [(a * s[0] + D * b * s[1]) % q, (b * s[0] + a * s[1]) % q]
            cert['cycles'].append({'states': st, 'period': len(st),
                                   'accepted_indices': [k for k, z in enumerate(st) if C.accepted(z, flt)]})
    Y = model.get('height')
    if Y is not None:
        total = acc = 0
        for i, seed in enumerate(seeds):
            M = last_index(D, seed, a, b, Y)
            total += M + 1
            if flt:
                P, J = cert['cycles'][i]['period'], cert['cycles'][i]['accepted_indices']
                acc += sum(1 + (M - r) // P for r in J if r <= M)
        cert['height_count'] = {'height': Y, 'nonnegative_branch': total, 'accepted': acc if flt else None}
    cert['status'] = 'complete'
    cert['result'] = C.check(cert, model)
    return cert


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('model', type=Path)
    ap.add_argument('--output', type=Path)
    ap.add_argument('--max-states', type=int, default=10 ** 6)
    ap.add_argument('--max-window', type=int, default=10 ** 7)
    a = ap.parse_args()
    try:
        cert = compile_model(json.loads(a.model.read_text()), a.max_states, a.max_window)
    except (ValueError, KeyError, TypeError) as e:
        print(json.dumps({'status': 'invalid_model', 'reason': str(e)}))
        sys.exit(2)
    if a.output and cert.get('status') == 'complete':
        a.output.write_text(json.dumps(cert, indent=1) + '\n')
    print(json.dumps({k: cert[k] for k in cert if k in ('status', 'seeds', 'height_count', 'reason')}, indent=2))


if __name__ == '__main__':
    main()
