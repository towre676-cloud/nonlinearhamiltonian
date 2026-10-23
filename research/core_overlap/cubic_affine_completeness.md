# Completing cubic-phase cores with nonlinear affine coefficient

Use one canonical pair, the original flat Weyl product, the bracket
`{H,G}=H_q G_p-H_p G_q`, and a characteristic-zero field K. Set
`P=p+w(q)`, `Q=q`, with `deg w=2` and `c=w''/2 !=0`.
The substitution is used to express the original operators, not to
assert invariance of the flat product under nonlinear coordinate changes.
Write `H=tilde h`, where `h=a(P)+Q b(P)`, and let `D={H,.}`.
All observables below are polynomials of arbitrary degree.
Historical priority and external peer review remain unestablished.

## The all-degree containment theorem

**Theorem AC.** Suppose `m=deg b>=2`, with no degree restriction on a.
Every element of the full dynamic core is affine in Q:

`D_infinity(H) subset tau*(K[P]+Q K[P])`.

In fact the third gate alone, through depths zero and one when m>=3,
and through depths zero, one and two when m=2, excludes every observable
whose Q degree is at least two. This is a bound on Q degree, not a claim
that those depths already identify the full core.

### The exact operators

In `(Q,P)` coordinates the original derivation is

`D=b partial_P-(a'+Q b') partial_Q`.

Expanding the third coefficient in the triangular transvectant formula gives

`C3 = 6c[b' partial_P^3+b'' partial_P^2
 -(a''+Q b'') partial_Q partial_P^2
 -(a'''+Q b''') partial_Q partial_P]
 +3b'' partial_Q^2 partial_P-(a'''+Q b''') partial_Q^3`.

Both operators preserve the increasing filtration by Q degree. If
`G=Q^N f(P)+lower Q powers`, its top Q coefficients under D and C3 are
respectively `L_N f` and `6c M_N f`, where

`L_N=b partial_P-N b'`,

`M_N=b' partial_P^3+(1-N)b'' partial_P^2-N b''' partial_P`.

Consequently the coefficient of Q^N in `C3 D^r G` is exactly
`6c M_N L_N^r f`. Lower Q components of G cannot cancel it.
This absence of cancellation is the essential all-degree step.

### Leading-degree obstruction

Let the leading coefficient of b be B, and let f have degree n with
nonzero leading coefficient F. For n>0 the potential leading coefficient
of `M_N f`, at P degree `n+m-4`, is

`B F m n (n+m-3)(n-1-N(m-1))`.                 (AC1)

Indeed the bracket before factoring is
`(n-1)(n-2)+(1-N)(m-1)(n-1)-N(m-1)(m-2)`, which equals
`(n+m-3)(n-1-N(m-1))`.
The factorization is a polynomial identity, not a sampled assertion.

Suppose N>=2. If m>=3, the equation `M_N f=0` allows only
`n=0` or `n=1+N(m-1)`. In the first case `L_N f` has degree m-1
and nonzero leading coefficient `-N m B F`. That degree is neither
allowed degree for a kernel element of M_N. In the second case
`L_N f` has degree `n+m-1`, with leading coefficient
`B F(n-Nm)=B F(1-N) !=0`, again neither allowed degree.
Thus `M_N f=M_N L_N f=0` is impossible.

If m=2, the allowed degrees are `n=0,1,N+1`, since (AC1) becomes
`2 B F n(n-1)(n-1-N)`. Degree one is sent by L_N to degree two,
with nonzero coefficient `B F(1-2N)`; degree N+1 is sent to
N+2 with nonzero coefficient `B F(1-N)`. Both new degrees are
forbidden. Degree zero is sent first to degree one and then to degree
two, with nonzero leading coefficients. Thus
`M_N f=M_N L_N f=M_N L_N^2 f=0` is impossible.
This proves Theorem AC in every polynomial degree.

## Full classification when deg b>=3

**Theorem AC-high.** If deg b>=3, for every polynomial a,

`D_infinity(H)=span{1,H}`.

