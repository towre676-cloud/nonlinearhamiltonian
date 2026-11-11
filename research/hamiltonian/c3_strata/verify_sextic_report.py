"""Verify a supplied sextic report against an independently supplied Hamiltonian.

No classification function is called.  Factorization, polynomial identities,
module structure, untruncated gate kernels, invariance, and obstruction witnesses
are checked separately.  All-degree completeness remains conditional on the
named written theorems; this program does not turn them into Lean theorems.

    python research/hamiltonian/c3_strata/verify_sextic_report.py report.json \
        --H 'q^6+p^2'

The default comparison window contains every monomial of total degree <= 6.
For a variable quadratic complementary coefficient it is additionally the full
weighted box in Theorem D, not a total-degree sample.  JSON is strict: duplicate
keys, nonfinite numbers, floating coefficients and ambiguous schema layouts fail.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as F
from itertools import permutations
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import verify_sextic_core as V  # noqa: E402

E = V.E
VerificationError = V.VerificationError
require = V.require
ONE, X, Y = {(0, 0): F(1)}, {(1, 0): F(1)}, {(0, 1): F(1)}
SCHEMA1, SCHEMA2 = "hamiltonian-sextic-core/1", "hamiltonian-sextic-core/2"
THEOREM = "research/hamiltonian/c3_strata/SEXTIC_STRATA_THEOREM.md"
EXTENSION = "research/hamiltonian/c3_strata/INHOMOGENEOUS_THEOREM.md"
QUADRATIC = "research/hamiltonian/c3_strata/QUADRATIC_SIXFOLD_THEOREM.md"
SEPARABLE = "research/hamiltonian/c3_strata/SEPARABLE_SIXFOLD_THEOREM.md"
WEIGHTED = "research/hamiltonian/c3_strata/WEIGHTED_SEPARABLE_THEOREM.md"
DEFINITIONS = "S^r imposes T3(H,D^i G)=T5(H,D^i G)=0 for 0<=i<=r; D=T1(H,.)"


def _keys(obj, required, *, optional=(), label="object"):
    require(type(obj) is dict, f"{label} must be an object")
    required, allowed = set(required), set(required) | set(optional)
    require(required <= obj.keys(), f"{label} is missing mandatory fields: {sorted(required - obj.keys())}")
    require(obj.keys() <= allowed, f"{label} contains undocumented fields: {sorted(obj.keys() - allowed)}")


def _json_value(value):
    if type(value) is dict:
        require(all(type(key) is str for key in value), "JSON keys must be strings")
        for item in value.values():
            _json_value(item)
    elif type(value) is list:
        for item in value:
            _json_value(item)
    else:
        require(value is None or type(value) in (str, int, bool),
                "Only exact JSON values are accepted; floating and nonfinite numbers are forbidden")


def rational(value):
    require(type(value) is str, "Rational values must be canonical strings")
    try:
        answer = F(value)
    except (ValueError, ZeroDivisionError) as exc:
        raise VerificationError("Invalid rational string") from exc
    require(str(answer) == value, "Rational strings must be reduced integer or numerator/denominator form")
    return answer


def polynomial(terms):
    require(type(terms) is list, "Polynomial terms must be a list")
    for term in terms:
        _keys(term, ("q", "p", "coefficient"), label="polynomial term")
        require(type(term["q"]) is int and type(term["p"]) is int
                and min(term["q"], term["p"]) >= 0, "Polynomial exponents must be nonnegative integers")
        require(rational(term["coefficient"]) != 0, "Zero terms are not canonical")
    return V.polynomial(terms)


def load_json(path):
    def pairs(entries):
        result = {}
        for key, value in entries:
            require(key not in result, f"Duplicate JSON key: {key}")
            result[key] = value
        return result

    def bad_constant(value):
        raise VerificationError(f"Nonfinite JSON number: {value}")

    return json.loads(Path(path).read_text(encoding="utf-8"), object_pairs_hook=pairs,
                      parse_constant=bad_constant)


def substitute(poly, left, right):
    result = {}
    for (i, j), value in poly.items():
        result = E.add(result, E.scale(E.multiply(E.power(left, i), E.power(right, j)), value))
    return result


def chart(L, M):
    require(L and M and all(sum(k) == 1 for k in L) and all(sum(k) == 1 for k in M),
            "Coordinates must be nonzero homogeneous linear forms")
    a, b, c, d = (L.get((1, 0), F(0)), L.get((0, 1), F(0)),
                  M.get((1, 0), F(0)), M.get((0, 1), F(0)))
    determinant = a * d - b * c
    require(determinant != 0, "Coordinates must be independent")
    inverse = (E.add(E.scale(X, d / determinant), E.scale(Y, -b / determinant)),
               E.add(E.scale(X, -c / determinant), E.scale(Y, a / determinant)))
    return determinant, inverse


def transverse(poly, L):
    return E.add(E.scale(E.derivative(poly, q=1), -L.get((0, 1), F(0))),
                 E.scale(E.derivative(poly, p=1), L.get((1, 0), F(0))))


def _scalar_multiple(poly, basis):
    if not basis:
        return F(0) if not poly else None
    pivot = next(iter(basis))
    scalar = poly.get(pivot, F(0)) / basis[pivot]
    return scalar if poly == E.scale(basis, scalar) else None


def _quadratic_generator(H, factors):
    """Recognize cubic composition by exact coefficient elimination, no factoring."""
    J2 = dict(ONE)
    for factor in factors:
        J2 = E.multiply(J2, polynomial(factor["terms"]))
    H6 = {k: v for k, v in H.items() if sum(k) == 6}
    a = _scalar_multiple(H6, E.power(J2, 3))
    require(a is not None and a != 0, "Triple-pair leading cube is inconsistent")
    H5 = {k: v for k, v in H.items() if sum(k) == 5}
    factor = E.scale(E.power(J2, 2), 3 * a)
    columns = [E.multiply(factor, X), E.multiply(factor, Y)]
    keys = sorted(set(H5) | set(columns[0]) | set(columns[1]))
    equations = [[col.get(k, F(0)) for col in columns] + [-H5.get(k, F(0))] for k in keys]
    solutions = V.nullspace(equations, 3)
    solution = next((row for row in solutions if row[2]), None)
    if solution is None:
        return None
    J = E.add(J2, E.scale(X, solution[0] / solution[2]), E.scale(Y, solution[1] / solution[2]))
    if not V.same_span([ONE, J, E.power(J, 2), E.power(J, 3)],
                       [ONE, J, E.power(J, 2), E.power(J, 3), H]):
        return None
    return J


def _recognize(H, pattern, factors, schema):
    if not H:
        return "zero", None
    if all(sum(k) == 6 for k in H):
        return "homogeneous", None
    if all(sum(k) in (0, 6) for k in H):
        return "constant_shift", None
    if pattern not in ([6], [5, 1], [3, 3]):
        return "leading_form", None
    if pattern == [3, 3]:
        J = _quadratic_generator(H, factors)
        return ("triple_pair_quadratic_composition", J) if J is not None else (None, None)
    L = polynomial(next(factor["terms"] for factor in factors if factor["multiplicity"] == pattern[0]))
    second = transverse(transverse(H, L), L)
    if not second:
        return ("sixfold_affine_complement" if pattern == [6] else "fivefold_affine_complement"), L
    if schema == SCHEMA2 and pattern == [6]:
        if not transverse(second, L):
            return "sixfold_quadratic_complement", L
        import verify_separable_sixfold as S
        if S.normalize(dict(H)) is not None:
            return "sixfold_separable_complement", L
        import verify_weighted_separable as W
        if W.normalize(dict(H)) is not None:
            return "sixfold_weighted_separable", L
    return None, None


def _metadata(H, report):
    _json_value(report)
    require(type(report) is dict and report.get("schema") in (SCHEMA1, SCHEMA2), "Unknown report schema")
    schema = report["schema"]
    required = {"schema", "status", "input", "degree", "homogeneous", "leading", "classification", "proof_boundary"}
    if schema == SCHEMA1:
        required |= {"obstruction", "quadratic_lift"}
    _keys(report, required, optional=("unsupported_reason",), label="report")
    require(report["status"] in ("classified", "unsupported"), "Unknown classification status")
    require(("unsupported_reason" in report) == (report["status"] == "unsupported"),
            "Unsupported reason must appear exactly for unsupported reports")
    require(polynomial(report["input"]) == H, "Report input does not match the independently supplied Hamiltonian")
    require((report["degree"] is None) if not H else (type(report["degree"]) is int and report["degree"] == 6),
            "Incorrect total-degree metadata")
    H6 = {key: value for key, value in H.items() if sum(key) == 6}
    require(type(report["homogeneous"]) is bool and report["homogeneous"] == (H == H6),
            "Incorrect homogeneous metadata")
    leading = report["leading"]
    _keys(leading, ("terms", "geometric_root_pattern", "dehomogenization", "infinity_point", "infinity_multiplicity", "factorization"),
          label="leading metadata")
    require(polynomial(leading["terms"]) == H6, "Incorrect leading polynomial")
    require(leading["dehomogenization"] == "H6(t,1)" and leading["infinity_point"] == "[1:0]",
            "Incorrect projective-coordinate convention")
    require(type(leading["infinity_multiplicity"]) is int
            and leading["infinity_multiplicity"] == (min(b for a, b in H6) if H6 else 0),
            "Incorrect multiplicity at infinity")
    factorization = leading["factorization"]
    _keys(factorization, ("coefficient", "factors"), label="factorization")
    scalar = rational(factorization["coefficient"])
    require(type(factorization["factors"]) is list, "Factors must be a list")
    for factor in factorization["factors"]:
        _keys(factor, ("terms", "multiplicity", "geometric_degree"), label="factor")
        polynomial(factor["terms"])
    if H:
        pattern = V.validated_factor_pattern(H6, factorization)
    else:
        require(scalar == 0 and factorization["factors"] == [], "Zero must have the empty factorization")
        pattern = []
    require(type(leading["geometric_root_pattern"]) is list
            and all(type(x) is int for x in leading["geometric_root_pattern"])
            and leading["geometric_root_pattern"] == pattern, "Incorrect geometric root pattern")
    spaces = report["classification"]
    require(type(spaces) is dict, "Classification must be an object")
    family = "multiplicity_" + "_".join(map(str, pattern)) if H else "zero"
    require(spaces.get("family") == family, "Incorrect classification family")
    method, data = _recognize(H, pattern, factorization["factors"], schema)
    require((report["status"] == "classified") == (method is not None),
            "Classification status suppresses or invents a supported family")
    require(spaces.get("method") == (method or "leading_form"), "Method disagrees with the independently recognized theorem family")
    boundary = report["proof_boundary"]
    _keys(boundary, ("formalized", "arithmetic", "sympy_version", "dependencies", "completeness", "definitions"),
          optional=("per_input_checks",), label="proof boundary")
    require(boundary["formalized"] is False, "The public classifier is not an end-to-end Lean theorem")
    require(boundary["definitions"] == DEFINITIONS, "The contraction/refinement convention was altered")
    require(boundary["arithmetic"] == "exact rational arithmetic; no approximate roots or numerical rank tests",
            "The exact arithmetic claim was altered")
    require(boundary["sympy_version"] is None or type(boundary["sympy_version"]) is str,
            "Malformed producer-version annotation")
    require(type(boundary["completeness"]) is str and bool(boundary["completeness"]), "Missing completeness boundary")
    dependencies = boundary["dependencies"]
    require(type(dependencies) is list and all(type(x) is str for x in dependencies)
            and len(set(dependencies)) == len(dependencies),
            "Missing or malformed theorem dependencies")
    require(set(dependencies) <= {THEOREM, EXTENSION, QUADRATIC, SEPARABLE, WEIGHTED},
            "Unknown theorem dependency in this verifier version")
    if method == "sixfold_separable_complement":
        require(set(dependencies) == {SEPARABLE}, "Separable classification depends exactly on its complete static-space theorem")
    elif method == "sixfold_weighted_separable":
        require(set(dependencies) == {SEPARABLE, WEIGHTED}, "Weighted classification depends exactly on its static-space and transfer theorems")
    else:
        require(THEOREM in dependencies, "Missing homogeneous classification dependency")
        if H and any(0 < sum(k) < 6 for k in H):
            require(EXTENSION in dependencies, "Inhomogeneous report omits its leading-form dependency")
        if method == "sixfold_quadratic_complement":
            require(QUADRATIC in dependencies, "Quadratic report omits Theorems A-E")
    if "per_input_checks" in boundary:
        require(type(boundary["per_input_checks"]) is list and all(type(x) is str for x in boundary["per_input_checks"]),
                "Malformed per-input annotations")
    return pattern, method, data


def _space(space):
    require(type(space) is dict, "A classified space must be an object")
    kind = space.get("kind")
    if kind == "finite_basis":
        _keys(space, ("kind", "dimension", "basis"), label="finite space")
        require(type(space["basis"]) is list, "Basis must be a list")
        basis = [polynomial(G) for G in space["basis"]]
        require(type(space["dimension"]) is int and space["dimension"] == len(basis) == V.span_rank(basis),
                "Finite basis has an incorrect dimension or dependent vectors")
        return basis
    require(kind in ("polynomial_family", "module_plus_finite"), "Unknown space representation")
    fields = {"kind", "dimension", "coefficient_generators", "module_basis", "description"}
    if kind == "module_plus_finite":
        fields.add("finite_span")
    _keys(space, fields, label="module space")
    require(space["dimension"] is None and type(space["description"]) is str, "Malformed module metadata")
    require(type(space["coefficient_generators"]) is list and type(space["module_basis"]) is list,
            "Module generators must be lists")
    generators = [polynomial(G) for G in space["coefficient_generators"]]
    module = [polynomial(G) for G in space["module_basis"]]
    require(bool(generators) and bool(module) and all(generators) and all(module), "Empty or zero module generators")
    finite = [polynomial(G) for G in space.get("finite_span", [])]
    require(kind != "module_plus_finite" or bool(finite), "Missing finite complement")
    return finite + module


def _determinant_polynomial(matrix):
    total = {}
    for perm in permutations(range(len(matrix))):
        sign = (-1) ** sum(perm[i] > perm[j] for i in range(len(perm)) for j in range(i + 1, len(perm)))
        term = dict(ONE)
        for i, j in enumerate(perm):
            term = E.multiply(term, matrix[i][j])
        total = E.add(total, E.scale(term, sign))
    return total


def _module_equal(space, inverse, width, finite):
    """Exact equality with Q[x]{1,y,...,y^(width-1)} + span(finite).

    A constant nonzero module determinant proves equality over Q[x].  Quotient
    by that whole module before comparing the finite span; no degree sampling.
    """
    _space(space)
    if width == 0:
        require(space["kind"] == "finite_basis", "Expected a finite space")
        actual = [substitute(polynomial(G), *inverse) for G in space["basis"]]
        require(V.same_span(actual, finite), "Finite space differs from the theorem's exact space")
        return
    require(space["kind"] == ("module_plus_finite" if finite else "polynomial_family"),
            "Incorrect module/finite-space kind")
    generators = [substitute(polynomial(G), *inverse) for G in space["coefficient_generators"]]
    require(len(generators) == 1 and V.total_degree(generators[0]) == 1
            and generators[0].get((1, 0), F(0)) != 0 and all(b == 0 for a, b in generators[0]),
            "Coefficient ring must be exactly Q[L]")
    module = [substitute(polynomial(G), *inverse) for G in space["module_basis"]]
    require(len(module) == width and all(b < width for G in module for a, b in G),
            "Incorrect rank or complementary degree of the module")
    matrix = [[{(a, 0): v for (a, b), v in G.items() if b == j} for G in module] for j in range(width)]
    det = _determinant_polynomial(matrix)
    require(det and set(det) == {(0, 0)}, "Reported module is a proper submodule; its determinant is not a unit")
    actual = [substitute(polynomial(G), *inverse) for G in space.get("finite_span", [])]
    quotient = lambda G: {key: value for key, value in G.items() if key[1] >= width}
    actual, expected = list(map(quotient, actual)), list(map(quotient, finite))
    require(len(actual) == V.span_rank(actual) and V.same_span(actual, expected),
            "Finite complement differs from the exact quotient by the polynomial module")


def _family_exact(H, report, pattern, recognized, degree):
    spaces = report["classification"]
    if pattern == []:
        for name in ("S1", "S2", "Dinf"):
            space = spaces[name]
            require(space["kind"] == "polynomial_family", "Zero has the whole polynomial ring")
            gens = [polynomial(G) for G in space["coefficient_generators"]]
            bases = [polynomial(G) for G in space["module_basis"]]
            require(len(gens) == 2 and all(V.total_degree(G) == 1 for G in gens)
                    and V.span_rank([ONE] + gens) == 3 and len(bases) == 1 and set(bases[0]) == {(0, 0)},
                    "Zero must describe all of Q[q,p]")
        return [{(a, n-a): F(1)} for n in range(degree + 1) for a in range(n + 1)]
    factors = report["leading"]["factorization"]["factors"]
    if pattern == [3, 3]:
        expected = recognized or _quadratic_generator(H, factors)
        for name in ("S1", "S2", "Dinf"):
            space = spaces[name]
            gens = [polynomial(G) for G in space["coefficient_generators"]]
            modules = [polynomial(G) for G in space["module_basis"]]
            require(len(gens) == 1 and V.same_span([ONE, gens[0]], [ONE, expected])
                    and len(modules) == 1 and set(modules[0]) == {(0, 0)},
                    "Triple-pair space must be the full polynomial algebra in its quadratic generator")
        return [E.power(expected, power) for power in range(degree // 2 + 1)]
    L = polynomial(next(f["terms"] for f in factors if f["multiplicity"] == pattern[0]))
    M = Y if L.get((1, 0), 0) else X
    _, inverse = chart(L, M)
    coefficient = transverse(H, L)
    width = 3 if pattern == [6] and V.total_degree(coefficient) <= 1 else 2
    for name in ("S1", "S2", "Dinf"):
        _module_equal(spaces[name], inverse, width, [])
    return [E.multiply(E.power(L, a), E.power(M, j))
            for j in range(width) for a in range(degree - j + 1)]


def kernels(H, exponents, depth):
    """Literal defining-star outputs, never projected back to the input box."""
    current = [{key: F(1)} for key in exponents]
    images = [{} for _ in exponents]
    result = []
    for iterate in range(depth + 1):
        for image, G in zip(images, current):
            for hbar, defect in E.defects(H, G).items():
                for key, value in defect.items():
                    image[iterate, hbar, key] = value
        rows = sorted({key for image in images for key in image})
        matrix = [[image.get(row, F(0)) for image in images] for row in rows]
        result.append([{key: c for key, c in zip(exponents, vector) if c}
                       for vector in V.nullspace(matrix, len(exponents))])
        current = [E.poisson(H, G) for G in current]
    return result


def _bounded(H, report, degree, family_window=None):
    if family_window is None:
        return [V.check_bounded_kernel(H, report, degree, depth) for depth in (1, 2)]
    # A general unimodular module basis may contain high-degree terms that
    # cancel.  Filtering its generators by degree would lose legitimate low
    # polynomials.  The exact module equality supplies this canonical slice.
    exponents = [(a, n-a) for n in range(degree + 1) for a in range(n + 1)]
    actual = kernels(H, exponents, 2)
    for depth in (1, 2):
        require(V.same_span(actual[depth], family_window), "Independent family-kernel mismatch")
    return [{"degree": degree, "refinement_depth": depth, "homogeneous_slice": False,
             "dimension": len(actual[depth])} for depth in (1, 2)]


def _schema1(H, report, pattern, recognized, degree):
    spaces = report["classification"]
    _keys(spaces, ("family", "method", "sufficient_refinement_depth", "S1", "S2", "Dinf"), label="schema-1 classification")
    for name in ("S1", "S2", "Dinf"):
        _space(spaces[name])
    _legacy_certificates(report)
    V.check_report(H, report)
    family_window = None
    if not H or pattern in ([6], [5, 1], [3, 3]):
        family_window = _family_exact(H, report, pattern, recognized, degree)
    return {"bounded_kernels": _bounded(H, report, degree, family_window), "exact_family_structure": family_window is not None}


def _legacy_certificates(report):
    witness = report["obstruction"]
    if witness is not None:
        _keys(witness, ("G", "iterate", "D2G", "T3", "T5"), label="second-iterate obstruction")
        require(type(witness["iterate"]) is int and witness["iterate"] == 2, "Incorrect obstruction iterate")
        for key in ("G", "D2G", "T3", "T5"):
            polynomial(witness[key])
    lift = report["quadratic_lift"]
    if lift is None:
        return
    require(type(lift) is dict and lift.get("status") in ("present", "absent"), "Invalid quadratic-lift status")
    fields = {"status", "leading_candidate"}
    if lift["status"] == "present":
        fields |= {"linear_correction", "coefficients"}
    if "system" in lift:
        fields |= {"system", "uniqueness_certificate" if lift["status"] == "present" else "inconsistency_certificate"}
    _keys(lift, fields, label="quadratic lift")
    polynomial(lift["leading_candidate"])
    if lift["status"] == "present":
        polynomial(lift["linear_correction"])
        _keys(lift["coefficients"], ("alpha", "beta"), label="lift coefficients")
        for value in lift["coefficients"].values():
            rational(value)
    if "system" not in lift:
        return
    system = lift["system"]
    _keys(system, ("unknowns", "row_count", "rank", "augmented_rank"), label="lift system")
    require(system["unknowns"] == ["alpha", "beta"], "Lift columns have the wrong interpretation")
    require(all(type(system[k]) is int and system[k] >= 0 for k in ("row_count", "rank", "augmented_rank")),
            "Lift ranks and row count must be nonnegative integers")
    certificate = lift["uniqueness_certificate" if lift["status"] == "present" else "inconsistency_certificate"]
    _keys(certificate, ("rows", "determinant"), label="lift determinant certificate")
    rational(certificate["determinant"])
    require(type(certificate["rows"]) is list, "Lift certificate rows must be a list")
    for row in certificate["rows"]:
        _keys(row, ("gate", "q", "p", "coefficients", "rhs"), label="lift certificate row")
        require(type(row["gate"]) is int and row["gate"] in (3, 5)
                and type(row["q"]) is int and type(row["p"]) is int and min(row["q"], row["p"]) >= 0,
                "Lift row must name an actual gate coefficient")
        require(type(row["coefficients"]) is list and len(row["coefficients"]) == 2, "Lift row must have two columns")
        for value in row["coefficients"] + [row["rhs"]]:
            rational(value)


def _stage_contract(spaces, *, quadratic=False):
    base = {"family", "method", "derived_from", "depth", "stages", "Dinf", "sharpness_witness", "obstruction", "quadratic_lift"}
    extra = {"regime", "coordinates", "square_first_integral"} if quadratic else set()
    _keys(spaces, base | extra, label="schema-2 classification")
    _keys(spaces["depth"], ("kind", "value"), label="refinement depth")
    d = spaces["depth"]["value"]
    require(type(d) is int and 0 <= d <= 16 and spaces["depth"]["kind"] in ("least", "sufficient"), "Malformed refinement depth")
    require(type(spaces["stages"]) is list and bool(spaces["stages"]), "Missing refinement stages")
    for index, stage in enumerate(spaces["stages"]):
        require(type(stage) is dict and stage.get("status") in ("classified", "unknown"), "Invalid stage status")
        _keys(stage, ("index", "status", "space") if stage["status"] == "classified" else ("index", "status", "space", "reason"), label="stage")
        require(type(stage["index"]) is int and stage["index"] == index, "Stages must be indexed consecutively from zero")
        if stage["status"] == "unknown":
            require(stage["space"] is None and type(stage["reason"]) is str and bool(stage["reason"]), "Unknown stage must carry a reason and no space")
        else:
            _space(stage["space"])
    _space(spaces["Dinf"])
    return d


def _constant_expected(Ht):
    c = Ht[(0, 2)]
    b = {(a, 0): v / c for (a, j), v in Ht.items() if j == 1}
    f = {(a, 0): v / c for (a, j), v in Ht.items() if j == 0}
    m = V.total_degree(b)
    P = E.add(Y, E.scale(b, F(1, 2)))
    potential = E.add(f, E.scale(E.power(b, 2), F(-1, 4)))
    low = [ONE, X, E.power(X, 2)]
    six = low + [P, E.multiply(X, P), Ht]
    if m <= 1:
        return "affine_shift", [(3, []), (2, [E.power(Y, 2)]),
            (1, [Y, E.multiply(X, Y), E.power(Y, 2)]), (0, six), (0, low + [Ht]), (0, [ONE, Ht])]
    extras = []
    if m == 2:
        xi = E.add(Y, E.scale(E.derivative(f, q=2), 1 / (3 * E.derivative(b, q=2)[(0, 0)])))
        for power in (1, 2):
            extras.append({(a, j + 2): v / ((j + 1) * (j + 2)) for (a, j), v in E.power(xi, power).items()})
    stages = [(2, [E.power(Y, 2)] + extras), (1, [Y, E.multiply(X, Y), Ht]), (0, six)]
    n = V.total_degree(potential)
    if n >= 4:
        return "generic_nonlinear", stages + [(0, low + [Ht]), (0, [ONE, Ht])]
    if n == 3:
        return "cubic_potential", stages + [(0, low + [P, Ht]), (0, [ONE, X, P, Ht]), (0, [ONE, X, Ht]), (0, [ONE, Ht])]
    return "hidden_quadratic", stages


def _check_first_failure(H, witness, depth):
    _keys(witness, ("G", "first_failing_iterate"), label="sharpness witness")
    require(type(witness["first_failing_iterate"]) is int and witness["first_failing_iterate"] == depth,
            "Incorrect sharpness-witness depth")
    G = polynomial(witness["G"])
    for iterate in range(depth + 1):
        require(bool(E.defects(H, G)) == (iterate == depth), "Sharpness witness fails at the wrong iterate")
        G = E.poisson(H, G)


def _quadratic(H, report, degree):
    spaces = report["classification"]
    d = _stage_contract(spaces, quadratic=True)
    require(spaces["derived_from"] == "hamiltonian-quadratic-sixfold/1"
            and spaces["depth"]["kind"] == "least" and d >= 1 and len(spaces["stages"]) == d + 1,
            "Quadratic stages must run through the least stabilization depth")
    require(spaces["obstruction"] is None and spaces["quadratic_lift"] is None, "Unexpected legacy quadratic certificate")
    coordinates = spaces["coordinates"]
    _keys(coordinates, ("L", "M"), label="quadratic coordinates")
    L, M = polynomial(coordinates["L"]), polynomial(coordinates["M"])
    _, inverse = chart(L, M)
    Ht = substitute(H, *inverse)
    require(max(j for a, j in Ht) == 2 and {k for k in Ht if sum(k) == 6} == {(6, 0)},
            "Reported chart does not give a quadratic complement with a sixfold leading form")
    cdegree = max(a for (a, j) in Ht if j == 2)
    bdegree = max((a for (a, j) in Ht if j == 1), default=-1)
    checks = {}
    if cdegree == 0:
        regime, expected = _constant_expected(Ht)
        require(spaces["regime"] == regime and len(expected) == len(spaces["stages"]), "Incorrect quadratic regime or least depth")
        for stage, (width, finite) in zip(spaces["stages"], expected):
            require(stage["status"] == "classified", "Constant-coefficient stages must all be classified")
            _module_equal(stage["space"], inverse, width, finite)
            # These identities include the degree-ten static generator, which
            # lies outside the separate default total-degree-six comparison.
            for G in _space(stage["space"]):
                V.gates_through(H, G, stage["index"])
        _module_equal(spaces["Dinf"], inverse, *expected[-1])
        require(spaces["square_first_integral"] is None, "Unexpected variable-coefficient square integral")
        exponents = [(a, n - a) for n in range(degree + 1) for a in range(n + 1)]
        actual = kernels(Ht, exponents, d)
        for index, stage in enumerate(spaces["stages"]):
            # Exact module equality above covers omitted high-degree generators.
            # Here a second independent kernel calculation checks its intersection.
            width, finite = expected[index]
            span = [{(a, j): F(1)} for j in range(width) for a in range(degree - j + 1)]
            span += [G for G in finite if V.total_degree(G) <= degree]
            require(V.same_span(actual[index], span), f"Independent total-degree kernel mismatch at stage {index}")
        checks["total_degree_window"] = {"degree": degree, "dimensions": [len(k) for k in actual]}
        checks["exact_module_and_finite_quotient_equalities"] = len(expected)
    else:
        require(spaces["regime"] == "variable_top_coefficient", "Incorrect variable-coefficient regime")
        require(spaces["stages"][0]["status"] == "unknown" and all(s["status"] == "classified" for s in spaces["stages"][1:]),
                "Only the variable-coefficient static space is unknown")
        if cdegree == 1:
            wx, wy, bound = (1, 3, 13) if bdegree == 4 else (2, 5, 22)
        elif cdegree == 2:
            wx, wy, bound = (2, 4, 18) if bdegree == 4 else (2, 4, 24)
        else:
            require(cdegree == 3, "Invalid quadratic coefficient degree")
            wx, wy, bound = 2, 3, 26
        exponents = [(a, j) for j in range(bound // wy + 1) for a in range((bound - wy * j) // wx + 1)]
        actual = kernels(Ht, exponents, d + 1)
        for index, stage in enumerate(spaces["stages"][1:], start=1):
            require(stage["space"]["kind"] == "finite_basis", "Variable-coefficient refinements must be finite")
            basis = [substitute(polynomial(G), *inverse) for G in stage["space"]["basis"]]
            require(V.same_span(actual[index], basis), f"Full weighted-box kernel mismatch at stage {index}")
        core = [substitute(polynomial(G), *inverse) for G in spaces["Dinf"]["basis"]]
        require(V.same_span(actual[d], core) and V.same_span(actual[d + 1], core), "Core disagrees with stabilization in the full weighted box")
        checks["theorem_D_weighted_box"] = {"L_weight": wx, "M_weight": wy, "bound": bound,
            "monomials": len(exponents), "dimensions": [len(k) for k in actual], "output_truncated": False}
        integral = spaces["square_first_integral"]
        require((integral is not None) == (len(core) == 3), "Three-dimensional variable core requires its square first integral")
        require(len(core) in (2, 3), "Variable core violates the closed dimension criterion")
        if integral is not None:
            Q = polynomial(integral)
            require(V.total_degree(Q) > 0 and not E.poisson(H, Q) and not E.defects(H, Q), "Invalid square first integral")
            square = E.power(Q, 2)
            pivot = next(k for k in square if sum(k))
            scale = H.get(pivot, F(0)) / square[pivot]
            require(scale != 0 and V.total_degree(E.add(H, E.scale(square, -scale))) <= 0,
                    "Hamiltonian is not a nonzero multiple of the claimed integral squared plus a constant")
            require(V.same_span(core, [ONE, Ht, substitute(Q, *inverse)]), "Square integral does not span the exceptional core")
    require(spaces["Dinf"]["kind"] == "finite_basis", "Quadratic core must be finite")
    core = [polynomial(G) for G in spaces["Dinf"]["basis"]]
    require(V.same_span(core, core + [ONE, H]), "Core must contain both 1 and H")
    final = spaces["stages"][-1]["space"]
    require(final["kind"] == "finite_basis" and V.same_span(core, [polynomial(G) for G in final["basis"]]), "Final stage differs from the core")
    for G in core:
        V.gates_through(H, G, d)
        require(V.same_span(core, core + [E.poisson(H, G)]), "Core is not invariant under the unprojected Poisson derivation")
    _check_first_failure(H, spaces["sharpness_witness"], d)
    return checks


def _schema2(H, report, pattern, method, recognized, degree):
    spaces = report["classification"]
    if method == "sixfold_quadratic_complement":
        return _quadratic(H, report, degree)
    if method == "sixfold_separable_complement":
        return _separable(H, report)
    if method == "sixfold_weighted_separable":
        return _weighted(H, report)
    d = _stage_contract(spaces)
    require(spaces["derived_from"] == SCHEMA1 and spaces["depth"]["kind"] == "sufficient"
            and len(spaces["stages"]) == 3 and spaces["stages"][0]["status"] == "unknown"
            and all(s["status"] == "classified" for s in spaces["stages"][1:]),
            "Schema-1-derived stage layout is inconsistent")
    require(spaces["sharpness_witness"] is None, "Sufficient-depth adapter has no least-depth witness")
    adapted = dict(report)
    adapted["schema"] = SCHEMA1
    adapted["classification"] = {"family": spaces["family"], "method": spaces["method"],
        "sufficient_refinement_depth": d, "S1": spaces["stages"][1]["space"],
        "S2": spaces["stages"][2]["space"], "Dinf": spaces["Dinf"]}
    adapted["obstruction"], adapted["quadratic_lift"] = spaces["obstruction"], spaces["quadratic_lift"]
    return _schema1(H, adapted, pattern, recognized, degree)


def _separable(H, report):
    import verify_separable_sixfold as S
    spaces = report["classification"]
    _keys(spaces, ("family", "method", "derived_from", "regime", "coordinates", "normal_form", "depth", "stages", "Dinf",
                   "sharpness_witness", "drop_witnesses", "obstruction", "quadratic_lift"), label="separable classification")
    require(spaces["obstruction"] is None and spaces["quadratic_lift"] is None, "Unexpected legacy separable certificate")
    coordinates = spaces["coordinates"]
    _keys(coordinates, ("L", "M", "determinant"), label="separable coordinates")
    polynomial(coordinates["L"])
    polynomial(coordinates["M"])
    rational(coordinates["determinant"])
    normal = spaces["normal_form"]
    _keys(normal, ("f", "g", "degree_f", "degree_g"), label="separable normal form")
    polynomial(normal["f"])
    polynomial(normal["g"])
    _keys(spaces["depth"], ("kind", "value"), label="separable depth")
    require(type(spaces["stages"]) is list, "Missing separable stages")
    for stage in spaces["stages"]:
        _keys(stage, ("index", "status", "space"), label="separable stage")
        _space(stage["space"])
    _space(spaces["Dinf"])
    require(type(spaces["drop_witnesses"]) is list, "Missing strict-drop witnesses")
    for witness in spaces["drop_witnesses"] + [spaces["sharpness_witness"]]:
        _keys(witness, ("G", "first_failing_iterate", "DiG", "T3", "T5"), label="separable drop witness")
        for key in ("G", "DiG", "T3", "T5"):
            polynomial(witness[key])
    try:
        return {"separable_full_static_box": S.check_report(H, report)}
    except S.VerificationError as exc:
        raise VerificationError(str(exc)) from exc


def _weighted(H, report):
    import verify_weighted_separable as W
    spaces = report["classification"]
    _keys(spaces, ("family", "method", "derived_from", "regime", "coordinates", "weighted_model", "depth", "stages", "Dinf",
                   "sharpness_witness", "drop_witnesses", "obstruction", "quadratic_lift"), label="weighted classification")
    require(spaces["obstruction"] is None and spaces["quadratic_lift"] is None, "Unexpected legacy weighted certificate")
    coordinates = spaces["coordinates"]
    _keys(coordinates, ("L", "M", "determinant"), label="weighted coordinates")
    polynomial(coordinates["L"])
    polynomial(coordinates["M"])
    rational(coordinates["determinant"])
    model = spaces["weighted_model"]
    _keys(model, ("degree_f", "degree_g", "weights", "hamiltonian_weight", "static_bound", "leading", "lower"), label="weighted model")
    _keys(model["weights"], ("L", "M"), label="weights")
    require(all(type(value) is int and value > 0 for value in
            [model["degree_f"], model["degree_g"], model["hamiltonian_weight"], model["static_bound"], *model["weights"].values()]),
            "Weights, degrees and bounds must be positive integers")
    polynomial(model["leading"])
    polynomial(model["lower"])
    _keys(spaces["depth"], ("kind", "value"), label="weighted depth")
    require(type(spaces["stages"]) is list, "Missing weighted stages")
    for stage in spaces["stages"]:
        _keys(stage, ("index", "status", "space"), label="weighted stage")
        _space(stage["space"])
    _space(spaces["Dinf"])
    require(type(spaces["drop_witnesses"]) is list, "Missing weighted strict-drop witnesses")
    for witness in spaces["drop_witnesses"] + [spaces["sharpness_witness"]]:
        _keys(witness, ("G", "first_failing_iterate", "DiG", "T3", "T5", "gates"), label="weighted drop witness")
        for key in ("G", "DiG", "T3", "T5"):
            polynomial(witness[key])
        _keys(witness["gates"], ("3", "5"), label="sextic odd gates")
        for value in witness["gates"].values():
            polynomial(value)
    try:
        return {"weighted_full_static_box": W.check_report(H, report)}
    except W.VerificationError as exc:
        raise VerificationError(str(exc)) from exc


def _unsupported(report):
    require(type(report.get("unsupported_reason")) is str and bool(report["unsupported_reason"]), "Unsupported result needs a reason")
    spaces = report["classification"]
    if report["schema"] == SCHEMA1:
        _keys(spaces, ("family", "method", "sufficient_refinement_depth", "S1", "S2", "Dinf"), label="unsupported classification")
        require(all(spaces[k] is None for k in ("S1", "S2", "Dinf", "sufficient_refinement_depth"))
                and report["obstruction"] is None and report["quadratic_lift"] is None, "Unsupported report contains a mathematical space or witness claim")
    else:
        _keys(spaces, ("family", "method", "derived_from", "depth", "stages", "Dinf", "sharpness_witness", "obstruction", "quadratic_lift"), label="unsupported classification")
        require(spaces["derived_from"] == SCHEMA1 and all(spaces[k] is None for k in
            ("depth", "stages", "Dinf", "sharpness_witness", "obstruction", "quadratic_lift")),
            "Unsupported report contains a mathematical space or witness claim")


def verify_report(H, report, *, degree=6):
    """Return a deterministic verification receipt, or raise VerificationError.

    The input is bound separately.  Producer provenance/annotations are not
    authenticated.  No classifier is called, including on unsupported reports.
    """
    try:
        require(type(H) is dict, "Independent input must be a sparse exact polynomial")
        for key, value in H.items():
            require(type(key) is tuple and len(key) == 2 and all(type(x) is int and x >= 0 for x in key), "Invalid independent-input exponent")
            require(type(value) is int or type(value) is F, "Independent-input coefficients must be exact rationals")
        H = {key: F(value) for key, value in H.items() if value}
        require(not H or V.total_degree(H) == 6, "Independent input must have degree six or be zero")
        require(type(degree) is int and degree >= 6, "Comparison degree must be an integer at least six")
        pattern, method, recognized = _metadata(H, report)
        if report["status"] == "unsupported":
            _unsupported(report)
            checks = {"supported_family_scope": "independently rejected; no space claimed"}
        elif report["schema"] == SCHEMA1:
            checks = _schema1(H, report, pattern, recognized, degree)
        else:
            checks = _schema2(H, report, pattern, method, recognized, degree)
        canonical = json.dumps(report, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
        paths = [Path(__file__).resolve(), HERE / "verify_sextic_core.py", HERE / "requirements.txt",
                 HERE.parent / "independent" / "engine.py"]
        for dependency in report["proof_boundary"]["dependencies"]:
            path = HERE.parents[2] / dependency
            require(path.is_file(), f"Named theorem dependency is missing: {dependency}")
            paths.append(path)
        if method in ("sixfold_separable_complement", "sixfold_weighted_separable"):
            paths.append(HERE / "verify_separable_sixfold.py")
        if method == "sixfold_weighted_separable":
            paths.append(HERE / "verify_weighted_separable.py")
        return {"schema": "hamiltonian-sextic-report-verification/1", "status": "PASS",
            "report_schema": report["schema"], "classification_status": report["status"],
            "input": E.serialize(H), "report_sha256": hashlib.sha256(canonical).hexdigest(),
            "family": report["classification"]["family"], "method": method,
            "checks": checks,
            "source_sha256": {str(path.relative_to(HERE.parents[2])): hashlib.sha256(path.read_bytes()).hexdigest() for path in sorted(set(paths))},
            "proof_boundary": {"classifier_called": False, "producer_import_required": False, "formalized": False,
                "all_degree_completeness": "conditional on the named written theorems; exact finite spaces and polynomial/module identities are independently checked",
                "unbounded_gate_outputs": True,
                "producer_provenance_authenticated": False,
                "free_text_annotations_verified": False}}
    except VerificationError:
        raise
    except ImportError as exc:
        raise VerificationError(f"Verification dependency unavailable: {exc}") from exc
    except (KeyError, TypeError, ValueError, IndexError, ZeroDivisionError, StopIteration, AttributeError) as exc:
        raise VerificationError(f"Malformed report: {type(exc).__name__}: {exc}") from exc


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", type=Path)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--H", help="Independent Hamiltonian in the exact CLI expression language")
    source.add_argument("--input-json", type=Path, help="Independent canonical polynomial term list")
    parser.add_argument("--degree", type=int, default=6)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    try:
        if args.H is not None:
            sys.path.insert(0, str(HERE.parent))
            import partner_lab
            H = partner_lab.parse(args.H)
        else:
            H = polynomial(load_json(args.input_json))
        receipt = verify_report(H, load_json(args.report), degree=args.degree)
        code = 0
    except (VerificationError, OSError, json.JSONDecodeError, ValueError) as exc:
        receipt = {"schema": "hamiltonian-sextic-report-verification/1", "status": "REJECTED", "reason": str(exc)}
        code = 2
    payload = json.dumps(receipt, sort_keys=True, indent=2) + "\n"
    if args.output is not None:
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
