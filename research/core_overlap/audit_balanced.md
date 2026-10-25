# Balanced-top audit and a minimal proof repair

The balanced theorem at Claude commit `e91e14d` survives this audit. One step in
its published argument needs a correction. Subtracting multiples of `H` does
**not** justify requiring an extra element's top exponent to satisfy `s < mu`.
For example, a hypothetical extra element can initially have top `(qp)^(mu+1)`.
The dynamic core is a vector space, not an algebra; powers of `H` cannot be
subtracted without first proving they belong to it.

No additional theorem is needed to repair the argument. Choose any element
`G` outside `span{1,H}`. Its top is `c(qp)^s` by the top-weight lemma. If `s=mu`,
subtract `cH`; if this leaves a nonconstant polynomial, its degree is smaller
than `2mu` and its new exponent differs from `mu`. If it leaves only a constant,
the original `G` was in the excluded span. Thus in every case, after rescaling,
there is an extra `G` with `s >= 1` and `s != mu`. This is the only condition
the rest of the proof uses.

The factor `s(s-mu)` is nonzero for every such exponent, including `s>mu`.
The positivity estimate is symmetric in `s` and `mu`: a matched pair of
monomials has indices `(x,y)` and `(x-mu+s,y-mu+s)`, all nonnegative. Consequently
both `2mu >= k+|u|` and `2s >= k+|u|`, where `k=2mu-x-y` and `u=x-y`.
All stated positivity conclusions remain valid unchanged.

There are two boundary cases worth stating explicitly. When the proposed
partner monomial has a negative exponent, the bracket relation immediately
forces the original off-diagonal coefficient to vanish. When `k` exceeds
the degree of one of the two polynomials, this is the same argument with
the missing homogeneous component set to zero. Thus induction continues
through all components, without a restriction on the relative degrees of
`H` and `G`.

The bracket's component at the first unremoved deficit has an off-diagonal
support. It must also be diagonal because `{H,G}` lies in the dynamic core,
whose top is in `K[qp]`. This justifies setting that component to zero; no
assumption that the whole bracket vanishes is needed. Lower components of
both polynomials are diagonal by induction and hence Poisson commute, so
they do not introduce additional terms at that deficit.

The all-odd-order vanishing for two polynomials in `qp` follows from exchanging
the two coordinates in the transvectant, or directly pairing its summands.
The finite checks at orders 3, 5, and 7 in `check_balanced.py` are useful
calibrations, while this antisymmetry argument supplies the statement for
every odd order.

`audit_balanced.py` independently checks the scalar identity directly from
falling-factorial transvectants, both relative exponent ranges, support
boundaries, and every possible zero in the finite declared grid. It does
not replace the symbolic identity or the positivity proof. Its purpose is
to exercise the cases omitted by the unnecessary `s<mu` assertion.

Theorem T and Lemma F in §6.6 have no additional blocker found in this audit.
Their transverse filtration may assign weight zero to `ell`: the associated
graded embedding still implies finiteness when the entire top core is finite.
For the pure part of T, the exclusion is specifically a **power of a linear
form**, `phi=c(ell+gamma)^e`; the phrase “perfect power” should not be read as
excluding, for example, a square of a nonlinear polynomial.

## Independent review of the new unequal transverse classification

The theorem and proof in `pure_perfect_power.md` have been read independently.
The transverse associated graded argument bounds the entire core by three
dimensions. Its extra element must have the exact shape
`J=(q+gamma)p+u(q+gamma)`, so the proof uses no bounded-degree guess for `u`.
The identity `T3(H,J)=-H_ppp u'''` eliminates every nonlinear `u` when the
transverse degree is at least three. A quadratic `J` is impossible under a
pure total top: the top of `{H,J}` then has coefficient `d` against `H`,
whereas its transverse top forces coefficient `r-s`, with `d>r+s`.

For transverse degree two, the Laurent-ring integration of the closure
equation is valid because `J` is algebraically independent of `t=q+gamma`
and the derivation is `t*d/dt` at fixed `J`. The eigenvalue `r-2` is a positive
integer. This forces `H-beta J-delta=t^(r-2)P(J)` with `P` quadratic. The
coefficient recognition equations have the correct signs in the stated
Poisson convention. Their constant test is necessary and sufficient, rather
than only a necessary test obtained by projecting the image.

The family is polynomial in the original variables and its nonquadratic
`J` passes every odd gate by the separate derivative argument. Hence it is
a valid counterexample to P003, not a nonlinear covariance assertion.

There is a further simple stationary example outside the *unequal* scope of
that theorem: `J=qp+q^3`, `H=J^2`. Here the total top is pure `q^6` and the
transverse top is balanced `q^2p^2`. The span of `1,J,H` survives, while
`T3(H,J^3)=72q^3J` is nonzero. This does not affect the balanced **total-top**
theorem, whose leading homogeneous part is a nondegenerate quadratic power.
