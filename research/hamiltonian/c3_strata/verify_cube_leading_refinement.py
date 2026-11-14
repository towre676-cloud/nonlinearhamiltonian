"""Exact replay for CUBE_LEADING_REFINEMENT_THEOREM.md (Theorem R).

On the region where one of b3, c4, c5 is nonzero this certifies the complete
refinement tower: the exact loci where dim S^1 jumps, the explicit extra
partners, and S^2 = span{1, H} at every parameter value.

Every rank lower bound is a stored minor (rows, columns) of an exact gate
matrix, reconstructed here and required to equal its stored determinant.  A
minor is used only in one of three ways: it is a nonzero rational constant; it
is a nonzero constant times one stated polynomial; or two minors in a single
variable have a stated greatest common divisor, exhibited by an explicit
Bezout identity.  No Groebner basis and no sampling enters a proof step.
"""
import json
from fractions import Fraction

import sympy as S
from sympy.polys.matrices import DomainMatrix

import cube_leading_boundary as M

q, P = M.q, M.P
report = {}

# 1. Universal partner identities, all ten coefficients symbolic --------------
bs = S.symbols("b0:4")
cs = S.symbols("c0:6")
alpha = S.Symbol("alpha")
B = sum(bs[i]*q**i for i in range(4))
C = sum(cs[i]*q**i for i in range(6))
D, T3, T5 = M.chart_operators(B, C)
assert (T3(q), T5(q), T5(D(q))) == (0, 0, 0)
assert S.expand(T3(D(q)) - 36*bs[3]) == 0
G = P + alpha*q
assert (T3(G), T5(G), T5(D(G))) == (0, 0, 0)
assert S.expand(T3(D(G)) - (36*alpha*bs[3] - 72*bs[2] - 144*cs[4] - (216*bs[3] + 720*cs[5])*q)) == 0


def gates(Bx, Cx, element, depth):
    Dx, T3x, T5x = M.chart_operators(Bx, Cx)
    current = element
    for _ in range(depth):
        current = Dx(current)
    return S.expand(T3x(current)), S.expand(T5x(current))


partners = {}
# q on b3 = 0
z = {bs[3]: 0}
t3, t5 = gates(B.subs(z), C.subs(z), q, 2)
assert t5 == 0
assert S.expand(t3 - (432*P*(2*bs[2] + 2*cs[4] + 10*cs[5]*q) + 432*cs[2] + 1296*cs[3]*q
                      + 2592*cs[4]*q**2 + 4320*cs[5]*q**3)) == 0
partners["q on b3=0"] = "T3(D^2 q) = " + S.sstr(S.collect(t3, P))
# Pi on 3 b3 + 10 c5 = 0
z = {cs[5]: -S.Rational(3, 10)*bs[3]}
Pi = bs[3]*P + (2*bs[2] + 4*cs[4])*q
assert gates(B.subs(z), C.subs(z), Pi, 0) == (0, 0) and gates(B.subs(z), C.subs(z), Pi, 1) == (0, 0)
t3, t5 = gates(B.subs(z), C.subs(z), Pi, 2)
assert t5 == 0 and S.expand(S.Poly(t3, P).coeff_monomial(P**2) - 5184*bs[3]**2) == 0
partners["Pi on 3b3+10c5=0"] = "P^2-coefficient of T3(D^2 Pi) = 5184*b3**2"
# J2 on c5 = 0, 4 c4 = 5 b3^2
z = {cs[5]: 0, cs[4]: S.Rational(5, 4)*bs[3]**2}
b0_, b1_, b2_, b3_ = bs
J2 = (54*b3_**2*P**2 + (168*b2_*b3_**2 + 245*b3_**4 - 36*b3_**3*q - 108*b3_*cs[3])*P
      + 36*b3_**3*q**3 + (36*b2_*b3_**2 + 15*b3_**4)*q**2
      + (-216*b1_*b3_**2 + 264*b2_**2*b3_ + 1270*b2_*b3_**3 - 216*b2_*cs[3] + 1225*b3_**5
         - 756*b3_**2*cs[3] + 216*b3_*cs[2])*q)
assert gates(B.subs(z), C.subs(z), J2, 0) == (0, 0) and gates(B.subs(z), C.subs(z), J2, 1) == (0, 0)
t3, t5 = gates(B.subs(z), C.subs(z), J2, 2)
top = S.Poly(t3, P, q).coeff_monomial(P**2*q)
assert t5 == 0 and S.expand(top - 1866240*b3_**4) == 0
partners["J2 on c5=0, 4c4=5b3^2"] = "q P^2-coefficient of T3(D^2 J2) = 1866240*b3**4"
# P on b3 = c5 = 0, b2 = -2 c4
z = {bs[3]: 0, cs[5]: 0, bs[2]: -2*cs[4]}
assert gates(B.subs(z), C.subs(z), P, 1) == (0, 0)
t3, t5 = gates(B.subs(z), C.subs(z), P, 2)
assert t5 == 0 and S.expand(t3 - (864*P*(3*cs[3] + 12*cs[4]*q) + 864*bs[1]*cs[4] - 3456*cs[4]**2*q)) == 0
partners["P on b3=c5=0, b2=-2c4"] = "T3(D^2 P) = " + S.sstr(S.collect(t3, P))
report["partners"] = partners

# 2. Stored minors ------------------------------------------------------------
with open("CUBE_LEADING_REFINEMENT_CERTIFICATE.json") as handle:
    certificate = json.load(handle)
