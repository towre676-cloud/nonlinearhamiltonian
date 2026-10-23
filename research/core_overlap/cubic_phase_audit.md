# Complete linear coupling in the cubic phase, and an obstruction audit

All statements use the original flat Weyl transvectants in one canonical
pair `(q,p)`, over a field K of characteristic zero. Write
`Q=q`, `P=p+w(q)`, where w is quadratic and `c=w''/2 != 0`.
The substitution is used to express the original operators, not to replace
their product by the flat product in `(Q,P)`.

## The complete linear-coupling theorem

**Theorem CPL.** Let

\[
 h(Q,P)=a(P)+Q\mu(P-r),\qquad \mu\ne0,\quad \deg a=f\ge3,
 \qquad H=h(q,p+w(q)).                                      \tag{CPL1}
\]

Every polynomial element of `D_infinity(H)` is affine in Q. Its full core,
with every displayed expression pulled back to `(q,p)`, has basis

\[
 1,\ P,\ P^2,\ h;
 \qquad Q\quad\text{if }f=3;
 \qquad (P-r)h\quad\text{if }f=3\text{ and }a''(r)=0.          \tag{CPL2}
\]

Thus its dimension is four when f is at least four, five for a cubic a
with `a''(r)!=0`, and six for a cubic a with `a''(r)=0`.
The value of `a(r)` does not affect the condition: adding a constant to
the Hamiltonian does not alter its derivation or its gates.

This closes the full-core upper-bound question in Claude's K1-prime
family. It does not rely on the restricted affine-observable theorem:
both the absence of higher Q powers and the remaining affine basis are
proved below independently. Higher gates introduce no further restriction
on the basis (CPL2).

### The exact third gate

For a general affine Hamiltonian `h=a(P)+Qb(P)`, the original third gate
rewritten in `(Q,P)` is

\[
\begin{split}
 C_3g={}&-(a'''+Qb''')g_{QQQ}+3b''g_{QQP}\\
 &+6c\bigl[b'g_{PPP}+b''g_{PP}
 -(a''+Qb'')g_{QPP}-(a'''+Qb''')g_{QP}\bigr].                \tag{CPL3}
\end{split}
\]

This follows by taking the coefficient of `t^3/3!` in the exact triangular
generating formula: `C3=Omega^3+6c Omega K`, with
`K=partial_P1 partial_P2^2+partial_P1^2 partial_P2`.
The checker also verifies (CPL3) directly with mixed derivatives in the
original coordinates, using an arithmetic engine independent of the
triangular producer.

### Diagonalizing the Hamiltonian derivation

Translate P by r, divide h by mu, and subtract the constant term. These
operations do not change its core. It is enough to treat

\[
 h=PJ,\qquad J=Q+A(P),\qquad A(P)=a(P)/P,
 \qquad m=\deg A=f-1\ge2.                                  \tag{CPL4}
\]

Here a has zero constant after the harmless subtraction, so A is a
polynomial. The coordinate change `(Q,P) <-> (P,J)` is a polynomial
bijection. A direct bracket calculation gives

\[
 DP=P,\qquad DJ=-J,\qquad
 D=P\partial_P-J\partial_J.                                \tag{CPL5}
\]

Consequently `P^u J^v` is an eigenvector of D of eigenvalue `u-v`.
Every polynomial is a finite sum of such eigenvectors. Because the core
is D-invariant, each of the distinct-eigenvalue components of any core
element is again in the core: the finite spectral projections are
polynomials in D, using the distinct integer eigenvalues and
characteristic zero. This argument has no input-degree cutoff.

### Excluding every Q degree at least two

Let g be a nonzero D-eigenpolynomial in the core, of J degree n. Its
highest-J term is `lambda P^d J^n` for some integer d at least zero and
nonzero lambda. J and Q differ only by a polynomial in P, so they define
the same highest transverse degree. The highest-Q part of (CPL3), for
`b=P`, is `6c partial_P^3`. Thus d is at most two. Rescale lambda to one.
The eigenvalue condition then forces

\[
 g=\sum_{j=0}^{\min(d,n)}\lambda_j P^{d-j}J^{n-j},
 \qquad \lambda_0=1,\quad d\in\{0,1,2\}.                  \tag{CPL6}
\]

In `(P,J)` the exact normally ordered third gate is

