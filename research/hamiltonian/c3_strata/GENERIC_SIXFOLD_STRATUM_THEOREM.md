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

## Not claimed

Nothing is asserted on $c_{05}=0$. The next strata are ordered by the Newton polygon: $c_{05}=0\ne c_{14}$ has leading vertices $q^6$ and $qp^4$, and so on down to the edges treated in the weighted cubic-form note. The human proofs here have not been refereed.

## Replay

~~~sh
python verify_generic_sixfold_stratum.py      # 10 checks
cd formal && lake build SexticC3.WeightedCubicForm && lake env lean AuditWeightedCubicForm.lean
~~~
