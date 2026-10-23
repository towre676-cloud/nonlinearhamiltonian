#!/usr/bin/env python3
"""Complete the degu>=3, degP>=3 polynomial shear-composition core.

Proof and all-degree stopping rule: shear_composition_complete.md.
The checker uses exact rational arithmetic and Python's standard library.
Finite kernels retain every output coordinate; they supplement the proof.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as F
import json
from pathlib import Path
import random
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import analytic_bridge_check as C


def compose(f, Q):
    """Return f(q,Q(q,p)); the input's second variable denotes Q."""
    return C.add(*(C.scale(C.mul(C.mono(i, 0), C.power(Q, int(j))), a)
                   for (i, j), a in f.items()))


def make(P, u, epsilon=0):
    """P maps integer degrees to rationals; u is sparse in the first variable."""
    Q = C.add(C.mono(0, 1), u)
    H = C.add(*(C.scale(C.power(Q, j), F(a)) for j, a in P.items()),
              C.mono(1, 0, epsilon))
    return H, Q


def recognize(H):
    """Recognize the SCP family exactly, returning None outside its scope.

    Input maps nonnegative integer exponent pairs to rational coefficients.
    Output contains sparse exact u,Q,P and the basis [1,H]. The harmless
    normalization u(0)=0 absorbs any constant shear into P.
    """
    normalized = {}
    try:
        for (i, j), value in H.items():
            i, j = F(i), F(j)
            if i < 0 or j < 0 or i.denominator != 1 or j.denominator != 1:
                return None
            if isinstance(value, float):
                return None
            if F(value):
                normalized[int(i), int(j)] = F(value)
    except (TypeError, ValueError, ZeroDivisionError):
        return None
    H = C.clean(normalized)
    mu = int(max((j for _, j in H), default=0))
    if mu < 3:
        return None
    top = {key: a for key, a in H.items() if key[1] == mu}
    if set(top) != {(0, F(mu))}:
        return None
    rho = top[0, F(mu)]
    u = C.clean({(i, 0): a / (mu * rho) for (i, j), a in H.items()
                 if j == mu - 1 and i})
    m = max((i for i, _ in u), default=0)
    if m < 3:
        return None
    transformed = compose(H, C.add(C.mono(0, 1), C.scale(u, -1)))
    if any(i and (i, j) != (1, 0) for i, j in transformed):
        return None
    P = C.clean({(0, j): a for (i, j), a in transformed.items() if not i})
    epsilon = transformed.get((1, F(0)), F(0))
    Q = C.add(C.mono(0, 1), u)
    assert C.add(compose(P, Q), C.mono(1, 0, epsilon)) == H
    return {"route": "SCP", "proved": True,
            "core": "span{1,H}", "core_dimension": 2, "dimension": 2,
            "degree_u": m, "degree_P": mu, "u": u, "Q": Q, "P": P,
            "epsilon": epsilon, "basis": [C.mono(0, 0), H],
            "third_gate_depth": 1, "stationary": True,
            "proof": "shear_composition_complete.md, Theorem SCP"}


classify = recognize


def d_new(f, P, epsilon):
    """D in independent variables (q,Q), with P sparse in Q alone."""
    return C.add(C.scale(C.derivative(f, np=1), epsilon),
                 C.scale(C.mul(C.derivative(P, np=1),
                               C.derivative(f, nq=1)), -1))


def c3_new(f, u, P):
    """The original-coordinate third gate, expressed in (q,Q)."""
    p1, p2, p3 = [C.derivative(P, np=j) for j in (1, 2, 3)]
    return C.add(
        C.mul(C.derivative(u, nq=3),
              C.add(C.mul(p1, C.derivative(f, np=3)),
                    C.scale(C.mul(p3, C.derivative(f, np=1)), -1))),
        C.scale(C.mul(C.derivative(u, nq=2),
                      C.add(C.mul(p2, C.derivative(f, nq=1, np=2)),
                            C.mul(p3, C.derivative(f, nq=1, np=1)))), -3),
        C.scale(C.mul(p3, C.derivative(f, nq=3)), -1))


def finite_kernel(u, P, epsilon, bound):
    """Two-test kernel in a transformed total-degree box; no projection."""
    basis = [C.mono(i, j) for i in range(bound + 1)
             for j in range(bound + 1 - i)]
    images = [(c3_new(f, u, P), c3_new(d_new(f, P, epsilon), u, P))
              for f in basis]
    keys = sorted({(step, i, j) for pair in images
                   for step, f in enumerate(pair) for i, j in f})
    rows = [[pair[step].get((i, j), F(0)) for pair in images]
            for step, i, j in keys]
    dim = len(basis) - C.rank(rows, len(basis))
    expected = 2 if bound >= max(int(j) for _, j in P) else 1
    assert dim == expected, (dim, expected, bound)
    return {"degree_bound_in_q_Q": bound, "input_monomials": len(basis),
            "full_output_coordinates": len(keys), "output_projection": False,
            "kernel_dimension": dim, "expected_dimension": expected,
            "third_gate_depth": 1}


