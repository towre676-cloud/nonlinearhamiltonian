"""Exact all-degree core classification for rational sextic Hamiltonians.

``classify_sextic`` accepts the sparse ``{(q_degree, p_degree): Fraction}``
representation used by ``independent.engine``.  It never parses expressions or
approximates roots.  SymPy is imported only when a nonzero input is classified.

Completeness uses the repository's characteristic-zero stratum theorem and its
leading-form extension.  The finite computations below select rational bases
and check witnesses; a finite degree search is not used as a completeness proof.
These are exact computer-assisted mathematical results, not Lean certificates.
"""

from collections.abc import Mapping
from fractions import Fraction
from importlib import util
from math import comb
from pathlib import Path


if __package__:
    from .independent import engine as E
else:
    # Also support the existing directly executed partner_lab.py entry point.
    _spec = util.spec_from_file_location(
        "_sextic_core_sparse_engine", Path(__file__).with_name("independent") / "engine.py"
    )
    E = util.module_from_spec(_spec)
    _spec.loader.exec_module(E)


SCHEMA = "hamiltonian-sextic-core/1"
_ONE = {(0, 0): Fraction(1)}
_Q = {(1, 0): Fraction(1)}
_P = {(0, 1): Fraction(1)}
_INFINITE_PATTERNS = {(6,), (5, 1), (3, 3)}
_QUADRATIC_PATTERNS = {(4, 2), (4, 1, 1)}
_FINITE_TWO_PATTERNS = {
    (3, 2, 1), (3, 1, 1, 1), (2, 2, 2), (2, 2, 1, 1),
    (2, 1, 1, 1, 1), (1, 1, 1, 1, 1, 1),
}
_THEOREM = "research/hamiltonian/c3_strata/SEXTIC_STRATA_THEOREM.md"
_TRIPLE_PAIR = "research/hamiltonian/c3_strata/TRIPLE_PAIR_PERTURBATIONS.md"
_SIXFOLD_CUBIC = "research/hamiltonian/c3_strata/SIXFOLD_CUBIC_COMPLEMENT_THEOREM.md"
_EXTENSION = "research/hamiltonian/c3_strata/INHOMOGENEOUS_THEOREM.md"


def _validate(H):
    if not isinstance(H, Mapping):
        raise TypeError("H must be a mapping from exponent pairs to exact rational coefficients")
    out = {}
    for key, coefficient in H.items():
        if not isinstance(key, tuple) or len(key) != 2:
            raise TypeError("Each monomial key must be a pair (q_degree, p_degree)")
        if any(type(exponent) is not int for exponent in key):
            raise TypeError("Monomial exponents must be integers, not booleans or floats")
        if min(key) < 0:
            raise ValueError("Monomial exponents must be nonnegative")
        if type(coefficient) is not int and not isinstance(coefficient, Fraction):
            raise TypeError("Coefficients must be fractions.Fraction or integers; floats are rejected")
        coefficient = Fraction(coefficient)
        if coefficient:
            out[key] = coefficient
    if out and max(sum(key) for key in out) != 6:
        raise ValueError("Expected zero or a polynomial of total degree exactly six")
    return out


def _fraction(value):
    return Fraction(int(value.p), int(value.q))


def _sympy():
    try:
        import sympy
    except ImportError as error:
        raise ImportError("Sextic classification requires SymPy; install the pinned research requirements") from error
    return sympy


