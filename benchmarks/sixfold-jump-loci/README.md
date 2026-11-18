# Sixfold Hamiltonian jump-locus benchmark

A synthetic benchmark for detecting a change in the exact refinement depth
when a single Hamiltonian coefficient changes. There are 60 groups across
five rational jump strata. Each group contains one depth-two model and three
depth-one near-misses, one each at coefficient offsets of magnitude 0.1,
0.001 and 0.00001. Twelve separate depth-six models anchor the upper end of
the refinement scale. The 252 models are distinct. They are a designed sample,
so class frequencies have no interpretation as population prevalence.

| Stratum | On-locus groups | Single coefficients changed |
| --- | ---: | --- |
| Quartic edge | 12 | Five graph coefficients or the leading mixed coefficient |
| Cubic coefficient of momentum squared | 12 | Coefficient of p³, qp³, or qp² |
| Cubic form, delta locus | 12 | Coefficient of q³p |
| Cubic form, gamma locus | 12 | Coefficient of q⁴ |
| Cubic form, both q and q² survive | 12 | Coefficient of q³p |
| Depth-six anchors | 12 | Separate examples with cubic shear and cubic restoring potential |

## Get the data

The exact catalog and reference manifest are checked in under `reference/`.
Run `python generate.py data` to reconstruct all trajectory arrays locally.
The repository’s Sixfold benchmark workflow also builds and uploads a
complete benchmark artifact.

## Exact track

`data/exact.jsonl` gives the ground truth. Polynomial terms are triples
`[q exponent, p exponent, exact rational string]`. Unlisted terms are zero.
All Hamiltonians have leading term q⁶ and are expressed in the original
canonical coordinates. The field for these instances is the rationals.

Each row records the branch, split, least depth, persistent-core dimension,
window dimensions through the stage after stabilization, and explicit probes.
For depth two, the probes form a basis of the extra first-refinement directions
modulo 1 and H. A depth-one near-miss carries the probes from its depth-two
partner, now with first failure at iterate one. For depth six the probes are
q and the sheared momentum, with first failures at iterates six and five.
The stored T3 and T5 polynomials are full exact obstructions at the first
nonzero iterate. The certificate convention is Df = T1(H,f) = H_q f_p − H_p f_q.
Membership in S^r means both gates vanish for iterates 0 through r.

The depth labels use the stated theorems, with exact kernel dimensions on the
corresponding windows as a cross-check. The bundled theorem notes explain the
completeness arguments. The degree-12 windows for depth-six anchors are
cross-checks of those examples. Neither the numerical trajectories nor rank
checks on arbitrary degree windows establish the universal theorem.

The weight-four system is included in `sources/` as a separate symbolic
challenge. Its necessary quadratic excludes rational instances. The benchmark
assigns it no positive witness or numeric score.

## Trajectory track

Use only the trajectory arrays and the permitted training labels when running
a trajectory-only method. Split membership is assigned by whole perturbation
group. The train, validation and test sets contain 126, 63 and 63 models
respectively. Reserve validation for fitting thresholds and picking methods.
The full answer key and generator are public in this package, so the test
split is a reproducible holdout protocol rather than a private challenge.

Each `trajectories_<split>.npz` contains:

- `ids` with opaque case identifiers, in array order.
- `t` with 49 time points from 0 to 0.18.
- `noise_sigma` with the four levels 0, 0.00001, 0.001 and 0.01.
- `qp` with shape `[model, noise, initial condition, time, coordinate]`,
  using six shared initial conditions and coordinate order q, p.

The clean trajectories use Hamilton's equations (q̇ = H_p, ṗ = −H_q) and DOP853. Noise is
independent additive Gaussian measurement error in both coordinates at each
sample, including the initial sample. Noise level and coefficient offset form
a crossed design. Clean tracks are finite-time simulated measurements with
numerical integration error. The observed maximum scaled energy drift was
3.48e−9. The initial conditions and time horizon define the observation
protocol and its limits. The data are synthetic and do not assess performance
on experimental observations.

