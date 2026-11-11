# Mathematical boundary of the Lean bridge

The bridge covers degrees 1 through 16 of the squarefree normal
form and checks the explicit exceptional obstruction. The coefficient model computes rows of the first-refinement
conditions. The finite theorems use a nonzero discriminant as a hypothesis.
The resultant calculation anchors the stored polynomial to the signed
determinant of multiplication by the quintic derivative in the quintic
remainder algebra. A general theorem that relates this expression to
geometric roots, or connects the coefficient model to Mathlib's
multivariate differential operators, is separate from the finite checks.

| Dependency of the complete C3 theorem | Work still required in Lean |
| --- | --- |
| Finite coefficient model | Transport the checked degrees 1 through 16 and their kernel bounds to a uniform polynomial and linear-map model. |
| Simple-root static tail | In the normalized simple-root chart, Lean proves the two-coefficient bound, forward substitution, the six reconstructed fifth-order rows, and the implications of the three target equations. Still required are the local chart change, comparison with the stored polynomial rows, chart coverage, and elimination replay. See [Static tail](STATIC_TAIL.md). |
| Covariance | Prove the chain rule for linear substitution in the alternating contraction and obtain the determinant factor \(\det(A)^{k+i}\) at iterate \(i\). Include the factor \(t^{i+1}\) for rescaling \(H\). Use the nonzero factors to transport gate kernels. |
| Root strata and descent | Formalize geometric multiplicity in the algebraic closure, the projective root normal forms, and the squarefree chart obtained by moving a simple root and shearing. Relate the normalized quintic discriminant to squarefreeness. Prove scalar extension and descent for the homogeneous kernels. |
| Monomial classifications and degeneration | Formalize the symbolic all-degree monomial kernel computations. Prove rank can only drop at the monomial specialization of the one-parameter family, degree by degree, over an infinite field. These results underlie the double-root and fourfold-root bounds. |
| Other repeated-root strata | Check the exact double-root elimination and the uniform triple-root Bézout certificates. Connect both to their all-degree bounds. |
| Exceptional \((4,1,1)\) | Normalize to \(H=q^4(p^2+\delta q^2)\) with \(\delta\ne0\). Prove the all-degree upper bound from degeneration and the constant degree-two pivot. Lean checks both gates on \(G=qp\) and \(D_HG\), and checks \(T_3(H,D_H^2G)=-82944\delta q^{10}\) in the coefficient model. Use the obstruction and the upper bound to prove \(S^1=\operatorname{span}\{1,H,G\}\) and \(S^2=D_\infty=\operatorname{span}\{1,H\}\). |
| Assembly | Prove the homogeneous pieces assemble without cancellation for each fixed gate and iterate. Show constants and the Hamiltonian survive all iterates and combine the eleven root strata, with a separate statement for \(H=0\). |

The existing computer-assisted classification and its reproduction commands
are in the parent directory. This project supplies finite Lean theorems
within the stated coefficient model.
