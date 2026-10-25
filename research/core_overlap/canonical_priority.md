# Targeted primary-source comparison for nonlinear shear sectors

This focused check was made on 22 October 2026 while preparing the overlap
package. It examined original papers, not secondary summaries. Its purpose
was to separate standard quantum-canonical machinery from the particular
fixed-Hamiltonian classifications proved in this package. It is not an
exhaustive historical search, and it does not establish priority.

T. Hakioglu, [*Extended covariance under nonlinear canonical transformations
in Weyl quantization*, arXiv:quant-ph/0011076v3](https://arxiv.org/abs/quant-ph/0011076),
is the closest inspected source for the protected-shear mechanism. Section
III, equations (50)--(52), treats the gauge transformation
`p -> p+A(q)`, `q -> q` and its unitary realization. Section IV, equations
(57)--(62), explicitly computes the quantum image of a cubic-generator
shear, including the additional third-derivative term: in its swapped
coordinate convention the transformation is
`exp[a(p^2 partial_q - hbar^2 partial_q^3/12)]`. Section VI(b), equation
(84), gives the general gauge generator through shifted derivative
arguments. Thus the quantum shear, its higher-derivative correction, and
the resulting agreement on sufficiently low transverse degrees are
standard machinery. The protected transport argument in
`canonical_bridge.md` is an explicit application of that machinery.

T. Dereli, T. Hakioglu and A. Tegmen,
[*Quantum canonical transformations in Weyl-Wigner-Groenewold-Moyal
formalism*, arXiv:0904.3416v2](https://arxiv.org/abs/0904.3416),
provides another direct primary comparison. Section 4, “Transform of
Functions,” formulates transformations using the Moyal Lie operator,
equations (53)--(56), and distinguishes general linear covariance from
its nonlinear example. This supports the package's distinction between
ordinary classical pullback and the quantum transformation of a Weyl
symbol; that distinction is not a novelty claim here.

T. Hakioglu and A. J. Dragt,
[*The Moyal-Lie Theory of Phase Space Quantum Mechanics*,
arXiv:quant-ph/0108081](https://arxiv.org/abs/quant-ph/0108081),
develops the general Lie-operator approach. Its time-evolution section
compares classical and quantum evolution under the same Hamiltonian,
including the special role of quadratic generators and nonlinear
examples. This is background for repeated-evolution questions, rather
than evidence that this package introduced the Moyal-Lie framework.

Mark J. Gotay, [*On the Groenewold-Van Hove problem for R^(2n)*,
arXiv:math-ph/9809015v2](https://arxiv.org/abs/math-ph/9809015),
classifies consistently quantizable polynomial Lie subalgebras in the
one-pair case under hypotheses including the standard Heisenberg
algebra. Its quadratic and coordinate algebras are essential background.
Those quantizability statements differ from determining, for a specified
nonlinear Hamiltonian and the specified flat Weyl map, every polynomial
whose entire classical Hamiltonian orbit passes all odd Moyal gates.

Within the inspected passages, none states the precise complete core
`span{1,q,Q,q^2,qQ,Q^2}` for arbitrary polynomial
`Q=p+u(q)`, `degree u>=3`, `H=AQ^2+BQ+C+epsilon q`, nor its sharp
third-gate depth-two characterization. Likewise, the inspected passages
do not state the package's complete parabolic-composition classification
for `Q=p+bq^2+cq+d`. These are candidate points of distinction only.
The existence of a nonlinear quantum-canonical transformation, a
six-dimensional transported quadratic Lie algebra, or a restricted
exact sector by itself should not be advertised as new. Establishing
historical priority for the complete fixed-H classifications requires a
broader, specialist review.
