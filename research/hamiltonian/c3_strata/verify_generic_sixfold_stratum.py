"""Independent replay of GENERIC_SIXFOLD_STRATUM_THEOREM.md.  Exit 0 iff all checks pass."""
import os, random, sys
from fractions import Fraction as Fr
from math import comb
import sympy as S

HERE = os.path.dirname(os.path.abspath(__file__))
q, p, y, i, j = S.symbols("q p y i j")
CHECKS = []


def ok(name, cond):
    CHECKS.append((name, bool(cond)))
    if not cond:
        print("FAIL", name)


def T(H, G, k):
    return S.expand(sum((-1) ** a * comb(k, a) * S.diff(H, q, k - a, p, a) * S.diff(G, q, a, p, k - a) for a in range(k + 1)))


H0 = q ** 6 + y * p ** 5
G = q ** i * p ** j
ok("T5 row formula, symbolic exponents", S.simplify(S.expand_func(S.powsimp(S.expand(T(H0, G, 5) / G))
   - (720 * q * S.ff(j, 5) / p ** 5 - 120 * y * S.ff(i, 5) / q ** 5))) == 0)
ok("T3 row formula, symbolic exponents", S.simplify(S.expand_func(S.powsimp(S.expand(T(H0, G, 3) / G))
   - (120 * q ** 3 * S.ff(j, 3) / p ** 3 - 60 * y * p ** 2 * S.ff(i, 3) / q ** 3))) == 0)
c0, c1 = S.symbols("c0 c1")
A = 720 * S.ff(j, 5) * c1 - 120 * y * S.ff(i, 5) * c0
B = 120 * S.ff(j, 3) * c1 - 60 * y * S.ff(i, 3) * c0
ok("link determinant is the resonance polynomial",
   S.simplify(S.expand_func(-A + 6 * (j - 3) * (j - 4) * B - 120 * y * S.ff(i, 3) * ((i - 3) * (i - 4) - 3 * (j - 3) * (j - 4)) * c0)) == 0)
ok("two consecutive resonances force 2i + 5j = 18",
   S.expand(((i - 3) * (i - 4) - 3 * (j - 3) * (j - 4)) - ((i - 9) * (i - 10) - 3 * (j + 2) * (j + 1)) - (12 * i + 30 * j - 108)) == 0)
ok("the only isolated resonance with 6<=i<=8, 0<=j<=2 is (6,0)",
   [(a, b) for a in (6, 7, 8) for b in (0, 1, 2) if (a - 3) * (a - 4) == 3 * (b + 2) * (b + 1)] == [(6, 0)])
static = [q ** a * p ** b for a in range(3) for b in range(3)] + [H0]
ok("the ten stated elements are static for symbolic y", all(T(H0, g_, 3) == 0 and T(H0, g_, 5) == 0 for g_ in static))
# exhaustive finite cross-check of the chain argument: no other static partner up to weight 400 (y = 1)
sys.path.insert(0, HERE)
import generic_sixfold_stratum as GS
from weighted_cubic_form import gate_system
h1 = GS.hamiltonian(1)
count = 0
for w in range(0, 401):
    chain = [(a, (w - 5 * a) // 6) for a in range(w // 5 + 1) if (w - 5 * a) % 6 == 0]
    if chain:
        count += len(gate_system(h1, chain, 0).witnesses())
ok("weights 0..400 carry exactly ten static partners (finite cross-check)", count == 10)
ok("S^0, S^1, S^2 of q^6 + p^5 have dimensions 10, 2, 2", GS.dims(h1) == [10, 2, 2])
rnd = random.Random(21)
res = []
for _ in range(25):
    low = {m: Fr(rnd.randint(-5, 5), rnd.randint(1, 3)) for m in GS.LOWER}
    yy = Fr(rnd.choice([-3, -2, -1, 1, 2, 5]), rnd.randint(1, 3))
    dd = GS.dims(GS.hamiltonian(yy, low))
    res.append(dd[0] <= 10 and dd[1] == 2 and dd[2] == 2)
ok("25 random members of the 21-parameter family: dim S^0 <= 10, S^1 = S^2 = span{1,H}", all(res))
sparse = []
for m in GS.LOWER:
    dd = GS.dims(GS.hamiltonian(1, {m: 1}))
    sparse.append(dd[0] <= 10 and dd[1:] == [2, 2])
ok("each single lower monomial added to q^6 + p^5", all(sparse))
fails = [n for n, c in CHECKS if not c]
print("%d checks, %d failed" % (len(CHECKS), len(fails)))
sys.exit(1 if fails else 0)
