# Three equations determine the analytic dynamic core

This is a finite-determination bridge between the polynomial dynamic-core
programme on `claude/adoring-ritchie-1hq1kw` and the analytic polygamma
calculations. It concerns the existing flat Weyl–Moyal gates, not a new
torsion operation or a literature-priority claim.

Let `I` be a connected open real interval, let
`A=C^omega(I,R)`, and suppose `F in A` has `F''` nowhere zero. Work in
`A[q]`, with finite degree in `q`. Write

\[
 H=qF(p),\qquad D=\{H,\cdot\},\qquad C_j=T_j(H,\cdot),
\]

with the compendium's affine canonical coordinates and transvectant
convention. The Hamiltonian derivation is
`D(q^c g)=q^c(Fg'-cF'g)`.

**Theorem FD.** The full dynamic core is determined by three equations:

\[
 \boxed{\mathcal D_\infty(qF)
   =\ker C_3\;\cap\;\ker(C_3D)\;\cap\;\ker C_5.}       \tag{FD1}
\]

Thus no gate above fifth order, and no Hamiltonian iterate above the
first, is needed to certify membership. This is an equality in all
finite `q` degrees, not a degree cutoff or a numerical stabilization
criterion. The three equations are individually indispensable across
this class of Hamiltonians.

In particular, with `r=cuberoot(F'')` and

