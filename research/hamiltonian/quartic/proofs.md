# Complete graded classification for homogeneous quartic Hamiltonians

These are direct derivations for the present investigation. They use classical apolarity, transvectants and the binary-quartic Hessian. No priority claim is made. The finite calculations in `verify.py` accompany the all-degree proofs below.

## Exactness space and its grading

Work over a field K of characteristic zero, with one canonical pair (q,p). Write

\[
T_k(F,G)=\sum_{j=0}^{k}(-1)^j\binom{k}{j}
(\partial_q^{k-j}\partial_p^jF)
(\partial_q^j\partial_p^{k-j}G).
\]

Thus T_1 is the Poisson bracket, and the normalized Weyl–Moyal commutator is

\[
\frac{F\star G-G\star F}{i\hbar}
=T_1(F,G)-\frac{\hbar^2}{24}T_3(F,G)
+\frac{\hbar^4}{1920}T_5(F,G)-\cdots.
\]

A partner G is a polynomial independent of hbar. Exactness means equality as a polynomial/formal identity in hbar. For a nonzero homogeneous quartic H, derivatives of H of order five and higher vanish. Consequently its complete exactness space is E(H)=ker T_3(H,·). If V_n denotes the degree-n binary forms, T_3(H,·) maps V_n to V_(n−2). Terms of different homogeneous degrees in G produce different output degrees, so E(H) is the direct sum of its homogeneous pieces E_n(H). Constants and linear forms are automatic partners: dim E_0=1 and dim E_1=2. All quadratics are also automatic, so dim E_2=3.

A first dimension count already proves that every homogeneous quartic has infinitely many exact partners: for n≥2, dim V_n=n+1 and dim V_(n−2)=n−1, hence dim E_n≥2. There is no generic quartic for which sufficiently high-degree polynomial exact partners disappear. The real classification questions are the exact graded dimensions, explicit bases, commuting versus active partners, and closure under multiplication or evolution.

## The apolar adjoint theorem

For F=Σ_(j=0)^n f_j q^(n−j)p^j and G=Σ_(j=0)^n g_j q^(n−j)p^j, define the nondegenerate apolar pairing

\[
B_n(F,G)=\sum_{j=0}^{n}\frac{(-1)^j}{\binom nj} f_jg_{n-j}.
\]

It is symmetric for even n and alternating for odd n. For H∈V_4, G∈V_n and F∈V_(n−2), the exact adjoint identity is

\[
\boxed{
B_{n-2}(T_3(H,G),F)
=-6n(n-1)B_n(G,T_1(H,F)).
}
\]

Here n≥2. For n=2 both sides vanish. For n≥3 it suffices by trilinearity to take H=q^(4−i)p^i, G=q^(n−j)p^j and F=q^(n−2−ell)p^ell. Both sides are zero unless i+j+ell=n+1. In that case the coefficient of the left output is S_3(4−i,i;n−j,j), and the coefficient of T_1(H,F) is 4ell−i(n−2). The identity reduces to

\[
S_3\frac{(-1)^{i+j-3}}{\binom{n-2}{i+j-3}}
=-6n(n-1)\,[4\ell-i(n-2)]\frac{(-1)^j}{\binom nj}.
\]

There are only five types of H. For i=0, S_3=24j(j−1)(j−2); for i=1, S_3=6j(j−1)(4j−3n−2); for i=2, S_3=12j(n−j)(n−2j). Substituting ell=n+1−i−j and simplifying the binomial coefficients proves the displayed identity in each of these three cases. The cases i=3,4 follow by interchanging q and p, which changes the sign of each odd transvectant in the matching way. This proves the adjoint formula for every H,F,G, not only for sampled degrees.

Since the pairings are nondegenerate and −6n(n−1) is nonzero, the rank of T_3(H,·):V_n→V_(n−2) equals the rank of the Poisson map T_1(H,·):V_(n−2)→V_n. Rank–nullity therefore gives

\[
\boxed{\dim E_n(H)=2+\dim C_{n-2}(H)},\qquad
C_k(H)=\{F\in V_k:\{H,F\}=0\}.
\]

This identifies every extra quantum-exact partner dimension with an ordinary classical centralizer dimension two degrees lower.

## Homogeneous centralizers and the three complete rank strata

Factor H over an algebraic closure as H=a∏L_i^(m_i), with distinct linear factors L_i and Σm_i=4. Let g=gcd(m_i), and put e=4/g. Thus H=aR^g, where R is homogeneous of degree e and is not itself a proper polynomial power. The only possibilities are e=1,2,4.

For a homogeneous F of degree k, the condition {H,F}=0 can be analyzed on q≠0. Write H=q^4h(t), F=q^kf(t), t=p/q. Then {H,F}=q^(k+2)[4h f′−k h′f]. If F is nonzero, vanishing says that the derivative of f^4/h^k is zero, hence f^4=c h^k in characteristic zero. The same homogeneous identity is F^4=cH^k. Factorization then forces 4ν_i(F)=km_i at every root. Such nonnegative integral multiplicities exist exactly when e divides k, and in that case F is a scalar multiple of R^(k/e). Hence