By AC it suffices to write `g=alpha+Q beta`. The top-Q third-gate
equation for N=1 and the same leading-factor argument imply
`beta=lambda b+nu`: subtract the leading multiple of b, which itself
solves `M_1 b=0`, and no nonconstant lower degree is permitted.
Subtract lambda h. The remaining observable is `alpha+nu Q`.
Its static third-gate equation is `(b' alpha'')'=0`; since b' is
nonconstant, alpha is linear. Write the remainder as `sP+t+nu Q`.
The Q coefficient of its bracket is `-nu b'`. For that bracket also
to be a core element this coefficient must be a multiple of b plus a
constant; degree comparison forces nu=0. Finally `D(sP+t)=s b`,
and `(b'b'')'` is nonzero for deg b>=3, so its third gate forces s=0.
Conversely 1 and H are always stationary core elements.

## Full classification when b is quadratic

Write `b=mu P^2+b1 P+b0`, `mu!=0`.

**Theorem AC-quadratic.** For every polynomial a, exactly one of the
following cases occurs.

* If `deg a<=2` (including the zero polynomial), put
  `lambda=a2/mu`, `X=Q+lambda`, and
  `a-lambda b=lP+k`. The full core is
  `span{1,X,XP,H}`, of dimension four.
* If `deg a=4`, set
  `A=a4`, `r=(b1/mu-a3/A)/2`, `r'=-b1/mu-r`.
  If `b(r)=0`, put `c2=a2-3A r(r+r')` and
  `G=A(P-r)^3+c2(P-r)+mu Q(P-r)`.
  The full core is `span{1,G,H}`, of dimension three.
* In every other case the full core is `span{1,H}`.

The middle case is exactly K4. Its recognition needs no algebraic-root
search: r is fixed by the rational coefficient formula, and `b(r)=0`
is one exact identity test. These statements hold over every
characteristic-zero coefficient field, without assuming b splits.

### Proof without bounded symbolic casework

Theorem AC bounds all core elements to `g=alpha+Q beta`. Its static
third-gate equation has Q coefficient `b' beta'''`, so beta has degree
at most two. Its remaining third-gate equation is

`(b' alpha''-beta' a'')'=0`.                    (AC2)

The projection of the core onto beta is an `ad_b`-invariant subspace
`B subset span{1,P,P^2}`, and contains b. Its kernel is exactly the
constant observables: beta=0 in (AC2) forces alpha linear, while the
third gate of `D(alpha)=alpha' b` forces its slope to vanish.

First suppose deg a>=3. The projection B cannot be all of sl2.
Otherwise a core element with beta=1 exists. Equation (AC2) makes its
density alpha linear. Applying (AC2) to its first bracket gives

`b'(alpha1 b''-a''')+b'' a'' in K`.            (AC3)

Center P at the root of b'. In the polynomial equation (AC3), the
coefficient multiplying the linear term of a'' cancels, whereas any
degree at least two in a'' survives. Therefore (AC3) forces
`deg a<=3` and `alpha1=0`. In the remaining cubic case the observable
is Q modulo a constant. For `D^2 Q`, the expression on the left of
(AC2) before its outer derivative is exactly `-(b')^2 a'''`.
Its derivative is nonzero, a contradiction. Thus dim B<=2.

If dim B=1, the kernel statement gives exactly span{1,H}. If dim B=2,
subtract a multiple of h from an independent observable to make its
beta linear. It cannot be constant: its adjoint bracket with b would
then produce the independent nonconstant linear polynomial b'.
Scale it to `beta=mu(P-r)` for some r in K. Adjoint invariance forces
`b(r)=0`: explicitly, adding mu b to `b beta'-b' beta` leaves
`mu[(b1+2mu r)P+2b0+b1 r]`, which is a multiple of beta precisely
when b(r)=0. Let `r'=-b1/mu-r`, `x=P-r`, and `delta=r'-r`.
The bracket closure, modulo the constant kernel, is then

`Dg=-mu H-mu delta g+constant`.                (AC4)

Its density equation, differentiated once and divided by the common
polynomial factor x, gives

`a''=2alpha'+(x-delta)alpha''`.

Together with (AC2) this becomes `x alpha''-2alpha' in K`.
For a polynomial alpha, the coefficient of x^(j-1) in that expression
is `j(j-3)alpha_j`. Consequently
`alpha=A x^3+C x+D`; integrating the displayed formula for a'' gives

`a=A x^3(x-delta)+C x^2+c1 x+c0`.

