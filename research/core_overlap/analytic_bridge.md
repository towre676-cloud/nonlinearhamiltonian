# A rational stopping theorem and an algebraic persistent cubic

This note connects the polynomial affine strips in
`programmes/DYNAMIC_CORE_RESULTS.md` with the analytic `qF(p)` results of
the polygamma programme. All statements use the original affine
coordinates `(q,p)`, the constant-Poisson Moyal product, and finite degree
in `q`. They do not assert covariance of this same product under a
nonlinear canonical substitution. Historical priority is unassessed.

Let `I` be a connected open real interval, `A=C^omega(I,R)`,
`H=qF(p)+B(p)`, and `D={H,·}` with
`{H,G}=H_q G_p-H_p G_q`. Let `C3=T3(H,·)`, using the transvectant
convention of the compendium. Formal Moyal exactness requires every odd
transvectant of order at least three to vanish. Put

\[
\mathcal D_\infty(H)=\{G\in A[q]:T_k(H,D^rG)=0\quad
  (k\ge3\text{ odd},\ r\ge0)\}.
\]

## Rational coefficients: one gate and one bracket suffice

**Theorem A.** Suppose `F` is rational with real coefficients, has no
pole on `I`, and `F''` is nowhere zero on `I`. Let `B` be arbitrary in
`A`. Then, in all finite `q` degrees,

\[
\boxed{\ker C_3\cap\ker(C_3D)
       =\mathcal D_\infty(H)=A\oplus qA.}                 \tag{A1}
\]

Thus the full infinite family of odd gates and repeated brackets has a
uniform stopping rule in this coefficient class: `T3(H,G)=0` and
`T3(H,{H,G})=0` already characterize the core. No degree cutoff on the
observable is present. The polynomial specialization is the affine
strip already classified by Claude's theorem; the uniform two-check
certificate and arbitrary analytic potential `B(p)` are the refinement.

**Proof.** The strip `A+qA` is invariant under `D` and all its elements
pass every odd gate, because the `q` degrees of both `H` and a strip
element are at most one. It remains to exclude `G` of `q` degree `c>=2`
from the left side of (A1).

Write its highest coefficient as `q^c g(p)`, with `g` not identically
zero. The highest `q` coefficient of `T3(H,G)` is

\[
c(c-1)q^{c-2}\,[3F''g'-(c-2)F'''g].                     \tag{A2}
\]

The term `B` contributes only to lower `q` degrees. Let
`r=cuberoot(F'')`, the nonzero real-analytic real branch. Equation (A2)
forces `g=C r^(c-2)` with a nonzero real constant `C`; in particular `g`
is nowhere zero. The highest `q` coefficient of `DG` is

\[
Fg'-cF'g=K_cg,\qquad
K_c=\frac{c-2}{3}\frac{FF'''}{F''}-cF'.                 \tag{A3}
\]

Applying (A2) to `DG` gives
`3c(c-1)F'' g K_c'=0`, whether or not `DG` still has degree `c`.
Consequently `K_c` would have to be constant. We prove this impossible
for rational `F` and every integer `c>=2`.

If `F` has a finite complex pole of order `m>=1`, write
`F=a t^(-m)+O(t^(-m+1))`, where `t=p-p0` and `a!=0`. Then

\[
K_c=\frac23\big[(c+1)m-c+2\big]a\,t^{-m-1}
          +O(t^{-m}).                                   \tag{A4}
\]

The bracket is at least three. Hence `K_c` has a pole and is not
constant. This includes nonreal poles: a rational function constant on
the real interval would be the same constant rational identity over
the complex numbers. If `F` has no finite complex poles, it is a
polynomial. Its degree `n` is at least two since `F''!=0`. If its
leading coefficient is `a`, then

\[
K_c=-\frac23\big[(c+1)n+c-2\big]a\,p^{n-1}
          +O(p^{n-2}),                                  \tag{A5}
\]

again nonconstant. This contradiction proves (A1). Every division was
by a function assumed or proved nonzero on the selected interval.

The numerator of the obstruction `K_c'` is particularly simple:

\[
\begin{split}
3(F'')^2K_c'={}&(c-2)
 \big[F'F'''F''+FF''''F''-F(F''')^2\big]
 -3c(F'')^3.                                             \tag{A6}