\[
\dim C_k(H)=\begin{cases}1,&e\mid k,\\0,&e\nmid k.\end{cases}
\]

This statement descends to the original characteristic-zero field by preservation of matrix rank under field extension. It is also directly available from unique factorization when H=aR^g is chosen over K.

Combining with the adjoint theorem yields the complete all-degree classification

\[
\boxed{\dim E_n(H)=2+\mathbf 1_{e\mid(n-2)}\quad(n\ge2).}
\]

The Hilbert series is therefore

\[
\boxed{
\sum_{n\ge0}\dim E_n(H)t^n
=1+2t+\frac{2t^2}{1-t}+\frac{t^2}{1-t^e}.
}
\]

For a fourth power of a linear form, e=1, every n≥2 has dimension three. For a square of a nondegenerate quadratic, e=2, even n≥2 have dimension three and odd n have dimension two. Every quartic that is not a square of a quadratic has e=4: the dimension is three precisely at n≡2 mod4, and is two otherwise. In particular, the root-multiplicity types (3,1), (2,1,1) and (1,1,1,1) have exactly the same graded dimensions. Their actual basis vectors differ, but their Hilbert function does not. The zero Hamiltonian is excluded; for H=0 every polynomial is an exact partner.

## Explicit monomial normal forms

For H=q^4, T_3(H,G)=24q∂_p^3G. Thus

\[
E(q^4)=K[q]\oplus pK[q]\oplus p^2K[q].
\]

For H=q^3p, a monomial q^cp^d belongs to E(H) precisely when d=0, d=1, or d=3c+2. The operator maps distinct monomials to distinct output monomials, so no cancellation between distinct input monomials is possible. Consequently this monomial condition classifies every polynomial partner, by taking its linear span. In fixed degree n, the exceptional monomial occurs precisely when n=4c+2, producing the e=4 dimension jump.

For H=q^2p^2, the third transvectant on q^cp^d has coefficient 12cd(c−d), with output q^(c−1)p^(d−1). Hence the entire space has basis all pure powers q^n and p^n, together with the diagonal monomials (qp)^r. Constants are counted only once. This produces the e=2 dimension pattern.

Invertible linear coordinate changes preserve the zero conditions T_k=0: under A∈GL_2, T_k(F∘A,G∘A)=(det A)^kT_k(F,G)∘A. Symplectic changes (det A=1) preserve the full fixed-parameter canonical Moyal structure. General GL_2 changes preserve exactness while rescaling the deformation parameter in the full star-product covariance statement.

## A canonical noncommuting partner: the quartic Hessian

Define

\[
\Delta_H=H_{qq}H_{pp}-H_{qp}^2.
\]

For every homogeneous binary quartic,

\[
\boxed{T_3(H,\Delta_H)=0.}
\]

This can be proved by direct coefficient expansion. If H=aq^4+4bq^3p+6cq^2p^2+4dqp^3+ep^4, then

\[
\Delta_H=144[(ac-b^2)q^4+2(ad-bc)q^3p
+(ae+2bd-3c^2)q^2p^2+2(be-cd)qp^3+(ce-d^2)p^4].
\]

Substitution into the four-term derivative formula for T_3 cancels every coefficient. The supplied verifier also gives a complete exact interpolation certificate: each output coefficient is a polynomial of degree at most three in each of the five coefficients of H, and it vanishes at all 4^5 grid points with coefficient values 0,1,2,3. Iterated univariate interpolation therefore proves the universal identity over characteristic zero.

When H is not a square of a quadratic, H and Δ_H are linearly independent. To see the converse characterization precisely, examine a root L of multiplicity m<4. The Hessian has multiplicity exactly 2m−2 there: the leading coefficient is −3m(4−m) times a nonzero square. Thus Δ_H=cH with c≠0 forces every root to have m=2. If Δ_H=0, the same calculation forces H to have one quadruple root. Conversely, for H=Q^2, direct differentiation gives Δ_H=12(det D^2Q)H. Hence Δ_H is proportional to H exactly for quadratic-square quartics, including fourth powers.

For a primitive quartic, the homogeneous Poisson centralizer in degree four is the line KH. Thus Δ_H is noncommuting, and because dim E_4=2, one gets the exact basis

\[
\boxed{E_4(H)=\operatorname{span}\{H,\Delta_H\}}
\]

for every quartic H that is not a square of a quadratic. This is a canonical, coordinate-covariant construction of an active exact partner, not merely an existence count. The sextic Jacobian J_H={H,Δ_H} measures its noncommutation.

## The square-of-H trap and the exact commuting intersection

A polynomial function of H Poisson-commutes with H, but its ordinary product need not star-commute with H. For every homogeneous quartic H and integer r≥2,

