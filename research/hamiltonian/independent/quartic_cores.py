#!/usr/bin/env python3
"""Quartic dynamic-core tables for the nonlinearhamiltonian project.

DEFINITION USED (quoted from the repository, not invented here):

  programmes/DYNAMIC_CORE_RESULTS.md, opening section:
    "D = {H,.} = H_q dp - H_p dq, and C_k = T_k(H,.) for the nonzero odd
     transvectants with k >= 3. The dynamic core is
        D_inf(H) = { G in Q[q,p] : C_k D^r G = 0
                     for all odd k >= 3 and all r >= 0 }."

  programmes/HAMILTONIAN_CORES.md gives the same object as
    D_inf(H) = { G in R : C_j D^r G = 0 for every j >= 1, r >= 0 },
    C_j = T_{2j+1}(H, .).

  research/hamiltonian/dynamics/proofs.md gives the equivalent form
    K_j(H) = intersection_{r=0}^{j} ker(L_{H4} delta_H^r),
    D(H)   = intersection_{j >= 0} K_j(H),
  and states D(H) is "the largest delta_H-invariant vector subspace
  contained in E" (E = one-step partner space).

For every Hamiltonian treated here deg H = 4, so T_k(H, .) = 0 for
k >= 5 (a k-th transvectant differentiates H k times) and the only
nonzero gate is C_3 = T_3(H, .).  The Moyal-defect checkers used for
cross-validation (repository engine, moyal_partner_checker) impose all
odd gates at once, so agreement with them also confirms that dropping
k >= 5 loses nothing for these H.

WHAT IS COMPUTED (exact rational arithmetic, stdlib Fractions only):
  * Per homogeneous degree n <= NMAX, the refinement spaces
        S^R_n(H) = { G in V_n : T_3(H, D^r G) = 0 for r = 0..R }
    for R = 0..RMAX.  S^0_n is the one-step partner (static) space E_n.
    The true graded core satisfies D_inf(H)_n subseteq S^R_n for every
    R, so dim S^R_n is a rigorous upper bound on dim D_inf(H)_n.
    Where dim S^R_n equals the dimension of an explicitly exhibited
    subspace of D_inf(H) (the repository's proved core, whose members
    are re-verified here to be killed by T_3 after every computed D^r
    and to be D-invariant in the computed range), the per-degree core
    in that degree is determined exactly.  No all-degree claim is made
    from the truncation alone; all-degree statements are the
    repository's theorems, cited in the report.
  * For the inhomogeneous contrast H = qp^3 + q^2, the refinements
        K_R^{<=N} = { G : deg G <= N, T_3(H, D^r G) = 0 for r = 0..R }
    with FULL (unprojected) D^r images.  Again D_inf(H) cap {deg <= N}
    subseteq K_R^{<=N} for every R, so dim K_R^{<=N} = 2 together with
    span{1, H} subseteq K_R^{<=N} proves the degree-<=N slice of the
    core is exactly span{1, H}, unconditionally.

CROSS-CHECKS: partner spaces E_n are compared, degree by degree, with
  (a) improvements/moyal_partner_checker.py  (independent D-operator
      checker), and
  (b) the repository's own research/hamiltonian/independent/engine.py
      (defining star-product engine, as used by partner_lab.py).
Both are located relative to this file; no absolute paths are used.

Output: quartic_cores.json next to this script.
"""

from fractions import Fraction
from math import comb, gcd, lcm
from functools import reduce
from pathlib import Path
import importlib.util
import json
import sys

HERE = Path(__file__).resolve().parent

NMAX = 16          # highest homogeneous degree tabulated
RMAX = 8           # highest refinement depth for homogeneous cases
XC_MAX = 12        # highest degree used in cross-checks
INH_NMAX = 8       # degree bound for the inhomogeneous candidate space
INH_RMAX = 10      # refinement depth for the inhomogeneous case

