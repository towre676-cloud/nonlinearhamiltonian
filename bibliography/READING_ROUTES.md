# Mathematical reading routes

The atlas is organized by the operation a reader wants to perform: calculate, certify, reconstruct, classify, evolve, transport or decide. These routes use actual theorems and declared worked models. They do not equate different theories merely because both use a spectrum, an entropy or a commutator.

Start with the [atlas report](../compendium/atlas/output/Mathematics_Atlas_2023_2026_Report.pdf), use the readable domain links below, and open a cited treatment by its source UID for its complete definitions, proof, example and limitations. The [interactive atlas](../compendium/atlas/output/Mathematics_Atlas_2023_2026.html) supplies ten finite worked models. Its broader capacity tags are not claims of unrestricted solver implementation.

## Evidence and implementation statuses

| Status | Meaning |
|---|---|
| proved_in_stated_scope | A displayed proof supports its exact hypotheses; this label is not a claim of novelty or independent formal verification. |
| implemented_worked_model | The interactive or exact engine implements the declared finite model and arithmetic, not an unrestricted domain solver. |
| documented_recipe | A mathematical workflow is described, but its general interactive engine is not implemented. |
| external_solver_dependency | The retained conclusion depends partly on explicitly identified archived external computation. |
| open_extension_in_retained_material | A proposed extension remains unproved in this collection; no claim is made that it is unsolved throughout the literature. |
| historical_source_gap | Required historical content was not recovered. A current illustrative model does not fill that provenance gap. |

## Cross-domain routes

### T01 · Recover a target, then decide which observation is worth buying

**Question.** What is the smallest observation that still determines the target or preserves the action?

Begin with equivalence classes and a transition rule that respects those classes. For linear data Hx and target Gx, work through ker H⊆ker G and G=LH, then calculate the recovery norm. Only after present target recovery is settled should you ask whether the observed state closes dynamically; HA=TH is an additional condition. Read hidden-target risk next: an unobserved coordinate can leave irreducible conditional variation even when observed noise tends to zero. Shared uncertainty then changes a decision difference because common terms cancel. Finish with the finite cheapest-experiment recursion, where the terminal condition is constancy of the target, rather than identification of every state.

**Constructive checkpoint.** Produce both a factorization certificate and a counterexample invisible vector for a failing target. In L01 compare the cheapest probes for the scalar target and a larger target. In L08 retain the same common uncertain variable in both actions.

**Boundary.** These finite exact examples do not establish nonlinear global fibre constancy, future predictive performance or an optimal noisy sensor policy.

Reading sequence: [D03-F01](<../compendium/readable/domains/D03.md>) → [D14-F01](<../compendium/readable/domains/D14.md>) → [D15-F01](<../compendium/readable/domains/D15.md>) → [D11-F01](<../compendium/readable/domains/D11.md>) → [D12-F04](<../compendium/readable/domains/D12.md>) → [D15-F04](<../compendium/readable/domains/D15.md>).

Domains: [D03](<../compendium/readable/domains/D03.md>) · [D14](<../compendium/readable/domains/D14.md>) · [D15](<../compendium/readable/domains/D15.md>) · [D11](<../compendium/readable/domains/D11.md>) · [D12](<../compendium/readable/domains/D12.md>). Bridges: B01. Worked models: L01, L08.

### T02 · From boundary matrices to gluing and transport

**Question.** Which local data assemble to a global object, and which obstruction survives?

Compute an actual chain complex before interpreting its homology: verify that the product of successive boundaries is zero, and keep the coefficient ring. L09 compares a graph cycle with the complex obtained by filling its face. Continue to integer torsion and cochain gluing, where a real nullspace calculation can lose an integral obstruction. A logarithmic differential then supplies a complementary local-to-global example: locally closed need not mean globally exact because loop periods remain. Connections and gauge transport add ordered matrix products. L05 displays order dependence for two shears, but a two-matrix loop is not a construction of curvature on an arbitrary manifold.

**Constructive checkpoint.** Write down the boundary or Čech maps and one obstruction class. Compare a zero local differential with a nonzero loop period, then keep the shear commutator distinct from the projection contraction in the second L05 mode.

**Boundary.** A picture of overlapping patches, an adjacency graph or a sampled transport loop does not determine a sheaf, its coefficient system, its derived comparison maps or a global connection.

Reading sequence: [D04-F02](<../compendium/readable/domains/D04.md>) → [D05-F01](<../compendium/readable/domains/D05.md>) → [D05-F03](<../compendium/readable/domains/D05.md>) → [D05-F04](<../compendium/readable/domains/D05.md>) → [D06-F03](<../compendium/readable/domains/D06.md>) → [D13-F03](<../compendium/readable/domains/D13.md>).

Domains: [D04](<../compendium/readable/domains/D04.md>) · [D05](<../compendium/readable/domains/D05.md>) · [D06](<../compendium/readable/domains/D06.md>) · [D13](<../compendium/readable/domains/D13.md>). Bridges: B02. Worked models: L09, L05.

### T03 · Spectral representation, stable evolution and inverse resolution

**Question.** When does a spectral formula control a trajectory or a reconstruction error?

Start with a self-adjoint operator and its domain, multiplicities and spectral measure. Derive the heat semigroup and its mean-zero energy decay before comparing it with a finite stencil. Check conservation, positivity and stability separately, and use normalized grid norms when discussing a continuum rate. The Lyapunov example then shows why stable eigenvalues do not rule out temporary Euclidean growth. Move to the inverse problem last: positive singular values give uniqueness, while a small singular-value tail makes the inverse unbounded. The admissible source ellipsoid and deterministic noise norm determine a cutoff bound with two distinct terms.

**Constructive checkpoint.** In L04 compare bias, noise amplification and total upper bound while changing N. In severe mode keep the logarithmic safety margin; that implemented mode fixes β=1. Use L05 only for the stated two-line principal-angle model, not as a substitute inverse solver.

**Boundary.** A residual-to-error bound needs operator hypotheses, and fixed-time trace class differs from a small-time heat asymptotic. No one lab implements all the PDE, frame or control recipes in this route.

Reading sequence: [D07-F04](<../compendium/readable/domains/D07.md>) → [D08-F01](<../compendium/readable/domains/D08.md>) → [D08-F02](<../compendium/readable/domains/D08.md>) → [D09-F01](<../compendium/readable/domains/D09.md>) → [D15-F03](<../compendium/readable/domains/D15.md>) → [D07-F01](<../compendium/readable/domains/D07.md>).

Domains: [D07](<../compendium/readable/domains/D07.md>) · [D08](<../compendium/readable/domains/D08.md>) · [D09](<../compendium/readable/domains/D09.md>) · [D15](<../compendium/readable/domains/D15.md>). Bridges: B03. Worked models: L04, L05.

### T04 · Exact populations, summaries and information loss

**Question.** What can be counted exactly, and which distinctions are lost by a compressed statistic?

Construct a finite population and its reversible address before using asymptotic approximations. L02 exhausts a six-item selection problem and exposes feasible counts, ranks and optimal values. Read random inclusion laws with a declared sampling model next; independence, fixed-size sampling and weighted sampling produce different pair probabilities. The graph-census family gives a stronger counterexample to overinterpreting summaries: two graphs can agree on a binary size–energy census while integer-height probes distinguish them. This connects exact enumeration to observation equivalence. A quotient suitable for optimization must preserve multiplicities if counts or probabilities are also requested.

