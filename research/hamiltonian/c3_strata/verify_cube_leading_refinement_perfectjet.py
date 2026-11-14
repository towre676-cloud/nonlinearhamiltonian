"""Independent PerfectJet replay of the Theorem R certificates.

Requires PerfectJet (installed or through PERFECTJET_SRC).  Two checks, both
in the original coordinates (q, p) with PerfectJet's own flat transvectants:

1. every stored minor of CUBE_LEADING_REFINEMENT_CERTIFICATE.json is rebuilt at
   random rational parameter points from PerfectJet iterated gates (only the
   row labels and the static basis come from the chart code) and its exact
   determinant is compared with the stored determinant evaluated there;
2. the ledger members are recomputed on the weight-12 window with PerfectJet
   gates and SymPy exact ranks, independently of the local flat engine.

These are exact point checks.  They test the transported operators and the
stored determinants; the all-parameter statements remain those proved in
CUBE_LEADING_REFINEMENT_THEOREM.md.
"""
import json
import os
import random
import sys
from fractions import Fraction

import sympy as S
from sympy.polys.matrices import DomainMatrix

import cube_leading_boundary as M

if os.environ.get("PERFECTJET_SRC"):
    sys.path.insert(0, os.environ["PERFECTJET_SRC"])
from perfectjet.polynomial import Poly
from perfectjet.transvectants import transvectant

q, P, p = M.q, M.P, M.p
bs = S.symbols("b0:4")
cs = S.symbols("c0:6")
names = {str(s): s for s in list(bs) + list(cs)}
names.update({"q": q, "P": P})


def to_flat(expr):
    poly = S.Poly(S.expand(expr.subs(P, p + q**2)), q, p)
    return Poly({mon: Fraction(int(S.numer(cf)), int(S.denom(cf))) for mon, cf in poly.terms()})


def to_chart(poly):
    expr = sum(S.Rational(Fraction(v).numerator, Fraction(v).denominator)*q**i*(P - q**2)**j
               for (i, j), v in poly.terms.items() if v)
    return S.Poly(S.expand(expr), q, P)


def symbolic_labels(Bx, Cx, basis, depth):
    Dx, T3x, T5x = M.chart_operators(Bx, Cx)
    keys = set()
    for g in basis:
        current = g
        for i in range(1, depth + 1):
            current = Dx(current)
            for name, op in (("3", T3x), ("5", T5x)):
                value = op(current)
                if value != 0:
                    keys.update((i, name) + mon for mon in S.Poly(value, q, P).monoms())
    return sorted(keys, key=str)


rnd = random.Random(20261114)
with open("CUBE_LEADING_REFINEMENT_CERTIFICATE.json") as handle:
    certificate = json.load(handle)
report = {"minor_point_checks": {}, "ledger": []}
for entry in certificate:
    Bx, Cx = S.sympify(entry["B"], locals=names), S.sympify(entry["C"], locals=names)
    params = [names[s] for s in entry["parameters"]]
    basis = M.static_window_basis(Bx, Cx, M.chart_window())
    labels = symbolic_labels(Bx, Cx, basis, entry["depth"])
    index = {key: n for n, key in enumerate(labels)}
    assert M.depth_matrix(Bx, Cx, basis, 1, entry["depth"]).rows == len(labels)
    checked = 0
    for _ in range(3):
        point = {s: S.Rational(rnd.randint(-9, 9), rnd.randint(1, 5)) for s in params}
        ham = to_flat((P**3 + Bx*P + Cx).subs(point))
        matrix = S.zeros(len(labels), len(basis))
        for col, g in enumerate(basis):
            current = to_flat(g.subs(point))
            for depth in range(1, entry["depth"] + 1):
                current = transvectant(ham, current, 1)
                for order in (3, 5):
                    gate = transvectant(ham, current, order)
                    if any(gate.terms.values()):
                        for mon, cf in to_chart(gate).terms():
                            matrix[index[(depth, str(order)) + mon], col] = cf
        for minor in entry["minors"]:
            sub = matrix.extract(minor["rows"], minor["cols"])
            det = DomainMatrix.from_Matrix(sub).det()
            det = det.element if hasattr(det, "element") else det
            stored = S.sympify(minor["det"], locals=names).subs(point)
            assert S.Rational(str(det)) == stored, (entry["name"], point)
            checked += 1
    report["minor_point_checks"][entry["name"]] = checked
    print("%-42s %d minor evaluations agree with PerfectJet" % (entry["name"], checked), flush=True)

with open("CUBE_LEADING_REFINEMENT_REPLAY.json") as handle:
    ledger = json.load(handle)["ledger"]
monomials = M.window(12)
for row in ledger:
    ham = Poly(M.reduced_hamiltonian(tuple(row["b"]), tuple(row["c"])))
    expected = row.get("dims_S0_to_S3") or [None] + row["dims_S1_to_S3"]
    columns = []
    for monomial in monomials:
        current, column = Poly({monomial: 1}), {}
        for depth in range(len(expected)):
            for order in (3, 5):
                for mon, value in transvectant(ham, current, order).terms.items():
                    if value:
                        column[(depth, order) + mon] = S.Rational(Fraction(value))
            if depth + 1 < len(expected):
                current = transvectant(ham, current, 1)
        columns.append(column)
    keys = sorted({key for column in columns for key in column})
    dims = []
    for depth, dimension in enumerate(expected):
        rows = [key for key in keys if key[0] <= depth]
        dm = DomainMatrix.from_Matrix(S.Matrix([[column.get(key, 0) for column in columns] for key in rows])).to_field()
        dims.append(len(monomials) - dm.rank())
        if dimension is not None:
            assert dims[-1] == dimension, (row["member"], depth, dims[-1])
    report["ledger"].append({"member": row["member"], "perfectjet_window_dimensions": dims})
    print("%-36s %s" % (row["member"], dims), flush=True)

with open("CUBE_LEADING_REFINEMENT_PERFECTJET_REPLAY.json", "w") as handle:
    json.dump(report, handle, indent=1)
    handle.write("\n")
print("PerfectJet replay of the refinement certificates: PASS")
