# Deformation obstructions and a genuine torsion module of exact observables

This note supplies an obstruction theory with an explicit all-degree
calibration. It uses the fixed original flat Weyl product. It does not
define a new Nijenhuis or Haantjes tensor. The cokernel and Smith module
below are ordinary algebraic constructions; their application to lifting
exact Hamiltonian sectors is the claim being developed here. Historical
priority is not established.

## Finite stopping operators and lifting classes

Let `P` be an observable vector space over a characteristic-zero field
`K`, let `t` be a formal parameter, and let `H_t` be a family. Suppose a
proved finite stopping rule identifies exact persistence in this family
with the kernel of

\[
 L_t:P[[t]]\longrightarrow Y[[t]],\qquad
 L_t=\sum_{i\ge0}t^iL_i.                                      \tag{DO1}
\]

The target `Y` is a finite direct sum of full polynomial output spaces,
one for each retained gate and Hamiltonian depth. Outputs are not
projected into the candidate input space. If the stopping theorem is
only known over `K(t)`, its extension to `P[[t]]` must be justified; it
must not be inferred merely from pointwise numerical stabilization.

Given `G_0,...,G_(n-1)` with `L_t sum_(j<n)t^jG_j=0 mod t^n`, put

\[
 b_n=-\sum_{i=1}^nL_iG_{n-i},\qquad
 \operatorname{ob}_n=[b_n]\in\operatorname{coker}L_0.             \tag{DO2}
\]

The jet extends through order `n` exactly when `ob_n=0`: its only new
equation is `L_0G_n=b_n`. A solution `G_n` is a primitive for this
linear equation; a functional `ell` with `ell L_0=0` and `ell(b_n)!=0`
is an independently checkable obstruction. At orders above one the
class is generally relative to the preceding jet. Independence from
lower-jet choices requires a separate argument, supplied below in the
calibration. No differential with square zero is asserted or needed.

The construction has an elementary naturality law. Under invertible
formal source and target changes `T_t,S_t`, replace
`L_t` by `L'_t=S_tL_tT_t^(-1)` and the lower jet by the corresponding
jet of `T_tG_t`. Then `ob_n` maps to `S_0 ob_n` in the naturally
identified cokernel. Indeed, multiplying a residual starting in order
`n` by `S_t` changes its leading coefficient by `S_0`; truncating the
transformed source jet changes that coefficient only by `L'_0` of a
source correction. Thus solvability and a nonzero obstruction are
independent of bases. Affine symplectic coordinate changes in the
original flat Weyl convention are admissible source/output changes.
Arbitrary nonlinear substitutions with the flat product retained are
not automatically admissible.

In a finite polynomial parameter problem, `L_t` becomes a matrix over
`K[t]`. Its cokernel can have actual module torsion. Smith factors then
measure delayed formal lifting failure. This is stronger than recording
only the dimension of a specialized kernel. A finite input restriction
alone never establishes an all-degree obstruction; the coefficient
functionals in the next theorem do.

## A complete lifting theorem at the quartic oscillator boundary

Put

\[
 Q=p+q^2,\qquad H_t=Q^2+\frac t2q^2,
 \qquad V=\operatorname{span}_K\{1,q,Q,q^2,qQ,Q^2\}.             \tag{DO3}
\]

Here the letter `V` denotes the six-dimensional observable space, not
an additive potential. In the polynomial coordinate ring `K[q,Q]`,

\[
 D_t=-2Q\partial_q+tq\partial_Q=D_0+tD_1,
 \qquad C_3=-12\partial_q\partial_Q^2=:C.                      \tag{DO4}
\]

These are exact rewritings of the original-coordinate operators, not a
replacement of the original flat Moyal product. The Hamiltonian has
degree four in `(q,p)`, so all odd gates above `C3` vanish identically.
Use

\[
 L_tG=(CG,CD_tG,CD_t^2G,CD_t^3G).                             \tag{DO5}
\]

For this family the oscillator theorem gives a uniform depth-three
stopping rule. At `t=0` the sharper depth-two rule follows directly
from the monomial computation below. The proof here also establishes
the lifting assertions without assuming a formal extension of a
pointwise stopping theorem: necessity uses only (DO5), first-order
sufficiency uses the explicit derivative identity in (DO9), and every
surviving second-order initial element has a constant exact lift in `V`.

**Theorem DO.** At `t=0`,

\[
 \mathcal D_\infty(H_0)=K[Q]+\operatorname{span}_K\{q,qQ,q^2\}.
                                                                    \tag{DO6}
\]

Consider any `G_0` in this initial core. Corrections at each order are
allowed to be arbitrary polynomials, with no common degree bound.

* A first-order exact jet `G_0+tG_1` exists precisely when
  `G_0 in V+KQ^3`, a seven-dimensional space.
* A second-order exact jet `G_0+tG_1+t^2G_2` exists precisely when
  `G_0 in V`.
