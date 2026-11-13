# The cube-leading boundary: gate symbol, uniform weight-12 tail, and the coupled family

Base commit: `a36cc7a` (`origin/main`). Convention: flat Weyl transvectants
$T_k(F,G)=\sum_t(-1)^t\binom kt(\partial_q^{k-t}\partial_p^tF)(\partial_q^t\partial_p^{k-t}G)$,
$D_H=T_1(H,-)$, $S^r(H)=\{G:\ T_3(H,D_H^iG)=T_5(H,D_H^iG)=0,\ 0\le i\le r\}$,
$D_\infty(H)=\bigcap_rS^r(H)$, observables of unrestricted degree, $K$ a field of
characteristic $0$. Weights are $\operatorname{wt}(q,p)=(1,2)$.

Evidence classes used below: **[proof]** complete human argument; **[cert]** exact
symbolic identity or rank certificate replayed by `verify_cube_leading_boundary.py`;
**[Lean]** kernel-checked in `formal/SexticC3/CubeLeadingGate.lean`; **[finite]**
bounded exact experiment, not a proof of anything beyond the stated instance.

## 0. Normalisation and covariance

Let $H=(q^2+\kappa p)^3+R$, $\kappa\ne0$, $\operatorname{wt}R<6$.

**N1 (covariance).** For an invertible affine map $\phi$ of the plane with linear part of
determinant $\delta\ne0$, $T_k(F\circ\phi,G\circ\phi)=\delta^k\,T_k(F,G)\circ\phi$. Hence
$S^r(H\circ\phi)=S^r(H)\circ\phi$ and $S^r(cH)=S^r(H)$ for $c\ne0$; the maps need not
be symplectic. [proof: chain rule; each $T_k$ is the $k$-th power of the constant
bidifferential operator $\partial_q\otimes\partial_p-\partial_p\otimes\partial_q$.]

**N2.** $\phi(q,p)=(q,p/\kappa)$ gives $\kappa=1$ and preserves weights. Put
$P=p+q^2$. A polynomial of weight $<6$ in $(q,p)$ is one of weight $<6$ in $(q,P)$,
so $H=P^3+A(q)P^2+B(q)P+C(q)$ with $\deg A\le1$, $\deg B\le3$, $\deg C\le5$.

**N3 (depression).** $Y=P+A/3=p+q^2+(a_0+a_1q)/3$; the substitution
$p\mapsto p+(a_0+a_1q)/3$ is an affine symplectic map of the original plane, and
$H=Y^3+(B-A^2/3)Y+(C-AB/3+2A^3/27)$ with the same degree bounds. [cert]

**N4.** $q\mapsto q+s$, $p\mapsto p-2sq-s^2$ is affine symplectic, fixes $P$ and
translates $B,C$. $(q,p)\mapsto(sq,s^2p)$ sends $P\mapsto s^2P$ and, after dividing by
$s^6$, $(b_i,c_i)\mapsto(s^{i-4}b_i,s^{i-6}c_i)$.

The reduced family is therefore $H=P^3+B(q)P+C(q)$, $B=\sum_{i\le3}b_iq^i$,
$C=\sum_{i\le5}c_iq^i$, and every statement below transports back to the original
boundary by N1–N3.

## 1. Transported operators

In the chart $(q,P)$ one has $\partial_p=\partial_P$ and
$\partial_q|_p=\delta:=\partial_q+2q\partial_P$, with $[\delta,\partial_P]=0$. Substituting
into the definition and expanding gives, for the reduced family,

$$D=(B'P+C')\partial_P-(3P^2+B)\partial_q,$$
$$T_3=-6\,\partial_q^3-36\,\partial_q\partial_PP\partial_P-6\,(b_2+3b_3q)\,\partial_q\partial_P^2+6E\,\partial_P^3,$$
$$T_5=-360\,\partial_P^4\Bigl(\partial_q-\tfrac{\beta}{3}\partial_P\Bigr),\qquad\beta=b_3+c_5,$$

