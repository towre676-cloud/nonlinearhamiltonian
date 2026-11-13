# Complete static classification for affine quadratic-momentum coefficients

Let K be a characteristic-zero field, let h(q)∈K[q] have degree six, and let A(q),B(q)∈K[q] satisfy deg A≤1 and deg B≤1. Put H=h(q)+A(q)p+B(q)p², and define S⁰(H)=ker T₃(H,-)∩ker T₅(H,-).

**Theorem (all polynomial degrees).** Every G∈S⁰(H) has degₚG≤4. Write G=∑_{j=0}⁴ g_j(q)pʲ and B(q)=b₀+b₁q.

If b₁≠0, the complete static classification is

- g₀∈K[q] arbitrary;
- g₃,g₄∈K[q] arbitrary of degree at most one;
- g₁ and g₂ are the polynomial solutions, unique up to affine summands, of
  g₁''=−h'''g₃/b₁ and g₂''=−2h'''g₄/b₁.

Thus S⁰(H) is isomorphic as a K-vector space to K[q]⊕K⁸, with four coefficients in g₃,g₄ and four integration constants. In particular it is infinite-dimensional.

If b₁=0, the complete static classification is G=g₀(q)+p g₁(q)+p²g₂(q) with g₀,g₁,g₂ arbitrary, i.e. S⁰(H)=K[q]⊕pK[q]⊕p²K[q].

**Proof.** The terms A(q)p and B(q)p² have total degree at most three, so their fifth-order partial derivatives vanish. Since h has degree six, T₅(H,G)=h'''''(q)∂ₚ⁵G and h'''''≠0, hence degₚG≤4.

The third gate is T₃(H,G)=h'''(q)∂ₚ³G+6b₁∂q²∂ₚG. Its coefficients at p³,p²,p¹,p⁰ respectively are

24b₁g₄'', 18b₁g₃'', 24h'''g₄+12b₁g₂'', 6h'''g₃+6b₁g₁''.

For b₁≠0, these equations yield exactly the stated solutions, and each polynomial right-hand side has a polynomial double antiderivative in characteristic zero. For b₁=0, h'''≠0 forces g₃=g₄=0, leaving g₀,g₁,g₂ arbitrary. Conversely every displayed solution satisfies both gates.

**Scope.** This classifies the entire static space for affine A,B, not just its momentum-quadratic sector. It does not classify S¹ or the persistent core, nor non-affine B(q). The proof is elementary and all-degree but not yet Lean formalized.
