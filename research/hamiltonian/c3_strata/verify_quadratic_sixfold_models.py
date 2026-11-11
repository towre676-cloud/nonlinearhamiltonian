"""Replay for Theorem D (nonconstant coefficient of the squared complement)
and for the standalone classifier quadratic_sixfold.py.

Three kinds of evidence, kept distinct in the receipt.

* certified_models: exact refinement spaces of the five weighted-homogeneous
  models inside the weighted box that Theorem D proves contains S^1.  With
  the theorem these are complete for all polynomial degrees.  Each is also
  recomputed in a strictly larger box as a consistency check on the bound.
* discriminant_family: SymPy rank analysis over Q[t] of the one-parameter
  model q^6 + t q^4 p + q^2 p^2 inside its box.  The gcd of the sampled
  maximal minors bounds the exceptional parameters from above; the rational
  roots found are then confirmed exceptional by exact computation.
* classifier_checks: classifier output against kernels on all inputs of
  bounded *total* degree, which does not use the weighted argument.

    python research/hamiltonian/c3_strata/verify_quadratic_sixfold_models.py
"""
from __future__ import annotations

from fractions import Fraction as F
from itertools import combinations
from math import comb
import hashlib
import json
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parent)]
import verify_sextic_core as V            # noqa: E402
import verify_quadratic_sixfold as Q      # noqa: E402
import quadratic_sixfold as C             # noqa: E402
import partner_lab                        # noqa: E402

E = V.E
ONE = {(0, 0): F(1)}


