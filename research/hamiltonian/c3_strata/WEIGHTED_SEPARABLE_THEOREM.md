# All-degree cores under mixed lower-weight perturbations

## Statement

Work over a characteristic-zero field. Let `n>=5`, let `m` be `3` or `4`,
put `d=gcd(n,m)`, and assign the positive weights

\[
 w_x=m/d,\qquad w_y=n/d,\qquad W=nm/d.
\]

Suppose

\[
 H=a x^n+b y^m+R(x,y),\qquad ab\ne0,\qquad \operatorname{wt}R<W.
\tag{1}
\]

The coefficients of every allowed mixed term in `R` are unrestricted.
The coordinates `x,y` may be any independent affine linear coordinates;
translations are absorbed in `R`. The static and refined spaces impose
all odd Moyal contractions, as defined in the
[separable theorem](SEPARABLE_SIXFOLD_THEOREM.md).

**Theorem.**

1. Every member of the complete static space has weighted degree at most
   `B=4w_y+2w_x=(4n+2m)/d`. Consequently every refinement is an exact
   finite-dimensional kernel in a known finite polynomial space.
2. For `m=3`, the first refinement has dimension at most four and
   `S^2=D_infinity=span{1,H}`. Its least stabilization depth is one if
   `dim S^1=2`, and two otherwise.
3. For `m=4`, `S^1=D_infinity=span{1,H}` and the least stabilization
   depth is exactly one.

The static dimension is at most fifteen for `m=3` and at most twelve
for `m=4`; in either case it is at least seven. No genericity condition
is imposed on `R`.

In the sextic cases the theorem takes the particularly small form:

| Leading binomial | Coordinate weights | Allowed perturbation | Complete static envelope | Core |
| --- | --- | --- | --- | --- |
| `a x^6+b y^3` | `(1,2)` | Every monomial has weight `<6` | Weight `<=10` | `S^2=span{1,H}` |
| `a x^6+b y^4` | `(2,3)` | Every monomial has weight `<12` | Weight `<=16` | `S^1=span{1,H}` |

These are full polynomial-space statements. The finite algorithm below
uses the proved envelope to compute the individual static and first
spaces; it does not promote a truncated search to an all-degree claim.

## 1. Weighted leading-component transfer

For a polynomial `F`, write `F^sharp` for its component of greatest
weight. Let `H_0=a x^n+b y^m`, of weight `W`, and let `G` have greatest
weight `v`. The coefficient of weight `W+v-k(w_x+w_y)` in `T_k(H,G)` is

\[
 T_k(H_0,G^\sharp).
\tag{2}
\]

To verify this, apply the definition of the contraction monomial by
monomial. Every term uses a total of `k` derivatives in each coordinate
across its two arguments. Hence it subtracts exactly `k(w_x+w_y)` from
their combined weight. A term involving a lower component of either
argument has strictly smaller weight. Formula (2) remains valid when
its right side is zero; it refers to the component in the *possible*
greatest weight, without assuming that component is nonzero.

The Poisson derivation has possible weight shift `W-w_x-w_y`.
Induction on `i` gives the corresponding top-component identity

\[
 [D_H^iG]_{v+i(W-w_x-w_y)}=D_{H_0}^iG^\sharp.
\]

Combining it with (2), every `G in S^r(H)` satisfies

\[
 G^\sharp\in S^r(H_0).
\tag{3}
\]

This is valid simultaneously for all correction orders and all finite
refinement depths. There is no use of nonlinear coordinate covariance.

If `S^r(H_0)` is finite-dimensional, (3) also implies

\[
 \dim S^r(H)\le\dim S^r(H_0).
\tag{4}
\]

One proof filters both spaces by weight. The map that takes a polynomial
to its highest-weight component induces an injective map on each
associated-graded quotient into the corresponding homogeneous piece of
`S^r(H_0)`. Summing these finite dimensions proves (4). Equivalently,
perform exact elimination on leading coefficients in each weight; it is
not legitimate to count arbitrary leading components of an arbitrary
basis without this elimination step.

## 2. The complete static bound

Apply the explicit static bases in the separable theorem to
`f=a x^n,g=b y^m`. Their antiderivative terms are constant multiples of
`x^(n+k)` for `k=0,1,2`, so every displayed basis element is
weighted-homogeneous.

For `m=3`, the largest weight is attained by

\[
 x^2y^4+\frac{4y I_f(x^2)}b,
\]

and equals `4w_y+2w_x`. For `m=4`, it is attained by

\[
 x^2y^4+\frac{I_f(x^2)}b,
\]

