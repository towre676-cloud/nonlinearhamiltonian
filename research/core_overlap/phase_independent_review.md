# Independent review of the cubic-phase completeness and restoring theorems

This review uses the original flat Weyl transvectants in one canonical pair
over a characteristic-zero field. It distinguishes universal written
arguments from finite arithmetic replays. Its checker imports no project
mathematical engine, producer classifier, triangular formula, or gate
implementation. Polynomial multiplication, differentiation, substitution,
mixed-derivative transvectants, and rational rank are implemented separately
with Python's standard-library `Fraction` arithmetic.

Historical priority and external peer review remain open. The review supports
the precise classifications below, not a classification of arbitrary
non-affine cubic-phase Hamiltonians.

## Scope and notation

Put `Q=q`, `P=p+w(q)`, with `w=cq^2+dq+e` and `c!=0`. This substitution
rewrites the original operators. It does not justify replacing the original
flat product by a different flat product in `(Q,P)`. The derivation is
`Dg={H,g}=H_q g_p-H_p g_q`.

The reviewed proof files are `cubic_affine_completeness.md` (AC),
`cubic_phase_audit.md` (CPL), `higher_restoring.md` (HR), and
`cubic_deformation.md` (CD), together with the universal extension
`restoring_deformation.md` (RD/RT). The first two complete the affine-in-Q
Hamiltonians in their stated branches; the low-degree branches are supplied
by the retained CQ/QC and positive-structure theorems. HR closes a separate
non-affine restoring family, and CD measures its formal degeneration.

## Independent operator and leading-coefficient checks

For `h=a(P)+Qb(P)`, direct original-coordinate differentiation gives

`C3g=-(a'''+Qb''')g_QQQ+3b''g_QQP`

`+6c[b'g_PPP+b''g_PP-(a''+Qb'')g_QPP-(a'''+Qb''')g_QP]`.

The checker verifies this formula against direct original-coordinate third
transvectants for thirty rational polynomial instances, including nonunit
and negative shear coefficients and affine terms in the shear.

On the highest transverse term `Q^N f(P)`, the operators are

`L_N=b partial_P-Nb'`,

`M_N=b' partial_P^3+(1-N)b'' partial_P^2-Nb''' partial_P`.

If `deg b=m`, `deg f=n`, and their leading coefficients are B and F,
the coefficient of `P^(n+m-4)` in `M_N f` is

`BF*m*n*(n+m-3)*(n-1-N(m-1))`.

The exponent is `n+m-4`. Vanishing derivative terms are omitted when this
exponent is negative. The factorization follows by direct expansion and is
replayed at 432 integer exponent combinations. For `N>=2`, comparison with
`L_N` excludes every positive N at least two after depths zero and one when
`m>=3`, and after depths zero through two when `m=2`. The permitted degree
sets are respectively `{0,1+N(m-1)}` and `{0,1,N+1}`; `L_N` immediately
leaves them, with one additional step in the constant quadratic-b case.
No lower-Q term can cancel a highest-Q coefficient, since both operators
preserve the Q-degree filtration. This verifies the essential all-degree
containment argument of AC.

For `m>=3`, the remaining affine observable has `beta=lambda*b+nu`.
Subtracting `lambda*h` reduces the density to a linear polynomial. The
Q coefficient after one bracket forces `nu=0`; the next static gate forces
the remaining P slope to vanish. Thus the full core is `span{1,H}` for
every polynomial a, including a of degree at most two.

For quadratic b, AC's proof of K4 necessity is independent of bounded
symbolic enumeration. The projected core is an `ad_b`-invariant subspace
of the three-dimensional quadratic-vector-field space. If its dimension
is two, its second generator can be normalized to `mu(P-r)` and bracket
closure forces `b(r)=0`. In the variable `x=P-r`, the two density equations
reduce to

`a''=2alpha'+(x-delta)alpha''`,

`x alpha''-2alpha' in K`.

The second equation has polynomial solutions
`alpha=A x^3+C x+D`, so the first forces
`a=A x^3(x-delta)+C x^2+c1 x+c0`. This proves K4 exhaustiveness in every
degree. A three-dimensional projection is excluded by the separate beta=1
argument and its second bracket. The low-a quadratic-b branch instead has
the complete four-dimensional core `span{1,X,XP,H}` after the stated
constant Q shift. These exceptional low degrees are necessary and are not
covered by Claude's original `deg a>=3` table.

