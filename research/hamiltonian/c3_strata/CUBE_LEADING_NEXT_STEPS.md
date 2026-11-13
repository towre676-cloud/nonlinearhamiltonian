# Cube-leading refinement and formalization plan

## Established starting point

Work in characteristic zero with

\[
H=P^3+B(q)P+C(q),\qquad P=p+q^2,\qquad \deg B\le3,\quad\deg C\le5.
\]

[Theorems K and G′](CUBE_LEADING_BOUNDARY_THEOREM.md) establish the complete
persistent-core criterion on these ten reduced parameters:

\[
D_\infty(H)=\operatorname{span}\{1,H\}
\quad\Longleftrightarrow\quad B,C\text{ are not both affine}.
\]

On the quadratic-B stratum `b3=c4=c5=0, b2!=0`, the first-refinement jump
is exactly `c3=0`; its dimensions are respectively four and three, and
`S2=span{1,H}` throughout. Neither question should be reopened as a conjecture.

Theorem K is a conventional all-degree proof. Its current Lean modules prove
specified supporting lemmas, not the complete classification. The repository
does not assert external peer review or a full 21-parameter refinement theorem.

## Priority 1: prove the sharp stopping depth

Determine the least uniform integer N such that `S^N=span{1,H}` whenever
one of `b3,c4,c5` is nonzero. The established conservative bounds are N=14
and N=13 on `3*b3+5*c5!=0`; reaching the core by depth five in sampled
members is not a uniform theorem.

Use the three disjoint Newton cases from Theorem K:

| Case | Coefficient conditions | Leading form | Weights `(q,P)` | Weight increment |
|---|---|---|---|---|
| I | `c5!=0` | `P^3+c5*q^5` | `(3,5)` | 7 |
| II | `c5=0, b3!=0` | `P^3+b3*q^3*P` | `(2,3)` | 4 |
| III | `c5=b3=0, c4!=0` | `P^3+c4*q^4` | `(3,4)` | 5 |

Begin the detailed calculation in case III, whose leading form is binomial,
then address cases II and I, including their lower-coefficient resonances.
All lower coefficients remain arbitrary in each final theorem.

Deliverables:

1. An exact rational example ledger listing complete refinement dimensions
   through stabilization, with explicit surviving partners and their first
   nonzero gate. This is discovery evidence only.
2. A proposed uniform bound with a proof covering every coefficient value in
   the case. Prefer a recurrence or filtration argument; retain finite-window
   rank certificates when necessary.
3. Explicit rational members attaining the proposed bound. An upper bound
   without a matching example must not be called sharp.

If a proposed depth bound fails, preserve the Hamiltonian, offending partner,
exact nonzero gate, and corrected dimension sequence as regression data.

## Priority 2: classify the temporary exceptional loci

Determine exactly where `dim S1` and `dim S2` increase in the three cases
above. The eventual core is already known and has no exceptional parameter
value there. A first-refinement exception must not be described as a core
exception.

Use the proved `(q,P)=(1,2)` finite windows: 49 monomials of weight at most
12, improved to 36 monomials of weight at most 10 on
`3*b3+5*c5!=0`. Use the finite first-refinement reduction even on the
infinite-static locus `E=0`; do not replace its infinite static space by an
unproved finite static basis.

For each claimed stratum, retain:

- Defining polynomial equations and nonvanishing conditions in the original
  reduced coefficients, including the field assumptions for any normalization.
- A kernel basis with verified gate identities and a proof that specialization
  preserves its stated dimension. Record every denominator restriction.
- Exact complementary rank certificates, using nonzero minors on open strata
  and unit-ideal or explicit Bezout identities where several minors are needed.
- Complete coverage of the parameter space, including intersections and boundary
  cases. A greatest-common-divisor computation alone does not establish a
  multivariable unit-ideal claim.

Start with the known resonance surfaces `3*b3+5*c5=0` and
`5*b2+9*c4=0`, and the locus `E=0`, as adversarial test sets. Their occurrence
in a recurrence is a reason to investigate them, not a proof that a refinement
dimension jumps there. Account for the derivative-invisible constant `c0`
without omitting it from the stated all-parameter theorem.

## Priority 3: complete the Lean bridge for Theorem K

Build on `formal/SexticC3/CubeLeadingGate.lean` and
`formal/SexticC3/CubeLeadingCore.lean` rather than restating the conclusion as
an assumption. The missing dependencies are:

1. Weighted leading forms and the positive-increment argument for a
   finite-dimensional `D_H`-stable polynomial space. Formalize nilpotence of
   the induced leading operation; do not assert nilpotence of `D_H` itself.
2. Coprimality for the three explicit leading forms and the UFD implication
   `h | s*h_P` and `gcd(h,h_P)=1` implies `h | s`.
3. The homogeneous kernel and no-preimage lemmas, including the weight and
   characteristic-zero hypotheses in the descent.
4. The chart identities and all-degree static recurrences connecting the
   abstract lemmas to the original flat transvectants.
5. Exclusion of every static partner with leading form `h^2`, allowing arbitrary
   lower-weight corrections, followed by the dimension argument.
6. A single exported theorem joining the three new Newton cases to the
   established seven-parameter core classification, with an axiom audit.

Success means an end-to-end theorem without `sorry` or an assumed bivariate
classification. Until then, state exactly which component lemmas are formalized.

## Verification and reproducibility

- Keep symbolic calculations exact over the declared rational or polynomial
  coefficient ring. Numerical rank tests are not certificates.
- Independently compare transported gates with PerfectJet in the original
  `(q,p)` coordinates, using the existing pinned engine. The nonlinear chart
  is symplectic for the Poisson bracket; this does not grant nonlinear
  covariance of the higher flat Moyal gates.
- Replay all claimed identities, rank witnesses and kernel vectors from stored
  data. Distinguish universal symbolic identities from individual point checks.
- Keep the shorter two-minor G′ proof and three-minor Theorem G proof as
  regression anchors while exploring new strata.
- After editing a manuscript included in a receipt's `source_sha256`, regenerate
  that receipt with its documented verifier. Inspect the mathematical-data
  diff separately from source fingerprints, then require the CI comparison to
  pass. Do not remove the source check to accommodate documentation changes.
- Submit each completed theorem or bounded experiment as a separately scoped
  follow-up, preserving counterexamples and explicit evidence limits.

## Wider coverage and review

Use the [Newton coverage table](BINOMIAL_NEWTON_SHARP_THEOREM.md#7-repository-reconciliation-and-remaining-boundaries)
as the current map. The two binomial edges are classified in all degree, with
their lower-weight perturbations. The cube-leading persistent core is now
classified, but its remaining intermediate-refinement loci are not. Other
branches still have separate static-space and full-tower questions; this plan
does not promote their leading-model or finite-window statements into stronger
global results.

Before extending the program to additional Newton boundaries, reconcile the
latest nonconstant quadratic-coefficient results and their exact hypotheses.
Seek independent specialist review of the leading-form/no-preimage argument,
the static recurrence obstruction, and the transport of the higher gates.
Repository integration and passing computational checks are not substitutes
for that mathematical review.

The next finished research increment should be a sharp depth theorem for one
complete Newton case, including a witness attaining the bound and reproducible
certificates. This gives a concrete result while the larger exceptional-locus
and formalization programs proceed.
