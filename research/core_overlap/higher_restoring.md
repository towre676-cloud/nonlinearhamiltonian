# Quadratic shears with every nonlinear composition and a restoring potential

This note closes a non-affine part of the cubic-phase sector in all
polynomial degrees. The coefficient field has characteristic zero. The
original flat Weyl product is fixed throughout; a nonlinear canonical
substitution does not replace that product by a new flat product.
Historical priority is unestablished.

## The complete restoring theorem

Let

\[
 P=p+w(q),\qquad w(q)=c q^2+dq+e,\qquad c\ne0,
 \qquad H=F(P)+\lambda q^2+\epsilon q+C,
 \qquad \deg F\ge3,\quad\lambda\ne0.
 \tag{HR1}
\]

Write \(D=\{H,\cdot\}\), with the convention
\(\{f,g\}=f_qg_p-f_pg_q\), and let \(C_3=T_3(H,\cdot)\) be the
third unnormalized odd transvectant in the original \((q,p)\)
coordinates. For \(r\ge0\), put

\[
 S_r=\bigcap_{j=0}^r\ker(C_3D^j).
 \tag{HR2}
\]

**Theorem HR.** In the full polynomial ring, without an input-degree
cutoff,

\[
 \begin{aligned}
 S_1&=\operatorname{span}\{1,q,P,H\},\\
 S_2&=\operatorname{span}\{1,P,H\},\\
 S_3&=\operatorname{span}\{1,H\}
       =\mathcal D_\infty(H).
 \end{aligned}
 \tag{HR3}
\]

Thus the third gate at Hamiltonian depths zero through three already
determines the entire dynamic core. Depth three is necessary. In
particular, for every integer \(m\ge3\),

\[
 H=(p+q^2)^m+\lambda q^2,\quad\lambda\ne0
 \quad\Longrightarrow\quad
 \mathcal D_\infty(H)=\operatorname{span}\{1,H\}.
 \tag{HR4}
\]

For \(\lambda=0\), the retained QC theorem instead gives the infinite
core \(K[P]+Kq\), sharply at third-gate depth one. Thus the nonlinear
composition undergoes an infinite-to-two transition and a depth-one to
depth-three transition when the restoring coefficient leaves zero.
For \(\deg F=2\), the retained SO/CQ theorem gives
the six-dimensional quadratic sector when the restoring coefficient is
nonzero. These are different proved branches; Theorem HR assumes both
\(\deg F\ge3\) and \(\lambda\ne0\).

## Exact original-coordinate operators

Expressing the original derivation and gate in the polynomial
coordinates \((q,P)\) gives

\[
 \begin{aligned}
 D&=-F'(P)\partial_q+(2\lambda q+\epsilon)\partial_P,\\
 C_3&=-F'''(P)\partial_q^3
       -6cF''(P)\partial_q\partial_P^2
       -6cF'''(P)\partial_q\partial_P.
 \end{aligned}
 \tag{HR5}
\]

The affine and constant terms of \(w\) do not enter the third gate.
The term \(\lambda q^2+\epsilon q+C\) has no original-coordinate
third derivatives and adds nothing to \(C_3\). Formula (HR5) follows
by the original mixed-derivative formula, or by retaining the
coefficient of degree three in the triangular generating formula. It
does not assert covariance of the flat Weyl product under the shear.

## Why two tests already give a four-dimensional upper space

Take \(G\in S_1\) and write
\(G=\sum_{j=0}^Nq^j g_j(P)\), with \(g_N\ne0\).
Assume first that \(N\ge3\). In \(C_3G=0\), the coefficients of
\(q^{N-1}\) and \(q^{N-2}\) are respectively nonzero scalar
multiples of

