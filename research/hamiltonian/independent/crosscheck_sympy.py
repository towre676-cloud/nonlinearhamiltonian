#!/usr/bin/env python3
"""Independent cross-checks with sympy (a genuinely separate
implementation: sympy differentiation and sympy rational linear
algebra; none of the Fraction/Quad engine of quartic_cores_ext.py is
used to build or solve these systems).

Checks, all against quartic_cores_ext.json / inhomogeneous_cores.json
produced by the main scripts:

  1. Homogeneous refinement dimensions dim S^R_n for samples of the
     seven homogeneous representatives and of the equianharmonic
     rational form q^4 + q p^3.
  2. The equianharmonic lambda form H_l, l^2 = -12, over Q(sqrt(-3)):
     the stacked matrix is built with a sympy symbol lam (entries in
     QQ[lam]); each entry P(lam) is then split as A + B sqrt(-3) via
     lam = 2 sqrt(-3), lam^2 = -12, and the K-nullity is recovered
     from the doubled rational system [[A, -3B], [B, A]]: a vector
     x = u + sqrt(-3) v (u, v rational) is killed by A + B sqrt(-3)
     iff Au - 3Bv = 0 and Bu + Av = 0, and the rational solution
     space of the doubled system has Q-dimension 2 * dim_K.
  3. Inhomogeneous truncated refinements K_R^{<=8} for
     H = q p^3 + q^2 and for the test case H = q^2 p^2 + q^2,
     R = 0..5, from sympy-built stacked matrices over QQ.
"""

from fractions import Fraction
from math import comb
from pathlib import Path
import json
import sys
import time

import sympy as sp

HERE = Path(__file__).resolve().parent
q, p, lam = sp.symbols("q p lam")

def T3(F, G):
    out = 0
    for j in range(4):
        out += ((-1) ** j) * comb(3, j) * \
            sp.diff(F, q, 3 - j, p, j) * sp.diff(G, q, j, p, 3 - j)
    return sp.expand(out)

def D(H, G):
    return sp.expand(sp.diff(H, q) * sp.diff(G, p)
                     - sp.diff(H, p) * sp.diff(G, q))

def coeff_rows(H, basis, R):
    """Stacked coefficient matrix (rows x basis) of T_3(H, D^r .) for
    r = 0..R, as a sympy Matrix over QQ[lam] (lam-free if H is)."""
    images = list(basis)
    rowdicts = []
    for r in range(R + 1):
        gated = [T3(H, im) for im in images]
        keys = set()
        per = []
        for g in gated:
            poly = sp.Poly(g, q, p)
            d = poly.as_dict() if poly is not None else {}
            per.append(d)
            keys.update(d)
        for k in sorted(keys):
            rowdicts.append([sp.expand(d.get(k, 0)) for d in per])
        images = [D(H, im) for im in images]
    if not rowdicts:
        return sp.zeros(0, len(basis))
    return sp.Matrix(rowdicts)

def dim_free_QQ(M):
    n = M.cols
    if M.rows == 0:
        return n
    return n - M.rank()

