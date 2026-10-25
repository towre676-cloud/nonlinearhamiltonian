# Protected nonlinear canonical transport of exact dynamic sectors

This note explains why a nonlinear canonical change can preserve a particular
flat Weyl–Moyal dynamic sector even though it does not preserve flat Moyal
exactness on every observable. It supplies a structural explanation for the
pure-top counterfamilies in this programme. No historical priority claim is
made for canonical transformations, Weyl ordering, or their quantum correction.

We use

\[
 \{A,B\}=A_qB_p-A_pB_q,\qquad
 \frac{[A,B]_\star}{i\hbar}
 =\sum_{r\ge0}\frac{(-1)^r\hbar^{2r}}{2^{2r}(2r+1)!}
    T_{2r+1}(A,B).
\]

All statements below are algebraic in characteristic zero. For polynomial
inputs the relevant series terminate. Formal powers of `hbar` are retained;
they are never fitted from numerical samples.

## The protected shear lemma

Let `w(q)` be a polynomial, choose an antiderivative `U'(q)=w(q)`, and
write `sigma_w A(q,p)=A(q,p+w(q))`. The quantum canonical automorphism

\[
 \mathscr S_w=\exp\left(\frac{\operatorname{ad}_\star U}{i\hbar}\right)
\]

has the exact factorization

\[
 \boxed{\quad
 \mathscr S_w
 =\sigma_w\exp\left(
   -\frac{\hbar^2}{24}w''\partial_p^3
   +\frac{\hbar^4}{1920}w^{(4)}\partial_p^5-\cdots
                 \right).\quad}                         \tag{C1}
\]

Indeed, `T_k(U,A)=U^(k) partial_p^k A`, and every coefficient in these
operators depends on `q` alone. Consequently all the displayed differential
operators commute. The exponential is finite on each polynomial because
each nonzero application lowers its `p` degree. Since its generator is an
inner star derivation, `S_w` preserves the star product.

In particular

\[
 \mathscr S_w A=\sigma_w A\qquad (\deg_p A\le2).            \tag{C2}
\]

This degree threshold is sharp when `w''` is nonzero:

\[
 \mathscr S_w(p^3)=(p+w)^3-\frac{\hbar^2}{4}w''.           \tag{C3}
\]

Here is the resulting transport principle. Suppose `H_0` and a linear
space `V` consist of polynomials of `p` degree at most two, every odd gate
`T_k(H_0,v)` with `k>=3` vanishes on `V`, and `{H_0,V} subset V`. Then

\[
 \sigma_w V\subseteq\mathcal D_\infty(\sigma_wH_0).        \tag{C4}
\]

To prove it, apply the star automorphism `S_w` to
`[H_0,v]_star/(i hbar)={H_0,v}`. Every member of this identity is in the
protected subspace, so (C2) changes the quantum transport into the ordinary
canonical pullback. Hence
`[sigma_wH_0,sigma_wv]_star/(i hbar)={sigma_wH_0,sigma_wv}`. The same
argument applies to every Hamiltonian iterate, because these remain in
`V`. This proves (C4). It does not assert transport of the entire core
under an arbitrary nonlinear change of coordinates.

## A complete pure-top family

Take `a>=1`, `A!=0`, `w` of degree `t>=2`, and arbitrary constants
`B,C,beta,delta`. Set

\[
 z=qp,\quad H_0=q^a(Az^2+Bz+C)+\beta z+\delta,
\]

\[
 G=qp+q w(q),\qquad
 H=q^a(AG^2+BG+C)+\beta G+\delta.                         \tag{C5}
\]

Then

\[
 \boxed{\mathcal D_\infty(H)=\operatorname{span}\{1,H,G\},
 \qquad \{H,G\}=a(H-\beta G-\delta).}                    \tag{C6}
\]

The lower bound follows from the protected shear lemma. It can also be
checked directly: `H` has `p` degree two and `G=qp+u(q)`. In every term of
an odd gate of order at least three, either three `p` derivatives hit
`H`, two hit `G`, or at least two `q` derivatives and one `p` derivative
hit `G`. Each possibility vanishes. The bracket in (C6) follows by
transporting the identity for `H_0` under `sigma_w`.

For completeness, filter by `p` degree. The transverse top of `H` is
`Aq^(a+2)p^2`. Its all-degree core is `span{1,qp,Aq^(a+2)p^2}` by the
unequal-monomial theorem, because `a+2>2`. The associated graded of the
core of `H` embeds in this three-dimensional core. Therefore the core of
`H` has dimension at most three; the three independent elements in (C6)
give equality. The top total-degree term of `H` is a nonzero multiple
of `q^(a+2t+2)`, so these are pure tops. The generator `G` has degree
`t+1>=3`: its presence is not explained by a quadratic core element.
The `p^2` coefficient `Aq^(a+2)` is nonconstant, so the family is outside
the previously proved affine and constant-quadratic strip structures.

The smallest example of this form is

\[
 H=q^7+2q^5p+q^3p^2=q(qp+q^3)^2,
 \quad G=qp+q^3,
 \quad \{H,G\}=H.                                       \tag{C7}
\]

