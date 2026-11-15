# Closed-form first-refinement jump loci on the three remaining sixfold branches

Base: branch `research/sixfold-global-depth` (PR #44, head `b7e8c30`).
Conventions, the family $H=q^6+\sum_{i+j\le5}c_{ij}q^ip^j$, the branch decision
chain and its line numbers are those of
[SIXFOLD_GLOBAL_DEPTH_THEOREM.md](SIXFOLD_GLOBAL_DEPTH_THEOREM.md). Field of
characteristic zero, unrestricted observables, flat gates in the original
coordinates, leading coefficient normalised to $f_6=1$.

On lines 4, 5 and 7a of the chain the global theorem proved
$S^2(H)=D_\infty(H)=\operatorname{span}\{1,H\}$ and left the choice between least
depth 1 and 2 to an exact computation on a proved finite window. This note
replaces those computations by coefficient equations and explicit partners.

Evidence classes: **[prior]** theorem already in the repository; **[proof]**
argument given here; **[cert]** exact symbolic identity replayed by
`verify_sixfold_jump_loci.py`, universal in the parameters; **[sweep]** exact
computation at individual members, a cross-check only.

## 1. Statement

Write $r_{ij}$ for the coefficient of $q^ip^j$ in the lower-weight part $R$ of
the branch in question.

**Theorem J.** In each of the three branches $S^1(H)=\operatorname{span}\{1,H\}\oplus
\operatorname{span}(\text{partners})$, where the partners and the exact conditions
for their presence are as follows. The least depth is 2 if a partner is present
and 1 otherwise.

**(J4) Quartic edge**, $c_{04}=y\ne0$, $c_{05}=c_{14}=c_{23}=0$, $\gamma=c_{32}$:
there is at most one partner, and it is present **if and only if**

$$\gamma^2=-40y,\qquad r_{41}=\frac{\gamma r_{13}}{2y},\qquad r_{50}=\frac{\gamma(13r_{13}^2-8yr_{22})}{160y^2},\qquad r_{03}=-\frac{\gamma(r_{13}^3-4yr_{13}r_{22}+8y^2r_{31})}{160y^2},$$

$$r_{40}=\frac{-9r_{13}^4+36yr_{13}^2r_{22}+24y^2r_{13}r_{31}+48\gamma y^2r_{12}-32y^2r_{22}^2}{384y^3},$$

$$r_{21}=\frac{3\gamma r_{13}^5-16\gamma yr_{13}^3r_{22}+24\gamma y^2r_{13}^2r_{31}+16\gamma y^2r_{13}r_{22}^2-32\gamma y^3r_{22}r_{31}+640y^3r_{12}r_{13}}{1280y^4}.$$

The partner is $p+\dfrac{r_{13}}{4y}\,q$. The jump locus is thus the graph of five
functions over the hypersurface $\gamma^2=-40y$: the coefficients
$r_{13},r_{22},r_{31},r_{12},r_{30},r_{20},r_{10},r_{11},r_{01},r_{02}$ are free.

**(J5) Cubic quadratic coefficient**, $c_{32}=b_3\ne0$,
$c_{05}=c_{14}=c_{23}=c_{04}=0$, so
$H=f+Ap+Bp^2+(c_{03}+c_{13}q)p^3$ with $B=\sum_{i\le3}b_iq^i$: there is at most one
partner, and it is present **if and only if**

$$c_{13}=0,\qquad c_{03}=0,\qquad b_2^2=3b_3b_1 .$$

So any cubic momentum term destroys the jump, and when there is none the locus
is the hypersurface $\Delta=0$ of Theorem N for every $A$; the partner is
$(q-s)p+\varphi$ of Theorem N, $s=-b_2/(3b_3)$.

**(J7) Cubic form off the cube locus**, $c_{03}=x\ne0$,
$(\alpha,\beta)=(c_{41},c_{22})$, all earlier tests failing and
$(\alpha,\beta,x)\notin\mathcal C$. With $\Delta_w=\beta^2-3\alpha x$ and
$\Gamma_2=12\alpha^2x^2+4\alpha\beta^2x-\beta^4-45\beta x^2$, the possible partners
are:

| Partner | Present exactly when |
|---|---|
| $q$ | $\Delta_w=0$ and $3x\,r_{31}=2\beta\,r_{12}$ |
| $p+\lambda q^2+\mu q$ | $\Gamma_2=0$, $\beta\ne0$, and $\Xi_\Gamma=0$ |
| $q^2$ | $\alpha=\beta=0$, $r_{31}=0$ and $r_{12}^2=3x\,r_{21}$ |
| $G_4+e_1q^3+e_2qp+e_3q^2+e_4p+e_5q$ | $(\alpha,\beta,x)$ is one of the two weight-4 points and $\Xi_1=\Xi_2=0$ |

where

$$\lambda=\frac{3\alpha x+\beta^2}{6\beta x},\qquad\mu=\frac{6\alpha r_{12}-10\beta\lambda r_{12}+21\lambda xr_{31}-30xr_{50}}{2\Delta_w},$$

$$\Xi_\Gamma=-2\beta\mu r_{12}-2\beta r_{21}-4\lambda r_{12}^2+12\lambda xr_{21}+3\mu xr_{31}+3r_{12}r_{31}-12xr_{40},$$

$$G_4=12\beta x^2p^2+6x(\alpha x+\beta^2)q^2p+\beta(\alpha x+\beta^2)q^4,$$

$$\Xi_1\ \propto\ 114\alpha^3x^2r_{12}+134\alpha^2\beta^2xr_{12}-141\alpha^2\beta x^2r_{31}-360\alpha^2x^3r_{50}-34\alpha\beta^4r_{12}+57\alpha\beta^3xr_{31}-90\alpha\beta^2x^2r_{50}$$
$$\qquad{}-540\alpha\beta x^2r_{12}-135\alpha x^3r_{31}-90\beta^3xr_{12}+135\beta^2x^2r_{31}+1350\beta x^3r_{50},$$

and $e_1,\dots,e_5$ and the 473-term polynomial $\Xi_2$ are recorded in
`SIXFOLD_JUMP_WEIGHT4_SYSTEM.json`. The four rows are mutually exclusive except
that at $\alpha=\beta=0$ the first and third can hold together, giving
$\dim S^1=4$. $\Xi_\Gamma=0$ is solved by $r_{40}$ and the first row by $r_{31}$,
so those two loci are again graphs. The weight-4 points are the two points of
$\mathbb P(1,2,3)$ with $2842\,t^2-53565\,t-245025=0$, $t=\beta^3/x^2$; that
quadratic has irrational roots, so **no member with rational coefficients lies
on the fourth row**.

**Corollary J (closed-form depth).** With Theorems G3, N, R and the cube-leading
theorems, the least stopping depth $N(H)$ of every member of the 21-parameter
family is now given by explicit conditions on the coefficients. Two of them
are stated in a form that is explicit but not expanded into equations: on line
6 the condition is $T_3(H,H_p)=T_5(H,H_p)=0$ (generic-stratum Theorem 7), and on
the branch $\deg B=2$ the square locus of quadratic-sixfold Theorem E is the
composition $H=c_2Q^2+\text{const}$.

## 2. Proof

In each branch the cited theorem gives $\dim S^1(H)\le\dim S^1(H^\sharp)$ and
places the leading form of every element of $S^1(H)$ in $S^1(H^\sharp)$, for the
weighted leading form $H^\sharp$ (the separation principle). The extra leading
forms of the models are known and have pairwise distinct weights, all different
from $0$ and $\operatorname{wt}H^\sharp$. Hence $S^1(H)$ is spanned by $1$, $H$ and,
for each extra leading form $L$ of the model, at most one element
$L+(\text{terms of weight}<\operatorname{wt}L)$. The lower terms range over an
explicit finite list of monomials, so the existence of that element is a
finite polynomial system in its unknown coefficients and the coefficients of
$H$. Each system below is linear in the unknowns once the leading form is
fixed, and is solved completely.

**(J4).** [prior: weighted cubic-form Theorem 5] $S^1(H_e)=\langle1,H_e\rangle$
unless $\gamma^2=-40y$, where it gains $p$, of weight 3 for the weights $(2,3)$.
The monomials of smaller weight are $q$ and $1$, so the candidate is $p+\mu q$.
It is static for every $\mu$, $T_5(H,D_H(p+\mu q))=0$, and the coefficients of
$T_3(H,D_H(p+\mu q))$ are eight explicit polynomials [cert]. The $q^2p$
coefficient is $-216(\gamma^2+40y)$. On $\gamma^2=-40y$ the $q^3$ coefficient
gives $\mu=r_{13}/(4y)$; the coefficients of $p^2$, $qp$, $q^2$, $p$, $q$ are
then solved in turn by $r_{41},r_{50},r_{03},r_{40},r_{21}$, each entering
linearly with a nonzero coefficient ($16y$, $40y$, $60$, $24y$, $3\gamma$ up to the
common factor; $\gamma\ne0$ because $\gamma^2=-40y$); and the constant coefficient vanishes identically modulo
$\gamma^2+40y$ after those substitutions [cert]. $\square$

**(J5).** [prior: quadratic-sixfold Lemma 5 and Theorem D]
$S^1(H^\sharp)=\langle1,qp,H^\sharp\rangle$, with $qp$ of weight 5 for the weights
$(2,3)$; the smaller monomials are $q^2,p,q,1$. The candidate is
$(q-s)p+u_1q+u_2q^2$. It is static, $T_5$ of its image vanishes, and in
$T_3(H,D_HG)$ the coefficient of $qp^2$ is $540\,b_3c_{13}$ and, once $c_{13}=0$,
the coefficient of $p^2$ is $-144\,b_3c_{03}$ [cert]. So $c_{13}=c_{03}=0$, and
the remaining equations are those of Theorem N: the $q^2p$ coefficient gives
$s=-b_2/(3b_3)$ and the $qp$ coefficient then equals $48(3b_1b_3-b_2^2)$ [cert].
$\square$

**(J7).** [prior: weighted cubic-form Theorems 2 and 3] The extra leading forms
of $S^1(H_w)$ have weight 1 on $\Delta_w=0$, weight 2 on $\Gamma_2=0$ and weight
4 at the two points, and off $\mathcal C$ the first two loci meet only at
$\alpha=\beta=0$.

*Weight 1.* The candidate is $q$. $T_3(H,D_Hq)=48(3\alpha x-\beta^2)\,q+12(3xr_{31}-2\beta r_{12})$
and $T_5(H,D_Hq)=0$ [cert].

*Weight 2, $\beta\ne0$.* The candidate is $p+\lambda q^2+\mu q$. The $p$
coefficient of $T_3(H,D_HG)$ gives $\lambda$; the $q^2$ coefficient is then
$48\,\Gamma_2/(\beta x)$; the $q$ coefficient is $-2\Delta_w\mu$ plus terms in
$r_{12},r_{31},r_{50}$, which gives $\mu$ because $\Delta_w\ne0$ here; the
constant coefficient is $12\,\Xi_\Gamma$ [cert]. If $\beta=0$ then $\Gamma_2=0$
forces $\alpha=0$.

*$\alpha=\beta=0$.* The leading forms are $q$ and $q^2$, so the candidates are
$aq^2+bq$, and $T_3(H,D_H(aq^2+bq))=504\,a\,x\,r_{31}\,q+12\,(a(12xr_{21}-4r_{12}^2)+3b\,x\,r_{31})$
[cert]. If $r_{31}\ne0$ nothing survives. If $r_{31}=0$, $q$ survives, and $q^2$
survives exactly when $r_{12}^2=3xr_{21}$.

*Weight 4.* The model element is $G_4$, and the two model equations in weight 4
vanish exactly at the two points [cert]. The candidate adds
$e_1q^3+e_2qp+e_3q^2+e_4p+e_5q$. The system is triangular by weight: the static
equation gives $e_1$, one weight-3 equation gives $e_2$ and the other is
$\Xi_1$, the two weight-2 equations give $e_3,e_4$, the weight-1 equation gives
$e_5$, and the weight-0 equation is $\Xi_2$. The denominators that occur are
products of $\alpha$, $\Delta_w$ and $\Gamma_2$, none of which vanishes at the two
points [cert: each is coprime to the defining polynomial]. $\square$

## 3. Cross-check [sweep]

For each branch the verifier builds members on the locus (solving the graph
equations exactly), near-misses that break one equation, and random members,
and compares the closed form with the exact kernel of the first-refinement
gates on the window proved to contain $S^1$: weight $\le20$ for (J4), $\le26$
for (J5), $\le12$ for (J7). In all 392 cases the dimension of $S^1$ is
$2+\#\text{partners}$, each returned partner satisfies the gates by direct
evaluation, and every near-miss has no partner. The weight-4 row cannot be
tested this way over $\mathbb Q$; its two residual conditions are certified
symbolically only.

## 4. Limits

The statements rest on the cited model theorems: Theorem 5 and Theorems 2, 3
of the weighted cubic-form note are proved with exact finite certificates on
top of human tail arguments, and Lemma 5 with Theorem D of the quadratic-sixfold
note likewise. Nothing here is formalised in Lean. The weight-4 row has no
numerical witness. Still open after this note: the full static spaces for
$\deg B\in\{1,2\}$, and coefficient equations for the square locus on the
branch $\deg B=2$.

## 5. Replay

```
cd research/hamiltonian/c3_strata
python verify_sixfold_jump_loci.py          # about 12 seconds
python -m unittest test_sixfold_global_depth -v
```
