# Oscillator forcing in polynomial shear coordinates

All brackets and gates below use the fixed flat Weyl convention in the
original coordinates `(q,p)`. The substitution `Q=p+u(q)` is used to
rewrite differential operators, not to assume nonlinear covariance.
The coefficient field has characteristic zero.

## Complete oscillator sector

Let

\[
 Q=p+u(q),\qquad
 H=AQ^2+BQ+C+\frac{\kappa}{2}q^2+\epsilon q,\qquad A\ne0.
\]

**Theorem SO.** If `deg u>=3`, then for every `kappa,B,C,epsilon`,

\[
 \mathcal D_\infty(H)=
 \ker C_3\cap\ker(C_3D)\cap\ker(C_3D^2)
 =\operatorname{span}\{1,q,Q,q^2,qQ,Q^2\}.             \tag{SO1}
\]

The depth two is sharp for every allowed parameter choice. If
`u=bq^2+cq+d`, `b!=0`, and `kappa!=0`, then instead

\[
 \mathcal D_\infty(H)=\bigcap_{r=0}^3\ker(C_3D^r)
 =\operatorname{span}\{1,q,Q,q^2,qQ,Q^2\},             \tag{SO2}
\]

and depth three is sharp. The quadratic-shear case `kappa=0` is the
previously classified infinite QC family and is excluded from (SO2).
Neither statement classifies nonpolynomial observables.

## Exact operators and the lower bound

Direct chain-rule expansion in `(q,Q)` gives

