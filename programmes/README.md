# Research programmes and milestone records

This directory imports the 2026-10-21 handoff programme documents and records what has been completed since. Code lives in `../extensions/`. Enveloped certificates live in `../results/`.

| File | Role |
|---|---|
| `PROGRAMME.md`, `TARGET_OBSERVERS.md`, `HAMILTONIAN_CORES.md`, `OBSTRUCTIONS_AND_ARITHMETIC.md`, `MODEL_COUNTEREXAMPLES.md` | The handoff programme, kept verbatim. |
| `TASKS.json` | The ordered tasks with their current status. |
| `CLAIMS_LEDGER.json` | Claims by status: retained results, implemented engines, certified computations, theorems and open targets. |
| `MACHINERY_MILESTONES.md` | C0, O1–O3 (including set-valued noise and metric search), S1–S3 (including integral Smith cohomology), A1–A2 (Pell orbits and units of both quadratic orders): theorems, certificates, retained counterexamples and scope. |
| `DYNAMIC_CORE_RESULTS.md` | W1–W4: the discovery backend, all-degree kernel certificates, certified cores, the six-parameter `qp³` theorem, the top-weight reduction lemma, homogeneous quartics, and the classification of quintic and sextic dynamic cores. |
| `EXTENSION_CHECKS.json` | The handoff's seed check list, kept as it was. `../extensions/run_all.py` supersedes it. |

## Next steps

1. Dynamic cores of homogeneous Hamiltonians of degree 7 and higher. The quintic/sextic argument (§3d of `DYNAMIC_CORE_RESULTS.md`) generalizes in outline: monomial classes, the top-weight lemma at roots of intermediate multiplicity, and static finiteness at a simple root followed by a chain argument. For degree `d ≥ 7`, however, the top cores at roots of multiplicity between 3 and `d − 3` still have to be computed, and the local static systems involve more variables.
2. Probabilistic or continuous noise for adaptive experiments. This needs posterior semantics and a different termination theorem.
3. Performance. The Weyl Gröbner backend uses `Fraction` arithmetic without a chain criterion.
