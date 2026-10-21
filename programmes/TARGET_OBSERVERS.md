# A target observer compiler: the strongest cross-domain engineering enhancement

This handoff is grounded in the published collection at commit `6097002895b85db2139ef350f49c93aff711ce12`. It proposes a new implementation programme; it does not claim that the classical quotient, realization, factorization or Bellman theorems are new discoveries. Source paths below are relative to the repository root. The accompanying `observation_closure_reference.py` is an exact, deliberately small executable seed, not the completed robust design system.

## The central mathematical capability

The most powerful observation machinery is the ability to replace an enormous state description with exactly the distinctions required by a declared future task, and to prove both sufficiency and minimality. Its basic equation is `G=L H`, but the useful system must distinguish present recovery, future prediction, noise stability and decision certification. A cheap panel which recovers today's target can lose tomorrow's target; an exactly invertible panel can amplify tiny errors enormously; and recovering every numerical score can cost more than certifying which action wins.

The proposed deliverable is a **certificate-producing target observer compiler**. Given a finite rational state model, allowed actions, targets, available sensors, costs and a declared error geometry, it should return a minimal exact observer, a cheapest certified sensor choice within the specified finite search class, and a small independent checker. When impossible, it should return an explicit invisible-state or negative-quadratic-form witness. Optimizers may search aggressively; the checker must verify identities, ranks, inequalities and completeness receipts without trusting that search.

## What is already implemented, and what remains a recipe

`compendium/atlas/labs/engine.js` implements L01 with four real coordinates, six fixed rational probes and all 64 subsets; L08 implements one additive shared-nuisance comparison; L04 evaluates analytic diagonal spectral-cutoff bounds. These are functioning finite models, not arbitrary matrix editors, adaptive experiment optimizers or general nonlinear observers. `domains/computation/verify.py` and `domains/probability/verify.py` check representative recipes and counterexamples. Preserve their public contracts while adding a separate general engine.

The strongest existing source families are `D15-F01` (fibre factorization, minimum recovery norm and dynamic closure), `D14-F01` (future equivalence and finite refinement), `D14-F02` (intertwiners, Hankel lower bounds and reachable-observable quotients), `D14-F03` (typed certificates), `D12-F04` (shared uncertainty), `D15-F03` (bias-noise tradeoff) and `D15-F04` (minimum-cost finite experiments). Their complete readable files are `compendium/readable/families/<ID>.md`; source payloads are in `compendium/atlas/data/atlas.json`.

Useful anchors include `2023:M016`, `2023:M017`, `2026:Y26-09-018`, `2026:Y26-09-019`, `2026:Y26-09-024`, `2026:Y26-10-019`, `2026:Y26-10-022`, `2026:Y26-10-023`, `2026:Y26-10-029`, and `2026:Y26-08-901` through `2026:Y26-08-905`. Their dates are historical evidence locations, not dates of invention of the retrospective proofs.

## The exact finite-dimensional theorem to implement completely

Work over the rationals for computation and over any field for the algebraic theorem. Let the state be `x in F^n`, allowed actions be matrices `A_a`, and the requested output be `Gx`. A chronological word `w=a_1...a_k` acts by `A_w=A_{a_k}...A_{a_1}`. Define

$$
W_0=\operatorname{row}G,\qquad
W_{k+1}=W_k+\sum_a W_kA_a,\qquad
W_* = \operatorname{span}\{\operatorname{row}(GA_w):w\text{ any word}\}.
$$

If `W_{k+1}=W_k`, it is invariant under every right action and already equals `W_*`. Every strict step increases dimension, so at most `n-rank(G)` strict steps occur. A basis matrix `Q` of `W_*` has unique matrices `B_a,C` satisfying

$$
QA_a=B_aQ,\qquad G=CQ.
$$

The reduced state `z=Qx` evolves by `z'=B_a z` and reproduces every requested future output. It is minimal among **linear state summaries sufficient for every target value after every allowed word and every initial state**: if `R` is any such summary, every `GA_w` factors through `R`, hence `W_* subset row(R)` and `rank(R)>=rank(Q)`.

For a fixed static sensor panel `H`, measured once at the initial state, every future target is recoverable exactly if and only if

$$
W_*\subseteq\operatorname{row}H
\quad\Longleftrightarrow\quad Q=KH
\quad\Longleftrightarrow\quad\ker H\subseteq\ker Q.
$$

This is a complete theorem in its declared finite linear scope, not a claim that this panel is optimal when later measurements, adaptive action choice, unknown dynamics or process noise are allowed. Affine known actions `A_a x+b_a` are an immediate extension: `z'=B_a z+Qb_a`. Unknown inputs require a separate model.

