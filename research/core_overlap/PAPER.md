---
title: "Exact Nonlinear Sectors"
subtitle: "Complete affine cubic-phase cores, restoring transitions and deformation torsion"
author: "Nonlinear Hamiltonian research programme"
date: "22 October 2026 - internally reviewed research draft"
fontsize: 10pt
colorlinks: true
linkcolor: NavyBlue
urlcolor: NavyBlue
toc-depth: 1
---

# Exact nonlinear sectors: cubic-phase classification and deformation

Research overlap with `claude/adoring-ritchie-1hq1kw`, incorporating
its cubic-phase work at `35d39be4` and the earlier reviewed integration
at `e6ef82d`, on 22 October 2026.
All results use one canonical pair and the compendium's fixed flat Weyl
convention. Written proofs were reviewed independently inside this research
session; historical priority and external peer review remain open.

## Cubic-phase completion

The continuation through Claude commit `35d39be4` closes the full affine
cubic-phase sector: `P=p+w(q)`, degree w two, `H=a(P)+q*b(P)`.
Theorem CP classifies every such polynomial Hamiltonian, including all
lower-degree boundaries. For degree a at least three, constant b gives
the infinite QC tower; linear b gives exactly the K1-prime spaces of
dimension four, five or six; quadratic b gives exactly K4's three-dimensional
space or `span{1,H}`; and degree b at least three gives `span{1,H}`.
Quadratic b with degree a at most two has a full four-dimensional core.
The full table and exact rational chart recognizer are
`cubic_phase_classification.*`. K1-prime and K4 upper bounds are proved.

The nonlinear restoring theorem is also complete: for EVERY polynomial
F of degree at least three and `lambda!=0`,

`H=F(p+w(q))+lambda*q^2+epsilon*q+C`

has full core `span{1,H}`. Intersections of the third-gate tests through depths one, two and three
have dimensions four, three and two, with explicit all-degree proofs and
sharp witnesses. At zero restoring force the core is instead the infinite
QC tower, sharply at depth one. See `higher_restoring.*`.

The cubic calibration `H_t=(p+q^2)^3+t*q^2` has first-order liftable
initial space `span{1,P,P^3}` and second-order/formal initial space
`span{1,P^3}`. Its delayed P obstruction is `864*t^2`.
The full uniform finite-weight Smith law is in `cubic_deformation.*`;
`restoring_deformation.*` proves the same three-to-two lifting hierarchy
for EVERY polynomial F of degree at least three, with the uniform Smith
law for every declared weight bound N at least twice the degree of F.
The independent review uses its own Fraction engine and imports no
project mathematical producer.

Claude's formal gauge theorem is retained with its parameter convention
explicit. Its vector-field defect is a total derivative and its full
operator defect a coboundary; no nontrivial scalar Gelfand-Fuchs class
is claimed. P003 and P004 remain refuted as stated. General non-affine
cubic-phase Hamiltonians beyond these proved classes remain open.

## The consequential finding

The blanket pure-top part of conjecture P003 is false. The simplest active
counterexample obtained here has degree four:

\[
 Q=p+q^2,\qquad H=Q^2,\qquad
 \mathcal D_\infty(H)=K[Q]+\operatorname{span}_K\{q,qQ,q^2\}.
\]

The failure is structural. With `Q=p+bq^2+cq+d`, `b!=0`, the complete
family `H=P(Q)+epsilon q` has core `K[Q]+Kq` for `deg P>=3`, and the displayed
larger core for `deg P=2`. If `epsilon!=0`, the whole tower `K[Q]` is active.
Consequently a general edge-polynomial finiteness theorem must exclude these
families. A Newton edge alone does not imply a finite core.

A second, different phenomenon has a finite three-dimensional active core:

\[
 J=qp+q^3,\qquad H=qJ^2,
 \qquad\{H,J\}=H,\qquad
 \mathcal D_\infty(H)=\operatorname{span}\{1,H,J\}.
\]

Its extension is a complete classification of all pure total tops with
unequal perfect-power transverse top `alpha p^s(q+gamma)^r`, `r,s>=2`.
For `s>=3` the core is `span{1,H}`. For `s=2`, precisely the explicitly
recognized nonlinear shear family has a third generator.

There is also a complete six-dimensional family. If `Q=p+u(q)`, `deg u>=3`,
and `H=AQ^2+BQ+C+epsilon q`, `A!=0`, the core is exactly
`span{1,q,Q,q^2,qQ,Q^2}`. Third-gate tests at Hamiltonian depths zero, one,
and two suffice, and depth two is necessary. Thus even finite pure cores
need not have dimension two or three.

This six-dimensional sector also connects directly to the compendium's
observer machinery. Its exact derivation matrix has Jordan blocks `3,2,1`
when the forcing vanishes and `5,1` otherwise. The minimal derivative
closures of the targets `q`, `q^2`, and their joint family change from
dimensions `2,3,5` to `3,5,6`. The existing independent observer checker
replays this reduction, and the closed evolution is polynomial in time.

Claude's near-top completion in commit `268d553` is incorporated on the
review branch. The edge theorem and the new pure exceptions have distinct
scopes. Independent review supplied two proof clarifications, without
changing the theorem or its determinant certificates.

## Classification and deformation continuation

The continuation starts from the published review tree at `4050dbf`.

It now classifies **every** polynomial Hamiltonian
`H=A*p^2+B(q)*p+C(q)` with nonzero constant A. Complete the square with
`Q=p+B(q)/(2A)` and `V=C-B(q)^2/(4A)`; the degrees of the shear and
residual potential determine the full core. The complete phase diagram
and unified exact classifier are `constant_quadratic_classification.*`.
The possible answers are the full polynomial ring, the infinite QC
tower, the six-dimensional quadratic sector, and `span{1,H}`.
The sharp third-gate depths reach seven; variable coefficients of p^2
remain outside this completed class.

For `Q=p+u(q)`, `deg u>=3`, and `H=P(Q)+epsilon*q`, `deg P>=3`, the
missing composition case has core exactly `span{1,H}`. The two equations
`C3G=C3DG=0` already determine that core. Together with QC and SS this
completes the main nonlinear shear-composition phase diagram.

Adding a quadratic restoring potential produces exact nonlinear oscillators.
For nonzero `A` and `deg u>=3`, the core
remains the six-dimensional quadratic sector in `(q,Q)`, with sharp
third-gate depth two. For a quadratic shear and `kappa!=0`, the same core
has sharp depth three. At `kappa=0` a quadratic shear instead has the
infinite QC core. Thus a quartic polynomial Hamiltonian exhibits an exact
infinite-to-six transition, and the closed sector can carry oscillatory
rather than merely polynomial-in-time dynamics.

The whole constant-quadratic-momentum higher-shear family is classified:
for `H=A(p+u(q))^2+V(q)`, `deg u=m>=3`, and arbitrary polynomial V,
the core is six-dimensional if `deg V<=2` and is `span{1,H}` otherwise.
The sharp third-gate stopping depths are respectively two, six when
`deg V=3`, and four when `deg V>=4`. A direct leading-transverse-degree
argument removes the initially excluded resonant boundary `deg V=2m`.
For the subfamily `deg V<2m`, the weighted bound remains a useful
independent certificate method: every core observable has `(1,m)` weight
at most `2m`, and exact elimination in `3m+3` ambient monomials computes
the core without any unproved numerical cutoff.

![Theorem QF: exact all-degree dimensions of the spaces passing third-gate depths zero through R. The curves start at R=2, where the proved upper space has dimension six; they are not dimensions extrapolated from a finite input box.](output/figures/Sharp_Depth_Transitions.png)

For analytic `H=q*p^(-1/4)+V(p)` on `p>0`, an additional cubic exists
exactly when `V=c0+a*p^(-1/4)+b*p^(3/4)+c*p^(5/2)`. Its full core is then
`A+qA+R*(H-c0)^3`; otherwise it is the affine strip. The proof solves a
fourth-order Euler compatibility equation, rather than searching a list
of powers. A general regular-chart compatibility system also describes
which potentials preserve a cubic for exceptional `F` with constant `K3`.

For `H_t=(p+q^2)^2+t*q^2/2`, the deformation obstruction hierarchy is
nontrivial in all degrees: at order zero the core is infinite, the space
of initial observables liftable through first order has dimension seven,
and through second order has dimension six. The cubic lifts once but is
obstructed at the next order; every higher power is obstructed already at
first order. The six-dimensional quadratic sector persists to all orders.
The full graded torsion of the declared gate-matrix cokernel is one
`K[t]/(t^2)` summand in degree three and one `K[t]/(t)` summand in every
degree at least four. This is literal module torsion and an explicit
deformation obstruction, not a newly named geometric torsion tensor.

Proofs and checkers are in `shear_composition_complete.*`,
`shear_oscillator.*`, `quadratic_frontier.*`,
`analytic_potential_classification.*`, and `deformation_obstructions.*`.
The independent review is `extension_proof_review.md`. Universal claims
rest on the written proofs; exact finite checks and certificates replay
those claims within their declared hypotheses. Historical priority remains
unestablished.

## Other proved overlaps

For `J=qp+u(q)` with `u'''!=0`, composition has a sharp phase diagram:
`H=P(J)` has the strip of transverse degree at most two when `deg P=1`,
the stationary span of `1,J,J^2` when `deg P=2`, and `span{1,H}` when
`deg P>=3`. The distinction from `Q=p+q^2` is essential.

For analytic coefficients `A=C^omega(I)` and finite degree in `q`, write
`D={H,·}` and `C_k=T_k(H,·)`. For every analytic `F,V`,

\[
\begin{aligned}
\mathcal D_\infty(qF)
 &=\ker C_3\cap\ker(C_3D)\cap\ker C_5,\\
\mathcal D_\infty(qF+V)
 &=\ker C_3\cap\ker C_5\cap\ker(C_3D)\cap\ker(C_3D^2).
\end{aligned}
\]

The bounds are sharp. For every polygamma `F`, and also `F=log Gamma`, an
arbitrary analytic `V` still gives the stronger equality
`D_infinity(qF+V)=ker C3 intersect ker(C3D)=A+qA`. A meromorphic pole or
the logarithmic Gamma singularity rules out every higher sector at once.

Outside that rigid class, the explicit algebraic profile
`F=a p^(-1/4)+b p` has the active cubic
`G=q^3p^(-3/4)`, with `D G=-(15b/4)G`. All iterated third-order tests can
nevertheless miss a fifth-order obstruction in other fractional-power
profiles, so the polynomial branch's third-gate arguments must retain their
coefficient hypotheses.

The nonlinear canonical mechanism is proved by an exact shear formula.
Quantum and classical shear pullbacks agree on transverse degree at most
two. At degree three the correction is `-hbar^2 w''/4`, explaining both
the protected finite core and the failure of unrestricted nonlinear
covariance.

## Proofs and reproduction

The polynomial proofs treat [unequal transverse powers](pure_perfect_power.md),
[parabolic compositions](pure_quadratic_composition.md),
[six-dimensional cores](analytic_shear_square.md), and
[shear compositions](audit_balanced_transverse.md).
The [analytic stopping rules](depth_finite_determination.md) and
[fractional family](analytic_bridge.md) connect to the polygamma work.
The [canonical transport proof](canonical_bridge.md) explains the protected
sector. The [balanced audit](audit_balanced.md) repairs the harmless `s<mu`
setup restriction; no upper bound is needed. The [independent review](review_assessment.md)
records the proof assessments.

Run `python3 -B research/core_overlap/verify_all.py` from the repository
root. All numerical receipts are supplementary to the proofs. The declared
coefficient-box census covers 3,888 exceptional families and 3,888 broken
closure perturbations, with additional exact affine transport checks.
The existing source populations and sealed baseline proofs are untouched. The portable bundle contains this research package and the required extension code; replay of the retained compendium archives requires the full repository.

## What remains open

The complete classification of arbitrary pure perturbations is still
open. The original P003 is disproved, so unresolved pure cases are
reported as unclassified rather than assigned the former conjectural core.
Claude's subsequent commit `268d553` completes the near-top question; its
edge theorem is integrated with two proof clarifications recorded in the
follow-up review. Recognition of the new composition families is sufficient for
their routes; it is not claimed to recognize every possible exception.

\clearpage

# A complete affine cubic-phase classification

Fix the original flat Weyl product, one canonical pair, and a field K of
characteristic zero. Set

\[
 Q=q,\qquad P=p+w(q),\qquad \deg w=2,\quad c=w''/2\ne0,
 \qquad H=h(q,p+w(q)),\quad h=a(P)+Qb(P).                 \tag{CP1}
\]

All cores in this note are full polynomial dynamic cores. The observable
degree is unrestricted. The coordinate substitution expresses the original
operators; it does not silently replace their product by a flat product.
Historical priority and external peer review remain unestablished.

## The classification

Write f=deg a and d=deg b, taking the degree of zero as minus infinity.
Every displayed space is pulled back to the original coordinates.

| Coefficient degrees | Full core | Dimension |
|---|---|---|
| d<=0, f<=1 | K[Q,P] | Infinite |
| d<=0, f=2 | K[P]+span{Q,QP,Q^2} | Infinite |
| d<=0, f>=3 | K[P]+KQ | Infinite |
| d=1, f<=1 | K[Q]+P K[Q]+P^2 K[Q] | Infinite |
| d=1, f=2 | span{1,Q,P,Q^2,QP,P^2} | Six |
| d=1, f>=3 | K1-prime basis below | Four, five or six |
| d=2, f<=2 | span{1,X,XP,H}, X=Q+a2/b2 | Four |
| d=2, f>=3 | span{1,G,H} in K4; otherwise span{1,H} | Three or two |
| d>=3, every a | span{1,H} | Two |

**Theorem CP.** This table exhausts every Hamiltonian (CP1).

For d=1 write b=mu(P-r), mu!=0. When f>=3 the basis is

\[
 1,P,P^2,H;\qquad Q\ \text{if }f=3;\qquad
 (P-r)H\ \text{if }f=3\text{ and }a''(r)=0.              \tag{CP2}
\]

For d=2 and f>=3 the exceptional case occurs exactly when f=4 and

\[
 r=\frac{b_1/b_2-a_3/a_4}{2},\qquad
 b(r)=0,\qquad r'=-b_1/b_2-r.                            \tag{CP3}
\]

