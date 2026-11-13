"""Independent replay of Theorem 5 (quartic Newton edge).  Exit 0 iff all checks pass."""
import itertools, os, random, sys
from fractions import Fraction as Fr
from math import comb
import sympy as S

HERE = os.path.dirname(os.path.abspath(__file__))
q, p, g, y, d, j, e = S.symbols("q p gamma y d j e")
CHECKS = []


def ok(name, cond):
    CHECKS.append((name, bool(cond)))
    if not cond:
        print("FAIL", name)


def T(H, G, k):
    return S.expand(sum((-1) ** a * comb(k, a) * S.diff(H, q, k - a, p, a) * S.diff(G, q, a, p, k - a) for a in range(k + 1)))


H = q ** 6 + g * q ** 3 * p ** 2 + y * p ** 4
G = q ** e * p ** j
t5 = S.powsimp(S.expand(T(H, G, 5) / G)) - (720 * q * S.ff(j, 5) / p ** 5 + 120 * g * e * (e - 1) * S.ff(j, 3) / (q ** 2 * p ** 3))
t3 = S.powsimp(S.expand(T(H, G, 3) / G)) - (120 * S.ff(j, 3) * q ** 3 / p ** 3
     + g * j * (6 * (j - 1) * (j - 2) - 36 * e * (j - 1) + 18 * e * (e - 1)) / p - 24 * y * e * (e - 1) * (e - 2) * p / q ** 3)
ok("T5 row formula, symbolic exponents", S.simplify(S.expand_func(t5)) == 0)
ok("T3 row formula, symbolic exponents", S.simplify(S.expand_func(t3)) == 0)
i = (d - 3 * j) / 2
N = g ** 2 * (S.Rational(1, 3) * i * (i - 1) - (j - 1) * (j - 2) + 6 * i * (j - 1)) - 24 * y * (i + 1) * (j - 1)
F0 = -g * (i + 3) * (i + 2) / (6 * j * (j - 1))
Fp = -g * i * (i - 1) / (6 * (j + 2) * (j + 1))
row = 120 * (j + 2) * (j + 1) * j * Fp * F0 + g * j * (6 * (j - 1) * (j - 2) - 36 * i * (j - 1) + 18 * i * (i - 1)) * F0 \
    - 24 * y * (i + 3) * (i + 2) * (i + 1)
ok("tail identity: (j-1) row = (i+3)(i+2) N(d,j)", S.simplify(row * (j - 1) - (i + 3) * (i + 2) * N) == 0)
co = S.Poly(S.expand(N), j).all_coeffs()
ok("N has degree <= 2 in j", len(co) == 3)
ok("N is never the zero polynomial unless gamma = y = 0",
   S.expand(4 * co[0] + 37 * g ** 2 - 144 * y) == 0 and S.expand(-2 * co[1] - (d + 5) * (24 * y - 5 * g ** 2)) == 0
   and S.solve([144 * y - 37 * g ** 2, 24 * y - 5 * g ** 2], [g, y], dict=True) == [{g: 0, y: 0}])

H1 = H.subs(y, 1)


def basis(w):
    return [q ** ((w - 3 * jj) // 2) * p ** jj for jj in range(w // 3 + 1) if (w - 3 * jj) % 2 == 0]


def drop(w, depth):
    cols = []
    for b in basis(w):
        ent, cur = {}, b
        for it in range(depth + 1):
            for k in (3, 5):
                t = T(H1, cur, k)
                if t != 0:
                    for mon, c in S.Poly(t, q, p).terms():
                        ent[(it, k) + tuple(mon)] = c
            if it < depth:
                cur = T(H1, cur, 1)
        cols.append(ent)
    rows = sorted({r for c in cols for r in c}, key=str)
    if not rows:
        return 0, S.Integer(0)
    M = S.Matrix([[c.get(r, 0) for c in cols] for r in rows])
    r = M.subs(g, S.Rational(11, 7)).rank()
    combos = [(rs, cs) for rs in itertools.combinations(range(M.rows), r) for cs in itertools.combinations(range(M.cols), r)]
    random.Random(1000 * depth + w).shuffle(combos)
    acc = S.Integer(0)
    for rs, cs in combos[:400]:
        acc = S.gcd(acc, S.expand(M.extract(list(rs), list(cs)).det()))
        if acc != 0 and acc.is_number:
            break
    return r, acc


EXPECT = {(0, 7): g, (0, 9): 3 * g ** 2 + 80, (0, 11): 3 * g ** 2 - 32, (0, 16): g, (0, 18): g ** 2 + 6, (0, 20): g ** 2 - 24,
          (1, 3): g ** 2 + 40}
KER = {0: {0: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 8: 1, 10: 1, 12: 1, 14: 1}, 1: {0: 1, 12: 1}, 2: {0: 1, 12: 1}}
good = True
for depth in (0, 1, 2):
    for w in range(0, 35):
        n = len(basis(w))
        if n == 0:
            continue
        r, acc = drop(w, depth)
        good &= (n - r) == KER[depth].get(w, 0)
        if (depth, w) in EXPECT:
            f = S.Poly(acc, g).monic().as_expr() if not acc.is_number else None
            good &= f is not None and S.expand(f - S.Poly(EXPECT[(depth, w)], g).monic().as_expr()) == 0
        else:
            good &= (r == 0) or (acc != 0 and acc.is_number)
        if not good:
            print("mismatch at depth", depth, "weight", w, r, acc)
            break
ok("weights 0..34, depths 0,1,2: generic kernels and rank-drop polynomials as stated", good)

sys.path.insert(0, HERE)
import quartic_edge as QE
pts = [(1, 3), (0, 3), (12, 6), (6, -6), (4, Fr(3, 2)), (4, Fr(-3, 5)), (2, Fr(-1, 10)), (2, 1), (Fr(-5, 2), Fr(7, 3))]
ok("engine dimensions equal Theorem 5 at rational points on every stratum", all(QE.dims(*pt) == QE.predicted_dims(*pt) for pt in pts))
ok("no static partner in weights 35..60 (sample)", all(not QE.gate_system(QE.hamiltonian(*pt), QE.weight_basis(w), 0).witnesses()
   for pt in pts[:5] for w in range(35, 61) if QE.weight_basis(w)))
rnd = random.Random(5)
sem = []
for _ in range(6):
    low = {(a, b): Fr(rnd.randint(-3, 3)) for a in range(6) for b in range(4) if 2 * a + 3 * b < 12 and a + b <= 5}
    gg, yy = Fr(rnd.randint(1, 5)), Fr(rnd.randint(1, 4))
    full, lead = QE.dims(gg, yy, low), QE.dims(gg, yy)
    sem.append(all(f <= l for f, l in zip(full, lead)) and full[2] == 2)
ok("lower-weight perturbations: dimensions bounded by the leading form and S^2 = span{1,H}", all(sem))
fails = [n for n, c in CHECKS if not c]
print("%d checks, %d failed" % (len(CHECKS), len(fails)))
sys.exit(1 if fails else 0)
