# Nonlinear shear compositions: a complete exact-core phase diagram

Use the fixed flat Weyl convention
`D_H={H,.}=H_q partial_p-H_p partial_q`. Work over any field of characteristic
zero. Put

\[
J=qp+u(q),\qquad u\in K[q],\quad u'''\ne0,\qquad H=P(J),
\quad \deg P=\mu\ge1.
\]

Then the entire polynomial dynamic exact core is

\[
\boxed{
D_\infty(P(J))=
\begin{cases}
K[q]\oplus pK[q]\oplus p^2K[q],&\mu=1,\\
\operatorname{span}_K\{1,J,J^2\},&\mu=2,\\
\operatorname{span}_K\{1,H\},&\mu\ge3.
\end{cases}}
\]

The last two sectors are stationary. The total homogeneous top of `H` is a
pure power of `q`, of degree `mu deg(u)`. Its transverse, or `p`-degree, top
is a balanced power `(qp)^mu`. Thus these are the balanced **transverse**
exceptions in §6.6 of Claude commit `e91e14d`, not counterexamples to its
balanced **total-top** theorem B.

For example,

\[
J=qp+q^3,\quad H=J^2,
\qquad D_\infty(H)=\operatorname{span}\{1,J,H\}.
\]

This is a second counterexample to P003. It is stationary, unlike the active
unequal-transverse family in `pure_perfect_power.md`. It also shows why
nonlinear canonical covariance cannot be assumed: a quadratic Hamiltonian
in `J` retains only a quadratic stationary sector, while
`T3(J^2,J^3)=72q^3J` is nonzero.

## A closed composition identity

For arbitrary univariate polynomials `F` and `G`, direct differentiation gives

\[
\boxed{
T_3(F(J),G(J))
=q^3u'''(q)\bigl(F'(J)G'''(J)-F'''(J)G'(J)\bigr).
}
\]

Here no nonlinear covariance is being used. To verify the identity, put
`A=p+u'`, `B=q`, `C=u''`, `E=u'''`. The four third derivatives of `F(J)` are

\[
\begin{aligned}
F(J)_{qqq}&=F'''A^3+3F''AC+F'E,\\
F(J)_{qqp}&=F'''A^2B+F''(CB+2A),\\
F(J)_{qpp}&=F'''AB^2+2F''B,\\
F(J)_{ppp}&=F'''B^3.
\end{aligned}
\]

Insert these and their `G` counterparts into the alternating third
transvectant. All terms cancel except `B^3E(F'G'''-F'''G')`.
In particular,

\[
T_3(J^\mu,J^s)
=\mu s(s-\mu)(s+\mu-3)q^3u'''J^{\mu+s-4},
\]

whenever the exponent on `J` is nonnegative; the remaining low-index cases
vanish directly. For nonzero `u'''`, this formula already bounds the static
exact powers of `J`. The next argument proves that arbitrary polynomial core
elements, including those not assumed to be functions of `J`, obey the same
finite bound.

## Proof for mu at least two

Multiplying `H` by a nonzero scalar or adding a constant does not change the
core. Write its leading coefficient as one, and set

\[
P(z)=z^\mu+bz^{\mu-1}+\cdots,\qquad
v(q)=u(q)+\frac b\mu,\qquad Q=qp.
\]

The first two pieces in decreasing `p`-degree are

\[
H_0=Q^\mu,\qquad
H_1=\mu v(q)Q^{\mu-1}.
\]

The transverse top of any core element belongs to the core of `Q^mu`.
By the monomial theorem, that core is `K[Q]`. Therefore a nonconstant core
element of transverse degree `s` can be normalized to have the first pieces

\[
A_0=Q^s,\qquad A_1=f(q)p^{s-1},\qquad s\ge1.
\]

At transverse degree zero the core contains only constants.

**One bracket determines the first correction.** The top term of
`{H,A}` vanishes since `{Q^mu,Q^s}=0`. Its coefficient at the next possible
`p`-degree, `mu+s-2`, is

\[
\mu q^{\mu-1}\bigl((s-1)f-qf'+s q^s v'\bigr).
\]

The bracket is again a core element. Hence this coefficient, if nonzero,
must be a multiple of `q^(mu+s-2)`. After dividing by `mu q^(mu-1)`, the
right-hand side must be a multiple of `q^(s-1)`. But the Euler operator
`f -> (s-1)f-qf'` has zero coefficient at that very monomial, and
`q^s v'` also has zero coefficient there. The putative multiple is therefore
zero. Solving the resulting polynomial Euler equation gives exactly

\[
f=sq^{s-1}v+cq^{s-1},\qquad c\in K.
\]

This argument does not require a degree bound for `f` or `u`.

**The first gate bounds the transverse degree.** The leading `p`-degree
piece of `T3(H,A)` vanishes for two powers of `Q`. At the next possible
degree, `mu+s-4`, only the pairs `(H_0,A_1)` and `(H_1,A_0)` contribute.
The diagonal summand `cQ^(s-1)` gives zero. Direct falling-factorial expansion
of the two remaining terms gives

\[
\boxed{
[p^{\mu+s-4}]\,T_3(H,A)
=\mu s(s-\mu)(s+\mu-3)q^{\mu+s-1}u'''(q).
}
\]

To check the identity for arbitrary `v`, it suffices by linearity to take
`v=q^n`. The coefficient on the left becomes

\[
s\,T_3[(\mu,\mu);(s-1+n,s-1)]
+\mu\,T_3[(\mu-1+n,\mu-1);(s,s)]
=\mu s(s-\mu)(s+\mu-3)n(n-1)(n-2).
\]

Here `T3[(a,b);(c,d)]` means the scalar multiplying
`q^(a+c-3)p^(b+d-3)` for the two monomials. The symbolic identity is verified
independently by `audit_balanced_transverse.py` using a polynomial ring in
the three integer parameters. The exceptional index `mu=2,s=1` has formal
output degree `-1`; the scalar is identically zero and no nonexistent
polynomial output is used in the argument.

Since `u'''` is nonzero, when `mu=2` the only allowed positive values of `s`
are `1,2`. The transverse associated graded core has at most one dimension
at each allowed degree `0,1,2`; therefore the entire core has dimension at
most three. Both `J` and `J^2=H` survive. Indeed every derivative of `J`
of order at least three is in `q` only, whereas `H` has `p`-degree two, so
all odd gates kill `J`; antisymmetry kills `H`; their Poisson bracket is
zero. This proves the quadratic case.

When `mu>=3`, the factor `s+mu-3` is positive for every integer `s>=1`.
The only allowed positive degree is `s=mu`. The same filtration argument
bounds the core by two dimensions, and `1,H` attain that bound. This proves
the remaining case.

## Linear compositions

For `H=aJ+b`, `a!=0`, the third gate is
`T3(H,.)=-a u''' partial_p^3`. Its polynomial kernel consists exactly of the
polynomials of `p`-degree at most two. Every higher odd gate kills this
space, and

\[
D_H=a\bigl((p+u')\partial_p-q\partial_q\bigr)
\]

preserves it. Thus the static and dynamic exact spaces coincide and equal
the stated strip.

If `u'''=0`, this phase diagram does not apply: `J` is quadratic. For
`mu>=2`, Theorem B gives the full stationary tower `K[J]`; for `mu=1`, all
polynomials are exact. The condition `u'''!=0` therefore identifies a real
change in exact observable sectors.

## Scope of the result

The proof is all-degree and applies to every coefficient choice satisfying
the hypotheses. Numerical degree cutoffs are not used. The nonlinear
substitution `p -> p+u(q)/q`, after removing `u(0)`, motivates the family
classically; every assertion about Weyl exactness is proved in the original
flat canonical coordinates. No historical-priority claim is made.
