#!/usr/bin/env python3
"""Construct exact rational contractions and solve a cocycle, with checkable witnesses."""
import argparse
import json
import sys
from fractions import Fraction as F
from pathlib import Path
from check_contraction import Matrix, zero, eye, mul, pack, unpack, read_model, model_hash, verify


def rref(m):
    a, pivots, row = [x[:] for x in m.a], [], 0
    for col in range(m.c):
        pivot = next((j for j in range(row, m.r) if a[j][col]), None)
        if pivot is None:
            continue
        a[row], a[pivot] = a[pivot], a[row]
        value = a[row][col]
        a[row] = [x / value for x in a[row]]
        for j in range(m.r):
            if j != row:
                value = a[j][col]
                a[j] = [x - value * y for x, y in zip(a[j], a[row])]
        pivots.append(col)
        row += 1
        if row == m.r:
            break
    return Matrix(m.r, m.c, a), pivots


def columns(m):
    return [[m.a[i][j] for i in range(m.r)] for j in range(m.c)]


def from_columns(rows, cols):
    return Matrix(rows, len(cols), [[col[i] for col in cols] for i in range(rows)])


def nullspace(m):
    reduced, pivots = rref(m)
    result = []
    for free in range(m.c):
        if free not in pivots:
            vector = [F(0)] * m.c
            vector[free] = F(1)
            for row, pivot in enumerate(pivots):
                vector[pivot] = -reduced.a[row][free]
            result.append(vector)
    return result


def inverse(m):
    if m.r != m.c:
        raise ValueError('inverse needs a square matrix')
    e = eye(m.r)
    reduced, pivots = rref(Matrix(m.r, 2 * m.c, [a + b for a, b in zip(m.a, e.a)]))
    if pivots[:m.r] != list(range(m.r)):
        raise ValueError('singular basis matrix')
    return Matrix(m.r, m.c, [row[m.c:] for row in reduced.a])


def build(model):
    n, d = read_model(model)
    all_d = d + [zero(0, n[-1])]
    boundaries, representatives, complements, bases = [], [], [], []
    for j, size in enumerate(n):
        prev = d[j - 1] if j else zero(size, 0)
        _, previous_pivots = rref(prev)
        b = [columns(prev)[k] for k in previous_pivots]
        span, h = b[:], []
        for vector in nullspace(all_d[j]):
            candidate = span + [vector]
            if len(rref(from_columns(size, candidate))[1]) > len(span):
                span, h = candidate, h + [vector]
        _, pivots = rref(all_d[j])
        l = [columns(eye(size))[k] for k in pivots]
        boundaries.append(b)
        representatives.append(h)
        complements.append(l)
        bases.append(inverse(from_columns(size, b + h + l)))
    certificate = {'schema': 'rational-contraction-v1', 'field': 'Q',
                   'model_sha256': model_hash(model),
                   'cohomology_dimensions': [len(x) for x in representatives],
                   'i': [], 'p': [], 'h': []}
    for j, size in enumerate(n):
        nb, nh = len(boundaries[j]), len(representatives[j])
        certificate['i'].append(pack(from_columns(size, representatives[j])))
        certificate['p'].append(pack(Matrix(nh, size, bases[j].a[nb:nb + nh])))
        h = zero(0, size) if not j else mul(from_columns(n[j - 1], complements[j - 1]),
                                          Matrix(nb, size, bases[j].a[:nb]))
        certificate['h'].append(pack(h))
    verify(model, certificate)
    return certificate


def solve(model, certificate, degree, vector):
    verify(model, certificate)
    n, d = read_model(model)
    if type(degree) is not int or not 0 <= degree < len(n):
        raise ValueError('degree outside supplied complex')
    if not isinstance(vector, (list, tuple)):
        raise ValueError('cocycle must be an array of exact coefficients')
    b = Matrix(n[degree], 1, [[x] for x in vector])
    if degree < len(d):
        db = mul(d[degree], b)
        if any(x[0] for x in db.a):
            return {'status': 'not_cocycle', 'field': 'Q', 'd_b': pack(db)}
    p = unpack(certificate['p'][degree])
    obstruction = mul(p, b)
    witness = next((j for j, row in enumerate(obstruction.a) if row[0]), None)
    if witness is None:
        return {'status': 'solved', 'field': 'Q', 'primitive': pack(mul(unpack(certificate['h'][degree]), b))}
    row = Matrix(1, p.c, [p.a[witness]])
    return {'status': 'obstructed', 'field': 'Q', 'class_coordinates': pack(obstruction),
            'separating_functional': pack(row), 'nonzero_pairing': pack(mul(row, b))}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('model', type=Path)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--degree', type=int)
    parser.add_argument('--cocycle', help='JSON vector of integers or rational strings')
    args = parser.parse_args()
    model = json.loads(args.model.read_text())
    certificate = build(model)
    if args.output:
        args.output.write_text(json.dumps(certificate, indent=2) + '\n')
    result = verify(model, certificate)
    if args.cocycle is not None:
        if args.degree is None:
            parser.error('--cocycle requires --degree')
        result = solve(model, certificate, args.degree, json.loads(args.cocycle))
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, KeyError, TypeError, ZeroDivisionError) as error:
        print(json.dumps({'status': 'invalid_model_or_certificate', 'reason': str(error)}))
        sys.exit(2)
