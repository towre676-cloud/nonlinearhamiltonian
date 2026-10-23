#!/usr/bin/env python3
"""Independent Fraction replay of the cubic-phase proof coefficients.

This file imports no project mathematical engine or producer classifier.
Its finite identities supplement the all-degree arguments in the note.
"""
from fractions import Fraction as F
from math import comb, factorial
from pathlib import Path
import argparse
import json
import random


def clean(f):
    return {e: F(a) for e, a in f.items() if a}


def add(*fs):
    out = {}
    for f in fs:
        for e, a in f.items():
            out[e] = out.get(e, F(0)) + a
    return clean(out)


def scale(f, a):
    return clean({e: a*b for e, b in f.items()})


def mul(f, g):
    out = {}
    for (i, j), a in f.items():
        for (k, l), b in g.items():
            e = (i+k, j+l)
            out[e] = out.get(e, F(0)) + a*b
    return clean(out)


def power(f, n):
    out = {(0, 0): F(1)}
    for _ in range(n):
        out = mul(out, f)
    return out


def der(f, q=0, p=0):
    return clean({(i-q, j-p): a*F(factorial(i), factorial(i-q))*
                  F(factorial(j), factorial(j-p))
                  for (i, j), a in f.items() if i >= q and j >= p})


def compose(f, x, y):
    return add(*(scale(mul(power(x, i), power(y, j)), a)
                 for (i, j), a in f.items()))


Q, P, ONE = {(1, 0): F(1)}, {(0, 1): F(1)}, {(0, 0): F(1)}


def bracket(h, g):
    return add(mul(der(h, q=1), der(g, p=1)),
               scale(mul(der(h, p=1), der(g, q=1)), -1))


def transvectant(h, g, k):
    return add(*(scale(mul(der(h, q=k-j, p=j),
                           der(g, q=j, p=k-j)), (-1)**j*comb(k, j))
                 for j in range(k+1)))


def pull(f, w):
    return compose(f, Q, add(P, w))


def affine_c3(a, b, g, c):
    a3b3 = add(der(a, p=3), mul(Q, der(b, p=3)))
    a2b2 = add(der(a, p=2), mul(Q, der(b, p=2)))
    return add(scale(mul(a3b3, der(g, q=3)), -1),
               scale(mul(der(b, p=2), der(g, q=2, p=1)), 3),
               scale(add(mul(der(b, p=1), der(g, p=3)),
                         mul(der(b, p=2), der(g, p=2)),
                         scale(mul(a2b2, der(g, q=1, p=2)), -1),
                         scale(mul(a3b3, der(g, q=1, p=1)), -1)), 6*c))


def restoring_c3(f, g, c):
    return add(scale(mul(der(f, p=3), der(g, q=3)), -1),
               scale(mul(der(f, p=2), der(g, q=1, p=2)), -6*c),
               scale(mul(der(f, p=3), der(g, q=1, p=1)), -6*c))


def diagonal_image(g, A, c):
    """Input/output variables are (J,P), J=Q+A(P), h=PJ."""
    gqp = compose(g, add(Q, A), P)
    image = affine_c3(mul(P, A), P, gqp, c)
    return compose(image, add(Q, scale(A, -1)), P)


def lagrange_coefficients(nodes, at):
    """Coefficients of the polynomial equal to delta_at on distinct nodes."""
    coefficients = [F(1)]
    for k, node in enumerate(nodes):
        if k == at:
            continue
        new = [F(0)]*(len(coefficients)+1)
        denominator = nodes[at]-node
        for j, a in enumerate(coefficients):
            new[j] -= node*a/denominator
            new[j+1] += a/denominator
        coefficients = new
    return coefficients


def rank(columns):
    keys = sorted({e for g in columns for e in g})
    rows = [[g.get(e, F(0)) for g in columns] for e in keys]
    pivot = 0
    for j in range(len(columns)):
        k = next((i for i in range(pivot, len(rows)) if rows[i][j]), None)
        if k is None:
            continue
        rows[pivot], rows[k] = rows[k], rows[pivot]
        s = rows[pivot][j]
        rows[pivot] = [a/s for a in rows[pivot]]
        for i in range(pivot+1, len(rows)):
            if rows[i][j]:
                s = rows[i][j]
                rows[i] = [a-s*b for a, b in zip(rows[i], rows[pivot])]
        pivot += 1
        if pivot == len(rows):
            break
    return pivot