def _factor_leading(H6, s):
    """Factor H6(t,1) over QQ and retain the root at [1:0] explicitly."""
    t = s.Symbol("t")
    polynomial = s.Poly(sum(s.Rational(c.numerator, c.denominator) * t**a
                            for (a, _), c in H6.items()), t, domain=s.QQ)
    scalar, univariate = polynomial.factor_list()
    factors = []
    for factor, multiplicity in univariate:
        degree = int(factor.degree())
        homogeneous = {(int(exponent[0]), degree - int(exponent[0])): _fraction(c)
                       for exponent, c in factor.terms() if c}
        factors.append((homogeneous, int(multiplicity), degree))
    infinity = 6 - int(polynomial.degree())
    if infinity:
        factors.append((dict(_P), infinity, 1))
    factors.sort(key=lambda row: (
        row[1], row[2], tuple((a, b, c.numerator, c.denominator)
                             for (a, b), c in sorted(row[0].items()))))
    rebuilt = E.scale(_ONE, _fraction(scalar))
    for factor, multiplicity, _ in factors:
        rebuilt = E.multiply(rebuilt, E.power(factor, multiplicity))
    if rebuilt != H6:
        raise RuntimeError("Exact homogeneous factorization failed reconstruction")
    pattern = tuple(sorted((m for _, m, degree in factors for _ in range(degree)), reverse=True))
    if sum(pattern) != 6:
        raise RuntimeError("Geometric multiplicities do not sum to six")
    report = {
        "terms": E.serialize(H6),
        "geometric_root_pattern": list(pattern),
        "dehomogenization": "H6(t,1)",
        "infinity_point": "[1:0]",
        "infinity_multiplicity": infinity,
        "factorization": {
            "coefficient": str(_fraction(scalar)),
            "factors": [{"terms": E.serialize(factor), "multiplicity": m,
                         "geometric_degree": degree} for factor, m, degree in factors],
        },
    }
    return pattern, factors, report


class _Operators:
    def __init__(self, H):
        self.H = H
        self.derivatives = {
            k: [(Fraction((-1)**j * comb(k, j)), E.derivative(H, q=k-j, p=j))
                for j in range(k + 1)] for k in (3, 5)
        }

    def D(self, G):
        return E.poisson(self.H, G)

    def T(self, G, k):
        return E.add(*(E.scale(E.multiply(derivative, E.derivative(G, q=j, p=k-j)), coefficient)
                       for j, (coefficient, derivative) in enumerate(self.derivatives[k])))

    def first_image(self, G):
        DG = self.D(G)
        return {(k, a, b): coefficient for k in (3, 5)
                for (a, b), coefficient in self.T(DG, k).items()}

    def gates_zero(self, G, depth):
        for _ in range(depth + 1):
            if self.T(G, 3) or self.T(G, 5):
                return False
            G = self.D(G)
        return True


def _quadratic_survivor(H6):
    operators = _Operators(H6)
    monomials = [E.monomial(a, 2-a) for a in range(3)]
    images = [operators.first_image(G) for G in monomials]
    keys = sorted(set().union(*(set(image) for image in images)))
    matrix = [[image.get(key, Fraction(0)) for image in images] for key in keys]
    vectors = E.nullspace(matrix, 3)
    if len(vectors) != 1:
        raise RuntimeError("The finite quadratic stratum must have exactly one leading survivor")
    G = E.primitive(E.add(*(E.scale(monomial, coefficient)
                            for monomial, coefficient in zip(monomials, vectors[0]))))
    if not operators.gates_zero(G, 1):
        raise RuntimeError("Leading quadratic survivor failed its exact gates")
    return G


def _lift_quadratic(H, J2, s):
    """Solve all coefficients of both gates for J2 + alpha*q + beta*p."""
    operators = _Operators(H)
    images = [operators.first_image(G) for G in (J2, _Q, _P)]
    keys = sorted(set().union(*(set(image) for image in images)))
    rational = lambda c: s.Rational(c.numerator, c.denominator)
    A = s.Matrix([[rational(images[i].get(key, Fraction(0))) for i in (1, 2)] for key in keys])
    rhs = s.Matrix([-rational(images[0].get(key, Fraction(0))) for key in keys])
    augmented = A.row_join(rhs)
    reduced, pivots = augmented.rref()
    rank = int(A.rank())
    if rank != 2:
        raise RuntimeError("Finite leading stratum unexpectedly permits a linear survivor")

    def rows(indices):
        return [{"gate": keys[i][0], "q": keys[i][1], "p": keys[i][2],
                 "coefficients": [str(_fraction(A[i, j])) for j in range(2)],
                 "rhs": str(_fraction(rhs[i, 0]))} for i in indices]

    report = {"leading_candidate": E.serialize(J2),
              "system": {"unknowns": ["alpha", "beta"], "row_count": len(keys),
                         "rank": rank, "augmented_rank": len(pivots)}}
    if 2 in pivots:
        indices = list(augmented.T.rref()[1])
        determinant = augmented[indices, :].det()
        report.update({"status": "absent", "inconsistency_certificate": {
            "rows": rows(indices), "determinant": str(_fraction(determinant))}})
        return None, report
    alpha, beta = (_fraction(reduced[i, 2]) for i in range(2))
    correction = E.add(E.scale(_Q, alpha), E.scale(_P, beta))
    G = E.add(J2, correction)
    if not operators.gates_zero(G, 1):
        raise RuntimeError("The reconstructed affine quadratic failed its exact gates")
    indices = list(A.T.rref()[1])
    report.update({"status": "present", "linear_correction": E.serialize(correction),
                   "coefficients": {"alpha": str(alpha), "beta": str(beta)},
                   "uniqueness_certificate": {"rows": rows(indices),
                       "determinant": str(_fraction(A[indices, :].det()))}})
    return G, report


