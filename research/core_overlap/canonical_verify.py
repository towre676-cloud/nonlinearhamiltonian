#!/usr/bin/env python3
"""Exact independent checks for protected nonlinear canonical transport.

Standard-library only. Polynomials use rational coefficients and exponent
triples (q,p,hbar). The star commutator and Jordan product are recomputed
directly from the defining transvectants; no discovery backend is imported.
"""
from fractions import Fraction as F
from math import comb, factorial
from pathlib import Path
import argparse
import json
import random


def clean(a):
    return {k: F(v) for k, v in a.items() if v}


def add(*xs):
    out = {}
    for x in xs:
        for k, v in x.items():
            out[k] = out.get(k, F(0)) + v
    return clean(out)


def scale(a, c):
    return clean({k: F(c)*v for k, v in a.items()})


def mul(a, b):
    out = {}
    for k, x in a.items():
        for ell, y in b.items():
            m = tuple(u+v for u, v in zip(k, ell))
            out[m] = out.get(m, F(0)) + x*y
    return clean(out)


def power(a, n):
    out = {(0, 0, 0): F(1)}
    for _ in range(n):
        out = mul(out, a)
    return out


def der(a, q=0, p=0):
    out = {}
    for (i, j, h), c in a.items():
        if i >= q and j >= p:
            fac = factorial(i)//factorial(i-q)*factorial(j)//factorial(j-p)
            out[i-q, j-p, h] = c*fac
    return clean(out)


def hshift(a, n):
    return {(i, j, h+n): c for (i, j, h), c in a.items()}


def trans(a, b, k):
    return add(*(scale(mul(der(a, k-j, j), der(b, j, k-j)),
                       (-1)**j*comb(k, j)) for j in range(k+1)))


def degree(a):
    return max((i+j for i, j, _ in a), default=-1)


