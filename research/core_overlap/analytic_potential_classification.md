# Exact classification of cubic-preserving analytic potentials

This note advances the finite stopping theorems in
`depth_finite_determination.md` to an explicit classification of the additive
potential for the algebraic cubic boundary. It uses the original affine
coordinates, the flat Weyl–Moyal gates, real-analytic coefficients and finite
degree in `q`. No external-priority claim is made.

Let `I` be a connected open subinterval of `(0,infinity)`, let
`A=C^omega(I,R)`, and put

\[
 H=q p^{-1/4}+V(p),\qquad D=\{H,\cdot\},\qquad
 W=A\oplus qA,
\]

where `V` is arbitrary in `A` and
`{H,G}=H_qG_p-H_pG_q`. The dynamic core consists of the elements `G` for
which every `T_j(H,D^rG)` vanishes, for odd `j>=3` and every `r>=0`.

## The complete potential theorem

**Theorem AP.** Exactly one of the following alternatives holds.

If there are real constants `c0,a,b,c` with

\[
 \boxed{V(p)=c_0+a p^{-1/4}+b p^{3/4}+c p^{5/2},}       \tag{AP1}
\]

then

\[
 \boxed{\mathcal D_\infty(H)
   =W\oplus\mathbb R\,(H-c_0)^3.}                     \tag{AP2}
\]

For every other analytic potential, `D_infty(H)=W`. These are equalities
in all finite `q` degrees, including when `I=(0,infinity)`. The extra
generator in (AP2) is stationary. The four constants in (AP1) are unique.

The constant shift must be removed before cubing. In general `H^3` is
not a valid replacement for `(H-c0)^3`: their difference contains
`3c0(H-c0)^2`, whose quadratic `q` coefficient need not lie in `W` or in
the core.

In fact the family (AP1) obeys the exact diagnostic
`T3(H,H^3)=-(45/16)c0 p^(-15/4)`, so a nonzero constant shift makes
the unshifted cube fail already at its static third gate.

### Highest-degree exclusion

The strip `W` is invariant under `D` and killed by every odd gate of
order at least three. Suppose that a core element has `q` degree `n>=2`
and highest coefficient `q^n g(p)`, with `g` nonzero. At the highest
output degree the potential contributes nothing, so `T3(H,G)=0` forces

\[
 3F''g'-(n-2)F'''g=0,\qquad F=p^{-1/4}.
\]

Consequently `g` is a nonzero constant multiple of
`p^{-3(n-2)/4}`. The highest coefficient of `DG` is `K_n g`, where