def _finite(basis):
    return {"kind": "finite_basis", "dimension": len(basis),
            "basis": [E.serialize(G) for G in basis]}


def _family(generators, module_basis, description):
    return {"kind": "polynomial_family", "dimension": None,
            "coefficient_generators": [E.serialize(G) for G in generators],
            "module_basis": [E.serialize(G) for G in module_basis],
            "description": description}


def _sixfold_coordinates(factors):
    L = E.primitive(factors[0][0])
    M = dict(_Q if L.get((0, 1), 0) else _P)
    return L, M


def _sixfold_space(L, M, *, quadratic):
    if quadratic:
        return _family([L], [_ONE, M, E.power(M, 2)],
                       "f0(L) + M*f1(L) + M^2*f2(L), with arbitrary fi in Q[t]")
    return _family([L], [_ONE, M], "f0(L) + M*f1(L), with arbitrary fi in Q[t]")


def _affine_complement(H, L, M):
    a, b = L.get((1, 0), 0), L.get((0, 1), 0)
    # The directional derivative along (-b, a) annihilates L and is
    # a nonzero constant multiple of differentiation in M at fixed L.
    def transverse_derivative(G):
        return E.add(E.scale(E.derivative(G, q=1), -b),
                     E.scale(E.derivative(G, p=1), a))

    coefficient = transverse_derivative(H)
    if transverse_derivative(coefficient):
        return None
    degree = max(map(sum, coefficient), default=-1)
    return _sixfold_space(L, M, quadratic=degree <= 1)


def _quadratic_sixfold_candidate(H, factors, s):
    L, M = _sixfold_coordinates(factors)
    a, b = L.get((1, 0), 0), L.get((0, 1), 0)
    c, d = M.get((1, 0), 0), M.get((0, 1), 0)
    determinant = a*d - b*c
    x, y = s.symbols("x y")
    q, p = (d*x - b*y) / determinant, (a*y - c*x) / determinant
    transformed = s.Poly(sum(coef*q**i*p**j for (i, j), coef in H.items()), y, x, domain=s.QQ)
    if transformed.degree(y) != 2:
        return None
    coefficients = transformed.as_dict()
    quadratic = s.Poly.from_dict({(i,): coef for (j, i), coef in coefficients.items() if j == 2}, x)
    linear = s.Poly.from_dict({(i,): coef for (j, i), coef in coefficients.items() if j == 1}, x)
    degree = quadratic.degree()
    if degree not in (2, 3) or linear.degree() > 4:
        return None
    u = s.Poly(x + quadratic.nth(degree - 1) / (degree * quadratic.nth(degree)), x)
    quotient = (linear.diff()*u - (degree - 1)*linear).quo(2*quadratic)
    v = quotient.integrate()

    def substitute_univariate(poly):
        return E.add(*(E.scale(E.power(L, i), _fraction(coef))
                       for (i,), coef in poly.terms() if coef))

    candidate = E.add(E.multiply(substitute_univariate(u), M), substitute_univariate(v))
    return degree, candidate


def _pure_linear_power(Hd, degree, s):
    """Return (primitive rational linear form, scalar) for Hd = scalar*L^degree."""
    if not Hd or any(sum(key) != degree for key in Hd):
        return None
    t = s.Symbol("t")
    polynomial = s.Poly(sum(s.Rational(coef.numerator, coef.denominator) * t**a
                            for (a, _), coef in Hd.items()), t, domain=s.QQ)
    infinity = degree - int(polynomial.degree())
    if infinity == degree:
        L = dict(_P)
    elif infinity == 0:
        _, factors = polynomial.factor_list()
        if len(factors) != 1:
            return None
        factor, multiplicity = factors[0]
        if int(multiplicity) != degree or int(factor.degree()) != 1:
            return None
        leading, constant = factor.all_coeffs()
        L = E.primitive({(1, 0): _fraction(leading), (0, 1): _fraction(constant)})
    else:
        return None
    power = E.power(L, degree)
    key = next((key for key, value in power.items() if value), None)
    if key is None or key not in Hd:
        return None
    scalar = Hd[key] / power[key]
    return (L, scalar) if E.scale(power, scalar) == Hd else None


