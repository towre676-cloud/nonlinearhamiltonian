"""Exact certificate for the first-refinement jump in Theorem G.

Normal form B = b0 + q^2, C = eps q + lam q^2 + gam q^3.  Proves
dim S^1 = 3 for gam != 0 and dim S^1 = 4 for gam = 0, with the explicit
fourth partner J = 3 P^2 + 2 q^2 + (2 - 6 lam) P on gam = 0.
"""
import itertools
import json
import random

import sympy as S
from sympy.polys.matrices import DomainMatrix

import cube_leading_boundary as M

q, P, p, lam, eps = M.q, M.P, M.p, M.lam, M.eps
gam, b0, tt = S.symbols("gamma b0 t")
B, C = b0 + q**2, eps*q + lam*q**2 + gam*q**3
H = P**3 + B*P + C
D, T3, T5 = M.chart_operators(B, C)
J = 3*P**2 + 2*q**2 + (2 - 6*lam)*P

# the partner J, in the chart and directly in the original coordinates
assert (T3(J), T5(J), T5(D(J))) == (0, 0, 0)
assert S.expand(T3(D(J)) + 1296*gam*q) == 0
flat = lambda G: S.expand(G.subs(P, p + q**2))
Hf, Jf = flat(H), flat(J)
DJf = M.flat_transvectant(Hf, Jf, 1)
assert M.flat_transvectant(Hf, Jf, 3) == 0 and M.flat_transvectant(Hf, Jf, 5) == 0
assert M.flat_transvectant(Hf, DJf, 5) == 0
assert S.expand(M.flat_transvectant(Hf, DJf, 3) + 1296*gam*q) == 0
for g in (S.Integer(1), q, H):
    assert (T3(g), T5(g), T3(D(g)), T5(D(g))) == (0, 0, 0, 0)

basis = M.static_window_basis(B, C, M.chart_window())
assert len(basis) == 15 and all(T3(g) == 0 and T5(g) == 0 for g in basis)
assert {S.Poly(g, P, q).LC() for g in basis} == {1}
assert len({S.Poly(g, P, q).monoms()[0] for g in basis}) == 15
matrix = M.depth_matrix(B, C, basis, 1, 1)


def minors(mat, rank, symbols, patterns, fixed, seed, each=2):
    rnd = random.Random(seed)
    ring = S.QQ[symbols] if symbols else S.QQ
    found = []
    for zero in patterns:
        for _ in range(each):
            point = dict(fixed)
            for s in symbols:
                if s not in point:
                    point[s] = S.Integer(0) if s in zero else S.Rational(rnd.randint(2, 40), rnd.randint(1, 9))
            order = list(range(mat.rows))
            rnd.shuffle(order)
            numeric = mat.subs(point).extract(order, list(range(mat.cols)))
            assert numeric.rank() == rank, (point, numeric.rank())
            _, pivots = numeric.T.rref()
            rows = sorted(order[i] for i in pivots[:rank])
            _, columns = mat.subs(point).extract(rows, list(range(mat.cols))).rref()
            sub = mat.extract(rows, list(columns))
            minor = S.expand(DomainMatrix.from_Matrix(sub).convert_to(ring).det().as_expr() if False
                             else DomainMatrix.from_Matrix(sub.applyfunc(S.expand)).det().as_expr())
            assert minor != 0
            found.append(minor)
    return found


free = (lam, eps, b0)
patterns = [zero for k in range(4) for zero in itertools.combinations(free, k)]

# gam != 0: rank 12 everywhere
rnd0 = random.Random(11)
m12 = []
for rep in range(2):
    g0 = S.Rational(rnd0.randint(2, 40), rnd0.randint(1, 9))
    m12 += minors(matrix, 12, (lam, eps, gam, b0), patterns, {gam: g0}, 100 + rep, each=1)
gb12 = S.groebner(m12 + [tt*gam - 1], tt, lam, eps, gam, b0, order="grevlex")
assert gb12.exprs == [1], gb12.exprs
gcd12 = S.Integer(0)
for m in m12:
    gcd12 = S.gcd(gcd12, m)

# gam = 0: rank 11 everywhere
matrix0 = matrix.subs(gam, 0)
m11 = minors(matrix0, 11, free, patterns, {}, 200)
gb11 = S.groebner(m11, *free, order="grevlex")
assert gb11.exprs == [1], gb11.exprs

with open("CUBE_LEADING_FIRST_REFINEMENT_CERTIFICATE.json", "w") as handle:
    json.dump({"normal_form": "B = b0 + q**2, C = epsilon*q + lambda*q**2 + gamma*q**3",
               "J": S.sstr(J), "T3(D J)": "-1296*gamma*q",
               "gamma_nonzero": {"rank": 12, "minors": len(m12), "saturated_ideal": "unit",
                                 "gcd": S.sstr(S.factor(gcd12))},
               "gamma_zero": {"rank": 11, "minors": len(m11), "ideal": "unit"},
               "minors_rank_12": [S.sstr(S.factor(m)) for m in m12],
               "minors_rank_11": [S.sstr(S.factor(m)) for m in m11]}, handle, indent=1)
print("gcd of rank-12 minors:", S.factor(gcd12))
print("first refinement of Theorem G: dim S^1 = 3 (gamma != 0), 4 (gamma = 0): PASS")
