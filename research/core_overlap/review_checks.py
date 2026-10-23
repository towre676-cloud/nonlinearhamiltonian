#!/usr/bin/env python3
"""Independent exact checks for the core-overlap results (standard library).

The differential identities are formal Laurent-polynomial identities. The
polynomial witnesses use direct differentiation, not the producing PBW code.
Finite modular ranks corroborate examples; the all-degree bound is the
separate transverse-filtration proof in pure_perfect_power.md.
"""
from __future__ import annotations

from fractions import Fraction as Q
from math import comb
import json
from pathlib import Path
import random


def add(*xs):
    out = {}
    for x in xs:
        for m, z in x.items():
            out[m] = out.get(m, Q(0)) + z
    return {m: z for m, z in out.items() if z}


def scale(x, z):
    return {m: z * c for m, c in x.items() if z * c}


def mul(x, y):
    out = {}
    for m, c in x.items():
        for n, d in y.items():
            mn = tuple(a + b for a, b in zip(m, n))
            out[mn] = out.get(mn, Q(0)) + c * d
    return {m: c for m, c in out.items() if c}


def power(x, n):
    out = {tuple(0 for _ in next(iter(x))): Q(1)}
    for _ in range(n):
        out = mul(out, x)
    return out


def partder(x, i):
    out = {}
    for m, c in x.items():
        if m[i]:
            n = list(m)
            n[i] -= 1
            out[tuple(n)] = c * m[i]
    return out


def differential_depth_identities():
    # Laurent ring Q[F,w,B,u,v,a,beta,k,delta]; B and v may have negative
    # exponents. The derivation models F'=w,w'=delta B,B'=u,u'=v,
    # v'=beta v u/B. All other generators are constants.
    n = 9
    one = {(0,) * n: Q(1)}

    def mon(i, exponent=1):
        e = [0] * n
        e[i] = exponent
        return {tuple(e): Q(1)}

    F, w, B, u, v, a, beta, k, delta = [mon(i) for i in range(n)]
    Binv, vinv = mon(2, -1), mon(4, -1)
    field = [w, mul(delta, B), u, v, mul(mul(mul(beta, v), u), Binv)]

    def D(x):
        return add(*(mul(partder(x, i), field[i]) for i in range(5)))

    E = add(mul(F, u), scale(mul(mul(a, w), B), -1),
            scale(mul(k, B), -1))
    L = add(mul(a, add(beta, scale(one, -1))), scale(one, 2))
    J = add(mul(mul(L, w), v),
            mul(mul(add(beta, scale(one, -1)), k), v),
            mul(mul(mul(add(one, scale(a, -3)), delta), B), u))
    assert not add(D(D(E)), scale(J, -1),
                   scale(mul(mul(mul(beta, v), Binv), E), -1))

    dcoef = add(mul(a, add(beta, scale(one, -4))), scale(one, 3))
    A = mul(add(scale(a, 3), scale(one, -1)), add(one, scale(beta, -1)))
    R = add(mul(mul(dcoef, B), v), scale(mul(A, mul(u, u)), -1))
    assert not add(mul(D(mul(J, vinv)), v), scale(mul(delta, R), -1))
    obstruction = mul(add(beta, scale(one, 5)),
                      add(one, mul(a, add(beta, scale(one, -2)))))
    assert not add(D(R), scale(mul(mul(u, v), obstruction), -1))
    cases = 0
    for c in range(5, 10001):
        av = Q(3*c, c-2)
        bv = Q(5*(c-2), 3*(c-4))
        assert 1 + av*(bv-2) == Q(8*(c+1), (c-4)*(c-2)) > 0
        assert av*(bv-1)+2 > 0 and bv > 1
        cases += 1
    return {"formal_laurent_identities": 3,
            "positive_sector_specializations": cases,
            "reason": "The residual differentiated identity cannot vanish on an interval with B' B'' != 0."}


def diff(x, nq=0, np=0):
    for _ in range(nq):
        x = partder(x, 0)
    for _ in range(np):
        x = partder(x, 1)
    return x


