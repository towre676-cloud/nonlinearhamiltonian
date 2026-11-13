"""Three-minor Bezout certificate for the full quadratic-B stratum.

Reconstruct three of the original 32 pivot minors, then exhibit an explicit
polynomial combination equal to one. No Groebner-basis calculation is needed.
The selected indices are zero-based in the original retained certificate.
"""
import itertools
import json
import random

import sympy as S
from sympy.polys.matrices import DomainMatrix

import cube_leading_boundary as M

q, P, lam, eps = M.q, M.P, M.lam, M.eps
gam, b0 = S.symbols("gamma b0")
symbols = (lam, eps, gam, b0)
B, C = b0 + q**2, eps*q + lam*q**2 + gam*q**3
basis = M.static_window_basis(B, C, M.chart_window())
assert len(basis) == 15
for g in basis:
    S.Poly(g, q, P, *symbols, domain=S.QQ)
assert {S.Poly(g, P, q).LC() for g in basis} == {1}
assert len({S.Poly(g, P, q).monoms()[0] for g in basis}) == 15
D, T3, T5 = M.chart_operators(B, C)
assert all(T3(g) == T5(g) == 0 for g in basis)
H = P**3 + B*P + C
for g in (S.Integer(1), H):
    assert (T3(D(g)), T5(D(g)), T3(D(D(g))), T5(D(D(g)))) == (0, 0, 0, 0)
assert S.expand(T3(D(D(q))) - 432*(2*P + 3*gam*q + lam)) == 0
assert (T3(D(q)), T5(D(q))) == (0, 0)
matrix = M.depth_matrix(B, C, basis, 1, 2)
patterns = [zero for k in range(5) for zero in itertools.combinations(symbols, k)]
rnd = random.Random(7)
selected = {}
index = 0
for zero in patterns:
    for _ in range(2):
        point = {s: (S.Integer(0) if s in zero else S.Rational(rnd.randint(2, 40), rnd.randint(1, 9)))
                 for s in symbols}
        order = list(range(matrix.rows))
        rnd.shuffle(order)
        if index in (8, 23, 28):
            numeric = matrix.subs(point).extract(order, list(range(matrix.cols)))
            assert numeric.rank() == 13
            _, pivots = numeric.T.rref()
            rows = sorted(order[i] for i in pivots[:13])
            _, cols = matrix.subs(point).extract(rows, list(range(matrix.cols))).rref()
            sub = matrix.extract(rows, list(cols))
            dm = DomainMatrix.from_Matrix(sub)
            determinant = S.expand(dm.domain.to_sympy(dm.det()))
            poly = S.Poly(determinant, *symbols, domain=S.QQ)
            leading = poly.LC()
            normalized = S.expand(determinant / leading)
            selected[index] = (rows, list(cols), determinant, leading, normalized)
            print("reconstructed minor", index, ":", S.factor(normalized), flush=True)
        index += 1
assert selected[8][4] == gam
assert selected[28][4] == lam
f = selected[23][4]
constant = S.expand(f.subs({lam: 0, gam: 0}))
assert constant == -S.Rational(35, 27)
lambda_cofactor = S.cancel((f - f.subs(lam, 0)) / lam)
gamma_cofactor = S.cancel((f.subs(lam, 0) - constant) / gam)
cofactors = {
    8: -gamma_cofactor / (constant * selected[8][3]),
    23: 1 / (constant * selected[23][3]),
    28: -lambda_cofactor / (constant * selected[28][3]),
}
for value in cofactors.values():
    S.Poly(value, *symbols, domain=S.QQ)
assert S.expand(sum(cofactors[i] * selected[i][2] for i in selected)) == 1
report = {
    "static_dimension": 15, "depth_2_rank": 13, "core_dimension": 2,
    "matrix_shape": list(matrix.shape), "original_minor_indices": sorted(selected),
    "normalized_minor_23": S.sstr(f), "constant_modulo_gamma_lambda": S.sstr(constant),
    "bezout_sum": "1",
    "minors": [{"index": i, "rows": selected[i][0], "columns": selected[i][1],
                "determinant": S.sstr(selected[i][2]),
                "normalizing_scalar": S.sstr(selected[i][3]),
                "normalized": S.sstr(selected[i][4]),
                "bezout_cofactor": S.sstr(S.expand(cofactors[i]))} for i in sorted(selected)],
}
with open("CUBE_LEADING_QUADRATIC_SHORT_CERTIFICATE.json", "w") as handle:
    json.dump(report, handle, indent=1)
    handle.write("\n")
print("three exact 13x13 minors have an explicit Bezout identity equal to 1: PASS")
