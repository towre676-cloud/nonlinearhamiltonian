# Global stabilization for the 21-parameter sixfold-leading family: $S^6=D_\infty$

Base commit: `ec31069` (`origin/main`, after PR #43). Field $K$ of characteristic
zero, observables in all of $K[q,p]$, flat gates in the original coordinates:

$$T_k(F,G)=\sum_{t}(-1)^t\binom kt(\partial_q^{k-t}\partial_p^tF)(\partial_q^t\partial_p^{k-t}G),\quad D_H=T_1(H,-),\quad S^r(H)=\{G:\ T_3(H,D_H^iG)=T_5(H,D_H^iG)=0,\ 0\le i\le r\},$$

$D_\infty(H)=\bigcap_rS^r(H)$. The family is

$$H=q^6+\sum_{i+j\le5}c_{ij}\,q^ip^j .$$

The *least depth* $N(H)$ is the least $r$ with $S^r(H)=D_\infty(H)$. Since
$S^r=S^{r+1}$ implies $S^r=D_\infty$, this is also the first place the chain
stops decreasing. $S^r(aH+b)=S^r(H)$ for $a\ne0$, so a leading coefficient
$f_6\ne0$ and the constant $c_{00}$ play no role.

Evidence classes: **[prior]** a theorem already in this repository, cited with
its own evidence limits and not re-proved here; **[proof]** human argument given
here; **[cert]** exact symbolic identity or stored minor replayed by
`verify_sixfold_global_depth.py`, universal in the parameters; **[sweep]** exact
computation at individual rational members, a cross-check and counterexample
search, never a proof step.

## 1. Results

**Theorem G1 (universal bound).** For every choice of the 21 coefficients,

$$S^6(H)=D_\infty(H),\qquad N(H)\in\{0,1,2,3,4,5,6\}.$$

The bound 6 is attained, so it is the least universal bound. The candidate
statement of the brief is therefore true, conditional on the cited prior
theorems (Section 3 lists exactly which).

**Theorem G2 (the depth-six locus).** $N(H)=6$ **if and only if**

$$H=c\,(p+\beta(q))^2+F(q),\qquad c\ne0,\quad\deg\beta=3,\quad\deg F=3 .$$

In coefficients (with $f_6=1$) this is the conjunction of

$$c_{05}=c_{14}=c_{23}=c_{04}=c_{32}=c_{13}=c_{03}=c_{22}=c_{12}=c_{41}=0,\qquad c_{02}\ne0,\qquad c_{31}^2=4c_{02},$$
$$4c_{02}c_{50}=2c_{31}c_{21},\qquad 4c_{02}c_{40}=c_{21}^2+2c_{31}c_{11},\qquad 4c_{02}c_{30}\ne2c_{31}c_{01}+2c_{21}c_{11},$$

an 8-dimensional locally closed subvariety of the 21-dimensional parameter
space (free: $c_{31}\ne0$, $c_{21},c_{11},c_{01}$, $c_{30}$ off one hyperplane,
$c_{20},c_{10},c_{00}$). On it $D_\infty=\operatorname{span}\{1,H\}$ and, with
$P=p+\beta$, $\beta=\sum\beta_iq^i$, $F_3$ the leading coefficient of $F$,

$$S^3=\operatorname{span}\{1,q,q^2,P,H\},\quad S^4=\operatorname{span}\{1,q,P,H\},\quad S^5=\operatorname{span}\{1,q,H\},\quad S^6=\operatorname{span}\{1,H\},$$

$$T_3(H,D_H^5P)=34560\,F_3^2c^4(\beta_2+3\beta_3q),\qquad T_3(H,D_H^6q)=-69120\,F_3^2c^5(\beta_2+3\beta_3q),$$

with all earlier gates of $P$ and of $q$ equal to zero. [prior: quadratic-sixfold
Theorem C for the chain; cert for the two obstruction formulas with
$c,\beta_i,F_i$ symbolic.]

**Theorem G3 (stopping depths, working downward).**

| $N(H)$ | Exactly when | $D_\infty$ |
|---|---|---|
| 6 | $H=c(p+\beta)^2+F$, $\deg\beta=3$, $\deg F=3$ | $\operatorname{span}\{1,H\}$ |
| 5 | $H=c\,p^2+(a_0+a_1q)\,p+f(q)$, $c\ne0$ | $\operatorname{span}\{1,H\}$ |
| 4 | $H=c(p+\beta)^2+F$, $\beta''\ne0$, $\deg F\ge4$ | $\operatorname{span}\{1,H\}$ |
| 3 | (a) $H=f+A\,p+B\,p^2$ with $\deg B=1$; (b) cube locus with reduced $b_2=b_3=c_3=c_4=c_5=0\ne c_2$ | $\operatorname{span}\{1,H\}$ |
| 0 | $H=f(q)+(a_0+a_1q)\,p$ | $K[q]+pK[q]+p^2K[q]$ |
| 1 or 2 | every other member | see Section 2 |

In rows 4 to 6, $F=f-A^2/(4c)$ and $\beta=A/(2c)$ for $H=f+Ap+cp^2$; "$\deg F\ge4$"
allows $\deg F=8$, which occurs when $\deg A=4$. Row 3(b) is, in the reduced
cube chart $Y^3+B(q)Y+C(q)$ of the cube-leading boundary theorem, the family
$Y^3+(b_0+b_1q)Y+c_2q^2+c_1q+c_0$ with $c_2\ne0$. Inside the last row the value
1 or 2 is given in closed form on the branches listed in Section 2 and is
otherwise an exact finite computation on a proved window (Section 6).

**Theorem N (nonconstant quadratic coefficient, arbitrary $A$).** Let
$H=f(q)+A(q)p+B(q)p^2$, $\deg f=6$, $\deg A\le4$, $k=\deg B\in\{1,2,3\}$. Section 5
gives, for every such $H$, the first refinement with explicit generators, the
exact stage dimensions, and the exact exceptional loci:

| $k$ | $\dim S^1$ | $\dim S^2$ | $\dim S^3$ | exceptional locus |
|---|---|---|---|---|
| 1 | 6 if $A'''=0$, 5 if $A'''\ne0$ | 3 | 2 | none beyond $A'''=0$ |
| 2 | 3 | 2, or 3 on the square locus of Theorem E | same | square locus only |
| 3 | 3 if $B'$ has a double root, 2 otherwise | 2 | 2 | $\Delta=b_2^2-3b_3b_1=0$, for every $A$ |

## 2. The branch decision chain

`sixfold_global_depth.classify` implements the following chain; the first
condition that holds fixes the branch. It is exhaustive by construction: each
line is the negation of all earlier ones plus one coefficient test.

| # | First coefficient test that holds | Weighted leading form, weights $(w_q,w_p)$ | $D_\infty$ | Bound | Exact $N(H)$ | Source |
|---|---|---|---|---|---|---|
| 1 | $c_{05}\ne0$ | $q^6+yp^5$, $(5,6)$ | $\langle1,H\rangle$ | 1 | 1 | generic-stratum Theorem 6 |
| 2 | $c_{14}\ne0$ | $q^6+zqp^4$, $(4,5)$ | $\langle1,H\rangle$ | 1 | 1 | binomial Newton sharp theorem |
| 3 | $c_{23}\ne0$ | $q^6+bq^2p^3$, $(3,4)$ | $\langle1,H\rangle$ | 1 | 1 | binomial Newton sharp theorem |
| 4 | $c_{04}\ne0$ | $q^6+\gamma q^3p^2+yp^4$, $(2,3)$ | $\langle1,H\rangle$ | 2 | 1 or 2, window | weighted cubic-form Theorem 5 |
| 5 | $c_{32}\ne0$ | $q^6+\gamma q^3p^2$, $(2,3)$ | $\langle1,H\rangle$ | 2 | 1 or 2; closed form if $p$-degree 2 (Theorem N) | quadratic-sixfold Lemmas 4, 5, Theorem D |
| 6 | $c_{13}\ne0$ | $q^6+cqp^3$, $(3,5)$ | $\langle1,H\rangle$ | 2 | 2 iff $T_3(H,H_p)=T_5(H,H_p)=0$, else 1 | generic-stratum Theorem 7 |
| 7a | $c_{03}\ne0$, not a cube | $q^6+\alpha q^4p+\beta q^2p^2+xp^3$, $(1,2)$ | $\langle1,H\rangle$ | 2 | 1 or 2, window; closed form off the special loci | weighted cubic-form Theorems 1–3 |
| 7b | $c_{03}\ne0$, cube, $B,C$ not both affine | $(q^2+\kappa p)^3$ | $\langle1,H\rangle$ | 3 | 1, 2 or 3, closed form | cube-leading Theorems C, E, G, G′, K, R |
| 7c | $c_{03}\ne0$, cube, $B,C$ affine | $(q^2+\kappa p)^3$ | dim 5, 6 or $\infty$ | 1 | 1 | cubic-phase table; Lemma G2 below |
| 8 | $p$-degree $\le1$ | — | $K[q]+pK[q]$ $(+p^2K[q])$ | 1 | 0 if $A$ affine, else 1 | inhomogeneous theorem, Section 10 |
| 9 | $B=c_{02}\ne0$ constant | — | $\langle1,H\rangle$, or dim 6 if $\deg F\le2$ | 6 | 5, 4, 6, 2 by $(b'',\deg F)$ | quadratic-sixfold Theorems A–C |
| 10 | $\deg B=1$ | $f_6q^6+c_1qp^2$ or $b_4q^4p+c_1qp^2$ | $\langle1,H\rangle$ | 3 | 3 | quadratic-sixfold Theorem D; Theorem N |
| 11 | $\deg B=2$ | $(2,4)$ models | $\langle1,H\rangle$, or $\langle1,Q,H\rangle$ | 2 | 2, or 1 on the square locus | quadratic-sixfold Theorems D, E; Theorem N |

Lines 1 to 7 are ordered by the slope $(6-i)/j$ of the Newton edge through
$q^6$; in each, every monomial not in the leading form has strictly smaller
weight, because the earlier tests failed. Lines 8 to 11 are the complement,
where all coefficients of $p^3,qp^3,q^2p^3,p^4,qp^4,p^5$ and of $q^3p^2$ vanish,
so $H=f+Ap+Bp^2$ with $\deg B\le2$. In line 7 put
$(\alpha,\beta,x)=(c_{41},c_{22},c_{03})$; the cube condition is $3\beta=\alpha^2$ and
$27x=\alpha^3$. Then $\kappa=\alpha/3$, and the reduced coefficients $(B,C)$ are
obtained by the substitution and depression of Section 0 of the cube-leading
boundary theorem (`cube_reduced_coefficients`).

The enlarged and infinite cores of the family are exactly those in lines 7c,
8, 9 (when $\deg F\le2$) and 11 (square locus):

| Core | Where |
|---|---|
| $K[q]+pK[q]+p^2K[q]$ | $H=f+(a_0+a_1q)p$ |
| $K[q]+pK[q]$ | $H=f+Ap$, $\deg A\ge2$ |
| $K[Y]+Kq$ | cube locus, reduced $Y^3+b_0Y+c_1q+c_0$ |
| $\operatorname{span}\{1,q,Y,Y^2,H\}$, plus $YH$ when $c_1=0$ | cube locus, reduced $Y^3+(b_0+b_1q)Y+c_1q+c_0$, $b_1\ne0$ |
| quadratic polynomials in $(q,P)$, dimension 6 | $H=c(p+\beta)^2+F$, $\deg\beta=3$, $\deg F\le2$ |
| $\operatorname{span}\{1,Q,H\}$ | $H=c_2Q^2+\text{const}$, $Q=up+v$, $u$ linear (Theorem E) |

In every other member $D_\infty=\operatorname{span}\{1,H\}$.

## 3. Proof of Theorems G1 and G3

**Lemma G0 (a floor).** $1,q,q^2\in S^0(H)$ for every $H$, and $H\in D_\infty(H)$.
Hence $N(H)\ge1$ whenever $D_\infty(H)$ is finite-dimensional and $q\notin
D_\infty(H)$ or $q^2\notin D_\infty(H)$; in particular whenever
$D_\infty=\operatorname{span}\{1,H\}$. [proof: for $G=g(q)$ of degree $\le2$ every
term of $T_k(H,G)$, $k\ge3$, contains a derivative of $G$ of order $\ge3$ or a
$p$-derivative of $G$.]

**Lemma G1 (finite chains).** If $S^r(H)$ is finite-dimensional then
$N(H)\le r+\dim S^r(H)-\dim D_\infty(H)$. [proof: the chain is strictly decreasing
until it stops.]

**Lemma G2 (the affine cube sub-branch).** Let $H=Y^3+(b_0+b_1q)Y+c_1q+c_0$ in
the reduced cube chart. Then $S^1(H)=D_\infty(H)$, so $N(H)=1$, and
(i) if $b_1\ne0$: $D_\infty=\operatorname{span}\{1,q,Y,Y^2,H\}$ for $c_1\ne0$ and
$\operatorname{span}\{1,q,Y,Y^2,H,YH\}$ for $c_1=0$ (in the normal form
$b_0=0$); (ii) if $b_1=0$: $D_\infty=K[Y]+Kq$.

*Proof.* (i) Normalise $b_0=0$, $b_1=1$. The listed spaces are static and
$D_H$-stable [cert, $c_1$ symbolic], hence inside $D_\infty\subset S^1$. Here
$E=1$, so $\dim S^0=15$ by Theorem A of the boundary theorem, with a basis
independent of $c_1$; one $10\times10$ minor of the depth-1 matrix equals a
nonzero constant times $c_1$, and at $c_1=0$ a $9\times9$ minor is a nonzero
constant [cert, stored minors]. So $\dim S^1\le5$, respectively $\le6$.
(ii) Here $E\equiv0$, $S^0=K[Y]\oplus V_H$ with $\dim V_H=8$, and $V_H$ does not
depend on $(b_0,c_1)$. $K[Y]+Kq$ is static and $D_H$-stable, since
$D_HY^m=c_1mY^{m-1}$ and $D_Hq=-(3Y^2+b_0)$ [cert]. For $G=g(Y)+v$, $v\in V_H$,
$D_HG$ is static iff $D_Hv$ is; one $7\times7$ minor of the gate matrix of
$D_H$ on $V_H$ is a nonzero constant in $(b_0,c_1)$ [cert]. So
$S^1=K[Y]+Kq$. In both cases $S^0\supsetneq S^1$. $\square$

*Proof of G1 and G3.* Go through the chain of Section 2.

Lines 1–3: the cited theorems give $S^1=D_\infty=\langle1,H\rangle$ for every
lower-weight perturbation; Lemma G0 gives $N=1$.

Lines 4–7a: the cited theorems give $S^2=D_\infty=\langle1,H\rangle$ for every
lower-weight perturbation, so $N\in\{1,2\}$ by G0.

Line 7b: $S^3=\langle1,H\rangle$, with exact depth from Theorems C, E, G and R;
depth 3 exactly on $b_2=b_3=c_3=c_4=c_5=0\ne c_2$. Line 7c: Lemma G2.

Line 8: $S^1=D_\infty$; $S^0=D_\infty$ iff $A$ is affine.

Line 9: $H/c_{02}=p^2+b\,p+f/c_{02}$ is the family of quadratic-sixfold Theorems
A–C, whose table gives least depths 5 ($b''=0$), 4 ($b''\ne0$, $\deg F\ge4$),
6 ($\deg F=3$), 2 ($\deg F\le2$). This is the only line where $N\ge4$ occurs.

Line 10: $S^3=\langle1,H\rangle$ by Theorem D(ii); $q\in S^2$ by Theorem N; so
$N=3$ for every member, not only for the leading model.

Line 11: $\dim S^1=3$ by Theorem N and Theorem D(i); so $N=2$ when
$D_\infty=\langle1,H\rangle$ and $N=1$ on the square locus, where
$S^1=D_\infty=\langle1,Q,H\rangle\subsetneq S^0$.

The maximum over all lines is 6, attained exactly in line 9 with $\deg F=3$;
values 5 and 4 occur only in line 9; value 3 only in lines 10 and 7b; value 0
only in line 8. $\square$

Theorem G2 is line 9 with $\deg F=3$: by Theorem C this forces $\deg b=3$, and
expanding $F=f-A^2/(4c_{02})$ gives the displayed equations. The dimension count
is immediate.

**Dependencies of G1.** The statement is exactly as strong as the union of:
generic-stratum Theorems 6 and 7; the binomial Newton sharp theorem; weighted
cubic-form Theorems 1–3 and 5; quadratic-sixfold Theorems A–E with Lemmas 4, 5;
inhomogeneous Section 10; cube-leading Theorems A, B, C, E, G, G′, K, R; and
Lemma G2 and Theorem N here. Several of those are computer-assisted (exact
certificates on proved finite windows), one part is formalised in Lean (the
cube-leading persistent-core criterion), and none has had external review.
Nothing in G1 depends on PR #39.

## 4. Adversarial search [sweep]

A drop $S^r\cap W\supsetneq S^{r+1}\cap W$ on any monomial window $W$ is an exact
certificate that $S^r\ne S^{r+1}$, because gate outputs are not truncated. A
counterexample to G1 would therefore show up as a drop after depth 6 on some
window. `verify_sixfold_global_depth.py` computes the chain to depth 9 on all
monomials of degree $\le12$ for 617 members (all supports of size $\le2$, random
supports of every size with rational coefficients, squares $c(p+\beta)^2+F$
with and without perturbation, the cube locus in unnormalised coordinates,
and 32 named members covering every row of both tables). In every case the
window chain stops exactly at the classifier's $N(H)$, no drop occurs after
depth 6, and the coefficient test of G2 agrees with $N(H)=6$. A larger offline
run of 4,611 members (all 1,350 supports of size $\le3$, 2,500 random, and 761
structured squares) gave the same agreement with no exception; that run is
not part of the replay. This is evidence for
the reconciliation, in particular against a mis-assigned branch; it is not
part of the proof.

## 5. Theorem N: stage descriptions for $H=f+Ap+Bp^2$, $B$ nonconstant

Gates, from (13)–(14) of the quadratic-sixfold note with $(c,b)=(B,A)$:

$$T_3=(f'''+A'''p+B'''p^2)G_{ppp}-3(A''+2B''p)G_{qpp}+6B'G_{qqp},\qquad D_H=(f'+A'p+B'p^2)\partial_p-(2Bp+A)\partial_q .$$

