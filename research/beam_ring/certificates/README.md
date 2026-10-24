# Exact decision bounds on a finite survival grid

This layer accepts a declared graph, nonnegative rational cell weights, an
origin, design identities and finite turn horizons. Each supplied observation is
survived (`1`), lost (`0`) or unknown (`-1`). A surrogate prediction stays unknown
unless a separate valid argument establishes its label. The layer certifies
consequences of the supplied observations; it does not certify that a simulator
or a source string reported physical truth.

`grid_bounds.py` produces bounds. `check_grid_certificate.py` independently
reconstructs horizon consequences and uses union-find plus integer weighted sums
to check them. The producer instead uses breadth-first search and rational sums.
Both share strict input validation and SHA-256 binding to the manifest and event
documents. Physics, lattice hash, seed policy, launch coordinates and loss rules
belong in the manifest's `physics` object; changing it invalidates the certificate.
Hashes bind the supplied documents, not an independently attested experiment.

Both objectives are explicit finite-table functions. `survival_weight` adds the
weights of every surviving cell. `origin_connected_weight` adds only the
surviving graph component containing the origin. Neither fills an enclosed lost
hole, nor presumes radial monotonicity. A disconnected surviving island is
included in the raw sum and omitted from the origin component. An unknown bridge
can make that island possible in the upper connected bound. If the origin is
unknown the lower component is empty; if it is lost both components are empty.
Cell weights may represent a declared quadrature, but these exact table results
alone do not bound a continuous area between grid points.

## Bound and exclusion proofs

For a fixed design and horizon, let `S` be the known survivors, `U` the unknown
cells and `Z` the known losses. Every admissible surviving set is between `S`
and `S∪U`. With nonnegative weights, the weighted sum is monotone under set
inclusion. The component reachable from the origin is also monotone: every path
in a subset remains a path in a superset. Evaluate both objectives at `S` and
`S∪U` to obtain exact lower and upper bounds. Each endpoint is attained by
assigning all unknowns zero or all unknowns one. The bounds are therefore tight
given these partial labels alone; no assumption on the survival boundary enters.

For maximizing objective vectors, design `A` can safely exclude design `B` if
every lower bound of `A` is at least the corresponding upper bound of `B` and
at least one is strictly larger. Every completion then makes `A` strictly
Pareto-dominate `B`. Equal vectors do not justify exclusion. The certificate
reports every ordered design pair satisfying this rule at each horizon. This
initial schema uses the raw and connected scores as its two components;
`pareto_excludes` also handles arbitrary explicit rational bound vectors.

For one deterministic trajectory with the same initial state, lattice, errors,
physics and cumulative loss convention, a loss by a short horizon persists at
longer horizons. Survival at a long horizon entails survival at shorter ones.
Survival at a short horizon does **not** establish long-horizon survival.
Reinjection, changed errors or a different launch condition violate the declared
prefix semantics and require a different design/manifest. Conflicting events
are rejected, including a short loss paired with a longer survival. Duplicate
observation keys are rejected even when identical; callers must deduplicate
their oracle log before certification and keep the original charged-call log.

These are elementary monotonicity and finite-graph facts, not a new general
algorithm or a proof of continuous or infinite-time accelerator stability.

## API and replay

The Python API is `make_manifest(cells, adjacency, weights, origin, designs,
horizons, physics=None)`, `objective_bounds(manifest, labels)`,
`certify(manifest, events)` and `check_certificate(manifest, events, certificate)`.
IDs are nonempty strings. Adjacency is a symmetric dictionary of neighbor lists;
weights are integers, rational strings or Python `Fraction` values passed through
the constructor. JSON documents contain rational strings, never binary-float
weights. A row event has `design`, `cell`, `horizon`, `label`, and optionally a
nonempty `source` string. Labels dictionaries must include every cell; event
tables may omit unobserved cells. Horizons are positive, distinct, increasing
integers. Threshold decisions return `accept`, `reject` or `unresolved` for the
declared inequality score ≥ target; equality at the upper bound remains
unresolved unless the lower bound also reaches the target.

From the repository root:

```sh
python -B research/beam_ring/certificates/run_demo.py
python -B research/beam_ring/certificates/check_grid_certificate.py --manifest research/beam_ring/certificates/results/manifest.json --events research/beam_ring/certificates/results/events.json --certificate research/beam_ring/certificates/results/certificate.json
```

The demo runs twelve tests, including every 729 partial labeling of a 2×3 grid
against all 4,096 compatible completion instances, independently enumerating
connected components by dense transitive closure. Adversarial checks reject
changed labels, bounds, components, hashes, horizons and schemas; negative/float
weights; duplicate/conflicting observations; and nonfinite or duplicate-key
JSON. The saved example is synthetic and is labeled accordingly. No tracking,
surrogate training or computational speedup occurs in this demo. Construction,
checking and any retained fallback tracking must be charged in a real benchmark.
