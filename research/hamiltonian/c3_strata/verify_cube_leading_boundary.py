"""Exact replay for CUBE_LEADING_BOUNDARY_THEOREM.md.

Run from this directory:  python verify_cube_leading_boundary.py
Use --require-perfectjet to require the independent cross-check; an installed
PerfectJet or PERFECTJET_SRC=/path/to/PerfectJet/src is supported.
Every comparison is exact (sympy rationals or
fractions.Fraction); a failed assertion aborts the replay.
"""
import argparse
import importlib.util
import json
import os
import random
import sys
from fractions import Fraction

import sympy as S

import cube_leading_boundary as M
from weighted_cubic_form import transvectant

q, P, p, mu, lam, eps = M.q, M.P, M.p, M.mu, M.lam, M.eps
report = {}

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--require-perfectjet", action="store_true")
args = parser.parse_args()
source = os.environ.get("PERFECTJET_SRC")
if source:
    sys.path.insert(0, source)
perfectjet_available = importlib.util.find_spec("perfectjet") is not None
if args.require_perfectjet and not perfectjet_available:
    parser.error("PerfectJet is required: install the pinned engine or set PERFECTJET_SRC")


def to_original(G):
    return S.expand(G.subs(P, p + q**2))


# 1. Transport of the flat transvectants, all ten parameters symbolic ----------
bs = S.symbols("b0:4")
cs = S.symbols("c0:6")
B = sum(bs[i]*q**i for i in range(4))
C = sum(cs[i]*q**i for i in range(6))
H = P**3 + B*P + C
D, T3, T5 = M.chart_operators(B, C)
Hflat = to_original(H)
for i in range(6):
    for k in range(7):
        G = q**i*P**k
        Gflat = to_original(G)
        for order, op in ((1, D), (3, T3), (5, T5)):
            assert S.expand(M.flat_transvectant(Hflat, Gflat, order) - to_original(op(G))) == 0
E = M.gate_symbol(B, C)
beta = bs[3] + cs[5]
u = S.Symbol("u")
for m in range(10):
    assert S.expand(T3(P**m) - 6*E*S.diff(P**m, P, 3)) == 0
    assert S.expand(T5(P**m) - 120*beta*S.diff(P**m, P, 5)) == 0
    g = u**m
    bracket = (beta**3/27 + 2*beta*P + (beta/3)*(bs[2] + 3*bs[3]*q) - E).subs(P, u - beta*q/3)
    predicted = -6*(S.diff(g, u, 3)*bracket + 2*beta*S.diff(g, u, 2))
    actual = T3((P + beta*q/3)**m).subs(P, u - beta*q/3)
    assert S.expand(actual - predicted) == 0
    assert T5((P + beta*q/3)**m) == 0
    top = S.Poly(S.expand(predicted), u, q).coeff_monomial(u**(m - 2)) if m >= 2 else 0
    assert S.expand(top + 6*m*(m - 1)*(2*beta*(m - 1) - bs[3]*(m - 2))) == 0
report["transport"] = "T1,T3,T5 chart operators equal the flat transvectants on q^i P^k, i<=5, k<=6, symbolic b,c"

# 2. Normalisation: depression of the P^2 term is affine in the original chart -
a0, a1, kappa = S.symbols("a0 a1 kappa")
A = a0 + a1*q
general = P**3 + A*P**2 + B*P + C
Y = S.Symbol("Y")
depressed = S.expand(general.subs(P, Y - A/3))
assert S.Poly(depressed, Y).coeff_monomial(Y**2) == 0
assert S.expand(S.Poly(depressed, Y).coeff_monomial(Y) - (B - A**2/3)) == 0
assert S.expand(S.Poly(depressed, Y).coeff_monomial(1) - (C - A*B/3 + 2*A**3/27)) == 0
assert S.degree(B - A**2/3, q) <= 3 and S.degree(C - A*B/3 + 2*A**3/27, q) <= 5
report["normalisation"] = "Y = P + A/3 = p + q^2 + (a0 + a1 q)/3 is p plus an affine function plus q^2"

# 3. Static dimension law on random members (flat engine, original chart) -----
rnd = random.Random(20261113)


def flat_dims(b, c, weight, depths):
    return M.window_dimensions(M.reduced_hamiltonian(b, c), weight, depths)


def symbol_vanishes(b, c):
    return b[3] == 0 and c[5] == 0 and b[1] + c[3] == 0 and 2*b[2] + 4*c[4] == 0