Thus a nonlinear shear of a three-dimensional exact sector is a mechanism
for retaining active polynomial exact dynamics beneath a pure top. It
also explains why a conjecture based only on affine normal forms can
miss this family.

## The complementary `qF(p)` chart

Let `F` be real analytic and nonzero on an interval `I`, and put

\[
 Q=qF(p),\qquad P=S(p),\qquad S'=1/F.
\]

Then `{Q,P}=1`, and also `[Q,P]_star=i hbar` exactly. The latter holds
because `Q` is affine in `q` and `P` depends only on `p`. Nevertheless
ordinary pullback fails already at the square:

\[
 T_3(Q,Q^2)=12FF'F'',\quad
 \frac{[Q,Q^2]_\star}{i\hbar}=-\frac{\hbar^2}{2}FF'F'',
 \quad \{Q,Q^2\}=0,                                    \tag{C8}
\]

\[
 Q\star Q=Q^2+\frac{\hbar^2}{4}(F')^2.                  \tag{C9}
\]

For a polygamma `F=psi^(m)`, the obstruction in (C8) is
`12 psi^(m) psi^(m+1) psi^(m+2)`; it is nowhere zero for `m>=1` on the
positive axis. For digamma one restricts to an interval avoiding its
zero. For `F=log Gamma`, the same expression is
`12 log Gamma psi psi^(1)` and is not identically zero on any open
interval avoiding the zeros of `F`. These are ordinary consequences of
the derivative identities; no numerical special-function evaluation is
used in (C8).

The exact quantum pullback of a finite polynomial in `Q` with analytic
`P` coefficients is

\[
 \mathscr W_F\bigl(Q^n a(P)\bigr)
   =J_Q^n\bigl(a(S(p))\bigr),\qquad
 J_Q(A)=\tfrac12(Q\star A+A\star Q).                     \tag{C10}
\]

Here `Q` inside the star product denotes `qF(p)`. The commutation
relation `[Q,a(S)]_star/(i hbar)=a'(S)` verifies the usual Weyl
relations. Formula (C10) is therefore a star-algebra homomorphism from
the flat `(Q,P)` algebra to the original one. It is invertible as a
formal triangular map: its leading term is ordinary canonical
pullback, and its corrections lower `q` degree by positive even
integers. Each finite `Q` degree has only finitely many corrections.

Writing `a` now for `a(S(p))`, its first two nontrivial cases are

\[
 \mathscr W_F(Q^2a)
 =q^2F^2a+\frac{\hbar^2}{4}F'(F'a+Fa'),                  \tag{C11}
\]

\[
 \mathscr W_F(Q^3a)
 =q^3F^3a+\frac{\hbar^2q}{4}
  \bigl[(5F(F')^2-F^2F'')a+3F^2F'a'\bigr].             \tag{C12}
\]

For every integer `n>=2`, the coefficient of `hbar^2` is

\[
 \frac{n(n-1)}{24}q^{n-2}F^{n-2}
 \bigl[(2n-1)(F')^2a+3FF'a'-(n-2)FF''a\bigr].           \tag{C13}
\]

For an all-`n` verification, write the `hbar^2` term as
`q^(n-2)b_n(p)`. The defining Jordan product gives `b_1=0` and

\[
 b_{n+1}=Fb_n+\frac n8\left[
  2nF^{n-1}(F')^2a+2F^nF'a'-(n-1)F^nF''a\right].
\]

Summing `sum j^2`, `sum j`, and `sum j(j-1)` gives (C13). Thus its
arbitrary-degree statement is an induction identity, rather than an
extrapolation of the companion checker's finite fixtures. No coordinate
covariance of the ordinary flat Moyal product is assumed.

Finally suppose `F''` is nowhere zero and

\[
 K_3=\frac{FF'''}{3F''}-3F'=\lambda.
\]

Then `r=cuberoot(F'')` satisfies
`r/F^3=c_0 exp(lambda S)` for a nonzero constant `c_0`. The classical
persistent cubic `q^3r` is the ordinary pullback of
`c_0 Q^3 exp(lambda P)`. Its first integral is

\[
 FF''-5(F')^2-3\lambda F'=C.
\]

Substitution into (C12) gives the exact correction

\[
 \mathscr W_F(Q^3e^{\lambda P})
 =q^3F^3e^{\lambda S}
   -\frac{C\hbar^2}{4}qF e^{\lambda S}.                 \tag{C14}
\]

Both terms are classical Hamiltonian eigenvectors of eigenvalue
`lambda`. In the explicitly constructed active family
`F'=aF^5+b`, `a!=0`, one has `lambda=-5b/3` and `C=0`. Thus its cubic
eigenpartner is a second protected nonlinear canonical pullback: the
classical and quantum Weyl pullbacks agree on this particular cubic,
although the square obstruction (C8) is generally nonzero. The
polynomial shear protection (C2) and the analytic cubic protection
(C14) supply complementary, precisely scoped links between the two
research programmes.

The companion `canonical_verify.py` independently checks the finite
shear identities, the protected pure-top family, and the explicit
Jordan-product formulas with exact rational polynomial arithmetic.
