# The generic stratum of the sixfold-leading sextic family, in all degrees

## Statement

Let $K$ be a field of characteristic zero and

$$H=q^6+\sum_{i+j\le5}c_{ij}\,q^ip^j,\qquad y:=c_{05}\ne0 .$$

All 21 lower coefficients are arbitrary subject to the single open condition that the coefficient of $p^5$ is nonzero. With the conventions of the [complete cubic theorem](COMPLETE_CUBIC_EXCEPTIONAL_THEOREM.md), where $S^r(H)$ is taken in all of $K[q,p]$:

**Theorem 6.** Every static partner of $H$ has ordinary degree at most 6, $\dim S^0(H)\le10$, and

$$S^1(H)=S^2(H)=D_\infty(H)=\operatorname{span}_K\{1,H\}.$$

For the leading form $H_0=q^6+yp^5$ the static space is exactly $S^0(H_0)=\operatorname{span}\{q^ip^j:\ 0\le i,j\le2\}\oplus K\,H_0$, of dimension 10.

There is no exceptional locus inside this stratum: the first refinement never jumps. The strata treated elsewhere in this directory (cubic, quadratic, separable, weighted, and the two Newton edges of [the weighted cubic-form note](WEIGHTED_CUBIC_FORM_THEOREM.md)) all lie in the closed complement $c_{05}=0$.

## Proof

Assign weights $\operatorname{wt}q=5$, $\operatorname{wt}p=6$. Then $q^6$ and $p^5$ have weight 30 and every other monomial of degree at most 5 has weight at most 29, so $H_0=q^6+yp^5$ is the weighted leading form of $H$. The transvectant $T_k$ lowers weight by $11k$, so by the separation principle of the weighted cubic-form note, the top weighted component of any element of $S^r(H)$ lies in $S^r(H_0)$ and $\dim S^r(H)\le\dim S^r(H_0)$. It remains to compute $S^r(H_0)$.

The gates of $H_0$ are

$$T_5(H_0,G)=720\,q\,\partial_p^5G-120\,y\,\partial_q^5G,\qquad T_3(H_0,G)=120\,q^3\,\partial_p^3G-60\,y\,p^2\,\partial_q^3G .$$

In weight $d$ the monomials form a single chain $(i_k,j_k)=(i_0-6k,\ j_0+5k)$, $0\le k\le L$, with $j_0\le4$ and $i_L\le5$; write $c_k$ for the coefficient of $q^{i_k}p^{j_k}$ and $n^{\underline m}$ for the falling factorial. Each gate couples only neighbours of the chain. For $1\le k\le L$ the coefficients of $q^{i_k+1}p^{j_k-5}$ and of $q^{i_k+3}p^{j_k-3}$ give

$$720\,j_k^{\underline5}\,c_k=120\,y\,i_{k-1}^{\underline5}\,c_{k-1},\qquad120\,j_k^{\underline3}\,c_k=60\,y\,i_{k-1}^{\underline3}\,c_{k-1},$$

and at the two ends the third gate gives $j_0^{\underline3}c_0=0$ and $y\,i_L^{\underline3}c_L=0$. Since $j_k\ge5$ and $i_{k-1}\ge6$ on a link, eliminating $c_k$ yields

$$\bigl[(i_{k-1}-3)(i_{k-1}-4)-3(j_k-3)(j_k-4)\bigr]c_{k-1}=0,$$

and $c_{k-1}=0$ forces $c_k=0$ and conversely. Call a link resonant when the bracket vanishes. Two consecutive links cannot both be resonant: subtracting the two conditions gives $2i_{k-1}+5j_k=18$, impossible for $i_{k-1}\ge6$, $j_k\ge5$. Hence a nonzero static $G$ of weight $d$ has either $L=0$, or $L=1$ with its one link resonant. If $L=0$ the end conditions give $j_0\le2$ and $i_0\le2$, the 9 monomials $q^ip^j$ with $i,j\le2$. If $L=1$ they give $j_0\le2$ and $i_1\le2$, that is $6\le i_0\le8$, and the resonance $(i_0-3)(i_0-4)=3(j_0+2)(j_0+1)$ has the single solution $(i_0,j_0)=(6,0)$, the chain $q^6\to p^5$, whose kernel vector is $H_0$. This proves the description of $S^0(H_0)$ in every weight.

