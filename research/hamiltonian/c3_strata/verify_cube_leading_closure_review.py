"""Independent short certificates for Theorems K and G'.

The three explicit resultants certify coprimality uniformly for every nonzero
edge coefficient. Two exact minors suffice for the first-refinement jump:
a 12x12 determinant is a nonzero rational multiple of gamma; an 11x11
determinant on gamma=0 is a nonzero rational constant. No Groebner basis is
needed for these rank lower bounds. The original 32-minor replay is retained.
"""
import itertools
import json
import random

import sympy as S
from sympy.polys.matrices import DomainMatrix

import cube_leading_boundary as M

q, P, lam, eps = M.q, M.P, M.lam, M.eps
gam, b0, c, b = S.symbols("gamma b0 c b")
resultants = {}
for name, h, expected in (
    ("I", P**3+c*q**5, 27*c**2*q**10),
    ("II", P**3+b*q**3*P, 4*b**3*q**9),
    ("III", P**3+c*q**4, 27*c**2*q**8),
):
    assert S.Poly(h, P).LC() == 1
    resultant = S.resultant(h, S.diff(h, P), P)
    assert S.expand(resultant - expected) == 0
    resultants[name] = S.sstr(S.factor(resultant))

B, C = b0+q**2, eps*q+lam*q**2+gam*q**3
basis = M.static_window_basis(B, C, M.chart_window())
assert len(basis) == 15
for g in basis:
    S.Poly(g, P, q, lam, eps, gam, b0, domain=S.QQ)
assert {S.Poly(g, P, q).LC() for g in basis} == {1}
assert len({S.Poly(g, P, q).monoms()[0] for g in basis}) == 15
D, T3, T5 = M.chart_operators(B, C)
assert all(T3(g) == T5(g) == 0 for g in basis)
H = P**3+B*P+C
J = 3*P**2+2*q**2+(2-6*lam)*P
for g in (S.Integer(1), q, H):
    assert (T3(g), T5(g), T3(D(g)), T5(D(g))) == (0, 0, 0, 0)
assert (T3(J), T5(J), T5(D(J))) == (0, 0, 0)
assert S.expand(T3(D(J)) + 1296*gam*q) == 0
matrix = M.depth_matrix(B, C, basis, 1, 1)
free = (lam, eps, b0)
patterns = [zero for k in range(4) for zero in itertools.combinations(free, k)]


def reconstruct_selected(mat, rank, symbols, fixed, seed, each, target):
    rnd = random.Random(seed)
    for index, zero in enumerate(zero for pattern in patterns for zero in [pattern]*each):
        point = dict(fixed)
        for symbol in symbols:
            if symbol not in point:
                point[symbol] = (S.Integer(0) if symbol in zero else
                                 S.Rational(rnd.randint(2, 40), rnd.randint(1, 9)))
        order = list(range(mat.rows))
        rnd.shuffle(order)
        if index != target:
            continue
        numeric = mat.subs(point).extract(order, list(range(mat.cols)))
        assert numeric.rank() == rank
        _, pivots = numeric.T.rref()
        rows = sorted(order[i] for i in pivots[:rank])
        _, columns = mat.subs(point).extract(rows, list(range(mat.cols))).rref()
        sub = DomainMatrix.from_Matrix(mat.extract(rows, list(columns)).applyfunc(S.expand))
        determinant = S.expand(sub.domain.to_sympy(sub.det()))
        return {"rank": rank, "rows": rows, "columns": list(columns),
                "determinant": S.sstr(determinant)}, determinant
    raise AssertionError("selected minor not reached")


# Original nonzero-gamma minor 14 belongs to repetition 1, local index 6.
rnd = random.Random(11)
gamma_values = [S.Rational(rnd.randint(2, 40), rnd.randint(1, 9)) for _ in range(2)]
m12, det12 = reconstruct_selected(matrix, 12, (lam, eps, gam, b0),
                                  {gam: gamma_values[1]}, 101, 1, 6)
constant12 = -S.Rational(11754292684114345474963087886302323287261184, 5)
assert S.expand(det12 - constant12*gam) == 0
m12.update({"original_minor_index": 14, "normalizing_scalar": str(constant12), "normalized": "gamma"})

# Original zero-gamma minor 5 is already constant in every remaining parameter.
m11, det11 = reconstruct_selected(matrix.subs(gam, 0), 11, free, {}, 200, 2, 5)
constant11 = -S.Integer(96171055181387888933271996733537124352000)
assert det11 == constant11
m11.update({"original_minor_index": 5, "normalizing_scalar": str(constant11), "normalized": "1"})

report = {"uniform_resultants": resultants, "matrix_shape": list(matrix.shape),
          "gamma_nonzero_minor": m12, "gamma_zero_minor": m11,
          "conclusion": "S1 has basis 1,q,H for gamma!=0 and 1,q,H,J for gamma=0"}
with open("CUBE_LEADING_CLOSURE_REVIEW_CERTIFICATE.json", "w") as handle:
    json.dump(report, handle, indent=1)
    handle.write("\n")
print("uniform resultants: PASS")
print("12x12 minor / scalar = gamma; 11x11 minor on gamma=0 / scalar = 1: PASS")
print("cube-leading closure independent short-certificate replay: PASS")
