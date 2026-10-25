# Quadratic shears with nonlinear residual potentials: the remaining constant-quadratic stratum

Let `Q=p+u(q)`, `deg u=2`, and let

\[
H=AQ^2+V(q),\qquad A\ne0,
\qquad V\in K[q],\quad\deg V\ge3,
\]

over a characteristic-zero field, using the original flat Weyl–Moyal
product in `(q,p)`.

**Theorem QR.** The full polynomial dynamic core is

\[
\boxed{\mathcal D_\infty(H)=\operatorname{span}\{1,H\}.}     \tag{QR1}
\]

Only the third gate is needed, with the sharp depths

\[
\boxed{\mathcal D_\infty(H)=
\bigcap_{r=0}^{R}\ker(C_3D^r),\qquad
R=\begin{cases}6,&\deg V=3,\\4,&\deg V\ge4.\end{cases}}    \tag{QR2}
\]

These are all-degree results, not extrapolations from bounded polynomial
spaces. Together with QC and the oscillator theorem, QR completes every
constant-quadratic Hamiltonian `A p^2+B(q)p+C(q)` with `deg B=2`.
Together with QF, all such Hamiltonians with `deg B>=2` are classified.

## Residual degree at least four

In the independent polynomial variables `(q,Q)`, the exact operators are

\[
D=-2AQ\partial_q+V'\partial_Q,\qquad
C_3=V'''\partial_Q^3-6Au''\partial_q\partial_Q^2,            \tag{QR3}
\]

where `u''` is a nonzero constant. Suppose a polynomial `G` has top
`Q` term `g(q)Q^N`, with `N>=3`. The coefficient of `Q^(N-2)`
in `C3G=0` forces `g'=0`. Let `h(q)` be the coefficient of
`Q^(N-1)`. The next coefficient then gives

\[
h'=\frac{N V'''g}{6Au''}.
\]

The leading `Q^N` coefficient of `DG` is `-2Ah'`, which is nonzero.
The leading equation `C3DG=0` forces its derivative to vanish, giving
`V''''g=0`. This is impossible when `deg V>=4`. Thus the joint
kernel of `C3,C3D` has `Q` degree at most two. Its quadratic coefficient
is constant because `u''!=0`.

The depth-two kernel is the six-dimensional space `S_H` defined in (QF8).
The proof of (QF9) applies verbatim. Its two successive `D` preimages
remove first `qQ,Q` and then `q^2,q`, since `deg V>=4`.
This proves (QR1) and depth-four sufficiency in this stratum. The exact
identity

