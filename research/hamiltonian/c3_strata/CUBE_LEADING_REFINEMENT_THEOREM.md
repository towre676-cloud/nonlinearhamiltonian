# Cube-leading refinement theorem: sharp stopping depth and the temporary exceptional loci

Base commit: `d2172cf` (`origin/main`, after PR #42). Notation, conventions, the
chart $P=p+q^2$, the transported gates, the gate symbol $E$, the normalisations
N1–N4 and Theorems A, B, K are those of
[CUBE_LEADING_BOUNDARY_THEOREM.md](CUBE_LEADING_BOUNDARY_THEOREM.md). Throughout,

$$H=P^3+B(q)P+C(q),\qquad B=\sum_{i\le3}b_iq^i,\quad C=\sum_{i\le5}c_iq^i,$$

over a field $K$ of characteristic $0$, and at least one of $b_3,c_4,c_5$ is
nonzero. The constant $c_0$ is invisible to $D_H$ and to both gates and only
shifts $H$ by a constant, so every statement below holds for all $c_0$.

Evidence classes: **[proof]** human argument; **[cert]** exact identity or stored
minor reconstructed by `verify_cube_leading_refinement.py`; **[finite]** exact
computation at individual rational members, discovery evidence only.

## 1. Statement

**Theorem R.** Let at least one of $b_3,c_4,c_5$ be nonzero. Then

$$S^2(H)=D_\infty(H)=\operatorname{span}\{1,H\}$$

for every value of all remaining coefficients, and $S^1(H)$ is as follows.

| Newton case | $S^1(H)$ off the jump locus | jump locus | $S^1(H)$ on the jump locus |
|---|---|---|---|
| I: $c_5\ne0$ | $\operatorname{span}\{1,H\}$ | $b_3=0$ | $\operatorname{span}\{1,q,H\}$ |
| | | $3b_3+10c_5=0$ | $\operatorname{span}\{1,\Pi,H\}$ |
| II: $c_5=0\ne b_3$ | $\operatorname{span}\{1,H\}$ | $4c_4=5b_3^2$ | $\operatorname{span}\{1,J_2,H\}$ |
| III: $b_3=c_5=0\ne c_4$ | $\operatorname{span}\{1,q,H\}$ | $b_2+2c_4=0$ | $\operatorname{span}\{1,q,P,H\}$ |

The extra partners are

$$\Pi=b_3P+(2b_2+4c_4)\,q,$$

$$J_2=54b_3^2P^2+\bigl(168b_2b_3^2+245b_3^4-36b_3^3q-108b_3c_3\bigr)P+36b_3^3q^3+(36b_2b_3^2+15b_3^4)q^2$$
$$\qquad{}+\bigl(-216b_1b_3^2+264b_2^2b_3+1270b_2b_3^3-216b_2c_3+1225b_3^5-756b_3^2c_3+216b_3c_2\bigr)q .$$

In case I the two jump loci are disjoint. The dimensions of $S^1$ are therefore
exactly $2$ or $3$ in cases I and II and exactly $3$ or $4$ in case III.

**Corollary R1 (sharp stopping depth).** On the whole region where one of
$b_3,c_4,c_5$ is nonzero the least uniform $N$ with
$S^N(H)=\operatorname{span}\{1,H\}$ is $N=2$. The exact stopping depth of an
individual member is $1$ when $c_5\ne0$ and $b_3(3b_3+10c_5)\ne0$, or when
$c_5=0\ne b_3$ and $4c_4\ne5b_3^2$; it is $2$ in every other member, in particular
in every member of case III. Rational witnesses attaining depth 2 in each case
are listed in Section 5.

This replaces the conservative bounds $S^{14}=D_\infty$ and $S^{13}=D_\infty$ of the
uniform stopping rule on this region.

**Corollary R2 (the whole reduced family).** If $B$ and $C$ are not both affine,
then $S^3(H)=D_\infty(H)=\operatorname{span}\{1,H\}$, and depth 3 is needed exactly
when $b_2=b_3=c_3=c_4=c_5=0\ne c_2$. [proof: Theorem R and the Corollary of
Section 4c of the boundary theorem.]

**Remarks on the resonances.** The static resonance $3b_3+5c_5=0$ raises
$\dim S^0$ from 14 to 15 but does not change $S^1$. The surface $5b_2+9c_4=0$,
which appears in the recurrence used in Theorem K, is not a jump locus. On the
infinite-static locus $E\equiv0$, which meets this region only inside case III
and there forces $b_2=-2c_4$, one has $S^1=\operatorname{span}\{1,q,P,H\}$ like
every other member with $b_2=-2c_4$.

## 2. Universal partner identities

With all ten coefficients symbolic [cert]:

$$T_3(H,q)=T_5(H,q)=T_5(H,D_Hq)=0,\qquad T_3(H,D_Hq)=36\,b_3,$$

$$T_3(H,D_H(P+\alpha q))=36\alpha b_3-72b_2-144c_4-(216b_3+720c_5)\,q,\qquad T_5(H,D_H(P+\alpha q))=0,$$

and $P+\alpha q$ is static for every $\alpha$. Hence, for the whole reduced family,
$q\in S^1$ **if and only if** $b_3=0$, and some $P+\alpha q$ lies in $S^1$ **if and
only if** $3b_3+10c_5=0$ and $\alpha b_3=2b_2+4c_4$ is solvable. This gives $q$ and
$\Pi$ in case I, and $q$ and $P$ in case III. On $c_5=0$, $4c_4=5b_3^2$, $b_3\ne0$
the polynomial $J_2$ satisfies $T_3=T_5=0$ on $J_2$ and on $D_HJ_2$ [cert,
symbolic in $b_0,b_1,b_2,b_3,c_1,c_2,c_3$].

First nonzero gates at depth 2 [cert]:

| partner | locus | exact obstruction |
|---|---|---|
| $q$ | $b_3=0$ | $T_3(H,D^2q)=432P(2b_2+2c_4+10c_5q)+432c_2+1296c_3q+2592c_4q^2+4320c_5q^3$ |
| $\Pi$ | $3b_3+10c_5=0$ | $P^2$-coefficient of $T_3(H,D^2\Pi)$ is $5184\,b_3^2$ |
| $J_2$ | $c_5=0$, $4c_4=5b_3^2$ | $qP^2$-coefficient of $T_3(H,D^2J_2)$ is $1866240\,b_3^4$ |
| $P$ | $b_3=c_5=0$, $b_2=-2c_4$ | $T_3(H,D^2P)=864P(3c_3+12c_4q)+864b_1c_4-3456c_4^2q$ |

Each is nonzero on its locus inside the region. These single-element
obstructions do not by themselves bound $S^2$; that is done by the rank
certificates of Section 4.

## 3. Reduction to finite matrices

By Theorems A and B every $S^r$, $r\ge1$, lies in a fixed finite-dimensional
static space $W$: $W=S^0$, of dimension 14 or 15, when $E\not\equiv0$, and
$W=K[P]_{\le6}\oplus V_H$, of dimension 15, when $E\equiv0$. In each normal form
below an explicit basis of $W$ is computed whose elements are polynomial in the
parameters, with pairwise distinct leading monomials and leading coefficients 1
[cert]. It therefore specialises to a linearly independent static family of the
same size at every parameter value. When $E\not\equiv0$ that family is a basis of
$S^0$ by the dimension count of Theorem A. When $E\equiv0$ (case III only) its 15
elements have $P$-degree $\le6$, and the static elements of $P$-degree $\le6$ are
exactly $K[P]_{\le6}\oplus V_H$, which has dimension 15; so the family is a basis
of $W$ there too. No finite static basis is being substituted for the infinite
static space: only the proved inclusion $S^1\subset W$ is used.

Consequently $S^r$ is the kernel of the depth-$r$ gate matrix in these
coordinates, at every parameter value. A lower bound on its rank at a parameter
point follows from one nonvanishing minor at that point; an upper bound follows
from the explicit partners of Section 2.

Normal forms (N4; scaling and translation preserve every locus in the table of
Section 1, and dimensions are invariant under extension of $K$):

| case | normalisation | remaining parameters | field assumption |
|---|---|---|---|
| I | $c_5=1$, $c_4=0$ | $b_0,b_1,b_2,b_3,c_1,c_2,c_3$ | none ($s=c_5$) |
| II | $b_3=1$, $b_2=0$ | $b_0,b_1,c_1,c_2,c_3,c_4$ | none ($s=b_3$) |
| III | $c_4=1$, $c_3=0$ | $b_0,b_1,b_2,c_1,c_2$ | $s^2=c_4$, over $K(\sqrt{c_4})$ |

Invariance of the loci: translation fixes $b_3,c_5$, fixes $c_4$ when $c_5=0$,
and fixes $b_2$ when $b_3=0$; scaling multiplies $b_3,c_5$ by $s^{-1}$ and
$b_2,c_4$ by $s^{-2}$. Hence $b_3=0$, $3b_3+10c_5=0$, $3b_3+5c_5=0$,
$4c_4=5b_3^2$ (on $c_5=0$) and $b_2+2c_4=0$ (on $b_3=c_5=0$) are well defined on
the unnormalised family, and the explicit partners above are given in
unnormalised coefficients and are defined over $K$.

## 4. Rank certificates

Thirteen statements, each proved by stored minors of the exact gate matrix
[cert: `CUBE_LEADING_REFINEMENT_CERTIFICATE.json`]. A minor is used in exactly
one of three ways: it is a nonzero rational constant; it is a nonzero constant
times one named polynomial; or two minors in the same single variable have a
named greatest common divisor, with the Bézout identity in $\mathbb Q[x]$
exhibited. No Gröbner basis is used and no multivariable gcd is invoked.

| normal form and locus | $\dim W$ | depth | rank | certificate |
|---|---|---|---|---|
| III, $b_2\ne-2$ | 15 | 1 | 12 | two minors in $\mathbb Q[b_2]$, gcd $b_2+2$ |
| III, $b_2=-2$ | 15 | 1 | 11 | constant minor |
| III, $b_2\ne-1$ | 15 | 2 | 13 | two minors in $\mathbb Q[b_2]$, gcd $b_2+1$ |
| III, $b_2=-1$ | 15 | 2 | 13 | constant minor |
| II, $4c_4\ne5$ | 14 | 1 | 12 | one minor, constant times $4c_4-5$ |
| II, $4c_4=5$ | 14 | 1 | 11 | constant minor |
| II, $4c_4=5$ | 14 | 2 | 12 | constant minor |
| I, $b_3(3b_3+10)(3b_3+5)\ne0$ | 14 | 1 | 12 | two minors in $\mathbb Q[b_3]$, gcd $b_3(3b_3+10)$ |
| I, $b_3=0$ | 14 | 1 | 11 | constant minor |
| I, $b_3=0$ | 14 | 2 | 12 | constant minor |
| I, $3b_3=-10$ | 14 | 1 | 11 | constant minor |
| I, $3b_3=-10$ | 14 | 2 | 12 | constant minor |
| I, $3b_3=-5$ | 15 | 1 | 13 | constant minor |

"Constant" means constant in all remaining parameters of the normal form, so
each row is uniform on its locus. The split at $b_2=-1$ in case III is a feature
of the two chosen minors, not a jump: the rank is 13 on both sides.

*Proof of Theorem R.* Case III. Rank $\ge12$ at depth 1 off $b_2=-2$ and
$1,q,H\in S^1$ give $S^1=\operatorname{span}\{1,q,H\}$; rank $\ge11$ on $b_2=-2$ and
$1,q,P,H\in S^1$ give the four-dimensional space. Rank $\ge13$ at depth 2
everywhere and $1,H\in S^2$ give $S^2=\operatorname{span}\{1,H\}$.

Case II. Here $3b_3+5c_5=3b_3\ne0$, so $\dim S^0=14$. Off the locus the depth-1
rank is $\ge12$, so $S^1=\operatorname{span}\{1,H\}$. On the locus the depth-1 rank
is $\ge11$ and $1,J_2,H\in S^1$ are independent; the depth-2 rank is $\ge12$.

Case I. If $3b_3+5c_5\ne0$ then $\dim S^0=14$: off the two jump loci the depth-1
rank is $\ge12$; on each of them it is $\ge11$, with $1,q,H$ respectively
$1,\Pi,H$ in $S^1$, and the depth-2 rank is $\ge12$. If $3b_3+5c_5=0$ then
$\dim S^0=15$, neither jump condition holds, and the depth-1 rank is $\ge13$.

In every case $S^2\subset S^1$, so $S^2=\operatorname{span}\{1,H\}$ also where
$S^1$ is already two-dimensional. $\square$

The equality $D_\infty=\operatorname{span}\{1,H\}$ on this region was already
Theorem K; Theorem R reproves it by a second, independent route and adds the
depth.

## 5. Ledger of exact members [finite]

Computed with the flat engine in the original coordinates $(q,p)$ on the proved
weight-12 window, with coefficients not in normal form
(`CUBE_LEADING_REFINEMENT_REPLAY.json`). These rows are discovery evidence and
regression data; the theorem does not depend on them.

| member | $(b_0,b_1,b_2,b_3)$ | $(c_1,\dots,c_5)$ | $\dim S^0,S^1,S^2,S^3$ |
|---|---|---|---|
| I generic | $(2,-1,3,2)$ | $(1,-2,4,3,5)$ | 14, 2, 2, 2 |
| I, $b_3=0$ | $(2,-1,3,0)$ | $(1,-2,4,3,5)$ | 14, 3, 2, 2 |
| I, $3b_3+10c_5=0$ | $(2,-1,3,10)$ | $(1,-2,4,3,-3)$ | 14, 3, 2, 2 |
| I, $3b_3+5c_5=0$ | $(2,-1,3,5)$ | $(1,-2,4,3,-3)$ | 15, 2, 2, 2 |
| II generic | $(2,-1,3,2)$ | $(1,-2,4,3,0)$ | 14, 2, 2, 2 |
| II, $4c_4=5b_3^2$, $b_2=0$ | $(2,-1,0,2)$ | $(1,-2,4,5,0)$ | 14, 3, 2, 2 |
| II, $4c_4=5b_3^2$, $b_2\ne0$ | $(2,-1,3,2)$ | $(1,-2,4,5,0)$ | 14, 3, 2, 2 |
| III generic | $(2,-1,3,0)$ | $(1,-2,4,3,0)$ | 15, 3, 2, 2 |
| III, $b_2=-2c_4$ | $(2,-1,-6,0)$ | $(1,-2,4,3,0)$ | 15, 4, 2, 2 |
| III, $b_2=-c_4$ | $(2,-1,-3,0)$ | $(1,-2,4,3,0)$ | 15, 3, 2, 2 |
| III, $5b_2+9c_4=0$ | $(2,-1,-9,0)$ | $(1,-2,4,5,0)$ | 15, 3, 2, 2 |
| III, $E\equiv0$ | $(2,3,-4,0)$ | $(1,-2,-3,2,0)$ | $\infty$, 4, 2, 2 |

Witnesses attaining depth 2: rows 2, 3, 6, 7 and every row of case III. The
last row is computed on the windows of weight 12 and 16, which agree from $S^1$
on.

## 6. Scope and limits

Proved: Theorem R and its corollaries, for all ten reduced coefficients on the
stated region, as human arguments resting on Theorems A and B and on exact
stored minors. Independent replay: `verify_cube_leading_refinement_perfectjet.py`
rebuilds every stored minor at three random rational parameter points from
PerfectJet iterated gates in the original coordinates $(q,p)$ and compares its
exact determinant with the stored one (48 evaluations), and recomputes the
ledger with PerfectJet gates and SymPy ranks; these are exact point checks of
the transported operators and of the stored determinants, not a second proof.
Not done: nothing in this document is formalised
in Lean; no independent specialist review is asserted. The coverage table in
`BINOMIAL_NEWTON_SHARP_THEOREM.md` now records Theorem R; its retained receipt
was regenerated with the full independent verifier. The separate polynomial
K3/K4 formalization is documented in `CUBE_LEADING_POLYNOMIAL_BRIDGE.md` and does
not formalize the static reduction or the rank-certificate proof of Theorem R.

## 7. Replay

```
cd research/hamiltonian/c3_strata
python verify_cube_leading_refinement.py     # about 1 minute; rewrites CUBE_LEADING_REFINEMENT_REPLAY.json
PERFECTJET_SRC=/path/to/PerfectJet/src python verify_cube_leading_refinement_perfectjet.py   # about 3 minutes
python -m pytest test_cube_leading_boundary.py
```
