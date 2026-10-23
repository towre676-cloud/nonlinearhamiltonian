# Research programmes and milestone records

This directory imports the 2026-10-21 handoff programme documents and records what has been completed since. Code lives in `../extensions/`. Enveloped certificates live in `../results/`.

| File | Role |
|---|---|
| `PROGRAMME.md`, `TARGET_OBSERVERS.md`, `HAMILTONIAN_CORES.md`, `OBSTRUCTIONS_AND_ARITHMETIC.md`, `MODEL_COUNTEREXAMPLES.md` | The handoff programme, kept verbatim. |
| `TASKS.json` | The ordered tasks with their current status. |
| `CLAIMS_LEDGER.json` | Claims by status: retained results, implemented engines, certified computations, theorems and open targets. |
| `MACHINERY_MILESTONES.md` | C0, O1–O3 (including set-valued noise and metric search), S1–S3 (including integral Smith cohomology), A1–A2 (Pell orbits and units of both quadratic orders): theorems, certificates, retained counterexamples and scope. |
| `DYNAMIC_CORE_RESULTS.md` | W1–W4: the discovery backend, all-degree kernel certificates, certified cores, the six-parameter `qp³` theorem, the top-weight reduction lemma, homogeneous quartics, the classification of quintic and sextic dynamic cores, and arbitrary-degree results (monomial theorem, simple-root rigidity, the root-rigidity theorem in all degrees, active part, perturbation corollary) and inhomogeneous Hamiltonians with two-root tops (§6, including the triangular families that refute the pure-top conjecture). |
| `EXTENSION_CHECKS.json` | The handoff's seed check list, kept as it was. `../extensions/run_all.py` supersedes it. |

## Next steps

1. Pure tops (`DYNAMIC_CORE_RESULTS.md` §§6.8–6.14). The original two-root conjecture is false for pure tops; balanced and near tops are proved. With constant transverse top everything outside the cubic phase is now proved, and the families K1, K1′, K2, K1+K2, K4 and K3 (`k ≥ 3`) are exact. The corrected conjecture P004 is itself false as stated: K3 needs an extra term `βG` for `k ≥ 3` (§6.14). The current statement is P005. Open: transverse tops `(ℓ+γ)ᵏ` with `k = 1` or `k = s`, which include the K3 upper bound for `k ≤ 2`. A careful literature review (§6.13) is still needed before any positioning claim.
2. Probabilistic or continuous noise for adaptive experiments. This needs posterior semantics and a different termination theorem.
3. Performance. The Weyl Gröbner backend uses `Fraction` arithmetic without a chain criterion.
