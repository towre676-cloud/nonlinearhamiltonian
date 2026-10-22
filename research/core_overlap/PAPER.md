---
title: "Exact Sectors Beyond the Pure-Top Conjecture"
subtitle: "Nonlinear composition, protected canonical transport and sharp analytic stopping rules"
author: "Nonlinear Hamiltonian research programme"
date: "22 October 2026 - internally reviewed research draft"
fontsize: 10pt
colorlinks: true
linkcolor: NavyBlue
urlcolor: NavyBlue
toc-depth: 1
---

# Exact sectors beyond the pure-top conjecture

Research overlap with `claude/adoring-ritchie-1hq1kw`, inspected at
`e91e14d` on 22 October 2026.
All results use one canonical pair and the compendium's fixed flat Weyl
convention. Written proofs were reviewed independently inside this research
session; historical priority and external peer review remain open.

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

No Nijenhuis, Haantjes, or Moyal operation is claimed to be newly invented.
The useful research claims here are the fixed-H sector classifications,
their explicit counterfamilies, and the finite stopping theorems.

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
dimensions exactly. It also feeds the transposed matrix into the existing
`extensions/observer/observation_closure_reference.py` compiler and replays
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
