# Machinery milestones: theorems, scopes, receipts and failure cases

Each milestone below follows one pattern. A **producer** searches, a separate **checker** replays exact identities without calling the producer, and a typed **envelope** (`extensions/envelope.py`, schema `machinery-envelope-v1`) binds the certificate to its model hash, coefficient domain **Q**, hypotheses, scope and atlas source ids. The envelope checker rejects an unknown domain, an unregistered witness kind, and any payload whose schema does not match the declared kind, so witness types cannot be swapped. Re-run everything with `python3 -B extensions/run_all.py`, and regenerate `results/` with `python3 -B extensions/build_results.py`.

The Hamiltonian milestones W1 and W2 have their own note, `DYNAMIC_CORE_RESULTS.md`.

## C0: typed claim envelopes

**What is checked.** `envelope.check` requires a nonempty list of hypotheses, a scope, and source ids that exist in `compendium/atlas/data/atlas.json`. It recomputes the model and payload hashes, then dispatches by witness kind to that kind's independent checker. The registered kinds are `observer-closure`, `noise-panel-selection`, `adaptive-experiment`, `weyl-invariant-kernel`, `weyl-polynomial-kernel`, `rational-contraction`, `rational-obstruction-answer`, `dgla-lifting` and `pell-orbit-reduction`.

**Failure cases kept in the tests.** The tests reject: domain `Z`; an observer payload labelled as a contraction or a Weyl receipt; the unknown source id `D99-F99`; empty hypotheses; edited payloads, whether or not the hash was refreshed; and an envelope that pairs one model with another model's certificate.

## O1: minimal target observer, `observer-closure-v2`

**Theorem.** Work over a field, with finitely many actions `A_a`, a target `G`, and chronological words acting by `A_{a_k}⋯A_{a_1}`. Let `W* = span{row(G A_w)}`, which is reached once `W_{k+1} = W_k`, after at most `n − rank G` strict steps. A basis `Q` of `W*` gives `QA_a = B_aQ` and `G = CQ`. Then `z = Qx` reproduces every future target value. Every linear summary `R` with that property satisfies `W* ⊆ row R`, so `rank R ≥ rank Q`. A static panel `H` suffices exactly when `ker H ⊆ ker Q`.

**Certificate.** The certificate holds the word provenance of every basis row, the rank, the intertwiners, the target factor, and either a recovery matrix `K` with `KH = Q` or a hidden state `v`. The hidden state satisfies `Hv = 0` and `Q_i v ≠ 0`, and comes with the lost target word and the exact output difference. Initial states `x` and `x+v` read identically on the panel but differ after that word.

**Checks.** The checker in `check_observer.py` has its own arithmetic. The tests cover all 26 seed fixtures, the seven seed models (same bases as v2), redundant and duplicate sensors, noncommuting actions, zero targets with and without sensors, and a budget that returns `unknown`. An oracle over 80 random models computes the span of all words up to length `n` by brute force. Eleven forgeries are rejected.

**Scope.** Finite known rational actions and linear summaries only. There is no noise model here: O2 adds one.

## O2: certified noise-aware cheapest panel, `noise-panel-v1`

**Theorem.** Readings are `y = H_P x + η` with `ηᵀR_P⁻¹η ≤ δ²`, where `R_P` is the principal block of one positive definite joint matrix `R`. A target `T` is recoverable with worst-case amplification at most `γ` for every `x` exactly when `M(P,T) = γ²H_PᵀR_P⁻¹H_P − TᵀT ⪰ 0`. This is Douglas factorization after whitening. The information matrix is monotone in the panel: by a Schur complement, `S ⊆ S'` implies `J(S) ⪯ J(S')`.

**Certificate.** A branch-and-bound tree with four leaf types:

- feasible: an exact LDLᵀ factorization with nonnegative diagonal for every target;
- infeasible: a vector `v` with `vᵀM(P∪U,T)v < 0`, which refutes every panel inside `P∪U` by monotonicity;
- cost: `cost(P) ≥ optimum`, so tie policy `one_optimum` applies;
- open: allowed only in an `incomplete` certificate, which states a lower bound and no optimum.

