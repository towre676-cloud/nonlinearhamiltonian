#!/usr/bin/env python3
"""Exact recognition and checks for the six-dimensional shear-square core.

Uses only the standard library and the sibling independent sparse
transvectant implementation analytic_bridge_check.py.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as F
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import analytic_bridge_check as C


def recognize(H):
    """Recognize H=A(p+u(q))^2+B(p+u(q))+epsilon*q+constant.

    H maps (q_exponent,p_exponent) to exact rational coefficients.
    Return exact parameters and a six-polynomial basis, or None.
    u is normalized to have zero constant term and must have degree>=3.
    """
    H = C.clean(H)
    if any(i < 0 or j < 0 or j.denominator != 1 for i, j in H):
        return None
    if not H or max(j for _, j in H) != 2:
        return None
    A = H.get((0, F(2)), F(0))
    if not A or any(i and j == 2 for i, j in H):
        return None
    B = H.get((0, F(1)), F(0))
    u = C.clean({(i, 0): a / (2 * A) for (i, j), a in H.items()
                 if j == 1 and i})
    if not u or max(i for i, _ in u) < 3:
        return None
    Q = C.add(C.mono(0, 1), u)
    residual = C.add(H, C.scale(C.power(Q, 2), -A), C.scale(Q, -B))
    if any(j or i > 1 for i, j in residual):
        return None
    epsilon = residual.get((1, F(0)), F(0))
    constant = residual.get((0, F(0)), F(0))
    q = C.mono(1, 0)
    basis = [C.mono(0, 0), q, Q, C.power(q, 2), C.mul(q, Q), C.power(Q, 2)]
    return {"route": "SS", "core_dimension": 6, "proved": True,
            "A": A, "B": B, "epsilon": epsilon, "constant": constant,
            "u": u, "Q": Q, "basis": basis}


def compose(f, Q):
    """Substitute the original-coordinate polynomial Q for the second variable."""
    out = {}
    for (i, j), a in f.items():
        assert j.denominator == 1 and j >= 0
        out = C.add(out, C.scale(C.mul(C.mono(i, 0), C.power(Q, int(j))), a))
    return out


def d_new(f, A, B, epsilon):
    return C.add(C.scale(C.mul(C.mono(0, 1), C.derivative(f, nq=1)), -2 * A),
                 C.scale(C.derivative(f, nq=1), -B),
                 C.scale(C.derivative(f, np=1), epsilon))


def c3_new(f, u, A, B):
    first = C.mul(C.add(C.mono(0, 1, 2 * A), C.mono(0, 0, B)),
                  C.mul(C.derivative(u, nq=3), C.derivative(f, np=3)))
    second = C.scale(C.mul(C.derivative(u, nq=2),
                           C.derivative(f, nq=1, np=2)), -6 * A)
    return C.add(first, second)


def finite_kernel(u, A, B, epsilon, bound=5):
    basis = [C.mono(i, j) for i in range(bound + 1) for j in range(bound + 1 - i)]
    images = []
    for f in basis:
        row = []
        for _ in range(3):
            row.append(c3_new(f, u, A, B))
            f = d_new(f, A, B, epsilon)
        images.append(row)
    keys = sorted({(step, i, j) for image in images for step, f in enumerate(image)
                   for i, j in f})
    rows = [[image[step].get((i, j), F(0)) for image in images] for step, i, j in keys]
    dimension = len(basis) - C.rank(rows, len(basis))
    assert dimension == 6
    return {"input_monomials": len(basis), "degree_bound_in_q_Q": bound,
            "third_gate_depth": 2, "kernel_dimension": dimension,
            "full_output_coordinates": len(keys), "output_projection": False}


def run():
    us = [C.mono(3, 0), C.mono(4, 0),
          C.add(C.mono(3, 0), C.mono(2, 0, 2), C.mono(1, 0, -1)),
          C.add(C.mono(4, 0, -2), C.mono(2, 0))]
    parameters = [(F(1), F(0), F(0)), (F(2), F(3), F(0)),
                  (F(-1), F(0), F(1)), (F(3, 2), F(-2), F(-3))]
    gate_checks = evolution_checks = protected_basis_checks = recognizer_checks = 0
    sharp_depth_checks = 0
    kernels = []
    for ui, u in enumerate(us):
        Q = C.add(C.mono(0, 1), u)
        for A, B, epsilon in parameters:
            H = C.add(C.scale(C.power(Q, 2), A), C.scale(Q, B),
                      C.mono(1, 0, epsilon), C.mono(0, 0, 7))
            recognized = recognize(H)
            assert recognized and recognized["u"] == u
            assert (recognized["A"], recognized["B"], recognized["epsilon"],
                    recognized["constant"]) == (A, B, epsilon, F(7))
            recognizer_checks += 1
            for i in range(5):
                for j in range(5):
                    f = C.mono(i, j)
                    original = compose(f, Q)
                    assert C.transvectant(H, original, 3) == compose(c3_new(f, u, A, B), Q)
                    gate_checks += 1
                    assert C.bracket(H, original) == compose(d_new(f, A, B, epsilon), Q)
                    evolution_checks += 1
            for basis_element in recognized["basis"]:
                actual = C.moyal(H, basis_element)
                assert all(k == 0 for k in actual)
                protected_basis_checks += 1
            cubic_q = C.mono(3, 0)
            assert not C.transvectant(H, cubic_q, 3)
            first = C.bracket(H, cubic_q)
            assert not C.transvectant(H, first, 3)
            assert C.transvectant(H, C.bracket(H, first), 3) == C.scale(C.derivative(u, nq=2), -288 * A ** 3)
            sharp_depth_checks += 3
            kernel = finite_kernel(u, A, B, epsilon)
            kernels.append({"u_index": ui, "A": str(A), "B": str(B),
                            "epsilon": str(epsilon), **kernel})
            assert recognize(C.add(H, C.mono(2, 0))) is None
            assert recognize(C.add(H, C.mono(1, 2))) is None
            assert recognize(C.add(H, C.mono(0, 3))) is None
            recognizer_checks += 3
    quadratic_Q = C.add(C.mono(0, 1), C.mono(2, 0))
    assert recognize(C.power(quadratic_Q, 2)) is None
    recognizer_checks += 1
    # The exclusion is real: every tested Q power is protected for u=q^2.
    for j in range(3, 11):
        assert all(k == 0 for k in C.moyal(C.power(quadratic_Q, 2), C.power(quadratic_Q, j)))
        protected_basis_checks += 1
    return {"format": "shear-square-core-v1", "passed": True,
            "recognizer_checks": recognizer_checks,
            "transformed_third_gate_checks": gate_checks,
            "transformed_evolution_checks": evolution_checks,
            "protected_basis_checks": protected_basis_checks,
            "sharp_depth_checks": sharp_depth_checks,
            "finite_box_kernels": kernels,
            "all_degree_proof": "analytic_shear_square.md, Theorem SS"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    encoded = json.dumps(run(), indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(encoded, encoding="utf-8")
    print(encoded)


if __name__ == "__main__":
    main()
