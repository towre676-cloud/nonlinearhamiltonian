"""Exact replay for the core-closure theorem (Theorem K) of
CUBE_LEADING_BOUNDARY_THEOREM.md: D_infinity = span{1, H} whenever one of
b3, c4, c5 is nonzero.

The proof is a human argument; this file replays every identity it uses and
runs adversarial exact checks on the loci where a naive count leaves room for
an exception.  A failed assertion aborts.
"""
import json
import random
from fractions import Fraction

import sympy as S

import cube_leading_boundary as M

q, P = M.q, M.P
report = {}
bs = S.symbols("b0:4")
cs = S.symbols("c0:6")
B = sum(bs[i]*q**i for i in range(4))
C = sum(cs[i]*q**i for i in range(6))
D, T3, T5 = M.chart_operators(B, C)
H = P**3 + B*P + C

# 1. D is the Poisson bracket of the chart ------------------------------------
G = S.Function("G")(q, P)
assert S.expand(D(G) - (S.diff(H, q)*S.diff(G, P) - S.diff(H, P)*S.diff(G, q))) == 0

# 2. Euler-Cramer identity and the three leading forms ------------------------
c, b = S.symbols("c b")
forms = {"I": (P**3 + c*q**5, (3, 5), 15), "II": (P**3 + b*q**3*P, (2, 3), 9), "III": (P**3 + c*q**4, (3, 4), 12)}
s = S.Function("s")(q, P)
w = S.Symbol("w")
lower = {"I": [q**3*P, q**4, q**2*P, q**3, q*P, q**2, P, q, 1],
         "II": [q**4, q**2*P, q**3, q*P, q**2, P, q, 1],
         "III": [q**2*P, q**3, q*P, q**2, P, q, 1]}
for name, (h, (wq, wP), d) in forms.items():
    weight = lambda mono: sum(e*x for e, x in zip(S.Poly(mono, q, P).monoms()[0], (wq, wP)))
    assert all(weight(t) == d for t in S.Add.make_args(h.subs({c: 1, b: 1})))
    assert all(weight(t) < d for t in lower[name])
    assert d - wq - wP > 0
    hq, hP, sq, sP = S.diff(h, q), S.diff(h, P), S.diff(s, q), S.diff(s, P)
    assert S.expand(wq*q*hq + wP*P*hP - d*h) == 0
    euler_s = wq*q*sq + wP*P*sP          # equals w*s on forms of weight w
    bracket = hq*sP - hP*sq
    assert S.expand(bracket*wq*q - (d*h*sP - euler_s*hP)) == 0
    # h is squarefree and coprime to h_P
    assert S.gcd(S.Poly(h, q, P), S.Poly(hP, q, P)).is_one or S.degree(S.gcd(h, hP), P) == 0
    assert S.resultant(h, hP, P) != 0
report["leading_forms"] = {k: S.sstr(v[0]) for k, v in forms.items()}

