# Guarded fixed-momentum tracker: BNL review prototype

This contribution follows the accelerator application rather than changing to
an unrelated sector. It measures a genuine implementation gain on a BNL-authored
public lattice, with explicit limits. Read the short PDF under `output/pdf/`
and the original protocols/raw arrays before using the performance numbers.

## Measured result

In the independently frozen 64-point, 256-turn confirmation, the fastest
qualified existing workflow used PyAT's native `QuadLinearPass` and
`BendLinearPass`, with ten sextupole steps. It took **2.67630 s** for the first
workload. Our selected guarded compiler took **1.66487 s**, including an allocated
**0.12799 s kernel build**, native lattice construction, compilation, warm-up and
all 25 guard-triggered native reruns per repetition. The observed first-workload
gain is **1.6075x**; tracking with fallback alone is **2.0458x**.

Fifteen variants were declared before this confirmation. Qualification requires
zero survival-label errors where 40- and 80-step native references agree, and
maximum core position/momentum errors below 1 micrometre/1e-6 normalized
momentum. The selected method passes all 63 reference-agreement labels; point 48
is unresolved. Its maximum core position error is 0.368 micrometres. Coarse
native and analytic variants that fail remain in the evidence. Speedup ratios
for accuracy-failed methods are suppressed by the independent replay.

The much larger **15.22x** ratio against uniform native40 is not the headline:
existing analytic passes already remove much of that cost. No tenfold advantage
over the strongest tested workflow, industrial optimization gain, operating
machine equivalence or BNL endorsement is established.

Reference generation cost **75.00257 s**, reported separately. The full measured
15-method confirmation campaign cost **164.77285 s**, including all executions,
setups, warm-ups and one kernel build; earlier exploration is additional. Either
cost erases the online saving in one fresh calculation. Conditional accounting
gives 58 distinct future equal-cost batches for reference-only costs, and **126
additional batches** to repay the measured confirmation campaign. Those counts
assume reusing the qualified configuration without further validation costs;
identical repeated inputs can be cached and do not demonstrate amortization.
Cold interpreter/package startup, installation and final report serialization
are excluded from per-method times. Confirmation methods ran sequentially on one
host; fast methods have three timing repeats, not three independent deployments.

## Longer check and numerical uncertainty

A separately frozen **post-selection** check reused the original 128 launches
and 512 turns. The selected method passed the stated fine-pair gate, with
0.726-micrometre core position error. Added ordinary analytic20/40 comparators
also passed; analytic20 cost 14.13526 s versus 3.66249 s for the selected compiler,
an observed 3.86x ratio. The ordinary extension has one timing only and was added
after selection, so this is not a second independent confirmation.

Follow-up diagnostics expose a critical limit of the gate. Backcheck point 41
survives native40 and native80, is lost with native160, then survives native320.
Confirmation point 48 also changes classification with refinement. No one
refinement is treated as continuum truth. **Fine-pair agreement is not a proof
of physical convergence**, and the boundary cases remain refinement-sensitive.
The frozen gate is not rewritten to conceal this later finding.

## Mathematical mechanism and model scope

At fixed delta, eligible linear-field bends, pure quadrupoles and drifts are
affine in the four transverse coordinates in the selected PyAT paraxial model.
The compiler composes the actual split-step matrices, retaining all thick
sextupoles. The selected configuration keeps 40-step linear-body maps and four
sextupole steps. A native C pass combines each matrix with its domain guard;
guard rejection is uncertainty and requires a charged native rerun. The BNL
model reduces from 3,030 to 631 elements. This uses established matrix transport
and specialization, not a claim of inventing linearization or optimization.

The independently audited real-arithmetic identities and finite-kick machinery
are the direct connection to the repository's exact-backbone/observer approach.
They do not imply quantum Moyal exactness or a complete pure-top classification.
The floating guard bounds have a large margin but are not outward IEEE
certificates. Independent element tests cover 108 family/momentum cases with
100 points each; the maximum transverse residual is 6.94e-18. The custom C
kernel passed 100 accepted points and three rejection cases. An exact rational
bound controls the removed linear ct increments over 4,096 turns, but full ct
evolution is not preserved and complete nonlinear/IEEE equivalence is unproved.

The source is `NSLS2/PyELEGANT/demo/nsls2cb65pm.lte`, pinned to commit
`11d97113ea7ae05fd0ffe710a88793f2bdc9ed84` and retained with its BSD license.
It is a historical complex-bend demonstrator, not current NSLS-II operations:
3 GeV, 791.958 m, fixed delta0, no RF/radiation/collective effects/errors or
mechanical apertures. The importer defaults to ten integration steps despite
the LTE's N_KICKS=40; matching nominal counts does not prove ELEGANT equivalence.
No native-ELEGANT cross-code validation was available.

Only this declared scope is qualified. The frozen generic helper has unsupported
cases including MaxOrder0 with nonzero higher stored coefficients and arbitrary
retained ct-coupled custom maps. Do not treat it as a general six-dimensional
drop-in tracker. A new lattice, momentum, error model, aperture or readout needs
separate qualification. The prototype does not communicate with machine controls.

## Replay and build

From this directory, offline confirmation audit needs only NumPy:

```sh
python check_results.py --output /tmp/bnl-audit.json
python -S audit/check_ct_bound.py --model nsls2cb65pm.lte
```

All original numerical arrays, snapshots, failures and later diagnostics are
inside `results/recorded_campaigns.zip`, with a per-member SHA-256 manifest.
`check_results.py` reads without extracting or loading pickles. An additional
independent verifier in `benchmarks/verify_results.py` accepts a relocated
extracted data root and checks confirmation, backcheck and diagnostic additions.

For live replay, use Linux/GCC and an isolated Python environment:

```sh
python -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python build_kernel.py --receipt /tmp/bnl-kernel-build.json
python replay_confirmation.py --build-receipt /tmp/bnl-kernel-build.json --output /tmp/new-bnl-confirmation
```

Alternatively install dependencies with `pip --target /path/to/runtime` and pass
`--runtime` explicitly. The launcher uses the fresh machine's build receipt;
historical build time is not silently reused. Replays reject existing output
directories. Vendored Apache-2.0 interface headers and portable C source are
included; no binary download or upstream kernel replacement is required.

## Review request

The immediate useful next step is independent testing against a BNL-maintained
lattice and acceptance contract, including relevant momentum offsets, errors,
apertures and horizon. BNL already develops square-matrix, chaos-indicator and
ML-assisted optimization methods; this packet proposes a qualified tracking
implementation to assess alongside those workflows. It does not ask staff to
accept a national-scale or operating-performance claim. No staff have been
contacted by this workflow.