def invariant_span(h, basis):
    n = rank(basis)
    assert n == len(basis)
    degree = max(sum(e) for e in h)
    for g in basis:
        assert all(not transvectant(h, g, k) for k in range(3, degree+1, 2))
        assert rank(basis+[bracket(h, g)]) == n


def check():
    rng = random.Random(3023)
    counts = {}
    n = 0
    for _ in range(30):
        a = clean({(0, j): F(rng.randint(-2, 2)) for j in range(7)})
        b = clean({(0, j): F(rng.randint(-2, 2)) for j in range(5)})
        g = clean({(i, j): F(rng.randint(-2, 2)) for i in range(4)
                   for j in range(5) if i+j <= 5})
        c = F(rng.choice([-2, 1, 3]))
        w = add(scale(power(Q, 2), c), scale(Q, rng.randint(-2, 2)),
                scale(ONE, rng.randint(-2, 2)))
        h = add(a, mul(Q, b))
        assert transvectant(pull(h, w), pull(g, w), 3) == pull(affine_c3(a, b, g, c), w)
        n += 1
    counts['original_coordinate_affine_third_gate'] = n
    n = 0
    for d in range(2, 8):
        b = add(power(P, d), scale(power(P, d-1), 2), P, ONE)
        for N in range(2, 8):
            for k in range(12):
                g = mul(power(Q, N), power(P, k))
                gate = affine_c3({}, b, g, F(1, 6))
                e = k+d-4
                expected = d*k*(k+d-3)*(k-1-N*(d-1))
                assert gate.get((N, e), F(0)) == expected
                n += 1
    counts['highest_Q_leading_factor'] = n
    n = 0
    for c in (F(1), F(-2), F(1, 3)):
        h = mul(Q, power(P, 2))
        g = add(power(Q, 2), scale(P, 2/c))
        assert not affine_c3({}, power(P, 2), g, c)
        dg = bracket(h, g)
        assert not affine_c3({}, power(P, 2), dg, c)
        actual = affine_c3({}, power(P, 2), bracket(h, dg), c)
        assert actual == add(scale(P, 864), scale(power(Q, 2), -288*c))
        n += 1
        for mu, a3 in ((F(2), F(1)), (F(-3), F(-2))):
            a = add(scale(power(P, 3), a3), scale(power(P, 2), 2), P, ONE)
            b = add(scale(power(P, 2), mu), scale(P, -3), ONE)
            h = add(a, mul(Q, b))
            g = add(scale(power(P, 2), F(3)*a3/(2*mu)), scale(P, 2), mul(Q, P))
            assert not affine_c3(a, b, g, c)
            image = affine_c3(a, b, bracket(h, g), c)
            assert image.get((0, 1), F(0)) == 144*c*mu*a3
            n += 1
    counts['quadratic_coupling_finite_stopping_coefficients'] = n
    n = 0
    for m in range(2, 7):
        A = add(power(P, m), scale(P, -2), ONE)
        a = mul(P, A)
        J = add(Q, A)
        for d in range(3):
            for N in range(2, 7):
                g = mul(power(P, d), power(J, N))
                image = affine_c3(a, P, g, F(2))
                image_J = compose(image, add(Q, scale(A, -1)), P)
                if N == 2:
                    expected = -24*m*m*(2*m-1)*(d+m-1)
                    target = (0, d+2*m-3)
                else:
                    expected = -12*m**4*N*(N-1)*(N-2)
                    target = (N-3, d+3*m-3)
                assert image_J.get(target, F(0)) == expected
                n += 1
    counts['linear_coupling_diagonal_leading_coefficients'] = n
    supports = moments = 0
    for m in range(2, 6):
        A = add(scale(power(P, m), F(2, 3)), scale(P, -1), ONE)
        shifts = set()
        for u in range(4):
            for v in range(4):
                image = diagonal_image(mul(power(Q, u), power(P, v)), A, F(1))
                shifts.update(j-i-(v-u) for i, j in image)
        assert shifts <= {-3, -1} | set(range(1, 3*m+1))
        assert len(shifts)-1 <= 3*m+1
        if m == 2:
            normalized = add(scale(power(P, 2), 2), ONE)
            normalized_shifts = set()
            for u in range(4):
                for v in range(4):
                    image = diagonal_image(mul(power(Q, u), power(P, v)), normalized, F(1))
                    normalized_shifts.update(j-i-(v-u) for i, j in image)
            assert normalized_shifts == {-3, 3, 6}
        supports += 1
        g = clean({(i, j): F(rng.randint(-2, 2)) for i in range(4)
                   for j in range(4) if i+j <= 4})
        images = []
        for r in range(len(shifts)):
            dg = clean({(i, j): a*F(j-i)**r for (i, j), a in g.items()})
            images.append(diagonal_image(dg, A, F(1)))
        targets = sorted({e for image in images for e in image})[:3]
        for target in targets:
            omega = target[1]-target[0]
            nodes = [omega-s for s in sorted(shifts)]
            values = [image.get(target, F(0)) for image in images]
            for at, weight in enumerate(nodes):
                coefficients = lagrange_coefficients(nodes, at)
                recovered = sum((a*b for a, b in zip(coefficients, values)), F(0))
                component = {e: a for e, a in g.items() if e[1]-e[0] == weight}
                assert recovered == diagonal_image(component, A, F(1)).get(target, F(0))
            moments += 1
    counts['linear_finite_stopping_weight_support'] = supports
    counts['linear_finite_stopping_vandermonde_coordinates'] = moments
    n = 0
    for degree in (3, 4, 5):
        for a2 in (0, 2):
            a = add(power(P, degree), scale(power(P, 2), a2), P, ONE)
            h = add(a, mul(Q, P))
            basis = [ONE, P, power(P, 2), h]
            if degree == 3:
                basis.append(Q)
                if a2 == 0:
                    basis.append(mul(P, h))
            for c in (F(1), F(-2)):
                w = add(scale(power(Q, 2), c), Q)
                invariant_span(pull(h, w), [pull(g, w) for g in basis])
                n += 1
    counts['full_output_linear_coupling_spans'] = n
    n = 0
    for degree in range(3, 8):
        for c in (F(1), F(-2)):
            f = add(power(P, degree), scale(power(P, 2), -2), P, ONE)
            lam, eps = F(3, 2), F(-2, 3)
            h = add(f, scale(power(Q, 2), lam), scale(Q, eps), ONE)
            w = add(scale(power(Q, 2), c), scale(Q, 2), scale(ONE, -1))
            ho, po = pull(h, w), pull(P, w)
            R = der(mul(der(f, p=2), der(f, p=3)), p=1)
            assert R
            q2 = bracket(ho, bracket(ho, Q))
            p2 = bracket(ho, bracket(ho, po))
            p3 = bracket(ho, p2)
            assert transvectant(ho, q2, 3) == pull(scale(R, 12*c*lam), w)
            assert not transvectant(ho, p2, 3)
            assert transvectant(ho, p3, 3) == pull(scale(R, 24*c*lam*lam), w)
            for g in (ONE, Q, P, h, power(Q, 2), power(Q, 3), mul(Q, power(P, 3))):
                assert transvectant(ho, pull(g, w), 3) == pull(restoring_c3(f, g, c), w)
            n += 1
    counts['restoring_gate_and_sharp_depth_instances'] = n
    # The vector-field defect is a total derivative, with no scalar Virasoro
    # interpretation inferred. Verify its polynomial identity independently.
    n = 0
    for i in range(9):
        for j in range(9):
            b, beta = power(P, i), power(P, j)
            left = add(mul(der(b, p=1), der(beta, p=3)),
                       scale(mul(der(b, p=3), der(beta, p=1)), -1))
            primitive = add(mul(der(b, p=1), der(beta, p=2)),
                            scale(mul(der(b, p=2), der(beta, p=1)), -1))
            assert left == der(primitive, p=1)
            n += 1
    counts['compatibility_defect_total_derivative'] = n
    return {'format': 'cubic-phase-independent-review-v1', 'status': 'passed',
            'checks': counts,
            'scope': 'Independent direct mixed derivatives and proof-coefficient replay; finite examples supplement all-degree proofs. Historical priority unestablished.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = check()
    if args.output:
        args.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