# ---------------------------------------------------------------- polys
# Polynomial: dict (a, b) -> Fraction, term q^a p^b.  Zero terms omitted.

def clean(p):
    return {k: v for k, v in p.items() if v != 0}

def add(*ps):
    out = {}
    for p in ps:
        for k, v in p.items():
            out[k] = out.get(k, Fraction(0)) + v
    return clean(out)

def scale(p, s):
    return clean({k: v * s for k, v in p.items()})

def mul(a, b):
    out = {}
    for (a1, b1), c1 in a.items():
        for (a2, b2), c2 in b.items():
            k = (a1 + a2, b1 + b2)
            out[k] = out.get(k, Fraction(0)) + c1 * c2
    return clean(out)

def mono(a, b, c=1):
    return {(a, b): Fraction(c)} if c else {}

def falling(n, k):
    if k < 0 or k > n:
        return 0
    r = 1
    for i in range(k):
        r *= n - i
    return r

def deriv(p, dq, dp):
    out = {}
    for (a, b), c in p.items():
        if a < dq or b < dp:
            continue
        k = (a - dq, b - dp)
        out[k] = out.get(k, Fraction(0)) + c * falling(a, dq) * falling(b, dp)
    return clean(out)

def poisson(H, G):
    """D_H G = {H, G} = H_q G_p - H_p G_q."""
    return add(mul(deriv(H, 1, 0), deriv(G, 0, 1)),
               scale(mul(deriv(H, 0, 1), deriv(G, 1, 0)), -1))

def transvectant(F, G, k):
    """T_k(F,G) exactly as in research/hamiltonian/quartic/proofs.md:
    sum_j (-1)^j C(k,j) (dq^{k-j} dp^j F)(dq^j dp^{k-j} G)."""
    out = {}
    for j in range(k + 1):
        left = deriv(F, k - j, j)
        right = deriv(G, j, k - j)
        if left and right:
            out = add(out, scale(mul(left, right),
                                 Fraction((-1) ** j * comb(k, j))))
    return out

def gate(H, G):
    """The only nonzero correction gate for deg H = 4: C_3 = T_3(H, .)."""
    return transvectant(H, G, 3)

# ------------------------------------------------------- linear algebra

def nullspace(rows, ncols):
    mat = [list(r) for r in rows]
    pivots = []
    r = 0
    for c in range(ncols):
        piv = next((i for i in range(r, len(mat)) if mat[i][c] != 0), None)
        if piv is None:
            continue
        mat[r], mat[piv] = mat[piv], mat[r]
        pv = mat[r][c]
        mat[r] = [x / pv for x in mat[r]]
        for i in range(len(mat)):
            if i != r and mat[i][c] != 0:
                f = mat[i][c]
                mat[i] = [x - f * y for x, y in zip(mat[i], mat[r])]
        pivots.append(c)
        r += 1
        if r >= len(mat):
            break
    basis = []
    for fc in (c for c in range(ncols) if c not in pivots):
        vec = [Fraction(0)] * ncols
        vec[fc] = Fraction(1)
        for i, pc in enumerate(pivots):
            vec[pc] = -mat[i][fc]
        basis.append(vec)
    return basis

def rank(vecs):
    """Rank of a list of equal-length Fraction vectors."""
    if not vecs:
        return 0
    mat = [list(v) for v in vecs]
    ncols = len(mat[0])
    r = 0
    for c in range(ncols):
        piv = next((i for i in range(r, len(mat)) if mat[i][c] != 0), None)
        if piv is None:
            continue
        mat[r], mat[piv] = mat[piv], mat[r]
        pv = mat[r][c]
        mat[r] = [x / pv for x in mat[r]]
        for i in range(len(mat)):
            if i != r and mat[i][c] != 0:
                f = mat[i][c]
                mat[i] = [x - f * y for x, y in zip(mat[i], mat[r])]
        r += 1
        if r >= len(mat):
            break
    return r