and has the same weight. Thus `S^0(H_0)` has no component above `B`.
Equation (3) shows that no nonzero member of `S^0(H)` can have weight
above `B`, proving the claimed finite envelope. Equation (4) gives the
dimension bounds fifteen and twelve.

All polynomials of ordinary total degree at most two pass every
correction gate for every Hamiltonian. Their six-dimensional space, plus
`H` of degree `n>=5`, gives the lower bound seven for `dim S^0(H)`.

## 3. Core and depth

For the cubic complement the separable theorem gives

\[
 S^1(H_0)=\operatorname{span}\{1,x,x^2,H_0\},\qquad
 S^2(H_0)=\operatorname{span}\{1,H_0\}.
\]

Equations (3)--(4) therefore bound `dim S^1(H)` by four and
`dim S^2(H)` by two. The polynomials `1,H` survive every iterate:
antisymmetry gives every odd `T_k(H,H)=0`, and `D_HH=D_H1=0`.
They are independent. Hence

\[
 S^2(H)=D_\infty(H)=\operatorname{span}\{1,H\}.
\]

If the first space already has dimension two it is this same core;
otherwise it strictly drops at depth two. The static dimension is at
least seven, so depth zero is never sufficient.

For the quartic complement, the separable theorem already gives
`S^1(H_0)=span{1,H_0}`. The same argument proves
`S^1(H)=D_infinity(H)=span{1,H}`, and the static lower bound makes depth
one sharp.

The cubic first refinement can have each dimension allowed by the
bound. Exact examples are

| Hamiltonian | `dim S^0` | `dim S^1` | `dim D_infinity` | Least depth |
| --- | ---: | ---: | ---: | ---: |
| `x^6+y^3+xy` | 15 | 4 | 2 | 2 |
| `x^6+y^3+xy^2` | 15 | 3 | 2 | 2 |
| `x^6+y^3+x^3y` | 15 | 2 | 2 | 1 |
| `x^6+y^4+xy^3` | 10 | 2 | 2 | 1 |
| `x^6+y^4+x^4y+x^2y^2` | 9 | 2 | 2 | 1 |

These per-input spaces and sharpness witnesses are reconstructed by the
independent replay. They illustrate why a classifier should return the
actual first space rather than only the terminal two-dimensional core.

## 4. Recognition and coordinate coverage

Since `w_x<w_y`, (1) has ordinary leading form `a x^n`. A rational input
therefore determines the repeated rational linear factor `L` up to a
nonzero scalar. Recover and check this leading power exactly, and choose
any independent rational linear complement `M`.

Changing complements has the form `M=alpha y+beta x` with `alpha!=0`.
Its inverse replaces `y` by a nonzero multiple of `M` plus a multiple of
`L`. Replacing a weight-`w_y` variable by itself plus a lower-weight
variable cannot increase weight. The term `b y^m` therefore has highest
part `b' M^m`, with all its other terms strictly below `W`, and all terms
of `R` remain strictly below `W`. Rescaling `L` only changes `a`.
Translations likewise add only lower-weight terms. This proves that a
detector using a fixed linear complement recognizes every rational
affine-coordinate image of either cone; no complement search or
nonlinear substitution is needed.

The decoder checks `n>=5`, `m in {3,4}`, both leading coefficients
nonzero, the exact leading binomial, and the strict weight inequality
for every other term. Inputs with another term of weight `W`, a term
above `W`, or a fifth-degree complement are outside this theorem.

## 5. Certificates, implementation, and boundary

`weighted_separable.classify_weighted_separable` accepts the general
rational family; `classify_weighted_separable_sixfold` is its
degree-six wrapper. A report retains the adapted linear coordinates,
weights, leading binomial, lower part, proven static bound, every
refinement basis, the least depth, and a first-failure witness for each
strict inclusion.

The producer first solves all odd static gates on every monomial of
weight at most `B`. It then takes full polynomial preimages using the
matrix `[D B_r | -B_r]`. The outputs of `D` are never truncated to the
input envelope. The supplied-report verifier independently constructs
the gates from the defining star exponential and uses separate rational
elimination. It rejects an incorrect bound, omitted stage, incomplete
static basis, false core, corrupted contraction, or altered depth.

For `n>6`, every potentially nonzero odd gate is included; limiting the
check to `T_3,T_5` would not be sufficient for a general mixed input.
Witnesses retain this complete gate list.

The all-degree result is proved above using the preceding separable
theorem and the weighted leading-component argument. The rational
implementation and its independent replay certify concrete inputs
within that mathematical boundary. These arguments have not been
formalized in Lean. General mixed complements outside the two stated
weight cones remain unclassified by this extension.
