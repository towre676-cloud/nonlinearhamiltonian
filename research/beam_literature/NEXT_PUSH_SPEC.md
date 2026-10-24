# Next push specification: public nonlinear ring acceptance

This is a prospective design brief, not a claim that the full benchmark is
already frozen or executed. Only the source-bound HMBA feasibility probe has
run. Final launch grids, horizons, control ranges and error distributions must
be serialized before optimizer data are generated. The original space-charge
benchmark and its failures remain unchanged.

**Owner of the first experiment:** implement an oracle adapter to existing
Accelerator Toolbox tracking and the public multipointBAX engine. Import the
existing method; do not write another generic optimizer. Pin simulator, lattice,
dependency versions and every physics mode. HMBA is a public substitute for the
unverified-private SSRL-X reproduction assets. One full turn must mean all 32
cells, not one MAT cell. Six-dimensional RF/radiation modes require a separate
configuration and validation, not an implicit switch.

**Controls and objective:** identify the actual nonlinear magnet families and
check the rank of their chromaticity response. If a chromaticity-preserving
nullspace is used, verify its preservation over the complete selected range.
State any broken mirror symmetry. Fix both dynamic and momentum acceptance
metrics, their physical coordinate units, loss/aperture conventions, launch
locations and finite turn horizon. Use the same metric for learning, reporting
and final validation. A change to an origin-connected or finite-grid objective
is substantive and cannot be described as the paper's original metric without
verification.

**Comparators:** include a credible production NSGA-II workflow, optimized
adaptive/batched PyAT acceptance and an ordinary surrogate-assisted competitor.
The unmodified adopted MeanBAX strategy is a baseline for any proposed
certificate enhancement. Tune all competitors under the same development
budget and hardware allocation. Provide each the same initialization and input
knowledge. Compare complete elapsed time and resource use at matched physical
quality. A ratio against NSGA-II alone is an adoption result, not evidence of
tenfold superiority to the strongest method discovered by this review.

**Data and quality separation:** reserve operating configurations and error
realizations before training. Score selected final designs on a denser launch
grid and longer horizon, documenting the change from the learning oracle.
Evaluate both acceptance objectives and declared optics/loss constraints. Keep
the held-out evaluator inaccessible to acquisition and model selection. Charge
every final candidate, including failures. A pilot with one seed is feasibility
evidence; a headline gain requires independent repeats and a stated variability
estimate. Do not infer missing counterfactual controller responses from ARES or
other fixed historical trajectories.

**Cost ledger:** separate simulator construction, initial tracking, model
training, acquisition optimization, physical queries, parsing/checkpoints and
final qualification. Count both query number and survived-turn work because
boundary particles have different costs from early losses. Record concurrency
and hardware; include failed runs and retries. Repeated-task amortization is
allowed only with an explicit number of tasks and a charged shared construction
cost. The reported tenfold target is a ratio of successful complete workflows
at the same validation contract, not an inference-time or loop-only ratio.

**Optional checked layer:** unknown finite-table labels must remain unknown.
For nonnegative weights and a monotone aggregation, assigning unknown labels
all-zero and all-one produces exact finite-table brackets. Pareto exclusion is
valid only from lower/upper domination; model confidence alone is not a proof.
An origin-connected grid objective can use connectivity brackets without
assuming radial monotonicity. Short-horizon losses imply long-horizon losses;
short-horizon survival does not imply long-horizon survival. No deterministic
bracket is assumed tight. Measure its query/checker cost before adopting it.

**Go/no-go:** begin with an empirical method replication, retaining independent
final tracking. Continue toward tenfold only if the complete-cost margin remains
after strong adaptive/batched comparators and held-out validation. Reject an
apparent win that relies on uncharged training, weaker physics, different
turns, coarser final maps, leaked error seeds, missing momentum acceptance or
surrogate labels treated as truth. A failure is a useful research result, not
permission to redefine the benchmark afterwards.

**Separate beam-solver lane:** reconstruct the published free-space PIF case,
repairing only documented compatibility/default issues. Compare it with an
optimized modern PIC implementation at matched emittance, covariance and
long-time error, including precomputation. Establish whether grid heating is
actually a limiting cost before porting PIF to the old short lattice. This lane
must not be combined arithmetically with a ring-BAX ratio from different physics.