names = {str(s): s for s in list(bs) + list(cs)}
names.update({"q": q, "P": P})
ranks = {}
for entry in certificate:
    Bx, Cx = S.sympify(entry["B"], locals=names), S.sympify(entry["C"], locals=names)
    params = [names[s] for s in entry["parameters"]]
    basis = M.static_window_basis(Bx, Cx, M.chart_window())
    Dx, T3x, T5x = M.chart_operators(Bx, Cx)
    assert all(T3x(g) == 0 and T5x(g) == 0 for g in basis)
    for g in basis:
        S.Poly(g, q, P, *params, domain=S.QQ)          # polynomial in the parameters
    assert {S.Poly(g, P, q).LC() for g in basis} == {1}
    assert len({S.Poly(g, P, q).monoms()[0] for g in basis}) == len(basis)
    assert len(basis) - entry["rank"] in (2, 3, 4)
    matrix = M.depth_matrix(Bx, Cx, basis, 1, entry["depth"])
    dets = []
    for minor in entry["minors"]:
        assert len(minor["rows"]) == len(minor["cols"]) == entry["rank"]
        sub = matrix.extract(minor["rows"], minor["cols"]).applyfunc(S.expand)
        det = DomainMatrix.from_Matrix(sub).det().as_expr()
        assert S.expand(det - S.sympify(minor["det"], locals=names)) == 0
        dets.append(det)
    claim = entry["claim"]
    if claim == "nonzero constant":
        assert len(dets) == 1 and dets[0].is_number and dets[0] != 0
    elif claim.startswith("const*"):
        target = S.sympify(claim[len("const*"):], locals=names)
        ratio = S.cancel(dets[0]/target)
        assert len(dets) == 1 and ratio.is_number and ratio != 0
    else:
        assert claim.startswith("gcd = const*") and len(dets) == 2
        target = S.sympify(claim[len("gcd = const*"):], locals=names)
        (x,) = target.free_symbols
        assert all(d.free_symbols == {x} for d in dets)
        u, v, g = S.gcdex(dets[0], dets[1], x)
        assert S.expand(u*dets[0] + v*dets[1] - g) == 0
        ratio = S.cancel(g/target)
        assert ratio.is_number and ratio != 0
    ranks[entry["name"]] = {"static_dimension": len(basis), "depth": entry["depth"],
                            "rank": entry["rank"], "kernel": len(basis) - entry["rank"], "claim": claim}
report["rank_certificates"] = ranks
assert len(ranks) == 13

# 3. Ledger: exact members in the original coordinates (discovery evidence) ---
F = Fraction
ledger_members = [
    ("I generic", (2, -1, 3, 2), (0, 1, -2, 4, 3, 5), [14, 2, 2, 2]),
    ("I, b3 = 0", (2, -1, 3, 0), (0, 1, -2, 4, 3, 5), [14, 3, 2, 2]),
    ("I, 3b3 + 10c5 = 0", (2, -1, 3, 10), (0, 1, -2, 4, 3, -3), [14, 3, 2, 2]),
    ("I, 3b3 + 5c5 = 0", (2, -1, 3, 5), (0, 1, -2, 4, 3, -3), [15, 2, 2, 2]),
    ("II generic", (2, -1, 3, 2), (0, 1, -2, 4, 3, 0), [14, 2, 2, 2]),
    ("II, 4c4 = 5b3^2, b2 = 0", (2, -1, 0, 2), (0, 1, -2, 4, 5, 0), [14, 3, 2, 2]),
    ("II, 4c4 = 5b3^2, b2 != 0", (2, -1, 3, 2), (0, 1, -2, 4, 5, 0), [14, 3, 2, 2]),
    ("III generic", (2, -1, 3, 0), (0, 1, -2, 4, 3, 0), [15, 3, 2, 2]),
    ("III, b2 = -2c4", (2, -1, -6, 0), (0, 1, -2, 4, 3, 0), [15, 4, 2, 2]),
    ("III, b2 = -c4", (2, -1, -3, 0), (0, 1, -2, 4, 3, 0), [15, 3, 2, 2]),
    ("III, 5b2 + 9c4 = 0", (2, -1, -9, 0), (0, 1, -2, 4, 5, 0), [15, 3, 2, 2]),
]
ledger = []
for name, b, c, expected in ledger_members:
    dims = M.window_dimensions(M.reduced_hamiltonian(b, c), 12, (0, 1, 2, 3))
    assert dims == expected, (name, dims)
    ledger.append({"member": name, "b": b, "c": c, "dims_S0_to_S3": dims})
# the infinite-static locus E = 0 inside case III: only S^1 onward is meaningful
dims = M.window_dimensions(M.reduced_hamiltonian((2, 3, -4, 0), (0, 1, -2, -3, 2, 0)), 12, (1, 2, 3))
assert dims == [4, 2, 2] == M.window_dimensions(M.reduced_hamiltonian((2, 3, -4, 0), (0, 1, -2, -3, 2, 0)), 16, (1, 2, 3))
ledger.append({"member": "III, E = 0 (static sector infinite)", "b": (2, 3, -4, 0), "c": (0, 1, -2, -3, 2, 0),
               "dims_S1_to_S3": dims})
report["ledger"] = ledger

with open("CUBE_LEADING_REFINEMENT_REPLAY.json", "w") as handle:
    json.dump(report, handle, indent=1, default=str)
for name, row in ranks.items():
    print("%-42s static %2d  depth %d  rank %2d  kernel %d  [%s]" % (
        name, row["static_dimension"], row["depth"], row["rank"], row["kernel"], row["claim"]))
print("cube-leading refinement replay: PASS")