with the **gate symbol**

$$E=b_3P+(b_1+c_3)+(2b_2+4c_4)\,q+(3b_3+10c_5)\,q^2 .$$

These are the original flat transvectants, not flat transvectants of the chart.
[cert: equality with the definition on all $q^iP^k$, $i\le5$, $k\le6$, with all ten
parameters symbolic; operators of order $\le5$ are determined by these values.]
The gates do not involve $b_0,c_0,c_1,c_2$. Two consequences:
$T_3(H,g(P))=6E\,g'''(P)$ and $T_5(H,g(P))=120\beta\,g^{(5)}(P)$.

## 2. Theorem A (static sector)

**Theorem A.** For $H=P^3+B(q)P+C(q)$:

1. $\dim S^0(H)=\infty$ **if and only if** $E\equiv0$, that is
   $b_3=c_5=0,\ c_3=-b_1,\ c_4=-b_2/2$. In that case $S^0(H)=K[P]\oplus V_H$ with
   $\dim V_H=8$ and $V_H$ of weight $\le8$.
2. If $E\not\equiv0$ then every static $G$ has $\deg_PG\le6$ and weight $\le12$, and
   $\dim S^0(H)=15$ if $3b_3+5c_5=0$, $\dim S^0(H)=14$ otherwise. In the latter
   case the static weight bound improves to 10, and is sharp.

*Proof.* Put $u=P+\beta q/3$, so $(\partial_q-\tfrac\beta3\partial_P)$ is $\partial_q$ at
fixed $u$. $T_5G=0$ says $\partial_q|_uG$ has $u$-degree $\le3$; integrating in $q$,
$G=g(u)+\tilde G$ with $\deg_u\tilde G\le3$. Each term of $T_3$ maps $P$-degree $\le3$
to $P$-degree $\le3$, so $T_3G=0$ forces $T_3g(u)$ to have $u$-degree $\le3$. With
$\partial_qg(u)=\tfrac\beta3g'$, $\partial_Pg(u)=g'$,

$$-\tfrac16T_3\,g(u)=g'''(u)\Bigl[k_0+(2\beta-b_3)u+k_1q-e_2q^2\Bigr]+2\beta\,g''(u),\qquad e_2=3b_3+10c_5,$$

with $k_0=\beta^3/27+\beta b_2/3-(b_1+c_3)$, $k_1=-2\beta^2/3+4\beta b_3/3-(2b_2+4c_4)$
[cert, $g=u^m$, $m\le9$]. Suppose $m=\deg g\ge7$. The coefficient of $q^2$ is
$-e_2g'''$, of degree $m-3\ge4$ unless $e_2=0$. The coefficient of $u^{m-2}$ in the
$q^0$ part is $m(m-1)\,[2\beta(m-1)-b_3(m-2)]$ times the leading coefficient of $g$;
with $e_2=0$ this bracket equals $b_3(2m+3)/5$, so $b_3=0$, hence $c_5=0$ and
$\beta=0$ [Lean: `top_coefficient_nonresonant`]. The bracket is then
$-(b_1+c_3)-(2b_2+4c_4)q$, and a nonzero coefficient $e$ with $\deg(e\,g''')\le3$
gives $\deg g\le6$ [Lean: `static_function_degree_le_six`]. So $m\ge7$ forces
$E\equiv0$. This proves the $P$-degree bound in (2) and the "only if" in (1).

For (2), write $G=\sum_{k\le6}a_k(q)P^k$. The $P^k$-coefficients of $T_5G=0$ and
$T_3G=0$ are