For $G=\varphi(q)+g(q)p+k(q)p^2$ and arbitrary polynomials $f,A,B$,
$T_5(H,G)=0$ and
$T_3(H,G)=6(B'g''-A''k')+12p\,(B'k''-B''k')$ [cert, with $f,A,B,\varphi,g,k$
undetermined functions].

**$k=1$.** Write $B=c_1(q-q_0)$. Define polynomials by

$$\varphi_1'=\frac{A'-A'(q_0)}{2B},\qquad\varphi_2'=\frac{qA'-q_0A'(q_0)}{2B},\qquad\varphi_3'=\frac{2f'-2f'(q_0)-\tfrac{(A'')^2}{2c_1}(q^2-q_0^2)}{B}\ \ (\text{when }A'''=0).$$

Then for every $f$ and every $A$ of degree $\le4$:

$$S^1=\operatorname{span}\{1,\ q,\ p+\varphi_1,\ qp+\varphi_2,\ H\}\ \oplus\ [A'''=0]\ K\,(p^2+\varphi_3),\qquad S^2=\operatorname{span}\{1,q,H\},\qquad S^3=\operatorname{span}\{1,H\}.$$

*Proof.* The listed elements are in $S^1$ [cert, all coefficients symbolic].
For $G=p^2+\varphi$ the coefficient of $p$ in $T_3(H,D_HG)$ is $36\,B'A'''$
[cert], so no choice of $\varphi$ works when $A'''\ne0$. Upper bounds: by
Theorem D(i), $\dim S^1\le6$ when $\deg A\le3$ and $\le5$ when $\deg A=4$.
For $\deg A=3$ the weights are $(2,5)$ and
$S^1(H^\sharp)=\operatorname{span}\{1,q,p,qp,p^2+\tfrac{12f_6}{5c_1}q^5,H^\sharp\}$
in weights $0,2,5,7,10,12$. A sixth element of $S^1(H)$ would have leading form
of weight 10, hence would be $p^2+\psi(q)p+\varphi(q)$; staticity gives
$\psi''=0$, so modulo the elements already found it is $p^2+\varphi$, which is
excluded. For $S^2$: $\dim S^2\le3$ by Lemma 4 and the model, and
$D_Hq=-2Bp-A=-2c_0'(p+\varphi_1)-2c_1(qp+\varphi_2)+\text{const}$ with
$B=c_0'+c_1q$, because $2c_0'\varphi_1'+2c_1\varphi_2'=A'$; so $q\in S^2$
[cert]. $S^3$ is Theorem D(ii), and $T_3(H,D_H^3q)\ne0$ has leading coefficient
$-14112\,c_1^2a_4^2$ in $q^5$, or $30240\,c_1^3f_6$ in $q^4$ when $a_4=0$ [cert].
$\square$

**$k=2$.** Write $B=c_2x^2+\delta$, $x=q-s$ ($s$ the root of $B'$). Let
$\varphi'$ be the polynomial quotient of $xA'-A$ by $2B$. Then for every $f,A$:

$$S^1=\operatorname{span}\{1,\ xp+\varphi,\ H\},$$

and $S^2=D_\infty$ is $\operatorname{span}\{1,H\}$ off the square locus of Theorem
E and equals $S^1$ on it. *Proof.* $xB'-2B=-2\delta$ is constant, so
$D_H(xp+\varphi)=-2\delta p^2+Mp+N$ and $T_3$ of it is $6B'M''$ with
$M=xA'-A-2B\varphi'$, which is affine by construction [cert]. Theorem D(i)
gives $\dim S^1\le3$, and Theorems D, E give the rest. $\square$ For affine
$A$ this is the generator $xp$ of PR #39.

**$k=3$.** Let $\Delta=b_2^2-3b_3b_1$, so $\Delta=0$ iff $B'$ has a double root
$s$, iff $B=b_3(q-s)^3+\delta$. For every $f$ and $A$:

$$S^1=\begin{cases}\operatorname{span}\{1,\ (q-s)p+\varphi,\ H\},&\Delta=0,\\ \operatorname{span}\{1,H\},&\Delta\ne0,\end{cases}\qquad S^2=D_\infty=\operatorname{span}\{1,H\},$$

where $\varphi'$ is the polynomial quotient of $xA'-2A$ by $2B$, $x=q-s$.
*Proof.* Weights $(2,3)$; $S^1(H^\sharp)=\operatorname{span}\{1,qp,H^\sharp\}$ in
weights $0,5,12$ (Theorem D). A third element of $S^1(H)$ has leading form $qp$,
so it is $(q-s)p+\varphi$ with $\deg\varphi\le2$. For such $G$ and arbitrary
cubic $B$, the coefficient of $p$ in $T_3(H,D_HG)$ is
$12\,[B'(B''+xB''')-x(B'')^2]$ [cert], which vanishes identically exactly when
$s=-b_2/(3b_3)$ and $b_1=b_2^2/(3b_3)$ [cert]. On that locus the stated
$\varphi$ makes $G\in S^1$ for every $A$ [cert]; the remainder of $xA'-2A$
modulo $b_3x^3+\delta$ has no $x^2$ term, which is why no condition on $A$
appears. $S^2$ is Theorem D(ii). $\square$ So the exceptional hypersurface of
PR #39 persists unchanged for nonlinear $A$, and $N(H)=2$ iff $\Delta=0$.
This closed form is for $p$-degree exactly 2; when lower-weight terms in
$qp^3,p^3$ are present (line 5 in general) only the bound 2 and the window
computation are available.