**Contracts.** Two contracts are kept separate. `per_target` bounds each finite-horizon word separately; this is the maximum over words. `stacked` bounds the joint Euclidean error.

**Retained counterexamples.**

- `diag(1, 1/1000)` recovers `y` exactly, yet is infeasible at `γ = 999`.
- Correlation `1/2` makes two averaged sensors fail where independent bars would pass; anticorrelation helps.
- `per_target` is feasible where `stacked` is infeasible.
- A future target needs the hidden coordinate at horizon 1.
- No finite `γ` repairs a hidden direction.

**Oracle.** Seventy random menus are compared with exhaustive subset search; both claim types occur at least six times.

**All-time invariant metric (`invariant-metric-v1`).** A rational `S` with `B_aᵀSB_a ⪯ S`, `CᵀC ⪯ S` and `QᵀSQ ⪯ γ²J(P)` bounds every future output error by `γδ`. This is **sufficient, not necessary**. A rotation passes with `S = I`. A shear fails with `S = I`, and that is reported as no certificate, not as instability.

## O3: finite adaptive experiments, `adaptive-tree-v1`

**Theorem.** For a deterministic finite test table with positive costs, set `V(S) = 0` on label-constant `S`. Otherwise `V(S) = min_e (c_e + max_y V(S_{e,y}))` over tests that strictly split `S`. The table is resolvable exactly when every pair of states with different labels is separated by some test.

**Certificate.** The upper half is a decision tree whose worst-case cost the checker computes. The lower half is a table `v` closed under splitting fibres, with `v(T) ≤ c_e + max v(T_y)` for every splitting test. Optimality means the two halves meet at the root. When the table is not resolvable, the certificate is an unresolvable pair.

**Checks.** Target-only decisions cost `1` where full identification costs `3`, which is the seed fixture. Eighty random tables agree with explicit enumeration of every decision tree.

**Set-valued (adversarial) noise.** A model may declare `"noise": "set_valued"`. Each test then returns, at a state, any element of a declared finite set.

- After observing `y` the feasible set is `S_y = {s : y possible at s}`. A test is admissible only if every possible observation strictly shrinks the feasible set.
- Optimality certificates are as before.
- A feasible set whose value is infinite carries a witness subset `W` with two labels on which every test has a common observation. Answering that observation forever defeats every policy. The checker verifies each such witness before treating the value as infinite.

Eighty random set-valued tables agree with an independent minimax oracle. Noise on `t1` raises the seed fixture's cost from 3 to 4.

**Not transferred.** Probabilistic and continuous noise, which need posterior semantics and a different termination theorem.

## S1: finite rational obstruction compiler, `rational-obstruction-answer-v1`

**Theorem** (from the seed). Suppose `pi = I`, `di = 0`, `pd = 0` and `I − ip = dh + hd`. For a cocycle `b`, if `pb = 0` then `hb` is a primitive. Otherwise a row of `p` is a functional that vanishes on all boundaries and is nonzero on `b`.

**Answers.** `obstruction.solve` returns one of `solved`, `obstructed`, `not_cocycle`, `invalid_model` (which covers `d² ≠ 0`, field `Z` and floats) or `unknown` (size budget). Every answer is replayable with matrix products alone: `d u = b`, or `f d = 0` together with `f b ≠ 0`.

**Checks.** A rank oracle on 60 generated complexes; both outcomes occur more than ten times.

**Boundary.** Over `Q`, multiplication by 2 is solvable, with `u = 1/2`, although `H¹` over `Z` is `Z/2`. Rational answers never certify torsion.

## S2: finite DGLA Maurer–Cartan lifting, `dgla-lift-v1`

