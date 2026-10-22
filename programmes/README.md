# Research programmes and milestone records

This directory imports the 2026-10-21 handoff programme documents and records what has been completed since. Code lives in `../extensions/`. Enveloped certificates live in `../results/`.

| File | Role |
|---|---|
| `PROGRAMME.md`, `TARGET_OBSERVERS.md`, `HAMILTONIAN_CORES.md`, `OBSTRUCTIONS_AND_ARITHMETIC.md`, `MODEL_COUNTEREXAMPLES.md` | The handoff programme, kept verbatim. |
| `TASKS.json` | The ordered tasks with their current status. |
| `CLAIMS_LEDGER.json` | Claims by status: retained results, implemented engines, certified computations, theorems and open targets. |
| `MACHINERY_MILESTONES.md` | C0, O1–O3 (including set-valued noise and metric search), S1–S3 (including integral Smith cohomology), A1–A2 (Pell orbits and units of both quadratic orders): theorems, certificates, retained counterexamples and scope. |
| `DYNAMIC_CORE_RESULTS.md` | W1–W4: the discovery backend, all-degree kernel certificates, certified cores, the six-parameter `qp³` theorem, the top-weight reduction lemma, homogeneous quartics, the classification of quintic and sextic dynamic cores, and arbitrary-degree results (monomial theorem, simple-root rigidity, the root-rigidity theorem in all degrees, active part, perturbation corollary) and inhomogeneous Hamiltonians with two-root tops (§6), the complete constant-quadratic-momentum phase diagram, and Claude's triangular containments reconciled with the proved PP/QC/SC/CQ cores (§6.18). |
| `EXTENSION_CHECKS.json` | The handoff's seed check list, kept as it was. `../extensions/run_all.py` supersedes it. |

## Next steps

1. Classify the remaining pure perturbations, especially K1′, the linear-transverse K3 family, variable quadratic-momentum coefficients and higher cubic-phase couplings (§6.18). Balanced and near tops and every nonzero constant quadratic-momentum coefficient are proved. Both P003 and Claude's corrected P004 are false as stated; the latter is refuted by the already proved PP extension with a nonzero linear term in its extra generator. QC/CQ/PP/SC upgrade the overlapping triangular containments to full equalities. See `research/core_overlap/README.md`; historical priority still requires specialist review.
2. Probabilistic or continuous noise for adaptive experiments. This needs posterior semantics and a different termination theorem.
3. Performance. The Weyl Gröbner backend uses `Fraction` arithmetic without a chain criterion.
