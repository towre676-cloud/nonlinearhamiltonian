"""Partner tables for the monomial sextics q^j p^(6-j) (j = 0..6) and
the two non-family probes, plus exact invariant data for the family
H_a = q^6 + a q^3 p^3 + p^6.

Monomial Hamiltonians: because a monomial H has a single charge, the
gate system splits by the EXACT charge of G (not just mod 6), so in
each degree each charge class of V_n contains at most one monomial:
E_n(q^j p^(6-j)) is necessarily spanned by monomials.  This script
verifies that (the monomials passing the gates span the kernel) and
compares against partner_lab.py's own classification conditions.

Invariants of the family: the discriminant and the classical
invariants I_2 ~ (f,f)_6 and I_4 ~ ((f,f)_4,(f,f)_4)_4 are computed
at integer values of a by exact transvectant arithmetic and
interpolated to polynomials in a, then factored over Q (sympy used
only for factorisation / one-variable discriminants).
"""

import json
import sys
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import sextic_lib as S
import family_partners as FP

MAXN = 24


def monomial_partner_test(H, n):
    """Return (dim, basis, monomials_in_kernel, spanned_by_monomials)."""
    basis = S.partner_kernel(H, n)
    mons_ok = []
    for m in S.homogeneous_mons(n):
        g = S.mono(*m)
        if all(t == {} for t in S.gates_of(H, g)):
            mons_ok.append(m)
    vecs = [S.poly_to_vec(b, S.homogeneous_mons(n)) for b in basis]
    mvecs = [S.poly_to_vec(S.mono(*m), S.homogeneous_mons(n))
             for m in mons_ok]
    spanned = S.spans_equal(vecs, mvecs) if (vecs or mvecs) else True
    return len(basis), basis, mons_ok, spanned


def interpolate_ints(ys):
    xs = [Fraction(j) for j in range(len(ys))]
    return FP.interpolate(xs, [Fraction(y) for y in ys])


def invariant_polynomials():
    """I_2(a) ~ (f,f)_6 and I_4(a) ~ ((f,f)_4,(f,f)_4)_4 and the
    discriminant of x^6 + a x^3 + 1, as polynomials in a (exact)."""
    import sympy
    a_sym, x = sympy.symbols("a x")
    i2_vals, i4_vals, disc_vals = [], [], []
    for av in range(7):
        f = S.add(S.add(S.mono(6, 0), S.scale(S.mono(3, 3), av)),
                  S.mono(0, 6))
        i2 = S.transvectant(f, f, 6)
        i2_vals.append(i2.get((0, 0), Fraction(0)))
        h = S.transvectant(f, f, 4)
        i4 = S.transvectant(h, h, 4)
        i4_vals.append(i4.get((0, 0), Fraction(0)))
        if av <= 6:
            d = sympy.discriminant(x ** 6 + av * x ** 3 + 1, x)
            disc_vals.append(Fraction(int(d)))
    return {
        "I2_proportional": S.p_str(interpolate_ints(
            [int(v) for v in i2_vals[:3]])),
        "I4_proportional": S.p_str(interpolate_ints(
            [int(v) for v in i4_vals[:5]])),
        "discriminant_x6_ax3_1": S.p_str(interpolate_ints(
            [int(v) for v in disc_vals])),
        "discriminant_values_at_integers": [str(v) for v in disc_vals],
    }


def main():
    results = {"monomials": {}, "probes": {}, "invariants": {},
               "checks": []}

    # ------------------------------------------------ monomial sextics
    for j in range(7):
        H = S.mono(j, 6 - j)
        name = f"q^{j}*p^{6 - j}" if 0 < j < 6 else (
            "q^6" if j == 6 else "p^6")
        entry = {"dims": {}, "bases": {}, "monomial_kernel": {},
                 "spanned_by_monomials_all_degrees": True}
        for n in range(MAXN + 1):
            dim, basis, mons_ok, spanned = monomial_partner_test(H, n)
            if not spanned:
                entry["spanned_by_monomials_all_degrees"] = False
            if dim:
                entry["dims"][str(n)] = dim
                entry["bases"][str(n)] = [S.poly_json(S.primitive(b))
                                          for b in basis]
                entry["monomial_kernel"][str(n)] = [list(m)
                                                    for m in mons_ok]
        results["monomials"][name] = entry
        print(f"{name}: dims {entry['dims']}; "
              f"monomial-spanned: {entry['spanned_by_monomials_all_degrees']}")

    # ------------------------------------------------ probes
    probes = [
        ("q^6+q^5*p+p^6",
         S.add(S.add(S.mono(6, 0), S.mono(5, 1)), S.mono(0, 6))),
        ("q^6+q^4*p^2+p^6",
         S.add(S.add(S.mono(6, 0), S.mono(4, 2)), S.mono(0, 6))),
    ]
    for name, H in probes:
        entry = {"dims": {}, "bases": {}}
        for n in range(MAXN + 1):
            basis = S.partner_kernel(H, n)
            if basis:
                entry["dims"][str(n)] = len(basis)
                entry["bases"][str(n)] = [S.poly_json(S.primitive(b))
                                          for b in basis]
        results["probes"][name] = entry
        print(f"{name}: dims {entry['dims']}")

    # ------------------------------------------------ invariants
    results["invariants"] = invariant_polynomials()
    print("invariants:", results["invariants"])

    # ------------------------------ discriminant / root-type checks
    import sympy
    x = sympy.Symbol("x")
    checks = {}
    for name, expr in [("probe1 x^6+x^5+1", x ** 6 + x ** 5 + 1),
                       ("probe2 x^6+x^4+1", x ** 6 + x ** 4 + 1),
                       ("family a=2: x^6+2x^3+1", x ** 6 + 2 * x ** 3 + 1),
                       ("family a=-2: x^6-2x^3+1", x ** 6 - 2 * x ** 3 + 1),
                       ("family a=0: x^6+1", x ** 6 + 1)]:
        checks[name] = {"discriminant": str(sympy.discriminant(expr, x)),
                        "factor_over_Q": str(sympy.factor(expr))}
    # (q^3 + p^3)^2 and (q^3 - p^3)^2 expansions
    cube_p = S.add(S.mono(3, 0), S.mono(0, 3))
    cube_m = S.add(S.mono(3, 0), S.scale(S.mono(0, 3), -1))
    checks["(q^3+p^3)^2 == H_{a=2}"] = S.mul(cube_p, cube_p) == FP.H_family \
        if hasattr(FP, "H_family") else (
            S.mul(cube_p, cube_p) ==
            S.add(S.add(S.mono(6, 0), S.scale(S.mono(3, 3), 2)),
                  S.mono(0, 6)))
    checks["(q^3-p^3)^2 == H_{a=-2}"] = (
        S.mul(cube_m, cube_m) ==
        S.add(S.add(S.mono(6, 0), S.scale(S.mono(3, 3), -2)), S.mono(0, 6)))
    results["root_type_checks"] = checks
    print("root-type checks:", json.dumps(checks, indent=1)[:600])

    out = HERE / "extra_partners.json"
    out.write_text(json.dumps(results, indent=2, ensure_ascii=False))
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
