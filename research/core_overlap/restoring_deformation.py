#!/usr/bin/env python3
"""All-degree lifting obstructions for F(p+c*q^2+d*q+e)+t*q^2.

The general theorem and every-N torsion law are proved in the sibling
restoring_deformation.md. This checker retains full polynomial outputs,
uses exact rational arithmetic, and replays polynomial Smith inverses.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
from fractions import Fraction as Q
import json
from pathlib import Path

import deformation_obstructions as O
from cubic_deformation import source_basis

mono, add, scale, mul, diff = O.mono, O.add, O.scale, O.mul, O.diff


def profile(coefficients):
    return add(*(mono(c=int(n), coefficient=Q(a)) for n, a in coefficients.items()))


def operators(f, c):
    f1, f2, f3 = diff(f, 1), diff(f, 1, 2), diff(f, 1, 3)

    def D(g):
        return add(scale(mul(f1, diff(g, 0)), -1),
                   scale(mul(mono(a=1, t=1), diff(g, 1)), 2))

    def C(g):
        return add(scale(mul(f3, diff(g, 0, 3)), -1),
                   scale(mul(f2, diff(diff(g, 1, 2), 0)), -6*c),
                   scale(mul(f3, diff(diff(g, 1), 0)), -6*c))

    def observe(g):
        images = []
        for _ in range(4):
            images.append(C(g))
            g = D(g)
        return images

    return D, C, observe


def matrix(coefficients, c, bound):
    _, _, observe = operators(profile(coefficients), c)
    basis = source_basis(bound)
    columns = [observe(mono(a=a, c=b)) for a, b in basis]
    keys = sorted({(r, a, b) for column in columns for r, p in enumerate(column)
                   for a, b, _ in p})
    M = [[O.clean({(0, 0, k): v for (i, j, k), v in columns[s][r].items()
                   if (i, j) == (a, b)}) for s in range(len(basis))]
         for r, a, b in keys]
    return basis, keys, M


def smith_certificate(coefficients, c, bound):
    """Exact Smith producer for the monomial-profile calibrations below."""
    basis, keys, original = matrix(coefficients, c, bound)
    M = deepcopy(original)
    rows, cols = len(M), len(M[0])
    U, Ui, V, Vi = O.identity(rows), O.identity(rows), O.identity(cols), O.identity(cols)

    def swaprow(i, j):
        M[i], M[j] = M[j], M[i]
        U[i], U[j] = U[j], U[i]
        for row in Ui:
            row[i], row[j] = row[j], row[i]

    def swapcol(i, j):
        for A in (M, V):
            for row in A:
                row[i], row[j] = row[j], row[i]
        Vi[i], Vi[j] = Vi[j], Vi[i]

    def scalerow(i, a):
        M[i], U[i] = [scale(p, a) for p in M[i]], [scale(p, a) for p in U[i]]
        for row in Ui:
            row[i] = scale(row[i], 1/a)

    def addrow(i, j, p):
        M[i] = [add(a, mul(p, b)) for a, b in zip(M[i], M[j])]
        U[i] = [add(a, mul(p, b)) for a, b in zip(U[i], U[j])]
        for row, old in zip(Ui, [row[i] for row in Ui]):
            row[j] = add(row[j], scale(mul(p, old), -1))

    def addcol(i, j, p):
        for A in (M, V):
            for row in A:
                row[i] = add(row[i], mul(p, row[j]))
        Vi[j] = [add(a, scale(mul(p, b), -1)) for a, b in zip(Vi[j], Vi[i])]

    def divide(p, e):
        assert all(a == b == 0 and k >= e for a, b, k in p)
        return {(0, 0, k-e): v for (_, _, k), v in p.items()}

    r, powers = 0, []
    while r < min(rows, cols):
        candidates = [(next(iter(p))[2], i, j) for i in range(r, rows)
                      for j in range(r, cols) if (p := M[i][j]) and len(p) == 1]
        if not candidates:
            assert not any(p for row in M[r:] for p in row[r:])
            break
        e, i, j = min(candidates)
        assert all(k >= e for row in M[r:] for p in row[r:] for _, _, k in p)
        swaprow(r, i)
        swapcol(r, j)
        scalerow(r, 1/next(iter(M[r][r].values())))
        for i in range(rows):
            if i != r and M[i][r]:
                addrow(i, r, scale(divide(M[i][r], e), -1))
        for j in range(cols):
            if j != r and M[r][j]:
                addcol(j, r, scale(divide(M[r][j], e), -1))
        powers.append(e)
        r += 1
    assert r == cols-2
    assert powers == [0]*(cols-2-bound//2)+[1]*(bound//2-1)+[2]
    return {"format": "restoring-polynomial-smith-v1", "field": "Q",
            "profile": {str(n): str(a) for n, a in coefficients.items()}, "shear_coefficient": str(c),
            "weight_bound": bound, "input_basis": [list(k) for k in basis],
            "output_coordinates": [list(k) for k in keys], "output_projection": False,
            "matrix": O.encode_matrix(original), "left": O.encode_matrix(U),
            "left_inverse": O.encode_matrix(Ui), "right": O.encode_matrix(V),
            "right_inverse": O.encode_matrix(Vi), "diagonal": O.encode_matrix(M),
            "nonzero_invariant_exponents": powers, "zero_source_columns": 2,
            "free_cokernel_rank": rows-r}


def verify_smith_certificate(cert):
    assert cert["format"] == "restoring-polynomial-smith-v1"
    coefficients = {int(n): Q(a) for n, a in cert["profile"].items()}
    c, bound = Q(cert["shear_coefficient"]), cert["weight_bound"]
    basis, keys, original = matrix(coefficients, c, bound)
    assert cert["input_basis"] == [list(k) for k in basis]
    assert cert["output_coordinates"] == [list(k) for k in keys]
    assert cert["output_projection"] is False
    M, U, Ui, V, Vi, S = [O.decode_matrix(cert[k]) for k in
                          ("matrix", "left", "left_inverse", "right", "right_inverse", "diagonal")]
    assert M == original
    rows, cols = len(M), len(M[0])
    for A, B, n in ((U, Ui, rows), (Ui, U, rows), (V, Vi, cols), (Vi, V, cols)):
        assert O.polynomial_matrix_product(A, B) == O.identity(n)
    assert O.polynomial_matrix_product(O.polynomial_matrix_product(U, M), V) == S
    powers = [0]*(cols-2-bound//2)+[1]*(bound//2-1)+[2]
    expected = [[{} for _ in range(cols)] for _ in range(rows)]
    for i, e in enumerate(powers):
        expected[i][i] = mono(t=e)
    assert S == expected and cert["nonzero_invariant_exponents"] == powers
    return True


def run():
    q, p = mono(a=1), mono(c=1)
    fixtures, scalar_checks, original_checks, commutator_checks = [], 0, 0, 0
    import analytic_bridge_check as A
    old_q, old_p = A.mono(1, 0), A.mono(0, 1)
    for m in range(3, 7):
        coefficients = {m: Q((-1)**m), m-1: Q(2, 3), 2: Q(-3, 5), 1: Q(4), 0: Q(-2)}
        for c in (Q(1), Q(-2, 3)):
            f = profile(coefficients)
            B, Bprime = diff(f, 1, 2), diff(f, 1, 3)
            R = diff(mul(B, Bprime), 1)
            D, C, observe = operators(f, c)
            assert R
            lead = coefficients[m]**2*m*m*(m-1)**2*(m-2)*(2*m-5)
            assert R.get((0, 2*m-6, 0)) == lead
            assert observe(q)[2] == scale(mul(mono(t=1), R), 12*c)
            assert observe(p)[3] == scale(mul(mono(t=2), R), 24*c)
            assert all(not O.t_coefficient(x, n) for x in observe(p) for n in (0, 1))
            assert D(p) == mono(a=1, t=1, coefficient=2)
            assert D(D(p)) == scale(mul(mono(t=1), diff(f, 1)), -2)
            assert D(D(D(p))) == scale(mul(mono(a=1, t=2), B), -4)
            scalar_checks += 7
            for i in range(5):
                for j in range(5):
                    test = mono(a=i, c=j)
                    D0test = O.t_coefficient(D(test), 0)
                    actual = add(C(D0test), scale(O.t_coefficient(D(C(test)), 0), -1))
                    testqq = diff(test, 0, 2)
                    expected = scale(mul(B, add(mul(Bprime, testqq), mul(B, diff(testqq, 1)))), 12*c)
                    assert actual == expected
                    commutator_checks += 1
            # All coefficients of the first- and second-order compatibility
            # identities are checked exactly, including mixed lower terms.
            a, beta = Q(2, 3), Q(-4, 5)
            g = add(scale(f, a), scale(p, Q(3, 7)), mono(coefficient=Q(-2, 5)))
            G1 = add(scale(mono(a=2), a), scale(q, beta), g)
            assert not C(G1)
            zero_D_G1 = O.t_coefficient(D(G1), 0)
            assert C(zero_D_G1) == scale(diff(mul(B, B), 1), 12*c*a)
            arbitrary_f = add(mono(c=m+2), mono(c=2, coefficient=Q(-2, 7)))
            first_variation = O.t_coefficient(observe(arbitrary_f)[1], 1)
            assert first_variation == scale(diff(mul(B, diff(arbitrary_f, 1, 2)), 1), -12*c)
            scalar_checks += 3
            # A general first lift of P, restricted by the order-two first
            # gate equation, has this form. Every remaining choice gives
            # the same nonzero depth-three second-order residual.
            G = add(p, mul(mono(t=1), add(scale(q, beta), g)),
                    mul(mono(t=2), add(scale(mono(a=2), a), scale(q, Q(5, 9)),
                                       mono(c=m+1, coefficient=Q(2, 7)))))
            observed = observe(G)
            assert not O.t_coefficient(observed[1], 2)
            assert O.t_coefficient(observed[2], 2) == scale(R, 12*c*beta)
            assert O.t_coefficient(observed[3], 2) == scale(R, 24*c)
            scalar_checks += 3
            # Generic initial Hamiltonian has the exact lift H_t.
            H = add(f, mono(a=2, t=1))
            assert not D(H) and all(not x for x in observe(H))
            scalar_checks += 1
            # Original-coordinate direct transvectants include affine
            # terms of the quadratic shear, absent from transformed C3.
            w = A.add(A.mono(2, 0, c), A.mono(1, 0, Q(2, 5)), A.mono(0, 0, Q(-3, 7)))
            P = A.add(old_p, w)
            H_old_base = A.add(*(A.scale(A.power(P, n), value) for n, value in coefficients.items()))
            for parameter in (Q(0), Q(2, 3)):
                H_old = A.add(H_old_base, A.mono(2, 0, parameter))
                for i, j in ((0, 1), (1, 0), (2, 1), (1, 3)):
                    actual_g = A.mul(A.power(old_q, i), A.power(P, j))
                    outputs = observe(mono(a=i, c=j))
                    for output in outputs:
                        expected = {}
                        for (u, v, k), value in output.items():
                            expected = A.add(expected, A.scale(A.mul(A.power(old_q, u), A.power(P, v)), value*parameter**k))
                        assert A.transvectant(H_old, actual_g, 3) == expected
                        actual_g = A.bracket(H_old, actual_g)
                        original_checks += 1
            fixtures.append({"degree": m, "shear_coefficient": str(c),
                             "R_degree": 2*m-6, "R_nonzero": True,
                             "first_order_dimension": 3, "second_order_dimension": 2})

    certificates, summaries = [], []
    for coefficients, c, bound in (({3: Q(1)}, Q(1), 6), ({4: Q(1)}, Q(-2, 3), 8)):
        cert = smith_certificate(coefficients, c, bound)
        assert verify_smith_certificate(cert)
        summaries.append({"profile": cert["profile"], "shear_coefficient": str(c), "weight_bound": bound,
                          "source_dimension": len(cert["input_basis"]),
                          "full_output_dimension": len(cert["output_coordinates"]),
                          "nonunit_exponents": [e for e in cert["nonzero_invariant_exponents"] if e]})
        if bound == 6:
            certificates.append(cert)
    forged = deepcopy(certificates[0])
    i, j = next((i, j) for i, row in enumerate(forged["matrix"]) for j, p in enumerate(row) if p)
    k = next(iter(forged["matrix"][i][j]))
    forged["matrix"][i][j][k] = str(Q(forged["matrix"][i][j][k])+1)
    try:
        verify_smith_certificate(forged)
    except AssertionError:
        pass
    else:
        raise AssertionError("forged observation matrix accepted")
    return {"format": "all-polynomial-restoring-deformation-v1", "status": "passed",
            "all_degree_theorem": "restoring_deformation.md, Theorem RD",
            "scope": "All F of degree>=3, every nonzero quadratic shear coefficient; arbitrary-degree polynomial formal corrections.",
            "first_order_initial_basis": ["1", "P", "F(P)"],
            "second_order_and_formal_initial_basis": ["1", "F(P)"],
            "q_first_order_residual": "12*c*t*(F''*F''')'",
            "P_second_order_residual": "24*c*t^2*(F''*F''')'",
            "all_N_torsion": "For N>=2degF: K[t]/t^2 plus floor(N/2)-1 copies K[t]/t",
            "profile_fixtures": fixtures, "exact_scalar_identity_checks": scalar_checks,
            "injective_commutator_calibrations": commutator_checks,
            "original_coordinate_gate_iterate_checks": original_checks,
            "smith_summaries": summaries, "smith_certificates": certificates,
            "forged_matrix_rejected": True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run()
    encoded = json.dumps(result, indent=2, sort_keys=True)+"\n"
    if args.output:
        args.output.write_text(encoded, encoding="utf-8")
    print(encoded)


if __name__ == "__main__":
    main()
