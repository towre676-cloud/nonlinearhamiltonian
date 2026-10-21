# Nonlinear Hamiltonians with exact classical–quantum partners

## A classification by size, closure and dynamics

**Research note · 21 October 2026.** One canonical pair, polynomial observables, exact rational computation and proofs valid in all degrees where stated. This note develops the question raised by the identity for \(H=qp^3\). It separates newly derived results in this investigation from classical structures and the existing PerfectJet sextic programme. Mathematical priority is not claimed. The accompanying executable checks support their named finite identities and models; the all-degree conclusions rest on the displayed proofs.

## What the question becomes

Fix the canonical Poisson bracket \(\{F,G\}=F_qG_p-F_pG_q\) and the Weyl–Moyal product with bidifferential exponential \(\exp[(i\hbar/2)(\overleftarrow\partial_q\overrightarrow\partial_p-\overleftarrow\partial_p\overrightarrow\partial_q)]\). Work over a characteristic-zero field; rational examples and all delivered calculations use exact fractions. Write

\[
T_k(F,G)=\sum_{j=0}^k(-1)^j\binom kj
F_{q^{k-j}p^j}G_{q^jp^{k-j}}.
\]

The normalized bracket has the finite polynomial expansion

\[
L_\star^H G:=\frac{H\star G-G\star H}{i\hbar}
=\{H,G\}-\frac{\hbar^2}{24}T_3(H,G)
+\frac{\hbar^4}{1920}T_5(H,G)-\cdots.
\]

A partner \(G\) is independent of \(\hbar\). Exactness means a polynomial identity in \(\hbar\), equivalently the vanishing of every higher odd transvectant. This is stronger than equality after inserting one chosen numerical value of \(\hbar\). Define

\[
\mathcal E(H)=\bigcap_{j\ge1}\ker T_{2j+1}(H,\cdot),
\qquad D_H=\{H,\cdot\}.
\]

The space \(\mathcal E(H)\) is linear. It need not be an associative algebra, a Poisson Lie algebra, or invariant under \(D_H\). To discuss active partners, quotient out \(\mathcal E(H)\cap\ker D_H\). “Infinitely many active partners” below means that this quotient is infinite dimensional, rather than the trivial observation that scalar multiples give infinitely many elements.

The space that supports exact repeated classical–quantum actions is

\[
\mathcal D(H)=\{G:D_H^jG\in\mathcal E(H)\ \text{for every }j\ge0\}.
\]

It is the largest \(D_H\)-invariant linear subspace of \(\mathcal E(H)\). On it, every formal Taylor coefficient of the classical and quantum evolutions agrees. This statement concerns algebraic formal time evolution; global analytic flow, operator domains and completeness require further assumptions.

The resulting classification has several strong answers. Every cubic and every quartic Hamiltonian has an infinite-dimensional active exact-partner quotient. Homogeneous quartics admit a complete all-degree dimension formula governed by a classical apolar duality. The family \(qF(p)\) admits a complete polynomial-partner classification for arbitrary coefficients and arbitrary degree. Monomial Hamiltonians admit a complete criterion for infinite active families and an effective finite algorithm in the remaining unequal-exponent cases. Closure and repeated evolution select smaller structures, including a known coordinate Lie algebra and explicit finite quantum ladders.

## A universal reason cubic and quartic families are large

Let \(\mathcal P_{\le N}\) be the polynomials of total degree at most \(N\), of dimension \((N+1)(N+2)/2\). If \(\deg H\le4\), only \(T_3\) can obstruct exactness, and

\[
T_3(H,\cdot):\mathcal P_{\le N}\longrightarrow\mathcal P_{\le N-2}.
\]

Consequently, for \(N\ge2\),

\[
\boxed{\dim(\mathcal E(H)\cap\mathcal P_{\le N})\ge2N+1.}
\]

This argument includes inhomogeneous quartics. It does not need a genericity assumption or a special factorization. Adding any polynomial \(Q\) of degree at most two preserves the entire exactness space, because every derivative of \(Q\) of order at least three vanishes:

\[
\boxed{\mathcal E(H+Q)=\mathcal E(H).}
\]

To ensure that large spaces are not explained entirely by commuting observables, an elementary centralizer estimate suffices. For nonconstant \(H\), choose affine symplectic coordinates and a line \(q=0\) with \(H_p(0,p)\ne0\). Restriction to that line is injective on the polynomial Poisson centralizer. Indeed, if a commuting polynomial vanishes there, write \(G=q^kJ\) with \(k\ge1\) and \(J(0,p)\ne0\). The leading \(q\)-adic coefficient of \(\{H,G\}\) is \(-kH_p(0,p)J(0,p)\), a nonzero polynomial. This contradicts commutation. Restricted polynomials have degree at most \(N\), so the centralizer through degree \(N\) has dimension at most \(N+1\). Therefore