def dim_free_lambda(M):
    """Nullity over K = Q(sqrt(-3)) of a matrix with entries in
    QQ[lam], specialised at lam^2 = -12, lam = 2 sqrt(-3), via the
    doubled rational system."""
    n = M.cols
    if M.rows == 0:
        return n
    Arows, Brows = [], []
    for i in range(M.rows):
        Arow, Brow = [], []
        for j in range(n):
            e = sp.Poly(M[i, j], lam)
            A, B = sp.Rational(0), sp.Rational(0)
            for (k,), c in e.as_dict().items():
                if k % 2 == 0:
                    A += c * (-12) ** (k // 2)
                else:
                    B += 2 * c * (-12) ** ((k - 1) // 2)
            Arow.append(A)
            Brow.append(B)
        Arows.append(Arow)
        Brows.append(Brow)
    A = sp.Matrix(Arows)
    B = sp.Matrix(Brows)
    Z = sp.zeros(A.rows, n)
    doubled = sp.Matrix.vstack(sp.Matrix.hstack(A, -3 * B),
                               sp.Matrix.hstack(B, A))
    nullity2 = 2 * n - doubled.rank()
    assert nullity2 % 2 == 0
    return nullity2 // 2

def homog_basis(n):
    return [q ** (n - t) * p ** t for t in range(n + 1)]

def all_basis(N):
    return [q ** a * p ** b for d in range(N + 1)
            for a in range(d + 1) for b in [d - a]]

def main():
    t0 = time.time()
    ext = json.loads((HERE / "quartic_cores_ext.json").read_text())
    inh = json.loads((HERE / "inhomogeneous_cores.json").read_text())
    main_by_id = {c["id"]: c for c in ext["cases"]}
    inh_by_id = {c["id"]: c for c in inh["cases"]}
    out = {"checks": [], "all_agree": True}

    def record(kind, label, n, R, ours, main_value):
        ok = ours == main_value
        out["all_agree"] &= ok
        out["checks"].append({"kind": kind, "case": label, "n": n,
                              "R": R, "sympy_dim": ours,
                              "main_dim": main_value, "agree": ok})
        print(f"{kind} {label} n={n} R={R}: sympy={ours} "
              f"main={main_value} agree={ok}", flush=True)

    H_of = {
        "q4": q ** 4, "q3p": q ** 3 * p, "qp3": q * p ** 3,
        "q2p2": q ** 2 * p ** 2, "q4_p4": q ** 4 + p ** 4,
        "q4_q2p2_p4": q ** 4 + q ** 2 * p ** 2 + p ** 4,
        "q4_mq2p2_p4": q ** 4 - q ** 2 * p ** 2 + p ** 4,
    }
    samples = {
        "q4": [(2, 0), (7, 1), (24, 1)],
        "q3p": [(6, 0), (6, 1), (18, 0), (18, 1), (22, 1)],
        "qp3": [(10, 0), (10, 1), (24, 1)],
        "q2p2": [(9, 1), (16, 0), (16, 1)],
        "q4_p4": [(5, 1), (6, 0), (6, 1), (13, 1), (24, 1)],
        "q4_q2p2_p4": [(6, 1), (17, 1)],
        "q4_mq2p2_p4": [(6, 0), (6, 1), (20, 1)],
    }
    for cid, ss in samples.items():
        H = H_of[cid]
        for (n, R) in ss:
            M = coeff_rows(H, homog_basis(n), R)
            record("homogeneous", cid, n, R, dim_free_QQ(M),
                   main_by_id[cid]["refinement_dims_by_degree"]
                   [str(n)][R])

    # equianharmonic reading A (rational form) over QQ
    HA = q ** 4 + q * p ** 3
    eqA = ext["equianharmonic"]["reading_A_rational_form"]
    for (n, R) in [(1, 0), (1, 1), (1, 2), (1, 3), (3, 1), (3, 2),
                   (5, 1), (8, 1), (13, 1)]:
        M = coeff_rows(HA, homog_basis(n), R)
        record("equianharmonic_A", "q^4+qp^3", n, R, dim_free_QQ(M),
               eqA["refinement_dims_by_degree"][str(n)][R])

    # equianharmonic reading B (lambda form) over Q(sqrt(-3))
    HB = q ** 4 + lam * q ** 2 * p ** 2 + p ** 4
    eqB = ext["equianharmonic"]["reading_B_lambda_form"]
    for (n, R) in [(1, 0), (1, 2), (1, 3), (3, 1), (3, 2), (4, 1),
                   (6, 1)]:
        M = coeff_rows(HB, homog_basis(n), R)
        record("equianharmonic_B", "q^4+lam q^2p^2+p^4", n, R,
               dim_free_lambda(M),
               eqB["refinement_dims_by_degree"][str(n)][R])

    # inhomogeneous truncated refinements, deg <= 8
    for cid, HH in [("qp3_plus_q2", q * p ** 3 + q ** 2),
                    ("q2p2_plus_q2_TEST", q ** 2 * p ** 2 + q ** 2)]:
        basis = all_basis(8)
        for R in range(6):
            M = coeff_rows(HH, basis, R)
            record("inhomogeneous_deg<=8", cid, 8, R, dim_free_QQ(M),
                   inh_by_id[cid]["runs"]["8"]
                   ["refinement_dims_by_R"][R])

    print(f"\nALL AGREE: {out['all_agree']}  "
          f"({len(out['checks'])} checks, {time.time() - t0:.1f}s)")
    (HERE / "crosscheck_sympy.json").write_text(
        json.dumps(out, indent=2, ensure_ascii=False))
    print(f"wrote {HERE / 'crosscheck_sympy.json'}")
    return 0 if out["all_agree"] else 1

if __name__ == "__main__":
    sys.exit(main())
