"""Additional independent checks for the reviewed cube-leading package.

Require PerfectJet (installed or through PERFECTJET_SRC). Build every iterated
gate directly with PerfectJet in the original q,p coordinates, then obtain
exact ranks with SymPy's DomainMatrix, independently of the local flat gate
and Fraction row-reduction engines. These point checks become all-degree
statements only in conjunction with the manuscript's uniform tail theorem.
"""
import hashlib
import json
import os
import sys
from fractions import Fraction

import sympy as S
from sympy.polys.matrices import DomainMatrix

import cube_leading_boundary as M

if os.environ.get("PERFECTJET_SRC"):
    sys.path.insert(0, os.environ["PERFECTJET_SRC"])
from perfectjet.polynomial import Poly
from perfectjet.transvectants import transvectant


def point_certificate(b, c, expected):
    ham = Poly(M.reduced_hamiltonian(b, c))
    monomials = M.window(12)
    columns = []
    for monomial in monomials:
        current = Poly({monomial: 1})
        column = {}
        for depth in range(len(expected)):
            for order in (3, 5):
                for mon, value in transvectant(ham, current, order).terms.items():
                    if value:
                        column[(depth, order) + mon] = S.Rational(Fraction(value))
            if depth + 1 < len(expected):
                current = transvectant(ham, current, 1)
        columns.append(column)
    labels = sorted({key for column in columns for key in column})
    result = []
    for depth, dimension in enumerate(expected):
        rows = [key for key in labels if key[0] <= depth]
        matrix = S.Matrix([[column.get(key, 0) for column in columns] for key in rows])
        dm = DomainMatrix.from_Matrix(matrix).to_field()
        _, pivot_columns = dm.rref()
        _, pivot_rows = dm.transpose().rref()
        assert len(monomials) - len(pivot_columns) == dimension
        minor = matrix.extract(list(pivot_rows), list(pivot_columns))
        determinant = DomainMatrix.from_Matrix(minor).det()
        assert determinant != 0
        kernel = matrix.nullspace()
        assert len(kernel) == dimension
        assert all(matrix * vector == S.zeros(matrix.rows, 1) for vector in kernel)
        encoded = json.dumps([[str(v) for v in row] for row in matrix.tolist()], separators=(",", ":"))
        result.append({"depth": depth, "dimension": dimension,
                       "matrix_shape": list(matrix.shape),
                       "matrix_sha256": hashlib.sha256(encoded.encode()).hexdigest(),
                       "minor_rows": list(pivot_rows), "minor_columns": list(pivot_columns),
                       "minor_determinant": str(determinant),
                       "kernel": [[str(v) for v in vector] for vector in kernel]})
    return result


def check_symbolic_bases():
    # Rule out parameter denominators before using a symbolic nullspace as a
    # basis at every specialization, including singular parameter values.
    q, P = M.q, M.P
    gamma, b0 = S.symbols("gamma b0")
    cases = [(q, gamma*q**3), (q, -q**3), (b0, q**3), (b0 + q**2, gamma*q**3)]
    for B, C in cases:
        if B == q and C == -q**3:
            basis = [P**k for k in range(7)] + M.static_window_basis(B, C, M.chart_window(3, 8, True))
        else:
            basis = M.static_window_basis(B, C, M.chart_window())
        assert len(basis) == 15
        for g in basis:
            S.Poly(g, P, q, gamma, b0, domain=S.QQ)
        assert {S.Poly(g, P, q).LC() for g in basis} == {1}
        assert len({S.Poly(g, P, q).monoms()[0] for g in basis}) == 15
    return len(cases)


if __name__ == "__main__":
    report = {"symbolic_bases_without_parameter_denominators": check_symbolic_bases()}
    cases = [
        ("generic", (2, -1, 3, 5), (1, 4, -2, 7, 3, -6), [14, 2]),
        ("coupled", (0, 2, 0, 0), (0, 3, 5, 0, 0, 0), [15, 4, 3, 2]),
        ("older_cubic_phase_overlap", (0, 0, Fraction(-1, 3), 0),
         (0, 0, 0, Fraction(2, 27), 0, 0), [15, 3, 2]),
        ("quadratic_stratum", (1, 0, 1, 0), (0, 2, 3, 4, 0, 0), [15, 3, 2]),
    ]
    for name, b, c, expected in cases:
        report[name] = point_certificate(b, c, expected)
        print(name, expected, "PASS", flush=True)
    with open("CUBE_LEADING_REVIEW_CERTIFICATE.json", "w") as handle:
        json.dump(report, handle, indent=1)
        handle.write("\n")
    print("independent iterated-gate review: PASS")
