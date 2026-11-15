"""Exact replay for SIXFOLD_GLOBAL_DEPTH_THEOREM.md.

    python verify_sixfold_global_depth.py [--perfectjet]

Sections 1-4 replay the symbolic identities and stored minors on which the new
proof steps rest (universal in the parameters).  Section 5 is an adversarial
exact sweep: for a deterministic sample of members of the 21-parameter family
it compares the classifier with the chain of S^r on the degree-12 window and
looks for any drop after depth six.  The sweep is a cross-check and a
counterexample search, not a proof step.  With --perfectjet a subsample is
recomputed with PerfectJet's transvectants (cross-check only).  With --extended
the sweep runs on a larger deterministic sample and writes its own receipt
without touching the standard replay file.
"""
import itertools
import json
import os
import random
import sys
from fractions import Fraction as Fr

import sympy as S
from sympy.polys.matrices import DomainMatrix

import cube_leading_boundary as M
import sixfold_global_depth as G

q, p, P = M.q, M.p, M.P
T = M.flat_transvectant
report = {}


def gates(H, obs, depth):
    cur = obs
    for _ in range(depth):
        cur = T(H, cur, 1)
    return S.expand(T(H, cur, 3)), S.expand(T(H, cur, 5))


def quotient(num, den):
    quo, _ = S.div(S.expand(num), den, q)
    return S.integrate(S.expand(quo), q)


# 1. Regression anchor retained from PR #39 -----------------------------------
H = q**6 + q*p**2
anchor = p**2 + S.Rational(12, 5)*q**5
assert gates(H, anchor, 0) == (0, 0) and gates(H, anchor, 1) == (0, 0)
assert S.expand(T(H, anchor, 1) - (2*p**3 - 12*q**5*p)) == 0
assert gates(H, anchor, 2)[0] == 51840*p*q**3
report["anchor"] = "p^2 + 12/5 q^5 lies in S^1 \\ S^2 of q^6 + q p^2; T3(H, D^2 G) = 51840 p q^3"

# 2. The depth-six locus:  H = c0 (p + beta)^2 + F,  deg beta = deg F = 3 -------
c0 = S.Symbol("c0")
be = S.symbols("beta0:4")
Fs = S.symbols("F0:4")
beta = sum(be[i]*q**i for i in range(4))
H = S.expand(c0*(p + beta)**2 + sum(Fs[i]*q**i for i in range(4)))
for depth in range(6):
    assert gates(H, q, depth) == (0, 0)
for depth in range(5):
    assert gates(H, p + beta, depth) == (0, 0)
t3, t5 = gates(H, q, 6)
assert t5 == 0 and S.expand(t3 + 69120*Fs[3]**2*c0**5*(be[2] + 3*be[3]*q)) == 0
t3, t5 = gates(H, p + beta, 5)
assert t5 == 0 and S.expand(t3 - 34560*Fs[3]**2*c0**4*(be[2] + 3*be[3]*q)) == 0
report["depth_six_obstructions"] = {"T3(H, D^6 q)": "-69120*F3^2*c0^5*(beta2 + 3*beta3*q)",
                                    "T3(H, D^5 P)": "34560*F3^2*c0^4*(beta2 + 3*beta3*q)"}

# 3. Nonconstant quadratic coefficient, arbitrary A of degree <= 4 -------------
a = S.symbols("a0:5")
f = S.symbols("f0:7")
s, dl, c1, c2, c3 = S.symbols("s delta c1 c2 c3")
A = sum(a[i]*q**i for i in range(5))
fq = sum(f[i]*q**i for i in range(7))
x = q - s
phi = S.Function("phi")(q)
nonconstant = {}
# k = 1
B = c1*x
H = fq + A*p + B*p**2
G1 = p + quotient(S.diff(A, q), 2*B)
G2 = q*p + quotient(q*S.diff(A, q), 2*B)
for obs in (q, G1, G2):
    assert gates(H, obs, 0) == (0, 0) and gates(H, obs, 1) == (0, 0)
