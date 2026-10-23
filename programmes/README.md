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

1. Pure tops (`DYNAMIC_CORE_RESULTS.md` §§6.8–6.13). The original two-root conjecture is false for pure tops; balanced and near tops are proved. The gauge form of the triangular gates (§6.10) settles the affine shear phase diagram, every non-affine first edge above the slope threshold, the boundary edge, every threshold edge with `deg w ≥ 3` (Theorem NT) and every edge below the threshold together with the flat lower terms (Theorem NV). What remains of Conjecture P004 is listed at the end of §6.4: linear `b`, linear or perfect-power transverse tops, and upper bounds for K2, K3 and K1′ (`deg a = 3`). A careful literature review (§6.13) is still needed before any positioning claim.
2. Probabilistic or continuous noise for adaptive experiments. This needs posterior semantics and a different termination theorem.
3. Performance. The Weyl Gröbner backend uses `Fraction` arithmetic without a chain criterion.
