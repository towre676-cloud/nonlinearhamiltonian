# Exact partners, closure and finite quantum ladders

All identities are in characteristic zero with one canonical pair, the Weyl product `star=exp[(i hbar/2)Lambda]`, and the normalized bracket `[H,G]_star/(i hbar)`. The parameter is formal and partners are hbar-independent polynomials. No statement concerns analytic domains of unbounded operators. `engine.py` independently expands the defining star exponential using exact Gaussian rational coefficients and polynomial derivatives; it does not call the closed falling-factorial coefficient formula used by other branches.

## The complete favorite space

Let `H=q p^3`, let `A=k[p] direct-sum q k[p]`, and define `E(H)` by exact equality of normalized Moyal and Poisson brackets. Since H has degree four, its sole possible correction is `−hbar² Lambda³(H,G)/24`. Direct differentiation gives

`Lambda³(H,G)=6(3p partial_p−q partial_q) partial_q² G`.

Distinct monomials have distinct images at this correction order. For a monomial `q^c p^d`, the scalar factor is `6c(c−1)(3d−c+2)`. Consequently the complete polynomial space is

`E(qp³)=k[p] direct-sum q k[p] direct-sum q² k[q³p]`.

The last direct summand is a vector-space/module description, not an assertion that E is an algebra. Its organizing variable `u=q³p` is invariant under the weighted Euler derivation `3p partial_p−q partial_q`. Equivalently, E is the preimage of the weighted invariant ring `k[u]` under the second q derivative. Integration twice accounts for the two free coefficient functions in A and the shifted resonant exponent line. Its Hilbert series is `(1+t)/(1−t)+t²/(1−t⁴)`; the homogeneous dimension is one in degree zero, two in degree one, and `2+1_(n congruent 2 mod4)` for n at least two.

## Three different structures

E is not an ordinary algebra: q² belongs to it and q⁴ does not. It is not a Poisson Lie algebra: q² and qp² belong to it, whereas their bracket `4q²p` does not. Neither statement depends on numerical tolerance or a finite-degree extrapolation.

The strip A is an exact Poisson Lie algebra. If `F=a(p)+q b(p)` and `G=c(p)+q d(p)`, then `{F,G}=bc'−a'd+q(bd'−b'd)`, again in A. Every odd Moyal contraction of order at least three requires more q derivatives across the two inputs than their total q degree permits, so this Lie bracket agrees exactly with the Moyal bracket for every pair in A. This is the semidirect polynomial vector-field/function algebra.

Write `L_P={H,.}` and `L_star=[H,.]_star/(i hbar)`. A is invariant under both. For every extra resonant basis element `C_r=q^(3r+2)p^r`, `L_P C_r=−(8r+6)q^(3r+2)p^(r+2)`, which lies outside E. Distinct r have distinct images, so their failures cannot cancel in a linear combination. Thus A is the full dynamically exact core: a polynomial has `L_star^n G=L_P^n G` for every n if and only if G lies in A. A is also the unique largest Poisson Lie subalgebra of E containing H: such a Lie subalgebra must be invariant under the bracket with H.

The associative question has a different answer. If a polynomial G has positive q degree c and its leading q coefficient has p degree d, then G³ has leading monomial `q^(3c)p^(3d)`. For that monomial to lie on the resonant exact line one would need `3c=9d+2`, impossible modulo three. Therefore `G³ in E` implies `G in k[p]`. Every ordinary associative subalgebra of E is contained in k[p], and k[p] is the unique maximal one. In particular no ordinary associative subalgebra contained in E can contain H.

## Every resonant partner has a second-action defect

Direct calculation yields the all-r identity

`L_star² C_r=(8r+6)(8r+4) q^(3r+2)p^(r+4)+(12r+9)(3r+2)(3r+1) hbar² q^(3r)p^(r+2)`.

The second term is nonzero for every nonnegative integer r. Exactness of the first commutator therefore does not imply equality of the full quantum and classical time evolutions. For r=0, the first action is `−6q²p²`, the classical second action is `24q²p⁴`, and the quantum second action adds `18hbar²p²`.

## Finite quantum ladders nonetheless survive

There is a stronger structure than that first-action identity. For any integer m at least two, take `H=q p^m`, nonnegative c,d, and assume `s=(c−d)/(m−1)` is a nonnegative integer. Put `N=s+c`. Then

`L_star^(N+1)(q^c p^d)=0`,