The trajectory task is to predict depth 1, 2 or 6, or abstain. Supply one JSON
line per case and noise level with keys `id`, `noise_index` and `depth`
(use JSON null to abstain). Score both members of each pair together, by
absolute coefficient perturbation and noise level. Coverage is the fraction
answered. Selective accuracy uses only answered cases. Both-correct fraction
uses every pair, including those with abstentions, as its denominator.
Per-depth metrics help account for the deliberate 3-to-1 near-miss ratio.

The included nearest-trajectory baseline tunes an abstention threshold on
validation for each noise level. It correctly distinguishes zero of the 45
test pairs at each of the four noise levels. Its overall selective accuracy
is 75–78% at 19–37% coverage. This is a result for this baseline and observation
protocol. It leaves open what a better estimator can recover.

## Physics-informed identification study

The [identification study](IDENTIFICATION.md) compares local derivative fits,
weak Hamiltonian regression, branch-aware numerical tests, and selective
decisions across the published holdout and three observation durations.
It includes a post-scoring exact-coefficient control and a separate symbolic
replay of rational candidates inferred from clean tracks.

```sh
OPENBLAS_NUM_THREADS=1 python experiment.py data identified
```

The output directory contains the full per-noise, per-stratum and per-offset
test scores, prediction records, and candidate certificates.

## Observability note

[OBSERVABILITY.md](OBSERVABILITY.md) derives the trajectory sensitivity of the delta locus
along q³p, an explicit remainder bound, known- and unknown-background discrimination limits,
a preregistered initial-state design, an abstention rule in place of exact-membership claims, and a
constrained profile-likelihood estimator confirmed on fresh held-out groups.
Run `sh observability/run_all.sh` (one minute) and `sh observability/run_estimator.sh` (about 45 minutes).
For a quick audit of the bundled estimator records, run `python observability/verify_saved.py`;
`python observability/score.py` independently regenerates their score summary. These quick checks
do not rerun nonlinear fitting. The full estimator replay resumes existing case records; use a clean
copy with `observability/out/estimator/calibration.jsonl` and `confirm.jsonl` removed to refit every case.

The [guarded-pipeline diagnosis](OBSERVABILITY.md)
traces the large-offset selective failure to abstention: forced decisions already separated 3/3 original
and 72/72 fresh design-A pairs. Run `sh observability/run_diagnosis.sh` for the diagnostic replay
(about four minutes with a clean feature cache), or `python observability/verify_diagnosis.py` to audit
the saved case grid, frozen confirmation hashes and cutoff mechanism. These ablations do not establish
an improved selective rule.

## Reproduce

Use Python 3.12 with the supplied dependency pins.

```sh
python -m pip install -r requirements.txt
python verify.py data
python evaluate.py data
python evaluate.py data --predictions baseline_predictions.jsonl
python generate.py reproduced
```

The generator verifies exact labels, independent partner counts and
obstructions before simulating trajectories. `data/manifest.json` records
the seed, versions, split counts and SHA-256 data digests. Reproduction of
floating-point bytes across platforms may depend on numerical libraries.
`verification.log` records the integrity replay. `baseline_report.json`
contains the per-stratum and paired scores.

Source provenance is [Theorem J, PR #45](https://github.com/towre676-cloud/nonlinearhamiltonian/pull/45),
commit `9695137deed389d619938c02216c4e8daa73ca20`, stacked on
[PR #44](https://github.com/towre676-cloud/nonlinearhamiltonian/pull/44).
`sources/` retains the referenced theorem notes, classifier and weight-four
system from the patch. This release package contains no Lean claim for Theorem J.

SHA-256 of the original review ZIP: `7785d41af9c45b5401f0c177a7944b2c44fa1c6b6e66a6111827fdcb739b729f`.