Then, with A=a4 and c2=a2-3A r(r+r'), the extra generator is

\[
 G=A(P-r)^3+c_2(P-r)+b_2Q(P-r).                          \tag{CP4}
\]

Thus K4's earlier exact containment is now the entire core. Formula
(CP3) is an exact coefficient test and needs no numerical root matching.

## Proof dependencies and the lower-degree boundaries

For d>=2, `cubic_affine_completeness.md` first proves that every core
element is affine in Q by taking its highest Q coefficient. It then
classifies that affine space directly. Its quadratic-b proof derives
K4's quartic form without bounded symbolic casework. Its low-density
branch supplies the four-dimensional row missing from a theorem that
assumes f>=3.

For d=1,f>=3, `cubic_phase_audit.md` diagonalizes D in polynomial
coordinates P,J after centering the root of b. The highest-Q third
gate limits each D-eigenpolynomial to at most three monomials. Explicit
nonzero leading coefficients rule out every Q degree at least two.
This proves both completeness and the basis (CP2), independently of a
finite-degree search.

The constant-b rows are the retained QC classification. If f<=1 the
original Hamiltonian is quadratic and has no higher odd gates.

For d=1,f=2, completing the square absorbs the QP and P terms into an
affine correction of w. The residual Q^2 coefficient is
-mu^2/(4a2), which is nonzero. The retained SO/CQ theorem therefore gives
the full six-dimensional quadratic sector. Its basis is unchanged by
the required affine changes in Q,P.

For d=1,f<=1 the original Hamiltonian has the form

\[
 H=(\mu q+\alpha)p+\phi(q),\qquad \phi'''=6\mu c\ne0.
                                                               \tag{CP5}
\]

Its sole higher odd gate is 6mu c partial_p^3. Its derivation preserves
polynomials of p degree at most two. Thus the full core is exactly the
three-strip in the table; shifting p to P preserves that degree bound.
This boundary explains why affine-Q containment must retain its degree
hypotheses: arbitrary powers of Q survive in this lower-degree row.

## Recovering the chart without losing an affine family

The exact rational recognizer is `cubic_phase_classification.py`.
It also accepts h directly through `classify_in_chart(h,c)`; that API
classifies every affine-Q input, including all lower-degree boundaries.
A recognizer miss never asserts collapse.

There is a practical ambiguity worth resolving. Write the original
polynomial as sum_j p^j H_j(q), and s=deg_p H>=1. If a quadratic shear
makes it affine in Q, then

\[
 H_s=a_s+q b_s,\qquad
 H_{s-1}=s w(q)H_s+a_{s-1}+q b_{s-1}.                    \tag{CP6}
\]

Hence deg H_s<=1. If H_s is linear, polynomial division of H_(s-1)
by s H_s recovers the quadratic and linear coefficients of w; its
constant is immaterial and is set to zero. If H_s is constant, the
linear term in w is mixed with q b_(s-1). Automatically absorbing that
term into a completed power can destroy the affine-Q description.

Instead recover the quadratic coefficient c from (CP6), put
h0(Q,P)=H(Q,P-cQ^2), and solve for the remaining rational slope alpha:

\[
 (\partial_Q-\alpha\partial_P)^2 h_0=0.                 \tag{CP7}
\]

For every monomial, (CP7) is a polynomial equation in alpha of degree
at most two. The common polynomial gcd therefore determines the
possible slopes exactly. Its rational roots are checked by exact
substitution. Taking w=cq^2+alpha q reconstructs h affine in Q, and
the recognizer verifies H=h(q,p+w(q)) identically.

For total degree h0>=3 there is at most one slope even over an
algebraic closure: two independent directions with zero second
directional derivative would make h0 at most bilinear in independent
coordinates, hence of total degree at most two. Therefore an existing
slope is rational for rational input (a sole root of a rational
polynomial of degree at most two is rational). The low-degree case
uses every rational root and exact reconstruction; the existing CQ
classifier covers quadratic charts requiring an algebraic slope.

The checker includes the formerly ambiguous family
h=P^m+2QP^(m-1)+1, m=3,...,6, with shifted shears. This is a regression
for chart recognition, not evidence replacing the classification proof.

## Relation to the non-affine sector and torsion

The affine-Q classification does not exhaust arbitrary h(Q,P).
`higher_restoring.md` independently closes the non-affine family
F(P)+lambda Q^2+epsilon Q+C for every deg F>=3 and lambda!=0, with
sharp third-gate depth three. `cubic_deformation.md` identifies the
all-degree lifting obstruction and every stated finite-weight Smith
torsion presentation at the cubic boundary.

The vector-field compatibility defect in Claude's formula is a total
derivative; the full derivation defect is a coboundary. Neither is
claimed here as a new nontrivial scalar Gelfand-Fuchs class. Our
parameter-module torsion is specified by its actual source and output
map. These distinctions are part of the results, not open conventions.

\clearpage

# Completing cubic-phase cores with nonlinear affine coefficient

Use one canonical pair, the original flat Weyl product, the bracket
`{H,G}=H_q G_p-H_p G_q`, and a characteristic-zero field K. Set
`P=p+w(q)`, `Q=q`, with `deg w=2` and `c=w''/2 !=0`.
The substitution is used to express the original operators, not to
assert invariance of the flat product under nonlinear coordinate changes.
Write `H=tilde h`, where `h=a(P)+Q b(P)`, and let `D={H,.}`.
All observables below are polynomials of arbitrary degree.
Historical priority and external peer review remain unestablished.

## The all-degree containment theorem

**Theorem AC.** Suppose `m=deg b>=2`, with no degree restriction on a.
Every element of the full dynamic core is affine in Q:

`D_infinity(H) subset tau*(K[P]+Q K[P])`.

In fact the third gate alone, through depths zero and one when m>=3,
and through depths zero, one and two when m=2, excludes every observable
whose Q degree is at least two. This is a bound on Q degree, not a claim
that those depths already identify the full core.

### The exact operators

In `(Q,P)` coordinates the original derivation is

`D=b partial_P-(a'+Q b') partial_Q`.

Expanding the third coefficient in the triangular transvectant formula gives

`C3 = 6c[b' partial_P^3+b'' partial_P^2
 -(a''+Q b'') partial_Q partial_P^2
 -(a'''+Q b''') partial_Q partial_P]
 +3b'' partial_Q^2 partial_P-(a'''+Q b''') partial_Q^3`.

Both operators preserve the increasing filtration by Q degree. If
`G=Q^N f(P)+lower Q powers`, its top Q coefficients under D and C3 are
respectively `L_N f` and `6c M_N f`, where

`L_N=b partial_P-N b'`,

`M_N=b' partial_P^3+(1-N)b'' partial_P^2-N b''' partial_P`.

Consequently the coefficient of Q^N in `C3 D^r G` is exactly
`6c M_N L_N^r f`. Lower Q components of G cannot cancel it.
This absence of cancellation is the essential all-degree step.

### Leading-degree obstruction

Let the leading coefficient of b be B, and let f have degree n with
nonzero leading coefficient F. For n>0 the potential leading coefficient
of `M_N f`, at P degree `n+m-4`, is

`B F m n (n+m-3)(n-1-N(m-1))`.                 (AC1)

Indeed the bracket before factoring is
`(n-1)(n-2)+(1-N)(m-1)(n-1)-N(m-1)(m-2)`, which equals
`(n+m-3)(n-1-N(m-1))`.
The factorization is a polynomial identity, not a sampled assertion.

Suppose N>=2. If m>=3, the equation `M_N f=0` allows only
`n=0` or `n=1+N(m-1)`. In the first case `L_N f` has degree m-1
and nonzero leading coefficient `-N m B F`. That degree is neither
allowed degree for a kernel element of M_N. In the second case
`L_N f` has degree `n+m-1`, with leading coefficient
`B F(n-Nm)=B F(1-N) !=0`, again neither allowed degree.
Thus `M_N f=M_N L_N f=0` is impossible.

If m=2, the allowed degrees are `n=0,1,N+1`, since (AC1) becomes
`2 B F n(n-1)(n-1-N)`. Degree one is sent by L_N to degree two,
with nonzero coefficient `B F(1-2N)`; degree N+1 is sent to
N+2 with nonzero coefficient `B F(1-N)`. Both new degrees are
forbidden. Degree zero is sent first to degree one and then to degree
two, with nonzero leading coefficients. Thus
`M_N f=M_N L_N f=M_N L_N^2 f=0` is impossible.
This proves Theorem AC in every polynomial degree.

## Full classification when deg b>=3

**Theorem AC-high.** If deg b>=3, for every polynomial a,

`D_infinity(H)=span{1,H}`.

By AC it suffices to write `g=alpha+Q beta`. The top-Q third-gate
equation for N=1 and the same leading-factor argument imply
`beta=lambda b+nu`: subtract the leading multiple of b, which itself
solves `M_1 b=0`, and no nonconstant lower degree is permitted.
Subtract lambda h. The remaining observable is `alpha+nu Q`.
Its static third-gate equation is `(b' alpha'')'=0`; since b' is
nonconstant, alpha is linear. Write the remainder as `sP+t+nu Q`.
The Q coefficient of its bracket is `-nu b'`. For that bracket also
to be a core element this coefficient must be a multiple of b plus a
constant; degree comparison forces nu=0. Finally `D(sP+t)=s b`,
and `(b'b'')'` is nonzero for deg b>=3, so its third gate forces s=0.
Conversely 1 and H are always stationary core elements.

## Full classification when b is quadratic

Write `b=mu P^2+b1 P+b0`, `mu!=0`.

**Theorem AC-quadratic.** For every polynomial a, exactly one of the
following cases occurs.

* If `deg a<=2` (including the zero polynomial), put
  `lambda=a2/mu`, `X=Q+lambda`, and
  `a-lambda b=lP+k`. The full core is
  `span{1,X,XP,H}`, of dimension four.
* If `deg a=4`, set
  `A=a4`, `r=(b1/mu-a3/A)/2`, `r'=-b1/mu-r`.
  If `b(r)=0`, put `c2=a2-3A r(r+r')` and
  `G=A(P-r)^3+c2(P-r)+mu Q(P-r)`.
  The full core is `span{1,G,H}`, of dimension three.
* In every other case the full core is `span{1,H}`.

The middle case is exactly K4. Its recognition needs no algebraic-root
search: r is fixed by the rational coefficient formula, and `b(r)=0`
is one exact identity test. These statements hold over every
characteristic-zero coefficient field, without assuming b splits.

### Proof without bounded symbolic casework

Theorem AC bounds all core elements to `g=alpha+Q beta`. Its static
third-gate equation has Q coefficient `b' beta'''`, so beta has degree
at most two. Its remaining third-gate equation is

`(b' alpha''-beta' a'')'=0`.                    (AC2)

The projection of the core onto beta is an `ad_b`-invariant subspace
`B subset span{1,P,P^2}`, and contains b. Its kernel is exactly the
constant observables: beta=0 in (AC2) forces alpha linear, while the
third gate of `D(alpha)=alpha' b` forces its slope to vanish.

First suppose deg a>=3. The projection B cannot be all of sl2.
Otherwise a core element with beta=1 exists. Equation (AC2) makes its
density alpha linear. Applying (AC2) to its first bracket gives

`b'(alpha1 b''-a''')+b'' a'' in K`.            (AC3)

Center P at the root of b'. In the polynomial equation (AC3), the
coefficient multiplying the linear term of a'' cancels, whereas any
degree at least two in a'' survives. Therefore (AC3) forces
`deg a<=3` and `alpha1=0`. In the remaining cubic case the observable
is Q modulo a constant. For `D^2 Q`, the expression on the left of
(AC2) before its outer derivative is exactly `-(b')^2 a'''`.
Its derivative is nonzero, a contradiction. Thus dim B<=2.

If dim B=1, the kernel statement gives exactly span{1,H}. If dim B=2,
subtract a multiple of h from an independent observable to make its
beta linear. It cannot be constant: its adjoint bracket with b would
then produce the independent nonconstant linear polynomial b'.
Scale it to `beta=mu(P-r)` for some r in K. Adjoint invariance forces
`b(r)=0`: explicitly, adding mu b to `b beta'-b' beta` leaves
`mu[(b1+2mu r)P+2b0+b1 r]`, which is a multiple of beta precisely
when b(r)=0. Let `r'=-b1/mu-r`, `x=P-r`, and `delta=r'-r`.
The bracket closure, modulo the constant kernel, is then

`Dg=-mu H-mu delta g+constant`.                (AC4)

Its density equation, differentiated once and divided by the common
polynomial factor x, gives

`a''=2alpha'+(x-delta)alpha''`.

Together with (AC2) this becomes `x alpha''-2alpha' in K`.
For a polynomial alpha, the coefficient of x^(j-1) in that expression
is `j(j-3)alpha_j`. Consequently
`alpha=A x^3+C x+D`; integrating the displayed formula for a'' gives

`a=A x^3(x-delta)+C x^2+c1 x+c0`.

Since deg a>=3, A is nonzero. This is precisely K4 and in particular
forces deg a=4. No finite-degree computation is used to exclude any
other degree. Matching the cubic coefficients fixes r by the formula
in the theorem, and matching degree two gives C=c2.

For sufficiency, beta and b are quadratic-or-lower. The K4 density
satisfies `b'alpha''-beta'a''=-2mu c2`, a constant. Under
`S_s=exp(s partial_P^3)`, h changes only by a linear polynomial in P
and g only by a constant. Therefore the third-derivative compatibility
defect stays zero for every s, proving every odd gate vanishes by the
cubic-phase gauge identity. Equation (AC4) proves closure. Independence
of 1,G,H follows from their independent Q coefficients beta,b.

Finally suppose deg a<=2. Shift to X as in the theorem, so the density
is lP+k. Static exactness forces beta quadratic-or-lower and alpha
linear in these coordinates. The next third-gate condition is the
single linear restriction

`mu alpha1=l beta2`.

It leaves exactly the four-dimensional space `span{1,X,XP,H}`.
It is invariant, with

`DX=-2mu XP-b1 X-l`,

`D(XP)=-H+k+b1 XP+2b0 X`, and `DH=0`.

All higher gates kill X because it is linear. They kill XP because
its original-coordinate degree is at most three and its third gate
vanishes; H has only its own trivial odd antisymmetric gates. This
proves sufficiency and completes the classification.

## Uniform finite stopping rules

The full classification above can be decided by the third gate at finite
Hamiltonian depth, with no input-degree bound:

`D_infinity(H)=intersection_(r=0)^R ker(C3 D^r)`,

where `R=1` for deg b>=3 and `R=2` for deg b=2.

For deg b>=3, AC already forces an element of the depth-one kernel to
be affine in Q. The static affine kernel is exactly
`span{1,H,P,Q}` by the proof of AC-high. The first bracket test removes
Q from its Q coefficient and then removes P from its density. Thus R=1.
It is sharp for every such Hamiltonian: P itself passes the static gate,
but `C3 DP=6c(b'b'')' !=0`.

For quadratic b, write S_r for the intersection of the third-gate kernels
through depth r restricted to V. The static space S_0 has dimension five.
Indeed beta is any quadratic polynomial, and if rho is the root of b',
then

`alpha''=(beta'a''-beta'(rho)a''(rho))/b'`,

with alpha_0 and alpha_1 arbitrary. The numerator is divisible by b'.
The kernel of the beta projection on S_1 consists only of constants,
because `C3 D(P)=6c(b'')^2 !=0`.

When deg a>=3, dim S_1 is at most three. Otherwise its beta projection
would be all of sl2. A beta=1 element of S_1 forces deg a<=3 and zero
slope of alpha, as in (AC3). For cubic a, a beta=P element of S_1 has
static density with leading term `3a3 P^2/(2mu)`. In its first bracket
the possible cubic density term cancels. Its third gate nevertheless
has leading term `144c mu a3 P`, which is nonzero. Thus that beta cannot
occur in S_1, a contradiction. Since S_1 has dimension at most three
and contains the two independent stationary elements 1,H, either
S_2=S_1 and the space is already invariant under D, or S_2 has dimension
two and equals span{1,H}. Equality at one stage in the descending chain
implies invariance and stabilization. Hence S_2 is the maximal
C3-killed invariant space, which the classification above proves is
the full core. When deg a<=2, the explicit four-dimensional space is
already S_1 and is invariant.

Finally AC forces every whole-polynomial depth-two candidate to be in
V, so the restricted argument proves the asserted full stopping rule.
The uniform bound two cannot be reduced: for `a=0`, `b=P^2`, the
observable `G=Q^2+2P/c` passes C3 and C3D but fails C3D^2; the latter
has Q^2 coefficient `-288c`. No sharpness claim is made separately for
every quadratic-b parameter value.

## Exact checks and scope

`cubic_affine_completeness.py` verifies the polynomial factor identity,
the transformed operators against original-coordinate mixed derivatives,
the highest-Q extraction, the obstruction degrees, exact K4 recognition,
and the four-dimensional low-density branch with original-coordinate
gates and brackets. It also rejects forged theorem-application data.
The all-degree conclusions rest on the written arguments above; finite
checks are independent calibration, not a completeness inference.
The linear-b branch is treated separately in `cubic_phase_audit.md`.

\clearpage

# Complete linear coupling in the cubic phase, and an obstruction audit

All statements use the original flat Weyl transvectants in one canonical
pair `(q,p)`, over a field K of characteristic zero. Write
`Q=q`, `P=p+w(q)`, where w is quadratic and `c=w''/2 != 0`.
The substitution is used to express the original operators, not to replace
their product by the flat product in `(Q,P)`.

## The complete linear-coupling theorem

**Theorem CPL.** Let

\[
 h(Q,P)=a(P)+Q\mu(P-r),\qquad \mu\ne0,\quad \deg a=f\ge3,
 \qquad H=h(q,p+w(q)).                                      \tag{CPL1}
\]

Every polynomial element of `D_infinity(H)` is affine in Q. Its full core,
with every displayed expression pulled back to `(q,p)`, has basis

\[
 1,\ P,\ P^2,\ h;
 \qquad Q\quad\text{if }f=3;
 \qquad (P-r)h\quad\text{if }f=3\text{ and }a''(r)=0.          \tag{CPL2}
\]

Thus its dimension is four when f is at least four, five for a cubic a
with `a''(r)!=0`, and six for a cubic a with `a''(r)=0`.
The value of `a(r)` does not affect the condition: adding a constant to
the Hamiltonian does not alter its derivation or its gates.

This closes the full-core upper-bound question in Claude's K1-prime
family. It does not rely on the restricted affine-observable theorem:
both the absence of higher Q powers and the remaining affine basis are
proved below independently. Higher gates introduce no further restriction
on the basis (CPL2).

### The exact third gate

For a general affine Hamiltonian `h=a(P)+Qb(P)`, the original third gate
rewritten in `(Q,P)` is

\[
\begin{aligned}
 C_3g={}&-(a'''+Qb''')g_{QQQ}+3b''g_{QQP}\\
 &+6c\bigl[b'g_{PPP}+b''g_{PP}
 -(a''+Qb'')g_{QPP}-(a'''+Qb''')g_{QP}\bigr].
\end{aligned}\tag{CPL3}
\]

This follows by taking the coefficient of `t^3/3!` in the exact triangular
generating formula: `C3=Omega^3+6c Omega K`, with
`K=partial_P1 partial_P2^2+partial_P1^2 partial_P2`.
The checker also verifies (CPL3) directly with mixed derivatives in the
original coordinates, using an arithmetic engine independent of the
triangular producer.

### Diagonalizing the Hamiltonian derivation

Translate P by r, divide h by mu, and subtract the constant term. These
operations do not change its core. It is enough to treat

\[
 h=PJ,\qquad J=Q+A(P),\qquad A(P)=a(P)/P,
 \qquad m=\deg A=f-1\ge2.                                  \tag{CPL4}
\]

Here a has zero constant after the harmless subtraction, so A is a
polynomial. The coordinate change `(Q,P) <-> (P,J)` is a polynomial
bijection. A direct bracket calculation gives

\[
 DP=P,\qquad DJ=-J,\qquad
 D=P\partial_P-J\partial_J.                                \tag{CPL5}
\]

Consequently `P^u J^v` is an eigenvector of D of eigenvalue `u-v`.
Every polynomial is a finite sum of such eigenvectors. Because the core
is D-invariant, each of the distinct-eigenvalue components of any core
element is again in the core: the finite spectral projections are
polynomials in D, using the distinct integer eigenvalues and
characteristic zero. This argument has no input-degree cutoff.

### Excluding every Q degree at least two

Let g be a nonzero D-eigenpolynomial in the core, of J degree n. Its
highest-J term is `lambda P^d J^n` for some integer d at least zero and
nonzero lambda. J and Q differ only by a polynomial in P, so they define
the same highest transverse degree. The highest-Q part of (CPL3), for
`b=P`, is `6c partial_P^3`. Thus d is at most two. Rescale lambda to one.
The eigenvalue condition then forces

\[
 g=\sum_{j=0}^{\min(d,n)}\lambda_j P^{d-j}J^{n-j},
 \qquad \lambda_0=1,\quad d\in\{0,1,2\}.                  \tag{CPL6}
\]

In `(P,J)` the exact normally ordered third gate is

\[
\begin{aligned}
 C_3={}&6c\partial_P^3
 +6c(A'-PA'')\partial_P^2\partial_J
 -6cA'(A'+2PA'')\partial_P\partial_J^2\\
 &-\bigl[6c(A')^2(A'+PA'')+3A''+PA'''\bigr]\partial_J^3
 -6cPA'''\partial_P\partial_J\\
 &-6c\bigl[2A'A''+P(A'')^2+PA'A'''\bigr]\partial_J^2
 +6cA'''\partial_J .
\end{aligned}\tag{CPL7}
\]

Coefficients are placed to the left of the derivatives. Let
`A=alpha P^m+lower`, where `alpha!=0` and `m>=2`.

If n is at least three, the term of highest P degree in `C3g` is

\[
 -6c\,m^4\alpha^3 n(n-1)(n-2)
       P^{d+3m-3}J^{n-3}.                                 \tag{CPL8}
\]

It comes only from the first term of (CPL6) and the leading
`-6c(A')^2(A'+PA'') partial_J^3` term. Every other term in (CPL7) has
smaller P degree; the lower terms in (CPL6) also lower that degree.
Its coefficient is nonzero, contradicting `C3g=0`.

If n equals two, the term of highest P degree in `C3g` instead is

\[
 -12c\,m^2(2m-1)(d+m-1)\alpha^2P^{d+2m-3}.                 \tag{CPL9}
\]

It is obtained by combining the two `partial_J^2` terms in (CPL7).
Again the lower terms of (CPL6) cannot reach this P degree, and the
displayed coefficient is nonzero because `m>=2,d>=0`. This excludes
n two as well. Therefore every D-eigencomponent of a core element,
and hence every core element itself, is affine in Q.

### Determining and certifying the remaining basis

For n zero, (CPL3) permits precisely `1,P,P^2`. For n one, (CPL6)
leaves only J, PJ and `P^2J`, modulo these already protected polynomials.
Their third gates are

\[
 C_3J=6cA''',\qquad C_3(PJ)=0,\qquad
 C_3(P^2J)=12c(A'-PA'')-6cP^2A'''.                         \tag{CPL10}
\]

For m at least three the last expression has nonzero leading coefficient
`-6c m(m-2)(m+1)alpha`, and `A'''` is nonzero. For m two,
`A=alpha P^2+a_2P+a_1`: J passes and the last expression is `12c a_2`.
Since J differs from Q by a combination of `1,P,P^2`, this gives exactly
(CPL2), with `a_2=a''(r)/(2mu)` before normalization.

Each listed span is D-invariant. Every odd gate kills `1,P,P^2` by
the triangular generating formula, h by antisymmetry, and Q because it
is linear in the original coordinates. For the exceptional `Ph`,
the third gate is `6c mu a''(r)` in the root-centered coordinates, hence
zero in the stated case. All odd gates of order at least five vanish:
both functions are affine in Q, so only the `Omega K^k` term can
contribute to order `2k+1`; for k at least two, its P derivatives
annihilate the linear coefficient b or the quadratic Q coefficient of
Ph. This proves sufficiency in every degree and completes Theorem CPL.

### A uniform finite stopping certificate

The diagonal derivation supplies a finite stopping bound as well. Split
the operator (CPL7) into its D-weight shifts: a normally ordered term
`P^i J^j partial_P^u partial_J^v` has shift `s=i-j-u+v`.
Let S be the finite set of shifts actually present after combining
coefficients. Then

\[
 \mathcal D_\infty(H)
 =\bigcap_{r=0}^{|S|-1}\ker(C_3D^r).                        \tag{CPL12}
\]

Indeed, fix an output monomial of weight omega. Its coefficient in
`C3 D^r g` is the sum, over s in S, of `(omega-s)^r` times the
contribution from the input weight `omega-s`. The first `|S|` equations
have a Vandermonde matrix with distinct nodes `omega-s`; hence each
contribution vanishes separately. Thus every D-eigencomponent of g is
killed by C3. The proof above classifies exactly these eigencomponents,
and all of them pass every gate. This argument retains every output
coefficient, with no projection and no input-degree cutoff.

For `m=deg A`, the displayed operator gives
`S subset {-3,-1} union {1,...,3m}` and therefore the uniform upper bound
`R<=3m+1`. The checker returns the smaller actual `|S|-1` bound. In the
six-dimensional normalized cubic branch
`a=alpha P^3+a1 P+a0`, `S={-3,3,6}`, so depths zero, one and two
already suffice in all polynomial degrees. Sharpness of these general
bounds is not asserted.

## A naming and normalization audit

Claude's gauge identity is algebraically correct in the formal generating
parameter t. Physical Moyal conventions often use `t=i hbar/2`, so a
coefficient written in t must be converted before being described as a
physical hbar coefficient. No numerical prefactor independent of the
chosen convention is asserted here.

The displayed vector-field defect satisfies the exact identity

\[
 b'\beta'''-b'''\beta'=(b'\beta''-b''\beta')'.              \tag{CPL11}
\]

Its integral over a periodic domain, or with compact support and no
boundary contribution, is therefore zero. It must not be identified
without further structure with the usual nontrivial scalar
Virasoro/Gelfand--Fuchs central-extension cocycle. The full defect
`Delta(X,Y)=partial^3[X,Y]-[partial^3X,Y]-[X,partial^3Y]` is, by its
definition, the derivation defect (a Chevalley--Eilenberg coboundary up
to sign) of the linear operator `partial_P^3` in the adjoint module.
It is a useful exact compatibility condition. A nontrivial cohomology
class would require a separately specified coefficient module and a
separate proof. None is claimed by this note.

For comparison, the conventional scalar Gelfand-Fuchs central-extension
formula is `(1/12) integral b''' beta`, as given by Ovsienko and Roger,
[arXiv:math/9812074](https://arxiv.org/abs/math/9812074), equation (9.2).
Integration by parts gives
`integral(b' beta''-b'' beta')=2 integral b''' beta` under the same
boundary conditions. Our displayed defect is the derivative of that
integrand, so its scalar integral vanishes rather than producing that
nontrivial central extension.

\clearpage

# Quadratic shears with every nonlinear composition and a restoring potential

This note closes a non-affine part of the cubic-phase sector in all
polynomial degrees. The coefficient field has characteristic zero. The
original flat Weyl product is fixed throughout; a nonlinear canonical
substitution does not replace that product by a new flat product.
Historical priority is unestablished.

## The complete restoring theorem

Let

\[
 P=p+w(q),\qquad w(q)=c q^2+dq+e,\qquad c\ne0,
 \qquad H=F(P)+\lambda q^2+\epsilon q+C,
 \qquad \deg F\ge3,\quad\lambda\ne0.
 \tag{HR1}
\]

Write \(D=\{H,\cdot\}\), with the convention
\(\{f,g\}=f_qg_p-f_pg_q\), and let \(C_3=T_3(H,\cdot)\) be the
third unnormalized odd transvectant in the original \((q,p)\)
coordinates. For \(r\ge0\), put

\[
 S_r=\bigcap_{j=0}^r\ker(C_3D^j).
 \tag{HR2}
\]

**Theorem HR.** In the full polynomial ring, without an input-degree
cutoff,

\[
 \begin{aligned}
 S_1&=\operatorname{span}\{1,q,P,H\},\\
 S_2&=\operatorname{span}\{1,P,H\},\\
 S_3&=\operatorname{span}\{1,H\}
       =\mathcal D_\infty(H).
 \end{aligned}
 \tag{HR3}
\]

Thus the third gate at Hamiltonian depths zero through three already
determines the entire dynamic core. Depth three is necessary. In
particular, for every integer \(m\ge3\),

\[
 H=(p+q^2)^m+\lambda q^2,\quad\lambda\ne0
 \quad\Longrightarrow\quad
 \mathcal D_\infty(H)=\operatorname{span}\{1,H\}.
 \tag{HR4}
\]

For \(\lambda=0\), the retained QC theorem instead gives the infinite
core \(K[P]+Kq\), sharply at third-gate depth one. Thus the nonlinear
composition undergoes an infinite-to-two transition and a depth-one to
depth-three transition when the restoring coefficient leaves zero.
For \(\deg F=2\), the retained SO/CQ theorem gives
the six-dimensional quadratic sector when the restoring coefficient is
nonzero. These are different proved branches; Theorem HR assumes both
\(\deg F\ge3\) and \(\lambda\ne0\).

## Exact original-coordinate operators

Expressing the original derivation and gate in the polynomial
coordinates \((q,P)\) gives

\[
 \begin{aligned}
 D&=-F'(P)\partial_q+(2\lambda q+\epsilon)\partial_P,\\
 C_3&=-F'''(P)\partial_q^3
       -6cF''(P)\partial_q\partial_P^2
       -6cF'''(P)\partial_q\partial_P.
 \end{aligned}
 \tag{HR5}
\]

The affine and constant terms of \(w\) do not enter the third gate.
The term \(\lambda q^2+\epsilon q+C\) has no original-coordinate
third derivatives and adds nothing to \(C_3\). Formula (HR5) follows
by the original mixed-derivative formula, or by retaining the
coefficient of degree three in the triangular generating formula. It
does not assert covariance of the flat Weyl product under the shear.

## Why two tests already give a four-dimensional upper space

Take \(G\in S_1\) and write
\(G=\sum_{j=0}^Nq^j g_j(P)\), with \(g_N\ne0\).
Assume first that \(N\ge3\). In \(C_3G=0\), the coefficients of
\(q^{N-1}\) and \(q^{N-2}\) are respectively nonzero scalar
multiples of

\[
 (F''g_N')'=0,\qquad (F''g_{N-1}')'=0.
 \tag{HR6}
\]

Since \(F''\) is nonconstant, a polynomial \(g_j\) can satisfy
\(F''g_j'\in K\) only when \(g_j'=0\). Hence
\(g_N\) and \(g_{N-1}\) are constants. The coefficient of
\(q^{N-3}\) then gives

\[
 6c(N-2)(F''g_{N-2}')'
       =-N(N-1)(N-2)g_NF'''.
 \tag{HR7}
\]

After integration,
\(F''[6c g_{N-2}'+N(N-1)g_N]\) is constant. Its second factor is
a polynomial; because \(F''\) is nonconstant, that constant must be
zero. Therefore

\[
 g_{N-2}'=-\frac{N(N-1)}{6c}g_N\in K.
 \tag{HR8}
\]

There are no terms of \(q\)-degree \(N+1\) or \(N\) in \(DG\).
Its coefficient of \(q^{N-1}\) is

\[
 A(P)=-NF'g_N+2\lambda g_{N-2}'.
 \tag{HR9}
\]

The highest possible coefficient of \(C_3DG\), at \(q^{N-2}\),
is consequently

\[
 -6c(N-1)(F''A')'
     =12cN(N-1)g_NF''F'''\ne0.
 \tag{HR10}
\]

All factors are nonzero in characteristic zero and \(\deg F\ge3\).
Lower coefficients of \(DG\) cannot contribute at that \(q\)-degree,
and the \(\partial_q^3\) term lowers the highest degree by three.
This contradicts \(C_3DG=0\), proving \(N\le2\).

The same top-coefficient argument in \(C_3G=0\) now makes both
positive-\(q\)-degree coefficients constant. Thus

\[
 G=g(P)+a q+bq^2.
 \tag{HR11}
\]

Substitution in (HR5) gives the exact identity

\[
 C_3DG
   =12c\bigl(F''[bF''-\lambda g'']\bigr)'.
 \tag{HR12}
\]

Again the product of nonconstant \(F''\) with a polynomial cannot
be a nonzero constant. Hence
\(g''=(b/\lambda)F''\), and
\(g=(b/\lambda)F+uP+v\). Equation (HR11) is therefore in
\(\operatorname{span}\{1,q,P,H\}\), after absorbing the linear and
constant terms of the restoring potential. Each of these four
generators passes \(C_3\) and \(C_3D\), proving the first equality
in (HR3).

## The two final eliminations and sharp depth

Put

\[
 R(P)=(F''F''')'.
 \tag{HR13}
\]

If \(F(P)=a_mP^m+\cdots\), \(m\ge3\), the leading coefficient
of \(R\) is
\(a_m^2m^2(m-1)^2(m-2)(2m-5)\), at degree \(2m-6\).
Thus \(R\ne0\). Direct calculation gives

\[
 \begin{aligned}
 C_3D^2q&=12c\lambda R, & C_3D^2P&=0,\\
 C_3D^3P&=24c\lambda^2R.&&
 \end{aligned}
 \tag{HR14}
\]

The first line removes \(q\) from \(S_1\); the second removes
\(P\) at the next depth. Constants and \(H\) survive every odd
gate and every depth because \(D1=DH=0\) and odd transvectants are
antisymmetric. This proves the full core equality. The observable
\(P\) passes depths zero, one and two but fails depth three, proving
sharpness.

At \(\lambda=0\), the same highest-\(q\) argument still gives (HR11),
and (HR12) then forces \(b=0\). Consequently
\(S_1=K[P]+Kq\). This space is invariant under
\(D=-F'\partial_q+\epsilon\partial_P\). All its higher odd gates
vanish: on two functions of \(P\), the quadratic-shear generating
formula contains only even powers of its parameter, and \(q\) is
linear in the original coordinates. The observable \(q^2\) passes
\(C_3\) but has
\(C_3D(q^2)=24cF''F'''\ne0\), proving the stated depth-one
sharpness in the zero-restoring branch as well.

## Exact checker and recognition

`higher_restoring.py` recognizes the family directly in rational
original-coordinate coefficients, computes the full original mixed
derivatives independently of (HR5), and checks (HR10), (HR12), and
(HR14). Finite full-output kernel calculations replay the dimensions
four, three and two in boxes containing the proved bases; those boxes
supplement the all-degree argument above. Invalid exponents, floating
inputs, zero restoring coefficient, nonquadratic shear and quadratic
composition are rejected rather than silently classified.

The recognizer normalizes the constant part of the shear to zero and
absorbs it into \(F\). Recognition failure means outside this theorem.
No general classification of arbitrary non-affine cubic-phase
Hamiltonians or variable restoring potentials is asserted.

\clearpage

# Universal restoring-force deformation obstructions

This note generalizes the cubic lifting theorem to every polynomial
composition of degree at least three. Work over a characteristic-zero
field `K`, in the original flat Weyl convention. Let

\[
 P=p+cq^2+dq+e,\qquad c\ne0,\qquad
 H_t=F(P)+tq^2,\qquad \deg F=m\ge3.                         \tag{RD1}
\]

Here `t` is a formal restoring parameter. Corrections in
`G(t)=sum_(j>=0)t^jG_j(q,P)` may have arbitrary finite polynomial
degree at every order; no common degree bound is imposed.

## The universal lifting theorem

Put `B=F''`, `A=F'''=B'`, and `R=(BA)'`. In the polynomial coordinate
ring `K[q,P]`, the exact original-coordinate derivation and third gate are

\[
 \begin{aligned}
 D_t&=-F'(P)\partial_q+2tq\partial_P=D_0+tD_1,\\
 C&=-A\partial_q^3-6cB\partial_q\partial_P^2
                         -6cA\partial_q\partial_P.
 \end{aligned}                                                   \tag{RD2}
\]

The affine terms `d,e` of the shear cancel from the gate. The quadratic
perturbation contributes no gate at any odd order at least three.
Higher odd gates for a general `F` need not vanish; their inclusion in
the full exact-core definition remains necessary unless a proved
stopping theorem applies. Theorem HR proves that, for a nonzero scalar
restoring force, third-gate depths zero through three already determine
the core. The formal lifting proof below uses those equations for
necessity and explicit full-gate lifts for sufficiency; it does not
infer a formal stopping theorem solely from scalar specializations.

**Theorem RD.** The initial exact core is

\[
 \mathcal D_\infty(H_0)=K[P]+Kq.
\]

Within this initial core, the first-order liftable initial values are
exactly

\[
 J_1=\operatorname{span}_K\{1,P,F(P)\}.
\]

The second-order and fully formal liftable initial values are exactly

\[
 \boxed{J_2=J_\infty=\operatorname{span}_K\{1,F(P)\}.}        \tag{RD3}
\]

These statements concern the complete dynamic-core definition, all
odd gates at all Hamiltonian depths. The initially active direction
`q` is obstructed at first order, while the stationary direction `P`
has a choice-independent delayed second-order obstruction. The initial
Hamiltonian has the exact lift `H_t`.

### A polynomial lemma controlling arbitrary corrections

Suppose `CX=0` and `CD_0X` is independent of `q`. Then

\[
 X=a q^2+\beta q+g(P),\qquad a,\beta\in K,
 \qquad CD_0X=12ca(B^2)'.                                   \tag{RD4}
\]

The exact commutator is

\[
 [C,D_0]=12cB(A+B\partial_P)\partial_q^2.                    \tag{RD4a}
\]

Its scalar polynomial operator is injective: if
`B(A+B partial_P)g=B(Bg)'=0`, then `Bg` is constant, which for
nonconstant `B` and polynomial `g` implies `g=0`. Since `CX=0`,
equation (RD4a) and the hypothesis `CD_0X in K[P]` force every
positive-`q`-degree coefficient of `partial_q^2X` to vanish. Thus
`X` has `q` degree at most two. Writing
`X=q^2a(P)+qb(P)+g(P)`, the two coefficients of `CX=0`
give `(Ba')'=0` and `(Bb')'=0`, making `a,b` constants. Direct
substitution proves the last equality in (RD4).

For comparison with the highest-degree lifting method, if `X` had
`q` degree `N>=3`, `CX=0` would make its leading coefficient
`g_N` constant, and the highest coefficient of `CD_0X` would be

\[
 12cN(N-1)g_NBA\ne0.                                      \tag{RD5}
\]

The commutator argument proves the same obstruction without a
degree bound or a highest-term assumption on the correction.

The same lemma with `CD_0X=0` proves
`ker C intersect ker(CD_0)=K[P]+Kq`: the factor `(B^2)'=2BA` is
nonzero, so `a=0`. Conversely the tower `K[P]` is exact by the
retained quadratic-shear star-commutativity identity

\[
 P\star f(P)=Pf(P)-\frac{c\hbar^2}{4}f''(P)
                 =f(P)\star P.
\]

Star powers are triangular in ordinary powers, so the star algebra
generated by `P` is `K[hbar][P]` and all odd gates between `F(P)` and
`f(P)` vanish separately. The generator `q` is linear and its first
bracket `D_0q=-F'` lies in that tower. This proves the initial core
statement without any degree cutoff.

### First-order compatibility

Write `G_0=f(P)+alpha q`. The static first-order equation gives
`CG_1=0`, and the first derivative gate gives

\[
 CD_0G_1=-CD_1G_0=12c(Bf'')'.                              \tag{RD6}
\]

The right side is independent of `q`. Apply (RD4):
`G_1=a q^2+beta q+g(P)`. The scalar equation is

\[
 (Bf'')'=a(B^2)',\qquad
 B(f''-aB)=\text{constant}.
\]

Because `B` is a nonconstant polynomial and `f''-aB` is polynomial,
the constant must be zero. Thus

\[
 f=aF+bP+d_0.                                               \tag{RD7}
\]

Every `G_1` of the displayed form has `CD_0^2G_1=0`, since `D_0^2`
removes the `q` dependence. The first variation of `CD_t^2f(P)` is
also zero: `D_0D_1f=-2F'f'` has no `q` dependence and `D_1D_0f=0`.
But direct calculation gives

\[
 CD_t^2q=12ctR.                                            \tag{RD8}
\]

This forces `alpha=0`. The polynomial `R` cannot vanish: if
`F=a_mP^m+...`, its leading term at degree `2m-6` has coefficient

\[
 a_m^2m^2(m-1)^2(m-2)(2m-5)\ne0.                           \tag{RD9}
\]

This proves the first-order necessity statement for every polynomial
correction, including corrections of arbitrarily high `P` or `q`
degree.

### Sufficiency and the second-order obstruction

The initial values `1` and `F(P)` have exact lifts `1` and `H_t`.
For `P` itself,

\[
 D_tP=2tq,\qquad D_t^2P=-2tF',\qquad
 D_t^3P=-4t^2qB.                                          \tag{RD10}
\]

The first two derivatives are multiples of a linear observable or
of an exact tower element. Every subsequent derivative has order at
least two in `t`. Thus `P` is a first-order exact jet for all gates
and all depths. This proves first-order sufficiency in (RD3).

Now suppose `P+tG_1+t^2G_2` is a second-order exact jet. The
first-order equations force `G_1=beta q+g(P)`, since `P` has zero
first-order residual. At second order the static and first-depth
conditions are

\[
 CG_2=0,\qquad CD_0G_2=12c(Bg'')'.
\]

Again (RD4) applies, giving

\[
 G_2=a q^2+\gamma q+u(P),\qquad g=aF+d_1P+e_1.              \tag{RD11}
\]

At depth two the order-two equation forces `beta=0` by (RD8).
At depth three, `D_0^3G_2=0`. The first variation of `CD_t^3G_1`
also vanishes: on any `g(P)` the only possible term is
`CD_0^2D_1g`, and `D_0^2(qg')=0`; on `q` the surviving intermediate
term is independent of `q` and is killed by `C`. Consequently no
choice in (RD11), or in the first lift, can cancel

\[
 \boxed{CD_t^3P=24ct^2R\ne0.}                              \tag{RD12}
\]

This is a coupled polynomial incompatibility: the lower-depth
equations first restrict every possible second correction, then the
third-depth residual cannot be removed. For general `F`, it must not
be replaced by the cubic case's constant-coefficient functional,
because `R` is generally nonconstant. Subtracting a multiple of the
exact lift `H_t` and a constant proves second-order necessity for
every initial value in (RD7). The explicit lifts of `1,F(P)` prove
second-order and full formal sufficiency. No convergence assertion or
uniform bound on correction degrees is required.

## Universal finite-presentation torsion law

For every integer `N>=2m`, let

\[
 V_N=\operatorname{span}_K\{q^aP^b:a+2b\le N\}.
\]

Use the declared `K[t]`-linear observation presentation

\[
 M_N(t):K[t]\otimes V_N\longrightarrow Y_N,\qquad
 G\longmapsto (CG,CD_tG,CD_t^2G,CD_t^3G),                    \tag{RD13}
\]

where `Y_N` retains the union of every polynomial output monomial of
the indicated source basis. Outputs are not projected back into
`V_N`. Put `s_N=dim V_N`, `r_N=dim Y_N`, and `d_N=floor(N/2)`.

**Corollary RT.** For every `F,c` in (RD1) and every `N>=2deg F`,

\[
 \boxed{\operatorname{Tor}_{K[t]}\operatorname{coker}M_N(t)
    \cong K[t]/(t^2)\oplus
                  \big(K[t]/(t)\big)^{d_N-1}.}             \tag{RD14}
\]

There are two zero source columns, `s_N-2-d_N` unit Smith factors,
`d_N-1` factors `t`, and one factor `t^2`. The free cokernel rank is
`r_N-s_N+2`.

**Proof.** For every nonzero scalar parameter, Theorem HR gives
`ker M_N(t)=span{1,H_t}`, also over an algebraic closure. These two
generators lie in the source because `N>=2m`. At zero the initial
kernel has dimension `d_N+2`, by (RD3). Thus the generic rank is
`s_N-2` and the rank at zero is `s_N-d_N-2`. Over the PID `K[t]`,
any nonunit Smith factor has roots only at zero: a root elsewhere,
after extension to an algebraic closure, would cause a further rank
drop. There are consequently exactly `d_N` nonunit factors, all
powers of `t`, and two zero columns.

In Smith coordinates, a zero column contributes a freely liftable
initial value. A factor `t^e` contributes a nonzero initial value to
the first-order jet space exactly when `e>=2`, and to the second-order
jet space exactly when `e>=3`. Theorem RD gives dimensions three and
two for these spaces. Its necessity proof used only the third gate
through depth three, so these upper bounds apply to the four-output
presentation (RD13) as well as to the full dynamic-core definition.
These same dimensions hold within `V_N`: global necessity applies
to its corrections, while the explicit lifts
`1,P,H_t` already lie in `V_N`. Hence exactly one exponent is at
least two and none is at least three. This proves (RD14).

The finite-source restriction is explicit, but the formula is proved
for every bound above the stated threshold. It is not an extrapolation
from finite matrices. The module is ordinary algebraic torsion for
the specified C3-only depth-three presentation. Invertible polynomial
source and target changes preserve its Smith factors. Its free part
depends on the declared target, and no invariance under arbitrary
nonlinear changes of the flat Moyal product is claimed.

## Verification and comparison

Run `python3 -B research/core_overlap/restoring_deformation.py`.
The standard-library checker verifies all coefficients in the
compatibility and residual identities for mixed polynomial profiles
of degrees three through six, with positive and negative rational
quadratic shear coefficients. Original-coordinate transvectants
independently check affine and constant shear terms. The checker also
constructs exact C3-only Smith certificates for monomial profiles of
degrees three and four, replays both polynomial inverses, and rejects
an edited observation matrix. Finite fixtures supplement the proofs
of (RD3) and (RD14).

The cubic theorem is the specialization `F=P^3,c=1`, where `R=36`
and (RD8), (RD12) become `432t`, `864t^2`. The earlier quadratic
composition `P^2+tq^2/2` instead retained a six-dimensional exact
sector, with seven first-order liftable initials. For every degree
at least three, this universal theorem reduces those dimensions to
three and two while preserving one delayed second-order factor.
The quantum shear correcting ordinary nonlinear pullback is the
same established operator `exp(-c hbar^2 partial_P^3/12)` for every
`F`. Beyond the cubic case its effect on the Hamiltonian need not
be central; this argument retains the original gates and does not
discard that correction.

\clearpage

# Formal lifting and torsion at the cubic restoring-force boundary

Work over a characteristic-zero field `K` and retain the original flat
Weyl convention. Set

\[
 P=p+q^2,\qquad H_t=P^3+tq^2.
\]

The parameter `t` is formal. A lift has the form
`G(t)=sum_(j>=0)t^jG_j(q,P)`, with every `G_j` an arbitrary polynomial.
No common degree bound on the corrections is assumed. Exactness through
order `s` means every odd Moyal gate on every Hamiltonian iterate
vanishes modulo `t^(s+1)`. Thus a first-order jet passes the complete
dynamic-core definition to first order, not merely a chosen finite
matrix of tests.

The note proves a complete lifting theorem in all degrees and a torsion
law for every sufficiently large finite weight presentation. It uses
ordinary cokernel obstruction classes and Smith modules; neither a new
geometric torsion tensor nor historical priority is claimed.

## Exact operators and the initial core

In the polynomial coordinate ring `K[q,P]`, chain rule gives

\[
 \begin{aligned}
 D_t&=-3P^2\partial_q+2tq\partial_P=D_0+tD_1,\\
 C&=C_3=-6\partial_q^3
       -36P\partial_q\partial_P^2-36\partial_q\partial_P,\\
 C_5&=-360\partial_q\partial_P^4.
 \end{aligned}                                                   \tag{CD1}
\]

All odd gates above fifth order vanish because `H_t` has degree six in
the original affine variables. The quadratic perturbation contributes
no gate. These formulas analyze the original gates; they do not replace
the original flat Moyal product by a flat product in `(q,P)`.

The useful commutator identity is

\[
 [C,D_0]=432P(1+P\partial_P)\partial_q^2.                       \tag{CD2}
\]

Indeed, put `B=P partial_P^2+partial_P`. Then
`C=-6 partial_q^3-36B partial_q`, while
`[B,P^2]=4P(1+P partial_P)`. The polynomial operator
`P(1+P partial_P)` is injective, since it maps `P^n` to
`(n+1)P^(n+1)`.

Consequently `CG=CD_0G=0` forces `G_qq=0`. Write
`G=q b(P)+f(P)`. The remaining static equation is
`-36(Pb''+b')=0`, so `b` is constant. Conversely `f(P)` is stationary
under `D_0`, all gates kill it, and `D_0q=-3P^2` is such a stationary
observable. This gives the all-degree identity

\[
 \boxed{\mathcal D_\infty(H_0)=\ker C\cap\ker(CD_0)
                 =K[P]+Kq.}                                  \tag{CD3}
\]

## Complete classification of liftable initial observables

**Theorem CD.** Within the initial core (CD3), the initial values that
admit first-order exact jets are precisely

\[
 J_1=\operatorname{span}_K\{1,P,P^3\}.
\]

The initial values admitting second-order exact jets, and those
admitting full formal exact lifts, are precisely

\[
 \boxed{J_2=J_\infty=\operatorname{span}_K\{1,P^3\}.}          \tag{CD4}
\]

Thus first-order liftability has dimension three, while second-order
and formal liftability have dimension two. The initially active
observable `q` fails at first order. The stationary observable `P`
passes first order but has a choice-independent second-order
obstruction. The initial Hamiltonian `P^3` has the exact lift `H_t`.

### Necessity at first order

Let `G_0=f(P)+alpha q` and suppose `G_0+tG_1` is a first-order exact
jet. The static equation gives `CG_1=0`. The first derivative gate is

\[
 CD_0G_1=-CD_1G_0=72(Pf'''+f'').                              \tag{CD5}
\]

Apply (CD2), using `CG_1=0`. Its right side is independent of `q`.
Injectivity of `P(1+P partial_P)` implies `partial_q^2G_1` is
independent of `q`, so `G_1` has `q` degree at most two. Write
`G_1=q^2a(P)+qb(P)+g(P)`. The coefficients of `q` and of the constant
in `CG_1=0` imply separately `(Pa')'=0` and `(Pb')'=0`. Polynomiality
forces `a,b` to be constants. Thus

\[
 G_1=a q^2+\beta q+g(P),\qquad
 Pf'''+f''=12aP.                                             \tag{CD6}
\]

Integrating `(Pf'')'=12aP` gives `Pf''=6aP^2+c`. The possible `c/P`
term in `f''` is excluded by polynomiality. Therefore

\[
 f(P)=aP^3+bP+c_0.
\]

To remove the remaining initial direction `alpha q`, use the second
derivative gate. For every polynomial `X`,

\[
 CD_0^rX\in P^{2r-1}K[q,P]\quad(r\ge1).                      \tag{CD7}
\]

This follows from `D_0^r=(-3)^rP^(2r) partial_q^r` and (CD1): the two
`P` derivatives in `C` are accompanied by a factor of `P`, and the
one-derivative term removes at most one power. In particular constant
coefficient extraction annihilates `CD_0^2X` for every polynomial
correction `X`. But direct differentiation gives

\[
 CD_t^2q=432t.                                               \tag{CD8}
\]

The first variation of `CD_t^2 f(P)` is zero: its only nonzero
intermediate expression is `D_0D_1f=-6P^2f'`, which has no `q`
dependence. Hence constant coefficient extraction at this depth gives
the obstruction `432 alpha`. Thus `alpha=0`. This necessity argument
allows every polynomial degree in `G_1`.

### First-order sufficiency and the delayed obstruction

Constants and `P^3` have exact lifts `1` and `H_t`. For the remaining
direction `P`,

\[
 D_tP=2tq,\qquad D_t^2P=-6tP^2,\qquad
 D_t^3P=-24t^2qP.                                          \tag{CD9}
\]

The first three iterates pass both gates modulo `t^2`; every subsequent
iterate has order at least two in `t`. Thus `P` itself is a valid
first-order lift for the full dynamic-core definition. However,

\[
 \boxed{CD_t^3P=864t^2.}                                    \tag{CD10}
\]

The factor is `864`, with the conventions (CD1); it follows from
`C(qP)=-36`. For comparison, the simpler first-order failure is
`CD_t(P^2)=-144t`.

Every first correction to `P` differs from zero by an element of
`ker L_0=K[P]+Kq`, where `L_0` includes all retained gates and depths.
For any such difference `Z`, the first variation of `CD_t^3Z` is zero.
For `Z=f(P)` the only potentially nonzero term is `CD_0^2D_1f`, and
`D_0^2(qf')=0`. For `Z=q`, the only surviving intermediate term is a
multiple of `P^3`, again killed by `C`. Hence the order-two constant
residual in (CD10) is independent of the choice of first lift.

Finally (CD7) with `r=3` shows that `CD_0^3G_2` is divisible by `P^5`
for any polynomial second correction, so it cannot cancel the
constant `864`. This proves that `P` cannot lift through second order.
Subtracting a multiple of the exact lift `H_t` and a constant proves
the necessity of (CD4) for every initial element of `J_1`. Its
sufficiency follows from the explicit constant/Hamiltonian lifts.
No convergence or uniformly bounded degree of a formal series has
been used.

## A parameter-torsion law for every finite weight presentation

Let

\[
 V_N=\operatorname{span}_K\{q^aP^c:a+2c\le N\},\qquad N\ge6.
\]

For the following presentation only, restrict the source to
`K[t] tensor V_N` and retain the complete polynomial outputs of

\[
 M_N(t)G=(CD_t^rG,C_5D_t^rG)_{r=0}^3.                        \tag{CD11}
\]

Choose the target basis as the union of all monomials appearing in
these eight polynomial outputs of the declared source basis. No
output is projected back into `V_N`. Let `s_N=dim V_N` and let `m_N`
be the target dimension. Their values are
`s_(2d)=(d+1)^2`, `s_(2d+1)=(d+1)(d+2)`; `m_N` is determined by the
declared full output population.

**Corollary CT.** For every `N>=6`, put `d=floor(N/2)`. The nonzero
Smith factors of `M_N(t)` consist of `s_N-2-d` units, `d-1` copies
of `t`, and one copy of `t^2`. There are two zero source columns.
Equivalently,

\[
 \boxed{\operatorname{Tor}_{K[t]}\operatorname{coker}M_N(t)
    \cong K[t]/(t^2)\oplus\big(K[t]/(t)\big)^{d-1}.}         \tag{CD12}
\]

The free cokernel rank is `m_N-s_N+2`. This is a theorem for every
declared weight bound `N>=6`, not a claim extrapolated from computed
matrices and not a diagonalization of an undeclared infinite matrix.

**Proof.** The cubic restoring-force theorem gives
`ker M_N(t)=span{1,H_t}` for every nonzero scalar `t`, also after
extension to an algebraic closure; its sharp stopping rule uses both
gates through depth three. The two polynomials belong to the source
for every `N>=6`. At `t=0`, (CD3) gives a kernel of dimension `d+2`.
Consequently the generic rank is `s_N-2`, and the rank at zero is
`s_N-d-2`. No nonunit Smith factor can have a root away from zero,
since it would force a rank drop there. Therefore exactly `d`
nonunit factors are powers of `t`; all remaining nonzero factors
are units. There are two zero factors from the generic kernel.

The first-order and second-order lifting theorem determines those
exponents. In Smith coordinates, each zero factor contributes one
freely liftable initial value; a factor `t^e` contributes a nonzero
initial value through first order exactly when `e>=2`, and through
second order exactly when `e>=3`. The first-order initial space has
dimension three, so exactly one exponent is at least two. The
second-order initial space has dimension two, so none is at least
three. Thus the exponents are `1,...,1,2` as asserted.

This application of Theorem CD to the finite source is legitimate in
both directions. Global necessity allows all corrections, and hence
also corrections in `V_N`; the first-order lifts `P`, `1`, and
`H_t=P^3+tq^2` lie in `V_N`, as do the exact second-order lifts.
Smith source/target changes are invertible over `K[t]`, so they do
not change the dimensions of these spaces of liftable initial values.

The module torsion is ordinary algebraic torsion for the specified
eight-output presentation. Invertible source and target changes
preserve it. Its free part depends on the target population; no
canonical invariance under undeclared gate presentations or nonlinear
changes of the flat product is asserted.

## Verification and relation to the quadratic boundary

There is an exact quantum-shear explanation of the two gates. Let
`sigma` be classical substitution `p -> p+q^2`, let

\[
 R_\hbar=\exp\!\left(-\frac{\hbar^2}{12}\partial_P^3\right),
\]

and use the quantum canonical shear formula from `canonical_bridge.md`.
The quantum shear `sigma R_hbar` sends the base Hamiltonian
`p^3+tq^2` to `H_t-hbar^2/2`. The discrepancy is central and therefore
does not change the Hamiltonian commutator. In `(q,P)` the full Moyal
derivation is consequently

\[
 R_\hbar\left(D_t+\frac{\hbar^2}{4}\partial_q^3\right)
 R_\hbar^{-1}
 =D_t-\frac{\hbar^2}{24}C+
            \frac{\hbar^4}{1920}C_5.                        \tag{CD13}
\]

This identity can also be proved directly, without invoking a
transformation theorem. For `J=partial_P^3`,

\[
 [J,D_t]=-18(P\partial_q\partial_P^2+\partial_q\partial_P),
 \qquad [J,[J,D_t]]=-54\partial_q\partial_P^4,
 \qquad [J,[J,[J,D_t]]]=0.                                  \tag{CD14}
\]

The truncated Baker--Campbell--Hausdorff expansion gives (CD13),
since `J` commutes with `partial_q^3`. In the earlier quadratic
composition, the base Hamiltonian has no intrinsic third gate and
the corresponding second nested commutator is already zero; only
the transformed third gate remains. Here the fifth gate is the
second nested gauge correction. These gauge formulas are established
quantum canonical machinery applied to this family. The new lifting
statements concern the separate restoring parameter `t`; they do not
assert that an ordinary nonlinear substitution preserves flat Moyal
exactness on every observable.

Run `python3 -B research/core_overlap/cubic_deformation.py`. The
checker uses exact rational polynomial arithmetic, computes all
outputs, constructs Smith certificates in weights six, eight, and
ten, and replays the matrices and both polynomial inverses. A complete
weight-six certificate is retained in the receipt, together with a
forgery-rejection check. Separate sparse original-coordinate
transvectants verify 512 gate/iterate identities. These finite checks
and 405 exact BCH-commutator calibrations check the written universal
identities.

The earlier family `P^2+tq^2/2` had a seven-dimensional first-order
initial space and a six-dimensional formally liftable space. Here the
cubic composition reduces those dimensions to three and two. In both
families one stationary initial direction has a delayed second-order
obstruction, reflected by a `t^2` factor; the remaining lost tower
directions have first-order factors. The cubic also destroys the
initial active direction `q` at first order. This is a concrete
comparison of exact-sector deformation mechanisms, rather than a new
name for the Moyal bracket defect.

\clearpage

# The cubic restoring boundary: a complete all-degree classification

Work over a field K of characteristic zero, with the fixed flat Weyl
structure in the original coordinates (q,p). Put

\[
P=p+q^2,\qquad H_\lambda=P^3+\lambda q^2,
\qquad D_\lambda=\{H_\lambda,\cdot\}.
\]

The dynamic core consists of polynomial observables killed by every odd
gate of order at least three after every Hamiltonian derivative. All
coordinate rewritings below refer to those original gates. They do not
replace the flat product by a new flat product in (q,P).

**Theorem CR.** If lambda is nonzero, the full polynomial dynamic core is

\[
\mathcal D_\infty(H_\lambda)=\operatorname{span}_K\{1,H_\lambda\}.
\]

The third gate alone at depths zero through three determines this space,
and depth three is necessary. At lambda zero the full core is
K[P]+Kq, and depths zero and one suffice sharply. There is no bound on
the input degree in either statement.

This note gives a cubic-specific independent derivation of the general
restoring theorem in `higher_restoring.md`. Its direct mixed-derivative
checker imports no producer arithmetic or transformed-gate implementation.
The deformation-lifting hierarchy at this boundary is treated separately
in the continuation's lifting notes. Historical priority is unestablished.

## Exact original-coordinate operators

Writing the original operators in the independent polynomial variables
(q,P) gives

\[
 D_\lambda=-3P^2\partial_q+2\lambda q\partial_P,
\]

\[
 C_3=-6\partial_q^3-36P\partial_q\partial_P^2
                 -36\partial_q\partial_P
     =-6\partial_q\bigl(\partial_q^2+6P\partial_P^2+6\partial_P\bigr),
\]

\[
 C_5=-360\partial_q\partial_P^4.
\]

All higher odd gates vanish because H has original total degree six.
For example, direct expansion of the original fifth gate is
720q partial_p^5-360 partial_q partial_p^4. Substituting
partial_q(original)=partial_q+2q partial_P cancels the two
q partial_P^5 terms, giving the displayed C5. The lambda q squared term
has no derivative of order three or higher.

## The all-degree first-depth theorem

Write S_r for the intersection of ker(C3 D_lambda^j), zero through r.
We first prove, without using C5,

\[
S_1=
\begin{cases}
K[P]+Kq,&\lambda=0,\\
\operatorname{span}_K\{1,q,P,H_\lambda\},&\lambda\ne0.
\end{cases}
\]

Let G=sum_(j=0)^N q^j g_j(P) be any polynomial satisfying C3G=C3DG=0,
with g_N nonzero. Suppose N is at least three. The coefficient of
q^(N-1) in C3G is -36N(P g_N')'. It vanishes, so g_N is constant:
integrating gives P g_N'=constant, and polynomiality forces that
constant to vanish. The next coefficient likewise makes g_(N-1)
constant. The coefficient of q^(N-3) then gives

\[
 (P g_{N-2}')'=-\frac{N(N-1)}6g_N,
 \qquad g_{N-2}'=-\frac{N(N-1)}6g_N.
\]

The second equality again follows from polynomiality after integration.
Thus DG has highest possible q power N-1, with coefficient

\[
A(P)=-3N P^2g_N+2\lambda g_{N-2}'.
\]

The coefficient of q^(N-2) in C3DG is therefore

\[
-36(N-1)(P A''+A')=432N(N-1)g_N P,
\]

which is nonzero in characteristic zero. This contradiction proves
N at most two. The coefficient comparison for C3G at N at most two
makes the q and q-squared coefficients constant. Hence

\[
G=g(P)+a q+b q^2.
\]

The remaining first-depth equation is exactly

\[
C_3D_\lambda G=-72\lambda(Pg'')'+864bP=0.
\]

For lambda zero this says b=0, with g arbitrary. For lambda nonzero,
integration and polynomiality give

\[
g''=\frac{6b}{\lambda}P,\qquad
g=\frac b\lambda P^3+cP+d.
\]

Consequently G=d+cP+aq+(b/lambda)H, proving the claimed S1 spaces.
Every equation was a coefficient identity for an arbitrary polynomial,
so this argument has no hidden degree cutoff.

## Two further derivatives close the core, sharply

For lambda nonzero, S1 is the four-dimensional space above. On its
generators,

\[
D1=DH=0,\qquad Dq=-3P^2,\qquad DP=2\lambda q.
\]

The polynomial P squared is not in S1. Thus requiring DG to lie in S1
removes the q coefficient and gives

\[
S_2=\operatorname{span}_K\{1,P,H\}.
\]

Requiring the next derivative to lie in S2 removes P, since DP is a
nonzero multiple of q. Therefore

\[
S_3=\operatorname{span}_K\{1,H\}.
\]

Constants and H are stationary and killed by every odd gate. Thus S3
is precisely the full dynamic core. The exact witnesses

\[
C_3D_\lambda^2q=432\lambda,\qquad
C_3D_\lambda^3P=864\lambda^2,
\]

show that the two eliminations are necessary. P passes all tests through
depth two, so the stopping depth three is sharp.

At lambda zero, S1=K[P]+Kq is already D-invariant and every gate kills
it: functions of P are killed by both displayed gates, and q is linear
in the original coordinates. Thus this is the full core. The witness
q squared lies in S0 and satisfies C3D0(q squared)=864P, proving sharp
depth one at zero.

## A separate finite bound using both gates

There is a useful independent calibration of the all-degree reduction.
The joint static kernel of C3 and C5 is

\[
K[P]+\operatorname{span}_K\{W_1,\ldots,W_8\},
\qquad
W_N=\sum_{j=0}^{\min(3,\lfloor(N-1)/2\rfloor)}
 \frac{(-1)^j(N)_{2j}}{6^j(j!)^2}q^{N-2j}P^j.
\]

Indeed, C5 forces every q-dependent term to have P degree at most
three. Writing that part as sum_(j=0)^3 a_j(q)P^j, C3 gives the chain

\[
a_3'''=0,\quad a_2'''+54a_3'=0,\quad
a_1'''+24a_2'=0,\quad a_0'''+6a_1'=0.
\]

Its q-dependent solutions have weighted degree at most eight for
weights (q,P)=(1,2), and the eight displayed W_N are independent
solutions with their respective highest q powers. If G=g(P)+W also
satisfies C5DG=0 and lambda is nonzero, then
C5Dg=-720 lambda g^(5), whereas C5DW has weighted degree at most two.
Hence deg g at most six, placing every such candidate in the proved
49-dimensional weighted space of degree at most twelve.

The independent exact finite replay in that space has dimensions
15,4,3,2 at depths zero through three using both gates. With C3 alone,
its dimensions are 19,4,3,2. These finite calculations are corroboration
of the all-degree argument, and the separate bound also explains why
the finite calculation can be made conclusive for both gates.

## Reproduction and boundaries

Run `python3 -B -S research/core_overlap/cubic_restoring.py`.
The optional `--output PATH` records a new receipt. The checker compares
588 original mixed-derivative gate calculations with the transformed
formulas, checks the eight static harmonics and commutator, verifies
the sharp witnesses at three nonzero rational parameters, and replays
the finite kernels with every output monomial retained. No floating
point arithmetic, optional symbolic package, or output projection is
used. This result classifies the entire stated family; it does not
classify arbitrary non-affine cubic-phase Hamiltonians.

\clearpage

# Independent review of the cubic-phase completeness and restoring theorems

This review uses the original flat Weyl transvectants in one canonical pair
over a characteristic-zero field. It distinguishes universal written
arguments from finite arithmetic replays. Its checker imports no project
mathematical engine, producer classifier, triangular formula, or gate
implementation. Polynomial multiplication, differentiation, substitution,
mixed-derivative transvectants, and rational rank are implemented separately
with Python's standard-library `Fraction` arithmetic.

Historical priority and external peer review remain open. The review supports
the precise classifications below, not a classification of arbitrary
non-affine cubic-phase Hamiltonians.

## Scope and notation

Put `Q=q`, `P=p+w(q)`, with `w=cq^2+dq+e` and `c!=0`. This substitution
rewrites the original operators. It does not justify replacing the original
flat product by a different flat product in `(Q,P)`. The derivation is
`Dg={H,g}=H_q g_p-H_p g_q`.

The reviewed proof files are `cubic_affine_completeness.md` (AC),
`cubic_phase_audit.md` (CPL), `higher_restoring.md` (HR), and
`cubic_deformation.md` (CD), together with the universal extension
`restoring_deformation.md` (RD/RT). The first two complete the affine-in-Q
Hamiltonians in their stated branches; the low-degree branches are supplied
by the retained CQ/QC and positive-structure theorems. HR closes a separate
non-affine restoring family, and CD measures its formal degeneration.

## Independent operator and leading-coefficient checks

For `h=a(P)+Qb(P)`, direct original-coordinate differentiation gives

`C3g=-(a'''+Qb''')g_QQQ+3b''g_QQP`

`+6c[b'g_PPP+b''g_PP-(a''+Qb'')g_QPP-(a'''+Qb''')g_QP]`.

The checker verifies this formula against direct original-coordinate third
transvectants for thirty rational polynomial instances, including nonunit
and negative shear coefficients and affine terms in the shear.

On the highest transverse term `Q^N f(P)`, the operators are

`L_N=b partial_P-Nb'`,

`M_N=b' partial_P^3+(1-N)b'' partial_P^2-Nb''' partial_P`.

If `deg b=m`, `deg f=n`, and their leading coefficients are B and F,
the coefficient of `P^(n+m-4)` in `M_N f` is

`BF*m*n*(n+m-3)*(n-1-N(m-1))`.

The exponent is `n+m-4`. Vanishing derivative terms are omitted when this
exponent is negative. The factorization follows by direct expansion and is
replayed at 432 integer exponent combinations. For `N>=2`, comparison with
`L_N` excludes every positive N at least two after depths zero and one when
`m>=3`, and after depths zero through two when `m=2`. The permitted degree
sets are respectively `{0,1+N(m-1)}` and `{0,1,N+1}`; `L_N` immediately
leaves them, with one additional step in the constant quadratic-b case.
No lower-Q term can cancel a highest-Q coefficient, since both operators
preserve the Q-degree filtration. This verifies the essential all-degree
containment argument of AC.

For `m>=3`, the remaining affine observable has `beta=lambda*b+nu`.
Subtracting `lambda*h` reduces the density to a linear polynomial. The
Q coefficient after one bracket forces `nu=0`; the next static gate forces
the remaining P slope to vanish. Thus the full core is `span{1,H}` for
every polynomial a, including a of degree at most two.

For quadratic b, AC's proof of K4 necessity is independent of bounded
symbolic enumeration. The projected core is an `ad_b`-invariant subspace
of the three-dimensional quadratic-vector-field space. If its dimension
is two, its second generator can be normalized to `mu(P-r)` and bracket
closure forces `b(r)=0`. In the variable `x=P-r`, the two density equations
reduce to

`a''=2alpha'+(x-delta)alpha''`,

`x alpha''-2alpha' in K`.

The second equation has polynomial solutions
`alpha=A x^3+C x+D`, so the first forces
`a=A x^3(x-delta)+C x^2+c1 x+c0`. This proves K4 exhaustiveness in every
degree. A three-dimensional projection is excluded by the separate beta=1
argument and its second bracket. The low-a quadratic-b branch instead has
the complete four-dimensional core `span{1,X,XP,H}` after the stated
constant Q shift. These exceptional low degrees are necessary and are not
covered by Claude's original `deg a>=3` table.

The stronger finite stopping statement also passes independent review.
Within the affine observable space, the static third-gate kernel has
dimension five. At depth one, the kernel of its beta projection consists
only of constants. For `deg a>=3`, a depth-one space of dimension at least
four would therefore project onto all three quadratic beta coefficients.
Its beta=1 representative forces a to be cubic. A beta=P representative
then has density leading coefficient `3a3/(2b2)` at P squared, but the
third gate of its first bracket has uncancellable leading term
`144c*b2*a3*P`. Thus the depth-one space has dimension at most three and
contains `1,H`. The next descending stage is either equal to it and
invariant, or is the two-dimensional stationary span. Low-degree a has
the explicitly invariant four-dimensional space already at depth one.
Combining this argument with the whole-ring Q-degree bound proves full
stopping at depth two for quadratic b. The witness
`h=QP^2`, `g=Q^2+2P/c` satisfies
`C3g=C3Dg=0` and `C3D^2g=864P-288cQ^2`, so the uniform bound is sharp.
For b of degree at least three, the complete stopping depth is one;
the same proof separately removes the Q and P coefficients at that depth.

## The independent linear-coupling argument

After scaling, translating P, and subtracting a constant, take
`h=PJ`, `J=Q+A(P)`, with `deg A=m>=2`. Its Hamiltonian derivation is

`D=P partial_P-J partial_J`.

Every polynomial is a finite sum of its integer-eigenvalue components.
Since the core is D invariant, finite spectral projections preserve it.
The highest-Q third-gate equation bounds the highest-P exponent d of
each component to `d<=2`. An eigencomponent of J degree n consequently has
only the terms `P^(d-j)J^(n-j)`, `0<=j<=min(d,n)`.

Independent chain-rule expansion gives the dominant `partial_J^3`
coefficient

`-6c(A')^2(A'+P A'')-(3A''+P A''')`.

For `A=alpha P^m+lower` and `n>=3`, the uniquely highest P-degree
contribution is

`-6c*m^4*alpha^3*n*(n-1)*(n-2) P^(d+3m-3)J^(n-3)`.

For `n=2`, combining the two `partial_J^2` terms gives instead

`-12c*m^2*(2m-1)*(d+m-1)*alpha^2 P^(d+2m-3)`.

The lower eigencomponent terms have strictly smaller P degree. Both
coefficients are nonzero in the stated range, which excludes every n at
least two. The independent checker replays 75 versions of these two leading
coefficients with lower terms in A retained. It separately checks every
relevant odd gate and full-output D closure on twelve protected linear-b
spans. This confirms the four-, five-, and six-dimensional full-core cases
of CPL.

The subsequent finite stopping extension is valid as well. If S is the
finite set of D-weight shifts of the normally ordered C3 operator, an
output coefficient of weight omega in `C3D^rG` has the form
`sum_(s in S)(omega-s)^r c_s`. The nodes `omega-s` are distinct in
characteristic zero. Inverting the Vandermonde matrix for
`r=0,...,|S|-1` forces each contribution to vanish, and hence forces
every input D-eigencomponent to pass C3 separately. CPL already
classifies exactly these components and proves that its listed basis
passes every odd gate. Thus `R=|S|-1` is a uniform all-degree stopping
bound for each declared Hamiltonian. Inspection of the exact operator
gives `S subset {-3,-1} union {1,...,3m}`, so `R<=3m+1`.
In the normalized six-dimensional cubic branch,
`A=alpha P^2+constant`, the support is exactly `{-3,3,6}` and R is two.
These are upper bounds; general sharpness is not asserted. Independent
replay verifies four shift supports and reconstructs twelve output
coordinates by exact Lagrange/Vandermonde projection.

## Unified chart recovery and lower-degree boundaries

The unified rational recognizer in `cubic_phase_classification.py` has
also been reviewed separately. If the highest-p coefficient is linear
in q, division of the next coefficient by its scaled predecessor can
change the recovered shear only by a constant. Its quadratic and linear
terms are therefore exact. If that leading coefficient is constant,
the quadratic shear term is still fixed, while the remaining slope alpha
satisfies the common equations
`(partial_Q-alpha partial_P)^2 h0=0`. Taking the polynomial gcd of those
equations preserves exactly their common algebraic roots. For total
degree at least three there cannot be two distinct roots: in coordinates
along two independent directions, both pure second derivatives would
vanish and the polynomial would be at most bilinear, hence of degree at
most two. A sole algebraic root of a rational polynomial of degree at
most two is rational. Exact reconstruction rejects spurious candidates.
This resolves the linear-shear ambiguity without inferring completeness
from a completed-power choice that could hide an affine family.

The lower-degree rows also pass direct structural review. With linear b
and quadratic a, completing the square produces a nonzero quadratic
restoring coefficient `-mu^2/(4a2)`, and CQ gives the six-dimensional
quadratic sector. With linear b and a of degree at most one, the original
Hamiltonian is `(mu q+alpha)p+phi(q)` with `phi'''=6mu c!=0`.
Its only higher odd gate is `6mu c partial_p^3`, and D preserves its
kernel, giving the full three-strip. Thus this case has an infinite
core, not a two-strip or a six-dimensional core. Purely q-dependent
affine Hamiltonians can be classified through the supplied-chart API;
the original-polynomial chart recognizer deliberately returns a miss
when its p degree is zero. No collapse claim follows from that miss.

## Restoring-force theorem: why the degree bound is universal

For `H=F(P)+lambda Q^2+epsilon Q+C`, `deg F>=3`, `lambda!=0`, the
original third gate is

`C3=-F''' partial_Q^3-6c partial_Q(F'' partial_P^2+F''' partial_P)`.

Take a polynomial G of Q degree N at least three passing `C3` and `C3D`.
The static top coefficients force `g_N,g_(N-1)` to be constants and
`g_(N-2)'=-N(N-1)g_N/(6c)`. The leading coefficient of `C3DG` is then

`12c*N*(N-1)*g_N*F''*F'''`,

which cannot vanish. This excludes all Q degrees at least three without a
bounded search. With N at most two, static exactness gives
`G=g(P)+aQ+bQ^2`; the next gate forces
`g''=(b/lambda)F''`. The integration constants that would give a term
proportional to `1/F''` are excluded by polynomiality, not by an unproved
analytic assumption. Thus the first two tests give exactly
`span{1,Q,P,H}`.

Let `R=(F''F''')'`. Its leading coefficient is nonzero for every polynomial
F of degree at least three. Direct differentiation then gives

`C3D^2Q=12c*lambda*R`,

`C3D^2P=0`,

`C3D^3P=24c*lambda^2*R`.

These identities remove Q and then P, proving the full core
`span{1,H}` and sharp third-gate depth three. The checker evaluates these
identities directly in original coordinates for ten examples spanning
degrees three through seven, with nonunit rational restoring coefficient
and a nonzero linear force. Higher odd gates cannot invalidate the answer:
the upper bound is supplied by C3 alone, and 1,H pass every odd gate by
stationarity and antisymmetry.

## Formal deformation and presentation-dependent module torsion

CD's cubic family uses `H_t=P^3+tQ^2`. Its unrestricted polynomial
corrections give first-order liftable initial space `span{1,P,P^3}`,
and second-order/formal initial space `span{1,P^3}`. The obstruction
`C3D_t^3P=864t^2` agrees with HR at `F=P^3,c=1,lambda=t`. The
constant-coefficient functional cannot be changed by an arbitrary-degree
second correction because `C3D_0^3X` is divisible by `P^5`. Changes of the
first lift belong to the initial core and have zero first variation in
that same functional. The no-degree-cutoff claim is therefore supported
by a coefficient functional, not a finite source matrix.

For the declared finite weight presentation `V_N`, `N>=6`, the Smith-factor
argument is also sound. Generic kernel dimension two and zero-parameter
kernel dimension `floor(N/2)+2` fix the number of nonunit factors. Over an
algebraic closure, no other nonzero parameter gives a rank drop, so all
nonunit factors are powers of t. The first- and second-order liftable
initial dimensions fix one exponent at two and all other exponents at
one. Sufficiency uses lifts already inside every declared `V_N`. Hence
the torsion formula holds for every N at least six. Its free target part
depends on the chosen output population; no presentation-independent
invariant of an undeclared infinite matrix is claimed.

The universal extension RD/RT also passes independent review for every
`H_t=F(P)+tQ^2`, `deg F>=3`. Set `B=F''`, `A=B'`. The exact commutator

`[C,D0]=12c B(A+B partial_P) partial_Q^2`

acts injectively on each nonzero polynomial coefficient of
`partial_Q^2G`, because `B(A+B partial_P)g=B(Bg)'` cannot vanish for a
nonzero polynomial g when B is nonconstant. Thus static exactness and a
Q-independent first-depth residual force every correction to have form
`aQ^2+beta Q+g(P)` with a,beta constant. This is an all-degree argument.
The first-order equations then force the initial tower polynomial to be
`aF+bP+d`, and the nonzero `12c(F''F''')'` residual removes the initial
Q direction.

For the delayed P obstruction, the second-order static and first-depth
equations again force the second correction to have Q degree at most two.
Its third unperturbed iterate is therefore zero. The first variation of
the third-depth gate on any allowed first correction is also zero,
leaving the nonzero residual `24c(F''F''')'`. This coupled argument is
essential: for general F that residual is not constant, so the cubic
case's constant-coefficient functional cannot simply be reused. RD
correctly uses the coupled argument and proves first-order initial space
`span{1,P,F}` and second-order/formal initial space `span{1,F}`.

For the C3-only depth-three finite presentation with weight bound
`N>=2deg F`, the same Smith-factor argument as above applies. HR gives
the generic two-dimensional kernel over the algebraic closure, the
zero-parameter kernel has dimension `floor(N/2)+2`, and the polynomial
lifts `1,P,H_t` lie inside every declared source. The first- and
second-order initial dimensions are therefore three and two in the
finite source as well. It follows that its torsion is exactly one
`K[t]/(t^2)` plus `floor(N/2)-1` copies of `K[t]/(t)`. No other parameter
roots or higher exponents are possible. This confirms both the
general-profile extension and its every-N claim without relying on
sampled Smith forms.

## Terminology, normalization, and primary background

The exact compatibility defect in the affine phase satisfies

`b'beta'''-b'''beta'=(b'beta''-b''beta')'`.

Its integral vanishes under periodic or compact-support boundary
conditions. It is therefore not the usual nontrivial scalar
Virasoro/Gelfand--Fuchs central-extension cocycle. The full defect
`Delta(X,Y)=partial^3[X,Y]-[partial^3X,Y]-[X,partial^3Y]` is the
Chevalley--Eilenberg coboundary, up to sign, of the operator `partial^3`
in the adjoint module. This is a useful explicit compatibility test;
a nontrivial class in a different coefficient module would require an
additional definition and proof.

Ovsienko and Roger give the standard scalar cocycle
`c(f partial,g partial)=(1/12) integral f'''g dx` in equation (9.2) of
[Deforming the Lie algebra of vector fields on the circle inside the Lie
algebra of pseudodifferential symbols](https://arxiv.org/abs/math/9812074)
(1998). The distinction above follows directly from our displayed total
derivative; the cited paper supplies the standard scalar convention.

Equivalence of coordinate-transformed star products with suitably related
Moyal products belongs to established deformation-quantization machinery.
Primary background includes Domański and Błaszak,
[On local equivalence of star-products on Poisson manifolds](https://arxiv.org/abs/1305.4026)
(v3, 2016; v1 appeared in 2013 under an earlier title), and Błaszak and
Domański, [Canonical transformations in quantum mechanics](https://arxiv.org/abs/1208.2835)
(2012). These references support the general background only; they do not
establish historical priority for the particular complete-core theorems
proved in this package.

Finally, the exact cubic gauge uses `s=ct^2/3` when its transvectant
generating product is `exp(t Omega)`. With the physical convention
`exp(i hbar Omega/2)`, substitution gives `s=-c hbar^2/12`. Zero-gate
classifications are unchanged by that parameter normalization. A claim
about a physical hbar coefficient must specify which convention is used.

## Reproduction

Run `python3 -B -S research/core_overlap/phase_independent_review.py`.
The retained receipt records 665 checks in nine categories. They calibrate
the universal proof identities and exact protected spans. They do not
turn finite experimental agreement into a proof of an unlimited core.

\clearpage

# Pure total tops with unequal perfect-power transverse tops

This note uses the flat Weyl convention of the compendium,
`D_H G = H_q G_p - H_p G_q`, and the polynomial dynamic core
`D_infinity(H) = intersection ker T_k(H,D_H^j ·)` for odd `k >= 3`, `j >= 0`.
The coefficient field has characteristic zero. The statements below concern
these fixed canonical coordinates; arbitrary nonlinear canonical substitutions
are not claimed to preserve Weyl exactness.

## A counterexample to the remaining pure-top conjecture

Put

\[
G=qp+q^3,\qquad
H=qG^2=q^3p^2+2q^5p+q^7.
\]

The total top of `H` is the pure seventh power `q^7`. Its transverse, or
`p`-degree, top is `q^3 p^2`, precisely one of the perfect-power exceptions
left open in Theorem T. Nevertheless

\[
\{H,G\}=H,\qquad T_k(H,G)=0\quad(k\ge3).
\]

For the gate identity, every derivative of `G` of total order at least three is
purely in `q`, whereas `H` has `p`-degree two. Thus the sole possibly nonzero
summand of `T_k(H,G)` contains `partial_p^k H=0`. Antisymmetry gives
`T_k(H,H)=0`, and `{H,H}=0`; consequently `G` survives every repeated bracket.
In particular, this is an **active** exact observable, not only a stationary
partner. The all-degree dimension argument below proves

\[
\boxed{D_\infty(H)=\operatorname{span}_K\{1,H,G\}.}
\]

This disproves the unrestricted pure/near two-root conjecture as it was stated
in `DYNAMIC_CORE_RESULTS.md` at commit `e91e14d`. It does not contradict its
proved Theorems B, Q, Q', or the restricted Theorem T.

## Complete classification of the unequal perfect-power exception

**Theorem.** Suppose the total top of a polynomial `H(q,p)` is `c q^d`, with
`d >= 3`, and the `p`-degree top is

\[
F=\alpha\,p^s(q+\gamma)^r,
\qquad \alpha\ne0,\quad r,s\ge2,\quad r\ne s.
\]

Set `t=q+gamma`. Then the following classification holds.

If `s >= 3`, the core is `span{1,H}`. If `s=2` (necessarily `r>=3`), the core
is also `span{1,H}` except for the following explicitly recognizable family:

\[
\begin{aligned}
J&=tp+u(t),\
H&=t^{r-2}\bigl(a_2J^2+a_1J+a_0\bigr)+\beta J+\delta,
\qquad a_2\ne0,\quad u\in K[t],\quad \deg u\ge3.
\end{aligned}
\]

An additive constant of `J` may be removed and absorbed into the displayed
parameters. For this family,

\[
D_\infty(H)=\operatorname{span}_K\{1,H,J\},\qquad
\{H,J\}=(r-2)(H-\beta J-\delta).
\]

The parameters do not impose an artificial degree bound. This is a family of
arbitrarily high total degree and a complete classification under the stated
unequal perfect-power transverse hypothesis. Historical priority is not claimed.

### Proof

**Transverse filtration.** Filter by degree in `p`. The top of `D_H` has
`p`-degree shift `s-1`; the top of `T_k(H,·)` has shift `s-k` because the two
arguments receive exactly `k` derivatives in `p` in each summand. Therefore
the transverse top of a core element lies in `D_infinity(F)`. This remains
valid for the nonnegative weight `(0,1)`; finite-dimensional filtered pieces
are not required. All polynomials have finite transverse degree, and the
usual leading-component comparison applies separately to each identity.

After translating `q`, `F=alpha t^r p^s`. The already proved unequal monomial
classification (Theorem M) gives

\[
D_\infty(F)=\operatorname{span}_K\{1,tp,F\}.
\]

It follows directly, by subtracting a multiple of `H` and descending in
transverse degree, that `dim D_infinity(H)<=3`. At transverse degree zero the
core consists only of constants. If a third element exists, normalize its
transverse top and subtract a multiple of `H` to write it

\[
J=tp+u(t),\qquad u\in K[t].
\]

The core is invariant under `D_H`, so

\[
\{H,J\}=aH+bJ+c.
\]

The coefficient of `p^s t^r` on the left is `(r-s)alpha`; hence
`a=r-s !=0`.

**The gate removes all `s>=3` cases.** Direct differentiation gives

\[
T_3(H,J)=-u'''(t)\,\partial_p^3H.
\]

If `s>=3`, this forces `deg u<=2`. But if `deg u<=2`, `J` is quadratic.
Since the total top of `H` is `c q^d`, comparison of total degree `d` in
`{H,J}=aH+bJ+c` gives `a=d`: the top term is
`q H_q=d c q^d`, and all contributions from lower total components of `H`
have smaller degree. On the other hand the pure total top implies `d>r+s`,
because `F` has a nonzero mixed monomial of degree `r+s`. This contradicts
`a=r-s`. Thus no third element exists for `s>=3`. The same comparison proves
`deg u>=3` whenever a third element exists for `s=2`.

**Integrate the closure relation for `s=2`.** Here `a=r-2>=1`. On the Laurent
polynomial algebra `K[t,t^{-1},J]`, the derivation

\[
H\longmapsto\{H,J\}
=tH_t-(p+u')H_p
\]

is `t partial_t` at fixed `J`. Thus

\[
H+\frac b a J+\frac c a=t^a P(J),\qquad P\in K[J].
\]

Since `H` has `p`-degree two, `P` has degree two and nonzero leading
coefficient. Set `beta=-b/a`, `delta=-c/a`. This is the displayed family.
Conversely, its closure identity follows by direct differentiation. Every
odd gate kills `J` since `H` has `p`-degree two; every odd gate kills `H` by
antisymmetry. Therefore the span of `1,H,J` is an invariant exact sector.
The transverse upper bound makes it the whole core. This proves the theorem.

## An exact decision test in the original polynomial coefficients

Write `H=A(t)p^2+B(t)p+C(t)` with `A=alpha t^r`, `r>=3`, and put `a=r-2`.
Choose the harmless normalization `u(0)=0`. The coefficient of `p` in the
closure identity is equivalent to

\[
2\alpha t^r u'=tB'-(a+1)B-bt.
\]

Its coefficient of `t` fixes `b=-a[t]B`. The numerator must be divisible by
`t^r`; if so, integration uniquely determines the polynomial `u` with
`u(0)=0`. Finally test whether

\[
tC'-Bu'-aC-bu
\]

is constant. This finite calculation is necessary and sufficient. It neither
fits a bounded ansatz nor infers an all-degree claim from a finite matrix.
The accompanying checker replays the closure identity and every nonzero odd
gate using independent PBW operator arithmetic.

## Why the coordinate mechanism is subtle

The nonlinear triangular substitution `p -> p+u(q)/q` explains the classical
eigenvector form when `u(0)=0`. Its Weyl exactness in this sector follows
from the separate derivative argument above, rather than from a claim that
the Moyal product is covariant under nonlinear canonical maps. For example,
the cubic choice `u=q^3` is outside affine covariance and creates a pure
total top from an unequal transverse monomial.

\clearpage

# A complete parabolic quadratic-composition family

Use the flat Weyl convention and polynomial dynamic core of the compendium.
Let the coefficient field have characteristic zero, and set

\[
Q=p+bq^2+cq+d,\qquad b\ne0,\qquad
H=P(Q)+\varepsilon q,\qquad P\in K[z].
\]

For `deg P>=2` the total top of `H` is a pure power of `q`. These are edge
polynomials with constant transverse leading coefficient; no nonlinear
covariance of the Moyal product is assumed.

**Theorem.** The full polynomial core in all degrees is

\[
\boxed{
D_\infty(H)=
\begin{cases}
K[q,p],&\deg P\le1,\\
K[Q]+\operatorname{span}_K\{q,qQ,q^2\},&\deg P=2,\\
K[Q]+Kq,&\deg P\ge3.
\end{cases}}
\]

For `epsilon=0`, `K[Q]` is stationary and `q` is active, with
`{H,q}=-P'(Q)`. For `epsilon!=0`, even the tower `K[Q]` is active:
`{H,f(Q)}=epsilon f'(Q)`. Thus these families disprove the unrestricted
pure-top collapse conjecture both through finite active extensions and
through an infinite active exact sector. Historical priority is not claimed.

## Proof

The polynomial change of variables `t=q`, `z=Q` is used only to analyze the
defining differential operators. Its inverse is `p=z-bt^2-ct-d`, so it is a
polynomial algebra isomorphism. Chain rule gives

\[
D_H=\varepsilon\partial_z-P'(z)\partial_t,
\]

and, by expanding the third transvectant,

\[
\boxed{C_3=-P'''(z)(\partial_t^3+6b\partial_t\partial_z)
               -6bP''(z)\partial_t\partial_z^2.}
\]

The linear summand `epsilon q` contributes no gate. The coefficient `c` and
the additive constant `d` cancel in the displayed chain-rule identity.

**Exactness of the tower.** With the standard Moyal parameter `hbar`,

\[
Q\star f(Q)=Qf(Q)-\frac{b\hbar^2}{4}f''(Q)
            =f(Q)\star Q.
\]

Every star power of `Q` is its ordinary power plus lower-degree polynomials
in `Q`. Induction therefore identifies `K[hbar][Q]` with the star algebra
generated by `Q`. It is commutative. In particular every odd transvectant
between `P(Q)` and `f(Q)` vanishes separately, since each is the coefficient
of a distinct power of `hbar`. The same holds for the added `epsilon q`,
whose gates vanish. This proves exactness of all of `K[Q]` without claiming
covariance under a nonlinear canonical transformation.

**Degree at least three.** Let a core element have positive `t`-degree `N`:

\[
G=\sum_{j=0}^N t^j f_j(z),\qquad f_N\ne0.
\]

The coefficient of `t^{N-1}` in `C_3G=0` is
`-6bN(P'' f_N')'=0`. Since `P''` is nonconstant, a polynomial `f_N` can
satisfy this only if `f_N` is constant. If `N>=2`, the next coefficient
similarly forces `f_{N-1}` constant: the `partial_t^3` term cannot reach
`t^{N-2}`. In `D_HG`, the coefficient of `t^{N-1}` is consequently
`-N P'f_N`; the possible term `epsilon f_{N-1}'` is zero. The coefficient
of `t^{N-2}` in `C_3D_HG` is then

\[
6bN(N-1)f_N\bigl((P'')^2\bigr)',
\]

which is nonzero. Hence `N<=1`; when `N=1`, the first comparison shows
`G=f_0(z)+a t`. Conversely `K[z]+Kt` is invariant under the displayed `D_H`,
and its generators pass every gate: the tower was proved exact and `q` is
linear. This proves the degree-at-least-three case using only `C_3` and one
further bracket.

**Degree two.** Write `P'(z)=kz+l`, `k!=0`. The third gate is now
`C_3=-6bk partial_t partial_z^2`, and no higher odd gate occurs because
`deg H=4`. Its polynomial kernel consists of

\[
G=A(z)+zB(t)+C(t).
\]

The decisive identities are exactly

\[
C_3D_HG=12bk^2B'',\qquad
C_3D_H^2G=-12bk^3C'''\quad\text{once }B''=0.
\]

They force `B''=0` and `C'''=0`. The forcing term
`epsilon partial_z` contributes no term to either decisive identity. Thus
the only extra generators are `t,tz,t^2`. Their brackets are

\[
\begin{aligned}
D_Ht&=-P'(z),\\
D_H(tz)&=\varepsilon t-zP'(z),\\
D_H(t^2)&=-2tP'(z).
\end{aligned}
\]

These lie in the asserted sector, whose third gate is zero. All later
brackets are therefore exact. If `deg P<=1`, `H` has degree at most two and
every gate vanishes, giving the whole polynomial ring. This completes the
proof.

## Concrete lowest-degree counterexample

For `Q=p+q^2` and `H=Q^2=q^4+2q^2p+p^2`,

\[
D_\infty(H)=K[p+q^2]+\operatorname{span}\{q,q(p+q^2),q^2\}.
\]

In particular `q` evolves exactly and nontrivially. This quartic is outside
the previously listed pure-top strip and affine structures: its transverse
second derivative is nonzero and its mixed term has degree three.

## Exact recognition

Normalize the coefficient of `p` in `Q` to one and its constant term to zero.
If `mu=deg_p H>=2` and the coefficient of `p^mu` is the nonzero constant
`a_mu`, the coefficient `B(q)` of `p^{mu-1}` must satisfy

\[
V(q)=\frac{B(q)-B(0)}{\mu a_\mu}=bq^2+cq,\qquad b\ne0.
\]

This fixes `Q=p+V(q)`. Substitute `p=z-V(q)` into `H`; recognition succeeds
exactly when the result is a polynomial in `z` plus `epsilon q`. Thus the
adjunct decision rule uses exact identities and never a fitted finite-degree
ansatz. Its independent checks compare the transformed third gate against
PBW arithmetic and directly test the asserted finite-degree dimensions.

\clearpage

# The exact six-dimensional core of a squared shear coordinate

Let `u in K[q]` have degree at least three, with `K` a field of
characteristic zero, and put `Q=p+u(q)`. Use the original flat Moyal
product in `(q,p)` and the convention `{H,G}=H_q G_p-H_p G_q`.

**Theorem SS.** For any quadratic polynomial

\[
H=AQ^2+BQ+C+\varepsilon q,\qquad A\ne0,
\]

the full polynomial dynamic core is exactly

\[
\boxed{\mathcal D_\infty(H)
 =\operatorname{span}_K\{1,q,Q,q^2,qQ,Q^2\}.}             \tag{SS1}
\]

It therefore has dimension six in all degrees. These pure-top
Hamiltonians are outside the conjectured two-dimensional collapse.
Their positive structure is an elementary polynomial canonical shear,
but covariance of the flat Moyal product under arbitrary nonlinear
canonical maps is not assumed in the proof.

**Proof.** Polynomial substitution identifies `K[q,p]` with `K[q,Q]`.
The Hamiltonian derivation and the third gate, expressed in this
polynomial coordinate ring, are exactly

\[
D=-(2AQ+B)\partial_q+\varepsilon\partial_Q,\qquad
C_3=(2AQ+B)u'''(q)\partial_Q^3
               -6Au''(q)\partial_q\partial_Q^2.           \tag{SS2}
\]

For clarity, the derivatives in (SS2) keep `Q` fixed. To check the gate,
use `H_qqq=(2AQ+B)u'''+6Au'u''`, `H_qqp=2Au''`, and
`H_qpp=H_ppp=0`, and then
`partial_q(old)=partial_q(new)+u' partial_Q`. The terms involving
`u'u''` cancel exactly.

Let `V` be the polynomials of total degree at most two in `(q,Q)`.
Equation (SS2) kills `V`, and `D` preserves `V`. Every element of `V`
has degree at most two in the original variable `p`, as does `H`, so
all odd transvectants of order at least five vanish. Thus
`V subset D_infty(H)`.

Suppose a core element `G` lies outside `V`, and let `G_N` be its
highest component in total degree, with `N>=3`. Write `m=deg u>=3` and
let `u_m` be the leading monomial of `u`. The top parts of the
operators for this total-degree filtration are

\[
D_0=-2AQ\partial_q,\qquad
C_0=2AQ u_m'''\partial_Q^3-6Au_m''\partial_q\partial_Q^2.
\]

The weighted shifts are zero for `D_0` and `m-5` for `C_0`. The other
terms have strictly smaller shifts; this includes the `B` term of
`C3`. Hence `C3 D^rG=0` implies `C_0 D_0^rG_N=0` for every `r>=0`.
Let `a` be the largest `q` exponent occurring in `G_N`. By homogeneity,

\[
D_0^aG_N=c_0Q^N,\qquad c_0\ne0.
\]

But then

\[
C_0D_0^aG_N=2A c_0(N)_3u_m'''Q^{N-2}\ne0,
\]

because `N>=3`, `A c_0!=0`, and `u_m'''!=0` in characteristic zero.
This contradiction proves (SS1), including the constant-force term
`epsilon q`. The argument gives a finite failure witness for every
proposed polynomial outside the core, not a finite-degree extrapolation.

**Sharp uniform stopping rule.** In fact,

\[
\boxed{\mathcal D_\infty(H)
 =\ker C_3\cap\ker(C_3D)\cap\ker(C_3D^2).}               \tag{SS3}
\]

To prove the uniform depth bound, write `u_m=alpha q^m`. The top
operator `C_0D_0^r` sends `q^aQ^c` to a single monomial, with
coefficient

\[
2A\alpha m(m-1)(-2A)^r(a)_r(c+r)_2
 \big[(m-2)(c+r-2)-3(a-r)\big].                          \tag{SS4}
\]

For fixed `r` the output shift is independent of `(a,c)`, so distinct
input monomials cannot cancel. Every monomial with `a+c>=3` fails one
of the checks `r=0,1,2`. If `c>=2` and the `r=0` bracket is zero,
then `a>=1` and the `r=1` bracket is `m+1`, nonzero. If `c=1`, then
`a>=2` and `r=1` gives `-3(a-1)`, nonzero. If `c=0`, then `a>=3`
and `r=2` gives `-3(a-2)`, nonzero. All the relevant falling factorials
are nonzero. Thus the joint top kernel has total degree at most two.
The same total-degree filtration used in the proof lifts this bound to
the actual operators, proving (SS3).

Two bracket steps are necessary for this gate: the cubic `q^3` satisfies

\[
C_3q^3=C_3Dq^3=0,\qquad
C_3D^2q^3=-288A^3u''\ne0.                               \tag{SS5}
\]

So discarding the last condition in (SS3) gives a strictly larger
space. The theorem settles both the all-degree core and the exact
uniform bracket depth for detecting it using `T3`.

## Recognition in the original coordinates

Suppose a supplied rational Hamiltonian has degree two in `p`, its
`p^2` coefficient is a nonzero constant `A`, and its `p` coefficient is
`b(q)`. Set

\[
B=b(0),\qquad u(q)=\frac{b(q)-B}{2A},\qquad Q=p+u(q).
\]

If `deg u>=3` and `H-AQ^2-BQ` is affine in `q`, Theorem SS applies. This
test uses exact coefficient arithmetic. It rejects a nonconstant
quadratic coefficient and rejects residual terms of degree at least two
scope. The canonical shear may subsequently be composed with affine
symplectic substitutions, under which the original flat Moyal
structure is covariant.

The qualification `deg u>=3` matters: when `u'''=0`, the last
contradiction does not apply. For instance if `deg u=2`, all
polynomials in `Q` pass every gate and remain in that space under `D`,
giving an infinite core. Such an input must not be assigned a
six-dimensional bound by this theorem.

`analytic_shear_square.py` supplies the exact recognizer and a direct
transvectant checker. It verifies the transformed gate on monomials,
all six basis elements under every nonzero odd correction, invariance
under `D`, and finite-box dimensions with full output retained. The
proof above establishes the all-degree result.

No literature-priority claim is made. The result is a scoped
classification for the fixed original affine Moyal product and an
explicit correction to the pure-top collapse conjecture.

\clearpage

# Completing the polynomial shear-composition phase diagram

All statements use one canonical pair, the original flat Weyl product in
`(q,p)`, and the convention `{H,G}=H_q G_p-H_p G_q`. The coefficient field
`K` has characteristic zero. The dynamic core consists of polynomials `G`
such that every odd transvectant `T_k(H,D^rG)`, `k>=3`, `r>=0`, vanishes,
where `D={H,.}`. No covariance under a nonlinear canonical substitution is
assumed. Historical priority is not established.

## The missing composition quadrant

**Theorem SCP.** Let

\[
Q=p+u(q),\qquad H=P(Q)+\varepsilon q,\qquad
m=\deg u\ge3,\quad \mu=\deg P\ge3.
\]

Then, in all polynomial degrees,

\[
\boxed{\mathcal D_\infty(H)
=\ker C_3\cap\ker(C_3D)
=\operatorname{span}_K\{1,H\}.}                         \tag{SCP1}
\]

Both tests in the middle expression are necessary for every allowed
choice of parameters. Thus one bracket step is a sharp uniform stopping
depth when using the third gate.

### Exact transformed operators

Use the polynomial algebra isomorphism `(q,p)->(q,Q)` only to express the
original operators. Derivatives below keep `Q` fixed. Chain rule gives

\[
D=\varepsilon\partial_Q-P'(Q)\partial_q,
\]

\[
\boxed{C_3=
u'''(P'\partial_Q^3-P'''\partial_Q)
-3u''(P''\partial_q\partial_Q^2+P'''\partial_q\partial_Q)
-P'''\partial_q^3.}                                    \tag{SCP2}
\]

Here the derivatives of `P` are evaluated at `Q`; those of `u` are
evaluated at `q`. To derive (SCP2), substitute
`partial_q(old)=partial_q(new)+u' partial_Q` and
`partial_p(old)=partial_Q` into the alternating third transvectant.
Terms containing `u'` cancel. In particular the derivative of `u'` in
the cubic power of the old `q` derivative contributes the term
`-u'''P''' partial_Q`; it must not be omitted. The linear forcing has
no third gate.

### All-degree proof and the absence of cancellation

Filter `K[q,Q]` by ordinary total degree. Write
`u=alpha q^m+lower` and `P=rho Q^mu+lower`, with `alpha rho != 0`.
The top derivation is

\[
D_0=-\rho\mu Q^{\mu-1}\partial_q,
\qquad\text{degree shift }\mu-2.
\]

The top third gate `C_0` consists of the first four terms in (SCP2),
using the leading monomials of `u` and `P`. Its degree shift is
`m+mu-7`. The omitted term `-P''' partial_q^3` has shift `mu-6`,
strictly smaller by `m-1`; all other omitted coefficient terms are
also lower. A negative gate shift, possible when `m=mu=3`, causes no
problem: lower input components still have strictly lower output degree.

For `c>=1`, direct differentiation gives

\[
\boxed{C_0(q^aQ^c)=\alpha\rho\mu m(m-1)
c(c+\mu-3)\big[(m-2)(c-\mu)-3(\mu-1)a\big]
q^{a+m-3}Q^{c+\mu-4}.}                                \tag{SCP3}
\]

For `c=0`, the image is zero directly. Distinct input monomials with
nonzero images have distinct output monomials, since the exponent
shift is fixed. Consequently no linear combination can cancel a
nonzero coefficient in (SCP3).

Suppose `G` passes `C_3` and `C_3D`, and let `G_N` be its highest
homogeneous component. Extracting the highest possible output degree
in the two equations gives

\[
C_0G_N=0,\qquad C_0D_0G_N=0.                           \tag{SCP4}
\]

The first equation permits only monomials with `c=0`, or with

\[
(m-2)(c-\mu)=3(\mu-1)a.                               \tag{SCP5}
\]

In the latter case `c>=mu`. Consider the second equation monomial by
monomial. Its nonzero images again have one fixed exponent shift,
now `(m-4,2mu-5)`, so they cannot cancel each other.

If `c=0,a>=1`, applying `D_0` gives a nonzero multiple of
`q^{a-1}Q^{mu-1}`. The last bracket in (SCP3) becomes
`-(m-2)-3(mu-1)(a-1)`, a strictly negative integer. The other
factors are nonzero. Such a monomial therefore fails (SCP4).

If (SCP5) holds and `a>=1`, applying `D_0` changes `(a,c)` to
`(a-1,c+mu-1)`. The last bracket changes from zero to
`(mu-1)(m+1)`, again nonzero. Such a monomial also fails (SCP4).

Only `1` and `Q^mu` remain in the joint top kernel. Thus a
nonconstant `G` has `N=mu` and `G_N=lambda Q^mu`. Subtract
`(lambda/rho)H`, which passes both tests by odd antisymmetry and
`DH=0`. The remainder has degree below `mu`, so the same argument
forces it to be constant. This proves that the two-test kernel is
`span{1,H}`. Every odd gate kills this span, which is stationary
under `D`; therefore it is also the full dynamic core. This proves
(SCP1) without a numerical degree bound.

### Sharp necessity of each test

The two witnesses work for every `u,P,epsilon` in the theorem:

\[
C_3q=0,\qquad
C_3Dq=u'''(P'''P''-P'P'''')\ne0;                        \tag{SCP6}
\]

\[
C_3Q=-u'''P'''\ne0,\qquad C_3DQ=0.                    \tag{SCP7}
\]

For (SCP6), the polynomial in parentheses has degree `2mu-5` and
leading coefficient `2rho^2 mu^2(mu-1)(mu-2)`, which is nonzero in
characteristic zero. For (SCP7), `DQ=epsilon` is constant. Thus
neither of the two tests may be discarded, and depth zero is
insufficient throughout the stated family.

## Exact recognition and the completed scope

For an input polynomial of `p` degree `mu>=3`, its leading `p`
coefficient must be a nonzero constant `rho`. If `B(q)` is its
`p^(mu-1)` coefficient, the normalization `u(0)=0` fixes

\[
u(q)=\frac{B(q)-B(0)}{\mu\rho}.
\]

Substitute `p=Q-u(q)` into `H`. Recognition succeeds exactly when
`deg u>=3` and the result is a polynomial in `Q` plus `epsilon q`.
This is a finite exact identity test; no bounded partner ansatz is
fitted. A failed recognition is outside this route, rather than a
certificate of collapse.

Together with the retained results this closes the composition
family `H=P(p+u(q))+epsilon q` for every polynomial `u` of degree at
least two. Quadratic `u` is Theorem QC in
`pure_quadratic_composition.md`. For `deg u>=3`, quadratic `P` is
Theorem SS in `analytic_shear_square.md`; degree at least three is
(SCP1). If `deg P=1`, the Hamiltonian has the form `a p+v(q)`:
when `deg v>=3`, Theorem P+ gives the strip of `p` degree at most
two; when `deg v<=2`, every polynomial is exact. A constant `P`
also gives a Hamiltonian of degree at most one, hence the whole
polynomial ring. These elementary low-degree cases are referenced
for completeness and are not new claims of this note.

`shear_composition_complete.py` supplies the rational-coefficient
recognizer, transformed operators, a symbolic four-parameter factor
identity, direct original-coordinate and independent PBW checks,
uniform sharpness witnesses, and full-output finite kernel checks.
The proof above supplies the all-degree result. The accompanying
JSON records the exact replay and its stated finite scope.

\clearpage

# Oscillator forcing in polynomial shear coordinates

All brackets and gates below use the fixed flat Weyl convention in the
original coordinates `(q,p)`. The substitution `Q=p+u(q)` is used to
rewrite differential operators, not to assume nonlinear covariance.
The coefficient field has characteristic zero.

## Complete oscillator sector

Let

\[
 Q=p+u(q),\qquad
 H=AQ^2+BQ+C+\frac{\kappa}{2}q^2+\epsilon q,\qquad A\ne0.
\]

**Theorem SO.** If `deg u>=3`, then for every `kappa,B,C,epsilon`,

\[
 \mathcal D_\infty(H)=
 \ker C_3\cap\ker(C_3D)\cap\ker(C_3D^2)
 =\operatorname{span}\{1,q,Q,q^2,qQ,Q^2\}.             \tag{SO1}
\]

The depth two is sharp for every allowed parameter choice. If
`u=bq^2+cq+d`, `b!=0`, and `kappa!=0`, then instead

\[
 \mathcal D_\infty(H)=\bigcap_{r=0}^3\ker(C_3D^r)
 =\operatorname{span}\{1,q,Q,q^2,qQ,Q^2\},             \tag{SO2}
\]

and depth three is sharp. The quadratic-shear case `kappa=0` is the
previously classified infinite QC family and is excluded from (SO2).
Neither statement classifies nonpolynomial observables.

## Exact operators and the lower bound

Direct chain-rule expansion in `(q,Q)` gives

\[
 D=(\kappa q+\epsilon)\partial_Q-(2AQ+B)\partial_q,
 \qquad
 C_3=(2AQ+B)u'''\partial_Q^3-6Au''\partial_q\partial_Q^2.
                                                               \tag{SO3}
\]

The quadratic `q` potential changes the derivation but no higher gate.
The space in (SO1) is invariant under `D`, and `C3` kills it. Every
higher odd gate vanishes on it in the original coordinates: both `H`
and each sector element have `p` degree at most two, whereas order at
least five requires their combined `p` differentiation order to be at
least five. This proves inclusion in the full core.

## Completeness and sharp depth when degree u is at least three

Put `m=deg u>=3` and give both `q,Q` degree one. The leading derivation
is `D0=kappa*q*partial_Q-2A*Q*partial_q`, of degree shift zero. The
leading gate `C0` has shift `m-5`; its action on a monomial `q^a Q^c`
is, up to a fixed nonzero scalar,

\[
 c(c-1)[(m-2)(c-2)-3a]q^{a+m-3}Q^{c-2}.              \tag{SO4}
\]

Distinct nonzero images have distinct exponents. The negative gate
shift for `m=3,4` is harmless: every lower input degree still produces
a strictly lower output degree, and all nonzero monomial outputs have
nonnegative exponents.

Suppose a polynomial passes the three tests and has homogeneous top
`G_N`, `N>2`. Its top must satisfy `C0 D0^r G_N=0`, `r=0,1,2`.
Equation (SO4) leaves only the monomials `q^N`, `q^(N-1)Q`, and
possibly a single resonance `q^(N-c)Q^c`, where

\[
 c=\frac{3N+2m-4}{m+1}.                              \tag{SO5}
\]

If that resonance is integral, `3<=c<=N-1`. Under `D0` its
`Q^(c+1)` monomial comes from the `-2AQ partial_q` part; its subsequent
`C0` image has `Q` exponent `c-1` and a nonzero coefficient, which
cannot be canceled by either other candidate.
The resonance coefficient therefore vanishes. The term originating in
the `Q^2` monomial of `D0(q^(N-1)Q)` next forces the coefficient of
`q^(N-1)Q` to vanish. Finally `D0^2(q^N)` has a `Q^2` monomial with
nonzero `C0` image, with bracket factor
`-3(N-2)` and derivation factor `4A^2N(N-1)`. This excludes the final
candidate. Thus every polynomial in the three-test kernel has degree
at most two in `(q,Q)`, proving (SO1).

Sharpness has the same witness even with oscillator forcing:

\[
 C_3q^3=C_3Dq^3=0,\qquad
 C_3D^2q^3=-288A^3u''\ne0.                           \tag{SO6}
\]

Indeed `D^2q^3=6q(2AQ+B)^2-6Aq^2(kappa q+epsilon)`; the additional
`q^3` term is killed by `C3`.

## Quadratic shear: four cubic derivatives are generated

For `u=bq^2+cq+d`, `b!=0`, the gate is the constant-coefficient
operator `C3=-12Ab*partial_q*partial_Q^2`. For `kappa!=0` use the affine
centering `x=q+epsilon/kappa`, `y=Q+B/(2A)`, so
`D=kappa*x*partial_y-2A*y*partial_x`.
Write `X=partial_x`, `Y=partial_y`, and start with `E0=XY^2`.
Successive right commutators `E_(r+1)=E_r D-D E_r` are

\[
\begin{aligned}
 E_0&=XY^2,\\
 E_1&=\kappa Y^3-4AX^2Y,\\
 E_2&=8A^2X^3-14A\kappa XY^2,\\
 E_3&=80A^2\kappa X^2Y-14A\kappa^2Y^3.
\end{aligned}                                                   \tag{SO7}
\]

Their coefficient matrix in `X^3,X^2Y,XY^2,Y^3` has determinant
`192A^4 kappa^2`, hence spans all constant-coefficient cubic
derivatives. If `C3D^rG=0`, `r=0..3`, then each `E_rG=0` by the
binomial commutator identity. Every third partial derivative of `G`
therefore vanishes, so `G` has degree at most two. This proves (SO2).

For every `B,epsilon`, the centered witness
`G=3kappa*x^2*y+4A*y^3` passes depths zero, one and two, but

\[
 C_3D^3G=-1728A^3b\kappa^2\ne0.                     \tag{SO8}
\]

For `B=epsilon=0`, this is `G=3kappa q^2Q+4AQ^3`.

## Exact finite dynamics

In the ordered basis `(1,q,Q,q^2,qQ,Q^2)`, columns of the following
matrix are the coefficients of the images under `D`:

\[
 M=\begin{pmatrix}
 0&-B&\epsilon&0&0&0\\
 0&0&\kappa&-2B&\epsilon&0\\
 0&-2A&0&0&-B&2\epsilon\\
 0&0&0&0&\kappa&0\\
 0&0&0&-4A&0&2\kappa\\
 0&0&0&0&-2A&0
 \end{pmatrix}.                                               \tag{SO9}
\]

Put `omega^2=2A*kappa` and define entire formal functions
`C(t)=sum_j (-omega^2)^j t^(2j)/(2j)!`,
`S(t)=sum_j (-omega^2)^j t^(2j+1)/(2j+1)!`, and
`T(t)=sum_j (-omega^2)^j t^(2j+2)/(2j+2)!`.
Thus `C'=-omega^2 S`, `S'=C`, `T'=S`, and `C+omega^2 T=1`.
The exact closed flow, uniformly including `kappa=0`, is

\[
\begin{aligned}
 q(t)&=C(t)q-S(t)(2AQ+B)-2A\epsilon T(t),\\
 Q(t)&=C(t)Q+S(t)(\kappa q+\epsilon)-\kappa B T(t).
\end{aligned}                                                   \tag{SO10}
\]

The remaining four basis flows are `1,q(t)^2,q(t)Q(t),Q(t)^2`.
When `2A*kappa>0` these are oscillator trigonometric functions; when
negative they are hyperbolic functions; when zero they reduce to the
previous polynomial shear-square flow. These are algebraic/formal
Hamiltonian identities, not claims about global operator domains or
experimental performance.

## Spectrum and minimal dynamics for nonzero oscillator strength

For `kappa!=0`, put `w=2A*kappa` and work over the algebraic closure.
The characteristic and minimal polynomials of (SO9) are exactly

\[
 \chi_M(z)=z^2(z^2+w)(z^2+4w),\qquad
 m_M(z)=z(z^2+w)(z^2+4w).                            \tag{SO11}
\]

In particular the six-dimensional sector is semisimple, with zero
eigenvalue of multiplicity two and the other eigenvalues
`r,-r,2r,-2r`, where `r^2=-w`. This is a genuine oscillatory or
hyperbolic extension of the earlier nilpotent shear-square motion.

For a direct proof, center `x=q+epsilon/kappa`, `y=Q+B/(2A)` and set
`L_+=y-r*x/(2A)`, `L_-=y+r*x/(2A)`. Then
`D L_+=r L_+`, `D L_-=-r L_-`. The basis
`1,L_+,L_-,L_+^2,L_+L_-,L_-^2` diagonalizes the action. The five
distinct eigenvalues prove the stated minimal polynomial, and the
two independent zero eigenvectors prove the multiplicity. An exact
matrix certificate independently checks (SO11), the polynomial matrix
identity `M^5+5w M^3+4w^2 M=0`, linear independence of
`I,M,...,M^4`, and `rank M=4`.

The retained exact observer compiler and independent checker also replay
the derivative-closure contracts for the original targets `q`, `q^2`,
and their joint pair, using this six-element coefficient basis. In the
checked fixtures their minimal dimensions are `2,3,5` when `epsilon=0`
and `3,5,6` otherwise. These are exact finite-model target ranks,
not a statement about noisy measurements, sensor cost, or a general
physical observation model. The contracts concern the original targets;
recentering a target can change its constant component and its closure.

## Recognition and verification

`shear_oscillator.py` recognizes this family directly from rational
coefficients of `H(q,p)`, normalizing `u(0)=0`. It extracts the constant
coefficient of `p^2`, recovers `u` from the nonconstant `p` coefficient,
and requires the remaining residual to be quadratic in `q`. The
recognizer rejects negative or fractional exponents and inexact
floating-point input before any polynomial normalization. The
quadratic-shear zero-oscillator case is returned as unrecognized here
and belongs to the retained QC route.

The checker compares both transformed operators with independent
original-coordinate differentiation, checks every protected basis gate,
verifies the sharp witnesses including centered nonzero `B,epsilon`,
and computes finite kernels while retaining every output coefficient.
It also checks the commutator span and the matrix/closed-flow formal
Taylor coefficients, characteristic/minimal polynomials, and retained
observer certificates exactly. Those finite calculations corroborate the
identities; the preceding proofs establish all polynomial degrees.

\clearpage

# Complete constant-quadratic momentum classification

Fix one canonical pair over a characteristic-zero field and the original
flat Weyl convention. Let

\[
\begin{aligned}
H&=A p^2+B(q)p+C(q),\qquad A\ne0\text{ constant},\\
u&=\frac{B(q)}{2A},\qquad Q=p+u(q),\qquad
V=C(q)-\frac{B(q)^2}{4A}.
\end{aligned}
\]

Thus `H=AQ^2+V` exactly. The constant term of `u` is retained in this
normalization. Put `m=deg u`, `n=deg V`, and use degree `-1` for the
zero polynomial. Write `D={H,.}`, `C3=T3(H,.)`, and

\[
 K_r(H)=\bigcap_{j=0}^r\ker(C_3D^j)
 \quad\text{inside }K[q,p].
\]

**Theorem CQ.** The following alternatives exhaust every such polynomial
Hamiltonian. In every row the displayed core equals `K_r(H)` for the
displayed depth, and every positive depth is sharp.

Write \(V_2=\operatorname{span}\{1,q,Q,q^2,qQ,Q^2\}\) and
\(T_2=K[Q]+\operatorname{span}\{q,qQ,q^2\}\).

| Shear degree | Residual degree | Full core | Dimension | Sharp depth |
|---|---|---|---|---|
| \(m\le1\) | \(n\le2\) | \(K[q,p]\) | infinite | \(0\) |
| \(m\le1\) | \(n=3\) | \(\operatorname{span}\{1,H\}\) | \(2\) | \(7\) |
| \(m\le1\) | \(n\ge4\) | \(\operatorname{span}\{1,H\}\) | \(2\) | \(5\) |
| \(m=2\) | \(n\le1\) | \(T_2\) | infinite | \(2\) |
| \(m=2\) | \(n=2\) | \(V_2\) | \(6\) | \(3\) |
| \(m\ge3\) | \(n\le2\) | \(V_2\) | \(6\) | \(2\) |
| \(m\ge2\) | \(n=3\) | \(\operatorname{span}\{1,H\}\) | \(2\) | \(6\) |
| \(m\ge2\) | \(n\ge4\) | \(\operatorname{span}\{1,H\}\) | \(2\) | \(4\) |

This is a complete classification in the constant-leading-coefficient
quadratic momentum scope, including Hamiltonians whose top need not be
pure. A variable coefficient of `p^2`, higher momentum degree, analytic
nonpolynomial observables, and more canonical pairs remain outside it.
No statement depends on sampled stabilization or a finite degree cutoff.

## Proof and dependencies

Completion of the square is an exact polynomial identity and does not
assert nonlinear covariance of the flat Weyl product. Each non-affine
shear branch instead uses its independently differentiated operators in
the original coordinates.

For `m<=1`, the shear is affine symplectic. If `n<=2`, `H` is quadratic,
so every higher odd gate vanishes. For nonlinear residuals, the complete
affine-shear potential theorem in `affine_shear_potentials.md` gives
dimension two and the respective sharp depths seven and five.

For `m=2,n<=1`, this is exactly the retained parabolic quadratic
composition theorem QC, with composition polynomial `P(z)=Az^2` and
linear forcing `V(q)`. Its proof gives the third-gate depths zero
through two as a complete criterion. The witness `q^3` passes depths
zero and one and fails at depth two by `-288A^3u''`.
Explicitly, with \(L=\partial_q\partial_Q^2\), the two successive
commutators with \(D=-2AQ\partial_q+V'\partial_Q\) are
\(-4A\partial_q^2\partial_Q\) and \(8A^2\partial_q^3\).
Their common polynomial kernel is exactly \(T_2\), since \(V'\) is
constant in this row. This also proves the uniform depth claim directly.

For `m=2,n=2` and `m>=3,n<=2`, the oscillator theorem in
`shear_oscillator.md` gives the six-dimensional sector. For `m=2`,
the coefficient `kappa=V''` is nonzero and the sharp depth is three.
For `m>=3`, the sharp depth is two, including zero oscillator strength.

For `m>=3,n>=3`, the all-degree six-dimensional upper reduction and
full-output invariant-kernel proof in `quadratic_frontier.md` give
`span{1,H}`, with sharp depth six for cubic residuals and four for
higher residuals. For `m=2,n>=3`, the complete nonlinear-residual
quadratic-shear theorem in `quadratic_shear_residual.md` gives the same
answer and depths. Its cubic case has a parameter-polynomial minor
certificate valid for every residual parameter, rather than just
sampled parameter values. These alternatives exhaust the integer
degree pairs and prove the table.

For each finite row the code also gives an exact basis in the original
coordinates and its Hamiltonian derivation matrix. The two-dimensional
cores are stationary. The six-dimensional cores carry the already
proved exact oscillator, hyperbolic, or nilpotent dynamics. In the
infinite QC row, linear forcing makes the polynomial tower active.

## Exact classifier and replay contract

`constant_quadratic_classification.py` accepts rational coefficients
directly as a sparse polynomial dictionary, or via its CLI as JSON rows
`[q_exponent,p_exponent,"rational coefficient"]`. Exponents must be
nonnegative integers. Floating-point coefficients or exponents,
fractional or negative powers, variable `p^2` coefficients, and higher
momentum degree are rejected before normalization.

The returned `CQ` record includes the case, core, dimension, normalized
`Q,V,A`, both degrees, exact finite basis where applicable, derivation
matrix, sharp third-gate depth, linked proof, and finite stopping
equality. This is a finite exact theorem-application record, even when
the classified core is infinite-dimensional; it is not a claim that
the returned finite matrix represents every polynomial observable.
`check_certificate` independently recovers the normal form and checks
the branch metadata and finite-basis gate identities. The all-degree
upper bound remains the stated written proof dependency.

The optional `--with-certificate` delegates to the existing QF, QR,
SO, QC, or affine-shear branch machinery for additional receipts where
available. The standard-library self-test covers every row, uses exact
original-coordinate gates and brackets, checks finite-basis closure and
sharp witnesses, and rejects altered theorem applications and invalid
scope inputs.

Example commands, from the repository root:

```sh
python3 -B research/core_overlap/constant_quadratic_classification.py
python3 -B research/core_overlap/constant_quadratic_classification.py --classify H.json
python3 -B research/core_overlap/constant_quadratic_classification.py --classify H.json --with-certificate
python3 -B research/core_overlap/constant_quadratic_classification.py --check-certificate application.json
```

The result organizes the component fixed-Hamiltonian classifications;
it does not claim to introduce completion of the square, nonlinear
canonical transformations, or the established general quantization
obstruction. Historical priority of the exact complete scope and sharp
depth table remains unestablished.

\clearpage

# Complete constant-quadratic higher-shear classification and sharp depths

Work over a characteristic-zero field with the original flat Weyl–Moyal
product in the canonical variables `(q,p)`. Let

\[
Q=p+u(q),\qquad H=AQ^2+V(q),\qquad A\ne0,
\qquad m=\deg u\ge3,
\]

where `V` is **any polynomial**, with no degree restriction relative to
`u`. Put `D={H,·}` and `C3=T3(H,·)`.

**Theorem QF.** The full polynomial dynamic core is

\[
\boxed{\mathcal D_\infty(H)=
\begin{cases}
\operatorname{span}\{1,q,Q,q^2,qQ,Q^2\},&\deg V\le2,\\
\operatorname{span}\{1,H\},&\deg V\ge3.
\end{cases}}                                                    \tag{QF1}
\]

The maximum necessary third-gate depth is exactly

\[
\boxed{R(H)=
\begin{cases}
2,&\deg V\le2,\\
6,&\deg V=3,\\
4,&\deg V\ge4,
\end{cases}
\quad
\mathcal D_\infty(H)=\bigcap_{r=0}^{R(H)}\ker(C_3D^r).}      \tag{QF2}
\]

Each bound is sharp for **every** Hamiltonian in its stratum. In
particular, no higher odd gate is needed for this entire polynomial
family. The result includes the degree-resonant boundary `deg V=2m`;
there is no exceptional locus at that degree.

Completing the square shows that this class is exactly the polynomial
Hamiltonians `A p^2+B(q)p+C(q)` with `A` nonzero constant and
`deg B>=3`. Take `u=B/(2A)` and `V=C-B^2/(4A)`. No division by a
nonconstant polynomial or nonlinear covariance of the flat Moyal product
is assumed. Quadratic shears `deg u=2` and nonconstant coefficients of
`p^2` remain outside this theorem.

## A two-equation bound in all momentum degrees

In the original canonical coordinates,

\[
C_3=H_{qqq}\partial_p^3-3H_{qqp}\partial_q\partial_p^2,
\quad H_{qqp}=2Au'',
\quad H_{qqq}=2Au'''p+\bigl(Au^2+V\bigr)'''.              \tag{QF3}
\]

Suppose `G` has top momentum term `g(q)p^N`, with `N>=3` and
`g!=0`. The coefficient of `p^(N-2)` in `C3G` is

\[
2A(N)_2\bigl((N-2)u'''g-3u''g'\bigr).                    \tag{QF4}
\]

All omitted terms have strictly smaller momentum degree: the constant
part of `H_qqq` lowers it by three, and lower momentum terms of `G`
cannot contribute to this coefficient. If `a=deg g`, vanishing implies

\[
3a=(N-2)(m-2)>0.                                         \tag{QF5}
\]

Thus `a>=1`, so `DG` has nonzero leading term
`-2Ag'(q)p^(N+1)`. Applying (QF4) to this leading term, the condition
`C3DG=0` would imply

\[
3(a-1)=(N-1)(m-2).                                       \tag{QF6}
\]

Subtracting (QF5) from (QF6) gives `-3=m-2`, contradicting `m>=3`.
This proves that the common kernel of `C3` and `C3D` has momentum
degree at most two, in **all** polynomial degrees, independently of
`V`. For momentum degree two, (QF4) specializes to `-12Au''g'`,
so the coefficient of `p^2` must be constant. This proof uses polynomial
leading degrees, not any finite numerical cutoff.

## The exact six-dimensional depth-two space

In the independent polynomial variables `(q,Q)`, the exact operators are

\[
D=-2AQ\partial_q+V'\partial_Q,
\qquad
C_3=(2AQ u'''+V''')\partial_Q^3
             -6Au''\partial_q\partial_Q^2.                \tag{QF7}
\]

Take an element passing depths zero, one, and two. By the preceding
argument, write

\[
G=cQ^2+b(q)Q+f(q),\qquad c\in K.
\]

The coefficient of `Q^2` in `DG` is `-2Ab'`. Since `DG` has
momentum degree at most two, its third gate is simply `-12Au''`
times the derivative of that coefficient. The condition `C3DG=0`
therefore gives `b''=0`, so `b=alpha q+beta`.

The coefficient of `Q` in `DG` is `-2Af'+2cV'`. Applying `C3` to
`D^2G` consequently gives the final condition

\[
f'''=(c/A)V'''.
\]

Integrating within the polynomial ring proves the inclusion in

\[
S_H=\operatorname{span}\{1,H,q,Q,q^2,qQ\}.                \tag{QF8}
\]

Conversely, direct use of (QF7) shows every displayed basis vector passes
the first three tests. For example the two derivatives of `qQ` have
momentum degrees two and one, respectively, with constant quadratic
coefficient at the first step; `H` is stationary. The six basis vectors
are independent because only `H` has a nonzero `Q^2` term. Thus

\[
\boxed{\ker C_3\cap\ker(C_3D)\cap\ker(C_3D^2)=S_H.}        \tag{QF9}
\]

For any `R>=2`, the space passing depths zero through `R` is exactly

\[
S_H\cap D^{-1}S_H\cap\cdots\cap D^{-(R-2)}S_H,            \tag{QF10}
\]

because membership of `D^jG` in `S_H` is precisely the block of
three gate tests at depths `j,j+1,j+2`.

## Nonlinear residual potentials force collapse

Write an arbitrary element of `S_H` as a Hamiltonian multiple and a
constant plus

\[
G=(\alpha q+\beta)Q+a q^2+bq.
\]

Its derivative, modulo the already included Hamiltonian multiple, is

\[
DG=-2\alpha H-2A(2aq+b)Q+
 \bigl(2\alpha V+(\alpha q+\beta)V'\bigr).                 \tag{QF11}
\]

It belongs to `S_H` exactly when the last parenthesis is quadratic in
`q`. If `n=deg V>=3`, its leading coefficient is
`alpha(n+2)V_n`, so `alpha=0`.

If `n>=4`, the remaining degree `n-1` coefficient is `beta nV_n`,
so `beta=0`. After one preimage step only `1,H,q,q^2` remain. Their
derivatives have `qQ,Q` coefficients `-4Aa,-2Ab`; the next preimage
step forces `a=b=0`. Equation (QF10) therefore gives depth four.

If `n=3`, one preimage step forces `alpha=0`. The next forces `a=0`,
since the `qQ` coefficient of (QF11) is `-4Aa`. The third forces
`beta=0`, since the `q^2` coefficient of (QF11) is `3 beta V_3`.
The fourth forces `b=0`, since its `Q` coefficient is `-2Ab`.
The successive dimensions are `6,5,4,3,2`; (QF10) gives depth six.
In either case only `1,H` remain. They always belong to the full core.

If `deg V<=2`, `S_H` is the quadratic polynomial sector in `(q,Q)`
and is invariant under `D`. It is killed by every odd gate: the third
by (QF7), all orders at least five because both `H` and every member
have original momentum degree at most two. Thus depth two already gives
the full six-dimensional core. This proves (QF1) and sufficiency in
(QF2).

## Sharp witnesses and exact failure formulas

For `deg V<=2`, the cubic `q^3` passes depths zero and one but

\[
C_3D^2q^3=-288A^3u''\ne0.                                \tag{QF12}
\]

For every potential, `q` passes depths zero through three and

\[
C_3D^4q=96A^4u''V''''.                                   \tag{QF13}
\]

This is nonzero exactly when `deg V>=4`, proving sharp depth four.
For cubic potentials, `q` passes depths zero through five and

\[
C_3D^6q=-960A^5u''(V''')^2\ne0.                           \tag{QF14}
\]

Thus depth six is necessary for every cubic residual potential, even
though the full core has dimension only two. These identities are in the
original flat Moyal structure; the transformed variables merely shorten
the polynomial calculation.

## Exact decision and independently replayable certificates

The closed classification already decides every input in scope. The code
also computes and certifies the answer by rational linear algebra inside
the proved six-dimensional upper space `S_H`. Start with that space
(which passes depths zero through two by QF9) and iterate

\[
K_{j+1}=\{G\in K_j:DG\in K_j\}.                            \tag{QF15}
\]

Every polynomial output is retained, including all terms outside `S_H`.
A strict step decreases dimension. At equality the space is `D` invariant
and killed by all gates, hence contained in the dynamic core. Conversely,
(QF9) places the full core in `S_H`, and invariance places it in every
stage. Thus the stabilized space equals the all-degree core.

The certificate records each stage basis, the original Hamiltonian,
recovered completion of square, final basis, exact derivation closure
matrix, and sharp depth. The checker independently recovers the initial
six-dimensional space, checks its three gate tests, and replays the rank
of `[D K_j | -K_j]` at every descent. Its nullity is the entire preimage
dimension. Membership and derivative membership are verified by augmented
ranks; the final closure identities certify the lower inclusion. The
checker uses the separate PBW engine and its own fraction elimination,
not the producer's Gaussian elimination. The universal upper bound rests
on (QF4)–(QF9), never numerical stabilization.

\clearpage

# Quadratic shears with nonlinear residual potentials: the remaining constant-quadratic stratum

Let `Q=p+u(q)`, `deg u=2`, and let

\[
H=AQ^2+V(q),\qquad A\ne0,
\qquad V\in K[q],\quad\deg V\ge3,
\]

over a characteristic-zero field, using the original flat Weyl–Moyal
product in `(q,p)`.

**Theorem QR.** The full polynomial dynamic core is

\[
\boxed{\mathcal D_\infty(H)=\operatorname{span}\{1,H\}.}     \tag{QR1}
\]

Only the third gate is needed, with the sharp depths

\[
\boxed{\mathcal D_\infty(H)=
\bigcap_{r=0}^{R}\ker(C_3D^r),\qquad
R=\begin{cases}6,&\deg V=3,\\4,&\deg V\ge4.\end{cases}}    \tag{QR2}
\]

These are all-degree results, not extrapolations from bounded polynomial
spaces. Together with QC and the oscillator theorem, QR completes every
constant-quadratic Hamiltonian `A p^2+B(q)p+C(q)` with `deg B=2`.
Together with QF, all such Hamiltonians with `deg B>=2` are classified.

## Residual degree at least four

In the independent polynomial variables `(q,Q)`, the exact operators are

\[
D=-2AQ\partial_q+V'\partial_Q,\qquad
C_3=V'''\partial_Q^3-6Au''\partial_q\partial_Q^2,            \tag{QR3}
\]

where `u''` is a nonzero constant. Suppose a polynomial `G` has top
`Q` term `g(q)Q^N`, with `N>=3`. The coefficient of `Q^(N-2)`
in `C3G=0` forces `g'=0`. Let `h(q)` be the coefficient of
`Q^(N-1)`. The next coefficient then gives

\[
h'=\frac{N V'''g}{6Au''}.
\]

The leading `Q^N` coefficient of `DG` is `-2Ah'`, which is nonzero.
The leading equation `C3DG=0` forces its derivative to vanish, giving
`V''''g=0`. This is impossible when `deg V>=4`. Thus the joint
kernel of `C3,C3D` has `Q` degree at most two. Its quadratic coefficient
is constant because `u''!=0`.

The depth-two kernel is the six-dimensional space `S_H` defined in (QF8).
The proof of (QF9) applies verbatim. Its two successive `D` preimages
remove first `qQ,Q` and then `q^2,q`, since `deg V>=4`.
This proves (QR1) and depth-four sufficiency in this stratum. The exact
identity

\[
C_3D^4q=96A^4u''V''''\ne0,
\qquad C_3D^rq=0\quad(0\le r\le3)                       \tag{QR4}
\]

proves sharpness.

## Cubic residual: rational normalization

Write `u=bq^2+cq+d`, `b!=0`, and
`V=vq^3+v_2q^2+v_1q+v_0`, `v!=0`. Translate
`q=x-v_2/(3v)` to remove the quadratic term of `V`, and use an affine
shear in `p` to remove the resulting linear and constant terms of `u`.
These are affine canonical transformations, so the flat Moyal gates are
covariant. Up to a constant the resulting Hamiltonian is

\[
A(p+bq^2)^2+vq^3+eq,
\qquad e=v_1-v_2^2/(3v).
\]

Now substitute `q=sx,p=ty`, with

\[
s=\frac{v}{Ab^2},\qquad t=bs^2,
\]

and divide the Hamiltonian by `At^2`. The normalized form is

\[
\boxed{H_\lambda=(p+q^2)^2+q^3+\lambda q,
\qquad \lambda=\frac{eA^2b^4}{v^3}.}                     \tag{QR5}
\]

All scales are nonzero elements of the coefficient field. The retained
`GL2` covariance of transvectants, together with nonzero Hamiltonian
rescaling and constant shifts, preserves every vanishing gate condition
and its bracket depth. Thus no algebraic extension or parameter exclusion
is hidden in this reduction.

In `(q,Q)` coordinates the normalized operators are

\[
D=-2Q\partial_q+(3q^2+\lambda)\partial_Q,
\qquad C_3=6\partial_Q^3-12\partial_q\partial_Q^2.           \tag{QR6}
\]

## An all-degree bound for the depth-two kernel

Give `q,Q` weights `1,2`, respectively. The top operators are

\[
D_0=-2Q\partial_q\quad(\text{shift }1),\qquad
C_0=-12\partial_q\partial_Q^2\quad(\text{shift }-5).
\]

Their joint kernel through depth two is

\[
K[Q]+\operatorname{span}\{q,qQ,q^2\}.                     \tag{QR7}
\]

Indeed, `C0 D0^r` sends each `q^aQ^c` to one monomial with coefficient
proportional to `(a)_(r+1)(c+r)_2`. At `r=0,1,2` these conditions leave
exactly the displayed monomials, and distinct inputs have distinct images
for each fixed `r`.

Consequently, a polynomial passing `C3D^r` for `r=0,1,2` and having
weighted degree greater than six would have top `c Q^N`, `N>=4`.
Normalize `c=1`. Let `G1` be its component of weight `2N-1`.
The gate component of weight `2N-6` is

\[
C_0G_1+6\partial_Q^3Q^N=0.
\]

Since `C0` is monomially injective on all monomials with positive
`q` degree and `Q` degree at least two, this forces

\[
G_1=\frac N2qQ^{N-1}+\beta q^{2N-1}+\gamma q^{2N-3}Q.      \tag{QR8}
\]

In particular, the correction `q^3Q^(N-2)` is forbidden when `N>=4`.
The term `lambda partial_Q` has shift `-2`, so it does not enter
this first-deficit calculation.

The top nonzero component of `DG` has weight `2N`, and is

\[
-NQ^N-2(2N-1)\beta q^{2N-2}Q
-2(2N-3)\gamma q^{2N-4}Q^2+3Nq^2Q^{N-1}.
\]

Applying `C0`, the final term contributes

\[
-72N(N-1)(N-2)qQ^{N-3}.
\]

It cannot cancel: the first two terms have zero gate, and the third
produces a monomial of `Q` degree zero, whereas `N-3>=1`.
This contradicts `C3DG=0`. Therefore the full depth-two kernel has
weight at most six, in all polynomial degrees.

The finite ambient space is consequently

\[
B_6=\operatorname{span}\{q^iQ^j:i+2j\le6\},\qquad\dim B_6=16.
                                                                    \tag{QR9}
\]

This is a proved bound. The exceptional cubic `N=3` is intentionally
retained and is handled by the exact finite certificate below.

## Exact parameter-polynomial rank certificate

Inside `B6`, form the full-output matrix of `C3D^r`, `r=0..6`.
Delete the columns `1,Q^2`; the remaining fourteen columns are

\[
\{q^iQ^j:i+2j\le6\}\setminus\{1,Q^2\}.
\]

Select the fourteen rows `(r,i,j)` recorded in the certificate:

\[
\begin{gathered}
(0,0,0),(0,1,0),(1,0,0),(1,1,0),(1,2,0),\\
(2,0,0),(2,1,0),(2,2,0),(2,3,0),\\
(3,0,0),(3,1,0),(4,0,0),(5,0,0),(6,0,0).
\end{gathered}
\]

Here `(i,j)` is the output monomial exponent pair in `(q,Q)`.
Their minor determinant is the nonzero constant polynomial

\[
-2489071056189074244411853807879968522240000000.           \tag{QR10}
\]

The independent standard-library checker verifies this as an **exact
polynomial identity**. Since `D=D_a+lambda partial_Q` and `C3` is
independent of `lambda`, every depth-`r` matrix entry has parameter
degree at most `r`. The determinant therefore has degree at most the
sum of its row depths, namely `32`. The checker recomputes the minor
and its exact rational determinant at the thirty-three distinct integers
`0..32`, obtaining the stated constant each time. A polynomial of degree
at most `32` with thirty-three roots is zero. This proves (QR10) for
every parameter, rather than inferring universality from sampled ranks.
All outputs are retained; none are projected into `B6`.

The full matrix therefore has rank at least fourteen for every `lambda`.
Its sixteen-dimensional domain contains the independent kernel vectors
`1,H_lambda`, so the rank is exactly fourteen and its kernel exactly
their span. Together with the proved bound (QR9), this establishes the
all-degree core and depth-six sufficiency.

## Sharp cubic depth and verification scope

For every cubic `V`, direct exact differentiation gives

\[
C_3D^rq=0\quad(0\le r\le5),\qquad
C_3D^6q=-960A^5u''(V''')^2\ne0.                           \tag{QR11}
\]

Thus depth six is necessary for every Hamiltonian in the cubic stratum,
including all lower coefficients. The code checks QR3 against the separate
original-coordinate PBW engine, and verifies QR4 and QR11 on eighteen
rational fixtures, including shifted shears, negative and rational
coefficients, general cubic potentials, and higher residual degrees.
It rejects corrupted minors, constants, parameter degree bounds, and
insufficient interpolation populations.

The theorem is about the fixed original flat Weyl product. It does not
claim arbitrary nonlinear covariance or historical priority. The finite
matrix is used only after an all-degree bound has been proved, and its
parameter universality is an exact bounded-degree polynomial identity.

\clearpage

# Affine shears with arbitrary polynomial potential

Use the fixed original flat Weyl product and the sign convention
`D={H,.}=H_q partial_p-H_p partial_q`. The coefficient field `K` has
characteristic zero. Put `C_3=T_3(H,.)` and let `R_r` be the joint
kernel of `C_3D^j`, `0<=j<=r`, on the full polynomial ring. No finite
observable degree is imposed in the statements below.

**Theorem AFP.** Let

\[
Q=p+u(q),\qquad \deg u\le1,\qquad
H=AQ^2+V(q),\qquad A\ne0,
\]

where a zero `u` is also allowed. If `deg V<=2`, the original
Hamiltonian is quadratic and its dynamic core is all of `K[q,p]`.
If `deg V=3`, then

\[
\boxed{\mathcal D_\infty(H)=R_7=\operatorname{span}_K\{1,H\}.}
                                                               \tag{AFP1}
\]

If `deg V>=4`, then

\[
\boxed{\mathcal D_\infty(H)=R_5=\operatorname{span}_K\{1,H\}.}
                                                               \tag{AFP2}
\]

The displayed third-gate stopping depths are sharp for every
Hamiltonian in their respective strata. This is a classification
within the stated affine-shear family; historical priority is not
established.

## Exact strip reduction

The affine symplectic substitution `(q,p)->(q,Q)` gives exactly

\[
D=-2AQ\partial_q+V'(q)\partial_Q,
\qquad C_3=V'''(q)\partial_Q^3.                         \tag{AFP3}
\]

The same identities also follow by direct differentiation in the
original variables. Suppose `deg V>=3`, so `V'''` is a nonzero
polynomial. Since `K[q,Q]` has no zero divisors, `C_3G=0` forces

\[
G=c(q)Q^2+b(q)Q+f(q).
\]

The next equations can be read successively from the cubic
coefficient in `Q`. First,

\[
C_3DG=-12A V'''c',
\]

so `c` is constant. Under this condition,

\[
C_3D^2G=24A^2 V'''b'',
\]

so `b` is affine. Under these two conditions,

\[
C_3D^3G=48A^2V'''(cV'''-Af''').                        \tag{AFP4}
\]

Therefore `f=(c/A)V+f_2`, where `deg f_2<=2`. Conversely each
polynomial of this form passes the four tests through depth three.
Thus the entire all-degree intermediate space is

\[
R_3=S=\operatorname{span}_K\{1,H,q,Q,q^2,qQ\}.          \tag{AFP5}
\]

This is an exact infinite-ring calculation, rather than a degree
bound inferred from a matrix.

## Exact invariant-preimage calculation

The nested kernels obey
`R_(r+1)={G in R_r : DG in R_r}`. Indeed, requiring `DG` to lie in
`R_r` adds precisely the equations at depths `1,...,r+1` to the
depth-zero equation. The required brackets on the nonstationary
generators of `S` are

\[
\begin{aligned}
Dq&=-2AQ,& DQ&=V',\\
Dq^2&=-4AqQ,& D(qQ)&=-2H+W(q),\qquad W=2V+qV'.
\end{aligned}                                               \tag{AFP6}
\]

The purely `q`-dependent polynomials in `S` are exactly
`span{1,q,q^2}`. A polynomial cannot use a nonzero multiple of `H`
to represent a pure `q` function, since that would leave a nonzero
`Q^2` coefficient.

If `n=deg V>=4`, then `deg W=n` and `deg V'=n-1>=3`.
Their leading degrees are distinct, so no nontrivial linear
combination of `W` and `V'` can lie in `span{1,q,q^2}`. Equation
(AFP6) therefore gives

\[
R_4=\operatorname{span}\{1,H,q,q^2\},\qquad
R_5=\operatorname{span}\{1,H\}.                         \tag{AFP7}
\]

In the second step the independent outputs `Q` and `qQ` exclude
`q` and `q^2` respectively.

If `n=3`, `W` has degree three while `V'` is a genuine quadratic.
The successive exact spaces are instead

\[
\begin{aligned}
R_4&=\operatorname{span}\{1,H,q,Q,q^2\},\\
R_5&=\operatorname{span}\{1,H,q,Q\},\\
R_6&=\operatorname{span}\{1,H,q\},\\
R_7&=\operatorname{span}\{1,H\}.
\end{aligned}                                               \tag{AFP8}
\]

The first step excludes `qQ` by its uncancellable cubic output.
The next excludes `q^2` by its `qQ` output, then `Q` by its
quadratic output, then `q` by its `Q` output. The surviving span
is stationary and every odd gate kills it by antisymmetry.
Consequently it is exactly the full dynamic core, proving
(AFP1)--(AFP2). Higher gates are not needed for either stopping
rule.

## Uniform sharpness

For `deg V>=4`, direct iteration gives

\[
C_3D^jq=0\quad(0\le j<5),\qquad
C_3D^5q=96A^4 V'''V''''\ne0.                           \tag{AFP9}
\]

The first four iterates have `Q` degree at most two; the cubic
coefficient in the fifth is `16A^4 V''''`. Both derivatives in
(AFP9) are nonzero polynomials, so their product is nonzero.

For a cubic potential, write `k=V'''`, a nonzero constant. The
same witness survives two more steps:

\[
C_3D^jq=0\quad(0\le j<7),\qquad
C_3D^7q=-960A^5k^3\ne0.                                \tag{AFP10}
\]

For clarity, the fifth iterate is
`-8A^3[(V'')^2+3kV']Q`; the sixth has quadratic coefficient
`80A^4 k V''`; the seventh therefore has cubic coefficient
`-160A^5 k^2`. Applying `C_3=k partial_Q^3` proves the constant
in (AFP10). Thus the claimed stopping depths are necessary for
every allowed potential, including arbitrary lower coefficients.

## Recognition and replay

For an input polynomial `H=A p^2+B(q)p+C(q)` with constant
`A!=0`, completing the square uniquely gives
`u=B/(2A)` and `V=C-Au^2`. The AFP recognizer succeeds precisely
when `deg u<=1`. It then returns the entire ring when `deg V<=2`,
or `span{1,H}` with sharp depth seven or five in the two higher
strata. Inputs outside the route return no classification.

`affine_shear_potentials.py` checks original-coordinate operators,
all conditional strip identities, the all-parameter witness
constants, exact intermediate kernel dimensions, and recognition
boundaries using standard-library rational arithmetic. Finite
matrices retain every output coordinate; the proof above establishes
the claims in all polynomial degrees. The replay receipt is
`affine_shear_potentials_results.json`.

\clearpage

# Deformation obstructions and a genuine torsion module of exact observables

This note supplies an obstruction theory with an explicit all-degree
calibration. It uses the fixed original flat Weyl product. It does not
define a new Nijenhuis or Haantjes tensor. The cokernel and Smith module
below are ordinary algebraic constructions; their application to lifting
exact Hamiltonian sectors is the claim being developed here. Historical
priority is not established.

## Finite stopping operators and lifting classes

Let `P` be an observable vector space over a characteristic-zero field
`K`, let `t` be a formal parameter, and let `H_t` be a family. Suppose a
proved finite stopping rule identifies exact persistence in this family
with the kernel of

\[
 L_t:P[[t]]\longrightarrow Y[[t]],\qquad
 L_t=\sum_{i\ge0}t^iL_i.                                      \tag{DO1}
\]

The target `Y` is a finite direct sum of full polynomial output spaces,
one for each retained gate and Hamiltonian depth. Outputs are not
projected into the candidate input space. If the stopping theorem is
only known over `K(t)`, its extension to `P[[t]]` must be justified; it
must not be inferred merely from pointwise numerical stabilization.

Given `G_0,...,G_(n-1)` with `L_t sum_(j<n)t^jG_j=0 mod t^n`, put

\[
 b_n=-\sum_{i=1}^nL_iG_{n-i},\qquad
 \operatorname{ob}_n=[b_n]\in\operatorname{coker}L_0.             \tag{DO2}
\]

The jet extends through order `n` exactly when `ob_n=0`: its only new
equation is `L_0G_n=b_n`. A solution `G_n` is a primitive for this
linear equation; a functional `ell` with `ell L_0=0` and `ell(b_n)!=0`
is an independently checkable obstruction. At orders above one the
class is generally relative to the preceding jet. Independence from
lower-jet choices requires a separate argument, supplied below in the
calibration. No differential with square zero is asserted or needed.

The construction has an elementary naturality law. Under invertible
formal source and target changes `T_t,S_t`, replace
`L_t` by `L'_t=S_tL_tT_t^(-1)` and the lower jet by the corresponding
jet of `T_tG_t`. Then `ob_n` maps to `S_0 ob_n` in the naturally
identified cokernel. Indeed, multiplying a residual starting in order
`n` by `S_t` changes its leading coefficient by `S_0`; truncating the
transformed source jet changes that coefficient only by `L'_0` of a
source correction. Thus solvability and a nonzero obstruction are
independent of bases. Affine symplectic coordinate changes in the
original flat Weyl convention are admissible source/output changes.
Arbitrary nonlinear substitutions with the flat product retained are
not automatically admissible.

In a finite polynomial parameter problem, `L_t` becomes a matrix over
`K[t]`. Its cokernel can have actual module torsion. Smith factors then
measure delayed formal lifting failure. This is stronger than recording
only the dimension of a specialized kernel. A finite input restriction
alone never establishes an all-degree obstruction; the coefficient
functionals in the next theorem do.

## A complete lifting theorem at the quartic oscillator boundary

Put

\[
 Q=p+q^2,\qquad H_t=Q^2+\frac t2q^2,
 \qquad V=\operatorname{span}_K\{1,q,Q,q^2,qQ,Q^2\}.             \tag{DO3}
\]

Here the letter `V` denotes the six-dimensional observable space, not
an additive potential. In the polynomial coordinate ring `K[q,Q]`,

\[
 D_t=-2Q\partial_q+tq\partial_Q=D_0+tD_1,
 \qquad C_3=-12\partial_q\partial_Q^2=:C.                      \tag{DO4}
\]

These are exact rewritings of the original-coordinate operators, not a
replacement of the original flat Moyal product. The Hamiltonian has
degree four in `(q,p)`, so all odd gates above `C3` vanish identically.
Use

\[
 L_tG=(CG,CD_tG,CD_t^2G,CD_t^3G).                             \tag{DO5}
\]

For this family the oscillator theorem gives a uniform depth-three
stopping rule. At `t=0` the sharper depth-two rule follows directly
from the monomial computation below. The proof here also establishes
the lifting assertions without assuming a formal extension of a
pointwise stopping theorem: necessity uses only (DO5), first-order
sufficiency uses the explicit derivative identity in (DO9), and every
surviving second-order initial element has a constant exact lift in `V`.

**Theorem DO.** At `t=0`,

\[
 \mathcal D_\infty(H_0)=K[Q]+\operatorname{span}_K\{q,qQ,q^2\}.
                                                                    \tag{DO6}
\]

Consider any `G_0` in this initial core. Corrections at each order are
allowed to be arbitrary polynomials, with no common degree bound.

* A first-order exact jet `G_0+tG_1` exists precisely when
  `G_0 in V+KQ^3`, a seven-dimensional space.
* A second-order exact jet `G_0+tG_1+t^2G_2` exists precisely when
  `G_0 in V`.
* A full formal exact lift exists precisely when `G_0 in V`; a constant
  lift already works there.

The extra cubic passes the first lifting step but has a choice-independent
second-order obstruction. The homogeneous cubic gate matrix has Smith
invariant factors `1,1,1,t^2`, so its cokernel is `K[t]/(t^2)`.

### Initial core and the protected exact lifts

For every monomial,

\[
 CD_0^r(q^aQ^c)
 =-12(-2)^r(a)_r(a-r)(c+r)_2
      q^{a-r-1}Q^{c+r-2}.                                  \tag{DO7}
\]

A term with a zero coefficient is omitted before interpreting its
exponents. For fixed `r`, nonzero monomial images are distinct.
The simultaneous kernel for `r=0,1,2` is exactly (DO6): `a=0` permits
every `Q^c`; with `a>0`, the only survivors are `q,qQ,q^2`.
This proves (DO6) directly, including all input degrees. Each polynomial
in `V` has total degree at most two in `(q,Q)`, is killed by `C`, and
`D_t` preserves that total degree. Therefore `V` consists of exact
observables for every `t` and supplies constant formal lifts.

### First-order obstructions in every higher tower degree

It suffices to start with `G_0=f(Q)`, since the remaining protected
directions have constant lifts. The static first-order condition is
`CG_1=0`, whence

\[
 G_1=a(q)+Qb(q)+g(Q).
\]

The coefficient of `t` in `CD_t(G_0+tG_1)` is

\[
 48b''(q)-12f'''(Q).                                      \tag{DO8}
\]

This vanishes only when `f'''` is constant. Thus `deg f<=3`, without
any degree restriction on the correction `G_1`. Conversely, the cubic
has the first-order lift

\[
 \widehat G_t=Q^3+\frac34tq^2Q,
 \qquad D_t\widehat G_t=\frac34t^2q^3,
 \qquad L_t\widehat G_t=(0,0,0,-432t^2).                    \tag{DO9}
\]

The derivative identity proves that every further iterate has order
at least two in `t`, so this is a first-order jet for the complete
dynamic-core definition, not just for the four retained tests. This
proves the seven-dimensional first-order statement. For an
explicit dual certificate, if `n>=4` define on four polynomial outputs

\[
 \ell_n(y)= [Q^{n-3}]y_1+
       \frac{2(n-1)}{n-3}[qQ^{n-4}]y_0.                   \tag{DO10}
\]

For every polynomial `X`, `ell_n(L_0X)=0`. Only the input monomial
`q^2Q^(n-2)` can contribute to either extracted coefficient; its two
coefficients are `48(n-1)(n-2)` and `-24(n-2)(n-3)`, which cancel.
For the first-order target of `Q^n`, however,

\[
 \ell_n(-L_1Q^n)=12n(n-1)(n-2)\ne0.                      \tag{DO11}
\]

The functional is valid on the entire polynomial output space. It is
not a certificate derived from a truncated kernel search.

### The cubic fails at second order, independently of the first lift

Every first correction to `Q^3` is
`G_1=(3/4)q^2Q+Z`, where `Z in ker L_0`, hence `Z` lies in (DO6).
The coefficient of `t` in `CD_t^3Z` is zero for every such `Z`.
It vanishes on `V` because all of `V` is protected. For `Z=f(Q)`, the
only potentially nonzero term is `CD_0^2D_1f`, and
`D_0^2(qf')=0`. This proves independence from the first-lift choice.

By (DO9), the third-depth output has residual `-432t^2`. On the other
hand `CD_0^3X` is divisible by `Q` for every polynomial `X`: applying
`D_0^3` introduces `Q^3`, and `C` removes at most two `Q` factors.
Consequently constant-coefficient extraction in the third-depth
output annihilates `L_0X`, but evaluates the residual to `-432`.
No polynomial second correction can remove it. Multiplying by the
initial cubic coefficient proves the second-order assertion for all
initial observables. The protected constant lifts then prove the full
formal statement.

### An exact Smith certificate for the delayed cubic obstruction

On homogeneous cubics, the full output at each depth is a constant in
`q,Q`; thus no output is discarded. In the source basis
`(q^3,q^2Q,qQ^2,Q^3)`, (DO5) is

\[
 M(t)=\begin{pmatrix}
 0&0&-24&0\\
 0&96&0&-72t\\
 -576&0&336t&0\\
 0&-1920t&0&1008t^2
 \end{pmatrix}.                                          \tag{DO12}
\]

Let `x=(x_a,x_b,x_c,x_d)` be source coordinates and let `y=Mx`.
Invertible polynomial target operations give

\[
 \left(-\frac{y_0}{24},
 -\frac{y_2+14ty_0}{576},
 \frac{y_1}{96},
 -\frac{y_3+20ty_1}{432}\right)
 =\left(x_c,x_a,x_b-\frac34tx_d,t^2x_d\right).             \tag{DO13}
\]

The source change `(x_c,x_a,x_b-(3/4)tx_d,x_d)` is also invertible over
`K[t]`. Hence (DO13) is the Smith form `diag(1,1,1,t^2)`. The checker
stores both transformation matrices and both polynomial inverses,
then replays all matrix products and recomputes `M` from the gate
operators. It also rejects an edited matrix. The literal module
torsion records the two-stage failure of the extra cubic; it is not a
claim that the existing notion of algebraic torsion is new.

## The entire graded torsion module

The cubic is the only degree with a delayed second-order obstruction.
The observation map also gives a complete infinite graded module
classification. Let `P_n=K[q,Q]_n` be the homogeneous degree-`n` space.
For `n>=3`, use the explicitly declared presentation

\[
 M_n(t):K[t]\otimes P_n\longrightarrow
       \big(K[t]\otimes P_{n-3}\big)^4,
 \qquad G\longmapsto (CG,CD_tG,CD_t^2G,CD_t^3G).             \tag{DO14}
\]

Each target summand retains every monomial of output degree `n-3`.
The target is assigned grade `n`; this compensates for the operator's
degree shift. Source degrees at most two have zero target and do not
contribute to the cokernel under this convention.

**Corollary GT.** Over any characteristic-zero field `K`,

\[
 \operatorname{coker}M_3\cong K[t]/(t^2),\qquad
 \operatorname{coker}M_n\cong
 K[t]^{3n-9}\oplus K[t]/(t)\quad(n\ge4).                    \tag{DO15}
\]

Consequently, for the graded direct-sum map in (DO14),

\[
 \boxed{\operatorname{Tor}_{K[t]}\operatorname{coker}L
  \cong \big(K[t]/(t^2)\big)_{\mathrm{grade}\ 3}
       \oplus\bigoplus_{n\ge4}
                 \big(K[t]/(t)\big)_{\mathrm{grade}\ n}.}    \tag{DO16}
\]

**Proof.** The cubic case is the explicit Smith certificate. For
`n>=4`, (DO7) shows `ker M_n(0)=KQ^n`, so the rank at zero is `n`.
For any nonzero scalar `t`, including over an algebraic closure, the
static kernel in degree `n` has basis
`q^n,q^(n-1)Q,Q^n`. The next gate sends the latter two elements to

\[
 CD_t(q^{n-1}Q)=48(n-1)(n-2)q^{n-3},\qquad
 CD_t(Q^n)=-12tn(n-1)(n-2)Q^{n-3}.                           \tag{DO17}
\]

Their outputs are independent because `n>=4`. Their coefficients
must therefore vanish. The remaining direction is removed by

\[
 CD_t^2(q^n)=-96n(n-1)(n-2)q^{n-3}\ne0.                    \tag{DO18}
\]

Thus `M_n(t)` has full column rank `n+1` at every nonzero parameter.
Smith normal form over the PID `K[t]` exists. Every nonunit invariant
factor can have roots only at zero, since any other root over the
algebraic closure would produce a rank drop there. The rank drop at
zero is exactly one, hence the invariant factors consist of `n`
units and a single `t^e`, up to units, with `e>=1`.

If `e>=2`, the Smith source change would give a polynomial first-order
lift of a nonzero vector spanning `ker M_n(0)=KQ^n`: choose the last
Smith coordinate constant and the unit coordinates zero. Its residual
would be divisible by `t^2`. But (DO10)--(DO11) exclude such a lift.
Therefore `e=1`. The free cokernel rank is the number of target rows
minus columns, `4(n-2)-(n+1)=3n-9`. This proves (DO15) and taking the
graded direct sum proves (DO16).

This is a classification of ordinary algebraic torsion for the
specified finite-depth observation presentation. Its free summands
depend on the declared target. Invertible source and target changes
preserve its Smith factors; no invariance under undeclared changes
of the gate presentation or nonlinear flat-product substitution is
asserted. The all-degree lifting theorem above is independent of a
candidate degree cutoff and independently confirms the two distinct
obstruction orders represented in (DO16).

## Verification and boundary

Run `python3 -B research/core_overlap/deformation_obstructions.py`.
The checker uses exact standard-library rational polynomial arithmetic
in `(q,Q,t)`, checks the Smith certificates without elimination, verifies
the universal-order symbolic identities and finite calibrations, and
compares 400 original-chart gate/iterate calculations using the separate
sparse transvectant engine. All polynomial outputs are retained.
In degrees four through nine it constructs and replays rectangular
Smith certificates with polynomial inverses; complete certificates for
degrees four and six are retained in the receipt. The proof above,
rather than these finitely many matrices, establishes (DO16).

The proof establishes the all-degree assertions. Neither the finite
calibrations nor the cubic Smith matrix alone proves absence of
higher-degree corrections; that follows from (DO8), (DO10), and the
divisibility argument. The construction concerns formal exact
observables, not convergence of a formal lift, Hilbert-space operator
domains, or a new geometric tensor.

\clearpage

# Exact observable closure inside the six-dimensional shear-square core

Take Theorem SS with `Q=p+u(q)`, `deg(u)>=3`, and

\[
H=AQ^2+BQ+C+\varepsilon q,\qquad A\ne0.
\]

Its exact sector has the ordered basis
`(1,q,Q,q^2,qQ,Q^2)`. This supplies a direct bridge to Claude's finite
target-observer closure machinery: repeated Hamiltonian derivatives of any
target in the sector become an exact finite rational matrix problem. No
truncation of the ambient polynomial algebra is required.

With coefficient vectors written as columns, the matrix of `D={H,.}` is

\[
M=\begin{pmatrix}
0&-B&\varepsilon&0&0&0\\
0&0&0&-2B&\varepsilon&0\\
0&-2A&0&0&-B&2\varepsilon\\
0&0&0&0&0&0\\
0&0&0&-4A&0&0\\
0&0&0&0&-2A&0
\end{pmatrix}.
\]

In particular `Dq=-(2AQ+B)` and `DQ=epsilon`. The exact flows in the
Hamiltonian-time convention `exp(tD)` are

\[
Q(t)=Q+\varepsilon t,\qquad
q(t)=q-(2AQ+B)t-A\varepsilon t^2.
\]

Every basis observable follows by substituting these two expressions; for
example `q^2(t)=q(t)^2`. The original classical momentum coordinate is
`p(t)=Q(t)-u(q(t))`; this nonlinear reconstructed observable generally lies
outside the exact sector, so it is not asserted to be its flat-Moyal symbol.
The time convention here is the compendium's observable
derivation convention; changing the sign of that convention reverses time.

## Nilpotency and the role of a constant force

For `epsilon=0`, `D^3=0` on the sector and the ranks of `D,D^2,D^3` are
`3,1,0`. Its Jordan block sizes are `3,2,1`. Indeed `D=-(2AQ+B)partial_q`
on quadratic polynomials in `(q,Q)`, so its kernel has dimension three and
the image of its square has dimension one.

For `epsilon!=0`, the ranks of `D,D^2,D^3,D^4,D^5` are `4,3,2,1,0`; the
Jordan block sizes are `5,1`. The displayed flow shows `D^5=0`, and

\[
D^4q^2=24A^2\varepsilon^2\ne0.
\]

Thus there is a size-five block, and the remaining one dimension is a
stationary block. A constant force changes the organization of the exact
sector without changing its dimension.

\Needspace{14\baselineskip}

## Minimal derivative closures for targets

The span generated by a target and all its repeated derivatives is its
Krylov closure. For all parameter choices in the theorem,

| Target family | epsilon=0 | epsilon nonzero |
|---|---:|---:|
| `q` | 2 | 3 |
| `q^2` | 3 | 5 |
| `q` and `q^2` together | 5 | 6 |

To see the last row explicitly, let `L=2AQ+B`. For zero force the joint
closure is `span{q,L,q^2,qL,L^2}`. For nonzero force the `q^2` chain spans
`q^2,qL,L^2-2A epsilon q,L,1`; adjoining the `q` target fills the sixth
dimension. These are minimal closure dimensions, not a claim about every
possible sensing model or noisy measurement design.

`audit_sector_dynamics.py` checks the matrix, closed forms, ranks and target
dimensions exactly. It also feeds the transposed matrix into the retained
observer compiler and replays
its independent `observer-closure-v1` certificate checker. Transposition is
essential: that backend acts on target rows and the state consists of basis
observable values. This is an application of the existing closure machinery,
with no external-priority claim.

\clearpage

# Nonlinear shear compositions: a complete exact-core phase diagram

Use the fixed flat Weyl convention
`D_H={H,.}=H_q partial_p-H_p partial_q`. Work over any field of characteristic
zero. Put

\[
J=qp+u(q),\qquad u\in K[q],\quad u'''\ne0,\qquad H=P(J),
\quad \deg P=\mu\ge1.
\]

Then the entire polynomial dynamic exact core is

\[
\boxed{
D_\infty(P(J))=
\begin{cases}
K[q]\oplus pK[q]\oplus p^2K[q],&\mu=1,\\
\operatorname{span}_K\{1,J,J^2\},&\mu=2,\\
\operatorname{span}_K\{1,H\},&\mu\ge3.
\end{cases}}
\]

The last two sectors are stationary. The total homogeneous top of `H` is a
pure power of `q`, of degree `mu deg(u)`. Its transverse, or `p`-degree, top
is a balanced power `(qp)^mu`. Thus these are the balanced **transverse**
exceptions in §6.6 of Claude commit `e91e14d`, not counterexamples to its
balanced **total-top** theorem B.

For example,

\[
J=qp+q^3,\quad H=J^2,
\qquad D_\infty(H)=\operatorname{span}\{1,J,H\}.
\]

This is a second counterexample to P003. It is stationary, unlike the active
unequal-transverse family in `pure_perfect_power.md`. It also shows why
nonlinear canonical covariance cannot be assumed: a quadratic Hamiltonian
in `J` retains only a quadratic stationary sector, while
`T3(J^2,J^3)=72q^3J` is nonzero.

## A closed composition identity

For arbitrary univariate polynomials `F` and `G`, direct differentiation gives

\[
\boxed{
T_3(F(J),G(J))
=q^3u'''(q)\bigl(F'(J)G'''(J)-F'''(J)G'(J)\bigr).
}
\]

Here no nonlinear covariance is being used. To verify the identity, put
`A=p+u'`, `B=q`, `C=u''`, `E=u'''`. The four third derivatives of `F(J)` are

\[
\begin{aligned}
F(J)_{qqq}&=F'''A^3+3F''AC+F'E,\\
F(J)_{qqp}&=F'''A^2B+F''(CB+2A),\\
F(J)_{qpp}&=F'''AB^2+2F''B,\\
F(J)_{ppp}&=F'''B^3.
\end{aligned}
\]

Insert these and their `G` counterparts into the alternating third
transvectant. All terms cancel except `B^3E(F'G'''-F'''G')`.
In particular,

\[
T_3(J^\mu,J^s)
=\mu s(s-\mu)(s+\mu-3)q^3u'''J^{\mu+s-4},
\]

whenever the exponent on `J` is nonnegative; the remaining low-index cases
vanish directly. For nonzero `u'''`, this formula already bounds the static
exact powers of `J`. The next argument proves that arbitrary polynomial core
elements, including those not assumed to be functions of `J`, obey the same
finite bound.

## Proof for mu at least two

Multiplying `H` by a nonzero scalar or adding a constant does not change the
core. Write its leading coefficient as one, and set

\[
P(z)=z^\mu+bz^{\mu-1}+\cdots,\qquad
v(q)=u(q)+\frac b\mu,\qquad Q=qp.
\]

The first two pieces in decreasing `p`-degree are

\[
H_0=Q^\mu,\qquad
H_1=\mu v(q)Q^{\mu-1}.
\]

The transverse top of any core element belongs to the core of `Q^mu`.
By the monomial theorem, that core is `K[Q]`. Therefore a nonconstant core
element of transverse degree `s` can be normalized to have the first pieces

\[
A_0=Q^s,\qquad A_1=f(q)p^{s-1},\qquad s\ge1.
\]

At transverse degree zero the core contains only constants.

**One bracket determines the first correction.** The top term of
`{H,A}` vanishes since `{Q^mu,Q^s}=0`. Its coefficient at the next possible
`p`-degree, `mu+s-2`, is

\[
\mu q^{\mu-1}\bigl((s-1)f-qf'+s q^s v'\bigr).
\]

The bracket is again a core element. Hence this coefficient, if nonzero,
must be a multiple of `q^(mu+s-2)`. After dividing by `mu q^(mu-1)`, the
right-hand side must be a multiple of `q^(s-1)`. But the Euler operator
`f -> (s-1)f-qf'` has zero coefficient at that very monomial, and
`q^s v'` also has zero coefficient there. The putative multiple is therefore
zero. Solving the resulting polynomial Euler equation gives exactly

\[
f=sq^{s-1}v+cq^{s-1},\qquad c\in K.
\]

This argument does not require a degree bound for `f` or `u`.

**The first gate bounds the transverse degree.** The leading `p`-degree
piece of `T3(H,A)` vanishes for two powers of `Q`. At the next possible
degree, `mu+s-4`, only the pairs `(H_0,A_1)` and `(H_1,A_0)` contribute.
The diagonal summand `cQ^(s-1)` gives zero. Direct falling-factorial expansion
of the two remaining terms gives

\[
\boxed{
[p^{\mu+s-4}]\,T_3(H,A)
=\mu s(s-\mu)(s+\mu-3)q^{\mu+s-1}u'''(q).
}
\]

To check the identity for arbitrary `v`, it suffices by linearity to take
`v=q^n`. The coefficient on the left becomes

\[
s\,T_3[(\mu,\mu);(s-1+n,s-1)]
+\mu\,T_3[(\mu-1+n,\mu-1);(s,s)]
=\mu s(s-\mu)(s+\mu-3)n(n-1)(n-2).
\]

Here `T3[(a,b);(c,d)]` means the scalar multiplying
`q^(a+c-3)p^(b+d-3)` for the two monomials. The symbolic identity is verified
independently by `audit_balanced_transverse.py` using a polynomial ring in
the three integer parameters. The exceptional index `mu=2,s=1` has formal
output degree `-1`; the scalar is identically zero and no nonexistent
polynomial output is used in the argument.

Since `u'''` is nonzero, when `mu=2` the only allowed positive values of `s`
are `1,2`. The transverse associated graded core has at most one dimension
at each allowed degree `0,1,2`; therefore the entire core has dimension at
most three. Both `J` and `J^2=H` survive. Indeed every derivative of `J`
of order at least three is in `q` only, whereas `H` has `p`-degree two, so
all odd gates kill `J`; antisymmetry kills `H`; their Poisson bracket is
zero. This proves the quadratic case.

When `mu>=3`, the factor `s+mu-3` is positive for every integer `s>=1`.
The only allowed positive degree is `s=mu`. The same filtration argument
bounds the core by two dimensions, and `1,H` attain that bound. This proves
the remaining case.

## Linear compositions

For `H=aJ+b`, `a!=0`, the third gate is
`T3(H,.)=-a u''' partial_p^3`. Its polynomial kernel consists exactly of the
polynomials of `p`-degree at most two. Every higher odd gate kills this
space, and

\[
D_H=a\bigl((p+u')\partial_p-q\partial_q\bigr)
\]

preserves it. Thus the static and dynamic exact spaces coincide and equal
the stated strip.

If `u'''=0`, this phase diagram does not apply: `J` is quadratic. For
`mu>=2`, Theorem B gives the full stationary tower `K[J]`; for `mu=1`, all
polynomials are exact. The condition `u'''!=0` therefore identifies a real
change in exact observable sectors.

## Scope of the result

The proof is all-degree and applies to every coefficient choice satisfying
the hypotheses. Numerical degree cutoffs are not used. The nonlinear
substitution `p -> p+u(q)/q`, after removing `u(0)`, motivates the family
classically; every assertion about Weyl exactness is proved in the original
flat canonical coordinates. No historical-priority claim is made.

\clearpage

# Three equations determine the analytic dynamic core

This is a finite-determination bridge between the polynomial dynamic-core
programme on `claude/adoring-ritchie-1hq1kw` and the analytic polygamma
calculations. It concerns the existing flat Weyl–Moyal gates, not a new
torsion operation or a literature-priority claim.

Let `I` be a connected open real interval, let
`A=C^omega(I,R)`, and suppose `F in A` has `F''` nowhere zero. Work in
`A[q]`, with finite degree in `q`. Write

\[
 H=qF(p),\qquad D=\{H,\cdot\},\qquad C_j=T_j(H,\cdot),
\]

with the compendium's affine canonical coordinates and transvectant
convention. The Hamiltonian derivation is
`D(q^c g)=q^c(Fg'-cF'g)`.

**Theorem FD.** The full dynamic core is determined by three equations:

\[
 \boxed{\mathcal D_\infty(qF)
   =\ker C_3\;\cap\;\ker(C_3D)\;\cap\;\ker C_5.}       \tag{FD1}
\]

Thus no gate above fifth order, and no Hamiltonian iterate above the
first, is needed to certify membership. This is an equality in all
finite `q` degrees, not a degree cutoff or a numerical stabilization
criterion. The three equations are individually indispensable across
this class of Hamiltonians.

In particular, with `r=cuberoot(F'')` and

\[
 K_3=\frac{FF'''}{3F''}-3F',
\]

the answer is

\[
 \mathcal D_\infty(qF)=
 \begin{cases}
 A\oplus qA\oplus\mathbb Rq^3r,&K_3\text{ constant},\\
 A\oplus qA,&K_3\text{ nonconstant}.
 \end{cases}                                               \tag{FD2}
\]

The constant case permits an active cubic eigenpartner. The theorem
does not replace the analytic hypotheses by arbitrary smoothness, nor
classify infinite `q` series.

**Analytic continuation extension.** The three-equation equality (FD1)
holds for every real-analytic `F` on a connected interval, including
zeros of `F''`. If `F''` vanishes identically, `H` is quadratic and
both sides are all of `A[q]`. Otherwise choose any open subinterval
where `F''` is nonzero. The proof below excludes every degree other
than zero, one and three on that subinterval, hence everywhere by
analyticity. A surviving cubic is a local eigenvector of `D`; its
analytic identity `DG=lambda*G` extends to the whole interval, and all
higher gates kill it by `q` degree. This proves the equality without
dividing by `F''` at a zero.

For the explicit formula (FD2) across those zeros, a nonzero cubic
coefficient must be a global analytic cube root of a constant multiple
of `F''`, and must obey the eigenvector identity. Such a cube root
exists exactly when every zero of `F''` has multiplicity divisible by
three. Thus the three-equation test is global, while a local cubic
formula may fail to extend through a zero.

## Proof by independent degree sectors

For odd `j`, direct expansion gives

\[
 C_j(q^c g)=(c)_{j-1}q^{c-j+1}
 \left[jF^{(j-1)}g'-(c-j+1)F^{(j)}g\right].             \tag{FD3}
\]

At fixed `j`, different input `q` degrees have different output degrees.
The derivation `D` also preserves each degree. Therefore all three
equations in (FD1) split by `q` degree.

Degrees zero and one are unrestricted, killed by every gate, and
preserved by `D`. For `c>=2`, `C_3(q^c g)=0` is

\[
 3F''g'-(c-2)F'''g=0.
\]

Put `B=|F''|>0`, `delta=sign(F'')`, and
`alpha=(c-2)/3`. A nonzero solution is `g=constant*B^alpha`,
and it never vanishes. Then

\[
 D(q^cg)=q^cgK_c,\qquad
 K_c=\alpha\frac{FB'}B-cF'.                              \tag{FD4}
\]

The equation `C_3D(q^c g)=0` is exactly `K_c'=0`. If all gates
kill this generator, a constant `K_c` makes it an eigenvector of `D`
and automatically proves persistence under every iterate.

At degree two, `K_2=-2F'` is not constant. At degree three, there
are no gates above `C_3`, so precisely the constant-`K_3` possibility
survives. It remains to exclude every `c>=4` using `C_5`.

For `c=4`, fifth order gives `B'B''=0`. Analyticity on the connected
interval implies `B''=0`, so `F` has degree at most three. For any
`c>=4` the latter case is impossible under constant `K_c`: if `F`
is quadratic then `K_c=-cF'` has nonzero derivative, and if
`F=f_3p^3+...` then its rational expression has leading term
`-(8c+2)f_3p^2/3`, which is not constant. An identity on the interval
would be a rational identity, so this leading-term argument applies
even on bounded intervals away from the zero of `F''`.

For `c>=5`, fifth order gives

\[
 BB'''=\beta B'B'',\qquad
 \beta=\frac{5(c-2)}{3(c-4)}>1.
\]

Hence `B''=kappa*B^beta` for a constant `kappa`. If `kappa=0`,
the polynomial case above concludes. Suppose `kappa!=0`. A constant
`K_c` would give

\[
 FB'-aF'B=kB,\qquad a=\frac{3c}{c-2}>0                 \tag{FD5}
\]

for some real `k`. Apply the following incompatibility lemma, using

\[
 1+a(\beta-2)=\frac{8(c+1)}{(c-4)(c-2)}>0.               \tag{FD6}
\]

This excludes every higher degree and proves (FD1) and (FD2).

## Scalar incompatibility lemma

Suppose `B>0`, `F''=delta*B`, `delta in {1,-1}`,
`B''=kappa*B^beta`, `kappa!=0`, `beta>1`, `a>0`, and
`1+a(beta-2)!=0`. Then `FB'/B-aF'` is not constant.

Write `u=B'`, `v=B''`, `w=F'`. If the expression equalled `k`,
then

\[
 Fu-awB=kB.
\]

Differentiate twice, use `v'=beta*vu/B` and `w'=delta*B`,
and eliminate `F`. The exact result is

\[
 Lwv=(3a-1)\delta Bu-(\beta-1)kv,
 \qquad L=a(\beta-1)+2>0.                               \tag{FD7}
\]

Since `v` is nowhere zero, solve this for `w` and differentiate. Using
`w'=delta*B` gives

\[
 [a(\beta-4)+3]Bv=(3a-1)(1-\beta)u^2.                   \tag{FD8}
\]

There is an open subinterval with `u!=0`, since `v` never vanishes.
Differentiate (FD8) there, cancel the nonzero `uv`, and obtain

\[
 (\beta+1)[a(\beta-4)+3]
   =2(3a-1)(1-\beta).
\]

Their difference factors as

\[
 (\beta+5)[1+a(\beta-2)]=0,
\]

contrary to the hypotheses. The argument makes no division by `u`
at a zero, by `F`, by a first-integral constant, or by either factor
in (FD8).

## Sharpness and the distinction from static gate determination

The examples below are on `p>0`, and every power is its positive real
analytic branch.

**The first-step condition is necessary.** For `F=p^2`, `G=q^2`
passes every static gate, while

\[
 C_3DG=-48.
\]

**The fifth-order condition is necessary even after arbitrarily many
third-order tests.** Take `F=p^{-2/5}` and `G=H^4=q^4p^{-8/5}`.
Then `DG=0` and `C_3G=0`, but

\[
 C_5G=-\frac{548352}{625}p^{-7}\ne0.
\]

Thus testing `C_3D^jG=0` for every `j>=0` still does not determine
the true dynamic core.

**The initial third-order condition is necessary.** For `F=p^2`
and `G=H^2=q^2p^4`, the equation `DG=0` makes `C_3DG=0`, and
`C_5G=0`, whereas

\[
 C_3G=48p^3\ne0.
\]

Finally, static exactness has a different universal bound: the full
static partner space is `ker C_3 intersect ker C_5 intersect ker C_7`,
by the complete analytic partner classification. Seventh order really
is required for that static statement: with
`F=p^{8/7}` and `G=q^6p^{-8/7}`,

\[
 C_3G=C_5G=0,\qquad
 C_7G=-\frac{1940889600}{117649}p^{-7}\ne0.
\]

Dynamic persistence lowers the necessary maximum gate from seven to
five. This explains a concrete way in which the analytic coefficient
space and the polynomial programme can share an exact finite stopping
rule even though their static partner spaces differ.

## A sharper two-equation certificate for gamma and polygamma

**Corollary FP.** For `F=log Gamma` or `F=psi^(m)`, `m>=0`,
on `p>0`,

\[
 \boxed{\mathcal D_\infty(qF)
   =\ker C_3\cap\ker(C_3D)=A\oplus qA.}                 \tag{FP1}
\]

This eliminates the fifth-order equation as well. It proves the
dynamic result directly, without first classifying the static partner
space. It still uses all finite `q` degrees with analytic coefficients.

More generally, suppose `F` analytically continues to a genuine
meromorphic pole of integer order `t>=1`,

\[
 F(p)=C_0p^{-t}+\text{a lower-order Laurent part},
 \qquad C_0\ne0,
\]

after shifting the pole to zero. A hypothetical sector with `c>=2`
that passes both equations would make `K_c` constant. But

\[
 K_c(p)\sim\frac{2C_0}{3}
   \big[(c+1)t-c+2\big]p^{-t-1}.                         \tag{FP2}
\]

Its coefficient does not vanish because

\[
 (c+1)t-c+2=(c+1)(t-1)+3>0.
\]

The meromorphic identity theorem transports a supposed constant
identity from the original interval to a punctured neighborhood of the
pole. Equation (FP2) contradicts that identity. No continuation of the
partner coefficient is required. Every polygamma has such a pole,
with `t=m+1` and `C_0=(-1)^(m+1)m!`.

For the logarithmic template
`F=-a log p+b(p)`, `a!=0`, with `b` analytic at zero,

\[
 K_c(p)=\frac{2a(c-2)}{3}\frac{\log p}{p}
   +\left[ca-\frac{2(c-2)b(0)}3\right]\frac1p
   +O(|\log p|+1).                                      \tag{FP3}
\]

At `c=2`, the coefficient `2a/p` is nonzero. At every `c>=3`, the
logarithmic coefficient is nonzero. Thus `K_c` is never constant, which
covers `log Gamma` using its `-log p` singularity. As above, the
potential must have the stated continuation; this is not an assertion
about a real-analytic function with no access to that singularity.

The two-equation conclusion for these pole and logarithmic classes also
holds for `H=qF(p)+V(p)` with **arbitrary analytic `V`**. The
highest `q`-degree of a hypothetical partner still satisfies exactly
the two equations above: the `V` terms lower `q` degree in both
`C_3` and `D`. Thus its degree cannot exceed one. Conversely,
`A+qA` is invariant under `D` and killed by every gate for this
affine-in-`q` Hamiltonian. This extends the polygamma result to an
arbitrary analytic additive potential without a new asymptotic
assumption on that potential.

The real integer pole restriction has content: the fractional power
`F=p^{-2/5}` in the sharpness example admits a stationary fourth-degree
sector through both third-order tests and fails the fifth gate. Thus
the two-equation corollary cannot be extended to all algebraic
singularities.

## Arbitrary additive potentials: a sharp depth-two theorem

**Theorem FA.** Let `F,V` be arbitrary real-analytic functions on a
connected open interval, and let `H=qF(p)+V(p)`. With the same finite
`q`-degree coefficient algebra,

\[
 \boxed{\mathcal D_\infty(H)=
  \ker C_3\cap\ker C_5\cap\ker(C_3D)\cap\ker(C_3D^2).}   \tag{FA1}
\]

Thus an arbitrary analytic additive potential requires at most two
Hamiltonian steps and gates no higher than fifth order. Two steps
really are necessary in this larger class.

**Proof.** First suppose `F''` is not identically zero. Choose an open
subinterval `J` where it is nowhere zero. Let `S_1` be the common
kernel of the first three operators in (FA1). The highest `q`-degree
sector of an element of `S_1`, restricted to `J`, satisfies exactly
the three equations of Theorem FD for `qF`: every `V` contribution
has strictly smaller `q` degree. The proof of FD therefore forces
its degree to be at most three. Analyticity extends the vanishing of
all higher coefficients from `J` to the whole interval.

The strip `W=A+qA` is invariant under `D` and killed by every gate.
Moreover,

\[
 \dim_{\mathbb R}(S_1/W)\le1.                            \tag{FA2}
\]

Indeed, the leading coefficient of a cubic is a scalar multiple of
`cuberoot(F'')` on `J`, hence has at most one free real scalar
globally. The difference of two candidates with equal cubic
coefficient has degree at most two. Its quadratic coefficient is
constant by `C_3G=0`, and `C_3DG=-12(F'')^2` on the generator `q^2`
excludes that coefficient. Thus the difference belongs to `W`.

Now let `G` pass all four equations in (FA1). Then `DG` belongs
to `S_1`: the two third-order equations follow from the last two
conditions on `G`, and `C_5DG=0` automatically because `DG` has
`q` degree at most three. If `G` is not in `W`, (FA2) gives

\[
 DG=\lambda G+w,\qquad \lambda\in\mathbb R,\quad w\in W.
\]

As `W` is invariant, every iterate stays in `S_1`, where the third
gate vanishes; every higher odd gate vanishes by `q` degree. If
`G` is in `W`, persistence already holds. This proves the sufficient
direction. Necessity follows directly from the definition of the core.

If `F''` is identically zero and `V'''` is not, the operator is
`C_3=-V'''*partial_q^3`. Hence its analytic kernel has `q` degree
at most two, is preserved by `D`, and is killed by every higher gate.
If both derivatives vanish identically, `H` is quadratic and every
gate vanishes on all of `A[q]`. These cases finish the proof.

**Exact sharpness witness.** On `p>0`, take

\[
 \begin{aligned}
 H&=qp^{-1/4}+p^{7/4},\\
 G&=q^3p^{-3/4}-\frac{21}{25}q^2p^{5/4}.
 \end{aligned}
\]

Direct rational-power differentiation gives

\[
 \begin{aligned}
 C_3G&=C_5G=C_3DG=0,\\
 DG&=-\frac{168}{25}q^2+\frac{147}{50}qp^2,\\
 C_3D^2G&=\frac{63}{8}p^{-9/2}\ne0.
 \end{aligned}                                          \tag{FA3}
\]

This partner passes every static gate and remains static after one
Hamiltonian bracket, but escapes at the second. Thus the one-step
bound for `qF` cannot be carried unchanged to `qF+V`. The corollary
for gamma and polygamma is stronger because its singularity excludes
the cubic sector before this obstruction can arise.

## Checkers and status

`depth_verify.py` independently expands the differential operators on
sparse fractional-power monomials using rational arithmetic. It checks
the sector formula, all four sharpness examples, the parameter identity
(FD6), a grid of the scalar factors, and the exact pole coefficient in
(FP2), as well as the sharp depth-two additive-potential example.
The separate adversarial audit
checks the formal differential elimination in the lemma.

\clearpage

# A rational stopping theorem and an algebraic persistent cubic

This note connects the polynomial affine strips in
`programmes/DYNAMIC_CORE_RESULTS.md` with the analytic `qF(p)` results of
the polygamma programme. All statements use the original affine
coordinates `(q,p)`, the constant-Poisson Moyal product, and finite degree
in `q`. They do not assert covariance of this same product under a
nonlinear canonical substitution. Historical priority is unassessed.

Let `I` be a connected open real interval, `A=C^omega(I,R)`,
`H=qF(p)+B(p)`, and `D={H,·}` with
`{H,G}=H_q G_p-H_p G_q`. Let `C3=T3(H,·)`, using the transvectant
convention of the compendium. Formal Moyal exactness requires every odd
transvectant of order at least three to vanish. Put

\[
\mathcal D_\infty(H)=\{G\in A[q]:T_k(H,D^rG)=0\quad
  (k\ge3\text{ odd},\ r\ge0)\}.
\]

## Rational coefficients: one gate and one bracket suffice

**Theorem A.** Suppose `F` is rational with real coefficients, has no
pole on `I`, and `F''` is nowhere zero on `I`. Let `B` be arbitrary in
`A`. Then, in all finite `q` degrees,

\[
\boxed{\ker C_3\cap\ker(C_3D)
       =\mathcal D_\infty(H)=A\oplus qA.}                 \tag{A1}
\]

Thus the full infinite family of odd gates and repeated brackets has a
uniform stopping rule in this coefficient class: `T3(H,G)=0` and
`T3(H,{H,G})=0` already characterize the core. No degree cutoff on the
observable is present. The polynomial specialization is the affine
strip already classified by Claude's theorem; the uniform two-check
certificate and arbitrary analytic potential `B(p)` are the refinement.

**Proof.** The strip `A+qA` is invariant under `D` and all its elements
pass every odd gate, because the `q` degrees of both `H` and a strip
element are at most one. It remains to exclude `G` of `q` degree `c>=2`
from the left side of (A1).

Write its highest coefficient as `q^c g(p)`, with `g` not identically
zero. The highest `q` coefficient of `T3(H,G)` is

\[
c(c-1)q^{c-2}\,[3F''g'-(c-2)F'''g].                     \tag{A2}
\]

The term `B` contributes only to lower `q` degrees. Let
`r=cuberoot(F'')`, the nonzero real-analytic real branch. Equation (A2)
forces `g=C r^(c-2)` with a nonzero real constant `C`; in particular `g`
is nowhere zero. The highest `q` coefficient of `DG` is

\[
Fg'-cF'g=K_cg,\qquad
K_c=\frac{c-2}{3}\frac{FF'''}{F''}-cF'.                 \tag{A3}
\]

Applying (A2) to `DG` gives
`3c(c-1)F'' g K_c'=0`, whether or not `DG` still has degree `c`.
Consequently `K_c` would have to be constant. We prove this impossible
for rational `F` and every integer `c>=2`.

If `F` has a finite complex pole of order `m>=1`, write
`F=a t^(-m)+O(t^(-m+1))`, where `t=p-p0` and `a!=0`. Then

\[
K_c=\frac23\big[(c+1)m-c+2\big]a\,t^{-m-1}
          +O(t^{-m}).                                   \tag{A4}
\]

The bracket is at least three. Hence `K_c` has a pole and is not
constant. This includes nonreal poles: a rational function constant on
the real interval would be the same constant rational identity over
the complex numbers. If `F` has no finite complex poles, it is a
polynomial. Its degree `n` is at least two since `F''!=0`. If its
leading coefficient is `a`, then

\[
K_c=-\frac23\big[(c+1)n+c-2\big]a\,p^{n-1}
          +O(p^{n-2}),                                  \tag{A5}
\]

again nonconstant. This contradiction proves (A1). Every division was
by a function assumed or proved nonzero on the selected interval.

The numerator of the obstruction `K_c'` is particularly simple:

\[
\begin{aligned}
3(F'')^2K_c'={}&(c-2)
 \big[F'F'''F''+FF''''F''-F(F''')^2\big]
 -3c(F'')^3.
\end{aligned}\tag{A6}
\]

This is affine in the integer `c`; equations (A4)--(A5) prove its
nonvanishing uniformly rather than searching over sectors.

**Corollary A.1 (a meromorphic pole suffices).** The same conclusion
(A1) holds if, instead of rationality, `F` has a meromorphic extension to
a connected complex domain containing `I` and at least one finite pole.
The analytic potential `B` still needs to be defined only on `I`.
Indeed, `K_c` is meromorphic on that domain. If it were constant on
`I`, the identity theorem would make it constant meromorphically, in
contradiction to the nonzero pole coefficient (A4). The pole may be
nonreal or outside the interval. No asymptotic estimate at infinity is
required.

Every polygamma `F=psi^(m)`, including digamma at `m=0`, satisfies this
corollary on `p>0`: it is meromorphic with poles of integer order
`m+1` at the nonpositive integers, and `F''=psi^(m+2)` has constant
nonzero sign on the positive axis. Thus

\[
\ker T_3(q\psi^{(m)}+B,\cdot)\cap
\ker[T_3(q\psi^{(m)}+B,D\cdot)]
 =A\oplus qA                                             \tag{A6a}
\]

for arbitrary analytic `B(p)` and every `m>=0`. The standard
polygamma definitions, recurrence and reflection identities are
documented in [NIST DLMF 5.15](https://dlmf.nist.gov/5.15).
Log-Gamma is not meromorphic; its separate asymptotic proof of the same
conclusion is recorded in `depth_finite_determination.md`.

## An explicit algebraic family across the boundary

**Theorem B.** On `p>0`, let

\[
F(p)=a p^{-1/4}+bp,\quad a\ne0,\qquad
H=qF(p),\qquad X=q p^{-1/4},\qquad G=X^3.
\]

Then

\[
\boxed{\frac{[H,G]_\star}{i\hbar}=\{H,G\}
      =-\frac{15b}{4}G,\qquad
 D^jG=\left(-\frac{15b}{4}\right)^jG.}                  \tag{A7}
\]

In particular `b!=0` gives a completely explicit algebraic active
persistent cubic outside the rational coefficient class of Theorem A.
It replaces the earlier implicit autonomous-ODE examples with elementary
fractional powers. Its full finite-`q`-degree core is

\[
\boxed{\mathcal D_\infty(H)=A\oplus qA\oplus\mathbb R X^3.} \tag{A8}
\]

**Proof of persistence.** Write `H=aX+bJ` with `J=qp`. The direct
transvectant identity gives `T3(X,X^3)=0`; all higher odd gates vanish
because their combined `q` degree is four. Also `J` is quadratic, so
it contributes no gate, and

\[
\{X,X^3\}=0,\qquad \{J,X^3\}=-\frac{15}{4}X^3.
\]

This proves (A7) independently of the complete analytic classification.
Equivalently, `F''=(5a/16)p^(-9/4)` and
`K3=FF'''/(3F'')-3F'=-15b/4`.

**Proof of completeness.** The complete analytic `qF` boundary theorem
is not needed here. Since `B=0`, distinct `q` degrees cannot cancel in
either `C3` or `C3D`. Equations (A2)--(A3) apply to each degree `c>=2`
separately, and direct simplification gives

\[
K_c=\frac{a(3-c)}2p^{-5/4}-\frac{b(7c-6)}4.             \tag{A8a}
\]

Because `a!=0`, this is constant exactly when `c=3`. Thus the common
kernel of `C3` and `C3D` is exactly the strip plus `R X^3`. Persistence
already proved in (A7) identifies it with the full dynamic core. Hence
the stronger identity

\[
\ker C_3\cap\ker(C_3D)
   =\mathcal D_\infty(H)=A\oplus qA\oplus\mathbb R X^3  \tag{A8b}
\]

is self-contained and holds in every finite `q` degree. The exceptional
cubic is selected directly by the factor `3-c`; no imported analytic
classification or numerical truncation is necessary.

**Why the cubic is a boundary, not a template for arbitrary degrees.**
For any integer `c>=4`, set

\[
\rho=\frac{2-c}{c+1},\qquad
H=q p^\rho+bqp,\qquad G=(q p^\rho)^c.
\]

Then `T3(H,G)=0` and
`{H,G}=bc(rho-1)G`, so `T3(H,D^jG)=0` for every `j>=0`.
Nevertheless, direct fifth-order arithmetic gives

\[
T_5(H,G)=-8(c)_4(\rho)_4q^{c-4}p^{-c-3}\ne0.             \tag{A8c}
\]

Thus arbitrarily deep third-order checks cannot replace higher gates
for general analytic coefficients. At `c=3`, `rho=-1/4` and the falling
factorial `(c)_4` vanishes; this is the genuine cubic family above.
The distinction matters when exporting a successful `T3` argument from
the polynomial branch to a wider coefficient ring.

## A sharp nonlinear canonical-coordinate obstruction

Set

\[
Y=\frac45p^{5/4}.
\]

Then `\{X,Y\}=1` and

\[
H=aX+\frac{5b}{4}XY.                                    \tag{A9}
\]

So this nonlinear Hamiltonian becomes quadratic in the algebraic
canonical coordinates `(X,Y)`. Rebuilding the standard flat Moyal
product in those new coordinates would make every observable exact.
The original flat Moyal product in `(q,p)` has a different answer:
although `X` and `X^3` belong to its dynamic core, `X^2` does not.
Indeed,

\[
\begin{aligned}
T_3(H,X^2)&=-\frac{15a}{16}p^{-15/4},\\
\frac{[H,X^2]_\star}{i\hbar}
 &=-\frac{5b}{2}X^2+\frac{5a\hbar^2}{128}p^{-15/4},\\
X\star X&=X^2+\frac{\hbar^2}{64}p^{-5/2}.
\end{aligned}\tag{A10}
\]

The star square is a quantum eigenobservable:
`[H,X star X]_star/(i hbar)=-(5b/2)(X star X)`, by the derivation law.
This does not put its ordinary leading term `X^2` in the classical
dynamic core; its explicit correction cancels the anomaly in (A10).
The core is a vector space, not an algebra under ordinary multiplication.
The formulas exhibit the coordinate dependence directly, without
mistaking a nonlinear change of coordinates for covariance of the same
flat Moyal product.

The classical evolution is elementary as well. Put `Z=p^(5/4)`.
Then `DZ=(5/4)(a+bZ)` and `DX=-(5b/4)X`. For `b!=0`,
`Z(t)=exp(5bt/4)(Z(0)+a/b)-a/b`, as long as the trajectory stays in
`p>0`, and `G(t)=exp(-15bt/4)G(0)` is exact under both evolutions.
These are local-domain evolution statements, not assertions of a
globally complete flow across the singular boundary `p=0`.

## Relation to the branch and verification scope

Theorem A recovers Claude's polynomial affine strips and adds an
observable-degree-independent gate-depth bound. Theorem B shows exactly
why extending a polynomial-core collapse statement to arbitrary analytic
coefficients would fail: a simple algebraic coefficient already adds an
active cubic. Log-Gamma and all polygammas lie on the collapsing side by
their separately proved analytic asymptotic/pole arguments.

`analytic_bridge_check.py` uses exact rational arithmetic and a sparse
fractional-power derivative engine. It checks the gate identities,
persistence, canonical relation, anomaly and star-square correction;
it also tests Theorem A on finite polynomial/Laurent boxes by a direct
matrix kernel calculation with no output projection. Those boxes
cross-check conventions; the proof above, not their size, supplies the
all-degree claims.

The distinction between affine covariance and nonlinear canonical
changes belongs to established Weyl quantization theory. Primary
background includes Mark Gotay, *On the Groenewold--Van Hove problem for
R^{2n}*, [arXiv:math-ph/9809015](https://arxiv.org/abs/math-ph/9809015).
No claim is made that a new geometric torsion operation or a new general
quantization obstruction has been invented. The specific stopping
theorem and explicit family here still require a focused priority check.

\clearpage

# Exact classification of cubic-preserving analytic potentials

This note advances the finite stopping theorems in
`depth_finite_determination.md` to an explicit classification of the additive
potential for the algebraic cubic boundary. It uses the original affine
coordinates, the flat Weyl–Moyal gates, real-analytic coefficients and finite
degree in `q`. No external-priority claim is made.

Let `I` be a connected open subinterval of `(0,infinity)`, let
`A=C^omega(I,R)`, and put

\[
 H=q p^{-1/4}+V(p),\qquad D=\{H,\cdot\},\qquad
 W=A\oplus qA,
\]

where `V` is arbitrary in `A` and
`{H,G}=H_qG_p-H_pG_q`. The dynamic core consists of the elements `G` for
which every `T_j(H,D^rG)` vanishes, for odd `j>=3` and every `r>=0`.

## The complete potential theorem

**Theorem AP.** Exactly one of the following alternatives holds.

If there are real constants `c0,a,b,c` with

\[
 \boxed{V(p)=c_0+a p^{-1/4}+b p^{3/4}+c p^{5/2},}       \tag{AP1}
\]

then

\[
 \boxed{\mathcal D_\infty(H)
   =W\oplus\mathbb R\,(H-c_0)^3.}                     \tag{AP2}
\]

For every other analytic potential, `D_infty(H)=W`. These are equalities
in all finite `q` degrees, including when `I=(0,infinity)`. The extra
generator in (AP2) is stationary. The four constants in (AP1) are unique.

The constant shift must be removed before cubing. In general `H^3` is
not a valid replacement for `(H-c0)^3`: their difference contains
`3c0(H-c0)^2`, whose quadratic `q` coefficient need not lie in `W` or in
the core.

In fact the family (AP1) obeys the exact diagnostic
`T3(H,H^3)=-(45/16)c0 p^(-15/4)`, so a nonzero constant shift makes
the unshifted cube fail already at its static third gate.

### Highest-degree exclusion

The strip `W` is invariant under `D` and killed by every odd gate of
order at least three. Suppose that a core element has `q` degree `n>=2`
and highest coefficient `q^n g(p)`, with `g` nonzero. At the highest
output degree the potential contributes nothing, so `T3(H,G)=0` forces

\[
 3F''g'-(n-2)F'''g=0,\qquad F=p^{-1/4}.
\]

Consequently `g` is a nonzero constant multiple of
`p^{-3(n-2)/4}`. The highest coefficient of `DG` is `K_n g`, where

\[
 K_n=\frac{n-2}{3}\frac{FF'''}{F''}-nF'
     =\frac{3-n}{2}p^{-5/4}.                            \tag{AP3}
\]

The equation `T3(H,DG)=0` then forces `K_n'=0`, which is possible only
for `n=3`. In particular there is no core element of `q` degree two,
and every core element has degree at most three. This excludes all
higher degrees directly, without invoking a degree cutoff, a numerical
kernel, or a fifth-gate completeness theorem.

Normalize the cubic coefficient to `g=p^{-3/4}`. Modulo `W`, any
additional core element must therefore have the form

\[
 G=q^3p^{-3/4}+q^2h(p).                                 \tag{AP4}
\]

Two normalized candidates differ by a core element of degree at most
two and hence by an element of `W`. Thus the quotient of the core by
`W` has dimension at most one.

### Necessary and sufficient compatibility equations

Direct third-order differentiation gives

\[
 T_3(H,G)=6F''h'-6V'''p^{-3/4}.
\]

The cubic coefficient of `DG` is zero, and its quadratic coefficient is

\[
 Fh'-2F'h-3V'p^{-3/4}.
\]

Because the core is invariant under `D` and has no degree-two element
outside `W`, a persistent cubic necessarily satisfies

\[
 \boxed{h'=\frac{16}{5}p^{3/2}V''',\qquad
       ph'+\frac12h=3p^{1/2}V'.}                        \tag{AP5}
\]

Conversely, these equations imply `T3(H,G)=0` and `DG in W`. Every
higher odd gate on `G` vanishes because the combined `q` degree of
`H` and `G` is four. The invariance and exactness of `W` therefore
prove that `G` belongs to the full dynamic core. Thus (AP5) is
necessary and sufficient, including for arbitrary analytic `V`.

### Solving the compatibility equation for every analytic potential

The second equation of (AP5), followed by the first, gives

\[
 h=6p^{1/2}V'-\frac{32}{5}p^{5/2}V'''.                 \tag{AP6}
\]

Differentiating (AP6) and substituting back into the first equation
shows that (AP5) is equivalent to

\[
 \boxed{p^4V''''+3p^3V'''-\frac{15}{16}p^2V''
                       -\frac{15}{32}pV'=0.}           \tag{AP7}
\]

This is a regular linear Euler equation on every interval `I` under
consideration. With `x=log p`, its indicial polynomial is

\[
 \nu(\nu-1)(\nu-2)(\nu-3)
 +3\nu(\nu-1)(\nu-2)-\frac{15}{16}\nu(\nu-1)
 -\frac{15}{32}\nu
 =\frac{\nu(4\nu+1)(4\nu-3)(2\nu-5)}{32}.            \tag{AP8}
\]

The four roots are distinct. The complete real-analytic solution
space is consequently the four-dimensional space in (AP1), not merely
the span of a collection of tested monomials. Standard uniqueness for
the regular fourth-order equation extends the local solution throughout
the connected interval.

The constant is recovered intrinsically by

\[
 c_0=\frac{32}{15}
       \left(p^3V'''-\frac{15}{16}pV'+\frac{15}{32}V\right),            \tag{AP9}
\]

which is constant exactly when (AP7) holds. Equivalently `v=V-c0`
satisfies the third-order equation

\[
 v'''-\frac{15}{16}p^{-2}v'
                      +\frac{15}{32}p^{-3}v=0.         \tag{AP10}
\]

The subtraction of `c0` in this last equation is essential. Substitution
in (AP6) now gives

\[
 h=3\left(a p^{-3/4}+b p^{1/4}+c p^2\right)
   =3p^{-1/2}(V-c_0).                                  \tag{AP11}
\]

The cubic and quadratic `q` coefficients of `(H-c0)^3` are exactly
those in (AP4) and (AP11). Its difference from `G` is in `W`, and it is
stationary because it is a power of `H-c0`. This proves (AP2), including
the completeness of both alternatives.

## General cubic-preserving potentials on a regular analytic chart

**Proposition GC.** Let `F,V` be real analytic on a connected interval,
assume `F''` is nowhere zero, and set

\[
 K_3=\frac{FF'''}{3F''}-3F'=\lambda\in\mathbb R.
\]

Choose any nonzero analytic solution `g` of
`g'/g=F'''/(3F'')`; for example a nonzero constant multiple of the
real cube root of `F''`. For

\[
 H=qF+V,\qquad G=q^3g+q^2h+w,\quad w\in W,
\]

membership of `G` in the full dynamic core is equivalent to

\[
 \boxed{h'=L_V:=\frac{gV'''}{F''},\qquad
 Fh'-(2F'+\lambda)h=3gV'.}                              \tag{GC1}
\]

The proof is the same leading-coefficient computation as above.
The first equation says `C3 G=0`. The top coefficient of `DG` is
`lambda g`; therefore the second says `DG-lambda G in W`. This is
sufficient for every iterate and every gate. For necessity,
`DG-lambda G` is a core element of degree at most two. Every such
element is in `W`: a quadratic coefficient is constant by its third
gate, and the next third gate gives its nonzero multiple of
`(F'')^2` unless that constant vanishes. Thus (GC1) is also necessary.
No claim about core elements of higher degree is needed in this
proposition.

Write `B=2F'+lambda`. On a **regular chart** where `F B` is nowhere
zero, (GC1) is a regular fourth-order linear equation for `V`:

\[
 \left(\frac{F L_V-3gV'}{B}\right)'=L_V.              \tag{GC2}
\]

It has a four-dimensional space of real-analytic solutions, and `h` is
uniquely reconstructed from `V`. An equivalent denominator-cleared
expression is obtained by setting

\[
 M=BF'',\qquad Z=g(FV'''-3F''V'):
 \qquad MZ'-M'Z-B^2F''gV'''=0.                         \tag{GC3}
\]

The coefficient of `V''''` in (GC3) is `B F'' F g`, which is nonzero
under the stated chart assumptions. The compatibility system (GC1)
remains meaningful at a zero of `F` or `B`, but the elimination and
four-dimensional regular-chart assertion are not asserted across such
zeros. Analytic continuation and matching there require a separate
argument.

## An active extension with a complete conditional classification

For

\[
 F=a_*p^{-1/4}+b_*p,\qquad a_*\ne0,
\]

one may choose `g=p^{-3/4}` and

\[
 \lambda=-\frac{15b_*}{4},\qquad
 K_n=\frac{a_*(3-n)}2p^{-5/4}
                     -\frac{b_*(7n-6)}4.               \tag{AC1}
\]

The same highest-degree argument forces every core element outside
`W` to have degree three, and the quotient by `W` still has dimension
at most one. Hence the full core is `W` unless there is a global
analytic solution `h` of (GC1), in which case it is

\[
 W\oplus\mathbb R(q^3p^{-3/4}+q^2h).
\]

On every connected regular chart
`F(2F'+lambda)!=0`, exactly a four-dimensional linear space of
potentials admits this additional cubic. This follows from the regular
fourth-order equation (GC2); a closed form or a global classification
across its singular charts is not claimed here. When `b_*!=0`, the
extra quotient is active, with eigenvalue `-15b_*/4`. For the explicit
translation potentials `V=tF+c0`, a representative is
`(q+t)^3p^{-3/4}`, and it is an exact eigenvector with that eigenvalue.

## Exact verification and a rejected potential

`analytic_potential_classification.py` is a standalone standard-library
checker. It implements mixed derivatives and transvectants independently
using rational coefficients, fractional `p` exponents, and formal
coefficient parameters. The generic Hamiltonian in (AP1), its shifted
cube and the compatibility identities are checked coefficient by
coefficient for all parameter values. The indicial factorization and
(AC1) are identities in a formal degree variable, not sampled degrees.
The active translated cubic is checked with formal parameters as well.

The rejected potential `V=p^(7/4)` gives a nonzero (AP7) coefficient
`-21/8`. Its published depth-two sharpness witness

\[
 H=qp^{-1/4}+p^{7/4},\qquad
 G=q^3p^{-3/4}-\frac{21}{25}q^2p^{5/4}
\]

passes `C3`, `C5` and `C3 D` but fails at
`C3 D^2 G=(63/8)p^(-9/2)`. This confirms that the failure is a genuine
compatibility obstruction rather than a missed static gate.

Run `python3 -B research/core_overlap/analytic_potential_classification.py`.
Use `--output PATH` to retain the JSON receipt. The proof above
establishes the all-analytic and all-degree statements; the checker
independently verifies the exact identities used in that proof.

\clearpage

# Protected nonlinear canonical transport of exact dynamic sectors

This note explains why a nonlinear canonical change can preserve a particular
flat Weyl–Moyal dynamic sector even though it does not preserve flat Moyal
exactness on every observable. It supplies a structural explanation for the
pure-top counterfamilies in this programme. No historical priority claim is
made for canonical transformations, Weyl ordering, or their quantum correction.

We use

\[
 \{A,B\}=A_qB_p-A_pB_q,\qquad
 \frac{[A,B]_\star}{i\hbar}
 =\sum_{r\ge0}\frac{(-1)^r\hbar^{2r}}{2^{2r}(2r+1)!}
    T_{2r+1}(A,B).
\]

All statements below are algebraic in characteristic zero. For polynomial
inputs the relevant series terminate. Formal powers of `hbar` are retained;
they are never fitted from numerical samples.

## The protected shear lemma

Let `w(q)` be a polynomial, choose an antiderivative `U'(q)=w(q)`, and
write `sigma_w A(q,p)=A(q,p+w(q))`. The quantum canonical automorphism

\[
 \mathscr S_w=\exp\left(\frac{\operatorname{ad}_\star U}{i\hbar}\right)
\]

has the exact factorization

\[
 \boxed{\quad
 \mathscr S_w
 =\sigma_w\exp\left(
   -\frac{\hbar^2}{24}w''\partial_p^3
   +\frac{\hbar^4}{1920}w^{(4)}\partial_p^5-\cdots
                 \right).\quad}                         \tag{C1}
\]

Indeed, `T_k(U,A)=U^(k) partial_p^k A`, and every coefficient in these
operators depends on `q` alone. Consequently all the displayed differential
operators commute. The exponential is finite on each polynomial because
each nonzero application lowers its `p` degree. Since its generator is an
inner star derivation, `S_w` preserves the star product.

In particular

\[
 \mathscr S_w A=\sigma_w A\qquad (\deg_p A\le2).            \tag{C2}
\]

This degree threshold is sharp when `w''` is nonzero:

\[
 \mathscr S_w(p^3)=(p+w)^3-\frac{\hbar^2}{4}w''.           \tag{C3}
\]

Here is the resulting transport principle. Suppose `H_0` and a linear
space `V` consist of polynomials of `p` degree at most two, every odd gate
`T_k(H_0,v)` with `k>=3` vanishes on `V`, and `{H_0,V} subset V`. Then

\[
 \sigma_w V\subseteq\mathcal D_\infty(\sigma_wH_0).        \tag{C4}
\]

To prove it, apply the star automorphism `S_w` to
`[H_0,v]_star/(i hbar)={H_0,v}`. Every member of this identity is in the
protected subspace, so (C2) changes the quantum transport into the ordinary
canonical pullback. Hence
`[sigma_wH_0,sigma_wv]_star/(i hbar)={sigma_wH_0,sigma_wv}`. The same
argument applies to every Hamiltonian iterate, because these remain in
`V`. This proves (C4). It does not assert transport of the entire core
under an arbitrary nonlinear change of coordinates.

## A complete pure-top family

Take `a>=1`, `A!=0`, `w` of degree `t>=2`, and arbitrary constants
`B,C,beta,delta`. Set

\[
 z=qp,\quad H_0=q^a(Az^2+Bz+C)+\beta z+\delta,
\]

\[
 G=qp+q w(q),\qquad
 H=q^a(AG^2+BG+C)+\beta G+\delta.                         \tag{C5}
\]

Then

\[
 \boxed{\mathcal D_\infty(H)=\operatorname{span}\{1,H,G\},
 \qquad \{H,G\}=a(H-\beta G-\delta).}                    \tag{C6}
\]

The lower bound follows from the protected shear lemma. It can also be
checked directly: `H` has `p` degree two and `G=qp+u(q)`. In every term of
an odd gate of order at least three, either three `p` derivatives hit
`H`, two hit `G`, or at least two `q` derivatives and one `p` derivative
hit `G`. Each possibility vanishes. The bracket in (C6) follows by
transporting the identity for `H_0` under `sigma_w`.

For completeness, filter by `p` degree. The transverse top of `H` is
`Aq^(a+2)p^2`. Its all-degree core is `span{1,qp,Aq^(a+2)p^2}` by the
unequal-monomial theorem, because `a+2>2`. The associated graded of the
core of `H` embeds in this three-dimensional core. Therefore the core of
`H` has dimension at most three; the three independent elements in (C6)
give equality. The top total-degree term of `H` is a nonzero multiple
of `q^(a+2t+2)`, so these are pure tops. The generator `G` has degree
`t+1>=3`: its presence is not explained by a quadratic core element.
The `p^2` coefficient `Aq^(a+2)` is nonconstant, so the family is outside
the previously proved affine and constant-quadratic strip structures.

The smallest example of this form is

\[
 H=q^7+2q^5p+q^3p^2=q(qp+q^3)^2,
 \quad G=qp+q^3,
 \quad \{H,G\}=H.                                       \tag{C7}
\]

Thus a nonlinear shear of a three-dimensional exact sector is a mechanism
for retaining active polynomial exact dynamics beneath a pure top. It
also explains why a conjecture based only on affine normal forms can
miss this family.

## The complementary `qF(p)` chart

Let `F` be real analytic and nonzero on an interval `I`, and put

\[
 Q=qF(p),\qquad P=S(p),\qquad S'=1/F.
\]

Then `{Q,P}=1`, and also `[Q,P]_star=i hbar` exactly. The latter holds
because `Q` is affine in `q` and `P` depends only on `p`. Nevertheless
ordinary pullback fails already at the square:

\[
 T_3(Q,Q^2)=12FF'F'',\quad
 \frac{[Q,Q^2]_\star}{i\hbar}=-\frac{\hbar^2}{2}FF'F'',
 \quad \{Q,Q^2\}=0,                                    \tag{C8}
\]

\[
 Q\star Q=Q^2+\frac{\hbar^2}{4}(F')^2.                  \tag{C9}
\]

For a polygamma `F=psi^(m)`, the obstruction in (C8) is
`12 psi^(m) psi^(m+1) psi^(m+2)`; it is nowhere zero for `m>=1` on the
positive axis. For digamma one restricts to an interval avoiding its
zero. For `F=log Gamma`, the same expression is
`12 log Gamma psi psi^(1)` and is not identically zero on any open
interval avoiding the zeros of `F`. These are ordinary consequences of
the derivative identities; no numerical special-function evaluation is
used in (C8).

The exact quantum pullback of a finite polynomial in `Q` with analytic
`P` coefficients is

\[
 \mathscr W_F\bigl(Q^n a(P)\bigr)
   =J_Q^n\bigl(a(S(p))\bigr),\qquad
 J_Q(A)=\tfrac12(Q\star A+A\star Q).                     \tag{C10}
\]

Here `Q` inside the star product denotes `qF(p)`. The commutation
relation `[Q,a(S)]_star/(i hbar)=a'(S)` verifies the usual Weyl
relations. Formula (C10) is therefore a star-algebra homomorphism from
the flat `(Q,P)` algebra to the original one. It is invertible as a
formal triangular map: its leading term is ordinary canonical
pullback, and its corrections lower `q` degree by positive even
integers. Each finite `Q` degree has only finitely many corrections.

Writing `a` now for `a(S(p))`, its first two nontrivial cases are

\[
 \mathscr W_F(Q^2a)
 =q^2F^2a+\frac{\hbar^2}{4}F'(F'a+Fa'),                  \tag{C11}
\]

\[
 \mathscr W_F(Q^3a)
 =q^3F^3a+\frac{\hbar^2q}{4}
  \bigl[(5F(F')^2-F^2F'')a+3F^2F'a'\bigr].             \tag{C12}
\]

For every integer `n>=2`, the coefficient of `hbar^2` is

\[
 \frac{n(n-1)}{24}q^{n-2}F^{n-2}
 \bigl[(2n-1)(F')^2a+3FF'a'-(n-2)FF''a\bigr].           \tag{C13}
\]

For an all-`n` verification, write the `hbar^2` term as
`q^(n-2)b_n(p)`. The defining Jordan product gives `b_1=0` and

\[
 b_{n+1}=Fb_n+\frac n8\left[
  2nF^{n-1}(F')^2a+2F^nF'a'-(n-1)F^nF''a\right].
\]

Summing `sum j^2`, `sum j`, and `sum j(j-1)` gives (C13). Thus its
arbitrary-degree statement is an induction identity, rather than an
extrapolation of the companion checker's finite fixtures. No coordinate
covariance of the ordinary flat Moyal product is assumed.

Finally suppose `F''` is nowhere zero and

\[
 K_3=\frac{FF'''}{3F''}-3F'=\lambda.
\]

Then `r=cuberoot(F'')` satisfies
`r/F^3=c_0 exp(lambda S)` for a nonzero constant `c_0`. The classical
persistent cubic `q^3r` is the ordinary pullback of
`c_0 Q^3 exp(lambda P)`. Its first integral is

\[
 FF''-5(F')^2-3\lambda F'=C.
\]

Substitution into (C12) gives the exact correction

\[
 \mathscr W_F(Q^3e^{\lambda P})
 =q^3F^3e^{\lambda S}
   -\frac{C\hbar^2}{4}qF e^{\lambda S}.                 \tag{C14}
\]

Both terms are classical Hamiltonian eigenvectors of eigenvalue
`lambda`. In the explicitly constructed active family
`F'=aF^5+b`, `a!=0`, one has `lambda=-5b/3` and `C=0`. Thus its cubic
eigenpartner is a second protected nonlinear canonical pullback: the
classical and quantum Weyl pullbacks agree on this particular cubic,
although the square obstruction (C8) is generally nonzero. The
polynomial shear protection (C2) and the analytic cubic protection
(C14) supply complementary, precisely scoped links between the two
research programmes.

\clearpage

# Balanced-top audit and a minimal proof repair

The balanced theorem at Claude commit `e91e14d` survives this audit. One step in
its published argument needs a correction. Subtracting multiples of `H` does
**not** justify requiring an extra element's top exponent to satisfy `s < mu`.
For example, a hypothetical extra element can initially have top `(qp)^(mu+1)`.
The dynamic core is a vector space, not an algebra; powers of `H` cannot be
subtracted without first proving they belong to it.

No additional theorem is needed to repair the argument. Choose any element
`G` outside `span{1,H}`. Its top is `c(qp)^s` by the top-weight lemma. If `s=mu`,
subtract `cH`; if this leaves a nonconstant polynomial, its degree is smaller
than `2mu` and its new exponent differs from `mu`. If it leaves only a constant,
the original `G` was in the excluded span. Thus in every case, after rescaling,
there is an extra `G` with `s >= 1` and `s != mu`. This is the only condition
the rest of the proof uses.

The factor `s(s-mu)` is nonzero for every such exponent, including `s>mu`.
The positivity estimate is symmetric in `s` and `mu`: a matched pair of
monomials has indices `(x,y)` and `(x-mu+s,y-mu+s)`, all nonnegative. Consequently
both `2mu >= k+|u|` and `2s >= k+|u|`, where `k=2mu-x-y` and `u=x-y`.
All stated positivity conclusions remain valid unchanged.

There are two boundary cases worth stating explicitly. When the proposed
partner monomial has a negative exponent, the bracket relation immediately
forces the original off-diagonal coefficient to vanish. When `k` exceeds
the degree of one of the two polynomials, this is the same argument with
the missing homogeneous component set to zero. Thus induction continues
through all components, without a restriction on the relative degrees of
`H` and `G`.

The bracket's component at the first unremoved deficit has an off-diagonal
support. It must also be diagonal because `{H,G}` lies in the dynamic core,
whose top is in `K[qp]`. This justifies setting that component to zero; no
assumption that the whole bracket vanishes is needed. Lower components of
both polynomials are diagonal by induction and hence Poisson commute, so
they do not introduce additional terms at that deficit.

The all-odd-order vanishing for two polynomials in `qp` follows from exchanging
the two coordinates in the transvectant, or directly pairing its summands.
The finite checks at orders 3, 5, and 7 in `check_balanced.py` are useful
calibrations, while this antisymmetry argument supplies the statement for
every odd order.

`audit_balanced.py` independently checks the scalar identity directly from
falling-factorial transvectants, both relative exponent ranges, support
boundaries, and every possible zero in the finite declared grid. It does
not replace the symbolic identity or the positivity proof. Its purpose is
to exercise the cases omitted by the unnecessary `s<mu` assertion.

Theorem T and Lemma F in §6.6 have no additional blocker found in this audit.
Their transverse filtration may assign weight zero to `ell`: the associated
graded embedding still implies finiteness when the entire top core is finite.
For the pure part of T, the exclusion is specifically a **power of a linear
form**, `phi=c(ell+gamma)^e`; the phrase “perfect power” should not be read as
excluding, for example, a square of a nonlinear polynomial.

## Independent review of the new unequal transverse classification

The theorem and proof in `pure_perfect_power.md` have been read independently.
The transverse associated graded argument bounds the entire core by three
dimensions. Its extra element must have the exact shape
`J=(q+gamma)p+u(q+gamma)`, so the proof uses no bounded-degree guess for `u`.
The identity `T3(H,J)=-H_ppp u'''` eliminates every nonlinear `u` when the
transverse degree is at least three. A quadratic `J` is impossible under a
pure total top: the top of `{H,J}` then has coefficient `d` against `H`,
whereas its transverse top forces coefficient `r-s`, with `d>r+s`.

For transverse degree two, the Laurent-ring integration of the closure
equation is valid because `J` is algebraically independent of `t=q+gamma`
and the derivation is `t*d/dt` at fixed `J`. The eigenvalue `r-2` is a positive
integer. This forces `H-beta J-delta=t^(r-2)P(J)` with `P` quadratic. The
coefficient recognition equations have the correct signs in the stated
Poisson convention. Their constant test is necessary and sufficient, rather
than only a necessary test obtained by projecting the image.

The family is polynomial in the original variables and its nonquadratic
`J` passes every odd gate by the separate derivative argument. Hence it is
a valid counterexample to P003, not a nonlinear covariance assertion.

There is a further simple stationary example outside the *unequal* scope of
that theorem: `J=qp+q^3`, `H=J^2`. Here the total top is pure `q^6` and the
transverse top is balanced `q^2p^2`. The span of `1,J,H` survives, while
`T3(H,J^3)=72q^3J` is nonzero. This does not affect the balanced **total-top**
theorem, whose leading homogeneous part is a nondegenerate quadratic power.

\clearpage

# Independent adversarial assessment

This assessment concerns the overlap work based on Claude commit
`e91e14d`. It is an internal mathematical
review, not external peer review, formal proof verification, or a priority claim.

## Pure-top counterexample and replacement stratum

The counterexample `J=qp+q^3`, `H=qJ^2` is valid. Direct differentiation
gives `{H,J}=H`. Every derivative of `J` of order at least three involves
only `q`, while `H` has degree two in `p`, so every odd gate vanishes.
The span of `1,H,J` is therefore invariant and exact. Its dimension is three,
because the three elements have different transverse degrees.

The all-degree upper bound does not follow from a finite search. It follows
from the transverse filtration and the already proved monomial theorem:
the transverse top `q^3p^2` has core `span{1,qp,q^3p^2}`. An additional
core element of transverse degree zero must be constant; after subtracting
a multiple of `H`, any other element has the uniquely normalized form
`qp+u(q)`. Hence the full core is exactly three-dimensional. This is a
counterexample to the unrestricted conjecture P003 at the inspected commit,
not to any of the restricted proved statements B, Q, Q', or T.

The proof of the complete unequal perfect-power classification in
`pure_perfect_power.md` is sound. The transverse filtration is valid with
weight `(0,1)` even though the filtered pieces are not finite-dimensional:
each polynomial has finite transverse degree and the leading comparison is
applied separately to each operator identity. Finite-dimensionality of the
resulting associated graded core, rather than of the ambient filtered
pieces, supplies the dimension bound.

If a third core element exists, it must be `J=tp+u(t)` and satisfy
`{H,J}=(r-s)H+bJ+c`. The identity `T3(H,J)=-u'''H_ppp` forces `u` to be
quadratic when `s>=3`. A quadratic `J` would force the top eigenvalue to be
the total degree `d`, whereas the transverse comparison forces it to be
`r-s`; pure total top implies `d>r+s`, a contradiction. For `s=2`, Euler
integration in the Laurent coordinates `(t,J)` gives precisely
`H=t^(r-2)P2(J)+beta J+delta`. The coefficient-based decision test has the
correct signs, and its divisibility conditions account for the resonant
coefficient of degree `r-1` in the linear-in-`p` part.

The independent checker `review_checks.py` uses its own direct polynomial
differentiation. It verifies 120 parameterized family members, 2,760 odd
gate identities, and brackets through depth five. For the basic degree-seven
example, independent modular matrices have nullity three through total
degree nine. Those matrices corroborate the example; the filtration proof
is what establishes the all-degree statement.

## Analytic finite determination

The theorem in `depth_finite_determination.md` is correct under its stated
real-analytic, connected-interval, finite-`q`-degree hypotheses and the
condition that `F''` is nowhere zero. The three tests
`C3 G=0`, `C3 D G=0`, and `C5 G=0` determine the full core. Sector splitting
is exact because `D` preserves `q` degree and each gate shifts every input
sector by the same amount.

For degrees at least five the shorter incompatibility argument is an
independent derivation of the obstruction. In the notation of the theorem,
let `E=Fu-awB-kB`, with `F'=w`, `w'=delta B`, `B'=u`, `u'=v`, and
`v'=beta vu/B`. Define `L=a(beta-1)+2` and

```
J = Lwv + (beta-1)kv + (1-3a)delta Bu,
R = [a(beta-4)+3]Bv - (3a-1)(1-beta)u^2.
```

The following three identities hold formally in a Laurent-polynomial ring:

```
E'' = J + beta v E/B,
v (J/v)' = delta R,
R' = uv (beta+5)[1+a(beta-2)].
```

The independent checker verifies these by exact symbolic arithmetic with
its own Laurent-polynomial derivation. There is no numerical differential
approximation and no hidden division by a first-integral constant. Since
`v` is nowhere zero and `u` is nonzero on some open subinterval, `E=0` would
force the nonzero scalar `(beta+5)[1+a(beta-2)]` to vanish. The parameter
identity shows the second factor is strictly positive for every integer
sector degree at least five. The separate degree-two, degree-four, and
`B''=0` cases are correctly treated in the theorem note.

The direct fractional-power examples in that note establish necessity of
each of the three tests. In particular, testing third-order corrections at
every bracket depth is still insufficient universally: the stationary
fourth-power example passes all of those tests and fails the fifth-order
gate.

## Rational coefficients with arbitrary analytic potential

The highest-`q`-degree proof of the rational-coefficient extension is also
valid: in `H=qF(p)+B(p)`, the additional potential contributes one lower
`q` degree to both the third gate and the derivation. It cannot cancel the
highest-sector obstruction. At a pole of integer order `m>=1`, the candidate
sector obstruction has nonzero leading coefficient proportional to
`(c+1)m-c+2`; if the rational function has no finite poles, its polynomial
leading coefficient is proportional to `(c+1)n+c-2`, also nonzero. Thus no
sector of degree at least two persists. This is an exact algebraic argument,
not a finite-degree extrapolation. A meromorphic function with a finite
pole gives the same contradiction when continuation to that pole is part
of the explicitly stated domain assumptions.

## Scope retained

No claim here transports the flat Moyal product through an arbitrary
nonlinear canonical map. The special shear family's exactness is proved
directly by derivatives. No claim identifies an analytic-function kernel
with a rational polynomial Weyl-ideal receipt. Literature priority remains
unresolved, and the remaining transverse balanced exception is a different
stratum from the unequal exception classified here.

## Nonlinear shear compositions with balanced transverse top

The theorem in `audit_balanced_transverse.md` is approved. Its key
transverse Euler resonance is exact: for `H=P(J)`, `J=qp+u(q)`, and a
hypothetical core element with first transverse pieces `Q^s+f(q)p^(s-1)`,
one bracket forces `f=sq^(s-1)v+cq^(s-1)`. The coefficient at the resonant
Euler monomial vanishes on the left, so a nonzero diagonal bracket top is
impossible. No assumption that powers of a core element remain in the core
is made in this reasoning.

The first nonzero third-gate coefficient is
`mu s(s-mu)(s+mu-3)q^(mu+s-1)u'''`. The formal negative output degree in
the exceptional pair `mu=2,s=1` has zero coefficient and is correctly
excluded from the polynomial comparison. Consequently the three regimes
are the width-two strip for linear compositions, the stationary space
`span{1,J,J^2}` for quadratic compositions, and `span{1,H}` for degree at
least three. This concerns a balanced transverse top and does not conflict
with the already proved balanced total-top theorem.

Independent direct differentiation now checks this first-gate factor in
90 complete polynomial composition pairs, rather than only in formal
monomial coefficients.

## Parabolic quadratic compositions, including linear forcing

The theorem in `pure_quadratic_composition.md` is approved in its full
stated scope `Q=p+bq^2+cq+d`, `b!=0`, `H=P(Q)+epsilon q`. The change of
variables is a polynomial algebra isomorphism used to transform the
operators; it is not an appeal to nonlinear covariance. Direct chain-rule
expansion gives the stated third gate and
`D=epsilon partial_z-P'(z)partial_t`.

For `deg P>=3`, the leading and second-leading `t` coefficients of a
candidate core element are constants. Applying the third gate after one
bracket then forces `t` degree at most one; the linear forcing contributes
no surviving term to that decisive coefficient. For `deg P=2`, write
`P'=kz+l` and a static candidate as `A(z)+zB(t)+C(t)`. The exact formulas
are `C3DG=12bk^2 B''` and, after `B''=0`,
`C3D^2G=-12bk^3 C'''`. Hence the additional generators are exactly
`t,tz,t^2`.

The infinite tower is proved without circularity. Since
`Q star f(Q)=Qf(Q)-b hbar^2 f''(Q)/4`, star powers of `Q` form a triangular
basis of its ordinary polynomial algebra. This algebra is commutative for
the star product. Each odd transvectant therefore vanishes individually.
The resulting sectors are invariant under the forced derivation as
claimed. In particular the forcing makes the tower active, which is a
substantial counterexample to unrestricted pure-top collapse.

The independent checker adds 48 direct comparisons of the transformed
derivation and third gate with differentiation in the original coordinates,
plus 262 odd-gate checks on tower and extension generators through two
further brackets.

## Arbitrary analytic additive potential: the second depth is sharp

The additive-potential finite-determination theorem in
`depth_finite_determination.md` is also approved. For
`H=qF(p)+V(p)`, the first three tests `C3G=0`, `C5G=0`, and `C3DG=0`
force finite `q` degree at most three. Their solution space modulo the
invariant affine strip has dimension at most one: cancellation of two
cubic leading coefficients would leave a quadratic candidate, which the
same third-gate and first-bracket tests exclude.

The additional equation `C3D^2G=0` places `DG` in that same first-three-test
space, since its `q` degree is at most three and fifth gates are then
automatic. Thus `DG=lambda G+strip`, and all later iterates pass every
gate. This proves the four-test stopping rule. The extension across
isolated zeros of `F''` follows by restriction to a subinterval where it
does not vanish and then by analyticity. The identically affine `F` case
is separately elementary, as stated in the note.

Independent sparse fractional-power differentiation verifies the sharp
example `H=q p^(-1/4)+p^(7/4)` and
`G=q^3p^(-3/4)-(21/25)q^2p^(5/4)`: its first three tests vanish, while
`C3D^2G=(63/8)p^(-9/2)` is nonzero. This is a genuine failure of a
first-bracket stopping rule when the potential is arbitrary.

## Explicit algebraic active cubic

The strengthened `analytic_bridge.md` is approved, including the family
`F=a p^(-1/4)+bp`, `a!=0`, on the positive axis. Independent simplification
gives the sector obstruction
`Kc=a(3-c)p^(-5/4)/2-b(7c-6)/4`; precisely the cubic degree survives.
The claimed eigenvalue, the nonlinear canonical quadratic representation,
and the second-power Moyal anomaly all have the stated constants and signs.
The general higher-degree fractional-power example has fifth-gate
coefficient `-8(c)_4(rho)_4`, with `rho=(2-c)/(c+1)`, so all-depth
third-order exactness does not imply full Moyal exactness.

The gamma/polygamma specialization FP is approved as well. The integer-pole
coefficient is nonzero in every integer degree at least two. For the
logarithmic template `F=-a log p+b(p)`, direct expansion of `F'''/F''`
gives the stated logarithmic-over-`p` leading term; at degree two the
remaining `2a/p` term is nonzero. The continuation requirement belongs to
the coefficient function `F`, while the additive potential remains
arbitrary analytic on the working interval.

## Arbitrary polynomial shear and the exact six-dimensional square sector

The further shear-square theorem is approved. Let `Q=p+u(q)`,
`deg u=n>=3`, and `H=AQ^2+BQ+C+epsilon q`, `A!=0`. In coordinates
`(q,Q)` the exact operators are

```
D  = epsilon partial_Q-(2AQ+B)partial_q,
C3 = (2AQ+B)u''' partial_Q^3-6A u'' partial_q partial_Q^2.
```

The proposed sector is every polynomial of total degree at most two in
`(q,Q)`, namely `span{1,q,Q,q^2,qQ,Q^2}`. The transformed derivation
preserves it, and the third gate kills it. Every higher odd gate kills it
in the original coordinates as well: both arguments have degree at most
two in `p`, so an odd gate of order at least five requires more than two
`p` derivatives on one argument.

Completeness follows from the stated total-degree filtration in `(q,Q)`.
The derivation has top part `D0=-2AQ partial_q`, of degree shift zero.
If a core element had homogeneous top `G_N`, `N>=3`, choose its highest
`q` exponent `a`. Then `D0^a G_N` is a nonzero multiple of `Q^N`.
The top third gate, of degree shift `n-5`, sends that monomial to a
nonzero multiple of `q^(n-3)Q^(N-2)`. Lower filtration pieces cannot
cancel this component. This remains true at `n=3`, when the gate shift
is negative: every lower-degree piece still has strictly lower output
degree. Thus a core element cannot have transformed degree above two.

This proof uses repeated third gates only for the upper bound and direct
derivative exactness for the six-dimensional lower bound. It never assumes
nonlinear covariance or closure under ordinary multiplication. The linear
forcing is fully included; it changes only the lower filtration part of
the derivation. Direct independent checks in `review_checks.py` compare
both transformed operators with original-coordinate differentiation and
check the whole protected sector under repeated brackets.

The stronger uniform depth-two corollary is approved. On a leading
monomial `q^a Q^c`, the top operator `C0 D0^r` has coefficient proportional
to

```
(a)_r (c+r)_2 [(n-2)(c+r-2)-3(a-r)].
```

Its output shift is independent of `(a,c)` at fixed `r`, so cancellation
between different input monomials is impossible. For total degree at least
three, these coefficients cannot vanish simultaneously at `r=0,1,2`.
For `c>=3`, a zero at `r=0` forces `a>=1`, and the bracket at `r=1` is
`n+1`. For `c=2`, positive `a` already fails at `r=0`; for `c=1`, the
required `a>=2` fails at `r=1`; and for `c=0`, `a>=3` fails at `r=2`.
The full three-test kernel is therefore exactly the six-dimensional sector.

The depth is sharp for every allowed shear and every linear forcing:
`q^3` passes the first two tests, while
`D^2q^3=6q(2AQ+B)^2-6A epsilon q^2` and hence
`C3D^2q^3=-288A^3u''`, which is nonzero. Independent original-coordinate
differentiation checks this identity in twenty parameterized fixtures,
alongside an exact grid of the monomial factors. This grid supplements the
case argument above rather than replacing its all-degree proof.

\clearpage

# Bounded review of Claude's subsequent near-edge theorem

This read-only follow-up inspected commit
`268d553eb6a4434afeaf5fcb4689a6294e5ab688`, specifically Theorem NE in
`programmes/DYNAMIC_CORE_RESULTS.md` section 6.7 and the new checker
`extensions/hamiltonian/check_near_edges.py`. It supplements the overlap
review; it is not a claim that the remaining pure-top conjecture is true.

**Assessment:** the near-top theorem is supported by the determinant
identities and the filtration argument, subject to the two explicit proof
clarifications below. Neither clarification supplies a counterexample to
Theorem NE. The unrestricted pure-top conjecture still has the exact
counterexamples recorded in the overlap package.

The checker was extracted, unchanged, with its PBW arithmetic dependency
to a temporary directory. Its full replay passed: `E1`, `E2`,
`E2_at1`, `E3`, and `E4`, including 150 direct operator grid checks.
The run took approximately 0.44 seconds. No current worktree source file
was overwritten during this review.

## First-edge and lattice issues

The first edge has a strictly positive weight. A lower monomial of
transverse exponent at most one cannot tie `m ell^(d-1)` as the ratio of
the positive weights is decreased from one. A non-affine monomial has
exponent at least two and ties at a positive ratio below one. Thus the
primitive edge step `(a,-b)` satisfies `b>a>=1`.

A weight-homogeneous polynomial is supported on a single primitive
lattice line. Its total-degree top lies in the near monomial core
`K[ell]+mK[ell]`, so it has one of the two stated types. Different
transverse congruence classes, including the two possibilities when the
primitive step has transverse size greater than one, are precisely the
separate alpha and beta cases. No half-integer step or unaccounted coset
is needed.

The determinant at fixed edge parameters is a nonzero polynomial in the
top ordinary degree `N`. Its displayed leading coefficient is nonzero
for all admissible integer parameters. It therefore has only finitely
many exceptional degrees. An explicit uniform bound in all edge
parameters is not needed for the finiteness assertion. Since the core of
the edge Hamiltonian is graded by a positive edge weight, a common bound
on the ordinary degrees of its homogeneous elements bounds the entire
core and makes it finite-dimensional.

The first nonzero edge coefficient may occur after a gap. This does not
introduce additional terms into the first-order determinant: at step
`t`, every term of `C3(E,G)` or `C3(E,D_E G)` uses only `G_0` and `G_t`,
because all intermediate edge coefficients of `E` vanish. In the
second-order exceptional case `a=t=1`, the four declared unknowns
`y2,e1*y1,e2*g,e1^2*g` cover every contribution. If the formal second
edge monomial does not exist, its coefficient `e2` is simply zero; an
invertible four-column system still forces `e1^2*g=0`.

## Clarification 1: intermediate coefficients need not all clear

The sentence asserting that the third-gate recurrence clears every
coefficient between steps zero and `t` is stronger than necessary and is
not always true. For alpha type with `a=1` and `t>=2`, the intermediate
monomial `m ell^(N-b)` is in the static near strip and passes every gate
of the unperturbed near monomial. It is not forced to vanish by that
recurrence.

The first-order determinant remains valid because this intermediate
coefficient cannot occur in either step-`t` equation. The sentence should
be replaced by the decoupling argument in the preceding paragraph. The
exceptional second-order calculation already includes its first-step
coefficient explicitly.

## Clarification 2: separate the cubic case in Lemma F

The proof of Lemma F, used after edge finiteness, should separate degree
three. For the near cubic top `m ell^2`, the top derivation has the finite
chain

```
m -> -2m ell -> 2m ell^2 -> 0.
```

Thus the lemma's stated unbounded-chain argument for every degree
`N` outside `{2,d}` is not valid at `d=3,N=1`. For `d>=4`, the argument
works: the only positive-degree chain starting points that can encounter
the stationary top degree `d` are `N=2` and `N=d`.

Theorem NE at degree three is already Theorem Q. Every non-affine
perturbation of a near cubic has a nonzero `m^2` term and otherwise terms
affine in `m`; that is exactly the degree-three case covered by the
retained binomial certificate. Stating "degree three follows from
Theorem Q; apply Lemma F's chain argument for degree at least four"
repairs the dependency without new computation or assumptions.

With these clarifications, no conceptual blocker was found in the
near-top completion. This bounded review checked the proof mechanism
and replayed its symbolic identities; it does not establish historical
priority or replace external mathematical review.

\clearpage

# Independent review of the structural extensions

This review concerns the new polynomial shear, oscillator, analytic-potential,
quadratic-frontier and deformation results developed after the first overlap
package. The review checks the all-degree arguments separately from their
finite calibrations. All polynomial statements are in characteristic zero and
retain the original flat Weyl–Moyal product in the original affine coordinates.
The analytic statements concern finite degree in `q` with real-analytic
coefficients on a connected positive interval. Historical priority and external
peer review are not established.

## Shear-composition closure

For `Q=p+u(q)`, `m=deg u>=3`, `H=P(Q)+epsilon*q`, and `mu=deg P>=3`,
the ordinary chain rule gives the transformed third gate

\[
 C_3=u'''(P'\partial_Q^3-P'''\partial_Q)
 -3u''(P''\partial_q\partial_Q^2+P'''\partial_q\partial_Q)
 -P'''\partial_q^3.
\]

The derivatives on the right keep `Q` fixed. This is an operator identity for
the original affine gate, not an assertion that nonlinear substitution
preserves the flat Moyal product. Under total degree in `(q,Q)`, the first
two groups have top shift `m+mu-7`; the last has shift `mu-6`, lower by
`m-1>0`. Lower terms of `P,u` have smaller shifts. The top derivation is
`D0=-mu*p_mu*Q^(mu-1)*partial_q`, of shift `mu-2`.

The top gate sends each monomial `q^a Q^c` to one monomial, with coefficient
proportional to

\[
 c(c+\mu-3)R(a,c),\qquad
 R(a,c)=(m-2)(c-\mu)-3(\mu-1)a.
\]

The nonzero output shift is independent of the input exponents, so distinct
inputs cannot cancel. For `a,c>0`, the second test replaces `R` by
`R+(mu-1)(m+1)`, and these cannot both be zero. For `c=0,a>=1`, its
second-test bracket is `-(m-2)-3(mu-1)(a-1)<0`. For `a=0,c>0`, the
first test leaves only `c=mu`. Consequently the simultaneous top kernel
contains only `1,Q^mu`. Subtract a leading multiple of `H`, which itself
passes both tests, and descend in total degree. This proves the claimed
all-degree equality with `span{1,H}`. Negative operator shifts at small
`m,mu` cause no exception: every nonzero actual output has nonnegative
monomial exponents.

The two tests are uniformly indispensable in this family. `Q` fails `C3`
but has `DQ=epsilon`, hence passes `C3D`. Conversely `q` passes `C3`,
while `C3Dq=u'''(P'''P''-P'P'''')` is nonzero: its leading coefficient in
`Q` is `2*p_mu^2*mu^2*(mu-1)*(mu-2)`. These arguments do not depend on a
finite parameter sample.

## Oscillator maximality and the two depth bounds

For

\[
 H=AQ^2+BQ+C+\frac\kappa2q^2+\epsilon q,
\]

with `A!=0`, the transformed operators are

\[
 D=-(2AQ+B)\partial_q+(\kappa q+\epsilon)\partial_Q,
 \qquad C_3=(2AQ+B)u'''\partial_Q^3
                  -6Au''\partial_q\partial_Q^2.
\]

The degree-at-most-two space in `(q,Q)` is invariant under `D` and killed
by every gate: for orders at least five, the total available `p` degree
of `H` and an element of the space is at most four. This proves the
six-dimensional lower bound directly in the original convention.

For `m>=3`, let `u_m=alpha*q^m` and use total degree in `(q,Q)`.
The top gate on `q^aQ^c` is proportional to

\[
 c(c-1)[(m-2)(c-2)-3a],
\]

with fixed exponent shift. In homogeneous degree `N>=3`, its kernel
contains `q^N`, `q^(N-1)Q`, and at most one resonance with `c>=3,a>=1`.
The top derivation is `D0=-2AQ partial_q+kappa*q partial_Q`. The resonance's
`-2AQ partial_q` contribution has the unique highest `Q` exponent in
`C0D0` of any remaining candidate, so it cannot cancel. Its coefficient
is nonzero because the resonance bracket changes by `m+1`. Remove it.
Then `C0D0` removes `q^(N-1)Q`; finally `C0D0^2` removes `q^N`.
This proves depth two suffices, even when `kappa!=0`; one cannot simply
reuse the original SS proof with its monomial derivation without this
extra no-cancellation argument. The cubic `q^3` proves sharpness for
all these parameters:

\[
 C_3q^3=C_3Dq^3=0,\qquad C_3D^2q^3=-288A^3u''\ne0.
\]

For quadratic `u=bq^2+cq+d`, `b!=0`, and `kappa!=0`, the gate is the
constant-coefficient operator `-12Ab partial_q partial_Q^2`. In homogeneous
degree `N>=3`, its kernel has the three monomials `q^N,q^(N-1)Q,Q^N`.
At `N>=4`, `C3D0` maps the latter two to distinct monomials and removes
them; `C3D0^2` removes the first. At `N=3` there is a resonance requiring
one further step. Lower affine terms `B,epsilon` have smaller shifts,
so the same leading argument proves the degree bound for arbitrary
`B,epsilon`, rather than only for a centered sample.

For `B=epsilon=0`, the explicit witness

\[
 G=Q^3+\frac{3\kappa}{4A}q^2Q
\]

passes the first three depth tests and has

\[
 C_3D^3G=-432A^2b\kappa^2\ne0.
\]

Equivalently multiply by `4A` to obtain the advertised
`-1728A^3b*kappa^2`. This proves the depth-three bound is sharp across
the quadratic-shear oscillator class. The unforced case `kappa=0` must
remain on its retained infinite-core QC route; it cannot be assigned
six dimensions. Affine shears are quadratic Hamiltonians and likewise
lie outside this nonlinear oscillator theorem.

The closed equations `Dq=-(2AQ+B)`, `DQ=kappa*q+epsilon` give
`D^2q=-2A*kappa*q-2A*epsilon`. Oscillatory terminology is justified for
real parameters only when `2A*kappa>0`. Exact sector closure itself
is algebraic and does not require a sign, analytic convergence, or a
self-adjoint realization of a quantum operator.

The spectral extension is also consistent with the exact quadratic-sector
representation. For `kappa!=0`, set `omega^2=2A*kappa`; affine centering
removes `B,epsilon`. Over an algebraic closure choose `r^2=-omega^2`.
The linear forms `Lplus=y-r*x/(2A)` and `Lminus=y+r*x/(2A)` have
derivation eigenvalues `r,-r`. Their quadratic products give eigenvalues
`2r,0,-2r`, while the constant has eigenvalue zero. Thus the
characteristic polynomial is `z^2(z^2+omega^2)(z^2+4omega^2)` and the
minimal polynomial is `z(z^2+omega^2)(z^2+4omega^2)`. This conclusion
uses `A*kappa!=0`; the nilpotent zero-oscillator case has its retained
separate Jordan description. Observer certificates establish only their
explicit finite models and target contracts.

## Analytic exceptional potentials

Let `F''` be nowhere zero, `r^3=F''`, and
`FF'''/(3F'')-3F'=lambda` constant. Modulo the invariant strip
`W=A+qA`, an extra cubic can be normalized as `q^3r+q^2h`.
Direct third-gate and derivation expansions yield exactly

\[
 h'=\frac{V'''r}{F''},\qquad
 Fh'-(2F'+\lambda)h=3V'r.
\]

The second condition says that `DG-lambda*G` is in `W`; together they
are sufficient for every future gate test. Necessity uses the retained
analytic finite-determination theorem: any additional element has degree
three, its cubic coefficient is unique up to scalar, and a degree-two
residual cannot persist. This is a regular-chart criterion, not a
claim of global classification for arbitrary `F` through zeros of its
second derivative or singularities.

For `F=p^(-1/4)`, normalize the cubic coefficient to `p^(-3/4)`.
Eliminating `h` gives

\[
 p^4V''''+3p^3V'''-\frac{15}{16}p^2V''
                    -\frac{15}{32}pV'=0.
\]

The logarithmic variable `x=log p` turns this into a constant-coefficient
fourth-order ODE. Its distinct indicial roots are
`0,-1/4,3/4,5/2`, so all real-analytic solutions on any connected
positive interval are precisely

\[
 V=c_0+a p^{-1/4}+b p^{3/4}+c p^{5/2}.
\]

This proves completeness in the analytic function space, not merely
among tested power ansatzes. For these potentials the proposed cubic
representative has the same `q^3,q^2` coefficients as `(H-c0)^3`;
their difference is in `W`. Thus the additional generator can be taken
stationary. The harmless constant in the Hamiltonian must be removed
before cubing: `H^3-(H-c0)^3` generally contains a forbidden `q^2` term.
If `V` fails the ODE, the compatibility system has no extra generator,
so the retained quotient bound proves the full core is exactly `W`.

## Complete constant-quadratic-momentum classification

For constant nonzero `A`, write `H=A(p+u(q))^2+V(q)`, with
`m=deg u>=3` and now **arbitrary polynomial** `V`. The initial
weighted-top argument gives a finite bound when `deg V<2m`, but the
following direct leading-transverse-degree argument removes that
restriction completely, including the former degree-resonant boundary.

In `(q,Q)`, the exact third gate is

\[
 C_3=(2AQ u'''+V''')\partial_Q^3
                       -6Au''\partial_q\partial_Q^2.
\]

If a polynomial `G` in `ker C3 intersect ker(C3D)` has highest
`Q` degree `N>=3` and coefficient `g(q)` of degree `a`, the leading
`Q^(N-2)` coefficient in its third gate is

\[
2A(N)_2\big((N-2)u'''g-3u''g'\big).
\]

The `V'''` term lowers `Q` degree by three and cannot affect it.
Comparing leading `q` coefficients gives `3a=(N-2)(m-2)>0`, so
`g'` is nonzero. The highest `Q` coefficient of `DG` is then
`-2Ag' Q^(N+1)`. Applying its third-gate condition gives
`3(a-1)=(N-1)(m-2)`. Subtracting the two identities forces
`-3=m-2`, impossible for `m>=3`. Thus `G` has `Q` degree at most
two. At degree two the leading gate is `-12Au''g'`, which forces
its quadratic coefficient to be constant.

The next two finite tests give the remaining coefficient constraints.
For `G=cQ^2+b(q)Q+f(q)`,

\[
 C_3DG=24A^2u''b'',\qquad
 C_3D^2G=48A^2u''(cV'''-Af''')\quad\text{when }b''=0.
\]

Consequently every polynomial passing depths zero through two lies in
`span{1,H,q,Q,q^2,qQ}`. This is an all-degree candidate theorem,
not a bound inferred from a finite matrix.

Modulo a Hamiltonian multiple and constant, write
`G=(alpha*q+beta)Q+a*q^2+b*q`. Its derivative, after subtracting
`-2alpha H`, has pure-`q` part

\[
R=2\alpha V+(\alpha q+\beta)V'.
\]

Passing the next depth forces `R` to have degree at most two. If
`n=deg V>=4`, its highest two coefficients force `alpha=beta=0`.
One further depth forces `a=b=0`. If `n=3`, successive depths first
force `alpha=0`, then `a=0`, then `beta=0`, and finally `b=0`.
The nesting fact used here is exact: if `G` passes depths zero through
`R`, then `DG` passes depths zero through `R-1`. Thus the complete
constant-quadratic-momentum classification is six dimensions for
`deg V<=2`, and exactly `span{1,H}` otherwise. The sharp uniform
third-gate depths are respectively `2`, `6` for cubic `V`, and `4`
for `deg V>=4`.

These depths have universal witnesses. For quadratic or lower `V`,
`q^3` has `C3D^2q^3=-288A^3u''` and passes the previous depths.
For degree at least four, `q` passes depths zero through three, but

\[
 C_3D^4q=96A^4u''V''''\ne0.
\]

For cubic `V`, writing `w=V'''!=0`, the same `q` passes depths zero
through five, while

\[
 C_3D^6q=-960A^5u''w^2\ne0.
\]

The first four derivatives of `q` are
`-2AQ`, `-2AV'`, `4A^2QV''`, and
`4A^2(V'V''-2AQ^2V''')`. In the cubic case the last expression has
quadratic `Q` coefficient `c=-8A^3w` and pure-`q` coefficient with
third derivative `12A^2w^2`, giving exactly the stated depth-six
value from the preceding general coefficient identity.

There is no remaining resonant boundary in `deg V`. Variable leading
momentum coefficients and analytic nonpolynomial residual potentials remain
distinct scopes. Quadratic and affine shears are resolved by the supplements
reviewed next.
The certificate procedure can start from the proof-backed finite
candidate space above and retain full outputs. A stable subspace that
is invariant under `D` and killed by every gate is exactly the core;
no arbitrary polynomial degree box is needed.

## Quadratic shears and the exact cubic parameter certificate

For `deg u=2`, `u''` is a nonzero constant and
`C3=V''' partial_Q^3-6Au'' partial_q partial_Q^2`. If `deg V>=4`,
a hypothetical highest term `g(q)Q^N`, `N>=3`, first has `g` constant.
Its next coefficient `h(q)Q^(N-1)` must satisfy
`h'=N V'''g/(6Au'')`. The top coefficient of `DG` is then
`-N V'''g/(3u'')` in degree `N`; applying its third gate would force
`V''''g=0`. This contradiction reduces the joint depth-one kernel
to degree at most two with constant quadratic coefficient. All subsequent
QF coefficient steps and its sharp depth-four witness remain valid.

For cubic `V`, translating `q` and making an affine momentum shear first
reduces to `A(p+bq^2)^2+v q^3+e q`, modulo a constant. The nonzero
rational scales `s=v/(Ab^2)` and `t=bs^2`, followed by division by
`At^2`, give `(p+q^2)^2+q^3+lambda q`, where
`lambda=eA^2b^4/v^3`. The retained `GL2` covariance, not merely
symplectic covariance, is used for these final independent scales.
Vanishing conditions and bracket depth survive all these transformations.

In the normalized `(q,Q)` variables, weights `(1,2)` give leading
operators `D0=-2Q partial_q` and `C0=-12 partial_q partial_Q^2`.
Their common kernel through depth two is the retained unforced QC core.
Thus a candidate of weight above six has top `Q^N`, `N>=4`. The
first-deficit static gate uniquely forces the next component to be

\[
\frac N2qQ^{N-1}+\beta q^{2N-1}+\gamma q^{2N-3}Q.
\]

The next derivation has a top contribution `3Nq^2Q^(N-1)`, whose
leading gate is `-72N(N-1)(N-2)qQ^(N-3)`. Other permitted terms
have zero gate or output with `Q` degree zero. Since `N>=4`, they
cannot cancel that nonzero contribution. Hence every depth-two candidate
has weight at most six, giving the sixteen-dimensional full candidate
space before any finite matrix is used.

The fourteen-row minor has the nonzero constant determinant specified in (QR10). Its row depths
sum to `32`. Each depth-`r` entry has parameter degree at most `r`
because `D=Da+lambda partial_Q` and `C3` is parameter independent.
Consequently thirty-three exact rational agreements prove the constant
polynomial identity for every `lambda`. The independent review checker
recomputes all thirty-three determinants using its own polynomial and
fraction arithmetic and obtains the same constant. This is a rigorous
interpolation certificate with a proved degree bound, not a numerical
rank extrapolation. Full rank fourteen together with independent kernel
vectors `1,H` gives exactly their span. The universal depth-six witness
is the same `q` and formula `-960A^5u''(V''')^2` as in QF.

This closes every quadratic shear with nonlinear polynomial potential.
Together with retained QC and the oscillator theorem, all quadratic-shear
residual degrees are classified. The characteristic-zero assumption
justifies both the rational normalization and the polynomial root count.

## Affine shears and the remaining constant-quadratic branch

For affine `u`, the change to `(q,Q)` is affine canonical. The exact
third gate is `C3=V''' partial_Q^3`. If `deg V<=2`, the Hamiltonian
is quadratic and every polynomial is exact. Otherwise its static kernel
has `Q` degree at most two, so write `G=c(q)Q^2+b(q)Q+f(q)`.
Successive third-gate equations are

\[
 C_3DG=-12AV'''c',\qquad
 C_3D^2G=24A^2V'''b'',\qquad
 C_3D^3G=48A^2V'''(cV'''-Af'''),
\]

with each later identity conditional on the preceding vanishings.
They force `c` constant, `b` affine, and `f'''=(c/A)V'''`.
Thus the depth-three space is exactly `span{1,H,q,Q,q^2,qQ}`.
The same exact preimage chain used in QF then gives depth five for
potentials of degree at least four and depth seven for cubics, always
with full core `span{1,H}`. The sharp witness `q` has

\[
 C_3D^5q=96A^4V'''V''''\quad(\deg V\ge4),\qquad
 C_3D^7q=-960A^5(V''')^3\quad(\deg V=3),
\]

and passes all preceding depths. The review checker independently
verifies these formulas for constant and genuinely affine shears, with
nontrivial rational kinetic coefficient and lower potential terms.

The three completed-square cases `deg u<=1`, `deg u=2` and `deg u>=3`
therefore exhaust every Hamiltonian `A p^2+B(q)p+C(q)` with nonzero
constant `A`. This completeness is a consequence of the proved routes;
it does not extend to a nonconstant leading momentum coefficient.

## First- and second-order deformation obstructions

Fix `Q=p+q^2` and `H_t=Q^2+t*q^2/2`. In fixed `(q,Q)` coordinates,

\[
 C=-12\partial_q\partial_Q^2,\quad
 D_t=D_0+tD_1=-2Q\partial_q+tq\partial_Q.
\]

The depth-zero-through-three operator vector `L_t` is uniform for this
family, including its exceptional fiber. A polynomial jet is required
to satisfy the coefficients of these exact operators modulo its stated
power of `t`; no observable-degree truncation is part of the definition.

Modulo the six-dimensional exact quadratic space, a zeroth-order
candidate is `f(Q)`. A first-order correction `X` must satisfy `CX=0`,
hence has form `a(q)+Qb(q)+g(Q)`. The coefficient of `t` in `CD_t`
is

\[
48b''(q)-12f'''(Q)=0.
\]

Its two sides depend on independent variables, so `f'''` must be
constant. This excludes every higher power and every nontrivial linear
combination of powers of degree at least four without a degree cutoff.
The only additional first-order direction is `Q^3`, which lifts as
`Q^3+(3/4)tq^2Q`.

For this lift, direct differentiation gives

\[
 D_tG=\tfrac34t^2q^3,\quad
 D_t^2G=-\tfrac92t^2q^2Q,\quad
 C D_t^3G=-432t^2.
\]

The constant-extraction functional in the third depth component
annihilates `L0 X` for every polynomial `X`, because `CD0^3X` is
divisible by `Q`. Any other first-order lift differs by an element of
the retained unforced QC core. The first variation of the third-depth
component vanishes on that entire core: it vanishes on the quadratic
sector for all `t`, and `D0^2D1f(Q)=0`. Hence no choice of first-order
lift changes the second-order obstruction. First-order liftable
zeroth-order observables form exactly a seven-dimensional space;
second-order liftable observables form exactly the six-dimensional
quadratic sector, which lifts to every order.

This is a genuine obstruction to deforming an exact observable sector.
Smith invariant factors of a finite presentation encode it, but no new
geometric torsion, general deformation theory, or novelty of Smith
normal form is claimed.

The graded extension is also sound. On homogeneous input degree `n>=4`,
the four outputs have degree `n-3`, so the matrix has `n+1` columns
and `4(n-2)` rows. At `t=0` its kernel is exactly the line `K Q^n`,
so its rank is `n`. At every nonzero parameter over the algebraic
closure, the oscillator theorem makes it injective in this degree.
Therefore all Smith factors except one are units, and the last is a
power `t^e`; a different nonunit factor would have a nonzero root
where rank dropped. Invertible polynomial Smith source/target changes
identify the exceptional initial line with that last factor. An
exponent `e>=2` would supply a first-order lift of its nonzero initial
direction, contrary to the all-degree obstruction above. Hence `e=1`.
For degree three the explicitly certified exponent is two. This proves

\[
\operatorname{Tor}\operatorname{coker}L_t
\cong (K[t]/(t^2))_{\text{degree }3}
\oplus\bigoplus_{n\ge4}(K[t]/(t))_{\text{degree }n}.
\]

The free cokernel rank in each degree `n>=4` is
`4(n-2)-(n+1)=3n-9`. The target must be the full direct sum of four
homogeneous output spaces; this calculation would be invalid if a
bounded matrix silently omitted output monomials.

## Independent arithmetic calibration and limits

`extension_proof_review.py` implements its own sparse rational arithmetic
and direct original-coordinate mixed derivatives. It imports none of
the new producers. It checks the transformed composition operator,
full-output joint kernels, lower affine oscillator parameters, both
sharp-depth witnesses, the Euler indicial factorization, allowed mixed
potentials and a rejected potential. It additionally checks the sharp quadratic-frontier depths at cubic, quartic, resonant and supercritical potential degrees, and the formal cubic lift residual coefficient by coefficient in the parameter. It also independently replays the quadratic-shear cubic minor at all thirty-three required parameter values and checks the affine-shear sharp-depth formulas. The receipts record finite
calibrations only. The universal claims above depend on their written
filtration, ODE and obstruction proofs. A recognizer failure is not a
certificate of collapse, and a failed optional search is not a theorem.

\clearpage

# Source and priority boundary

The source branch reviewed here is
[`claude/adoring-ritchie-1hq1kw`](https://github.com/towre676-cloud/nonlinearhamiltonian/tree/claude/adoring-ritchie-1hq1kw),
pinned at `e91e14d`.
The subsequent near-top completion at `268d553` is integrated and separately
reviewed. The retained monomial theorem, affine covariance and associated-graded
reduction are dependencies of the polynomial classifications. The new
analytic arguments are supplied explicitly and do not substitute analytic
coefficients into polynomial Weyl-ideal receipts.

The literature checks below establish background overlap, not priority for
the fixed-H classifications in this package. No literature-priority claim
has been made. These primary sources were inspected on 22 October 2026.

Mark J. Gotay, *On the Groenewold-Van Hove problem for R^{2n}*,
J. Math. Phys. 40 (1999), 2107-2116,
[arXiv:math-ph/9809015](https://arxiv.org/abs/math-ph/9809015).
The quantization obstruction and quantizable polynomial Lie subalgebras are
mature background. In particular the coordinate-affine algebra underlying
the strip is not a new construction.

T. Dereli, T. Hakioglu and A. Tegmen, *Quantum canonical transformations in
Weyl-Wigner-Groenewold-Moyal formalism*,
[arXiv:0904.3416](https://arxiv.org/abs/0904.3416), especially sections 2-4.
Gauge and point transformations, star-exponential representations and
nonlinear function transforms are existing theory. The protected-sector
shear explanation in this package is an explicit application of that
theory; it is not a claim to have invented quantum canonical transformations.

T. Hakioglu, *Extended covariance under nonlinear canonical transformations
in Weyl quantization*, [arXiv:quant-ph/0011076](https://arxiv.org/abs/quant-ph/0011076),
version 3 (2001), section VI(b) and equations 62 and 84. The gauge-transform
operator and its explicit higher-derivative quantum correction already
appear in this source. The protected shear mechanism is therefore established
background, not a novelty candidate. T. Hakioglu and A. Dragt,
*The Moyal-Lie Theory of Phase Space Quantum Mechanics*,
[arXiv:quant-ph/0108081](https://arxiv.org/abs/quant-ph/0108081), provides a
broader Lie-algebraic treatment of these quantum transformations.

Didier Robert, *When Poisson and Moyal Brackets are equal?*,
[arXiv:2207.08798](https://arxiv.org/abs/2207.08798), version 2 (2023),
Theorem 1.1. Equality against every Schwartz observable under the paper's
symbol hypotheses forces a quadratic Hamiltonian. Our fixed nonlinear H
and restricted observable sectors have different quantifiers and do not
contradict that theorem. The local analytic formal-gate setting here also
differs from its global symbol assumptions.

The present claims concern algebraic/formal gate identities for every power
of hbar separately, and repeated Hamiltonian brackets. Global self-adjoint
operator domains, convergence of a star series for arbitrary smooth
functions, spectral predictions, and experimental realizability are outside
the claims. Finite-q-degree analytic observables have finitely many gates
against H=qF+V, so no infinite gate summation is used there.


## Cubic-phase background and scope

Domański and Błaszak, *On local equivalence of star-products on Poisson manifolds*,
[arXiv:1305.4026](https://arxiv.org/abs/1305.4026), and Błaszak and Domański,
*Canonical transformations in quantum mechanics*,
[arXiv:1208.2835](https://arxiv.org/abs/1208.2835), supply established
star-product-equivalence and quantum-canonical background. They are not
used as proof of the specific full-core classification theorems here.
Ovsienko and Roger, [arXiv:math/9812074](https://arxiv.org/abs/math/9812074),
equation (9.2), gives the conventional scalar Gelfand-Fuchs integral.
Our displayed vector-field defect integrates to zero under periodic or
compact-support boundary conditions; the independent review states the
precise distinction. Historical priority of the new scoped classifications
remains unestablished.