t3, t5 = gates(H, p**2 + phi, 1)
assert t5 == 0 and S.expand(S.Poly(t3, p).coeff_monomial(p) - 36*c1*S.diff(A, q, 3)) == 0
A2 = A.subs({a[3]: 0, a[4]: 0})
H2 = fq + A2*p + B*p**2
G3 = p**2 + quotient(2*S.diff(fq, q) - S.diff(A2, q, 2)**2/(2*c1)*q**2, B)
assert gates(H2, G3, 0) == (0, 0) and gates(H2, G3, 1) == (0, 0)
assert gates(H, q, 2) == (0, 0)
combo = T(H, q, 1) + 2*(-c1*s)*G1 + 2*c1*G2          # B = -c1*s + c1*q
assert S.Poly(S.expand(combo), q, p).total_degree() <= 0
t3 = S.Poly(gates(H, q, 3)[0], q)
assert S.expand(t3.coeff_monomial(q**5) + 144*98*c1**2*a[4]**2) == 0
assert S.expand(t3.coeff_monomial(q**4).subs(a[4], 0) - 144*210*c1**3*f[6]) == 0
nonconstant["k=1"] = "q, p+phi1, q p+phi2 in S^1 for every A; p^2+phi3 iff A'''=0 (obstruction 36 B' A''' p); q in S^2 \\ S^3"
# k = 2
B = c2*x**2 + dl
H = fq + A*p + B*p**2
G4 = x*p + quotient(x*S.diff(A, q) - A, 2*B)
assert gates(H, G4, 0) == (0, 0) and gates(H, G4, 1) == (0, 0)
nonconstant["k=2"] = "x p + phi in S^1 for every A, x = q - (root of B')"
# k = 3
bb = S.symbols("B0:4")
Bg = sum(bb[i]*q**i for i in range(4))
t3, t5 = gates(fq + A*p + Bg*p**2, x*p + phi, 1)
pc = S.Poly(t3, p).coeff_monomial(p)
assert t5 == 0 and S.expand(pc - 24*(bb[1]*bb[2] + 6*bb[1]*bb[3]*q - 3*bb[1]*bb[3]*s + 2*bb[2]**2*s
                                       + 3*bb[2]*bb[3]*q**2 + 6*bb[2]*bb[3]*q*s + 9*bb[3]**2*q**2*s)) == 0
assert S.expand(pc - 12*(S.diff(Bg, q)*(S.diff(Bg, q, 2) + x*S.diff(Bg, q, 3)) - x*S.diff(Bg, q, 2)**2)) == 0
coeffs = S.Poly(pc, q).all_coeffs()
sol = S.solve(coeffs, [s, bb[1]], dict=True)
assert sol == [{s: -bb[2]/(3*bb[3]), bb[1]: bb[2]**2/(3*bb[3])}]
B = c3*x**3 + dl
H = fq + A*p + B*p**2
G5 = x*p + quotient(x*S.diff(A, q) - 2*A, 2*B)
assert gates(H, G5, 0) == (0, 0) and gates(H, G5, 1) == (0, 0)
# every p-degree <= 2 static element, all A, all nonconstant B
kk, gg, ff = (S.Function(n)(q) for n in ("k", "g", "f"))
Bf, Af, hf = (S.Function(n)(q) for n in ("B", "A", "h"))
Hf = hf + Af*p + Bf*p**2
t3, t5 = gates(Hf, ff + gg*p + kk*p**2, 0)
assert t5 == 0
assert S.expand(t3 - (6*(S.diff(Bf, q)*S.diff(gg, q, 2) - S.diff(Af, q, 2)*S.diff(kk, q))
                      + 12*p*(S.diff(Bf, q)*S.diff(kk, q, 2) - S.diff(Bf, q, 2)*S.diff(kk, q)))) == 0
nonconstant["k=3"] = "(q-s) p + phi in S^1 iff B' has a double root at s (Delta = b2^2 - 3 b3 b1 = 0)"
report["nonconstant_quadratic_coefficient"] = nonconstant

# 4. The affine cube sub-branch: stored minors and stable static spaces --------
names = {"q": q, "P": P, "b0": S.Symbol("b0"), "c1": S.Symbol("c1")}
with open("SIXFOLD_GLOBAL_DEPTH_CERTIFICATE.json") as handle:
    certificate = json.load(handle)
cube = {}
for entry in certificate:
    Bx, Cx = S.sympify(entry["B"], locals=names), S.sympify(entry["C"], locals=names)
    window = M.chart_window() if entry["basis"] == "static" else M.chart_window(3, 8, True)
    basis = M.static_window_basis(Bx, Cx, window)
    assert len(basis) == (15 if entry["basis"] == "static" else 8)
    matrix = M.depth_matrix(Bx, Cx, basis, 1, 1)
    minor = entry["minors"][0]
    det = DomainMatrix.from_Matrix(matrix.extract(minor["rows"], minor["cols"]).applyfunc(S.expand)).det()
    det = det.as_expr() if hasattr(det, "as_expr") else S.Rational(str(det))
    assert S.expand(det - S.sympify(minor["det"], locals=names)) == 0
    if entry["claim"] == "nonzero constant":
        assert det.is_number and det != 0
    else:
        ratio = S.cancel(det/S.sympify(entry["claim"][len("const*"):], locals=names))
        assert ratio.is_number and ratio != 0
    cube[entry["name"]] = {"rank": entry["rank"], "kernel": len(basis) - entry["rank"]}
