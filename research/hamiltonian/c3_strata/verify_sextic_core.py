"""Independent bounded replay of the sextic-core classifier.

The checker expands the defining star product with independent/engine.py.  It
does not import the classifier's contractions, factorization, or kernel solver.
Finite kernel comparisons are explicitly bounded evidence, not all-degree
proofs.  Run this file for a deterministic JSON receipt; it writes no files.
"""
from __future__ import annotations

from fractions import Fraction as F
import hashlib
import importlib.util
from itertools import permutations, product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
_SPEC = importlib.util.spec_from_file_location(
    "sextic_independent_star_engine", HERE.parent / "independent" / "engine.py"
)
if _SPEC is None or _SPEC.loader is None:
    raise RuntimeError("Cannot load the independent star-exponential engine")
E = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(E)
_CLASSIFIER_SPEC = importlib.util.spec_from_file_location(
    "sextic_core_under_replay", HERE.parent / "sextic_core.py"
)
if _CLASSIFIER_SPEC is None or _CLASSIFIER_SPEC.loader is None:
    raise RuntimeError("Cannot load the sextic-core classifier")
C = importlib.util.module_from_spec(_CLASSIFIER_SPEC)
_CLASSIFIER_SPEC.loader.exec_module(C)


class VerificationError(RuntimeError):
    """An explicit failed replay condition, also active under python -O."""


def require(condition, message):
    if not condition:
        raise VerificationError(message)


def polynomial(terms):
    """Read the public exact serialization without using producer helpers."""
    require(isinstance(terms, list), "Polynomial terms must be a list")
    answer = {}
    for term in terms:
        require(isinstance(term, dict), "Polynomial term must be an object")
        a, b = term.get("q"), term.get("p")
        require(type(a) is int and type(b) is int and min(a, b) >= 0,
                "Polynomial exponents must be nonnegative integers")
        require((a, b) not in answer, "Duplicate serialized monomial")
        value = term.get("coefficient")
        require(isinstance(value, str), "Coefficients must be exact rational strings")
        try:
            answer[a, b] = F(value)
        except (ValueError, ZeroDivisionError) as exc:
            raise VerificationError("Invalid rational coefficient") from exc
    return {key: value for key, value in answer.items() if value}


def sparse_add(*polys):
    answer = {}
    for poly in polys:
        for key, value in poly.items():
            answer[key] = answer.get(key, F(0)) + F(value)
    return {key: value for key, value in answer.items() if value}


def sparse_product(left, right):
    answer = {}
    for (a, b), x in left.items():
        for (c, d), y in right.items():
            key = a + c, b + d
            answer[key] = answer.get(key, F(0)) + F(x) * F(y)
    return {key: value for key, value in answer.items() if value}


def sparse_power(poly, exponent):
    answer = {(0, 0): F(1)}
    for _ in range(exponent):
        answer = sparse_product(answer, poly)
    return answer


def affine_substitute(poly, matrix=((1, 0), (0, 1)), shift=(0, 0), scalar=1):
    """Literal sparse substitution, independent of all producer transforms."""
    (a, b), (c, d) = matrix
    left = {(1, 0): F(a), (0, 1): F(b), (0, 0): F(shift[0])}
    right = {(1, 0): F(c), (0, 1): F(d), (0, 0): F(shift[1])}
    left = {k: v for k, v in left.items() if v}
    right = {k: v for k, v in right.items() if v}
    answer = {}
    for (i, j), coefficient in poly.items():
        term = sparse_product(sparse_power(left, i), sparse_power(right, j))
        answer = sparse_add(answer, {k: F(scalar) * coefficient * v
                                     for k, v in term.items()})
    return answer


def total_degree(poly):
    return max((sum(key) for key in poly), default=-1)


