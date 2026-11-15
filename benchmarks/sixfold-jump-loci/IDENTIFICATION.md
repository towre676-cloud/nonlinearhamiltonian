# Recovering sixfold refinement depth from trajectories

Benchmark base [PR #46](https://github.com/towre676-cloud/nonlinearhamiltonian/pull/46),
commit `271543d4ff48b11da687068b724e3d3a675daa89`.

## Reproduction and split audit

The regenerated data matched the four published SHA-256 digests. The original
nearest-trajectory predictions and report reproduced byte for byte.
The benchmark verifier checked exact labels, obstructions, and group isolation.
An independent scorer rebuilt the pair lists, verified each exact coefficient
change, and agreed with the published scorer on every reported stratum,
perturbation magnitude, and noise level. A pair counts only when the depth-two
member receives 2 and its matched near-miss receives 1. An abstention on
either side leaves that pair in the denominator. Each depth-two member
appears in three pairs. There are 15 test groups and 45 test pairs, with
three test groups per jump stratum.

The quartic validation axes are p³, q²p and q⁴p. The quartic test axes are
q³p², q⁴ and q⁵. Calibration therefore transfers across disjoint quartic
perturbation axes. The published split is preserved.

## Estimators

- **Raw nearest** compares time-binned positions. Its 49-frame selective
  predictions reproduce the benchmark baseline.
- **Local field nearest** fits local cubic position and velocity estimates.
  It reconstructs a degree-five Hamiltonian correction by joint least
  squares on q̇ and ṗ, then compares its coefficient vector with training
  vectors using fixed monomial scaling.
- **Weak field nearest** uses the same coefficient library in integral
  equations. For each track, the test functions are the time primitives of
  the first six nonconstant Legendre polynomials. The primitives vanish
  at both endpoints. Integration by parts moves the derivative onto
  the test function. The estimator uses quintic interpolation for clean
  tracks and a degree-six time regression for noisy tracks.
- **Weak locus** evaluates numerical residuals of the rational jump-locus
  equations and depth-six equalities. It uses the Jacobian of the constraints
  and the inverse information from the moment fit to estimate a distance to
  each locus. These distances are linearized diagnostics. Errors in the
  smoothed regressors, overlapping branch closures, and near-singular
  constraint Jacobians limit their statistical interpretation.
- **Guarded weak locus** uses detectable leading coefficients to restrict
  candidate branches in theorem order. In particular, it requires a
  detectable β before considering the cleared gamma conditions. This
  prevents the degenerate gamma equations from accepting some origin
  near-misses. An ambiguous support decision can still miss the true branch.
- **Regularized weak locus** shrinks the noisy weak estimate with a covariance
  fitted to clean training trajectories. It propagates the corresponding
  Gaussian approximation through the guarded tests.
- **Calibrated weak locus** fits a balanced ridge classifier to log distances
  using training labels.

The trajectory track uses the published Hamiltonian form with a fixed q⁶
term. The constant term is unobservable. Test cases are predicted individually
from the given time grid, noise level and six tracks at that level. IDs are
used for label joins and scoring. Validation labels calibrate cutoffs.
The rule-based methods choose a locus tolerance by validation macro recall.
Each confidence cutoff targets 80% overall validation accuracy among at
least five answered cases, with full abstention when no cutoff qualifies.
This target provides no held-out accuracy guarantee. Scores are also
reported with forced decisions to show the effect of abstention.

Group IDs, exact coefficients, true strata, perturbation axes, offset
magnitudes and test labels are excluded from fitting. The benchmark
design and all labels are public, and this is an exploratory comparison
on the published split. The branch guard is a follow-up to the first
locus experiment. An independent set of groups and noise realizations
is needed to estimate generalization.

## Full observation window, selective decisions

The window is 0.18 time units and 49 frames per track. There are 15 pairs
at each magnitude. Pair coverage requires both decisions. Case coverage
and selective accuracy use the 63 individual test Hamiltonians.

| Noise σ | Baseline pairs correct | Guarded pairs correct by magnitude 0.1 / 0.001 / 0.00001 | Guarded pairs answered | Guarded case coverage | Guarded case selective accuracy |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | 0/45 | 15/15 · 15/15 · 14/15 | 45/45 | 63/63 | 62/63 (98.4%) |
| 0.00001 | 0/45 | 2/15 · 0/15 · 0/15 | 11/45 | 31/63 | 22/31 (71.0%) |
| 0.001 | 0/45 | 0/15 · 0/15 · 0/15 | 25/45 | 39/63 | 30/39 (76.9%) |
| 0.01 | 0/45 | 0/15 · 0/15 · 0/15 | 2/45 | 5/63 | 3/5 (60.0%) |

On clean tracks the guarded estimator answered all pairs, with 8/9 correct
on the quartic edge and 9/9 on each of c32, delta, gamma and origin.
It recovered all three depth-six anchors. The two selective successes at
σ = 0.00001 belong to gamma and origin, both at magnitude 0.1.

## Observation length and forced decisions

Each cell gives the count of correct test pairs out of 45 in ascending
noise order. The full replay reports coverage, selective accuracy, and
pair outcomes for each duration, noise, stratum and magnitude. Prefixes
change both the duration and the number of samples.

| Method | 0.045 time units, 13 frames | 0.09 time units, 25 frames | 0.18 time units, 49 frames |
| --- | --- | --- | --- |
| Raw nearest | 0 / 0 / 0 / 6 | 0 / 0 / 2 / 6 | 0 / 0 / 0 / 5 |
| Local field nearest | 2 / 2 / 10 / 9 | 2 / 4 / 7 / 8 | 2 / 4 / 13 / 7 |
| Weak field nearest | 2 / 5 / 0 / 6 | 2 / 2 / 8 / 5 | 2 / 3 / 12 / 5 |
| Weak locus | 33 / 7 / 7 / 0 | 32 / 20 / 9 / 6 | 32 / 7 / 2 / 3 |
| Guarded weak locus | 42 / 0 / 0 / 0 | 42 / 17 / 0 / 0 | 44 / 10 / 0 / 0 |
| Regularized weak locus | 42 / 4 / 0 / 0 | 42 / 12 / 0 / 0 | 44 / 11 / 1 / 3 |
| Calibrated weak locus | 14 / 6 / 7 / 6 | 15 / 5 / 4 / 4 | 17 / 9 / 3 / 9 |

Longer observation improved the clean guarded result. At nonzero noise
the gains were nonmonotonic and sensitive to the decision rule. For example,
the unguarded weak locus recovered 20 pairs with forced decisions at
σ = 0.00001 over 25 frames, with zero complete pairs after abstention.
The regularized rule abstained on all noisy cases at 49 frames. The local
field rule recovered 13 pairs with forced decisions at σ = 0.001 over
49 frames and zero under selective scoring. Those forced decisions can
count incidental splits between noisy observations and should be read
alongside the corresponding selective and per-depth results.

## Coefficient uncertainty and the exact track

For the full window, the median per-case maximum absolute coefficient
error in the weak fit was 1.20×10⁻⁸, 0.0527, 5.93 and 40.45 across the
four noise levels. The clean column-scaled field design had median
condition number about 1,213. Short arcs and high-degree monomials make the
inverse coefficient problem sensitive to errors in position.

A post-scoring binary oracle quantifies the measurement limit given both
exact clean track means, known pair membership and equal priors. For means
separated by Euclidean distance d and Gaussian coordinate noise σ, the
optimal individual-case accuracy is Φ(d/(2σ)). At 49 frames and σ = 0.01,
its mean accuracy is 83.48% at offset 0.1, 50.80% at offset 0.001 and
50.008% at offset 0.00001. At σ = 0.00001, even the oracle averages only
56.79% on the smallest offset, while averaging 99.92% on the middle
offset. This is an individual binary discrimination result under extra
information. It does not score complete pairs. The middle-offset result
at the smallest nonzero noise points to an estimator gap.

The exact-input control supplied the rational coefficients to the theorem
classifier and verified 63/63 depths. The separate candidate replay
rationalized coefficients reconstructed from clean 49-frame observations,
reintegrated the proposed polynomial against each observed track, and
applied the existing exact classifier to candidates passing a fixed
2×10⁻⁸ maximum coordinate-error tolerance. Where an explicit longer-lived
partner was available, it recorded the exact T3 and T5 polynomials at its
first failing iterate. The theorem classification supplies the corresponding
upper bound on candidate depth.

Of 63 clean cases, 59 candidates passed the numerical replay. Their exact
depths matched the reference in 56 cases, and their rational coefficients
matched exactly in 27. Four cases yielded no replayed candidate. Three
replayed candidates had the wrong reference depth. Thus a symbolic
certificate establishes a property of the proposed rational polynomial.
Claiming it for the generator would additionally require identification
assumptions that exclude nearby polynomials of other depths. In particular,
a neighborhood of a jump locus can include both depth-one and depth-two
members. A small numerical residual cannot certify exact locus membership.

## Replay

From this benchmark directory, with Python 3.12 and the pinned dependencies:

```sh
python generate.py data
python verify.py data
OPENBLAS_NUM_THREADS=1 python experiment.py data identified
```

The experiment writes `results.json`, `predictions.json` and
`candidate_certificates.json`. The proposed benchmark workflow reproduces
these outputs alongside the existing data verification.
