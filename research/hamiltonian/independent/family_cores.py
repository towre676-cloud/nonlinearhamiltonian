"""Dynamic cores D_inf(H) for sextics, by refinement:

    S^R_n(H) = { G in V_n : T_k(H, D^r G) = 0, k in {3,5}, r = 0..R },
    D = {H, .}.   D_inf(H)_n is contained in S^R_n for every R, so
    dim S^R_n is a rigorous upper bound on dim D_inf(H)_n.

Certification scheme (exact, no floating point):
  * Low depths (R <= 2): dim S^R_n computed directly over Q.
  * All depths: for primes p not dividing any row denominator,
    rank_Q(rows) >= rank_{F_p}(rows mod p) (a minor nonzero mod p is
    a nonzero rational), hence
        dim D_inf(H)_n <= dim S^R_n <= (n+1) - max_p rank_p =: U_R.
    U_R is reported for every R.  As soon as U_R equals the dimension
    of an exhibited subspace of D_inf(H), the degree-n core is
    determined EXACTLY (the exhibited space is contained in D_inf,
    hence in S^R_n, and the bound matches).
  * Exhibited subspaces: span{1, H} needs no computation (the gates
    T_k(H,.) kill 1 and H: T_k(H,H) = 0 for odd k by antisymmetry,
    {H,H} = 0, {H,1} = 0).  For the monomial patterns of the
    repository's Theorem M the exhibited monomials are additionally
    verified in-script to be killed by both gates after D^r for
    r <= R_VERIFY.

Predictions tested (repository theorems W4 / M; not assumed):
  * family H_a, all a in the grid: D_inf = span{1, H} (root types
    (1^6), and (2,2,2) at a = +-2; all have >= 3 distinct roots).
  * monomials per Theorem M; probes span{1, H} (distinct roots).

Output: family_cores.json.
"""

import json
import sys
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import sextic_lib as S

NMAX = 16
RMAX = 12
R_Q = 2                      # depths computed directly over Q
R_VERIFY = 10
PRIMES = (1000003, 999983, 999979)

H0 = S.add(S.mono(6, 0), S.mono(0, 6))
H1 = S.mono(3, 3)


def H_family(a):
    return S.add(H0, S.scale(H1, a))


def rank_mod(rows, ncols, p):
    mat = []
    for row in rows:
        r = []
        for x in row:
            if x == 0:
                r.append(0)
            else:
                assert x.denominator % p != 0
                r.append((x.numerator % p) *
                         pow(x.denominator % p, -1, p) % p)
        mat.append(r)
    rk = 0
    for c in range(ncols):
        piv = next((i for i in range(rk, len(mat)) if mat[i][c] % p),
                   None)
        if piv is None:
            continue
        mat[rk], mat[piv] = mat[piv], mat[rk]
        inv = pow(mat[rk][c] % p, -1, p)
        mat[rk] = [(v * inv) % p for v in mat[rk]]
        for i in range(len(mat)):
            if i != rk and mat[i][c] % p:
                f = mat[i][c] % p
                mat[i] = [(a - f * b) % p for a, b in zip(mat[i], mat[rk])]
        rk += 1
        if rk >= len(mat):
            break
    return rk


