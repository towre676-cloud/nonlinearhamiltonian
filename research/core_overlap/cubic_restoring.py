#!/usr/bin/env python3
"""Independent exact calibration of the cubic restoring theorem.

For H=(p+q^2)^3+lam*q^2, lam!=0, the full polynomial dynamic core is
span{1,H}. C3 alone at depths 0..3 determines it, sharply. The proof in
cubic_restoring.md is all-degree; finite matrices below are exact replays.
Only the Python standard library is required.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as F
from math import comb, factorial
import json
from pathlib import Path


def tidy(f):
    return {k: F(v) for k, v in f.items() if v}


def add(*fs):
    out = {}
    for f in fs:
        for k, v in f.items():
            out[k] = out.get(k, F(0)) + v
    return tidy(out)


def scale(f, c):
    return tidy({k: v*c for k, v in f.items()})


def mul(f, g):
    out = {}
    for (a, b), x in f.items():
        for (c, d), y in g.items():
            out[a+c, b+d] = out.get((a+c, b+d), F(0)) + x*y
    return tidy(out)


def power(f, n):
    out = {(0, 0): F(1)}
    for _ in range(n):
        out = mul(out, f)
    return out


def derivative(f, a=0, b=0):
    out = {}
    for (i, j), c in f.items():
        if i >= a and j >= b:
            out[i-a, j-b] = c*(factorial(i)//factorial(i-a))*(factorial(j)//factorial(j-b))
    return tidy(out)


def d(f, lam):
    return add(scale(mul({(0, 2): F(1)}, derivative(f, 1)), -3),
               scale(mul({(1, 0): F(1)}, derivative(f, 0, 1)), 2*lam))


def c3(f):
    return add(scale(derivative(f, 3), -6),
               scale(mul({(0, 1): F(1)}, derivative(f, 1, 2)), -36),
               scale(derivative(f, 1, 1), -36))


def c5(f):
    return scale(derivative(f, 1, 4), -360)


def pullback(f):
    """f(q,P) evaluated at P=p+q^2, by the binomial formula."""
    out = {}
    for (a, b), c in f.items():
        for j in range(b+1):
            k = a+2*(b-j), j
            out[k] = out.get(k, F(0)) + c*comb(b, j)
    return tidy(out)


def original_gate(h, f, k):
    """Direct mixed derivatives, independent of the transformed formulas."""
    return add(*(scale(mul(derivative(h, k-j, j), derivative(f, j, k-j)),
                       (-1)**j*comb(k, j)) for j in range(k+1)))


def rref(rows, ncols):
    rows = [list(map(F, row)) for row in rows]
    rank = 0
    pivots = []
    for j in range(ncols):
        p = next((i for i in range(rank, len(rows)) if rows[i][j]), None)
        if p is None:
            continue
        rows[rank], rows[p] = rows[p], rows[rank]
        divisor = rows[rank][j]
        rows[rank] = [x/divisor for x in rows[rank]]
        for i, row in enumerate(rows):
            if i != rank and row[j]:
                factor = row[j]
                rows[i] = [x-factor*y for x, y in zip(row, rows[rank])]
        pivots.append(j)
        rank += 1
        if rank == len(rows):
            break
    return rows[:rank], pivots


def null_basis(rows, ncols):
    reduced, pivots = rref(rows, ncols)
    out = []
    for free in range(ncols):
        if free not in pivots:
            v = [F(0)]*ncols
            v[free] = F(1)
            for row, pivot in zip(reduced, pivots):
                v[pivot] = -row[free]
            out.append(v)
    return out


def encode(f):
    return [[i, j, str(v)] for (i, j), v in sorted(f.items())]


def combine(basis, coeffs):
    return add(*(scale(f, c) for f, c in zip(basis, coeffs)))


def finite_depths(lam, bound=12, both=False):
    """Exact full-output matrices in a declared weighted input space."""
    basis = [{(a, b): F(1)} for b in range(bound//2+1)
             for a in range(bound-2*b+1)]
    images = [{} for _ in basis]
    cur = list(basis)
    rows = []
    for depth in range(4):
        for column, f in zip(images, cur):
            for k, gate in ((3, c3), (5, c5)) if both else ((3, c3),):
                for monomial, value in gate(f).items():
                    column[depth, k, monomial] = value
        keys = sorted({k for column in images for k in column})
        matrix = [[column.get(k, F(0)) for column in images] for k in keys]
        vectors = null_basis(matrix, len(basis))
        kernel = [combine(basis, v) for v in vectors]
        rows.append({'depth': depth, 'dimension': len(vectors),
                     'input_monomials': len(basis),
                     'full_output_coordinates': len(keys),
                     'output_projection': False,
                     'basis': [encode(f) for f in kernel]})
        cur = [d(f, lam) for f in cur]
    expected = [4, 3, 2] if lam else [bound//2+2]*3
    assert [r['dimension'] for r in rows[1:]] == expected
    h = {(0, 3): F(1), (2, 0): lam}
    if lam:
        assert len(kernel) == 2 and not c3(h) and not d(h, lam)
    return {'lambda': str(lam), 'weight': [1, 2], 'weighted_input_bound': bound,
            'gates': [3, 5] if both else [3], 'stages': rows}


def static_basis(n):
    """The q-dependent joint-static harmonic W_n, 1<=n<=8."""
    return {(n-2*j, j): F((-1)**j*factorial(n),
                           factorial(n-2*j)*6**j*factorial(j)**2)
            for j in range(min(3, (n-1)//2)+1)}


def verify():
    grid = 0
    for lam in (F(0), F(1), F(-2), F(1, 3)):
        h = {(0, 3): F(1), (2, 0): lam}
        original_h = pullback(h)
        for b in range(7):
            for a in range(7):
                f = {(a, b): F(1)}
                original_f = pullback(f)
                for k, expected in ((1, d(f, lam)), (3, c3(f)), (5, c5(f))):
                    assert original_gate(original_h, original_f, k) == pullback(expected)
                    grid += 1
    for n in range(1, 9):
        w = static_basis(n)
        assert not c3(w) and not c5(w)
        comm = add(c3(d(w, F(0))), scale(d(c3(w), F(0)), -1))
        expected = scale(mul({(0, 1): F(1)},
                             derivative(add(w, mul({(0, 1): F(1)}, derivative(w, 0, 1))), 2)), 432)
        assert comm == expected
    q, p = {(1, 0): F(1)}, {(0, 1): F(1)}
    q_squared = {(2, 0): F(1)}
    assert not c3(q_squared)
    assert c3(d(q_squared, F(0))) == {(0, 1): F(864)}
    sharp = []
    for lam in (F(1), F(-2), F(1, 3)):
        cur = p
        for depth in range(4):
            expected = {(0, 0): 864*lam**2} if depth == 3 else {}
            assert c3(cur) == expected
            cur = d(cur, lam)
        assert c3(d(d(q, lam), lam)) == {(0, 0): 432*lam}
        sharp.append({'lambda': str(lam), 'witness': 'P',
                      'first_failing_depth': 3, 'C3D3P': str(864*lam**2)})
    phases = [finite_depths(lam) for lam in (F(0), F(1), F(-2), F(1, 3))]
    phases.append(finite_depths(F(1), both=True))
    return {'status': 'passed', 'format': 'cubic-restoring-core-v1',
            'theorem': 'lambda nonzero: full core span{1,H}, sharp third-gate depth three; lambda zero: K[P]+Kq, sharp depth one',
            'direct_original_operator_checks': grid, 'joint_static_basis_checks': 8,
            'sharp_depth_checks': sharp, 'finite_replays': phases,
            'scope': 'Universal conclusions use the written highest-q-degree proof; matrices retain all output coordinates and provide exact finite regression checks.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = verify()
    if args.output:
        args.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