$$a_{k+4}'=\tfrac\beta3(k+5)\,a_{k+5},$$
$$a_k'''=-6(k+1)^2a_{k+1}'-(k+2)(k+1)(b_2+3b_3q)\,a_{k+2}'+b_3(k+2)(k+1)k\,a_{k+2}+E_0(q)(k+3)(k+2)(k+1)\,a_{k+3},$$

$E_0=E-b_3P$. Hence $a_6$ is constant, $\deg a_5\le1$, $\deg a_4\le2$, and then
$\deg a_3\le5$, $\deg a_2\le7$, $\deg a_1\le9$, $\deg a_0\le11$: weight $\le12$.
The system is triangular; the free constants are one each for $a_6,a_5,a_4$ and
three each for $a_3,\dots,a_0$, and the only compatibility condition is the $k=4$
equation, $0=a_4'''=(120b_3-300\beta)a_6$, i.e. $(3b_3+5c_5)a_6=0$. This gives 15 or 14.
If $3b_3+5c_5\ne0$, then $a_6=0$ and the same equations give degree bounds
$0,1,3,5,7,9$ for $a_5,a_4,a_3,a_2,a_1,a_0$, respectively. Thus the weight is
at most 10. The free constant $a_5$ can be chosen nonzero, so this static bound
is attained.

For (1) with $E\equiv0$: $T_5=-360\,\partial_P^4\partial_q$ and $T_3=-6M\partial_q$,
$M=\partial_q^2+6\partial_PP\partial_P+b_2\partial_P^2$, so $K[P]\subset S^0$ and
$S^0=K[P]\oplus V_H$ where $V_H$ consists of the $q$-divisible $G$ with
$W=\partial_qG=\sum_{k\le3}w_kP^k$ and $w_k''=-6(k+1)^2w_{k+1}-b_2(k+2)(k+1)w_{k+2}$:
two constants for each of $w_3,\dots,w_0$, degrees $\le1,3,5,7$. $\square$

[finite cross-check: the dimension law is reproduced by the flat engine in the
original coordinates on 16 members, with windows of weight 12 and 15 agreeing.]

## 3. Theorem B (first refinement on the locus $E\equiv0$) and the uniform tail

**Theorem B.** Let $E\equiv0$. Then $\dim S^1(H)<\infty$ **if and only if**
$(b_1,b_2,c_2)\ne(0,0,0)$, and in that case $S^1(H)\subset K[P]_{\le6}\oplus V_H$, of
weight $\le12$. The excluded family is exactly $H=P^3+b_0P+c_1q+c_0$, for which
$K[P]+Kq\subset D_\infty(H)$.

*Proof.* Let $G=g(P)+\tilde G\in S^1$, $\tilde G\in V_H$. Every element $F$ of
$S^0$ has $\deg_P\partial_qF\le3$. Now $DG=(B'P+C')g'(P)+D\tilde G$ and
$\deg_PD\tilde G\le5$, so $(B''P+C'')\,g'(P)$ has $P$-degree $\le5$. On the locus,
$B''P+C''=2b_2P+2c_2-6b_1q-6b_2q^2$. If $\deg g\ge7$ the coefficients of $q^2$, $q$,
$q^0$ give successively $b_2=0$, $b_1=0$, $c_2=0$. Conversely, in the excluded
family $D(P^m)=c_1mP^{m-1}$ and $Dq=-(3P^2+b_0)$, so $K[P]+Kq$ is $D$-stable and
static. $\square$

**Corollary (uniform weight-12 tail).** For every member of the reduced
ten-parameter family other than $P^3+b_0P+c_1q+c_0$, $S^r(H)$ lies in the
49-dimensional space of weight $\le12$ for every $r\ge1$ (for $r=0$ as well when
$E\not\equiv0$). Consequently each $S^r$, $r\ge1$, and $D_\infty$ are exactly the
kernels of finite exact matrices on that window, uniformly in the parameters, and
kernel dimension is upper semicontinuous on the complement of the excluded family.
The static bound 12 is attained (Section 4); sharpness of the same upper bound
for $S^1$ is not claimed.