c1s, b0s = names["c1"], names["b0"]
D, T3, T5 = M.chart_operators(q, c1s*q)
Hc = P**3 + q*P + c1s*q
space = [S.Integer(1), q, P, P**2, Hc]
assert all(T3(g) == 0 and T5(g) == 0 for g in space)
for g in space:                                    # D-stable: D g is a combination of the space
    xs = S.symbols("y0:5")
    diff = S.Poly(S.expand(D(g) - sum(u*v for u, v in zip(xs, space))), q, P).coeffs()
    assert S.solve(diff, xs, dict=True)
D0, T30, T50 = M.chart_operators(q, 0*q)
H0 = P**3 + q*P
assert T30(P*H0) == 0 and T50(P*H0) == 0 and S.expand(D0(P*H0) - P*H0) == 0
De, T3e, T5e = M.chart_operators(b0s + 0*q, c1s*q)
for m in range(9):
    assert T3e(P**m) == 0 and T5e(P**m) == 0 and S.expand(De(P**m) - c1s*m*P**(m - 1)) == 0
assert T3e(q) == 0 and T5e(q) == 0 and S.expand(De(q) + 3*P**2 + b0s) == 0
report["cube_affine"] = cube

# 5. Adversarial sweep ---------------------------------------------------------
mons = [(i, j) for j in range(6) for i in range(6 - j) if (i, j) != (0, 0)]
rnd = random.Random(20261114)
members = []
for k in (1, 2):
    for sup in itertools.combinations(mons, k):
        members.append({(6, 0): Fr(1), **{m: Fr(1) for m in sup}})
for _ in range(220):
    sup = rnd.sample(mons, rnd.choice([2, 3, 4, 5, 6, 8, 12, 20]))
    members.append({(6, 0): Fr(1), **{m: Fr(rnd.choice([-3, -2, -1, 1, 2, 3]), rnd.choice([1, 1, 2])) for m in sup}})


def from_expr(expr):
    poly = S.Poly(S.expand(expr), q, p)
    return {mon: Fr(str(cf)) for mon, cf in poly.terms()}


for _ in range(160):                               # squares c (p + beta)^2 + F, sometimes perturbed
    bt = sum(rnd.randint(-2, 2)*q**i for i in range(3)) + rnd.choice([0, 1, -1, 2])*q**3 + rnd.choice([0, 0, 1])*q**4
    dF = rnd.choice([0, 1, 2, 3, 3, 3, 4, 5, 6])
    expr = rnd.choice([1, 2, -1, 3])*(p + bt)**2 + sum(rnd.randint(-2, 2)*q**i for i in range(dF)) + rnd.choice([1, -2, 3])*q**dF
    if rnd.random() < 0.3:
        expr += rnd.randint(-2, 2)*rnd.choice([q*p**2, q**2*p**2, p**3, q*p**3, q**3*p**2])
    poly = S.Poly(S.expand(expr), q, p)
    if poly.coeff_monomial(q**6) != 0 and all(sum(m) < 6 or m == (6, 0) for m in poly.monoms()):
        members.append(from_expr(expr))
for _ in range(80):                                # the cube locus in unnormalised coordinates
    kap = rnd.choice([1, -1, 2, S.Rational(1, 2), 3])
    Pc = q**2 + kap*p
    expr = Pc**3 + (rnd.randint(-1, 1) + rnd.randint(-1, 1)*q)*Pc**2
    expr += sum(rnd.choice([0, 0, 1, -1, 2])*q**i for i in range(4))*Pc + sum(rnd.choice([0, 0, 1, -1, 2])*q**i for i in range(6))
    if rnd.random() < 0.5:                         # force both B and C affine half the time
        expr = Pc**3 + (rnd.randint(-2, 2) + rnd.randint(-2, 2)*q)*Pc + rnd.randint(-2, 2)*q
    members.append(from_expr(expr))