def T(H, G, k):
    return add(*(scale(mul(diff(H, k-i, i), diff(G, i, k-i)),
                       (-1)**i * comb(k, i)) for i in range(k+1)))


def pure_witnesses():
    rng = random.Random(20261022)
    q, p, one = {(1, 0): Q(1)}, {(0, 1): Q(1)}, {(0, 0): Q(1)}
    gate_checks = 0
    for trial in range(120):
        exponent = 1 + trial % 5
        degree = 3 + trial % 5
        u = {(i, 0): Q(rng.randrange(-3, 4)) for i in range(1, degree+1)}
        u[(degree, 0)] = Q(1 + trial % 3)
        J = add(mul(q, p), u)
        a2 = Q((-1)**trial * (1 + trial % 3))
        a1, a0, beta, delta = [Q(rng.randrange(-3, 4)) for _ in range(4)]
        P = add(scale(power(J, 2), a2), scale(J, a1), scale(one, a0))
        H = add(mul(power(q, exponent), P), scale(J, beta), scale(one, delta))
        assert T(H, J, 1) == scale(add(H, scale(J, -beta), scale(one, -delta)), exponent)
        assert max(sum(m) for m in H) == exponent + 2*degree
        assert [(m, z) for m, z in H.items() if sum(m) == exponent+2*degree] == [((exponent+2*degree, 0), a2*u[(degree, 0)]**2)]
        for k in range(3, degree+1, 2):
            assert not T(H, J, k)
            gate_checks += 1
        DG = T(H, J, 1)
        for depth in range(1, 5):
            assert T(H, DG, 1) == scale(DG, -exponent*beta)
            for k in range(3, max(sum(m) for m in DG)+1 if DG else 3, 2):
                assert not T(H, DG, k)
                gate_checks += 1
            DG = T(H, DG, 1)
    return {"parameterized_polynomial_fixtures": 120,
            "direct_odd_gate_checks": gate_checks,
            "direct_bracket_depth": 5}


def rank_mod(rows, modulus):
    pivots = {}
    for row in rows:
        row = {i: int(c) % modulus for i, c in row.items() if int(c) % modulus}
        while row:
            i = min(row)
            if i not in pivots:
                z = pow(row[i], -1, modulus)
                pivots[i] = {j: (c*z) % modulus for j, c in row.items()}
                break
            z = row[i]
            old = pivots[i]
            row = {j: (row.get(j, 0)-z*old.get(j, 0)) % modulus
                   for j in set(row) | set(old)}
            row = {j: c for j, c in row.items() if c}
    return len(pivots)


def finite_modular_corroboration():
    q, p = {(1, 0): Q(1)}, {(0, 1): Q(1)}
    J = add(mul(q, p), power(q, 3))
    H = mul(q, power(J, 2))
    receipts = []
    for bound in (7, 9):
        monomials = [(i, j) for i in range(bound+1) for j in range(bound+1-i)]
        rows = {}
        for column, m in enumerate(monomials):
            image = {m: Q(1)}
            for depth in range(5):
                for k in (3, 5, 7):
                    for out, z in T(H, image, k).items():
                        rows.setdefault((depth, k, out), {})[column] = z
                image = T(H, image, 1)
        rank = rank_mod(rows.values(), 1000003)
        assert rank == len(monomials)-3
        receipts.append({"degree_bound": bound, "columns": len(monomials),
                         "rank_mod_1000003": rank, "nullity": 3,
                         "maximum_bracket_depth": 4})
    return receipts


def compose(H, X, Y):
    return add(*(scale(mul(power(X, i), power(Y, j)), z)
                 for (i, j), z in H.items()))


