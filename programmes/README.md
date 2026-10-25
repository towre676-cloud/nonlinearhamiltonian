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

1. Pure tops. Two independent lines now coexist. The core-overlap line (`DYNAMIC_CORE_RESULTS.md` §§6.8–6.22, `research/core_overlap/`) proves PP, QC, SC, SS, SCP, CQ, HR and the full affine cubic-phase sector CP, and lists its remaining targets in `research/core_overlap/CLAUDE_HANDOFF.md`. The check_gauge line (§§6.18, 6.23–6.28) proves P005: every pure top has `D∞ = span{1, H}` or the exact span of one of K1, K1′, K2, K1+K2, the extended K3 (with `βG`) or K4, including the non-affine cubic phase (Theorems NT with `e = 2` and NQ). Both P003 and P004 are false as stated. Next step: an independent audit reconciling the two lines (the test suite already compares both classifiers against direct computation). Historical priority and a careful literature review (§6.27) remain open.
2. Probabilistic or continuous noise for adaptive experiments. This needs posterior semantics and a different termination theorem.
3. Performance. The Weyl Gröbner backend uses `Fraction` arithmetic without a chain criterion.