\[
C_3D^4q=96A^4u''V''''\ne0,
\qquad C_3D^rq=0\quad(0\le r\le3)                       \tag{QR4}
\]

proves sharpness.

## Cubic residual: rational normalization

Write `u=bq^2+cq+d`, `b!=0`, and
`V=vq^3+v_2q^2+v_1q+v_0`, `v!=0`. Translate
`q=x-v_2/(3v)` to remove the quadratic term of `V`, and use an affine
shear in `p` to remove the resulting linear and constant terms of `u`.
These are affine canonical transformations, so the flat Moyal gates are
covariant. Up to a constant the resulting Hamiltonian is

\[
A(p+bq^2)^2+vq^3+eq,
\qquad e=v_1-v_2^2/(3v).
\]

Now substitute `q=sx,p=ty`, with

\[
s=\frac{v}{Ab^2},\qquad t=bs^2,
\]

and divide the Hamiltonian by `At^2`. The normalized form is

\[
\boxed{H_\lambda=(p+q^2)^2+q^3+\lambda q,
\qquad \lambda=\frac{eA^2b^4}{v^3}.}                     \tag{QR5}
\]

All scales are nonzero elements of the coefficient field. The retained
`GL2` covariance of transvectants, together with nonzero Hamiltonian
rescaling and constant shifts, preserves every vanishing gate condition
and its bracket depth. Thus no algebraic extension or parameter exclusion
is hidden in this reduction.

In `(q,Q)` coordinates the normalized operators are

\[
D=-2Q\partial_q+(3q^2+\lambda)\partial_Q,
\qquad C_3=6\partial_Q^3-12\partial_q\partial_Q^2.           \tag{QR6}
\]

## An all-degree bound for the depth-two kernel

Give `q,Q` weights `1,2`, respectively. The top operators are

\[
D_0=-2Q\partial_q\quad(\text{shift }1),\qquad
C_0=-12\partial_q\partial_Q^2\quad(\text{shift }-5).
\]

Their joint kernel through depth two is

\[
K[Q]+\operatorname{span}\{q,qQ,q^2\}.                     \tag{QR7}
\]

Indeed, `C0 D0^r` sends each `q^aQ^c` to one monomial with coefficient
proportional to `(a)_(r+1)(c+r)_2`. At `r=0,1,2` these conditions leave
exactly the displayed monomials, and distinct inputs have distinct images
for each fixed `r`.

Consequently, a polynomial passing `C3D^r` for `r=0,1,2` and having
weighted degree greater than six would have top `c Q^N`, `N>=4`.
Normalize `c=1`. Let `G1` be its component of weight `2N-1`.
The gate component of weight `2N-6` is

\[
C_0G_1+6\partial_Q^3Q^N=0.
\]

Since `C0` is monomially injective on all monomials with positive
`q` degree and `Q` degree at least two, this forces

\[
G_1=\frac N2qQ^{N-1}+\beta q^{2N-1}+\gamma q^{2N-3}Q.      \tag{QR8}
\]

In particular, the correction `q^3Q^(N-2)` is forbidden when `N>=4`.
The term `lambda partial_Q` has shift `-2`, so it does not enter
this first-deficit calculation.

The top nonzero component of `DG` has weight `2N`, and is

\[
-NQ^N-2(2N-1)\beta q^{2N-2}Q
-2(2N-3)\gamma q^{2N-4}Q^2+3Nq^2Q^{N-1}.
\]

Applying `C0`, the final term contributes

\[
-72N(N-1)(N-2)qQ^{N-3}.
\]

It cannot cancel: the first two terms have zero gate, and the third
produces a monomial of `Q` degree zero, whereas `N-3>=1`.
This contradicts `C3DG=0`. Therefore the full depth-two kernel has
weight at most six, in all polynomial degrees.

The finite ambient space is consequently

\[
B_6=\operatorname{span}\{q^iQ^j:i+2j\le6\},\qquad\dim B_6=16.
                                                                    \tag{QR9}
\]

This is a proved bound. The exceptional cubic `N=3` is intentionally
retained and is handled by the exact finite certificate below.

## Exact parameter-polynomial rank certificate

Inside `B6`, form the full-output matrix of `C3D^r`, `r=0..6`.
Delete the columns `1,Q^2`; the remaining fourteen columns are

\[
\{q^iQ^j:i+2j\le6\}\setminus\{1,Q^2\}.
\]

Select the fourteen rows `(r,i,j)` recorded in the certificate:

\[
\begin{gathered}
(0,0,0),(0,1,0),(1,0,0),(1,1,0),(1,2,0),\\
(2,0,0),(2,1,0),(2,2,0),(2,3,0),\\
(3,0,0),(3,1,0),(4,0,0),(5,0,0),(6,0,0).
\end{gathered}
\]

Here `(i,j)` is the output monomial exponent pair in `(q,Q)`.
Their minor determinant is the nonzero constant polynomial

\[
-2489071056189074244411853807879968522240000000.           \tag{QR10}
\]

The independent standard-library checker verifies this as an **exact
polynomial identity**. Since `D=D_a+lambda partial_Q` and `C3` is
independent of `lambda`, every depth-`r` matrix entry has parameter
degree at most `r`. The determinant therefore has degree at most the
sum of its row depths, namely `32`. The checker recomputes the minor
and its exact rational determinant at the thirty-three distinct integers
`0..32`, obtaining the stated constant each time. A polynomial of degree
at most `32` with thirty-three roots is zero. This proves (QR10) for
every parameter, rather than inferring universality from sampled ranks.
All outputs are retained; none are projected into `B6`.

The full matrix therefore has rank at least fourteen for every `lambda`.
Its sixteen-dimensional domain contains the independent kernel vectors
`1,H_lambda`, so the rank is exactly fourteen and its kernel exactly
their span. Together with the proved bound (QR9), this establishes the
all-degree core and depth-six sufficiency.

## Sharp cubic depth and verification scope

For every cubic `V`, direct exact differentiation gives

\[
C_3D^rq=0\quad(0\le r\le5),\qquad
C_3D^6q=-960A^5u''(V''')^2\ne0.                           \tag{QR11}
\]

Thus depth six is necessary for every Hamiltonian in the cubic stratum,
including all lower coefficients. The code checks QR3 against the separate
original-coordinate PBW engine, and verifies QR4 and QR11 on eighteen
rational fixtures, including shifted shears, negative and rational
coefficients, general cubic potentials, and higher residual degrees.
It rejects corrupted minors, constants, parameter degree bounds, and
insufficient interpolation populations.

The theorem is about the fixed original flat Weyl product. It does not
claim arbitrary nonlinear covariance or historical priority. The finite
matrix is used only after an all-degree bound has been proved, and its
parameter universality is an exact bounded-degree polynomial identity.