**Theorem.** In a DGLA, if `x_1, …, x_{n−1}` solve `dx + ½[x,x] = 0` modulo `t^n`, then `ob_n = ½Σ_{i+j=n}[x_i,x_j]` is a cocycle in `L²`, and `x_n` exists exactly when `[ob_n] = 0`. The contraction gives `x_n = h(−ob_n)`; any cocycle of `L¹` may be added, which is the gauge or complement choice. A nonzero class gives a functional on `L²` that vanishes on `d(L¹)`. At order 2 the class `½[[x_1,x_1]]` depends only on `[x_1]`, so an order-2 witness obstructs every jet with that first-order class. At higher orders the witness is **relative to the declared jet**, and the certificate says so through `intrinsic: false`.

**Checker.** The checker re-verifies degrees, `d² = 0`, Leibniz and graded Jacobi on all basis pairs and triples before it checks the Maurer–Cartan equations.

**Generator.** The Chevalley–Eilenberg DGLA `Hom(Λ^{k+1}g, g)` with the Nijenhuis–Richardson bracket and `d = [μ,·]`. Its Maurer–Cartan elements are the deformations `μ + x`. The degree-0..2 truncation is a quotient by a DG ideal, and it is enough for lifting.

**Checks.**

- On a 21-dimensional model for the Heisenberg algebra `h₃`, the computed `dim H²(h₃,h₃) = 5` agrees with the classical value.
- On the abelian algebra, `so(3)` lifts and a non-Jacobi direction is obstructed at order 2.
- On `h₃`, intrinsic order-2 obstructions occur, and a jet-relative order-3 obstruction occurs.

**Not claimed.** Convergence and moduli statements.

## A1: supplied-unit Pell orbits, `pell-orbits-v1`

**Theorem** (derivation in `OBSTRUCTIONS_AND_ARITHMETIC.md`). Take nonsquare `D > 0`, `N ≠ 0`, and a unit `ε = a + b√D` with `a, b > 0` and `a² − Db² = 1`. Every `α > 0` of norm `N` is uniquely `seed·ε^j` with `j ∈ Z`. The seeds are exactly the window solutions:

- for `N > 0`: `y² < b²N`;
- for `N < 0`: `Dy² < a²|N|`.

The nonnegative branch is `j ≥ 0`.

**Certificate.** The checker re-enumerates the window with integer square tests, so a missing or an extra seed is detected. It re-runs full-state modular cycles and confirms closure with no tail, and it recounts filtered height populations by direct iteration. The producer instead uses the residue-count formula with an exact `M(Y)` found by bracketing and binary search.

**Checks.**

- The four handoff fixtures reproduce exactly: seeds, populations and mod-3 cycles.
- The proper-power unit `17 + 12√2` gives four seeds and the same points.
- `x² − 3y² = 2` has an empty seed list, which is a complete negative answer.
- Sixty random models agree with brute force.
- Invalid `D`, `N` and units are rejected, and state and window budgets return `unknown`.

**Not claimed.** Fundamental units and the maximal order.

## S3: integral cohomology and integer coboundary decisions, `integer-smith-v1`

**Certificate.** For each differential `d_k` the certificate records integer matrices `P`, `P⁻¹`, `Q` and `Q⁻¹`. The checker verifies `PP⁻¹ = I` and `QQ⁻¹ = I`, so both transforms are unimodular. It also verifies `P d_k Q = diag(s_1, …, s_r, 0, …)` with `s_1 | s_2 | ⋯`.

**What the checker derives.** Without any elimination of its own, it reads off `H^k(C;Z) = Z^{n_k − r_k − r_{k−1}} ⊕ ⨁_{s_i>1} Z/s_i`, taking the `s_i` from `d_{k−1}`.

**Answers for an integer cocycle `b`.** One of three:

- an integer primitive `u`;
- a rational obstruction functional;
- a torsion functional `f` with `f d ≡ 0 (mod m)` and `f b ≢ 0 (mod m)`. This is a `Z/m`-valued cochain functional that vanishes on all coboundaries, so `b` is not an integral coboundary even when it is a rational one.