\[
\boxed{
\dim\frac{\mathcal E(H)\cap\mathcal P_{\le N}}
{\mathcal E(H)\cap\ker D_H\cap\mathcal P_{\le N}}
\ge N.
}
\]

Every nonconstant quartic thus has active partners in unbounded degrees. The original \(qp^3\) identity is an especially sparse explicit presentation of a widespread phenomenon.

For a cubic Hamiltonian, the sole gate \(T_3(H,\cdot)\) is a nonzero constant-coefficient third-order differential operator, depending only on the homogeneous cubic part. Its map on homogeneous degree \(n\) is surjective onto degree \(n-3\): the apolar dual is multiplication by a nonzero cubic, which is injective in a polynomial ring. Hence the exact dimensions are \(\min(n+1,3)\); through degree \(N\ge2\), the exact space has dimension \(3N\). Its characteristic cubic factors into three linear directions over an algebraic closure. Distinct factors give univariate characteristic families; repeated factors give polynomial factors multiplying such families. This is a complete constant-coefficient PDE organization of the all-cubic problem.

## Homogeneous quartics: the exact dimension formula

Let \(H\ne0\) be a homogeneous binary quartic. Write \(H=aR^g\), where \(R\) is not a proper polynomial power, and set \(e=\deg R=4/g\). The possibilities are \(e=1,2,4\). If \(\mathcal E_n(H)\) denotes homogeneous degree \(n\), then

\[
\boxed{
\dim\mathcal E_n(H)=2+\mathbf1_{e\mid(n-2)},\qquad n\ge2.
}
\]

The dimensions in degrees zero and one are one and two. The Hilbert series is

\[
\boxed{
\sum_{n\ge0}\dim\mathcal E_n(H)t^n
=1+2t+\frac{2t^2}{1-t}+\frac{t^2}{1-t^e}.
}
\]

The proof identifies the adjoint of the third transvectant with a first transvectant under invariant apolar pairings. Explicitly, for the nondegenerate degree-\(n\) pairing \(B_n\),

\[
B_{n-2}(T_3(H,G),F)
=-6n(n-1)B_n(G,\{H,F\}).
\]

Rank–nullity gives \(\dim\mathcal E_n=2+\dim C_{n-2}(H)\), and the homogeneous centralizer has one dimension exactly when \(e\) divides its degree. This is the structural reason for the periodic dimension jumps. The full proof, signs and explicit coefficient recurrence appear in the quartic appendix.

Fourth powers of linear forms have dimension three in every degree at least two. Squares of genuine quadratics have dimension three in even degrees and two in odd degrees. Every quartic that is not a square has dimension three at degrees congruent to two modulo four and dimension two otherwise. Four distinct roots and a triple-plus-simple-root quartic have the same Hilbert function, although their actual partner polynomials differ. Root geometry influences bases beyond what the dimension sequence records.

A canonical exact partner is the Hessian determinant

\[
\Delta_H=H_{qq}H_{pp}-H_{qp}^2,
\qquad \boxed{T_3(H,\Delta_H)=0.}
\]

For every quartic that is not a square of a quadratic,

\[
\boxed{\mathcal E_4(H)=\operatorname{span}\{H,\Delta_H\}.}
\]

The Hessian then has a nonzero Poisson bracket with \(H\). Thus invariant theory constructs an active exact partner directly. For \(H=q^4+\lambda q^2p^2+p^4\),

\[
\Delta_H=24\lambda(q^4+p^4)+(144-12\lambda^2)q^2p^2,
\]

\[
\{H,\Delta_H\}=288(4-\lambda^2)qp(q^4-p^4).
\]

The activity disappears at \(\lambda=\pm2\), precisely the displayed quadratic-square cases. This is a clean algebraic boundary rather than a numerical threshold.

## Arbitrary coefficients: the complete qF(p) classification

Put \(\mathcal A=K[p]\oplus qK[p]\) and let \(H=qF(p)\), with \(M=\deg F\ge2\). Every polynomial has a unique expansion \(G=\sum_cq^cA_c(p)\). For odd \(k\ge3\), the correction gate on one component is