* A full formal exact lift exists precisely when `G_0 in V`; a constant
  lift already works there.

The extra cubic passes the first lifting step but has a choice-independent
second-order obstruction. The homogeneous cubic gate matrix has Smith
invariant factors `1,1,1,t^2`, so its cokernel is `K[t]/(t^2)`.

### Initial core and the protected exact lifts

For every monomial,

\[
 CD_0^r(q^aQ^c)
 =-12(-2)^r(a)_r(a-r)(c+r)_2
      q^{a-r-1}Q^{c+r-2}.                                  \tag{DO7}
\]

A term with a zero coefficient is omitted before interpreting its
exponents. For fixed `r`, nonzero monomial images are distinct.
The simultaneous kernel for `r=0,1,2` is exactly (DO6): `a=0` permits
every `Q^c`; with `a>0`, the only survivors are `q,qQ,q^2`.
This proves (DO6) directly, including all input degrees. Each polynomial
in `V` has total degree at most two in `(q,Q)`, is killed by `C`, and
`D_t` preserves that total degree. Therefore `V` consists of exact
observables for every `t` and supplies constant formal lifts.

### First-order obstructions in every higher tower degree

It suffices to start with `G_0=f(Q)`, since the remaining protected
directions have constant lifts. The static first-order condition is
`CG_1=0`, whence

\[
 G_1=a(q)+Qb(q)+g(Q).
\]

The coefficient of `t` in `CD_t(G_0+tG_1)` is

