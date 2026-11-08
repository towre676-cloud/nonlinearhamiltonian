"""Independent, fail-closed replay of squarefree sextic certificates.

Rebuilds all four gates by literal differentiation. Checks the triangular
kernel reconstruction, explicit determinantal identities, and discriminant
membership. Imports neither the producer nor explore.py; uses no Groebner
basis, modular rank, floating point, or nonzero-minor sampling.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import json
from pathlib import Path
import sympy as s

q, p, a, b, c, d = s.symbols('q p a b c d')
VARIABLES = (a, b, c, d)
H = q*p**5+a*q**3*p**3+b*q**4*p**2+c*q**5*p+d*q**6
HERE = Path(__file__).resolve().parent


class CertificateError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise CertificateError(message)


def unpack(data):
    require(isinstance(data, list), 'polynomial must be a sparse list')
    out, seen = s.S.Zero, set()
    for term in data:
        require(isinstance(term, list) and len(term) == 2, 'invalid monomial')
        exponents, coefficient = term
        require(isinstance(exponents, list) and len(exponents) == 4
                and all(type(e) is int and e >= 0 for e in exponents), 'invalid exponents')
        exponents = tuple(exponents)
        require(exponents not in seen, 'duplicate monomial')
        seen.add(exponents)
        require(isinstance(coefficient, str), 'coefficient must be rational text')
        try:
            coefficient = Fraction(coefficient)
        except (ValueError, ZeroDivisionError) as exc:
            raise CertificateError('invalid rational coefficient') from exc
        require(coefficient != 0, 'zero coefficient must be omitted')
        out += s.Rational(coefficient.numerator, coefficient.denominator)*s.prod(
            x**e for x, e in zip(VARIABLES, exponents))
    return out


def transvectant(f, g, k):
    return s.expand(sum((-1)**j*s.binomial(k, j)
                        *s.diff(f, q, k-j, p, j)*s.diff(g, q, j, p, k-j)
                        for j in range(k+1)))


def literal_matrix(n, hamiltonian=H):
    columns = []
    for j in range(n+1):
        g = q**j*p**(n-j)
        column = {}
        for depth, f in [(0, g), (1, transvectant(hamiltonian, g, 1))]:
            for k in (3, 5):
                for (u, v), value in s.Poly(transvectant(hamiltonian, f, k), q, p).terms():
                    if value:
                        column[(depth, k, u, v)] = value
        columns.append(column)
    keys = sorted(set().union(*(set(column) for column in columns)))
    return keys, s.Matrix([[column.get(key, 0) for column in columns] for key in keys])


def combine(terms, polynomials):
    require(isinstance(terms, list) and terms, 'empty identity')
    result, seen = s.S.Zero, set()
    for term in terms:
        require(isinstance(term, list) and len(term) == 2, 'invalid identity term')
        index, coefficient = term
        require(type(index) is int and 0 <= index < len(polynomials), 'invalid or forward reference')
        require(index not in seen, 'duplicate identity reference')
        seen.add(index)
        result += unpack(coefficient)*polynomials[index]
    return s.expand(result)


def verify_record(record, discriminant):
    n = record['n']
    require(type(n) is int and 1 <= n <= 16, 'invalid degree')
    keys, matrix = literal_matrix(n)
    require(record['row_keys'] == list(map(list, keys)), 'row-key mismatch')
    data = record['kernel_lift']
    require(len(data) == n+1 and all(len(row) == 2 for row in data), 'kernel-lift dimensions')
    lift = s.Matrix([[unpack(value) for value in row] for row in data])
    require(lift[:2, :] == s.eye(2), 'wrong leading partner coordinates')
    expected_pivots = [keys.index((int(n-2*j+2 == 0), 3, j-2,
                                  n+4*int(n-2*j+2 == 0)-j+2)) for j in range(2, n+1)]
    require(record['pivot_rows'] == expected_pivots, 'wrong pivot coverage')
    for j, row in zip(range(2, n+1), expected_pivots):
        pivot = matrix[row, j]
        require(pivot.is_Rational and pivot != 0, 'pivot is not a nonzero rational constant')
        require(all(matrix[row, k] == 0 for k in range(j+1, n+1)), 'nontriangular pivots')
    residual = (matrix*lift).applyfunc(s.expand)
    require(all(residual[row, k] == 0 for row in expected_pivots for k in range(2)),
            'kernel reconstruction does not kill the pivot equations')
    if n == 6:
        coefficients = s.Matrix([s.expand(H).coeff(q, j).coeff(p, 6-j) for j in range(7)])
        require(lift[:, 1] == coefficients and residual[:, 1] == s.zeros(matrix.rows, 1),
                'degree-six core is not precisely H')
    polynomials = []
    require(record['minor_rows'], 'no determinantal generators')
    seen = set()
    for rows in record['minor_rows']:
        require(len(rows) == (1 if n == 6 else 2), 'wrong minor order')
        require(all(type(i) is int and 0 <= i < matrix.rows for i in rows), 'invalid minor row')
        require(rows == sorted(set(rows)) and tuple(rows) not in seen, 'duplicate minor')
        seen.add(tuple(rows))
        if n == 6:
            polynomials.append(residual[rows[0], 0])
        else:
            i, j = rows
            polynomials.append(s.expand(residual[i, 0]*residual[j, 1]-residual[i, 1]*residual[j, 0]))
    for node in record['derived']:
        value = unpack(node['polynomial'])
        require(s.expand(combine(node['terms'], polynomials)-value) == 0,
                f'degree {n}: false ideal-membership step')
        polynomials.append(value)
    require(s.expand(combine(record['discriminant_identity'], polynomials)-discriminant) == 0,
            f'degree {n}: false discriminant identity')
    return {'n': n, 'matrix_rows': matrix.rows, 'matrix_columns': matrix.cols,
            'pivots': n-1, 'minor_order': 1 if n == 6 else 2,
            'selected_minors': len(record['minor_rows']), 'derived_identities': len(record['derived'])}


def verify(data=None, progress=True):
    if data is None:
        data = json.loads((HERE/'squarefree_certificate.json').read_text(encoding='utf-8'))
    require(data['format'] == 'squarefree-sextic-discriminant-v1', 'wrong certificate format')
    require(data['variables'] == ['a', 'b', 'c', 'd'], 'wrong variable order')
    require(data['normal_form'] == 'q*p**5+a*q**3*p**3+b*q**4*p**2+c*q**5*p+d*q**6',
            'wrong Hamiltonian')
    require([r['n'] for r in data['records']] == list(range(1, 17)), 'missing or duplicate degree')
    x = s.Symbol('x')
    discriminant = s.discriminant(x**5+a*x**3+b*x**2+c*x+d, x)
    require(s.expand(unpack(data['discriminant'])-discriminant) == 0, 'wrong discriminant')
    records = []
    for record in data['records']:
        result = verify_record(record, discriminant)
        records.append(result)
        if progress:
            print(f"degree {record['n']}: exact discriminant membership PASS", flush=True)
    return {'status': 'PASS', 'field': 'Q', 'degrees': 16,
            'selected_minors': sum(r['selected_minors'] for r in records),
            'derived_identities': sum(r['derived_identities'] for r in records),
            'discriminant_power': 1, 'records': records,
            'scope': 'All squarefree sextics in degrees 1..16; all-degree conclusion uses inherited static tail.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('certificate', type=Path, nargs='?', default=HERE/'squarefree_certificate.json')
    parser.add_argument('--receipt', type=Path)
    args = parser.parse_args()
    result = verify(json.loads(args.certificate.read_text(encoding='utf-8')))
    if args.receipt:
        args.receipt.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in result.items() if k != 'records'}, indent=2))
