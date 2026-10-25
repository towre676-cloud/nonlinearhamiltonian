# Independent review of the structural extensions

This review concerns the new polynomial shear, oscillator, analytic-potential,
quadratic-frontier and deformation results developed after the first overlap
package. The review checks the all-degree arguments separately from their
finite calibrations. All polynomial statements are in characteristic zero and
retain the original flat Weyl–Moyal product in the original affine coordinates.
The analytic statements concern finite degree in `q` with real-analytic
coefficients on a connected positive interval. Historical priority and external
peer review are not established.

## Shear-composition closure

For `Q=p+u(q)`, `m=deg u>=3`, `H=P(Q)+epsilon*q`, and `mu=deg P>=3`,
the ordinary chain rule gives the transformed third gate

\[
 C_3=u'''(P'\partial_Q^3-P'''\partial_Q)
 -3u''(P''\partial_q\partial_Q^2+P'''\partial_q\partial_Q)
 -P'''\partial_q^3.
\]

The derivatives on the right keep `Q` fixed. This is an operator identity for
the original affine gate, not an assertion that nonlinear substitution
preserves the flat Moyal product. Under total degree in `(q,Q)`, the first
two groups have top shift `m+mu-7`; the last has shift `mu-6`, lower by
`m-1>0`. Lower terms of `P,u` have smaller shifts. The top derivation is
`D0=-mu*p_mu*Q^(mu-1)*partial_q`, of shift `mu-2`.

The top gate sends each monomial `q^a Q^c` to one monomial, with coefficient
proportional to

\[
 c(c+\mu-3)R(a,c),\qquad
 R(a,c)=(m-2)(c-\mu)-3(\mu-1)a.
\]

The nonzero output shift is independent of the input exponents, so distinct
inputs cannot cancel. For `a,c>0`, the second test replaces `R` by
`R+(mu-1)(m+1)`, and these cannot both be zero. For `c=0,a>=1`, its
second-test bracket is `-(m-2)-3(mu-1)(a-1)<0`. For `a=0,c>0`, the
first test leaves only `c=mu`. Consequently the simultaneous top kernel
contains only `1,Q^mu`. Subtract a leading multiple of `H`, which itself
passes both tests, and descend in total degree. This proves the claimed
all-degree equality with `span{1,H}`. Negative operator shifts at small
`m,mu` cause no exception: every nonzero actual output has nonnegative
monomial exponents.

The two tests are uniformly indispensable in this family. `Q` fails `C3`
but has `DQ=epsilon`, hence passes `C3D`. Conversely `q` passes `C3`,
while `C3Dq=u'''(P'''P''-P'P'''')` is nonzero: its leading coefficient in
`Q` is `2*p_mu^2*mu^2*(mu-1)*(mu-2)`. These arguments do not depend on a
finite parameter sample.

## Oscillator maximality and the two depth bounds

For

\[
 H=AQ^2+BQ+C+\frac\kappa2q^2+\epsilon q,
\]

with `A!=0`, the transformed operators are