Since deg a>=3, A is nonzero. This is precisely K4 and in particular
forces deg a=4. No finite-degree computation is used to exclude any
other degree. Matching the cubic coefficients fixes r by the formula
in the theorem, and matching degree two gives C=c2.

For sufficiency, beta and b are quadratic-or-lower. The K4 density
satisfies `b'alpha''-beta'a''=-2mu c2`, a constant. Under
`S_s=exp(s partial_P^3)`, h changes only by a linear polynomial in P
and g only by a constant. Therefore the third-derivative compatibility
defect stays zero for every s, proving every odd gate vanishes by the
cubic-phase gauge identity. Equation (AC4) proves closure. Independence
of 1,G,H follows from their independent Q coefficients beta,b.

Finally suppose deg a<=2. Shift to X as in the theorem, so the density
is lP+k. Static exactness forces beta quadratic-or-lower and alpha
linear in these coordinates. The next third-gate condition is the
single linear restriction

`mu alpha1=l beta2`.

It leaves exactly the four-dimensional space `span{1,X,XP,H}`.
It is invariant, with

`DX=-2mu XP-b1 X-l`,

`D(XP)=-H+k+b1 XP+2b0 X`, and `DH=0`.

All higher gates kill X because it is linear. They kill XP because
its original-coordinate degree is at most three and its third gate
vanishes; H has only its own trivial odd antisymmetric gates. This
proves sufficiency and completes the classification.

## Uniform finite stopping rules

The full classification above can be decided by the third gate at finite
Hamiltonian depth, with no input-degree bound:

`D_infinity(H)=intersection_(r=0)^R ker(C3 D^r)`,

where `R=1` for deg b>=3 and `R=2` for deg b=2.

For deg b>=3, AC already forces an element of the depth-one kernel to
be affine in Q. The static affine kernel is exactly
`span{1,H,P,Q}` by the proof of AC-high. The first bracket test removes
Q from its Q coefficient and then removes P from its density. Thus R=1.
It is sharp for every such Hamiltonian: P itself passes the static gate,
but `C3 DP=6c(b'b'')' !=0`.

For quadratic b, write S_r for the intersection of the third-gate kernels
through depth r restricted to V. The static space S_0 has dimension five.
Indeed beta is any quadratic polynomial, and if rho is the root of b',
then

`alpha''=(beta'a''-beta'(rho)a''(rho))/b'`,

with alpha_0 and alpha_1 arbitrary. The numerator is divisible by b'.
The kernel of the beta projection on S_1 consists only of constants,
because `C3 D(P)=6c(b'')^2 !=0`.

When deg a>=3, dim S_1 is at most three. Otherwise its beta projection
would be all of sl2. A beta=1 element of S_1 forces deg a<=3 and zero
slope of alpha, as in (AC3). For cubic a, a beta=P element of S_1 has
static density with leading term `3a3 P^2/(2mu)`. In its first bracket
the possible cubic density term cancels. Its third gate nevertheless
has leading term `144c mu a3 P`, which is nonzero. Thus that beta cannot
occur in S_1, a contradiction. Since S_1 has dimension at most three
and contains the two independent stationary elements 1,H, either
S_2=S_1 and the space is already invariant under D, or S_2 has dimension
two and equals span{1,H}. Equality at one stage in the descending chain
implies invariance and stabilization. Hence S_2 is the maximal
C3-killed invariant space, which the classification above proves is
the full core. When deg a<=2, the explicit four-dimensional space is
already S_1 and is invariant.

Finally AC forces every whole-polynomial depth-two candidate to be in
V, so the restricted argument proves the asserted full stopping rule.
The uniform bound two cannot be reduced: for `a=0`, `b=P^2`, the
observable `G=Q^2+2P/c` passes C3 and C3D but fails C3D^2; the latter
has Q^2 coefficient `-288c`. No sharpness claim is made separately for
every quadratic-b parameter value.

## Exact checks and scope

`cubic_affine_completeness.py` verifies the polynomial factor identity,
the transformed operators against original-coordinate mixed derivatives,
the highest-Q extraction, the obstruction degrees, exact K4 recognition,
and the four-dimensional low-density branch with original-coordinate
gates and brackets. It also rejects forged theorem-application data.
The all-degree conclusions rest on the written arguments above; finite
checks are independent calibration, not a completeness inference.
The linear-b branch is treated separately in `cubic_phase_audit.md`.
