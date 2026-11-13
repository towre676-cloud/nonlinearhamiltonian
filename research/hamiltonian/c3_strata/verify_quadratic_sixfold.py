"""Exact replay for H = p^2 + b(q) p + f(q), deg f = 6, deg b <= 4.

Companion to QUADRATIC_SIXFOLD_THEOREM.md.  Every kernel is computed by the
independent defining-star engine through verify_sextic_core.kernel_on_monomials
on inputs of bounded total degree with untruncated gate outputs.  Those
comparisons are bounded evidence for the theorem; the all-degree statements
are proved in the note.  The witness and invariance checks are unbounded exact
identities on the named polynomials.  Prints a deterministic JSON receipt and
writes no files.

    python research/hamiltonian/c3_strata/verify_quadratic_sixfold.py
"""
from __future__ import annotations

from fractions import Fraction as F
import argparse
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE)]
import verify_sextic_core as V  # noqa: E402

E = V.E
X = {(1, 0): F(1)}
Y = {(0, 1): F(1)}
ONE = {(0, 0): F(1)}


def source_hashes(*extra):
    """SHA-256 of the sources a receipt depends on, by repository-relative path."""
    base = [HERE.parent / "sextic_core.py", HERE.parent / "independent" / "engine.py",
            HERE.parent / "partner_lab.py", HERE / "verify_sextic_core.py",
            HERE / "verify_quadratic_sixfold.py"]
    return {str(path.relative_to(HERE.parents[2])): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in sorted(set(base) | set(extra))}


def uni(coefficients):
    """Polynomial in q from ascending coefficients."""
    return {(i, 0): F(c) for i, c in enumerate(coefficients) if c}


def udeg(poly):
    return max((a for a, _ in poly), default=-1)


def uderiv(poly, order=1):
    return E.derivative(poly, q=order)


def hamiltonian(f, b):
    return E.add(E.power(Y, 2), E.multiply(b, Y), f)


def shifted(b):
    """P = p + b(q)/2."""
    return E.add(Y, E.scale(b, F(1, 2)))


def potential(f, b):
    """F = f - b^2/4, so that H = P^2 + F(q)."""
    return E.add(f, E.scale(E.multiply(b, b), F(-1, 4)))


def from_shifted(G, b):
    """Rewrite G(q, P) as a polynomial in (q, p) by P = p + b/2."""
    P = shifted(b)
    out = {}
    for (i, j), c in G.items():
        out = E.add(out, E.scale(E.multiply({(i, 0): F(1)}, E.power(P, j)), c))
    return out


def regime(f, b):
    """Exact recognizer for the branch of the theorem."""
    V.require(udeg(f) == 6 and udeg(b) <= 4, "Need deg f = 6 and deg b <= 4")
    if udeg(b) <= 1:
        return "affine_shift"
    n = udeg(potential(f, b))
    if n >= 4:
        return "generic_nonlinear"
    return "cubic_potential" if n == 3 else "hidden_quadratic"


SHARP_DEPTH = {"affine_shift": 5, "generic_nonlinear": 4,
               "cubic_potential": 6, "hidden_quadratic": 2}


def monomials(degree, p_degree=None):
    return [{(a, d - a): F(1)} for d in range(degree + 1) for a in range(d + 1)
            if p_degree is None or d - a <= p_degree]


def predicted(f, b, stage, degree):
    """Spanning set of the proved S^stage intersected with total degree <= degree.

    Requires degree >= 6 so that every finite generator of S^1, S^2, ... fits.
    """
    V.require(degree >= 6, "Bounded comparison needs degree >= 6")
    H, P, kind = hamiltonian(f, b), shifted(b), regime(f, b)
    xs = [{(i, 0): F(1)} for i in range(degree + 1)]
    low = [ONE, X, E.power(X, 2)]
    xP = E.multiply(X, P)
    if kind == "affine_shift":
        table = [
            monomials(degree, 2),
            xs + [E.multiply({(i, 0): F(1)}, Y) for i in range(degree)] + [E.power(Y, 2)],
            xs + [Y, E.multiply(X, Y), E.power(Y, 2)],
            low + [P, xP, H],
            low + [H],
        ]
        return table[stage] if stage < 5 else [ONE, H]
    if stage == 0:
        return static_space(f, b, degree)
    if stage == 1:
        return xs + [Y, E.multiply(X, Y), H]
    six = low + [P, xP, H]
    if stage == 2 or kind == "hidden_quadratic":
        return six
    if kind == "generic_nonlinear":
        return low + [H] if stage == 3 else [ONE, H]
    table = {3: low + [P, H], 4: [ONE, X, P, H], 5: [ONE, X, H]}
    return table.get(stage, [ONE, H])


