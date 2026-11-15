"""Exact replay for SIXFOLD_JUMP_LOCI_THEOREM.md (Theorem J).

Sections 1-4 replay, with every coefficient symbolic, the gate identities from
which the closed-form jump loci are read off; they are universal in the
parameters.  Section 5 compares the closed forms with exact kernels on the
windows proved to contain the first refinement, at members constructed on each
locus, at near-misses, and at random members.  Section 5 is a cross-check.
"""
import json
import random
from fractions import Fraction as Fr

import sympy as S

import cube_leading_boundary as M
import sixfold_global_depth as G
import sixfold_jump_loci as J

q, p = M.q, M.p
T = M.flat_transvectant
report = {}


def refinement_coefficients(H, obs):
    """Static gates of obs, and the coefficient dictionary of T3(H, D obs); T5(H, D obs) must vanish."""
    assert T(H, obs, 3) == 0 and T(H, obs, 5) == 0
    d = T(H, obs, 1)
    assert T(H, d, 5) == 0
    return {mon: S.expand(cf) for mon, cf in S.Poly(T(H, d, 3), q, p).terms()}


def symbols_for(monomials):
    return {m: S.Symbol("r%d%d" % m) for m in monomials}


# 1. Quartic edge:  H = q^6 + g q^3 p^2 + y p^4 + R,  candidate p + mu q --------
g, y, mu = S.symbols("gamma y mu")
mons4 = [(i, j) for j in range(4) for i in range(6) if i + j <= 5 and 0 < 2*i + 3*j < 12 and (i, j) != (2, 3)]
r = symbols_for(mons4)
H = q**6 + g*q**3*p**2 + y*p**4 + sum(r[m]*q**m[0]*p**m[1] for m in mons4)
co = refinement_coefficients(H, p + mu*q)
rr = lambda i, j: r[(i, j)]
expected = {
    (2, 1): -216*(g**2 + 40*y),
    (3, 0): -72*(3*g**2*mu + 40*mu*y + 20*rr(1, 3)),
    (0, 2): -36*(-4*g*mu*y - 7*g*rr(1, 3) + 16*rr(4, 1)*y),
    (1, 1): -72*(-g*mu*rr(1, 3) + 2*g*rr(2, 2) - 6*rr(1, 3)*rr(4, 1) + 40*rr(5, 0)*y),
    (2, 0): -36*(6*g*mu*rr(2, 2) + 3*g*rr(3, 1) - 10*mu*rr(1, 3)*rr(4, 1) + 40*mu*rr(5, 0)*y + 60*rr(0, 3)
                 + 10*rr(1, 3)*rr(5, 0) - 4*rr(2, 2)*rr(4, 1)),
    (1, 0): -24*(3*g*mu*rr(1, 2) + 3*g*rr(2, 1) - 6*mu*rr(0, 3)*rr(4, 1) - 6*mu*rr(1, 3)*rr(3, 1)
                 + 2*mu*rr(2, 2)**2 + 24*mu*rr(4, 0)*y + 30*rr(0, 3)*rr(5, 0) - 6*rr(1, 2)*rr(4, 1)),
    (0, 1): -24*(-3*g*mu*rr(0, 3) - 3*g*rr(1, 2) + 6*rr(0, 3)*rr(4, 1) - 6*rr(1, 3)*rr(3, 1)
                 + 2*rr(2, 2)**2 + 24*rr(4, 0)*y),
    (0, 0): -12*(-3*mu*rr(0, 3)*rr(3, 1) + 2*mu*rr(1, 2)*rr(2, 2) - 3*mu*rr(1, 3)*rr(2, 1) + 12*mu*rr(3, 0)*y
                 + 12*rr(0, 3)*rr(4, 0) - 3*rr(1, 2)*rr(3, 1) - 3*rr(1, 3)*rr(3, 0) + 2*rr(2, 1)*rr(2, 2)),
}
assert set(co) == set(expected) and all(S.expand(co[m] - expected[m]) == 0 for m in co)
# on gamma^2 = -40 y the (3,0) row gives mu = r13/(4y), and the last row is a consequence of the others
assert S.expand((expected[(3, 0)]/(-72)).subs(g**2, -40*y) - (-80*mu*y + 20*rr(1, 3))) == 0
solved = {mu: rr(1, 3)/(4*y)}
for mon, var in (((0, 2), rr(4, 1)), ((1, 1), rr(5, 0)), ((2, 0), rr(0, 3)), ((0, 1), rr(4, 0)), ((1, 0), rr(2, 1))):
    solved[var] = S.solve(expected[mon].subs(solved), var)[0]
