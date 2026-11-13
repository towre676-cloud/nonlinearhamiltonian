# Exact quadratic-in-momentum static sector for nonconstant B(q)

Let K be a characteristic-zero field, h,A,B ∈ K[q], deg h=6, and B nonconstant. Set H=h(q)+A(q)p+B(q)p². Write V₂=K[q]⊕pK[q]⊕p²K[q]. The following is an **exact all-degree intersection theorem**:

S⁰(H) ∩ V₂ = { f(q) + p(λA(q)+a q+d) + p²(λB(q)+μ) : f∈K[q], λ,a,d,μ∈K }.

In particular this static intersection is infinite-dimensional, but no claim is made that the full S⁰(H) equals this intersection.

**Proof.** For G=f+pg+p²k, direct evaluation of the odd transvectants gives

T₃(H,G)=6(B'g''−A''k')+12p(B'k''−B''k'),   T₅(H,G)=0.

The polynomial identity B'k''−B''k'=0 says (k'/B')'=0 in K(q). Since B' is a nonzero polynomial, k'=λB' and hence k=λB+μ for λ,μ∈K. The other identity becomes B'(g''−λA'')=0, so g=λA+aq+d. Conversely these forms satisfy both gates.

**First-refinement condition, corrected.** With G as above, the coefficient of p³ in D_HG is 2μB'. This alone does not force μ=0: D_HG may be static without belonging to V₂. For example H=q⁶+qp² and G=p²+(12/5)q⁵ have μ=1, yet G and D_HG=2p³−12q⁵p both satisfy T₃=T₅=0. In fact T₃(H,D_H²G)=51840pq³, so G∈S¹ but G∉S².

A valid necessary condition comes from the coefficient of p² in T₃(H,D_HG): it equals 24μ(2B'B'''−3(B'')²). If deg B=d≥2, the polynomial in parentheses has leading coefficient −d²(d−1)(d+1)b_d²≠0, so μ=0 is necessary in that nonlinear case. It remains insufficient by itself. For affine B the obstruction vanishes identically and μ need not be zero.

For affine A and quadratic or cubic B, the full all-degree refinements are proved in `NONLINEAR_B_QUADRATIC_CUBIC.md`; its proof does not use the former incorrect inference.

This result does not cover B constant, static partners of p-degree ≥3, or the full 21-parameter classification. It is not Lean formalized.