def static_extras(f, b):
    """The two static partners beyond W when deg b = 2 (Theorem B, part (a)).

    With beta = b'' they are p^3 + (f''/beta) p^2 and
    p^4 + (4 f''/(3 beta)) p^3 + (2 f''^2/(3 beta^2)) p^2, of total degrees 6 and 10.
    """
    if udeg(b) != 2:
        return []
    beta = uderiv(b, 2)[(0, 0)]
    f2 = uderiv(f, 2)
    return [
        E.add(E.power(Y, 3), E.scale(E.multiply(f2, E.power(Y, 2)), 1 / beta)),
        E.add(E.power(Y, 4), E.scale(E.multiply(f2, E.power(Y, 3)), F(4, 3) / beta),
              E.scale(E.multiply(E.multiply(f2, f2), E.power(Y, 2)), F(2, 3) / beta ** 2)),
    ]


def static_space(f, b, degree):
    """Proved S^0 for b'' != 0, restricted to total degree <= degree.

    W = K[q] + K[q] p + K p^2, plus the two extras when deg b = 2.
    """
    out = [{(i, 0): F(1)} for i in range(degree + 1)]
    out += [E.multiply({(i, 0): F(1)}, Y) for i in range(degree)]
    out.append(E.power(Y, 2))
    return out + [G for G in static_extras(f, b) if V.total_degree(G) <= degree]


def kernels(H, degree, depth):
    """Bounded S^0..S^depth, sharing the iterates between stages.

    Same rows as verify_sextic_core.kernel_on_monomials, which recomputes the
    iterates for each stage; agreement is asserted in verify().
    """
    exponents = [(a, d - a) for d in range(degree + 1) for a in range(d + 1)]
    current = [{e: F(1)} for e in exponents]
    images = [{} for _ in exponents]
    out = []
    for iterate in range(depth + 1):
        for image, poly in zip(images, current):
            for hbar, defect in E.defects(H, poly).items():
                for (a, b), coefficient in defect.items():
                    image[iterate, hbar, a, b] = coefficient
        keys = sorted({key for image in images for key in image})
        rows = [[image.get(key, F(0)) for image in images] for key in keys]
        out.append([{e: c for e, c in zip(exponents, vector) if c}
                    for vector in V.nullspace(rows, len(exponents))])
        if iterate < depth:
            current = [E.poisson(H, poly) for poly in current]
    return out


def first_failure(H, G, limit=12):
    """Least i with a nonzero odd gate on D_H^i G, or None up to limit."""
    current = G
    for i in range(limit + 1):
        if E.defects(H, current):
            return i
        current = E.poisson(H, current)
    return None


def check_gate_formula(f, b):
    """Odd gates in the shifted variables, against the defining star product.

    T3 = (F''' + b''' P) G_PPP - 3 b'' G_qPP,
    T5 = (f^(5) - 5 b'''' b'/2) G_PPPPP - 5 b'''' G_qPPPP,
    D_H = F' d_P - 2 P d_q, all derivatives in the (q, P) chart.
    """
    H, Fq = hamiltonian(f, b), potential(f, b)
    probes = [
        {(2, 3): F(1), (1, 5): F(-2), (3, 4): F(1, 3), (0, 6): F(5), (4, 2): F(7)},
        {(1, 4): F(3), (5, 3): F(-1), (2, 5): F(2), (0, 2): F(1), (3, 1): F(4)},
    ]
    for G in probes:
        d = lambda q=0, p=0: E.derivative(G, q=q, p=p)
        t3 = E.add(
            E.multiply(E.add(uderiv(Fq, 3), E.multiply(uderiv(b, 3), Y)), d(p=3)),
            E.scale(E.multiply(uderiv(b, 2), d(q=1, p=2)), -3))
        t5 = E.add(
            E.multiply(E.add(uderiv(f, 5),
                             E.scale(E.multiply(uderiv(b, 4), uderiv(b, 1)), F(-5, 2))),
                       d(p=5)),
            E.scale(E.multiply(uderiv(b, 4), d(q=1, p=4)), -5))
        dh = E.add(E.multiply(uderiv(Fq, 1), d(p=1)),
                   E.scale(E.multiply(Y, d(q=1)), -2))
        g = from_shifted(G, b)
        defects = E.defects(H, g)
        V.require(defects.get(2, {}) == E.scale(from_shifted(t3, b), F(-1, 24)),
                  "Shifted T3 formula disagrees with the star product")
        V.require(defects.get(4, {}) == E.scale(from_shifted(t5, b), F(1, 1920)),
                  "Shifted T5 formula disagrees with the star product")
        V.require(E.poisson(H, g) == from_shifted(dh, b),
                  "Shifted Poisson derivation disagrees")


