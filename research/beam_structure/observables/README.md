# Adapted common-observable compiler

This executable building block uses exact `Fraction` polynomials to discover
and certify a common classical observable space for prescribed controls. Its
specific family has a fixed canonical shear `Q=q, P=p+c*q**2` and Hamiltonians
`P**3/3`, `Q`, `Q*P`. The minimal common summary for all physical first and second
moments has dimension **25 for nonzero c**, and **9 for c=0**. The certificate
contains action matrices and physical output reconstructions.

[THEOREMS.md](THEOREMS.md) proves these dimensions, two all-degree control
obstructions, a positive-particle-cloud missing-information witness, and the
quadratic-backbone residual route. The obstruction is useful diagnostic output:
adding a quadrupole breaks every finite common polynomial closure containing
these outputs. A physical kinetic control does the same when the shear is
nonzero. The finite-word compiler remains available when global closure fails.

From the repository root, all commands use only the Python standard library:

```sh
python -B -S research/beam_structure/observables/run_observables.py
python -B -S research/beam_structure/observables/check_observables.py
python -B -S -m unittest discover -s research/beam_structure/observables -p 'test_*.py'
```

`run_observables.py --output NEW_DIRECTORY` rebuilds the certificates and test
receipt. `check_observables.py --results DIRECTORY` checks source/result hashes,
the declared generator matrices, reconstruction formulas and positive-cloud
witness, without rerunning reachable-space discovery. `results/` includes both
certificate branches, the obstruction witnesses, backbone routes and exact
finite-word pullbacks. No downloaded model or external solver is executed.

The API entry points are `compile_family`, `check_certificate`,
`first_missing_image`, `finite_word_pullback`, `quadratic_backbone`,
`shared_backbone`, and `residual_observable_bound` in `compiler.py`. The first
function defaults to shear `1`. Coordinates and units are formal canonical
coordinates; mapping a physical beam's slopes to canonical momenta requires an
explicit normalization. Matrix rows represent `L(phi_i)=sum_j M_ij phi_j`, with
physical sign `L(F)=H_P*F_Q-H_Q*F_P`.

This is a structural model and exact checker, not a validated replacement for
PIC. It assumes prescribed generators sharing a fixed shear. Self-consistent
space charge, beamline acceptance, full phase-space caps and error propagation
require additional premises. Classical closure is separate from quantum
exactness. No measured computational or industrial speedup is claimed.
