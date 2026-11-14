# Polynomial K3/K4 bridge for the cube-leading boundary

The Lean development now proves the no-slice lemma K3 and the leading-form
conclusion of K4 for actual bivariate polynomials over every characteristic-zero
field. It also proves the required coprimality for all three Newton leading
forms. The arbitrary-degree Moyal static reduction and the final core
classification remain conventional proofs.

## Mathematical interface

Write `Poly K = MvPolynomial (Fin 2) K`, with `X 0 = q` and `X 1 = P`.
The operators are defined using Mathlib's `pderiv`, not supplied as abstract
functions:

\[
D_hf=h_qf_P-h_Pf_q,\qquad
E_wf=w_q qf_q+w_P Pf_P.
\]

The implementation proves the equivalence between `E_w f = n f` and weighted
homogeneity by comparing every monomial coefficient. For positive variable
weights, it proves that negative-weight forms vanish and that a weight-zero
form is the constant polynomial given by its constant coefficient.

For a nonzero homogeneous `h` of weight `d > w_q + w_P`, relatively prime to
`h_P`, the exported concrete theorems are:

| Theorem | Conclusion and hypotheses beyond those above |
|---|---|
| `polynomial_kernel_forms` | If homogeneous `f` satisfies `D_h f = 0`, then `f = a h^k` for a scalar `a : K` and `k : ℕ`. |
| `polynomial_no_preimage` | For homogeneous `f`, `D_h f` cannot equal `a h^k` with nonzero scalar `a`. |
| `polynomial_no_slice` | If homogeneous `f` is killed by any iterate of `D_h`, then `f = a h^k`. |
| `polynomial_leading_forms_of_stable` | If `H` has top weighted component `h`, every leading form of a finite-dimensional `D_H`-stable polynomial space is `a h^k`. |
| `polynomial_leading_forms_of_stable_nonzero` | The scalar is nonzero for a nonzero polynomial in that space. |

The K4 interface asks for the actual geometric hypotheses that `H` has weight
at most `d` and component `h` at weight `d`. It does not ask the caller for a
weight bound on the stable space, leading-operator compatibility, or a
nilpotence hypothesis.

## The three Newton forms

For every nonzero coefficient `c`, coprimality is proved in the polynomial ring
itself. A common prime divisor would divide both `q` and `P`, contradicting
their relative primality. This includes the reducible middle leading form.

| Case | Leading form | Variable weights | Weight d | Bracket increment |
|---|---|---|---|---|
| I | `P³ + c q⁵` | `(3,5)` | 15 | 7 |
| II | `P³ + c q³ P` | `(2,3)` | 9 | 4 |
| III | `P³ + c q⁴` | `(3,4)` | 12 | 5 |

`case_one_no_slice`, `case_two_no_slice`, and `case_three_no_slice` specialize
K3 without leaving a coprimality hypothesis. The corresponding `case_*_stable`
theorems apply to `H = h + lower` for any polynomial `lower` of weight at most
14, 8, or 11 respectively, and any finite-dimensional space stable under
`D_H`. No coefficient sampling or degree cutoff occurs in these proofs.

## Filtration argument

`Bounded w n f` is a statement about every nonzero coefficient of the actual
polynomial `f`. The proof of `finite_dimensional_bounded` chooses a finite
spanning set and takes the largest weight appearing in its members.

The universal identity `component_bracket_top` states that, for polynomials
bounded by weights `d` and `n`, the component of their bracket at weight
`n + d - w_q - w_P` is the bracket of their top components. Its proof uses
formal differentiation and coefficientwise multiplication, including cases
where the top bracket cancels.

Iteration gives an equality between the component of `D_H^m f` at weight
`n + m δ` and `D_h^m` of the initial leading form. Stability keeps the former
polynomial inside the finite-dimensional space. Once `n + m δ` exceeds that
space's proved bound, the component vanishes. K3 then applies to the initial
leading form. This argument does not assert nilpotence of `D_H`.

## Source and verification

- `CubeLeadingPolynomial.lean`: the concrete `LeadingData` instance, scalar
  identification, and polynomial kernel, no-preimage and K3 theorems.
- `CubeLeadingCoprime.lean`: relative primality for the three leading forms.
- `CubeLeadingFiltration.lean`: polynomial weight bounds, top-component
  transport, finite-dimensional boundedness and K4's leading-form conclusion.
- `CubeLeadingNewton.lean`: the three homogeneous and perturbed specializations.

All four modules build with the repository's pinned Lean 4.19.0 and Mathlib
revision. `AuditCubeLeadingPolynomial.lean` checks 22 declarations; the retained
output lists only `propext`, `Classical.choice`, and `Quot.sound`. No `sorry`,
`admit`, or new axiom is introduced. `TestCubeLeadingPolynomial.lean` checks
the excluded zero-coefficient boundary and a lower-term example where the
leading bracket vanishes while the actual bracket is nonzero.

From `formal/`:

```sh
lake build +SexticC3.CubeLeadingNewton:olean
lake env lean AuditCubeLeadingPolynomial.lean > AuditCubeLeadingPolynomial.actual.txt
diff -u AuditCubeLeadingPolynomial.output.txt AuditCubeLeadingPolynomial.actual.txt
lake env lean TestCubeLeadingPolynomial.lean
```

The `sextic-formal` workflow runs these commands alongside the existing builds
and audits. The coverage table now includes Theorem R; its binomial receipt was
regenerated with the full PerfectJet verifier, changing only the manuscript's
source fingerprint.

## Remaining classification dependencies

This closes dependencies 1–3 of Priority 3 in the Theorem K Lean
plan. It does not formalize the nonlinear transport of the higher flat gates,
the all-degree static recurrences, exclusion of a static partner with leading
form `h²` and arbitrary lower corrections, the final dimension argument, or
the joined ten-parameter classification. Theorem R's symbolic rank-certificate
proof also remains outside Lean. The PerfectJet point replay retains its stated
shared-basis and row-label dependencies.
