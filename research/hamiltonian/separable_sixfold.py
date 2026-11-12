"""All-degree refinement of affine-separable polynomial Hamiltonians.

For H=f(L)+g(M), deg f>=5, deg g in {3,4}, the theorem in
c3_strata/SEPARABLE_SIXFOLD_THEOREM.md gives a complete finite static space.
The algorithm takes exact invariant-subspace preimages, without projecting D.
It never infers an all-degree answer from an arbitrary degree cutoff.
"""
from __future__ import annotations

from collections.abc import Mapping
from fractions import Fraction as F
from importlib import util
from math import comb
from pathlib import Path

_spec = util.spec_from_file_location(
    "_separable_sparse_engine", Path(__file__).with_name("independent") / "engine.py")
E = util.module_from_spec(_spec)
_spec.loader.exec_module(E)

SCHEMA = "hamiltonian-separable-core/1"
THEOREM = "research/hamiltonian/c3_strata/SEPARABLE_SIXFOLD_THEOREM.md"
ONE, X, Y = (E.monomial(*key) for key in ((0, 0), (1, 0), (0, 1)))


def _validate(H):
    if not isinstance(H, Mapping):
        raise TypeError("H must map exponent pairs to exact rational coefficients")
    answer = {}
    for key, value in H.items():
        if (not isinstance(key, tuple) or len(key) != 2 or
                any(type(i) is not int or i < 0 for i in key)):
            raise ValueError("Exponents must be pairs of nonnegative integers")
        if type(value) is not int and not isinstance(value, F):
            raise TypeError("Coefficients must be integers or Fraction, not floating values")
        if value:
            answer[key] = F(value)
    return answer


def _substitute(poly, first, second):
    return E.add(*(E.scale(E.multiply(E.power(first, i), E.power(second, j)), value)
                   for (i, j), value in poly.items()))


def _normal_form(H):
    """Recover every rational affine-separable chart, absorbing translations in f,g."""
    potential_degree = max(map(sum, H), default=-1)
    leading = {key: value for key, value in H.items() if sum(key) == potential_degree}
    a = leading.get((potential_degree, 0), F(0))
    if a:
        slope = leading.get((potential_degree - 1, 1), F(0)) / (potential_degree * a)
        L, M = E.add(X, E.scale(Y, slope)), dict(Y)
        inverse = E.add(X, E.scale(Y, -slope)), dict(Y)
    else:
        a = leading.get((0, potential_degree), F(0))
        L, M, inverse = dict(Y), dict(X), (dict(Y), dict(X))
    if not a or leading != E.scale(E.power(L, potential_degree), a):
        return None
    transformed = _substitute(H, *inverse)
    degree = max((j for _, j in transformed), default=-1)
    if degree not in (3, 4):
        return None
    top = {(i, 0): value for (i, j), value in transformed.items() if j == degree}
    next_top = {(i, 0): value for (i, j), value in transformed.items() if j == degree - 1}
    if set(top) != {(0, 0)} or any(i > 1 for i, _ in next_top):
        return None
    shear = next_top.get((1, 0), F(0)) / (degree * top[(0, 0)])
    P = E.add(M, E.scale(L, shear))
    separated = _substitute(transformed, X, E.add(Y, E.scale(X, -shear)))
    if any(i and j for i, j in separated):
        return None
    f = {key: value for key, value in separated.items() if key[1] == 0}
    g = {key: value for key, value in separated.items() if key[1] != 0}
    if max((i for i, _ in f), default=-1) != potential_degree:
        return None
    if _substitute(E.add(f, g), L, P) != H:
        raise RuntimeError("Affine-separable reconstruction failed")
    determinant = (L.get((1, 0), 0) * P.get((0, 1), 0) -
                   L.get((0, 1), 0) * P.get((1, 0), 0))
    if not determinant:
        raise RuntimeError("Adapted coordinates are dependent")
    return L, P, f, g, potential_degree, degree, determinant


