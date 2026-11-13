"""All-degree cores for lower-weight perturbations of separable binomials.

The written weighted-transfer theorem supplies a complete static envelope.
Every kernel and Poisson preimage is computed without projecting its output.
"""
from __future__ import annotations

from fractions import Fraction as F
from importlib import util
from math import gcd
from pathlib import Path

_spec = util.spec_from_file_location("_weighted_separable_helpers", Path(__file__).with_name("separable_sixfold.py"))
S = util.module_from_spec(_spec)
_spec.loader.exec_module(S)
E, ONE, X, Y = S.E, S.ONE, S.X, S.Y
SCHEMA = "hamiltonian-weighted-separable-core/1"
THEOREM = "research/hamiltonian/c3_strata/WEIGHTED_SEPARABLE_THEOREM.md"


def _normalize(H):
    n = max(map(sum, H), default=-1)
    if n < 5:
        return None
    leading = {key: value for key, value in H.items() if sum(key) == n}
    a = leading.get((n, 0), F(0))
    if a:
        slope = leading.get((n-1, 1), F(0))/(n*a)
        L, M = E.add(X, E.scale(Y, slope)), dict(Y)
        inverse = E.add(X, E.scale(Y, -slope)), dict(Y)
    else:
        a = leading.get((0, n), F(0))
        L, M = dict(Y), dict(X)
        inverse = dict(Y), dict(X)
    if not a or leading != E.scale(E.power(L, n), a):
        return None
    Ht = S._substitute(H, *inverse)
    m = max(j for _, j in Ht)
    if m not in (3, 4):
        return None
    divisor = gcd(n, m)
    wx, wy = m//divisor, n//divisor
    weight = n*wx
    highest = {key: value for key, value in Ht.items() if wx*key[0]+wy*key[1] == weight}
    if (any(wx*i+wy*j > weight for i, j in Ht) or
            set(highest) != {(n, 0), (0, m)}):
        return None
    lower = {key: value for key, value in Ht.items() if key not in highest}
    determinant = L.get((1, 0), 0)*M.get((0, 1), 0)-L.get((0, 1), 0)*M.get((1, 0), 0)
    return {"L": L, "M": M, "H": Ht, "n": n, "m": m, "wx": wx, "wy": wy,
            "weight": weight, "bound": (4*n+2*m)//divisor, "leading": highest,
            "lower": lower, "determinant": determinant}