The proof certificate must contain input hashes and arithmetic type, the chronological word convention, `Q`, `B_a`, `C`, exact rank, and a provenance expression showing each row of `Q` is a row of some `GA_w` or an explicit linear combination of such rows. Invariance plus containment of `G` proves sufficiency; provenance proves minimality, so both directions matter. The reference seed selects actual word rows as its basis, making provenance particularly simple. A failed panel must carry `v` with `Hv=0` but `Qv!=0`, and one target/action word witnessing the lost output.

## Add stable recovery without confusing it with rank

Fix the target norm and physical units. For observations `y=H_P x+eta` with the deterministic ellipsoidal error model `eta^T R_P^{-1}eta<=delta^2`, where `R_P` is rational positive definite, a target matrix `T` admits a linear reconstruction with worst-case amplification at most `gamma` precisely when

$$
T^T T\preceq\gamma^2 H_P^T R_P^{-1}H_P.
$$

This is the finite-dimensional factorization/majorization theorem already underlying D15-F01, applied after whitening. It simultaneously checks target identifiability and sensitivity. Setting a large finite `gamma` cannot repair a hidden target direction. Conversely rank alone cannot rule out arbitrary amplification.

For a finite horizon, enumerate the declared word set and check this inequality for each `T=GA_w`. If a joint stacked-output Euclidean error is the target instead, stack the `GA_w` into one `T`; these are different contracts. A request for a bound at every time/word means a maximum, not a stacked norm. Exact rational PSD checks and negative quadratic witnesses should be first-class certificate types; floating singular values may suggest candidates but cannot certify an exact zero.

For all-time switched dynamics, closure dimension alone gives no uniform noise bound. A sufficient certificate is a rational `S>0` and `gamma^2>=0` such that

$$
B_a^T S B_a\preceq S\quad(\text{every }a),\qquad C^TC\preceq S,
\qquad Q^TSQ\preceq\gamma^2 H_P^T R_P^{-1}H_P.
$$

The last inequality supplies a reconstruction of `Qx` whose error has `S`-norm at most `gamma delta`; the first two transport that bound to every future output. This certificate is sufficient, not necessary for all stable switched systems. Failure to find a common quadratic metric must be reported as `unknown/no_certificate`, not as instability. Non-diagonal inverse problems and data-dependent regularization are later extensions, with the source-class and norm assumptions retained.

## Cheapest experiments: a meaningful certified objective

First implement finite static selection: minimize `sum_{j in P}cost_j` subject to exact future-target recovery, and then the stronger user-selected amplification cap. For small menus, exhaustive search supplies an independent oracle. For larger menus, branch and bound can return a **complete search certificate**. At a node with selected sensors `P` and undecided sensors `U`, if even `H_{P union U}` misses a required target direction, an explicit kernel witness rejects every descendant. If its best attainable information matrix fails the PSD cap, a rational negative quadratic witness rejects every descendant. A cost lower bound can reject a branch that cannot improve the incumbent. Record whether ties are enumerated; pruning at equality is appropriate for one optimum but not for counting every optimizer.

For correlated noise, use the relevant principal block of one declared joint covariance/ellipsoid matrix. Adding sensors increases the information matrix by a positive semidefinite Schur-complement term. Do not replace correlated noise by independent coordinate bars without changing the claimed model. The worst-case search remains exponential; a resource cap returns an incumbent with explicit remaining bound or `unknown`, never an unsupported global optimum.

Second implement a separate finite deterministic test-table backend. For state subset `S`, target labels `tau(s)` and positive test costs,

$$
V(S)=0\quad\text{if }\tau\text{ is constant on }S,\qquad
V(S)=\min_e\left(c_e+\max_{y:S_{e,y}\ne\varnothing}V(S_{e,y})\right).
$$

This is a complete finite optimum under target-separating available tests and useful strict splits. The result should include the decision tree and all Bellman values needed to check both upper and lower bounds. Start with at most ten explicit states/tests. Noisy or continuous outcomes need posterior feasible-set semantics and a new termination theorem; do not import the deterministic table result silently.

## Shared uncertainty and dynamic relevance

Compile **score differences**, when the decision contract permits, rather than separately reconstructing all scores. For `J_A=c+d`, `J_B=c`, the difference is `d`, so a nuisance direction changing only `c` can be discarded initially. If dynamics keep that direction invisible to all future differences, it remains discardable; if `d'=d+c`, it becomes future-relevant. The row-module closure detects the distinction exactly.

