#!/usr/bin/env python3
"""Small exact Q-certificate checker. It does not import the constructor."""
from fractions import Fraction as F
import hashlib
import json
import sys


class Matrix:
    def __init__(self, rows, cols, entries):
        if type(rows) is not int or type(cols) is not int or min(rows, cols) < 0:
            raise ValueError('invalid matrix dimensions')
        if not isinstance(entries, (list, tuple)) or any(not isinstance(row, (list, tuple)) for row in entries):
            raise ValueError('matrix entries must be an array of row arrays')
        if len(entries) != rows or any(len(row) != cols for row in entries):
            raise ValueError('matrix shape mismatch')
        if any(type(x) not in (int, str, F) for row in entries for x in row):
            raise ValueError('coefficients must be exact integers or rational strings')
        self.r, self.c = rows, cols
        self.a = [[F(x) for x in row] for row in entries]


def zero(r, c):
    return Matrix(r, c, [[0] * c for _ in range(r)])


def eye(n):
    return Matrix(n, n, [[int(i == j) for j in range(n)] for i in range(n)])


def mul(a, b):
    if a.c != b.r:
        raise ValueError('matrix product shape mismatch')
    return Matrix(a.r, b.c, [[sum((a.a[i][k] * b.a[k][j] for k in range(a.c)), F(0))
                             for j in range(b.c)] for i in range(a.r)])


def add(a, b, sign=1):
    if (a.r, a.c) != (b.r, b.c):
        raise ValueError('matrix sum shape mismatch')
    return Matrix(a.r, a.c, [[a.a[i][j] + sign * b.a[i][j]
                             for j in range(a.c)] for i in range(a.r)])


def same(a, b):
    return (a.r, a.c, a.a) == (b.r, b.c, b.a)


def pack(a):
    return {'rows': a.r, 'cols': a.c, 'entries': [[str(x) for x in row] for row in a.a]}


def unpack(x):
    return Matrix(x['rows'], x['cols'], x['entries'])


def model_hash(model):
    return hashlib.sha256(json.dumps(model, sort_keys=True, separators=(',', ':'),
                                     ensure_ascii=False).encode()).hexdigest()


def read_model(model):
    if model.get('field') != 'Q':
        raise ValueError('this seed requires field Q; integral torsion is outside its scope')
    n = model['dimensions']
    if not n or any(type(x) is not int or x < 0 for x in n):
        raise ValueError('invalid complex dimensions')
    if len(model['differentials']) != len(n) - 1:
        raise ValueError('wrong number of differentials')
    d = [Matrix(n[j + 1], n[j], x) for j, x in enumerate(model['differentials'])]
    for j in range(len(d) - 1):
        product = mul(d[j + 1], d[j])
        witness = next(((r, c, x) for r, row in enumerate(product.a)
                        for c, x in enumerate(row) if x), None)
        if witness:
            raise ValueError('invalid complex: d^2 != 0 at degree ' + str(j)
                             + ', entry ' + str(witness[:2]) + ' = ' + str(witness[2]))
    return n, d


def verify(model, certificate):
    n, d = read_model(model)
    if certificate.get('schema') != 'rational-contraction-v1':
        raise ValueError('unsupported certificate schema')
    if certificate.get('field') != 'Q':
        raise ValueError('certificate coefficient field must be Q')
    if certificate.get('model_sha256') != model_hash(model):
        raise ValueError('certificate belongs to another exact model')
    hdim = certificate['cohomology_dimensions']
    if len(hdim) != len(n) or any(type(x) is not int or x < 0 for x in hdim):
        raise ValueError('invalid cohomology dimensions')
    maps = {key: [unpack(x) for x in certificate[key]] for key in ('i', 'p', 'h')}
    if any(len(x) != len(n) for x in maps.values()):
        raise ValueError('wrong number of certificate maps')
    checks = 0
    for j, size in enumerate(n):
        i, p, h = (maps[key][j] for key in ('i', 'p', 'h'))
        shapes = [(i.r, i.c), (p.r, p.c), (h.r, h.c)]
        if shapes != [(size, hdim[j]), (hdim[j], size), (n[j - 1] if j else 0, size)]:
            raise ValueError('map shape mismatch at degree ' + str(j))
        tests = [('pi', mul(p, i), eye(hdim[j]))]
        if j < len(d):
            tests.append(('di', mul(d[j], i), zero(n[j + 1], hdim[j])))
        if j:
            tests.append(('pd', mul(p, d[j - 1]), zero(hdim[j], n[j - 1])))
        dh = mul(d[j - 1], h) if j else zero(size, size)
        hd = mul(maps['h'][j + 1], d[j]) if j < len(d) else zero(size, size)
        tests.append(('homotopy', add(eye(size), mul(i, p), -1), add(dh, hd)))
        for label, lhs, rhs in tests:
            if not same(lhs, rhs):
                raise ValueError(label + ' certificate fails at degree ' + str(j))
            checks += 1
    return {'status': 'passed', 'field': 'Q', 'cohomology_dimensions': hdim,
            'exact_identity_checks': checks,
            'scope': 'Rational cohomology only; no integral torsion or nonlinear bracket claim.'}


if __name__ == '__main__':
    try:
        model = json.load(open(sys.argv[1], encoding='utf-8'))
        certificate = json.load(open(sys.argv[2], encoding='utf-8'))
        print(json.dumps(verify(model, certificate), indent=2))
    except (ValueError, KeyError, IndexError, TypeError, ZeroDivisionError) as error:
        print(json.dumps({'status': 'rejected', 'reason': str(error)}))
        sys.exit(2)