The stronger finite stopping statement also passes independent review.
Within the affine observable space, the static third-gate kernel has
dimension five. At depth one, the kernel of its beta projection consists
only of constants. For `deg a>=3`, a depth-one space of dimension at least
four would therefore project onto all three quadratic beta coefficients.
Its beta=1 representative forces a to be cubic. A beta=P representative
then has density leading coefficient `3a3/(2b2)` at P squared, but the
third gate of its first bracket has uncancellable leading term
`144c*b2*a3*P`. Thus the depth-one space has dimension at most three and
contains `1,H`. The next descending stage is either equal to it and
invariant, or is the two-dimensional stationary span. Low-degree a has
the explicitly invariant four-dimensional space already at depth one.
Combining this argument with the whole-ring Q-degree bound proves full
stopping at depth two for quadratic b. The witness
`h=QP^2`, `g=Q^2+2P/c` satisfies
`C3g=C3Dg=0` and `C3D^2g=864P-288cQ^2`, so the uniform bound is sharp.
For b of degree at least three, the complete stopping depth is one;
the same proof separately removes the Q and P coefficients at that depth.

## The independent linear-coupling argument

After scaling, translating P, and subtracting a constant, take
`h=PJ`, `J=Q+A(P)`, with `deg A=m>=2`. Its Hamiltonian derivation is

`D=P partial_P-J partial_J`.

Every polynomial is a finite sum of its integer-eigenvalue components.
Since the core is D invariant, finite spectral projections preserve it.
The highest-Q third-gate equation bounds the highest-P exponent d of
each component to `d<=2`. An eigencomponent of J degree n consequently has
only the terms `P^(d-j)J^(n-j)`, `0<=j<=min(d,n)`.

Independent chain-rule expansion gives the dominant `partial_J^3`
coefficient

`-6c(A')^2(A'+P A'')-(3A''+P A''')`.

For `A=alpha P^m+lower` and `n>=3`, the uniquely highest P-degree
contribution is

`-6c*m^4*alpha^3*n*(n-1)*(n-2) P^(d+3m-3)J^(n-3)`.

For `n=2`, combining the two `partial_J^2` terms gives instead

`-12c*m^2*(2m-1)*(d+m-1)*alpha^2 P^(d+2m-3)`.

The lower eigencomponent terms have strictly smaller P degree. Both
coefficients are nonzero in the stated range, which excludes every n at
least two. The independent checker replays 75 versions of these two leading
coefficients with lower terms in A retained. It separately checks every
relevant odd gate and full-output D closure on twelve protected linear-b
spans. This confirms the four-, five-, and six-dimensional full-core cases
of CPL.

The subsequent finite stopping extension is valid as well. If S is the
finite set of D-weight shifts of the normally ordered C3 operator, an
output coefficient of weight omega in `C3D^rG` has the form
`sum_(s in S)(omega-s)^r c_s`. The nodes `omega-s` are distinct in
characteristic zero. Inverting the Vandermonde matrix for
`r=0,...,|S|-1` forces each contribution to vanish, and hence forces
every input D-eigencomponent to pass C3 separately. CPL already
classifies exactly these components and proves that its listed basis
passes every odd gate. Thus `R=|S|-1` is a uniform all-degree stopping
bound for each declared Hamiltonian. Inspection of the exact operator
gives `S subset {-3,-1} union {1,...,3m}`, so `R<=3m+1`.
In the normalized six-dimensional cubic branch,
`A=alpha P^2+constant`, the support is exactly `{-3,3,6}` and R is two.
These are upper bounds; general sharpness is not asserted. Independent
replay verifies four shift supports and reconstructs twelve output
coordinates by exact Lagrange/Vandermonde projection.

## Unified chart recovery and lower-degree boundaries