\[
 K_3=\frac{FF'''}{3F''}-3F',
\]

the answer is

\[
 \mathcal D_\infty(qF)=
 \begin{cases}
 A\oplus qA\oplus\mathbb Rq^3r,&K_3\text{ constant},\\
 A\oplus qA,&K_3\text{ nonconstant}.
 \end{cases}                                               \tag{FD2}
\]

The constant case permits an active cubic eigenpartner. The theorem
does not replace the analytic hypotheses by arbitrary smoothness, nor
classify infinite `q` series.

**Analytic continuation extension.** The three-equation equality (FD1)
holds for every real-analytic `F` on a connected interval, including
zeros of `F''`. If `F''` vanishes identically, `H` is quadratic and
both sides are all of `A[q]`. Otherwise choose any open subinterval
where `F''` is nonzero. The proof below excludes every degree other
than zero, one and three on that subinterval, hence everywhere by
analyticity. A surviving cubic is a local eigenvector of `D`; its
analytic identity `DG=lambda*G` extends to the whole interval, and all
higher gates kill it by `q` degree. This proves the equality without
dividing by `F''` at a zero.

For the explicit formula (FD2) across those zeros, a nonzero cubic
coefficient must be a global analytic cube root of a constant multiple
of `F''`, and must obey the eigenvector identity. Such a cube root
exists exactly when every zero of `F''` has multiplicity divisible by
three. Thus the three-equation test is global, while a local cubic
formula may fail to extend through a zero.

## Proof by independent degree sectors

For odd `j`, direct expansion gives

\[
 C_j(q^c g)=(c)_{j-1}q^{c-j+1}
 \left[jF^{(j-1)}g'-(c-j+1)F^{(j)}g\right].             \tag{FD3}
\]

At fixed `j`, different input `q` degrees have different output degrees.
The derivation `D` also preserves each degree. Therefore all three
equations in (FD1) split by `q` degree.

Degrees zero and one are unrestricted, killed by every gate, and
preserved by `D`. For `c>=2`, `C_3(q^c g)=0` is

\[
 3F''g'-(c-2)F'''g=0.
\]

Put `B=|F''|>0`, `delta=sign(F'')`, and
`alpha=(c-2)/3`. A nonzero solution is `g=constant*B^alpha`,
and it never vanishes. Then

\[
 D(q^cg)=q^cgK_c,\qquad
 K_c=\alpha\frac{FB'}B-cF'.                              \tag{FD4}
\]

The equation `C_3D(q^c g)=0` is exactly `K_c'=0`. If all gates
kill this generator, a constant `K_c` makes it an eigenvector of `D`
and automatically proves persistence under every iterate.

At degree two, `K_2=-2F'` is not constant. At degree three, there
are no gates above `C_3`, so precisely the constant-`K_3` possibility
survives. It remains to exclude every `c>=4` using `C_5`.

For `c=4`, fifth order gives `B'B''=0`. Analyticity on the connected
interval implies `B''=0`, so `F` has degree at most three. For any
`c>=4` the latter case is impossible under constant `K_c`: if `F`
is quadratic then `K_c=-cF'` has nonzero derivative, and if
`F=f_3p^3+...` then its rational expression has leading term
`-(8c+2)f_3p^2/3`, which is not constant. An identity on the interval
would be a rational identity, so this leading-term argument applies
even on bounded intervals away from the zero of `F''`.

For `c>=5`, fifth order gives

\[
 BB'''=\beta B'B'',\qquad
 \beta=\frac{5(c-2)}{3(c-4)}>1.
\]

Hence `B''=kappa*B^beta` for a constant `kappa`. If `kappa=0`,
the polynomial case above concludes. Suppose `kappa!=0`. A constant
`K_c` would give

\[
 FB'-aF'B=kB,\qquad a=\frac{3c}{c-2}>0                 \tag{FD5}
\]

for some real `k`. Apply the following incompatibility lemma, using

\[
 1+a(\beta-2)=\frac{8(c+1)}{(c-4)(c-2)}>0.               \tag{FD6}
\]

This excludes every higher degree and proves (FD1) and (FD2).

## Scalar incompatibility lemma

Suppose `B>0`, `F''=delta*B`, `delta in {1,-1}`,
`B''=kappa*B^beta`, `kappa!=0`, `beta>1`, `a>0`, and
`1+a(beta-2)!=0`. Then `FB'/B-aF'` is not constant.

Write `u=B'`, `v=B''`, `w=F'`. If the expression equalled `k`,
then

\[
 Fu-awB=kB.
\]

Differentiate twice, use `v'=beta*vu/B` and `w'=delta*B`,
and eliminate `F`. The exact result is

\[
 Lwv=(3a-1)\delta Bu-(\beta-1)kv,
 \qquad L=a(\beta-1)+2>0.                               \tag{FD7}
\]

Since `v` is nowhere zero, solve this for `w` and differentiate. Using
`w'=delta*B` gives

\[
 [a(\beta-4)+3]Bv=(3a-1)(1-\beta)u^2.                   \tag{FD8}
\]

There is an open subinterval with `u!=0`, since `v` never vanishes.
Differentiate (FD8) there, cancel the nonzero `uv`, and obtain

\[
 (\beta+1)[a(\beta-4)+3]
   =2(3a-1)(1-\beta).
\]

Their difference factors as

\[
 (\beta+5)[1+a(\beta-2)]=0,
\]

contrary to the hypotheses. The argument makes no division by `u`
at a zero, by `F`, by a first-integral constant, or by either factor
in (FD8).

## Sharpness and the distinction from static gate determination

The examples below are on `p>0`, and every power is its positive real
analytic branch.

**The first-step condition is necessary.** For `F=p^2`, `G=q^2`
passes every static gate, while

\[
 C_3DG=-48.
\]

**The fifth-order condition is necessary even after arbitrarily many
third-order tests.** Take `F=p^{-2/5}` and `G=H^4=q^4p^{-8/5}`.
Then `DG=0` and `C_3G=0`, but

\[
 C_5G=-\frac{548352}{625}p^{-7}\ne0.
\]

Thus testing `C_3D^jG=0` for every `j>=0` still does not determine
the true dynamic core.

**The initial third-order condition is necessary.** For `F=p^2`
and `G=H^2=q^2p^4`, the equation `DG=0` makes `C_3DG=0`, and
`C_5G=0`, whereas

\[
 C_3G=48p^3\ne0.
\]

Finally, static exactness has a different universal bound: the full
static partner space is `ker C_3 intersect ker C_5 intersect ker C_7`,
by the complete analytic partner classification. Seventh order really
is required for that static statement: with
`F=p^{8/7}` and `G=q^6p^{-8/7}`,

\[
 C_3G=C_5G=0,\qquad
 C_7G=-\frac{1940889600}{117649}p^{-7}\ne0.
\]

Dynamic persistence lowers the necessary maximum gate from seven to
five. This explains a concrete way in which the analytic coefficient
space and the polynomial programme can share an exact finite stopping
rule even though their static partner spaces differ.

## A sharper two-equation certificate for gamma and polygamma

**Corollary FP.** For `F=log Gamma` or `F=psi^(m)`, `m>=0`,
on `p>0`,

\[
 \boxed{\mathcal D_\infty(qF)
   =\ker C_3\cap\ker(C_3D)=A\oplus qA.}                 \tag{FP1}
\]

This eliminates the fifth-order equation as well. It proves the
dynamic result directly, without first classifying the static partner
space. It still uses all finite `q` degrees with analytic coefficients.

More generally, suppose `F` analytically continues to a genuine
meromorphic pole of integer order `t>=1`,

\[
 F(p)=C_0p^{-t}+\text{a lower-order Laurent part},
 \qquad C_0\ne0,
\]

after shifting the pole to zero. A hypothetical sector with `c>=2`
that passes both equations would make `K_c` constant. But

\[
 K_c(p)\sim\frac{2C_0}{3}
   \big[(c+1)t-c+2\big]p^{-t-1}.                         \tag{FP2}
\]

Its coefficient does not vanish because

\[
 (c+1)t-c+2=(c+1)(t-1)+3>0.
\]

The meromorphic identity theorem transports a supposed constant
identity from the original interval to a punctured neighborhood of the
pole. Equation (FP2) contradicts that identity. No continuation of the
partner coefficient is required. Every polygamma has such a pole,
with `t=m+1` and `C_0=(-1)^(m+1)m!`.

For the logarithmic template
`F=-a log p+b(p)`, `a!=0`, with `b` analytic at zero,

\[
 K_c(p)=\frac{2a(c-2)}{3}\frac{\log p}{p}
   +\left[ca-\frac{2(c-2)b(0)}3\right]\frac1p
   +O(|\log p|+1).                                      \tag{FP3}
\]

At `c=2`, the coefficient `2a/p` is nonzero. At every `c>=3`, the
logarithmic coefficient is nonzero. Thus `K_c` is never constant, which
covers `log Gamma` using its `-log p` singularity. As above, the
potential must have the stated continuation; this is not an assertion
about a real-analytic function with no access to that singularity.

The two-equation conclusion for these pole and logarithmic classes also
holds for `H=qF(p)+V(p)` with **arbitrary analytic `V`**. The
highest `q`-degree of a hypothetical partner still satisfies exactly
the two equations above: the `V` terms lower `q` degree in both
`C_3` and `D`. Thus its degree cannot exceed one. Conversely,
`A+qA` is invariant under `D` and killed by every gate for this
affine-in-`q` Hamiltonian. This extends the polygamma result to an
arbitrary analytic additive potential without a new asymptotic
assumption on that potential.

The real integer pole restriction has content: the fractional power
`F=p^{-2/5}` in the sharpness example admits a stationary fourth-degree
sector through both third-order tests and fails the fifth gate. Thus
the two-equation corollary cannot be extended to all algebraic
singularities.

## Arbitrary additive potentials: a sharp depth-two theorem

**Theorem FA.** Let `F,V` be arbitrary real-analytic functions on a
connected open interval, and let `H=qF(p)+V(p)`. With the same finite
`q`-degree coefficient algebra,

\[
 \boxed{\mathcal D_\infty(H)=
  \ker C_3\cap\ker C_5\cap\ker(C_3D)\cap\ker(C_3D^2).}   \tag{FA1}
\]

Thus an arbitrary analytic additive potential requires at most two
Hamiltonian steps and gates no higher than fifth order. Two steps
really are necessary in this larger class.

**Proof.** First suppose `F''` is not identically zero. Choose an open
subinterval `J` where it is nowhere zero. Let `S_1` be the common
kernel of the first three operators in (FA1). The highest `q`-degree
sector of an element of `S_1`, restricted to `J`, satisfies exactly
the three equations of Theorem FD for `qF`: every `V` contribution
has strictly smaller `q` degree. The proof of FD therefore forces
its degree to be at most three. Analyticity extends the vanishing of
all higher coefficients from `J` to the whole interval.

The strip `W=A+qA` is invariant under `D` and killed by every gate.
Moreover,

\[
 \dim_{\mathbb R}(S_1/W)\le1.                            \tag{FA2}
\]

Indeed, the leading coefficient of a cubic is a scalar multiple of
`cuberoot(F'')` on `J`, hence has at most one free real scalar
globally. The difference of two candidates with equal cubic
coefficient has degree at most two. Its quadratic coefficient is
constant by `C_3G=0`, and `C_3DG=-12(F'')^2` on the generator `q^2`
excludes that coefficient. Thus the difference belongs to `W`.

Now let `G` pass all four equations in (FA1). Then `DG` belongs
to `S_1`: the two third-order equations follow from the last two
conditions on `G`, and `C_5DG=0` automatically because `DG` has
`q` degree at most three. If `G` is not in `W`, (FA2) gives

\[
 DG=\lambda G+w,\qquad \lambda\in\mathbb R,\quad w\in W.
\]

As `W` is invariant, every iterate stays in `S_1`, where the third
gate vanishes; every higher odd gate vanishes by `q` degree. If
`G` is in `W`, persistence already holds. This proves the sufficient
direction. Necessity follows directly from the definition of the core.

If `F''` is identically zero and `V'''` is not, the operator is
`C_3=-V'''*partial_q^3`. Hence its analytic kernel has `q` degree
at most two, is preserved by `D`, and is killed by every higher gate.
If both derivatives vanish identically, `H` is quadratic and every
gate vanishes on all of `A[q]`. These cases finish the proof.

**Exact sharpness witness.** On `p>0`, take

\[
 \begin{aligned}
 H&=qp^{-1/4}+p^{7/4},\\
 G&=q^3p^{-3/4}-\frac{21}{25}q^2p^{5/4}.
 \end{aligned}
\]

Direct rational-power differentiation gives

\[
 \begin{aligned}
 C_3G&=C_5G=C_3DG=0,\\
 DG&=-\frac{168}{25}q^2+\frac{147}{50}qp^2,\\
 C_3D^2G&=\frac{63}{8}p^{-9/2}\ne0.
 \end{aligned}                                          \tag{FA3}
\]

This partner passes every static gate and remains static after one
Hamiltonian bracket, but escapes at the second. Thus the one-step
bound for `qF` cannot be carried unchanged to `qF+V`. The corollary
for gamma and polygamma is stronger because its singularity excludes
the cubic sector before this obstruction can arise.

## Checkers and status

`depth_verify.py` independently expands the differential operators on
sparse fractional-power monomials using rational arithmetic. It checks
the sector formula, all four sharpness examples, the parameter identity
(FD6), a grid of the scalar factors, and the exact pole coefficient in
(FP2), as well as the sharp depth-two additive-potential example.
The separate adversarial audit
checks the formal differential elimination in the lemma.

The proof, rather than the grid, establishes the unbounded-degree
statement. Literature priority has not been established. The argument
extends the analytic qF calculations in the previous research package;
it does not alter the sealed baseline or assume that analytic functions
can be substituted into a polynomial Weyl-ideal receipt.
