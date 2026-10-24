# Research decision: adopt selective particle tracking before inventing another closure

Research checked on 23–24 October 2026. The review covers 73 method-source records
plus 12 dataset and software-asset groups.
Repeated records are intentional cross-checks, not 73 independent papers. The
scope includes accelerator control, numerical space charge, differentiable
simulation, reduced kinetic models, diagnostic inference and public benchmarks.
This is a broad targeted review, not an exhaustive claim about all literature.

**The recommended next computational experiment is multipoint Bayesian algorithm
execution for storage-ring dynamic and momentum aperture design, using a public
Accelerator Toolbox lattice.** This is adoption and independent testing of an
existing method. It is a deliberate new workload, not a relabeling of our old
beam-matching result as tenfold. The first task is an honest empirical comparison;
a new global certificate is not a prerequisite for beginning it.

## Why this method has a better cost structure

In the collective space-charge problem, the simulated particles jointly determine
the force. Evaluating a small subset changes that force unless a separate
approximation is justified. In an external-field storage-ring acceptance study,
each launched test particle can be tracked independently. That makes it possible
to choose expensive individual trajectories before reconstructing the overall
acceptance objective. The relevant saving is in the amount of physics evaluated,
not merely the speed of a fitted objective.

The [October 2026 DAMA-BAX paper](https://doi.org/10.1103/4t6l-7jmg)
reports approximately 40 times fewer tracking acquisitions than NSGA-II at
comparable Pareto performance, including its final validation. This is not a
complete measured wall-clock speedup: its tracking-time analysis is estimated,
and complete neural-training/acquisition overhead is not replayable from public
raw logs. Its implemented acquisition uses one deterministic network rather than
a calibrated Bayesian posterior. The [public mpBAX engine](https://github.com/SLAC-ML/mpBAX)
is accessible, but the original SSRL-X lattice, weights and complete logs were
not verified public. Our test must therefore be a method replication on a new
public benchmark, not a claimed reproduction of that numerical result.

The practical sector is nonlinear magnet-lattice design for synchrotron light
sources and storage rings. Acceptance studies ask which positions and energy
offsets remain captured, directly connecting the computation to useful beam
transport. This is computational design research; neither this review nor our
small tracking probe demonstrates facility deployment or operating savings.

## Where we were rebuilding established machinery

Our low-cost envelope plus reference discrepancy correction sits within
established multifidelity model management. [March and Willcox's 2012 method](https://doi.org/10.2514/1.J051125)
already combines a low-fidelity model with local discrepancy interpolation and
trust-region assumptions. Our implementation and conditional proof remain
useful, but they do not constitute a new general optimization paradigm.

Finite nonlinear observable lifting belongs beside
[Koopman invariant-subspace methods](https://doi.org/10.1371/journal.pone.0150171),
Carleman linearization, polynomial generators and Mori-Zwanzig memory. Exact
sector classifications and explicit nonclosure results may be specialized
contributions; a broad claim to having invented finite observable models or
memory closure would be inappropriate. This audit does not decide
priority for the separate nonlinear-Hamiltonian classification programme.
The [direct fit audit](CORE_VS_TRACTABILITY.md) proves why an exact core need
not supply finite observable closure and identifies the existing bosonic-gsim
quantum workflow as close prior art. New tractable sectors would be a distinct
research contribution; the BAX engineering gain does not follow from the
Moyal-core theorem.

There is an especially important baseline correction. Xsuite's
[quasi-frozen space-charge model](https://xsuite.readthedocs.io/en/latest/spacechargeauto.html)
updates Gaussian force parameters while retaining the simulated particles and
their existing momenta. It does not reset the population to a fresh Gaussian.
Our reset counterexample therefore does not invalidate that model. A comparison
against it is required before claiming that a richer moment closure is needed.

Differentiable self-consistent tracking is also established. The recent
[HELIX paper](https://arxiv.org/html/2609.04421v1) measures a 1.45-fold
end-to-end reverse-mode advantage at sixteen knobs. Its documented differentiable
scope is not a drop-in replacement for our continuous-beam calculation.
Derivative quality, evaluation count, memory and total optimization time must
remain separate quantities. A discrete adjoint is a strong comparator, not an
automatic tenfold result.

## Why the old experiment is a poor tenfold target

Our successful sixteen-control ordinary correction costs about 198 seconds and
seven charged high-fidelity solves, including the generated target. With that
accounting, even a free predictor retaining one unchanged target solve and one
full final audit cannot exceed roughly seven divided by two in equal-call
savings. Removing only optimizer iterations cannot overcome this floor.

The two-control comparisons have similar call-budget ceilings. These are
workload-specific facts, not universal impossibility results. A prospective
change to measured targets, repeated tasks, cheaper validated solves or different
acquisition granularity can change the economics. It must be declared before
testing, and it must not retroactively turn our 3.88-fold and 5.14-fold measured
results into a tenfold claim.

Our old very tight discrete objective was also stricter than parts of the
numerical refinement variation. A new physical study should fix useful rms,
divergence, covariance, emittance and loss tolerances against a qualified
reference, rather than spending calls solely matching one discretization.

## Alternatives worth importing, with transfer gates

**Free-space particle-in-Fourier is the best parallel full-solver lead for the
existing beam programme.** [Shen, Cerfon and Muralikrishnan](https://arxiv.org/html/2403.13911v2)
report 298.6 seconds versus 3557.5 seconds for a long-time open-boundary beam
example at comparable radius/emittance behavior. The gain comes from avoiding
grid heating and a much finer PIC mesh, not from being faster at equal mesh.
Their public Python PIC comparator rebuilds sparse interpolation structures;
an optimized ImpactX and modern higher-order/geometric PIC comparison remains
essential. The short lattice may not have the same heating bottleneck. This is
a reproduction candidate, not an independently reproduced speedup here.

**Variance-reduced PIC is a conditional low-signal candidate.** The 2026
[VR-PIC preprint](https://arxiv.org/html/2602.15041v1) reports about 17-fold
same-device runtime savings on weak Landau damping by using fewer particles at
comparable damping behavior. It is slower at equal particle count and uses a
biased weight approximation with moment correction. Transfer to our strongly
evolving open beam, and comparison against its existing quiet Sobol loading and
ordinary delta-f competitors, remain unproved.

**Adaptive fidelity is useful but does not erase the audit floor.**
[Irshad, Karsch and Dopp](https://arxiv.org/abs/2210.03484) report order-of-magnitude
optimization savings in a laser-plasma study that selects numerical resolution
and box size. That problem has many expensive evaluations and a large fidelity
cost ratio. It is relevant precedent, not evidence for tenfold on our seven-call
task. A coupled particle/mesh/slice ladder is more credible than another fitted
response wrapper alone.

Exact hierarchical sparse-grid coupling, symplectic learned forces, neural
delta-f, reversible low-rank adjoints and dynamic symplectic hyper-reduction
remain cataloged leads. Their advertised gains concern different denominators,
physics, sampling regimes or training budgets. We should not multiply their
headlines together or treat them as independent savings.

## What was actually ingested and tested

The original [FBPIC multifidelity archive](https://zenodo.org/records/7565882)
was downloaded and checked against its publisher checksum. Independent array
inspection finds 2443 rows but only 2286 unique encoded inputs, six conflicting
exact-input groups and 407 zero-charge penalty rows. Inputs are normalized;
physical-unit values are not recoverable by assuming the column labels supply
a normalization. Substantive paired-fidelity coverage is concentrated at domain
corners. These are results of our direct ingestion, not claims inferred from
the abstract. An offline surrogate fitted to this archive must not become its
own ground-truth optimizer benchmark.

Two licensed differentiable-simulation CSVs were ingested with checksums and a
repeatable descriptive fit over 609 recorded measurements. A real SNS measured
wire-profile file was extracted with ZIP CRC and SHA-256 verification. Actual
LANSCE RF data and a separate large-array header both declare 100 examples,
whereas their README says 500; the discrepancy is retained. The complete large
phase-space array was not downloaded or integrity-validated. Sources and
licenses are in the ingestion manifests.

[ARES](https://zenodo.org/records/7853721) supplies published real and simulated
tuning histories. [SNS tomography](https://zenodo.org/records/14807780) supplies
measured projections and optics. These are complementary evidence: screen-only
tuning histories do not establish full exit covariance, and static diagnostic
archives do not reveal what an arbitrary new controller would do at unmeasured
settings. Dataset splits must follow whole trials, operating conditions and
acquisition days, not nearby rows.

The public HMBA lattice and SPEAR3 source were downloaded with their Apache
license and pinned source identity. Our independently executed HMBA probe
expanded the 32-cell representation to a full 3872-element, 6 GeV ring. Across
64 initial points and 128 turns, individual and batched tracking agreed exactly:
42 survived and 22 were lost. Three warm timing repeats show only a 1.08-fold
batching difference in this small probe. It validates a runnable oracle and
turn convention, not an aperture accuracy, optimizer or tenfold result. RF,
radiation, space charge and errors were disabled.

## How to make the next test decisive

The first comparison should adopt the published acquisition strategy and an
ordinary surrogate, preserving the same finite-turn physical objective for
every method. It must include PyAT's existing adaptive/batched acceptance
machinery and credible surrogate-assisted optimization, not only a serial grid
or finite differences. [The official acceptance API](https://atcollab.github.io/at/p/api/at.acceptance.acceptance.html)
already exposes recursive, flood-fill, momentum-acceptance and parallel paths.

Every elapsed comparison must charge data generation, model training, selection,
checkpointing, all failed proposals and independent final maps. Report CPU and
GPU allocations, warm/cold startup and batch occupancy separately. Track-count
savings are a secondary diagnostic. Compare at matched validated objective
quality, including held-out error realizations and a longer-horizon check.

The possible mathematical contribution is a checked decision layer around the
existing sampler. On a declared finite launch grid, unknown survival labels give
exact lower/upper bounds for monotone acceptance objectives; a design can be
discarded when another design's lower objective vector dominates its upper
vector. Connected-component bounds can retain holes and disconnected islands.
These are elementary finite-table/graph principles, not a claimed new general
theory. Their cost and usefulness must be measured, and they do not prove
continuous or infinite-time stability.

Do not delay the empirical reproduction for those certificates. Add them only
when they reduce final verification or prevent a demonstrated false exclusion
at acceptable cost. If the advantage disappears against adaptive acceptance,
after training/final validation, or on new error seeds, retain that failure and
stop treating the method as our tenfold route.

**Decision:** adopt multipointBAX for a public storage-ring acceptance benchmark;
keep particle-in-Fourier as a separate solver reproduction for long-time
space-charge dynamics. The intended first result is a measured adoption gain.
A tenfold improvement beyond the best existing method remains an unproved,
separate ambition.