def in_span(vec, basis_vecs):
    if not basis_vecs:
        return all(v == 0 for v in vec)
    return rank(basis_vecs + [vec]) == rank(basis_vecs)

def spans_equal(basis_a, basis_b, ambient_dim):
    va = [list(v) for v in basis_a]
    vb = [list(v) for v in basis_b]
    return rank(va) == rank(vb) == rank(va + vb)

# ------------------------------------------------------------ formatting

def primitive(p):
    if not p:
        return {}
    den = reduce(lcm, (v.denominator for v in p.values()), 1)
    ints = {k: int(v * den) for k, v in p.items()}
    g = reduce(gcd, (abs(v) for v in ints.values()))
    first = sorted(ints)[0]
    sgn = 1 if ints[first] > 0 else -1
    return {k: Fraction(v * sgn, g) for k, v in ints.items()}

def fmt(p):
    if not p:
        return "0"
    def keyf(kv):
        (a, b), _ = kv
        return (-(a + b), -a, b)
    parts = []
    for (a, b), c in sorted(p.items(), key=keyf):
        t = ""
        if a:
            t += f"q^{a}" if a > 1 else "q"
        if b:
            t += f"p^{b}" if b > 1 else "p"
        if not t:
            t = "1"
        if c == 1:
            parts.append(t)
        elif c == -1:
            parts.append("-" + t)
        else:
            parts.append(f"({c})*{t}")
    return " + ".join(parts).replace("+ -", "- ")

def vec_to_poly(vec, mons):
    return clean({m: c for c, m in zip(vec, mons) if c})

def poly_to_vec(p, mons):
    return [p.get(m, Fraction(0)) for m in mons]

# ------------------------------------------------------- core machinery

def refinement_dims_and_basis(H, mons, rmax):
    """Stacked conditions T_3(H, D^r G) = 0 for r = 0..rmax on the span
    of the monomials `mons`.  D^r images are kept as full polynomials
    (no projection back into any bounded space).
    Returns (dims_by_R, final_basis_polys)."""
    images = [mono(a, b) for (a, b) in mons]   # D^0 images
    rows = []
    dims = []
    basis = []
    for r in range(rmax + 1):
        gated = [gate(H, im) for im in images]
        keys = sorted({k for g in gated for k in g})
        for k in keys:
            rows.append([g.get(k, Fraction(0)) for g in gated])
        vecs = nullspace(rows, len(mons))
        dims.append(len(vecs))
        basis = [vec_to_poly(v, mons) for v in vecs]
        images = [poisson(H, im) for im in images]  # next D iterate
    return dims, basis

def homogeneous_mons(n):
    return [(a, n - a) for a in range(n + 1)]

def all_mons_upto(n):
    return [(a, b) for d in range(n + 1) for a in range(d + 1)
            for b in [d - a]]

# ------------------------------------------------- external cross-check

def load_module(name, candidates):
    for cand in candidates:
        p = cand.resolve()
        if p.is_file():
            spec = importlib.util.spec_from_file_location(name, p)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            return mod, p
    return None, None

def find_checkers():
    moyal_candidates = [
        HERE / "moyal_partner_checker.py",
        HERE / ".." / ".." / "improvements" / "moyal_partner_checker.py",
        HERE / ".." / "improvements" / "moyal_partner_checker.py",
    ]
    engine_candidates = [
        HERE / "engine.py",
        HERE / ".." / ".." / "nonlinearhamiltonian" / "research"
        / "hamiltonian" / "independent" / "engine.py",
        HERE / ".." / "nonlinearhamiltonian" / "research"
        / "hamiltonian" / "independent" / "engine.py",
    ]
    moyal, mp = load_module("moyal_partner_checker_x", moyal_candidates)
    engine, ep = load_module("repo_engine_x", engine_candidates)
    return moyal, mp, engine, ep

# ------------------------------------------------------------- the data

def H_parse(*terms):
    out = {}
    for a, b, c in terms:
        out = add(out, mono(a, b, c))
    return out