**Static spaces.** For $k=3$ and every $A$ of degree $\le4$,

$$S^0(H)=K[q]\ \oplus\ \operatorname{span}\{p,\ qp,\ p^2,\ H\}.$$

*Proof.* The four elements and $K[q]$ are static by the $p$-degree-two formula
above ($k=\lambda B+\mu$, $g=\lambda A+aq+e$). Conversely, for
$H^\sharp=f_6q^6+b_3q^3p^2$ the static space is $K[q]\oplus\langle p,qp,p^2,H^\sharp\rangle$
by PR #39, Section 2 (the case $A=0$, $B=b_3q^3$). By Lemma 4 at $r=0$ the
leading form of any static $G$ is in that space. Subtracting elements of
$K[q]\subset S^0(H)$ one may assume the leading form involves $p$; its weight is
then one of $3,5,6,12$, and two elements with the same such weight differ, after
scaling and reduction modulo $K[q]$, by an element of lower weight. So
$\dim S^0(H)/K[q]\le4$. $\square$ This step, and only this step, depends on
PR #39, which is not merged.

For $k\in\{1,2\}$ the full static space is **not** determined here. [sweep] On
700 random members the complement of $K[q]$ in $S^0$, measured on the windows
of degree 12, 18 and 26, has stable dimension 8 for $k=1$, $\deg A\le3$; 7 for
$k=1$, $\deg A=4$; 6, 7 or 8 for $k=2$, $\deg A\le3$; 5 or 6 for $k=2$,
$\deg A=4$. These are observations.

