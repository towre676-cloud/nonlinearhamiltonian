# Mathematical boundary of the Lean bridge

`SexticC3.SquarefreeGeometry` proves the geometric squarefree case for a
homogeneous binary sextic over any characteristic-zero field. Its projective
root hypothesis is tested by the gradient over the algebraic closure. The
theorem applies to an arbitrary polynomial observable over the original field.
The order-three and order-five differential gates vanish on the observable and
its first Poisson iterate exactly when it is a constant plus a scalar multiple
of the Hamiltonian. These observables pass the gates at every iterate.

The proof connects the uniform differential-polynomial operators to the
checked coefficient rows, constructs an invertible simple-root chart, and
proves determinant covariance, the separability-to-discriminant implication,
homogeneous assembly, and scalar descent. The normalized coefficient proof
combines the sixteen finite degrees and the uniform static tail. See
[Static tail](STATIC_TAIL.md) for the coefficient certificates.

| Dependency of the complete C3 classification | Formal status |
| --- | --- |
| Geometric squarefree case | `squarefree_firstRefinement_iff_shape` and `squarefree_firstRefinement_iff_core` |
| Triple-root case | `tripleRoot_highDegree_zero_of_chart` excludes degrees at least 17 under the exhibited normalized chart hypothesis. The finite triple-root Bézout certificates and geometric multiplicity transport remain to be formalized. |
| Monomial classifications and degeneration | The uniform monomial kernels and specialization rank arguments remain to be formalized. These results underlie the double-root and fourfold-root bounds. |
| Other repeated-root strata | The repeated-root normal forms, exact double-root elimination, and corresponding kernel bounds remain to be formalized. |
| Exceptional `(4,1,1)` | `exceptional_second_gate` proves the exact differential obstruction, and `exceptional_obstruction_of_chart` transports the witness through invertible linear maps and nonzero scaling. The geometric normal form for the entire stratum and the exact first- and second-refinement upper bounds remain open. |
| Complete assembly | The checked homogeneous decomposition can be reused. The eleven-stratum theorem still needs its remaining stratum bounds. The zero Hamiltonian is covered by `zero_hamiltonian_persistentCore`. |

`AuditGeometry.lean` checks the axioms of the new proof chain. The
computer-assisted classification and its Python reproduction commands are in
the parent directory.
