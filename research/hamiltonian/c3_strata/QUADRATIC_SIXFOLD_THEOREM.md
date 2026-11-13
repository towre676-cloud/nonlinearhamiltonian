# Sixfold leading form with quadratic dependence on a complementary coordinate

## Scope and principal result

Let \(K\) be a field of characteristic zero and

\[
H=p^2+b(q)\,p+f(q),\qquad \deg f=6,\qquad b=0\ \text{or}\ \deg b\le4 .
\tag{1}
\]

The leading form is \(f_6q^6\), so \(q\) defines the sixfold root and
\(p\) is complementary to it. Section 10 of the
[inhomogeneous note](INHOMOGENEOUS_THEOREM.md) treats Hamiltonians affine
in the complement. This note treats the next family, quadratic in the
complement with constant top coefficient, and classifies it completely:
the first refinement \(S^1\), the persistent core \(D_\infty\), and the
least depth at which the core is reached, for every admissible pair
\((f,b)\). Conventions are those of Section 1 of the inhomogeneous note:
\(D_HG=H_qG_p-H_pG_q\), \(T_k\) is the unnormalized alternating
contraction, and \(S^r=\{G:T_k(H,D_H^iG)=0,\ k=3,5,\ 0\le i\le r\}\).

Put

\[
P=p+\tfrac12 b(q),\qquad F=f-\tfrac14 b^2,\qquad H=P^2+F(q),
\qquad N=\deg F .
\tag{2}
\]

Since \(\deg f=6\), one has \(N=6\) when \(\deg b\le2\), \(N=8\) when
\(\deg b=4\), and \(N\le6\) can take any value when \(\deg b=3\), because
the sextic terms of \(f\) and \(b^2/4\) may cancel. The answer depends on
\(b''\) and on \(N\) only.

| Hypothesis | \(S^1\) | \(D_\infty\) | \(\dim D_\infty\) | Least depth |
|---|---|---|---|---|
| \(b''=0\) | \(K[q]+K[q]\,p+K\,p^2\) | \(\operatorname{span}\{1,H\}\) | 2 | 5 |
| \(b''\ne0,\ N\ge4\) | \(K[q]+Kp+Kqp+KH\) | \(\operatorname{span}\{1,H\}\) | 2 | 4 |
| \(b''\ne0,\ N=3\) | \(K[q]+Kp+Kqp+KH\) | \(\operatorname{span}\{1,H\}\) | 2 | 6 |
| \(b''\ne0,\ N\le2\) | \(K[q]+Kp+Kqp+KH\) | \(\operatorname{span}\{1,q,q^2,P,qP,P^2\}\) | 6 | 2 |

The last two rows occur only for \(\deg b=3\). Every depth is sharp, with
an explicit witness. The static space is also determined: for \(b''=0\) it
is \(K[q]+K[q]p+K[q]p^2\); for \(\deg b\in\{3,4\}\) it is
\(W=K[q]+K[q]p+Kp^2\); and for \(\deg b=2\) it is \(W\) plus exactly two
further dimensions (Theorem B). The depth is not monotone in the degeneracy: a
nonlinear \(b\) shortens the generic filtration from 5 to 4, a cubic
residual potential lengthens it to 6, and a residual potential of degree
at most two stops it at 2 with a six-dimensional core. The statements are
all-degree theorems proved by differentiation and polynomial degree.

Section 7 removes the restriction to a constant coefficient of \(p^2\).
For \(H=c(q)p^2+b(q)p+f(q)\) with \(1\le\deg c\le3\) the first refinement
is finite-dimensional, it lies in an explicit weighted box, and the core
is \(\operatorname{span}\{1,H\}\) unless \(H\) is, up to a constant, a
multiple of the square of a polynomial \(Q=up+v\) with \(u\) linear, in
which case it is \(\operatorname{span}\{1,Q,H\}\) (Theorems D and E). That proof is computer-assisted: a
hand-proved a priori bound reduces the all-degree statement to exact
linear algebra on at most 70 monomials. Together with Section 10 of the
inhomogeneous note this covers every sixfold-leading sextic of degree at
most two in a complementary coordinate. Section 9 states exactly which
parts are replayed by computation and what remains open.

## 1. The gates in the shifted chart

The substitution \((q,p)\mapsto(q,P)\) is a polynomial symplectic map. It
is affine only when \(b''=0\), so the covariance rule (6) of the
inhomogeneous note does not apply to it when \(b''\ne0\). The Poisson
derivation is nevertheless intrinsic, while the fixed flat gates must be
transported by hand.

**Lemma 1.** Regard \(G\) as a polynomial in \((q,P)\), and let
subscripts denote partial derivatives in that chart. Then

\[
D_HG=F'G_P-2P\,G_q ,
\tag{3}
\]

\[
T_3(H,G)=(F'''+b'''P)\,G_{PPP}-3b''\,G_{qPP},
\tag{4}
\]