static_cases = []
samples = [
    ((2, -1, 3, 5), (1, 4, -2, 7, 3, -6)),
    ((2, -1, 3, 5), (1, 4, -2, 7, 3, -3)),
    ((0, 0, 0, 10), (0, 0, 0, 0, 0, -3)),
    ((0, 0, 0, 1), (0, 0, 0, 0, 0, -1)),
    ((0, 1, 0, 0), (0, 0, 0, 0, 0, 0)),
    ((0, 0, 1, 0), (0, 0, 0, 0, 0, 0)),
    ((0, 0, 0, 0), (0, 0, 0, 1, 0, 0)),
    ((0, 0, 0, 0), (0, 0, 0, 0, 1, 0)),
    ((0, 0, 0, 0), (0, 0, 0, 0, 0, 1)),
    ((1, 2, 0, 0), (3, 1, 4, 0, 0, 0)),
]
for _ in range(6):
    samples.append((tuple(rnd.randint(-4, 4) for _ in range(4)), tuple(rnd.randint(-4, 4) for _ in range(6))))
for b, c in samples:
    assert not symbol_vanishes(b, c)
    expected = 15 if 3*b[3] + 5*c[5] == 0 else 14
    d12 = flat_dims(b, c, 12, (0,))[0]
    d15 = flat_dims(b, c, 15, (0,))[0]
    assert d12 == d15 == expected, (b, c, d12, d15, expected)
    static_cases.append({"b": b, "c": c, "dim_S0": d12})
report["static_dimension_law"] = static_cases

# 4. First refinement on the locus E = 0 --------------------------------------
refinement_cases = []
for b, c in [((1, 1, 0, 0), (0, 2, 0, -1, 0, 0)), ((0, 0, 2, 0), (0, 0, 0, 0, -1, 0)),
             ((3, 1, 2, 0), (1, 2, 5, -1, -1, 0)), ((0, 0, 0, 0), (0, 0, 1, 0, 0, 0)),
             ((2, 0, 0, 0), (0, 3, 1, 0, 0, 0)), ((0, 3, -4, 0), (0, 0, 0, -3, 2, 0))]:
    assert symbol_vanishes(b, c) and (b[1], b[2], c[2]) != (0, 0, 0)
    d12 = flat_dims(b, c, 12, (0, 1, 2, 3))
    d16 = flat_dims(b, c, 16, (0, 1, 2, 3))
    assert d12[1:] == d16[1:] and d16[0] > d12[0]
    refinement_cases.append({"b": b, "c": c, "window12": d12, "window16": d16})
for b, c in [((0, 0, 0, 0), (0, 1, 0, 0, 0, 0)), ((2, 0, 0, 0), (5, 3, 0, 0, 0, 0))]:
    d12 = flat_dims(b, c, 12, (3,))[0]
    d16 = flat_dims(b, c, 16, (3,))[0]
    assert d16 > d12
    refinement_cases.append({"b": b, "c": c, "excluded_family": True, "S3_window12": d12, "S3_window16": d16})
report["first_refinement"] = refinement_cases

# 5. The coupled family B = mu q, C = eps q + lam q^2 -------------------------
Bc, Cc = mu*q, eps*q + lam*q**2
Hc = P**3 + Bc*P + Cc
Dc, T3c, T5c = M.chart_operators(Bc, Cc)
basis = M.static_basis()
assert len(basis) == 15 and all(T3c(g) == 0 and T5c(g) == 0 for g in basis)
leading = sorted(S.Poly(g, P, q).monoms()[0] for g in basis)
assert len(set(leading)) == 15
report["coupled_static_basis"] = [S.sstr(g) for g in basis]


def obstruction(g, depth):
    cur = g
    for _ in range(depth):
        cur = Dc(cur)
    return S.factor(T3c(cur)), S.factor(T5c(cur))


for g in (S.Integer(1), Hc):
    assert all(obstruction(g, r) == (0, 0) for r in range(5))
assert [obstruction(q, r) for r in range(3)] == [(0, 0), (0, 0), (432*lam, 0)]
assert [obstruction(P, r) for r in range(4)] == [(0, 0), (0, 0), (0, 0), (864*lam**2, 0)]
report["coupled_obstructions"] = {"T3(D^2 q)": "432*lambda", "T3(D^3 P)": "864*lambda**2"}

basis1 = [g.subs(mu, 1) for g in basis]
B1, C1 = q, eps*q + lam*q**2


def pivot_minors(matrix, rank, points, seed):
    """Symbolic maximal minors whose rows and columns are pivots at the given points."""
    local = random.Random(seed)
    found = []
    for point in points:
        order = list(range(matrix.rows))
        local.shuffle(order)
        numeric = matrix.subs(point).extract(order, list(range(matrix.cols)))
        assert numeric.rank() == rank, (point, numeric.rank())
        _, pivots = numeric.T.rref()
        rows = sorted(order[i] for i in pivots[:rank])
        _, columns = matrix.subs(point).extract(rows, list(range(matrix.cols))).rref()
        minor = S.expand(S.numer(S.together(matrix.extract(rows, list(columns)).det(method="bareiss"))))
        assert minor != 0
        found.append(minor)
    return found


