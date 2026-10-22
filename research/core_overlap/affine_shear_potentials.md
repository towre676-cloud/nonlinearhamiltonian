# Affine shears with arbitrary polynomial potential

Use the fixed original flat Weyl product and the sign convention
`D={H,.}=H_q partial_p-H_p partial_q`. The coefficient field `K` has
characteristic zero. Put `C_3=T_3(H,.)` and let `R_r` be the joint
kernel of `C_3D^j`, `0<=j<=r`, on the full polynomial ring. No finite
observable degree is imposed in the statements below.

**Theorem AFP.** Let

\[
Q=p+u(q),\qquad \deg u\le1,\qquad
H=AQ^2+V(q),\qquad A\ne0,
\]

where a zero `u` is also allowed. If `deg V<=2`, the original
Hamiltonian is quadratic and its dynamic core is all of `K[q,p]`.
If `deg V=3`, then

\[
\boxed{\mathcal D_\infty(H)=R_7=\operatorname{span}_K\{1,H\}.}
                                                               \tag{AFP1}
\]

If `deg V>=4`, then

\[
\boxed{\mathcal D_\infty(H)=R_5=\operatorname{span}_K\{1,H\}.}
                                                               \tag{AFP2}
\]

The displayed third-gate stopping depths are sharp for every
Hamiltonian in their respective strata. This is a classification
within the stated affine-shear family; historical priority is not
established.

## Exact strip reduction

The affine symplectic substitution `(q,p)->(q,Q)` gives exactly

\[
D=-2AQ\partial_q+V'(q)\partial_Q,
\qquad C_3=V'''(q)\partial_Q^3.                         \tag{AFP3}
\]

The same identities also follow by direct differentiation in the
original variables. Suppose `deg V>=3`, so `V'''` is a nonzero
polynomial. Since `K[q,Q]` has no zero divisors, `C_3G=0` forces

\[
G=c(q)Q^2+b(q)Q+f(q).
\]

The next equations can be read successively from the cubic
coefficient in `Q`. First,

\[
C_3DG=-12A V'''c',
\]

so `c` is constant. Under this condition,

\[
C_3D^2G=24A^2 V'''b'',
\]

so `b` is affine. Under these two conditions,

\[
C_3D^3G=48A^2V'''(cV'''-Af''').                        \tag{AFP4}
\]

Therefore `f=(c/A)V+f_2`, where `deg f_2<=2`. Conversely each
polynomial of this form passes the four tests through depth three.
Thus the entire all-degree intermediate space is

\[
R_3=S=\operatorname{span}_K\{1,H,q,Q,q^2,qQ\}.          \tag{AFP5}
\]

This is an exact infinite-ring calculation, rather than a degree
bound inferred from a matrix.

## Exact invariant-preimage calculation

The nested kernels obey
`R_(r+1)={G in R_r : DG in R_r}`. Indeed, requiring `DG` to lie in
`R_r` adds precisely the equations at depths `1,...,r+1` to the
depth-zero equation. The required brackets on the nonstationary
generators of `S` are

\[
\begin{aligned}
Dq&=-2AQ,& DQ&=V',\\
Dq^2&=-4AqQ,& D(qQ)&=-2H+W(q),\qquad W=2V+qV'.
\end{aligned}                                               \tag{AFP6}
\]

The purely `q`-dependent polynomials in `S` are exactly
`span{1,q,q^2}`. A polynomial cannot use a nonzero multiple of `H`
to represent a pure `q` function, since that would leave a nonzero
`Q^2` coefficient.

If `n=deg V>=4`, then `deg W=n` and `deg V'=n-1>=3`.
Their leading degrees are distinct, so no nontrivial linear
combination of `W` and `V'` can lie in `span{1,q,q^2}`. Equation
(AFP6) therefore gives

\[
R_4=\operatorname{span}\{1,H,q,q^2\},\qquad
R_5=\operatorname{span}\{1,H\}.                         \tag{AFP7}
\]

In the second step the independent outputs `Q` and `qQ` exclude
`q` and `q^2` respectively.

If `n=3`, `W` has degree three while `V'` is a genuine quadratic.
The successive exact spaces are instead

\[
\begin{aligned}
R_4&=\operatorname{span}\{1,H,q,Q,q^2\},\\
R_5&=\operatorname{span}\{1,H,q,Q\},\\
R_6&=\operatorname{span}\{1,H,q\},\\
R_7&=\operatorname{span}\{1,H\}.
\end{aligned}                                               \tag{AFP8}
\]

The first step excludes `qQ` by its uncancellable cubic output.
The next excludes `q^2` by its `qQ` output, then `Q` by its
quadratic output, then `q` by its `Q` output. The surviving span
is stationary and every odd gate kills it by antisymmetry.
Consequently it is exactly the full dynamic core, proving
(AFP1)--(AFP2). Higher gates are not needed for either stopping
rule.

## Uniform sharpness

For `deg V>=4`, direct iteration gives

\[
C_3D^jq=0\quad(0\le j<5),\qquad
C_3D^5q=96A^4 V'''V''''\ne0.                           \tag{AFP9}
\]

The first four iterates have `Q` degree at most two; the cubic
coefficient in the fifth is `16A^4 V''''`. Both derivatives in
(AFP9) are nonzero polynomials, so their product is nonzero.

For a cubic potential, write `k=V'''`, a nonzero constant. The
same witness survives two more steps:

\[
C_3D^jq=0\quad(0\le j<7),\qquad
C_3D^7q=-960A^5k^3\ne0.                                \tag{AFP10}
\]

For clarity, the fifth iterate is
`-8A^3[(V'')^2+3kV']Q`; the sixth has quadratic coefficient
`80A^4 k V''`; the seventh therefore has cubic coefficient
`-160A^5 k^2`. Applying `C_3=k partial_Q^3` proves the constant
in (AFP10). Thus the claimed stopping depths are necessary for
every allowed potential, including arbitrary lower coefficients.

## Recognition and replay

For an input polynomial `H=A p^2+B(q)p+C(q)` with constant
`A!=0`, completing the square uniquely gives
`u=B/(2A)` and `V=C-Au^2`. The AFP recognizer succeeds precisely
when `deg u<=1`. It then returns the entire ring when `deg V<=2`,
or `span{1,H}` with sharp depth seven or five in the two higher
strata. Inputs outside the route return no classification.

`affine_shear_potentials.py` checks original-coordinate operators,
all conditional strip identities, the all-parameter witness
constants, exact intermediate kernel dimensions, and recognition
boundaries using standard-library rational arithmetic. Finite
matrices retain every output coordinate; the proof above establishes
the claims in all polynomial degrees. The replay receipt is
`affine_shear_potentials_results.json`.