last = S.together(expected[(0, 0)].subs(solved))
assert S.rem(S.expand(S.numer(last)), g**2 + 40*y, g) == 0
report["quartic_edge"] = {"partner": "p + r13/(4*y)*q", "graph": {S.sstr(k): S.sstr(S.factor(v)) for k, v in solved.items()},
                          "redundant": "the (0,0) equation follows from the other five and gamma^2 = -40*y"}

# 2. Cubic quadratic coefficient with cubic momentum terms ----------------------
a = S.symbols("a0:5")
f = S.symbols("f0:6")
b = S.symbols("b0:4")
c03, c13, s, u1, u2 = S.symbols("c03 c13 s u1 u2")
H = (q**6 + sum(f[i]*q**i for i in range(6)) + sum(a[i]*q**i for i in range(5))*p
     + sum(b[i]*q**i for i in range(4))*p**2 + (c03 + c13*q)*p**3)
co = refinement_coefficients(H, (q - s)*p + u1*q + u2*q**2)
assert S.expand(co[(1, 2)] - 540*b[3]*c13) == 0
assert S.expand(co[(0, 2)].subs(c13, 0) + 144*b[3]*c03) == 0
assert S.expand(co[(2, 1)].subs(c13, 0) - 72*b[3]*(b[2] + 3*b[3]*s)) == 0
assert S.expand(co[(1, 1)].subs({c13: 0, c03: 0, s: -b[2]/(3*b[3])}) - 48*(3*b[1]*b[3] - b[2]**2)) == 0
report["cubic_coefficient"] = "540*b3*c13 and -144*b3*c03 force c13 = c03 = 0; then s = -b2/(3 b3) and b2^2 = 3 b3 b1"

# 3. Cubic form off the cube locus ----------------------------------------------
al, be, x, lam = S.symbols("alpha beta x lambda")
mons7 = [(i, j) for j in range(3) for i in range(6) if 0 < i + 2*j <= 5]
r = symbols_for(mons7)
rr = lambda i, j: r[(i, j)]
H = q**6 + al*q**4*p + be*q**2*p**2 + x*p**3 + sum(r[m]*q**m[0]*p**m[1] for m in mons7)
co = refinement_coefficients(H, q)
assert co == {(1, 0): S.expand(48*(3*al*x - be**2)), (0, 0): S.expand(12*(-2*be*rr(1, 2) + 3*rr(3, 1)*x))}
co = refinement_coefficients(H, p + lam*q**2 + mu*q)
exp2 = {
    (2, 0): 144*(al*be + 8*al*lam*x - 2*be**2*lam - 15*x),
    (0, 1): -48*(3*al*x + be**2 - 6*be*lam*x),
    (1, 0): 24*(6*al*mu*x + 6*al*rr(1, 2) - 2*be**2*mu - 10*be*lam*rr(1, 2) + 21*lam*rr(3, 1)*x - 30*rr(5, 0)*x),
    (0, 0): 12*(-2*be*mu*rr(1, 2) - 2*be*rr(2, 1) - 4*lam*rr(1, 2)**2 + 12*lam*rr(2, 1)*x + 3*mu*rr(3, 1)*x
                + 3*rr(1, 2)*rr(3, 1) - 12*rr(4, 0)*x),
}
assert set(co) == set(exp2) and all(S.expand(co[m] - exp2[m]) == 0 for m in co)
lam0 = (3*al*x + be**2)/(6*be*x)
gamma2 = 12*al**2*x**2 + 4*al*be**2*x - be**4 - 45*be*x**2
assert S.simplify(exp2[(2, 0)].subs(lam, lam0) - 48*gamma2/(be*x)) == 0
aa, bb = S.symbols("a b")
H0 = H.subs({al: 0, be: 0})
d = T(H0, aa*q**2 + bb*q, 1)
assert T(H0, d, 5) == 0
co = {mon: S.expand(cf) for mon, cf in S.Poly(T(H0, d, 3), q, p).terms()}
assert co == {(1, 0): S.expand(504*aa*rr(3, 1)*x),
              (0, 0): S.expand(12*(-4*aa*rr(1, 2)**2 + 12*aa*rr(2, 1)*x + 3*bb*rr(3, 1)*x))}