def _triple_integral(poly):
    return {(i + 3, 0): value / ((i + 1) * (i + 2) * (i + 3))
            for (i, j), value in poly.items() if value and j == 0}


def _static_basis(f, g, degree):
    low = [ONE, X, E.power(X, 2)]
    answer = [E.multiply(u, E.power(Y, j)) for j in range(3) for u in low]
    f3 = E.derivative(f, q=3)
    leading = g[(0, degree)]
    for u in low:
        integral = _triple_integral(E.multiply(f3, u))
        if degree == 3:
            answer.append(E.add(E.multiply(u, E.power(Y, 3)), E.scale(integral, 1 / leading)))
        else:
            upper = E.add(E.power(Y, 4), E.scale(E.power(Y, 3), g.get((0, 3), F(0)) / leading))
            answer.append(E.add(E.multiply(u, upper), E.scale(integral, 1 / leading)))
    if degree == 3:
        for u in low:
            integral = _triple_integral(E.multiply(f3, u))
            answer.append(E.add(E.multiply(u, E.power(Y, 4)),
                                E.scale(E.multiply(integral, Y), 4 / leading)))
    return answer


def _matrix(polys):
    import sympy as s
    keys = sorted({key for poly in polys for key in poly})
    return s.Matrix([[s.Rational(poly.get(key, 0)) for poly in polys] for key in keys])


def _in_span(basis, G):
    return _matrix(basis + [G]).rank() == len(basis)


def _preimage(H, basis):
    """basis intersect D^-1(span(basis)), using the full polynomial images."""
    n = len(basis)
    images = [E.poisson(H, G) for G in basis]
    columns = images + [E.scale(G, -1) for G in basis]
    vectors = _matrix(columns).nullspace()
    answer = []
    for vector in vectors:
        G = E.add(*(E.scale(B, F(value)) for B, value in zip(basis, vector[:n])))
        if not G:
            raise RuntimeError("Independent basis produced a zero projected relation")
        answer.append(E.primitive(G))
    return answer


def _T(H, G, order):
    return E.add(*(E.scale(E.multiply(E.derivative(H, q=order-j, p=j),
                                     E.derivative(G, q=j, p=order-j)),
                            (-1)**j * comb(order, j)) for j in range(order + 1)))


def _witness(H, G, iterate):
    current = G
    for r in range(iterate + 1):
        T3, T5 = _T(H, current, 3), _T(H, current, 5)
        if bool(T3 or T5) != (r == iterate):
            raise RuntimeError("A strict-drop witness failed at the wrong iterate")
        if r < iterate:
            current = E.poisson(H, current)
    return {"G": E.serialize(G), "first_failing_iterate": iterate,
            "DiG": E.serialize(current), "T3": E.serialize(T3), "T5": E.serialize(T5)}


def _space(basis):
    return {"kind": "finite_basis", "dimension": len(basis),
            "basis": [E.serialize(G) for G in basis]}


