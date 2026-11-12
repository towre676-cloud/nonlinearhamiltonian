# Mathematical boundary of the Lean bridge

The bridge covers degrees 1 through 16 of the squarefree normal
form and checks the explicit exceptional obstruction. The coefficient model
computes rows of the first-refinement conditions. A uniform bridge now proves that these rows are coefficients of
actual Mathlib multivariate-polynomial partial-derivative contractions, for
both the static gate and its first Poisson iterate. The finite theorems use a
nonzero discriminant as a hypothesis.
The resultant calculation anchors the stored polynomial to the signed
determinant of multiplication by the quintic derivative in the quintic
remainder algebra. A general theorem that relates this expression to
geometric roots remains separate. The differential-semantics connection is now proved in
`Differential.lean` and `PolynomialBridge.lean`, uniformly in contraction
order and partner degree. `finite_differential_kernel_iff` and
`finite_differential_core_iff` give the exact first-refinement and persistent
core of every homogeneous partner in degrees 1 through 16 on the normalized
chart. They conclude zero except in degree six, where the partner is a scalar
multiple of the Hamiltonian. The persistent-core converse checks every
Poisson iterate, using stationarity of that multiple.

| Dependency of the complete C3 theorem | Formal status or work still required |
| --- | --- |
| Finite differential model | Completed for the normalized chart: all-degree monomial differentiation, both row depths, the four-gate first-refinement predicate, and exact homogeneous first-refinement/core classifications in degrees 1 through 16 are proved using Mathlib's `MvPolynomial.pderiv`. This does not remove the all-degree tail or normalization obligations below. |
| Simple-root static tail | Formalize the local normal form and top-equation argument for all integer degrees \(n\ge17\). Connect the symbolic elimination replay, its two target branches, and the bound on possible degrees to the static kernel. This argument is used for squarefree forms and the triple-root family. |
| Covariance | Prove the chain rule for linear substitution in the alternating contraction and obtain the determinant factor \(\det(A)^{k+i}\) at iterate \(i\). Include the factor \(t^{i+1}\) for rescaling \(H\). Use the nonzero factors to transport gate kernels. |
| Root strata and descent | Formalize geometric multiplicity in the algebraic closure, the projective root normal forms, and the squarefree chart obtained by moving a simple root and shearing. Relate the normalized quintic discriminant to squarefreeness. Prove scalar extension and descent for the homogeneous kernels. |
| Monomial classifications and degeneration | Formalize the symbolic all-degree monomial kernel computations. Prove rank can only drop at the monomial specialization of the one-parameter family, degree by degree, over an infinite field. These results underlie the double-root and fourfold-root bounds. |
| Other repeated-root strata | Check the exact double-root elimination and the uniform triple-root Bézout certificates. Connect both to their all-degree bounds. |
| Exceptional \((4,1,1)\) | Normalize to \(H=q^4(p^2+\delta q^2)\) with \(\delta\ne0\). Prove the all-degree upper bound from degeneration and the constant degree-two pivot. Lean checks both gates on \(G=qp\) and \(D_HG\), and checks \(T_3(H,D_H^2G)=-82944\delta q^{10}\) in the coefficient model. Use the obstruction and the upper bound to prove \(S^1=\operatorname{span}\{1,H,G\}\) and \(S^2=D_\infty=\operatorname{span}\{1,H\}\). |
| Assembly | Prove the homogeneous pieces assemble without cancellation for each fixed gate and iterate. The Hamiltonian and each scalar multiple now survive all Poisson iterates in the actual differential model. Add the constant component and combine the eleven root strata, with a separate statement for \(H=0\). |

The existing computer-assisted classification and its reproduction commands
are in the parent directory. This project supplies finite Lean theorems in both the checked coefficient
model and the actual differential polynomial model on the normalized chart.
