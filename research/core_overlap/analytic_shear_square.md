# The exact six-dimensional core of a squared shear coordinate

Let `u in K[q]` have degree at least three, with `K` a field of
characteristic zero, and put `Q=p+u(q)`. Use the original flat Moyal
product in `(q,p)` and the convention `{H,G}=H_q G_p-H_p G_q`.

**Theorem SS.** For any quadratic polynomial

\[
H=AQ^2+BQ+C+\varepsilon q,\qquad A\ne0,
\]

the full polynomial dynamic core is exactly

\[
\boxed{\mathcal D_\infty(H)
 =\operatorname{span}_K\{1,q,Q,q^2,qQ,Q^2\}.}             \tag{SS1}
\]

It therefore has dimension six in all degrees. These pure-top
Hamiltonians are outside the conjectured two-dimensional collapse.
Their positive structure is an elementary polynomial canonical shear,
but covariance of the flat Moyal product under arbitrary nonlinear
canonical maps is not assumed in the proof.

**Proof.** Polynomial substitution identifies `K[q,p]` with `K[q,Q]`.
The Hamiltonian derivation and the third gate, expressed in this
polynomial coordinate ring, are exactly

\[
D=-(2AQ+B)\partial_q+\varepsilon\partial_Q,\qquad
C_3=(2AQ+B)u'''(q)\partial_Q^3
               -6Au''(q)\partial_q\partial_Q^2.           \tag{SS2}
\]

For clarity, the derivatives in (SS2) keep `Q` fixed. To check the gate,
use `H_qqq=(2AQ+B)u'''+6Au'u''`, `H_qqp=2Au''`, and
`H_qpp=H_ppp=0`, and then
`partial_q(old)=partial_q(new)+u' partial_Q`. The terms involving
`u'u''` cancel exactly.

Let `V` be the polynomials of total degree at most two in `(q,Q)`.
Equation (SS2) kills `V`, and `D` preserves `V`. Every element of `V`
has degree at most two in the original variable `p`, as does `H`, so
all odd transvectants of order at least five vanish. Thus
`V subset D_infty(H)`.

Suppose a core element `G` lies outside `V`, and let `G_N` be its
highest component in total degree, with `N>=3`. Write `m=deg u>=3` and
let `u_m` be the leading monomial of `u`. The top parts of the
operators for this total-degree filtration are

\[
D_0=-2AQ\partial_q,\qquad
C_0=2AQ u_m'''\partial_Q^3-6Au_m''\partial_q\partial_Q^2.
\]

The weighted shifts are zero for `D_0` and `m-5` for `C_0`. The other
terms have strictly smaller shifts; this includes the `B` term of
`C3`. Hence `C3 D^rG=0` implies `C_0 D_0^rG_N=0` for every `r>=0`.
Let `a` be the largest `q` exponent occurring in `G_N`. By homogeneity,

\[
D_0^aG_N=c_0Q^N,\qquad c_0\ne0.
\]

But then

\[
C_0D_0^aG_N=2A c_0(N)_3u_m'''Q^{N-2}\ne0,
\]

because `N>=3`, `A c_0!=0`, and `u_m'''!=0` in characteristic zero.
This contradiction proves (SS1), including the constant-force term
`epsilon q`. The argument gives a finite failure witness for every
proposed polynomial outside the core, not a finite-degree extrapolation.

**Sharp uniform stopping rule.** In fact,

\[
\boxed{\mathcal D_\infty(H)
 =\ker C_3\cap\ker(C_3D)\cap\ker(C_3D^2).}               \tag{SS3}
\]

To prove the uniform depth bound, write `u_m=alpha q^m`. The top
operator `C_0D_0^r` sends `q^aQ^c` to a single monomial, with
coefficient

\[
2A\alpha m(m-1)(-2A)^r(a)_r(c+r)_2
 \big[(m-2)(c+r-2)-3(a-r)\big].                          \tag{SS4}
\]

For fixed `r` the output shift is independent of `(a,c)`, so distinct
input monomials cannot cancel. Every monomial with `a+c>=3` fails one
of the checks `r=0,1,2`. If `c>=2` and the `r=0` bracket is zero,
then `a>=1` and the `r=1` bracket is `m+1`, nonzero. If `c=1`, then
`a>=2` and `r=1` gives `-3(a-1)`, nonzero. If `c=0`, then `a>=3`
and `r=2` gives `-3(a-2)`, nonzero. All the relevant falling factorials
are nonzero. Thus the joint top kernel has total degree at most two.
The same total-degree filtration used in the proof lifts this bound to
the actual operators, proving (SS3).

Two bracket steps are necessary for this gate: the cubic `q^3` satisfies

\[
C_3q^3=C_3Dq^3=0,\qquad
C_3D^2q^3=-288A^3u''\ne0.                               \tag{SS5}
\]

So discarding the last condition in (SS3) gives a strictly larger
space. The theorem settles both the all-degree core and the exact
uniform bracket depth for detecting it using `T3`.

## Recognition in the original coordinates

Suppose a supplied rational Hamiltonian has degree two in `p`, its
`p^2` coefficient is a nonzero constant `A`, and its `p` coefficient is
`b(q)`. Set

\[
B=b(0),\qquad u(q)=\frac{b(q)-B}{2A},\qquad Q=p+u(q).
\]

If `deg u>=3` and `H-AQ^2-BQ` is affine in `q`, Theorem SS applies. This
test uses exact coefficient arithmetic. It rejects a nonconstant
quadratic coefficient and rejects residual terms of degree at least two
scope. The canonical shear may subsequently be composed with affine
symplectic substitutions, under which the original flat Moyal
structure is covariant.

The qualification `deg u>=3` matters: when `u'''=0`, the last
contradiction does not apply. For instance if `deg u=2`, all
polynomials in `Q` pass every gate and remain in that space under `D`,
giving an infinite core. Such an input must not be assigned a
six-dimensional bound by this theorem.

`analytic_shear_square.py` supplies the exact recognizer and a direct
transvectant checker. It verifies the transformed gate on monomials,
all six basis elements under every nonzero odd correction, invariance
under `D`, and finite-box dimensions with full output retained. The
proof above establishes the all-degree result.

No literature-priority claim is made. The result is a scoped
classification for the fixed original affine Moyal product and an
explicit correction to the pure-top collapse conjecture.