**Checks.**

- The classical example `[[2,4,4],[−6,6,12],[10,−4,−16]]` gives invariant factors `2|6|12`.
- `RP²`, the torus and the Klein bottle give the expected cohomology.
- On 120 random matrices the invariant factors match the determinantal-divisor oracle.
- On 120 random cocycles, the rational/integral classification matches an exact rank oracle.

The standing `×2` example is solvable over **Q**, but over **Z** it is obstructed with modulus 2. This closes the torsion boundary that S1 deliberately left open.

## A2: fundamental units, `fundamental-unit-v1`

**Method.** Any unit `x + y√D > 1` of norm `±1` satisfies `|x/y − √D| < 1/(2y²)`, because `x/y + √D ≥ 1 + √2`. By Legendre's criterion `x/y` is then a convergent of `√D`.

**Certificate.** The checker recomputes the convergents exactly. It verifies that the declared `ε₀` is the first convergent of norm `±1` and `ε₁` the first of norm `+1`. Hence every unit of `Z[√D]` is `±ε₀^j`, and every norm-one unit is `±ε₁^j`.

**Integration with A1.** A Pell model may declare `"unit": "fundamental"`. The orbit compiler then embeds the unit certificate, and the checker upgrades the scope to orbits under the full norm-one unit group.

**Checks.**

- Brute force agrees for every nonsquare `D < 120` whose solutions are small.
- `D = 61` gives `29718 + 3805√61` of norm `−1`.
- `D = 991` is the classical 30-digit example.
- The proper power `17 + 12√2` is rejected as fundamental.

**Maximal order.** For `D ≡ 1 (mod 4)` a Pell model may declare `"order": "maximal"`.

- Elements are `(x + y√D)/2` with `x ≡ y (mod 2)`. The norm equation becomes `x² − Dy² = 4N`, and the supplied unit `(a + b√D)/2` has `a² − Db² = 4`.
- The reduction argument is unchanged, so the seed window has the same form: `y² < b²N` for `N > 0` and `Dy² < a²|N|` for `N < 0`.
- Unit steps divide by 2 exactly, and modular filters require an odd modulus.

Forty random maximal-order models match brute force. For `D = 5`, `N = −1` the solutions are the odd-index Fibonacci pairs.

**Fundamental units of `O = Z[(1+√D)/2]`** (the maximal order when `D` is squarefree).

- *Index argument.* `(O/2O)^×` has order 1 or 3, so `η³ ∈ Z + 2O = Z[√D]` for every unit `η`. The fundamental unit of `O` is therefore either `ε`, the certified fundamental unit of `Z[√D]`, or an exact cube root of `ε`.
- *Checker.* It either verifies `η³ = ε` exactly in half-coordinates, or proves that no cube root exists. A cube root would have trace `u` with `u³ − 3νu − 2a = 0`. That cubic has a single real root. Either the root lies strictly between consecutive integers, or it is an integer `u` for which `(u² − 4ν)/D` is not an integral square of the right parity. The non-squarefree case `D = 189` is the standing example of the second alternative.
- *Tests.* Brute force agrees for 72 values `D ≡ 1 (mod 4)`.
- *Pell integration.* Pell models with `"order": "maximal"` may use `"unit": "fundamental"`.

## O2b: rational invariant-metric search

**Candidates.** `panels.metric_search` tries two kinds of candidate `S`:

- the finite-semigroup average `Σ_g gᵀCᵀCg`, used when the quotient actions generate a finite semigroup within the budget;
- truncated weighted word sums `Σ_{|w|≤L} B_wᵀ(CᵀC + εI)B_w`, which suit contractive families.

**Acceptance.** Each candidate is accepted only by the exact `invariant-metric-v1` checker. Failure is reported as `no_certificate`.

**Checks.**

- A dihedral group is found.
- A contractive non-commuting pair is found.
- A shear gets `no_certificate`.
- So does a pair whose actions each have spectral radius 1/2 but whose product is unstable.