CASES = [
    {
        "id": "q4",
        "H_str": "q^4",
        "H": H_parse((4, 0, 1)),
        "root_type": "(4) -- fourth power of a linear form",
        "e": 1,
        "repo_proved_core": "Q[q] + p*Q[q] + p^2*Q[q]  (the full strip E(q^4))",
        "repo_source": "DYNAMIC_CORE_RESULTS.md sec.3c table; dynamics/proofs.md (fourth powers, a=0 stratum)",
        "family": "strip: in degree n the monomials q^n, q^(n-1) p (n>=1), q^(n-2) p^2 (n>=2)",
    },
    {
        "id": "q3p",
        "H_str": "q^3 p",
        "H": H_parse((3, 1, 1)),
        "root_type": "(3,1)",
        "e": 4,
        "repo_proved_core": "Q[q] + p*Q[q]",
        "repo_source": "DYNAMIC_CORE_RESULTS.md sec.3c table (type (3,1))",
        "family": "in degree n the monomials q^n and q^(n-1) p (n>=1)",
    },
    {
        "id": "qp3",
        "H_str": "q p^3",
        "H": H_parse((1, 3, 1)),
        "root_type": "(3,1) with q and p exchanged",
        "e": 4,
        "repo_proved_core": "Q[p] + q*Q[p]",
        "repo_source": "DYNAMIC_CORE_RESULTS.md sec.2 calibration table (H = qp^3); sec.5.1 monomial theorem (b=1 case, swapped)",
        "family": "in degree n the monomials p^n and q p^(n-1) (n>=1)",
    },
    {
        "id": "q2p2",
        "H_str": "q^2 p^2",
        "H": H_parse((2, 2, 1)),
        "root_type": "(2,2) -- square of the nondegenerate quadratic qp",
        "e": 2,
        "repo_proved_core": "Q[qp]",
        "repo_source": "DYNAMIC_CORE_RESULTS.md sec.3c table (type (2,2))",
        "family": "in degree n the monomial (qp)^(n/2) if n is even, nothing if n is odd",
    },
    {
        "id": "q4_p4",
        "H_str": "q^4 + p^4",
        "H": H_parse((4, 0, 1), (0, 4, 1)),
        "root_type": "distinct roots, lambda = 0 in H_lambda = q^4 + lambda q^2 p^2 + p^4",
        "e": 4,
        "repo_proved_core": "span{1, H}",
        "repo_source": "DYNAMIC_CORE_RESULTS.md sec.3c table (distinct, lambda=0) and distinct-roots all-degree theorem",
        "family": "1 in degree 0, H in degree 4, nothing else",
    },
    {
        "id": "q4_q2p2_p4",
        "H_str": "q^4 + q^2 p^2 + p^4",
        "H": H_parse((4, 0, 1), (2, 2, 1), (0, 4, 1)),
        "root_type": "distinct roots, lambda = 1 in H_lambda",
        "e": 4,
        "repo_proved_core": "span{1, H}",
        "repo_source": "DYNAMIC_CORE_RESULTS.md sec.3c table (distinct, lambda=1; 22 generators)",
        "family": "1 in degree 0, H in degree 4, nothing else",
    },
]

INH_CASE = {
    "id": "qp3_plus_q2",
    "H_str": "q p^3 + q^2",
    "H": H_parse((1, 3, 1), (2, 0, 1)),
    "repo_proved_core": "span{1, H}",
    "repo_source": "DYNAMIC_CORE_RESULTS.md sec.2 table (qp^3 + q^2, 13 generators, finite support) and sec.3 theorem (alpha != 0 stratum); partner_lab.py core-demo stages 6 -> 4 -> 2",
}

def expected_static_dim(e, n):
    """quartic/proofs.md: dim E_n = 2 + 1_{e | (n-2)} for n >= 2;
    dim E_0 = 1, dim E_1 = 2."""
    if n == 0:
        return 1
    if n == 1:
        return 2
    return 2 + (1 if (n - 2) % e == 0 else 0)

