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

## Priorities 1 and 2: resolved by Theorem R

[CUBE_LEADING_REFINEMENT_THEOREM.md](CUBE_LEADING_REFINEMENT_THEOREM.md) settles
both former priorities on the whole region where one of `b3,c4,c5` is nonzero.

- Sharp stopping depth: `S^2 = span{1,H}` at every parameter value, so the least
  uniform N is 2, replacing the conservative bounds 14 and 13. Individual
  members stop at depth 1 exactly off the jump loci of cases I and II.
- Temporary exceptional loci, with explicit partners: case I, `b3=0` (partner
  `q`) and `3*b3+10*c5=0` (partner `b3*P+(2*b2+4*c4)*q`); case II,
  `4*c4=5*b3^2` (an explicit quadratic partner `J2`); case III, `q` always and
  `P` exactly on `b2+2*c4=0`. `dim S1` is 2 or 3 in cases I and II and 3 or 4
  in case III; `dim S2` never jumps.
- The resonance surfaces `3*b3+5*c5=0` and `5*b2+9*c4=0` are not jump loci, and
  the locus `E=0` behaves like the rest of `b2+2*c4=0`.
- With the seven-parameter stratum: `S^3 = span{1,H}` whenever `B,C` are not
  both affine, depth 3 being needed exactly on `b2=b3=c3=c4=c5=0`, `c2!=0`.

Every rank bound is a stored minor that is a nonzero constant, a constant times
one named polynomial, or one of two univariate minors with an explicit Bezout
identity; `verify_cube_leading_refinement.py` reconstructs all of them. These
statements should not be reopened as conjectures. The independent PerfectJet
point replay of all thirteen certificates and of the ledger is
`verify_cube_leading_refinement_perfectjet.py`. The coverage table in `BINOMIAL_NEWTON_SHARP_THEOREM.md` now includes Theorem R;
its receipt was regenerated with the full PerfectJet verifier, with only the
manuscript fingerprint changing.

## Priority 3: complete the Lean bridge for Theorem K

Build on `formal/SexticC3/CubeLeadingGate.lean` and
`formal/SexticC3/CubeLeadingCore.lean` rather than restating the conclusion as
an assumption. The dependency list is below; items 1–3 are now complete, as detailed after
the list.

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

Status. Dependencies 1, 2 and 3 are now proved for actual bivariate polynomials
in `CubeLeadingPolynomial.lean`, `CubeLeadingCoprime.lean`,
`CubeLeadingFiltration.lean` and `CubeLeadingNewton.lean`.

- `LeadingData` is instantiated using Mathlib's partial derivatives on
  `MvPolynomial (Fin 2) K`, over every characteristic-zero field K.
- Euler eigenforms are characterized coefficientwise; negative-weight forms
  vanish and positive variable weights force every weight-zero form to be a
  scalar. Concrete kernel, no-preimage and no-slice theorems follow.
- All three explicit leading forms are proved relatively prime to their
  P-derivatives for every nonzero leading coefficient, including the reducible
  middle form. These proofs take place in the polynomial UFD, not its fraction
  field alone.
- Finite-dimensional polynomial spaces are proved to have a common weight
  bound. Top-component transport is proved for the actual Poisson bracket.
  The leading-form conclusion of K4 follows by iterating this identity, without
  assuming boundedness, abstract leading compatibility, or nilpotence of D_H.
- `case_one_stable`, `case_two_stable` and `case_three_stable` allow arbitrary
  strictly lower-weight polynomial perturbations of the three leading forms.

See [the polynomial bridge](CUBE_LEADING_POLYNOMIAL_BRIDGE.md) for exact theorem
interfaces and the axiom audit. Dependencies 4, 5 and 6 remain: the transported
flat gates and all-degree static recurrences, exclusion of h² with all lower
corrections and the dimension argument, and the single full classification
theorem. Theorem K and Theorem R are not yet end-to-end Lean theorems.

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
their lower-weight perturbations. The cube-leading persistent core and its
intermediate refinements are now classified (Theorems K, G′, R). Other
branches still have separate static-space and full-tower questions; this plan
does not promote their leading-model or finite-window statements into stronger
global results.

Before extending the program to additional Newton boundaries, reconcile the
latest nonconstant quadratic-coefficient results and their exact hypotheses.
Seek independent specialist review of the leading-form/no-preimage argument,
the static recurrence obstruction, and the transport of the higher gates.
Repository integration and passing computational checks are not substitutes
for that mathematical review.

The sharp depth theorem and the exceptional-locus classification are complete
for all three Newton cases (Theorem R). The next finished increments are the
Lean bridge of Priority 3 and the independent review described above.
