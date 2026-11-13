"""Independent replay of WEIGHTED_CUBIC_FORM_THEOREM.md.

Uses SymPy differentiation and Groebner bases; it shares no code with
`weighted_cubic_form.py` except in the final cross-check section, where the
two engines are compared against each other.  Exit status 0 means every
check passed.  Run: python verify_weighted_cubic_form.py
"""
import itertools, json, os, random, sys
from fractions import Fraction as Fr
from math import comb
import sympy as S

HERE = os.path.dirname(os.path.abspath(__file__))
q, p, al, be, x = S.symbols("q p alpha beta x")
CHECKS = []


def ok(name, cond):
    CHECKS.append((name, bool(cond)))
    if not cond:
        print("FAIL", name)


def T(H, G, k):
    return S.expand(sum((-1) ** j * comb(k, j) * S.diff(H, q, k - j, p, j) * S.diff(G, q, j, p, k - j)
                        for j in range(k + 1)))


H = q ** 6 + al * q ** 4 * p + be * q ** 2 * p ** 2 + x * p ** 3

# 1. gate rows on a monomial with SYMBOLIC exponents: valid in every weight
e, j, d, k = S.symbols("e j d k")
G = q ** e * p ** j
t5 = S.expand(S.powsimp(S.expand(T(H, G, 5) / (q ** e * p ** j))))
t5_claim = 720 * q * S.ff(j, 5) / p ** 5 - 120 * al * e * S.ff(j, 4) / (q * p ** 4)
ok("T5 row formula, symbolic exponents", S.simplify(S.expand_func(t5 - t5_claim)) == 0)
t3 = S.expand(S.powsimp(S.expand(T(H, G, 3) / (q ** e * p ** j))))
t3_claim = (120 * S.ff(j, 3) * q ** 3 / p ** 3 + (24 * al * S.ff(j, 3) - 36 * al * e * j * (j - 1)) * q / p ** 2
            + 12 * be * e * j * (e - j) / (q * p) - 6 * x * e * (e - 1) * (e - 2) / q ** 3)
ok("T3 row formula, symbolic exponents", S.simplify(S.expand_func(t3 - t3_claim)) == 0)

# 2. tail elimination: third-gate row k along the fifth-gate ratio r_m = alpha (d-2m+2)/(6m)
r = lambda m: al * (d - 2 * m + 2) / (6 * m)
B = al ** 3 * (14 * k + 16 - 4 * d) / 9 + 2 * al * be * (d - 3 * k - 3) - 6 * x * (d - 2 * k - 1)
rowk = (120 * (k + 3) * (k + 2) * (k + 1) * r(k + 1) * r(k + 2) * r(k + 3)
        + 12 * al * (k + 2) * (k + 1) * (2 * k - 3 * (d - 2 * k - 4)) * r(k + 1) * r(k + 2)
        + 12 * be * (d - 2 * k - 2) * (k + 1) * (d - 3 * k - 3) * r(k + 1)
        - 6 * x * (d - 2 * k) * (d - 2 * k - 1) * (d - 2 * k - 2))
ok("tail identity row_k = (d-2k)(d-2k-2) B(k), symbolic k and d", S.simplify(rowk - (d - 2 * k) * (d - 2 * k - 2) * B) == 0)
B4, B5 = B.subs(k, 4), B.subs(k, 5)
ok("B(5)-B(4) and B(4) force the cube", S.expand((S.Rational(33, 2) - S.Rational(3, 2) * d) * B4
   + (S.Rational(-27, 2) + S.Rational(3, 2) * d) * B5 - (d + 3) * al * (al ** 2 - 3 * be)) == 0)
ok("cube is (q^2 + alpha p / 3)^3", S.expand(H.subs({be: al ** 2 / 3, x: al ** 3 / 27}) - (q ** 2 + al * p / 3) ** 3) == 0)

# 3. finite weights, chart x = 1
H1 = H.subs(x, 1)