\[
\boxed{
T_3(H,H^r)
=-\frac{r(r-1)(4r+1)}3 H^{r-2}\{H,\Delta_H\}.
}
\]

For proof, differentiation of H^r separates the third derivative into one-third-derivative, second/first-derivative, and three-first-derivative terms. The first contribution contracts to T_3(H,H)=0. The second contributes −3r(r−1)H^(r−2){H,Δ_H}. Euler homogeneity gives the third contribution through

\[
D^3H[(H_p,-H_q)^3]
=-\frac43H\{H,\Delta_H\}.
\]

Combining them gives the formula. More generally, for homogeneous degree m≥2, the same proof replaces (4r+1)/3 by (mr+m−3)/(m−1). The Euler identity can be checked at a point (1,0) in linear coordinates: write the first four affine coefficients of H, use H_q=mH, H_qq=m(m−1)H, and the analogous mixed-derivative identities, and the two cubic-gradient expressions agree term by term. Covariance and polynomial continuation then give the identity everywhere.

If H is primitive, its centralizer is K[H], and J_H≠0. Every H^r with r≥2 therefore fails exactness. Different powers produce different homogeneous output degrees and cannot cancel. The full commuting exact subspace is exactly span{1,H}. If H=Q^2 with Q nondegenerate quadratic, the centralizer is K[Q] and all its elements are exact; after a linear extension of scalars Q reduces to a scalar multiple of qp, where this is the diagonal-monomial computation above. For a fourth power H=L^4, the centralizer K[L] is likewise entirely exact. These facts separate large active families from merely commuting ones.

## Constructing every homogeneous partner by a finite recurrence

Let H=Σ_(i=0)^4 a_iq^(4−i)p^i and G=Σ_(j=0)^n b_jq^(n−j)p^j. Put b_j=0 outside 0≤j≤n. Then the complete necessary and sufficient equations are

\[
\sum_{i=0}^4 a_i b_{s+3-i}
S_3(4-i,i;n-s-3+i,s+3-i)=0,
\quad0\le s\le n-2.
\]

This is an explicit banded (n−1)×(n+1) rational/integer matrix. Its nullspace is exactly E_n(H); no higher-order constraint is hidden. A linear coordinate choice can ensure a_0≠0 for any nonzero H. Then the equations successively determine b_3,…,b_n from the three seeds b_0,b_1,b_2, followed by one terminal compatibility equation. The dimension theorem proves exactly when that final equation vanishes identically rather than imposing one condition.

For the important family H_λ=q^4+λq^2p^2+p^4, the recurrence simplifies to

\[
2(s+3)(s+2)(s+1)b_{s+3}
+\lambda(n-s-1)(s+1)(n-2s-2)b_{s+1}
-2(n-s+1)(n-s)(n-s-1)b_{s-1}=0.
\]

The Hessian and its Jacobian are

\[
\Delta_{H_\lambda}=24\lambda(q^4+p^4)+(144-12\lambda^2)q^2p^2,
\qquad
\{H_\lambda,\Delta_{H_\lambda}\}
=288(4-\lambda^2)qp(q^4-p^4).
\]

The square stratum is λ=±2. Two explicit cubic partners for every λ are q^2p−(λ/6)p^3 and qp^2−(λ/6)q^3. For λ^2≠4, the quartic partners are exactly span{H_λ,q^2p^2}. These formulas and the recurrence provide tractable all-degree constructions while the apolar theorem certifies the dimension at every step.

## Exact once does not mean exact under repeated evolution

The exactness space is generally neither an ordinary product algebra nor invariant under the Hamiltonian action. For H=q^4+p^4 and G=q^2p^2, the first normalized Moyal commutator equals the Poisson bracket K=8(q^5p−qp^5). But

\[
T_3(H,K)=-23040q^2p^2,
\quad
\frac{[H,K]_\star}{i\hbar}
=\{H,K\}+960\hbar^2q^2p^2.
\]

Thus G is exact for one Hamiltonian action, but the next action has a nonzero correction. Also H itself is exact while H^2 is not. Any claim about exact classical-versus-quantum trajectories needs a subspace invariant under the Hamiltonian derivation, not merely membership in E(H). This is a separate classification problem.

## Result and remaining scope

The complete graded dimensions of all polynomial Moyal-exact partners of every nonzero homogeneous quartic are now determined, and an explicit finite matrix/recurrence computes every basis at every degree. The organizing structures are apolar adjointness, the primitive polynomial root of H, and the Hessian/Jacobian covariants. Explicit bases for arbitrary coefficients at every degree need not have a simple single closed expression, but the recurrence is exhaustive and the all-degree dimension formula proves its rank. Higher-degree Hamiltonians require simultaneous higher odd-transvectant constraints, and nonlinear canonical coordinate changes do not automatically preserve this flat constant-coefficient Moyal product. Classification of invariant exact-dynamics spaces remains distinct from the static exact-partner problem solved here.