\[
\begin{split}
 C_3={}&6c\partial_P^3
 +6c(A'-PA'')\partial_P^2\partial_J
 -6cA'(A'+2PA'')\partial_P\partial_J^2\\
 &-\bigl[6c(A')^2(A'+PA'')+3A''+PA'''\bigr]\partial_J^3
 -6cPA'''\partial_P\partial_J\\
 &-6c\bigl[2A'A''+P(A'')^2+PA'A'''\bigr]\partial_J^2
 +6cA'''\partial_J .                                      \tag{CPL7}
\end{split}
\]

Coefficients are placed to the left of the derivatives. Let
`A=alpha P^m+lower`, where `alpha!=0` and `m>=2`.

If n is at least three, the term of highest P degree in `C3g` is

\[
 -6c\,m^4\alpha^3 n(n-1)(n-2)
       P^{d+3m-3}J^{n-3}.                                 \tag{CPL8}
\]

It comes only from the first term of (CPL6) and the leading
`-6c(A')^2(A'+PA'') partial_J^3` term. Every other term in (CPL7) has
smaller P degree; the lower terms in (CPL6) also lower that degree.
Its coefficient is nonzero, contradicting `C3g=0`.

If n equals two, the term of highest P degree in `C3g` instead is

\[
 -12c\,m^2(2m-1)(d+m-1)\alpha^2P^{d+2m-3}.                 \tag{CPL9}
\]

It is obtained by combining the two `partial_J^2` terms in (CPL7).
Again the lower terms of (CPL6) cannot reach this P degree, and the
displayed coefficient is nonzero because `m>=2,d>=0`. This excludes
n two as well. Therefore every D-eigencomponent of a core element,
and hence every core element itself, is affine in Q.

### Determining and certifying the remaining basis

For n zero, (CPL3) permits precisely `1,P,P^2`. For n one, (CPL6)
leaves only J, PJ and `P^2J`, modulo these already protected polynomials.
Their third gates are

\[
 C_3J=6cA''',\qquad C_3(PJ)=0,\qquad
 C_3(P^2J)=12c(A'-PA'')-6cP^2A'''.                         \tag{CPL10}
\]

For m at least three the last expression has nonzero leading coefficient
`-6c m(m-2)(m+1)alpha`, and `A'''` is nonzero. For m two,
`A=alpha P^2+a_2P+a_1`: J passes and the last expression is `12c a_2`.
Since J differs from Q by a combination of `1,P,P^2`, this gives exactly
(CPL2), with `a_2=a''(r)/(2mu)` before normalization.

Each listed span is D-invariant. Every odd gate kills `1,P,P^2` by
the triangular generating formula, h by antisymmetry, and Q because it
is linear in the original coordinates. For the exceptional `Ph`,
the third gate is `6c mu a''(r)` in the root-centered coordinates, hence
zero in the stated case. All odd gates of order at least five vanish:
both functions are affine in Q, so only the `Omega K^k` term can
contribute to order `2k+1`; for k at least two, its P derivatives
annihilate the linear coefficient b or the quadratic Q coefficient of
Ph. This proves sufficiency in every degree and completes Theorem CPL.

### A uniform finite stopping certificate

The diagonal derivation supplies a finite stopping bound as well. Split
the operator (CPL7) into its D-weight shifts: a normally ordered term
`P^i J^j partial_P^u partial_J^v` has shift `s=i-j-u+v`.
Let S be the finite set of shifts actually present after combining
coefficients. Then

\[
 \mathcal D_\infty(H)
 =\bigcap_{r=0}^{|S|-1}\ker(C_3D^r).                        \tag{CPL12}
\]

Indeed, fix an output monomial of weight omega. Its coefficient in
`C3 D^r g` is the sum, over s in S, of `(omega-s)^r` times the
contribution from the input weight `omega-s`. The first `|S|` equations
have a Vandermonde matrix with distinct nodes `omega-s`; hence each
contribution vanishes separately. Thus every D-eigencomponent of g is
killed by C3. The proof above classifies exactly these eigencomponents,
and all of them pass every gate. This argument retains every output
coefficient, with no projection and no input-degree cutoff.

For `m=deg A`, the displayed operator gives
`S subset {-3,-1} union {1,...,3m}` and therefore the uniform upper bound
`R<=3m+1`. The checker returns the smaller actual `|S|-1` bound. In the
six-dimensional normalized cubic branch
`a=alpha P^3+a1 P+a0`, `S={-3,3,6}`, so depths zero, one and two
already suffice in all polynomial degrees. Sharpness of these general
bounds is not asserted.

## A naming and normalization audit

Claude's gauge identity is algebraically correct in the formal generating
parameter t. Physical Moyal conventions often use `t=i hbar/2`, so a
coefficient written in t must be converted before being described as a
physical hbar coefficient. No numerical prefactor independent of the
chosen convention is asserted here.

The displayed vector-field defect satisfies the exact identity

\[
 b'\beta'''-b'''\beta'=(b'\beta''-b''\beta')'.              \tag{CPL11}
\]

Its integral over a periodic domain, or with compact support and no
boundary contribution, is therefore zero. It must not be identified
without further structure with the usual nontrivial scalar
Virasoro/Gelfand--Fuchs central-extension cocycle. The full defect
`Delta(X,Y)=partial^3[X,Y]-[partial^3X,Y]-[X,partial^3Y]` is, by its
definition, the derivation defect (a Chevalley--Eilenberg coboundary up
to sign) of the linear operator `partial_P^3` in the adjoint module.
It is a useful exact compatibility condition. A nontrivial cohomology
class would require a separately specified coefficient module and a
separate proof. None is claimed by this note.

For comparison, the conventional scalar Gelfand-Fuchs central-extension
formula is `(1/12) integral b''' beta`, as given by Ovsienko and Roger,
[arXiv:math/9812074](https://arxiv.org/abs/math/9812074), equation (9.2).
Integration by parts gives
`integral(b' beta''-b'' beta')=2 integral b''' beta` under the same
boundary conditions. Our displayed defect is the derivative of that
integrand, so its scalar integral vanishes rather than producing that
nontrivial central extension.

## Exact replay and limits

Run `python3 -B -S research/core_overlap/cubic_phase_audit.py`.
The checker independently verifies the original-coordinate third gate,
the diagonal derivation and transformed operator, the two leading
coefficient formulas, full-output weight kernels, and shifted/nonunit
linear-coupling examples with every relevant odd gate. Its classifier
recognizes only the scope `deg a>=3,deg b=1`; lower a degrees and other
b degrees belong to the companion classifications, not to this parser.
The finite kernels supplement the all-degree proof above. Historical
priority and external peer review remain open.