def _square_plus(beta, extra):
    """Ascending coefficients of beta(q)^2 + extra(q)."""
    out = [0] * 7
    for i, x in enumerate(beta):
        for j, y in enumerate(beta):
            out[i + j] += x * y
    for i, x in enumerate(extra):
        out[i] += x
    return out


_BETA = [1, -3, 1, 1]          # b = 2 beta, so H = (p + beta)^2 + extra
_B = [2 * c for c in _BETA]
CASES = [
    # name, f ascending, b ascending
    ("calibration q^6+p^2", [0, 0, 0, 0, 0, 0, 1], []),
    ("b=0 generic f", [1, 7, -1, 5, 1, -3, 2], []),
    ("b affine", [1, 7, -1, 5, 1, -3, 2], [-2, 3]),
    ("holdout q^6+q^2 p+p^2", [0, 0, 0, 0, 0, 0, 1], [0, 0, 1]),
    ("deg b=2 generic", [1, 7, -1, 5, 1, -3, 2], [3, 1, -2]),
    ("deg b=3, N=6", [1, 7, -1, 5, 1, -3, 2], [4, 0, -1, 2]),
    ("deg b=3, N=5", _square_plus(_BETA, [2, 0, -1, 0, 1, 3]), _B),
    ("deg b=3, N=4", _square_plus(_BETA, [0, 1, 3, -1, -2]), _B),
    ("deg b=3, N=3", _square_plus(_BETA, [4, 5, 1, -2]), _B),
    ("(p+q^3)^2+q^3", [0, 0, 0, 1, 0, 0, 1], [0, 0, 0, 2]),
    ("deg b=3, N=2", _square_plus(_BETA, [0, -1, 3]), _B),
    ("deg b=3, N=1", _square_plus(_BETA, [0, 5]), _B),
    ("holdout (p+q^3)^2", [0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 2]),
    ("holdout q^6+q^4 p+p^2", [0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 1]),
    ("deg b=4 generic", [1, 7, -1, 5, 1, -3, 2], [1, 2, 0, -1, 3]),
]
EXPECTED_REGIME = [
    "affine_shift", "affine_shift", "affine_shift",
    "generic_nonlinear", "generic_nonlinear", "generic_nonlinear",
    "generic_nonlinear", "generic_nonlinear", "cubic_potential",
    "cubic_potential", "hidden_quadratic", "hidden_quadratic",
    "hidden_quadratic", "generic_nonlinear", "generic_nonlinear",
]
COVARIANCE = [  # case index, matrix, shift, scalar, constant
    (1, ((2, 1), (1, 3)), (1, -2), F(3, 2), 5),
    (4, ((1, 2), (-1, 3)), (F(1, 2), 1), -2, 1),
    (8, ((3, 1), (2, 2)), (-1, 2), F(2, 3), -4),
    (11, ((1, 1), (0, 2)), (2, F(-1, 3)), 5, 0),
    (14, ((2, -1), (1, 1)), (0, 1), F(-1, 2), 2),
]


