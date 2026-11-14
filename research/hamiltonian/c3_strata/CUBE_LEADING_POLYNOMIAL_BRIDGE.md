# Polynomial and flat-gate proof of the full cube-leading core criterion

Theorem K is now an end-to-end Lean theorem for the region where at least one
of `b3,c4,c5` is nonzero. The exported theorem
`all_flat_newton_persistent_core` quantifies over every characteristic-zero
field and every polynomial partner, in the original `(q,p)` coordinates.
It identifies the persistent kernel of **all odd flat gates of order at least
three** with `span{1,H}`. Neither finite-dimensionality, a support cutoff,
static recurrences nor a bivariate classification is assumed.

The full ten-parameter if-and-only-if is now exported as
`all_flat_core_iff_nonaffine`. It joins Theorem K to direct coefficient
elimination on the older seven-parameter stratum and proves the affine
converse using the extra persistent partner `P`. Theorem R's sharp stopping
depths and full exceptional-locus classification remain outside Lean.

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

## Original-coordinate classification

For ten arbitrary coefficients, `hamiltonian t` is

\[
H_{\rm chart}=P^3+(b_0+b_1q+b_2q^2+b_3q^3)P+
 c_0+c_1q+c_2q^2+c_3q^3+c_4q^4+c_5q^5.
\]

`shear 1` substitutes `P=p+q²`. `flatContraction k` is the unnormalized
alternating sum of mixed Mathlib partial derivatives with binomial
coefficients. `AllFlatPersistent H f` requires every odd contraction of order
at least three to vanish on every iterate of the actual bracket `D_H`.

The final statement is:

```lean
all_flat_newton_persistent_core (t : HamiltonianParameters K)
    (hnew : t.b₃ ≠ 0 ∨ t.c₄ ≠ 0 ∨ t.c₅ ≠ 0) (f : Poly K) :
  AllFlatPersistent (shear 1 (hamiltonian t)) f ↔
    ∃ a b : K, f = C a + C b * shear 1 (hamiltonian t)
```

The proof closes dependencies 4 and 5 and the three-case portion of dependency
6 in the Priority 3 plan:

| Module | Proved contribution |
|---|---|
| `CubeLeadingStatic` | Actual third/fifth differential operators and coefficient recurrences at every pair of nonnegative indices. |
| `CubeLeadingCutoff` | Off `E=0`, every static polynomial has momentum degree at most six; a common `(1,3)` weight bound 20 gives finite-dimensionality through an injective finite coefficient map. |
| `CubeLeadingSquare` | In each Newton case, no static polynomial has leading form `a*h²`, for any nonzero scalar and arbitrary lower-weight corrections. |
| `CubeLeadingDimension` | Momentum degree bounds force the leading exponent to be at most two; square exclusion and cancellation of successive leading forms give equality with `span{1,H}`. |
| `CubeLeadingHamiltonian` | The ten-parameter Hamiltonian, its bracket and staticity; on `b3=c5=0, b2≠0`, simultaneous staticity of `f` and `D_H f` forces momentum degree at most six. This covers the `E=0` part of case III. |
| `CubeLeadingClassification` | The three-case equality for every stable static subspace containing `1,H`; finite-dimensionality and the cutoff are conclusions of preceding proofs. |
| `CubeLeadingPersistent` | The persistent core is constructed as an intersection of pulled-back static submodules, proved stable, and identified with `span{1,H}`. |
| `CubeLeadingTransport` | The nonlinear shear and inverse, both chain rules, bracket transport, and exact universal third/fifth flat-gate identities. |
| `CubeLeadingFlatCore` | Original-coordinate persistent-core equality; total degree at most six forces all higher flat contractions to vanish, yielding the all-odd-gate theorem. |

The cutoff proof avoids a static basis. If the highest momentum exponent is
`m≥7`, the fifth recurrence bounds the q-degrees of its top four coefficient
polynomials. Third-gate coefficients then force `3*b3+10*c5=0` and the
nonresonance identity, hence `b3=c5=0`. The remaining top equations force
`b1+c3=2*b2+4*c4=0`, exactly `E=0`. On the relevant part of `E=0`, staticity
of `D_H f` forces the forbidden top coefficient to vanish because `b2≠0`.

The finite-dimensionality proof uses a convenient weight bound 20, **not**
the conventional theorem's sharp bound 12 or its exact dimensions 14/15.
Those stronger static-dimension assertions are not claimed formal here.
The final core equality does not require them.

The transport formulas are proved for every polynomial partner, not at sampled
parameter points:

\[
T_3(H_{\rm original},\operatorname{shear}f)
 =\operatorname{shear}(-6\,\mathrm{thirdGate}(f)),\qquad
T_5(H_{\rm original},\operatorname{shear}f)
 =\operatorname{shear}(-120\,\mathrm{fifthGate}(f)).
\]

This explicitly accounts for the nonlinear chart. It does not assume nonlinear
covariance of higher flat contractions.