## 6. What "exact $N(H)$" means on lines 4, 5 and 7a

On line 4 every static partner has $(2,3)$-weight $\le20$; on line 7a every
static partner has $(1,2)$-weight $\le12$; on line 5 every element of $S^1$ has
$(2,3)$-weight $\le26$. `classify` computes $S^1$ and $S^2$ on those windows by
exact rational linear algebra, which is complete for all polynomial degrees by
the cited bounds, and reports 1 or 2. Closed forms on these lines exist only
for the leading models and for the sub-loci named in the cited theorems
(for example $\gamma^2=-40y$ on line 4, and $\Delta_w$, $\Gamma_2$ and the two
weight-4 points on line 7a); the perturbed exceptional loci are open.

## 7. Reconciliation

*PR #39 and the static-sector note.* `NONCONSTANT_QUADRATIC_STATIC_SECTOR.md` on
main inferred $\mu=0$ for $G\in S^1\cap V_2$ from the $p^3$-coefficient of
$D_HG$. That inference is invalid, because $D_HG$ may be static without having
$p$-degree $\le2$. The regression anchor is

$$H=q^6+qp^2,\qquad G=p^2+\tfrac{12}5q^5:\qquad D_HG=2p^3-12q^5p,\quad G\in S^1\setminus S^2,\quad T_3(H,D_H^2G)=51840\,pq^3$$