\[
 D=(\kappa q+\epsilon)\partial_Q-(2AQ+B)\partial_q,
 \qquad
 C_3=(2AQ+B)u'''\partial_Q^3-6Au''\partial_q\partial_Q^2.
                                                               \tag{SO3}
\]

The quadratic `q` potential changes the derivation but no higher gate.
The space in (SO1) is invariant under `D`, and `C3` kills it. Every
higher odd gate vanishes on it in the original coordinates: both `H`
and each sector element have `p` degree at most two, whereas order at
least five requires their combined `p` differentiation order to be at
least five. This proves inclusion in the full core.

## Completeness and sharp depth when degree u is at least three

Put `m=deg u>=3` and give both `q,Q` degree one. The leading derivation
is `D0=kappa*q*partial_Q-2A*Q*partial_q`, of degree shift zero. The
leading gate `C0` has shift `m-5`; its action on a monomial `q^a Q^c`
is, up to a fixed nonzero scalar,

\[
 c(c-1)[(m-2)(c-2)-3a]q^{a+m-3}Q^{c-2}.              \tag{SO4}
\]

Distinct nonzero images have distinct exponents. The negative gate
shift for `m=3,4` is harmless: every lower input degree still produces
a strictly lower output degree, and all nonzero monomial outputs have
nonnegative exponents.

Suppose a polynomial passes the three tests and has homogeneous top
`G_N`, `N>2`. Its top must satisfy `C0 D0^r G_N=0`, `r=0,1,2`.
Equation (SO4) leaves only the monomials `q^N`, `q^(N-1)Q`, and
possibly a single resonance `q^(N-c)Q^c`, where

\[
 c=\frac{3N+2m-4}{m+1}.                              \tag{SO5}
\]

If that resonance is integral, `3<=c<=N-1`. Under `D0` its
`Q^(c+1)` monomial comes from the `-2AQ partial_q` part; its subsequent
`C0` image has `Q` exponent `c-1` and a nonzero coefficient, which
cannot be canceled by either other candidate.
The resonance coefficient therefore vanishes. The term originating in
the `Q^2` monomial of `D0(q^(N-1)Q)` next forces the coefficient of
`q^(N-1)Q` to vanish. Finally `D0^2(q^N)` has a `Q^2` monomial with
nonzero `C0` image, with bracket factor
`-3(N-2)` and derivation factor `4A^2N(N-1)`. This excludes the final
candidate. Thus every polynomial in the three-test kernel has degree
at most two in `(q,Q)`, proving (SO1).

Sharpness has the same witness even with oscillator forcing:

\[
 C_3q^3=C_3Dq^3=0,\qquad
 C_3D^2q^3=-288A^3u''\ne0.                           \tag{SO6}
\]

Indeed `D^2q^3=6q(2AQ+B)^2-6Aq^2(kappa q+epsilon)`; the additional
`q^3` term is killed by `C3`.

## Quadratic shear: four cubic derivatives are generated

For `u=bq^2+cq+d`, `b!=0`, the gate is the constant-coefficient
operator `C3=-12Ab*partial_q*partial_Q^2`. For `kappa!=0` use the affine
centering `x=q+epsilon/kappa`, `y=Q+B/(2A)`, so
`D=kappa*x*partial_y-2A*y*partial_x`.
Write `X=partial_x`, `Y=partial_y`, and start with `E0=XY^2`.
Successive right commutators `E_(r+1)=E_r D-D E_r` are

\[
\begin{aligned}
 E_0&=XY^2,\\
 E_1&=\kappa Y^3-4AX^2Y,\\
 E_2&=8A^2X^3-14A\kappa XY^2,\\
 E_3&=80A^2\kappa X^2Y-14A\kappa^2Y^3.
\end{aligned}                                                   \tag{SO7}
\]

Their coefficient matrix in `X^3,X^2Y,XY^2,Y^3` has determinant
`192A^4 kappa^2`, hence spans all constant-coefficient cubic
derivatives. If `C3D^rG=0`, `r=0..3`, then each `E_rG=0` by the
binomial commutator identity. Every third partial derivative of `G`
therefore vanishes, so `G` has degree at most two. This proves (SO2).

For every `B,epsilon`, the centered witness
`G=3kappa*x^2*y+4A*y^3` passes depths zero, one and two, but

\[
 C_3D^3G=-1728A^3b\kappa^2\ne0.                     \tag{SO8}
\]

For `B=epsilon=0`, this is `G=3kappa q^2Q+4AQ^3`.

## Exact finite dynamics

In the ordered basis `(1,q,Q,q^2,qQ,Q^2)`, columns of the following
matrix are the coefficients of the images under `D`:

\[
 M=\begin{pmatrix}
 0&-B&\epsilon&0&0&0\\
 0&0&\kappa&-2B&\epsilon&0\\
 0&-2A&0&0&-B&2\epsilon\\
 0&0&0&0&\kappa&0\\
 0&0&0&-4A&0&2\kappa\\
 0&0&0&0&-2A&0
 \end{pmatrix}.                                               \tag{SO9}
\]

Put `omega^2=2A*kappa` and define entire formal functions
`C(t)=sum_j (-omega^2)^j t^(2j)/(2j)!`,
`S(t)=sum_j (-omega^2)^j t^(2j+1)/(2j+1)!`, and
`T(t)=sum_j (-omega^2)^j t^(2j+2)/(2j+2)!`.
Thus `C'=-omega^2 S`, `S'=C`, `T'=S`, and `C+omega^2 T=1`.
The exact closed flow, uniformly including `kappa=0`, is

\[
\begin{aligned}
 q(t)&=C(t)q-S(t)(2AQ+B)-2A\epsilon T(t),\\
 Q(t)&=C(t)Q+S(t)(\kappa q+\epsilon)-\kappa B T(t).
\end{aligned}                                                   \tag{SO10}
\]

The remaining four basis flows are `1,q(t)^2,q(t)Q(t),Q(t)^2`.
When `2A*kappa>0` these are oscillator trigonometric functions; when
negative they are hyperbolic functions; when zero they reduce to the
previous polynomial shear-square flow. These are algebraic/formal
Hamiltonian identities, not claims about global operator domains or
experimental performance.

## Spectrum and minimal dynamics for nonzero oscillator strength

For `kappa!=0`, put `w=2A*kappa` and work over the algebraic closure.
The characteristic and minimal polynomials of (SO9) are exactly

\[
 \chi_M(z)=z^2(z^2+w)(z^2+4w),\qquad
 m_M(z)=z(z^2+w)(z^2+4w).                            \tag{SO11}
\]

In particular the six-dimensional sector is semisimple, with zero
eigenvalue of multiplicity two and the other eigenvalues
`r,-r,2r,-2r`, where `r^2=-w`. This is a genuine oscillatory or
hyperbolic extension of the earlier nilpotent shear-square motion.

For a direct proof, center `x=q+epsilon/kappa`, `y=Q+B/(2A)` and set
`L_+=y-r*x/(2A)`, `L_-=y+r*x/(2A)`. Then
`D L_+=r L_+`, `D L_-=-r L_-`. The basis
`1,L_+,L_-,L_+^2,L_+L_-,L_-^2` diagonalizes the action. The five
distinct eigenvalues prove the stated minimal polynomial, and the
two independent zero eigenvectors prove the multiplicity. An exact
matrix certificate independently checks (SO11), the polynomial matrix
identity `M^5+5w M^3+4w^2 M=0`, linear independence of
`I,M,...,M^4`, and `rank M=4`.

The retained exact observer compiler and independent checker also replay
the derivative-closure contracts for the original targets `q`, `q^2`,
and their joint pair, using this six-element coefficient basis. In the
checked fixtures their minimal dimensions are `2,3,5` when `epsilon=0`
and `3,5,6` otherwise. These are exact finite-model target ranks,
not a statement about noisy measurements, sensor cost, or a general
physical observation model. The contracts concern the original targets;
recentering a target can change its constant component and its closure.

## Recognition and verification

`shear_oscillator.py` recognizes this family directly from rational
coefficients of `H(q,p)`, normalizing `u(0)=0`. It extracts the constant
coefficient of `p^2`, recovers `u` from the nonconstant `p` coefficient,
and requires the remaining residual to be quadratic in `q`. The
recognizer rejects negative or fractional exponents and inexact
floating-point input before any polynomial normalization. The
quadratic-shear zero-oscillator case is returned as unrecognized here
and belongs to the retained QC route.

The checker compares both transformed operators with independent
original-coordinate differentiation, checks every protected basis gate,
verifies the sharp witnesses including centered nonzero `B,epsilon`,
and computes finite kernels while retaining every output coefficient.
It also checks the commutator span and the matrix/closed-flow formal
Taylor coefficients, characteristic/minimal polynomials, and retained
observer certificates exactly. Those finite calculations corroborate the
identities; the preceding proofs establish all polynomial degrees.