def _sixfold_cubic_complement(H, factors, s, report):
    """All-degree theorem for a*L^6 + b*M^3 + c with independent L,M."""
    if any(sum(key) not in (0, 3, 6) for key in H):
        return None
    H3 = {key: coefficient for key, coefficient in H.items() if sum(key) == 3}
    cubic = _pure_linear_power(H3, 3, s)
    if cubic is None:
        return None
    M, cubic_scalar = cubic
    L = E.primitive(factors[0][0])
    determinant = (L.get((1, 0), 0) * M.get((0, 1), 0)
                   - L.get((0, 1), 0) * M.get((1, 0), 0))
    if not determinant:
        return None

    S1 = [dict(_ONE), L, E.power(L, 2), H]
    core = [dict(_ONE), H]
    operators = _Operators(H)
    _verify_finite_spaces(H, S1, core)
    D2L = operators.D(operators.D(L))
    T3, T5 = operators.T(D2L, 3), operators.T(D2L, 5)
    if not (T3 or T5):
        raise RuntimeError("Sixfold cubic-complement linear witness must fail at refinement two")

    report["obstruction"] = {
        "G": E.serialize(L), "iterate": 2, "D2G": E.serialize(D2L),
        "T3": E.serialize(T3), "T5": E.serialize(T5),
    }
    report["sixfold_cubic_complement"] = {
        "L": E.serialize(L), "M": E.serialize(M),
        "determinant": str(determinant), "cubic_scalar": str(cubic_scalar),
    }
    report["proof_boundary"]["dependencies"].append(_SIXFOLD_CUBIC)
    report["proof_boundary"]["completeness"] = (
        "SIXFOLD_CUBIC_COMPLEMENT_THEOREM.md reduces every polynomial static partner "
        "to an explicit 15-dimensional space and eliminates its noncore directions "
        "by exact first- and second-refinement coefficient identities.")
    report["classification"].update({
        "method": "sixfold_cubic_complement",
        "sufficient_refinement_depth": 2,
        "S1": _finite(S1), "S2": _finite(core), "Dinf": _finite(core),
    })
    return report


def _triple_pair_generator(factors):
    Q = dict(_ONE)
    for factor, multiplicity, _ in factors:
        if multiplicity != 3:
            raise RuntimeError("Unexpected rational factor in geometric (3,3) stratum")
        Q = E.multiply(Q, factor)
    return E.primitive(Q)


def _triple_pair_center(H, H6, factors, s):
    Q = _triple_pair_generator(factors)
    q, p = s.symbols("q p")

    def polynomial(G):
        return s.Poly.from_dict(G, (q, p), domain=s.QQ)

    Q2 = E.power(Q, 2)
    Q3 = E.multiply(Q2, Q)
    monomial = next(iter(Q3))
    a = H6[monomial] / Q3[monomial]
    H5 = {key: coefficient for key, coefficient in H.items() if sum(key) == 5}
    linear, remainder = polynomial(H5).div(polynomial(E.scale(Q2, 3*a)))
    if not remainder.is_zero:
        return None
    J = E.add(Q, {key: _fraction(value) for key, value in linear.terms() if value})
    return J, a


def _triple_pair_residual(H, J, a):
    residual = E.add(H, E.scale(E.power(J, 3), -a))
    for exponent in (2, 1):
        power = E.power(J, exponent)
        key = max(power, key=lambda key: (sum(key), key))
        coefficient = residual.get(key, 0) / power[key]
        residual = E.add(residual, E.scale(power, -coefficient))
    return residual


def _quadratic_composition(centered, residual):
    if centered is None or any(sum(key) for key in residual):
        return None
    J, _ = centered
    return _family([J], [_ONE], "f(J), with arbitrary f in Q[t]; J is the rational quadratic generator")


