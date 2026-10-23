# The cubic restoring boundary: a complete all-degree classification

Work over a field K of characteristic zero, with the fixed flat Weyl
structure in the original coordinates (q,p). Put

\[
P=p+q^2,\qquad H_\lambda=P^3+\lambda q^2,
\qquad D_\lambda=\{H_\lambda,\cdot\}.
\]

The dynamic core consists of polynomial observables killed by every odd
gate of order at least three after every Hamiltonian derivative. All
coordinate rewritings below refer to those original gates. They do not
replace the flat product by a new flat product in (q,P).

**Theorem CR.** If lambda is nonzero, the full polynomial dynamic core is

\[
\mathcal D_\infty(H_\lambda)=\operatorname{span}_K\{1,H_\lambda\}.
\]

The third gate alone at depths zero through three determines this space,
and depth three is necessary. At lambda zero the full core is
K[P]+Kq, and depths zero and one suffice sharply. There is no bound on
the input degree in either statement.

This note gives a cubic-specific independent derivation of the general
restoring theorem in `higher_restoring.md`. Its direct mixed-derivative
checker imports no producer arithmetic or transformed-gate implementation.
The deformation-lifting hierarchy at this boundary is treated separately
in the continuation's lifting notes. Historical priority is unestablished.

## Exact original-coordinate operators

Writing the original operators in the independent polynomial variables
(q,P) gives

\[
 D_\lambda=-3P^2\partial_q+2\lambda q\partial_P,
\]

\[
 C_3=-6\partial_q^3-36P\partial_q\partial_P^2
                 -36\partial_q\partial_P
     =-6\partial_q\bigl(\partial_q^2+6P\partial_P^2+6\partial_P\bigr),
\]

\[
 C_5=-360\partial_q\partial_P^4.
\]

All higher odd gates vanish because H has original total degree six.
For example, direct expansion of the original fifth gate is
720q partial_p^5-360 partial_q partial_p^4. Substituting
partial_q(original)=partial_q+2q partial_P cancels the two
q partial_P^5 terms, giving the displayed C5. The lambda q squared term
has no derivative of order three or higher.

## The all-degree first-depth theorem

Write S_r for the intersection of ker(C3 D_lambda^j), zero through r.
We first prove, without using C5,

\[
S_1=
\begin{cases}
K[P]+Kq,&\lambda=0,\\
\operatorname{span}_K\{1,q,P,H_\lambda\},&\lambda\ne0.
\end{cases}
\]

Let G=sum_(j=0)^N q^j g_j(P) be any polynomial satisfying C3G=C3DG=0,
with g_N nonzero. Suppose N is at least three. The coefficient of
q^(N-1) in C3G is -36N(P g_N')'. It vanishes, so g_N is constant:
integrating gives P g_N'=constant, and polynomiality forces that
constant to vanish. The next coefficient likewise makes g_(N-1)
constant. The coefficient of q^(N-3) then gives

\[
 (P g_{N-2}')'=-\frac{N(N-1)}6g_N,
 \qquad g_{N-2}'=-\frac{N(N-1)}6g_N.
\]

The second equality again follows from polynomiality after integration.
Thus DG has highest possible q power N-1, with coefficient

\[
A(P)=-3N P^2g_N+2\lambda g_{N-2}'.
\]

The coefficient of q^(N-2) in C3DG is therefore

\[
-36(N-1)(P A''+A')=432N(N-1)g_N P,
\]

which is nonzero in characteristic zero. This contradiction proves
N at most two. The coefficient comparison for C3G at N at most two
makes the q and q-squared coefficients constant. Hence

\[
G=g(P)+a q+b q^2.
\]

The remaining first-depth equation is exactly

\[
C_3D_\lambda G=-72\lambda(Pg'')'+864bP=0.
\]

For lambda zero this says b=0, with g arbitrary. For lambda nonzero,
integration and polynomiality give

\[
g''=\frac{6b}{\lambda}P,\qquad
g=\frac b\lambda P^3+cP+d.
\]

Consequently G=d+cP+aq+(b/lambda)H, proving the claimed S1 spaces.
Every equation was a coefficient identity for an arbitrary polynomial,
so this argument has no hidden degree cutoff.

## Two further derivatives close the core, sharply

For lambda nonzero, S1 is the four-dimensional space above. On its
generators,

\[
D1=DH=0,\qquad Dq=-3P^2,\qquad DP=2\lambda q.
\]

The polynomial P squared is not in S1. Thus requiring DG to lie in S1
removes the q coefficient and gives

\[
S_2=\operatorname{span}_K\{1,P,H\}.
\]

Requiring the next derivative to lie in S2 removes P, since DP is a
nonzero multiple of q. Therefore

\[
S_3=\operatorname{span}_K\{1,H\}.
\]

Constants and H are stationary and killed by every odd gate. Thus S3
is precisely the full dynamic core. The exact witnesses

\[
C_3D_\lambda^2q=432\lambda,\qquad
C_3D_\lambda^3P=864\lambda^2,
\]

show that the two eliminations are necessary. P passes all tests through
depth two, so the stopping depth three is sharp.

At lambda zero, S1=K[P]+Kq is already D-invariant and every gate kills
it: functions of P are killed by both displayed gates, and q is linear
in the original coordinates. Thus this is the full core. The witness
q squared lies in S0 and satisfies C3D0(q squared)=864P, proving sharp
depth one at zero.

## A separate finite bound using both gates

There is a useful independent calibration of the all-degree reduction.
The joint static kernel of C3 and C5 is

\[
K[P]+\operatorname{span}_K\{W_1,\ldots,W_8\},
\qquad
W_N=\sum_{j=0}^{\min(3,\lfloor(N-1)/2\rfloor)}
 \frac{(-1)^j(N)_{2j}}{6^j(j!)^2}q^{N-2j}P^j.
\]

Indeed, C5 forces every q-dependent term to have P degree at most
three. Writing that part as sum_(j=0)^3 a_j(q)P^j, C3 gives the chain

\[
a_3'''=0,\quad a_2'''+54a_3'=0,\quad
a_1'''+24a_2'=0,\quad a_0'''+6a_1'=0.
\]

Its q-dependent solutions have weighted degree at most eight for
weights (q,P)=(1,2), and the eight displayed W_N are independent
solutions with their respective highest q powers. If G=g(P)+W also
satisfies C5DG=0 and lambda is nonzero, then
C5Dg=-720 lambda g^(5), whereas C5DW has weighted degree at most two.
Hence deg g at most six, placing every such candidate in the proved
49-dimensional weighted space of degree at most twelve.

The independent exact finite replay in that space has dimensions
15,4,3,2 at depths zero through three using both gates. With C3 alone,
its dimensions are 19,4,3,2. These finite calculations are corroboration
of the all-degree argument, and the separate bound also explains why
the finite calculation can be made conclusive for both gates.

## Reproduction and boundaries

Run `python3 -B -S research/core_overlap/cubic_restoring.py`.
The optional `--output PATH` records a new receipt. The checker compares
588 original mixed-derivative gate calculations with the transformed
formulas, checks the eight static harmonics and commutator, verifies
the sharp witnesses at three nonzero rational parameters, and replays
the finite kernels with every output monomial retained. No floating
point arithmetic, optional symbolic package, or output projection is
used. This result classifies the entire stated family; it does not
classify arbitrary non-affine cubic-phase Hamiltonians.
