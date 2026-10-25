# Pure total tops with unequal perfect-power transverse tops

This note uses the flat Weyl convention of the compendium,
`D_H G = H_q G_p - H_p G_q`, and the polynomial dynamic core
`D_infinity(H) = intersection ker T_k(H,D_H^j ·)` for odd `k >= 3`, `j >= 0`.
The coefficient field has characteristic zero. The statements below concern
these fixed canonical coordinates; arbitrary nonlinear canonical substitutions
are not claimed to preserve Weyl exactness.

## A counterexample to the remaining pure-top conjecture

Put

\[
G=qp+q^3,\qquad
H=qG^2=q^3p^2+2q^5p+q^7.
\]

The total top of `H` is the pure seventh power `q^7`. Its transverse, or
`p`-degree, top is `q^3 p^2`, precisely one of the perfect-power exceptions
left open in Theorem T. Nevertheless

\[
\{H,G\}=H,\qquad T_k(H,G)=0\quad(k\ge3).
\]

For the gate identity, every derivative of `G` of total order at least three is
purely in `q`, whereas `H` has `p`-degree two. Thus the sole possibly nonzero
summand of `T_k(H,G)` contains `partial_p^k H=0`. Antisymmetry gives
`T_k(H,H)=0`, and `{H,H}=0`; consequently `G` survives every repeated bracket.
In particular, this is an **active** exact observable, not only a stationary
partner. The all-degree dimension argument below proves

\[
\boxed{D_\infty(H)=\operatorname{span}_K\{1,H,G\}.}
\]

This disproves the unrestricted pure/near two-root conjecture as it was stated
in `DYNAMIC_CORE_RESULTS.md` at commit `e91e14d`. It does not contradict its
proved Theorems B, Q, Q', or the restricted Theorem T.

## Complete classification of the unequal perfect-power exception

**Theorem.** Suppose the total top of a polynomial `H(q,p)` is `c q^d`, with
`d >= 3`, and the `p`-degree top is

\[
F=\alpha\,p^s(q+\gamma)^r,
\qquad \alpha\ne0,\quad r,s\ge2,\quad r\ne s.
\]

Set `t=q+gamma`. Then the following classification holds.

If `s >= 3`, the core is `span{1,H}`. If `s=2` (necessarily `r>=3`), the core
is also `span{1,H}` except for the following explicitly recognizable family:

\[
\begin{aligned}
J&=tp+u(t),\
H&=t^{r-2}\bigl(a_2J^2+a_1J+a_0\bigr)+\beta J+\delta,
\qquad a_2\ne0,\quad u\in K[t],\quad \deg u\ge3.
\end{aligned}
\]

An additive constant of `J` may be removed and absorbed into the displayed
parameters. For this family,

\[
D_\infty(H)=\operatorname{span}_K\{1,H,J\},\qquad
\{H,J\}=(r-2)(H-\beta J-\delta).
\]

The parameters do not impose an artificial degree bound. This is a family of
arbitrarily high total degree and a complete classification under the stated
unequal perfect-power transverse hypothesis. Historical priority is not claimed.

### Proof

**Transverse filtration.** Filter by degree in `p`. The top of `D_H` has
`p`-degree shift `s-1`; the top of `T_k(H,·)` has shift `s-k` because the two
arguments receive exactly `k` derivatives in `p` in each summand. Therefore
the transverse top of a core element lies in `D_infinity(F)`. This remains
valid for the nonnegative weight `(0,1)`; finite-dimensional filtered pieces
are not required. All polynomials have finite transverse degree, and the
usual leading-component comparison applies separately to each identity.

After translating `q`, `F=alpha t^r p^s`. The already proved unequal monomial
classification (Theorem M) gives

\[
D_\infty(F)=\operatorname{span}_K\{1,tp,F\}.
\]

It follows directly, by subtracting a multiple of `H` and descending in
transverse degree, that `dim D_infinity(H)<=3`. At transverse degree zero the
core consists only of constants. If a third element exists, normalize its
transverse top and subtract a multiple of `H` to write it

\[
J=tp+u(t),\qquad u\in K[t].
\]

The core is invariant under `D_H`, so

\[
\{H,J\}=aH+bJ+c.
\]

The coefficient of `p^s t^r` on the left is `(r-s)alpha`; hence
`a=r-s !=0`.

**The gate removes all `s>=3` cases.** Direct differentiation gives

\[
T_3(H,J)=-u'''(t)\,\partial_p^3H.
\]

If `s>=3`, this forces `deg u<=2`. But if `deg u<=2`, `J` is quadratic.
Since the total top of `H` is `c q^d`, comparison of total degree `d` in
`{H,J}=aH+bJ+c` gives `a=d`: the top term is
`q H_q=d c q^d`, and all contributions from lower total components of `H`
have smaller degree. On the other hand the pure total top implies `d>r+s`,
because `F` has a nonzero mixed monomial of degree `r+s`. This contradicts
`a=r-s`. Thus no third element exists for `s>=3`. The same comparison proves
`deg u>=3` whenever a third element exists for `s=2`.

**Integrate the closure relation for `s=2`.** Here `a=r-2>=1`. On the Laurent
polynomial algebra `K[t,t^{-1},J]`, the derivation

\[
H\longmapsto\{H,J\}
=tH_t-(p+u')H_p
\]

is `t partial_t` at fixed `J`. Thus

\[
H+\frac b a J+\frac c a=t^a P(J),\qquad P\in K[J].
\]

Since `H` has `p`-degree two, `P` has degree two and nonzero leading
coefficient. Set `beta=-b/a`, `delta=-c/a`. This is the displayed family.
Conversely, its closure identity follows by direct differentiation. Every
odd gate kills `J` since `H` has `p`-degree two; every odd gate kills `H` by
antisymmetry. Therefore the span of `1,H,J` is an invariant exact sector.
The transverse upper bound makes it the whole core. This proves the theorem.

## An exact decision test in the original polynomial coefficients

Write `H=A(t)p^2+B(t)p+C(t)` with `A=alpha t^r`, `r>=3`, and put `a=r-2`.
Choose the harmless normalization `u(0)=0`. The coefficient of `p` in the
closure identity is equivalent to

\[
2\alpha t^r u'=tB'-(a+1)B-bt.
\]

Its coefficient of `t` fixes `b=-a[t]B`. The numerator must be divisible by
`t^r`; if so, integration uniquely determines the polynomial `u` with
`u(0)=0`. Finally test whether

\[
tC'-Bu'-aC-bu
\]

is constant. This finite calculation is necessary and sufficient. It neither
fits a bounded ansatz nor infers an all-degree claim from a finite matrix.
The accompanying checker replays the closure identity and every nonzero odd
gate using independent PBW operator arithmetic.

## Why the coordinate mechanism is subtle

The nonlinear triangular substitution `p -> p+u(q)/q` explains the classical
eigenvector form when `u(0)=0`. Its Weyl exactness in this sector follows
from the separate derivative argument above, rather than from a claim that
the Moyal product is covariant under nonlinear canonical maps. For example,
the cubic choice `u=q^3` is outside affine covariance and creates a pure
total top from an unequal transverse monomial.
