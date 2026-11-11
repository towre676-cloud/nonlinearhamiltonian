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


def _sixfold_affine_complement(H, factors):
    L, M = _sixfold_coordinates(factors)
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


def _infinite_space(pattern, factors):
    if pattern == (6,):
        return _sixfold_space(*_sixfold_coordinates(factors), quadratic=True)
    if pattern == (5, 1):
        L = E.primitive(next(factor for factor, m, degree in factors if m == 5 and degree == 1))
        M = E.primitive(next(factor for factor, m, degree in factors if m == 1 and degree == 1))
        return _family([L], [_ONE, M], "f0(L) + M*f1(L), with arbitrary fi in Q[t]")
    if pattern == (3, 3):
        Q = dict(_ONE)
        for factor, multiplicity, _ in factors:
            if multiplicity != 3:
                raise RuntimeError("Unexpected rational factor in geometric (3,3) stratum")
            Q = E.multiply(Q, factor)
        Q = E.primitive(Q)
        return _family([Q], [_ONE], "f(Q), with arbitrary f in Q[t]; Q is the rational quadratic generator")
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


def classify_sextic(H):
    """Return a JSON-serializable exact classification, or an explicit scope limit.

    Nonzero inputs must have total degree exactly six.  Every homogeneous
    rational sextic (and its constant shifts) is supported.  Nonconstant
    lower terms are supported for the finite-dimensional leading strata
    and for the sixfold family affine in a complementary coordinate.
    Remaining inputs return ``status=unsupported``.
    """
    H = _validate(H)
    if not H:
        space = _family([_Q, _P], [_ONE], "All polynomials in Q[q,p]")
        return {"schema": SCHEMA, "status": "classified", "input": [], "degree": None,
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
    report = {"schema": SCHEMA, "status": "classified", "input": E.serialize(H), "degree": 6,
              "homogeneous": homogeneous, "leading": leading, "obstruction": None,
              "quadratic_lift": None, "proof_boundary": _boundary(method, s.__version__)}
    family = "multiplicity_" + "_".join(map(str, pattern))
    classification = {"family": family, "method": method, "sufficient_refinement_depth": 1}
    report["classification"] = classification

    if pattern in _INFINITE_PATTERNS:
        if not constant_shift:
            if pattern == (6,):
                space = _sixfold_affine_complement(H, factors)
                if space is not None:
                    classification.update({"method": "sixfold_affine_complement",
                                           "S1": space, "S2": space, "Dinf": space})
                    return report
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
