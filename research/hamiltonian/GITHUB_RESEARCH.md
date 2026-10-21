<!-- GitHub reading edition: delimiters and relative links adapted from output/Nonlinear_Hamiltonian_Partners.md; original preserved. -->


# Nonlinear Hamiltonians with exact classical–quantum partners

## A classification by size, closure and dynamics

**Research note · 21 October 2026.** One canonical pair, polynomial observables, exact rational computation and proofs valid in all degrees where stated. This note develops the question raised by the identity for $H=qp^3$. It separates newly derived results in this investigation from classical structures and the existing PerfectJet sextic programme. Mathematical priority is not claimed. The accompanying executable checks support their named finite identities and models; the all-degree conclusions rest on the displayed proofs.

## What the question becomes

Fix the canonical Poisson bracket $\{F,G\}=F_qG_p-F_pG_q$ and the Weyl–Moyal product with bidifferential exponential $\exp[(i\hbar/2)(\overleftarrow\partial_q\overrightarrow\partial_p-\overleftarrow\partial_p\overrightarrow\partial_q)]$. Work over a characteristic-zero field; rational examples and all delivered calculations use exact fractions. Write

$$
T_k(F,G)=\sum_{j=0}^k(-1)^j\binom kj
F_{q^{k-j}p^j}G_{q^jp^{k-j}}.
$$

The normalized bracket has the finite polynomial expansion

$$
L_\star^H G:=\frac{H\star G-G\star H}{i\hbar}
=\{H,G\}-\frac{\hbar^2}{24}T_3(H,G)
+\frac{\hbar^4}{1920}T_5(H,G)-\cdots.
$$

A partner $G$ is independent of $\hbar$. Exactness means a polynomial identity in $\hbar$, equivalently the vanishing of every higher odd transvectant. This is stronger than equality after inserting one chosen numerical value of $\hbar$. Define

$$
\mathcal E(H)=\bigcap_{j\ge1}\ker T_{2j+1}(H,\cdot),
\qquad D_H=\{H,\cdot\}.
$$

The space $\mathcal E(H)$ is linear. It need not be an associative algebra, a Poisson Lie algebra, or invariant under $D_H$. To discuss active partners, quotient out $\mathcal E(H)\cap\ker D_H$. “Infinitely many active partners” below means that this quotient is infinite dimensional, rather than the trivial observation that scalar multiples give infinitely many elements.

The space that supports exact repeated classical–quantum actions is

$$
\mathcal D(H)=\{G:D_H^jG\in\mathcal E(H)\ \text{for every }j\ge0\}.
$$

It is the largest $D_H$-invariant linear subspace of $\mathcal E(H)$. On it, every formal Taylor coefficient of the classical and quantum evolutions agrees. This statement concerns algebraic formal time evolution; global analytic flow, operator domains and completeness require further assumptions.

The resulting classification has several strong answers. Every cubic and every quartic Hamiltonian has an infinite-dimensional active exact-partner quotient. Homogeneous quartics admit a complete all-degree dimension formula governed by a classical apolar duality. The family $qF(p)$ admits a complete polynomial-partner classification for arbitrary coefficients and arbitrary degree. Monomial Hamiltonians admit a complete criterion for infinite active families and an effective finite algorithm in the remaining unequal-exponent cases. Closure and repeated evolution select smaller structures, including a known coordinate Lie algebra and explicit finite quantum ladders.

## A universal reason cubic and quartic families are large

Let $\mathcal P_{\le N}$ be the polynomials of total degree at most $N$, of dimension $(N+1)(N+2)/2$. If $\deg H\le4$, only $T_3$ can obstruct exactness, and

$$
T_3(H,\cdot):\mathcal P_{\le N}\longrightarrow\mathcal P_{\le N-2}.
$$

Consequently, for $N\ge2$,

$$
\boxed{\dim(\mathcal E(H)\cap\mathcal P_{\le N})\ge2N+1.}
$$

This argument includes inhomogeneous quartics. It does not need a genericity assumption or a special factorization. Adding any polynomial $Q$ of degree at most two preserves the entire exactness space, because every derivative of $Q$ of order at least three vanishes:

$$
\boxed{\mathcal E(H+Q)=\mathcal E(H).}
$$

To ensure that large spaces are not explained entirely by commuting observables, an elementary centralizer estimate suffices. For nonconstant $H$, choose affine symplectic coordinates and a line $q=0$ with $H_p(0,p)\ne0$. Restriction to that line is injective on the polynomial Poisson centralizer. Indeed, if a commuting polynomial vanishes there, write $G=q^kJ$ with $k\ge1$ and $J(0,p)\ne0$. The leading $q$-adic coefficient of $\{H,G\}$ is $-kH_p(0,p)J(0,p)$, a nonzero polynomial. This contradicts commutation. Restricted polynomials have degree at most $N$, so the centralizer through degree $N$ has dimension at most $N+1$. Therefore

$$
\boxed{
\dim\frac{\mathcal E(H)\cap\mathcal P_{\le N}}
{\mathcal E(H)\cap\ker D_H\cap\mathcal P_{\le N}}
\ge N.
}
$$

Every nonconstant quartic thus has active partners in unbounded degrees. The original $qp^3$ identity is an especially sparse explicit presentation of a widespread phenomenon.

For a cubic Hamiltonian, the sole gate $T_3(H,\cdot)$ is a nonzero constant-coefficient third-order differential operator, depending only on the homogeneous cubic part. Its map on homogeneous degree $n$ is surjective onto degree $n-3$: the apolar dual is multiplication by a nonzero cubic, which is injective in a polynomial ring. Hence the exact dimensions are $\min(n+1,3)$; through degree $N\ge2$, the exact space has dimension $3N$. Its characteristic cubic factors into three linear directions over an algebraic closure. Distinct factors give univariate characteristic families; repeated factors give polynomial factors multiplying such families. This is a complete constant-coefficient PDE organization of the all-cubic problem.

## Homogeneous quartics: the exact dimension formula

Let $H\ne0$ be a homogeneous binary quartic. Write $H=aR^g$, where $R$ is not a proper polynomial power, and set $e=\deg R=4/g$. The possibilities are $e=1,2,4$. If $\mathcal E_n(H)$ denotes homogeneous degree $n$, then

$$
\boxed{
\dim\mathcal E_n(H)=2+\mathbf1_{e\mid(n-2)},\qquad n\ge2.
}
$$

The dimensions in degrees zero and one are one and two. The Hilbert series is

$$
\boxed{
\sum_{n\ge0}\dim\mathcal E_n(H)t^n
=1+2t+\frac{2t^2}{1-t}+\frac{t^2}{1-t^e}.
}
$$

The proof identifies the adjoint of the third transvectant with a first transvectant under invariant apolar pairings. Explicitly, for the nondegenerate degree-$n$ pairing $B_n$,

$$
B_{n-2}(T_3(H,G),F)
=-6n(n-1)B_n(G,\{H,F\}).
$$

Rank–nullity gives $\dim\mathcal E_n=2+\dim C_{n-2}(H)$, and the homogeneous centralizer has one dimension exactly when $e$ divides its degree. This is the structural reason for the periodic dimension jumps. The full proof, signs and explicit coefficient recurrence appear in the quartic appendix.

