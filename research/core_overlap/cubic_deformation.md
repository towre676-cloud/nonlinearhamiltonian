# Formal lifting and torsion at the cubic restoring-force boundary

Work over a characteristic-zero field `K` and retain the original flat
Weyl convention. Set

\[
 P=p+q^2,\qquad H_t=P^3+tq^2.
\]

The parameter `t` is formal. A lift has the form
`G(t)=sum_(j>=0)t^jG_j(q,P)`, with every `G_j` an arbitrary polynomial.
No common degree bound on the corrections is assumed. Exactness through
order `s` means every odd Moyal gate on every Hamiltonian iterate
vanishes modulo `t^(s+1)`. Thus a first-order jet passes the complete
dynamic-core definition to first order, not merely a chosen finite
matrix of tests.

The note proves a complete lifting theorem in all degrees and a torsion
law for every sufficiently large finite weight presentation. It uses
ordinary cokernel obstruction classes and Smith modules; neither a new
geometric torsion tensor nor historical priority is claimed.

## Exact operators and the initial core

In the polynomial coordinate ring `K[q,P]`, chain rule gives

\[
 \begin{aligned}
 D_t&=-3P^2\partial_q+2tq\partial_P=D_0+tD_1,\\
 C&=C_3=-6\partial_q^3
       -36P\partial_q\partial_P^2-36\partial_q\partial_P,\\
 C_5&=-360\partial_q\partial_P^4.
 \end{aligned}                                                   \tag{CD1}
\]

All odd gates above fifth order vanish because `H_t` has degree six in
the original affine variables. The quadratic perturbation contributes
no gate. These formulas analyze the original gates; they do not replace
the original flat Moyal product by a flat product in `(q,P)`.

The useful commutator identity is

\[
 [C,D_0]=432P(1+P\partial_P)\partial_q^2.                       \tag{CD2}
\]

Indeed, put `B=P partial_P^2+partial_P`. Then
`C=-6 partial_q^3-36B partial_q`, while
`[B,P^2]=4P(1+P partial_P)`. The polynomial operator
`P(1+P partial_P)` is injective, since it maps `P^n` to
`(n+1)P^(n+1)`.

Consequently `CG=CD_0G=0` forces `G_qq=0`. Write
`G=q b(P)+f(P)`. The remaining static equation is
`-36(Pb''+b')=0`, so `b` is constant. Conversely `f(P)` is stationary
under `D_0`, all gates kill it, and `D_0q=-3P^2` is such a stationary
observable. This gives the all-degree identity

\[
 \boxed{\mathcal D_\infty(H_0)=\ker C\cap\ker(CD_0)
                 =K[P]+Kq.}                                  \tag{CD3}
\]

## Complete classification of liftable initial observables

**Theorem CD.** Within the initial core (CD3), the initial values that
admit first-order exact jets are precisely

\[
 J_1=\operatorname{span}_K\{1,P,P^3\}.
\]

The initial values admitting second-order exact jets, and those
admitting full formal exact lifts, are precisely

\[
 \boxed{J_2=J_\infty=\operatorname{span}_K\{1,P^3\}.}          \tag{CD4}
\]

Thus first-order liftability has dimension three, while second-order
and formal liftability have dimension two. The initially active
observable `q` fails at first order. The stationary observable `P`
passes first order but has a choice-independent second-order
obstruction. The initial Hamiltonian `P^3` has the exact lift `H_t`.

### Necessity at first order

Let `G_0=f(P)+alpha q` and suppose `G_0+tG_1` is a first-order exact
jet. The static equation gives `CG_1=0`. The first derivative gate is

