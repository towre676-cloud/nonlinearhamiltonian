# Complete cubic partner classification by root multiplicity

This supplement is an all-degree theorem, not an extrapolation of the checks. Work over an algebraically closed characteristic-zero field; rational/real kernels are recovered by taking the corresponding field-valued part. Let H be any polynomial of degree exactly three, and let H3 be its top homogeneous part. Every lower-degree term has zero third derivatives, and no correction beyond order three is possible. Therefore E(H)=ker[H3(partial_p,−partial_q)].

Factor `H3=gamma product_i ell_i^(m_i)`, with pairwise nonproportional linear forms ell_i, positive multiplicities m_i and sum m_i=3. Let `D_i={ell_i,.}` and choose a linear form t_i with `D_i t_i=1`. Then the complete ordinary polynomial partner space is

`E(H)=sum_i sum_(j=0)^(m_i−1) t_i^j k[ell_i]`.

The sums are vector-space sums, generally not direct. In particular every degree-three Hamiltonian has an infinite-dimensional exact partner space, organized by the three root multiplicity patterns of its top binary cubic.

If all three roots are distinct, the solution is the sum of three univariate polynomial families k[ell_i]. For a double root and a simple root, it is `(k[ell_1]+t_1 k[ell_1])+k[ell_2]`. For a triple root, it is `k[ell]+t k[ell]+t²k[ell]`. These descriptions hold even if arbitrary linear, quadratic and constant terms are added to H. A term such as H² is not thereby asserted to be a partner: the displayed space must be used.

Proof of inclusion: the correction differential operator is exactly `Lambda³(H,G)=6 H3(partial_p,−partial_q)G=6gamma product_i D_i^(m_i)G`. All D_i commute because their coefficients are constant. Every summand `t_i^j F(ell_i)` is killed by D_i^(m_i) when j<m_i, hence is killed by the full product.

For completeness, the operator on homogeneous degree n polynomials maps V_n to V_(n−3). Under a nondegenerate apolar pairing its transpose is, up to a nonzero scalar, multiplication by H3. Multiplication is injective because the polynomial ring is a domain. Consequently the correction map is surjective for n>=3 and its kernel has dimension `(n+1)−(n−2)=3`. For n=2 its kernel is all V2, also dimension three; V0 and V1 have dimensions one and two.

The proposed families span exactly that many dimensions in each degree. Choose a projective chart in which `ell_i=q+lambda_i p`, with distinct lambda_i, and use `t_i=p`; this can always be achieved after an invertible linear coordinate change. For n>=2 the three displayed degree-n candidates `p^j(q+lambda_i p)^(n−j)`, with j<m_i, are scalar multiples of the lambda-derivatives of `(q+lambda p)^n`. Their first three coefficient rows form, after nonzero row/column scalings, the confluent Vandermonde matrix for the distinct nodes lambda_i with multiplicities m_i. Its determinant is nonzero, so their span has dimension three. In degrees zero and one the same families span V0 and V1. Inclusion plus the exact dimension proves the complete formula. An invertible linear change only changes the Poisson tensor by a nonzero determinant scalar, which does not affect vanishing of this correction kernel; an affine symplectic change preserves the full stated Weyl convention directly.

Equivalently, `dim E(H)_0=1`, `dim E(H)_1=2`, and `dim E(H)_n=3` for every n>=2. The Hilbert series is `1+2t+3t²/(1−t)`. This gives a universal large-family theorem for cubic Hamiltonians and an explicit root-multiplicity organization of all partners. It does not assert product closure, Lie closure or all-time quantum/classical agreement.