The unified rational recognizer in `cubic_phase_classification.py` has
also been reviewed separately. If the highest-p coefficient is linear
in q, division of the next coefficient by its scaled predecessor can
change the recovered shear only by a constant. Its quadratic and linear
terms are therefore exact. If that leading coefficient is constant,
the quadratic shear term is still fixed, while the remaining slope alpha
satisfies the common equations
`(partial_Q-alpha partial_P)^2 h0=0`. Taking the polynomial gcd of those
equations preserves exactly their common algebraic roots. For total
degree at least three there cannot be two distinct roots: in coordinates
along two independent directions, both pure second derivatives would
vanish and the polynomial would be at most bilinear, hence of degree at
most two. A sole algebraic root of a rational polynomial of degree at
most two is rational. Exact reconstruction rejects spurious candidates.
This resolves the linear-shear ambiguity without inferring completeness
from a completed-power choice that could hide an affine family.

The lower-degree rows also pass direct structural review. With linear b
and quadratic a, completing the square produces a nonzero quadratic
restoring coefficient `-mu^2/(4a2)`, and CQ gives the six-dimensional
quadratic sector. With linear b and a of degree at most one, the original
Hamiltonian is `(mu q+alpha)p+phi(q)` with `phi'''=6mu c!=0`.
Its only higher odd gate is `6mu c partial_p^3`, and D preserves its
kernel, giving the full three-strip. Thus this case has an infinite
core, not a two-strip or a six-dimensional core. Purely q-dependent
affine Hamiltonians can be classified through the supplied-chart API;
the original-polynomial chart recognizer deliberately returns a miss
when its p degree is zero. No collapse claim follows from that miss.

## Restoring-force theorem: why the degree bound is universal

For `H=F(P)+lambda Q^2+epsilon Q+C`, `deg F>=3`, `lambda!=0`, the
original third gate is

`C3=-F''' partial_Q^3-6c partial_Q(F'' partial_P^2+F''' partial_P)`.

Take a polynomial G of Q degree N at least three passing `C3` and `C3D`.
The static top coefficients force `g_N,g_(N-1)` to be constants and
`g_(N-2)'=-N(N-1)g_N/(6c)`. The leading coefficient of `C3DG` is then

`12c*N*(N-1)*g_N*F''*F'''`,

which cannot vanish. This excludes all Q degrees at least three without a
bounded search. With N at most two, static exactness gives
`G=g(P)+aQ+bQ^2`; the next gate forces
`g''=(b/lambda)F''`. The integration constants that would give a term
proportional to `1/F''` are excluded by polynomiality, not by an unproved
analytic assumption. Thus the first two tests give exactly
`span{1,Q,P,H}`.

Let `R=(F''F''')'`. Its leading coefficient is nonzero for every polynomial
F of degree at least three. Direct differentiation then gives

`C3D^2Q=12c*lambda*R`,

`C3D^2P=0`,

`C3D^3P=24c*lambda^2*R`.

These identities remove Q and then P, proving the full core
`span{1,H}` and sharp third-gate depth three. The checker evaluates these
identities directly in original coordinates for ten examples spanning
degrees three through seven, with nonunit rational restoring coefficient
and a nonzero linear force. Higher odd gates cannot invalidate the answer:
the upper bound is supplied by C3 alone, and 1,H pass every odd gate by
stationarity and antisymmetry.

## Formal deformation and presentation-dependent module torsion

CD's cubic family uses `H_t=P^3+tQ^2`. Its unrestricted polynomial
corrections give first-order liftable initial space `span{1,P,P^3}`,
and second-order/formal initial space `span{1,P^3}`. The obstruction
`C3D_t^3P=864t^2` agrees with HR at `F=P^3,c=1,lambda=t`. The
constant-coefficient functional cannot be changed by an arbitrary-degree
second correction because `C3D_0^3X` is divisible by `P^5`. Changes of the
first lift belong to the initial core and have zero first variation in
that same functional. The no-degree-cutoff claim is therefore supported
by a coefficient functional, not a finite source matrix.

For the declared finite weight presentation `V_N`, `N>=6`, the Smith-factor
argument is also sound. Generic kernel dimension two and zero-parameter
kernel dimension `floor(N/2)+2` fix the number of nonunit factors. Over an
algebraic closure, no other nonzero parameter gives a rank drop, so all
nonunit factors are powers of t. The first- and second-order liftable
initial dimensions fix one exponent at two and all other exponents at
one. Sufficiency uses lifts already inside every declared `V_N`. Hence
the torsion formula holds for every N at least six. Its free target part
depends on the chosen output population; no presentation-independent
invariant of an undeclared infinite matrix is claimed.

