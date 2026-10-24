# Index of executable statements and boundaries

| Statement | Proof and checker | Scope |
|---|---|---|
| Centered emittance kick identity and sharp residual-force radius | `emittance/THEORY.md`, `exact.py`, 14 tests with predictor | Classical weighted clouds or distributions; fixed-position kick, unchanged measure. Established force projection, not a novelty claim. |
| Two-plane Schur covariance identity and positive-semidefinite residual block | `emittance/THEORY.md`, `exact.py` | Full transverse determinant versus projected emittance distinguished. |
| Conditional emittance-radius transport through a permitted word | `emittance/predictor.py`, `test_predictor.py` | Explicit per-kick force premises; rejects unsupported coupling/loss. No cheap physical premise generator established. |
| Minimal common physical-moment representation has dimension 25 for fixed nonzero shear, 9 for zero shear | `observables/THEOREMS.md` §1, `compiler.py`, `check_observables.py` | Prescribed classical cubic family with independently allowed generators and shared coordinates. |
| Adding the quadrupole control forces infinite common polynomial closure | `observables/THEOREMS.md` §2, obstruction replay | All-degree algebraic obstruction, not just a finite failed search. |
| Adding physical kinetic control forces infinite closure for nonzero shear | `observables/THEOREMS.md` §3 | Zero-shear exception preserved. Does not rule out approximate or nonpolynomial representations. |
| Two positive laws agree on all 25 retained moments but later differ in physical second moment and emittance | `observables/THEOREMS.md` §4, `results/missing_information_witness.json` | Explicit finite clouds and declared map word; no physical beam or smooth-density claim. |
| Shared quadratic backbone and local residual bound | `observables/THEOREMS.md` §5, `results/backbone_routes.json` | Common-shear condition checked; support and horizon amplification remain additional premises. |
| Unknown-label connected-grid bounds and strict Pareto exclusions | `../beam_ring/certificates/README.md`, independent union-find checker | Conditional on observed finite-grid labels. Neither continuous aperture nor infinite-time stability. |

The 114 checked generator/reconstruction identities support the implementation.
The all-degree conclusions follow from the displayed proofs, rather than from
a finite test sample. No Lean/formal-kernel verification or complete pure-top
classification is asserted.