Fourth powers of linear forms have dimension three in every degree at least two. Squares of genuine quadratics have dimension three in even degrees and two in odd degrees. Every quartic that is not a square has dimension three at degrees congruent to two modulo four and dimension two otherwise. Four distinct roots and a triple-plus-simple-root quartic have the same Hilbert function, although their actual partner polynomials differ. Root geometry influences bases beyond what the dimension sequence records.

A canonical exact partner is the Hessian determinant

$$
\Delta_H=H_{qq}H_{pp}-H_{qp}^2,
\qquad \boxed{T_3(H,\Delta_H)=0.}
$$

For every quartic that is not a square of a quadratic,

$$
\boxed{\mathcal E_4(H)=\operatorname{span}\{H,\Delta_H\}.}
$$

The Hessian then has a nonzero Poisson bracket with $H$. Thus invariant theory constructs an active exact partner directly. For $H=q^4+\lambda q^2p^2+p^4$,

$$
\Delta_H=24\lambda(q^4+p^4)+(144-12\lambda^2)q^2p^2,
$$

$$
\{H,\Delta_H\}=288(4-\lambda^2)qp(q^4-p^4).
$$

The activity disappears at $\lambda=\pm2$, precisely the displayed quadratic-square cases. This is a clean algebraic boundary rather than a numerical threshold.

## Arbitrary coefficients: the complete qF(p) classification

Put $\mathcal A=K[p]\oplus qK[p]$ and let $H=qF(p)$, with $M=\deg F\ge2$. Every polynomial has a unique expansion $G=\sum_cq^cA_c(p)$. For odd $k\ge3$, the correction gate on one component is