def _infinite_space(pattern, factors):
    if pattern == (6,):
        return _sixfold_space(*_sixfold_coordinates(factors), quadratic=True)
    if pattern == (5, 1):
        L = E.primitive(next(factor for factor, m, degree in factors if m == 5 and degree == 1))
        M = E.primitive(next(factor for factor, m, degree in factors if m == 1 and degree == 1))
        return _family([L], [_ONE, M], "f0(L) + M*f1(L), with arbitrary fi in Q[t]")
    if pattern == (3, 3):
        return _family([_triple_pair_generator(factors)], [_ONE], "f(Q), with arbitrary f in Q[t]; Q is the rational quadratic generator")
    raise RuntimeError("Unknown infinite-family stratum")


def _span_contains(basis, G):
    keys = sorted(set(G).union(*(set(B) for B in basis)))
    columns = basis + [G]
    matrix = [[column.get(key, Fraction(0)) for column in columns] for key in keys]
    return any(vector[-1] for vector in E.nullspace(matrix, len(columns)))


def _verify_finite_spaces(H, S1, core):
    operators = _Operators(H)
    if not all(operators.gates_zero(G, 1) for G in S1):
        raise RuntimeError("A reported S1 basis vector failed its exact gates")
    if not all(operators.gates_zero(G, 2) for G in core):
        raise RuntimeError("A reported core basis vector failed its second-refinement gates")
    if not all(_span_contains(core, operators.D(G)) for G in core):
        raise RuntimeError("The reported finite core is not invariant under the exact Poisson action")


def _quadratic_sixfold_report(H, degree, G, report):
    S1 = core = [dict(_ONE), H]
    operators = _Operators(H)
    if not operators.gates_zero(G, 0):
        raise RuntimeError("The proposed sixfold lift failed its static gates")
    first = operators.D(G)
    T3, T5 = operators.T(first, 3), operators.T(first, 5)
    if T3 or T5:
        if degree == 2:
            raise RuntimeError("A weight-six lift must pass the first refinement")
        report["first_refinement_obstruction"] = {
            "G": E.serialize(G), "iterate": 1, "DG": E.serialize(first),
            "T3": E.serialize(T3), "T5": E.serialize(T5),
        }
    else:
        S1 = core = [dict(_ONE), G, H]
        second = operators.D(first)
        T3, T5 = operators.T(second, 3), operators.T(second, 5)
        if T3 or T5:
            core = [dict(_ONE), H]
            report["obstruction"] = {"G": E.serialize(G), "iterate": 2,
                                     "D2G": E.serialize(second),
                                     "T3": E.serialize(T3), "T5": E.serialize(T5)}
    _verify_finite_spaces(H, S1, core)
    report["classification"].update({
        "method": "sixfold_quadratic_complement",
        "sufficient_refinement_depth": 2 if report["obstruction"] else 1,
        "S1": _finite(S1), "S2": _finite(core), "Dinf": _finite(core),
    })
    return report



def _triple_pair_perturbation(H, factors, centered, residual, report):
    core = [dict(_ONE), H]
    J = centered[0] if centered is not None else _triple_pair_generator(factors)
    operators = _Operators(H)
    first = operators.D(J)
    T3, T5 = operators.T(first, 3), operators.T(first, 5)
    first_survives = centered is not None and all(sum(key) <= 2 for key in residual)
    if first_survives == bool(T3 or T5):
        raise RuntimeError("Triple-pair quadratic scope test disagrees with the exact gates")
    if not first_survives:
        S1 = core
        report["first_refinement_obstruction"] = {
            "G": E.serialize(J), "iterate": 1, "DG": E.serialize(first),
            "T3": E.serialize(T3), "T5": E.serialize(T5),
        }
    else:
        S1 = [dict(_ONE), J, H]
        second = operators.D(first)
        T3, T5 = operators.T(second, 3), operators.T(second, 5)
        if not (T3 or T5):
            raise RuntimeError("A non-composition triple-pair lift must fail the second refinement")
        report["obstruction"] = {
            "G": E.serialize(J), "iterate": 2, "D2G": E.serialize(second),
            "T3": E.serialize(T3), "T5": E.serialize(T5),
        }
    _verify_finite_spaces(H, S1, core)
    report["proof_boundary"]["dependencies"].append(_TRIPLE_PAIR)
    report["classification"].update({
        "method": "triple_pair_perturbation",
        "sufficient_refinement_depth": 2 if report["obstruction"] else 1,
        "S1": _finite(S1), "S2": _finite(core), "Dinf": _finite(core),
    })
    return report