\[
 D=-(2AQ+B)\partial_q+(\kappa q+\epsilon)\partial_Q,
 \qquad C_3=(2AQ+B)u'''\partial_Q^3
                  -6Au''\partial_q\partial_Q^2.
\]

The degree-at-most-two space in `(q,Q)` is invariant under `D` and killed
by every gate: for orders at least five, the total available `p` degree
of `H` and an element of the space is at most four. This proves the
six-dimensional lower bound directly in the original convention.

For `m>=3`, let `u_m=alpha*q^m` and use total degree in `(q,Q)`.
The top gate on `q^aQ^c` is proportional to

\[
 c(c-1)[(m-2)(c-2)-3a],
\]

with fixed exponent shift. In homogeneous degree `N>=3`, its kernel
contains `q^N`, `q^(N-1)Q`, and at most one resonance with `c>=3,a>=1`.
The top derivation is `D0=-2AQ partial_q+kappa*q partial_Q`. The resonance's
`-2AQ partial_q` contribution has the unique highest `Q` exponent in
`C0D0` of any remaining candidate, so it cannot cancel. Its coefficient
is nonzero because the resonance bracket changes by `m+1`. Remove it.
Then `C0D0` removes `q^(N-1)Q`; finally `C0D0^2` removes `q^N`.
This proves depth two suffices, even when `kappa!=0`; one cannot simply
reuse the original SS proof with its monomial derivation without this
extra no-cancellation argument. The cubic `q^3` proves sharpness for
all these parameters:

\[
 C_3q^3=C_3Dq^3=0,\qquad C_3D^2q^3=-288A^3u''\ne0.
\]

For quadratic `u=bq^2+cq+d`, `b!=0`, and `kappa!=0`, the gate is the
constant-coefficient operator `-12Ab partial_q partial_Q^2`. In homogeneous
degree `N>=3`, its kernel has the three monomials `q^N,q^(N-1)Q,Q^N`.
At `N>=4`, `C3D0` maps the latter two to distinct monomials and removes
them; `C3D0^2` removes the first. At `N=3` there is a resonance requiring
one further step. Lower affine terms `B,epsilon` have smaller shifts,
so the same leading argument proves the degree bound for arbitrary
`B,epsilon`, rather than only for a centered sample.

For `B=epsilon=0`, the explicit witness

\[
 G=Q^3+\frac{3\kappa}{4A}q^2Q
\]

passes the first three depth tests and has

\[
 C_3D^3G=-432A^2b\kappa^2\ne0.
\]

Equivalently multiply by `4A` to obtain the advertised
`-1728A^3b*kappa^2`. This proves the depth-three bound is sharp across
the quadratic-shear oscillator class. The unforced case `kappa=0` must
remain on its retained infinite-core QC route; it cannot be assigned
six dimensions. Affine shears are quadratic Hamiltonians and likewise
lie outside this nonlinear oscillator theorem.

The closed equations `Dq=-(2AQ+B)`, `DQ=kappa*q+epsilon` give
`D^2q=-2A*kappa*q-2A*epsilon`. Oscillatory terminology is justified for
real parameters only when `2A*kappa>0`. Exact sector closure itself
is algebraic and does not require a sign, analytic convergence, or a
self-adjoint realization of a quantum operator.

The spectral extension is also consistent with the exact quadratic-sector
representation. For `kappa!=0`, set `omega^2=2A*kappa`; affine centering
removes `B,epsilon`. Over an algebraic closure choose `r^2=-omega^2`.
The linear forms `Lplus=y-r*x/(2A)` and `Lminus=y+r*x/(2A)` have
derivation eigenvalues `r,-r`. Their quadratic products give eigenvalues
`2r,0,-2r`, while the constant has eigenvalue zero. Thus the
characteristic polynomial is `z^2(z^2+omega^2)(z^2+4omega^2)` and the
minimal polynomial is `z(z^2+omega^2)(z^2+4omega^2)`. This conclusion
uses `A*kappa!=0`; the nilpotent zero-oscillator case has its retained
separate Jordan description. Observer certificates establish only their
explicit finite models and target contracts.

## Analytic exceptional potentials

Let `F''` be nowhere zero, `r^3=F''`, and
`FF'''/(3F'')-3F'=lambda` constant. Modulo the invariant strip
`W=A+qA`, an extra cubic can be normalized as `q^3r+q^2h`.
Direct third-gate and derivation expansions yield exactly

\[
 h'=\frac{V'''r}{F''},\qquad
 Fh'-(2F'+\lambda)h=3V'r.
\]

The second condition says that `DG-lambda*G` is in `W`; together they
are sufficient for every future gate test. Necessity uses the retained
analytic finite-determination theorem: any additional element has degree
three, its cubic coefficient is unique up to scalar, and a degree-two
residual cannot persist. This is a regular-chart criterion, not a
claim of global classification for arbitrary `F` through zeros of its
second derivative or singularities.

For `F=p^(-1/4)`, normalize the cubic coefficient to `p^(-3/4)`.
Eliminating `h` gives

\[
 p^4V''''+3p^3V'''-\frac{15}{16}p^2V''
                    -\frac{15}{32}pV'=0.
\]

The logarithmic variable `x=log p` turns this into a constant-coefficient
fourth-order ODE. Its distinct indicial roots are
`0,-1/4,3/4,5/2`, so all real-analytic solutions on any connected
positive interval are precisely

\[
 V=c_0+a p^{-1/4}+b p^{3/4}+c p^{5/2}.
\]

This proves completeness in the analytic function space, not merely
among tested power ansatzes. For these potentials the proposed cubic
representative has the same `q^3,q^2` coefficients as `(H-c0)^3`;
their difference is in `W`. Thus the additional generator can be taken
stationary. The harmless constant in the Hamiltonian must be removed
before cubing: `H^3-(H-c0)^3` generally contains a forbidden `q^2` term.
If `V` fails the ODE, the compatibility system has no extra generator,
so the retained quotient bound proves the full core is exactly `W`.

