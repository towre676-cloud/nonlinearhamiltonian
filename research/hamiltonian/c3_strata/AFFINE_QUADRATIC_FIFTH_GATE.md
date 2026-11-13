# Complete all-degree classification: affine quadratic-momentum sextics

Let K be characteristic zero, h∈K[q] have degree six, A=a₀+a₁q, B=b₀+b₁q with b₁≠0, and H=h(q)+A(q)p+B(q)p². Write D=T₁(H,-), S⁰=ker T₃(H,-)∩ker T₅(H,-), and Sʳ={G∈S⁰ : DⁱG∈S⁰ for 0≤i≤r}.

**Theorem.** The static space is infinite-dimensional, with the complete description

S⁰={f(q)+p(λA(q)+aq+d)+p²(λB(q)+μ)+p³(u+vq)+p⁴(w+xq) plus polynomial corrections to the p and p² coefficients forced by the cubic gate},

where the complete and unambiguous description of those corrections is given by the equations

g₄=w+xq, g₃=u+vq, g₂''=−2h'''g₄/b₁, g₁''=−h'''g₃/b₁, and g₀ arbitrary.

**The complete refinements are**

S¹(H)=span_K{1,q,p,qp,H}, dim 5;
S²(H)=span_K{1,q,H}, dim 3;
S³(H)=D∞(H)=span_K{1,H}, dim 2.

All claims hold for every sextic h and every affine A,B with b₁≠0, without truncating the observable degree.

## Proof

Because A p+B p² has total degree at most three, T₅(H,G)=h'''''∂ₚ⁵G. Since h'''''≠0, degₚG≤4. The third gate is T₃(H,G)=h'''∂ₚ³G+6b₁∂q²∂ₚG. Equating its coefficients gives the complete static description above.

For G∈S¹, write the static coefficients as g₄=w+xq, g₃=u+vq, g₂, g₁, g₀. The coefficient of p⁵ in DG is 4b₁g₄−2Bg₄'; since B is nonconstant affine and g₄ affine, its vanishing forces g₄=0. Similarly, the coefficient of p⁴ then forces g₃=0. Thus G=f(q)+p(λA+aq+d)+p²(λB+μ). The coefficient of p³ in DG is 2μb₁, so μ=0. The remaining third-gate condition on DG reduces to (B(f−λh)')''=0. Since B is nonconstant affine and f−λh is polynomial, this forces f−λh to be affine. Hence G=λH+u+vq+p(aq+d), giving S¹ as claimed. Direct substitution proves the converse.

For this general S¹ element, symbolic differentiation gives T₅(H,D²G)=0 and the p⁰ coefficient of T₃(H,D²G) has q⁴ coefficient −15120 a b₁² times the leading coefficient of h. Therefore a=0. With a=0, its q³ coefficient is −4320 d b₁² times the leading coefficient of h. Hence d=0. Conversely every λH+u+vq passes the first two refinements, so S²=span{1,q,H}.

Finally, for G=λH+u+vq, T₃(H,D³G) has q⁴ coefficient 30240 v b₁³ times the leading coefficient of h, forcing v=0. Conversely 1 and H lie in every refinement, proving S³=D∞=span{1,H}.

The coefficient identities have an independently runnable SymPy replay, including arbitrary sextic lower coefficients. This is an all-degree human proof with exact symbolic checks, not a Lean-formalized theorem.

## Boundary and scope

When b₁=0 the static space instead equals K[q]⊕pK[q]⊕p²K[q]; the above refinement theorem does not assert its behavior. When B is nonlinear, fifth-order derivatives of Bp² may contribute, and this argument must be modified. No claim of complete 21-parameter classification is made.