def rank(rows, width):
    """Independent exact row elimination, used only to compare spans."""
    work = [[F(x) for x in row] for row in rows]
    pivot_row = 0
    for column in range(width):
        pivot = next((i for i in range(pivot_row, len(work))
                      if work[i][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        divisor = work[pivot_row][column]
        work[pivot_row] = [v / divisor for v in work[pivot_row]]
        for i in range(pivot_row + 1, len(work)):
            if work[i][column]:
                factor = work[i][column]
                work[i] = [x - factor * y
                           for x, y in zip(work[i], work[pivot_row])]
        pivot_row += 1
        if pivot_row == len(work):
            break
    return pivot_row


def span_rank(polys):
    keys = sorted({key for poly in polys for key in poly})
    return rank([[poly.get(key, F(0)) for key in keys] for poly in polys], len(keys))


def nullspace(rows, width):
    """Forward elimination and back substitution, separate from E.nullspace."""
    work = [[F(x) for x in row] for row in rows]
    pivots = []
    for column in range(width):
        index = len(pivots)
        pivot = next((i for i in range(index, len(work)) if work[i][column]), None)
        if pivot is None:
            continue
        work[index], work[pivot] = work[pivot], work[index]
        for i in range(index + 1, len(work)):
            if work[i][column]:
                factor = work[i][column] / work[index][column]
                work[i] = [x - factor * y for x, y in zip(work[i], work[index])]
        pivots.append(column)
        if len(pivots) == len(work):
            break
    answer = []
    for free in (j for j in range(width) if j not in pivots):
        vector = [F(0)] * width
        vector[free] = F(1)
        for row, pivot in reversed(list(enumerate(pivots))):
            vector[pivot] = -sum(work[row][j] * vector[j] for j in range(pivot + 1, width)) / work[row][pivot]
        answer.append(vector)
    return answer


def same_span(left, right):
    return span_rank(left) == span_rank(right) == span_rank(left + right)


def space_basis(space):
    require(space.get("kind") == "finite_basis", "Expected a finite-basis space")
    basis = [polynomial(poly) for poly in space.get("basis", [])]
    require(type(space.get("dimension")) is int, "Finite dimension must be an integer")
    require(len(basis) == space["dimension"] == span_rank(basis),
            "Reported finite basis has the wrong dimension or is dependent")
    return basis


def family_samples(space, powers=(0, 1, 2)):
    require(space.get("kind") == "polynomial_family", "Expected a polynomial family")
    require(space.get("dimension") is None, "Infinite family must have null dimension")
    generators = [polynomial(p) for p in space.get("coefficient_generators", [])]
    modules = [polynomial(p) for p in space.get("module_basis", [])]
    require(bool(generators) and bool(modules), "Family description is incomplete")
    answer = []
    for exponents in product(powers, repeat=len(generators)):
        coefficient = {(0, 0): F(1)}
        for generator, exponent in zip(generators, exponents):
            coefficient = sparse_product(coefficient, sparse_power(generator, exponent))
        answer.extend(sparse_product(coefficient, base) for base in modules)
    return answer


def gates_through(H, G, depth):
    current = G
    for iterate in range(depth + 1):
        require(not E.defects(H, current),
                f"Nonzero defining-star defect at iterate {iterate}")
        current = E.poisson(H, current)


def small_determinant(rows):
    n = len(rows)
    require(n in (2, 3) and all(len(row) == n for row in rows),
            "Lift certificate must be a two- or three-row square determinant")
    answer = F(0)
    for perm in permutations(range(n)):
        sign = (-1) ** sum(perm[i] > perm[j] for i in range(n) for j in range(i + 1, n))
        term = F(sign)
        for i in range(n):
            term *= rows[i][perm[i]]
        answer += term
    return answer


def univariate_gcd_degree(left, right):
    """Degree of a rational-polynomial gcd, by literal Euclidean division."""
    left, right = dict(left), dict(right)
    while right:
        remainder = dict(left)
        right_degree = max(right)
        while remainder and max(remainder) >= right_degree:
            shift = max(remainder) - right_degree
            coefficient = remainder[max(remainder)] / right[right_degree]
            for degree, value in right.items():
                key = degree + shift
                remainder[key] = remainder.get(key, F(0)) - coefficient * value
                if not remainder[key]:
                    del remainder[key]
        left, right = right, remainder
    return max(left, default=-1)


def validated_factor_pattern(leading, factors):
    """Check a squarefree, coprime factor decomposition without refactoring H.

    Irreducibility is unnecessary: a squarefree homogeneous degree-d factor has
    d distinct geometric roots.  Distinct factors must share no projective root.
    """
    reconstructed = {(0, 0): F(factors["coefficient"])}
    previous = []
    pattern = []
    for factor in factors["factors"]:
        term = polynomial(factor["terms"])
        degree, multiplicity = factor["geometric_degree"], factor["multiplicity"]
        require(type(degree) is int and degree >= 1 and type(multiplicity) is int and multiplicity >= 1,
                "Factor degrees and multiplicities must be positive integers")
        require(term and all(sum(key) == degree for key in term),
                "Incorrect homogeneous factor degree")
        affine = {a: value for (a, b), value in term.items()}
        infinity = degree - max(affine)
        derivative = {a - 1: a * value for a, value in affine.items() if a}
        require(infinity in (0, 1) and univariate_gcd_degree(affine, derivative) == 0,
                "Reported geometric factor is not squarefree")
        for old_affine, old_infinity in previous:
            require(not (infinity and old_infinity) and univariate_gcd_degree(affine, old_affine) == 0,
                    "Reported geometric factors share a projective root")
        previous.append((affine, infinity))
        pattern.extend([multiplicity] * degree)
        reconstructed = sparse_product(reconstructed, sparse_power(term, multiplicity))
    require(reconstructed == leading, "Factorization does not reconstruct the leading form")
    require(sum(pattern) == 6, "Geometric multiplicities do not sum to six")
    return sorted(pattern, reverse=True)


def check_lift_certificate(H, lift):
    """Replay the tiny reported linear-system minors through star expansion."""
    J2 = polynomial(lift["leading_candidate"])
    require(J2 and all(sum(key) == 2 for key in J2),
            "Quadratic candidate must be nonzero and homogeneous of degree two")
    leading = {key: value for key, value in H.items() if sum(key) == 6}
    gates_through(leading, J2, 1)
    if "system" not in lift:
        return
    images = []
    for G in (J2, {(1, 0): F(1)}, {(0, 1): F(1)}):
        defects = E.defects(H, E.poisson(H, G))
        image = {}
        for hbar, gate, multiplier in ((2, 3, -24), (4, 5, 1920)):
            for (a, b), value in defects.get(hbar, {}).items():
                image[gate, a, b] = multiplier * value
        images.append(image)
    keys = sorted({key for image in images for key in image})
    require(lift["system"]["row_count"] == len(keys), "Lift system has the wrong row count")
    require(rank([[images[i].get(key, F(0)) for i in (1, 2)] for key in keys], 2) == 2,
            "Lift linear part is not independently injective")
    present = lift["status"] == "present"
    require(lift["status"] in ("present", "absent"), "Unknown quadratic-lift status")
    for field, expected in (("rank", 2), ("augmented_rank", 2 if present else 3)):
        value = lift["system"].get(field)
        require(type(value) is int and value == expected, f"Incorrect lift system {field}")
    certificate = lift["uniqueness_certificate" if present else "inconsistency_certificate"]
    matrix = []
    seen = set()
    for row in certificate["rows"]:
        key = row["gate"], row["q"], row["p"]
        require(key in keys and key not in seen, "Invalid or duplicate lift-certificate row")
        seen.add(key)
        coefficients = [F(x) for x in row["coefficients"]]
        rhs = F(row["rhs"])
        require(coefficients == [images[i].get(key, F(0)) for i in (1, 2)] and
                rhs == -images[0].get(key, F(0)), "Lift row does not match the defining star expansion")
        matrix.append(coefficients if present else coefficients + [rhs])
    determinant = small_determinant(matrix)
    require(determinant != 0 and determinant == F(certificate["determinant"]),
            "Incorrect affine-lift determinant")
    if present:
        alpha, beta = (F(lift["coefficients"][name]) for name in ("alpha", "beta"))
        correction = {key: value for key, value in (((1, 0), alpha), ((0, 1), beta)) if value}
        require(polynomial(lift["linear_correction"]) == correction,
                "Affine lift coefficients disagree with its polynomial")
        gates_through(H, sparse_add(J2, correction), 1)


def check_report(H, report, *, sample_powers=(0, 1, 2)):
    """Check supplied claims; this does not generate a classification."""
    H = {key: F(value) for key, value in H.items() if value}
    require(report.get("schema") in ("hamiltonian-sextic-core/1", "hamiltonian-sextic-core/2"), "Unexpected classifier schema")
    require(report.get("status") == "classified", "Expected a classified result")
    require(polynomial(report.get("input")) == H, "Input polynomial was not preserved")
    pattern = []
    if H:
        leading = {k: v for k, v in H.items() if sum(k) == 6}
        require(polynomial(report["leading"]["terms"]) == leading,
                "Leading polynomial does not match input")
        require(report["leading"]["infinity_multiplicity"] == min(b for a, b in leading),
                "Incorrect multiplicity at the projective point [1:0]")
        pattern = validated_factor_pattern(leading, report["leading"]["factorization"])
    require(report["leading"]["geometric_root_pattern"] == pattern,
            "Reported geometric root pattern disagrees with validated factors")
    spaces = report["classification"]
    family = "multiplicity_" + "_".join(map(str, pattern)) if H else "zero"
    require(spaces.get("family") == family, "Classification family disagrees with geometric root pattern")
    infinite = not H or pattern in ([6], [5, 1], [3, 3])
    if spaces["method"] == "sixfold_quadratic_complement":
        require(pattern == [6] and report["schema"].endswith("/2"),
                "Quadratic sixfold classification requires schema 2 and a sixfold leading form")
        infinite = False
    if spaces["method"] == "triple_pair_perturbation":
        require(pattern == [3, 3] and report["schema"].endswith("/2"),
                "Triple-pair perturbation classification requires schema 2 and a triple-pair leading form")
        require(spaces["S1"]["dimension"] in (2, 3) and spaces["Dinf"]["dimension"] == 2,
                "Incorrect finite dimensions for a triple-pair perturbation")
        infinite = False
    expected_kind = "polynomial_family" if infinite else "finite_basis"
    for name, depth in (("S1", 1), ("S2", 2), ("Dinf", 2)):
        space = spaces[name]
        require(space.get("kind") == expected_kind, "Space kind disagrees with the geometric stratum")
        if space["kind"] == "finite_basis":
            samples = space_basis(space)
            require(span_rank(samples + [{(0, 0): F(1)}, H]) == len(samples),
                    f"Finite {name} space must contain both 1 and H")
        else:
            samples = family_samples(space, sample_powers)
        for G in samples:
            gates_through(H, G, depth)
        if name == "Dinf" and space["kind"] == "finite_basis":
            for G in samples:
                require(span_rank(samples + [E.poisson(H, G)]) == len(samples),
                        "Finite invariant core is not closed under the classical derivation")
    if spaces["S2"]["kind"] == "finite_basis":
        first, core = space_basis(spaces["S1"]), space_basis(spaces["Dinf"])
        require(same_span(space_basis(spaces["S2"]), core),
                "S2 and invariant core differ in a finite classified result")
        require(span_rank(first + core) == len(first), "Invariant core is not a subspace of S1")
        loss = len(first) > len(core)
        if loss:
            require(report.get("obstruction") is not None,
                    "A lost S1 direction requires a second-iterate obstruction")
        else:
            require(report.get("obstruction") is None, "An invariant S1 cannot have a second-iterate obstruction")
        expected_depth = 2 if loss else 1
    else:
        require(report.get("obstruction") is None, "An invariant polynomial family cannot have an obstruction")
        expected_depth = 1 if H else 0
    require(type(spaces.get("sufficient_refinement_depth")) is int and
            spaces["sufficient_refinement_depth"] == expected_depth,
            "Refinement depth disagrees with the reported spaces and obstruction")
    lift = report.get("quadratic_lift")
    if pattern in ([4, 2], [4, 1, 1]):
        require(isinstance(lift, dict), "Fourfold stratum requires a quadratic lift report")
        perturbed = any(0 < sum(key) < 6 for key in H)
        require(("system" in lift) == perturbed, "Incorrect affine lift system presence")
        require(perturbed or lift.get("status") == "present",
                "A homogeneous fourfold stratum requires a quadratic lift")
        check_lift_certificate(H, lift)
        if lift.get("status") == "absent":
            require(spaces["S1"]["dimension"] == 2, "An absent lift requires dimension two")
    else:
        require(lift is None, "Unexpected quadratic lift outside the fourfold strata")
    if lift and lift.get("status") == "present":
        G = sparse_add(polynomial(lift["leading_candidate"]), polynomial(lift["linear_correction"]))
        first = space_basis(spaces["S1"])
        require(span_rank(first + [G]) == len(first), "Reported quadratic lift is missing from S1")
    first_witness = report.get("first_refinement_obstruction")
    obstruction_methods = ("sixfold_quadratic_complement", "triple_pair_perturbation")
    if spaces["method"] in obstruction_methods:
        require((first_witness is not None) == (spaces["S1"]["dimension"] == 2),
                "A failed quadratic lift requires a first-refinement witness")
    if first_witness is not None:
        require(spaces["method"] in obstruction_methods and first_witness["iterate"] == 1,
                "Unexpected first-refinement witness")
        G = polynomial(first_witness["G"])
        gates_through(H, G, 0)
        DG = E.poisson(H, G)
        require(polynomial(first_witness["DG"]) == DG, "Incorrect first classical iterate")
        defects = E.defects(H, DG)
        require(bool(defects), "Claimed first obstruction has no star defect")
        require(polynomial(first_witness["T3"]) == E.scale(defects.get(2, {}), -24),
                "Incorrect first T3 obstruction")
        require(polynomial(first_witness["T5"]) == E.scale(defects.get(4, {}), 1920),
                "Incorrect first T5 obstruction")
    witness = report.get("obstruction")
    if witness is not None:
        G = polynomial(witness["G"])
        first, core = space_basis(spaces["S1"]), space_basis(spaces["Dinf"])
        require(span_rank(first + [G]) == len(first), "Obstruction witness is missing from S1")
        require(span_rank(core + [G]) > len(core), "Obstruction witness belongs to the invariant core")
        require(witness.get("iterate") == 2, "Obstruction has the wrong iterate")
        gates_through(H, G, 1)
        D2G = E.poisson(H, E.poisson(H, G))
        require(polynomial(witness["D2G"]) == D2G, "Incorrect second classical iterate")
        defects = E.defects(H, D2G)
        require(bool(defects), "Claimed obstruction has no star defect")
        require(polynomial(witness["T3"]) == E.scale(defects.get(2, {}), -24),
                "Incorrect T3 obstruction polynomial")
        require(polynomial(witness["T5"]) == E.scale(defects.get(4, {}), 1920),
                "Incorrect T5 obstruction polynomial")
    return report


def kernel_on_monomials(H, exponents, depth):
    """Bounded kernel by the independently expanded defining star exponential."""
    images = []
    for exponent in exponents:
        image = {}
        current = {exponent: F(1)}
        for iterate in range(depth + 1):
            for hbar, poly in E.defects(H, current).items():
                for (a, b), coefficient in poly.items():
                    image[iterate, hbar, a, b] = coefficient
            current = E.poisson(H, current)
        images.append(image)
    keys = sorted({key for image in images for key in image})
    rows = [[image.get(key, F(0)) for image in images] for key in keys]
    return [{e: c for e, c in zip(exponents, vector) if c}
            for vector in nullspace(rows, len(exponents))]


def restrict_space(space, degree, *, homogeneous=False):
    allowed = (lambda key: sum(key) == degree) if homogeneous else (lambda key: sum(key) <= degree)
    if space["kind"] == "polynomial_family":
        samples = family_samples(space, tuple(range(degree + 1)))
        return [poly for poly in samples if poly and all(allowed(k) for k in poly)]
    basis = space_basis(space)
    forbidden = sorted({key for poly in basis for key in poly if not allowed(key)})
    rows = [[poly.get(key, F(0)) for poly in basis] for key in forbidden]
    answer = []
    for vector in nullspace(rows, len(basis)):
        answer.append(sparse_add(*[{key: scalar * value for key, value in poly.items()}
                                   for scalar, poly in zip(vector, basis)]))
    return answer


def check_bounded_kernel(H, report, degree, depth, *, homogeneous=False):
    if homogeneous:
        exponents = [(a, degree - a) for a in range(degree + 1)]
    else:
        exponents = [(a, d - a) for d in range(degree + 1) for a in range(d + 1)]
    actual = kernel_on_monomials(H, exponents, depth)
    declared = restrict_space(report["classification"][f"S{depth}"], degree,
                              homogeneous=homogeneous)
    require(same_span(actual, declared),
            f"Independent kernel mismatch: degree {degree}, depth {depth}, homogeneous={homogeneous}")
    return {"degree": degree, "refinement_depth": depth,
            "homogeneous_slice": homogeneous, "dimension": len(actual)}


def fixtures():
    q, p = {(1, 0): F(1)}, {(0, 1): F(1)}
    qm = lambda c: sparse_add(p, {(1, 0): -F(c)})
    prod = lambda *terms: _product(terms)
    return [
        ("sixfold", [6], sparse_power(q, 6), None),
        ("five_one", [5, 1], prod(sparse_power(q, 5), p), None),
        ("four_two", [4, 2], prod(sparse_power(q, 4), sparse_power(p, 2)), (3, 3)),
        ("four_one_one", [4, 1, 1], prod(sparse_power(q, 4),
            sparse_add(sparse_power(p, 2), sparse_power(q, 2))), (3, 2)),
        ("three_three", [3, 3], prod(sparse_power(q, 3), sparse_power(p, 3)), None),
        ("three_two_one", [3, 2, 1], prod(sparse_power(q, 3), sparse_power(p, 2), qm(1)), (2, 2)),
        ("three_one_one_one", [3, 1, 1, 1], prod(sparse_power(q, 3), p, qm(1), qm(2)), (2, 2)),
        ("two_two_two", [2, 2, 2], prod(sparse_power(q, 2), sparse_power(p, 2), sparse_power(qm(1), 2)), (2, 2)),
        ("two_two_one_one", [2, 2, 1, 1], prod(sparse_power(q, 2), sparse_power(p, 2), qm(1), qm(2)), (2, 2)),
        ("two_one_one_one_one", [2, 1, 1, 1, 1], prod(sparse_power(q, 2), p, qm(1), qm(2), qm(3)), (2, 2)),
        ("squarefree_with_infinity", [1, 1, 1, 1, 1, 1], prod(q, p, qm(1), qm(2), qm(3), qm(4)), (2, 2)),
    ]


def _product(polys):
    result = {(0, 0): F(1)}
    for poly in polys:
        result = sparse_product(result, poly)
    return result


def check_pattern(report, pattern, dimensions=None):
    require(report["leading"]["geometric_root_pattern"] == pattern,
            "Wrong geometric root-multiplicity stratum")
    if dimensions is not None:
        require(report["classification"]["S1"]["dimension"] == dimensions[0], "Wrong S1 dimension")
        require(report["classification"]["S2"]["dimension"] == dimensions[1], "Wrong S2 dimension")


def verify():
    classify_sextic = C.classify_sextic

    records = []
    reports = {}
    obstruction_count = 0
    for name, pattern, H, dimensions in fixtures():
        report = check_report(H, classify_sextic(H))
        check_pattern(report, pattern, dimensions)
        reports[name] = report
        checks = [check_bounded_kernel(H, report, 2, 1),
                  check_bounded_kernel(H, report, 2, 2),
                  check_bounded_kernel(H, report, 6, 1, homogeneous=True)]
        records.append({"case": name, "root_pattern": pattern, "bounded_kernels": checks})
        obstruction_count += report.get("obstruction") is not None

    transformations = [(((2, 1), (1, 2)), F(-2, 3)),
                       (((F(1, 2), 2), (1, F(1, 3))), F(5, 7))]
    transformed_count = 0
    for name, pattern, H, dimensions in fixtures():
        for matrix, scalar in transformations:
            transformed = affine_substitute(H, matrix, scalar=scalar)
            report = check_report(transformed, classify_sextic(transformed))
            check_pattern(report, pattern, dimensions)
            for field in ("S1", "S2", "Dinf"):
                original = reports[name]["classification"][field]
                if original["kind"] == "finite_basis":
                    expected = [affine_substitute(G, matrix) for G in space_basis(original)]
                    require(same_span(expected, space_basis(report["classification"][field])),
                            "Finite space failed rational GL2 covariance")
            transformed_count += 1
            obstruction_count += report.get("obstruction") is not None

    zero = check_report({}, classify_sextic({}))
    check_bounded_kernel({}, zero, 2, 2)
    q2p2 = {(2, 0): F(1), (0, 2): F(1)}
    nonsplit_H = sparse_power(q2p2, 3)
    nonsplit = check_report(nonsplit_H, classify_sextic(nonsplit_H), sample_powers=(0, 1, 2, 4, 7))
    check_pattern(nonsplit, [3, 3])
    require(same_span([q2p2], [polynomial(p) for p in nonsplit["classification"]["S1"]["coefficient_generators"]]),
            "Nonsplit quadratic family did not descend over the rationals")
    check_bounded_kernel(nonsplit_H, nonsplit, 6, 1, homogeneous=True)
    infinity_H = {(0, 6): F(1)}
    infinity = check_report(infinity_H, classify_sextic(infinity_H))
    check_pattern(infinity, [6])
    require(infinity["leading"]["infinity_multiplicity"] == 6, "Lost a sixfold root at infinity")

    H0 = {(4, 2): F(1), (6, 0): F(1)}
    M0 = {(4, 2): F(1)}
    inhomogeneous = [
        ("exception_plus_q3", sparse_add(H0, {(3, 0): F(1)}), (3, 2)),
        ("exception_plus_p3", sparse_add(H0, {(0, 3): F(1)}), (2, 2)),
        ("translated_exception", affine_substitute(H0, shift=(1, -2)), (3, 2)),
        ("four_two_plus_q5", sparse_add(M0, {(5, 0): F(1)}), None),
        ("four_two_plus_qp", sparse_add(M0, {(1, 1): F(1)}), (3, 3)),
        ("translated_four_two", affine_substitute(M0, shift=(1, -2)), (3, 3)),
        ("squarefree_lower_terms", {(6, 0): F(1), (0, 6): F(1), (4, 0): F(2),
                                     (0, 3): F(-3), (1, 1): F(5), (0, 0): F(7)}, (2, 2)),
    ]
    for name, pattern, H, dimensions in fixtures():
        if dimensions == (2, 2) and pattern != [1] * 6:
            inhomogeneous.append((name + "_lower_terms", sparse_add(H, {
                (5, 0): F(2), (0, 4): F(-3), (1, 1): F(5), (0, 0): F(7)
            }), (2, 2)))
    inhomogeneous_records = []
    for name, H, dimensions in inhomogeneous:
        report = check_report(H, classify_sextic(H))
        require(report["homogeneous"] is False, "Nonhomogeneous input marked homogeneous")
        if dimensions is not None:
            require((report["classification"]["S1"]["dimension"], report["classification"]["S2"]["dimension"]) == dimensions,
                    f"Wrong refinement dimensions for {name}")
        checks = [check_bounded_kernel(H, report, 2, 1), check_bounded_kernel(H, report, 2, 2)]
        if name == "translated_exception":
            basis = space_basis(report["classification"]["S1"])
            require(any(any(sum(k) == 1 for k in G) and total_degree(G) == 2 for G in basis),
                    "Translated exception lost its nonzero affine correction")
            require(same_span(basis, [{(0, 0): F(1)}, H,
                                     affine_substitute({(1, 1): F(1)}, shift=(1, -2))]),
                    "Translated exceptional lift is incorrect")
        inhomogeneous_records.append({"case": name,
            "S1_dimension": report["classification"]["S1"]["dimension"],
            "S2_dimension": report["classification"]["S2"]["dimension"],
            "bounded_kernels": checks})
        obstruction_count += report.get("obstruction") is not None

    constant_shifts = 0
    unsupported = []
    for name, pattern, H, dimensions in fixtures():
        shifted = sparse_add(H, {(0, 0): F(7, 3)})
        report = check_report(shifted, classify_sextic(shifted))
        check_pattern(report, pattern, dimensions)
        constant_shifts += 1
        obstruction_count += report.get("obstruction") is not None
        if pattern in ([6], [5, 1], [3, 3]):
            changed = sparse_add(H, {(1, 0): F(1), (0, 1): F(1)})
            if pattern in ([6], [5, 1]):
                changed = sparse_add(changed, {(0, 2): F(1)})
            result = classify_sextic(changed)
            require(result.get("status") == "unsupported", "Unsupported inhomogeneous stratum was classified")
            require(all(result.get("classification", {}).get(field) is None
                        for field in ("S1", "S2", "Dinf")),
                    "Unsupported result contains space claims")
            unsupported.append(name)

    sixfold_affine_checks = []
    for degree in range(5):
        H0 = {(6, 0): F(1), (3, 0): F(-2), (degree, 1): F(3, 7)}
        for transformed in (False, True):
            transform = {"matrix": ((0, F(1, 2)), (F(3, 2), 1)),
                         "shift": (F(1, 3), F(-2, 5))} if transformed else {}
            H = affine_substitute(H0, scalar=F(-2, 3), **transform)
            report = check_report(H, classify_sextic(H), sample_powers=(0, 1, 4))
            check_pattern(report, [6])
            require(report["classification"]["method"] == "sixfold_affine_complement",
                    "Missing sixfold affine-complement classification")
            checks = [check_bounded_kernel(H, report, 5, depth) for depth in (1, 2)]
            require(all(check["dimension"] == (15 if degree <= 1 else 11)
                        for check in checks), "Incorrect sixfold kernel dimension")
            square = affine_substitute({(0, 2): F(1)}, **transform)
            gates_through(H, square, 0)
            require(bool(E.defects(H, E.poisson(H, square))) == (degree >= 2),
                    "Incorrect first-iterate obstruction for the quadratic direction")
            sixfold_affine_checks.append({"coefficient_degree": degree,
                                           "rational_affine_change": transformed,
                                           "bounded_kernels": checks})

    further_affine_checks = []
    for H, pattern, method, dimension in (
        ({(5, 1): F(1), (3, 1): F(2), (4, 0): F(-1)}, [5, 1],
         "fivefold_affine_complement", 11),
        (sparse_add(sparse_power({(1, 1): F(1), (0, 1): F(2)}, 3),
                    sparse_power({(1, 1): F(1), (0, 1): F(2)}, 2)), [3, 3],
         "triple_pair_quadratic_composition", 3),
        (sparse_power({(2, 0): F(1), (0, 2): F(1), (1, 0): F(3)}, 3), [3, 3],
         "triple_pair_quadratic_composition", 3),
    ):
        for transformed in (False, True):
            candidate = affine_substitute(H, ((0, F(1, 2)), (F(3, 2), 1)),
                                          shift=(F(1, 3), F(-2, 5)),
                                          scalar=F(-2, 3)) if transformed else H
            report = check_report(candidate, classify_sextic(candidate), sample_powers=(0, 1, 4))
            check_pattern(report, pattern)
            require(report["classification"]["method"] == method, "Wrong inhomogeneous family")
            checks = [check_bounded_kernel(candidate, report, 5, depth) for depth in (1, 2)]
            require(all(check["dimension"] == dimension for check in checks),
                    "Incorrect inhomogeneous kernel dimension")
            further_affine_checks.append({"method": method, "rational_affine_change": transformed,
                                          "bounded_kernels": checks})

    quadratic_sixfold_checks = []
    Q = {(1, 1): F(1), (0, 1): F(2), (3, 0): F(1)}
    for H, first_dimension, core_dimension in (
        (sparse_add(sparse_power(Q, 2), {(0, 0): F(3, 2)}), 3, 3),
        ({(6, 0): F(1), (2, 2): F(1)}, 3, 2),
        ({(6, 0): F(1), (2, 2): F(1), (0, 2): F(1), (4, 1): F(2)}, 3, 2),
        ({(6, 0): F(1), (3, 2): F(1)}, 3, 2),
        ({(6, 0): F(1), (3, 2): F(1), (1, 2): F(1)}, 2, 2),
    ):
        for transformed in (False, True):
            transform = {"matrix": ((0, F(1, 2)), (F(3, 2), 1)),
                         "shift": (F(1, 3), F(-2, 5))} if transformed else {}
            candidate = affine_substitute(H, scalar=F(-2, 3), **transform)
            require(classify_sextic(candidate)["status"] == "unsupported",
                    "Schema 1 changed its quadratic sixfold scope")
            report = check_report(candidate, classify_sextic(candidate, schema=2))
            check_pattern(report, [6], (first_dimension, core_dimension))
            checks = [check_bounded_kernel(candidate, report, 6, depth) for depth in (1, 2)]
            square = affine_substitute({(2, 0): F(1)}, **transform)
            gates_through(candidate, square, 0)
            require(bool(E.defects(candidate, E.poisson(candidate, square))),
                    "Expected a first-iterate quadratic obstruction")
            quadratic_sixfold_checks.append({"first_dimension": first_dimension,
                                             "core_dimension": core_dimension,
                                             "rational_affine_change": transformed,
                                             "bounded_kernels": checks})

    return {
        "schema": "hamiltonian-sextic-core-independent-replay/1",
        "status": "PASS",
        "classified_input_checks": len(records) + transformed_count + 3 + len(inhomogeneous_records) + constant_shifts + len(sixfold_affine_checks) + len(further_affine_checks) + len(quadratic_sixfold_checks),
        "bounded_kernel_checks": sum(len(row["bounded_kernels"]) for row in records + inhomogeneous_records + sixfold_affine_checks + further_affine_checks + quadratic_sixfold_checks) + 2,
        "geometric_strata": records,
        "rational_GL2_and_scalar_checks": transformed_count,
        "zero_ring_check": True,
        "sixfold_infinity_check": True,
        "nonsplit_quadratic_cube_check": True,
        "constant_shift_checks": constant_shifts,
        "inhomogeneous_checks": inhomogeneous_records,
        "sixfold_affine_checks": sixfold_affine_checks,
        "further_affine_checks": further_affine_checks,
        "quadratic_sixfold_checks": quadratic_sixfold_checks,
        "unsupported_inhomogeneous_patterns": unsupported,
        "second_iterate_obstruction_checks": obstruction_count,
        "source_sha256": {
            str(path.relative_to(HERE.parents[2])): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in (HERE.parent / "sextic_core.py", HERE.parent / "independent" / "engine.py",
                         Path(__file__).resolve(), HERE / "test_sextic_core.py")
        },
        "symbolic_family_records": [
            {"H": "q^6", "family": "q^n p^j, n>=0, 0<=j<=2",
             "derivation": "D(q^n p^j)=6j q^(n+5) p^(j-1)",
             "reason": "Every odd contraction of order >=3 needs at least three p derivatives on the partner."},
            {"H": "q^5 p", "family": "q^n p^j, n>=0, 0<=j<=1",
             "derivation": "D(q^n p^j)=(5j-n)q^(n+4)p^j",
             "reason": "The H factor has p degree one; each order>=3 contraction requires at least two p derivatives on the partner."},
            {"H": "(q p)^3", "family": "(q p)^n, n>=0",
             "derivation": "D((q p)^n)=0",
             "reason": "Odd contraction terms cancel in pairs under exchange of q and p; rational quadratic forms descend by covariance."},
            {"H": "0", "family": "Q[q,p]", "derivation": "D=0 and every star defect is zero"},
        ],
        "proof_boundary": {
            "finite_checks": "Direct defining-star expansion, exact span checks, and bounded kernels only.",
            "all_degree_dependencies": "SEXTIC_STRATA_THEOREM.md, inherited monomial/static-tail proofs, and INHOMOGENEOUS_THEOREM.md.",
            "formalization": "This Python replay is not a Lean proof and does not replay the sixteen heavy squarefree certificates.",
        },
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2, sort_keys=True))