def symbolic_factor_identity():
    """Expand the coefficient identity in four independent indeterminates."""
    n = 4
    def constant(v):
        return {(0,) * n: F(v)} if v else {}
    def add(*ps):
        out = {}
        for p in ps:
            for k, v in p.items():
                out[k] = out.get(k, F(0)) + v
        return {k: v for k, v in out.items() if v}
    def scale(p, v):
        return {k: v * a for k, a in p.items() if v * a}
    def mul(*ps):
        out = constant(1)
        for p in ps:
            nxt = {}
            for k, a in out.items():
                for l, b in p.items():
                    key = tuple(x + y for x, y in zip(k, l))
                    nxt[key] = nxt.get(key, F(0)) + a * b
            out = {k: v for k, v in nxt.items() if v}
        return out
    variables = [{tuple(int(i == j) for j in range(n)): F(1)} for i in range(n)]
    a, c, m, mu = variables
    minus = lambda p, k: add(p, constant(-k))
    raw = add(mul(minus(m, 2),
                  add(mul(c, minus(c, 1), minus(c, 2)),
                      scale(mul(minus(mu, 1), minus(mu, 2), c), -1))),
              scale(mul(minus(mu, 1), a, c, minus(c, 1)), -3),
              scale(mul(minus(mu, 1), minus(mu, 2), a, c), -3))
    factored = mul(c, add(c, mu, constant(-3)),
                   add(mul(minus(m, 2), add(c, scale(mu, -1))),
                       scale(mul(minus(mu, 1), a), -3)))
    assert raw == factored
    return {"indeterminates": ["a", "c", "m", "mu"],
            "expanded_nonzero_terms": len(raw), "identity": "SCP3"}


