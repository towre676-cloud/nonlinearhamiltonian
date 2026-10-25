"""Partner kernels for the interpolating sextic family
    H_a = q^6 + a q^3 p^3 + p^6,   a in Q (and loci over Qbar).

Method (see sextic_lib.py for conventions):
  * The gate system on V_n (unknowns: the n+1 monomials q^c p^(n-c))
    has entries affine in a: M_n(a) = M_n^(0) + a M_n^(1), from
    H_a = H_0 + a H_1 with H_0 = q^6 + p^6, H_1 = q^3 p^3.
  * Charge (c - e) mod 6 splits the system into independent blocks,
    because every monomial of H_a has charge == 0 (mod 6) and the
    transvectants are charge-additive.  Block membership is asserted
    entry-by-entry during assembly.
  * GENERIC structure: exact nullspace over Q(a) per block, using
    rational-function Gauss-Jordan (sextic_lib.nullspace_rf).
  * EXCEPTIONAL loci: for each block of generic rank rho, one nonzero
    rho x rho minor mu(a) is computed exactly (its determinant as a
    polynomial in a, by evaluation + Lagrange interpolation).  The
    rank of the block can drop at a only where mu(a) = 0, since the
    drop locus is the zero set of the gcd of ALL maximal minors and
    that gcd divides mu.  Every irreducible factor of every mu is
    then tested exactly: rational roots by rational specialization,
    higher-degree factors by exact linear algebra over Q[t]/(factor).
    At each candidate locus EVERY block is re-evaluated in that
    field, so the reported total dimension there is exact.
  * SPECIALIZATIONS at rational a: dimensions by blocked rational
    linear algebra, cross-checked against the unblocked system;
    bases by the unblocked exact kernel.

Output: family_partners.json.  Exact rational arithmetic throughout;
sympy is used only to factor the minor polynomials over Q.
"""

import json
import sys
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import sextic_lib as S

H0 = S.add(S.mono(6, 0), S.mono(0, 6))     # q^6 + p^6
H1 = S.mono(3, 3)                          # q^3 p^3

MAXN_SYMBOLIC = 30       # generic/exceptional analysis degrees 0..30
MAXN_BASIS = 20          # explicit bases (generic and specialized)
A_LIST = [Fraction(x) for x in
          (0, "1/2", "-1/2", 1, -1, 2, -2, 3, -3, "3/2", "-3/2",
           "5/2", "-5/2", "2/3", "-2/3", "1/3", "-1/3", 4, -4, 5, -5)]


def charge(m):
    return m[0] - m[1]


def affine_block(n, cls):
    """Block of the gate system on V_n for charge class cls (mod 6).
    Returns (mons_in, rows) with rows of (c0, c1) Fraction pairs:
    entry(a) = c0 + c1 * a."""
    mons = [m for m in S.homogeneous_mons(n) if charge(m) % 6 == cls]
    rows = []
    for k in S.GATES:
        cols = []
        for m in mons:
            g0 = S.transvectant(H0, S.mono(*m), k)
            g1 = S.transvectant(H1, S.mono(*m), k)
            cols.append((g0, g1))
        keys = sorted({key for g0, g1 in cols for key in g0} |
                      {key for g0, g1 in cols for key in g1})
        for key in keys:
            if charge(key) % 6 != cls:
                # structural assertion: no leakage between blocks
                assert all(g0.get(key, 0) == 0 and g1.get(key, 0) == 0
                           for g0, g1 in cols), (n, cls, key)
                continue
            rows.append([(g0.get(key, Fraction(0)), g1.get(key, Fraction(0)))
                         for g0, g1 in cols])
    return mons, rows


def block_at_a(rows, a0):
    return [[c0 + c1 * a0 for (c0, c1) in row] for row in rows]


def rank_profile(rows, ncols):
    """Gauss-Jordan over Q on a numeric matrix; returns
    (rank, pivot_row_indices, pivot_cols)."""
    mat = [list(r) for r in rows]
    idx = list(range(len(rows)))
    pivots_rows, pivots_cols = [], []
    r = 0
    for c in range(ncols):
        piv = next((i for i in range(r, len(mat)) if mat[i][c] != 0), None)
        if piv is None:
            continue
        mat[r], mat[piv] = mat[piv], mat[r]
        idx[r], idx[piv] = idx[piv], idx[r]
        pv = mat[r][c]
        mat[r] = [x / pv for x in mat[r]]
        for i in range(len(mat)):
            if i != r and mat[i][c] != 0:
                f = mat[i][c]
                mat[i] = [x - f * y for x, y in zip(mat[i], mat[r])]
        pivots_rows.append(idx[r])
        pivots_cols.append(c)
        r += 1
        if r >= len(mat):
            break
    return len(pivots_cols), pivots_rows, pivots_cols


