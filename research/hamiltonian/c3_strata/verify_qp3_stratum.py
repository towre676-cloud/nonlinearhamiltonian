"""Independent replay of Theorem 7 (stratum with leading form q^6 + c q p^3).  Exit 0 iff all checks pass."""
import os, random, sys
from fractions import Fraction as Fr
from math import comb
import sympy as S

HERE = os.path.dirname(os.path.abspath(__file__))
q, p, c, m = S.symbols("q p c m")
CHECKS = []


def ok(name, cond):
    CHECKS.append((name, bool(cond)))
    if not cond:
        print("FAIL", name)


def T(H, G, k):
    return S.expand(sum((-1) ** a * comb(k, a) * S.diff(H, q, k - a, p, a) * S.diff(G, q, a, p, k - a) for a in range(k + 1)))


H = q ** 6 + c * q * p ** 3
ok("fifth derivatives of H: only d_q^5 H = 720 q is nonzero",
   [S.diff(H, q, 5 - a, p, a) for a in range(6)] == [720 * q, 0, 0, 0, 0, 0])
g = [S.Function("g%d" % j)(q) for j in range(5)]
G = sum(g[j] * p ** j for j in range(5))
t3 = S.expand(sum((-1) ** a * comb(3, a) * S.diff(H, q, 3 - a, p, a) * S.diff(G, q, a, p, 3 - a) for a in range(4)))
rows = True
for j in range(5):
    claim = 120 * q ** 3 * (j + 3) * (j + 2) * (j + 1) * (g[j + 3] if j + 3 < 5 else 0) + 18 * c * j * S.diff(g[j], q, 2) - 6 * c * q * S.diff(g[j], q, 3)
    rows &= S.simplify(t3.coeff(p, j) - claim) == 0
ok("third gate = five ordinary differential equations, for arbitrary g_j", rows and S.simplify(t3.coeff(p, 5)) == 0)
ok("indicial polynomial of q g''' - 3 j g'' is m(m-1)(m-2-3j)", all(
   S.factor(S.simplify((q * S.diff(q ** m, q, 3) - 3 * j * S.diff(q ** m, q, 2)) / q ** (m - 2)) - m * (m - 1) * (m - 2 - 3 * j)) == 0 for j in range(5)))
ok("the only resonance: source q^3 from the constant term of g_4 meets the root m = 5 of row j = 1",
   [(j, s) for j, src in ((1, (0, 1, 14)), (0, (0, 1, 11))) for s in src if (s + 5) * (s + 4) * (s + 3 - 3 * j) == 0] == [(1, 0)])
basis = [S.Integer(1), q, q ** 2, p, q * p, q ** 5 * p, p ** 2, q * p ** 2, q ** 8 * p ** 2, p ** 3 + 2 * q ** 5 / c, q * p ** 3 + q ** 6 / c,
         q ** 11 * p ** 3 + q ** 16 / (28 * c), q * p ** 4 + 16 * q ** 6 * p / c, q ** 14 * p ** 4 + 40 * q ** 19 * p / (399 * c)]
ok("the 14 stated elements are static for symbolic c", all(S.simplify(T(H, b, 3)) == 0 and T(H, b, 5) == 0 for b in basis))
ok("they are linearly independent (distinct leading monomials in p, then q)", len({S.Poly(b, p, q).monoms(order="lex")[0] for b in basis}) == 14)
ok("p^4 has no static completion", S.factor(T(H, p ** 4, 3)) == 2880 * p * q ** 3)
ok("q survives the first refinement: D_H q = -3 c q p^2 is static", S.expand(T(H, q, 1) + 3 * c * q * p ** 2) == 0 and T(H, q * p ** 2, 3) == 0)

sys.path.insert(0, HERE)
from weighted_cubic_form import gate_system
h = {(6, 0): Fr(1), (1, 3): Fr(1)}
B = [(a, b) for a in range(21) for b in range(5)]
ok("S^0, S^1, S^2 of q^6 + q p^3 have dimensions 14, 3, 2", [len(gate_system(h, B, r).witnesses()) for r in (0, 1, 2)] == [14, 3, 2])
W = [(a, b) for a in range(21) for b in range(13) if 3 * a + 5 * b <= 62]
LOW = [(a, b) for a in range(6) for b in range(6) if a + b <= 5 and 3 * a + 5 * b < 18]
rnd = random.Random(13)
good = len(LOW) == 15
for _ in range(4):
    h2 = dict(h)
    h2[(1, 3)] = Fr(rnd.choice([-2, 1, 3]), rnd.randint(1, 2))
    h2.update({mm: Fr(rnd.randint(-3, 3)) for mm in LOW})
    h2 = {k: v for k, v in h2.items() if v}
    d = [len(gate_system(h2, W, r).witnesses()) for r in (0, 1, 2)]
    good &= d[0] <= 14 and d[1] <= 3 and d[2] == 2
ok("random members with all 15 lower-weight terms: dims within (14, 3) and S^2 = span{1,H}", good)
fails = [n for n, c_ in CHECKS if not c_]
print("%d checks, %d failed" % (len(CHECKS), len(fails)))
sys.exit(1 if fails else 0)