# 3. Bounded adversarial check of Nil(D_h) = K[h] -----------------------------
nil = {}
for name, (h, (wq, wP), d) in forms.items():
    hh = h.subs({c: S.Rational(3, 7), b: S.Rational(-5, 2)})
    Dh = lambda g: S.expand(S.diff(hh, q)*S.diff(g, P) - S.diff(hh, P)*S.diff(g, q))
    for weight in range(0, 4*d + 1):
        mons = [q**i*P**k for k in range(weight//wP + 1) for i in [(weight - wP*k)//wq]
                if wq*i + wP*k == weight]
        if not mons:
            continue
        xs = S.symbols("x0:%d" % len(mons))
        g = sum(x*m for x, m in zip(xs, mons))
        def kernel_dim(expr):
            eqs = S.Poly(expr, q, P).coeffs() if expr != 0 else []
            if not eqs:
                return len(mons)
            A, _ = S.linear_eq_to_matrix(eqs, xs)
            return len(mons) - A.rank()
        k1, k2 = kernel_dim(Dh(g)), kernel_dim(Dh(Dh(g)))
        assert k2 == k1 == (1 if weight % d == 0 else 0), (name, weight, k1, k2)
    nil[name] = "ker D_h^2 = ker D_h = K h^k in weights <= %d" % (4*d)
report["nil_check"] = nil

# 4. Coefficient recurrences of the static equations --------------------------
A = [S.Function("a%d" % k)(q) for k in range(7)]
Gs = sum(A[k]*P**k for k in range(7))
beta = bs[3] + cs[5]
E0 = (bs[1] + cs[3]) + (2*bs[2] + 4*cs[4])*q + (3*bs[3] + 10*cs[5])*q**2
a = lambda k: A[k] if k <= 6 else S.Integer(0)
t5, t3 = S.expand(T5(Gs)), S.expand(T3(Gs))
for k in range(0, 8):
    lhs5 = t5.coeff(P, k)
    rhs5 = -360*S.ff(k + 4, 4)*S.diff(a(k + 4), q) + 120*beta*S.ff(k + 5, 5)*a(k + 5)
    assert S.expand(lhs5 - rhs5) == 0
    lhs3 = t3.coeff(P, k)
    rhs3 = -6*(S.diff(a(k), q, 3) + 6*(k + 1)**2*S.diff(a(k + 1), q)
               + (k + 2)*(k + 1)*(bs[2] + 3*bs[3]*q)*S.diff(a(k + 2), q)
               - bs[3]*(k + 2)*(k + 1)*k*a(k + 2) - E0*(k + 3)*(k + 2)*(k + 1)*a(k + 3))
    assert S.expand(lhs3 - rhs3) == 0

# 5. The forced top coefficients ----------------------------------------------
al5, al4 = S.symbols("alpha5 alpha4")
a6 = S.Integer(1)
a5 = 2*beta*a6*q + al5
a4 = S.integrate(S.Rational(5, 3)*beta*a5, q) + al4
rhs_a3 = (-96*S.diff(a4, q) - 20*(bs[2] + 3*bs[3]*q)*S.diff(a5, q) + 60*bs[3]*a5 + 120*E0*a6)
assert S.degree(S.expand(rhs_a3), q) <= 2
top_a3 = S.Poly(S.expand(rhs_a3), q).coeff_monomial(q**2)/60          # coefficient of q^5 in a3
assert S.expand(top_a3 - 2*(3*bs[3] + 10*cs[5])) == 0
# compatibility of the P^4 equation
assert S.expand(-150*S.diff(a5, q) - 30*(bs[2] + 3*bs[3]*q)*0 + 120*bs[3]*a6 + 60*(3*bs[3] + 5*cs[5])) == 0
# case I: 3 b3 + 5 c5 = 0 and 2 e2 = 2 c5 force c5 = 0
sol = S.solve([3*bs[3] + 5*cs[5], 2*(3*bs[3] + 10*cs[5]) - 2*cs[5]], [bs[3], cs[5]], dict=True)
assert sol == [{bs[3]: 0, cs[5]: 0}]
# case III (b3 = c5 = 0): a3 = 2 c4 q^4 + ... forces the q^6 coefficient of a2
zero = {bs[3]: 0, cs[5]: 0}
x3 = S.symbols("y0:4")
a3 = 2*cs[4]*q**4 + sum(x3[i]*q**i for i in range(4))
rhs_a2 = (-54*S.diff(a3, q) - 12*bs[2]*S.diff(a4.subs(zero), q) + 60*E0.subs(zero)*a5.subs(zero))
top_a2 = S.Poly(S.expand(rhs_a2), q).coeff_monomial(q**3)/120
assert S.expand(top_a2 + S.Rational(18, 5)*cs[4]) == 0
report["forced_coefficients"] = {"a3[q^5]": "2*(3*b3 + 10*c5)*a6", "case III a2[q^6]": "-18*c4/5"}

# 6. Adversarial exact members (flat engine, original coordinates) -----------
rnd = random.Random(41)
r = lambda: rnd.randint(-4, 4)
members = {
    "I generic": ((r(), r(), r(), 2), (0, r(), r(), r(), r(), 3)),
    "I, 3b3+5c5=0": ((r(), r(), r(), 5), (0, r(), r(), r(), r(), -3)),
    "I, b3=0": ((r(), r(), r(), 0), (0, r(), r(), r(), r(), 1)),
    "I, pure": ((0, 0, 0, 0), (0, 0, 0, 0, 0, 1)),
    "II generic": ((r(), r(), r(), 3), (0, r(), r(), r(), r(), 0)),
    "II, pure": ((0, 0, 0, 1), (0, 0, 0, 0, 0, 0)),
    "III generic": ((r(), r(), r(), 0), (0, r(), r(), r(), 2, 0)),
    "III, 5b2+9c4=0": ((r(), r(), -9, 0), (0, r(), r(), r(), 5, 0)),
    "III, E=0": ((r(), 3, -4, 0), (0, r(), r(), -3, 2, 0)),
    "III, pure": ((0, 0, 0, 0), (0, 0, 0, 0, 1, 0)),
}
adversarial = {}
for name, (bb, cc) in members.items():
    dims = M.window_dimensions(M.reduced_hamiltonian(bb, cc), 12, (0, 1, 2, 3, 4, 5))
    assert dims[-1] == 2, (name, dims)
    adversarial[name] = {"b": bb, "c": cc, "dims_S0_to_S5": dims}
report["adversarial_members"] = adversarial
random_members = []
for case in ("I", "II", "III"):
    for _ in range(10):
        bb, cc = [r() for _ in range(4)], [0] + [r() for _ in range(5)]
        nz = rnd.choice([-3, -2, -1, 1, 2, 3])
        if case == "I":
            cc[5] = nz
        elif case == "II":
            cc[5], bb[3] = 0, nz
        else:
            cc[5], bb[3], cc[4] = 0, 0, nz
        dims = M.window_dimensions(M.reduced_hamiltonian(tuple(bb), tuple(cc)), 12, (1, 3, 5))
        assert dims[-1] == 2, (case, bb, cc, dims)
        random_members.append({"case": case, "b": bb, "c": cc, "dims_S1_S3_S5": dims})
report["random_members"] = random_members

with open("CUBE_LEADING_CORE_CLOSURE_REPLAY.json", "w") as handle:
    json.dump(report, handle, indent=1, default=str)
print(json.dumps(adversarial, indent=1, default=str))
print("cube-leading core closure replay: PASS")
