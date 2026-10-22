# Dynamic cores of quartics: four root strata and quadratic perturbations

This October 22, 2026 supplement extends the October 21 publication without replacing its proofs or archived editions. The results below are direct algebraic derivations; no literature-priority claim is made. Work over a characteristic-zero field K. Statements about root multiplicities and changes of coordinates can be read over its algebraic closure and then descended to K. The fixed product is the canonical Weyl–Moyal product in one pair. Put L_H G = T_3(H,G) and delta_H G = {H,G}. All symbols G are independent of hbar.

## Exactness, refinement and valid stopping rules

For H = H_4 + Q with H_4 a nonzero homogeneous quartic and degree Q at most two, E(H) = ker L_(H_4). Write

\[
K_j(H)=\bigcap_{r=0}^{j}\ker(L_{H_4}\delta_H^r),\qquad
D(H)=\bigcap_{j\geq0}K_j(H).
\]

Thus K_0 is one-step exactness. K_1 additionally requires that the first classical derivative is an exact partner; this is the condition for two successive Hamiltonian actions to agree. These are linear preimage intersections, not products of bidifferential operators. An active partner has delta_H G nonzero; its membership in E alone says nothing about membership in D.

The core D is the largest delta_H-invariant vector subspace contained in E. It is exactly the space on which every iterated classical and normalized Moyal action agrees. If all lower iterates agree, applying the two actions one more time shows that their difference is the Moyal defect of that classical iterate. This proves both implications by induction. No analytic convergence of the time series is asserted.

If a finite-dimensional candidate W lies in E and exact rational identities delta_H w_i = sum_j a_(ji) w_j hold for every basis vector, W lies in D by induction. If a proved global refinement K_j equals W, this also proves D = W. A matrix that projects higher-degree terms back into W is invalid. A plateau of bounded-degree preimage dimensions is also insufficient: the surviving vectors may evolve to degrees beyond that bound. The implementation returns the full action matrix only when there is no such leakage.

There is also a useful leading-form principle. For every G in D(H_4+Q), its highest homogeneous component lies in D(H_4). More generally its leading component lies in K_j(H_4) whenever G lies in K_j(H_4+Q). Indeed delta_(H_4) raises total degree by two, delta_Q raises it by at most zero, and L_(H_4) lowers it by two. The highest-degree coefficient of L_(H_4) delta_H^r G is therefore L_(H_4) delta_(H_4)^r G_top, including when that expression is zero. This gives necessary conditions without assuming that individual iterates retain their initial degrees.

## Classification in four root strata

In the following displayed normal forms Q = a p^2 + b qp + c q^2 + d p + e q + f. Scalar multiplication of the entire H and affine symplectic changes of coordinates preserve the classifications, with the displayed coefficients interpreted in those coordinates.

\[
\begin{array}{c|c|c}
H_4&\text{parameter stratum}&D(H_4+Q)\\\hline
q^4&a=0&K[q]+pK[q]+p^2K[q]\\
q^4&a\ne0&\operatorname{span}_K\{1,H\}\\
q^3p&a=0&K[q]+pK[q]\\
q^3p&a\ne0&\operatorname{span}_K\{1,H\}\\
(qp)^2&Q\in K\,qp+K&K[qp]\\
(qp)^2&Q\notin K\,qp+K&\operatorname{span}_K\{1,H\}\\
q^2p^2+\kappa q^4,\ \kappa\ne0&\text{every }Q&\operatorname{span}_K\{1,H\}.
\end{array}
\]

These are complete all-degree results in the stated normal forms, including the equality boundaries a = 0 and the entire commuting-perturbation plane for the square stratum. They cover root multiplicities (4), (3,1), (2,2), and (2,1,1). The four-simple-root stratum remains open here. The degree bound in a numerical fixture is not part of these theorems.