def bracket(a, b):
    return add(*(hshift(scale(trans(a, b, 2*r+1),
                              F((-1)**r, 2**(2*r)*factorial(2*r+1))), 2*r)
                 for r in range((min(degree(a), degree(b))+1)//2)))


def poisson(a, b):
    return trans(a, b, 1)


def jordan(a, b):
    return add(*(hshift(scale(trans(a, b, 2*r),
                              F((-1)**r, 2**(2*r)*factorial(2*r))), 2*r)
                 for r in range(min(degree(a), degree(b))//2+1)))


def antiderivative_q(w):
    return {(i+1, j, h): c/F(i+1) for (i, j, h), c in w.items()}


def classical_shear(a, w):
    out = {}
    for (i, j, h), c in a.items():
        for k in range(j+1):
            mon = {(i, j-k, h): c*comb(j, k)}
            out = add(out, mul(mon, power(w, k)))
    return out


def quantum_shear(a, w):
    u = antiderivative_q(w)
    out, term = a, a
    for n in range(1, max((j for _, j, _ in a), default=0)+1):
        term = bracket(u, term)
        out = add(out, scale(term, F(1, factorial(n))))
    return out


def check_equal(a, b, label):
    if a != b:
        raise AssertionError(label + ': residual=' + str(add(a, scale(b, -1))))


def check_zeros(a, label):
    check_equal(a, {}, label)


def random_poly(rng, max_q, max_p, terms):
    out = {}
    for _ in range(terms):
        key = (rng.randrange(max_q+1), rng.randrange(max_p+1), 0)
        out[key] = out.get(key, F(0)) + F(rng.randrange(-3, 4), rng.randrange(1, 4))
    return clean(out)


def checks():
    rng = random.Random(736019)
    q = {(1, 0, 0): F(1)}
    p = {(0, 1, 0): F(1)}
    one = {(0, 0, 0): F(1)}
    z = mul(q, p)
    counts = {'shear_protection': 0, 'sharp_cubic': 0,
              'quantum_bracket_covariance': 0, 'pure_top_families': 0,
              'pure_family_gate_checks': 0, 'pure_family_iterates': 0,
              'qF_square_cubic': 0, 'qF_hbar2_general': 0}

    for t in range(2, 7):
        w = add(power(q, t), scale(q, F(2, 3)), scale(one, -1))
        for _ in range(6):
            a = random_poly(rng, 4, 2, 7)
            check_equal(quantum_shear(a, w), classical_shear(a, w),
                        'protected shear')
            counts['shear_protection'] += 1
        check_equal(quantum_shear(power(p, 3), w),
                    add(classical_shear(power(p, 3), w),
                        hshift(scale(der(w, q=2), F(-1, 4)), 2)),
                    'sharp cubic')
        counts['sharp_cubic'] += 1

    for _ in range(18):
        w = add(power(q, rng.randrange(2, 5)), q, one)
        a = random_poly(rng, 3, 3, 5)
        b = random_poly(rng, 3, 3, 5)
        check_equal(quantum_shear(bracket(a, b), w),
                    bracket(quantum_shear(a, w), quantum_shear(b, w)),
                    'quantum shear bracket covariance')
        counts['quantum_bracket_covariance'] += 1

    for a in range(1, 5):
        for t in range(2, 6):
            for sample in range(2):
                w = add(power(q, t), scale(q, F(sample+1, 3)))
                A, B, C = F(sample+1), F(-2, 3), F(5, 7)
                beta, delta = F(sample-1, 2), F(3)
                u = mul(q, w)
                g = add(z, u)
                h0 = add(mul(power(q, a),
                             add(scale(power(z, 2), A), scale(z, B), scale(one, C))),
                         scale(z, beta), scale(one, delta))
                h = add(mul(power(q, a),
                            add(scale(power(g, 2), A), scale(g, B), scale(one, C))),
                        scale(g, beta), scale(one, delta))
                check_equal(h, classical_shear(h0, w), 'pure family pullback')
                target = scale(add(h, scale(g, -beta), scale(one, -delta)), a)
                check_equal(poisson(h, g), target, 'pure family bracket')
                for k in range(3, min(degree(h), degree(g))+1, 2):
                    check_zeros(trans(h, g, k), 'pure family gate')
                    counts['pure_family_gate_checks'] += 1
                iterate = g
                for _ in range(5):
                    check_equal(bracket(h, iterate), poisson(h, iterate),
                                'pure family exact iterate')
                    iterate = poisson(h, iterate)
                    counts['pure_family_iterates'] += 1
                counts['pure_top_families'] += 1

    for _ in range(12):
        f = add(power(p, rng.randrange(2, 5)), scale(p, F(2, 3)), one)
        a = add(power(p, rng.randrange(0, 4)), scale(p, F(-1, 2)), one)
        h = mul(q, f)
        fp, fpp = der(f, p=1), der(f, p=2)
        ap = der(a, p=1)
        actual2 = jordan(h, jordan(h, a))
        expected2 = add(mul(power(h, 2), a),
                        hshift(scale(mul(fp, add(mul(fp, a), mul(f, ap))), F(1, 4)), 2))
        check_equal(actual2, expected2, 'qF Jordan square')
        actual3 = jordan(h, actual2)
        b3 = add(mul(add(scale(mul(f, power(fp, 2)), 5),
                             scale(mul(power(f, 2), fpp), -1)), a),
                 scale(mul(mul(power(f, 2), fp), ap), 3))
        expected3 = add(mul(power(h, 3), a), hshift(scale(mul(q, b3), F(1, 4)), 2))
        check_equal(actual3, expected3, 'qF Jordan cubic')
        check_equal(trans(h, power(h, 2), 3),
                    scale(mul(mul(f, fp), fpp), 12), 'qF square obstruction')
        counts['qF_square_cubic'] += 1
        actual = a
        for n in range(1, 9):
            actual = jordan(h, actual)
            if n >= 2:
                expected = scale(mul(mul(power(q, n-2), power(f, n-2)),
                                      add(scale(mul(power(fp, 2), a), 2*n-1),
                                          scale(mul(mul(f, fp), ap), 3),
                                          scale(mul(mul(f, fpp), a), -(n-2)))),
                                 F(n*(n-1), 24))
                h2 = {(i, j, 0): c for (i, j, hh), c in actual.items() if hh == 2}
                check_equal(h2, expected, 'qF general hbar2 coefficient')
                counts['qF_hbar2_general'] += 1

    return {'schema': 'protected-canonical-transport-v1', 'status': 'passed',
            'arithmetic': 'exact rational polynomial arithmetic; standard library',
            'seed': 736019, 'checks': counts,
            'limits': ('These finite checks independently replay identities and fixtures. '
                       'The all-degree claims use the proofs in canonical_bridge.md; '
                       'historical priority and arbitrary nonlinear covariance are not claimed.')}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = checks()
    payload = json.dumps(result, indent=2) + '\n'
    if args.output:
        args.output.write_text(payload)
    print(payload, end='')


if __name__ == '__main__':
    main()