For linear affine margins on a declared box, simplify common variables before exact support bounds. For ellipsoids, preserve the quadratic form. For finite state sets, target labels can collapse states with different numerical scores but the same certified decision; this may be strictly coarser than the minimal linear summary for exact values. Do not call the linear compiler the globally minimal decision system without specifying the encoding class and target.

## Hankel and nonlinear backends: explicit second phase

For known rational input-output realizations `(A,B,C)`, compute the reachable space and quotient it by its invisible part. Export an intertwiner plus a nonzero matching block-Hankel minor. Those give a global upper realization and a lower bound, rather than a recurrence fitted to a finite prefix. Keep the distinction between arbitrary initial-state observation and the zero-initial driven system. For multiple outputs, minimal polynomial degree can be less than state dimension (`A=C=I_n` is the compulsory counterexample).

For finite nonlinear state/action tables, implement stable partition refinement of future target outputs. A quotient is valid only when all actions respect its fibres. It stabilizes after at most `|S|-1` strict refinements. For continuous nonlinear maps, only return a local differential statement unless full fibre constancy is proved; `H(x,z)=x`, `g(x,z)=z^2` at `z=0` defeats the tangent-only shortcut. Ordinary field rank, tropical register lower bounds and nonlinear encoding dimension remain distinct certificate types.

## The useful Hamiltonian connection

The invisible-space recursion is

$$
N_0=\ker G,\qquad N_{k+1}=N_0\cap\bigcap_a A_a^{-1}N_k.
$$

Its fixed point is the largest action-invariant subspace inside the initially invisible space. The Hamiltonian companion uses the same fixed-point pattern to extract the largest dynamically invariant sector inside a one-step exact-partner space. This suggests a shared **typed invariant-subspace certificate interface**. It does not allow finite-dimensional stabilization bounds to be transferred to polynomial spaces with unbounded degree, or prove that finite truncations settle the Hamiltonian all-degree problem.

## Executable tasks and acceptance conditions for Claude Code

Phase O1 should turn the reference seed into a package module accepting arbitrary rational matrices and action alphabets, with certificate JSON and a separate checker. The checker must recompute word provenance, `QA_a=B_aQ`, `G=CQ`, basis rank, panel factorization or counterexample, and reject a deliberately corrupted certificate. Report the dimension sequence and proved stabilization, not a numerical rank tolerance. Preserve zero targets, redundant rows and rank-deficient panels.

Phase O2 should implement exact rational PSD/negative-witness certificates and finite-horizon noise caps, then complete static panel search with an exhaustive small-menu oracle and a proof-carrying branch-and-bound mode. A mode must declare `initial_static`, `finite_horizon`, `all_words`, norm, noise set, initial-state quantifier and tie policy. Every reported optimum needs a matching lower-bound certificate. Benchmark measured costs separately from theorem counts; no deployment or sensor-saving claim follows from synthetic examples.

Phase O3 should implement the small finite adaptive table backend and its Bellman checker. Demonstrate a target-only decision tree cheaper than state identification; demonstrate an unresolved pair if tests do not separate labels. Phase O4 may add rational invariant-metric certificates and reachable-observable/Hankel reduction. SDP search is optional; exact checking is mandatory. Where a general certificate cannot be found, keep an explicit open obligation.

The acceptance fixture suite must include current-target recovery that fails under evolution; ordered noncommuting actions; a shared nuisance which stays irrelevant and one which feeds the target; an exactly invertible but badly conditioned observation; individually stable action matrices with an unstable product; MIMO recurrence degree versus state dimension; local tangent cancellation without global fibre constancy; duplicate/no-op sensors; impossible target pairs; and corrupted proof data. Successful fixtures do not establish general soundness by themselves: the written theorems and exact invariant checks supply that claim.

Suggested integration paths are `engines/observer/closure.py`, `factorization.py`, `stability.py`, `panels.py`, `adaptive.py`, `certificates.py`, `check_certificate.py`, `tests/fixtures/observer/`, and a small input editor after the exact engine exists. Keep the existing L01/L08 labs operational. A general engine should drive any new interactive controls rather than turn explanatory labels into apparent implementation.

## Primary grounding and priority boundary

The existing D15-F01 reference is R. G. Douglas, “On majorization, factorization, and range inclusion,” DOI `10.1090/S0002-9939-1966-0203464-1`. D14-F02 cites Balle et al., “Canonical forms for weighted automata,” arXiv `1501.06841`. D14-F03 cites Boyd and Vandenberghe's *Convex Optimization*. This handoff derives the finite rational assembly from the source collection and elementary linear algebra; it is not a fresh comprehensive literature review or a claim of priority. The ambitious result to pursue is a rigorously checked general implementation with useful new structural classifications and sharp problem-specific consequences.
