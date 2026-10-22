# Research programmes and milestone records

This directory imports the 2026-10-21 handoff programme documents and records what has been completed since. Code lives in `../extensions/`. Enveloped certificates live in `../results/`.

| File | Role |
|---|---|
| `PROGRAMME.md`, `TARGET_OBSERVERS.md`, `HAMILTONIAN_CORES.md`, `OBSTRUCTIONS_AND_ARITHMETIC.md`, `MODEL_COUNTEREXAMPLES.md` | The handoff programme, kept verbatim. |
| `TASKS.json` | The ordered tasks with their current status. |
| `CLAIMS_LEDGER.json` | Claims by status: retained results, implemented engines, certified computations, theorems and open targets. |
| `MACHINERY_MILESTONES.md` | C0, O1–O3 (including set-valued noise and metric search), S1–S3 (including integral Smith cohomology), A1–A2 (Pell orbits and units of both quadratic orders): theorems, certificates, retained counterexamples and scope. |
| `DYNAMIC_CORE_RESULTS.md` | W1–W3: the discovery backend, all-degree kernel certificates, certified cores, the six-parameter `qp³` theorem, the top-weight reduction lemma and homogeneous quartics. |
| `EXTENSION_CHECKS.json` | The handoff's seed check list, kept as it was. `../extensions/run_all.py` supersedes it. |

## Next steps

1. A uniform-in-degree proof that `D∞(H) = span{1,H}` for every binary quartic with distinct roots. What is already certified:
   - the per-degree theorem, for all `λ ∈ Q̄` and every degree in the certified range;
   - all-degree certificates at `λ = 0` and `λ = 1`.

   One candidate route is the `SL₂` decomposition of `T₃(H, T₁(H,·))` into transvectants with `H²`, the Hessian and the invariant.
2. Probabilistic or continuous noise for adaptive experiments. This needs posterior semantics and a different termination theorem. Deterministic and set-valued adversarial noise are done.
3. Performance. The Weyl Gröbner backend uses `Fraction` arithmetic without a chain criterion. Distinct-root quartics with generic `λ` take about 20 minutes each.