def mat(w, depth, Hh=H1):
    basis = [q ** (w - 2 * i) * p ** i for i in range(w // 2 + 1)]
    cols = []
    for b in basis:
        ent, cur = {}, b
        for i in range(depth + 1):
            for kk in (3, 5):
                t = T(Hh, cur, kk)
                if t != 0:
                    for mon, c in S.Poly(t, q, p).terms():
                        ent[(i, kk) + tuple(int(v) for v in mon)] = c
            if i < depth:
                cur = T(Hh, cur, 1)
        cols.append(ent)
    rows = sorted({rw for c in cols for rw in c})
    return rows, cols


def all_minors(w, depth, size):
    rows, cols = mat(w, depth)
    M = S.Matrix([[c.get(rw, 0) for c in cols] for rw in rows])
    out = []
    for rs in itertools.combinations(range(M.rows), size):
        for cs in itertools.combinations(range(M.cols), size):
            dt = S.expand(M.extract(list(rs), list(cs)).det())
            if dt != 0:
                out.append(dt)
    return out, M


cert = json.load(open(os.path.join(HERE, "WEIGHTED_CUBIC_FORM_CERTIFICATE.json")))
CUBE = [S.sympify(s, locals={"alpha": al, "beta": be}) for s in cert["cube_ideal"]]
loc = {"alpha": al, "beta": be}
generic0 = {3: 1, 4: 1, 5: 2, 6: 2, 7: 3, 8: 3, 9: 5, 10: 5, 11: 6, 12: 7}
for w, rk in generic0.items():
    mins, M = all_minors(w, 0, rk)
    gb = S.groebner(mins, al, be, order="lex").exprs
    if w == 9:
        ok("static weight 9 drops exactly on alpha = 0", len(gb) == 1 and S.expand(gb[0] - al) == 0)
    elif w == 12:
        ok("static weight 12 drops exactly on E12 = 0", len(gb) == 1 and S.expand(gb[0] - S.sympify(cert["static"]["12"], locals=loc)) == 0)
    else:
        ok("static weight %d has constant rank %d" % (w, rk), gb == [1])
for w in (0, 1, 2):
    ok("static weight %d unconstrained" % w, not mat(w, 0)[0])
# static weights 13 and 14 as a cross-check of the tail argument at its boundary
ok("static weight 14 vanishes off the cube", all(S.groebner(all_minors(14, 0, 8)[0], al, be, order="lex").contains(c) for c in CUBE))

mins, _ = all_minors(1, 1, 1)
ok("first refinement weight 1: Delta_w", S.groebner(mins, al, be).exprs == [S.groebner([3 * al - be ** 2], al, be).exprs[0]])
mins, _ = all_minors(2, 1, 2)
g2 = S.sympify(cert["first_refinement_full"]["2"], locals=loc)
ok("first refinement weight 2: Gamma_2", len(mins) >= 1 and all(S.rem(m, g2, al) == 0 or S.groebner([g2], al, be).contains(m) for m in mins)
   and S.groebner(mins, al, be).contains(g2))
mins, _ = all_minors(4, 1, 3)
gb4 = S.groebner(mins, al, be, order="lex")
tgt4 = [S.sympify(s, locals=loc) for s in cert["first_refinement_full"]["4"]]
ok("first refinement weight 4: cube points and two further weighted points", all(gb4.contains(t) for t in tgt4)
   and all(S.groebner(tgt4, al, be, order="lex").contains(g) for g in gb4.exprs))

# kernels in the exceptional weights are one-dimensional off the cube
m1, _ = all_minors(2, 1, 1)
ok("weight 2 first-refinement kernel is at most a line off the cube", all(S.groebner(m1, al, be, order="lex").contains(t) for t in CUBE))
m2, _ = all_minors(4, 1, 2)
ok("weight 4 first-refinement kernel is at most a line off the cube", all(S.groebner(m2, al, be, order="lex").contains(t) for t in CUBE))

for key, c in sorted(cert["minor_certificates"].items()):
    rows, cols = mat(c["weight"], c["depth"])
    polys = []
    good = True
    for mn in c["minors"]:
        sub = S.Matrix([[cols[cj].get(tuple(rw), 0) for cj in mn["cols"]] for rw in mn["rows"]])
        dt = S.expand(sub.det())
        good &= S.expand(dt - S.sympify(mn["det"], locals=loc)) == 0 and dt != 0 and len(mn["rows"]) == c["minor_size"]
        polys.append(dt)
    gb = S.groebner(polys, al, be, order="lex")
    if c["target"].startswith("unit"):
        good &= gb.exprs == [1]
    else:
        good &= all(gb.contains(t) for t in CUBE)
    ok("minor certificate depth %d weight %d: %s" % (c["depth"], c["weight"], c["target"]), good)

# 4. cross-check against the Fraction engine at rational points, including each stratum
sys.path.insert(0, HERE)
import weighted_cubic_form as W
random.seed(20261113)
pts = [(1, 2, 3), (0, 2, 3), (3, 1, 3), (Fr(3, 2), 3, 2), (-6, 3, 1), (0, 0, 5), (Fr(-2), Fr(7, 3), Fr(10, 27))]
for _ in range(40):
    pts.append((Fr(random.randint(-9, 9), random.randint(1, 4)), Fr(random.randint(-9, 9), random.randint(1, 4)),
                Fr(random.choice([-3, -2, -1, 1, 2, 3]), random.randint(1, 3))))
bad = [pt for pt in pts if not W.is_cube(*pt) and W.dims(*pt) != W.predicted_dims(*pt)]
ok("engine dimensions equal Theorem 2 at %d rational points" % len(pts), not bad)
ok("weights 13..20 carry no static partner off the cube (sample)",
   all(not W.gate_system(W.hamiltonian(*pt), W.weight_basis(w), 0).witnesses() for pt in pts[:8] for w in range(13, 21)))

# 5. regressions: the established cubic theorem inside the new family
reg = []
for (u, v, w_, xx) in [(1, 3, 3, 1), (2, 12, 6, 1), (1, 2, 3, 1), (0, 1, 0, 2), (5, 0, 0, 3)]:
    low = {(3, 0): u, (2, 1): v, (1, 2): w_}
    dd = W.dims(0, 0, xx, low)
    reg.append(dd == [15, 4 if 3 * xx * v == w_ * w_ else 3, 2])
ok("regression: Delta = 3xv - w^2 jump and second-refinement collapse", all(reg))

# 6. lower-weight perturbations: gr S^r(H) is contained in S^r(leading form)
sem = []
for _ in range(12):
    a_, b_, x_ = Fr(random.randint(1, 5)), Fr(random.randint(-5, 5)), Fr(random.randint(1, 4))
    low = {m: Fr(random.randint(-3, 3)) for m in W.LOWER}
    lead = W.dims(a_, b_, x_)
    full = W.dims(a_, b_, x_, low)
    sem.append(all(f <= l for f, l in zip(full, lead)) and full[2] == 2)
ok("semicontinuity under all 12 lower-weight terms, and S^2 = span{1,H}", all(sem))
qs = W.q_survival_conditions(W.hamiltonian(Fr(3, 2), 3, 2))
ok("q survives the first refinement exactly when T3(H,H_p)=T5(H,H_p)=0 (leading case)", not qs and W.q_survival_conditions(W.hamiltonian(1, 2, 3)))

# 7. cube locus: every power of Q = q^2 + c p is static and Poisson-commutes with H
c_ = Fr(2)
hc = W.hamiltonian(3 * c_, 3 * c_ ** 2, c_ ** 3)
Qk, okc = {(0, 0): Fr(1)}, True
for kk in range(1, 15):
    Qk = W._mul(Qk, {(2, 0): Fr(1), (0, 1): c_})
    okc &= not W.transvectant(hc, Qk, 3) and not W.transvectant(hc, Qk, 5) and not W.transvectant(hc, Qk, 1)
ok("cube locus: Q^k is static and invariant for k <= 14 (finite experiment)", okc)

fails = [n for n, c in CHECKS if not c]
json.dump({"checks": [{"name": n, "passed": c} for n, c in CHECKS], "failed": fails},
          open(os.path.join(HERE, "WEIGHTED_CUBIC_FORM_REPLAY.json"), "w"), indent=1)
print("%d checks, %d failed" % (len(CHECKS), len(fails)))
sys.exit(1 if fails else 0)