**Corollary (uniform finite stopping rule).** Outside the excluded family,
$\dim S^1\le15$ and $S^{14}=D_\infty$. Thus the core at every parameter point is
the kernel of the finite matrix with columns $q^iP^j$, $i+2j\le12$, and rows the
coefficients of $T_3(H,D^kG)$ and $T_5(H,D^kG)$ for $0\le k\le14$.

*Proof.* The dimension bound follows from Theorem A, or from the
15-dimensional containing space in Theorem B. Also
$S^{r+1}=S^r\cap D^{-1}(S^r)$. Equality at any step makes $S^r$ invariant under
$D$, so all subsequent refinements agree. Since every $S^r$ contains the
independent elements $1,H$, at most 13 strict drops can occur after $S^1$.
If all 13 occur, $S^{14}=\operatorname{span}\{1,H\}$; otherwise stabilization
occurred earlier. This proves the claimed bound without computing the matrices.
$\square$

On the locus $3b_3+5c_5\ne0$, the same reasoning sharpens the finite stopping
rule to $S^{13}=D_\infty$, with every refinement supported on the 36 monomials
of weight at most 10: there $\dim S^1\le\dim S^0=14$.

**Theorem D (generic core).** On a nonempty Zariski-open subset of the parameter
space, $\dim S^0=14$ and $S^1(H)=D_\infty(H)=\operatorname{span}\{1,H\}$.
*Proof.* By the Corollary and semicontinuity it suffices to exhibit one member;
$B=2-q+3q^2+5q^3$, $C=1+4q-2q^2+7q^3+3q^4-6q^5$ has window dimensions $(14,2)$
[cert, flat engine], and $1,H\in D_\infty$ always. $\square$

## 4. Theorem C (the coupled family)

**Theorem C.** Let $H=P^3+(b_0+\mu q)P+\lambda q^2+\epsilon q+c_0$ with $\mu\lambda\ne0$.
After the translation N4 take $b_0=0$. Then

$$\dim S^0=15,\quad S^1=\operatorname{span}\{1,q,P,H\},\quad S^2=\operatorname{span}\{1,P,H\},\quad S^3=D_\infty=\operatorname{span}\{1,H\},$$

with exact obstructions $T_3(H,D^2q)=432\lambda$ and $T_3(H,D^3P)=864\lambda^2$. Depth
3 is necessary and sufficient, and there is no exceptional parameter value in
$\mu\lambda\ne0$ (for any $\epsilon$). On the boundary $\lambda=0$, $\mu\ne0$ the family is the
cubic-phase family (core of dimension 6 if $\epsilon=0$, 5 otherwise); on $\mu=0$
with $\lambda\ne0$ it is the higher-restoring family (same chain 4, 3, 2 but
$\dim S^0=\infty$). The intersection $\mu=\lambda=0$ is the excluded infinite-core family.

*Proof.* Here $E=\mu\ne0$ and $b_3=c_5=0$, so $\dim S^0=15$ by Theorem A; the gates
do not see $\lambda,\epsilon$, and an explicit basis (leading terms
$q^iP^k$, $i\le2$, $k\le3$, and $P^4,P^5,P^6$) is `static_basis()`; the top element is
$\tfrac17(7P^6+140\mu P^3q^3-378\mu P^2q^5+216\mu Pq^7+7\mu^2q^6-18\mu q^9)$ of weight
12 [cert]. $S^r$ is the kernel of the depth-$r$ gate matrix in these coordinates.
Dimensions are invariant under extension of $K$, so by N4 we may scale $\mu=1$.
Upper bounds on the rank: $1,q,P,H\in S^1$, $1,P,H\in S^2$, $1,H\in S^3$ by direct
evaluation [cert, symbolic $\mu,\lambda,\epsilon$]. Lower bounds: pivot minors of
sizes 11, 12, 13 over $\mathbb Q[\lambda,\epsilon]$ have greatest common divisor a
constant times a power of $\lambda$, and the ideal generated by the cofactors
contains a power of $\lambda$ [cert, Gröbner basis; the exponents recorded in
`CUBE_LEADING_BOUNDARY_REPLAY.json` are 4, 5, 8 for the gcd]. So the common zero
locus of the minors lies in $\{\lambda=0\}$.
Hence for $\lambda\ne0$ some minor is nonzero and the ranks
are exactly 11, 12, 13. $\square$