def composition_checks():
    q, p, one = {(1, 0): Q(1)}, {(0, 1): Q(1)}, {(0, 0): Q(1)}
    scalar_cases = 0
    for mu in range(2, 7):
        for s in range(1, 7):
            for n in range(3, 6):
                J = add(mul(q, p), power(q, n))
                image = T(power(J, mu), power(J, s), 3)
                pdegree = mu+s-4
                coefficient = mu*s*(s-mu)*(s+mu-3)*n*(n-1)*(n-2)
                retained = {m: z for m, z in image.items() if m[1] == pdegree}
                expected = {(mu+s+n-4, pdegree): Q(coefficient)} if coefficient else {}
                assert retained == expected
                scalar_cases += 1

    rng = random.Random(99120261022)
    transformed_cases, gate_cases = 0, 0
    for trial in range(16):
        mu = 2 + trial % 4
        b = Q((-1)**trial * (1 + trial % 3))
        c, d, epsilon = [Q(rng.randrange(-3, 4)) for _ in range(3)]
        Qpoly = add(p, scale(power(q, 2), b), scale(q, c), scale(one, d))
        P = {(0, i): Q(rng.randrange(-3, 4)) for i in range(mu+1)}
        P[(0, mu)] = Q(1 + trial % 3)
        H = add(compose(P, q, Qpoly), scale(q, epsilon))
        P1, P2, P3 = diff(P, np=1), diff(P, np=2), diff(P, np=3)
        for _ in range(3):
            Gbar = {(rng.randrange(5), rng.randrange(5)): Q(rng.randrange(-3, 4))
                    for _ in range(8)}
            G = compose(Gbar, q, Qpoly)
            Dbar = add(scale(diff(Gbar, np=1), epsilon),
                       scale(mul(P1, diff(Gbar, nq=1)), -1))
            Cbar = add(scale(mul(P3, add(diff(Gbar, nq=3),
                                                   scale(diff(Gbar, nq=1, np=1), 6*b))), -1),
                       scale(mul(P2, diff(Gbar, nq=1, np=2)), -6*b))
            assert T(H, G, 1) == compose(Dbar, q, Qpoly)
            assert T(H, G, 3) == compose(Cbar, q, Qpoly)
            transformed_cases += 1

        basis = [power(Qpoly, i) for i in range(6)] + [q]
        if mu == 2:
            basis += [mul(q, Qpoly), power(q, 2)]
        for G in basis:
            for depth in range(3):
                if not G:
                    break
                maximum = min(max(sum(m) for m in H), max(sum(m) for m in G))
                for k in range(3, maximum+1, 2):
                    assert not T(H, G, k)
                    gate_cases += 1
                G = T(H, G, 1)
    return {"balanced_transverse_leading_gate_cases": scalar_cases,
            "parabolic_change_of_variable_cases": transformed_cases,
            "parabolic_sector_odd_gate_checks": gate_cases,
            "parabolic_repeated_bracket_depth": 2}


def additive_potential_sharpness():
    H = {(1, Q(-1, 4)): Q(1), (0, Q(7, 4)): Q(1)}
    G = {(3, Q(-3, 4)): Q(1), (2, Q(5, 4)): Q(-21, 25)}
    DG = T(H, G, 1)
    assert DG == {(2, Q(0)): Q(-168, 25), (1, Q(2)): Q(147, 50)}
    assert not T(H, G, 3)
    assert not T(H, G, 5)
    assert not T(H, DG, 3)
    assert T(H, T(H, DG, 1), 3) == {(0, Q(-9, 2)): Q(63, 8)}
    return {"first_three_conditions": "zero",
            "second_iterate_third_gate": "63/8 p^(-9/2)",
            "reason": "The second bracket depth is indispensable with an arbitrary analytic potential."}


