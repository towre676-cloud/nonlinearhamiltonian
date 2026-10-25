#!/usr/bin/env python3
"""Exact affine-shear potential cores and sharp third-gate depths.

Proof: affine_shear_potentials.md. Standard library, exact rationals,
direct original-coordinate gates, and full-output finite kernel checks.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as F
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import analytic_bridge_check as C


def compose(f, Q):
    return C.add(*(C.scale(C.mul(C.mono(i, 0), C.power(Q, int(j))), a)
                   for (i, j), a in f.items()))


def make(A, u, V):
    Q = C.add(C.mono(0, 1), u)
    return C.add(C.scale(C.power(Q, 2), A), V), Q


def recognize(H):
    """Recognize constant kinetic coefficient with an affine completed shear.

    Input/output polynomials are sparse exact rational dictionaries. Outside
    scope returns None. A valid quadratic input returns the whole ring.
    """
    try:
        normalized = {}
        for (i, j), value in H.items():
            i, j = F(i), F(j)
            if min(i, j) < 0 or i.denominator != 1 or j.denominator != 1:
                return None
            if isinstance(value, float):
                return None
            if F(value):
                normalized[int(i), int(j)] = F(value)
    except (TypeError, ValueError, ZeroDivisionError):
        return None
    H = C.clean(normalized)
    if not H or max(j for _, j in H) != 2:
        return None
    A = H.get((0, F(2)), F(0))
    if not A or any(i and j == 2 for i, j in H):
        return None
    u = C.clean({(i, 0): a / (2 * A) for (i, j), a in H.items() if j == 1})
    if max((i for i, _ in u), default=0) > 1:
        return None
    Q = C.add(C.mono(0, 1), u)
    V = C.add(H, C.scale(C.power(Q, 2), -A))
    if any(j for _, j in V):
        return None
    n = max((i for i, _ in V), default=0)
    quadratic = n <= 2
    return {"route": "AFP", "proved": True, "A": A, "u": u,
            "Q": Q, "V": V, "degree_V": n,
            "core": "K[q,p]" if quadratic else "span{1,H}",
            "dimension": "infinite" if quadratic else 2,
            "core_dimension": "infinite" if quadratic else 2,
            "basis": None if quadratic else [C.mono(0, 0), H],
            "third_gate_depth": 0 if quadratic else (7 if n == 3 else 5),
            "all_gates_zero": quadratic,
            "proof": "affine_shear_potentials.md, Theorem AFP"}


classify = recognize


def d_new(f, A, V):
    return C.add(C.scale(C.mul(C.mono(0, 1), C.derivative(f, nq=1)), -2 * A),
                 C.mul(C.derivative(V, nq=1), C.derivative(f, np=1)))


def c3_new(f, V):
    return C.mul(C.derivative(V, nq=3), C.derivative(f, np=3))


def finite_kernel(A, V, depth, bound):
    """Full-output kernel through the specified third-gate depth."""
    basis = [C.mono(i, j) for i in range(bound + 1)
             for j in range(bound + 1 - i)]
    images = []
    for f in basis:
        row = []
        for _ in range(depth + 1):
            row.append(c3_new(f, V))
            f = d_new(f, A, V)
        images.append(row)
    keys = sorted({(r, i, j) for row in images
                   for r, f in enumerate(row) for i, j in f})
    rows = [[row[r].get((i, j), F(0)) for row in images] for r, i, j in keys]
    return {"degree_bound_in_q_Q": bound, "third_gate_depth": depth,
            "input_monomials": len(basis), "full_output_coordinates": len(keys),
            "output_projection": False,
            "kernel_dimension": len(basis) - C.rank(rows, len(basis))}


def run():
    counts = {"recognition_acceptances": 0, "recognition_rejections": 0,
              "direct_gate_checks": 0, "direct_derivation_checks": 0,
              "conditional_strip_identities": 0, "sharp_witness_checks": 0,
              "independent_pbw_operator_checks": 0, "quadratic_full_ring_checks": 0}
    us = [{}, C.mono(0, 0, 3), C.mono(1, 0, F(-2, 3)),
          C.add(C.mono(1, 0, 2), C.mono(0, 0, F(-1, 2)))]
    potentials = [C.add(C.mono(2, 0, 2), C.mono(1, 0, -3), C.mono(0, 0, 7)),
                  C.add(C.mono(3, 0, F(-2, 3)), C.mono(2, 0, 2), C.mono(0, 0)),
                  C.add(C.mono(4, 0, F(3, 2)), C.mono(2, 0, -1), C.mono(1, 0, 2)),
                  C.add(C.mono(5, 0, -1), C.mono(3, 0, 2), C.mono(0, 0, 3))]
    for A in (F(1), F(-2), F(2, 3)):
        for u in us:
            for V in potentials:
                H, Q = make(A, u, V)
                answer = recognize(H)
                assert answer and (answer["A"], answer["u"], answer["V"]) == (A, u, V)
                counts["recognition_acceptances"] += 1
                for a, c in ((0, 1), (0, 3), (1, 2), (3, 1), (2, 4)):
                    f = C.add(C.mono(a, c), C.mono(0, 0, F(1, 7)))
                    original = compose(f, Q)
                    assert C.transvectant(H, original, 3) == compose(c3_new(f, V), Q)
                    assert C.bracket(H, original) == compose(d_new(f, A, V), Q)
                    counts["direct_gate_checks"] += 1
                    counts["direct_derivation_checks"] += 1
                n = max(i for i, _ in V)
                if n <= 2:
                    assert answer["all_gates_zero"] and answer["dimension"] == "infinite"
                    for f in (C.mono(5, 7), C.mono(9, 4), C.mono(2, 8)):
                        assert not C.transvectant(H, compose(f, Q), 3)
                        counts["quadratic_full_ring_checks"] += 1
                else:
                    depth = 7 if n == 3 else 5
                    assert answer["third_gate_depth"] == depth
                    current = C.mono(1, 0)
                    for r in range(depth + 1):
                        actual = C.transvectant(H, current, 3)
                        if r < depth:
                            assert not actual, (n, r, actual)
                        else:
                            expected = (C.scale(C.power(C.derivative(V, nq=3), 3), -960 * A ** 5)
                                        if n == 3 else C.scale(C.mul(C.derivative(V, nq=3),
                                                                     C.derivative(V, nq=4)), 96 * A ** 4))
                            assert expected and actual == expected
                        counts["sharp_witness_checks"] += 1
                        current = C.bracket(H, current)
                for perturbation in (C.mono(1, 2), C.mono(2, 1), C.mono(0, 3)):
                    assert recognize(C.add(H, perturbation)) is None
                    counts["recognition_rejections"] += 1
    # Conditional strip identities are checked independently in original
    # coordinates at the precise stage where their hypotheses apply.
    for A in (F(1), F(-2, 3)):
        for V in potentials[1:]:
            u = us[-1]
            H, Q = make(A, u, V)
            c = C.add(C.mono(3, 0), C.mono(1, 0, -2))
            b = C.add(C.mono(4, 0), C.mono(0, 0))
            f = C.add(C.mono(5, 0), C.mono(2, 0, -3))
            g = C.add(C.mul(c, C.mono(0, 2)), C.mul(b, C.mono(0, 1)), f)
            actual = C.transvectant(H, C.bracket(H, compose(g, Q)), 3)
            assert actual == C.scale(C.mul(C.derivative(V, nq=3), C.derivative(c, nq=1)), -12 * A)
            counts["conditional_strip_identities"] += 1
            c = F(3, 2)
            g = C.add(C.mono(0, 2, c), C.mul(b, C.mono(0, 1)), f)
            current = compose(g, Q)
            for _ in range(2):
                current = C.bracket(H, current)
            assert C.transvectant(H, current, 3) == C.scale(
                C.mul(C.derivative(V, nq=3), C.derivative(b, nq=2)), 24 * A ** 2)
            counts["conditional_strip_identities"] += 1
            b = C.add(C.mono(1, 0, F(-2, 3)), C.mono(0, 0, 2))
            g = C.add(C.mono(0, 2, c), C.mul(b, C.mono(0, 1)), f)
            current = compose(g, Q)
            for _ in range(3):
                current = C.bracket(H, current)
            expected = C.scale(C.mul(C.derivative(V, nq=3),
                C.add(C.scale(C.derivative(V, nq=3), c),
                      C.scale(C.derivative(f, nq=3), -A))), 48 * A ** 2)
            assert C.transvectant(H, current, 3) == expected
            counts["conditional_strip_identities"] += 1
    matrices = []
    for V in potentials[1:]:
        n = max(i for i, _ in V)
        expected = {3: 6, 4: 5, 5: 4, 6: 3, 7: 2} if n == 3 else {3: 6, 4: 4, 5: 2}
        for depth, dimension in expected.items():
            receipt = finite_kernel(F(-2, 3), V, depth, n + 1)
            assert receipt["kernel_dimension"] == dimension
            matrices.append({"degree_V": n, **receipt})
        receipt = finite_kernel(F(1), V, 7 if n == 3 else 5, 2)
        assert receipt["kernel_dimension"] == 1
        matrices.append({"degree_V": n, **receipt})
    root = HERE.parents[1]
    sys.path[:0] = [str(root / "extensions" / "hamiltonian"), str(root / "extensions")]
    import weyl_receipts as W
    for V in potentials[1:]:
        A, u = F(-2, 3), us[-1]
        H, Q = make(A, u, V)
        integer_H = {(int(i), int(j)): a for (i, j), a in H.items()}
        gate, derivation = W.gate(integer_H, 3), W.derivation(integer_H)
        for a, c in ((0, 3), (1, 2), (3, 1), (2, 4)):
            f = C.mono(a, c)
            original = {(int(i), int(j)): v for (i, j), v in compose(f, Q).items()}
            assert W.act(gate, original) == compose(c3_new(f, V), Q)
            assert W.act(derivation, original) == compose(d_new(f, A, V), Q)
            counts["independent_pbw_operator_checks"] += 2
    return {"format": "affine-shear-potentials-v1", "passed": True,
            "checks": counts, "finite_box_kernels": matrices,
            "all_degree_proof": "affine_shear_potentials.md, Theorem AFP",
            "scope": "H=A(p+u(q))^2+V(q), A!=0, degu<=1, polynomialV",
            "phase_depths": {"degree_V<=2": "all gates identically zero",
                             "degree_V=3": 7, "degree_V>=4": 5},
            "limits": "Finite matrices supplement the all-degree proof; rejected inputs are unclassified by this route. No historical-priority claim."}


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
