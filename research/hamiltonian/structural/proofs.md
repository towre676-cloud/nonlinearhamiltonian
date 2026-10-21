# Structural exact partners for polynomial Weyl–Moyal brackets

These are theorem-level derivations for a fixed canonical Weyl–Moyal product, together with finite exact fixtures. They are not a priority claim. The familiar algebra of functions affine in one Lagrangian half of the variables is a classical coordinate algebra; the useful classification here is the exact partner space for an individually specified Hamiltonian, and its dynamically coherent part. All polynomial coefficient fields have characteristic zero. Factorization statements may be read over the complex numbers, with real subspaces obtained by conjugation invariance.

## Definitions and the distinction that matters

Write Λ(H,G)=H_qG_p−H_pG_q and let Λ^k denote the k-fold constant Poisson-bivector contraction, not composition of the unary Hamiltonian derivation. Explicitly,

Λ^k(H,G)=Σ_{j=0}^k (−1)^j binom(k,j) (∂_q^{k−j}∂_p^j H)(∂_q^j∂_p^{k−j}G).

For polynomial symbols, the normalized Moyal bracket is the finite formal expression

M_HG=[H,G]_⋆/(iℏ)=Σ_{r≥0} (−1)^r ℏ^{2r} Λ^{2r+1}(H,G)/(2^{2r}(2r+1)!).

Thus E(H)={G:M_HG=Λ(H,G) as a polynomial in ℏ} is exactly the intersection of ker Λ^{2r+1}(H,·), r≥1. This definition requires every correction coefficient to vanish. An accidental equality at one numerical value of ℏ is a different problem.

The space E(H) is a vector space. It need not be an algebra, a Poisson Lie algebra, or an invariant space for the classical Hamiltonian derivation D_HG=Λ(H,G). Define D∞(H)={G:D_H^rG∈E(H) for every r≥0}. This is exactly the space on which all iterated Moyal and Poisson actions coincide: induction proves one direction, and applying M_H to the equality of the r-th iterates proves the converse. Consequently the two formal Heisenberg flows agree coefficient by coefficient in time exactly on D∞(H). No analytic operator-domain assertion is being made.

## The complete arbitrary-F classification for H=qF(p)

Let F be a polynomial of degree M≥2, and write A=k[p]⊕qk[p]. Then E(qF) has the following complete classification.

If M=2, E(qF)=A⊕q²k[q].

If M=3, put y=F'', a nonconstant affine polynomial. Then E(qF)=A⊕span{q^{3r+2}y^r:r≥0}.

If M≥4, E(qF)=A⊕kq², with one additional line kq³R(p) precisely when F''=γR(p)³ for a nonzero constant γ and a polynomial R. If F'' is not a constant multiple of a polynomial cube, there is no such line. The direct sums here are vector-space sums, not assertions of multiplicative or Lie closure.

This result covers arbitrary coefficients and every polynomial degree. In particular, the high-degree exception is governed by the multiplicities of the roots of F'': all must be divisible by three. Over the reals, the nonzero scalar γ can absorb its own cube root. The integer degree M−2 must be divisible by three when the exceptional line occurs, but degree divisibility alone does not suffice.

To prove the classification, decompose G=Σ_{c≥0}q^c A_c(p). Because H has q-degree one, only two terms survive in Λ^k for odd k≥3:

Λ^k(qF,q^c A_c)=(c)_{k−1}q^{c−k+1}[kF^{(k−1)}A_c'−(c−k+1)F^{(k)}A_c].

Different c give different output q-degrees for each fixed k, so cancellation between distinct c is impossible. For c=0,1 every expression vanishes, which gives A. For c≥2 the k=3 condition is

3F''A_c'−(c−2)F'''A_c=0.

A nonzero polynomial solution is unique up to a constant, since two solutions have constant ratio in k(p). If M=2, F'' is constant and the condition is A_c'=0. Every higher condition vanishes automatically, giving q²k[q]. If M=3, set y=F''; the equation becomes 3yA_c'=(c−2)y'A_c. Expanding around the unique root of y forces A_c to be a scalar multiple of y^{(c−2)/3}. It is polynomial exactly when c=3r+2. Again all k≥5 conditions vanish because F has degree three.

Now suppose M≥4. At c=2 the condition gives A_2 constant. At c=3 it gives 3yA_3'=y'A_3, or equivalently (A_3³/y)'=0. A nonzero solution therefore exists exactly when y=γA_3³. For c=3 every k≥5 expression has the factor (c)_{k−1}=0, so this condition is sufficient.

It remains to exclude every c≥4. Let d=deg A_c. Comparing the leading terms of the k=3 equation gives d=(M−2)(c−2)/3. The k=5 equation then has leading scalar factor

5d−(M−4)(c−4)=2[(M+1)(c+1)−15]/3.

This is strictly positive when M,c≥4. The remaining leading factors, including (M)_4(c)_4 and the leading coefficients, are nonzero. Hence the fifth-order condition fails. This completes the unrestricted classification. The simultaneous third- and fifth-order constraints suffice because q-degree three is the only exceptional degree left after that exclusion.

For a concrete high-degree example, take F=5p⁸+28p⁶+70p⁴+140p². Then F''=280(p²+1)³, so q³(p²+1) is an additional exact partner for the degree-nine Hamiltonian qF. The partner exists because a polynomial cube appears in the second derivative, even though F itself is not a monomial. Replacing F by a generic degree-eight polynomial destroys that extra line. Every Hamiltonian in this class nevertheless retains the infinite-dimensional strip A.

## The coherent core and its maximality

For every F of degree M≥2,

D∞(qF)=A=k[p]⊕qk[p].

Indeed D_{qF}(q^cA_c)=q^c(FA_c'−cF'A_c), so q-degree is preserved. The subspace A is invariant. For c≥2, the exact coefficient space is at most one-dimensional by the k=3 equation. Its nonzero A_c has degree d=(M−2)(c−2)/3. The leading coefficient of FA_c'−cF'A_c is proportional to

d−cM=−2[(M+1)c+(M−2)]/3,

which never vanishes. Its degree is M+d−1>d, so it cannot be proportional to A_c. Thus every exceptional q-degree component exits E after just one classical action. No cancellation across q-degrees can rescue it. In fact the first invariant-space refinement E∩D_H^{-1}E already equals A.

The space A is a Poisson Lie algebra and is pairwise Moyal-exact. For G=qA(p)+B(p) and K=qC(p)+D(p),

{G,K}=q(AC'−A'C)+(AD'−B'C).

It has q-degree at most one. For odd derivative orders at least three, the total required q-differentiation exceeds the sum of the two available q-degrees, so every Moyal correction vanishes. If L⊆E(qF) is any Poisson Lie subalgebra containing qF, it must be invariant under ad_{qF}, and hence L⊆D∞(qF)=A. Therefore A is the unique largest Poisson Lie subalgebra of exact partners containing this Hamiltonian. This is much stronger than merely observing several individually exact brackets.

The algebra has a direct operator interpretation. In the momentum representation, Weyl quantization sends qF(p)+B(p) to iℏ(F∂_p+F'/2)+B. These are first-order transport operators with the half-density correction. First-order operators close under commutators, and the polynomial symbol bracket above matches their normalized commutator. This explains the coherent core structurally. It also explains why special higher-order resonant partners can be individually exact and yet fail to form an invariant quantum-classical sector.

For the motivating H=qp³ and G=q², the first bracket is exactly −6q²p². The second Moyal action is 24q²p⁴+18ℏ²p², while the second classical action is 24q²p⁴. One-step agreement therefore does not establish exact time evolution. The infinite family q^{3r+2}p^r lies outside the coherent core and likewise leaves the exact space after one Hamiltonian action.

## Every cubic Hamiltonian has large exact families

Let H have nonzero homogeneous cubic part H₃, with arbitrary terms of degree at most two. Then

E(H)=ker H₃(∂_p,−∂_q).

The overall factor 6 in Λ³ is immaterial, and every odd contraction of order at least five vanishes. The remaining operator is constant-coefficient and homogeneous of differential order three. On the homogeneous degree-n space k[q,p]_n, its kernel has dimension min(n+1,3). Hence the cumulative space through total degree N has dimension 3N for every N≥2. This proves unbounded exact families for every cubic Hamiltonian, including generic cubics; it is not a bounded numerical observation.

For completeness, the degreewise differential map k[q,p]_n→k[q,p]_{n−3} is surjective. Under the perfect apolar pairing, its transpose is multiplication by the nonzero cubic H₃ with a fixed invertible coordinate rotation. Multiplication by a nonzero polynomial is injective in the polynomial ring. The differential map consequently has full target rank, giving the stated kernel dimension.

The geometry is the factorization of the binary cubic. Over the complex numbers write H₃=γ∏ℓ_i^{m_i}, where the distinct linear forms ℓ_i=a_iq+b_ip have multiplicities summing to three. Let L_i=a_i∂_p−b_i∂_q; it annihilates ℓ_i. Choose a transverse linear form t_i with L_it_i=1. Then the full exact partner space is the sum of the spaces

Σ_{j=0}^{m_i−1} t_i^j k[ℓ_i].

These sums overlap in low degree; no direct-sum assertion is intended. To prove completeness, in each homogeneous degree the annihilator of ker L_i^{m_i} is the image of multiplication by the corresponding dual linear form to power m_i. The intersection of these principal homogeneous ideals is their product because distinct linear forms are coprime. Taking orthogonal complements shows that the sum of the individual kernels is precisely the kernel of the product operator.

A pure cube ℓ³ gives a transverse-degree-two strip. A double factor ℓ²m gives two transverse layers along ℓ plus one arbitrary-function family along m. Three distinct factors give three characteristic arbitrary-function families. For H=q³+p³ these are the three line directions ℓ=q+λp satisfying λ³=1. Over the reals, one real family and the real and imaginary parts of the conjugate families supply real polynomial solutions.

There are unbounded-degree noncommuting partners in every cubic case. If H₃ is not a pure cube, choose a factor ℓ on which H₃ is not solely a function; then {H,ℓ^n} has a nonzero leading term for all n≥1. If H₃ is a pure cube, use tℓ^n with a transverse t. Lower-degree terms of H cannot cancel these leading contributions.

## General preservation and failure principles

Adding any polynomial Q of total degree at most two leaves E unchanged: E(H+Q)=E(H), since Λ^k(Q,G)=0 for all k≥3. This is equality of one-step exactness spaces. It does not imply equality of dynamic cores. The root investigation supplies the striking reviewed example H=qp³+q², for which E(H)=E(qp³), but D∞(H)=span{1,H}. With Y=q+p³/2, the first two refinements give E₁={cH+A(p)+q(b₁p+b₀)} and E₂=span{1,p,p²,Y,pY,H}. The identities Dp=2Y, DY=3p⁵/2, Dp²=4pY and D(pY)=2H+2p⁶ force every invariant subspace of E₂ into span{1,H}. To see the finite refinement explicitly, the extra resonant terms q^{3r+2}p^r with r≥1 are eliminated from E₁ by their distinct q-degree residue classes. For G=u q²+A(p)+qB(p), the q² coefficient of DG is 2B′−6up², which must be constant; therefore B=up³+b₁p+b₀ and G=uH+A+q(b₁p+b₀). Its derivative is DG=p³A′+q(2A′−2b₁p³−3b₀p²)+2b₁q². Membership in E₁ forces A′=2b₁p³+(3/2)b₀p²+linear, and integration yields exactly the displayed six-dimensional E₂. Since p⁵ and p⁶ are linearly independent modulo E₂, any invariant subspace of E₂ has zero Y and pY components. The images of p and p² then force those coefficients to vanish as well. This proves the full invariant-core claim. The calculation was independently checked here, but the root owns its derivation and separate verification.

Affine symplectic transformations preserve every Λ^k by the ordinary chain rule and preservation of the constant Poisson tensor. They therefore transport E and D∞ exactly. Translations and nonzero scalar rescaling of H also preserve the corresponding classifications. Ordinary nonlinear canonical substitutions do not have this covariance for unchanged Weyl symbols. In canonical coordinates (Q,P), P³ and Q²P are exact partners. The canonical shear Q=q, P=p+q² gives H=(p+q²)³ and G=q²(p+q²), for which Λ³(H,G)=−72q and all higher odd contractions vanish. Thus the normalized Moyal bracket acquires the correction 3ℏ²q. A nonlinear canonical transformation requires its own corrected quantization; simply substituting symbols is insufficient.

Exact partner spaces need not be multiplicatively or Lie closed. For H=p³, both q and q² are exact, but their product q³ is not. Both q² and q²p are exact, but their Poisson bracket 2q³ is not. These are explicit polynomial counterexamples, with no operator-domain subtlety.

## Lagrangian degree, several degrees of freedom and composition

A useful sufficient condition is a transverse-degree budget. In canonical variables (q₁,…,q_n,p₁,…,p_n), if H has total q-degree at most r, G has total q-degree at most s, and r+s≤2, all odd Moyal corrections vanish. Every order-k Poisson contraction differentiates in q a total of k times across the two symbols, which is impossible for k≥3 under that budget. Arbitrarily high p-degrees are permitted. Thus a Hamiltonian quadratic in the q-variables has every polynomial in p as an exact partner; a Hamiltonian affine in q has every other q-affine polynomial as an exact partner.

The coherent multi-dimensional coordinate algebra is A_n={Σ_iq_iF_i(p)+B(p)}. It is pairwise Moyal-exact and Poisson Lie closed. Its Hamiltonian equations are ṗ=−F(p), q̇=(DF(p))ᵀq+∇B(p). The nonlinear evolution of p can therefore coexist with an infinite exact symbol sector. This is a known transport/cotangent-lift mechanism, not a claim that arbitrary nonlinear Hamiltonians admit universal exact quantization.

For H=F(L), where L is a nonconstant affine linear observable and deg F≥3, the complete exact partner space in any number of degrees of freedom is ker X_L³, where X_L={L,·} is a constant directional derivative. Indeed Λ³(H,G)=F'''(L)X_L³G, up to the fixed harmless convention sign. The polynomial ring is an integral domain, so the third-order condition forces X_L³G=0; then all higher conditions vanish. In a conjugate coordinate Q, this is exactly degree at most two in Q, with arbitrary dependence on L and the spectator variables. Since X_LF'(L)=0, D_H=F'(L)X_L preserves this space, so D∞=E in this class.

If H depends on one canonical pair only, its exact partner space extends by arbitrary polynomial coefficients in spectator variables: E_n(H)=E_1(H)⊗k[spectators]. This is a vector-space statement; the extension need not be Lie closed because the spectator variables have their own Poisson brackets. If H=Σ_i H_i(q_i,p_i), products ∏_iG_i with G_i∈E(H_i) are exact partners, since each contraction differentiates H_i only in its own pair. This proves an inclusion of the tensor product of the individual exact spaces, not equality: cancellations between components can create additional partners.

A separable Hamiltonian V(q)+T(p) always admits the nine-dimensional biquadratic space span{q^ap^b:0≤a,b≤2}. Both third pure derivatives of such a G vanish. This finite sufficient sector alone does not prove an infinite high-degree classification for arbitrary separable potentials. The cubic theorem supplies such a classification when the highest degree is three; higher-degree separable cases require their own simultaneous constraints.

## What is proved and what is still open

The arbitrary-F qF theorem is a complete polynomial partner classification, with no degree cutoff. Its dynamically coherent and largest-Lie core is also classified completely. Every cubic Hamiltonian has a complete characteristic-PDE description and a proved degreewise Hilbert function. Single-linear-coordinate Hamiltonians have a complete transverse-strip classification in any dimension. Affine symplectic covariance, quadratic-perturbation invariance of E, closure failures and nonlinear-canonical covariance failure are exact statements with explicit proofs.

The companion quartic investigation supplies a complete graded classification for nonzero homogeneous binary quartics through apolarity and a constructive recurrence. The remaining general boundary is arbitrary inhomogeneous quartics and higher-degree polynomial Hamiltonians, including their dynamically invariant exact cores. A large one-step partner space and a large dynamically coherent core are different objectives. The appropriate next invariant is the pair (E(H),D∞(H)), supplemented by the exact Lie sectors inside it. Quadratic perturbations can preserve the first component and radically shrink the second. This is a structural reason to classify dynamics as well as isolated commutators.
