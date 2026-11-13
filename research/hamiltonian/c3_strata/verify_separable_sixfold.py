"""Independent supplied-report verification for separable polynomial cores.

No producer functions are imported.  Static kernels come from the defining
star exponential on the theorem-proved envelope; exact forward elimination
and back substitution reconstruct every full polynomial preimage.
"""
from __future__ import annotations

from fractions import Fraction as F
from importlib import util
from pathlib import Path

HERE = Path(__file__).resolve().parent
_spec = util.spec_from_file_location("_separable_independent_star", HERE.parent / "independent" / "engine.py")
E = util.module_from_spec(_spec)
_spec.loader.exec_module(E)
THEOREM = "research/hamiltonian/c3_strata/SEPARABLE_SIXFOLD_THEOREM.md"
SCHEMA = "hamiltonian-separable-core/1"


class VerificationError(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise VerificationError(message)


def polynomial(terms):
    require(isinstance(terms, list), "Polynomial terms must be a list")
    answer = {}
    for item in terms:
        require(isinstance(item, dict), "Polynomial term must be an object")
        i, j, value = item.get("q"), item.get("p"), item.get("coefficient")
        require(type(i) is int and type(j) is int and i >= 0 and j >= 0,
                "Polynomial exponents must be nonnegative integers")
        require((i, j) not in answer and isinstance(value, str), "Duplicate monomial or non-string coefficient")
        try:
            answer[i, j] = F(value)
        except (ValueError, ZeroDivisionError) as exc:
            raise VerificationError("Invalid rational coefficient") from exc
    return {key: value for key, value in answer.items() if value}


def _substitute(poly, L, M):
    result = {}
    for (i, j), value in poly.items():
        result = E.add(result, E.scale(E.multiply(E.power(L, i), E.power(M, j)), value))
    return result


def normalize(H):
    """Independent exact scope recognizer; return a normal form or None.

    Factoring the leading binary form and SymPy polynomial substitution are
    independent of the producer's coefficient-ratio and sparse substitutions.
    """
    import sympy as s
    q, p, x, y, z = s.symbols("q p x y z")
    # SymPy's domain conversion can rewrite the supplied coefficient dict.
    # Preserve the caller's exact Fraction representation and identity.
    source = s.Poly.from_dict(dict(H), (q, p), domain=s.QQ)
    n = source.total_degree()
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
    determinant = a*d-b*c
    expr = source.as_expr().subs({q: (d*x-b*y)/determinant, p: (a*y-c*x)/determinant}, simultaneous=True)
    poly = s.Poly(expr, y, x, domain=s.QQ)
    m = poly.degree(y)
    if m not in (3, 4):
        return None
    top = s.Poly(poly.as_expr().coeff(y, m), x, domain=s.QQ)
    next_top = s.Poly(poly.as_expr().coeff(y, m-1), x, domain=s.QQ)
    if top.degree() != 0 or next_top.degree() > 1:
        return None
    shear = next_top.nth(1) / (m*top.nth(0))
    separated = s.Poly(poly.as_expr().subs(y, z-shear*x), x, z, domain=s.QQ)
    if any(i and j for (i, j), _ in separated.terms()):
        return None
    Mfinal = s.Poly(Mp + shear*Lp, q, p, domain=s.QQ)
    sparse = lambda P: {key: F(value) for key, value in P.terms() if value}
    f = {(i, 0): F(value) for (i, j), value in separated.terms() if j == 0 and value}
    g = {(0, j): F(value) for (i, j), value in separated.terms() if j != 0 and value}
    return {"L": sparse(s.Poly(Lp, q, p, domain=s.QQ)), "M": sparse(Mfinal),
            "f": f, "g": g, "degree_f": int(n), "degree_g": int(m)}


def _nullspace(rows, width):
    """Forward elimination/back substitution; independent of producer/SymPy."""
    work = [[F(value) for value in row] for row in rows]
    pivots = []
    for column in range(width):
        r = len(pivots)
        pivot = next((i for i in range(r, len(work)) if work[i][column]), None)
        if pivot is None:
            continue
        work[r], work[pivot] = work[pivot], work[r]
        for i in range(r+1, len(work)):
            if work[i][column]:
                factor = work[i][column] / work[r][column]
                work[i] = [left - factor*right for left, right in zip(work[i], work[r])]
        pivots.append(column)
        if len(pivots) == len(work):
            break
    answer = []
    for free in (j for j in range(width) if j not in pivots):
        vector = [F(0)] * width
        vector[free] = F(1)
        for row, pivot in reversed(list(enumerate(pivots))):
            vector[pivot] = -sum(work[row][j]*vector[j] for j in range(pivot+1, width)) / work[row][pivot]
        answer.append(vector)
    return answer


def _columns(polys):
    keys = sorted({key for poly in polys for key in poly})
    return [[poly.get(key, F(0)) for poly in polys] for key in keys]


def _rank(polys):
    return len(polys) - len(_nullspace(_columns(polys), len(polys)))


def _same_span(left, right):
    return _rank(left) == _rank(right) == _rank(left + right)


def _space(value):
    require(isinstance(value, dict) and value.get("kind") == "finite_basis", "Expected finite_basis space")
    require(type(value.get("dimension")) is int and isinstance(value.get("basis"), list), "Invalid finite space metadata")
    basis = [polynomial(terms) for terms in value["basis"]]
    require(len(basis) == value["dimension"] == _rank(basis), "Finite space dimension/dependence mismatch")
    return basis


def _static(H, n, m):
    exponents = [(i, j) for j in range(5)
                 for i in range((n+2 if j < (2 if m == 3 else 1) else 2)+1)]
    images = [E.defects(H, E.monomial(*key)) for key in exponents]
    keys = sorted({(hbar, i, j) for image in images for hbar, poly in image.items() for i, j in poly})
    rows = [[image.get(hbar, {}).get((i, j), F(0)) for image in images] for hbar, i, j in keys]
    return [E.tidy(dict(zip(exponents, vector))) for vector in _nullspace(rows, len(exponents))]


def _preimage(H, basis):
    columns = [E.poisson(H, G) for G in basis] + [E.scale(G, -1) for G in basis]
    vectors = _nullspace(_columns(columns), 2*len(basis))
    answer = [E.add(*(E.scale(G, value) for G, value in zip(basis, vector[:len(basis)]))) for vector in vectors]
    require(all(answer), "Zero projected preimage relation")
    return answer


def _witness(H, value, expected):
    require(isinstance(value, dict), "Missing strict-drop witness")
    require(type(value.get("first_failing_iterate")) is int and value["first_failing_iterate"] == expected,
            "Wrong witness iterate")
    current = polynomial(value.get("G"))
    for r in range(expected+1):
        defects = E.defects(H, current)
        require(bool(defects) == (r == expected), "Witness fails at wrong first iterate")
        if r < expected:
            current = E.poisson(H, current)
    require(polynomial(value.get("DiG")) == current, "Corrupted witness Poisson iterate")
    require(polynomial(value.get("T3")) == E.scale(defects.get(2, {}), -24), "Corrupted witness T3")
    require(polynomial(value.get("T5")) == E.scale(defects.get(4, {}), 1920), "Corrupted witness T5")
    require(bool(defects.get(2) or defects.get(4)), "Witness needs a third/fifth-gate obstruction")


def check_report(H, report):
    """Validate an externally supplied standalone or schema-2 classification."""
    require(isinstance(report, dict), "Report must be an object")
    require(report.get("schema") in (SCHEMA, "hamiltonian-sextic-core/2"), "Unknown separable report schema")
    require(report.get("status") == "classified", "Expected a classified separable report")
    require(polynomial(report.get("input")) == H, "Input mismatch")
    classification = report.get("classification")
    require(isinstance(classification, dict), "Missing classification")
    coordinates = classification.get("coordinates")
    normal = classification.get("normal_form")
    require(isinstance(coordinates, dict) and isinstance(normal, dict), "Missing separable normal form")
    L, M = polynomial(coordinates.get("L")), polynomial(coordinates.get("M"))
    require(L and M and all(sum(key) == 1 for key in L.keys() | M.keys()), "Coordinates must be linear forms")
    determinant = L.get((1, 0), 0)*M.get((0, 1), 0)-L.get((0, 1), 0)*M.get((1, 0), 0)
    require(bool(determinant), "Dependent coordinates")
    require(isinstance(coordinates.get("determinant"), str), "Determinant must be an exact rational string")
    try:
        require(F(coordinates["determinant"]) == determinant, "Incorrect coordinate determinant")
    except (ValueError, ZeroDivisionError) as exc:
        raise VerificationError("Invalid coordinate determinant") from exc
    f, g = polynomial(normal.get("f")), polynomial(normal.get("g"))
    require(f and g and all(j == 0 for _, j in f) and all(i == 0 and j > 0 for i, j in g),
            "Normal form must contain a potential and a constant-free complement")
    n, m = max(i for i, _ in f), max(j for _, j in g)
    require(n >= 5 and m in (3, 4), "Normal form outside the proved degrees")
    require(type(normal.get("degree_f")) is int and normal["degree_f"] == n and
            type(normal.get("degree_g")) is int and normal["degree_g"] == m, "Incorrect degree metadata")
    require(_substitute(E.add(f, g), L, M) == H, "Normal form does not reconstruct the input")
    require(classification.get("method") == ("sixfold_separable_complement" if n == 6 else "separable_polynomial_complement"),
            "Incorrect classification method")
    require(classification.get("derived_from") == SCHEMA and classification.get("family") == "multiplicity_"+str(n),
            "Incorrect family/provenance metadata")
    require(classification.get("regime") == ("cubic_kinetic" if m == 3 else "quartic_kinetic"), "Incorrect complement regime")
    if report["schema"] == "hamiltonian-sextic-core/2":
        require(n == 6, "Sextic schema cannot carry a nonsextic input")
    depth = classification.get("depth")
    expected_depth = 2 if m == 3 else 1
    require(isinstance(depth, dict) and depth.get("kind") == "least" and
            type(depth.get("value")) is int and depth["value"] == expected_depth, "Incorrect least depth")
    stages = classification.get("stages")
    require(isinstance(stages, list) and len(stages) == expected_depth+1, "Incomplete refinement stages")
    Ht = E.add(f, g)
    expected = _static(Ht, n, m)
    dimensions = [15, 4, 2] if m == 3 else [12, 2]
    for index, stage in enumerate(stages):
        require(isinstance(stage, dict) and type(stage.get("index")) is int and stage["index"] == index and
                stage.get("status") == "classified", "Incorrect stage metadata")
        actual = _space(stage.get("space"))
        back = [_substitute(G, L, M) for G in expected]
        require(len(expected) == dimensions[index] and _same_span(actual, back), "Stage is not the complete exact kernel")
        new = _preimage(Ht, expected)
        if index == expected_depth:
            require(_same_span(expected, new), "Terminal space is not D-invariant")
        expected = new
    core = _space(classification.get("Dinf"))
    require(_same_span(core, [E.monomial(0, 0), H]), "Core differs from span{1,H}")
    require(_same_span(core, _space(stages[-1]["space"])), "Core and terminal stage disagree")
    witnesses = classification.get("drop_witnesses")
    require(isinstance(witnesses, list) and len(witnesses) == expected_depth, "Incomplete strict-drop witnesses")
    for index, value in enumerate(witnesses, start=1):
        _witness(H, value, index)
    require(classification.get("sharpness_witness") == witnesses[-1], "Sharpness witness disagrees with final drop")
    boundary = report.get("proof_boundary")
    require(isinstance(boundary, dict) and boundary.get("formalized") is False and
            THEOREM in boundary.get("dependencies", []), "Incorrect proof boundary")
    return {"status": "PASS", "potential_degree": n, "complement_degree": m,
            "static_dimension": dimensions[0], "stage_dimensions": dimensions,
            "least_depth": expected_depth, "core_dimension": 2}


def verify():
    """Deterministic corpus replay; per-input validation never calls the producer."""
    import hashlib
    import sys
    sys.path.insert(0, str(HERE.parent))
    from partner_lab import parse
    from separable_sixfold import classify_separable
    examples = [f"q^{n}+q^2-q+2*p^{m}-p^2+p+3" for n in (5, 6, 7, 8) for m in (3, 4)]
    examples += [
        "q^6+q^5/2-q^2+3*p^3+2*p^2-5*p+7",
        "q^6+q^3+p^4+p^3-p^2+p",
        "-2/3*((2*q+3*p+1)^6+3*(q-2*p-3)^3+(q-2*p-3)^2)",
        "3/5*((2*q+3*p+1)^6-2*(q-2*p-3)^4+(q-2*p-3)^3)",
        "(q+2*p+1)^8+(q-p-2)^3",
        "p^6+q^3+q^2",
        "p^6+q^4+q",
    ]
    checks = []
    for expression in examples:
        H = parse(expression)
        report = classify_separable(H)
        require(normalize(H) is not None, "Independent recognizer omitted a supported corpus input")
        checks.append({"H": expression, **check_report(H, report)})
    sources = [HERE.parent / "separable_sixfold.py", Path(__file__),
               HERE / "SEPARABLE_SIXFOLD_THEOREM.md", HERE.parent / "independent" / "engine.py"]
    return {"schema": "hamiltonian-separable-replay/1", "status": "PASS", "classified_inputs": len(checks),
            "potential_degrees": [5, 6, 7, 8], "checks": checks,
            "sources": {str(path.relative_to(HERE.parent)): hashlib.sha256(path.read_bytes()).hexdigest()
                        for path in sources}}


if __name__ == "__main__":
    import json
    print(json.dumps(verify(), indent=2, sort_keys=True))
