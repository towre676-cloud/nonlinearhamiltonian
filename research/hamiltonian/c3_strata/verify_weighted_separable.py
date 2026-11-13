"""Independent supplied-report checker for mixed weighted-separable families."""
from __future__ import annotations

from fractions import Fraction as F
from importlib import util
from math import factorial, gcd
from pathlib import Path

HERE = Path(__file__).resolve().parent
_spec = util.spec_from_file_location("_weighted_independent_helpers", HERE / "verify_separable_sixfold.py")
S = util.module_from_spec(_spec)
_spec.loader.exec_module(S)
E, require, polynomial, VerificationError = S.E, S.require, S.polynomial, S.VerificationError
SCHEMA = "hamiltonian-weighted-separable-core/1"
THEOREM = "research/hamiltonian/c3_strata/WEIGHTED_SEPARABLE_THEOREM.md"


def normalize(H):
    """Recognize the weighted cone through factorization and exact substitution."""
    import sympy as s
    q, p, x, y = s.symbols("q p x y")
    source = s.Poly.from_dict(dict(H), (q, p), domain=s.QQ)
    n = int(source.total_degree())
    if source.is_zero or n < 5:
        return None
    leading = s.Poly.from_dict({key: value for key, value in H.items() if sum(key) == n}, (q, p), domain=s.QQ)
    _, factors = leading.factor_list()
    if len(factors) != 1 or factors[0][1] != n or factors[0][0].total_degree() != 1:
        return None
    Lp = factors[0][0].as_expr()
    a, b = Lp.coeff(q), Lp.coeff(p)
    Mp = p if a else q
    c, d = Mp.coeff(q), Mp.coeff(p)
    det = a*d-b*c
    transformed = s.Poly(source.as_expr().subs({q: (d*x-b*y)/det, p: (a*y-c*x)/det}, simultaneous=True), x, y, domain=s.QQ)
    m = int(transformed.degree(y))
    if m not in (3, 4):
        return None
    divisor = gcd(n, m)
    wx, wy, weight = m//divisor, n//divisor, n*m//divisor
    terms = transformed.terms()
    if any(wx*i+wy*j > weight for (i, j), _ in terms):
        return None
    highest = {key: F(value) for key, value in terms if wx*key[0]+wy*key[1] == weight}
    if set(highest) != {(n, 0), (0, m)}:
        return None
    sparse = lambda P: {key: F(value) for key, value in P.terms() if value}
    return {"L": sparse(s.Poly(Lp, q, p, domain=s.QQ)), "M": sparse(s.Poly(Mp, q, p, domain=s.QQ)),
            "H": sparse(transformed), "n": n, "m": m, "wx": wx, "wy": wy,
            "weight": weight, "bound": (4*n+2*m)//divisor}


def _static(H, wx, wy, bound):
    exponents = [(i, j) for j in range(bound//wy+1) for i in range((bound-wy*j)//wx+1)]
    images = [E.defects(H, E.monomial(*key)) for key in exponents]
    keys = sorted({(hbar, i, j) for image in images for hbar, poly in image.items() for i, j in poly})
    rows = [[image.get(hbar, {}).get((i, j), F(0)) for image in images] for hbar, i, j in keys]
    return [E.tidy(dict(zip(exponents, vector))) for vector in S._nullspace(rows, len(exponents))]


def _witness(H, record, expected, n):
    require(isinstance(record, dict) and type(record.get("first_failing_iterate")) is int and
            record["first_failing_iterate"] == expected, "Wrong weighted witness iterate")
    current = polynomial(record.get("G"))
    for r in range(expected+1):
        defects = E.defects(H, current)
        require(bool(defects) == (r == expected), "Weighted witness fails at wrong first iterate")
        if r < expected:
            current = E.poisson(H, current)
    require(polynomial(record.get("DiG")) == current, "Corrupted weighted Poisson iterate")
    gates = record.get("gates")
    orders = list(range(3, n+1, 2))
    require(isinstance(gates, dict) and set(gates) == {str(k) for k in orders}, "Incomplete odd-gate witness")
    for order in orders:
        scale = (-1)**((order-1)//2) * 2**(order-1) * factorial(order)
        require(polynomial(gates[str(order)]) == E.scale(defects.get(order-1, {}), scale), "Corrupted weighted contraction")
    require(polynomial(record.get("T3")) == polynomial(gates["3"]) and
            polynomial(record.get("T5")) == polynomial(gates["5"]), "Inconsistent weighted gate aliases")


def check_report(H, report):
    require(isinstance(report, dict) and report.get("schema") in (SCHEMA, "hamiltonian-sextic-core/2"),
            "Unknown weighted report schema")
    require(report.get("status") == "classified" and polynomial(report.get("input")) == H, "Weighted status/input mismatch")
    claim = report.get("classification")
    require(isinstance(claim, dict), "Missing weighted classification")
    coordinates, model = claim.get("coordinates"), claim.get("weighted_model")
    require(isinstance(coordinates, dict) and isinstance(model, dict), "Missing weighted model")
    L, M = polynomial(coordinates.get("L")), polynomial(coordinates.get("M"))
    require(L and M and all(sum(key) == 1 for key in L.keys() | M.keys()), "Weighted coordinates must be linear")
    det = L.get((1, 0), 0)*M.get((0, 1), 0)-L.get((0, 1), 0)*M.get((1, 0), 0)
    require(bool(det) and isinstance(coordinates.get("determinant"), str), "Invalid weighted coordinate determinant")
    try:
        require(F(coordinates["determinant"]) == det, "Incorrect weighted determinant")
    except (ValueError, ZeroDivisionError) as exc:
        raise VerificationError("Invalid weighted determinant") from exc
    n, m = model.get("degree_f"), model.get("degree_g")
    require(type(n) is int and n >= 5 and type(m) is int and m in (3, 4), "Incorrect weighted degrees")
    divisor = gcd(n, m)
    wx, wy, weight, bound = m//divisor, n//divisor, n*m//divisor, (4*n+2*m)//divisor
    weights = model.get("weights")
    require(isinstance(weights, dict) and type(weights.get("L")) is int and type(weights.get("M")) is int and
            weights["L"] == wx and weights["M"] == wy, "Incorrect coordinate weights")
    require(type(model.get("hamiltonian_weight")) is int and model["hamiltonian_weight"] == weight and
            type(model.get("static_bound")) is int and model["static_bound"] == bound, "Incorrect proved weighted bound")
    leading, lower = polynomial(model.get("leading")), polynomial(model.get("lower"))
    require(set(leading) == {(n, 0), (0, m)}, "Leading form is not the nonzero weighted binomial")
    require(all(wx*i+wy*j < weight for i, j in lower), "Perturbation is not strictly lower weight")
    Ht = E.add(leading, lower)
    require(S._substitute(Ht, L, M) == H, "Weighted model does not reconstruct input")
    require(claim.get("family") == "multiplicity_"+str(n) and claim.get("derived_from") == SCHEMA,
            "Incorrect weighted family/provenance")
    require(claim.get("method") == ("sixfold_weighted_separable" if n == 6 else "weighted_separable_polynomial"),
            "Incorrect weighted method")
    require(claim.get("regime") == ("cubic_weighted_perturbation" if m == 3 else "quartic_weighted_perturbation"),
            "Incorrect weighted regime")
    if report["schema"] == "hamiltonian-sextic-core/2":
        require(n == 6, "Sextic report carries a nonsextic weighted input")
    depth = claim.get("depth")
    require(isinstance(depth, dict) and depth.get("kind") == "least" and type(depth.get("value")) is int,
            "Incorrect weighted depth metadata")
    terminal = depth["value"]
    require(terminal in ((1, 2) if m == 3 else (1,)), "Weighted depth exceeds theorem")
    stages = claim.get("stages")
    require(isinstance(stages, list) and len(stages) == terminal+1, "Incomplete weighted stages")
    expected = _static(Ht, wx, wy, bound)
    dimensions = []
    require(7 <= len(expected) <= (15 if m == 3 else 12), "Weighted static dimension violates theorem")
    for index, stage in enumerate(stages):
        require(isinstance(stage, dict) and type(stage.get("index")) is int and stage["index"] == index and
                stage.get("status") == "classified", "Incorrect weighted stage metadata")
        actual = S._space(stage.get("space"))
        require(S._same_span(actual, [S._substitute(G, L, M) for G in expected]), "Weighted stage is not complete")
        dimensions.append(len(expected))
        new = S._preimage(Ht, expected)
        if index < terminal:
            require(len(new) < len(expected), "Claimed weighted depth is not least")
        else:
            require(S._same_span(expected, new), "Terminal weighted stage is not invariant")
        expected = new
    require(dimensions[1] <= (4 if m == 3 else 2), "First weighted space exceeds theorem")
    core = S._space(claim.get("Dinf"))
    require(S._same_span(core, [E.monomial(0, 0), H]) and S._same_span(core, S._space(stages[-1]["space"])),
            "Weighted core is not terminal span{1,H}")
    witnesses = claim.get("drop_witnesses")
    require(isinstance(witnesses, list) and len(witnesses) == terminal, "Incomplete weighted strict-drop witnesses")
    for index, record in enumerate(witnesses, start=1):
        _witness(H, record, index, n)
    require(claim.get("sharpness_witness") == witnesses[-1], "Incorrect weighted sharpness witness")
    boundary = report.get("proof_boundary")
    require(isinstance(boundary, dict) and boundary.get("formalized") is False and
            all(path in boundary.get("dependencies", []) for path in (S.THEOREM, THEOREM)), "Incorrect weighted proof boundary")
    return {"status": "PASS", "potential_degree": n, "complement_degree": m,
            "weights": [wx, wy], "static_bound": bound, "stage_dimensions": dimensions,
            "least_depth": terminal, "core_dimension": 2}


def verify():
    import hashlib
    import sys
    sys.path.insert(0, str(HERE.parent))
    from partner_lab import parse
    from weighted_separable import classify_weighted_separable
    examples = [f"q^{n}+2*p^3+q*p^2-q^2+3" for n in (5, 6, 7, 8)]
    examples += [f"q^{n}-3*p^4+q*p^3+q^2-p" for n in (5, 6, 7, 8)]
    examples += ["q^6+p^3+q*p", "q^6+p^3+q^3*p", "q^6+p^4+q^4*p+q^2*p^2",
                 "-2/3*((2*q+3*p+1)^6+(q-2*p-3)^3+(2*q+3*p+1)*(q-2*p-3)^2)",
                 "3/5*((2*q+3*p+1)^6-(q-2*p-3)^4+(2*q+3*p+1)*(q-2*p-3)^3)",
                 "p^6+q^3+p*q^2", "p^6+q^4+p^4*q"]
    checks = []
    for expression in examples:
        H = parse(expression)
        report = classify_weighted_separable(H)
        require(normalize(H) is not None, "Independent weighted recognizer omitted supported input")
        checks.append({"H": expression, **check_report(H, report)})
    sources = [HERE.parent / "weighted_separable.py", HERE.parent / "separable_sixfold.py", Path(__file__),
               HERE / "verify_separable_sixfold.py", HERE / "SEPARABLE_SIXFOLD_THEOREM.md",
               HERE / "WEIGHTED_SEPARABLE_THEOREM.md", HERE.parent / "independent" / "engine.py"]
    return {"schema": "hamiltonian-weighted-separable-replay/1", "status": "PASS", "classified_inputs": len(checks),
            "checks": checks, "sources": {str(path.relative_to(HERE.parent)): hashlib.sha256(path.read_bytes()).hexdigest()
                                          for path in sources}}


if __name__ == "__main__":
    import json
    print(json.dumps(verify(), indent=2, sort_keys=True))
