"""Independent cross-checks for the sextic-family computations.

Routes compared (all exact):
  (A) this programme's gate machinery (transvectants T_3, T_5);
  (B) improvements/moyal_partner_checker.py: the D-operator checker
      (D^(2m+1)(H, G) = 0 for all m >= 1), an independent implementation;
  (C) the repository's own research/hamiltonian/independent/engine.py
      (the star-product engine behind partner_lab.py): homogeneous_
      kernel and exact_partner;
  (D) the repository CLI partner_lab.py `kernel` command, run as a
      subprocess, for a sample of cases.

Checks performed:
  1. Partner-space span equality (A) vs (B) and (A) vs (C) on a grid:
     the family at a in {0, 1/2, 1, -1, 2, -2, 20, 40/7} (including
     exceptional values), the monomial sextics, and the probes, at
     assorted degrees including exceptional degrees 3, 4, 5.
  2. Monomial verdicts: for every monomial G of degree <= 8 and each
     H in the grid, gate verdict (A) == exact_partner (C) ==
     is_correction_free (B).
  3. partner_lab CLI (D) dimensions agree on the sample.
  4. Static consistency: refinement dims at R = 0 (family_cores
     machinery) equal partner dims, for the core cases at degrees
     <= 16.
  5. Core membership: span{1, H} is killed by both gates after D^r,
     r <= 6, for every core case (necessary condition for the
     exhibited core subspaces).
  6. Generic-vs-specialization: family_partners.json already asserts
     blocked == unblocked and generic == specialized off the
     exceptional loci; here the exceptional rational values a = 20,
     a = +-40/7 (degrees 3, 5) get explicit bases from route (A)
     re-verified by routes (B) and (C) as spans.

Output: cross_checks.json with a pass/fail summary; the script exits
nonzero if any check fails.
"""

import json
import subprocess
import sys
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE))  # moyal_partner_checker.py lives in this directory (checker change)
REPO = HERE.parents[2]  # repository root
sys.path.insert(0, str(REPO / "research" / "hamiltonian" / "independent"))
import sextic_lib as S
import moyal_partner_checker as M
import engine as E

REPO_LAB = str(REPO / "research" / "hamiltonian" / "partner_lab.py")

FAIL = []


def note(ok, msg):
    print(("PASS  " if ok else "FAIL  ") + msg)
    if not ok:
        FAIL.append(msg)
    return ok


def spans_all_routes(H, n, label):
    mons = S.homogeneous_mons(n)
    ours = [S.poly_to_vec(b, mons) for b in S.partner_kernel(H, n)]
    mb = [S.poly_to_vec(b, mons) for b in M.homogeneous_kernel(H, n)]
    eb = [S.poly_to_vec(b, mons) for b in E.homogeneous_kernel(H, n)]
    ok = S.spans_equal(ours, mb) and S.spans_equal(ours, eb)
    return note(ok, f"spans A=B=C for {label}, degree {n} "
                    f"(dim {len(ours)})")


def H_family(a):
    return S.add(S.add(S.mono(6, 0), S.scale(S.mono(3, 3), a)),
                 S.mono(0, 6))


def main():
    summary = {}

    # ---------------------------------------------------------- 1
    fam_degrees = [3, 4, 5, 6, 8, 10, 12, 16, 20]
    for a in [Fraction(0), Fraction(1, 2), Fraction(1), Fraction(-1),
              Fraction(2), Fraction(-2), Fraction(20), Fraction(40, 7),
              Fraction(-40, 7)]:
        H = H_family(a)
        for n in fam_degrees:
            spans_all_routes(H, n, f"H_a a={a}")
    for j in range(7):
        H = S.mono(j, 6 - j)
        for n in [3, 4, 6, 11, 12, 13, 18]:
            spans_all_routes(H, n, f"q^{j} p^{6 - j}")
    probes = [
        ("q^6+q^5*p+p^6",
         S.add(S.add(S.mono(6, 0), S.mono(5, 1)), S.mono(0, 6))),
        ("q^6+q^4*p^2+p^6",
         S.add(S.add(S.mono(6, 0), S.mono(4, 2)), S.mono(0, 6))),
    ]
    for name, H in probes:
        for n in [3, 4, 5, 6, 8, 12]:
            spans_all_routes(H, n, name)
    summary["span_checks_done"] = True

    # ---------------------------------------------------------- 2
    bad = 0
    total = 0
    Hs = [H_family(Fraction(0)), H_family(Fraction(1)),
          H_family(Fraction(-2)), S.mono(3, 3), S.mono(4, 2),
          probes[0][1]]
    for H in Hs:
        for c in range(9):
            for e in range(9 - c):
                g = S.mono(c, e)
                total += 1
                ours = all(t == {} for t in S.gates_of(H, g))
                theirs_b, _ = M.is_correction_free(H, g)
                theirs_c = E.exact_partner(H, g)
                if not (ours == theirs_b == theirs_c):
                    bad += 1
                    print("  monomial mismatch", S.fmt(H), S.fmt(g),
                          ours, theirs_b, theirs_c)
    note(bad == 0, f"monomial verdicts agree on {total} pairs "
                   f"({bad} mismatches)")

    # ---------------------------------------------------------- 3
    cli_cases = [
        ("q^6+p^6", 3, 2), ("q^6+p^6", 10, 1),
        ("q^6+2*q^3*p^3+p^6", 6, None),
        ("q^3*p^3", 12, 3), ("q^6+q^3*p^3+p^6", 4, 1),
        ("q^6+q^5*p+p^6", 6, None),
    ]
    for hstr, n, _exp in cli_cases:
        out = subprocess.run(
            [sys.executable, REPO_LAB, "kernel", "--H", hstr,
             "--degree", str(n)],
            capture_output=True, text=True, timeout=600)
        data = json.loads(out.stdout)
        H = {"q^6+p^6": H_family(Fraction(0)),
             "q^6+2*q^3*p^3+p^6": H_family(Fraction(2)),
             "q^3*p^3": S.mono(3, 3),
             "q^6+q^3*p^3+p^6": H_family(Fraction(1)),
             "q^6+q^5*p+p^6": probes[0][1]}[hstr]
        ours = S.partner_dim(H, n)
        note(data["dimension"] == ours,
             f"partner_lab CLI dim for H={hstr}, degree {n}: "
             f"CLI {data['dimension']} vs ours {ours}")

    # ---------------------------------------------------------- 4, 5
    core_Hs = [("family a=0", H_family(Fraction(0))),
               ("family a=2", H_family(Fraction(2))),
               ("q^3*p^3", S.mono(3, 3)),
               ("probe1", probes[0][1])]
    for name, H in core_Hs:
        ok = True
        for n in range(17):
            dims, _ = S.refinement(H, n, 0)
            if dims[0] != S.partner_dim(H, n):
                ok = False
        note(ok, f"refinement R=0 dims == partner dims for {name}")
        ok = True
        for g in [S.mono(0, 0), H]:
            img = g
            for r in range(7):
                if any(t != {} for t in S.gates_of(H, img)):
                    ok = False
                img = S.poisson(H, img)
        note(ok, f"1 and H are gate-killed after D^r (r<=6) for {name}")

    summary["failures"] = FAIL
    out = HERE / "cross_checks.json"
    out.write_text(json.dumps(summary, indent=2, ensure_ascii=False))
    print(f"\n{len(FAIL)} failures; wrote {out}")
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