**Constructive checkpoint.** Check a rank/unrank round trip and a lower-bound certificate for the finite optimum. In L03 compare the entire exact coefficient census, then evaluate it at a chosen floating q while retaining the distinction between the polynomial identity and its numerical value.

**Boundary.** The six-item and seven-vertex examples do not reconstruct missing large-instance historical tables. A matching summary is an equivalence only relative to its stated probes.

Reading sequence: [D13-F01](<../compendium/readable/domains/D13.md>) → [D13-F02](<../compendium/readable/domains/D13.md>) → [D10-F02](<../compendium/readable/domains/D10.md>) → [D11-F04](<../compendium/readable/domains/D11.md>) → [D12-F03](<../compendium/readable/domains/D12.md>) → [D14-F01](<../compendium/readable/domains/D14.md>).

Domains: [D13](<../compendium/readable/domains/D13.md>) · [D10](<../compendium/readable/domains/D10.md>) · [D11](<../compendium/readable/domains/D11.md>) · [D12](<../compendium/readable/domains/D12.md>) · [D14](<../compendium/readable/domains/D14.md>). Bridges: B04. Worked models: L02, L03.

### T05 · Poisson geometry to exact Moyal partners and coherent dynamics

**Question.** When does a nonlinear Hamiltonian admit exact classical–quantum partners, and when does equality persist under evolution?

Fix one canonical pair, a characteristic-zero coefficient field and the flat Weyl–Moyal convention. Compute every nonzero odd transvectant gate rather than only the cubic correction. L06 makes this finite polynomial calculation inspectable. Then read the Hamiltonian note: separate the one-step kernel E(H), active partners with nonzero first bracket, the iterated invariant core D∞(H), exact Lie sectors and product closure. The note supplies all-degree proofs for its stated cubic, homogeneous-quartic, qF(p) and monomial classes, while finite fixtures independently replay named instances. The observability bridge interprets the coherent core as the invariant space invisible to correction outputs; exact invariance must be checked in the full polynomial ring.

**Constructive checkpoint.** Read the universal-observable theorem of Robert with its quantifier before comparing a restricted polynomial partner family. Reproduce a partner whose second action fails, and contrast it with an invariant exact sector. Use the pinned PerfectJet documents to locate the existing full-sextic through-degree-20 result.

**Boundary.** Universal Schwartz-observable exactness is different from a restricted infinite polynomial sector. The retained full-space sextic classification has archived msolve dependencies; degrees 21 and above and independent proof-carrying replay remain separate obligations. A nonlinear canonical map need not preserve the same flat star product.

Reading sequence: [D06-F02](<../compendium/readable/domains/D06.md>) → [D03-F04](<../compendium/readable/domains/D03.md>) → [D16-F03](<../compendium/readable/domains/D16.md>) → [D16-F06](<../compendium/readable/domains/D16.md>) → [D14-F03](<../compendium/readable/domains/D14.md>) → [D15-F01](<../compendium/readable/domains/D15.md>).

Domains: [D06](<../compendium/readable/domains/D06.md>) · [D03](<../compendium/readable/domains/D03.md>) · [D16](<../compendium/readable/domains/D16.md>) · [D14](<../compendium/readable/domains/D14.md>) · [D15](<../compendium/readable/domains/D15.md>). Bridges: B05. Worked models: L06.

### T06 · Arithmetic reduction with complete orbit certificates

**Question.** How can a finite certificate establish a statement about an infinite arithmetic family?

Begin with the scalar ring, residue system and p-adic precision. A root modulo p^n becomes a genuine p-adic root only with a compatible lifting and completeness argument. Cyclotomic reduction then provides a finite exact map whose fibres can be exhausted. L07 evaluates the unit reduction underlying the displayed phase map. Move to Pell orbits next: a unit action generates candidates, but a reduction argument and complete seed list are required for exhaustiveness. L10 navigates exact integer iterates of a proved orbit decomposition. Norm forms and elliptic height lattices extend the same pattern while adding class, unit, descent and saturation conditions.

**Constructive checkpoint.** Display one exact congruence or determinant certificate and state the theorem connecting it to the infinite result. For a Pell claim, identify all seeds and verify the descent that reaches them, rather than only computing many iterates.

**Boundary.** Finite residues do not certify an exact zero by themselves. A rational-point search does not prove completeness without the corresponding descent, rank and saturation obligations.

Reading sequence: [D01-F01](<../compendium/readable/domains/D01.md>) → [D01-F03](<../compendium/readable/domains/D01.md>) → [D01-F04](<../compendium/readable/domains/D01.md>) → [D01-F05](<../compendium/readable/domains/D01.md>) → [D02-F02](<../compendium/readable/domains/D02.md>) → [D14-F03](<../compendium/readable/domains/D14.md>).

Domains: [D01](<../compendium/readable/domains/D01.md>) · [D02](<../compendium/readable/domains/D02.md>) · [D09](<../compendium/readable/domains/D09.md>) · [D14](<../compendium/readable/domains/D14.md>). Bridges: B06. Worked models: L07, L10.

### T07 · Periods, singular differential equations and asymptotic constants

**Question.** How does a specified integral become a differential equation and a controlled limiting value?

Use the exact-integral family to establish a convergent representation, a branch and an interchange argument. Mellin moments provide a transparent example with a rational tail bound. For a parameter-dependent period, supply its operator and cycle data before calling it Picard–Fuchs. The Frobenius divided difference demonstrates how a logarithm emerges from coalescing exponents while the normalized Wronskian stays nonzero. Continue around a singular point to distinguish identity monodromy from a matrix whose eigenvalues are merely all one. Finish with the factorial Borel model, cubic fold and elliptic logarithmic constant: each states a small parameter and a quantified finite remainder or exact scaling identity.

**Constructive checkpoint.** Carry branch, cycle, normalization and operator metadata through one calculation. Distinguish a removable basis pole from singular boundary data, then compare a convergent evaluation with a divergent but valid finite asymptotic expansion.

**Boundary.** A period name does not recover a missing differential operator. A local germ does not determine global Stokes constants, and naming a period does not prove algebraic independence.

Reading sequence: [D01-F06](<../compendium/readable/domains/D01.md>) → [D02-F04](<../compendium/readable/domains/D02.md>) → [D05-F04](<../compendium/readable/domains/D05.md>) → [D07-F03](<../compendium/readable/domains/D07.md>) → [D08-F03](<../compendium/readable/domains/D08.md>) → [D08-F04](<../compendium/readable/domains/D08.md>).

Domains: [D01](<../compendium/readable/domains/D01.md>) · [D02](<../compendium/readable/domains/D02.md>) · [D05](<../compendium/readable/domains/D05.md>) · [D07](<../compendium/readable/domains/D07.md>) · [D08](<../compendium/readable/domains/D08.md>). Bridges: B02, B03. Worked models: documented recipes; no dedicated lab.

### T08 · From random laws to reliable robust decisions

**Question.** Which uncertainty model supports a useful action guarantee?

Specify the joint law or deterministic uncertainty set before computing a variance or worst-case range. Stochastic dynamics requires its own time discretization and Itô correction; a marginal law does not determine dependence. Conditional risk identifies uncertainty left by the observation itself, whereas independent repeated measurements may only reduce sensor noise. Statistical validation then asks whether a procedure calibrated on one sample predicts another. In the deterministic branch, duality and robust difference bounds provide certificates for an action across a declared set. Correlated errors can cancel in a comparison even when their separate marginal intervals are wide.

