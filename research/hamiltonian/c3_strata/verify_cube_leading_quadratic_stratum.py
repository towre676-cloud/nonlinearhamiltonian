"""Exact certificate for Theorem G of CUBE_LEADING_BOUNDARY_THEOREM.md.

Stratum b3 = c4 = c5 = 0, b2 != 0, normalised to B = b0 + q^2,
C = eps q + lam q^2 + gam q^3.  The 13 x 13 minors of the depth-2 gate matrix
on the 15-dimensional static space, with pivots chosen at generic points and
on every coordinate stratum of (lam, eps, gam, b0), generate the unit ideal.
Runs for several minutes.
"""
import itertools
import json
import random

import sympy as S

import cube_leading_boundary as M

q, P, lam, eps = M.q, M.P, M.lam, M.eps
gam, b0 = S.symbols("gamma b0")
B = b0 + q**2
C = eps*q + lam*q**2 + gam*q**3
H = P**3 + B*P + C
D, T3, T5 = M.chart_operators(B, C)
assert S.expand(M.gate_symbol(B, C) - (gam + 2*q)) == 0

basis = M.static_window_basis(B, C, M.chart_window())
assert len(basis) == 15 and all(T3(g) == 0 and T5(g) == 0 for g in basis)
assert len({S.Poly(g, P, q).monoms()[0] for g in basis}) == 15
assert {S.Poly(g, P, q).LC() for g in basis} == {1}
for g in (S.Integer(1), q, H):
    assert (T3(D(g)), T5(D(g))) == (0, 0)
for g in (S.Integer(1), H):
    assert (T3(D(D(g))), T5(D(D(g)))) == (0, 0)
obstruction = S.factor(T3(D(D(q))))
assert obstruction != 0

matrix = M.depth_matrix(B, C, basis, 1, 2)
symbols = (lam, eps, gam, b0)
patterns = [zero for k in range(5) for zero in itertools.combinations(symbols, k)]
rnd = random.Random(7)
minors = []
for zero in patterns:
    for _ in range(2):
        point = {s: (S.Integer(0) if s in zero else S.Rational(rnd.randint(2, 40), rnd.randint(1, 9)))
                 for s in symbols}
        order = list(range(matrix.rows))
        rnd.shuffle(order)
        numeric = matrix.subs(point).extract(order, list(range(matrix.cols)))
        assert numeric.rank() == 13, point
        _, pivots = numeric.T.rref()
        rows = sorted(order[i] for i in pivots[:13])
        _, columns = matrix.subs(point).extract(rows, list(range(matrix.cols))).rref()
        minor = S.expand(S.numer(S.together(matrix.extract(rows, list(columns)).det(method="bareiss"))))
        assert minor != 0
        minors.append(minor)
        print("quadratic stratum: verified minor %d/32" % len(minors), flush=True)
groebner = S.groebner(minors, *symbols, order="grevlex")
assert groebner.exprs == [1], groebner.exprs

with open("CUBE_LEADING_QUADRATIC_STRATUM_CERTIFICATE.json", "w") as handle:
    json.dump({"B": "b0 + q**2", "C": "epsilon*q + lambda*q**2 + gamma*q**3", "static_dimension": 15,
               "depth_2_rank": 13, "minor_ideal": "unit", "T3(D^2 q)": S.sstr(obstruction),
               "minors": [S.sstr(S.factor(m)) for m in minors]}, handle, indent=1)
print("T3(D^2 q) =", obstruction)
print("quadratic stratum: 32 minors generate the unit ideal: PASS")