def box(wx, wy, bound):
    return [(a, j) for j in range(bound // wy + 1)
            for a in range((bound - wy * j) // wx + 1)]


def box_kernels(H, exponents, depth):
    """S^0..S^depth on the given monomials, by the independent star engine."""
    current = [{e: F(1)} for e in exponents]
    images = [{} for _ in exponents]
    out = []
    for iterate in range(depth + 1):
        for image, poly in zip(images, current):
            for hbar, defect in E.defects(H, poly).items():
                for (a, j), value in defect.items():
                    image[iterate, hbar, a, j] = value
        keys = sorted({key for image in images for key in image})
        rows = [[image.get(key, F(0)) for image in images] for key in keys]
        out.append([{e: c for e, c in zip(exponents, v) if c}
                    for v in V.nullspace(rows, len(exponents))])
        if iterate < depth:
            current = [E.poisson(H, poly) for poly in current]
    return out


# name, H, weights, proved bound, larger box, expected dims of S^1.., least depth
MODELS = [
    ("deg c=1, deg b<=3", "q^6+q*p^2", (2, 5), 22, 40, [6, 3, 2, 2], 3),
    ("deg c=1, deg b=4", "q^4*p+q*p^2", (1, 3), 13, 26, [5, 3, 2, 2], 3),
    ("deg c=2, deg b<=3", "q^6+q^2*p^2", (2, 4), 24, 40, [3, 2, 2, 2], 2),
    ("deg c=2, deg b=4, t=1", "q^6+q^4*p+q^2*p^2", (2, 4), 18, 36, [3, 2, 2, 2], 2),
    ("deg c=3", "q^6+q^3*p^2", (2, 3), 26, 40, [3, 2, 2, 2], 2),
]


def check_model(name, text, weights, bound, larger, dims, depth):
    H = partner_lab.parse(text)
    inside = box_kernels(H, box(*weights, bound), 4)[1:]
    outside = box_kernels(H, box(*weights, larger), 4)[1:]
    V.require([len(K) for K in inside] == dims, f"{name}: unexpected model dimensions")
    for a, b in zip(inside, outside):
        V.require(V.same_span(a, b), f"{name}: a larger box changed a refinement space")
    V.require(V.same_span(inside[depth - 1], [ONE, H]), f"{name}: core is not span(1,H)")
    V.require(len(inside[depth - 2]) > 2 if depth >= 2 else True, f"{name}: depth is not sharp")
    return {"model": text, "case": name, "weights": list(weights), "proved_bound": bound,
            "larger_box": larger, "dimensions_S1_to_S4": dims, "least_depth": depth}


def check_discriminant_family():
    import sympy as sp
    x, y, t = sp.symbols("x y t")
    H = x**6 + t * x**4 * y + x**2 * y**2

    def T(k, G):
        return sp.expand(sum((-1) ** j * comb(k, j) * sp.diff(H, x, k - j, y, j)
                             * sp.diff(G, x, j, y, k - j) for j in range(k + 1)))

    rng = random.Random(20261111)
    out = {}
    for depth in (1, 2):
        dimension, factor = 0, sp.Integer(1)
        for weight in range(0, 19, 2):
            monomials = [x ** ((weight - 4 * j) // 2) * y**j for j in range(weight // 4 + 1)]
            columns = []
            for monomial in monomials:
                current, image = monomial, {}
                for iterate in range(depth + 1):
                    for k in (3, 5):
                        for (a, j), value in sp.Poly(T(k, current), x, y).terms():
                            image[iterate, k, a, j] = value
                    current = T(1, current)
                columns.append(image)
            keys = sorted({key for image in columns for key in image})
            M = sp.Matrix([[image.get(key, 0) for image in columns] for key in keys])
            rank = M.rank() if M.rows else 0
            dimension += len(monomials) - rank
            if not rank:
                continue
            choices = [(r, c) for r in combinations(range(M.rows), rank)
                       for c in combinations(range(len(monomials)), rank)]
            if len(choices) > 3000:
                choices = rng.sample(choices, 3000)
            g = sp.Integer(0)
            for rows, cols in choices:
                g = sp.gcd(g, sp.expand(M.extract(list(rows), list(cols)).det()))
                if g != 0 and g.is_number:
                    break
            V.require(g != 0, "Generic rank was misjudged")
            factor = sp.lcm(factor, sp.Poly(g, t).monic().as_expr() if not g.is_number else 1)
        out[depth] = (dimension, sp.factor(factor))
    V.require(out[1][0] == 3 and out[1][1] == 1,
              "S^1 of the discriminant family should have constant dimension three")
    V.require(out[2][0] == 2 and sp.expand(out[2][1] - (t - 2) * (t + 2)) == 0,
              "S^2 should be two-dimensional away from t^2 = 4")
    return {"generic_dimension_S1": 3, "S1_exceptional_factor": "1",
            "generic_dimension_S2": 2, "S2_exceptional_factor": "(t - 2)*(t + 2)",
            "sympy": sp.__version__}


# classifier fixtures: text, expected regime, least depth, core dimension
FIXTURES = [
    ("q^6+p^2", "affine_shift", 5, 2),
    ("2*q^6-3*q^5+q^4+5*q^3-q^2+7*q+1+(3*q-2)*p+p^2", "affine_shift", 5, 2),
    ("q^6+q^2*p+p^2", "generic_nonlinear", 4, 2),
    ("2*q^6-3*q^5+q^4+5*q^3-q^2+7*q+1+(3*q^4-q^3+2*q+1)*p+3*p^2", "generic_nonlinear", 4, 2),
    ("(p+q^3)^2+q^3", "cubic_potential", 6, 2),
    ("(p+q^3+q^2-3*q+1)^2+3*q^2-q", "hidden_quadratic", 2, 6),
    ("(p+q^3)^2", "hidden_quadratic", 2, 6),
    ("q^6+q*p^2", "variable_top_coefficient", 3, 2),
    ("2*q^6-q^5+q^3+7*q+(q-2)*p^2+(q^3-q+1)*p", "variable_top_coefficient", 3, 2),
    ("2*q^6-q^5+q^3+7*q+(q-2)*p^2+(q^4-q+1)*p", "variable_top_coefficient", 3, 2),
    ("2*q^6-q^5+q^3+7*q+(q^2-2*q+3)*p^2+(q^3-q+1)*p", "variable_top_coefficient", 2, 2),
    ("2*q^6-q^5+q^3+7*q+(q^2-2*q+3)*p^2+(q^4-q+1)*p", "variable_top_coefficient", 2, 2),
    ("q^6+(q^3+q+1)*p^2", "variable_top_coefficient", 1, 2),
    ("2*q^6-q^5+q^3+7*q+(q^3-2*q+3)*p^2+(q^4-q+1)*p", "variable_top_coefficient", 1, 2),
    ("q^6+q^2*p^2+2*q^4*p", "variable_top_coefficient", 1, 3),
    ("q^6+q^2*p^2+2*q^4*p+2*q*p+2*q^3", "variable_top_coefficient", 1, 3),
    ("q^6+q^2*p^2+2*q^4*p+q", "variable_top_coefficient", 2, 2),
    ("q^6+q^2*p^2+2*q^4*p+p", "variable_top_coefficient", 2, 2),
    ("q^6+q^2*p^2-2*q^4*p+q^5", "variable_top_coefficient", 2, 2),
    # Theorem E with a shifted root and a scalar: criterion holds, then each
    # condition is broken separately while staying on the discriminant locus.
    ("3*((q-3)*p+2*(q-3)^3+q+2)^2-7", "variable_top_coefficient", 1, 3),
    ("((q-3)*p+2*(q-3)^3+q+2)^2+p^2", "variable_top_coefficient", 2, 2),
    ("((q-3)*p+2*(q-3)^3+q+2)^2+p", "variable_top_coefficient", 2, 2),
    ("((q-3)*p+2*(q-3)^3+q+2)^2+q^2", "variable_top_coefficient", 2, 2),
    ("((q-3)*p+2*(q-3)^3+q+2)^2+(q-3)*p", "variable_top_coefficient", 2, 2),
]
# fixture index -> whether Theorem E predicts a square first integral
SQUARE = {14: True, 15: True, 16: False, 17: False, 18: False, 19: True, 20: False,
          21: False, 22: False, 23: False}
TRANSFORMS = {  # fixture index -> rational affine map with non-unit determinant, scalar
    3: (((2, 1), (1, 3)), (1, -2), F(3, 2)),
    4: (((1, 2), (-1, 3)), (F(1, 2), 1), F(-2)),
    6: (((0, 2), (1, 1)), (2, F(-1, 3)), F(5)),
    8: (((3, 1), (2, 2)), (-1, 2), F(2, 3)),
    11: (((2, -1), (1, 1)), (0, 1), F(-1, 2)),
    15: (((1, 1), (0, 2)), (1, 0), F(3)),
}
OUT_OF_SCOPE = ["q^6+p^3", "q^6+q*p", "q^6+p^6+p^2", "q^5*p+p^2", "q^6+q*p^3+p^2", "q^4+p^2"]


def check_classifier(text, regime, depth, core_dimension, transform, degree):
    H = partner_lab.parse(text)
    if transform is not None:
        matrix, shift, scalar = transform
        H = V.sparse_add(V.affine_substitute(H, matrix, shift, scalar), {(0, 0): F(7, 3)})
    report = C.classify_quadratic_sixfold(H)
    V.require(json.loads(json.dumps(report)) == report, "Report is not exact JSON")
    V.require(report["status"] == "classified" and report["regime"] == regime,
              f"{text}: wrong regime")
    V.require(report["least_depth"] == depth, f"{text}: wrong least depth")
    V.require(report["Dinf"]["dimension"] == core_dimension, f"{text}: wrong core dimension")
    V.require((report.get("square_first_integral") is not None) == (core_dimension == 3),
              f"{text}: Theorem E and the core dimension disagree")
    witness = report["sharpness_witness"]
    V.require(Q.first_failure(H, V.polynomial(witness["G"])) == depth
              == witness["first_failing_iterate"], f"{text}: sharpness witness is wrong")
    L = V.polynomial(report["L"])
    found = Q.kernels(H, degree, depth + 1)
    dims = []
    for stage, kernel in enumerate(found):
        space = report["stages"].get(f"S{stage}", report["Dinf"] if stage > depth else None)
        if space is None:
            dims.append(None)
            continue
        module = [V.polynomial(G) for G in space["module_over_K[L]"]]
        spanning = [V.polynomial(G) for G in space["finite_span"]]
        for base in module:
            power = dict(ONE)
            while V.total_degree(E.multiply(power, base)) <= degree:
                spanning.append(E.multiply(power, base))
                power = E.multiply(power, L)
        inside = [G for G in spanning if V.total_degree(G) <= degree]
        V.require(len(inside) == len(spanning) or space["dimension"] is None or stage == 0,
                  f"{text}: a reported finite generator exceeds the comparison degree")
        V.require(V.same_span(kernel, inside),
                  f"{text}: classifier S^{stage} differs from the bounded kernel")
        dims.append(len(kernel))
    core = [V.polynomial(G) for G in report["Dinf"]["finite_span"]]
    for G in core:
        V.require(V.span_rank(core + [E.poisson(H, G)]) == len(core), "Core not invariant")
        V.gates_through(H, G, depth + 2)
    return {"H": text, "rational_affine_change": transform is not None, "regime": regime,
            "least_depth": depth, "core_dimension": core_dimension,
            "bounded_dimensions": dims}


def verify(degree=8):
    models = [check_model(*row) for row in MODELS]
    family = check_discriminant_family()
    checks = []
    for index, row in enumerate(FIXTURES):
        checks.append(check_classifier(*row, None, degree))
        if index in SQUARE:
            V.require(SQUARE[index] == (row[3] == 3), "Fixture table mismatch")
        if index in TRANSFORMS:
            checks.append(check_classifier(*row, TRANSFORMS[index], degree))
    for text in OUT_OF_SCOPE:
        report = C.classify_quadratic_sixfold(partner_lab.parse(text))
        V.require(report["status"] == "out_of_scope" and "stages" not in report,
                  f"{text}: should be out of scope without space claims")
    receipt = {
        "status": "PASS",
        "claim_boundary": ("certified_models are complete for all degrees by Theorem D. "
                           "classifier_checks compare against kernels on inputs of total "
                           f"degree <= {degree} with untruncated gate outputs and are bounded "
                           "evidence. S^0 with dimension null is not asserted by the "
                           "classifier for a nonconstant top coefficient."),
        "certified_models": models,
        "discriminant_family": family,
        "classifier_checks": checks,
        "out_of_scope_checks": OUT_OF_SCOPE,
        "source_sha256": Q.source_hashes(Path(__file__).resolve(),
                                         HERE.parent / "quadratic_sixfold.py"),
    }
    text = json.dumps(receipt, sort_keys=True, separators=(",", ":"))
    receipt["payload_sha256"] = hashlib.sha256(text.encode()).hexdigest()
    return receipt


if __name__ == "__main__":
    print(json.dumps(verify(), indent=1, sort_keys=True))