**Constructive checkpoint.** Separate irreducible target uncertainty, observation noise, model uncertainty and finite-sample calibration. In L08 check the exact action difference under a shared variable, and in L01 test whether a new probe removes a target-relevant null direction.

**Boundary.** A deterministic interval is not a confidence interval without a probabilistic coverage argument. Development-set optimality is neither causal evidence nor an out-of-sample guarantee.

Reading sequence: [D10-F01](<../compendium/readable/domains/D10.md>) → [D10-F03](<../compendium/readable/domains/D10.md>) → [D11-F01](<../compendium/readable/domains/D11.md>) → [D11-F03](<../compendium/readable/domains/D11.md>) → [D12-F01](<../compendium/readable/domains/D12.md>) → [D12-F04](<../compendium/readable/domains/D12.md>) → [D15-F04](<../compendium/readable/domains/D15.md>).

Domains: [D10](<../compendium/readable/domains/D10.md>) · [D11](<../compendium/readable/domains/D11.md>) · [D12](<../compendium/readable/domains/D12.md>) · [D15](<../compendium/readable/domains/D15.md>). Bridges: B01, B04. Worked models: L08, L01.

## Domain reading sequences

Each sequence follows the atlas chapter’s concept order. The checkpoint is the family’s declared central question; its worked proof and example appear in the linked domain. Source anchors provide direct entry points into the annual material. The final frontier is a task left open in this retained collection, not a claim about worldwide mathematical novelty.

## D01

**Arithmetic and number fields**

How can an exact arithmetic construction retain its scalar domain, local data and completeness certificate as it is transported into a larger mathematical framework?

| Order | Family and constructive checkpoint | Direct source entry points | Implemented link or recipe |
|---:|---|---|---|
| 1 | [D01-F01 — Arithmetic types, completions and certified p-adic precision](<../compendium/readable/domains/D01.md>). Which arithmetic statements survive a change of scalar domain, and what can a finite p-adic calculation actually certify? | [2023:M001](<../compendium/readable/years/2023/M001.md>) · [2023:M002](<../compendium/readable/years/2023/M002.md>) · [2025:Y25-08-907](<../compendium/readable/years/2025/Y25-08-907.md>) | Documented recipe / worked proof |
| 2 | [D01-F02 — Divisor incidence, valuations and constructive integer parametrization](<../compendium/readable/domains/D01.md>). How can multiplicative arithmetic become a finite lattice calculation with a complete certificate? | [2025:Y25-05-020](<../compendium/readable/years/2025/Y25-05-020.md>) · [2025:Y25-06-004](<../compendium/readable/years/2025/Y25-06-004.md>) · [2026:Y26-01-006](<../compendium/readable/years/2026/Y26-01-006.md>) | Documented recipe / worked proof |
| 3 | [D01-F03 — Cyclotomic degrees, Galois fibres and trace transport](<../compendium/readable/domains/D01.md>). What exact structure follows from conductor 1680, and which additional certificates are needed to connect it to another representation? | [2025:Y25-04-001](<../compendium/readable/years/2025/Y25-04-001.md>) · [2025:Y25-05-003](<../compendium/readable/years/2025/Y25-05-003.md>) · [2025:Y25-10-026](<../compendium/readable/years/2025/Y25-10-026.md>) | L07 |
| 4 | [D01-F04 — Quadratic units, complete Pell orbits and congruence populations](<../compendium/readable/domains/D01.md>). When does a recurrence describe every integer solution, and how do finite congruence filters change an infinite population? | [2024:Y24-03-024](<../compendium/readable/years/2024/Y24-03-024.md>) · [2026:Y26-05-005](<../compendium/readable/years/2026/Y26-05-005.md>) · [2026:Y26-09-029](<../compendium/readable/years/2026/Y26-09-029.md>) | L10 |
| 5 | [D01-F05 — Number fields, norm forms and arithmetic obstructions](<../compendium/readable/domains/D01.md>). Which field, ideal and lattice data are sufficient to turn a norm identity into a complete arithmetic statement? | [2025:Y25-07-022](<../compendium/readable/years/2025/Y25-07-022.md>) · [2025:Y25-07-023](<../compendium/readable/years/2025/Y25-07-023.md>) · [2026:Y26-06-009](<../compendium/readable/years/2026/Y26-06-009.md>) | Documented recipe / worked proof |
| 6 | [D01-F06 — Modular forms, Hecke relations and arithmetic local factors](<../compendium/readable/domains/D01.md>). Which identities genuinely characterize modular arithmetic, rather than an arbitrary prime-indexed statistic? | [2024:Y24-06-008](<../compendium/readable/years/2024/Y24-06-008.md>) · [2024:Y24-09-025](<../compendium/readable/years/2024/Y24-09-025.md>) · [2024:Y24-12-020](<../compendium/readable/years/2024/Y24-12-020.md>) | Documented recipe / worked proof |
| 7 | [D01-F07 — Euler products, prime sums and the analytic burden of identification](<../compendium/readable/domains/D01.md>). How do multiplicative identities become analytic formulas without losing signs, prime powers, convergence or main terms? | [2024:Y24-09-018](<../compendium/readable/years/2024/Y24-09-018.md>) · [2024:Y24-10-009](<../compendium/readable/years/2024/Y24-10-009.md>) · [2024:Y24-10-010](<../compendium/readable/years/2024/Y24-10-010.md>) | Documented recipe / worked proof |

**Cross-domain continuation.** T06 · T07.

**Next boundary.** The most valuable extensions would certify complete unit bases and lattice-return conditions for the norm examples, extend seed proofs to additional Pell cores, and provide explicit integral intertwiners for the proposed conductor-to-lattice bridge. Each is a precise missing theorem or certificate rather than an unspecified generalization.

## D02

**Algebraic and arithmetic geometry**

Which geometric model, maps and comparison data make a claim about arithmetic, singularities or cohomology precise enough to prove?

| Order | Family and constructive checkpoint | Direct source entry points | Implemented link or recipe |
|---:|---|---|---|
| 1 | [D02-F01 — Algebraic maps, singularities and the choice of smooth model](<../compendium/readable/domains/D02.md>). Which geometric information is preserved by a parametrization, a birational coordinate change or a normalization? | [2023:M098](<../compendium/readable/years/2023/M098.md>) · [2023:M102](<../compendium/readable/years/2023/M102.md>) · [2024:Y24-10-019](<../compendium/readable/years/2024/Y24-10-019.md>) | Documented recipe / worked proof |
| 2 | [D02-F03 — Divisors, compactification and projective positivity](<../compendium/readable/domains/D02.md>). What separate certificates establish a smooth quotient, a well-behaved boundary, positivity and an actual projective embedding? | [2023:M027](<../compendium/readable/years/2023/M027.md>) · [2023:M028](<../compendium/readable/years/2023/M028.md>) · [2023:M029](<../compendium/readable/years/2023/M029.md>) | Documented recipe / worked proof |
| 3 | [D02-F02 — Elliptic arithmetic: local counts, global points and height lattices](<../compendium/readable/domains/D02.md>). How far can exact local and group-law certificates take us toward rational rank, and where do descent and global conjectures enter? | [2024:Y24-09-012](<../compendium/readable/years/2024/Y24-09-012.md>) · [2024:Y24-09-013](<../compendium/readable/years/2024/Y24-09-013.md>) · [2024:Y24-12-025](<../compendium/readable/years/2024/Y24-12-025.md>) | Documented recipe / worked proof |
| 4 | [D02-F04 — Cohomological realizations, Hodge filtrations and comparison types](<../compendium/readable/domains/D02.md>). Which information survives a realization, and what additional structure is required before two cohomology theories can be compared? | [2023:M097](<../compendium/readable/years/2023/M097.md>) · [2024:Y24-07-011](<../compendium/readable/years/2024/Y24-07-011.md>) · [2024:Y24-08-009](<../compendium/readable/years/2024/Y24-08-009.md>) | Documented recipe / worked proof |

