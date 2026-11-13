# Exact all-degree refinement classification of H=q^6+qp²

Let K be a characteristic-zero field and H=q⁶+qp². With T₃ and T₅ the usual odd transvectants, D=T₁(H,-), and Sʳ={G : DⁱG∈ker T₃∩ker T₅ for 0≤i≤r}, the following holds in K[q,p].

**Theorem.** S⁰ is infinite-dimensional; dim S¹=6, dim S²=3, and S³=D∞=span_K{1,H}.

**Proof (no degree cutoff).** T₅(H,G)=720q ∂ₚ⁵G and T₃(H,G)=120q³∂ₚ³G+6∂q²∂ₚG. Therefore G∈S⁰ iff G=∑_{j=0}⁴ gⱼ(q)pʲ with

g₄=c+dq, g₃=a+bq,
g₂=g+hq−12cq⁵−8dq⁶,
g₁=e+tq−6aq⁵−4bq⁶,
g₀=F(q) arbitrary.

Here a,b,c,d,e,t,g,h∈K. Thus S⁰ is infinite-dimensional.

D=(6q⁵+p²)∂ₚ−2qp∂q. For G in this general form, the p⁵ coefficient of DG is 4c+2dq, while the p¹ and p² coefficients of T₃(H,DG) are respectively 720q³(36a+35bq) and 1440q³(50c+49dq). The first-refinement equations force a=b=c=d=0. The remaining p⁰ equation is

qF''' +2F''=240gq³+180hq⁴.

Since F is a polynomial in characteristic zero, its complete solution is F=u+vq+(12/5)gq⁵+hq⁶. Hence

S¹={u+vq+(12/5)gq⁵+hq⁶+(e+tq)p+(g+hq)p² : u,v,e,t,g,h∈K},

a six-dimensional space. Its elements satisfy T₃(DG)=T₅(DG)=0 by direct substitution.

For G in this S¹, the exact second-refinement obstruction is

T₃(H,D²G)=2160q³(-2e-7tq+24gp),   T₅(H,D²G)=0.

Thus e=t=g=0, giving S²={u+vq+hH}, of dimension three.

Finally, for G=u+vq+hH, the third-refinement obstruction is

T₃(H,D³G)=30240q⁴v,   T₅(H,D³G)=0.

Therefore v=0, so S³=span{1,H}. Both 1 and H lie in every refinement since D1=DH=0, proving the persistent-core statement.

**Verification status.** The coefficient identities were independently checked with SymPy using arbitrary symbolic F(q) and exact rational arithmetic. This is a human all-degree proof, not a Lean formalization. The theorem covers this specific mixed quadratic boundary, not general h(q)+A(q)p+B(q)p².