*Comparison with existing families.* The boundary cases above recover the
previous affine-in-$q$ and restoring classifications. No inequivalence to the
entire family $F(P)+qG(P)$ follows from the dimension pair $(15,2)$: for example,
$P^3+qP^2$, after depression, has $B=-q^2/3$, $C=2q^3/27$ and dimensions
$(\dim S^0,\dim S^1,\dim S^2)=(15,3,2)$. This example is covered by the older
cubic-phase theorem as well as Theorem G. The present proof of Theorem C does
not depend on a novelty or inequivalence claim.

## 4b. Theorem E (the stratum $\deg B\le1$, $\deg C\le3$)

**Theorem E.** Let $H=P^3+(b_0+b_1q)P+c_0+c_1q+c_2q^2+c_3q^3$ (that is,
$b_2=b_3=c_4=c_5=0$). Then $D_\infty(H)=\operatorname{span}\{1,H\}$ **if and only if**
$(c_2,c_3)\ne(0,0)$. More precisely:

1. if $c_3\ne0$, then $S^1=\operatorname{span}\{1,q,P,H\}$ and
   $S^2=D_\infty=\operatorname{span}\{1,H\}$, with $\dim S^0=15$ when $c_3\ne-b_1$ and
   $\dim S^0=\infty$ when $c_3=-b_1$; depth 2 is necessary and sufficient;
2. if $c_3=0\ne c_2$, the chain is that of Theorem C ($b_1\ne0$) or of the
   higher-restoring theorem ($b_1=0$): $S^1\supsetneq S^2\supsetneq S^3=D_\infty$;
3. if $c_2=c_3=0$, $H$ is in the cubic-phase family and
   $\dim D_\infty\in\{5,6,\infty\}$.

In case 1 with $b_1=1$, $b_0=0$ the exact obstructions are
$T_3(H,D^2q)=432(3c_3q+c_2)$ and $T_3(H,D^2P)=2592\,c_3P$; the second vanishes
exactly on the Theorem C locus, which is why that locus needs depth 3.

*Proof.* Cases 2 and 3 are Theorem C and the `core_overlap` theorems. For case 1,
$1,q,P,H\in S^1$ by direct evaluation [cert, symbolic]. Three normal forms cover
the case by N4. (a) $b_1\ne0$, $c_3\ne-b_1$: translate to $b_0=0$, scale to
$b_1=1$, parameters $(\lambda,\epsilon,\gamma)=(c_2,c_1,c_3)$; $E=1+\gamma\ne0$, so
$\dim S^0=15$ by Theorem A, with a basis polynomial in $\gamma$ having 15 distinct
leading monomials with leading coefficient 1. Maximal minors of sizes 11 and 13 of
the depth-1 and depth-2 matrices, with pivots chosen at generic points and at
points of $\{\lambda=0\}$, $\{\epsilon=0\}$, $\{\lambda=\epsilon=0\}$, generate together
with $t\gamma(\gamma+1)-1$ the unit ideal of $\mathbb Q[t,\lambda,\epsilon,\gamma]$
[cert, Gröbner basis]; so the ranks are 11 and 13 at every point with
$\gamma(\gamma+1)\ne0$. (b) $b_1\ne0$, $c_3=-b_1$: here $E\equiv0$ and, by Theorem B,
$S^1\subset K[P]_{\le6}\oplus V_H$, a 15-dimensional static space; the same minors
in $(\lambda,\epsilon)$ generate the unit ideal [cert]. (c) $b_1=0$: scale to
$c_3=1$, translate to $c_2=0$, parameters $(b_0,\epsilon)$; $E=1$, and the minors
generate the unit ideal [cert]. $\square$