**Cross-domain continuation.** T06 · T07.

**Next boundary.** The next substantial work would supply explicit global compactification data in a fixed higher-dimensional example, certified descent and saturation for the elliptic subgroup, and correctly graded functorial comparison maps. A numerical invariant can assist those tasks but cannot replace the relevant geometry or cohomology.

## D03

**Algebra and representation theory: structures, actions and exact certificates**

What algebraic structure is specified, and which exact maps or identities justify the invariant being claimed?

| Order | Family and constructive checkpoint | Direct source entry points | Implemented link or recipe |
|---:|---|---|---|
| 1 | [D03-F01 — Typed operations, quotients and finite algebraic structure](<../compendium/readable/domains/D03.md>). Which operations, equations and equivalences actually determine an algebra, and which information survives quotienting? | [2024:Y24-06-001](<../compendium/readable/years/2024/Y24-06-001.md>) · [2024:Y24-09-003](<../compendium/readable/years/2024/Y24-09-003.md>) · [2025:Y25-12-020](<../compendium/readable/years/2025/Y25-12-020.md>) | Documented recipe / worked proof |
| 2 | [D03-F02 — Exact matrix structure, metrics and spectral certificates](<../compendium/readable/domains/D03.md>). Which finite identities certify rank, spectrum and decomposition, and which metric is each certificate using? | [2023:M059](<../compendium/readable/years/2023/M059.md>) · [2023:M068](<../compendium/readable/years/2023/M068.md>) · [2023:M083](<../compendium/readable/years/2023/M083.md>) | L01, L04 |
| 3 | [D03-F03 — Symmetry as an action, representation and orbit calculation](<../compendium/readable/domains/D03.md>). What does a specified symmetry force, and which numerical features remain free after imposing it? | [2023:M033](<../compendium/readable/years/2023/M033.md>) · [2023:M036](<../compendium/readable/years/2023/M036.md>) · [2023:M038](<../compendium/readable/years/2023/M038.md>) | L02 |
| 4 | [D03-F04 — Lie brackets, octonion associators and exceptional weight structure](<../compendium/readable/domains/D03.md>). Which identities survive a nonassociative or graded product, and what additional data turn exceptional dimensions into a Lie algebra? | [2023:M007](<../compendium/readable/years/2023/M007.md>) · [2023:M008](<../compendium/readable/years/2023/M008.md>) · [2024:Y24-05-004](<../compendium/readable/years/2024/Y24-05-004.md>) | Documented recipe / worked proof |
| 5 | [D03-F05 — Local algebras, jets, path bases and structural flatness](<../compendium/readable/domains/D03.md>). How do relations determine a finite algebra, and which properties remain constant when those relations vary? | [2023:M095](<../compendium/readable/years/2023/M095.md>) · [2026:Y26-01-034](<../compendium/readable/years/2026/Y26-01-034.md>) · [2026:Y26-07-002](<../compendium/readable/years/2026/Y26-07-002.md>) | Documented recipe / worked proof |
| 6 | [D03-F06 — Finite operator algebras, modular flow and equilibrium](<../compendium/readable/domains/D03.md>). What do a faithful state and its dynamics determine exactly in a finite algebra? | [2023:M103](<../compendium/readable/years/2023/M103.md>) · [2025:Y25-03-012](<../compendium/readable/years/2025/Y25-03-012.md>) · [2025:Y25-03-014](<../compendium/readable/years/2025/Y25-03-014.md>) | Documented recipe / worked proof |

**Cross-domain continuation.** T01 · T05.

**Next boundary.** Recover the actual multiplication, representation and cochain matrices behind the larger historical objects; then test completeness of invariants, exceptional bracket identities and parameter-stratified derived invariants.

## D04

**Categories and homological methods**

Which constructions preserve the object, and what explicit maps certify preservation?

| Order | Family and constructive checkpoint | Direct source entry points | Implemented link or recipe |
|---:|---|---|---|
| 1 | [D04-F01 — Universal constructions, quotients and equivalence](<../compendium/readable/domains/D04.md>). Which maps descend through a quotient, and which reversible constructions preserve the whole mathematical problem? | [2024:Y24-05-010](<../compendium/readable/years/2024/Y24-05-010.md>) · [2025:Y25-02-013](<../compendium/readable/years/2025/Y25-02-013.md>) · [2025:Y25-06-007](<../compendium/readable/years/2025/Y25-06-007.md>) | Documented recipe / worked proof |
| 2 | [D04-F02 — Chain complexes, exactness and certificates of equivalence](<../compendium/readable/domains/D04.md>). How can a reduction preserve homology, and what finite identities certify that nothing essential was lost? | [2023:M095](<../compendium/readable/years/2023/M095.md>) · [2024:Y24-10-022](<../compendium/readable/years/2024/Y24-10-022.md>) · [2025:Y25-03-021](<../compendium/readable/years/2025/Y25-03-021.md>) | L09 |
| 3 | [D04-F03 — Derived products, extension classes and deformation obstructions](<../compendium/readable/domains/D04.md>). What information survives in Tor, Ext and a tangent complex that an ordinary product or dimension count discards? | [2025:Y25-01-015](<../compendium/readable/years/2025/Y25-01-015.md>) · [2025:Y25-05-011](<../compendium/readable/years/2025/Y25-05-011.md>) · [2025:Y25-07-013](<../compendium/readable/years/2025/Y25-07-013.md>) | Documented recipe / worked proof |
| 4 | [D04-F04 — Filtrations, spectral sequences and information at infinity](<../compendium/readable/domains/D04.md>). How much of a total object can be recovered from graded pages, truncations and inverse systems? | [2024:Y24-04-013](<../compendium/readable/years/2024/Y24-04-013.md>) · [2024:Y24-10-025](<../compendium/readable/years/2024/Y24-10-025.md>) · [2025:Y25-01-016](<../compendium/readable/years/2025/Y25-01-016.md>) | Documented recipe / worked proof |

**Cross-domain continuation.** T02.

**Next boundary.** Build actual comparison functors, controlling complexes and higher-coherence maps for the proposed structures; compute unknown differentials and extension classes before claiming equivalence or reconstruction.

## D05

**Topology, cohomology and gluing**

Which global features survive local changes, and which exact obstruction prevents a global construction?