## Complete constant-quadratic-momentum classification

For constant nonzero `A`, write `H=A(p+u(q))^2+V(q)`, with
`m=deg u>=3` and now **arbitrary polynomial** `V`. The initial
weighted-top argument gives a finite bound when `deg V<2m`, but the
following direct leading-transverse-degree argument removes that
restriction completely, including the former degree-resonant boundary.

In `(q,Q)`, the exact third gate is

\[
 C_3=(2AQ u'''+V''')\partial_Q^3
                       -6Au''\partial_q\partial_Q^2.
\]

If a polynomial `G` in `ker C3 intersect ker(C3D)` has highest
`Q` degree `N>=3` and coefficient `g(q)` of degree `a`, the leading
`Q^(N-2)` coefficient in its third gate is

\[
2A(N)_2\big((N-2)u'''g-3u''g'\big).
\]

The `V'''` term lowers `Q` degree by three and cannot affect it.
Comparing leading `q` coefficients gives `3a=(N-2)(m-2)>0`, so
`g'` is nonzero. The highest `Q` coefficient of `DG` is then
`-2Ag' Q^(N+1)`. Applying its third-gate condition gives
`3(a-1)=(N-1)(m-2)`. Subtracting the two identities forces
`-3=m-2`, impossible for `m>=3`. Thus `G` has `Q` degree at most
two. At degree two the leading gate is `-12Au''g'`, which forces
its quadratic coefficient to be constant.

The next two finite tests give the remaining coefficient constraints.
For `G=cQ^2+b(q)Q+f(q)`,

\[
 C_3DG=24A^2u''b'',\qquad
 C_3D^2G=48A^2u''(cV'''-Af''')\quad\text{when }b''=0.
\]

Consequently every polynomial passing depths zero through two lies in
`span{1,H,q,Q,q^2,qQ}`. This is an all-degree candidate theorem,
not a bound inferred from a finite matrix.

Modulo a Hamiltonian multiple and constant, write
`G=(alpha*q+beta)Q+a*q^2+b*q`. Its derivative, after subtracting
`-2alpha H`, has pure-`q` part

\[
R=2\alpha V+(\alpha q+\beta)V'.
\]

Passing the next depth forces `R` to have degree at most two. If
`n=deg V>=4`, its highest two coefficients force `alpha=beta=0`.
One further depth forces `a=b=0`. If `n=3`, successive depths first
force `alpha=0`, then `a=0`, then `beta=0`, and finally `b=0`.
The nesting fact used here is exact: if `G` passes depths zero through
`R`, then `DG` passes depths zero through `R-1`. Thus the complete
constant-quadratic-momentum classification is six dimensions for
`deg V<=2`, and exactly `span{1,H}` otherwise. The sharp uniform
third-gate depths are respectively `2`, `6` for cubic `V`, and `4`
for `deg V>=4`.

These depths have universal witnesses. For quadratic or lower `V`,
`q^3` has `C3D^2q^3=-288A^3u''` and passes the previous depths.
For degree at least four, `q` passes depths zero through three, but

\[
 C_3D^4q=96A^4u''V''''\ne0.
\]

For cubic `V`, writing `w=V'''!=0`, the same `q` passes depths zero
through five, while

\[
 C_3D^6q=-960A^5u''w^2\ne0.
\]

The first four derivatives of `q` are
`-2AQ`, `-2AV'`, `4A^2QV''`, and
`4A^2(V'V''-2AQ^2V''')`. In the cubic case the last expression has
quadratic `Q` coefficient `c=-8A^3w` and pure-`q` coefficient with
third derivative `12A^2w^2`, giving exactly the stated depth-six
value from the preceding general coefficient identity.

There is no remaining resonant boundary in `deg V`. Variable leading
momentum coefficients and analytic nonpolynomial residual potentials remain
distinct scopes. Quadratic and affine shears are resolved by the supplements
reviewed next.
The certificate procedure can start from the proof-backed finite
candidate space above and retain full outputs. A stable subspace that
is invariant under `D` and killed by every gate is exactly the core;
no arbitrary polynomial degree box is needed.

## Quadratic shears and the exact cubic parameter certificate

For `deg u=2`, `u''` is a nonzero constant and
`C3=V''' partial_Q^3-6Au'' partial_q partial_Q^2`. If `deg V>=4`,
a hypothetical highest term `g(q)Q^N`, `N>=3`, first has `g` constant.
Its next coefficient `h(q)Q^(N-1)` must satisfy
`h'=N V'''g/(6Au'')`. The top coefficient of `DG` is then
`-N V'''g/(3u'')` in degree `N`; applying its third gate would force
`V''''g=0`. This contradiction reduces the joint depth-one kernel
to degree at most two with constant quadratic coefficient. All subsequent
QF coefficient steps and its sharp depth-four witness remain valid.

For cubic `V`, translating `q` and making an affine momentum shear first
reduces to `A(p+bq^2)^2+v q^3+e q`, modulo a constant. The nonzero
rational scales `s=v/(Ab^2)` and `t=bs^2`, followed by division by
`At^2`, give `(p+q^2)^2+q^3+lambda q`, where
`lambda=eA^2b^4/v^3`. The retained `GL2` covariance, not merely
symplectic covariance, is used for these final independent scales.
Vanishing conditions and bracket depth survive all these transformations.

In the normalized `(q,Q)` variables, weights `(1,2)` give leading
operators `D0=-2Q partial_q` and `C0=-12 partial_q partial_Q^2`.
Their common kernel through depth two is the retained unforced QC core.
Thus a candidate of weight above six has top `Q^N`, `N>=4`. The
first-deficit static gate uniquely forces the next component to be

\[
\frac N2qQ^{N-1}+\beta q^{2N-1}+\gamma q^{2N-3}Q.
\]

The next derivation has a top contribution `3Nq^2Q^(N-1)`, whose
leading gate is `-72N(N-1)(N-2)qQ^(N-3)`. Other permitted terms
have zero gate or output with `Q` degree zero. Since `N>=4`, they
cannot cancel that nonzero contribution. Hence every depth-two candidate
has weight at most six, giving the sixteen-dimensional full candidate
space before any finite matrix is used.

The fourteen-row minor has the nonzero constant determinant specified in (QR10). Its row depths
sum to `32`. Each depth-`r` entry has parameter degree at most `r`
because `D=Da+lambda partial_Q` and `C3` is parameter independent.
Consequently thirty-three exact rational agreements prove the constant
polynomial identity for every `lambda`. The independent review checker
recomputes all thirty-three determinants using its own polynomial and
fraction arithmetic and obtains the same constant. This is a rigorous
interpolation certificate with a proved degree bound, not a numerical
rank extrapolation. Full rank fourteen together with independent kernel
vectors `1,H` gives exactly their span. The universal depth-six witness
is the same `q` and formula `-960A^5u''(V''')^2` as in QF.

This closes every quadratic shear with nonlinear polynomial potential.
Together with retained QC and the oscillator theorem, all quadratic-shear
residual degrees are classified. The characteristic-zero assumption
justifies both the rational normalization and the polynomial root count.

## Affine shears and the remaining constant-quadratic branch

For affine `u`, the change to `(q,Q)` is affine canonical. The exact
third gate is `C3=V''' partial_Q^3`. If `deg V<=2`, the Hamiltonian
is quadratic and every polynomial is exact. Otherwise its static kernel
has `Q` degree at most two, so write `G=c(q)Q^2+b(q)Q+f(q)`.
Successive third-gate equations are

\[
 C_3DG=-12AV'''c',\qquad
 C_3D^2G=24A^2V'''b'',\qquad
 C_3D^3G=48A^2V'''(cV'''-Af'''),
\]

with each later identity conditional on the preceding vanishings.
They force `c` constant, `b` affine, and `f'''=(c/A)V'''`.
Thus the depth-three space is exactly `span{1,H,q,Q,q^2,qQ}`.
The same exact preimage chain used in QF then gives depth five for
potentials of degree at least four and depth seven for cubics, always
with full core `span{1,H}`. The sharp witness `q` has

\[
 C_3D^5q=96A^4V'''V''''\quad(\deg V\ge4),\qquad
 C_3D^7q=-960A^5(V''')^3\quad(\deg V=3),
\]

and passes all preceding depths. The review checker independently
verifies these formulas for constant and genuinely affine shears, with
nontrivial rational kinetic coefficient and lower potential terms.

The three completed-square cases `deg u<=1`, `deg u=2` and `deg u>=3`
therefore exhaust every Hamiltonian `A p^2+B(q)p+C(q)` with nonzero
constant `A`. This completeness is a consequence of the proved routes;
it does not extend to a nonconstant leading momentum coefficient.

## First- and second-order deformation obstructions

Fix `Q=p+q^2` and `H_t=Q^2+t*q^2/2`. In fixed `(q,Q)` coordinates,

\[
 C=-12\partial_q\partial_Q^2,\quad
 D_t=D_0+tD_1=-2Q\partial_q+tq\partial_Q.
\]

The depth-zero-through-three operator vector `L_t` is uniform for this
family, including its exceptional fiber. A polynomial jet is required
to satisfy the coefficients of these exact operators modulo its stated
power of `t`; no observable-degree truncation is part of the definition.

Modulo the six-dimensional exact quadratic space, a zeroth-order
candidate is `f(Q)`. A first-order correction `X` must satisfy `CX=0`,
hence has form `a(q)+Qb(q)+g(Q)`. The coefficient of `t` in `CD_t`
is

\[
48b''(q)-12f'''(Q)=0.
\]

Its two sides depend on independent variables, so `f'''` must be
constant. This excludes every higher power and every nontrivial linear
combination of powers of degree at least four without a degree cutoff.
The only additional first-order direction is `Q^3`, which lifts as
`Q^3+(3/4)tq^2Q`.

For this lift, direct differentiation gives

\[
 D_tG=\tfrac34t^2q^3,\quad
 D_t^2G=-\tfrac92t^2q^2Q,\quad
 C D_t^3G=-432t^2.
\]

The constant-extraction functional in the third depth component
annihilates `L0 X` for every polynomial `X`, because `CD0^3X` is
divisible by `Q`. Any other first-order lift differs by an element of
the retained unforced QC core. The first variation of the third-depth
component vanishes on that entire core: it vanishes on the quadratic
sector for all `t`, and `D0^2D1f(Q)=0`. Hence no choice of first-order
lift changes the second-order obstruction. First-order liftable
zeroth-order observables form exactly a seven-dimensional space;
second-order liftable observables form exactly the six-dimensional
quadratic sector, which lifts to every order.

This is a genuine obstruction to deforming an exact observable sector.
Smith invariant factors of a finite presentation encode it, but no new
geometric torsion, general deformation theory, or novelty of Smith
normal form is claimed.

The graded extension is also sound. On homogeneous input degree `n>=4`,
the four outputs have degree `n-3`, so the matrix has `n+1` columns
and `4(n-2)` rows. At `t=0` its kernel is exactly the line `K Q^n`,
so its rank is `n`. At every nonzero parameter over the algebraic
closure, the oscillator theorem makes it injective in this degree.
Therefore all Smith factors except one are units, and the last is a
power `t^e`; a different nonunit factor would have a nonzero root
where rank dropped. Invertible polynomial Smith source/target changes
identify the exceptional initial line with that last factor. An
exponent `e>=2` would supply a first-order lift of its nonzero initial
direction, contrary to the all-degree obstruction above. Hence `e=1`.
For degree three the explicitly certified exponent is two. This proves

\[
\operatorname{Tor}\operatorname{coker}L_t
\cong (K[t]/(t^2))_{\text{degree }3}
\oplus\bigoplus_{n\ge4}(K[t]/(t))_{\text{degree }n}.
\]

The free cokernel rank in each degree `n>=4` is
`4(n-2)-(n+1)=3n-9`. The target must be the full direct sum of four
homogeneous output spaces; this calculation would be invalid if a
bounded matrix silently omitted output monomials.

## Independent arithmetic calibration and limits

`extension_proof_review.py` implements its own sparse rational arithmetic
and direct original-coordinate mixed derivatives. It imports none of
the new producers. It checks the transformed composition operator,
full-output joint kernels, lower affine oscillator parameters, both
sharp-depth witnesses, the Euler indicial factorization, allowed mixed
potentials and a rejected potential. It additionally checks the sharp quadratic-frontier depths at cubic, quartic, resonant and supercritical potential degrees, and the formal cubic lift residual coefficient by coefficient in the parameter. It also independently replays the quadratic-shear cubic minor at all thirty-three required parameter values and checks the affine-shear sharp-depth formulas. The receipts record finite
calibrations only. The universal claims above depend on their written
filtration, ODE and obstruction proofs. A recognizer failure is not a
certificate of collapse, and a failed optional search is not a theorem.
