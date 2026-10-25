#!/usr/bin/env python3
"""Inhomogeneous quartic cores: collapse depths for quadratic
perturbations, in truncated spaces deg <= 8 (and deg <= 10).

Setting (repository, programmes/DYNAMIC_CORE_RESULTS.md): the dynamic
core D_inf(H) = { G : C_k D^r G = 0 for all odd k >= 3, all r >= 0 },
D = {H, .}, C_k = T_k(H, .).  For a quartic top part the only gate is
T_3, and T_3 sees only the part of H of degree >= 3: a quadratic
perturbation never changes the gate, only D.

For each inhomogeneous H below and each N in {8, 10} this computes,
in exact rational arithmetic,
    K_R^{<=N}(H) = { G : deg G <= N, T_3(H, D^r G) = 0 for r <= R },
    R = 0..12,
with D^r images kept as full polynomials.  D_inf(H) cap {deg <= N}
subseteq K_R^{<=N} for every R, and span{1, H} subseteq K_R^{<=N}
always, so:
  * if dim K_R^{<=N} = 2 for some R, the deg-<=N slice of D_inf(H) is
    exactly span{1, H} -- proved by this computation alone;
  * if dim K_12^{<=N} equals the dimension of a family F cap {deg<=N}
    with F subseteq D_inf(H) (a repository theorem, cited per case)
    and F cap {deg<=N} subseteq K_12^{<=N} (verified here), the slice
    is exactly F cap {deg <= N}.

The algebra (polynomials, Poisson bracket, transvectant, exact
nullspace) is imported from quartic_cores_ext.py in this directory,
which is itself cross-checked there against the repository engine,
the independent Moyal checker, the repository Weyl-operator
machinery, and the wave-one tables.  Final bases here are additionally
verified element-by-element with the repository engine and the Moyal
checker (independent star-product routes) on the iterates D^r G.

Paths are relative to this file.  Standard library only.
"""

from fractions import Fraction
from pathlib import Path
import importlib.util
import json
import sys
import time

HERE = Path(__file__).resolve().parent

spec = importlib.util.spec_from_file_location(
    "quartic_cores_ext", HERE / "quartic_cores_ext.py")
X = importlib.util.module_from_spec(spec)
spec.loader.exec_module(X)

add, mono, fmt = X.add, X.mono, X.fmt
gate, poisson, refinement = X.gate, X.poisson, X.refinement
poly_to_vec, in_span = X.poly_to_vec, X.in_span

RMAX = 12
N_LIST_MAIN = (8, 10)
N_LIST_T_FAMILY = (8,)   # t != 1 values only at deg <= 8 (see report:
                         # torus scaling makes dims t-independent)

def H_parse(*terms):
    out = {}
    for a, b, c in terms:
        out = add(out, mono(a, b, Fraction(c)))
    return out

def all_mons_upto(n):
    return [(a, b) for d in range(n + 1) for a in range(d + 1)
            for b in [d - a]]

# Families F with F subseteq D_inf(H) by repository theorems.
def strip_mons(N):
    """Q[q] + p Q[q] + p^2 Q[q] (core of q^4), truncated to deg <= N."""
    return [(a, b) for b in (0, 1, 2) for a in range(N - b + 1)]

