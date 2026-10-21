# Independent structural reductions for root integration

These are session derivations and elementary proofs, not claims of historical novelty. They complement the literature recovery. Work over an infinite characteristic-zero field and its extension as needed, with the canonical polynomial Weyl–Moyal convention. Let F_N be polynomials of total degree at most N and set F_k=0 for k<0. Define E(H) by equality of the scaled Moyal commutator and the Poisson bracket as a polynomial identity in the formal parameter hbar. Let C(H)=ker{H,·}.

## Quadratic perturbations do not change exact partner spaces

For every polynomial Q of degree at most two, E(H+Q)=E(H). Indeed every correction gate is an odd bidifferential contraction Λ^k(H,G) with k≥3, which vanishes on Q in the H input. The common Poisson/Moyal bracket itself changes by {Q,G}, so activity and Hamiltonian evolution can change even though the exact partner set does not.

## A centralizer growth bound with an elementary proof

For every nonconstant H, dim(C(H)∩F_N)≤N+1. Choose an affine line along which H is nonconstant. After an affine symplectic coordinate change it is q=0 and H_p(0,p) is a nonzero polynomial. Restriction to q=0 maps C(H)∩F_N into the N+1-dimensional space of one-variable polynomials of degree at most N. This restriction is injective: if a nonzero G in the centralizer vanishes on that line, write G=q^kJ with k≥1 and q not dividing J. Then

{H,G}=q^(k−1)(−k H_p J+q{H,J}).

Reducing the vanishing bracket divided by q^(k−1) modulo q gives −k H_p(0,p)J(0,p)=0. The polynomial ring in p is an integral domain and characteristic zero makes k nonzero. This contradicts q not dividing J. Hence restriction is injective, proving the bound without invoking a full polynomial-centralizer structure theorem.

## Every cubic has infinite exact active partners

If deg H=3, its sole correction gate is D_H=Λ³(H,·), a nonzero constant-coefficient differential operator of order three. On homogeneous degree n, it maps V_n to V_(n−3). Under the nondegenerate derivative/coefficient pairing its transpose is multiplication by a nonzero cubic, which is injective. Thus D_H is surjective in each degree and dim ker(D_H|V_n)=min(n+1,3). Quadratic perturbations leave this unchanged. Consequently for N≥2, dim(E(H)∩F_N)=3N.

The active dimension means the dimension of the image {H,E(H)∩F_N}, equivalently E(H)∩F_N modulo its intersection with C(H). The centralizer bound implies an active dimension at least 2N−1. This proves arbitrarily many linearly independent active directions for every polynomial cubic H. It does not assert that the partner space is closed under products, brackets between arbitrary partners, or repeated bracketing with H.

## Every quartic has infinite exact active partners

If deg H=4, again its sole correction gate is Λ³(H,·). Because its coefficients have degree at most one, D_H maps F_N into F_(N−2). For N≥1, rank-nullity gives

dim(E(H)∩F_N) ≥ dim F_N−dim F_(N−2) = 2N+1.

Combining this with the centralizer bound gives active dimension at least N. Therefore every polynomial quartic Hamiltonian, homogeneous or not, has an infinite-dimensional space of exact partners and arbitrarily many independent noncommuting exact directions. The statement is a dimension theorem; it is not a closed-form basis for every inhomogeneous quartic.

For homogeneous quartics, the other agent's stronger apolar-adjoint classification can determine the exact Hilbert function. The lower-bound theorem here shows that infinite-family existence through degree four is automatic. Thus the interesting distinction is the structure, sparse bases, rank jumps, symmetries and dynamical closure of those families. Degree five is the first degree at which the additional fifth-order gate can defeat this simple dimension argument; this observation does not by itself classify quintics or prove generic finite dimensionality.
