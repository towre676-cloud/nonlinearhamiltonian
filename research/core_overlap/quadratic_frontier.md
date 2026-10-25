# Complete constant-quadratic higher-shear classification and sharp depths

Work over a characteristic-zero field with the original flat Weyl–Moyal
product in the canonical variables `(q,p)`. Let

\[
Q=p+u(q),\qquad H=AQ^2+V(q),\qquad A\ne0,
\qquad m=\deg u\ge3,
\]

where `V` is **any polynomial**, with no degree restriction relative to
`u`. Put `D={H,·}` and `C3=T3(H,·)`.

**Theorem QF.** The full polynomial dynamic core is

\[
\boxed{\mathcal D_\infty(H)=
\begin{cases}
\operatorname{span}\{1,q,Q,q^2,qQ,Q^2\},&\deg V\le2,\\
\operatorname{span}\{1,H\},&\deg V\ge3.
\end{cases}}                                                    \tag{QF1}
\]

The maximum necessary third-gate depth is exactly

\[
\boxed{R(H)=
\begin{cases}
2,&\deg V\le2,\\
6,&\deg V=3,\\
4,&\deg V\ge4,
\end{cases}
\quad
\mathcal D_\infty(H)=\bigcap_{r=0}^{R(H)}\ker(C_3D^r).}      \tag{QF2}
\]

Each bound is sharp for **every** Hamiltonian in its stratum. In
particular, no higher odd gate is needed for this entire polynomial
family. The result includes the degree-resonant boundary `deg V=2m`;
there is no exceptional locus at that degree.

Completing the square shows that this class is exactly the polynomial
Hamiltonians `A p^2+B(q)p+C(q)` with `A` nonzero constant and
`deg B>=3`. Take `u=B/(2A)` and `V=C-B^2/(4A)`. No division by a
nonconstant polynomial or nonlinear covariance of the flat Moyal product
is assumed. Quadratic shears `deg u=2` and nonconstant coefficients of
`p^2` remain outside this theorem.

## A two-equation bound in all momentum degrees

In the original canonical coordinates,

\[
C_3=H_{qqq}\partial_p^3-3H_{qqp}\partial_q\partial_p^2,
\quad H_{qqp}=2Au'',
\quad H_{qqq}=2Au'''p+\bigl(Au^2+V\bigr)'''.              \tag{QF3}
\]

Suppose `G` has top momentum term `g(q)p^N`, with `N>=3` and
`g!=0`. The coefficient of `p^(N-2)` in `C3G` is