named = [("(p+q^3)^2+q^3", 6, 2), ("3*(p+q^3-q)^2+2*q^3+q", 6, 2), ("q^6+p^2", 5, 2), ("q^6+q*p+p^2+q^5", 5, 2),
         ("(p+q^3)^2+q^5", 4, 2), ("(p+q^2)^2+q^6", 4, 2), ("p^2+q^4*p+q^6", 4, 2),
         ("(p+q^2)^3+q*(p+q^2)+q^2", 3, 2), ("(p+q^2)^3+q^2", 3, 2), ("q^6+q*p^2", 3, 2), ("q^6+q^4*p+(q+1)*p^2", 3, 2),
         ("(p+q^3)^2+q^2", 2, 6), ("(p+q^3)^2", 2, 6), ("q^6+20*q^3*p^2-10*p^4", 2, 2), ("q^6+q^2*p^2", 2, 2),
         ("q^6+q^3*p^2", 2, 2), ("q^6+(q^3+q)*p^2", 1, 2), ("(q*p+q^3)^2", 1, 3), ("(q*p+q^3+1)^2-1", 1, 3),
         ("(p+q^2)^3+q*(p+q^2)", 1, 6), ("(p+q^2)^3+q*(p+q^2)+q", 1, 5), ("(p+q^2)^3+q", 1, G.INF),
         ("(p+q^2)^3", 1, G.INF), ("q^6+q^2*p", 1, G.INF), ("q^6+q*p", 0, G.INF), ("q^6", 0, G.INF),
         ("q^6+p^5", 1, 2), ("q^6+q*p^4", 1, 2), ("q^6+q^2*p^3", 1, 2), ("q^6+p^4", 1, 2), ("q^6+q*p^3", 2, 2), ("q^6+p^3", 2, 2)]
named_report = []
for text, depth, core in named:
    info = G.classify(G.parse(text))
    assert (info["depth"], info["core_dimension"]) == (depth, core), (text, info)
    named_report.append({"H": text, "branch": info["branch"], "depth": depth,
                         "core_dimension": "infinite" if core == G.INF else core})
    members.append(G.parse(text))
report["named_members"] = named_report

if "--extended" in sys.argv:                       # larger deterministic sample, same checks
    for sup in itertools.combinations(mons, 3):
        members.append({(6, 0): Fr(1), **{m: Fr(1) for m in sup}})
    for _ in range(2280):
        sup = rnd.sample(mons, rnd.choice([2, 3, 4, 5, 6, 8, 12, 20]))
        members.append({(6, 0): Fr(1), **{m: Fr(rnd.choice([-3, -2, -1, 1, 2, 3]), rnd.choice([1, 1, 2])) for m in sup}})

window = G.degree_window(12)
tally = {}
for h in members:
    info = G.classify(h)
    dims = G.chain(h, window, 9)
    assert dims[-1] == dims[-2] == dims[6], ("drop after depth six", h, dims)
    stop = G.first_stable(dims)
    assert stop == info["depth"] <= info["depth_bound"] <= 6, (h, dims, info)
    assert (info["depth"] == 6) == G.depth_six_conditions(h)
    key = "%s | depth %d" % (info["branch"], info["depth"])
    tally[key] = tally.get(key, 0) + 1
report["sweep"] = {"members": len(members), "tally": dict(sorted(tally.items()))}

# 6. Optional PerfectJet cross-check -------------------------------------------
if "--perfectjet" in sys.argv:
    if os.environ.get("PERFECTJET_SRC"):
        sys.path.insert(0, os.environ["PERFECTJET_SRC"])
    from perfectjet.polynomial import Poly
    from perfectjet.transvectants import transvectant as pj
    checked = 0
    for h in members[::12]:
        ham = Poly(h)
        for mon in G.degree_window(6):
            g = {mon: Fr(1)}
            for order in (1, 3, 5):
                ours = {k: Fr(v) for k, v in G.transvectant(h, g, order).items() if v}
                theirs = {k: Fr(v) for k, v in pj(ham, Poly(g), order).terms.items() if v}
                assert ours == theirs
                checked += 1
    report["perfectjet_cross_check"] = "%d transvectant comparisons agree" % checked

if "--extended" in sys.argv:
    with open("SIXFOLD_GLOBAL_DEPTH_EXTENDED_SWEEP.json", "w") as handle:
        json.dump(report["sweep"], handle, indent=1)
        handle.write("\n")
    for key, value in report["sweep"]["tally"].items():
        print("%-58s %d" % (key, value))
    print("sixfold global depth extended sweep: PASS (%d members swept)" % len(members))
    sys.exit(0)

with open("SIXFOLD_GLOBAL_DEPTH_REPLAY.json", "w") as handle:
    json.dump(report, handle, indent=1)
    handle.write("\n")
for key, value in report["sweep"]["tally"].items():
    print("%-58s %d" % (key, value))
print("sixfold global depth replay: PASS (%d members swept)" % len(members))