def refinement_bounds(H, n, predicted_dim, exhibits):
    """Returns dict with exact low-R dims, U_R bounds, the first R at
    which U_R == predicted_dim (certification depth), and the exact
    basis of S^R_n at that depth when computed over Q cheaply."""
    mons = S.homogeneous_mons(n)
    images = [S.mono(c, e) for (c, e) in mons]
    rows = []
    exact_dims = []
    bounds = []
    cert_R = None
    basis_at_cert = None
    for r in range(RMAX + 1):
        for k in S.GATES:
            gated = [S.transvectant(H, im, k) for im in images]
            keys = sorted({key for g in gated for key in g})
            for key in keys:
                rows.append([g.get(key, Fraction(0)) for g in gated])
        if r <= R_Q:
            vecs = S.nullspace(rows, len(mons))
            exact_dims.append(len(vecs))
            if cert_R is None and len(vecs) == predicted_dim:
                cert_R = r
                basis_at_cert = [S.vec_to_poly(v, mons) for v in vecs]
        rk = max(rank_mod(rows, len(mons), p) for p in PRIMES)
        U = len(mons) - rk
        bounds.append(U)
        if cert_R is None and U == predicted_dim:
            cert_R = r
            # one exact computation at the certification depth
            vecs = S.nullspace(rows, len(mons))
            assert len(vecs) == predicted_dim, (n, r, len(vecs))
            basis_at_cert = [S.vec_to_poly(v, mons) for v in vecs]
        if cert_R is not None and r >= cert_R + 1:
            break
        images = [S.poisson(H, im) for im in images]
    return {"exact_dims_low_R": exact_dims, "upper_bounds_U_R": bounds,
            "certified_at_R": cert_R, "basis_at_certification":
            [S.fmt(S.primitive(b)) for b in basis_at_cert]
            if basis_at_cert else [],
            "basis_polys": basis_at_cert or []}


def verify_exhibits(H, exhibits):
    """Each exhibited poly must be killed by both gates after D^r,
    r = 0..R_VERIFY (a finite check of membership in D_inf's
    defining conditions; the all-r membership for span{1,H} is a
    proof, for monomial patterns it is the repository's Theorem M,
    and this is the in-range verification)."""
    for g in exhibits:
        img = g
        for r in range(R_VERIFY + 1):
            if any(t != {} for t in S.gates_of(H, img)):
                return False
            img = S.poisson(H, img)
    return True


def run_case(name, H, predicted, predicted_desc, exhibit_by_degree):
    entry = {"name": name, "H": S.fmt(H),
             "predicted_core": predicted_desc, "degrees": {},
             "all_degrees_certified": True,
             "exhibits_verified_to_R": R_VERIFY}
    finals = []
    for n in range(NMAX + 1):
        ex = exhibit_by_degree.get(n, [])
        assert len(ex) == predicted[n], (name, n)
        ok_ex = verify_exhibits(H, ex)
        info = refinement_bounds(H, n, predicted[n], ex)
        certified = info["certified_at_R"] is not None and ok_ex
        span_ok = True
        if certified and ex:
            # basis at certification must span the exhibited space
            mons = S.homogeneous_mons(n)
            bvecs = [S.poly_to_vec(b, mons) for b in info["basis_polys"]]
            evecs = [S.poly_to_vec(g, mons) for g in ex]
            span_ok = S.spans_equal(bvecs, evecs)
            certified = certified and span_ok
        entry["degrees"][str(n)] = {
            "predicted_dim": predicted[n],
            "exact_dims_R0_R1_R2": info["exact_dims_low_R"],
            "upper_bounds_U_R": info["upper_bounds_U_R"],
            "certified_at_R": info["certified_at_R"],
            "exhibits_verified": ok_ex,
            "basis_matches_exhibits": span_ok,
            "certified": certified,
            "basis_at_certification": info["basis_at_certification"],
        }
        if not certified:
            entry["all_degrees_certified"] = False
        finals.append(str(predicted[n]) if certified else
                      f">={predicted[n]},<={info['upper_bounds_U_R'][-1]}")
    print(f"{name}: certified dims n=0..{NMAX}: {' '.join(finals)}  "
          f"all certified: {entry['all_degrees_certified']}")
    return entry


def span_pred():
    return {n: (1 if n in (0, 6) else 0) for n in range(NMAX + 1)}