\[
 K_n=\frac{n-2}{3}\frac{FF'''}{F''}-nF'
     =\frac{3-n}{2}p^{-5/4}.                            \tag{AP3}
\]

The equation `T3(H,DG)=0` then forces `K_n'=0`, which is possible only
for `n=3`. In particular there is no core element of `q` degree two,
and every core element has degree at most three. This excludes all
higher degrees directly, without invoking a degree cutoff, a numerical
kernel, or a fifth-gate completeness theorem.

Normalize the cubic coefficient to `g=p^{-3/4}`. Modulo `W`, any
additional core element must therefore have the form

\[
 G=q^3p^{-3/4}+q^2h(p).                                 \tag{AP4}
\]

Two normalized candidates differ by a core element of degree at most
two and hence by an element of `W`. Thus the quotient of the core by
`W` has dimension at most one.

### Necessary and sufficient compatibility equations

Direct third-order differentiation gives

\[
 T_3(H,G)=6F''h'-6V'''p^{-3/4}.
\]

The cubic coefficient of `DG` is zero, and its quadratic coefficient is

\[
 Fh'-2F'h-3V'p^{-3/4}.
\]

Because the core is invariant under `D` and has no degree-two element
outside `W`, a persistent cubic necessarily satisfies

\[
 \boxed{h'=\frac{16}{5}p^{3/2}V''',\qquad
       ph'+\frac12h=3p^{1/2}V'.}                        \tag{AP5}
\]

Conversely, these equations imply `T3(H,G)=0` and `DG in W`. Every
higher odd gate on `G` vanishes because the combined `q` degree of
`H` and `G` is four. The invariance and exactness of `W` therefore
prove that `G` belongs to the full dynamic core. Thus (AP5) is
necessary and sufficient, including for arbitrary analytic `V`.

### Solving the compatibility equation for every analytic potential

The second equation of (AP5), followed by the first, gives

\[
 h=6p^{1/2}V'-\frac{32}{5}p^{5/2}V'''.                 \tag{AP6}
\]

Differentiating (AP6) and substituting back into the first equation
shows that (AP5) is equivalent to

\[
 \boxed{p^4V''''+3p^3V'''-\frac{15}{16}p^2V''
                       -\frac{15}{32}pV'=0.}           \tag{AP7}
\]

This is a regular linear Euler equation on every interval `I` under
consideration. With `x=log p`, its indicial polynomial is

\[
 \nu(\nu-1)(\nu-2)(\nu-3)
 +3\nu(\nu-1)(\nu-2)-\frac{15}{16}\nu(\nu-1)
 -\frac{15}{32}\nu
 =\frac{\nu(4\nu+1)(4\nu-3)(2\nu-5)}{32}.            \tag{AP8}
\]

The four roots are distinct. The complete real-analytic solution
space is consequently the four-dimensional space in (AP1), not merely
the span of a collection of tested monomials. Standard uniqueness for
the regular fourth-order equation extends the local solution throughout
the connected interval.

The constant is recovered intrinsically by

\[
 c_0=\frac{32}{15}
       \left(p^3V'''-\frac{15}{16}pV'+\frac{15}{32}V\right),            \tag{AP9}
\]

which is constant exactly when (AP7) holds. Equivalently `v=V-c0`
satisfies the third-order equation

\[
 v'''-\frac{15}{16}p^{-2}v'
                      +\frac{15}{32}p^{-3}v=0.         \tag{AP10}
\]

The subtraction of `c0` in this last equation is essential. Substitution
in (AP6) now gives

\[
 h=3\left(a p^{-3/4}+b p^{1/4}+c p^2\right)
   =3p^{-1/2}(V-c_0).                                  \tag{AP11}
\]

The cubic and quadratic `q` coefficients of `(H-c0)^3` are exactly
those in (AP4) and (AP11). Its difference from `G` is in `W`, and it is
stationary because it is a power of `H-c0`. This proves (AP2), including
the completeness of both alternatives.

## General cubic-preserving potentials on a regular analytic chart

**Proposition GC.** Let `F,V` be real analytic on a connected interval,
assume `F''` is nowhere zero, and set

\[
 K_3=\frac{FF'''}{3F''}-3F'=\lambda\in\mathbb R.
\]

Choose any nonzero analytic solution `g` of
`g'/g=F'''/(3F'')`; for example a nonzero constant multiple of the
real cube root of `F''`. For

\[
 H=qF+V,\qquad G=q^3g+q^2h+w,\quad w\in W,
\]

membership of `G` in the full dynamic core is equivalent to

\[
 \boxed{h'=L_V:=\frac{gV'''}{F''},\qquad
 Fh'-(2F'+\lambda)h=3gV'.}                              \tag{GC1}
\]

The proof is the same leading-coefficient computation as above.
The first equation says `C3 G=0`. The top coefficient of `DG` is
`lambda g`; therefore the second says `DG-lambda G in W`. This is
sufficient for every iterate and every gate. For necessity,
`DG-lambda G` is a core element of degree at most two. Every such
element is in `W`: a quadratic coefficient is constant by its third
gate, and the next third gate gives its nonzero multiple of
`(F'')^2` unless that constant vanishes. Thus (GC1) is also necessary.
No claim about core elements of higher degree is needed in this
proposition.

Write `B=2F'+lambda`. On a **regular chart** where `F B` is nowhere
zero, (GC1) is a regular fourth-order linear equation for `V`:

\[
 \left(\frac{F L_V-3gV'}{B}\right)'=L_V.              \tag{GC2}
\]

It has a four-dimensional space of real-analytic solutions, and `h` is
uniquely reconstructed from `V`. An equivalent denominator-cleared
expression is obtained by setting

\[
 M=BF'',\qquad Z=g(FV'''-3F''V'):
 \qquad MZ'-M'Z-B^2F''gV'''=0.                         \tag{GC3}
\]

The coefficient of `V''''` in (GC3) is `B F'' F g`, which is nonzero
under the stated chart assumptions. The compatibility system (GC1)
remains meaningful at a zero of `F` or `B`, but the elimination and
four-dimensional regular-chart assertion are not asserted across such
zeros. Analytic continuation and matching there require a separate
argument.

## An active extension with a complete conditional classification

For

\[
 F=a_*p^{-1/4}+b_*p,\qquad a_*\ne0,
\]

one may choose `g=p^{-3/4}` and

\[
 \lambda=-\frac{15b_*}{4},\qquad
 K_n=\frac{a_*(3-n)}2p^{-5/4}
                     -\frac{b_*(7n-6)}4.               \tag{AC1}
\]

The same highest-degree argument forces every core element outside
`W` to have degree three, and the quotient by `W` still has dimension
at most one. Hence the full core is `W` unless there is a global
analytic solution `h` of (GC1), in which case it is

\[
 W\oplus\mathbb R(q^3p^{-3/4}+q^2h).
\]

On every connected regular chart
`F(2F'+lambda)!=0`, exactly a four-dimensional linear space of
potentials admits this additional cubic. This follows from the regular
fourth-order equation (GC2); a closed form or a global classification
across its singular charts is not claimed here. When `b_*!=0`, the
extra quotient is active, with eigenvalue `-15b_*/4`. For the explicit
translation potentials `V=tF+c0`, a representative is
`(q+t)^3p^{-3/4}`, and it is an exact eigenvector with that eigenvalue.

## Exact verification and a rejected potential

`analytic_potential_classification.py` is a standalone standard-library
checker. It implements mixed derivatives and transvectants independently
using rational coefficients, fractional `p` exponents, and formal
coefficient parameters. The generic Hamiltonian in (AP1), its shifted
cube and the compatibility identities are checked coefficient by
coefficient for all parameter values. The indicial factorization and
(AC1) are identities in a formal degree variable, not sampled degrees.
The active translated cubic is checked with formal parameters as well.

The rejected potential `V=p^(7/4)` gives a nonzero (AP7) coefficient
`-21/8`. Its published depth-two sharpness witness

\[
 H=qp^{-1/4}+p^{7/4},\qquad
 G=q^3p^{-3/4}-\frac{21}{25}q^2p^{5/4}
\]

passes `C3`, `C5` and `C3 D` but fails at
`C3 D^2 G=(63/8)p^(-9/2)`. This confirms that the failure is a genuine
compatibility obstruction rather than a missed static gate.

Run `python3 -B research/core_overlap/analytic_potential_classification.py`.
Use `--output PATH` to retain the JSON receipt. The proof above
establishes the all-analytic and all-degree statements; the checker
independently verifies the exact identities used in that proof.