[cert]. It is the element $p^2+\varphi_3$ of Theorem N at $k=1$, $A=0$. This
patch replaces the note by PR #39's corrected text, byte for byte, so that the
two merge cleanly; its final sentence refers to `NONLINEAR_B_QUADRATIC_CUBIC.md`,
which exists only on PR #39. Theorem N agrees with PR #39 on its domain
(affine $A$, $k\in\{2,3\}$) and extends it to every $A$ of degree $\le4$ and to
$k=1$; it does not duplicate the Lean formalisation there.

*Stale statements.* The coverage table in `BINOMIAL_NEWTON_SHARP_THEOREM.md`
still describes the 21-parameter refinement classification as incomplete. With
G1–G3 the persistent core and the least depth are determined for every member;
what remains open is listed in Section 8. That manuscript is fingerprinted by a
receipt and is not edited here.

## 8. Not proved here

1. Closed-form exceptional loci for the first refinement under arbitrary
   lower-weight perturbation on lines 4, 5 (with $p$-degree 3 terms) and 7a.
2. The full static space for $\deg B\in\{1,2\}$.
3. Any Lean formalisation of G1–G3 or Theorem N. The planned next Lean push is
   Theorem R; nothing here changes that.
4. Independent review. G1 inherits every limit of the theorems it cites.

## 9. Replay

```
cd research/hamiltonian/c3_strata
python -m unittest test_sixfold_global_depth -v
python verify_sixfold_global_depth.py --perfectjet     # about 15 seconds; PerfectJet at the pinned commit
python -c "import sixfold_global_depth as G; print(G.classify(G.parse('(p+q^3)^2+q^3')))"
```
