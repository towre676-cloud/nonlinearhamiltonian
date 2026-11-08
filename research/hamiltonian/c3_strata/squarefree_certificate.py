"""Produce exact discriminant-in-determinantal-ideal certificates over QQ.

Uses the maintained falling-factorial gate builder. Replay uses independent
literal differentiation in verify_squarefree.py and no Groebner-basis engine.
Run from any directory: python squarefree_certificate.py [--output PATH].
"""
from __future__ import annotations

import argparse
from itertools import combinations
import json
from pathlib import Path

import sympy as s
from sympy.polys.domains import QQ
from sympy.polys.rings import ring

from explore import mat

A, B, C, E = s.symbols('a b c d')
VARIABLES = (A, B, C, E)
P, *RING_VARIABLES = ring('a,b,c,d', QQ, order='grevlex')
H = {(1, 5): 1, (3, 3): A, (4, 2): B, (5, 1): C, (6, 0): E}
HERE = Path(__file__).resolve().parent
BASE = 'b17ff8568ff81067274e87486ced2a397f2a53e3'

# Rows discovered by exact elimination of the two leading partner coefficients.
# These are indices into the sorted nonzero row keys of the full gate matrix.
ROW_SELECTION = {
    1: [0, 1, 2, 3, 4, 6, 7], 2: [1, 2, 3, 4, 7, 8],
    3: [2, 3, 4, 5, 8], 4: [1, 3, 4, 5, 7, 8],
    5: [4, 6, 7, 8, 9], 6: [2, 8, 10, 11],
    7: [8, 9, 10, 12, 13], 8: [3, 9, 11, 14, 15, 16],
    9: [10, 11, 12, 16, 17], 10: [4, 11, 12, 18, 19],
    11: [12, 13, 14, 20, 21], 12: [13, 14, 22, 23, 26],
    13: [14, 15, 16, 24, 25], 14: [15, 16, 17, 26, 27, 29],
    15: [16, 17, 18, 28, 29], 16: [17, 18, 19, 30, 31],
}


def pack(poly):
    """Sparse rational polynomial; never serialize executable expressions."""
    if not hasattr(poly, 'ring'):
        poly = P.from_expr(poly)
    return [[list(exponents), str(coefficient)]
            for exponents, coefficient in sorted(poly.items()) if coefficient]


def reduction(n):
    keys, matrix = mat(H, n)
    lift = [s.Matrix([[1, 0]]), s.Matrix([[0, 1]])]
    pivots = []
    for j in range(2, n + 1):
        depth = int(n - 2*j + 2 == 0)
        key = (depth, 3, j-2, n + 4*depth - j + 2)
        row = keys.index(key)
        pivot = matrix[row, j]
        if not pivot.is_Rational or not pivot:
            raise ArithmeticError('nonconstant or zero pivot')
        if any(matrix[row, k] for k in range(j+1, n+1)):
            raise ArithmeticError('pivot submatrix is not triangular')
        value = -sum((matrix[row, k]*lift[k] for k in range(j)),
                     s.zeros(1, 2))/pivot
        lift.append(value.applyfunc(s.expand))
        pivots.append(row)
    lift = s.Matrix.vstack(*lift)
    residual = (matrix*lift).applyfunc(s.expand)
    return keys, matrix, lift, residual, pivots


def membership(generators, target):
    """Discover a finite ideal-membership straight-line proof.

    Division and S-polynomials are only discovery operations. Every retained
    node carries its explicit polynomial identity in earlier nodes; the
    verifier neither trusts nor reexecutes this search.
    """
    polynomials = [P.from_expr(x) for x in generators]
    nodes, basis, pairs = [], [], set()
    target = P.from_expr(target)

    def finish():
        if not basis:
            return None
        quotients, remainder = target.div([polynomials[i] for i in basis])
        if remainder:
            return None
        return [(i, q) for i, q in zip(basis, quotients) if q]

    def append(poly, terms):
        quotients, remainder = poly.div([polynomials[j] for j in basis])
        if not remainder:
            return
        leading = remainder.LC
        terms = terms.copy()
        for j, quotient in zip(basis, quotients):
            if quotient:
                terms[j] = terms.get(j, P.zero) - quotient
        terms = {j: q/leading for j, q in terms.items() if q}
        remainder = remainder.monic()
        if remainder != sum((q*polynomials[j] for j, q in terms.items()), P.zero):
            raise ArithmeticError('discovery identity failed')
        index = len(polynomials)
        polynomials.append(remainder)
        nodes.append({'polynomial': pack(remainder),
                      'terms': [[j, pack(q)] for j, q in sorted(terms.items())]})
        for j in basis:
            if P.monomial_mul(remainder.LM, polynomials[j].LM) != P.monomial_lcm(remainder.LM, polynomials[j].LM):
                pairs.add((j, index))
        basis.append(index)

    order = sorted((j for j, poly in enumerate(polynomials) if poly),
                   key=lambda j: (P.order(polynomials[j].LM), j))
    for i in order:
        append(polynomials[i], {i: P.one})
        identity = finish()
        if identity is not None:
            return nodes, [[j, pack(q)] for j, q in identity]
    while pairs:
        i, j = min(pairs, key=lambda ij: (
            P.order(P.monomial_lcm(polynomials[ij[0]].LM, polynomials[ij[1]].LM)), ij))
        pairs.remove((i, j))
        lcm = P.monomial_lcm(polynomials[i].LM, polynomials[j].LM)
        u = P.from_dict({P.monomial_div(lcm, polynomials[i].LM): QQ.one})
        v = P.from_dict({P.monomial_div(lcm, polynomials[j].LM): QQ.one})
        append(u*polynomials[i]-v*polynomials[j], {i: u, j: -v})
        identity = finish()
        if identity is not None:
            return nodes, [[j, pack(q)] for j, q in identity]
    raise ArithmeticError('discriminant membership was not found')


def produce():
    x = s.Symbol('x')
    discriminant = s.discriminant(x**5+A*x**3+B*x**2+C*x+E, x)
    records = []
    for n in range(1, 17):
        keys, matrix, lift, residual, pivots = reduction(n)
        rows = ROW_SELECTION[n]
        minors = [[i] for i in rows] if n == 6 else list(map(list, combinations(rows, 2)))
        generators = [residual[i[0], 0] if n == 6 else
                      s.expand(residual[i[0], 0]*residual[i[1], 1]
                               - residual[i[0], 1]*residual[i[1], 0]) for i in minors]
        nodes, identity = membership(generators, discriminant)
        records.append({
            'n': n, 'row_keys': list(map(list, keys)), 'pivot_rows': pivots,
            'kernel_lift': [[pack(lift[j, k]) for k in range(2)] for j in range(n+1)],
            'minor_rows': minors, 'derived': nodes, 'discriminant_identity': identity,
        })
        print(f'degree {n}: {len(minors)} selected minors, {len(nodes)} derivation nodes', flush=True)
    return {'format': 'squarefree-sextic-discriminant-v1', 'base_commit': BASE,
            'variables': ['a', 'b', 'c', 'd'],
            'normal_form': 'q*p**5+a*q**3*p**3+b*q**4*p**2+c*q**5*p+d*q**6',
            'discriminant': pack(discriminant), 'records': records}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=HERE/'squarefree_certificate.json')
    args = parser.parse_args()
    args.output.write_text(json.dumps(produce(), indent=2)+'\n', encoding='utf-8')
