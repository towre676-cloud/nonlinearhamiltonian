#!/usr/bin/env python3
"""Independent exact checks for analytic_bridge.md (Python standard library).

Sparse monomials q^i p^r have i in N and r rational. Derivatives are
expanded directly rather than importing either programme's gate engine.
Finite-box ranks cross-check conventions only; the note proves all degrees.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as Q
from math import comb, factorial
import json
from pathlib import Path


def clean(f):
    return {(int(i), Q(r)): Q(v) for (i, r), v in f.items() if v}


def mono(i, r, v=1):
    return clean({(i, Q(r)): Q(v)})


def add(*fs):
    out = {}
    for f in fs:
        for key, value in f.items():
            out[key] = out.get(key, Q(0)) + value
    return clean(out)


def scale(f, a):
    return clean({key: a * value for key, value in f.items()})


def mul(f, g):
    out = {}
    for (i, r), a in f.items():
        for (j, s), b in g.items():
            key = i + j, r + s
            out[key] = out.get(key, Q(0)) + a * b
    return clean(out)


def power(f, n):
    out = mono(0, 0)
    for _ in range(n):
        out = mul(out, f)
    return out


def derivative(f, nq=0, np=0):
    out = clean(f)
    for axis, count in [(0, nq), (1, np)]:
        for _ in range(count):
            nxt = {}
            for (i, r), a in out.items():
                exponent = i if axis == 0 else r
                if exponent:
                    key = (i - 1, r) if axis == 0 else (i, r - 1)
                    nxt[key] = a * exponent
            out = clean(nxt)
    return out


def transvectant(f, g, k):
    out = {}
    for j in range(k + 1):
        out = add(out, scale(mul(derivative(f, k - j, j),
                                 derivative(g, j, k - j)),
                             (-1) ** j * comb(k, j)))
    return out


def bracket(f, g):
    return transvectant(f, g, 1)


def maxq(f):
    return max((i for i, _ in f), default=0)


def moyal(f, g):
    """Normalized commutator as {even hbar exponent: sparse coefficient}."""
    out = {}
    for k in range(1, maxq(f) + maxq(g) + 1, 2):
        value = scale(transvectant(f, g, k),
                      Q((-1) ** ((k - 1) // 2), 2 ** (k - 1) * factorial(k)))
        if value:
            out[k - 1] = value
    return out


def even_star(f, g):
    """Even part of f star g; f=g implies this is the full star square."""
    out = {}
    for k in range(0, maxq(f) + maxq(g) + 1, 2):
        value = scale(transvectant(f, g, k),
                      Q((-1) ** (k // 2), 2 ** k * factorial(k)))
        if value:
            out[k] = value
    return out


def rank(rows, ncols):
    a = [list(row) for row in rows]
    pivot_row = 0
    for col in range(ncols):
        pick = next((i for i in range(pivot_row, len(a)) if a[i][col]), None)
        if pick is None:
            continue
        a[pivot_row], a[pick] = a[pick], a[pivot_row]
        coefficient = a[pivot_row][col]
        a[pivot_row] = [x / coefficient for x in a[pivot_row]]
        for i in range(pivot_row + 1, len(a)):
            if a[i][col]:
                coefficient = a[i][col]
                a[i] = [x - coefficient * y for x, y in zip(a[i], a[pivot_row])]
        pivot_row += 1
        if pivot_row == len(a):
            break
    return pivot_row


def box_kernel(H, qbound=5, pmin=-2, pmax=5):
    basis = [mono(i, j) for i in range(qbound + 1) for j in range(pmin, pmax + 1)]
    images = [(transvectant(H, g, 3), transvectant(H, bracket(H, g), 3))
              for g in basis]
    keys = sorted({(step, i, r) for pair in images for step, f in enumerate(pair)
                   for i, r in f})
    rows = [[pair[step].get((i, r), Q(0)) for pair in images]
            for step, i, r in keys]
    dimension = len(basis) - rank(rows, len(basis))
    expected = 2 * (pmax - pmin + 1)
    assert dimension == expected, (H, dimension, expected)
    for g in basis[:expected]:
        assert not transvectant(H, g, 3)
        assert not transvectant(H, bracket(H, g), 3)
    return {"input_monomials": len(basis), "output_coordinates": len(keys),
            "kernel_dimension": dimension, "expected_strip_dimension": expected,
            "output_projection": False}


def check_asymptotic_coefficients():
    count = 0
    for c in range(2, 41):
        alpha = Q(c - 2, 3)
        for m in range(1, 41):
            # F=p^-m; Kc is exactly the leading monomial in (A4).
            coefficient = -alpha * (m + 2) + c * m
            expected = Q(2, 3) * ((c + 1) * m - c + 2)
            assert coefficient == expected and coefficient > 0
            count += 1
        for n in range(2, 41):
            # F=p^n; includes n=2 where F'''=0.
            coefficient = alpha * (n - 2) - c * n
            expected = -Q(2, 3) * ((c + 1) * n + c - 2)
            assert coefficient == expected and coefficient < 0
            count += 1
    return count


def check_top_coefficient():
    count = 0
    for c in range(2, 13):
        for exponent in [Q(-3), Q(-1), Q(2), Q(3), Q(7), Q(-1, 4)]:
            F = mono(0, exponent)
            H = add(mul(mono(1, 0), F), mono(0, 5), mono(0, -2, 3))
            for r in [Q(-3, 4), Q(0), Q(2), Q(5, 3)]:
                g = mono(0, r)
                G = mono(c, r)
                actual = {key: a for key, a in transvectant(H, G, 3).items()
                          if key[0] == c - 2}
                expected = mul(mono(c - 2, 0, c * (c - 1)),
                               add(scale(mul(derivative(F, np=2), derivative(g, np=1)), 3),
                                   scale(mul(derivative(F, np=3), g), -(c - 2))))
                assert actual == expected
                count += 1
    return count


def check_obstruction_identity():
    # Verify A6 after clearing denominators by direct rational polynomial algebra.
    # The quotient derivative of U/V is represented by U'V-UV'.
    count = 0
    for c in range(2, 19):
        for F in [mono(0, 2), mono(0, 5), mono(0, -1),
                  add(mono(0, -3), mono(0, 2), mono(0, 1)),
                  add(mono(0, 6), mono(0, 4, 2), mono(0, 0, 7))]:
            f1, f2, f3, f4 = [derivative(F, np=j) for j in range(1, 5)]
            # Kc = N/(3F'').
            N = add(scale(mul(F, f3), c - 2), scale(mul(f1, f2), -3 * c))
            quotient_numerator = add(mul(derivative(N, np=1), f2),
                                     scale(mul(N, f3), -1))
            expected = add(scale(add(mul(mul(f1, f3), f2),
                                     mul(mul(F, f4), f2),
                                     scale(mul(F, mul(f3, f3)), -1)), c - 2),
                           scale(power(f2, 3), -3 * c))
            assert quotient_numerator == expected
            count += 1
    return count


def check_explicit_family():
    count = 0
    X, Y = mono(1, Q(-1, 4)), mono(0, Q(5, 4), Q(4, 5))
    G = power(X, 3)
    assert bracket(X, Y) == mono(0, 0)
    assert even_star(X, X) == {0: power(X, 2), 2: mono(0, Q(-5, 2), Q(1, 64))}
    for a in [Q(-3), Q(1), Q(7, 5)]:
        for b in [Q(-2), Q(0), Q(5, 3)]:
            H = add(scale(X, a), mono(1, 1, b))
            assert H == add(scale(X, a), scale(mul(X, Y), Q(5, 4) * b))
            eigenvalue = -Q(15, 4) * b
            assert moyal(H, G) == ({} if not eigenvalue else {0: scale(G, eigenvalue)})
            current = G
            for j in range(13):
                assert current == scale(G, eigenvalue ** j)
                assert not any(k for k in moyal(H, current))
                current = bracket(H, current)
                count += 1
            square = power(X, 2)
            assert transvectant(H, square, 3) == mono(0, Q(-15, 4), -Q(15, 16) * a)
            expected = {2: mono(0, Q(-15, 4), Q(5, 128) * a)}
            if b:
                expected[0] = scale(square, -Q(5, 2) * b)
            assert moyal(H, square) == expected
            # Quantum star-square eigenidentity, including its exact hbar^2 term.
            star_square = even_star(X, X)
            action = {}
            for hbar_degree, coefficient in star_square.items():
                for k, value in moyal(H, coefficient).items():
                    degree = hbar_degree + k
                    action[degree] = add(action.get(degree, {}), value)
            action = {k: value for k, value in action.items() if value}
            expected_action = {k: scale(value, -Q(5, 2) * b)
                               for k, value in star_square.items() if b}
            assert action == expected_action
            # Product nonclosure also holds for G^2.
            assert transvectant(H, power(G, 2), 3) == mono(4, Q(-19, 4), Q(675, 16) * a)
            count += 6
    return count


def check_cubic_selection():
    count = 0
    for a in [Q(-3), Q(1), Q(7, 5)]:
        for b in [Q(-2), Q(0), Q(5, 3)]:
            F = add(mono(0, Q(-1, 4), a), mono(0, 1, b))
            f1, f2, f3 = [derivative(F, np=j) for j in range(1, 4)]
            for c in range(2, 41):
                numerator = add(scale(mul(F, f3), c - 2),
                                scale(mul(f1, f2), -3 * c))
                expected_K = add(mono(0, Q(-5, 4), a * Q(3 - c, 2)),
                                 mono(0, 0, -b * Q(7 * c - 6, 4)))
                assert numerator == scale(mul(f2, expected_K), 3)
                assert (not derivative(expected_K, np=1)) == (c == 3)
                count += 1
    return count


def check_third_gate_insufficiency():
    count = 0
    for c in range(4, 21):
        rho = Q(2 - c, c + 1)
        X = mono(1, rho)
        H = add(X, mono(1, 1))
        G = power(X, c)
        eigenvalue = c * (rho - 1)
        assert bracket(H, G) == scale(G, eigenvalue)
        for j in range(5):
            assert not transvectant(H, scale(G, eigenvalue ** j), 3)
            count += 1
        falling_c = c * (c - 1) * (c - 2) * (c - 3)
        falling_rho = rho * (rho - 1) * (rho - 2) * (rho - 3)
        expected = mono(c - 4, -c - 3, -8 * falling_c * falling_rho)
        assert expected and transvectant(H, G, 5) == expected
        count += 2
    return count


def run():
    boxes = []
    functions = [mono(0, 2), mono(0, 3), mono(0, 5), mono(0, -1),
                 add(mono(0, -2), mono(0, 3), mono(0, 1, 2)),
                 add(mono(0, 6), mono(0, 4, 2), mono(0, 0, 7))]
    potentials = [{}, add(mono(0, 7), mono(0, -1, 3))]
    for i, F in enumerate(functions):
        for j, B in enumerate(potentials):
            H = add(mul(mono(1, 0), F), B)
            receipt = box_kernel(H)
            boxes.append({"function_index": i, "potential_index": j, **receipt})
    return {"format": "analytic-polynomial-bridge-v1", "passed": True,
            "asymptotic_coefficient_checks": check_asymptotic_coefficients(),
            "highest_sector_checks": check_top_coefficient(),
            "obstruction_numerator_checks": check_obstruction_identity(),
            "cubic_selection_checks": check_cubic_selection(),
            "third_gate_insufficiency_checks": check_third_gate_insufficiency(),
            "explicit_family_checks": check_explicit_family(),
            "finite_box_checks": boxes,
            "all_degree_proof": "analytic_bridge.md; no finite-box extrapolation"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run()
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(encoded, encoding="utf-8")
    print(encoded)


if __name__ == "__main__":
    main()
