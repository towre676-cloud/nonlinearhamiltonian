# Mathematical boundary of the Lean bridge

The bridge concerns fixed homogeneous degrees of the squarefree normal
form. The coefficient model computes rows of the first-refinement
conditions. The finite theorems use a nonzero discriminant as a hypothesis.
The resultant calculation anchors the stored polynomial to the signed
determinant of multiplication by the quintic derivative in the quintic
remainder algebra. A general theorem that relates this expression to
geometric roots, or connects the coefficient model to Mathlib's
multivariate differential operators, is separate from the finite checks.

| Dependency of the complete C3 theorem | Work still required in Lean |
| --- | --- |
| Remaining squarefree finite degrees | Check the thirteen other records and their pivot reductions. Prove the finite support and dimension statements in a uniform polynomial and linear-map model. |
| Simple-root static tail | Formalize the local normal form and top-equation argument for all integer degrees \(n\ge17\). Connect the symbolic elimination replay, its two target branches, and the bound on possible degrees to the static kernel. This argument is used for squarefree forms and the triple-root family. |
| Covariance | Prove the chain rule for linear substitution in the alternating contraction and obtain the determinant factor \(\det(A)^{k+i}\) at iterate \(i\). Include the factor \(t^{i+1}\) for rescaling \(H\). Use the nonzero factors to transport gate kernels. |
| Root strata and descent | Formalize geometric multiplicity in the algebraic closure, the projective root normal forms, and the squarefree chart obtained by moving a simple root and shearing. Relate the normalized quintic discriminant to squarefreeness. Prove scalar extension and descent for the homogeneous kernels. |
| Monomial classifications and degeneration | Formalize the symbolic all-degree monomial kernel computations. Prove rank can only drop at the monomial specialization of the one-parameter family, degree by degree, over an infinite field. These results underlie the double-root and fourfold-root bounds. |
| Other repeated-root strata | Check the exact double-root elimination and the uniform triple-root Bézout certificates. Connect both to their all-degree bounds. |
| Exceptional \((4,1,1)\) | Normalize to \(H=q^4(p^2+\delta q^2)\) with \(\delta\ne0\). Prove the all-degree upper bound from degeneration and the constant degree-two pivot. For \(G=qp\), verify both gates on \(G\) and \(D_HG\), then \(T_3(H,D_H^2G)=-82944\delta q^{10}\). Use the obstruction and the upper bound to prove \(S^1=\operatorname{span}\{1,H,G\}\) and \(S^2=D_\infty=\operatorname{span}\{1,H\}\). |
| Assembly | Prove the homogeneous pieces assemble without cancellation for each fixed gate and iterate. Show constants and the Hamiltonian survive all iterates and combine the eleven root strata, with a separate statement for \(H=0\). |

The existing computer-assisted classification and its reproduction commands
are in the parent directory. This project supplies finite Lean theorems
within the stated coefficient model.