def run():
    rng = random.Random(202610221)
    counts = {"composition_instances": 0, "recognition_acceptances": 0,
              "recognition_rejections": 0, "direct_third_gate_checks": 0,
              "direct_derivation_checks": 0, "sharp_test_checks": 0,
              "independent_pbw_operator_checks": 0,
              "leading_monomial_checks": 0, "leading_resonance_checks": 0}
    factor = symbolic_factor_identity()
    us = [C.mono(3, 0),
          C.add(C.mono(4, 0, F(-2, 3)), C.mono(2, 0), C.mono(1, 0, -2)),
          C.add(C.mono(6, 0, F(3, 2)), C.mono(3, 0, -1))]
    finite_boxes = []
    for mu in (3, 4, 5):
        for ui, u in enumerate(us):
            coefficients = {mu: F(-2 if ui == 1 else 1),
                            mu - 1: F(2, 3), 1: F(-3, 2), 0: F(7)}
            for epsilon in (F(0), F(2), F(-3, 5)):
                H, Q = make(coefficients, u, epsilon)
                P = C.clean({(0, j): a for j, a in coefficients.items()})
                answer = recognize(H)
                assert answer and answer["u"] == u and answer["P"] == P
                assert answer["epsilon"] == epsilon
                counts["composition_instances"] += 1
                counts["recognition_acceptances"] += 1
                for a, c in ((0, 1), (0, 3), (1, 0), (1, 2), (3, 1), (2, 4)):
                    f = C.add(C.mono(a, c), C.mono(0, 0, F(1, 7)))
                    original = compose(f, Q)
                    assert C.transvectant(H, original, 3) == compose(c3_new(f, u, P), Q)
                    assert C.bracket(H, original) == compose(d_new(f, P, epsilon), Q)
                    counts["direct_third_gate_checks"] += 1
                    counts["direct_derivation_checks"] += 1
                q = C.mono(1, 0)
                assert not C.transvectant(H, q, 3)
                obstruction = C.mul(C.derivative(u, nq=3),
                    C.add(C.mul(C.derivative(P, np=3), C.derivative(P, np=2)),
                          C.scale(C.mul(C.derivative(P, np=1), C.derivative(P, np=4)), -1)))
                assert obstruction
                assert C.transvectant(H, C.bracket(H, q), 3) == compose(obstruction, Q)
                assert C.transvectant(H, Q, 3) == C.scale(
                    compose(C.mul(C.derivative(u, nq=3), C.derivative(P, np=3)), Q), -1)
                assert C.transvectant(H, Q, 3)
                assert not C.transvectant(H, C.bracket(H, Q), 3)
                counts["sharp_test_checks"] += 6
                for perturbation in (C.mono(2, 0), C.mono(1, mu), C.mono(1, 1)):
                    assert recognize(C.add(H, perturbation)) is None
                    counts["recognition_rejections"] += 1
                if ui < 2 and epsilon in (0, 2):
                    finite_boxes.append({"degree_u": max(i for i, _ in u),
                        "degree_P": mu, "epsilon": str(epsilon),
                        **finite_kernel(u, P, epsilon, mu + 1)})
    # Constant shear terms are absorbed into P, rather than spuriously rejected.
    H, Q = make({3: F(2), 1: F(-1)}, C.add(C.mono(3, 0), C.mono(0, 0, 4)), F(3))
    answer = recognize(H)
    assert answer and answer["u"] == C.mono(3, 0)
    counts["recognition_acceptances"] += 1
    # The degree boundaries have different cores in the retained QC/SS results.
    for u, P in ((C.mono(2, 0), {3: 1}), (C.mono(3, 0), {2: 1}),
                 (C.mono(1, 0), {4: 1}), (C.mono(3, 0), {1: 1})):
        assert recognize(make(P, u)[0]) is None
        counts["recognition_rejections"] += 1
    for malformed in ({(0, F(3, 2)): 1}, {(0, -1): 1}, {(0, 3): 1.5}):
        assert recognize(malformed) is None
        counts["recognition_rejections"] += 1
    # Check the leading map on actual full operators, retaining lower terms.
    for m in range(3, 8):
        u = C.mono(m, 0, F(-2, 3))
        for mu in range(3, 7):
            P = C.mono(0, mu, F(3, 2))
            for _ in range(12):
                a, c = rng.randrange(7), rng.randrange(9)
                actual = c3_new(C.mono(a, c), u, P)
                degree = a + c + m + mu - 7
                top = C.clean({k: v for k, v in actual.items() if sum(k) == degree})
                coefficient = (F(-2, 3) * F(3, 2) * mu * m * (m - 1)
                               * c * (c + mu - 3)
                               * ((m - 2) * (c - mu) - 3 * (mu - 1) * a))
                expected = C.mono(a + m - 3, c + mu - 4, coefficient) if coefficient else {}
                assert top == expected
                counts["leading_monomial_checks"] += 1
            # Force a genuine positive-a resonance, including the boundary
            # m=mu=3 where the gate's total-degree shift is negative.
            a, c = m - 2, mu + 3 * (mu - 1)
            f = C.mono(a, c)
            degree = a + c + m + mu - 7
            assert not {k: v for k, v in c3_new(f, u, P).items()
                        if sum(k) == degree}
            image = c3_new(d_new(f, P, 0), u, P)
            assert any(sum(k) == degree + mu - 2 for k in image)
            counts["leading_resonance_checks"] += 2
    # A second implementation constructs original-coordinate differential
    # operators in PBW form; this does not call c3_new or C.transvectant.
    root = HERE.parents[1]
    sys.path[:0] = [str(root / "extensions" / "hamiltonian"), str(root / "extensions")]
    import weyl_receipts as W
    for mu in (3, 4):
        u = C.add(C.mono(3, 0), C.mono(1, 0, F(-1, 2)))
        coefficients = {mu: F(2), 1: F(-3), 0: F(1)}
        H, Q = make(coefficients, u, F(2, 3))
        P = C.clean({(0, j): a for j, a in coefficients.items()})
        integer_H = {(int(i), int(j)): a for (i, j), a in H.items()}
        gate, derivation = W.gate(integer_H, 3), W.derivation(integer_H)
        for a, c in ((0, 1), (1, 2), (2, 0), (2, 3), (4, 1)):
            f = C.mono(a, c)
            original = {(int(i), int(j)): v for (i, j), v in compose(f, Q).items()}
            assert W.act(gate, original) == compose(c3_new(f, u, P), Q)
            assert W.act(derivation, original) == compose(d_new(f, P, F(2, 3)), Q)
            counts["independent_pbw_operator_checks"] += 2
    return {"format": "shear-composition-complete-v1", "passed": True,
            "checks": counts, "symbolic_factor_identity": factor,
            "finite_box_kernels": finite_boxes,
            "all_degree_proof": "shear_composition_complete.md, Theorem SCP",
            "scope": "Q=p+u(q), degu>=3; H=P(Q)+epsilon*q, degP>=3",
            "limits": "Finite boxes supplement the proof; failed recognition is outside scope. No nonlinear flat-Moyal covariance or literature-priority claim."}


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