## 4c. Theorem G (the stratum $b_3=c_4=c_5=0$, $b_2\ne0$)

**Theorem G.** Let $H=P^3+(b_0+b_1q+b_2q^2)P+c_0+c_1q+c_2q^2+c_3q^3$ with
$b_2\ne0$. Then for every value of the remaining parameters $\dim S^0=15$,
$q\in S^1\setminus S^2$, and

$$S^2(H)=D_\infty(H)=\operatorname{span}\{1,H\}.$$

Depth 2 is necessary and sufficient and there is no exceptional parameter value.

*Proof.* $E=(b_1+c_3)+2b_2q\not\equiv0$ and $3b_3+5c_5=0$, so $\dim S^0=15$ by
Theorem A. Translate to $b_1=0$ and scale to $b_2=1$ (N4; dimensions are invariant
under extension of $K$), leaving $(\lambda,\epsilon,\gamma,b_0)=(c_2,c_1,c_3,b_0)$. A
basis of $S^0$ polynomial in the parameters, with 15 distinct leading monomials
and leading coefficients 1, is computed exactly; $1,q,H\in S^1$ and $1,H\in S^2$
by evaluation. Three $13\times13$ minors of the depth-2 matrix, after division
by nonzero rational constants, are

$$\gamma,\qquad\lambda,\qquad
R=-\frac{(6\lambda-5)(27\gamma^2-18\lambda-28)}{108}.$$

Their common zero set is empty, since $R(0,0)=-35/27$. More explicitly,

$$1=-\frac{27}{35}R+\frac{27}{28}\gamma^2+
\lambda\left(\frac{27}{35}\lambda+\frac{39}{70}-\frac{81}{70}\gamma^2\right).$$

The exact rows, columns, determinants and rational polynomial cofactors are
retained in `CUBE_LEADING_QUADRATIC_SHORT_CERTIFICATE.json` and independently
reconstructed by `verify_cube_leading_quadratic_short.py`. These are minors
8, 23, 28 (zero-based) of the original 32-minor certificate; that larger
certificate and its optional replay are retained. No Groebner-basis
calculation is needed for the three-minor proof. So the depth-2 rank is 13 at every
parameter value. In this normal form,
$T_3(H,D^2q)=432(2P+3\gamma q+\lambda)$; its nonzero $P$ coefficient proves
$q\notin S^2$ at every parameter point. $\square$

[finite] In the normal form $b_1=0$, $b_2=1$: $\dim S^1=3$ at sampled members
with $c_3\ne0$ and $4$ at sampled members with $c_3=0$; the exact locus where
$\dim S^1=4$ was not determined.

**Corollary (Theorems C, E, G).** On the seven-parameter stratum
$b_3=c_4=c_5=0$ ($\deg B\le2$, $\deg C\le3$): $D_\infty(H)=\operatorname{span}\{1,H\}$
if and only if $B$ and $C$ are not both affine. On this two-dimensional-core
locus, depth 2 is necessary and sufficient when $(b_2,c_3)\ne(0,0)$; when
$b_2=c_3=0$ and $c_2\ne0$, depth 3 is necessary and sufficient.

## 5. Conditions, by logical status

| condition | status | consequence |
|---|---|---|
| $E\equiv0$ | equivalent | $\dim S^0=\infty$ |
| $E\not\equiv0$, $3b_3+5c_5=0$ | equivalent | $\dim S^0=15$ (otherwise 14) |
| $E\equiv0$ and $b_1=b_2=c_2=0$ | equivalent | $\dim S^1=\infty$; then $D_\infty\supset K[P]+Kq$ |
| not the excluded family | sufficient | all $S^r$, $r\ge1$, inside weight $\le12$; $S^{14}=D_\infty$ |
| $\deg B=1$, $\deg C=2$ | sufficient | chain 15, 4, 3, 2; depth 3 needed |
| $b_3=c_4=c_5=0$: $B,C$ not both affine | equivalent | $D_\infty=\operatorname{span}\{1,H\}$ |
| $b_3=c_4=c_5=0$, $(b_2,c_3)\ne(0,0)$ | equivalent on the two-dimensional-core locus | depth 2 is necessary and sufficient; the remaining $c_2\ne0$ branch needs depth 3 |
| $B$, $C$ both affine | equivalent on that stratum, conjectural in general | $D_\infty\ne\operatorname{span}\{1,H\}$ |