\[
T_5(H,G)=\bigl(f^{(5)}-\tfrac52 b''''b'\bigr)G_{PPPPP}-5b''''\,G_{qPPPP}.
\tag{5}
\]

**Proof.** In the original chart \(H_{pp}=2\) is constant, so every mixed
derivative of \(H\) with at least two \(p\)-derivatives and at least one
further derivative vanishes. Only the terms \(j=0,1\) of the contraction
survive:

\[
T_3=(f'''+b'''p)\,\partial_p^3G-3b''\,\partial_q\partial_p^2G,\qquad
T_5=f^{(5)}\,\partial_p^5G-5b''''\,\partial_q\partial_p^4G,
\]

where \(b^{(5)}=0\) was used. At fixed \(p\) one has
\(\partial_p=\partial_P\) and
\(\partial_q|_p=\partial_q|_P+\tfrac12b'\partial_P\). Substituting
\(p=P-\tfrac12b\) gives the coefficient
\(f'''-\tfrac12bb'''-\tfrac32b'b''+b'''P\) of \(G_{PPP}\), and
\(F'''=f'''-\tfrac14(b^2)'''=f'''-\tfrac32b'b''-\tfrac12bb'''\). This is
(4). The same substitution in \(T_5\) gives (5). Finally (3) is the
Poisson bracket in the symplectic chart \((q,P)\) with \(H=P^2+F\).
\(\square\)

Formula (4) has the shape of the affine-family gate of Section 10 with
\(f\) replaced by \(F\). The change is entirely in the derivation (3),
which now raises the \(P\)-degree through \(-2PG_q\).

## 2. The case \(b''=0\), including \(b=0\)

**Theorem A.** Let \(b''=0\). With arbitrary polynomials \(A,B,C\in K[q]\)
at stage zero, the filtration is

| Stage | Space |
|---|---|
| \(S^0\) | \(A+BP+CP^2\) |
| \(S^1\) | the same with \(C\) constant |
| \(S^2\) | the same with \(C\) constant and \(B\) affine |
| \(S^3\) | \(cH+(aq+\beta)P+R(q)\), \(\deg R\le2\) |
| \(S^4\) | \(cH+R(q)\), \(\deg R\le2\) |
| \(S^5=D_\infty\) | \(\operatorname{span}\{1,H\}\) |

Each inclusion is strict, and \(q\in S^4\setminus S^5\). The least depth
is 5.

**Proof.** When \(b\) is affine the map \((q,p)\mapsto(q,P)\) is affine
with determinant one, so by covariance (6) it suffices to treat
\(H=P^2+F\) in the flat chart \((q,P)\), with \(\deg F=6\). Then
\(T_3=F'''G_{PPP}\) and \(F'''\ne0\), so the third gate holds exactly on
\(P\)-degree at most two, where \(T_5\) vanishes. This is \(S^0\). For
\(G=A+BP+CP^2\),

\[
D_HG=F'B+(2CF'-2A')P-2B'P^2-2C'P^3 .
\tag{6}
\]

Membership of \(D_HG\) in \(S^0\) is \(C'=0\). Membership in \(S^1\) adds
\(B''=0\). Membership in \(S^2\) adds \((2CF'-2A')''=0\), which is
\(A=cF+R\) with \(c=C\) and \(\deg R\le2\), so \(G=cH+BP+R\). For such
\(G\) with \(B=aq+\beta\),

\[
D_HG=F'B-2R'P-2aP^2 .
\tag{7}
\]

This lies in \(S^3\) exactly when \(F'B+2aF\) has degree at most two. Its
coefficient of \(q^6\) is \(8aF_6\), so \(a=0\), and then \(\beta F'\) of
degree five forces \(\beta=0\). Hence \(S^4=\{cH+R\}\). There
\(D_HG=-2R'P\), which lies in \(S^4\) only if \(R'=0\). The space
\(\operatorname{span}\{1,H\}\) is annihilated by \(D_H\), so the filtration
is stationary from \(S^5\). The polynomial \(q\) has \(c=0\), \(R=q\), so
it lies in \(S^4\) and not in \(S^5\). \(\square\)

For \(H=q^6+p^2\) the spaces of total degree at most six have dimensions
\(18,14,10,6,4,2\). The bounded benchmark is finite because the input
degree is bounded. The all-degree spaces \(S^0\), \(S^1\), \(S^2\) are
infinite-dimensional, and the benchmark reaches 2 at depth 5 because
\(S^3\) is already finite-dimensional and contained in degree at most six.

## 3. The first two refinements for \(b''\ne0\)

Let \(m=\deg b\in\{2,3,4\}\) and

\[
W=K[q]+K[q]\,P+K\,P^2 .
\]

**Lemma 2.** If \(b''\ne0\), then \(W\subseteq S^0\), and a polynomial of
\(P\)-degree at most two lies in \(S^0\) exactly when it lies in \(W\).

**Proof.** On \(P\)-degree at most two, (5) vanishes and (4) reduces to
\(-6b''C'\), where \(C\) is the coefficient of \(P^2\). \(\square\)

**Lemma 3.** If \(b''\ne0\), then \(S^1\subseteq W\).

**Proof.** Let \(G\in S^0\) have \(P\)-degree \(d\ge2\) and leading
coefficient \(g(q)\ne0\). The coefficient of \(P^{d-2}\) in (4), divided
by \(d(d-1)\), is

\[
(d-2)\,b'''g-3b''g'=0 .
\tag{8}
\]

If \(m\ge3\), comparing leading coefficients in (8) gives
\(3\deg g=(d-2)(m-2)\). If \(m=2\), then \(b'''=0\) and (8) gives
\(g'=0\). In both cases \(d=2\) forces \(g\) constant, so it remains to
exclude \(d\ge3\) for \(G\in S^1\).

Let \(m\ge3\) and \(d\ge3\). Then \(n=\deg g=(d-2)(m-2)/3>0\), so
\(g'\ne0\). By (3) the polynomial \(D_HG\) has \(P\)-degree \(d+1\) and
leading coefficient \(-2g'\) of degree \(n-1\). Since \(D_HG\in S^0\), the
degree relation applied to it requires that degree to be
\((d-1)(m-2)/3>n-1\). This is a contradiction.

Let \(m=2\) and \(d\ge3\), and normalize \(g=1\). Write \(g_1\) for the
coefficient of \(P^{d-1}\) in \(G\). The coefficient of \(P^{d-3}\) in
(4), divided by \((d-1)(d-2)\), is

\[
d\,F'''-3b''g_1'=0 ,
\tag{9}
\]

so \(g_1'=dF'''/(3b'')\), with \(b''\) a nonzero constant. Here
\(\deg F=6\), so \(g_1'\) has degree three. By (3) the coefficient of
\(P^{d+1}\) in \(D_HG\) is \(-2g'=0\) and the coefficient of \(P^d\) is
\(-2g_1'\). Thus \(D_HG\in S^0\) has \(P\)-degree \(d\ge3\) with a
nonconstant leading coefficient, contradicting (8). \(\square\)

**Theorem B.** Let \(b''\ne0\).

(a) If \(\deg b\in\{3,4\}\), then \(S^0=W\). If \(\deg b=2\), write
\(\beta=b''\in K^\times\); then \(S^0=W\oplus KG_3\oplus KG_4\) with

\[
G_3=p^3+\frac{f''}{\beta}\,p^2,\qquad
G_4=p^4+\frac{4f''}{3\beta}\,p^3+\frac{2f''^2}{3\beta^2}\,p^2,
\]

of total degrees 6 and 10. Neither lies in \(S^1\).

(b) In all cases

\[
S^1=\{A(q)+(aq+\beta)P+cP^2\}=K[q]\oplus Kp\oplus Kqp\oplus KH,
\tag{10}
\]

\[
S^2=\{cH+(aq+\beta)P+R(q):\deg R\le2\}
=\operatorname{span}\{1,q,q^2,P,qP,H\},
\tag{11}
\]

and \(S^0\supsetneq S^1\supsetneq S^2\). Moreover \(D_HS^2\subseteq S^1\),
and for \(G=cH+(aq+\beta)P+R\in S^2\),

\[
G\in S^3\iff\deg\bigl((aq+\beta)F'+2aF\bigr)\le2 .
\tag{12}
\]

**Proof of (a).** Work in the original chart, where
\(W=K[q]+K[q]p+Kp^2\), and put \(U=G_{pp}\). By the proof of Lemma 1,

\[
T_3=(f'''+b'''p)U_p-3b''U_q,\qquad T_5=f^{(5)}U_{ppp}-5b''''U_{qpp}.
\]

Let \(U\ne0\) have \(p\)-degree \(e\) and leading coefficient \(u(q)\).
The coefficient of \(p^e\) in \(T_3\) gives \(e\,b'''u=3b''u'\), hence
\(3\deg u=e(m-2)\) when \(m\ge3\). If \(m=3\), then \(b''''=0\) and
\(f^{(5)}\ne0\), so \(T_5=0\) forces \(e\le2\), and \(3\deg u=e\) forces
\(e=0\). If \(m=4\) and \(e\ge2\), the coefficient of \(p^{e-2}\) in \(T_5\)
is \(-5b''''e(e-1)u'\), so \(u'=0\), contradicting \(3\deg u=2e\); and
\(e=1\) contradicts integrality. So \(e=0\) in both cases, then
\(3b''U'=0\), and \(U\) is constant. This is \(G\in W\).

If \(m=2\), then \(T_3=EU\) for the vector field
\(E=f'''\partial_p-3\beta\partial_q\), and \(\xi=p+f''/(3\beta)\) satisfies
\(E\xi=0\). In the polynomial coordinates \((q,\xi)\) the field is
\(-3\beta\partial_q\), so its polynomial kernel is \(K[\xi]\). For
\(U=\Phi(\xi)\) the fifth gate is \(f^{(5)}\Phi'''(\xi)\) with
\(f^{(5)}\ne0\), so \(\Phi\) is at most quadratic. Integrating
\(1,\xi,\xi^2\) twice in \(p\) gives \(p^2/2\), \(G_3/6\), \(G_4/12\)
modulo \(K[q]+K[q]p\). The degrees follow from \(\deg f''=4\). By Lemma 3,
\(G_3,G_4\notin S^1\). \(\square\)

**Proof of (b).** By Lemmas 2 and 3, \(S^1=\{G\in W:D_HG\in S^0\}\). For
\(G=A+BP+cP^2\) formula (6) with \(C=c\) shows that \(D_HG\) has
\(P\)-degree at most two with \(P^2\)-coefficient \(-2B'\). By Lemma 2
this is in \(S^0\) exactly when \(B''=0\). The second description in (10)
holds because \(P\equiv p\) and \(qP\equiv qp\) modulo \(K[q]\), and
\(P^2\equiv H\) modulo \(K[q]\). Next, \(D_HG\in S^1\) requires in
addition that the coefficient \(2cF'-2A'\) of \(P\) be affine, which is
\(A=cF+R\) with \(\deg R\le2\). This is (11). Formula (7) holds for these
\(G\), and \(D_HG=F'B-2R'P-2aP^2\) has the form \(c_1H+B_1P+R_1\) with
\(c_1=-2a\), \(B_1=-2R'\) affine, and \(R_1=F'B+2aF\). It lies in \(S^2\)
exactly when \(\deg R_1\le2\), which is (12). Strictness:
\(q^2P\in W\setminus S^1\), and \(q^3\in S^1\setminus S^2\).
\(\square\)

The first two refinement spaces therefore do not see \(f\) at all beyond
the definition of \(H\). In total degree at most \(n\ge6\) their
dimensions are \(n+4\) and \(6\), and the static dimension is \(2n+2\),
plus one when \(\deg b=2\), plus one more when \(\deg b=2\) and
\(n\ge10\).

## 4. The three terminal regimes for \(b''\ne0\)

**Theorem C.** Let \(b''\ne0\) and \(N=\deg F\).

If \(N\ge4\), then \(S^3=\{cH+R:\deg R\le2\}\) and
\(S^4=D_\infty=\operatorname{span}\{1,H\}\). The least depth is 4, with
\(q\in S^3\setminus S^4\).

If \(N=3\), then

\[
S^3=\operatorname{span}\{1,q,q^2,P,H\},\quad
S^4=\operatorname{span}\{1,q,P,H\},\quad
S^5=\operatorname{span}\{1,q,H\},\quad
S^6=D_\infty=\operatorname{span}\{1,H\}.
\]

The least depth is 6, with \(q\in S^5\setminus S^6\).

If \(N\le2\), then \(S^2=D_\infty=\operatorname{span}\{1,q,q^2,P,qP,P^2\}\),
the polynomials of degree at most two in the chart \((q,P)\). The least
depth is 2, and \(D_\infty\) is six-dimensional.

**Proof.** Use (12) and (7). Let \(N\ge4\). The coefficient of \(q^N\) in
\((aq+\beta)F'+2aF\) is \((N+2)aF_N\), so \(a=0\), and then
\(\deg(\beta F')=N-1\ge3\) gives \(\beta=0\). On \(S^3=\{cH+R\}\),
\(D_HG=-2R'P\) lies in \(S^3\) only if \(R'=0\). The span of \(1\) and
\(H\) is \(D_H\)-invariant and inside \(S^0\), hence equals \(D_\infty\).

Let \(N=3\). The coefficient of \(q^3\) is \(5aF_3\), so \(a=0\), while
\(\beta F'\) is quadratic and imposes nothing. So
\(S^3=\{cH+\beta P+R\}\). For such \(G\), \(D_HG=\beta F'-2R'P\). It lies
in \(S^3\) exactly when \(-2R'\) is constant, so
\(S^4=\{cH+\beta P+r_1q+r_0\}\). There \(D_HG=\beta F'-2r_1P\) lies in
\(S^4\) exactly when \(\beta F'\) is affine. Since \(F'\) is quadratic,
\(\beta=0\) and \(S^5=\{cH+r_1q+r_0\}\). Finally \(D_HG=-2r_1P\) lies in
\(S^5\) only if \(r_1=0\).

Let \(N\le2\). Then \((aq+\beta)F'+2aF\) always has degree at most two,
so \(S^3=S^2\) by (12). Hence \(D_HS^2\subseteq S^2\), and an invariant
subspace of \(S^0\) lies in \(D_\infty\). Since \(F\) has degree at most
two, \(\operatorname{span}\{1,q,q^2,P,qP,H\}\) is the space of quadratic
polynomials in \((q,P)\). The depth is sharp because \(S^1\) is
infinite-dimensional. \(\square\)

The six-dimensional core has a structural explanation. When \(N\le2\) the
Hamiltonian is a quadratic polynomial in the symplectic chart \((q,P)\).
The quadratic polynomials of that chart form a Lie algebra under the
Poisson bracket, so they are stable under \(D_H\), and Lemma 2 shows that
they pass both flat gates even though the chart is not flat. The perfect
square \(H=(p+\beta(q))^2\) with \(\deg\beta=3\) is the case
\(F=0\), where \(P\) itself is a polynomial first integral. The mechanism
breaks precisely at \(N=3\): the generator \(P\) then survives three
further refinements and \(q\) survives four, which is the longest
filtration in the family.

## 5. Hypotheses used

Characteristic zero is used through the nonvanishing of the integers
\(d(d-1)\), \((d-1)(d-2)\), \(3\), \(m(m-1)\), \(N+2\), and through the
fact that differentiation lowers a positive degree by exactly one. The
bound \(\deg b\le4\) is used for \(b^{(5)}=0\) in Lemma 1 and for the
leading form to be \(f_6q^6\). The hypothesis \(\deg f=6\) enters Theorem A
through \(F'''\ne0\) and \(\deg F=6\), and enters Lemma 3 only in the case
\(m=2\), through \(\deg F'''\ge1\). For \(m\in\{3,4\}\) Lemma 3 and Theorem
B use no property of \(f\). Theorem C uses only \(N\). The constant top
coefficient of \(p^2\) is essential: it is what makes \(H_{pp}\) constant
in Lemma 1.

## 6. Adapted linear coordinates

Let \(L,M\) be independent linear forms and
\(H=c_0M^2+b(L)M+f(L)+c_1\) with \(c_0\ne0\), \(\deg f=6\),
\(\deg b\le4\). By covariance (6) of the inhomogeneous note, applied to
the linear map \((q,p)\mapsto(L,M)\), the scalar \(c_0\), and the constant
\(c_1\), all statements above hold with \(q,p,b,f\) replaced by
\(L,M,b/c_0,f/c_0\). Only affine substitutions are used in this step. The
verifier replays five rational affine maps with determinants
\(5,5,4,2,3\) and scalars \(3/2,-2,2/3,5,-1/2\), one for each regime and
each value of \(\deg b\) that produces a distinct proof branch.


## 7. Nonconstant coefficient of the squared complement

Now let

\[
H=c(q)\,p^2+b(q)\,p+f(q),\qquad \deg f=6,\quad k=\deg c\in\{1,2,3\},
\quad \deg b\le4 .
\]

These are all sextics with leading form \(f_6q^6\) that have degree
exactly two in \(p\) and a nonconstant top coefficient. Write \(c_k\),
\(b_4\), \(f_6\) for the indicated coefficients, with \(b_4=0\) allowed.
Expanding the contractions as in Lemma 1,

\[
T_3=(f'''+b'''p+c'''p^2)G_{ppp}-3(b''+2c''p)G_{qpp}+6c'G_{qqp},
\tag{13}
\]

\[
T_5=f^{(5)}G_{ppppp}-5b''''G_{qpppp}+20c'''G_{qqppp},
\qquad D_H=(f'+b'p+c'p^2)\partial_p-(2cp+b)\partial_q .
\tag{14}
\]

**Weights.** Give \(q\) and \(p\) positive integer weights. Each \(T_j\)
sends a pair of monomials to a multiple of one monomial and lowers the
total weight by \(j(\operatorname{wt}q+\operatorname{wt}p)\). For a
polynomial \(G\ne0\) let \(G^\sharp\) be its component of highest weight.
The table fixes the weights, the weighted leading part \(H^\sharp\), and a
bound used below. In every row all other terms of \(H\) have strictly
smaller weight.

| Case | \(\operatorname{wt}q,\operatorname{wt}p\) | \(H^\sharp\) | Box bound |
|---|---|---|---|
| \(k=1,\ \deg b\le3\) | 2, 5 | \(f_6q^6+c_1qp^2\) | 22 |
| \(k=1,\ \deg b=4\) | 1, 3 | \(b_4q^4p+c_1qp^2\) | 13 |
| \(k=2,\ \deg b\le3\) | 2, 4 | \(f_6q^6+c_2q^2p^2\) | 24 |
| \(k=2,\ \deg b=4\) | 2, 4 | \(f_6q^6+b_4q^4p+c_2q^2p^2\) | 18 |
| \(k=3\) | 2, 3 | \(f_6q^6+c_3q^3p^2\) | 26 |

**Lemma 4 (weighted transfer).** For every \(r\ge0\), if \(G\in S^r(H)\)
then \(G^\sharp\in S^r(H^\sharp)\). The space \(S^r(H^\sharp)\) is spanned
by weighted-homogeneous polynomials, and if it is finite-dimensional then
\(\dim S^r(H)\le\dim S^r(H^\sharp)\).

**Proof.** This is Lemma 1 of the inhomogeneous note with the weighted
grading in place of total degree. By induction the component of
\(D_H^iG\) in the top possible weight is \(D_{H^\sharp}^iG^\sharp\), and
the component of \(T_j(H,D_H^iG)\) in the top possible weight is
\(T_j(H^\sharp,D_{H^\sharp}^iG^\sharp)\); either may be zero. The gates of
\(H^\sharp\) are homogeneous operators, so its refinement spaces are
graded. Finally a subspace whose leading components span a
finite-dimensional space has that dimension at most. \(\square\)

**Lemma 5 (the box).** Let \(G\) be weighted-homogeneous in
\(S^1(H^\sharp)\). Then the weight of \(G\) is at most the box bound.

**Proof.** The coefficients of \(G\) in powers of \(p\) are monomials in
\(q\). Let \(G\) have \(p\)-degree \(d\) and leading term
\(\gamma q^np^d\). Only the three terms of (13) carrying \(c\) reach
\(p^{d-1}\), and only \(c'p^2\partial_p-2cp\partial_q\) reaches \(p^{d+1}\)
in (14). Hence for \(d\ge1\) the coefficient of \(p^{d-1}\) in
\(T_3(H^\sharp,G)\) is

\[
\gamma c_k\,k\,d\,\lambda_k(d,n)\,q^{n+k-3},\qquad
\lambda_k(d,n)=(k-1)(k-2)(d-1)(d-2)-6(k-1)(d-1)n+6n(n-1),
\tag{15}
\]

Formula (15) is used as a polynomial coefficient when \(n+k-3\ge0\).
When \(n+k-3<0\), the possibilities are \(k=1,n=0,1\) or
\(k=2,n=0\). In each case the differentiated coefficient is zero and
\(\lambda_k(d,n)=0\) identically; these cases impose the displayed
relation directly without using a negative power of \(q\).

The coefficient of \(p^{d+1}\) in \(D_{H^\sharp}G\) is

\[
\gamma c_k\,(kd-2n)\,q^{n+k-1}.
\tag{16}
\]

If \(d=0\) and \(n\ge1\), then by (16) \(D_{H^\sharp}G\) has \(p\)-degree
one with leading exponent \(N=n+k-1\), and \(\lambda_k(1,N)=6N(N-1)\)
forces \(N\le1\). So \(n\le1\), and the weight is at most 2.

Let \(d\ge1\), so \(\lambda_k(d,n)=0\).

Case \(k=1\). Here \(\lambda_1=6n(n-1)\), so \(n\le1\). If \(\deg b\le3\),
then \(T_5=720f_6\,q\,\partial_p^5G\) forces \(d\le4\), and the weight
\(2n+5d\) is at most 22. If \(\deg b=4\), then
\(T_5=-120b_4\,\partial_q\partial_p^4G\). For \(n=1\) its coefficient of
\(p^{d-4}\) forces \(d\le3\). For \(n=0\) and \(d\ge3\) the next term of
\(G\) is \(\gamma'q^3p^{d-1}\), and the coefficient of \(qp^{d-2}\) in
(13) is \(36c_1(d-1)\gamma'+24b_4d(d-1)(d-2)\gamma\), so
\(\gamma'=-\tfrac{2b_4}{3c_1}d(d-2)\gamma\ne0\). This term is the only one
of \(G\) contributing to \(q^2p^{d-5}\) in \(T_5\), so \(d\le4\). The
weight \(n+3d\) is at most 12.

Case \(k=2\). Here \(\lambda_2=6n(n-d)\), so \(n\in\{0,d\}\). If
\(\deg b\le3\), then \(T_5=720f_6\,q\,\partial_p^5G\) forces \(d\le4\) and
the weight \(2n+4d\) is at most 24. If \(\deg b=4\) and \(n=0\), then by
(16) \(D_{H^\sharp}G\) has \(p\)-degree \(d+1\) and leading exponent 1,
which is neither 0 nor \(d+1\). So \(n=d\). The coefficient of \(p^{d-4}\)
in \(T_5\) is then \(-120b_4d^2(d-1)(d-2)(d-3)\gamma q^{d-1}\), so
\(d\le3\) and the weight \(6d\) is at most 18.

Case \(k=3\). The coefficient of \(p^{d-3}\) in \(T_5\) is
\(120c_3d(d-1)(d-2)n(n-1)\gamma q^{n-2}\), so \(d\ge3\) forces \(n\le1\).
Then \(\lambda_3(d,0)=2(d-1)(d-2)\ne0\) and
\(\lambda_3(d,1)=2(d-1)(d-8)\), which leaves \((d,n)=(8,1)\). For \(d\le2\),
\(\lambda_3(1,n)=6n(n-1)\) and \(\lambda_3(2,n)=6n(n-3)\). The largest
weight \(2n+3d\) is 26. \(\square\)

**Theorem D.** In the setting of this section:

(i) \(S^1(H)\) is finite-dimensional, of dimension at most
\(6,5,3,3,3\) in the five rows of the table, and every element has
weighted degree at most the box bound.

(ii) If \(k\in\{1,3\}\), or \(k=2\) and \(b_4^2\ne4f_6c_2\), then
\(D_\infty(H)=\operatorname{span}\{1,H\}\). More precisely
\(S^r(H)=\operatorname{span}\{1,H\}\) for \(r\ge3\) when \(k=1\) and for
\(r\ge2\) when \(k\in\{2,3\}\). These depths are attained by \(H^\sharp\)
itself.

(iii) If \(k=2\), \(\deg b=4\) and \(b_4^2=4f_6c_2\), then
\(2\le\dim D_\infty(H)\le3\), \(\dim S^1(H)\le3\), and both values of
\(\dim D_\infty\) occur. Theorem E decides which.

**Proof.** By Lemmas 4 and 5 every element of \(S^1(H)\) has leading
component of weight at most the bound, which gives the last clause of
(i). The dimension of a refinement space is unchanged by extension of
the base field, since it is the kernel of a linear system over \(K\), and
by covariance it is unchanged under \(q\mapsto\lambda q\),
\(p\mapsto\mu p\), \(H\mapsto aH\). Over an algebraic closure these
normalize \(H^\sharp\) to one of

\[
q^6+qp^2,\qquad q^4p+qp^2,\qquad q^6+q^2p^2,\qquad
q^6+t\,q^4p+q^2p^2\ \ (t^2=b_4^2/(f_6c_2)\ne0),\qquad q^6+q^3p^2 .
\]

For each model, Lemma 5 confines \(S^1\) to the monomials inside the box,
so the exact rational kernel of the gates on those monomials is the
complete space \(S^r\), \(r\ge1\). The computed dimensions of
\(S^1,S^2,S^3\) are \(6,3,2\), then \(5,3,2\), then \(3,2,2\), and
\(3,2,2\) for the last model. For the one-parameter model the gate
matrices have entries in \(\mathbb Q[t]\). In each weight the gcd of a set
of maximal minors is a nonzero constant at depth one and a constant
multiple of \(t^2-4\) at depth two, with generic dimensions 3 and 2. A
nonvanishing minor bounds the kernel dimension from above, so
\(\dim S^1\le3\) for all \(t\) and \(\dim S^2\le2\) for \(t^2\ne4\).
Lemma 4 transfers the bounds to \(H\), and
\(\operatorname{span}\{1,H\}\subseteq S^r(H)\) gives equality in (ii). At
\(t=\pm2\) the model is \(q^2(p\pm q^2)^2\) and its core is
\(\operatorname{span}\{1,\ q(p\pm q^2),\ H\}\), which gives the upper bound
in (iii). The core is three-dimensional for \(H=(qp+q^3)^2\) and for
\(H=(qp+q^3+1)^2-1\), and two-dimensional for
\((qp+q^3)^2+q\), \((qp+q^3)^2+p\) and \((qp-q^3)^2+q^5\); each of these
is computed exactly inside the box, which is complete by (i).
\(\square\)

Individual Hamiltonians can stabilize earlier than the model: for
\(H=q^6+(q^3+q+1)p^2\) already \(S^1=\operatorname{span}\{1,H\}\). Because
of (i), the exact \(S^r(H)\), \(r\ge1\), of any given \(H\) in this family
is obtained by exact linear algebra on the box, and that computation is
complete for all polynomial degrees.

**Theorem E (the discriminant locus).** In the setting of this section,
\(\dim D_\infty(H)=3\) exactly when all three conditions hold:
\(c=c_2u^2\) for a monic linear polynomial \(u\); \(u\) divides \(b\); and
\(f-b^2/(4c)\) is constant. In that case put

\[
Q=u\,p+\frac{b}{2c_2u}.
\]

Then \(H=c_2Q^2+\text{const}\) and
\(S^1(H)=D_\infty(H)=\operatorname{span}\{1,Q,H\}\). In every other case
\(D_\infty(H)=\operatorname{span}\{1,H\}\). The three conditions imply
\(\deg b=4\) and \(b_4^2=4f_6c_2\).

**Proof.** Suppose the conditions hold and write \(b=uw\). Then
\(cp^2+bp+b^2/(4c)=c_2(up+w/(2c_2))^2=c_2Q^2\), so \(H=c_2Q^2+\text{const}\)
and \(D_HQ=0\). Since \(Q\) has \(p\)-degree one with a linear coefficient,
every term of (13) and (14) vanishes on it. Hence \(Q\in D_\infty\), and
with Theorem D(i) and (iii), \(S^1=D_\infty=\operatorname{span}\{1,Q,H\}\).
Comparing degrees, \(\deg w=3\), so \(\deg b=4\) and \(b_4^2=4f_6c_2\).

Conversely let \(\dim D_\infty(H)=3\). By Theorem D this forces \(k=2\),
\(\deg b=4\), \(b_4^2=4f_6c_2\), and by Lemma 4 the leading components of
\(D_\infty(H)\) span \(D_\infty(H^\sharp)\), whose weights are 0, 6, 12. So
there is \(G\in D_\infty(H)\) of weight 6. The monomials of weight at most 6
are \(1,q,q^2,q^3,p,qp\), and \(G^\sharp\) is a multiple of
\(qp+\tfrac{b_4}{2c_2}q^3\), so after scaling \(G=up+v\) with \(u\) monic
linear and \(\deg v\le3\). The bracket lowers weight by 6 and
\(D_{H^\sharp}G^\sharp=0\), so \(D_HG\) has weight below 12. It lies in
\(D_\infty(H)\), which is invariant, and the only elements of
\(D_\infty(H)\) of weight below 12 are in \(\operatorname{span}\{1,G\}\).
Thus \(D_HG=aG+d\) with \(a,d\in K\). By (14),

\[
D_HG=(c'u-2c)\,p^2+(b'u-b-2cv')\,p+(f'u-bv') .
\]

The coefficient of \(p^2\) gives \(c'u=2c\), hence \(c=c_2u^2\). The
coefficient of \(p\) gives \(b'u-b-2c_2u^2v'=au\); reducing modulo \(u\)
gives \(u\mid b\). With \(b=uw\) one has \(b'u-b=u^2w'\), so
\(u\,(w'-2c_2v')=a\), and evaluating at the root of \(u\) gives \(a=0\) and
\(v'=w'/(2c_2)\). The constant coefficient is then
\(u\,(f'-ww'/(2c_2))=d\), so \(d=0\) and \(f-w^2/(4c_2)=f-b^2/(4c)\) is
constant. \(\square\)

**Proposition (strict first step).** For every nonconstant \(c\), the
polynomial \(q^2\) passes both static gates and

\[
T_3\bigl(H,D_H(q^2)\bigr)=-24\,c'\,(qc)''\ne0 .
\]

Hence \(S^0(H)\supsetneq S^1(H)\), and whenever \(S^1(H)=D_\infty(H)\) the
least depth is exactly one, although \(S^0\) is not classified.

**Proof.** A polynomial in \(q\) alone is annihilated by (13) and (14).
By (14), \(D_H(q^2)=-4qc\,p-2qb\), and on a polynomial of \(p\)-degree one
only the last term of (13) survives. \(\square\)

## 8. Classifier and schema 2

The module `quadratic_sixfold.py` implements the results of this note for
rational input. It finds the rational linear form \(L\) with
\(H_6=aL^6\), takes \(M=p\) or \(M=q\) as complement, and requires degree
exactly two in \(M\). The property of being a polynomial in \(L\) of
degree two in \(M\) does not depend on the choice of complement, and the
map \((q,p)\mapsto(L,M)\) has determinant \(\pm1\). For a constant top
coefficient it returns the closed-form filtration of Theorems A, B, C
with the regime decided by \(b''\) and \(\deg(f-b^2/4)\) after dividing by
the top coefficient. For a nonconstant top coefficient it returns the
exact \(S^1,S^2,\dots\) and the core from the box of Theorem D, asserts
nothing about \(S^0\), evaluates the criterion of Theorem E in closed
form, and raises an error if the box computation and the criterion
disagree. Every report carries a sharpness witness, and the classifier
verifies that it fails first at the reported least depth.

Schema `hamiltonian-sextic-core/1` cannot express these results. Its
contract, enforced by `verify_sextic_core.check_report`, requires \(S^1\),
\(S^2\) and \(D_\infty\) to be of one kind and the depth to be at most two,
while here the stages mix infinite families with finite spaces and the
depth reaches six. The results are therefore exposed through an opt-in
schema `hamiltonian-sextic-core/2`, by `sextic_core.classify_sextic_v2` or
`partner_lab.py sextic-core --schema 2`. Schema 1 is the default and its
function, output and regressions are unchanged; in particular
\(q^6+q+p+p^2\) remains unsupported there.

A schema-2 report has `classification.stages`, a list indexed by
refinement depth. Each entry has `status` equal to `classified`, with a
`space`, or `unknown`, with `space` null and a reason. An unknown stage
asserts nothing, so an unclassified \(S^0\) is never confused with a
computed space. A space is a `finite_basis`, a `polynomial_family` (a free
module over \(\mathbb Q[L]\)), or a `module_plus_finite` (such a module
plus a finite rational span, as in (10)). The field `depth` records a value
and a kind: `least`, with a checked `sharpness_witness`, for this family,
and `sufficient` for results carried over from schema 1, whose \(S^1\),
\(S^2\), \(D_\infty\), obstruction and lift certificates are reproduced
verbatim.

## 9. Audit

Six deterministic commands, from the repository root, replay the
evidence. All use exact rational arithmetic.

```
python research/hamiltonian/c3_strata/verify_quadratic_sixfold.py
python research/hamiltonian/c3_strata/verify_quadratic_sixfold_models.py
python research/hamiltonian/c3_strata/verify_sextic_core_v2.py
python research/hamiltonian/c3_strata/audit_quadratic_sixfold_steps.py
python -m unittest discover -s research/hamiltonian/c3_strata -p "test_quadratic_sixfold.py" -q
python -m unittest discover -s research/hamiltonian/c3_strata -p "test_sextic_core.py" -q
```

The first three take roughly six, six and three minutes and print the
receipts committed as `QUADRATIC_SIXFOLD_REPLAY.json`,
`QUADRATIC_SIXFOLD_MODELS_REPLAY.json` and `SEXTIC_CORE_V2_REPLAY.json`.
Each receipt records the SHA-256 of the sources it was produced from, and
the regressions fail if a committed receipt is stale against those
sources. The source manifest `research/hamiltonian/MANIFEST.sha256` lists
every file added or changed here.

**Constant top coefficient.** Kernels on all inputs of total degree at
most six, untruncated gate outputs, stages 0 through 7, compared as
rational spans with Theorems A, B, C including the static stage.

| Input | \(\deg b\) | \(N\) | Bounded dimensions \(S^0,\dots,S^7\) |
|---|---|---|---|
| \(q^6+p^2\) | none | 6 | 18, 14, 10, 6, 4, 2, 2, 2 |
| generic \(f\), \(b=0\) | none | 6 | 18, 14, 10, 6, 4, 2, 2, 2 |
| generic \(f\), \(b=3q-2\) | 1 | 6 | 18, 14, 10, 6, 4, 2, 2, 2 |
| \(q^6+q^2p+p^2\) | 2 | 6 | 15, 10, 6, 4, 2, 2, 2, 2 |
| generic \(f\), \(b=-2q^2+q+3\) | 2 | 6 | 15, 10, 6, 4, 2, 2, 2, 2 |
| generic \(f\), \(b=2q^3-q^2+4\) | 3 | 6 | 14, 10, 6, 4, 2, 2, 2, 2 |
| \((p+\beta)^2+F\), \(\deg F=5\) | 3 | 5 | 14, 10, 6, 4, 2, 2, 2, 2 |
| \((p+\beta)^2+F\), \(\deg F=4\) | 3 | 4 | 14, 10, 6, 4, 2, 2, 2, 2 |
| \((p+\beta)^2+F\), \(\deg F=3\) | 3 | 3 | 14, 10, 6, 5, 4, 3, 2, 2 |
| \((p+q^3)^2+q^3\) | 3 | 3 | 14, 10, 6, 5, 4, 3, 2, 2 |
| \((p+\beta)^2+3q^2-q\) | 3 | 2 | 14, 10, 6, 6, 6, 6, 6, 6 |
| \((p+\beta)^2+5q\) | 3 | 1 | 14, 10, 6, 6, 6, 6, 6, 6 |
| \((p+q^3)^2\) | 3 | none | 14, 10, 6, 6, 6, 6, 6, 6 |
| \(q^6+q^4p+p^2\) | 4 | 8 | 14, 10, 6, 4, 2, 2, 2, 2 |
| generic \(f\), \(b=3q^4-q^3+2q+1\) | 4 | 8 | 14, 10, 6, 4, 2, 2, 2, 2 |

Here \(\beta=q^3+q^2-3q+1\) and the generic sextic is
\(2q^6-3q^5+q^4+5q^3-q^2+7q+1\). The static stage is also compared at
input degree 12 on six cases, with dimensions 28 for \(\deg b=2\) and 26
for \(\deg b\in\{3,4\}\), as Theorem B(a) predicts. Exact identities with
no bound on the input: formulas (3), (4), (5) against the defining star
product on two probes of \(P\)-degree up to six; invariance and static
gates of each core; the first failing iterate of each witness, namely 5,
4, 6 for \(q\), 2 for \(q^3\), and 1 for \(G_3\) and \(G_4\). Five rational
affine maps with determinants \(5,5,4,2,3\) and non-unit scalars confirm
covariance of every bounded kernel.

**Nonconstant top coefficient.** The five models are computed inside
their boxes and again inside strictly larger boxes (weights up to 40, 26,
40, 36, 40), with identical spaces. The parametric analysis reports
exceptional factor 1 at depth one and \((t-2)(t+2)\) at depth two. The
classifier is then compared, stage by stage, with kernels on all inputs
of total degree at most 8 for 24 Hamiltonians and for 6 of them after a
rational affine map with non-unit determinant and scalar, covering every
regime of both parts and generic lower terms. Ten of the 24 lie on the
discriminant locus: three satisfy the criterion of Theorem E, including a
shifted root with a non-unit scalar, and seven violate it, among them
inputs that break each of the three conditions. In every case the closed
criterion, the box computation and the total-degree kernel agree. Six
out-of-scope inputs are checked to return no space claims.

**Schema 2.** The third command checks 27 reports derived from schema 1,
namely the eleven homogeneous strata, their constant shifts, four
inhomogeneous inputs and the zero polynomial, for verbatim agreement with
a schema-1 report that itself passes the maintained checker. It checks 23
reports of the quadratic-complement family against kernels of total
degree at most six at every classified stage, with nesting, invariance of
the core, the sharpness witness and the first integral, confirms that
schema 1 still reports each of them as unsupported, checks four
unsupported inputs for the absence of space claims, and confirms that
four corrupted reports are rejected.

**Proof steps.** The fourth command checks with SymPy, independently of
the star engine, every displayed coefficient identity: Lemma 1 and the
vanishing of \(T_7\) with arbitrary functions of \(q\) as coefficients;
(6) through (9) for \(d=2,\dots,7\); the first integral and the two extras
of Theorem B(a) with symbolic \(f\) and \(b\); (13), (14), and the laws
(15), (16) with symbolic exponents \(n\) and \(d\); the second coefficient
used in the case \(k=1\), \(\deg b=4\); the three coefficients of
\(D_H(up+v)\), the divisibility step and the converse of Theorem E; and
the witness identity of the Proposition.

**What is proved and what is evidence.** Theorems A, B, C, E and the
Proposition are proved by hand for all degrees, Theorem E using Theorem D;
their computations are bounded evidence and the proofs do not depend on
them. Theorem D is computer-assisted: Lemmas 4 and 5 are proved by hand,
and the finite computations inside the boxes are then complete, not
bounded evidence. The comparison of the classifier with total-degree
kernels is independent bounded evidence. In the parametric step the gcd
is taken over all maximal minors when there are at most 3000 and over a
fixed pseudorandom sample of 3000 otherwise; this can only enlarge the
reported exceptional set, so the conclusion for \(t^2\ne4\) is rigorous
given SymPy's exact polynomial arithmetic.

**Remaining gaps.** Degree three or more in the complementary coordinate
is not treated; Lemmas 4 and 5 suggest the same weighted method, but
nothing is claimed. For a nonconstant top coefficient \(S^0\) is not
classified, and \(S^1\) is given by a certified computation and a
dimension bound, not by a closed formula in the coefficients, except on
the locus of Theorem E. Nothing here is formalized: no Lean toolchain
with Mathlib was reachable from the build environment, and the symbolic
audit is a substitute of lower strength. The natural first targets are
Theorem B(a) and the identities (3) through (9). There has been no
external review. The strata snapshot file `SHA256SUMS` does not cover the
classifier files and is unchanged, as in earlier classifier revisions.