def _static(H, n, wx, wy, bound):
    exponents = [(i, j) for j in range(bound//wy+1) for i in range((bound-wy*j)//wx+1)]
    basis = [E.monomial(i, j) for i, j in exponents]
    images = []
    for G in basis:
        image = {}
        for order in range(3, n+1, 2):
            image.update({(order, i, j): value for (i, j), value in S._T(H, G, order).items()})
        images.append(image)
    vectors = S._matrix(images).nullspace()
    return [E.primitive(E.tidy({key: F(value) for key, value in zip(exponents, vector)})) for vector in vectors]


def _witness(H, G, iterate, n):
    current = G
    for r in range(iterate+1):
        gates = {str(order): S._T(H, current, order) for order in range(3, n+1, 2)}
        if any(gates.values()) != (r == iterate):
            raise RuntimeError("Weighted strict-drop witness has wrong first failure")
        if r < iterate:
            current = E.poisson(H, current)
    return {"G": E.serialize(G), "first_failing_iterate": iterate, "DiG": E.serialize(current),
            "T3": E.serialize(gates.get("3", {})), "T5": E.serialize(gates.get("5", {})),
            "gates": {order: E.serialize(value) for order, value in gates.items()}}


def classify_weighted_separable(H):
    """Classify every rational input in the two declared weighted cones."""
    H = S._validate(H)
    report = {"schema": SCHEMA, "status": "out_of_scope", "input": E.serialize(H)}
    normal = _normalize(H)
    if normal is None:
        report["reason"] = "No adapted weighted leading binomial a*L^n+b*M^m with n>=5 and m=3 or4"
        return report
    L, M, Ht = normal["L"], normal["M"], normal["H"]
    n, m = normal["n"], normal["m"]
    basis = _static(Ht, n, normal["wx"], normal["wy"], normal["bound"])
    if not 7 <= len(basis) <= (15 if m == 3 else 12):
        raise RuntimeError("Static dimension contradicts the weighted bound")
    back = lambda G: S._substitute(G, L, M)
    stages, witnesses = [], []
    for depth in range(3 if m == 3 else 2):
        stages.append({"index": depth, "status": "classified", "space": S._space([back(G) for G in basis])})
        new = S._preimage(Ht, basis)
        if len(new) == len(basis):
            break
        if not 2 <= len(new) < len(basis):
            raise RuntimeError("Weighted refinement has inconsistent dimension")
        removed = next(G for G in basis if not S._in_span(new, G))
        witnesses.append(_witness(H, back(removed), depth+1, n))
        basis = new
    else:
        raise RuntimeError("Weighted refinement exceeded its proved stopping depth")
    if len(basis) != 2 or not S._in_span(basis, ONE) or not S._in_span(basis, Ht):
        raise RuntimeError("Computed core disagrees with the all-degree span{1,H} theorem")
    if not all(S._in_span(basis, E.poisson(Ht, G)) for G in basis):
        raise RuntimeError("Terminal weighted core is not invariant")
    if m == 3 and stages[1]["space"]["dimension"] > 4:
        raise RuntimeError("Cubic first refinement exceeds its proved dimension")
    if (m == 4 and depth != 1) or (m == 3 and depth not in (1, 2)):
        raise RuntimeError("Least depth violates the weighted theorem")
    report.update({"status": "classified", "classification": {
        "family": "multiplicity_"+str(n),
        "method": "sixfold_weighted_separable" if n == 6 else "weighted_separable_polynomial",
        "derived_from": SCHEMA,
        "regime": "cubic_weighted_perturbation" if m == 3 else "quartic_weighted_perturbation",
        "coordinates": {"L": E.serialize(L), "M": E.serialize(M), "determinant": str(normal["determinant"])},
        "weighted_model": {"degree_f": n, "degree_g": m,
                           "weights": {"L": normal["wx"], "M": normal["wy"]},
                           "hamiltonian_weight": normal["weight"], "static_bound": normal["bound"],
                           "leading": E.serialize(normal["leading"]), "lower": E.serialize(normal["lower"])},
        "depth": {"kind": "least", "value": depth}, "stages": stages,
        "Dinf": S._space([back(G) for G in basis]), "sharpness_witness": witnesses[-1],
        "drop_witnesses": witnesses, "obstruction": None, "quadratic_lift": None,
    }, "proof_boundary": {
        "formalized": False, "arithmetic": "exact rational arithmetic; full unprojected polynomial Poisson action",
        "dependencies": [S.THEOREM, THEOREM],
        "completeness": "Weighted leading-component transfer from the proved separable binomial confines all "
                        "static observables to the stated finite weighted envelope. Exact full polynomial "
                        "preimages classify every refinement; the core is span{1,H} by the same transfer theorem.",
        "definitions": "S^r imposes every odd Moyal contraction on D^iG for 0<=i<=r; D=T1(H,.)",
        "per_input_checks": ["Exact weighted leading binomial and strict lower weights",
                             "All odd static gates in the proved envelope", "Full unprojected Poisson preimages",
                             "Every strict-drop witness", "Core agrees with span{1,H} and is invariant"],
    }})
    return report


def classify_weighted_separable_sixfold(H):
    H = S._validate(H)
    if max(map(sum, H), default=-1) != 6:
        return {"schema": SCHEMA, "status": "out_of_scope", "input": E.serialize(H),
                "reason": "The sextic wrapper requires total degree six"}
    return classify_weighted_separable(H)