## 6. Conjecture and finite evidence

**Conjecture F.** $D_\infty(H)=\operatorname{span}\{1,H\}$ for every member of the
reduced family in which $B$ and $C$ are not both affine.

The Corollary of Section 4c proves it when $b_3=c_4=c_5=0$. A complete parameter
stratification is still open on the union where at least one of $b_3,c_4,c_5$
is nonzero; Theorem D already covers a nonempty open subset there. [finite] By the uniform tail each
single-stratum member listed in `CUBE_LEADING_BOUNDARY_REPLAY.json` under
`survey_finite_evidence` (including $b_3$, $c_4$, $c_5$ alone and the generic point of
Theorem D) is individually a theorem, $S^4=\operatorname{span}\{1,H\}$ on the exact
window, but those strata are sampled, not classified. The method of Sections
4–4c applies verbatim, the tail bound being uniform; the obstacle is only the
size of the symbolic minors in the remaining parameters, and on the locus
$3b_3+5c_5\ne0$ the static space has dimension 14 with a parameter-dependent basis.
There is no remaining unknown degree cutoff or stopping depth on this family:
the unresolved problem is the explicit parameter classification of the finite
matrices, including any exceptional loci.

## 7. Lean

`formal/SexticC3/CubeLeadingGate.lean` (Lean 4.19.0, Mathlib `c44e0c8e`), axioms
`propext`, `Classical.choice`, `Quot.sound` only, no `sorry`:
`natDegree_le_of_iterate_derivative`, `gate_degree_bound`
($e\ne0$, $\deg(e\,g''')\le d\Rightarrow\deg g\le d+3$, for all $g\in K[X]$),
`static_function_degree_le_six`, `top_coefficient_nonresonant`. These are the two
steps of Theorem A that hold for arbitrary degree. **Not formalised:** the
transport of $T_3,T_5$ to the chart, the reduction $G=g(u)+\tilde G$, and the rank
certificates of Theorem C; the Lean lemmas are univariate and are linked to the
bivariate operators only through the [cert] identities of Sections 1–2.

## 8. Replay

```
cd research/hamiltonian/c3_strata
python verify_cube_leading_boundary.py --require-perfectjet # exact replay; installed PerfectJet or PERFECTJET_SRC required
python verify_cube_leading_quadratic_short.py   # Theorem G: three exact minors and explicit Bezout identity
python verify_cube_leading_review.py           # independent iterated PerfectJet gates, exact minors and kernels
# Optional historical 32-minor replay (may take substantially longer):
# python verify_cube_leading_quadratic_stratum.py
python -m pytest test_cube_leading_boundary.py  # fast unit tests
cd formal && lake build SexticC3.CubeLeadingGate && lake env lean AuditCubeLeadingGate.lean
```

The cube-leading workflow requires the pinned PerfectJet comparison and checks
that replay leaves the four active JSON receipts unchanged. The original
32-minor receipt remains available with its optional slower replay. The
`sextic-formal` workflow explicitly builds the new module and compares its
axiom audit with the retained output. The Lean scope remains the univariate
lemmas described above, not an end-to-end formalization of the classifications.
The additional review certificate verifies that all four specialized symbolic
static bases have polynomial parameter coefficients, and records explicit
nonzero minors and kernel vectors for twelve matrices built entirely with
PerfectJet at four rational parameter points. These point checks supplement,
and do not replace, the parameter-uniform rank certificates.