| Order | Family and constructive checkpoint | Direct source entry points | Implemented link or recipe |
|---:|---|---|---|
| 1 | [D05-F01 — Spaces, chains, torsion and refined homology](<../compendium/readable/domains/D05.md>). Which features belong to the space, which to its cell structure, and which survive a change of coefficients? | [2024:Y24-06-014](<../compendium/readable/years/2024/Y24-06-014.md>) · [2024:Y24-06-018](<../compendium/readable/years/2024/Y24-06-018.md>) · [2024:Y24-07-013](<../compendium/readable/years/2024/Y24-07-013.md>) | L09 |
| 2 | [D05-F02 — Persistent topology, interleavings and random birth laws](<../compendium/readable/domains/D05.md>). How does a topological feature persist through a filtration, and what perturbation or randomness can be certified? | [2023:M040](<../compendium/readable/years/2023/M040.md>) · [2024:Y24-08-001](<../compendium/readable/years/2024/Y24-08-001.md>) · [2024:Y24-09-008](<../compendium/readable/years/2024/Y24-09-008.md>) | L09 |
| 3 | [D05-F03 — Local-to-global gluing, cellular sheaves and Hodge obstructions](<../compendium/readable/domains/D05.md>). When can compatible local data be replaced by one global object, and how can the obstruction be calculated exactly? | [2024:Y24-06-009](<../compendium/readable/years/2024/Y24-06-009.md>) · [2024:Y24-09-009](<../compendium/readable/years/2024/Y24-09-009.md>) · [2025:Y25-08-017](<../compendium/readable/years/2025/Y25-08-017.md>) | L05 |
| 4 | [D05-F04 — Periods, cocycles, winding and characteristic classes](<../compendium/readable/domains/D05.md>). Which global defects survive changes of local choices, and what makes their values topological? | [2023:M089](<../compendium/readable/years/2023/M089.md>) · [2024:Y24-06-015](<../compendium/readable/years/2024/Y24-06-015.md>) · [2024:Y24-11-022](<../compendium/readable/years/2024/Y24-11-022.md>) | Documented recipe / worked proof |

**Cross-domain continuation.** T02 · T07.

**Next boundary.** Specify the spaces, coefficient systems, legal filtrations and attachment maps in the larger proposals; produce integer certificates and valid cochain comparisons that preserve the intended global obstruction.

## D06

**Differential and symplectic geometry**

What becomes computable once the metric, form, connection and symmetry are explicitly declared?

| Order | Family and constructive checkpoint | Direct source entry points | Implemented link or recipe |
|---:|---|---|---|
| 1 | [D06-F01 — Metrics, curvature, scale and transport geometry](<../compendium/readable/domains/D06.md>). Which conclusions follow from a declared metric, and which survive a change of scale or representation? | [2024:Y24-06-012](<../compendium/readable/years/2024/Y24-06-012.md>) · [2024:Y24-12-017](<../compendium/readable/years/2024/Y24-12-017.md>) · [2025:Y25-03-008](<../compendium/readable/years/2025/Y25-03-008.md>) | Documented recipe / worked proof |
| 2 | [D06-F02 — Hamiltonian, symplectic and contact structures](<../compendium/readable/domains/D06.md>). How do conservation, reduction and projection follow from a specified geometric form? | [2024:Y24-03-031](<../compendium/readable/years/2024/Y24-03-031.md>) · [2024:Y24-06-003](<../compendium/readable/years/2024/Y24-06-003.md>) · [2024:Y24-07-014](<../compendium/readable/years/2024/Y24-07-014.md>) | Documented recipe / worked proof |
| 3 | [D06-F03 — Connections, gauge covariance, curvature and holonomy](<../compendium/readable/domains/D06.md>). How can local transport and global loop effects be distinguished and checked without confusing flatness with triviality? | [2023:M041](<../compendium/readable/years/2023/M041.md>) · [2024:Y24-12-006](<../compendium/readable/years/2024/Y24-12-006.md>) · [2025:Y25-02-016](<../compendium/readable/years/2025/Y25-02-016.md>) | L05 |
| 4 | [D06-F04 — Curves, moving frames and geometric variational models](<../compendium/readable/domains/D06.md>). Which curve geometry is fixed by curvature, and when does a variational principle actually select a shape? | [2023:M046](<../compendium/readable/years/2023/M046.md>) · [2024:Y24-11-021](<../compendium/readable/years/2024/Y24-11-021.md>) · [2024:Y24-12-001](<../compendium/readable/years/2024/Y24-12-001.md>) | Documented recipe / worked proof |

**Cross-domain continuation.** T02 · T05.

**Next boundary.** Construct genuine two-dimensional transport refinements, verify regular quotient hypotheses and solve geometric variational problems with the full intended boundary conditions; distinguish representation singularities from failure of the underlying structure.

## D07

**Analysis, transforms and special functions**

What analytic representation makes the desired quantity computable without losing its domain, norm or normalization?

| Order | Family and constructive checkpoint | Direct source entry points | Implemented link or recipe |
|---:|---|---|---|
| 1 | [D07-F01 — Transforms, frames and cancellation in a declared norm](<../compendium/readable/domains/D07.md>). When do coefficients preserve information, and how does the chosen measure control a reconstruction error? | [2023:M019](<../compendium/readable/years/2023/M019.md>) · [2023:M066](<../compendium/readable/years/2023/M066.md>) · [2023:M067](<../compendium/readable/years/2023/M067.md>) | L04 |
| 2 | [D07-F02 — Analytic domains, contour certificates and positive spectral functions](<../compendium/readable/domains/D07.md>). What information is certified by local analytic data, and which global conclusions require a domain or positivity theorem? | [2024:Y24-03-026](<../compendium/readable/years/2024/Y24-03-026.md>) · [2024:Y24-08-008](<../compendium/readable/years/2024/Y24-08-008.md>) · [2025:Y25-04-012](<../compendium/readable/years/2025/Y25-04-012.md>) | Documented recipe / worked proof |
| 3 | [D07-F03 — Exact integrals, special functions and normalized periods](<../compendium/readable/domains/D07.md>). How can an integral be reduced to an exact constant while keeping convergence, branch and normalization information visible? | [2023:M014](<../compendium/readable/years/2023/M014.md>) · [2023:M034](<../compendium/readable/years/2023/M034.md>) · [2023:M050](<../compendium/readable/years/2023/M050.md>) | Documented recipe / worked proof |
| 4 | [D07-F04 — Self-adjoint spectra, heat traces and spectral dimension](<../compendium/readable/domains/D07.md>). What does a spectrum actually determine, and which operator-domain and multiplicity data are needed before using it? | [2023:M024](<../compendium/readable/years/2023/M024.md>) · [2024:Y24-09-021](<../compendium/readable/years/2024/Y24-09-021.md>) · [2024:Y24-09-016](<../compendium/readable/years/2024/Y24-09-016.md>) | Documented recipe / worked proof |

**Cross-domain continuation.** T03 · T07.

**Next boundary.** The main frontier is a portable certificate that carries domains, measures, branches, multiplicities and uniform error bounds through changes of representation. The recovered material does not yet provide one general automated solver.

## D08

**Differential equations and asymptotics**

How does a stated equation produce a controlled solution, approximation or limiting law?

| Order | Family and constructive checkpoint | Direct source entry points | Implemented link or recipe |
|---:|---|---|---|
| 1 | [D08-F01 — Evolution equations through conservation and energy](<../compendium/readable/domains/D08.md>). Which quantities are transported, conserved or dissipated by the stated evolution law and boundary conditions? | [2023:M009](<../compendium/readable/years/2023/M009.md>) · [2024:Y24-04-020](<../compendium/readable/years/2024/Y24-04-020.md>) · [2024:Y24-04-021](<../compendium/readable/years/2024/Y24-04-021.md>) | Documented recipe / worked proof |
| 2 | [D08-F02 — Discretization, truncation and controlled approximation](<../compendium/readable/domains/D08.md>). Which finite approximation preserves the model’s invariants, and what bound connects it to the intended continuous object? | [2023:M044](<../compendium/readable/years/2023/M044.md>) · [2025:Y25-02-007](<../compendium/readable/years/2025/Y25-02-007.md>) · [2025:Y25-05-006](<../compendium/readable/years/2025/Y25-05-006.md>) | L04 |
| 3 | [D08-F03 — Regular-singular equations, normalized bases and monodromy](<../compendium/readable/domains/D08.md>). How should a parameter-dependent local basis be chosen so logarithms, resonances and continuation data remain meaningful? | [2025:Y25-02-014](<../compendium/readable/years/2025/Y25-02-014.md>) · [2025:Y25-07-014](<../compendium/readable/years/2025/Y25-07-014.md>) · [2025:Y25-08-016](<../compendium/readable/years/2025/Y25-08-016.md>) | Documented recipe / worked proof |
| 4 | [D08-F04 — Asymptotic expansions, singular scales and exponentially small data](<../compendium/readable/domains/D08.md>). What does a finite asymptotic expansion determine, and how can its remainder and missing exponential contribution be made explicit? | [2023:M113](<../compendium/readable/years/2023/M113.md>) · [2025:Y25-03-006](<../compendium/readable/years/2025/Y25-03-006.md>) · [2025:Y25-08-027](<../compendium/readable/years/2025/Y25-08-027.md>) | Documented recipe / worked proof |