\[
T_k(qF,q^cA_c)
=(c)_{k-1}q^{c-k+1}
\bigl[kF^{(k-1)}A_c'-(c-k+1)F^{(k)}A_c\bigr].
\]

Different \(q\)-degrees cannot cancel at a fixed derivative order. The third gate, for \(c\ge2\), becomes

\[
3F''A_c'=(c-2)F'''A_c.
\]

This is a first-order differential equation with a polynomial-integrality condition. Together with the fifth gate it produces the following exhaustive answer.

For \(M=2\),

\[
\boxed{\mathcal E(qF)=\mathcal A\oplus q^2K[q].}
\]

For \(M=3\),

\[
\boxed{
\mathcal E(qF)=\mathcal A\oplus
\operatorname{span}\{q^{3r+2}(F'')^r:r\ge0\}.
}
\]

For \(M\ge4\), the answer is \(\mathcal A\oplus Kq^2\), with exactly one additional line \(Kq^3R(p)\) if and only if \(F''=\gamma R^3\) for a nonzero scalar \(\gamma\) and polynomial \(R\). Thus

\[
\boxed{
\mathcal E(qF)=\mathcal A\oplus Kq^2
\quad\text{or}\quad
\mathcal A\oplus Kq^2\oplus Kq^3R.
}
\]

The cube condition says that the multiplicities of every irreducible factor of \(F''\) are divisible by three. It is a structural algebraic locus. For example,

\[
F=5p^8+28p^6+70p^4+140p^2,
\qquad F''=280(p^2+1)^3,
\]

has the extra partner \(q^3(p^2+1)\). The Hamiltonian is degree nine and has several terms, so this theorem extends well beyond homogeneous monomial demonstrations.

Why do all higher \(q\)-degrees disappear once \(M\ge4\)? If \(c\ge4\) and \(d=\deg A_c\), the leading coefficients of the third and fifth gates force

\[
3d=(M-2)(c-2),\qquad5d=(M-4)(c-4).
\]

Eliminating \(d\) gives \((M+1)(c+1)=15\), impossible for \(M,c\ge4\). The \(c=2\) equation forces a constant coefficient, and the \(c=3\) equation forces the cube root of \(F''\). This finite obstruction calculation closes the arbitrary-degree classification.

## The Lie structure and the smaller stable core

The coordinate space \(\mathcal A\) is pairwise Moyal-exact and Poisson Lie-closed:

\[
\{qA+B,qC+D\}=q(AC'-A'C)+(AD'-B'C).
\]

It is a semidirect structure built from polynomial vector fields on a line and polynomial functions. In the momentum representation, Weyl quantization gives first-order differential operators, including the half-density correction \(B'(p)/2\). This coordinate Lie algebra is classical and belongs to the established Groenewold–Van Hove literature; the Hamiltonian-specific conclusions here identify its role inside the larger partner kernel.

For every \(H=qF(p)\) with \(\deg F\ge2\),

\[
\boxed{\mathcal D(H)=\mathcal A.}
\]

In a permitted component \(q^cA_c\) with \(c\ge2\), the exact coefficient space is one dimensional. The Poisson action sends its coefficient to \(FA_c'-cF'A_c\). Its leading degree increases by \(M-1\), with nonzero leading factor \(d-cM\). It therefore leaves that one-dimensional permitted coefficient line. Distinct \(q\)-degrees cannot repair the failure. Only \(\mathcal A\) remains invariant.

Every Lie subalgebra contained in \(\mathcal E(H)\) and containing \(H\) must be invariant under \(D_H\). Consequently \(\mathcal A\) is the unique largest such Lie subalgebra. For the favorite \(qp^3\), the unique largest ordinary associative subalgebra of \(\mathcal E(H)\) is \(K[p]\): the leading term of the cube of any polynomial of positive \(q\)-degree violates the resonance congruence. These are different closure answers to different questions.

## A quadratic perturbation that changes the dynamical answer completely

Take

\[
H_0=qp^3,\qquad H=qp^3+q^2.
\]

The entire first-bracket space is unchanged: \(\mathcal E(H)=\mathcal E(H_0)\). Nevertheless,

\[
\boxed{\mathcal D(H_0)=K[p]\oplus qK[p],
\qquad\mathcal D(H)=\operatorname{span}\{1,H\}.}
\]

Here is a finite reduction proof. Let \(E_0=\mathcal E(H)\) and \(E_{j+1}=E_j\cap D_H^{-1}E_j\). Direct coefficient comparison in the known monomial basis gives

\[
E_1=\{uH+A(p)+q(b_1p+b_0)\}.
\]

The higher resonant monomials cannot survive: the base Hamiltonian sends them to the wrong \(p\)-degree, while the \(q^2\) perturbation sends them into a different \(q\)-degree congruence class. The \(q^2\) coefficient is the single place where a cancellation can occur with the strip component.

Writing \(Y=q+p^3/2\), a second comparison yields

\[
E_2=\operatorname{span}\{1,p,p^2,Y,pY,H\}.
\]

The exact Poisson actions are

\[
D_Hp=2Y,\quad D_HY=\tfrac32p^5,\quad
D_Hp^2=4pY,\quad D_H(pY)=2H+2p^6.
\]

The independent outside components \(p^5,p^6\) remove \(Y,pY\) from any invariant subspace. The first and third equations then remove \(p,p^2\). Constants and \(H\) remain. Equivalently, the descending dimensions after reaching \(E_2\) are six, four and two, with the last space verified invariant. This proves the global answer, rather than inferring it from a degree truncation.

This reduction is an observability calculation. Regard the correction operators as outputs and the Poisson action as a transition operator. Then

\[
\boxed{
\mathcal D(H)=\bigcap_{j\ge0}\ker\bigl(C_H D_H^j\bigr),
\qquad C_H=(T_3(H,\cdot),T_5(H,\cdot),\ldots).
}
\]

The stable exact sector is the unobservable subspace for quantum-correction outputs. In a proved finite-dimensional invariant model, the usual invariant-kernel algorithm can certify it. A naive degree cutoff is insufficient when \(D_H\) increases degree; exact invariance must be checked in the full polynomial ring. This gives a concrete route from the atlas's observability machinery to a quantum-classical classification problem.

## Complete monomial organization

For \(H=q^ap^b\), each odd correction sends distinct partner monomials to distinct output monomials. Thus \(\mathcal E(H)\) is monomial-spanned, and a full polynomial classification reduces to an exponent classification. The coefficient is

\[
S_k(a,b;c,d)=\sum_{j=0}^k(-1)^j\binom kj
(a)_{k-j}(b)_j(c)_j(d)_{k-j}.
\]

A monomial \(q^cp^d\) is exact if and only if every \(S_k\) for odd \(k\ge3\) vanishes. The full classification developed here gives a particularly simple global criterion for nonconstant monomial Hamiltonians:

\[
\boxed{
\mathcal E(q^ap^b)/\bigl(\mathcal E(q^ap^b)\cap\ker D_H\bigr)
\text{ is infinite dimensional}
\iff \min(a,b)\le2.
}
\]

A small transverse degree gives explicit noncommuting univariate families. When \(a,b\ge3\) and \(a\ne b\), the entire exact-partner space is finite dimensional. Its complete exponent list is computable from finitely many integer-root tests of cubics, followed by all correction gates. The top odd correction reduces candidates to finite-width strips and, in even total degree, one affine line. On each strip or line the third gate is a nonzero cubic. This is a terminating all-degree algorithm, not a rectangular search bound. The appendix gives the proof and delivered implementation.

A concrete unequal-exponent output of the complete algorithm is

\[
\boxed{\mathcal E(q^3p^5)=\mathcal P_{\le2}
\oplus\operatorname{span}\{q^3p^5,qp^{17}\}.}
\]

The degree-eighteen partner has nonzero bracket \(46q^3p^{21}\). This finite basis is complete over all partner degrees. More generally, \(q^3p^b\) and \(qp^{3b+2}\) are exact partners: the third-order resonance cancels and their combined available q differentiation excludes every higher odd correction. It also follows by exchanging the Hamiltonian and observable roles in the exceptional cube-root line of the \(qF\) theorem. Exactness is a symmetric relation between two symbols, although the partner space attached to each fixed Hamiltonian can have a very different size.

Balanced powers have a different structure. Put \(H=(qp)^m\), and let \(\mathcal P_{\le2}\) denote all quadratics and lower degrees. The exact answers are

\[
\mathcal E((qp)^2)=K[q]+K[p]+K[qp],
\]

\[
\boxed{
\mathcal E((qp)^3)=K[qp]+\mathcal P_{\le2}
+\operatorname{span}\{qp^{11},q^{11}p\},
}
\]

\[
\boxed{
\mathcal E((qp)^m)=K[qp]+\mathcal P_{\le2},\qquad m\ge4.
}
\]

Thus a balanced sextic has two exceptional active degree-twelve partners; balanced higher powers have only the four active quadratic directions modulo their commuting diagonal family. The infinite commuting family \(K[qp]\) must be distinguished from an infinite active sector.

Ordinary functions of a Hamiltonian require care. For unequal \(a,b\ge2\), the third correction on \(H^r\), \(r\ge2\), has nonzero coefficient

\[
-2ab\,r(a-b)(r-1)\bigl((a+b)(r+1)-3\bigr).
\]

Consequently classical conservation of \(H^r\) does not make its uncorrected Weyl symbol commute quantum mechanically. Star powers provide the corrected quantum conserved expressions.

## The original family has a finite quantum ladder

For \(H=qp^3\), write \(C_r=q^{3r+2}p^r\). Its first bracket is exact, but the second differs by a nonzero term:

\[
(L_\star^H)^2C_r-D_H^2C_r
=(12r+9)(3r+2)(3r+1)\hbar^2q^{3r}p^{r+2}.
\]

There is still a deeper organizing structure. Set \(c=3r+2\) and \(N=4r+3\). Both the classical and quantum chains terminate at exactly the same finite length:

\[
D_H^NC_r=(-2)^NN!H^c,\qquad D_H^{N+1}C_r=0,
\]

\[
\boxed{
(L_\star^H)^NC_r=(-2)^NN!H^{\star c},
\qquad(L_\star^H)^{N+1}C_r=0.
}
\]

The last surviving classical invariant is an ordinary power; the quantum one is the corresponding star power. For \(r=0\), the full formal evolution is an especially transparent polynomial:

\[
\boxed{
e^{tL_\star^H}q^2
=q^2(1-2tp^2)^3
+9\hbar^2t^2p^2(1-2tp^2).
}
\]

The first term is the classical evolution. The second is its exact quantum correction. At first order in time the two agree; the difference begins at second order. All time coefficients terminate after degree three in this example.

The proof uses a faithful localized Weyl representation. With \(q=i\hbar\partial_p\), the Hamiltonian becomes \(i\hbar(p^3\partial_p+3p^2/2)\). The algebraic coordinate \(y=p^{-2}\) and conjugation by \(y^{3/4}\) reduce it to \(-2i\hbar\partial_y\). The transformed \(C_r\) has polynomial coefficients in \(y\) of maximum degree \(N\); repeated commutators differentiate those coefficients. The argument is algebraic after localization and does not assert a globally defined real coordinate transformation or analytic operator equivalence. Full details and exact finite-chain checks are supplied in the independent appendix.

## Coordinate changes, existing research and the next boundary

Affine symplectic changes preserve the full canonical Moyal structure and transport all the exactness results. General invertible linear changes preserve the vanishing transvectant gates while rescaling the deformation parameter. Ordinary nonlinear canonical substitutions require additional care. For example, the exact pair \(P^3,Q^2P\) in canonical variables becomes \((p+q^2)^3,q^2(p+q^2)\) under \(Q=q,P=p+q^2\), but its third transvectant is \(-72q\). The new normalized bracket has a \(+3\hbar^2q\) correction. Classical symplectic covariance alone does not justify using the same flat-coordinate Moyal formula after a nonlinear substitution.

Robert's universal-observable theorem says that, under its symbol-growth assumptions, equality with the Moyal bracket for every Schwartz observable forces a Hamiltonian to be quadratic. Our statements concern explicitly restricted polynomial partner spaces and do not challenge that theorem. Gotay's coordinate Lie algebra supplies the classical closure context. The transvectant language belongs to established invariant theory, including Olver–Sanders. The derived formulas in this note are proved and replayed here without a claim that their literature priority has been established.

The current PerfectJet main source, pinned at commit `494caaf6df145175e11ac65c260b39b6e1aa2765`, already integrates the full seven-coefficient sextic partner classification through partner degree twenty. Its global classification retains archived computer-algebra solver dependencies; exact instance replay and global solver receipts have different evidential roles. Degrees twenty-one and above remain open for that full-space programme. The monomial all-degree results here close specific strata without replacing or overstating that broader classification.

The next substantial frontier is therefore sharply located. For arbitrary quintic and sextic Hamiltonians, classify active polynomial kernels in all degrees and identify exceptional factorization loci. For quartics, build canonical bases and dynamic cores across the full moduli space, beyond the completely determined static dimensions. For larger degrees of freedom, classify stable exact Lie sectors under their own hypotheses. For computation, produce independently checkable certificates for the invariant-kernel reductions and explicit partner bases. Each task now has a precise object, a proof obligation and a usable exact engine.