For a square H_4 = alpha R^2 of a nondegenerate homogeneous quadratic R, the coordinate-free version is D = K[R] if {R,Q} = 0, and D = span{1,H} otherwise. A quadratic Q commutes with nondegenerate R exactly when Q belongs to K R + K. Diagonalize R to a nonzero multiple of qp over the algebraic closure; the assertion follows from the square proof below and rank descent. In particular it covers real elliptic quadratics such as q^2+p^2, not only split quadratics. A degenerate R belongs to the fourth-power case instead.

## Fourth powers: a complete five-parameter perturbation boundary

For H = q^4 + Q the October 21 kernel is the full p-degree-two strip E = {A(q)+pB(q)+p^2 C(q)}. Put V(q) = q^4+cq^2+eq+f. The derivation is

\[
\delta_H=(V'(q)+bp)\partial_p-(2ap+bq+d)\partial_q.
\]

If a = 0 it preserves that entire strip, so D = E. In fact it preserves each finite span in the strip with weighted degree at most w, assigning weights 1 to q and 3 to p. Every term of the displayed derivation has nonpositive weighted degree. Thus every observable in this infinite core belongs to a finite-dimensional invariant family. For Q = 0 the action on the strip is nilpotent of index at most three.

Now let a be nonzero. The p^3 coefficient of delta_H G is -2a C'. The first global refinement therefore forces C constant. The p^2 coefficient is then -2a B'+2bC; requiring its derivative to vanish forces B'' = 0 in the second refinement. The p coefficient of delta_H G is 2CV'+bB-(bq+d)B'-2a A'. Requiring its second derivative to vanish in the third refinement forces A''' = (C/a)V'''. Consequently

\[
K_3(H)=\operatorname{span}\{1,H,q,q^2,p,qp\}.
\]

For clarity, integrating the last identity gives A = (C/a)V plus an arbitrary quadratic, and B is arbitrary affine; absorbing the bpq and dp terms into H gives exactly this six-dimensional space. Conversely these coefficient conditions suffice, so this is an equality of global polynomial spaces.

In an invariant subspace of K_3, the coefficient of qp must vanish: delta_H(qp) has q^4 and p^2 coefficients 4 and -2a, whereas H has those coefficients 1 and a. No other displayed derivative supplies both of these terms, so membership in K_3 forces that coefficient to zero. Next the coefficient of p vanishes because delta_H p = 4q^3+2cq+e+bp and q^3 is absent from K_3. The images of q and q^2 have respectively nonzero p and qp coefficients -2a and -4a. Invariance then forces those coefficients to vanish too. What remains is span{1,H}; both vectors are stationary. Equivalently K_5 = span{1,H}. This proves the collapse for every b,c,d,e,f.

## Triple roots: the same boundary, a different infinite core

Let H = q^3p + Q. Its static kernel is

\[
E=K[q]+pK[q]+\operatorname{span}\{q^r p^{3r+2}:r\geq0\}.
\]

For a resonant term q^r p^(3r+2), the quartic action has p-degree 3r+2, q-degree r+2, and nonzero coefficient 8r+6. The quadratic action on a resonant term changes p-degree by at most one; distinct resonant p-degrees differ by three. Terms from the affine-p strip have p-degree at most two after the quadratic action. Thus for r at least one this quartic term cannot be canceled, or made into another allowed resonant monomial. Every such coefficient vanishes in K_1. The only possible remaining resonance is the constant multiple u p^2.

If a = 0, the same argument eliminates that last term, whose derivative has nonconstant p^2 coefficient. The affine-p strip is invariant under H, so K_1 = D = K[q]+pK[q]. This is pairwise Moyal-exact and Poisson Lie closed. For Q = 0, however, delta_H^j(q) has nonzero degree 2j+1 for every j. These active orbits are infinite dimensional, unlike the locally finite fourth-power strip.

Suppose a is nonzero. Write F = q^3+bq+d and V = cq^2+eq+f, so H = pF+ap^2+V. For G = A+pB+up^2 the three p coefficients of its derivative, from highest to lowest, are

\[
2uF'-2aB',\quad F'B+2uV'-FB'-2aA',\quad V'B-FA'.
\]

The first must be constant, giving B = (u/a)F+vq+w. It follows that K_1 = K H + K[q] + p span{1,q}. For such a vector, subtracting its H component and applying the same condition once more gives

\[
A'=\frac{2v}{a}q^3+\frac{3w}{2a}q^2+\text{an affine polynomial}.
\]

Hence the second global refinement is the six-dimensional space

\[
K_2=\operatorname{span}\{1,H,q,q^2,Y,Z\},\quad
Y=p+\frac{q^3}{2a},\quad Z=qp+\frac{q^4}{2a}.
\]

The leading pure-q terms of delta_H Y and delta_H Z are respectively -3q^5/(2a) and -2q^6/a. No other basis derivative has these terms. Invariance first removes Z and then Y. Finally delta_H q = -2aY-bq-d and delta_H(q^2) = -4aZ-2bq^2-2dq remove q and q^2. Thus D = span{1,H}, and in fact K_4 already equals it. This is an arbitrary-quadratic extension of the published qp^3+q^2 example, transported by exchanging the canonical directions with the appropriate sign.

## Two double roots: loss of the entire commuting tower

Let s = qp, H = s^2+Q, and write Q = A q^2+B s+C p^2+D q+E p+F for this paragraph. The static exact space is K[q]+K[p]+K[s]. Choose a unique decomposition by putting the common constant in one summand and using only positive powers in the others. The quartic action on q^i p^j is 2(j-i) q^(i+1) p^(j+1). Its action kills every C_0(s), and

\[
\{Q,C_0(s)\}=C_0'(s)(2Aq^2-2Cp^2+Dq-Ep).
\]

If A,C,D,E all vanish, the first refinement removes all nonconstant pure powers, leaving K[s], which is stationary and therefore equals D.

Otherwise C_0 can have degree at most two in K_1. Indeed for any highest power s^k with k at least three, a nonzero quadratic transverse coefficient produces an uncancellable mixed monomial q^(k+1)p^(k-1) or its exchange, with exponent difference two. If the quadratic transverse coefficients both vanish, a nonzero linear transverse coefficient instead produces q^k p^(k-1) or its exchange, with exponent difference one. Both exponents are positive, these monomials are not diagonal, and neither the quartic nor quadratic action on pure-q or pure-p polynomials can cancel them. Distinct powers of s cannot cancel the term with the same exponent difference. This is an all-degree exclusion.

The remaining pure-q and pure-p polynomials have degree at most two: their quartic action would otherwise produce uncancellable mixed terms. Write G = u s^2+v s+A_2 q^2+C_2 p^2+D_1 q+E_1 p+F_0. Comparing q^3p, qp^3, q^2p and qp^2 in delta_H G gives A_2=uA, C_2=uC, D_1=uD and E_1=uE. Thus

\[
K_1(H)=\operatorname{span}\{1,H,s\}.
\]

The derivative of s is 2Aq^2-2Cp^2+Dq-Ep. It belongs to that three-dimensional space only when it is zero, which was excluded. Hence K_2 = D = span{1,H}. An arbitrarily small nonzero transverse perturbation destroys every higher member of the stationary tower K[s], even though E is completely unchanged.

## A double root and two simple roots: all quadratic perturbations collapse

Over the algebraic closure any binary quartic of root type (2,1,1) can be carried, up to a scalar, to H_4 = q^2p^2+kappa q^4 with kappa nonzero. Send its double root to q = 0 and complete the square in p by a linear symplectic shear. A field extension used for this normal form does not change kernel ranks or polynomial equality statements.

Here is an all-degree argument requiring no symbolic rank extrapolation. For a nonzero homogeneous G of degree n, let i be its least q exponent and d = n-i. In L_(H_4) G the term with least possible q exponent i-1 has coefficient 12 i d(d-i) times that coefficient of G. The kappa q^4 part contributes only at q exponent i+1 or higher. Therefore an exact G can have least exponent only i = 0, i = n/2, or i = n.

For n positive, if i = 0, delta_(H_4) G has least q exponent 1 and nonzero coefficient 2n. This is none of the three permitted least exponents for an exact degree-(n+2) form. If i = n, its derivative has least exponent n+1 and again fails the same test. Both cases leave K_1.

In the remaining case n = 2m and i = m, the q^(m+1) term of delta_(H_4) G cancels. If its derivative is nonzero and exact, its least exponent is strictly greater than m+1. The only permitted possibility is n+2, so the derivative must be a nonzero pure q^(n+2). Its next derivative fails the same test. Consequently every G in K_2 must commute with H_4.

The October 21 homogeneous centralizer theorem says such a G is a scalar multiple of H_4^r, with n = 4r. The power-obstruction formula proved there gives

\[
T_3(H_4,H_4^r)=-\frac{r(r-1)(4r+1)}3\,H_4^{r-2}\{H_4,\Delta_{H_4}\}.
\]

Here Delta = -12q^2p^2+24 kappa q^4 and {H_4,Delta} = -288 kappa q^5p, which is nonzero. Thus only r = 0,1 are exact. Constants are handled separately. We have proved K_2(H_4) = span{1,H_4} in every degree.

Apply the leading-form principle to H_4+Q. Every element of K_2 has degree at most four and its degree-four component is a scalar multiple of H_4. Subtract that multiple of H, which lies in every K_j. Any nonconstant remainder of degree at most three contradicts the same leading-form principle. Therefore, for every quadratic Q,

\[
K_2(H_4+Q)=D(H_4+Q)=\operatorname{span}\{1,H_4+Q\}.
\]

This proves both stabilization and perturbation independence in the entire (2,1,1) stratum.

## What the core is, and what it is not

It is false that polynomial functions of H automatically form an exact core. For H = q^4+p^2, H is stationary and exact but T_3(H,H^2) = 576 q p is nonzero. Hence K[H] is not even contained in E. The proved answer is span{1,H}, whose active quotient is zero. It is an abelian exact Lie algebra but is not an ordinary product algebra or a star subalgebra: H star H has leading hbar-free term H^2 outside that span.

For H = (qp)^2 with commuting quadratic perturbation, D = K[qp] is stationary, pairwise Moyal-exact, and Poisson abelian. Its formal hbar extension is an associative star subalgebra: every term in the star product of two diagonal monomials remains diagonal. In an elliptic quadratic normal form the same claim follows by affine symplectic covariance.

The triple-root affine-p core is a pairwise exact Poisson Lie algebra; it is not an associative algebra, since p times p = p^2 is outside it. The fourth-power core at a = 0 includes the affine-p Lie sector but is itself generally not Poisson Lie closed or multiplicatively closed. For example p^2 and qp^2 lie in it while their Poisson bracket is -2p^3. These distinctions persist even though every vector of that larger strip has exact repeated evolution under its chosen H.

## Computations, negative results and the remaining stratum

The executable uses the October 21 exact star-exponential engine for preimage intersections, and a separate direct derivative-contraction implementation verifies every generated certificate. Full polynomial terms are retained at all iterations. The recorded parameter fixtures are rational examples supporting the displayed proofs, not a symbolic completeness certificate for unseen strata. Invariant certificates list a rational action matrix and are replayed independently. Supported normal-form classification returns theorem identifiers separately from bounded computations.

The four-simple-root family is not classified by this supplement. Finite intersections for H_lambda = q^4+lambda q^2p^2+p^4, including nonsquare rational lambda, and a mixed quartic suggest span{1,H}; any bounded result remains labeled as such. The square parameters lambda = plus or minus two are governed by the square theorem and behave differently. In particular a finite calculation of K_1 through degree N cannot exclude a new high-degree survivor.

For a four-simple-root quartic, the leading-form principle would extend a proof of homogeneous D = span{1,H_4} to every quadratic perturbation immediately. The missing step is that all-degree homogeneous exclusion. Root type alone also does not encode the cross-ratio modulus of four simple roots. No complete classification, universal stabilization index, or invariant-core Hilbert series is claimed there. Higher-degree Hamiltonians and cubic perturbations are outside these theorems.
