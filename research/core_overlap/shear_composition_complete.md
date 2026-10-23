# Completing the polynomial shear-composition phase diagram

All statements use one canonical pair, the original flat Weyl product in
`(q,p)`, and the convention `{H,G}=H_q G_p-H_p G_q`. The coefficient field
`K` has characteristic zero. The dynamic core consists of polynomials `G`
such that every odd transvectant `T_k(H,D^rG)`, `k>=3`, `r>=0`, vanishes,
where `D={H,.}`. No covariance under a nonlinear canonical substitution is
assumed. Historical priority is not established.

## The missing composition quadrant

**Theorem SCP.** Let

\[
Q=p+u(q),\qquad H=P(Q)+\varepsilon q,\qquad
m=\deg u\ge3,\quad \mu=\deg P\ge3.
\]

Then, in all polynomial degrees,

\[
\boxed{\mathcal D_\infty(H)
=\ker C_3\cap\ker(C_3D)
=\operatorname{span}_K\{1,H\}.}                         \tag{SCP1}
\]

Both tests in the middle expression are necessary for every allowed
choice of parameters. Thus one bracket step is a sharp uniform stopping
depth when using the third gate.

### Exact transformed operators

Use the polynomial algebra isomorphism `(q,p)->(q,Q)` only to express the
original operators. Derivatives below keep `Q` fixed. Chain rule gives

\[
D=\varepsilon\partial_Q-P'(Q)\partial_q,
\]

\[
\boxed{C_3=
u'''(P'\partial_Q^3-P'''\partial_Q)
-3u''(P''\partial_q\partial_Q^2+P'''\partial_q\partial_Q)
-P'''\partial_q^3.}                                    \tag{SCP2}
\]

Here the derivatives of `P` are evaluated at `Q`; those of `u` are
evaluated at `q`. To derive (SCP2), substitute
`partial_q(old)=partial_q(new)+u' partial_Q` and
`partial_p(old)=partial_Q` into the alternating third transvectant.
Terms containing `u'` cancel. In particular the derivative of `u'` in
the cubic power of the old `q` derivative contributes the term
`-u'''P''' partial_Q`; it must not be omitted. The linear forcing has
no third gate.

### All-degree proof and the absence of cancellation

Filter `K[q,Q]` by ordinary total degree. Write
`u=alpha q^m+lower` and `P=rho Q^mu+lower`, with `alpha rho != 0`.
The top derivation is

\[
D_0=-\rho\mu Q^{\mu-1}\partial_q,
\qquad\text{degree shift }\mu-2.
\]

The top third gate `C_0` consists of the first four terms in (SCP2),
using the leading monomials of `u` and `P`. Its degree shift is
`m+mu-7`. The omitted term `-P''' partial_q^3` has shift `mu-6`,
strictly smaller by `m-1`; all other omitted coefficient terms are
also lower. A negative gate shift, possible when `m=mu=3`, causes no
problem: lower input components still have strictly lower output degree.

For `c>=1`, direct differentiation gives

\[
\boxed{C_0(q^aQ^c)=\alpha\rho\mu m(m-1)
c(c+\mu-3)\big[(m-2)(c-\mu)-3(\mu-1)a\big]
q^{a+m-3}Q^{c+\mu-4}.}                                \tag{SCP3}
\]

For `c=0`, the image is zero directly. Distinct input monomials with
nonzero images have distinct output monomials, since the exponent
shift is fixed. Consequently no linear combination can cancel a
nonzero coefficient in (SCP3).

Suppose `G` passes `C_3` and `C_3D`, and let `G_N` be its highest
homogeneous component. Extracting the highest possible output degree
in the two equations gives

\[
C_0G_N=0,\qquad C_0D_0G_N=0.                           \tag{SCP4}
\]

The first equation permits only monomials with `c=0`, or with

\[
(m-2)(c-\mu)=3(\mu-1)a.                               \tag{SCP5}
\]

In the latter case `c>=mu`. Consider the second equation monomial by
monomial. Its nonzero images again have one fixed exponent shift,
now `(m-4,2mu-5)`, so they cannot cancel each other.

If `c=0,a>=1`, applying `D_0` gives a nonzero multiple of
`q^{a-1}Q^{mu-1}`. The last bracket in (SCP3) becomes
`-(m-2)-3(mu-1)(a-1)`, a strictly negative integer. The other
factors are nonzero. Such a monomial therefore fails (SCP4).

If (SCP5) holds and `a>=1`, applying `D_0` changes `(a,c)` to
`(a-1,c+mu-1)`. The last bracket changes from zero to
`(mu-1)(m+1)`, again nonzero. Such a monomial also fails (SCP4).

Only `1` and `Q^mu` remain in the joint top kernel. Thus a
nonconstant `G` has `N=mu` and `G_N=lambda Q^mu`. Subtract
`(lambda/rho)H`, which passes both tests by odd antisymmetry and
`DH=0`. The remainder has degree below `mu`, so the same argument
forces it to be constant. This proves that the two-test kernel is
`span{1,H}`. Every odd gate kills this span, which is stationary
under `D`; therefore it is also the full dynamic core. This proves
(SCP1) without a numerical degree bound.

### Sharp necessity of each test

The two witnesses work for every `u,P,epsilon` in the theorem:

\[
C_3q=0,\qquad
C_3Dq=u'''(P'''P''-P'P'''')\ne0;                        \tag{SCP6}
\]

\[
C_3Q=-u'''P'''\ne0,\qquad C_3DQ=0.                    \tag{SCP7}
\]

For (SCP6), the polynomial in parentheses has degree `2mu-5` and
leading coefficient `2rho^2 mu^2(mu-1)(mu-2)`, which is nonzero in
characteristic zero. For (SCP7), `DQ=epsilon` is constant. Thus
neither of the two tests may be discarded, and depth zero is
insufficient throughout the stated family.

## Exact recognition and the completed scope

For an input polynomial of `p` degree `mu>=3`, its leading `p`
coefficient must be a nonzero constant `rho`. If `B(q)` is its
`p^(mu-1)` coefficient, the normalization `u(0)=0` fixes

\[
u(q)=\frac{B(q)-B(0)}{\mu\rho}.
\]

Substitute `p=Q-u(q)` into `H`. Recognition succeeds exactly when
`deg u>=3` and the result is a polynomial in `Q` plus `epsilon q`.
This is a finite exact identity test; no bounded partner ansatz is
fitted. A failed recognition is outside this route, rather than a
certificate of collapse.

Together with the retained results this closes the composition
family `H=P(p+u(q))+epsilon q` for every polynomial `u` of degree at
least two. Quadratic `u` is Theorem QC in
`pure_quadratic_composition.md`. For `deg u>=3`, quadratic `P` is
Theorem SS in `analytic_shear_square.md`; degree at least three is
(SCP1). If `deg P=1`, the Hamiltonian has the form `a p+v(q)`:
when `deg v>=3`, Theorem P+ gives the strip of `p` degree at most
two; when `deg v<=2`, every polynomial is exact. A constant `P`
also gives a Hamiltonian of degree at most one, hence the whole
polynomial ring. These elementary low-degree cases are referenced
for completeness and are not new claims of this note.

`shear_composition_complete.py` supplies the rational-coefficient
recognizer, transformed operators, a symbolic four-parameter factor
identity, direct original-coordinate and independent PBW checks,
uniform sharpness witnesses, and full-output finite kernel checks.
The proof above supplies the all-degree result. The accompanying
JSON records the exact replay and its stated finite scope.