\[
 (F''g_N')'=0,\qquad (F''g_{N-1}')'=0.
 \tag{HR6}
\]

Since \(F''\) is nonconstant, a polynomial \(g_j\) can satisfy
\(F''g_j'\in K\) only when \(g_j'=0\). Hence
\(g_N\) and \(g_{N-1}\) are constants. The coefficient of
\(q^{N-3}\) then gives

\[
 6c(N-2)(F''g_{N-2}')'
       =-N(N-1)(N-2)g_NF'''.
 \tag{HR7}
\]

After integration,
\(F''[6c g_{N-2}'+N(N-1)g_N]\) is constant. Its second factor is
a polynomial; because \(F''\) is nonconstant, that constant must be
zero. Therefore

\[
 g_{N-2}'=-\frac{N(N-1)}{6c}g_N\in K.
 \tag{HR8}
\]

There are no terms of \(q\)-degree \(N+1\) or \(N\) in \(DG\).
Its coefficient of \(q^{N-1}\) is

\[
 A(P)=-NF'g_N+2\lambda g_{N-2}'.
 \tag{HR9}
\]

The highest possible coefficient of \(C_3DG\), at \(q^{N-2}\),
is consequently

\[
 -6c(N-1)(F''A')'
     =12cN(N-1)g_NF''F'''\ne0.
 \tag{HR10}
\]

All factors are nonzero in characteristic zero and \(\deg F\ge3\).
Lower coefficients of \(DG\) cannot contribute at that \(q\)-degree,
and the \(\partial_q^3\) term lowers the highest degree by three.
This contradicts \(C_3DG=0\), proving \(N\le2\).

The same top-coefficient argument in \(C_3G=0\) now makes both
positive-\(q\)-degree coefficients constant. Thus

\[
 G=g(P)+a q+bq^2.
 \tag{HR11}
\]

Substitution in (HR5) gives the exact identity

\[
 C_3DG
   =12c\bigl(F''[bF''-\lambda g'']\bigr)'.
 \tag{HR12}
\]

Again the product of nonconstant \(F''\) with a polynomial cannot
be a nonzero constant. Hence
\(g''=(b/\lambda)F''\), and
\(g=(b/\lambda)F+uP+v\). Equation (HR11) is therefore in
\(\operatorname{span}\{1,q,P,H\}\), after absorbing the linear and
constant terms of the restoring potential. Each of these four
generators passes \(C_3\) and \(C_3D\), proving the first equality
in (HR3).

## The two final eliminations and sharp depth

Put

\[
 R(P)=(F''F''')'.
 \tag{HR13}
\]

If \(F(P)=a_mP^m+\cdots\), \(m\ge3\), the leading coefficient
of \(R\) is
\(a_m^2m^2(m-1)^2(m-2)(2m-5)\), at degree \(2m-6\).
Thus \(R\ne0\). Direct calculation gives

\[
 \begin{aligned}
 C_3D^2q&=12c\lambda R, & C_3D^2P&=0,\\
 C_3D^3P&=24c\lambda^2R.&&
 \end{aligned}
 \tag{HR14}
\]

The first line removes \(q\) from \(S_1\); the second removes
\(P\) at the next depth. Constants and \(H\) survive every odd
gate and every depth because \(D1=DH=0\) and odd transvectants are
antisymmetric. This proves the full core equality. The observable
\(P\) passes depths zero, one and two but fails depth three, proving
sharpness.

At \(\lambda=0\), the same highest-\(q\) argument still gives (HR11),
and (HR12) then forces \(b=0\). Consequently
\(S_1=K[P]+Kq\). This space is invariant under
\(D=-F'\partial_q+\epsilon\partial_P\). All its higher odd gates
vanish: on two functions of \(P\), the quadratic-shear generating
formula contains only even powers of its parameter, and \(q\) is
linear in the original coordinates. The observable \(q^2\) passes
\(C_3\) but has
\(C_3D(q^2)=24cF''F'''\ne0\), proving the stated depth-one
sharpness in the zero-restoring branch as well.

## Exact checker and recognition

`higher_restoring.py` recognizes the family directly in rational
original-coordinate coefficients, computes the full original mixed
derivatives independently of (HR5), and checks (HR10), (HR12), and
(HR14). Finite full-output kernel calculations replay the dimensions
four, three and two in boxes containing the proved bases; those boxes
supplement the all-degree argument above. Invalid exponents, floating
inputs, zero restoring coefficient, nonquadratic shear and quadratic
composition are rejected rather than silently classified.

The recognizer normalizes the constant part of the shear to zero and
absorbs it into \(F\). Recognition failure means outside this theorem.
No general classification of arbitrary non-affine cubic-phase
Hamiltonians or variable restoring potentials is asserted.
