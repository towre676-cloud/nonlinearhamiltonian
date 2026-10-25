# Independent adversarial assessment

This assessment concerns the overlap work based on Claude commit
`e91e14da9d59e799ad9ed0331f59b2b500e478e8`. It is an internal mathematical
review, not external peer review, formal proof verification, or a priority claim.

## Pure-top counterexample and replacement stratum

The counterexample `J=qp+q^3`, `H=qJ^2` is valid. Direct differentiation
gives `{H,J}=H`. Every derivative of `J` of order at least three involves
only `q`, while `H` has degree two in `p`, so every odd gate vanishes.
The span of `1,H,J` is therefore invariant and exact. Its dimension is three,
because the three elements have different transverse degrees.

The all-degree upper bound does not follow from a finite search. It follows
from the transverse filtration and the already proved monomial theorem:
the transverse top `q^3p^2` has core `span{1,qp,q^3p^2}`. An additional
core element of transverse degree zero must be constant; after subtracting
a multiple of `H`, any other element has the uniquely normalized form
`qp+u(q)`. Hence the full core is exactly three-dimensional. This is a
counterexample to the unrestricted conjecture P003 at the inspected commit,
not to any of the restricted proved statements B, Q, Q', or T.

The proof of the complete unequal perfect-power classification in
`pure_perfect_power.md` is sound. The transverse filtration is valid with
weight `(0,1)` even though the filtered pieces are not finite-dimensional:
each polynomial has finite transverse degree and the leading comparison is
applied separately to each operator identity. Finite-dimensionality of the
resulting associated graded core, rather than of the ambient filtered
pieces, supplies the dimension bound.

If a third core element exists, it must be `J=tp+u(t)` and satisfy
`{H,J}=(r-s)H+bJ+c`. The identity `T3(H,J)=-u'''H_ppp` forces `u` to be
quadratic when `s>=3`. A quadratic `J` would force the top eigenvalue to be
the total degree `d`, whereas the transverse comparison forces it to be
`r-s`; pure total top implies `d>r+s`, a contradiction. For `s=2`, Euler
integration in the Laurent coordinates `(t,J)` gives precisely
`H=t^(r-2)P2(J)+beta J+delta`. The coefficient-based decision test has the
correct signs, and its divisibility conditions account for the resonant
coefficient of degree `r-1` in the linear-in-`p` part.

The independent checker `review_checks.py` uses its own direct polynomial
differentiation. It verifies 120 parameterized family members, 2,760 odd
gate identities, and brackets through depth five. For the basic degree-seven
example, independent modular matrices have nullity three through total
degree nine. Those matrices corroborate the example; the filtration proof
is what establishes the all-degree statement.

## Analytic finite determination

The theorem in `depth_finite_determination.md` is correct under its stated
real-analytic, connected-interval, finite-`q`-degree hypotheses and the
condition that `F''` is nowhere zero. The three tests
`C3 G=0`, `C3 D G=0`, and `C5 G=0` determine the full core. Sector splitting
is exact because `D` preserves `q` degree and each gate shifts every input
sector by the same amount.

For degrees at least five the shorter incompatibility argument is an
independent derivation of the obstruction. In the notation of the theorem,
let `E=Fu-awB-kB`, with `F'=w`, `w'=delta B`, `B'=u`, `u'=v`, and
`v'=beta vu/B`. Define `L=a(beta-1)+2` and

```
J = Lwv + (beta-1)kv + (1-3a)delta Bu,
R = [a(beta-4)+3]Bv - (3a-1)(1-beta)u^2.
```

The following three identities hold formally in a Laurent-polynomial ring:

```
E'' = J + beta v E/B,
v (J/v)' = delta R,
R' = uv (beta+5)[1+a(beta-2)].
```

The independent checker verifies these by exact symbolic arithmetic with
its own Laurent-polynomial derivation. There is no numerical differential
approximation and no hidden division by a first-integral constant. Since
`v` is nowhere zero and `u` is nonzero on some open subinterval, `E=0` would
force the nonzero scalar `(beta+5)[1+a(beta-2)]` to vanish. The parameter
identity shows the second factor is strictly positive for every integer
sector degree at least five. The separate degree-two, degree-four, and
`B''=0` cases are correctly treated in the theorem note.

The direct fractional-power examples in that note establish necessity of
each of the three tests. In particular, testing third-order corrections at
every bracket depth is still insufficient universally: the stationary
fourth-power example passes all of those tests and fails the fifth-order
gate.

## Rational coefficients with arbitrary analytic potential