report["cubic_form"] = {"q": "Delta_w = 0 and 3*x*r31 = 2*beta*r12",
                        "weight 2": "Gamma_2 = 0, lambda = (3*alpha*x+beta^2)/(6*beta*x), mu and Xi_Gamma as in the note",
                        "alpha = beta = 0": "q iff r31 = 0; q^2 iff r31 = 0 and r12^2 = 3*x*r21"}

# 4. The two weight-4 points ----------------------------------------------------
with open("SIXFOLD_JUMP_WEIGHT4_SYSTEM.json") as handle:
    stored = json.load(handle)
names = {str(v): v for v in list(r.values()) + [al, be, x]}
e = S.symbols("e1:6")
names.update({str(v): v for v in e})
names.update({"q": q, "p": p})
k = al*x + be**2
G4 = 12*be*x**2*p**2 + 6*x*k*q**2*p + be*k*q**4
assert S.expand(G4 - S.sympify(stored["G4"], locals=names)) == 0
cand = G4 + e[0]*q**3 + e[1]*q*p + e[2]*q**2 + e[3]*p + e[4]*q
E = {}
for tag, expr in (("S3", T(H, cand, 3)), ("S5", T(H, cand, 5)), ("D3", T(H, T(H, cand, 1), 3)), ("D5", T(H, T(H, cand, 1), 5))):
    if expr != 0:
        for mon, cf in S.Poly(expr, q, p).terms():
            E[(tag, mon)] = S.expand(cf)
assert sorted(E) == [("D3", m) for m in [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1), (3, 0), (4, 0)]] + [("S3", (0, 0))]
model = [E[("D3", (4, 0))], E[("D3", (2, 1))]]
assert all(S.expand(m - S.sympify(t, locals=names)) == 0 for m, t in zip(model, stored["model_equations"]))
sol = {v: S.sympify(stored["solution"][str(v)], locals=names) for v in e}
for key in (("S3", (0, 0)), ("D3", (1, 1)), ("D3", (2, 0)), ("D3", (0, 1)), ("D3", (1, 0))):
    assert S.simplify(E[key].subs(sol)) == 0
xi1 = S.sympify(stored["Xi1"], locals=names)/S.sympify(stored["Xi1_denominator"], locals=names)
xi2 = S.sympify(stored["Xi2"], locals=names)/S.sympify(stored["Xi2_denominator"], locals=names)
assert S.simplify(E[("D3", (3, 0))].subs(sol) - xi1) == 0
assert S.simplify(E[("D3", (0, 0))].subs(sol) - xi2) == 0
point = 2842*be**6 - 53565*be**3 - 245025
alpha_at = (79305*be**2 - 2842*be**5)/23265
for mdl in model:
    assert S.rem(S.numer(S.together(mdl.subs({x: 1, al: alpha_at}))), point, be) == 0