def shear_square_checks():
    rng = random.Random(2026102293)
    q, p, one = {(1, 0): Q(1)}, {(0, 1): Q(1)}, {(0, 0): Q(1)}
    changes, gates = 0, 0
    for trial in range(20):
        n = 3 + trial % 5
        u = {(i, 0): Q(rng.randrange(-2, 3)) for i in range(n+1)}
        u[(n, 0)] = Q(1 + trial % 2)
        Qpoly = add(p, u)
        A = Q((-1)**trial * (1 + trial % 3))
        B, C, epsilon = [Q(rng.randrange(-2, 3)) for _ in range(3)]
        H = add(scale(power(Qpoly, 2), A), scale(Qpoly, B),
                scale(one, C), scale(q, epsilon))
        linear = add(scale(p, 2*A), scale(one, B))
        u2, u3 = diff(u, nq=2), diff(u, nq=3)
        sharp = power(q, 3)
        assert not T(H, sharp, 3)
        assert not T(H, T(H, sharp, 1), 3)
        assert T(H, T(H, T(H, sharp, 1), 1), 3) == scale(u2, -288*A**3)
        for _ in range(3):
            Gbar = {(rng.randrange(5), rng.randrange(5)): Q(rng.randrange(-2, 3))
                    for _ in range(6)}
            G = compose(Gbar, q, Qpoly)
            Dbar = add(scale(diff(Gbar, np=1), epsilon),
                       scale(mul(linear, diff(Gbar, nq=1)), -1))
            Cbar = add(mul(mul(linear, u3), diff(Gbar, np=3)),
                       scale(mul(u2, diff(Gbar, nq=1, np=2)), -6*A))
            assert T(H, G, 1) == compose(Dbar, q, Qpoly)
            assert T(H, G, 3) == compose(Cbar, q, Qpoly)
            changes += 1
        basis = [one, q, Qpoly, power(q, 2), mul(q, Qpoly), power(Qpoly, 2)]
        for G in basis:
            for depth in range(3):
                if not G:
                    break
                maximum = min(max(sum(m) for m in H), max(sum(m) for m in G))
                for k in range(3, maximum+1, 2):
                    assert not T(H, G, k)
                    gates += 1
                G = T(H, G, 1)

    # Independent finite matrices in the transformed polynomial algebra.
    # The proof supplies the all-degree upper bound; these corroborate it.
    u = add(power(q, 3), q)
    u2, u3 = diff(u, nq=2), diff(u, nq=3)
    linear = add(scale(p, 2), scale(one, 2))

    def Dbar(G):
        return add(scale(diff(G, np=1), 3),
                   scale(mul(linear, diff(G, nq=1)), -1))

    def Cbar(G):
        return add(mul(mul(linear, u3), diff(G, np=3)),
                   scale(mul(u2, diff(G, nq=1, np=2)), -6))

    ranks = []
    for bound in (4, 6, 8):
        monomials = [(i, j) for i in range(bound+1) for j in range(bound+1-i)]
        rows = {}
        for column, m in enumerate(monomials):
            G = {m: Q(1)}
            for depth in range(bound+1):
                for out, z in Cbar(G).items():
                    rows.setdefault((depth, out), {})[column] = z
                G = Dbar(G)
        rank = rank_mod(rows.values(), 1000003)
        assert rank == len(monomials)-6
        ranks.append({"transformed_degree_bound": bound, "columns": len(monomials),
                      "rank_mod_1000003": rank, "nullity": 6})
    scalar_depth_cases = 0
    for n in range(3, 31):
        for a in range(26):
            for c in range(26):
                if a+c < 3:
                    continue
                coefficients = []
                for r in range(3):
                    falling = 1
                    for j in range(r):
                        falling *= a-j
                    coefficients.append(falling*(c+r)*(c+r-1)*
                                        ((n-2)*(c+r-2)-3*(a-r)))
                assert any(coefficients)
                scalar_depth_cases += 1
    return {"original_vs_transformed_operator_cases": changes,
            "sector_odd_gate_checks": gates, "bracket_depth": 2,
            "uniform_depth_two_scalar_cases": scalar_depth_cases,
            "sharp_q_cubed_fixtures": 20,
            "supplementary_modular_ranks": ranks}


def main():
    report = {"status": "passed", "schema": "independent-core-overlap-review-v1",
              "depth": differential_depth_identities(),
              "pure": pure_witnesses(),
              "finite_example_corroboration": finite_modular_corroboration(),
              "composition_families": composition_checks(),
              "additive_potential_depth_sharpness": additive_potential_sharpness(),
              "shear_square": shear_square_checks(),
              "limits": "Finite matrices corroborate examples only. The all-degree claims rely on the explicit proofs, not on extrapolation or literature priority."}
    path = Path(__file__).with_name("review_results.json")
    path.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