def _boundary(method, sympy_version=None):
    dependencies = [_THEOREM]
    if method == "leading_form":
        dependencies.append(_EXTENSION)
    return {
        "formalized": False,
        "arithmetic": "exact rational arithmetic; no approximate roots or numerical rank tests",
        "sympy_version": sympy_version,
        "dependencies": dependencies,
        "completeness": "Uses the stated all-degree theorems, covariance and rational descent; finite per-input gates alone do not prove completeness",
        "definitions": "S^r imposes T3(H,D^i G)=T5(H,D^i G)=0 for 0<=i<=r; D=T1(H,.)",
    }


def classify_sextic(H, *, schema=1):
    """Return a JSON-serializable exact classification, or an explicit scope limit.

    Nonzero inputs must have total degree exactly six.  Every homogeneous
    rational sextic (and its constant shifts) is supported.  Nonconstant
    lower terms are supported for the finite-dimensional leading strata
    and for the affine-complement and quadratic-composition subfamilies.
    Schema 2 additionally supports all triple-pair perturbations and
    quadratic sixfold families of weights six and seven.
    Remaining inputs return ``status=unsupported``.
    """
    if type(schema) is not int or schema not in (1, 2):
        raise ValueError("Sextic core schema must be 1 or 2")
    schema_id = SCHEMA if schema == 1 else "hamiltonian-sextic-core/2"
    H = _validate(H)
    if not H:
        space = _family([_Q, _P], [_ONE], "All polynomials in Q[q,p]")
        return {"schema": schema_id, "status": "classified", "input": [], "degree": None,
                "homogeneous": True,
                "leading": {"terms": [], "geometric_root_pattern": [], "dehomogenization": "H6(t,1)",
                            "infinity_point": "[1:0]", "infinity_multiplicity": 0,
                            "factorization": {"coefficient": "0", "factors": []}},
                "classification": {"family": "zero", "method": "zero", "sufficient_refinement_depth": 0,
                                   "S1": space, "S2": space, "Dinf": space},
                "obstruction": None, "quadratic_lift": None, "proof_boundary": _boundary("zero")}

    s = _sympy()
    H6 = {key: coefficient for key, coefficient in H.items() if sum(key) == 6}
    homogeneous = H == H6
    constant_shift = all(sum(key) in (0, 6) for key in H)
    method = "homogeneous" if homogeneous else "constant_shift" if constant_shift else "leading_form"
    pattern, factors, leading = _factor_leading(H6, s)
    report = {"schema": schema_id, "status": "classified", "input": E.serialize(H), "degree": 6,
              "homogeneous": homogeneous, "leading": leading, "obstruction": None,
              "quadratic_lift": None, "proof_boundary": _boundary(method, s.__version__)}
    family = "multiplicity_" + "_".join(map(str, pattern))
    classification = {"family": family, "method": method, "sufficient_refinement_depth": 1}
    report["classification"] = classification

    if pattern in _INFINITE_PATTERNS:
        if not constant_shift:
            if pattern == (6,):
                cubic_report = _sixfold_cubic_complement(H, factors, s, report)
                if cubic_report is not None:
                    return cubic_report
                method = "sixfold_affine_complement"
                space = _affine_complement(H, *_sixfold_coordinates(factors))
            elif pattern == (5, 1):
                method = "fivefold_affine_complement"
                L = E.primitive(next(factor for factor, m, _ in factors if m == 5))
                M = E.primitive(next(factor for factor, m, _ in factors if m == 1))
                space = _affine_complement(H, L, M)
            else:
                method = "triple_pair_quadratic_composition"
                centered = _triple_pair_center(H, H6, factors, s)
                residual = _triple_pair_residual(H, *centered) if centered is not None else None
                space = _quadratic_composition(centered, residual)
            if space is not None:
                classification.update({"method": method, "S1": space, "S2": space, "Dinf": space})
                return report
            if pattern == (3, 3) and schema == 2:
                return _triple_pair_perturbation(H, factors, centered, residual, report)
            if pattern == (6,) and schema == 2:
                candidate = _quadratic_sixfold_candidate(H, factors, s)
                if candidate is not None:
                    degree, G = candidate
                    return _quadratic_sixfold_report(H, degree, G, report)
            report["status"] = "unsupported"
            report["unsupported_reason"] = (
                "Nonconstant lower-degree terms with this infinite-dimensional leading S1 are outside "
                "the proved inhomogeneous families; no all-degree S1 or core is asserted")
            classification.update({"sufficient_refinement_depth": None, "S1": None, "S2": None, "Dinf": None})
            return report
        space = _infinite_space(pattern, factors)
        classification.update({"S1": space, "S2": space, "Dinf": space})
        return report

    base = [dict(_ONE), H]
    if pattern in _FINITE_TWO_PATTERNS:
        S1 = core = base
    elif pattern in _QUADRATIC_PATTERNS:
        J2 = _quadratic_survivor(H6)
        if constant_shift:
            G = J2
            report["quadratic_lift"] = {"status": "present", "leading_candidate": E.serialize(J2),
                                        "linear_correction": [], "coefficients": {"alpha": "0", "beta": "0"}}
        else:
            G, report["quadratic_lift"] = _lift_quadratic(H, J2, s)
        if G is None:
            S1 = core = base
        else:
            S1 = [dict(_ONE), G, H]
            operators = _Operators(H)
            D2G = operators.D(operators.D(G))
            T3, T5 = operators.T(D2G, 3), operators.T(D2G, 5)
            if T3 or T5:
                core = base
                classification["sufficient_refinement_depth"] = 2
                report["obstruction"] = {"G": E.serialize(G), "iterate": 2,
                                          "D2G": E.serialize(D2G), "T3": E.serialize(T3), "T5": E.serialize(T5)}
            else:
                if pattern == (4, 1, 1):
                    raise RuntimeError("The exceptional leading stratum must have a nonzero second obstruction")
                core = S1
    else:
        raise RuntimeError("Geometric sextic multiplicity pattern is outside the eleven partitions")

    _verify_finite_spaces(H, S1, core)
    classification.update({"S1": _finite(S1), "S2": _finite(core), "Dinf": _finite(core)})
    report["proof_boundary"]["per_input_checks"] = [
        "Exact rational factor reconstruction including the root at infinity",
        "Both gates vanish on every S1 basis vector through iterate one",
        "Both gates vanish on every core basis vector through iterate two",
        "The reported core is invariant under the full, unprojected Poisson action",
    ]
    return report