The universal extension RD/RT also passes independent review for every
`H_t=F(P)+tQ^2`, `deg F>=3`. Set `B=F''`, `A=B'`. The exact commutator

`[C,D0]=12c B(A+B partial_P) partial_Q^2`

acts injectively on each nonzero polynomial coefficient of
`partial_Q^2G`, because `B(A+B partial_P)g=B(Bg)'` cannot vanish for a
nonzero polynomial g when B is nonconstant. Thus static exactness and a
Q-independent first-depth residual force every correction to have form
`aQ^2+beta Q+g(P)` with a,beta constant. This is an all-degree argument.
The first-order equations then force the initial tower polynomial to be
`aF+bP+d`, and the nonzero `12c(F''F''')'` residual removes the initial
Q direction.

For the delayed P obstruction, the second-order static and first-depth
equations again force the second correction to have Q degree at most two.
Its third unperturbed iterate is therefore zero. The first variation of
the third-depth gate on any allowed first correction is also zero,
leaving the nonzero residual `24c(F''F''')'`. This coupled argument is
essential: for general F that residual is not constant, so the cubic
case's constant-coefficient functional cannot simply be reused. RD
correctly uses the coupled argument and proves first-order initial space
`span{1,P,F}` and second-order/formal initial space `span{1,F}`.

For the C3-only depth-three finite presentation with weight bound
`N>=2deg F`, the same Smith-factor argument as above applies. HR gives
the generic two-dimensional kernel over the algebraic closure, the
zero-parameter kernel has dimension `floor(N/2)+2`, and the polynomial
lifts `1,P,H_t` lie inside every declared source. The first- and
second-order initial dimensions are therefore three and two in the
finite source as well. It follows that its torsion is exactly one
`K[t]/(t^2)` plus `floor(N/2)-1` copies of `K[t]/(t)`. No other parameter
roots or higher exponents are possible. This confirms both the
general-profile extension and its every-N claim without relying on
sampled Smith forms.

## Terminology, normalization, and primary background

The exact compatibility defect in the affine phase satisfies

`b'beta'''-b'''beta'=(b'beta''-b''beta')'`.

Its integral vanishes under periodic or compact-support boundary
conditions. It is therefore not the usual nontrivial scalar
Virasoro/Gelfand--Fuchs central-extension cocycle. The full defect
`Delta(X,Y)=partial^3[X,Y]-[partial^3X,Y]-[X,partial^3Y]` is the
Chevalley--Eilenberg coboundary, up to sign, of the operator `partial^3`
in the adjoint module. This is a useful explicit compatibility test;
a nontrivial class in a different coefficient module would require an
additional definition and proof.

Ovsienko and Roger give the standard scalar cocycle
`c(f partial,g partial)=(1/12) integral f'''g dx` in equation (9.2) of
[Deforming the Lie algebra of vector fields on the circle inside the Lie
algebra of pseudodifferential symbols](https://arxiv.org/abs/math/9812074)
(1998). The distinction above follows directly from our displayed total
derivative; the cited paper supplies the standard scalar convention.

Equivalence of coordinate-transformed star products with suitably related
Moyal products belongs to established deformation-quantization machinery.
Primary background includes Domański and Błaszak,
[On local equivalence of star-products on Poisson manifolds](https://arxiv.org/abs/1305.4026)
(v3, 2016; v1 appeared in 2013 under an earlier title), and Błaszak and
Domański, [Canonical transformations in quantum mechanics](https://arxiv.org/abs/1208.2835)
(2012). These references support the general background only; they do not
establish historical priority for the particular complete-core theorems
proved in this package.

Finally, the exact cubic gauge uses `s=ct^2/3` when its transvectant
generating product is `exp(t Omega)`. With the physical convention
`exp(i hbar Omega/2)`, substitution gives `s=-c hbar^2/12`. Zero-gate
classifications are unchanged by that parameter normalization. A claim
about a physical hbar coefficient must specify which convention is used.

## Reproduction

Run `python3 -B -S research/core_overlap/phase_independent_review.py`.
The retained receipt records 665 checks in nine categories. They calibrate
the universal proof identities and exact protected spans. They do not
turn finite experimental agreement into a proof of an unlimited core.