def classify_separable(H):
    """Return a complete schema-2-compatible classification, or out_of_scope.

    All rational affine changes of independent linear coordinates and all
    rational lower coefficients of f and g are supported.  No non-affine
    coordinate covariance is assumed.  The static basis and exact preimages
    prove completeness in unbounded observable degree relative to the note.
    """
    H = _validate(H)
    report = {"schema": SCHEMA, "status": "out_of_scope", "input": E.serialize(H)}
    if max(map(sum, H), default=-1) < 5:
        report["reason"] = "Potential degree must be at least five"
        return report
    normal = _normal_form(H)
    if normal is None:
        report["reason"] = "Not affine-separable with potential degree at least five and cubic/quartic complement"
        return report
    L, M, f, g, potential_degree, degree, determinant = normal
    Ht = E.add(f, g)
    basis = _static_basis(f, g, degree)
    expected = 15 if degree == 3 else 12
    if len(basis) != expected or _matrix(basis).rank() != expected:
        raise RuntimeError("Static basis has incorrect rank")
    if any(_T(Ht, G, 3) or _T(Ht, G, 5) for G in basis):
        raise RuntimeError("Static formula failed its gates")
    back = lambda G: _substitute(G, L, M)
    stages, witnesses = [], []
    for depth in range(expected - 1):
        stages.append({"index": depth, "status": "classified", "space": _space([back(G) for G in basis])})
        new = _preimage(Ht, basis)
        if len(new) == len(basis):
            break
        if len(new) < 2 or len(new) >= len(basis):
            raise RuntimeError("Refinement violates its strict dimension descent")
        removed = next(G for G in basis if not _in_span(new, G))
        witnesses.append(_witness(H, back(removed), depth + 1))
        basis = new
    else:
        raise RuntimeError("Refinement exceeded the proved dimension bound")
    if not all(_in_span(basis, E.poisson(Ht, G)) for G in basis):
        raise RuntimeError("Terminal space is not invariant under unprojected D")
    if not _in_span(basis, ONE) or not _in_span(basis, Ht):
        raise RuntimeError("Core does not contain 1 and H")
    dimensions = [stage["space"]["dimension"] for stage in stages]
    if dimensions != ([15, 4, 2] if degree == 3 else [12, 2]):
        raise RuntimeError("Exact preimages disagree with the closed all-degree theorem")
    if len(basis) != 2:
        raise RuntimeError("Core must equal span{1,H}")
    if degree == 3:
        first = [{(item["q"], item["p"]): F(item["coefficient"]) for item in terms}
                 for terms in stages[1]["space"]["basis"]]
        if not all(_in_span(first, G) for G in (ONE, L, E.power(L, 2), H)):
            raise RuntimeError("First refinement disagrees with span{1,L,L^2,H}")
    core = _space([back(G) for G in basis])
    report.update({
        "status": "classified",
        "classification": {
            "family": "multiplicity_" + str(potential_degree),
            "method": "sixfold_separable_complement" if potential_degree == 6 else "separable_polynomial_complement",
            "derived_from": SCHEMA, "regime": "cubic_kinetic" if degree == 3 else "quartic_kinetic",
            "coordinates": {"L": E.serialize(L), "M": E.serialize(M), "determinant": str(determinant)},
            "normal_form": {"f": E.serialize(f), "g": E.serialize(g),
                            "degree_f": potential_degree, "degree_g": degree},
            "depth": {"kind": "least", "value": depth}, "stages": stages, "Dinf": core,
            "sharpness_witness": witnesses[-1] if witnesses else None,
            "drop_witnesses": witnesses, "obstruction": None, "quadratic_lift": None,
        },
        "proof_boundary": {
            "formalized": False,
            "arithmetic": "exact rational arithmetic; full unprojected polynomial Poisson action",
            "dependencies": [THEOREM],
            "completeness": "The explicit complete static basis has dimension 15 (cubic) or 12 (quartic). "
                            "Every later stage is its exact invariant-subspace preimage. "
                            "A repeated dimension is checked by full D-invariance; the depth is least.",
            "definitions": "S^r imposes T3(H,D^i G)=T5(H,D^i G)=0 for 0<=i<=r; D=T1(H,.)",
            "per_input_checks": ["Exact affine-separable reconstruction", "Complete static-basis rank and gates",
                                 "Full polynomial preimage at each refinement", "Every strict-drop obstruction",
                                 "Terminal D-invariance and containment of 1,H"],
        },
    })
    return report


def classify_separable_sixfold(H):
    """Sextic-only wrapper used by the existing sextic schema-2 classifier."""
    H = _validate(H)
    if max(map(sum, H), default=-1) != 6:
        return {"schema": SCHEMA, "status": "out_of_scope", "input": E.serialize(H),
                "reason": "The sextic wrapper requires total degree six"}
    return classify_separable(H)