\[
 CD_0G_1=-CD_1G_0=72(Pf'''+f'').                              \tag{CD5}
\]

Apply (CD2), using `CG_1=0`. Its right side is independent of `q`.
Injectivity of `P(1+P partial_P)` implies `partial_q^2G_1` is
independent of `q`, so `G_1` has `q` degree at most two. Write
`G_1=q^2a(P)+qb(P)+g(P)`. The coefficients of `q` and of the constant
in `CG_1=0` imply separately `(Pa')'=0` and `(Pb')'=0`. Polynomiality
forces `a,b` to be constants. Thus

\[
 G_1=a q^2+\beta q+g(P),\qquad
 Pf'''+f''=12aP.                                             \tag{CD6}
\]

Integrating `(Pf'')'=12aP` gives `Pf''=6aP^2+c`. The possible `c/P`
term in `f''` is excluded by polynomiality. Therefore

\[
 f(P)=aP^3+bP+c_0.
\]

To remove the remaining initial direction `alpha q`, use the second
derivative gate. For every polynomial `X`,

\[
 CD_0^rX\in P^{2r-1}K[q,P]\quad(r\ge1).                      \tag{CD7}
\]

This follows from `D_0^r=(-3)^rP^(2r) partial_q^r` and (CD1): the two
`P` derivatives in `C` are accompanied by a factor of `P`, and the
one-derivative term removes at most one power. In particular constant
coefficient extraction annihilates `CD_0^2X` for every polynomial
correction `X`. But direct differentiation gives

\[
 CD_t^2q=432t.                                               \tag{CD8}
\]

The first variation of `CD_t^2 f(P)` is zero: its only nonzero
intermediate expression is `D_0D_1f=-6P^2f'`, which has no `q`
dependence. Hence constant coefficient extraction at this depth gives
the obstruction `432 alpha`. Thus `alpha=0`. This necessity argument
allows every polynomial degree in `G_1`.

### First-order sufficiency and the delayed obstruction

Constants and `P^3` have exact lifts `1` and `H_t`. For the remaining
direction `P`,

\[
 D_tP=2tq,\qquad D_t^2P=-6tP^2,\qquad
 D_t^3P=-24t^2qP.                                          \tag{CD9}
\]

The first three iterates pass both gates modulo `t^2`; every subsequent
iterate has order at least two in `t`. Thus `P` itself is a valid
first-order lift for the full dynamic-core definition. However,

\[
 \boxed{CD_t^3P=864t^2.}                                    \tag{CD10}
\]

The factor is `864`, with the conventions (CD1); it follows from
`C(qP)=-36`. For comparison, the simpler first-order failure is
`CD_t(P^2)=-144t`.

Every first correction to `P` differs from zero by an element of
`ker L_0=K[P]+Kq`, where `L_0` includes all retained gates and depths.
For any such difference `Z`, the first variation of `CD_t^3Z` is zero.
For `Z=f(P)` the only potentially nonzero term is `CD_0^2D_1f`, and
`D_0^2(qf')=0`. For `Z=q`, the only surviving intermediate term is a
multiple of `P^3`, again killed by `C`. Hence the order-two constant
residual in (CD10) is independent of the choice of first lift.

Finally (CD7) with `r=3` shows that `CD_0^3G_2` is divisible by `P^5`
for any polynomial second correction, so it cannot cancel the
constant `864`. This proves that `P` cannot lift through second order.
Subtracting a multiple of the exact lift `H_t` and a constant proves
the necessity of (CD4) for every initial element of `J_1`. Its
sufficiency follows from the explicit constant/Hamiltonian lifts.
No convergence or uniformly bounded degree of a formal series has
been used.

## A parameter-torsion law for every finite weight presentation

Let

\[
 V_N=\operatorname{span}_K\{q^aP^c:a+2c\le N\},\qquad N\ge6.
\]

For the following presentation only, restrict the source to
`K[t] tensor V_N` and retain the complete polynomial outputs of

\[
 M_N(t)G=(CD_t^rG,C_5D_t^rG)_{r=0}^3.                        \tag{CD11}
\]

Choose the target basis as the union of all monomials appearing in
these eight polynomial outputs of the declared source basis. No
output is projected back into `V_N`. Let `s_N=dim V_N` and let `m_N`
be the target dimension. Their values are
`s_(2d)=(d+1)^2`, `s_(2d+1)=(d+1)(d+2)`; `m_N` is determined by the
declared full output population.

**Corollary CT.** For every `N>=6`, put `d=floor(N/2)`. The nonzero
Smith factors of `M_N(t)` consist of `s_N-2-d` units, `d-1` copies
of `t`, and one copy of `t^2`. There are two zero source columns.
Equivalently,

\[
 \boxed{\operatorname{Tor}_{K[t]}\operatorname{coker}M_N(t)
    \cong K[t]/(t^2)\oplus\big(K[t]/(t)\big)^{d-1}.}         \tag{CD12}
\]

The free cokernel rank is `m_N-s_N+2`. This is a theorem for every
declared weight bound `N>=6`, not a claim extrapolated from computed
matrices and not a diagonalization of an undeclared infinite matrix.

**Proof.** The cubic restoring-force theorem gives
`ker M_N(t)=span{1,H_t}` for every nonzero scalar `t`, also after
extension to an algebraic closure; its sharp stopping rule uses both
gates through depth three. The two polynomials belong to the source
for every `N>=6`. At `t=0`, (CD3) gives a kernel of dimension `d+2`.
Consequently the generic rank is `s_N-2`, and the rank at zero is
`s_N-d-2`. No nonunit Smith factor can have a root away from zero,
since it would force a rank drop there. Therefore exactly `d`
nonunit factors are powers of `t`; all remaining nonzero factors
are units. There are two zero factors from the generic kernel.

The first-order and second-order lifting theorem determines those
exponents. In Smith coordinates, each zero factor contributes one
freely liftable initial value; a factor `t^e` contributes a nonzero
initial value through first order exactly when `e>=2`, and through
second order exactly when `e>=3`. The first-order initial space has
dimension three, so exactly one exponent is at least two. The
second-order initial space has dimension two, so none is at least
three. Thus the exponents are `1,...,1,2` as asserted.

This application of Theorem CD to the finite source is legitimate in
both directions. Global necessity allows all corrections, and hence
also corrections in `V_N`; the first-order lifts `P`, `1`, and
`H_t=P^3+tq^2` lie in `V_N`, as do the exact second-order lifts.
Smith source/target changes are invertible over `K[t]`, so they do
not change the dimensions of these spaces of liftable initial values.

The module torsion is ordinary algebraic torsion for the specified
eight-output presentation. Invertible source and target changes
preserve it. Its free part depends on the target population; no
canonical invariance under undeclared gate presentations or nonlinear
changes of the flat product is asserted.

## Verification and relation to the quadratic boundary

There is an exact quantum-shear explanation of the two gates. Let
`sigma` be classical substitution `p -> p+q^2`, let

\[
 R_\hbar=\exp\!\left(-\frac{\hbar^2}{12}\partial_P^3\right),
\]

and use the quantum canonical shear formula from `canonical_bridge.md`.
The quantum shear `sigma R_hbar` sends the base Hamiltonian
`p^3+tq^2` to `H_t-hbar^2/2`. The discrepancy is central and therefore
does not change the Hamiltonian commutator. In `(q,P)` the full Moyal
derivation is consequently

\[
 R_\hbar\left(D_t+\frac{\hbar^2}{4}\partial_q^3\right)
 R_\hbar^{-1}
 =D_t-\frac{\hbar^2}{24}C+
            \frac{\hbar^4}{1920}C_5.                        \tag{CD13}
\]

This identity can also be proved directly, without invoking a
transformation theorem. For `J=partial_P^3`,

\[
 [J,D_t]=-18(P\partial_q\partial_P^2+\partial_q\partial_P),
 \qquad [J,[J,D_t]]=-54\partial_q\partial_P^4,
 \qquad [J,[J,[J,D_t]]]=0.                                  \tag{CD14}
\]

The truncated Baker--Campbell--Hausdorff expansion gives (CD13),
since `J` commutes with `partial_q^3`. In the earlier quadratic
composition, the base Hamiltonian has no intrinsic third gate and
the corresponding second nested commutator is already zero; only
the transformed third gate remains. Here the fifth gate is the
second nested gauge correction. These gauge formulas are established
quantum canonical machinery applied to this family. The new lifting
statements concern the separate restoring parameter `t`; they do not
assert that an ordinary nonlinear substitution preserves flat Moyal
exactness on every observable.

Run `python3 -B research/core_overlap/cubic_deformation.py`. The
checker uses exact rational polynomial arithmetic, computes all
outputs, constructs Smith certificates in weights six, eight, and
ten, and replays the matrices and both polynomial inverses. A complete
weight-six certificate is retained in the receipt, together with a
forgery-rejection check. Separate sparse original-coordinate
transvectants verify 512 gate/iterate identities. These finite checks
and 405 exact BCH-commutator calibrations check the written universal
identities.

The earlier family `P^2+tq^2/2` had a seven-dimensional first-order
initial space and a six-dimensional formally liftable space. Here the
cubic composition reduces those dimensions to three and two. In both
families one stationary initial direction has a delayed second-order
obstruction, reflected by a `t^2` factor; the remaining lost tower
directions have first-order factors. The cubic also destroys the
initial active direction `q` at first order. This is a concrete
comparison of exact-sector deformation mechanisms, rather than a new
name for the Moyal bracket defect.