def det_numeric(mat):
    n = len(mat)
    mat = [list(r) for r in mat]
    det = Fraction(1)
    for c in range(n):
        piv = next((i for i in range(c, n) if mat[i][c] != 0), None)
        if piv is None:
            return Fraction(0)
        if piv != c:
            mat[c], mat[piv] = mat[piv], mat[c]
            det = -det
        det *= mat[c][c]
        pv = mat[c][c]
        mat[c] = [x / pv for x in mat[c]]
        for i in range(c + 1, n):
            if mat[i][c] != 0:
                f = mat[i][c]
                mat[i] = [x - f * y for x, y in zip(mat[i], mat[c])]
    return det


def interpolate(xs, ys):
    """Lagrange interpolation over Q; returns ascending Fraction tuple."""
    out = ()
    for i, (xi, yi) in enumerate(zip(xs, ys)):
        num = (Fraction(1),)
        den = Fraction(1)
        for j, xj in enumerate(xs):
            if i == j:
                continue
            num = S.p_mul(num, (-xj, Fraction(1)))
            den *= (xi - xj)
        out = S.p_add(out, S.p_scale(num, yi / den))
    return out


def minor_polynomial(rows, prow, pcol):
    rho = len(pcol)
    xs = [Fraction(j) for j in range(rho + 1)]
    ys = []
    for x in xs:
        mat = block_at_a(rows, x)
        sub = [[mat[i][j] for j in pcol] for i in prow]
        ys.append(det_numeric(sub))
    return interpolate(xs, ys)


def block_generic(n, cls):
    """Generic (over Q(a)) rank and nullspace basis of one block."""
    mons, rows = affine_block(n, cls)
    ncols = len(mons)
    if ncols == 0:
        return mons, rows, 0, []
    rf_rows = [[S.rf((c0, c1)) for (c0, c1) in row] for row in rows]
    rk, basis = S.nullspace_rf(rf_rows, ncols)
    return mons, rows, rk, basis


def factor_list_q(poly):
    """Distinct irreducible factors of a polynomial in a over Q,
    via sympy (used only for factorisation)."""
    import sympy
    a = sympy.Symbol("a")
    expr = sum(sympy.Rational(c.numerator, c.denominator) * a ** i
               for i, c in enumerate(poly))
    if expr == 0:
        return []
    fac = sympy.factor_list(expr, a)
    out = []
    for f_expr, _mult in fac[1]:
        fpoly = sympy.Poly(f_expr, a)
        coeffs = []
        for i in range(fpoly.degree() + 1):
            c = fpoly.nth(i)
            coeffs.append(Fraction(c.p, c.q))
        coeffs = S.p_trim(coeffs)
        lc = coeffs[-1]                      # normalize to monic
        out.append(tuple(c / lc for c in coeffs))
    return out


def block_nullity_at_locus(rows, ncols, locus):
    """Exact nullity of one block at an algebraic locus.
    locus is None for generic (handled elsewhere), or
    ('rat', a0) or ('field', NumberField)."""
    kind, val = locus
    if kind == "rat":
        mat = block_at_a(rows, val)
        return ncols - S.rank_of(mat)
    K = val
    mat = [[S.p_trim((c0, c1)) for (c0, c1) in row] for row in rows]
    rk, _ = K.nullspace(mat, ncols)
    return ncols - rk


