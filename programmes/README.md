# Research programmes and milestone records

This directory imports the 2026-10-21 handoff programme documents and records what has been completed since. Code lives in `../extensions/`. Enveloped certificates live in `../results/`.

| File | Role |
|---|---|
| `PROGRAMME.md`, `TARGET_OBSERVERS.md`, `HAMILTONIAN_CORES.md`, `OBSTRUCTIONS_AND_ARITHMETIC.md`, `MODEL_COUNTEREXAMPLES.md` | The handoff programme, kept verbatim. |
| `TASKS.json` | The ordered tasks with their current status. |
| `CLAIMS_LEDGER.json` | Claims by status: retained results, implemented engines, certified computations, theorems and open targets. |
| `MACHINERY_MILESTONES.md` | C0, O1–O3, S1, S2 and A1: theorems, certificates, retained counterexamples and scope. |
| `DYNAMIC_CORE_RESULTS.md` | W1 and W2: the discovery backend, all-degree kernel certificates, certified cores, and the theorem for `qp³+αq²+βp²`. |
| `EXTENSION_CHECKS.json` | The handoff's seed check list, kept as it was. `../extensions/run_all.py` supersedes it. |

## Next steps

1. The six-parameter quadratic perturbation family of `qp³`. After normalization the `qp` coefficient is a continuous modulus, so it needs a parametric (comprehensive) Weyl Gröbner computation or a structural argument.
2. Homogeneous quartic dynamic-core moduli. `q⁴+p⁴` exceeds the default discovery budget. Possible routes are better pair criteria, signature-based completion, or an external backend such as Macaulay2 WeylAlgebras whose output is replayed by `weyl_receipts.py`.
3. An integer Smith-form backend for torsion. Rational answers stay rational.
4. Rational SDP search for invariant metrics. The exact checker already exists.
5. Fundamental-unit and maximal-order adapters for the Pell compiler.