\end{split}
\]

This is affine in the integer `c`; equations (A4)--(A5) prove its
nonvanishing uniformly rather than searching over sectors.

**Corollary A.1 (a meromorphic pole suffices).** The same conclusion
(A1) holds if, instead of rationality, `F` has a meromorphic extension to
a connected complex domain containing `I` and at least one finite pole.
The analytic potential `B` still needs to be defined only on `I`.
Indeed, `K_c` is meromorphic on that domain. If it were constant on
`I`, the identity theorem would make it constant meromorphically, in
contradiction to the nonzero pole coefficient (A4). The pole may be
nonreal or outside the interval. No asymptotic estimate at infinity is
required.

Every polygamma `F=psi^(m)`, including digamma at `m=0`, satisfies this
corollary on `p>0`: it is meromorphic with poles of integer order
`m+1` at the nonpositive integers, and `F''=psi^(m+2)` has constant
nonzero sign on the positive axis. Thus

\[
\ker T_3(q\psi^{(m)}+B,\cdot)\cap
\ker[T_3(q\psi^{(m)}+B,D\cdot)]
 =A\oplus qA                                             \tag{A6a}
\]

for arbitrary analytic `B(p)` and every `m>=0`. The standard
polygamma definitions, recurrence and reflection identities are
documented in [NIST DLMF 5.15](https://dlmf.nist.gov/5.15).
Log-Gamma is not meromorphic; its separate asymptotic proof of the same
conclusion is recorded in `depth_finite_determination.md`.

## An explicit algebraic family across the boundary

**Theorem B.** On `p>0`, let

\[
F(p)=a p^{-1/4}+bp,\quad a\ne0,\qquad
H=qF(p),\qquad X=q p^{-1/4},\qquad G=X^3.
\]

Then

\[
\boxed{\frac{[H,G]_\star}{i\hbar}=\{H,G\}
      =-\frac{15b}{4}G,\qquad
 D^jG=\left(-\frac{15b}{4}\right)^jG.}                  \tag{A7}
\]

In particular `b!=0` gives a completely explicit algebraic active
persistent cubic outside the rational coefficient class of Theorem A.
It replaces the earlier implicit autonomous-ODE examples with elementary
fractional powers. Its full finite-`q`-degree core is

\[
\boxed{\mathcal D_\infty(H)=A\oplus qA\oplus\mathbb R X^3.} \tag{A8}
\]

**Proof of persistence.** Write `H=aX+bJ` with `J=qp`. The direct
transvectant identity gives `T3(X,X^3)=0`; all higher odd gates vanish
because their combined `q` degree is four. Also `J` is quadratic, so
it contributes no gate, and

\[
\{X,X^3\}=0,\qquad \{J,X^3\}=-\frac{15}{4}X^3.
\]

This proves (A7) independently of the complete analytic classification.
Equivalently, `F''=(5a/16)p^(-9/4)` and
`K3=FF'''/(3F'')-3F'=-15b/4`.

**Proof of completeness.** The complete analytic `qF` boundary theorem
is not needed here. Since `B=0`, distinct `q` degrees cannot cancel in
either `C3` or `C3D`. Equations (A2)--(A3) apply to each degree `c>=2`
separately, and direct simplification gives

\[
K_c=\frac{a(3-c)}2p^{-5/4}-\frac{b(7c-6)}4.             \tag{A8a}
\]

Because `a!=0`, this is constant exactly when `c=3`. Thus the common
kernel of `C3` and `C3D` is exactly the strip plus `R X^3`. Persistence
already proved in (A7) identifies it with the full dynamic core. Hence
the stronger identity

\[
\ker C_3\cap\ker(C_3D)
   =\mathcal D_\infty(H)=A\oplus qA\oplus\mathbb R X^3  \tag{A8b}
\]

is self-contained and holds in every finite `q` degree. The exceptional
cubic is selected directly by the factor `3-c`; no imported analytic
classification or numerical truncation is necessary.

**Why the cubic is a boundary, not a template for arbitrary degrees.**
For any integer `c>=4`, set

\[
\rho=\frac{2-c}{c+1},\qquad
H=q p^\rho+bqp,\qquad G=(q p^\rho)^c.
\]

Then `T3(H,G)=0` and
`{H,G}=bc(rho-1)G`, so `T3(H,D^jG)=0` for every `j>=0`.
Nevertheless, direct fifth-order arithmetic gives

\[
T_5(H,G)=-8(c)_4(\rho)_4q^{c-4}p^{-c-3}\ne0.             \tag{A8c}
\]

Thus arbitrarily deep third-order checks cannot replace higher gates
for general analytic coefficients. At `c=3`, `rho=-1/4` and the falling
factorial `(c)_4` vanishes; this is the genuine cubic family above.
The distinction matters when exporting a successful `T3` argument from
the polynomial branch to a wider coefficient ring.

## A sharp nonlinear canonical-coordinate obstruction

Set

\[
Y=\frac45p^{5/4}.
\]

Then `\{X,Y\}=1` and

\[
H=aX+\frac{5b}{4}XY.                                    \tag{A9}
\]

So this nonlinear Hamiltonian becomes quadratic in the algebraic
canonical coordinates `(X,Y)`. Rebuilding the standard flat Moyal
product in those new coordinates would make every observable exact.
The original flat Moyal product in `(q,p)` has a different answer:
although `X` and `X^3` belong to its dynamic core, `X^2` does not.
Indeed,

\[
\begin{aligned}
T_3(H,X^2)&=-\frac{15a}{16}p^{-15/4},\\
\frac{[H,X^2]_\star}{i\hbar}
 &=-\frac{5b}{2}X^2+\frac{5a\hbar^2}{128}p^{-15/4},\\
X\star X&=X^2+\frac{\hbar^2}{64}p^{-5/2}.                \tag{A10}
\end{aligned}
\]

The star square is a quantum eigenobservable:
`[H,X star X]_star/(i hbar)=-(5b/2)(X star X)`, by the derivation law.
This does not put its ordinary leading term `X^2` in the classical
dynamic core; its explicit correction cancels the anomaly in (A10).
The core is a vector space, not an algebra under ordinary multiplication.
The formulas exhibit the coordinate dependence directly, without
mistaking a nonlinear change of coordinates for covariance of the same
flat Moyal product.

The classical evolution is elementary as well. Put `Z=p^(5/4)`.
Then `DZ=(5/4)(a+bZ)` and `DX=-(5b/4)X`. For `b!=0`,
`Z(t)=exp(5bt/4)(Z(0)+a/b)-a/b`, as long as the trajectory stays in
`p>0`, and `G(t)=exp(-15bt/4)G(0)` is exact under both evolutions.
These are local-domain evolution statements, not assertions of a
globally complete flow across the singular boundary `p=0`.

## Relation to the branch and verification scope

Theorem A recovers Claude's polynomial affine strips and adds an
observable-degree-independent gate-depth bound. Theorem B shows exactly
why extending a polynomial-core collapse statement to arbitrary analytic
coefficients would fail: a simple algebraic coefficient already adds an
active cubic. Log-Gamma and all polygammas lie on the collapsing side by
their separately proved analytic asymptotic/pole arguments.

`analytic_bridge_check.py` uses exact rational arithmetic and a sparse
fractional-power derivative engine. It checks the gate identities,
persistence, canonical relation, anomaly and star-square correction;
it also tests Theorem A on finite polynomial/Laurent boxes by a direct
matrix kernel calculation with no output projection. Those boxes
cross-check conventions; the proof above, not their size, supplies the
all-degree claims.

The distinction between affine covariance and nonlinear canonical
changes belongs to established Weyl quantization theory. Primary
background includes Mark Gotay, *On the Groenewold--Van Hove problem for
R^{2n}*, [arXiv:math-ph/9809015](https://arxiv.org/abs/math-ph/9809015).
No claim is made that a new geometric torsion operation or a new general
quantization obstruction has been invented. The specific stopping
theorem and explicit family here still require a focused priority check.