def main():
    results = {
        "family": "H_a = q^6 + a*q^3*p^3 + p^6",
        "method": ("charge-mod-6 blocked gate system (T_3, T_5), entries "
                   "affine in a; generic nullspace over Q(a) by exact "
                   "rational-function Gauss-Jordan; exceptional loci from "
                   "maximal-minor factors, each tested by exact linear "
                   "algebra over Q or over Q[t]/(factor)"),
        "degrees": {},
        "specializations": {},
        "checks": [],
    }
    checks = results["checks"]

    # ------------------------------------------ generic + exceptional
    for n in range(MAXN_SYMBOLIC + 1):
        blocks = []
        total_generic_dim = 0
        candidate_factors = {}   # factor tuple -> True (collect all)
        for cls in range(6):
            mons, rows, rk, basis = block_generic(n, cls)
            ncols = len(mons)
            if ncols == 0:
                continue
            gdim = ncols - rk
            total_generic_dim += gdim
            entry = {"class": cls, "mons": mons, "ncols": ncols,
                     "rank": rk, "generic_dim": gdim, "basis_rf": basis,
                     "rows": rows}
            if 0 < rk:
                # one nonzero maximal minor, from a generic test point
                test = block_at_a(rows, Fraction(1000))
                rk2, prow, pcol = rank_profile(test, ncols)
                assert rk2 == rk, (n, cls, rk2, rk)
                mu = minor_polynomial(rows, prow, pcol)
                assert any(mu), (n, cls)
                entry["minor"] = mu
                for f in factor_list_q(mu):
                    candidate_factors[f] = True
            blocks.append(entry)
        # evaluate every candidate locus exactly, all blocks
        exceptional = []
        for f in sorted(candidate_factors, key=lambda p: (len(p), p)):
            if len(f) == 2:      # linear: rational root
                a0 = -f[0] / f[1]
                locus = ("rat", a0)
                name = f"a = {a0}"
            else:
                locus = ("field", S.NumberField(f))
                name = f"root of ({S.p_str(f)}) = 0"
            total = 0
            per_block = []
            for entry in blocks:
                d = block_nullity_at_locus(entry["rows"], entry["ncols"],
                                            locus)
                per_block.append(d)
                total += d
            if total > total_generic_dim:
                exceptional.append({
                    "locus": name,
                    "factor": [str(c) for c in f],
                    "total_dim": total,
                    "per_block_dims": per_block,
                })
        deg_entry = {
            "generic_dim": total_generic_dim,
            "exceptional": exceptional,
            "blocks": [
                {"charge_class_mod_6": e["class"],
                 "monomials": [list(m) for m in e["mons"]],
                 "rank": e["rank"], "generic_dim": e["generic_dim"],
                 "minor_polynomial_in_a":
                     S.p_str(e["minor"]) if "minor" in e else None}
                for e in blocks],
        }
        if n <= MAXN_BASIS:
            basis_desc = []
            for e in blocks:
                for vec in e["basis_rf"]:
                    terms = []
                    for val, m in zip(vec, e["mons"]):
                        if not S.rf_is_zero(val):
                            terms.append({"q": m[0], "p": m[1],
                                          "coefficient": S.rf_str(val)})
                    basis_desc.append(terms)
            deg_entry["generic_basis"] = basis_desc
        results["degrees"][str(n)] = deg_entry
        exc = "; ".join(f"{x['locus']}: dim {x['total_dim']}"
                        for x in exceptional)
        print(f"n={n:2d} generic dim {total_generic_dim}"
              + (f"  EXCEPTIONAL {exc}" if exc else ""))

    # ------------------------------------------ specializations
    for a0 in A_LIST:
        H = S.add(H0, S.scale(H1, a0))
        dims = {}
        bases = {}
        for n in range(MAXN_SYMBOLIC + 1):
            # blocked dimension (all H_a charges are 0 mod 6)
            tot = 0
            for cls in range(6):
                mons, rows, rk, _ = block_generic(n, cls)
                mat = block_at_a(rows, a0)
                tot += len(mons) - S.rank_of(mat)
            d_full = S.partner_dim(H, n)
            assert tot == d_full, (a0, n, tot, d_full)
            dims[str(n)] = d_full
            if n <= MAXN_BASIS and d_full:
                bases[str(n)] = [S.poly_json(S.primitive(b))
                                 for b in S.partner_kernel(H, n)]
        results["specializations"][str(a0)] = {"dims": dims, "bases": bases}
        nz = {n: d for n, d in dims.items() if d}
        print(f"a={a0}: nonzero dims {nz}")
    checks.append(
        "blocked (charge mod 6) dimensions equal unblocked dimensions "
        "for every (a, n) in the specialization grid: asserted in code")

    # generic dims must agree with specializations off the exceptional loci
    exc_rational = set()
    for n, de in results["degrees"].items():
        for x in de["exceptional"]:
            if x["factor"] and len(x["factor"]) == 2:
                f = [Fraction(c) for c in x["factor"]]
                exc_rational.add(-f[0] / f[1])
    for a0 in A_LIST:
        if a0 in exc_rational:
            continue
        for n in range(MAXN_SYMBOLIC + 1):
            gd = results["degrees"][str(n)]["generic_dim"]
            sd = results["specializations"][str(a0)]["dims"][str(n)]
            assert gd == sd, (a0, n, gd, sd)
    checks.append(
        "generic Q(a) dimension equals the specialized dimension at "
        "every non-exceptional rational point of the grid: asserted")

    out = HERE / "family_partners.json"
    out.write_text(json.dumps(results, indent=2, ensure_ascii=False))
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