def main():
    moyal, moyal_path, engine, engine_path = find_checkers()
    print(f"moyal checker: {moyal_path.name if moyal_path else None}")
    print(f"repo engine:   {engine_path.name if engine_path else None}")

    results = {
        "definition": (
            "D_inf(H) = { G in Q[q,p] : C_k D^r G = 0 for all odd k >= 3 "
            "and all r >= 0 }, D = {H,.}, C_k = T_k(H,.) "
            "(programmes/DYNAMIC_CORE_RESULTS.md); equivalently "
            "D(H) = intersection_{j>=0} K_j(H), K_j = intersection_{r<=j} "
            "ker(L_{H4} delta_H^r) (research/hamiltonian/dynamics/"
            "proofs.md). For deg H = 4 the only nonzero gate is T_3."
        ),
        "parameters": {"NMAX": NMAX, "RMAX": RMAX, "XC_MAX": XC_MAX,
                       "INH_NMAX": INH_NMAX, "INH_RMAX": INH_RMAX},
        "arithmetic": "exact rational (fractions.Fraction), stdlib only",
        "cross_check_sources": {
            "moyal_partner_checker": moyal_path.name if moyal_path else None,
            "repo_engine": engine_path.name if engine_path else None,
        },
        "cases": [],
        "inhomogeneous_case": None,
        "cross_checks": {},
    }

    xc = {"partner_dims_agree_all": True, "partner_spans_agree_all": True,
          "monomial_verdicts_agree_all": True, "details": []}

    for case in CASES:
        H = case["H"]
        print(f"\n=== H = {case['H_str']} ===")
        entry = {k: case[k] for k in
                 ("id", "H_str", "root_type", "e", "repo_proved_core",
                  "repo_source", "family")}
        entry["partner_dims_by_degree"] = {}
        entry["refinement_dims_by_degree"] = {}
        entry["core_dims_by_degree_truncated"] = {}
        entry["core_bases_by_degree"] = {}
        entry["static_dim_formula_agrees"] = True
        entry["invariance_in_computed_range"] = True

        core_basis_by_n = {}
        for n in range(NMAX + 1):
            mons = homogeneous_mons(n)
            dims, basis = refinement_dims_and_basis(H, mons, RMAX)
            entry["partner_dims_by_degree"][str(n)] = dims[0]
            entry["refinement_dims_by_degree"][str(n)] = dims
            entry["core_dims_by_degree_truncated"][str(n)] = dims[-1]
            core_basis_by_n[n] = basis
            if dims[0] != expected_static_dim(case["e"], n):
                entry["static_dim_formula_agrees"] = False
            if basis:
                entry["core_bases_by_degree"][str(n)] = [
                    fmt(primitive(b)) for b in basis]
            # cross-checks of the partner space E_n
            if n <= XC_MAX and moyal is not None and engine is not None:
                ours = [poly_to_vec(b, mons) for b in
                        refinement_dims_and_basis(H, mons, 0)[1]]
                mb = moyal.homogeneous_kernel(H, n)
                eb = engine.homogeneous_kernel(H, n)
                mv = [poly_to_vec(b, mons) for b in mb]
                ev = [poly_to_vec(b, mons) for b in eb]
                dims_ok = len(ours) == len(mv) == len(ev) == dims[0]
                spans_ok = (spans_equal(ours, mv, n + 1)
                            and spans_equal(ours, ev, n + 1))
                if not (dims_ok and spans_ok):
                    xc["partner_dims_agree_all"] &= dims_ok
                    xc["partner_spans_agree_all"] &= spans_ok
                    xc["details"].append(
                        f"MISMATCH H={case['H_str']} n={n}: ours={len(ours)} "
                        f"moyal={len(mv)} engine={len(ev)} spans_ok={spans_ok}")
        # D-invariance of the truncated core in the computed range:
        # D maps S^{RMAX}_n into S^{RMAX}_{n+2} for n + 2 <= NMAX.
        for n in range(NMAX - 1):
            if not core_basis_by_n[n]:
                continue
            target_mons = homogeneous_mons(n + 2)
            target_vecs = [poly_to_vec(b, target_mons)
                           for b in core_basis_by_n[n + 2]]
            for G in core_basis_by_n[n]:
                DG = poisson(H, G)
                if not in_span(poly_to_vec(DG, target_mons), target_vecs):
                    entry["invariance_in_computed_range"] = False
                    xc["details"].append(
                        f"INVARIANCE FAIL H={case['H_str']} n={n} G={fmt(G)}")
        # monomial verdict spot-check: our T_3 verdict vs both checkers
        if moyal is not None and engine is not None:
            for a in range(7):
                for b in range(7 - a):
                    g = mono(a, b)
                    ours_free = (gate(H, g) == {})
                    moyal_free, _ = moyal.is_correction_free(H, g)
                    engine_free = engine.exact_partner(H, g)
                    if not (ours_free == moyal_free == engine_free):
                        xc["monomial_verdicts_agree_all"] = False
                        xc["details"].append(
                            f"MONOMIAL MISMATCH H={case['H_str']} "
                            f"G=q^{a}p^{b}: ours={ours_free} "
                            f"moyal={moyal_free} engine={engine_free}")
        dims_str = " ".join(str(entry["core_dims_by_degree_truncated"][str(n)])
                             for n in range(NMAX + 1))
        print(f"partner dims n=0..{XC_MAX}: "
              f"{[entry['partner_dims_by_degree'][str(n)] for n in range(XC_MAX + 1)]}")
        print(f"truncated core dims n=0..{NMAX}: {dims_str}")
        print(f"static formula agrees: {entry['static_dim_formula_agrees']}; "
              f"invariance in range: {entry['invariance_in_computed_range']}")
        results["cases"].append(entry)

    # ------------------------------------------------ inhomogeneous case
    H = INH_CASE["H"]
    print(f"\n=== H = {INH_CASE['H_str']} (inhomogeneous) ===")
    mons = all_mons_upto(INH_NMAX)
    dims, basis = refinement_dims_and_basis(H, mons, INH_RMAX)
    print(f"candidate monomials deg <= {INH_NMAX}: {len(mons)}")
    print(f"K_R dims for R=0..{INH_RMAX}: {dims}")
    print("final basis:", [fmt(primitive(b)) for b in basis])
    one = mono(0, 0)
    span1H = [poly_to_vec(one, mons), poly_to_vec(H, mons)]
    final_vecs = [poly_to_vec(b, mons) for b in basis]
    inh = dict(INH_CASE)
    inh.pop("H")
    inh.update({
        "candidate_space": f"all polynomials of total degree <= {INH_NMAX} "
                           f"({len(mons)} monomials)",
        "refinement_dims_by_R": dims,
        "final_basis": [fmt(primitive(b)) for b in basis],
        "span_1_H_contained_in_final": all(
            in_span(v, final_vecs) for v in span1H),
        "D_of_1": fmt(poisson(H, one)),
        "D_of_H": fmt(poisson(H, H)),
        "gate_of_1": fmt(gate(H, one)),
        "gate_of_H": fmt(gate(H, H)),
        "static_dims_by_degree_note": (
            "The gate T_3(H,.) depends only on the degree>=3 part qp^3 "
            "(third derivatives of q^2 vanish), so the per-degree static "
            "partner spaces equal those of qp^3, cross-checked above."),
    })
    results["inhomogeneous_case"] = inh

    results["cross_checks"] = xc
    print("\ncross-checks:", {k: v for k, v in xc.items() if k != "details"})
    if xc["details"]:
        print("cross-check details:", *xc["details"], sep="\n  ")

    out = HERE / "quartic_cores.json"
    out.write_text(json.dumps(results, indent=2, ensure_ascii=False))
    print(f"\nwrote {out.name}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
