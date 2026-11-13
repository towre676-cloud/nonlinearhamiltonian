# Uniform fifth-gate cutoff for affine quadratic-momentum coefficients

Let K be a characteristic-zero field, let h(q)∈K[q] have degree six, and let A(q),B(q)∈K[q] satisfy deg A≤1 and deg B≤1. Put

H=h(q)+A(q)p+B(q)p².

**Theorem.** Every polynomial static partner G satisfying T₅(H,G)=0 has degₚ G≤4. In particular S⁰(H) is contained in K[q]⊕pK[q]⊕⋯⊕p⁴K[q]. If B(q)=a+bq, the third gate on this five-row space is

T₃(H,G)=h'''(q)∂ₚ³G+6b∂q²∂ₚG.

**Proof.** The terms A(q)p and B(q)p² have total degree at most three, so all of their fifth-order partial derivatives vanish. The only fifth-order derivative of H is ∂q⁵H=h'''''(q), which is a nonzero linear polynomial because deg h=6. Consequently T₅(H,G)=h'''''(q)∂ₚ⁵G. Since K[q,p] is an integral domain and characteristic zero, this vanishes exactly when ∂ₚ⁵G=0, equivalent to degₚG≤4. The only nonzero third derivatives of H are ∂q³H=h''' and ∂q∂p²H=2b. The binomial coefficient 3 in T₃ yields the additional 6b∂q²∂ₚG term.

This applies to arbitrary sextic h and affine A,B. It does not classify the static coefficients or refinements, and does not extend unchanged to nonlinear A or B.
