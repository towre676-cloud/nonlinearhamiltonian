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

## Scope

This classifies the entire four-parameter **cubic** lower-order slice with
\(x\ne0\). General quintic/quartic perturbations, the cubic boundary \(x=0\),
the full 21-parameter all-degree classification, and Lean formalization are
separate open problems. The proof is an exact symbolic argument with
replayable integer/rational minors, not a bounded empirical search.