`L_star^N(q^c p^d)= (−(m−1))^N N! H^(star c)`,

and this top action is nonzero. The corresponding classical identities replace the star power by the ordinary power. This is a sufficient finite-ladder criterion, not a classification of every locally nilpotent observable.

Here is an algebraic proof. Use the faithful Weyl representation `p=x`, `q=i hbar D_x` over a characteristic-zero differential field with formal nonzero hbar. Weyl symmetrization sends H to `i hbar[x^m D_x+(m/2)x^(m−1)]`. Make the algebraic differential-field substitution `y=x^(−(m−1))`. The bracketed operator becomes `−(m−1)D_y+m/(2y)`. Conjugate by the multiplication operator `M=y^(m/[2(m−1)])`, adjoining a finite fractional power of y if necessary. Then `M^(-1) Hhat M=−(m−1)i hbar D_y`.

Normal ordering a Weyl monomial gives

`W(q^c p^d)=(i hbar)^c sum_j binom(c,j)(d)_j 2^(−j) x^(d−j)D_x^(c−j)`.

After the coordinate substitution and gauge conjugation, it has the form `(i hbar)^c sum_(ell=0)^c A_ell y^(s+ell)D_y^ell`, with rational constants A_ell and nonzero highest coefficient `A_c=(−(m−1))^c`. Because s is a nonnegative integer, all coefficient powers are nonnegative integers and their maximum is N. Commuting with `−(m−1)D_y` differentiates these coefficient polynomials. The action N+1 is zero; at action N only the highest derivative-order term survives. Its coefficient agrees exactly with `(−(m−1))^N N!` times the transformed Weyl operator of the c-th star power of H. Faithfulness and injectivity of localization pull the identity back into the original polynomial Weyl algebra. The calculation is algebraic; it does not require choosing an analytic branch of x or defining an operator on a Hilbert-space domain.

The classical proof is even shorter: `L_P(q^c p^d)=(d−mc)q^c p^(d+m−1)`. Successive coefficients are `(m−1)(j−N)`, so the N-th action is `(−(m−1))^N N!H^c` and the next action vanishes.

For the favorite family m=3, c=3r+2,d=r, one has s=r+1 and N=4r+3. Thus every C_r generates a finite quantum ladder of exact nilpotence index `4r+4`, terminating at a star power of H; its classical ladder terminates at the ordinary power. The intermediate ladders disagree from the second action onward.

For r=0 the entire formal flow is explicitly

`exp(t L_star)q²=q²(1−2tp²)^3+9hbar²t²p²(1−2tp²)`.

The classical flow is the first summand alone. Both are cubic polynomials in t. Their top derivatives agree with `L_star³q²=−48 H star H` and `L_P³q²=−48H²`, and `H star H=H²+(9/4)hbar²p⁴`.

## Independent review of arbitrary F and binary quartics

The independent verifier computes full bounded p-polynomial coefficient kernels separately in each q degree for ten nonhomogeneous fixtures H=qF(p). It agrees with the structural branch's all-degree classification: degree-two F gives the strip plus all q-only powers of degree at least two; degree-three F gives the strip plus `q^(3r+2)(F'')^r`; degree at least four gives the strip, q², and an extra q³R precisely when `F''=gamma R³`. This includes the nonmonomial example `F=p⁸/56+p⁶/10+p⁴/4+p²/2`, whose second derivative is `(p²+1)³` and whose additional partner is `q³(p²+1)`. Every tested extra coefficient-space vector leaves E after one classical action, while all strip vectors remain exact.

The binary-quartic branch's apolar adjoint identity was independently replayed using the direct-star engine. For raw coefficient pairing `B_n(A,B)=sum_j (−1)^j A_(n−j,j) B_(j,n−j)/binom(n,j)`, the identity is

`B_(n−2)(Lambda³(H,G),F)=−6n(n−1)B_n(G,{H,F})`.

Seven quartic normal forms, degrees two through sixteen, and exact random coefficient vectors all agree. The predicted homogeneous exact-partner dimension is `2+1_(e divides n−2)`, where e is the primitive root degree of H, and each tested Hessian determinant is an exact partner. These checks support the quartic branch's proof; they are not a substitute for its all-degree apolar/centralizer argument. A second-action failure was independently checked for `H=q⁴+p⁴`, `G=q²p²`: `K={H,G}=8(q⁵p−qp⁵)` is not in E(H), and the normalized Moyal correction on K is `960hbar²q²p²`.
