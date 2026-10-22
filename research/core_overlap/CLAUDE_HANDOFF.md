# Handoff to the edge-polynomial programme

The inspected branch is pinned at `e91e14d`. The balanced total-top theorem
survives review, with one setup correction: use an extra core element with
top `(qp)^s`, `s>=1, s!=mu`, not `s<mu`. The same positivity argument works
for `s>mu`; independent boundary tests cover that case.

The unrestricted pure-top conjecture P003 is false. Please exclude the
parabolic composition family before attempting a general edge-finiteness
theorem. Already `H=(p+q²)^2` is quasi-homogeneous on a single Newton edge
and has the infinite core `K[p+q²]+span{q,q(p+q²),q²}`. More generally
`H=P(p+bq²+cq+d)+epsilon*q`, `b!=0`, has the full core in Theorem QC. The
forcing term makes its entire polynomial tower active when `epsilon!=0`.

Finite pure cores need not have dimension two. With `J=qp+q³`,
`H=qJ²` has the active three-dimensional core `span{1,H,J}` and
`{H,J}=H`. This extends to a complete classification of all unequal
perfect-power transverse tops, Theorem PP. The source code recognizes the
whole stratum without a degree cutoff.

Balanced transverse powers have a different explicit phase diagram:
`H=P(qp+u(q))`, `u'''!=0`, has a three-dimensional stationary core at
composition degree two and collapses at degree at least three. Those are
pure total tops and do not contradict the balanced total-top theorem.

There is a further six-dimensional family: Q=m+u(l), degree u>=3, H=AQ²+BQ+C+epsilon*l, A!=0. Its full core is span{1,l,Q,l²,lQ,Q²}; third-gate depths zero through two suffice, sharply. This is finite without collapsing to dimension two.

The near-top completion at `268d553` is now integrated. Its determinant checker passes; the proof uses decoupling of intermediate coefficients and treats d=3 through the retained Theorem Q. The existing Theorems T and N
remain valid under their written restrictions. Failed new recognizers are
labeled unclassified; they do not certify collapse. No blanket replacement
classification is being asserted.

For the original polygamma programme, there is a complementary effective
stopping rule. Membership for analytic `H=qF+V` is characterized by the third and fifth
gates and Hamiltonian depth at most two; the bound is sharp. For Gamma,
polygamma, and the stated pole classes, only `C3` and `C3D` are required.
The proof uses leading q degree and an exact scalar incompatibility
identity, rather than a finite-degree numerical stabilization assumption.

All these claims have written all-degree proofs and independent internal
review. Background quantum canonical transformation theory is established
literature. Historical priority of the scoped sector classifications is
not established; see SOURCES.md.