# ---------------------------------------------------------------------------
# Schema-2 compatibility layer reconciled from the nonlinear proof platform.
# This layer wraps the current schema-1 classifier; it does not replace the
# newer triple-pair core implementation above.
SCHEMA_V2 = "hamiltonian-sextic-core/2"
_QUADRATIC_SIXFOLD = "research/hamiltonian/c3_strata/QUADRATIC_SIXFOLD_THEOREM.md"
_SEPARABLE_SIXFOLD = "research/hamiltonian/c3_strata/SEPARABLE_SIXFOLD_THEOREM.md"
_WEIGHTED_SEPARABLE = "research/hamiltonian/c3_strata/WEIGHTED_SEPARABLE_THEOREM.md"


def _quadratic_sixfold_module():
    spec = util.spec_from_file_location(
        "_sextic_core_quadratic_sixfold", Path(__file__).with_name("quadratic_sixfold.py"))
    module = util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _separable_sixfold_module():
    spec = util.spec_from_file_location(
        "_sextic_core_separable", Path(__file__).with_name("separable_sixfold.py"))
    module = util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _weighted_separable_module():
    spec = util.spec_from_file_location(
        "_sextic_core_weighted", Path(__file__).with_name("weighted_separable.py"))
    module = util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _unknown_stage(index, reason):
    return {"index": index, "status": "unknown", "space": None, "reason": reason}


def _stage(index, space):
    return {"index": index, "status": "classified", "space": space}