\[
 48b''(q)-12f'''(Q).                                      \tag{DO8}
\]

This vanishes only when `f'''` is constant. Thus `deg f<=3`, without
any degree restriction on the correction `G_1`. Conversely, the cubic
has the first-order lift

\[
 \widehat G_t=Q^3+\frac34tq^2Q,
 \qquad D_t\widehat G_t=\frac34t^2q^3,
 \qquad L_t\widehat G_t=(0,0,0,-432t^2).                    \tag{DO9}
\]

The derivative identity proves that every further iterate has order
at least two in `t`, so this is a first-order jet for the complete
dynamic-core definition, not just for the four retained tests. This
proves the seven-dimensional first-order statement. For an
explicit dual certificate, if `n>=4` define on four polynomial outputs

\[
 \ell_n(y)= [Q^{n-3}]y_1+
       \frac{2(n-1)}{n-3}[qQ^{n-4}]y_0.                   \tag{DO10}
\]

For every polynomial `X`, `ell_n(L_0X)=0`. Only the input monomial
`q^2Q^(n-2)` can contribute to either extracted coefficient; its two
coefficients are `48(n-1)(n-2)` and `-24(n-2)(n-3)`, which cancel.
For the first-order target of `Q^n`, however,

\[
 \ell_n(-L_1Q^n)=12n(n-1)(n-2)\ne0.                      \tag{DO11}
\]

The functional is valid on the entire polynomial output space. It is
not a certificate derived from a truncated kernel search.

### The cubic fails at second order, independently of the first lift

Every first correction to `Q^3` is
`G_1=(3/4)q^2Q+Z`, where `Z in ker L_0`, hence `Z` lies in (DO6).
The coefficient of `t` in `CD_t^3Z` is zero for every such `Z`.
It vanishes on `V` because all of `V` is protected. For `Z=f(Q)`, the
only potentially nonzero term is `CD_0^2D_1f`, and
`D_0^2(qf')=0`. This proves independence from the first-lift choice.

By (DO9), the third-depth output has residual `-432t^2`. On the other
hand `CD_0^3X` is divisible by `Q` for every polynomial `X`: applying
`D_0^3` introduces `Q^3`, and `C` removes at most two `Q` factors.
Consequently constant-coefficient extraction in the third-depth
output annihilates `L_0X`, but evaluates the residual to `-432`.
No polynomial second correction can remove it. Multiplying by the
initial cubic coefficient proves the second-order assertion for all
initial observables. The protected constant lifts then prove the full
formal statement.

### An exact Smith certificate for the delayed cubic obstruction

On homogeneous cubics, the full output at each depth is a constant in
`q,Q`; thus no output is discarded. In the source basis
`(q^3,q^2Q,qQ^2,Q^3)`, (DO5) is

\[
 M(t)=\begin{pmatrix}
 0&0&-24&0\\
 0&96&0&-72t\\
 -576&0&336t&0\\
 0&-1920t&0&1008t^2
 \end{pmatrix}.                                          \tag{DO12}
\]

Let `x=(x_a,x_b,x_c,x_d)` be source coordinates and let `y=Mx`.
Invertible polynomial target operations give

\[
 \left(-\frac{y_0}{24},
 -\frac{y_2+14ty_0}{576},
 \frac{y_1}{96},
 -\frac{y_3+20ty_1}{432}\right)
 =\left(x_c,x_a,x_b-\frac34tx_d,t^2x_d\right).             \tag{DO13}
\]

The source change `(x_c,x_a,x_b-(3/4)tx_d,x_d)` is also invertible over
`K[t]`. Hence (DO13) is the Smith form `diag(1,1,1,t^2)`. The checker
stores both transformation matrices and both polynomial inverses,
then replays all matrix products and recomputes `M` from the gate
operators. It also rejects an edited matrix. The literal module
torsion records the two-stage failure of the extra cubic; it is not a
claim that the existing notion of algebraic torsion is new.

## The entire graded torsion module

The cubic is the only degree with a delayed second-order obstruction.
The observation map also gives a complete infinite graded module
classification. Let `P_n=K[q,Q]_n` be the homogeneous degree-`n` space.
For `n>=3`, use the explicitly declared presentation

\[
 M_n(t):K[t]\otimes P_n\longrightarrow
       \big(K[t]\otimes P_{n-3}\big)^4,
 \qquad G\longmapsto (CG,CD_tG,CD_t^2G,CD_t^3G).             \tag{DO14}
\]

Each target summand retains every monomial of output degree `n-3`.
The target is assigned grade `n`; this compensates for the operator's
degree shift. Source degrees at most two have zero target and do not
contribute to the cokernel under this convention.

**Corollary GT.** Over any characteristic-zero field `K`,

\[
 \operatorname{coker}M_3\cong K[t]/(t^2),\qquad
 \operatorname{coker}M_n\cong
 K[t]^{3n-9}\oplus K[t]/(t)\quad(n\ge4).                    \tag{DO15}
\]

Consequently, for the graded direct-sum map in (DO14),

\[
 \boxed{\operatorname{Tor}_{K[t]}\operatorname{coker}L
  \cong \big(K[t]/(t^2)\big)_{\mathrm{grade}\ 3}
       \oplus\bigoplus_{n\ge4}
                 \big(K[t]/(t)\big)_{\mathrm{grade}\ n}.}    \tag{DO16}
\]

**Proof.** The cubic case is the explicit Smith certificate. For
`n>=4`, (DO7) shows `ker M_n(0)=KQ^n`, so the rank at zero is `n`.
For any nonzero scalar `t`, including over an algebraic closure, the
static kernel in degree `n` has basis
`q^n,q^(n-1)Q,Q^n`. The next gate sends the latter two elements to

\[
 CD_t(q^{n-1}Q)=48(n-1)(n-2)q^{n-3},\qquad
 CD_t(Q^n)=-12tn(n-1)(n-2)Q^{n-3}.                           \tag{DO17}
\]

Their outputs are independent because `n>=4`. Their coefficients
must therefore vanish. The remaining direction is removed by

\[
 CD_t^2(q^n)=-96n(n-1)(n-2)q^{n-3}\ne0.                    \tag{DO18}
\]

Thus `M_n(t)` has full column rank `n+1` at every nonzero parameter.
Smith normal form over the PID `K[t]` exists. Every nonunit invariant
factor can have roots only at zero, since any other root over the
algebraic closure would produce a rank drop there. The rank drop at
zero is exactly one, hence the invariant factors consist of `n`
units and a single `t^e`, up to units, with `e>=1`.

If `e>=2`, the Smith source change would give a polynomial first-order
lift of a nonzero vector spanning `ker M_n(0)=KQ^n`: choose the last
Smith coordinate constant and the unit coordinates zero. Its residual
would be divisible by `t^2`. But (DO10)--(DO11) exclude such a lift.
Therefore `e=1`. The free cokernel rank is the number of target rows
minus columns, `4(n-2)-(n+1)=3n-9`. This proves (DO15) and taking the
graded direct sum proves (DO16).

This is a classification of ordinary algebraic torsion for the
specified finite-depth observation presentation. Its free summands
depend on the declared target. Invertible source and target changes
preserve its Smith factors; no invariance under undeclared changes
of the gate presentation or nonlinear flat-product substitution is
asserted. The all-degree lifting theorem above is independent of a
candidate degree cutoff and independently confirms the two distinct
obstruction orders represented in (DO16).

## Verification and boundary

Run `python3 -B research/core_overlap/deformation_obstructions.py`.
The checker uses exact standard-library rational polynomial arithmetic
in `(q,Q,t)`, checks the Smith certificates without elimination, verifies
the universal-order symbolic identities and finite calibrations, and
compares 400 original-chart gate/iterate calculations using the separate
sparse transvectant engine. All polynomial outputs are retained.
In degrees four through nine it constructs and replays rectangular
Smith certificates with polynomial inverses; complete certificates for
degrees four and six are retained in the receipt. The proof above,
rather than these finitely many matrices, establishes (DO16).

The proof establishes the all-degree assertions. Neither the finite
calibrations nor the cubic Smith matrix alone proves absence of
higher-degree corrections; that follows from (DO8), (DO10), and the
divisibility argument. The construction concerns formal exact
observables, not convergence of a formal lift, Hilbert-space operator
domains, or a new geometric tensor.