**Cross-domain continuation.** T03 · T07.

**Next boundary.** Uniform multi-parameter error bounds, resonant basis normalization, nonlinear invariant-preserving schemes and global selection of asymptotic branches remain the central extensions.

## D09

**Dynamics, mechanics and mathematical modeling**

What state, metric and invariant make a dynamical claim precise and testable?

| Order | Family and constructive checkpoint | Direct source entry points | Implemented link or recipe |
|---:|---|---|---|
| 1 | [D09-F01 — Stability in the right metric, including transient and hybrid behavior](<../compendium/readable/domains/D09.md>). Which norm or storage function certifies decay when eigenvalues, Euclidean growth and switching tell different stories? | [2023:M058](<../compendium/readable/years/2023/M058.md>) · [2024:Y24-03-032](<../compendium/readable/years/2024/Y24-03-032.md>) · [2025:Y25-04-027](<../compendium/readable/years/2025/Y25-04-027.md>) | L05 |
| 2 | [D09-F02 — Local bifurcation, exact cycles and the boundary of chaos claims](<../compendium/readable/domains/D09.md>). Which changes of stability can be derived from a return map, and what additional work separates a local bifurcation from global chaos? | [2023:M091](<../compendium/readable/years/2023/M091.md>) · [2024:Y24-04-018](<../compendium/readable/years/2024/Y24-04-018.md>) · [2024:Y24-04-019](<../compendium/readable/years/2024/Y24-04-019.md>) | Documented recipe / worked proof |
| 3 | [D09-F03 — Mechanics, dimensional modeling and invariant flow coordinates](<../compendium/readable/domains/D09.md>). Which quantities and scaling laws survive a change of coordinates, units or time parameter? | [2023:M064](<../compendium/readable/years/2023/M064.md>) · [2023:M070](<../compendium/readable/years/2023/M070.md>) · [2023:M113](<../compendium/readable/years/2023/M113.md>) | Documented recipe / worked proof |
| 4 | [D09-F04 — Memory, recurrence and the information needed for a closed evolution](<../compendium/readable/domains/D09.md>). When does a reduced state determine its own future, and what exact memory or symbolic data repair a failure of closure? | [2024:Y24-07-001](<../compendium/readable/years/2024/Y24-07-001.md>) · [2024:Y24-09-011](<../compendium/readable/years/2024/Y24-09-011.md>) · [2025:Y25-03-023](<../compendium/readable/years/2025/Y25-03-023.md>) | Documented recipe / worked proof |

**Cross-domain continuation.** T03 · T06.

**Next boundary.** The most useful next step is to combine certified basins, physically meaningful transient norms and minimal sufficient reduced states for specific models, with quantitative memory-approximation bounds.

## D10

**Probability and stochastic processes**

What is the complete law, and which operations preserve or transform the uncertainty needed by the question?

| Order | Family and constructive checkpoint | Direct source entry points | Implemented link or recipe |
|---:|---|---|---|
| 1 | [D10-F01 — Probability laws, moments and joint dependence](<../compendium/readable/domains/D10.md>). Which parts of a conclusion follow from marginal probabilities, and which require a full joint law? | [2023:M060](<../compendium/readable/years/2023/M060.md>) · [2023:M106](<../compendium/readable/years/2023/M106.md>) · [2024:Y24-04-008](<../compendium/readable/years/2024/Y24-04-008.md>) | Documented recipe / worked proof |
| 2 | [D10-F02 — Random filtrations, weighted sampling and exact inclusion laws](<../compendium/readable/domains/D10.md>). How can random selection be transported into an exact expectation of a combinatorial or topological observable? | [2026:Y26-02-003](<../compendium/readable/years/2026/Y26-02-003.md>) · [2026:Y26-02-002](<../compendium/readable/years/2026/Y26-02-002.md>) · [2025:Y25-03-029](<../compendium/readable/years/2025/Y25-03-029.md>) | L02, L09 |
| 3 | [D10-F03 — Stochastic dynamics, Itô correction and finite-horizon prediction](<../compendium/readable/domains/D10.md>). Which drift, noise and observation model determines the uncertainty at a future time? | [2024:Y24-05-012](<../compendium/readable/years/2024/Y24-05-012.md>) · [2025:Y25-12-007](<../compendium/readable/years/2025/Y25-12-007.md>) · [2025:Y25-12-027](<../compendium/readable/years/2025/Y25-12-027.md>) | L01 |
| 4 | [D10-F04 — Scaling limits, stable laws and the geometry of approximation](<../compendium/readable/domains/D10.md>). When does repeated averaging simplify a law, and which quantitative information survives the limit? | [2024:Y24-06-019](<../compendium/readable/years/2024/Y24-06-019.md>) · [2026:Y26-05-003](<../compendium/readable/years/2026/Y26-05-003.md>) · [2026:Y26-01-027](<../compendium/readable/years/2026/Y26-01-027.md>) | Documented recipe / worked proof |

**Cross-domain continuation.** T04 · T08.

**Next boundary.** Combine exact finite combinatorial expectations with quantitative approximation of stochastic dynamics, retaining explicit dependence, topology and error metrics rather than replacing them by one scalar uncertainty score.

## D11

**Information, statistics and inference**

What does the available observation distinguish, and what claim does its evidence actually justify?

| Order | Family and constructive checkpoint | Direct source entry points | Implemented link or recipe |
|---:|---|---|---|
| 1 | [D11-F01 — Covariance geometry, nonlinear uncertainty and hidden-target risk](<../compendium/readable/domains/D11.md>). Which uncertainty is reducible by precision, and which requires a different observation? | [2026:Y26-09-022](<../compendium/readable/years/2026/Y26-09-022.md>) · [2026:Y26-02-025](<../compendium/readable/years/2026/Y26-02-025.md>) · [2024:Y24-04-006](<../compendium/readable/years/2024/Y24-04-006.md>) | L01, L08 |
| 2 | [D11-F02 — Entropy contraction, channel information and Fisher geometry](<../compendium/readable/domains/D11.md>). Which information quantity is monotone under a declared transformation, and what geometry does it induce? | [2023:M026](<../compendium/readable/years/2023/M026.md>) · [2023:M047](<../compendium/readable/years/2023/M047.md>) · [2024:Y24-07-002](<../compendium/readable/years/2024/Y24-07-002.md>) | Documented recipe / worked proof |
| 3 | [D11-F03 — Identifiability, calibration and honest statistical validation](<../compendium/readable/domains/D11.md>). What mathematical contract turns a fitted pattern into a justified inference about unseen outcomes? | [2025:Y25-02-012](<../compendium/readable/years/2025/Y25-02-012.md>) · [2025:Y25-05-021](<../compendium/readable/years/2025/Y25-05-021.md>) · [2026:Y26-09-004](<../compendium/readable/years/2026/Y26-09-004.md>) | Documented recipe / worked proof |
| 4 | [D11-F04 — Finite information, observation equivalence and diagnostic statistics](<../compendium/readable/domains/D11.md>). How much can an observation distinguish, and what information does a summary discard? | [2026:Y26-06-028](<../compendium/readable/years/2026/Y26-06-028.md>) · [2026:Y26-02-034](<../compendium/readable/years/2026/Y26-02-034.md>) · [2026:Y26-02-023](<../compendium/readable/years/2026/Y26-02-023.md>) | L02 |