\[
2A(N)_2\bigl((N-2)u'''g-3u''g'\bigr).                    \tag{QF4}
\]

All omitted terms have strictly smaller momentum degree: the constant
part of `H_qqq` lowers it by three, and lower momentum terms of `G`
cannot contribute to this coefficient. If `a=deg g`, vanishing implies

\[
3a=(N-2)(m-2)>0.                                         \tag{QF5}
\]

Thus `a>=1`, so `DG` has nonzero leading term
`-2Ag'(q)p^(N+1)`. Applying (QF4) to this leading term, the condition
`C3DG=0` would imply

\[
3(a-1)=(N-1)(m-2).                                       \tag{QF6}
\]

Subtracting (QF5) from (QF6) gives `-3=m-2`, contradicting `m>=3`.
This proves that the common kernel of `C3` and `C3D` has momentum
degree at most two, in **all** polynomial degrees, independently of
`V`. For momentum degree two, (QF4) specializes to `-12Au''g'`,
so the coefficient of `p^2` must be constant. This proof uses polynomial
leading degrees, not any finite numerical cutoff.

## The exact six-dimensional depth-two space

In the independent polynomial variables `(q,Q)`, the exact operators are

\[
D=-2AQ\partial_q+V'\partial_Q,
\qquad
C_3=(2AQ u'''+V''')\partial_Q^3
             -6Au''\partial_q\partial_Q^2.                \tag{QF7}
\]

Take an element passing depths zero, one, and two. By the preceding
argument, write

\[
G=cQ^2+b(q)Q+f(q),\qquad c\in K.
\]

The coefficient of `Q^2` in `DG` is `-2Ab'`. Since `DG` has
momentum degree at most two, its third gate is simply `-12Au''`
times the derivative of that coefficient. The condition `C3DG=0`
therefore gives `b''=0`, so `b=alpha q+beta`.

The coefficient of `Q` in `DG` is `-2Af'+2cV'`. Applying `C3` to
`D^2G` consequently gives the final condition

\[
f'''=(c/A)V'''.
\]

Integrating within the polynomial ring proves the inclusion in

\[
S_H=\operatorname{span}\{1,H,q,Q,q^2,qQ\}.                \tag{QF8}
\]

Conversely, direct use of (QF7) shows every displayed basis vector passes
the first three tests. For example the two derivatives of `qQ` have
momentum degrees two and one, respectively, with constant quadratic
coefficient at the first step; `H` is stationary. The six basis vectors
are independent because only `H` has a nonzero `Q^2` term. Thus

\[
\boxed{\ker C_3\cap\ker(C_3D)\cap\ker(C_3D^2)=S_H.}        \tag{QF9}
\]

For any `R>=2`, the space passing depths zero through `R` is exactly

\[
S_H\cap D^{-1}S_H\cap\cdots\cap D^{-(R-2)}S_H,            \tag{QF10}
\]

because membership of `D^jG` in `S_H` is precisely the block of
three gate tests at depths `j,j+1,j+2`.

## Nonlinear residual potentials force collapse

Write an arbitrary element of `S_H` as a Hamiltonian multiple and a
constant plus

\[
G=(\alpha q+\beta)Q+a q^2+bq.
\]

Its derivative, modulo the already included Hamiltonian multiple, is

\[
DG=-2\alpha H-2A(2aq+b)Q+
 \bigl(2\alpha V+(\alpha q+\beta)V'\bigr).                 \tag{QF11}
\]

It belongs to `S_H` exactly when the last parenthesis is quadratic in
`q`. If `n=deg V>=3`, its leading coefficient is
`alpha(n+2)V_n`, so `alpha=0`.

If `n>=4`, the remaining degree `n-1` coefficient is `beta nV_n`,
so `beta=0`. After one preimage step only `1,H,q,q^2` remain. Their
derivatives have `qQ,Q` coefficients `-4Aa,-2Ab`; the next preimage
step forces `a=b=0`. Equation (QF10) therefore gives depth four.

If `n=3`, one preimage step forces `alpha=0`. The next forces `a=0`,
since the `qQ` coefficient of (QF11) is `-4Aa`. The third forces
`beta=0`, since the `q^2` coefficient of (QF11) is `3 beta V_3`.
The fourth forces `b=0`, since its `Q` coefficient is `-2Ab`.
The successive dimensions are `6,5,4,3,2`; (QF10) gives depth six.
In either case only `1,H` remain. They always belong to the full core.

If `deg V<=2`, `S_H` is the quadratic polynomial sector in `(q,Q)`
and is invariant under `D`. It is killed by every odd gate: the third
by (QF7), all orders at least five because both `H` and every member
have original momentum degree at most two. Thus depth two already gives
the full six-dimensional core. This proves (QF1) and sufficiency in
(QF2).

## Sharp witnesses and exact failure formulas

For `deg V<=2`, the cubic `q^3` passes depths zero and one but

\[
C_3D^2q^3=-288A^3u''\ne0.                                \tag{QF12}
\]

For every potential, `q` passes depths zero through three and

\[
C_3D^4q=96A^4u''V''''.                                   \tag{QF13}
\]

This is nonzero exactly when `deg V>=4`, proving sharp depth four.
For cubic potentials, `q` passes depths zero through five and

\[
C_3D^6q=-960A^5u''(V''')^2\ne0.                           \tag{QF14}
\]

Thus depth six is necessary for every cubic residual potential, even
though the full core has dimension only two. These identities are in the
original flat Moyal structure; the transformed variables merely shorten
the polynomial calculation.

## Exact decision and independently replayable certificates

The closed classification already decides every input in scope. The code
also computes and certifies the answer by rational linear algebra inside
the proved six-dimensional upper space `S_H`. Start with that space
(which passes depths zero through two by QF9) and iterate

\[
K_{j+1}=\{G\in K_j:DG\in K_j\}.                            \tag{QF15}
\]

Every polynomial output is retained, including all terms outside `S_H`.
A strict step decreases dimension. At equality the space is `D` invariant
and killed by all gates, hence contained in the dynamic core. Conversely,
(QF9) places the full core in `S_H`, and invariance places it in every
stage. Thus the stabilized space equals the all-degree core.

The certificate records each stage basis, the original Hamiltonian,
recovered completion of square, final basis, exact derivation closure
matrix, and sharp depth. The checker independently recovers the initial
six-dimensional space, checks its three gate tests, and replays the rank
of `[D K_j | -K_j]` at every descent. Its nullity is the entire preimage
dimension. Membership and derivative membership are verified by augmented
ranks; the final closure identities certify the lower inclusion. The
checker uses the separate PBW engine and its own fraction elimination,
not the producer's Gaussian elimination. The universal upper bound rests
on (QF4)–(QF9), never numerical stabilization.