def tower_mons(N):
    """Q[qp], truncated to deg <= N."""
    return [(j, j) for j in range(N // 2 + 1)]

def near_strip_mons(N):
    """Q[p] + q Q[p] (core of q p^3), truncated to deg <= N."""
    return [(0, b) for b in range(N + 1)] + \
           [(1, b) for b in range(N)]

CASES = [
    {"id": "qp3_plus_half_q2", "t": "1/2",
     "H_str": "q p^3 + (1/2) q^2",
     "H": H_parse((1, 3, 1), (2, 0, Fraction(1, 2))),
     "family_id": "qp3_plus_t_q2",
     "prediction": "collapse to span{1,H}",
     "predicted_family": None},
    {"id": "qp3_plus_q2", "t": "1",
     "H_str": "q p^3 + q^2",
     "H": H_parse((1, 3, 1), (2, 0, 1)),
     "family_id": "qp3_plus_t_q2",
     "prediction": "collapse to span{1,H}",
     "predicted_family": None},
    {"id": "qp3_plus_2q2", "t": "2",
     "H_str": "q p^3 + 2 q^2",
     "H": H_parse((1, 3, 1), (2, 0, 2)),
     "family_id": "qp3_plus_t_q2",
     "prediction": "collapse to span{1,H}",
     "predicted_family": None},
    {"id": "q3p_plus_half_p2", "t": "1/2",
     "H_str": "q^3 p + (1/2) p^2",
     "H": H_parse((3, 1, 1), (0, 2, Fraction(1, 2))),
     "family_id": "q3p_plus_t_p2",
     "prediction": "collapse to span{1,H} (mirror of qp3 + t q^2)",
     "predicted_family": None},
    {"id": "q3p_plus_p2", "t": "1",
     "H_str": "q^3 p + p^2",
     "H": H_parse((3, 1, 1), (0, 2, 1)),
     "family_id": "q3p_plus_t_p2",
     "prediction": "collapse to span{1,H} (mirror of qp3 + t q^2)",
     "predicted_family": None},
    {"id": "q3p_plus_2p2", "t": "2",
     "H_str": "q^3 p + 2 p^2",
     "H": H_parse((3, 1, 1), (0, 2, 2)),
     "family_id": "q3p_plus_t_p2",
     "prediction": "collapse to span{1,H} (mirror of qp3 + t q^2)",
     "predicted_family": None},
    {"id": "q4_plus_q2", "t": "1",
     "H_str": "q^4 + q^2",
     "H": H_parse((4, 0, 1), (2, 0, 1)),
     "family_id": "q4_plus_q2",
     "prediction": ("no collapse: slice = strip Q[q]+pQ[q]+p^2Q[q] "
                    "(Thm P+ case 1, DYNAMIC_CORE_RESULTS.md sec.6.2)"),
     "predicted_family": "strip"},
    {"id": "q2p2_plus_qp", "t": "1",
     "H_str": "q^2 p^2 + q p",
     "H": H_parse((2, 2, 1), (1, 1, 1)),
     "family_id": "q2p2_plus_qp",
     "prediction": ("no collapse: slice = Q[qp] (H in Q[G], G = qp; "
                    "Thm P+ case 3 / Thm B, sec.6.2/6.5)"),
     "predicted_family": "tower"},
    {"id": "q2p2_plus_q2_TEST", "t": "1",
     "H_str": "q^2 p^2 + q^2",
     "H": H_parse((2, 2, 1), (2, 0, 1)),
     "family_id": "q2p2_plus_q2",
     "prediction": ("TEST CASE (not used to formulate the pattern): "
                    "collapse to span{1,H}, because H is not in Q[G] "
                    "for any quadratic G with leading part qp "
                    "(Thm B, sec.6.5)"),
     "predicted_family": None},
    {"id": "qp3_plus_qp_TEST", "t": "1",
     "H_str": "q p^3 + q p",
     "H": H_parse((1, 3, 1), (1, 1, 1)),
     "family_id": "qp3_plus_qp",
     "prediction": ("TEST CASE (not used to formulate the pattern): "
                    "no collapse: slice = Q[p] + q Q[p] (six-parameter "
                    "family theorem with a = 0, sec.3b)"),
     "predicted_family": "near_strip"},
]

FAMILIES = {"strip": strip_mons, "tower": tower_mons,
            "near_strip": near_strip_mons}

def stabilisation_depth(dims):
    """First R from which dims is constant through RMAX."""
    fin = dims[-1]
    for r in range(len(dims)):
        if all(d == fin for d in dims[r:]):
            return r
    return None

def main():
    t0 = time.time()
    moyal, moyal_path, engine, engine_path = X.find_checkers()
    print(f"moyal checker: {moyal_path}")
    print(f"repo engine:   {engine_path}", flush=True)

    results = {"parameters": {"RMAX": RMAX},
               "cases": [], "family_consistency": {}}
    seq_by_family = {}

    for case in CASES:
        H = case["H"]
        print(f"\n=== H = {case['H_str']} ===", flush=True)
        entry = {k: case[k] for k in
                 ("id", "H_str", "t", "family_id", "prediction",
                  "predicted_family")}
        entry["runs"] = {}
        n_list = N_LIST_MAIN if case["t"] == "1" else N_LIST_T_FAMILY
        for N in n_list:
            mons = all_mons_upto(N)
            dims, bases = refinement(H, mons, RMAX,
                                     want_bases_at=(RMAX,))
            final = bases[RMAX]
            final_vecs = [poly_to_vec(b, mons) for b in final]
            one = mono(0, 0, Fraction(1))
            span1H_ok = all(
                in_span(poly_to_vec(g, mons), final_vecs)
                for g in (one, H))
            fam = case["predicted_family"]
            fam_check = None
            if fam is not None:
                fm = FAMILIES[fam](N)
                fam_vecs_in = all(
                    in_span(poly_to_vec(mono(a, b, Fraction(1)), mons),
                            final_vecs) for (a, b) in fm)
                fam_check = {
                    "family": fam,
                    "family_truncated_dim": len(fm),
                    "family_contained_in_final": fam_vecs_in,
                    "final_dim_equals_family_dim":
                        len(fm) == dims[-1] and fam_vecs_in,
                }
            run = {
                "candidate_monomials": len(mons),
                "refinement_dims_by_R": dims,
                "stabilisation_depth": stabilisation_depth(dims),
                "final_dim": dims[-1],
                "final_basis": [fmt(b) for b in final],
                "span_1_H_contained_in_final": span1H_ok,
                "slice_equals_span_1_H_proved_by_computation":
                    bool(dims[-1] == 2 and span1H_ok),
                "family_check": fam_check,
            }
            entry["runs"][str(N)] = run
            print(f"  N={N}: dims R=0..{RMAX}: {dims}")
            print(f"       stabilisation depth: "
                  f"{run['stabilisation_depth']}, final dim "
                  f"{dims[-1]}, span{{1,H}} in final: {span1H_ok}, "
                  f"family check: {fam_check}", flush=True)
            if N == 8:
                seq_by_family.setdefault(case["family_id"], {})[
                    case["t"]] = dims
        # independent engine verification of the final basis (N = 8):
        mons8 = all_mons_upto(8)
        _, bases8 = refinement(H, mons8, RMAX, want_bases_at=(RMAX,))
        eng_ok, moy_ok = True, True
        for G in bases8[RMAX]:
            img = G
            for r in range(5):
                if not engine.exact_partner(H, img):
                    eng_ok = False
                free, _ = moyal.is_correction_free(H, img)
                if not free:
                    moy_ok = False
                img = poisson(H, img)
        entry["engine_verifies_final_basis_iterates_r<=4"] = eng_ok
        entry["moyal_verifies_final_basis_iterates_r<=4"] = moy_ok
        print(f"  engine/moyal verify final basis iterates: "
              f"{eng_ok}/{moy_ok}", flush=True)
        results["cases"].append(entry)

    for fam, seqs in seq_by_family.items():
        vals = list(seqs.values())
        results["family_consistency"][fam] = {
            "sequences_by_t": seqs,
            "all_t_sequences_identical": all(v == vals[0] for v in vals),
        }
    # mirror consistency: qp3 + t q^2 vs q3p + t p^2 at deg <= 8
    a = seq_by_family.get("qp3_plus_t_q2", {})
    b = seq_by_family.get("q3p_plus_t_p2", {})
    results["family_consistency"]["mirror_qp3_q3p_identical"] = bool(
        a and b and all(a[t] == b[t] for t in a if t in b))
    print("\nfamily consistency:",
          json.dumps(results["family_consistency"], indent=1)[:800])
    print(f"elapsed: {time.time() - t0:.1f}s")
    out = HERE / "inhomogeneous_cores.json"
    out.write_text(json.dumps(results, indent=2, ensure_ascii=False))
    print(f"wrote {out}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