**Cross-domain continuation.** T01 · T04 · T08.

**Next boundary.** Design observations sufficient for a specified target or action, then combine exact structural guarantees with independent finite-sample calibration without conflating identifiability, uncertainty and predictive performance.

## D12

**Optimization and decision theory**

Which objective, feasible set and certificate turn a proposed choice into a justified global decision?

| Order | Family and constructive checkpoint | Direct source entry points | Implemented link or recipe |
|---:|---|---|---|
| 1 | [D12-F01 — Convex duality, singular quadratic programs and global certificates](<../compendium/readable/domains/D12.md>). What finite certificate proves global optimality, including null directions and boundary cases? | [2023:M062](<../compendium/readable/years/2023/M062.md>) · [2023:M093](<../compendium/readable/years/2023/M093.md>) · [2025:Y25-12-009](<../compendium/readable/years/2025/Y25-12-009.md>) | Documented recipe / worked proof |
| 2 | [D12-F02 — Proximal maps, projected descent and stable optimization dynamics](<../compendium/readable/domains/D12.md>). Which update respects the feasible geometry and comes with a descent or contraction theorem? | [2024:Y24-04-003](<../compendium/readable/years/2024/Y24-04-003.md>) · [2025:Y25-10-021](<../compendium/readable/years/2025/Y25-10-021.md>) · [2025:Y25-12-015](<../compendium/readable/years/2025/Y25-12-015.md>) | Documented recipe / worked proof |
| 3 | [D12-F03 — Objective design, discrete selection and certified finite search](<../compendium/readable/domains/D12.md>). Which feasible set and objective make a proposed improvement mathematically meaningful? | [2024:Y24-04-001](<../compendium/readable/years/2024/Y24-04-001.md>) · [2024:Y24-04-002](<../compendium/readable/years/2024/Y24-04-002.md>) · [2025:Y25-02-003](<../compendium/readable/years/2025/Y25-02-003.md>) | L02, L03 |
| 4 | [D12-F04 — Shared uncertainty, robust margins and decision-sufficient measurement](<../compendium/readable/domains/D12.md>). What must be measured to certify the decision, rather than reconstruct every uncertain score? | [2026:Y26-10-023](<../compendium/readable/years/2026/Y26-10-023.md>) · [2026:Y26-01-033](<../compendium/readable/years/2026/Y26-01-033.md>) · [2023:M055](<../compendium/readable/years/2023/M055.md>) | L08 |

**Cross-domain continuation.** T01 · T04 · T08.

**Next boundary.** Construct exact positivity and dual certificates for nonlinear decision differences, then optimize finite measurement trees whose outcome fibres preserve those certificates at minimum guaranteed cost.

## D13

**Combinatorics and graph mathematics**

What exact information must be retained to count, distinguish or compose finite structures?

| Order | Family and constructive checkpoint | Direct source entry points | Implemented link or recipe |
|---:|---|---|---|
| 1 | [D13-F01 — Exact populations: products, recurrences and reversible addresses](<../compendium/readable/domains/D13.md>). How can a finite combinatorial population be counted, optimized and indexed without confusing objects with their statistics? | [2023:M035](<../compendium/readable/years/2023/M035.md>) · [2024:Y24-07-008](<../compendium/readable/years/2024/Y24-07-008.md>) · [2026:Y26-05-021](<../compendium/readable/years/2026/Y26-05-021.md>) | L02 |
| 2 | [D13-F03 — Incidence kernels, path differences and primal–dual graph witnesses](<../compendium/readable/domains/D13.md>). How do local incidence constraints produce global cycles, and when does a short witness prove an optimal graph action count? | [2024:Y24-10-032](<../compendium/readable/years/2024/Y24-10-032.md>) · [2026:Y26-04-001](<../compendium/readable/years/2026/Y26-04-001.md>) · [2026:Y26-04-027](<../compendium/readable/years/2026/Y26-04-027.md>) | L09 |
| 3 | [D13-F02 — Graph observations: spectra, cut censuses and stronger energy probes](<../compendium/readable/domains/D13.md>). Which graph features survive an observation, and what extra measurement separates a known collision? | [2023:M020](<../compendium/readable/years/2023/M020.md>) · [2025:Y25-08-023](<../compendium/readable/years/2025/Y25-08-023.md>) · [2025:Y25-08-024](<../compendium/readable/years/2025/Y25-08-024.md>) | L03 |
| 4 | [D13-F04 — Separators, semiring elimination and multiplicity-preserving quotients](<../compendium/readable/domains/D13.md>). What boundary state is sufficient to compose local computations without changing a count or optimum? | [2026:Y26-08-804](<../compendium/readable/years/2026/Y26-08-804.md>) · [2026:Y26-09-006](<../compendium/readable/years/2026/Y26-09-006.md>) · [2026:Y26-10-015](<../compendium/readable/years/2026/Y26-10-015.md>) | L02 |

**Cross-domain continuation.** T02 · T04.

**Next boundary.** Recover original large-instance tables and proof dependencies; characterize the distinguishing strength of bounded-height graph observations; build minimal boundary quotients that preserve counts as well as values.

## D14

**Logic, computation and exact certification**

Which semantics and finite witnesses justify a global computational claim?

| Order | Family and constructive checkpoint | Direct source entry points | Implemented link or recipe |
|---:|---|---|---|
| 1 | [D14-F01 — Future equivalence, bisimulation and executable quotient states](<../compendium/readable/domains/D14.md>). When can two internal states be merged while preserving every permitted future observation? | [2025:Y25-09-014](<../compendium/readable/years/2025/Y25-09-014.md>) · [2026:Y26-01-003](<../compendium/readable/years/2026/Y26-01-003.md>) · [2026:Y26-09-006](<../compendium/readable/years/2026/Y26-09-006.md>) | L01 |
| 2 | [D14-F02 — Hankel witnesses and minimal observable memory](<../compendium/readable/domains/D14.md>). How can an exact realization and an independent lower bound prove the smallest recurrence or register dimension? | [2023:M016](<../compendium/readable/years/2023/M016.md>) · [2023:M017](<../compendium/readable/years/2023/M017.md>) · [2026:Y26-03-012](<../compendium/readable/years/2026/Y26-03-012.md>) | L01 |
| 3 | [D14-F03 — Typed proof certificates and the boundary between examples and completeness](<../compendium/readable/domains/D14.md>). What exact claim does each certificate establish, and which dependencies remain outside its proof boundary? | [2024:Y24-10-026](<../compendium/readable/years/2024/Y24-10-026.md>) · [2024:Y24-10-027](<../compendium/readable/years/2024/Y24-10-027.md>) · [2025:Y25-06-024](<../compendium/readable/years/2025/Y25-06-024.md>) | L02 |
| 4 | [D14-F04 — Coding and raw-state recovery by exact lattice certificates](<../compendium/readable/domains/D14.md>). When do finitely many output words determine a hidden state, and how does that injectivity become optimal error correction? | [2023:M037](<../compendium/readable/years/2023/M037.md>) · [2024:Y24-07-003](<../compendium/readable/years/2024/Y24-07-003.md>) · [2026:Y26-05-028](<../compendium/readable/years/2026/Y26-05-028.md>) | Documented recipe / worked proof |