def sample_points(symbols, zero_patterns, seed=5, each=3):
    local = random.Random(seed)
    return [{s: (S.Integer(0) if s in zero else S.Rational(local.randint(2, 40), local.randint(1, 9)))
             for s in symbols} for zero in zero_patterns for _ in range(each)]


certificates = {}
for depth, expected_rank in ((1, 11), (2, 12), (3, 13)):
    matrix = M.depth_matrix(B1, C1, basis1, 1, depth)
    assert matrix.rank() == expected_rank
    minors = pivot_minors(matrix, expected_rank, sample_points((lam, eps), [()], seed=depth, each=10), depth)
    common = S.Integer(0)
    for minor in minors:
        common = S.gcd(common, minor)
    content = S.Poly(common, lam, eps)
    assert len(content.monoms()) == 1 and content.monoms()[0][1] == 0, common
    residual = [S.expand(S.cancel(minor/common)) for minor in minors]
    groebner = S.groebner(residual, lam, eps, order="lex")
    zero_set_inside_lambda_zero = any(S.Poly(g, lam, eps).monoms() == [(k, 0)]
                                      for g in groebner.exprs for k in range(0, 40)
                                      if S.Poly(g, lam, eps).is_monomial)
    assert zero_set_inside_lambda_zero, groebner.exprs
    certificates[str(depth)] = {"rank": expected_rank, "kernel": 15 - expected_rank,
                                "common_factor": S.sstr(S.factor(common)),
                                "residual_ideal": [S.sstr(g) for g in groebner.exprs],
                                "minors": [S.sstr(m) for m in minors]}
report["coupled_rank_certificates"] = {k: {x: v[x] for x in ("rank", "kernel", "common_factor", "residual_ideal")}
                                       for k, v in certificates.items()}

# 5b. The stratum deg B <= 1, deg C = 3 -----------------------------------------
gam, b0s, tt = S.symbols("gamma b0 t")
patterns2 = lambda x, y: [(), (x,), (y,), (x, y)]
cubic = {}


def cubic_case(name, Bx, Cx, basis_x, symbols, patterns, saturate=None):
    Dx, T3x, T5x = M.chart_operators(Bx, Cx)
    Hx = P**3 + Bx*P + Cx
    assert len(basis_x) == 15 and all(T3x(g) == 0 and T5x(g) == 0 for g in basis_x)
    assert len({S.Poly(g, P, q).monoms()[0] for g in basis_x}) == 15
    assert {S.Poly(g, P, q).LC() for g in basis_x} == {1}
    for g in (S.Integer(1), q, P, Hx):
        assert (T3x(Dx(g)), T5x(Dx(g))) == (0, 0)
    entry = {"T3(D^2 q)": S.sstr(S.factor(T3x(Dx(Dx(q))))), "T3(D^2 P)": S.sstr(S.factor(T3x(Dx(Dx(P)))))}
    for depth, expected_rank in ((1, 11), (2, 13)):
        matrix = M.depth_matrix(Bx, Cx, basis_x, 1, depth)
        minors = pivot_minors(matrix, expected_rank, sample_points(symbols, patterns), depth)
        gens = minors + ([tt*saturate - 1] if saturate is not None else [])
        variables = ((tt,) if saturate is not None else ()) + tuple(symbols)
        groebner = S.groebner(gens, *variables, order="grevlex")
        assert groebner.exprs == [1], (name, depth, groebner.exprs)
        entry["depth_%d" % depth] = {"rank": expected_rank, "minors": len(minors), "ideal": "unit"}
    cubic[name] = entry


window12 = M.chart_window()
Bg, Cg = q, eps*q + lam*q**2 + gam*q**3
cubic_case("b1=1, c3=gamma, gamma(gamma+1)!=0", Bg, Cg, M.static_window_basis(Bg, Cg, window12),
           (lam, eps, gam), [(), (lam,), (eps,), (lam, eps)], saturate=gam*(gam + 1))
Be, Ce = q, eps*q + lam*q**2 - q**3
cubic_case("b1=1, c3=-1 (E=0)", Be, Ce,
           [P**k for k in range(7)] + M.static_window_basis(Be, Ce, M.chart_window(3, 8, True)),
           (lam, eps), patterns2(lam, eps))
Bz, Cz = b0s + 0*q, eps*q + q**3
cubic_case("b1=0, c3=1, c2=0", Bz, Cz, M.static_window_basis(Bz, Cz, window12), (b0s, eps), patterns2(b0s, eps))
report["cubic_potential_stratum"] = cubic

