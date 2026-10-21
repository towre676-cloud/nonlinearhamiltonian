#!/usr/bin/env python3
"""Finite rational obstruction compiler (S1): primitive, obstruction witness or invalid model.

Stable interface over the contraction seed for arbitrary bounded finite complexes over Q:

  solve(model, degree, cocycle, max_size=...) ->
    {'status': 'solved',     'primitive': u}          with d_(k-1) u = b
    {'status': 'obstructed', 'functional': f}         with f d_(k-1) = 0 and f b != 0
    {'status': 'not_cocycle','d_b': d_k b}
    {'status': 'invalid_model', 'reason': ...}        e.g. d^2 != 0, field Z, floats
    {'status': 'unknown', 'reason': ...}              declared size budget exceeded

Each answer carries the contraction certificate it was derived from, and every
answer is replayed by `check_answer`, which needs only matrix products: a solved
answer is an explicit primitive, an obstructed answer is a functional vanishing on
all boundaries but not on b. Coefficients are Q only: a rational answer says nothing
about integral torsion (multiplication by 2 on Z is the standing counterexample).

Usage: obstruction.py MODEL.json --degree K --cocycle '[...]' [--max-size N]
"""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from check_contraction import Matrix, mul, pack, unpack, read_model, verify  # noqa: E402
from contraction_seed import build  # noqa: E402

SCHEMA = 'rational-obstruction-answer-v1'


def solve(model, degree, cocycle, max_size=400):
    try:
        n, d = read_model(model)
    except (ValueError, KeyError, TypeError) as e:
        return {'schema': SCHEMA, 'status': 'invalid_model', 'reason': str(e)}
    total = sum(n)
    if total > max_size:
        return {'schema': SCHEMA, 'status': 'unknown',
                'reason': f'total dimension {total} exceeds declared budget {max_size}', 'resources': {'size': total}}
    try:
        cert = build(model)
        answer = _solve(model, cert, n, d, degree, cocycle)
    except (ValueError, KeyError, TypeError) as e:
        return {'schema': SCHEMA, 'status': 'invalid_model', 'reason': str(e)}
    answer.update(schema=SCHEMA, field='Q', degree=degree, cocycle=[str(x) for x in cocycle],
                  contraction=cert, resources={'size': total})
    check_answer(model, answer)
    return answer


def _solve(model, cert, n, d, degree, cocycle):
    if type(degree) is not int or not 0 <= degree < len(n):
        raise ValueError('degree outside supplied complex')
    if not isinstance(cocycle, list) or len(cocycle) != n[degree]:
        raise ValueError('cocycle has the wrong length')
    b = Matrix(n[degree], 1, [[x] for x in cocycle])
    if degree < len(d):
        db = mul(d[degree], b)
        if any(r[0] for r in db.a):
            return {'status': 'not_cocycle', 'd_b': pack(db)}
    p = unpack(cert['p'][degree])
    cls = mul(p, b)
    k = next((i for i, r in enumerate(cls.a) if r[0]), None)
    if k is None:
        return {'status': 'solved', 'primitive': pack(mul(unpack(cert['h'][degree]), b))}
    return {'status': 'obstructed', 'class_coordinates': pack(cls),
            'functional': pack(Matrix(1, p.c, [p.a[k]]))}


def check_answer(model, ans):
    """Replay an answer with matrix products only (plus the contraction identities)."""
    n, d = read_model(model)
    verify(model, ans['contraction'])
    k = ans['degree']
    b = Matrix(n[k], 1, [[x] for x in ans['cocycle']])
    st = ans['status']
    if st == 'not_cocycle':
        if mul(d[k], b).a != unpack(ans['d_b']).a or not any(r[0] for r in unpack(ans['d_b']).a):
            raise ValueError('not_cocycle claim fails')
    elif st == 'solved':
        u = unpack(ans['primitive'])
        if k == 0:
            if any(r[0] for r in b.a):
                raise ValueError('nonzero degree-0 cocycle cannot be a boundary')
        elif mul(d[k - 1], u).a != b.a:
            raise ValueError('primitive does not satisfy d u = b')
    elif st == 'obstructed':
        f = unpack(ans['functional'])
        if k and any(x for x in mul(f, d[k - 1]).a[0]):
            raise ValueError('functional does not vanish on boundaries')
        if not mul(f, b).a[0][0]:
            raise ValueError('functional does not detect the cocycle')
    else:
        raise ValueError('unknown answer status')
    return {'status': 'passed', 'answer': st}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('model', type=Path)
    ap.add_argument('--degree', type=int, required=True)
    ap.add_argument('--cocycle', required=True)
    ap.add_argument('--max-size', type=int, default=400)
    a = ap.parse_args()
    ans = solve(json.loads(a.model.read_text()), a.degree, json.loads(a.cocycle), a.max_size)
    ans.pop('contraction', None)
    print(json.dumps(ans, indent=2))
    sys.exit(0 if ans['status'] in ('solved', 'obstructed', 'not_cocycle') else 2)


if __name__ == '__main__':
    main()