def main():
    results = {
        "definition": ("D_inf(H) = {G : C_k D^r G = 0, all odd k >= 3, "
                       "all r >= 0}; S^R_n refinement with gates "
                       "T_3, T_5 (programmes/DYNAMIC_CORE_RESULTS.md)"),
        "parameters": {"NMAX": NMAX, "RMAX": RMAX, "R_Q": R_Q,
                       "R_VERIFY": R_VERIFY, "PRIMES": PRIMES},
        "certification": ("dim S^R_n <= (n+1) - max_p rank_p(rows) "
                          "over the three primes; equality with an "
                          "exhibited D_inf subspace certifies the "
                          "degree exactly"),
        "family": [], "monomials": [], "probes": [],
    }
    one = S.mono(0, 0)
    sp = span_pred()

    for a in [Fraction(0), Fraction(1, 2), Fraction(-1, 2), Fraction(1),
              Fraction(-1), Fraction(2), Fraction(-2), Fraction(3),
              Fraction(20)]:
        H = H_family(a)
        results["family"].append(run_case(
            f"H_a, a={a}", H, sp,
            "span{1, H} (repo Theorem W4)",
            {0: [one], 6: [H]}))

    def strip(kind):
        d = {}
        for n in range(NMAX + 1):
            if kind == "strip3":
                d[n] = 1 if n == 0 else (2 if n == 1 else 3)
            elif kind == "strip2":
                d[n] = 1 if n == 0 else 2
            elif kind == "span_qp":
                d[n] = 1 if n in (0, 2, 6) else 0
            elif kind == "balanced":
                d[n] = 1 if n % 2 == 0 else 0
        return d

    mon_cases = [
        ("q^6", S.mono(6, 0), "strip3", "Q[q] + p Q[q] + p^2 Q[q]",
         {n: [S.mono(n, 0)] + ([S.mono(n - 1, 1)] if n >= 1 else [])
             + ([S.mono(n - 2, 2)] if n >= 2 else [])
          for n in range(NMAX + 1)}),
        ("q^5*p", S.mono(5, 1), "strip2", "Q[q] + p Q[q]",
         {n: [S.mono(n, 0)] + ([S.mono(n - 1, 1)] if n >= 1 else [])
          for n in range(NMAX + 1)}),
        ("q^4*p^2", S.mono(4, 2), "span_qp", "span{1, qp, H}",
         {0: [one], 2: [S.mono(1, 1)], 6: [S.mono(4, 2)]}),
        ("q^3*p^3", S.mono(3, 3), "balanced", "Q[qp]",
         {n: ([S.mono(n // 2, n // 2)] if n % 2 == 0 else [])
          for n in range(NMAX + 1)}),
        ("q^2*p^4", S.mono(2, 4), "span_qp", "span{1, qp, H}",
         {0: [one], 2: [S.mono(1, 1)], 6: [S.mono(2, 4)]}),
        ("q*p^5", S.mono(1, 5), "strip2", "Q[p] + q Q[p]",
         {n: [S.mono(0, n)] + ([S.mono(1, n - 1)] if n >= 1 else [])
          for n in range(NMAX + 1)}),
        ("p^6", S.mono(0, 6), "strip3", "Q[p] + q Q[p] + q^2 Q[p]",
         {n: [S.mono(0, n)] + ([S.mono(1, n - 1)] if n >= 1 else [])
             + ([S.mono(2, n - 2)] if n >= 2 else [])
          for n in range(NMAX + 1)}),
    ]
    for name, H, kind, desc, exhibit in mon_cases:
        results["monomials"].append(run_case(
            name, H, strip(kind), f"{desc} (repo Theorem M)",
            {n: v for n, v in exhibit.items() if v}))

    probes = [
        ("q^6+q^5*p+p^6",
         S.add(S.add(S.mono(6, 0), S.mono(5, 1)), S.mono(0, 6))),
        ("q^6+q^4*p^2+p^6",
         S.add(S.add(S.mono(6, 0), S.mono(4, 2)), S.mono(0, 6))),
    ]
    for name, H in probes:
        results["probes"].append(run_case(
            name, H, sp, "span{1, H} (repo Theorem W4)",
            {0: [one], 6: [H]}))

    out = HERE / "family_cores.json"
    out.write_text(json.dumps(results, indent=2, ensure_ascii=False))
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