**Cross-domain continuation.** T01 · T04 · T05 · T06.

**Next boundary.** Formalize supplied exact certificates without losing their input semantics; recover operational tables and missing completeness proofs; quantify approximate state reduction separately from exact equivalence.

## D15

**Control, observability and inverse problems**

What can be recovered or controlled from declared observations, at what cost and with what guarantee?

| Order | Family and constructive checkpoint | Direct source entry points | Implemented link or recipe |
|---:|---|---|---|
| 1 | [D15-F01 — Target-relative observation: fibres, factorization and dynamic closure](<../compendium/readable/domains/D15.md>). Which hidden directions matter for the requested target, and when can the observation itself evolve as a closed state? | [2023:M016](<../compendium/readable/years/2023/M016.md>) · [2024:Y24-07-015](<../compendium/readable/years/2024/Y24-07-015.md>) · [2026:Y26-05-010](<../compendium/readable/years/2026/Y26-05-010.md>) | L01 |
| 2 | [D15-F02 — Control energies, compatible metrics and constrained descriptor dynamics](<../compendium/readable/domains/D15.md>). How can a declared system carry a complete stability, reachability or optimal-control certificate? | [2023:M069](<../compendium/readable/years/2023/M069.md>) · [2025:Y25-07-010](<../compendium/readable/years/2025/Y25-07-010.md>) · [2025:Y25-11-030](<../compendium/readable/years/2025/Y25-11-030.md>) | Documented recipe / worked proof |
| 3 | [D15-F03 — Regularized inverse problems: bias, noise and certified stopping](<../compendium/readable/domains/D15.md>). How should finite resolution be chosen when inversion amplifies measurement error? | [2026:Y26-08-901](<../compendium/readable/years/2026/Y26-08-901.md>) · [2026:Y26-08-902](<../compendium/readable/years/2026/Y26-08-902.md>) · [2026:Y26-08-903](<../compendium/readable/years/2026/Y26-08-903.md>) | L04 |
| 4 | [D15-F04 — Cheapest distinguishing experiments and uncertainty-aware decisions](<../compendium/readable/domains/D15.md>). Which next observation resolves the target at minimum guaranteed cost, and when does additional data remain irrelevant? | [2026:Y26-08-016](<../compendium/readable/years/2026/Y26-08-016.md>) · [2026:Y26-09-020](<../compendium/readable/years/2026/Y26-09-020.md>) · [2026:Y26-09-022](<../compendium/readable/years/2026/Y26-09-022.md>) | L01, L08 |

**Cross-domain continuation.** T01 · T03 · T05 · T08.

**Next boundary.** Extend finite fibre certificates to supplied nonlinear or noisy models; derive robust experiment policies with computable lower bounds; select regularization from data without unproved source assumptions.

## D16

**Quantum, deformation and integrable structures: finite models with explicit boundaries**

Which state, product, coherence equation or spectral model is actually implemented, and what finite certificate proves its claimed behaviour?

| Order | Family and constructive checkpoint | Direct source entry points | Implemented link or recipe |
|---:|---|---|---|
| 1 | [D16-F01 — Quantum states, coherence, channels and complete instruments](<../compendium/readable/domains/D16.md>). Which observations distinguish states, and which transformations preserve their physical probability structure? | [2023:M048](<../compendium/readable/years/2023/M048.md>) · [2023:M063](<../compendium/readable/years/2023/M063.md>) · [2024:Y24-06-023](<../compendium/readable/years/2024/Y24-06-023.md>) | L01, L09 |
| 2 | [D16-F02 — Finite Weyl systems, symplectic Pauli geometry and projective phases](<../compendium/readable/domains/D16.md>). What finite operator relations can hold exactly, and how are their commutation and central phases certified? | [2025:Y25-07-015](<../compendium/readable/years/2025/Y25-07-015.md>) · [2025:Y25-04-017](<../compendium/readable/years/2025/Y25-04-017.md>) · [2026:Y26-06-001](<../compendium/readable/years/2026/Y26-06-001.md>) | L07 |
| 3 | [D16-F03 — Polynomial Moyal exactness and the complete bounded sextic monomial atlas](<../compendium/readable/domains/D16.md>). Exactly when does a polynomial Moyal bracket equal its Poisson bracket, and when does a vanished cubic correction hide a fifth-order defect? | [2023:M086](<../compendium/readable/years/2023/M086.md>) · [2026:Y26-06-018](<../compendium/readable/years/2026/Y26-06-018.md>) · [2026:Y26-06-019](<../compendium/readable/years/2026/Y26-06-019.md>) | L06 |
| 4 | [D16-F04 — Braid representations, fusion rules and complete finite coherence data](<../compendium/readable/domains/D16.md>). Which explicit relations turn braid or fusion numbers into a consistent algebraic or categorical structure? | [2024:Y24-06-010](<../compendium/readable/years/2024/Y24-06-010.md>) · [2024:Y24-11-012](<../compendium/readable/years/2024/Y24-11-012.md>) · [2025:Y25-03-028](<../compendium/readable/years/2025/Y25-03-028.md>) | Documented recipe / worked proof |
| 5 | [D16-F05 — Integrable models as finite spectral and tau-function bridges](<../compendium/readable/domains/D16.md>). How can an integrability claim be anchored simultaneously in an explicit operator and a verified scalar equation? | [2023:M011](<../compendium/readable/years/2023/M011.md>) · [2023:M012](<../compendium/readable/years/2023/M012.md>) · [2023:M104](<../compendium/readable/years/2023/M104.md>) | Documented recipe / worked proof |
| 6 | [D16-F06 — Deformations, obstruction equations and Poisson transport](<../compendium/readable/domains/D16.md>). When does a first-order algebraic change extend to a genuine family, and which structural invariants can still jump? | [2024:Y24-08-005](<../compendium/readable/years/2024/Y24-08-005.md>) · [2024:Y24-08-010](<../compendium/readable/years/2024/Y24-08-010.md>) · [2025:Y25-02-015](<../compendium/readable/years/2025/Y25-02-015.md>) | L06 |

**Cross-domain continuation.** T05.

**Next boundary.** Extend the bounded monomial Moyal classification to arbitrary polynomial coefficient varieties; recover full anyon and monodromy matrices; prove all-order or completeness statements only with their actual obstruction or spectral data.

## Focused Hamiltonian route

Read the [Hamiltonian note](../research/hamiltonian/output/Nonlinear_Hamiltonian_Partners.md) after T05. Follow definitions of E(H) and D∞(H), the cubic rank argument, the homogeneous-quartic apolar adjoint, arbitrary qF(p), monomial all-degree organization, and then dynamic closure and quantum ladders. The appendices display the general proofs; exact engines and fixtures replay specified finite examples. Appendix F pins the prior PerfectJet source, classical literature and external-solver boundary. Use the [bibliography](REFERENCES.md) to distinguish current project documents from external primary resources.