for den in (al, be, be**2 - 3*al, gamma2.subs(x, 1)):
    value = S.numer(S.together(den.subs(al, alpha_at)))
    assert S.gcd(S.Poly(value, be), S.Poly(point, be)).degree() == 0
disc = 53565**2 + 4*2842*245025                     # discriminant of 2842 t^2 - 53565 t - 245025, t = beta^3/x^2
assert S.integer_nthroot(disc, 2)[1] is False
report["weight_4_points"] = {"residual_conditions": 2, "Xi2_terms": len(S.Add.make_args(S.sympify(stored["Xi2"], locals=names))),
                             "rational_points": "none: 2842 t^2 - 53565 t - 245025 has irrational roots"}

# 5. Cross-check against exact kernels on the proved windows --------------------
rnd = random.Random(20261115)
ri = lambda lo=-3, hi=3: Fr(rnd.randint(lo, hi))
W4, W5, W7 = G.weight_window(2, 3, 20), G.weight_window(2, 3, 26), G.weight_window(1, 2, 12)


def check(h, window, partners, label):
    dims = G.chain(h, window, 2)
    assert dims[2] == 2 and dims[1] == 2 + len(partners), (label, dims, partners)
    for partner in partners:
        d = G.transvectant(h, partner, 1)
        for obs in (partner, d):
            assert not G.transvectant(h, obs, 3) and not G.transvectant(h, obs, 5), label
    assert G.classify(h)["depth"] == (2 if partners else 1)
    return len(partners)


tally = {}


def record(label, n):
    tally.setdefault(label, [0, 0])[1 if n else 0] += 1


def quartic_member(on_locus):
    yy = Fr(-10)*rnd.choice([1, 4]) if on_locus else Fr(rnd.choice([-10, 3, 5]))
    gg = Fr(20)*(1 if yy == -10 else 2) if on_locus else Fr(rnd.choice([20, 1, -2]))
    free = {m: ri() for m in mons4}
    h = {(6, 0): Fr(1), (3, 2): gg, (0, 4): yy}
    if on_locus:
        vals = {g: S.Rational(gg), y: S.Rational(yy)}
        vals.update({symbols_for(mons4)[m]: S.Rational(free[m]) for m in mons4})
        r4 = symbols_for(mons4)
        for var_mon in ((4, 1), (5, 0), (0, 3), (4, 0), (2, 1)):
            expr = report_solved[r4[var_mon]].subs(vals)
            free[var_mon] = Fr(str(expr))
            vals[r4[var_mon]] = expr
    h.update({m: v for m, v in free.items() if v})
    return h


# the solved graph of section 1, keyed by the coefficient symbols
sym4 = symbols_for(mons4)
report_solved = {sym4[(4, 1)]: solved[S.Symbol("r41")], sym4[(5, 0)]: solved[S.Symbol("r50")],
                 sym4[(0, 3)]: solved[S.Symbol("r03")], sym4[(4, 0)]: solved[S.Symbol("r40")],
                 sym4[(2, 1)]: solved[S.Symbol("r21")]}
for _ in range(12):
    h = quartic_member(True)
    record("c04 on locus", check(h, W4, J.quartic_edge_partners(h), "c04 on"))
    for mon in ((4, 1), (5, 0), (0, 3), (4, 0), (2, 1)):          # near-misses: break one equation
        h2 = dict(h)
        h2[mon] = h2.get(mon, Fr(0)) + 1
        record("c04 near miss", check(h2, W4, J.quartic_edge_partners(h2), "c04 near"))
for _ in range(60):
    h = quartic_member(False)
    record("c04 random", check(h, W4, J.quartic_edge_partners(h), "c04 random"))

