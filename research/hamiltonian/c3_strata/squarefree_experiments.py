"""Optional exact elimination and modular diagnostics; not theorem dependencies.

The proof is squarefree_certificate.json + verify_squarefree.py. This file
records the discovery geometry in 46 partner charts and seeded finite-field
checks of the full, unreduced gate matrices. Modular data assert no statement
about characteristic zero.
"""
import argparse
import json
from pathlib import Path
import random
import sympy as s
from squarefree_certificate import VARIABLES, reduction, pack

a, b, c, d = VARIABLES


def rank_mod(matrix, prime):
    matrix = [row[:] for row in matrix]
    rank = 0
    for col in range(len(matrix[0])):
        pivot = next((r for r in range(rank, len(matrix)) if matrix[r][col] % prime), None)
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        inv = pow(matrix[rank][col] % prime, -1, prime)
        matrix[rank] = [(v*inv) % prime for v in matrix[rank]]
        for r in range(rank+1, len(matrix)):
            factor = matrix[r][col] % prime
            if factor:
                matrix[r] = [(x-factor*y) % prime for x, y in zip(matrix[r], matrix[rank])]
        rank += 1
        if rank == len(matrix):
            break
    return rank


def terms(expression):
    return [(exponents, int(coefficient)) for exponents, coefficient
            in s.Poly(expression, *VARIABLES, domain=s.ZZ).terms() if coefficient]


def evaluate(polynomial, point, prime):
    return sum(coefficient*s.prod(pow(x, e, prime) for x, e in zip(point, exponents))
               for exponents, coefficient in polynomial) % prime


def run():
    x = s.Symbol('x')
    delta = s.discriminant(x**5+a*x**3+b*x**2+c*x+d, x)
    deltat = terms(delta)
    charts, matrices = [], []
    for n in range(1, 17):
        _, matrix, _, residual, _ = reduction(n)
        matrices.append([[terms(value) for value in row] for row in matrix.tolist()])
        for chart in (['A'] if n == 6 else ['A', 'B', 'A+B']):
            generators = [row[0] if chart == 'A' else row[1] if chart == 'B' else sum(row)
                          for row in residual.tolist()]
            generators = list(dict.fromkeys(s.Poly(g, *VARIABLES, domain=s.QQ).monic().as_expr()
                                             for g in generators if g != 0))
            basis = s.groebner(generators, *VARIABLES, order='grevlex')
            if basis.reduce(delta)[1] != 0:
                raise ArithmeticError('chart discriminant membership failed')
            charts.append({'n': n, 'chart': chart,
                           'groebner_basis': [pack(poly.as_expr()) for poly in basis.polys],
                           'discriminant_remainder': []})
        print(f'exact partner charts: degree {n}', flush=True)
    rng = random.Random(20261108)
    samples, defects = [], []
    for prime in (101, 103):
        accepted = 0
        while accepted < 64:
            point = [rng.randrange(prime) for _ in range(4)]
            if not evaluate(deltat, point, prime):
                continue
            accepted += 1
            ranks = []
            for n, matrix in enumerate(matrices, 1):
                evaluated = [[int(evaluate(value, point, prime)) for value in row] for row in matrix]
                rank = rank_mod(evaluated, prime)
                ranks.append(rank)
                if rank != (6 if n == 6 else n+1):
                    defects.append({'prime': prime, 'point': point, 'n': n, 'rank': rank})
            samples.append({'prime': prime, 'point': point, 'ranks': ranks})
        print(f'modular diagnostics: 64 squarefree forms over F_{prime}', flush=True)
    return {'scope': 'Discovery/diagnostics only. Characteristic-zero theorem uses independent identity replay.',
            'seed': 20261108, 'exact_charts': charts, 'samples': samples,
            'modular_forms': len(samples), 'modular_gate_ranks': 16*len(samples),
            'modular_rank_defects': defects}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=Path(__file__).with_name('squarefree_experiments.json'))
    args = parser.parse_args()
    args.output.write_text(json.dumps(run(), indent=2)+'\n', encoding='utf-8')
