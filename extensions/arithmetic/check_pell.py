#!/usr/bin/env python3
"""Independent checker for supplied-unit Pell orbit certificates (pell-orbits-v1).

Model: x^2 - D y^2 = N in the declared order Z[sqrt D] with integer coordinates, D > 0
nonsquare, N != 0, and a supplied unit eps = a + b sqrt D, a, b > 0, a^2 - D b^2 = 1 (not
necessarily fundamental). Reduction theorem (programmes/OBSTRUCTIONS_AND_ARITHMETIC.md):
every solution alpha > 0 is uniquely seed * eps^j (j in Z), the seeds being exactly
  N > 0:  x > 0, y >= 0, y^2 < b^2 N            (x = sqrt(N + D y^2))
  N < 0:  x >= 0, y > 0, D y^2 < a^2 |N|        (x = sqrt(D y^2 - |N|))
and the nonnegative-coordinate branch is exactly {seed * eps^j : j >= 0}.

The checker re-enumerates the window with exact integer square tests, so a missing or
extra seed is detected; it re-runs every modular cycle on the full state (x mod q, y mod q)
and confirms closure; and it recounts the filtered height population by iterating the
orbits directly (no logarithms). Usage: check_pell.py CERT.json --input MODEL.json
"""
from __future__ import annotations
import argparse
import hashlib
import json
import sys
from math import isqrt
from pathlib import Path

FORMAT = 'pell-orbits-v1'


def digest(model):
    return hashlib.sha256(json.dumps(model, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def read(model, cert=None):
    D, N = model['D'], model['N']
    if model['unit'] == 'fundamental':
        # The orbit unit is the certified smallest norm-one unit of Z[sqrt D].
        if cert is None or 'unit_certificate' not in cert:
            raise ValueError('a fundamental-unit model needs an embedded unit certificate')
        import check_units
        uc = cert['unit_certificate']
        check_units.check(uc, {'D': D})
        a, b = uc['norm_one_unit']
    else:
        a, b = model['unit']
    if any(type(v) is not int for v in (D, N, a, b)):
        raise ValueError('D, N and the unit must be integers')
    if D <= 0 or isqrt(D) ** 2 == D:
        raise ValueError('D must be a positive nonsquare')
    if N == 0:
        raise ValueError('N must be nonzero')
    if a <= 0 or b <= 0 or a * a - D * b * b != 1:
        raise ValueError('supplied unit must satisfy a, b > 0 and a^2 - D b^2 = 1')
    return D, N, a, b


def window(D, N, a, b):
    seeds = []
    y = 0 if N > 0 else 1
    while (y * y < b * b * N) if N > 0 else (D * y * y < a * a * (-N)):
        s = N + D * y * y
        if s >= 0 and isqrt(s) ** 2 == s and (N < 0 or isqrt(s) > 0):
            seeds.append([isqrt(s), y])
        y += 1
    return seeds, y


def accepted(state, flt):
    x, y = state
    q = flt['modulus']
    return [x % q, y % q] in flt['accept']


def check(cert, model):
    if cert.get('format') != FORMAT or cert.get('model_sha256') != digest(model):
        raise ValueError('not a pell-orbits-v1 certificate for this model')
    D, N, a, b = read(model, cert)
    seeds, end = window(D, N, a, b)
    if cert['seeds'] != seeds or cert['window_end_exclusive'] != end:
        raise ValueError('seed list differs from the exact window enumeration')
    for x, y in seeds:
        if x * x - D * y * y != N:
            raise ValueError('seed has the wrong norm')
    flt = model.get('filter')
    if flt:
        q = flt['modulus']
        if type(q) is not int or q < 1 or any(len(r) != 2 or not all(type(v) is int and 0 <= v < q for v in r)
                                              for r in flt['accept']):
            raise ValueError('malformed modular filter')
        if len(cert['cycles']) != len(seeds):
            raise ValueError('one modular cycle per seed required')
        for (x, y), cyc in zip(seeds, cert['cycles']):
            st = cyc['states']
            if st[0] != [x % q, y % q] or cyc['period'] != len(st) or len(set(map(tuple, st))) != len(st):
                raise ValueError('cycle must start at the seed state and have distinct states')
            for k in range(len(st)):
                u, v = st[k]
                nxt = [(a * u + D * b * v) % q, (b * u + a * v) % q]
                if nxt != st[(k + 1) % len(st)]:
                    raise ValueError('cycle does not follow the unit map')
            if cyc['accepted_indices'] != [k for k, s in enumerate(st) if accepted(s, flt)]:
                raise ValueError('accepted residues are wrong')
    Y = model.get('height')
    if Y is not None:
        total = acc = 0
        for x, y in seeds:
            while y <= Y:
                total += 1
                acc += bool(flt) and accepted((x, y), flt)
                x, y = a * x + D * b * y, b * x + a * y
        if cert['height_count'] != {'height': Y, 'nonnegative_branch': total,
                                    'accepted': acc if flt else None}:
            raise ValueError('height counts are wrong')
    full = model['unit'] == 'fundamental'
    return {'status': 'passed', 'complete': True, 'seeds': seeds, 'unit': [a, b],
            'scope': ('every integer solution is +/- seed * eps^j (j in Z), eps the certified smallest norm-one '
                      'unit, so the seeds are exactly the orbits under the full norm-one unit group of Z[sqrt D]'
                      if full else
                      'every integer solution is +/- seed * eps^j (j in Z) for the supplied unit; the '
                      'nonnegative branch is seed * eps^j, j >= 0; no claim about fundamental units')
                     + '; the maximal order is not treated'}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('certificate', type=Path)
    ap.add_argument('--input', type=Path, required=True)
    a = ap.parse_args()
    try:
        print(json.dumps(check(json.loads(a.certificate.read_text()), json.loads(a.input.read_text())), indent=2))
    except (ValueError, KeyError, TypeError, IndexError) as e:
        print(json.dumps({'status': 'rejected', 'reason': str(e)}))
        sys.exit(2)


if __name__ == '__main__':
    main()
