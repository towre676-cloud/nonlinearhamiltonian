#!/usr/bin/env python3
"""Exact formal-lifting and parameter-torsion certificates for a cubic shear.

H_t=(p+q^2)^3+t*q^2.  All polynomial outputs are retained.  The source
weight bound used for a finite Smith presentation is declared, and the
all-degree lifting theorem is proved separately in cubic_deformation.md.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
from fractions import Fraction as F
import json
from pathlib import Path

import deformation_obstructions as O

mono, add, scale, mul, diff = O.mono, O.add, O.scale, O.mul, O.diff


def D(g):
    return add(scale(mul(mono(c=2), diff(g, 0)), -3),
               scale(mul(mono(a=1, t=1), diff(g, 1)), 2))


def C3(g):
    return add(scale(diff(g, 0, 3), -6),
               scale(mul(mono(c=1), diff(diff(g, 1, 2), 0)), -36),
               scale(diff(diff(g, 1), 0), -36))


def C5(g):
    return scale(diff(diff(g, 1, 4), 0), -360)


def observation(g):
    result = []
    for _ in range(4):
        result.append(C3(g))
        result.append(C5(g))
        g = D(g)
    return result


def source_basis(bound):
    return sorted([(a, c) for a in range(bound+1) for c in range(bound//2+1)
                   if a+2*c <= bound], key=lambda x: (x[0]+2*x[1], x[0]))


def observation_matrix(bound):
    basis = source_basis(bound)
    columns = [observation(mono(a=a, c=c)) for a, c in basis]
    keys = sorted({(r, a, c) for column in columns for r, p in enumerate(column)
                   for a, c, _ in p})
    matrix = [[O.clean({(0, 0, k): v for (i, j, k), v in columns[s][r].items()
                       if (i, j) == (a, c)}) for s in range(len(basis))]
              for r, a, c in keys]
    return basis, keys, matrix


def smith_certificate(bound):
    basis, keys, original = observation_matrix(bound)
    M = deepcopy(original)
    rows, cols = len(M), len(M[0])
    U, Ui, V, Vi = O.identity(rows), O.identity(rows), O.identity(cols), O.identity(cols)

    def swap_rows(i, j):
        M[i], M[j] = M[j], M[i]
        U[i], U[j] = U[j], U[i]
        for row in Ui:
            row[i], row[j] = row[j], row[i]

    def swap_columns(i, j):
        for A in (M, V):
            for row in A:
                row[i], row[j] = row[j], row[i]
        Vi[i], Vi[j] = Vi[j], Vi[i]

    def scale_row(i, v):
        M[i] = [scale(p, v) for p in M[i]]
        U[i] = [scale(p, v) for p in U[i]]
        for row in Ui:
            row[i] = scale(row[i], 1/v)

    def add_row(i, j, p):
        M[i] = [add(a, mul(p, b)) for a, b in zip(M[i], M[j])]
        U[i] = [add(a, mul(p, b)) for a, b in zip(U[i], U[j])]
        old = [row[i] for row in Ui]
        for row, x in zip(Ui, old):
            row[j] = add(row[j], scale(mul(p, x), -1))

    def add_column(i, j, p):
        for A in (M, V):
            for row in A:
                row[i] = add(row[i], mul(p, row[j]))
        Vi[j] = [add(a, scale(mul(p, b), -1)) for a, b in zip(Vi[j], Vi[i])]

    def quotient(p, exponent):
        assert all(a == c == 0 and k >= exponent for a, c, k in p)
        return {(0, 0, k-exponent): v for (_, _, k), v in p.items()}

    rank = 0
    exponents = []
    while rank < min(rows, cols):
        candidates = [(next(iter(p))[2], i, j) for i in range(rank, rows)
                      for j in range(rank, cols) if (p := M[i][j]) and len(p) == 1]
        if not candidates:
            assert not any(p for row in M[rank:] for p in row[rank:])
            break
        exponent, i, j = min(candidates)
        assert all(k >= exponent for row in M[rank:] for p in row[rank:]
                   for _, _, k in p)
        swap_rows(rank, i)
        swap_columns(rank, j)
        scale_row(rank, 1/next(iter(M[rank][rank].values())))
        for i in range(rows):
            if i != rank and M[i][rank]:
                add_row(i, rank, scale(quotient(M[i][rank], exponent), -1))
        for j in range(cols):
            if j != rank and M[rank][j]:
                add_column(j, rank, scale(quotient(M[rank][j], exponent), -1))
        exponents.append(exponent)
        rank += 1
    assert rank == cols-2
    assert exponents == sorted(exponents)
    assert [e for e in exponents if e] == [1]*(bound//2-1)+[2]
    return {"format": "cubic-shear-polynomial-smith-v1", "field": "Q",
            "weight_bound": bound, "weights": {"q": 1, "P": 2},
            "input_basis": [[a, c] for a, c in basis],
            "output_coordinates": [[r, a, c] for r, a, c in keys],
            "output_projection": False,
            "matrix": O.encode_matrix(original), "left": O.encode_matrix(U),
            "left_inverse": O.encode_matrix(Ui), "right": O.encode_matrix(V),
            "right_inverse": O.encode_matrix(Vi), "diagonal": O.encode_matrix(M),
            "nonzero_invariant_exponents": exponents,
            "zero_source_columns": 2, "free_cokernel_rank": rows-rank}


def verify_smith_certificate(cert):
    assert cert["format"] == "cubic-shear-polynomial-smith-v1"
    basis, keys, original = observation_matrix(cert["weight_bound"])
    assert cert["input_basis"] == [list(k) for k in basis]
    assert cert["output_coordinates"] == [list(k) for k in keys]
    assert cert["output_projection"] is False
    M, U, Ui, V, Vi, S = [O.decode_matrix(cert[k]) for k in
                          ("matrix", "left", "left_inverse", "right", "right_inverse", "diagonal")]
    assert M == original
    rows, cols = len(M), len(M[0])
    for A, B, dimension in ((U, Ui, rows), (Ui, U, rows), (V, Vi, cols), (Vi, V, cols)):
        assert O.polynomial_matrix_product(A, B) == O.identity(dimension)
    assert O.polynomial_matrix_product(O.polynomial_matrix_product(U, M), V) == S
    expected = [[{} for _ in range(cols)] for _ in range(rows)]
    n = cert["weight_bound"]//2
    exponents = [0]*(cols-2-n)+[1]*(n-1)+[2]
    for i, exponent in enumerate(exponents):
        expected[i][i] = mono(t=exponent)
    assert S == expected
    assert cert["nonzero_invariant_exponents"] == exponents
    return True


def run():
    p, q = mono(c=1), mono(a=1)
    h = add(mono(c=3), mono(a=2, t=1))
    assert not D(h)
    assert all(not x for x in observation(h))
    assert observation(q)[4] == mono(t=1, coefficient=432)
    assert observation(p)[6] == mono(t=2, coefficient=864)
    assert observation(mono(c=2))[2] == mono(t=1, coefficient=-144)
    assert all(not O.t_coefficient(x, order) for x in observation(p)
               for order in (0, 1))
    # First-order sufficiency must hold for all depths, not just a matrix:
    # D(P)=2tq, D^2(P)=-6tP^2, D^3(P)=-24t^2qP.
    assert D(p) == mono(a=1, t=1, coefficient=2)
    assert D(D(p)) == mono(c=2, t=1, coefficient=-6)
    assert D(D(D(p))) == mono(a=1, c=1, t=2, coefficient=-24)

    certificates, summaries = [], []
    for bound in (6, 8, 10):
        cert = smith_certificate(bound)
        assert verify_smith_certificate(cert)
        summaries.append({"weight_bound": bound,
                          "input_dimension": len(cert["input_basis"]),
                          "full_output_dimension": len(cert["output_coordinates"]),
                          "nonunit_exponents": [e for e in cert["nonzero_invariant_exponents"] if e],
                          "free_cokernel_rank": cert["free_cokernel_rank"]})
        if bound == 6:
            certificates.append(cert)
    forged = deepcopy(certificates[0])
    first = next((i, j) for i, row in enumerate(forged["matrix"])
                 for j, value in enumerate(row) if value)
    i, j = first
    key = next(iter(forged["matrix"][i][j]))
    forged["matrix"][i][j][key] = str(F(forged["matrix"][i][j][key])+1)
    try:
        verify_smith_certificate(forged)
    except AssertionError:
        pass
    else:
        raise AssertionError("edited operator matrix accepted")

    divisibility = 0
    commutator_checks = 0
    gauge_bch_checks = 0
    for a in range(9):
        for c in range(9):
            g = mono(a=a, c=c)
            outputs = observation(g)
            d0_g = O.t_coefficient(D(g), 0)
            d0_cg = O.t_coefficient(D(C3(g)), 0)
            actual = add(C3(d0_g), scale(d0_cg, -1))
            second_q = diff(g, 0, 2)
            expected = scale(mul(mono(c=1), add(second_q, mul(mono(c=1), diff(second_q, 1)))), 432)
            assert actual == expected
            commutator_checks += 1
            J = lambda p: diff(p, 1, 3)
            first = lambda p: add(J(D(p)), scale(D(J(p)), -1))
            second = lambda p: add(J(first(p)), scale(first(J(p)), -1))
            first_expected = scale(add(mul(mono(c=1), diff(diff(g, 1, 2), 0)),
                                       diff(diff(g, 1), 0)), -18)
            second_expected = scale(diff(diff(g, 1, 4), 0), -54)
            assert first(g) == first_expected
            assert second(g) == second_expected
            assert not add(J(second(g)), scale(second(J(g)), -1))
            assert add(scale(first(g), F(-1, 12)), scale(diff(g, 0, 3), F(1, 4))) == scale(C3(g), F(-1, 24))
            assert scale(second(g), F(1, 288)) == scale(C5(g), F(1, 1920))
            gauge_bch_checks += 5
            for r in (2, 3):
                zero_parameter = O.t_coefficient(outputs[2*r], 0)
                assert all(j >= 2*r-1 for _, j, _ in zero_parameter)
                divisibility += 1
    # Changes in a first lift are any element of K[P]+Kq. Their
    # first variation in depth three has zero constant coefficient.
    first_lift_independence = 0
    for g in [q]+[mono(c=n) for n in range(16)]:
        assert O.constant_coefficient(O.t_coefficient(observation(g)[6], 1)) == 0
        first_lift_independence += 1

    # Independent original-coordinate transvectant checks.
    import analytic_bridge_check as A
    old_q, old_p = A.mono(1, 0), A.mono(0, 1)
    P = A.add(old_p, A.power(old_q, 2))
    original_checks = 0
    for parameter in (F(0), F(1), F(-2), F(2, 3)):
        H = A.add(A.power(P, 3), A.mono(2, 0, parameter))
        for a in range(4):
            for c in range(4):
                g_original = A.mul(A.power(old_q, a), A.power(P, c))
                images = observation(mono(a=a, c=c))
                for r in range(4):
                    for gate, idx in ((3, 2*r), (5, 2*r+1)):
                        expected = {}
                        for (i, j, k), value in images[idx].items():
                            term = A.scale(A.mul(A.power(old_q, i), A.power(P, j)), value*parameter**k)
                            expected = A.add(expected, term)
                        assert A.transvectant(H, g_original, gate) == expected
                        original_checks += 1
                    g_original = A.bracket(H, g_original)

    return {"format": "cubic-shear-deformation-v1", "status": "passed",
            "all_degree_theorem": "cubic_deformation.md, Theorem CD",
            "initial_core": "K[P]+Kq", "first_order_liftable_initial_dimension": 3,
            "first_order_liftable_initial_basis": ["1", "P", "P^3"],
            "second_order_and_formal_initial_dimension": 2,
            "second_order_and_formal_initial_basis": ["1", "P^3"],
            "q_first_order_residual": "432*t", "P_second_order_residual": "864*t^2",
            "P_square_first_order_residual": "-144*t",
            "smith_summaries": summaries, "smith_certificates": certificates,
            "all_bound_torsion_law": "For N>=6: K[t]/(t^2) plus floor(N/2)-1 copies K[t]/(t)",
            "arbitrary_degree_divisibility_calibrations": divisibility,
            "commutator_identity_calibrations": commutator_checks,
            "gauge_bch_identity_calibrations": gauge_bch_checks,
            "first_lift_independence_calibrations": first_lift_independence,
            "original_coordinate_gate_iterate_checks": original_checks,
            "forged_matrix_rejected": True,
            "scope": "Universal claims rest on written all-degree arguments. N in Smith presentations is declared; the torsion law is proved for every N>=6, not extrapolated from computed matrices."}


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
