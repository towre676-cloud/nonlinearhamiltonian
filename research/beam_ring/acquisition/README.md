# Existing-method integration and finite MeanBAX acquisition

This directory contains our original adapter and finite-candidate pilot code.
It does not redistribute upstream source. The recorded upstream commit is
`82766c7fb22ec675025d6485ce11761cdc7a6056`; its actual root tree is
`28fb59254e24081c3cd02cc462a70b7ca769c183`.

## What has actually run

Ten minimal files from [SLAC-ML/mpBAX](https://github.com/SLAC-ML/mpBAX)
were downloaded privately and checked against their exact Git blob identities
and SHA256 hashes. Its unchanged basic example ran five loops and made sixty
quadratic-oracle evaluations. Our finite-table oracle, acquisition and small
surrogate then ran three loops on the **actual unchanged upstream Engine**,
making fourteen unique synthetic physical-callback evaluations. Checkpointing
and model persistence completed. `UPSTREAM_REPLAY.json` and the logs preserve
these results. Twelve behavioral tests passed; their source hashes and runtime
versions are in `ADAPTER_TEST_RECEIPT.json`.

The official framework's core requires NumPy and PyYAML. No Torch, BoTorch or
GPyTorch installation was needed. Its shipped `RandomSampling` and
`GreedySampling` algorithms do not implement the DAMA paper's acquisition.
Thus this smoke run establishes framework compatibility, not a reproduction
of that paper or its reported gain.

The pinned package metadata says MIT, but its root tree does not provide a
LICENSE file. We retain only identity metadata and our execution outputs here;
the inspected upstream source remains outside this repository. This records
the observed packaging gap rather than asserting that its authors forbid use.

## Selection rule and declared differences

The [DAMA paper](https://arxiv.org/html/2511.17850v1), Appendix A, uses a
deterministic MeanBAX heuristic: estimate acceptance objectives from surrogate
survival maps, identify promising Pareto configurations, then randomly acquire
points whose predicted lifetimes lie near their stability boundaries.

`FiniteMeanBAX` implements those selection steps on a frozen finite design set.
It estimates each objective using a supplied boolean-map callback, keeps all
maximization-nondominated rows, and samples unobserved boundary points without
replacement. If the boundary pool is empty, it explicitly falls back to uniform
unobserved points. A nonempty pool smaller than the requested batch is returned
without padding; the caller must account for actual query counts. Exhaustion
returns an empty batch.

This is a **method-level pilot**, with substantive declared differences: finite
candidate enumeration replaces continuous NSGA-II and its accumulated near-front
region; the small sklearn L-BFGS MLP replaces the paper's neural field and
training schedule; our optional origin-connected finite-grid objective replaces
the original acceptance metric; the empty-boundary fallback is explicit here.
The default surrogate cutoffs and lifetime intervals follow the paper, but they
are acquisition settings, never physical survival guarantees. MLP outputs are
clipped regression values, not calibrated posterior probabilities. Training
nonconvergence warnings remain in each fit receipt.

## Public interfaces

`FiniteMeanBAX(weights, batch_size, seed, objective_callbacks=...)` accepts one
`(design, launch)` prediction table and boolean observed mask per objective.
`select(predictions, observed)` returns `(objective, design, launch)` triples.
Only masks enter acquisition: truth labels stay with the physical oracle.
`last_selection` records estimates, candidate counts, chosen designs, fallback
reason and selection time. Equal objective vectors remain nondominated.

`SurvivalMLP.fit(X,y)` fits normalized lifetime fractions and
`predict(X)` returns an `(n,1)` array. `feature_table(designs, launches)` creates
the stable concatenated feature grid. `connected_weighted_score` supports an
origin-connected objective while preserving holes and excluding disconnected
islands; no radial monotonicity is assumed.

`FiniteTableOracle` adapts a frozen feature grid and physical
`query(design,launch)` callback to the upstream `X -> Y` interface. It separates
charged successful calls, failed calls and cache hits. Failed calls cannot mark
a point observed. `FiniteTableAlgorithm` connects these tables and policy to
the upstream Engine and refuses to accept validation-phase tables for learning.
These are software guards, not a proof against a malicious callback that leaks
validation data through another channel.

## Replay

From the project root:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python -m unittest discover -s research/beam_ring/acquisition -p 'test_*.py' -v
```

For the upstream integration replay, obtain the recorded upstream checkout
separately and give its local path. The script checks all ten expected files
before importing it, and requires a new output directory:

```sh
python research/beam_ring/acquisition/run_upstream_smoke.py --upstream-dir /path/to/mpBAX --output /tmp/new-mpbax-smoke
```

The synthetic replay validates protocol behavior only. Physical accuracy,
held-out quality and complete optimization cost are assessed separately by the
root ring experiment. No tenfold result is established in this directory.
