"""Explicit partner bases at the exceptional loci of the family
H_a = q^6 + a q^3 p^3 + p^6 found by family_partners.py:

  rational loci:  n = 3, a = +-20 (dim 1 each; a = 0 gives dim 2,
                  already tabulated);
                  n = 5, a = +-40/7 (dim 1 each);
  quadratic loci: n = 4, a^2 = -50 (dim 3 over Q(sqrt(-50)));
                  n = 14, a^2 = -50 (dim 1);
                  n = 12, a^2 = -5 (dim 1 over Q(sqrt(-5))).

Algebraic bases are computed by the charge-blocked system over the
number field Q[t]/(f) and then VERIFIED by a field-valued
transvectant computation: with coefficients in K = Q[t]/(f), the
gates T_3(H_a, G) and T_5(H_a, G) are recomputed from scratch and
must vanish identically.  Rational bases are verified by the rational
gate machinery (and cross-checked against two other engines in
cross_checks.py).
"""

import json
import sys
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import sextic_lib as S
import family_partners as FP


# -------------------------------------------- field-valued polynomials
# A K-poly is a dict (c, e) -> element of K (tuple of Fractions).

def k_clean(p):
    return {k: v for k, v in p.items() if v}

def k_add(K, *ps):
    out = {}
    for p in ps:
        for k, v in p.items():
            out[k] = K.add(out.get(k, ()), v)
    return k_clean(out)

def k_scale(K, p, s):
    return k_clean({k: K.mul(v, s) for k, v in p.items()})

def k_mul(K, a, b):
    out = {}
    for (c1, e1), v1 in a.items():
        for (c2, e2), v2 in b.items():
            k = (c1 + c2, e1 + e2)
            out[k] = K.add(out.get(k, ()), K.mul(v1, v2))
    return k_clean(out)

def k_deriv(K, p, dq, dp):
    out = {}
    for (c, e), v in p.items():
        if c < dq or e < dp:
            continue
        coef = K.mul(v, (Fraction(S.falling(c, dq) * S.falling(e, dp)),))
        k = (c - dq, e - dp)
        out[k] = K.add(out.get(k, ()), coef)
    return k_clean(out)

def k_transvectant(K, F, G, k):
    from math import comb
    out = {}
    for j in range(k + 1):
        left = k_deriv(K, F, k - j, j)
        right = k_deriv(K, G, j, k - j)
        if left and right:
            s = (Fraction((-1) ** j * comb(k, j)),)
            out = k_add(K, out, k_scale(K, k_mul(K, left, right), s))
    return out


def field_kernel(K, n):
    """Partner basis of H_t over K in degree n, via charge blocks."""
    t = (Fraction(0), Fraction(1)) if K.deg >= 2 else (Fraction(0),)
    H = {(6, 0): (Fraction(1),), (3, 3): t, (0, 6): (Fraction(1),)}
    basis = []
    for cls in range(6):
        mons, rows = FP.affine_block(n, cls)
        if not mons:
            continue
        mat = [[S.p_trim((c0, c1)) for (c0, c1) in row] for row in rows]
        rk, bvecs = K.nullspace(mat, len(mons))
        for vec in bvecs:
            basis.append({m: v for v, m in zip(vec, mons) if v})
    # verify with field-valued transvectants
    for G in basis:
        for k in S.GATES:
            assert k_transvectant(K, H, G, k) == {}, (n, k)
    return basis


def kpoly_str(K, p):
    parts = []
    for (c, e), v in sorted(p.items()):
        t = ""
        if c:
            t += f"q^{c}" if c > 1 else "q"
        if e:
            t += f"p^{e}" if e > 1 else "p"
        if not t:
            t = "1"
        parts.append(f"({K.elem_str(v)})*{t}")
    return " + ".join(parts) if parts else "0"


def main():
    results = {"rational": {}, "algebraic": {}}

    for a0 in [Fraction(20), Fraction(-20)]:
        H = S.add(FP.H0, S.scale(FP.H1, a0))
        basis = S.partner_kernel(H, 3)
        assert len(basis) == 1
        results["rational"][f"n=3, a={a0}"] = {
            "dim": 1, "basis": [S.fmt(S.primitive(b)) for b in basis]}
        print(f"n=3, a={a0}: {[S.fmt(S.primitive(b)) for b in basis]}")
    for a0 in [Fraction(40, 7), Fraction(-40, 7)]:
        H = S.add(FP.H0, S.scale(FP.H1, a0))
        basis = S.partner_kernel(H, 5)
        assert len(basis) == 1
        results["rational"][f"n=5, a={a0}"] = {
            "dim": 1, "basis": [S.fmt(S.primitive(b)) for b in basis]}
        print(f"n=5, a={a0}: {[S.fmt(S.primitive(b)) for b in basis]}")

    for f, ns in [((Fraction(50), Fraction(0), Fraction(1)), (4, 14)),
                  ((Fraction(5), Fraction(0), Fraction(1)), (12,))]:
        K = S.NumberField(f)
        for n in ns:
            basis = field_kernel(K, n)
            strs = [kpoly_str(K, b) for b in basis]
            results["algebraic"][f"n={n}, a^2 = {-f[0]}"] = {
                "field": f"Q[t]/(t^2 + {f[0]})", "dim": len(basis),
                "basis": strs}
            print(f"n={n}, a^2={-f[0]}: dim {len(basis)}")
            for s in strs:
                print("   ", s)

    out = HERE / "exceptional_bases.json"
    out.write_text(json.dumps(results, indent=2, ensure_ascii=False))
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