The highest-`q`-degree proof of the rational-coefficient extension is also
valid: in `H=qF(p)+B(p)`, the additional potential contributes one lower
`q` degree to both the third gate and the derivation. It cannot cancel the
highest-sector obstruction. At a pole of integer order `m>=1`, the candidate
sector obstruction has nonzero leading coefficient proportional to
`(c+1)m-c+2`; if the rational function has no finite poles, its polynomial
leading coefficient is proportional to `(c+1)n+c-2`, also nonzero. Thus no
sector of degree at least two persists. This is an exact algebraic argument,
not a finite-degree extrapolation. A meromorphic function with a finite
pole gives the same contradiction when continuation to that pole is part
of the explicitly stated domain assumptions.

## Scope retained

No claim here transports the flat Moyal product through an arbitrary
nonlinear canonical map. The special shear family's exactness is proved
directly by derivatives. No claim identifies an analytic-function kernel
with a rational polynomial Weyl-ideal receipt. Literature priority remains
unresolved, and the remaining transverse balanced exception is a different
stratum from the unequal exception classified here.

## Nonlinear shear compositions with balanced transverse top

The theorem in `audit_balanced_transverse.md` is approved. Its key
transverse Euler resonance is exact: for `H=P(J)`, `J=qp+u(q)`, and a
hypothetical core element with first transverse pieces `Q^s+f(q)p^(s-1)`,
one bracket forces `f=sq^(s-1)v+cq^(s-1)`. The coefficient at the resonant
Euler monomial vanishes on the left, so a nonzero diagonal bracket top is
impossible. No assumption that powers of a core element remain in the core
is made in this reasoning.

The first nonzero third-gate coefficient is
`mu s(s-mu)(s+mu-3)q^(mu+s-1)u'''`. The formal negative output degree in
the exceptional pair `mu=2,s=1` has zero coefficient and is correctly
excluded from the polynomial comparison. Consequently the three regimes
are the width-two strip for linear compositions, the stationary space
`span{1,J,J^2}` for quadratic compositions, and `span{1,H}` for degree at
least three. This concerns a balanced transverse top and does not conflict
with the already proved balanced total-top theorem.

Independent direct differentiation now checks this first-gate factor in
90 complete polynomial composition pairs, rather than only in formal
monomial coefficients.

## Parabolic quadratic compositions, including linear forcing

The theorem in `pure_quadratic_composition.md` is approved in its full
stated scope `Q=p+bq^2+cq+d`, `b!=0`, `H=P(Q)+epsilon q`. The change of
variables is a polynomial algebra isomorphism used to transform the
operators; it is not an appeal to nonlinear covariance. Direct chain-rule
expansion gives the stated third gate and
`D=epsilon partial_z-P'(z)partial_t`.

For `deg P>=3`, the leading and second-leading `t` coefficients of a
candidate core element are constants. Applying the third gate after one
bracket then forces `t` degree at most one; the linear forcing contributes
no surviving term to that decisive coefficient. For `deg P=2`, write
`P'=kz+l` and a static candidate as `A(z)+zB(t)+C(t)`. The exact formulas
are `C3DG=12bk^2 B''` and, after `B''=0`,
`C3D^2G=-12bk^3 C'''`. Hence the additional generators are exactly
`t,tz,t^2`.

The infinite tower is proved without circularity. Since
`Q star f(Q)=Qf(Q)-b hbar^2 f''(Q)/4`, star powers of `Q` form a triangular
basis of its ordinary polynomial algebra. This algebra is commutative for
the star product. Each odd transvectant therefore vanishes individually.
The resulting sectors are invariant under the forced derivation as
claimed. In particular the forcing makes the tower active, which is a
substantial counterexample to unrestricted pure-top collapse.

The independent checker adds 48 direct comparisons of the transformed
derivation and third gate with differentiation in the original coordinates,
plus 262 odd-gate checks on tower and extension generators through two
further brackets.

## Arbitrary analytic additive potential: the second depth is sharp

The additive-potential finite-determination theorem in
`depth_finite_determination.md` is also approved. For
`H=qF(p)+V(p)`, the first three tests `C3G=0`, `C5G=0`, and `C3DG=0`
force finite `q` degree at most three. Their solution space modulo the
invariant affine strip has dimension at most one: cancellation of two
cubic leading coefficients would leave a quadratic candidate, which the
same third-gate and first-bracket tests exclude.

The additional equation `C3D^2G=0` places `DG` in that same first-three-test
space, since its `q` degree is at most three and fifth gates are then
automatic. Thus `DG=lambda G+strip`, and all later iterates pass every
gate. This proves the four-test stopping rule. The extension across
isolated zeros of `F''` follows by restriction to a subinterval where it
does not vanish and then by analyticity. The identically affine `F` case
is separately elementary, as stated in the note.