$$
T_k(qF,q^cA_c)
=(c)_{k-1}q^{c-k+1}
\bigl[kF^{(k-1)}A_c'-(c-k+1)F^{(k)}A_c\bigr].
$$

Different $q$-degrees cannot cancel at a fixed derivative order. The third gate, for $c\ge2$, becomes

$$
3F''A_c'=(c-2)F'''A_c.
$$

This is a first-order differential equation with a polynomial-integrality condition. Together with the fifth gate it produces the following exhaustive answer.

For $M=2$,

$$
\boxed{\mathcal E(qF)=\mathcal A\oplus q^2K[q].}
$$

For $M=3$,

$$
\boxed{
\mathcal E(qF)=\mathcal A\oplus
\operatorname{span}\{q^{3r+2}(F'')^r:r\ge0\}.
}
$$

For $M\ge4$, the answer is $\mathcal A\oplus Kq^2$, with exactly one additional line $Kq^3R(p)$ if and only if $F''=\gamma R^3$ for a nonzero scalar $\gamma$ and polynomial $R$. Thus

$$
\boxed{
\mathcal E(qF)=\mathcal A\oplus Kq^2
\quad\text{or}\quad
\mathcal A\oplus Kq^2\oplus Kq^3R.
}
$$

The cube condition says that the multiplicities of every irreducible factor of $F''$ are divisible by three. It is a structural algebraic locus. For example,

$$
F=5p^8+28p^6+70p^4+140p^2,
\qquad F''=280(p^2+1)^3,
$$

has the extra partner $q^3(p^2+1)$. The Hamiltonian is degree nine and has several terms, so this theorem extends well beyond homogeneous monomial demonstrations.

Why do all higher $q$-degrees disappear once $M\ge4$? If $c\ge4$ and $d=\deg A_c$, the leading coefficients of the third and fifth gates force

$$
3d=(M-2)(c-2),\qquad5d=(M-4)(c-4).
$$

Eliminating $d$ gives $(M+1)(c+1)=15$, impossible for $M,c\ge4$. The $c=2$ equation forces a constant coefficient, and the $c=3$ equation forces the cube root of $F''$. This finite obstruction calculation closes the arbitrary-degree classification.

## The Lie structure and the smaller stable core

The coordinate space $\mathcal A$ is pairwise Moyal-exact and Poisson Lie-closed:

$$
\{qA+B,qC+D\}=q(AC'-A'C)+(AD'-B'C).
$$

It is a semidirect structure built from polynomial vector fields on a line and polynomial functions. In the momentum representation, Weyl quantization gives first-order differential operators, including the half-density correction $B'(p)/2$. This coordinate Lie algebra is classical and belongs to the established Groenewold–Van Hove literature; the Hamiltonian-specific conclusions here identify its role inside the larger partner kernel.

For every $H=qF(p)$ with $\deg F\ge2$,

$$
\boxed{\mathcal D(H)=\mathcal A.}
$$

In a permitted component $q^cA_c$ with $c\ge2$, the exact coefficient space is one dimensional. The Poisson action sends its coefficient to $FA_c'-cF'A_c$. Its leading degree increases by $M-1$, with nonzero leading factor $d-cM$. It therefore leaves that one-dimensional permitted coefficient line. Distinct $q$-degrees cannot repair the failure. Only $\mathcal A$ remains invariant.

Every Lie subalgebra contained in $\mathcal E(H)$ and containing $H$ must be invariant under $D_H$. Consequently $\mathcal A$ is the unique largest such Lie subalgebra. For the favorite $qp^3$, the unique largest ordinary associative subalgebra of $\mathcal E(H)$ is $K[p]$: the leading term of the cube of any polynomial of positive $q$-degree violates the resonance congruence. These are different closure answers to different questions.

## A quadratic perturbation that changes the dynamical answer completely

Take

$$
H_0=qp^3,\qquad H=qp^3+q^2.
$$

The entire first-bracket space is unchanged: $\mathcal E(H)=\mathcal E(H_0)$. Nevertheless,

$$
\boxed{\mathcal D(H_0)=K[p]\oplus qK[p],
\qquad\mathcal D(H)=\operatorname{span}\{1,H\}.}
$$

Here is a finite reduction proof. Let $E_0=\mathcal E(H)$ and $E_{j+1}=E_j\cap D_H^{-1}E_j$. Direct coefficient comparison in the known monomial basis gives

$$
E_1=\{uH+A(p)+q(b_1p+b_0)\}.
$$

The higher resonant monomials cannot survive: the base Hamiltonian sends them to the wrong $p$-degree, while the $q^2$ perturbation sends them into a different $q$-degree congruence class. The $q^2$ coefficient is the single place where a cancellation can occur with the strip component.

Writing $Y=q+p^3/2$, a second comparison yields

$$
E_2=\operatorname{span}\{1,p,p^2,Y,pY,H\}.
$$

The exact Poisson actions are

$$
D_Hp=2Y,\quad D_HY=\tfrac32p^5,\quad
D_Hp^2=4pY,\quad D_H(pY)=2H+2p^6.
$$

The independent outside components $p^5,p^6$ remove $Y,pY$ from any invariant subspace. The first and third equations then remove $p,p^2$. Constants and $H$ remain. Equivalently, the descending dimensions after reaching $E_2$ are six, four and two, with the last space verified invariant. This proves the global answer, rather than inferring it from a degree truncation.

This reduction is an observability calculation. Regard the correction operators as outputs and the Poisson action as a transition operator. Then

$$
\boxed{
\mathcal D(H)=\bigcap_{j\ge0}\ker\bigl(C_H D_H^j\bigr),
\qquad C_H=(T_3(H,\cdot),T_5(H,\cdot),\ldots).
}
$$

The stable exact sector is the unobservable subspace for quantum-correction outputs. In a proved finite-dimensional invariant model, the usual invariant-kernel algorithm can certify it. A naive degree cutoff is insufficient when $D_H$ increases degree; exact invariance must be checked in the full polynomial ring. This gives a concrete route from the atlas's observability machinery to a quantum-classical classification problem.

## Complete monomial organization

For $H=q^ap^b$, each odd correction sends distinct partner monomials to distinct output monomials. Thus $\mathcal E(H)$ is monomial-spanned, and a full polynomial classification reduces to an exponent classification. The coefficient is

$$
S_k(a,b;c,d)=\sum_{j=0}^k(-1)^j\binom kj
(a)_{k-j}(b)_j(c)_j(d)_{k-j}.
$$

A monomial $q^cp^d$ is exact if and only if every $S_k$ for odd $k\ge3$ vanishes. The full classification developed here gives a particularly simple global criterion for nonconstant monomial Hamiltonians:

$$
\boxed{
\mathcal E(q^ap^b)/\bigl(\mathcal E(q^ap^b)\cap\ker D_H\bigr)
\text{ is infinite dimensional}
\iff \min(a,b)\le2.
}
$$

A small transverse degree gives explicit noncommuting univariate families. When $a,b\ge3$ and $a\ne b$, the entire exact-partner space is finite dimensional. Its complete exponent list is computable from finitely many integer-root tests of cubics, followed by all correction gates. The top odd correction reduces candidates to finite-width strips and, in even total degree, one affine line. On each strip or line the third gate is a nonzero cubic. This is a terminating all-degree algorithm, not a rectangular search bound. The appendix gives the proof and delivered implementation.

A concrete unequal-exponent output of the complete algorithm is

$$
\boxed{\mathcal E(q^3p^5)=\mathcal P_{\le2}
\oplus\operatorname{span}\{q^3p^5,qp^{17}\}.}
$$

The degree-eighteen partner has nonzero bracket $46q^3p^{21}$. This finite basis is complete over all partner degrees. More generally, $q^3p^b$ and $qp^{3b+2}$ are exact partners: the third-order resonance cancels and their combined available q differentiation excludes every higher odd correction. It also follows by exchanging the Hamiltonian and observable roles in the exceptional cube-root line of the $qF$ theorem. Exactness is a symmetric relation between two symbols, although the partner space attached to each fixed Hamiltonian can have a very different size.

Balanced powers have a different structure. Put $H=(qp)^m$, and let $\mathcal P_{\le2}$ denote all quadratics and lower degrees. The exact answers are

$$
\mathcal E((qp)^2)=K[q]+K[p]+K[qp],
$$

$$
\boxed{
\mathcal E((qp)^3)=K[qp]+\mathcal P_{\le2}
+\operatorname{span}\{qp^{11},q^{11}p\},
}
$$

$$
\boxed{
\mathcal E((qp)^m)=K[qp]+\mathcal P_{\le2},\qquad m\ge4.
}
$$

Thus a balanced sextic has two exceptional active degree-twelve partners; balanced higher powers have only the four active quadratic directions modulo their commuting diagonal family. The infinite commuting family $K[qp]$ must be distinguished from an infinite active sector.

Ordinary functions of a Hamiltonian require care. For unequal $a,b\ge2$, the third correction on $H^r$, $r\ge2$, has nonzero coefficient

$$
-2ab\,r(a-b)(r-1)\bigl((a+b)(r+1)-3\bigr).
$$

Consequently classical conservation of $H^r$ does not make its uncorrected Weyl symbol commute quantum mechanically. Star powers provide the corrected quantum conserved expressions.

## The original family has a finite quantum ladder

For $H=qp^3$, write $C_r=q^{3r+2}p^r$. Its first bracket is exact, but the second differs by a nonzero term:

$$
(L_\star^H)^2C_r-D_H^2C_r
=(12r+9)(3r+2)(3r+1)\hbar^2q^{3r}p^{r+2}.
$$

There is still a deeper organizing structure. Set $c=3r+2$ and $N=4r+3$. Both the classical and quantum chains terminate at exactly the same finite length:

$$
D_H^NC_r=(-2)^NN!H^c,\qquad D_H^{N+1}C_r=0,
$$

$$
\boxed{
(L_\star^H)^NC_r=(-2)^NN!H^{\star c},
\qquad(L_\star^H)^{N+1}C_r=0.
}
$$

The last surviving classical invariant is an ordinary power; the quantum one is the corresponding star power. For $r=0$, the full formal evolution is an especially transparent polynomial:

$$
\boxed{
e^{tL_\star^H}q^2
=q^2(1-2tp^2)^3
+9\hbar^2t^2p^2(1-2tp^2).
}
$$

The first term is the classical evolution. The second is its exact quantum correction. At first order in time the two agree; the difference begins at second order. All time coefficients terminate after degree three in this example.

The proof uses a faithful localized Weyl representation. With $q=i\hbar\partial_p$, the Hamiltonian becomes $i\hbar(p^3\partial_p+3p^2/2)$. The algebraic coordinate $y=p^{-2}$ and conjugation by $y^{3/4}$ reduce it to $-2i\hbar\partial_y$. The transformed $C_r$ has polynomial coefficients in $y$ of maximum degree $N$; repeated commutators differentiate those coefficients. The argument is algebraic after localization and does not assert a globally defined real coordinate transformation or analytic operator equivalence. Full details and exact finite-chain checks are supplied in the independent appendix.

## Coordinate changes, existing research and the next boundary

Affine symplectic changes preserve the full canonical Moyal structure and transport all the exactness results. General invertible linear changes preserve the vanishing transvectant gates while rescaling the deformation parameter. Ordinary nonlinear canonical substitutions require additional care. For example, the exact pair $P^3,Q^2P$ in canonical variables becomes $(p+q^2)^3,q^2(p+q^2)$ under $Q=q,P=p+q^2$, but its third transvectant is $-72q$. The new normalized bracket has a $+3\hbar^2q$ correction. Classical symplectic covariance alone does not justify using the same flat-coordinate Moyal formula after a nonlinear substitution.

Robert's universal-observable theorem says that, under its symbol-growth assumptions, equality with the Moyal bracket for every Schwartz observable forces a Hamiltonian to be quadratic. Our statements concern explicitly restricted polynomial partner spaces and do not challenge that theorem. Gotay's coordinate Lie algebra supplies the classical closure context. The transvectant language belongs to established invariant theory, including Olver–Sanders. The derived formulas in this note are proved and replayed here without a claim that their literature priority has been established.

The current PerfectJet main source, pinned at commit `494caaf6df145175e11ac65c260b39b6e1aa2765`, already integrates the full seven-coefficient sextic partner classification through partner degree twenty. Its global classification retains archived computer-algebra solver dependencies; exact instance replay and global solver receipts have different evidential roles. Degrees twenty-one and above remain open for that full-space programme. The monomial all-degree results here close specific strata without replacing or overstating that broader classification.

The next substantial frontier is therefore sharply located. For arbitrary quintic and sextic Hamiltonians, classify active polynomial kernels in all degrees and identify exceptional factorization loci. For quartics, build canonical bases and dynamic cores across the full moduli space, beyond the completely determined static dimensions. For larger degrees of freedom, classify stable exact Lie sectors under their own hypotheses. For computation, produce independently checkable certificates for the invariant-kernel reductions and explicit partner bases. Each task now has a precise object, a proof obligation and a usable exact engine.


# Appendix A · Complete quartic proofs

These are direct derivations for the present investigation. They use classical apolarity, transvectants and the binary-quartic Hessian. No priority claim is made. The finite calculations in `verify.py` accompany the all-degree proofs below.

## Exactness space and its grading

Work over a field K of characteristic zero, with one canonical pair (q,p). Write

$$
T_k(F,G)=\sum_{j=0}^{k}(-1)^j\binom{k}{j}
(\partial_q^{k-j}\partial_p^jF)
(\partial_q^j\partial_p^{k-j}G).
$$

Thus T_1 is the Poisson bracket, and the normalized Weyl–Moyal commutator is

$$
\frac{F\star G-G\star F}{i\hbar}
=T_1(F,G)-\frac{\hbar^2}{24}T_3(F,G)
+\frac{\hbar^4}{1920}T_5(F,G)-\cdots.
$$

A partner G is a polynomial independent of hbar. Exactness means equality as a polynomial/formal identity in hbar. For a nonzero homogeneous quartic H, derivatives of H of order five and higher vanish. Consequently its complete exactness space is E(H)=ker T_3(H,·). If V_n denotes the degree-n binary forms, T_3(H,·) maps V_n to V_(n−2). Terms of different homogeneous degrees in G produce different output degrees, so E(H) is the direct sum of its homogeneous pieces E_n(H). Constants and linear forms are automatic partners: dim E_0=1 and dim E_1=2. All quadratics are also automatic, so dim E_2=3.

A first dimension count already proves that every homogeneous quartic has infinitely many exact partners: for n≥2, dim V_n=n+1 and dim V_(n−2)=n−1, hence dim E_n≥2. There is no generic quartic for which sufficiently high-degree polynomial exact partners disappear. The real classification questions are the exact graded dimensions, explicit bases, commuting versus active partners, and closure under multiplication or evolution.

## The apolar adjoint theorem

For F=Σ_(j=0)^n f_j q^(n−j)p^j and G=Σ_(j=0)^n g_j q^(n−j)p^j, define the nondegenerate apolar pairing

$$
B_n(F,G)=\sum_{j=0}^{n}\frac{(-1)^j}{\binom nj} f_jg_{n-j}.
$$

It is symmetric for even n and alternating for odd n. For H∈V_4, G∈V_n and F∈V_(n−2), the exact adjoint identity is

$$
\boxed{
B_{n-2}(T_3(H,G),F)
=-6n(n-1)B_n(G,T_1(H,F)).
}
$$

Here n≥2. For n=2 both sides vanish. For n≥3 it suffices by trilinearity to take H=q^(4−i)p^i, G=q^(n−j)p^j and F=q^(n−2−ell)p^ell. Both sides are zero unless i+j+ell=n+1. In that case the coefficient of the left output is S_3(4−i,i;n−j,j), and the coefficient of T_1(H,F) is 4ell−i(n−2). The identity reduces to

$$
S_3\frac{(-1)^{i+j-3}}{\binom{n-2}{i+j-3}}
=-6n(n-1)\,[4\ell-i(n-2)]\frac{(-1)^j}{\binom nj}.
$$

There are only five types of H. For i=0, S_3=24j(j−1)(j−2); for i=1, S_3=6j(j−1)(4j−3n−2); for i=2, S_3=12j(n−j)(n−2j). Substituting ell=n+1−i−j and simplifying the binomial coefficients proves the displayed identity in each of these three cases. The cases i=3,4 follow by interchanging q and p, which changes the sign of each odd transvectant in the matching way. This proves the adjoint formula for every H,F,G, not only for sampled degrees.

Since the pairings are nondegenerate and −6n(n−1) is nonzero, the rank of T_3(H,·):V_n→V_(n−2) equals the rank of the Poisson map T_1(H,·):V_(n−2)→V_n. Rank–nullity therefore gives

$$
\boxed{\dim E_n(H)=2+\dim C_{n-2}(H)},\qquad
C_k(H)=\{F\in V_k:\{H,F\}=0\}.
$$

This identifies every extra quantum-exact partner dimension with an ordinary classical centralizer dimension two degrees lower.

## Homogeneous centralizers and the three complete rank strata

Factor H over an algebraic closure as H=a∏L_i^(m_i), with distinct linear factors L_i and Σm_i=4. Let g=gcd(m_i), and put e=4/g. Thus H=aR^g, where R is homogeneous of degree e and is not itself a proper polynomial power. The only possibilities are e=1,2,4.

For a homogeneous F of degree k, the condition {H,F}=0 can be analyzed on q≠0. Write H=q^4h(t), F=q^kf(t), t=p/q. Then {H,F}=q^(k+2)[4h f′−k h′f]. If F is nonzero, vanishing says that the derivative of f^4/h^k is zero, hence f^4=c h^k in characteristic zero. The same homogeneous identity is F^4=cH^k. Factorization then forces 4ν_i(F)=km_i at every root. Such nonnegative integral multiplicities exist exactly when e divides k, and in that case F is a scalar multiple of R^(k/e). Hence

$$
\dim C_k(H)=\begin{cases}1,&e\mid k,\\0,&e\nmid k.\end{cases}
$$

This statement descends to the original characteristic-zero field by preservation of matrix rank under field extension. It is also directly available from unique factorization when H=aR^g is chosen over K.

Combining with the adjoint theorem yields the complete all-degree classification

$$
\boxed{\dim E_n(H)=2+\mathbf 1_{e\mid(n-2)}\quad(n\ge2).}
$$

The Hilbert series is therefore

$$
\boxed{
\sum_{n\ge0}\dim E_n(H)t^n
=1+2t+\frac{2t^2}{1-t}+\frac{t^2}{1-t^e}.
}
$$

For a fourth power of a linear form, e=1, every n≥2 has dimension three. For a square of a nondegenerate quadratic, e=2, even n≥2 have dimension three and odd n have dimension two. Every quartic that is not a square of a quadratic has e=4: the dimension is three precisely at n≡2 mod4, and is two otherwise. In particular, the root-multiplicity types (3,1), (2,1,1) and (1,1,1,1) have exactly the same graded dimensions. Their actual basis vectors differ, but their Hilbert function does not. The zero Hamiltonian is excluded; for H=0 every polynomial is an exact partner.

## Explicit monomial normal forms

For H=q^4, T_3(H,G)=24q∂_p^3G. Thus

$$
E(q^4)=K[q]\oplus pK[q]\oplus p^2K[q].
$$

For H=q^3p, a monomial q^cp^d belongs to E(H) precisely when d=0, d=1, or d=3c+2. The operator maps distinct monomials to distinct output monomials, so no cancellation between distinct input monomials is possible. Consequently this monomial condition classifies every polynomial partner, by taking its linear span. In fixed degree n, the exceptional monomial occurs precisely when n=4c+2, producing the e=4 dimension jump.

For H=q^2p^2, the third transvectant on q^cp^d has coefficient 12cd(c−d), with output q^(c−1)p^(d−1). Hence the entire space has basis all pure powers q^n and p^n, together with the diagonal monomials (qp)^r. Constants are counted only once. This produces the e=2 dimension pattern.

Invertible linear coordinate changes preserve the zero conditions T_k=0: under A∈GL_2, T_k(F∘A,G∘A)=(det A)^kT_k(F,G)∘A. Symplectic changes (det A=1) preserve the full fixed-parameter canonical Moyal structure. General GL_2 changes preserve exactness while rescaling the deformation parameter in the full star-product covariance statement.

## A canonical noncommuting partner: the quartic Hessian

Define

$$
\Delta_H=H_{qq}H_{pp}-H_{qp}^2.
$$

For every homogeneous binary quartic,

$$
\boxed{T_3(H,\Delta_H)=0.}
$$

This can be proved by direct coefficient expansion. If H=aq^4+4bq^3p+6cq^2p^2+4dqp^3+ep^4, then

$$
\Delta_H=144[(ac-b^2)q^4+2(ad-bc)q^3p
+(ae+2bd-3c^2)q^2p^2+2(be-cd)qp^3+(ce-d^2)p^4].
$$

Substitution into the four-term derivative formula for T_3 cancels every coefficient. The supplied verifier also gives a complete exact interpolation certificate: each output coefficient is a polynomial of degree at most three in each of the five coefficients of H, and it vanishes at all 4^5 grid points with coefficient values 0,1,2,3. Iterated univariate interpolation therefore proves the universal identity over characteristic zero.

When H is not a square of a quadratic, H and Δ_H are linearly independent. To see the converse characterization precisely, examine a root L of multiplicity m<4. The Hessian has multiplicity exactly 2m−2 there: the leading coefficient is −3m(4−m) times a nonzero square. Thus Δ_H=cH with c≠0 forces every root to have m=2. If Δ_H=0, the same calculation forces H to have one quadruple root. Conversely, for H=Q^2, direct differentiation gives Δ_H=12(det D^2Q)H. Hence Δ_H is proportional to H exactly for quadratic-square quartics, including fourth powers.

For a primitive quartic, the homogeneous Poisson centralizer in degree four is the line KH. Thus Δ_H is noncommuting, and because dim E_4=2, one gets the exact basis

$$
\boxed{E_4(H)=\operatorname{span}\{H,\Delta_H\}}
$$

for every quartic H that is not a square of a quadratic. This is a canonical, coordinate-covariant construction of an active exact partner, not merely an existence count. The sextic Jacobian J_H={H,Δ_H} measures its noncommutation.

## The square-of-H trap and the exact commuting intersection

A polynomial function of H Poisson-commutes with H, but its ordinary product need not star-commute with H. For every homogeneous quartic H and integer r≥2,

$$
\boxed{
T_3(H,H^r)
=-\frac{r(r-1)(4r+1)}3 H^{r-2}\{H,\Delta_H\}.
}
$$

For proof, differentiation of H^r separates the third derivative into one-third-derivative, second/first-derivative, and three-first-derivative terms. The first contribution contracts to T_3(H,H)=0. The second contributes −3r(r−1)H^(r−2){H,Δ_H}. Euler homogeneity gives the third contribution through

$$
D^3H[(H_p,-H_q)^3]
=-\frac43H\{H,\Delta_H\}.
$$

Combining them gives the formula. More generally, for homogeneous degree m≥2, the same proof replaces (4r+1)/3 by (mr+m−3)/(m−1). The Euler identity can be checked at a point (1,0) in linear coordinates: write the first four affine coefficients of H, use H_q=mH, H_qq=m(m−1)H, and the analogous mixed-derivative identities, and the two cubic-gradient expressions agree term by term. Covariance and polynomial continuation then give the identity everywhere.

If H is primitive, its centralizer is K[H], and J_H≠0. Every H^r with r≥2 therefore fails exactness. Different powers produce different homogeneous output degrees and cannot cancel. The full commuting exact subspace is exactly span{1,H}. If H=Q^2 with Q nondegenerate quadratic, the centralizer is K[Q] and all its elements are exact; after a linear extension of scalars Q reduces to a scalar multiple of qp, where this is the diagonal-monomial computation above. For a fourth power H=L^4, the centralizer K[L] is likewise entirely exact. These facts separate large active families from merely commuting ones.

## Constructing every homogeneous partner by a finite recurrence

Let H=Σ_(i=0)^4 a_iq^(4−i)p^i and G=Σ_(j=0)^n b_jq^(n−j)p^j. Put b_j=0 outside 0≤j≤n. Then the complete necessary and sufficient equations are

$$
\sum_{i=0}^4 a_i b_{s+3-i}
S_3(4-i,i;n-s-3+i,s+3-i)=0,
\quad0\le s\le n-2.
$$

This is an explicit banded (n−1)×(n+1) rational/integer matrix. Its nullspace is exactly E_n(H); no higher-order constraint is hidden. A linear coordinate choice can ensure a_0≠0 for any nonzero H. Then the equations successively determine b_3,…,b_n from the three seeds b_0,b_1,b_2, followed by one terminal compatibility equation. The dimension theorem proves exactly when that final equation vanishes identically rather than imposing one condition.

For the important family H_λ=q^4+λq^2p^2+p^4, the recurrence simplifies to

$$
2(s+3)(s+2)(s+1)b_{s+3}
+\lambda(n-s-1)(s+1)(n-2s-2)b_{s+1}
-2(n-s+1)(n-s)(n-s-1)b_{s-1}=0.
$$

The Hessian and its Jacobian are

$$
\Delta_{H_\lambda}=24\lambda(q^4+p^4)+(144-12\lambda^2)q^2p^2,
\qquad
\{H_\lambda,\Delta_{H_\lambda}\}
=288(4-\lambda^2)qp(q^4-p^4).
$$

The square stratum is λ=±2. Two explicit cubic partners for every λ are q^2p−(λ/6)p^3 and qp^2−(λ/6)q^3. For λ^2≠4, the quartic partners are exactly span{H_λ,q^2p^2}. These formulas and the recurrence provide tractable all-degree constructions while the apolar theorem certifies the dimension at every step.

## Exact once does not mean exact under repeated evolution

The exactness space is generally neither an ordinary product algebra nor invariant under the Hamiltonian action. For H=q^4+p^4 and G=q^2p^2, the first normalized Moyal commutator equals the Poisson bracket K=8(q^5p−qp^5). But

$$
T_3(H,K)=-23040q^2p^2,
\quad
\frac{[H,K]_\star}{i\hbar}
=\{H,K\}+960\hbar^2q^2p^2.
$$

Thus G is exact for one Hamiltonian action, but the next action has a nonzero correction. Also H itself is exact while H^2 is not. Any claim about exact classical-versus-quantum trajectories needs a subspace invariant under the Hamiltonian derivation, not merely membership in E(H). This is a separate classification problem.

## Result and remaining scope

The complete graded dimensions of all polynomial Moyal-exact partners of every nonzero homogeneous quartic are now determined, and an explicit finite matrix/recurrence computes every basis at every degree. The organizing structures are apolar adjointness, the primitive polynomial root of H, and the Hessian/Jacobian covariants. Explicit bases for arbitrary coefficients at every degree need not have a simple single closed expression, but the recurrence is exhaustive and the all-degree dimension formula proves its rank. Higher-degree Hamiltonians require simultaneous higher odd-transvectant constraints, and nonlinear canonical coordinate changes do not automatically preserve this flat constant-coefficient Moyal product. Classification of invariant exact-dynamics spaces remains distinct from the static exact-partner problem solved here.


# Appendix B · Arbitrary F, cubic PDEs and dynamical cores

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


# Appendix C · Complete cubic characteristic families

This supplement is an all-degree theorem, not an extrapolation of the checks. Work over an algebraically closed characteristic-zero field; rational/real kernels are recovered by taking the corresponding field-valued part. Let H be any polynomial of degree exactly three, and let H3 be its top homogeneous part. Every lower-degree term has zero third derivatives, and no correction beyond order three is possible. Therefore E(H)=ker[H3(partial_p,−partial_q)].

Factor `H3=gamma product_i ell_i^(m_i)`, with pairwise nonproportional linear forms ell_i, positive multiplicities m_i and sum m_i=3. Let `D_i={ell_i,.}` and choose a linear form t_i with `D_i t_i=1`. Then the complete ordinary polynomial partner space is

`E(H)=sum_i sum_(j=0)^(m_i−1) t_i^j k[ell_i]`.

The sums are vector-space sums, generally not direct. In particular every degree-three Hamiltonian has an infinite-dimensional exact partner space, organized by the three root multiplicity patterns of its top binary cubic.

If all three roots are distinct, the solution is the sum of three univariate polynomial families k[ell_i]. For a double root and a simple root, it is `(k[ell_1]+t_1 k[ell_1])+k[ell_2]`. For a triple root, it is `k[ell]+t k[ell]+t²k[ell]`. These descriptions hold even if arbitrary linear, quadratic and constant terms are added to H. A term such as H² is not thereby asserted to be a partner: the displayed space must be used.

Proof of inclusion: the correction differential operator is exactly `Lambda³(H,G)=6 H3(partial_p,−partial_q)G=6gamma product_i D_i^(m_i)G`. All D_i commute because their coefficients are constant. Every summand `t_i^j F(ell_i)` is killed by D_i^(m_i) when j<m_i, hence is killed by the full product.

For completeness, the operator on homogeneous degree n polynomials maps V_n to V_(n−3). Under a nondegenerate apolar pairing its transpose is, up to a nonzero scalar, multiplication by H3. Multiplication is injective because the polynomial ring is a domain. Consequently the correction map is surjective for n>=3 and its kernel has dimension `(n+1)−(n−2)=3`. For n=2 its kernel is all V2, also dimension three; V0 and V1 have dimensions one and two.

The proposed families span exactly that many dimensions in each degree. Choose a projective chart in which `ell_i=q+lambda_i p`, with distinct lambda_i, and use `t_i=p`; this can always be achieved after an invertible linear coordinate change. For n>=2 the three displayed degree-n candidates `p^j(q+lambda_i p)^(n−j)`, with j<m_i, are scalar multiples of the lambda-derivatives of `(q+lambda p)^n`. Their first three coefficient rows form, after nonzero row/column scalings, the confluent Vandermonde matrix for the distinct nodes lambda_i with multiplicities m_i. Its determinant is nonzero, so their span has dimension three. In degrees zero and one the same families span V0 and V1. Inclusion plus the exact dimension proves the complete formula. An invertible linear change only changes the Poisson tensor by a nonzero determinant scalar, which does not affect vanishing of this correction kernel; an affine symplectic change preserves the full stated Weyl convention directly.

Equivalently, `dim E(H)_0=1`, `dim E(H)_1=2`, and `dim E(H)_n=3` for every n>=2. The Hilbert series is `1+2t+3t²/(1−t)`. This gives a universal large-family theorem for cubic Hamiltonians and an explicit root-multiplicity organization of all partners. It does not assert product closure, Lie closure or all-time quantum/classical agreement.


# Appendix D · All-degree monomial classification

Work over a characteristic-zero field k and use the canonical Weyl–Moyal product. A partner is always an ordinary, hbar-independent polynomial. Set E(H)={G in k[q,p]:[H,G]_star/(i hbar)={H,G}}. This is a linear space; neither ordinary multiplication nor arbitrary Poisson brackets are assumed to preserve it. Write P_2 for the polynomials of total degree at most two.

## The exponent-basis reduction

For H=q^a p^b and G=q^c p^d, define

S_k(a,b;c,d)=sum_(j=0)^k (-1)^j binom(k,j)(a)_(k-j)(b)_j(c)_j(d)_(k-j),

where (n)_r is a falling factorial, zero for r>n. The normalized Moyal bracket is the finite sum over odd k of (-1)^((k-1)/2) hbar^(k-1) S_k q^(a+c-k)p^(b+d-k)/(2^(k-1)k!). Thus G is exact if and only if every S_k for odd k>=3 vanishes. For a fixed H and a fixed correction order, distinct partner exponent pairs have distinct output exponents. Consequently no cancellation between different monomials of G is possible at that order. E(H) is exactly the linear span of the admissible exponent pairs. Distinct correction orders also have distinct hbar powers; cancellation between them is not allowed by the definition.

The Poisson coefficient is ad-bc. The distinction between exact partners and commuting partners is therefore completely visible on this basis.

## Complete effective classification for unequal exponents a,b>=2

Let D=a+b. The following algorithm is complete over all nonnegative partner exponents; it has no partner-degree cutoff. A coordinate-axis algebra is retained symbolically when a=2 or b=2. The supplied classification.py implements this algorithm using integer polynomial arithmetic and the integer-root theorem.

If D is odd, only j=b can survive in S_D, hence

S_D=(-1)^b D! (c)_b(d)_a.

Every partner therefore has c<b or d<a. If c is fixed, S_3 is a cubic in d with leading coefficient (a)_3; if a=2, its degree is two with leading coefficient -6bc, nonzero unless c=0. In that exceptional case every p^d is exact and the whole algebra k[p] is recorded symbolically. The swapped assertion applies when d is fixed and b=2. All remaining strip candidates are the nonnegative integer roots of finitely many nonzero cubic or quadratic polynomials.

If D is even, precisely j=b-1,b can survive in S_(D-1), giving

S_(D-1)=(-1)^(b-1)(D-1)!(c)_(b-1)(d)_(a-1)[b(d-a+1)-a(c-b+1)].

Thus every partner has c<b-1, d<a-1, or lies on b(d+1)=a(c+1). The strips are handled as above. On the affine line, put g=gcd(a,b), A=a/g and B=b/g. Its nonnegative integer points are exactly c=Bn-1, d=An-1 with n>=1, because A and B are coprime and unequal. S_3 on that line is a nonzero polynomial of degree at most three. One direct proof of nonvanishing is to evaluate its polynomial continuation at n=0, so c=d=-1: the result is

-6(a-b)[a^2+b^2-3(a+b)+2].

This is nonzero for unequal a,b>=2 of the same parity. Indeed the bracket is positive for the smallest such pairs (2,4) and (3,5), and increases thereafter in either exponent. Evaluating the polynomial at n=0 is only an identity test; n=0 is not an admissible partner. Therefore only finitely many additional line candidates occur. Finally, every candidate is checked against every odd correction order. The strip/line argument proves completeness, while the final checks prove sufficiency.

A nonnegative integer root of a nonzero integer polynomial is either zero or a positive divisor of its first nonzero coefficient after removing powers of the variable. This gives a terminating exact root routine. The table complete_table_2_to_12.json applies the complete procedure to every unequal pair 2<=a<b<=12. It does not truncate the partner degree.

Examples are E(q^2p^3)=k[p]+span{q,qp,q^2,q^2p^3,q^8p}, and E(q^2p^8)=k[p]+span{q,qp,q^2,q^2p^8,q^3p}. The complete algorithm gives E(q^3p^4)=P_2+span{q^3p^4,qp^14} and E(q^4p^5)=P_2+span{q^4p^5}. These are complete fixed-H classifications, justified by the finite candidate theorem. Patterns observed across a finite Hamiltonian table are not asserted as universal closed formulae.

## Closed classification for balanced monomials

For H=(qp)^m the complete answer is

E((qp)^2)=k[q]+k[p]+k[qp],

E((qp)^3)=k[qp]+P_2+span{qp^11,q^11p},

E((qp)^m)=k[qp]+P_2 for every integer m>=4.

For m<=1 the Hamiltonian has degree at most two and every polynomial is exact. The sums displayed above are vector-space sums, not assertions of directness or multiplication closure.

To prove this, put n=c+d, t=cd, and define Q_3=(m-2)(n-1)(n-2)-2(2m-1)t. Direct expansion gives S_3=m(m-1)(d-c)Q_3. The diagonal c=d makes every odd S_k vanish by pairing j with k-j. For m=2, Q_3=-6cd, so the off-diagonal solutions are precisely the two coordinate axes, proving the quartic formula.

For m=3, the only further correction is S_5=360(c)_2(d)_2(d-c). Off the diagonal, one exponent must be at most one. At c=0, S_3=6(d)_3, giving d=0,1,2. At c=1, S_3=6d(d-1)(d-11), giving d=0,1,11. Swapping c,d completes the sextic classification. In particular the degree-twelve exceptional partners are genuine; checking only low partner degrees would miss them.

For m>=4, write S_5=m(m-1)(m-2)(d-c)P_5, where

P_5=(m-3)(m-4)(n-1)(n-2)(n-3)(n-4)
-4(2m-3)[(m-3)n^2-5(m-4)n+5(2m-7)]t
+4(2m-1)(2m-3)t^2.

The following exact polynomial identity is a short elimination certificate:

(2m-1)P_5+3(n-1)(n-2)(2m+n-7)(2m^2+mn-6m-4n+12)=Q_3 R,

R=(2m-3)[mn^2-7mn-4mt+18m-4n^2+34n+2t-66].

If c!=d and S_3=0, then Q_3=0. For n>2 and m>=4, every factor of the second term is strictly positive: the last factor equals 2(m^2-3m+6)+(m-4)n. Therefore P_5 cannot vanish. This excludes every off-diagonal partner of total degree above two. Quadratic partners and diagonal partners are already known to be sufficient, completing the proof for all m. The verifier checks the displayed elimination identity by exact multivariate polynomial coefficient comparison, not numerical substitution.

## Finiteness and the criterion for large noncommuting families

For unequal a,b>=3, all candidate strip and line polynomials above are nonzero, and there is no symbolic coordinate axis. Hence E(q^a p^b) is finite-dimensional. Balanced a=b>=3 has an infinite-dimensional E(H), but its unbounded family k[qp] commutes classically and under the star commutator. Its space of noncommuting directions has dimension six for m=3 and four for m>=4, measured as E(H)/(E(H) intersect ker{H,-}).

Consequently a nonlinear monomial Hamiltonian q^a p^b of degree at least three has an infinite-dimensional space of noncommuting exact partner directions if and only if min(a,b)<=2. If a=1 or 2, use G=p^r, r>=1: these are exact because H has q-degree at most two, and their distinct nonzero Poisson images are ar q^(a-1)p^(b+r-1). If a=0, use G=qp^r; exactness follows from q-degree one of G, and the nonzero images -b p^(b+r-1) are distinct. Swap coordinates for b<=2. The preceding finite/balanced classification proves necessity for min(a,b)>=3. This criterion concerns monomial Hamiltonians and fixed canonical coordinates; it is not a classification of every nonlinear polynomial Hamiltonian.

## Ordinary powers are not automatic partners

For c=ar,d=br, exact expansion yields

S_3(a,b;ar,br)=-2ab r(a-b)(r-1)[(a+b)(r+1)-3].

For unequal a,b>=2 and integer r>=2 this is nonzero. Although {H,H^r}=0, the ordinary symbol H^r fails to commute in the Moyal sense. Star powers are hbar-dependent objects and do not supply the hbar-independent partners asked for here. More generally, when unequal a,b>=3, any exact classically commuting monomial is constant or H itself: the classical condition ad-bc=0 permits rational r, and the displayed factor leaves only r=0 or 1 for nonnegative exponents. Thus E(H) intersect ker{H,-}=span{1,H}. This is one concrete reason the exact-partner space should not be assumed to be an ordinary polynomial algebra.

## Scope

The balanced classifications and the infinite-noncommuting-family criterion are proved universal statements. The strip/affine-line procedure is a complete effective algorithm for each unequal a,b>=2. The supplied 55-Hamiltonian table is a finite application of that complete algorithm, while its independent bounded grid comparison is a regression check of the implementation. None of these claims establishes a universal closed formula for all unequal exponent pairs, a classification under nonlinear canonical transformations, or a new mathematical priority claim.


# Appendix E · Closure and finite quantum ladders

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


# Appendix F · Existing work and evidential boundaries

This is a read-only recovery of the relevant PerfectJet source and primary literature on 21 October 2026. The repository snapshot is pinned to `494caaf6df145175e11ac65c260b39b6e1aa2765`, tree `d723a6e0d5c985c144ced79e8e4365544ad91e53`. Seven relevant source files are preserved with Git blob hashes and SHA-256 values in `source_snapshot.json`. Pull request 2 is now closed and merged; the older memory that it remained conflicting is stale.

## What the existing repository already has

The authoritative current exposition is `docs/PARTNER_INCIDENCE.md`, integrated via release 0.17.0, and the explicit trust boundary is `docs/SEXTIC_INTEGRATION.md`. For a homogeneous binary sextic f and a homogeneous degree-N form g, its correction-free condition is exactly `(f,g)_3=(f,g)_5=0`. The first transvectant `(f,g)_1` is tested separately to decide whether the pair is active, meaning that its common Poisson/Moyal bracket is nonzero. A zero correction kernel vector is not the same as an active family.

The source constructs the complete rational instance matrix L_N(f) by stacking the third and fifth transvectant matrices. This is linear algebra in g. Its Math Lab interface can compute the full kernel and test each rational basis vector. This exact-instance machinery is stronger than scanning only monomial pairs, because cancellations between the coefficients of a general g are permitted.

The global classification treats the full seven-coefficient sextic space, using the dense root-placement slice `xy(x−y)(x³+px²y+qxy²+ry³)` and a separate classification of degenerate root patterns. The two root-separation factors are removed with a Rabinowitsch variable. Projection determinants define a superset of a rank-drop locus; emptiness of that superset excludes the true locus. Invariant-relation tests and classical orbit separation then identify exceptional classes. Line probes recover exact restrictions of possible hypersurfaces but do not independently certify genericity or exclude components they do not meet.

The archived classification through partner degree 20 is already substantial:

| Partner degree N | Existing stated exceptional locus |
|---|---|
| 3 | B=6A²; kernel dimension at least two exactly for the dihedral class x⁶+y⁶ or a root of multiplicity at least five |
| 4 | Beyond the universal quartic covariant (f,f)₄, the octahedral class xy(x⁴−y⁴) or a root of multiplicity at least five |
| 5 | A root of multiplicity at least four, or x⁶+(40/7)x³y³+y⁶ up to GL₂ over the algebraic closure |
| 6 | Beyond f itself, a root of multiplicity at least four |
| 7,9,11,13,15,17,19 | A root of multiplicity at least four |
| 8 | A root of multiplicity at least four, or the order-three family x⁶+λx³y³+y⁶ and its x³y³ boundary |
| 10 | A root of multiplicity at least four, x³y³, or the class x⁶+y⁶ |
| 12 | A²=25B/96 |
| 14 | A root of multiplicity at least four, x³y³, or the octahedral class |
| 16,18,20 | A root of multiplicity at least four, or x³y³ |

These global results carry a carefully stated external-computation boundary. Characteristic-zero slice verdicts rely on archived msolve results. Singular computations at two primes and a dependency-free modular engine provide supporting checks. A finite-prime emptiness result alone does not prove characteristic-zero emptiness. The present recovery reads the archived receipts; it does not rerun msolve or turn those receipts into independent rational certificates. Degrees 21 and above, proof-carrying rational replay of the solver verdicts, and formal attachment remain open in the current documentation.

Several exact constructions are already present and must not be claimed as new in this follow-up. Every sextic has the quartic correction-free partner `(f,f)₄` and its self-partner f. The family `f_λ=x⁶+λx³y³+y⁶` has the degree-eight partner `xy(x⁶+y⁶−(7λ/20)x³y³)` for every λ. The quintic candidate `xy(x³−y³)` has third gate `72(7λ−40)(x⁴y+xy⁴)` and fifth gate zero, hence the exceptional λ=40/7. These identities are implemented in `src/perfectjet/transvectants.py` and can be checked exactly.

## What the external literature establishes

Didier Robert's *When Poisson and Moyal Brackets are equal?*, arXiv:2207.08798v2 (2 March 2023), gives a strong universal boundary. Theorem 1.1 assumes fixed nonzero Planck parameter (scaled to one), H in a moderate-growth symbol class S^μ_δ with δ<1/2, and equality of the Poisson and Moyal brackets for every Schwartz observable A. It concludes that H has degree at most two. Theorem 4.1 similarly characterizes Hamiltonians for which a universal finite Moyal truncation is exact: retaining terms through order 2m+1 forces degree H≤2m+2. The theorem concerns a universal observable quantifier, so a nonlinear H can still possess a restricted infinite family of exact partners. The author's Poisson sign convention is opposite to the q-first convention used in the atlas; the equality and degree statements are unchanged after consistent sign conversion.

Mark J. Gotay's *On the Groenewold–Van Hove problem for R²ⁿ*, Journal of Mathematical Physics 40 (1999), 2107–2116, arXiv:math-ph/9809015, classifies maximal polynomial Lie subalgebras containing the Heisenberg algebra when n=1. Theorem 8 and Corollary 9 identify, up to isomorphism, the degree-at-most-two algebra and the coordinate algebra C={f(q)p+g(q)}. The latter has arbitrarily high polynomial degrees while remaining affine in one canonical variable. This is a classical structural source of infinite exact sectors. The paper explicitly says that the classification does not extend unchanged to higher dimensions. Its operator-quantization hypotheses and maximal-subalgebra question are stronger and different from finding E(H) for one fixed H.

Peter J. Olver and Jan A. Sanders, *Transvectants, Modular Forms, and the Heisenberg Algebra*, Advances in Applied Mathematics 25 (2000), 252–283, DOI 10.1006/aama.2000.0700, is a primary source for the established relationship among transvectants, classical invariant theory, Heisenberg representations, star products and Moyal brackets. The publisher and author bibliography confirm this relationship. The author PDF is accessible, but its extracted text has broken encoding, so no specific theorem in it is invoked here without visual or independent verification.

## Productive genuinely separate directions for this session

The short monomial identity in the chat motivates an all-degree classification for particular H, not another bounded monomial census. An exact closed description of E(qp^m), its exceptional exponent rays and their disappearance under higher gates would complement the full sextic incidence classification. General qF(p), affine symplectic transport, nonhomogeneous perturbations and several canonical pairs are further structural directions. Statements that require an entire family to be invariant under Hamiltonian evolution are stronger still: a one-step equality `[H,G]_star/(iℏ)={H,G}` need not persist after replacing G with `{H,G}`. For H=qp³, the resonance partner q^(3r+2)p^r is sent to a multiple of q^(3r+2)p^(r+2), which generally leaves the resonance line. Thus exact partner, invariant sector, pairwise exact Lie algebra, and associative star subalgebra must be distinguished.

Affine symplectic covariance of the flat Moyal product is already implemented in `src/perfectjet/moyal.py`. Ordinary pullback by a nonlinear symplectomorphism generally preserves the Poisson bracket but fails to preserve the same flat star product; the source includes an exact nonlinear-shear covariance defect. Consequently a nonlinear canonical change of coordinates cannot automatically transport an exact sector without transporting or correcting the star product as well.

No originality claim is justified by this recovery. A new proof in this session may be mathematically useful and independently checkable while still belonging to an established theory. The research should identify its exact relation to these existing results and keep finite computations, all-degree proofs, external-solver conclusions and open classifications separate.


# Primary references

**Didier Robert (2023). When Poisson and Moyal Brackets are equal?.** Universal-observable boundary; does not exclude restricted infinite exact-partner sectors. [Primary source](https://arxiv.org/pdf/2207.08798).

**Mark J. Gotay (1999). On the Groenewold–Van Hove problem for R2n.** Classical origin of affine-in-one-variable exact Lie sectors and scope distinction from fixed-H partner kernels. [Primary source](https://www.pims.math.ca/~gotay/r2n.pdf).

**Peter J. Olver; Jan A. Sanders (2000). Transvectants, Modular Forms, and the Heisenberg Algebra.** Established transvectant/invariant-theory/Heisenberg/Moyal relationship; PDF text extraction corrupt, so no unverified specific theorem borrowed. [Primary source](https://www.sciencedirect.com/science/article/pii/S0196885800907000).

**PerfectJet repository contributors (2026). Partner incidence over the full sextic space.** Current full-space sextic classification through partner degree20, archived external solver dependencies, activity distinction, degree>=21 boundary. [Primary source](https://github.com/towre676-cloud/PerfectJet/blob/494caaf6df145175e11ac65c260b39b6e1aa2765/docs/PARTNER_INCIDENCE.md).

**PerfectJet repository contributors (2026). Sextic research integration, v0.17.0.** Explicit trust boundary: exact instance replay versus archived msolve/Singular receipts and remaining formal/independent obligations. [Primary source](https://github.com/towre676-cloud/PerfectJet/blob/494caaf6df145175e11ac65c260b39b6e1aa2765/docs/SEXTIC_INTEGRATION.md).

**R. James Shank (2002). Classical Covariants and Modular Invariants.** Example5.2 lists classical quartic covariant generators f,H,i,t,j. Does not directly certify the session apolar-adjoint formula. [Primary source](https://www.kent.ac.uk/smsas/personal/rjs/ccmi.pdf).