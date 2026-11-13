# Complete all-degree exceptional variety for cubic sixfold perturbations

**Theorem.** Let \(u,v,w,x\in\mathbb Q\), \(x\ne0\), and

\[
H=q^6+uq^3+vq^2p+wqp^2+xp^3.
\]

Let \(S^r(H)\) be the kernel of the third and fifth odd Moyal correction
operators applied to \(G,D_HG,\ldots,D_H^rG\) in the **entire** polynomial ring
\(\mathbb Q[q,p]\). Then the following statements are exact for every polynomial
degree:

\[
\dim S^0(H)=15,\qquad
S^2(H)=D_\infty(H)=\operatorname{span}_{\mathbb Q}\{1,H\}.
\]

For the first refinement, with \(\Delta=3xv-w^2\),

\[
\boxed{
S^1(H)=
\begin{cases}
\operatorname{span}_{\mathbb Q}\{1,q,q^2,H\},&\Delta=0,\\
\operatorname{span}_{\mathbb Q}\{1,q,H\},&\Delta\ne0.
\end{cases}}
\]

Thus the exceptional first-refinement locus is **exactly** the algebraic
hypersurface \(\Delta=0\) on the open parameter stratum \(x\ne0\), with no
additional rank-drop components.

## Reduction by symplectic shear

The canonical linear shear \(r=p+\frac{w}{3x}q\) preserves
\(\{q,r\}=1\). It transforms the Hamiltonian into

\[
H=q^6+u' q^3+v' q^2r+xr^3,
\]

where

\[
u'=u-\frac{vw}{3x}+\frac{2w^3}{27x^2},
\qquad v'=v-\frac{w^2}{3x}=\frac{\Delta}{3x}.
\]

It suffices to prove the theorem when \(w=0\), and all coefficient changes
are rational as \(x\ne0\).

## Why the proof covers all degrees

The static fifth gate enforces \(G_{p^5}=0\).
For \(G=\sum_{j=0}^4g_j(q)p^j\), the third gate gives the triangular exact
recurrence

\[
xg'''_j=(20q^3+u)(j+3)(j+2)(j+1)g_{j+3}
-v(j+2)(j+1)g'_{j+2}+w(j+1)g''_{j+1}.
\]

For each \(j=4,3,2,1,0\), exactly three quadratic integration constants
remain. Hence the static space is fifteen-dimensional **globally**, and
all its elements have total degree at most nine.

## Exact global rank certificates

The verifier constructs that fifteen-column symbolic basis for \(w=0\)
over \(\mathbb Q(u,v,x)\), then independently constructs the full first and
second iterated gate matrices.

It checks three specified minors, without probabilistic evaluation:

| Gate matrix | Minor size | Exact determinant |
| --- | ---: | --- |
| First iterate | \(11\times11\) | \(-18886784506215213600737640604237824000000000000\,x^{11}\) |
| First iterate | \(12\times12\) | \(16899153589846893438848121333350400000000\,v^5x^{12}\) |
| Iterates one and two | \(13\times13\) | \(-25378036356152937765773242368902013596467200000000000000\,x^{15}\) |

All minor row and column indices are part of the exact replay receipt.

The universal first-stage survivors \(1,q,H\) cap the first rank at twelve.
When \(v=0\), \(q^2\) survives because

\[
T_3(H,D_Hq^2)=144vx=0
\]

and the fifth gate vanishes. The \(11\times11\) minor ensures nothing else
survives. For \(v\ne0\), the \(12\times12\) minor forces exactly rank twelve.
At the second refinement the \(13\times13\) minor and the invariant directions
\(1,H\) give rank thirteen for **all** \(x\ne0\), including the exceptional
hypersurface.

For the unreduced variables, direct exact differentiation gives

\[
T_3(H,D_Hq^2)=48(3xv-w^2)=48\Delta,
\]

independently corroborating the shear.

## Lean verification

[`CubicExceptional`](formal/SexticC3/CubicExceptional.lean) proves the
displayed defect identity, the equivalence between `q²` surviving the
first refinement and `Δ = 0`, and the survival of `q`. It also
proves the normal form and iterated gate transport under the shear, both
static differential identities, and the resulting bound on p-exponents.

For the determinant step, the exact symbolic replay gives the following
permutations of the selected minors. These are zero-based positions
within each extracted minor, in the order used by the verifier. Applying
both permutations gives lower triangular matrices.

| Minor | Row permutation | Column permutation |
| --- | --- | --- |
| 11 | 2, 5, 6, 8, 0, 9, 1, 3, 10, 4, 7 | 0, 3, 1, 7, 8, 4, 5, 9, 2, 6, 10 |
| 12 | 4, 7, 9, 1, 10, 2, 5, 11, 3, 6, 8, 0 | 2, 0, 6, 10, 3, 7, 8, 1, 4, 5, 9, 11 |
| 13 | 2, 5, 6, 8, 0, 9, 1, 3, 10, 4, 7, 11, 12 | 0, 3, 1, 7, 8, 4, 5, 9, 2, 6, 10, 11, 12 |

A Lean determinant proof can establish the above-diagonal zeros and
diagonal entries directly from the static basis and iterated gates, then
use the triangular determinant theorem and the permutation signs. The
static basis completeness and these matrix entry identities are still
external to Lean.

## Scope

This classifies the entire four-parameter **cubic** lower-order slice with
\(x\ne0\). General quintic/quartic perturbations, the cubic boundary \(x=0\),
the full 21-parameter all-degree classification, and a complete Lean formalization are
separate open problems. The proof is an exact symbolic argument with
replayable integer/rational minors, not a bounded empirical search.
