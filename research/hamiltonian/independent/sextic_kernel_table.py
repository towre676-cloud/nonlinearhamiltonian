"""Computed homogeneous partner kernels for three sextic Hamiltonians.

This is a computed table, not a general classification proof.
Each entry was computed with the independent checker in
moyal_partner_checker.py (exact rational nullspace of the
D^(2m+1) = 0 equations, m >= 1) and, where stated in the
accompanying report, cross-checked against the repository
partner_lab.py kernel command.

Scope: homogeneous polynomials G of total degree d, H homogeneous
of degree 6, flat Weyl-Moyal convention, hbar-independent G.

Run with: python3 sextic_kernel_table.py
It writes sextic_kernel_table.json beside itself.
"""

import json
from pathlib import Path

from moyal_partner_checker import monomial, add, homogeneous_kernel

HERE = Path(__file__).resolve().parent

HAMILTONIANS = {
    "q^6+p^6": add(monomial(6, 0), monomial(0, 6)),
    "q^3*p^3": monomial(3, 3),
    "q^6+q^3*p^3+p^6": add(add(monomial(6, 0), monomial(3, 3)), monomial(0, 6)),
}


def main(max_degree=30):
    table = {}
    for name, h in HAMILTONIANS.items():
        entries = []
        for degree in range(max_degree + 1):
            basis = homogeneous_kernel(h, degree)
            if basis:
                entries.append(
                    {
                        "degree": degree,
                        "dimension": len(basis),
                        "basis": [
                            [{"q": a, "p": b, "coefficient": str(c)} for (a, b), c in sorted(poly.items())]
                            for poly in basis
                        ],
                    }
                )
        table[name] = entries
        print(f"{name}: nonzero degrees: {[e['degree'] for e in entries]}")
    out = HERE / "sextic_kernel_table.json"
    with open(out, "w") as f:
        json.dump(table, f, indent=2)
    print(f"wrote {out.name}")


if __name__ == "__main__":
    main()
