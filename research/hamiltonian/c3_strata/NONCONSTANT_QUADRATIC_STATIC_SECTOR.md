# Exact quadratic-in-momentum static sector for nonconstant B(q)

Let K be a characteristic-zero field, h,A,B ∈ K[q], deg h=6, and B nonconstant. Set H=h(q)+A(q)p+B(q)p². Write V₂=K[q]⊕pK[q]⊕p²K[q]. The following is an **exact all-degree intersection theorem**:

S⁰(H) ∩ V₂ = { f(q) + p(λA(q)+a q+d) + p²(λB(q)+μ) : f∈K[q], λ,a,d,μ∈K }.

In particular this static intersection is infinite-dimensional, but no claim is made that the full S⁰(H) equals this intersection.

**Proof.** For G=f+pg+p²k, direct evaluation of the odd transvectants gives

T₃(H,G)=6(B'g''−A''k')+12p(B'k''−B''k'),   T₅(H,G)=0.

The polynomial identity B'k''−B''k'=0 says (k'/B')'=0 in K(q). Since B' is a nonzero polynomial, k'=λB' and hence k=λB+μ for λ,μ∈K. The other identity becomes B'(g''−λA'')=0, so g=λA+aq+d. Conversely these forms satisfy both gates.

**First-refinement necessary condition.** With G as above, the coefficient of p³ in D_HG is 2μB'. Therefore any G∈S¹(H)∩V₂ necessarily has μ=0. This condition is not sufficient: the third gate of D_HG also needs to vanish. We make no claim about S¹ or D∞ beyond this necessary condition.

This result does not cover B constant, static partners of p-degree ≥3, or the full 21-parameter classification. It is not Lean formalized.