for _ in range(120):
    b3 = Fr(rnd.choice([1, -1, 2, 3]))
    sroot, delta = ri(), ri()
    on = rnd.random() < 0.5
    bq = [delta - b3*sroot**3, 3*b3*sroot**2, -3*b3*sroot, b3] if on else [ri(), ri(), ri(), b3]
    h = {(6, 0): Fr(1)}
    h.update({(i, 2): v for i, v in enumerate(bq) if v})
    h.update({(i, 1): ri() for i in range(5)})
    h.update({(i, 0): ri() for i in range(1, 6)})
    if rnd.random() < 0.4:
        h[(0, 3)] = ri()
        h[(1, 3)] = ri() if rnd.random() < 0.5 else Fr(0)
    h = {k2: v for k2, v in h.items() if v}
    record("c32", check(h, W5, J.cubic_coefficient_partners(h), "c32"))


def cubic_form_member(kind):
    R = {m: ri() for m in mons7}
    if kind == "delta":
        A, Bc, X = Fr(6), Fr(6), Fr(2)
        R[(3, 1)] = 2*Bc*R[(1, 2)]/(3*X)
    elif kind == "gamma":
        A, Bc, X = rnd.choice([(Fr(1), Fr(-4), Fr(1)), (Fr(-6), Fr(3), Fr(1)), (Fr(51, 32), Fr(3, 4), Fr(1))])
        lam_ = (3*A*X + Bc*Bc)/(6*Bc*X)
        mu_ = (-6*A*R[(1, 2)] + 10*Bc*lam_*R[(1, 2)] - 21*lam_*R[(3, 1)]*X + 30*R[(5, 0)]*X)/(-2*(Bc*Bc - 3*A*X))
        R[(4, 0)] = (-2*Bc*mu_*R[(1, 2)] - 2*Bc*R[(2, 1)] - 4*lam_*R[(1, 2)]**2 + 12*lam_*R[(2, 1)]*X
                     + 3*mu_*R[(3, 1)]*X + 3*R[(1, 2)]*R[(3, 1)])/(12*X)
    elif kind == "origin":
        A, Bc, X = Fr(0), Fr(0), Fr(rnd.choice([1, 3, -2]))
        R[(3, 1)] = Fr(0)
        if rnd.random() < 0.5:
            R[(1, 2)] = Fr(3)*rnd.choice([1, -1, 0])
            R[(2, 1)] = R[(1, 2)]**2/(3*X)
    else:
        A, Bc, X = ri(), ri(), Fr(rnd.choice([1, 2, -1, 3]))
        if 3*Bc == A*A and 27*X == A**3:
            X += 1
    h = {(6, 0): Fr(1), (4, 1): A, (2, 2): Bc, (0, 3): X}
    h.update(R)
    return {k2: v for k2, v in h.items() if v}


for kind, count in (("delta", 15), ("gamma", 15), ("origin", 20), ("random", 60)):
    for _ in range(count):
        h = cubic_form_member(kind)
        n = check(h, W7, J.cubic_form_partners(h), "c03 " + kind)
        record("c03 " + kind, n)
        if kind in ("delta", "gamma"):
            assert n >= 1
            h2 = dict(h)
            mon = (3, 1) if kind == "delta" else (4, 0)
            h2[mon] = h2.get(mon, Fr(0)) + 1
            record("c03 %s near miss" % kind, check(h2, W7, J.cubic_form_partners(h2), "c03 near"))
assert tally["c04 on locus"] == [0, 12] and tally["c04 near miss"][1] == 0
assert tally["c03 delta near miss"][1] == 0 and tally["c03 gamma near miss"][1] == 0
report["cross_check"] = {k2: {"no partner": v[0], "partner": v[1]} for k2, v in sorted(tally.items())}

with open("SIXFOLD_JUMP_LOCI_REPLAY.json", "w") as handle:
    json.dump(report, handle, indent=1)
    handle.write("\n")
for k2, v in report["cross_check"].items():
    print("%-24s no partner %3d   partner %3d" % (k2, v["no partner"], v["partner"]))
print("sixfold jump loci replay: PASS")
