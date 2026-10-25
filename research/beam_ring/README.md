# Public-ring oracle and finite-candidate acquisition pilot

This is an executed first implementation, not a reproduction of the published
SSRL-X DAMA-BAX result or a tenfold industrial gain. It uses the public HMBA
lattice already ingested by `research/beam_literature/`, Accelerator Toolbox
0.9.0, all 32 cells per turn, 6 GeV, and no RF, radiation, collective force or
magnet errors. No mechanical apertures were added; the loss rule is the native
PyAT element/aperture/numerical check. Source identity is checked before tracking.

## What was frozen and executed

`protocol.json` was serialized before new survival labels were generated. Nine
designs vary six named sextupole coefficients in a numerical four-dimensional
chromaticity-response nullspace. Mirror symmetry may be broken. The selected
designs and 16 control-box corners were checked numerically; the largest corner
chromaticity departure was about 1.32e-6. This is no uniform interval theorem.

The two objectives are normalized origin-connected survival counts on declared
entrance grids: x/y and relative momentum. Learning uses 45+17 launches and 64
full turns; final validation uses 91+25 launches and 256 turns for two selected
designs. These are finite-grid scores, not continuous dynamic aperture or
longitudinally resolved momentum acceptance. Validation grids/horizons are
withheld from acquisition. No error seeds or global validation optimum were
evaluated.

| Method | Learning point evaluations | Final point evaluations | Reported charged seconds | Selected designs |
|---|---:|---:|---:|---|
| Full grid | 558 | 232 | 91.782 | 1, 8 |
| Exact connected-frontier search | 506 | 232 | 94.535 | 1, 8 |
| Uniform sampling with surrogate | 144 | 232 | 69.590 | 4, 2 |
| Finite-candidate MeanBAX heuristic | 106 | 232 | 66.459 | 2, 8 |

All 2,242 physical point evaluations are retained with protocol hashes, stages,
loss turns/elements, batched-call timings and selection records. Times include
per-method construction, tracking, training, acquisition and certificate checks,
plus a charged copy of protocol preparation. They exclude installation, cold
imports, development and final event/result-log serialization. The host was
shared with verification tasks; these are pilot timings, not dedicated-machine
performance estimates or a matched-quality speedup claim.

The exact frontier search recovered every exhaustive learning objective while
leaving 52 irrelevant labels unknown. Smaller batches erased the runtime saving.
The momentum score saturated at 1.0; this is not a demanding two-objective task.
Longer/denser validation changed rankings: the coarse-grid winners scored about
0.615/0.604 in x/y, while uniform sampling selected designs scoring about
0.637/0.659 and MeanBAX selected about 0.659/0.604. The MeanBAX run underfilled its
boundary batches; actual calls, not the maximum budget, are charged. Every MLP
fit retained its convergence warning. No superiority over the stronger ordinary
surrogate workflow is established.

## Method adoption and mathematical decisions

The pinned public `SLAC-ML/mpBAX` Engine ran its unchanged small example and our
plugin, but its shipped Random/Greedy selectors are not the DAMA paper's MeanBAX
implementation. [acquisition/README.md](acquisition/README.md) records this gap.
The live pilot ports the paper's deterministic Pareto-boundary sampling idea;
finite enumeration replaces NSGA-II and a small sklearn MLP replaces its neural
field. The changed objective is explicit. These differences prevent a paper
reproduction claim. No external source is redistributed without a verified
license; private inspected source has pinned identities.

The independent finite-grid checker uses exact rational bounds and a different
graph algorithm from the producer. [certificates/README.md](certificates/README.md)
gives its proof and exhaustive small-grid tests. `verify_pilot.py` binds each
grid, weight, origin and observed event to the frozen protocol, then combines
the **connected** objectives across the two grids. Per-grid certificates also
contain raw-survival objectives; their separate exclusions are not interpreted
as exclusions for the combined tuning objective. Hashes bind provenance and do
not prove that the numerical simulator labels are physical truth.

## Replays and historical source identity

Offline audit, without PyAT or new tracking:

```sh
python -B -S research/beam_ring/verify_pilot.py --output /tmp/ring-audit.json
```

The campaign's four executed source files are retained byte-for-byte in
`results/pilot/source_snapshot/`; their hashes match `execution_frozen.json`.
After the campaign, the public oracle was hardened to detach caller mutations,
validate protocols and retain failed tracking-call costs. Six additional tests
and a separate live regression check this version. Historical labels are not
retroactively attributed to the later version.

Two separate 48-point live oracle regressions are retained with their own source
hashes; the final one checks the current hardened version. Individual and batched
loss labels/elements agree and deterministic prefix checks pass for those points.
The installed PyAT recursive acceptance API also ran successfully, in about
2.71 seconds on its declared nominal probe. Its radial-boundary metric differs
from the Cartesian connected-grid objective; no speedup ratio is formed between
them. See `results/pyat_recursive_probe.json`.

For new tracking, install the pinned ring dependencies in an isolated environment:

```sh
python -m pip install -r research/beam_literature/requirements-ring.txt
python -m pip install -r research/beam_structure/requirements.txt
python research/beam_ring/check_live_oracle.py --output /tmp/new-oracle-check.json
python research/beam_ring/run_pilot.py --output /tmp/new-ring-pilot
```

An optional `--runtime /path/to/isolated/dependencies` supports an existing target
directory. Existing campaign output paths are rejected. For a changed experiment,
write a new protocol first; do not change this frozen pilot retrospectively.

The next performance experiment needs a qualified, nonsaturated momentum
objective, longer-horizon/grid convergence, more than one optimization seed,
strong production adaptive/batched comparators and a matched-quality stopping
contract. The source-bound oracle, query ledger and decision checker now exist
to support that experiment.