def check_case(name, f, b, degree, depth):
    f, b = uni(f), uni(b)
    H, P, kind = hamiltonian(f, b), shifted(b), regime(f, b)
    sharp = SHARP_DEPTH[kind]
    check_gate_formula(f, b)
    dims = []
    for stage, found in enumerate(kernels(H, degree, depth)):
        dims.append(len(found))
        V.require(V.same_span(found, predicted(f, b, stage, degree)),
                  f"{name}: bounded S^{stage} differs from the theorem")
    for G in static_extras(f, b):
        V.require(first_failure(H, G) == 1,
                  f"{name}: a static extra should lie in S^0 and fail S^1")
    # Unbounded exact checks on named polynomials.
    core = [ONE, H] if kind != "hidden_quadratic" else [
        ONE, X, E.power(X, 2), P, E.multiply(X, P), H]
    for G in core:
        V.require(V.span_rank(core + [E.poisson(H, G)]) == len(core),
                  f"{name}: core is not D_H-invariant")
        V.require(not E.defects(H, G), f"{name}: core fails a static gate")
    if kind == "hidden_quadratic":
        witness, label = E.power(X, 3), "q^3"
        V.require(first_failure(H, E.multiply(E.power(X, 2), Y)) == 1,
                  f"{name}: q^2 p should lie in S^0 and fail S^1")
        V.require(first_failure(H, witness) == 2, f"{name}: q^3 should fail first at S^2")
    else:
        witness, label = X, "q"
        V.require(first_failure(H, witness) == sharp,
                  f"{name}: q should lie in S^{sharp - 1} and fail S^{sharp}")
    return {
        "name": name,
        "H": V.E.serialize(H),
        "deg_b": udeg(b),
        "deg_F": udeg(potential(f, b)),
        "regime": kind,
        "bounded_dimensions": dims,
        "static_dimension_beyond_W": len(static_extras(f, b)) if kind != "affine_shift" else None,
        "sharp_depth": sharp,
        "core_dimension": len(core),
        "sharpness_witness": label,
    }


def check_covariance(index, matrix, shift, scalar, constant, degree, depth):
    _, f, b = CASES[index]
    H = hamiltonian(uni(f), uni(b))
    moved = V.sparse_add(V.affine_substitute(H, matrix, shift, scalar),
                         {(0, 0): F(constant)})
    (a, b_), (c, d) = matrix
    V.require(a * d - b_ * c not in (0, 1, -1), "Use a nonunimodular test matrix")
    dims = []
    for stage, (here, there) in enumerate(zip(kernels(moved, degree, depth),
                                              kernels(H, degree, depth))):
        pulled = [V.affine_substitute(G, matrix, shift) for G in there]
        V.require(V.same_span(here, pulled),
                  f"Covariance failure for case {index} at stage {stage}")
        dims.append(len(here))
    return {"case": CASES[index][0], "determinant": str(F(a * d - b_ * c)),
            "scalar": str(F(scalar)), "bounded_dimensions": dims}


STATIC_PROBES = (3, 4, 5, 8, 12, 14)


def verify(degree=6, depth=7, static_degree=12):
    V.require(len(CASES) == len(EXPECTED_REGIME), "Fixture table mismatch")
    cases = []
    for (name, f, b), want in zip(CASES, EXPECTED_REGIME):
        V.require(regime(uni(f), uni(b)) == want, f"{name}: unexpected regime")
        cases.append(check_case(name, f, b, degree, depth))
    covariance = [check_covariance(*row, degree, depth) for row in COVARIANCE]
    # The shared-iterate solver agrees with the maintained bounded solver.
    exponents = [(a, d - a) for d in range(degree + 1) for a in range(d + 1)]
    for index in (0, 9):
        H = hamiltonian(uni(CASES[index][1]), uni(CASES[index][2]))
        for stage, found in enumerate(kernels(H, degree, depth)):
            V.require(found == V.kernel_on_monomials(H, exponents, stage),
                      "Shared-iterate kernel differs from kernel_on_monomials")
    static = []
    for index in STATIC_PROBES:
        name, f, b = CASES[index]
        f, b = uni(f), uni(b)
        found = kernels(hamiltonian(f, b), static_degree, 0)[0]
        V.require(V.same_span(found, static_space(f, b, static_degree)),
                  f"{name}: bounded S^0 at degree {static_degree} differs from the theorem")
        static.append({"name": name, "input_degree": static_degree,
                       "dimension": len(found)})
    receipt = {
        "status": "PASS",
        "claim_boundary": ("Kernel comparisons use inputs of total degree <= "
                           f"{degree} with untruncated gate outputs, stages 0..{depth}. "
                           "They are bounded evidence. Witness, invariance and "
                           "shifted-gate checks are exact polynomial identities."),
        "input_degree": degree,
        "depth": depth,
        "cases": cases,
        "rational_affine_covariance": covariance,
        "static_probes": static,
        "source_sha256": source_hashes(),
    }
    text = json.dumps(receipt, sort_keys=True, separators=(",", ":"))
    receipt["payload_sha256"] = hashlib.sha256(text.encode()).hexdigest()
    return receipt


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--degree", type=int, default=6)
    parser.add_argument("--depth", type=int, default=7)
    args = parser.parse_args()
    print(json.dumps(verify(args.degree, args.depth), indent=1, sort_keys=True))