## Classification verification

`AuditCubeLeadingClassification.lean` audits 34 declarations, including the
final all-odd-gate theorem. The retained axiom lists contain only `propext`,
`Classical.choice`, and `Quot.sound`; no `sorry`, `admit`, new axiom or native
computation oracle is introduced. The six regression assertions cover a
seventh-degree static solution on `E=0` that fails after one Hamiltonian
iterate, the theorem at that exceptional point, an extra persistent partner
on the excluded all-affine family, its independence from `1,H`, and the
normalization/sign of the third original-coordinate gate.

```sh
lake build +SexticC3.CubeLeadingFlatCore:olean
lake env lean AuditCubeLeadingClassification.lean > AuditCubeLeadingClassification.actual.txt
diff -u AuditCubeLeadingClassification.output.txt AuditCubeLeadingClassification.actual.txt
lake env lean TestCubeLeadingClassification.lean
```

The CI workflow retains the earlier audits and adds these commands. The
independent PerfectJet point replay still has its documented shared-basis and
row-label dependencies; the Lean proof of Theorem K does not use either.

## Still outside this theorem

- Theorem R's sharp refinement depths and temporary exceptional varieties
  still use their exact symbolic rank certificates outside Lean.
- No independent specialist review is asserted.

## The full ten-parameter criterion

For the Hamiltonian above, the single exported theorem is:

```lean
all_flat_core_iff_nonaffine (t : HamiltonianParameters K) :
  (∀ f : Poly K, AllFlatPersistent (shear 1 (hamiltonian t)) f ↔
    ∃ a b : K, f = C a+C b*shear 1 (hamiltonian t)) ↔ NonAffine t
```

Here `NonAffine t` says that at least one of `b2,b3,c2,c3,c4,c5` is nonzero,
exactly the condition that B and C are not both affine. The field is arbitrary
of characteristic zero. No classification, degree bound, normal form,
finite-dimensionality, matrix rank, or external certificate checker is a
hypothesis.

The older stratum is proved directly in the unnormalized coefficients:

1. If `b3=c4=c5=0` and `b2,c3,c2` are not all zero, staticity of `f` and
   `D_H f` forces momentum degree at most six. This includes the infinite
   static sector `b2=0, b1+c3=0`. The proof uses the actual highest coefficient
   and fifth-gate equations, not a finite search window.
2. The universal third recurrence determines such a static polynomial from
   its first three q coefficients at each momentum degree. After subtracting
   its constant and Hamiltonian components, it is exactly a combination of
   13 explicitly checked static polynomials. Every basis element and the
   reconstruction theorem are Lean proofs.
3. Forty exact coefficient rows from actual Hamiltonian iterates give three
   triangular eliminations. Each pivot is a nonzero rational times a power
   of the branch's nonzero parameter. The cubic-C branch uses two final rows
   in the combination `27*A+4*B`, avoiding any auxiliary parameter exclusion.

| Branch | Raw rows | Greatest iterate used | Nonzero pivot parameter |
|---|---:|---:|---|
| `b2 ≠ 0` | 13 | 2 | `b2` |
| `b2=0, c3 ≠ 0` | 14 | 2 | `c3` |
| `b2=c3=0, c2 ≠ 0` | 13 | 3 | `c2` |

`generate_cube_leading_seven.py` constructs the basis, evaluates the actual
polynomial bracket and static operators, and emits the coefficient and
elimination identities. Lean derives every row from its own differential
recurrences and verifies every elimination identity using field arithmetic.
The generator is reproducible but is not part of the trusted proof chain.
The scalar evaluation table is proved equal to the polynomial coefficient
map, so its use introduces no independent coefficient-array assumption.

When B and C are affine, the actual bracket sends P to `b1*P+c1`.
Consequently `span{1,P}` is a static invariant space and P is persistent.
Coefficient comparison proves P is outside `span{1,H}`. The shear transports
this witness to `p+q²` in the original coordinates. This proves the necessity
of the non-affine condition as well as its sufficiency.

`AuditCubeLeadingFullCriterion.lean` adds 19 audited declarations, including
both chart and original-coordinate iff theorems. Its axiom lists contain only
`propext`, `Classical.choice`, and `Quot.sound`. The new boundary regressions
cover all three non-affine branches, the infinite-static-sector cutoff, the
affine converse, and the quadratic-restoring point where a partner survives
iterates 0, 1 and 2 but fails at iterate 3. These checks do not promote the
full sharp-refinement classification into a formal theorem.

```sh
python generate_cube_leading_seven.py
lake build +SexticC3.CubeLeadingFullCriterion:olean
lake env lean AuditCubeLeadingFullCriterion.lean > AuditCubeLeadingFullCriterion.actual.txt
diff -u AuditCubeLeadingFullCriterion.output.txt AuditCubeLeadingFullCriterion.actual.txt
lake env lean TestCubeLeadingFullCriterion.lean
```