Independent sparse fractional-power differentiation verifies the sharp
example `H=q p^(-1/4)+p^(7/4)` and
`G=q^3p^(-3/4)-(21/25)q^2p^(5/4)`: its first three tests vanish, while
`C3D^2G=(63/8)p^(-9/2)` is nonzero. This is a genuine failure of a
first-bracket stopping rule when the potential is arbitrary.

## Explicit algebraic active cubic

The strengthened `analytic_bridge.md` is approved, including the family
`F=a p^(-1/4)+bp`, `a!=0`, on the positive axis. Independent simplification
gives the sector obstruction
`Kc=a(3-c)p^(-5/4)/2-b(7c-6)/4`; precisely the cubic degree survives.
The claimed eigenvalue, the nonlinear canonical quadratic representation,
and the second-power Moyal anomaly all have the stated constants and signs.
The general higher-degree fractional-power example has fifth-gate
coefficient `-8(c)_4(rho)_4`, with `rho=(2-c)/(c+1)`, so all-depth
third-order exactness does not imply full Moyal exactness.

The gamma/polygamma specialization FP is approved as well. The integer-pole
coefficient is nonzero in every integer degree at least two. For the
logarithmic template `F=-a log p+b(p)`, direct expansion of `F'''/F''`
gives the stated logarithmic-over-`p` leading term; at degree two the
remaining `2a/p` term is nonzero. The continuation requirement belongs to
the coefficient function `F`, while the additive potential remains
arbitrary analytic on the working interval.

## Arbitrary polynomial shear and the exact six-dimensional square sector

The further shear-square theorem is approved. Let `Q=p+u(q)`,
`deg u=n>=3`, and `H=AQ^2+BQ+C+epsilon q`, `A!=0`. In coordinates
`(q,Q)` the exact operators are

```
D  = epsilon partial_Q-(2AQ+B)partial_q,
C3 = (2AQ+B)u''' partial_Q^3-6A u'' partial_q partial_Q^2.
```

The proposed sector is every polynomial of total degree at most two in
`(q,Q)`, namely `span{1,q,Q,q^2,qQ,Q^2}`. The transformed derivation
preserves it, and the third gate kills it. Every higher odd gate kills it
in the original coordinates as well: both arguments have degree at most
two in `p`, so an odd gate of order at least five requires more than two
`p` derivatives on one argument.

Completeness follows from the stated total-degree filtration in `(q,Q)`.
The derivation has top part `D0=-2AQ partial_q`, of degree shift zero.
If a core element had homogeneous top `G_N`, `N>=3`, choose its highest
`q` exponent `a`. Then `D0^a G_N` is a nonzero multiple of `Q^N`.
The top third gate, of degree shift `n-5`, sends that monomial to a
nonzero multiple of `q^(n-3)Q^(N-2)`. Lower filtration pieces cannot
cancel this component. This remains true at `n=3`, when the gate shift
is negative: every lower-degree piece still has strictly lower output
degree. Thus a core element cannot have transformed degree above two.

This proof uses repeated third gates only for the upper bound and direct
derivative exactness for the six-dimensional lower bound. It never assumes
nonlinear covariance or closure under ordinary multiplication. The linear
forcing is fully included; it changes only the lower filtration part of
the derivation. Direct independent checks in `review_checks.py` compare
both transformed operators with original-coordinate differentiation and
check the whole protected sector under repeated brackets.

The stronger uniform depth-two corollary is approved. On a leading
monomial `q^a Q^c`, the top operator `C0 D0^r` has coefficient proportional
to

```
(a)_r (c+r)_2 [(n-2)(c+r-2)-3(a-r)].
```

Its output shift is independent of `(a,c)` at fixed `r`, so cancellation
between different input monomials is impossible. For total degree at least
three, these coefficients cannot vanish simultaneously at `r=0,1,2`.
For `c>=3`, a zero at `r=0` forces `a>=1`, and the bracket at `r=1` is
`n+1`. For `c=2`, positive `a` already fails at `r=0`; for `c=1`, the
required `a>=2` fails at `r=1`; and for `c=0`, `a>=3` fails at `r=2`.
The full three-test kernel is therefore exactly the six-dimensional sector.

The depth is sharp for every allowed shear and every linear forcing:
`q^3` passes the first two tests, while
`D^2q^3=6q(2AQ+B)^2-6A epsilon q^2` and hence
`C3D^2q^3=-288A^3u''`, which is nonzero. Independent original-coordinate
differentiation checks this identity in twenty parameterized fixtures,
alongside an exact grid of the monomial factors. This grid supplements the
case argument above rather than replacing its all-degree proof.