def _v2_space(space, L):
    module, finite = space["module_over_K[L]"], space["finite_span"]
    if not module:
        return {"kind": "finite_basis", "dimension": len(finite), "basis": finite}
    answer = {"kind": "polynomial_family" if not finite else "module_plus_finite",
              "dimension": None, "coefficient_generators": [L], "module_basis": module,
              "description": "sum of fi(L)*module_basis[i] with arbitrary fi in Q[t]"}
    if finite:
        answer["finite_span"] = finite
        answer["description"] += ", plus the rational span of finite_span"
    return answer


def classify_sextic_v2(H):
    """Schema-2 classification layered on the reconciled schema-1 classifier."""
    first = classify_sextic(H)
    report = {key: first[key] for key in ("status", "input", "degree", "homogeneous", "leading")}
    report["schema"] = SCHEMA_V2
    report["proof_boundary"] = dict(first["proof_boundary"])
    old = first["classification"]
    if first["status"] == "classified":
        depth = old["sufficient_refinement_depth"]
        report["classification"] = {
            "family": old["family"], "method": old["method"],
            "derived_from": SCHEMA,
            "depth": {"value": depth, "kind": "sufficient"},
            "stages": [_unknown_stage(0, "S0 is not asserted by the schema-1 theorems"),
                       _stage(1, old["S1"]), _stage(2, old["S2"])],
            "Dinf": old["Dinf"],
            "sharpness_witness": None,
            "obstruction": first["obstruction"],
            "quadratic_lift": first["quadratic_lift"],
        }
        return report

    second = _quadratic_sixfold_module().classify_quadratic_sixfold(_validate(H))
    if second["status"] != "classified":
        third = _separable_sixfold_module().classify_separable_sixfold(_validate(H))
        if third["status"] == "classified":
            report["status"] = "classified"
            report["classification"] = third["classification"]
            boundary = report["proof_boundary"]
            boundary["dependencies"] = [_SEPARABLE_SIXFOLD]
            for key in ("completeness", "per_input_checks"):
                boundary[key] = third["proof_boundary"][key]
            return report
        fourth = _weighted_separable_module().classify_weighted_separable_sixfold(_validate(H))
        if fourth["status"] == "classified":
            report["status"] = "classified"
            report["classification"] = fourth["classification"]
            boundary = report["proof_boundary"]
            boundary["dependencies"] = [_SEPARABLE_SIXFOLD, _WEIGHTED_SEPARABLE]
            for key in ("completeness", "per_input_checks"):
                boundary[key] = fourth["proof_boundary"][key]
            return report
        report["unsupported_reason"] = first["unsupported_reason"]
        report["classification"] = {"family": old["family"], "method": old["method"],
                                    "derived_from": SCHEMA, "depth": None, "stages": None,
                                    "Dinf": None, "sharpness_witness": None,
                                    "obstruction": None, "quadratic_lift": None}
        return report

    L = second["L"]
    stages = []
    for index in range(second["least_depth"] + 1):
        space = second["stages"].get(f"S{index}")
        stages.append(_unknown_stage(index, "S0 is not classified for a nonconstant "
                                            "coefficient of the squared complement")
                      if space is None else _stage(index, _v2_space(space, L)))
    report["status"] = "classified"
    report["classification"] = {
        "family": old["family"], "method": "sixfold_quadratic_complement",
        "derived_from": second["schema"],
        "regime": second["regime"],
        "coordinates": {"L": L, "M": second["M"]},
        "depth": {"value": second["least_depth"], "kind": "least"},
        "stages": stages,
        "Dinf": _v2_space(second["Dinf"], L),
        "sharpness_witness": second["sharpness_witness"],
        "square_first_integral": second.get("square_first_integral"),
        "obstruction": None, "quadratic_lift": None,
    }
    boundary = report["proof_boundary"]
    boundary["dependencies"] = list(boundary["dependencies"]) + [_QUADRATIC_SIXFOLD]
    boundary["completeness"] = (
        "Theorems A-E of QUADRATIC_SIXFOLD_THEOREM.md. For a nonconstant top coefficient the "
        "stages are exact kernels inside the weighted box that Theorem D proves contains S1, "
        "and the core dimension is cross-checked against the closed criterion of Theorem E")
    boundary["per_input_checks"] = [
        "The sharpness witness passes both gates through iterate depth-1 and fails at iterate depth",
        "For a nonconstant top coefficient: stable stage invariant under the Poisson action, "
        "box computation equal to the Theorem E prediction",
    ]
    return report
