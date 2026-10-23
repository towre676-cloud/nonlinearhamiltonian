# Certificate-producing mathematics machinery

This directory holds exact tools built on one pattern. A **producer** searches. A separate **checker** replays exact identities and never calls the producer. A typed **envelope** binds the result to its model, coefficient domain (Q), hypotheses, scope and atlas sources.

Everything uses the Python standard library and `fractions.Fraction`. Floating-point input is rejected.

The 2026-10-21 handoff supplied the seeds. They are kept as they were, and the new layers sit beside them. Theorems, hypotheses and failure cases are written up in `../programmes/MACHINERY_MILESTONES.md` and `../programmes/DYNAMIC_CORE_RESULTS.md`. Claims are tracked in `../programmes/CLAIMS_LEDGER.json`.

| Area | Producer | Independent checker | Format |
|---|---|---|---|
| Minimal target observer | `observer/observer.py` | `observer/check_observer.py` | `observer-closure-v2` |
| Cheapest noise-aware panel | `observer/panels.py` | `observer/check_panel.py` | `noise-panel-v1`, `invariant-metric-v1` |
| Adaptive experiments | `observer/adaptive.py` | `observer/check_adaptive.py` | `adaptive-tree-v1` |
| Weyl discovery (dynamic cores) | `hamiltonian/weyl_groebner.py` | `hamiltonian/weyl_receipts.py` (seed) | `weyl-invariant-kernel-v1` |
| All-degree polynomial kernels | `hamiltonian/weyl_kernel.py` | `hamiltonian/check_weyl_kernel.py` | `weyl-kernel-v1` |
| Obstruction answers | `structure/obstruction.py` | `check_answer` in the same file (matrix products only), plus `structure/check_contraction.py` | `rational-obstruction-answer-v1` |
| DGLA Maurer–Cartan lifting | `structure/dgla.py` | `structure/check_dgla.py` | `dgla-lift-v1` |
| Supplied-unit Pell orbits | `arithmetic/pell.py` | `arithmetic/check_pell.py` | `pell-orbits-v1` |
| Envelopes | `envelope.py make` | `envelope.py check` | `machinery-envelope-v1` |

The handoff seeds are `observer/observation_closure_reference.py`, `hamiltonian/weyl_receipts.py`, `structure/contraction_seed.py`, `structure/check_contraction.py` and `counterexamples.py`.

## Commands

All commands run from the repository root.

```bash
python3 -B extensions/run_all.py                 # every suite, seed check and results replay
python3 -B extensions/run_all.py --quick         # skip the slow Weyl suite and the results replay
python3 -B extensions/build_results.py           # regenerate results/ (about 10 minutes)
python3 -B extensions/envelope.py check results/hamiltonian/qp3_plus_q2.json

python3 -B extensions/observer/observer.py compile extensions/observer/observation_example.json
python3 -B extensions/observer/panels.py solve MODEL.json --output CERT.json
python3 -B extensions/observer/check_panel.py CERT.json --input MODEL.json
python3 -B extensions/hamiltonian/weyl_groebner.py discover "q^3*p^3" --output R.json --kernel-degree 8
python3 -B extensions/hamiltonian/weyl_kernel.py R.json --output K.json
python3 -B extensions/structure/obstruction.py extensions/structure/triangle.json --degree 1 --cocycle '[1,2,-2]'
python3 -B extensions/structure/dgla.py lie --dim 3 --structure '{"0,1": {"2": 1}}' --output heis.json
python3 -B extensions/arithmetic/pell.py MODEL.json --output CERT.json
```

## Boundaries that the code enforces

- `unknown` and `incomplete` are never upgraded to a classification. A budget returns one of them.
- A bounded polynomial window (`--kernel-degree`) is labelled a diagnostic. All-degree kernel claims come only from `weyl-kernel-v1` certificates.
- Rational answers make no statement about integral torsion; `field: "Z"` is rejected.
- Invariant-metric certificates are sufficient conditions only. Failing to find one is reported as no certificate.
- Higher-order DGLA obstructions are relative to the declared jet. Only order 2 is intrinsic to the first-order class.
- Pell completeness rests on the written reduction proof. The checker re-enumerates the proved window.