coupled_points = []
for b1, c1, c2 in ((1, 0, 1), (2, 3, 5), (-3, 1, Fraction(7, 2)), (5, -2, -1)):
    b, c = (0, b1, 0, 0), (0, c1, c2, 0, 0, 0)
    d12 = flat_dims(b, c, 12, (0, 1, 2, 3, 4))
    assert d12 == [15, 4, 3, 2, 2]
    assert flat_dims(b, c, 15, (0, 1))[0:2] == [15, 4]
    coupled_points.append({"mu": str(b1), "epsilon": str(c1), "lambda": str(c2), "dims": d12})
report["coupled_flat_points"] = coupled_points

# 6. Regressions against the core_overlap theorems ----------------------------
assert flat_dims((0, 1, 0, 0), (0, 0, 0, 0, 0, 0), 12, (0, 1, 2, 3, 4)) == [15, 6, 6, 6, 6]
assert flat_dims((0, 1, 0, 0), (0, 1, 0, 0, 0, 0), 12, (0, 1, 2, 3, 4)) == [15, 5, 5, 5, 5]
hr = flat_dims((0, 0, 0, 0), (0, 1, 2, 0, 0, 0), 12, (1, 2, 3, 4))
assert hr == [4, 3, 2, 2] == flat_dims((0, 0, 0, 0), (0, 1, 2, 0, 0, 0), 16, (1, 2, 3, 4))
report["regressions"] = {"cubic_phase_c1_zero": 6, "cubic_phase_c1_nonzero": 5, "higher_restoring": hr}

# 7. Generic point and the survey behind Conjecture F -------------------------
generic = flat_dims((2, -1, 3, 5), (1, 4, -2, 7, 3, -6), 12, (0, 1))
assert generic == [14, 2]
survey = []
for name, b, c in [
    ("b2 only", (0, 0, 1, 0), (0,)*6), ("b3 only", (0, 0, 0, 1), (0,)*6),
    ("c3 only", (0,)*4, (0, 0, 0, 1, 0, 0)), ("c4 only", (0,)*4, (0, 0, 0, 0, 1, 0)),
    ("c5 only", (0,)*4, (0, 0, 0, 0, 0, 1)), ("E=0, b1", (0, 1, 0, 0), (0, 0, 0, -1, 0, 0)),
    ("E=0, b2", (0, 0, 2, 0), (0, 0, 0, 0, -1, 0)), ("B affine, C cubic", (0, 1, 0, 0), (0, 0, 0, 2, 0, 0)),
    ("B quadratic, C affine", (0, 1, 1, 0), (0, 1, 0, 0, 0, 0)), ("B constant, C cubic", (1, 0, 0, 0), (0, 0, 0, 1, 0, 0)),
]:
    dims = flat_dims(b, c, 12, (1, 2, 3, 4))
    assert dims[-1] == 2
    survey.append({"stratum": name, "b": b, "c": c, "S1_to_S4": dims})
report["survey_finite_evidence"] = survey

# 8. Independent PerfectJet transvectants --------------------------------------
if perfectjet_available:
    from perfectjet.polynomial import Poly
    from perfectjet.transvectants import transvectant as pj_transvectant
    h = M.reduced_hamiltonian((2, -1, 3, 5), (1, 4, -2, 7, 3, -6))
    hc = M.reduced_hamiltonian((0, 2, 0, 0), (0, 3, 5, 0, 0, 0))
    count = 0
    for ham in (h, hc):
        pj_h = Poly({k: v for k, v in ham.items()})
        for mon in M.window(12):
            for order in (1, 3, 5):
                ours = {k: v for k, v in transvectant(ham, {mon: Fraction(1)}, order).items() if v}
                theirs = {k: Fraction(v) for k, v in pj_transvectant(pj_h, Poly({mon: 1}), order).terms.items() if v}
                assert ours == theirs
                count += 1
    report["perfectjet"] = "%d transvectant comparisons agree" % count
else:
    report["perfectjet"] = "skipped: PerfectJet is not installed and PERFECTJET_SRC was not usable"

with open("CUBE_LEADING_BOUNDARY_REPLAY.json", "w") as handle:
    json.dump(report, handle, indent=1, default=str)
with open("CUBE_LEADING_BOUNDARY_CERTIFICATE.json", "w") as handle:
    json.dump(certificates, handle, indent=1)
print(json.dumps({k: report[k] for k in ("transport", "coupled_rank_certificates", "coupled_obstructions", "cubic_potential_stratum",
                                         "regressions", "perfectjet")}, indent=1))
print("cube-leading boundary replay: PASS")