For the refinements it suffices, by the scaling $q\mapsto q/\mu$, $p\mapsto\mu p$ over an algebraic closure and invariance of rank under extension of scalars, to take $y=1$. Then $S^1(H_0)$ is the kernel of the depth-1 gates on the explicit 10-dimensional space above, a finite exact computation with result $\operatorname{span}\{1,H_0\}$. Since $1,H\in D_\infty(H)$ always, $\dim S^1(H)\le2$ gives the theorem. $\qquad\blacksquare$

## Evidence classes

| Claim | Status |
| --- | --- |
| Gate formulas for $H_0$, link elimination | Symbolic identities in symbolic exponents, replayed by `verify_generic_sixfold_stratum.py` |
| Link elimination, no two consecutive resonances, the isolated resonance | Formalized in `formal/SexticC3/WeightedCubicForm.lean`: `GenericStratum.link_resonance`, `no_consecutive_resonance`, `isolated_resonance`; axioms `propext`, `Quot.sound` |
| $S^0(H_0)$ in every weight | Human proof above; additionally an exhaustive exact check of weights 0 to 400 finds exactly these 10 elements |
| $S^1(H_0)=\operatorname{span}\{1,H_0\}$ | Exact rational linear algebra on a 10-dimensional space |
| Passage to all 21 parameters | Human proof (separation principle); spot-checked on 25 random members and on each single added monomial |
| Theorem 6 as a whole | Not formalized in Lean |

Because every static partner has degree at most 6, `generic_sixfold_stratum.refinement` computes $S^r(H)$ exactly, for all polynomial degrees, for any given member with $c_{05}\ne0$.

## The stratum with leading form $q^6+cqp^3$, in all degrees

This stratum is $c_{05}=c_{14}=c_{23}=c_{04}=c_{32}=0\ne c_{13}$. With weights $\operatorname{wt}q=3$, $\operatorname{wt}p=5$ the leading form is $H_c=q^6+cqp^3$, of weight 18, and the 15 remaining monomials of degree at most 5 have lower weight. The classification of $S^0(H_c)$ below is due to C; it is reproduced and replayed here, and it replaces the finite experiment previously recorded for this stratum.

**Theorem 7.** For every $c\ne0$, $\dim S^0(H_c)=14$ in all of $K[q,p]$, with basis

$$1,\ q,\ q^2,\quad p,\ qp,\ q^5p,\quad p^2,\ qp^2,\ q^8p^2,\quad p^3+\tfrac2cq^5,\ \ qp^3+\tfrac1cq^6,\ \ q^{11}p^3+\tfrac1{28c}q^{16},\quad qp^4+\tfrac{16}cq^6p,\ \ q^{14}p^4+\tfrac{40}{399c}q^{19}p .$$

Moreover $S^1(H_c)=\operatorname{span}\{1,q,H_c\}$ and $S^2(H_c)=D_\infty(H_c)=\operatorname{span}\{1,H_c\}$. For every $H=H_c+R$ with $R$ of lower weight,

$$\dim S^0(H)\le14,\qquad S^2(H)=D_\infty(H)=\operatorname{span}\{1,H\},$$

and $S^1(H)$ is $\operatorname{span}\{1,q,H\}$ if $T_3(H,H_p)=T_5(H,H_p)=0$ and $\operatorname{span}\{1,H\}$ otherwise.

*Proof.* The only nonzero fifth derivative of $H_c$ is $\partial_q^5H_c=720q$, so $T_5(H_c,G)=720\,q\,\partial_p^5G$ and every static partner is $G=\sum_{j=0}^4g_j(q)p^j$. Since $\partial_q^2\partial_pH_c=0$, $\partial_q\partial_p^2H_c=6cp$ and $\partial_p^3H_c=6cq$, the coefficient of $p^j$ in $T_3(H_c,G)$ is

