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
