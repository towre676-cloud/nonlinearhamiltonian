# From one identity to a classification programme

Edited discussion prepared for publication from the completed [research paper](../research/hamiltonian/GITHUB_RESEARCH.md). The full proofs, definitions, examples, references and computational receipts are in that paper and its [source package](../research/hamiltonian/README.md). This page explains the structure of the results rather than presenting a reconstructed dialogue as a verbatim transcript.

Fix $H$ and define $T_k$ using the flat canonical Poisson bivector. For polynomial observables independent of $\hbar$,

$$
\mathcal E(H)=\bigcap_{j\ge1}\ker T_{2j+1}(H,\cdot)
$$

is exactly the space of one-step classical–quantum partners. The sum is finite on each polynomial. A meaningful notion of a large family should remove the automatic low-degree partners and distinguish active observables, for which $\{H,G\}\ne0$, from commuting ones. Growth by partner degree, algebraic closure, symplectic equivalence and invariance under repeated $D_H=\{H,\cdot\}$ are separate organizing questions.

For cubics the problem becomes a constant-coefficient third-order PDE. Over a suitable splitting field the top cubic factors into linear forms, and the kernel decomposes into characteristic-direction polynomial families with transverse multiplicities. This supplies a complete all-degree classification in the paper’s stated setting. The degree-$n$ homogeneous kernel has dimension $\min(n+1,3)$; lower-order terms of the Hamiltonian do not create higher Moyal corrections.

For a nonzero homogeneous quartic, the organizing invariant is the power decomposition $H=aR^g$ with primitive $R$ of degree $e\in\{1,2,4\}$. For $n\ge2$,

$$
\dim\mathcal E_n(H)=2+\mathbf1_{e\mid n-2},\qquad
\operatorname{Hilb}_{\mathcal E(H)}(t)=1+2t+\frac{2t^2}{1-t}+\frac{t^2}{1-t^e}.
$$

An apolar adjoint identity transfers the correction operator’s rank problem to the Poisson centralizer. The Hessian determinant is an explicit exact partner; for a primitive quartic it accompanies $H$ in the degree-four kernel. An arbitrary inhomogeneous quartic still has a proved lower bound on the filtered space, but should not be assigned the homogeneous dimension formula without its hypotheses.

The family $H=qF(p)$ admits a particularly explicit classification over the paper’s characteristic-zero algebraic setting. Write $M=\deg F\ge2$ and $\mathcal A=\mathbb C[p]\oplus q\mathbb C[p]$. If $M=2$, the extra sector is $q^2\mathbb C[q]$. If $M=3$, it is spanned by $q^{3r+2}(F'')^r$ for $r\ge0$. If $M\ge4$, only the universal $q^2$ direction remains, except that $q^3R$ also occurs when $F''=\gamma R^3$. The corresponding dynamic core is exactly $\mathcal A$. The third transvectant explains the resonance, and higher transvectants decide whether the apparent family survives.

For monomials $H=q^ap^b$, active partners exist in arbitrarily high degree exactly when $\min(a,b)\le2$. The balanced case has additional exact commuting structure. Unequal exponents at least three have a finite all-degree classification via the highest surviving odd correction and exact integer-root checks. The paper distinguishes this monomial classification from the much harder classification of arbitrary polynomial Hamiltonians.

Closure supplies counterexamples that a dimension table alone misses. The perturbation $qp^3+q^2$ has the same one-step exact-partner space as $qp^3$, yet its dynamic core collapses to $\operatorname{span}\{1,H\}$. Thus one can preserve the space of exact first brackets while changing which observables remain exact under evolution. Finite quantum ladders also show that equality of generators at selected steps does not identify the full classical and quantum time evolutions.

The most substantial next question is a classification of dynamically invariant exact sectors under affine symplectic equivalence, with polynomial degree growth and active quotient growth recorded as invariants. Higher-degree full polynomial partners require simultaneous odd-transvectant kernels and coefficient cancellations, not only a census of monomial pairs. The pinned PerfectJet snapshot supplies existing full-space sextic results through partner degree 20, with explicitly archived msolve dependencies. It does not close partner degrees 21 and above, and this publication does not claim to have rerun those external solver verdicts.

The [35-page PDF](../research/hamiltonian/output/Nonlinear_Hamiltonian_Partners.pdf), [interactive models](../research/hamiltonian/output/Nonlinear_Hamiltonian_Partners.html), exact classifier and seven replay suites make this programme inspectable. General claims rest on the written proofs; finite exact tests certify their declared computations. Mathematical priority is not claimed.