$$6c\bigl(3j\,g_j''-q\,g_j'''\bigr)+120\,(j+3)(j+2)(j+1)\,q^3g_{j+3}=0,\qquad0\le j\le4,\quad g_5=g_6=g_7=0 .$$

On $q^m$ the operator $g\mapsto q\,g'''-3j\,g''$ acts by $m(m-1)(m-2-3j)\,q^{m-2}$. For $j=4,3,2$ the equation is homogeneous, with polynomial solutions $\operatorname{span}\{1,q,q^{3j+2}\}$. For $j=1$ and $j=0$ the source is $q^3g_4$ and $q^3g_3$, with exponents in $\{3,4,17\}$ and $\{3,4,14\}$; a polynomial particular solution exists for a source $q^s$ exactly when $(s+2)(s+1)(s-3j)\ne0$, which fails only for $j=1$, $s=3$. That source comes from the constant term of $g_4$, which must therefore vanish, and every other source integrates. The solution space has dimension $5\cdot3-1=14$, and solving the two inhomogeneous equations gives the stated basis. For the refinements, $S^1\subset S^0$ is a finite exact computation on this basis, carried out at $c=1$, which suffices by the scaling $q\mapsto q/\mu$, $p\mapsto\mu p$ over an algebraic closure. The statements for $H$ follow from the separation principle; a third element of $S^1(H)$ has top component $q$, so it is $q$ modulo constants. $\qquad\blacksquare$

Status: the differential equations and the 14 elements are replayed for symbolic $c$ by `verify_qp3_stratum.py` (10 checks); the refinement dimensions are exact rational linear algebra; the passage to $R\ne0$ rests on the separation principle, a human proof that has not been refereed; nothing here is formalized in Lean.

## Newton strata: proved rows and historical experiments

The same weighting argument orders the complement $c_{05}=0$. The two
binomial rows formerly supported by the degree-360 experiment now have a
[complete endpoint/resonance proof, sharp support bounds and exact certificates](BINOMIAL_NEWTON_SHARP_THEOREM.md).
Both have ten static partners and $S^1=D_\infty=\operatorname{span}\{1,H\}$,
also after arbitrary strictly lower-weight perturbations. Static dimension
can drop under perturbation; the sharp uniform bounds are 44 and 28.
The historical experiment column is retained as a regression, not as proof.

| Stratum | Leading form, weights | Static partners found (weights $\le360$) | $\dim S^0,S^1,S^2$ of the leading form | One random member |
| --- | --- | --- | --- | --- |
| $c_{05}=0\ne c_{14}$ | $q^6+qp^4$, $(4,5)$ | 10, sharp proved top weight 44 | 10, 2, 2 (all degrees) | 7, 2, 2 |
| $c_{05}=c_{14}=0\ne c_{23}$ | $q^6+q^2p^3$, $(3,4)$ | 10, sharp proved top weight 28 | 10, 2, 2 (all degrees) | 8, 2, 2 |
| $c_{05}=c_{14}=c_{23}=0\ne c_{04}$ | $q^6+\gamma q^3p^2+yp^4$, $(2,3)$ | Theorem 5 of the weighted cubic-form note | | |
| then $c_{04}=c_{32}=0\ne c_{13}$ | $q^6+cqp^3$, $(3,5)$ | Theorem 7 above | | |
| then $c_{13}=0\ne c_{03}$ | $q^6+\alpha q^4p+\beta q^2p^2+xp^3$, $(1,2)$ | Theorems 1 to 3 of the weighted cubic-form note | | |

## Not claimed

These results do not assert a complete classification of all 21 parameters. In particular the weighted cubic cube locus with arbitrary lower terms remains outside the finite-tail theorems. The $c_{04}=0\ne c_{32}$ boundary has an infinite static space; the quadratic-sixfold theorem separately supplies finite first-refinement bounds and a core result for its leading form. See the [reconciled coverage table](BINOMIAL_NEWTON_SHARP_THEOREM.md#7-repository-reconciliation-and-remaining-boundaries) for the distinction. The human proofs here have not been externally refereed or fully formalized.

## Replay

~~~sh
python verify_generic_sixfold_stratum.py      # 10 checks
python verify_qp3_stratum.py                  # 10 checks, about 1 minute
cd formal && lake build SexticC3.WeightedCubicForm && lake env lean AuditWeightedCubicForm.lean
~~~
