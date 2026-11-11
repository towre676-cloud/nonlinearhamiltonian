# Inhomogeneous sextic refinement from the leading form

## Scope and principal result

Let \(K\) be a field of characteristic zero, and let \(H\in K[q,p]\)
have ordinary total degree six. Write

\[
H=h+R,\qquad h=H_6\ne0,\qquad \deg R\le5,
\]

where \(H_6\) is the highest homogeneous part. This note extends the
[homogeneous root-multiplicity classification](SEXTIC_STRATA_THEOREM.md)
to every such Hamiltonian whose leading form has a finite-dimensional
first-refinement space. These are eight of the eleven geometric root
strata. Every coefficient of the lower-degree polynomial \(R\) is allowed.

For the six leading strata whose homogeneous first refinement is already
\(\operatorname{span}_K\{1,h\}\), the answer is

\[
S^1(H)=D_\infty(H)=\operatorname{span}_K\{1,H\}.
\tag{1}
\]

In particular, (1) holds whenever the leading sextic is squarefree. For
leading types \((4,2)\) and \((4,1,1)\), a two-unknown linear system
determines the entire first refinement, in all polynomial degrees. At most
one further refinement is needed. The second-refinement test distinguishes
a surviving three-dimensional core from a two-dimensional core for type
\((4,2)\). For type \((4,1,1)\), the core is always
\(\operatorname{span}_K\{1,H\}\), and an extra first-refinement observable,
when present, has an explicit nonzero obstruction at the second refinement.

The proof uses the ordinary total-degree filtration and the maintained
all-degree homogeneous theorem. It does not impose a numerical degree
cutoff on an observable. The results are mathematical theorems with the
inherited computer-assisted dependencies stated in Section 9; they are not
claimed as Lean formalizations. Historical priority and external peer
review remain open.

## 1. Operators, refinement, and coordinates

Use the unnormalized alternating contraction

\[
T_k(F,G)=\sum_{j=0}^k(-1)^j\binom{k}{j}
\bigl(\partial_q^{k-j}\partial_p^jF\bigr)
\bigl(\partial_q^j\partial_p^{k-j}G\bigr),
\qquad D_HG=T_1(H,G)=H_qG_p-H_pG_q.
\tag{2}
\]

For an integer \(r\ge0\), put

\[
S^r(H)=\{G\in K[q,p]:
T_k(H,D_H^iG)=0\text{ for }k\in\{3,5\},\ 0\le i\le r\},
\qquad
D_\infty(H)=\bigcap_{r\ge0}S^r(H).
\tag{3}
\]

Thus \(S^0\) imposes the two static gates, while \(S^1\) also imposes
them after one classical derivative. The convention is the fixed flat
Weyl--Moyal product with \(\hbar\)-independent polynomial observables.
Because \(\deg H=6\), all higher odd gates vanish identically. The formal
Moyal-bracket correction is

\[
-\frac{\hbar^2}{24}T_3(H,G)
+\frac{\hbar^4}{1920}T_5(H,G).
\tag{4}
\]

The two powers of \(\hbar\) are independent, so both gates must vanish.

For odd \(k\), interchanging the arguments in (2) gives
\(T_k(F,G)=-T_k(G,F)\). Consequently

\[
C_H:=\operatorname{span}_K\{1,H\}\subseteq D_\infty(H),
\qquad D_H1=D_HH=0.
\tag{5}
\]

All scalar and coordinate normalizations used below preserve the kernel
conditions. More precisely, let \(\phi(z)=Az+b\), with
\(A\in\mathrm{GL}_2(K)\), and let \(a\in K^\times\), \(c\in K\).
The chain rule gives

\[
T_k(F\circ\phi,G\circ\phi)
=\det(A)^k\,T_k(F,G)\circ\phi.
\]

Induction on \(i\) therefore yields

\[
T_k\bigl(aH\circ\phi+c,
D_{aH\circ\phi+c}^{\,i}(G\circ\phi)\bigr)
=a^{i+1}\det(A)^{k+i}\,
T_k(H,D_H^iG)\circ\phi.
\tag{6}
\]

Every factor is nonzero. In particular, nonunit determinants and nonunit
Hamiltonian scalings are retained explicitly; there is no restriction to
symplectic coordinate changes for these zero conditions. Addition of a
constant to \(H\) changes none of the refinement spaces. Coordinate
substitutions in this note are affine linear and use the original flat
product.

## 2. The leading-component identity

Let \(V_n\) denote the homogeneous polynomials of degree \(n\), and let
\(F_n=\bigoplus_{0\le j\le n}V_j\). Put \(F_n=V_n=0\) for \(n<0\),
and write \(\pi_n\) for homogeneous-component extraction, also zero for
negative \(n\). For \(G\in F_n\), set \(g=\pi_nG\). This notation
allows \(g=0\).

**Lemma 1 (principal component of every gate and iterate).** For every
\(i\ge0\),

\[
D_H^iG\in F_{n+4i},\qquad
\pi_{n+4i}(D_H^iG)=D_h^ig.
\tag{7}
\]

For \(k\in\{3,5\}\),

\[
T_k(H,D_H^iG)\in F_{n+4i+6-2k},\qquad
\pi_{n+4i+6-2k}\bigl(T_k(H,D_H^iG)\bigr)
=T_k(h,D_h^ig).
\tag{8}
\]

**Proof.** Differentiation lowers total degree by its order, and
multiplication adds degrees. Hence \(D_HF_m\subseteq F_{m+4}\).
The component of degree \(m+4\) in \(D_HX\), for \(X\in F_m\), can
use only the degree-six component of \(H\) and the degree-\(m\)
component of \(X\). Every occurrence of a lower component lowers the
bound by at least one. This proves (7) by induction. The same argument
for the \(k\) derivatives on each argument of (2) proves (8).

The formulas identify a specified homogeneous component, without asserting
that it is nonzero or that the degree bounds are attained. In particular,
if a leading Poisson bracket cancels, its component on both sides of (7)
is zero; the induction and (8) still hold. Negative output degrees mean
that both sides vanish. \(\square\)

The four first-refinement output degrees for an input component of degree
\(n\) are consequently:

| Gate | Degree whose component is identified |
| --- | ---: |
| \(T_3(H,G)\) | \(n\) |
| \(T_5(H,G)\) | \(n-4\) |
| \(T_3(H,D_HG)\) | \(n+4\) |
| \(T_5(H,D_HG)\) | \(n\) |

Cancellation between terms of an inhomogeneous observable is fully
permitted. Equation (8) isolates the top component of each individual
gate, which lower-degree terms cannot cancel.

**Corollary 2 (filtered inclusion).** For every finite \(r\ge0\) and
every \(n\ge0\), leading-component extraction induces an injective map

\[
\frac{S^r(H)\cap F_n}{S^r(H)\cap F_{n-1}}
\lhook\joinrel\longrightarrow S^r(h)\cap V_n.
\tag{9}
\]

The same assertion holds with \(D_\infty\) in place of \(S^r\).

**Proof.** If every required gate of \(G\) vanishes, (8) makes the
corresponding gate of \(\pi_nG\) vanish. The kernel of this leading-part
map is exactly the preceding filtration step. For \(D_\infty\), apply
the same identity separately to every integer \(i\); no finite stopping
assumption or exchange of limits is needed. \(\square\)

In particular, a finite-dimensional homogeneous refinement supplies an
all-degree upper bound for the inhomogeneous refinement. Equality in (9)
is not automatic: lower terms can obstruct the lifting of a homogeneous
survivor.

## 3. Transfer of a two-dimensional space

**Theorem 3 (finite-refinement and core transfer).** Suppose
\(S^r(h)=\operatorname{span}_K\{1,h\}\) for some finite \(r\ge0\).
Then

\[
S^r(H)=S^{r+1}(H)=\cdots=D_\infty(H)=C_H.
\tag{10}
\]

If only \(D_\infty(h)=\operatorname{span}_K\{1,h\}\) is known, then
\(D_\infty(H)=C_H\).

**Proof.** Consider a nonzero member \(G\) of the space on the left.
By Corollary 2, its highest homogeneous part belongs to the corresponding
space for \(h\). That space has nonzero homogeneous pieces only in
degrees zero and six. If \(G\) is nonconstant, it therefore has degree
six and highest part \(\lambda h\). By (5),
\(G-\lambda H\) remains in the same space and has degree at most five.
Its highest part must then have degree zero, so it is constant. This proves
the upper inclusion in (10), or the asserted core equality. Equation (5)
proves the converse. The intervening refinements are trapped between the
same two-dimensional space. \(\square\)

Let

\[
\mathcal F=
\{(3,2,1),(3,1,1,1),(2,2,2),(2,2,1,1),
(2,1,1,1,1),(1,1,1,1,1,1)\}.
\tag{11}
\]

**Corollary 4 (all lower-degree perturbations in six leading strata).**
If the geometric root multiplicities of \(h\) lie in \(\mathcal F\),
then (1) holds for every \(R\) of degree at most five.

**Proof.** The maintained homogeneous theorem gives
\(S^1(h)=\operatorname{span}_K\{1,h\}\). Apply Theorem 3.
\(\square\)

For example, \(q^6+p^6\) is squarefree over every characteristic-zero
field. Thus every polynomial

\[
H=q^6+p^6+\sum_{a+b\le5}r_{ab}q^ap^b
\]

has exactly \(C_H\) as its first refinement and dynamic core, with no
restrictions on the coefficients \(r_{ab}\in K\).

## 4. Fourfold leading roots and the complete lift system

Suppose the leading type is \((4,2)\) or \((4,1,1)\). Its unique
fourfold projective root is defined over \(K\). One direct justification
is squarefree factorization over \(K\): an irreducible factor of
multiplicity four can have degree only one in a degree-six form.

Choose independent linear forms \(u,w\in K[q,p]_1\), with \(u=0\)
that root. Then

\[
h=u^4(Aw^2+Buw+Cu^2),\qquad A\ne0.
\]

Set

\[
v=w+\frac{B}{2A}u,\qquad
c=A,\qquad
\delta=\frac CA-\frac{B^2}{4A^2},\qquad
\kappa=T_1(u,v)\ne0.
\]

This gives the rational normal form

\[
h=c\,u^4(v^2+\delta u^2),\qquad J_2=uv.
\tag{12}
\]

Type \((4,2)\) means \(\delta=0\); type \((4,1,1)\) means
\(\delta\ne0\). The two simple roots in the latter case need not be
defined over \(K\). Equation (6) and the homogeneous theorem give

\[
S^1(h)=\operatorname{span}_K\{1,h,J_2\}.
\tag{13}
\]

Define the linear map with full polynomial outputs

\[
\mathcal L_H(X)=
\bigl(T_3(H,D_HX),T_5(H,D_HX)\bigr).
\tag{14}
\]

**Theorem 5 (complete affine correction).** Solve the equation

\[
\alpha\mathcal L_H(q)+\beta\mathcal L_H(p)
=-\mathcal L_H(J_2),\qquad \alpha,\beta\in K.
\tag{15}
\]

There is either no solution or exactly one solution. If there is no
solution, \(S^1(H)=C_H\). If there is a solution, put

\[
J=J_2+\alpha q+\beta p.
\tag{16}
\]

Then

\[
S^1(H)=\operatorname{span}_K\{1,H,J\}.
\tag{17}
\]

**Proof.** For a polynomial of degree at most two, both static gates
vanish because all its derivatives of order three and five vanish. Thus
(15) is precisely the remaining condition for (16) to lie in \(S^1(H)\).

Conversely, let \(G\in S^1(H)\). Corollary 2 and (13) constrain its
highest degree to zero, two, or six. At degree six subtract its uniquely
determined multiple of \(H\). A nonconstant remainder must have degree
two with highest part a nonzero multiple of \(J_2\). Divide by that
multiple and subtract its constant term to obtain (16). This proves
existence of a solution whenever \(S^1(H)\ne C_H\), and exhausts every
observable degree.

Two solutions of (15) would differ by a nonzero linear polynomial in
\(S^1(H)\). Its highest component would belong to
\(S^1(h)\cap V_1=0\), a contradiction. Once one lift exists, the same
argument expresses every \(G\) as a linear combination in (17).
\(\square\)

Equation (15) is a finite exact linear system in two unknowns, even though
Theorem 5 describes the entire polynomial space. Coefficients of every
monomial in both output polynomials are retained. For the quadratic input,
the two output degrees are at most six and two, respectively; outputs
must not be projected back into the input space.

The two columns of the system are always independent. In the coordinates
of (12), literal differentiation gives

\[
T_3(h,D_hu)=-576c^2\kappa^4u^5,\qquad
T_3(h,D_hv)=-576c^2\kappa^4u^4v,
\tag{18}
\]

and both corresponding \(T_5\) expressions are zero. These are the
degree-five components of the full \(H\) expressions. They also give
a direct constructive proof of uniqueness. Over \(\mathbb Q\), exact
linear algebra therefore returns either one rational correction or an
inconsistency; no extension field is needed.

The choice of normalization of \(J_2\) changes the representative of
the one-dimensional quotient, but not the spaces in (17). Solving (15)
in the original rational coordinates automatically retains the affine
terms induced by a translated coordinate system.

## 5. The second refinement is sufficient

The elementary identity

\[
S^{r+1}(H)=S^r(H)\cap D_H^{-1}S^r(H)
\tag{19}
\]

holds for every \(r\ge0\): the extra condition is exactly the gate
at iterate \(r+1\). If two successive spaces coincide, that space is
\(D_H\)-invariant and equals \(D_\infty(H)\). In particular, if
\(S^r(H)\) is finite-dimensional of dimension \(m\), its descending
refinement sequence reaches the core by step \(r+m-2\): it contains
the fixed two-dimensional subspace (5), and every nonstationary step
strictly lowers dimension. Once dimension two is reached, the space is
\(C_H\) and is stationary.

For (17), compute the full obstruction pair

\[
W_H(J)=\bigl(T_3(H,D_H^2J),T_5(H,D_H^2J)\bigr).
\tag{20}
\]

**Theorem 6 (exact core in both fourfold strata).** If (15) has no
solution, then \(D_\infty(H)=S^1(H)=C_H\). Otherwise:

1. If \(W_H(J)=0\), then
   \(D_\infty(H)=S^1(H)=\operatorname{span}_K\{1,H,J\}\).
2. If \(W_H(J)\ne0\), then
   \(D_\infty(H)=S^2(H)=C_H\), and \(J\in S^1(H)\setminus S^2(H)\).

**Proof.** The first assertion follows from (5). In the lifted case,
\(W_H(J)=0\) is equivalent to \(D_HJ\in S^1(H)\), since the static
gates on \(D_HJ\) already vanish. Together with \(D_H1=D_HH=0\),
this makes the basis in (17) invariant under \(D_H\), proving the first
case. In the second case, the iterate-two output for
\(a+bH+eJ\) is \(eW_H(J)\). Because \(K\) is a field and
\(W_H(J)\ne0\), it vanishes exactly when \(e=0\). Equation (5)
then proves the asserted core equality. \(\square\)

This gives a sufficient depth of two for every lower-degree perturbation
of both fourfold leading strata. The first case can occur for \((4,2)\).
The following obstruction rules it out for \((4,1,1)\).

**Theorem 7 (nonzero principal obstruction for type \((4,1,1)\)).**
Assume \(\delta\ne0\) in (12), and suppose the lift (16) exists. Then

\[
\pi_{10}\bigl(T_3(H,D_H^2J)\bigr)
=-82944c^3\kappa^5\delta\,u^{10}\ne0.
\tag{21}
\]

Consequently \(D_\infty(H)=C_H\) for every lower-degree perturbation
of a \((4,1,1)\) leading form. When the lift exists, refinement depth
two is necessary and sufficient; when it does not, depth one suffices.

**Proof.** In coordinates \((x,y)\), put
\(F=x^4(y^2+\delta x^2)\) and \(J_0=xy\). Direct use of (2) gives

\[
D_FJ_0=2F+4\delta x^6,\qquad
D_F^2J_0=-48\delta x^9y,\qquad
T_3(F,D_F^2J_0)=-82944\delta x^{10}.
\tag{22}
\]

Apply (6) with Hamiltonian scale \(c\), linear coordinate forms
\((u,v)\), gate order three, and iterate two. This gives
\(-82944c^3\kappa^5\delta u^{10}\) for the homogeneous calculation.
Equation (8), with \(n=2\), identifies it with the degree-ten component
in (21). Both the lower part of \(H\) and the affine correction to
\(J\) contribute only to smaller degrees. Every factor in (21) is
nonzero, and \(K[q,p]\) is an integral domain. Theorem 6 completes the
proof. \(\square\)

For \((4,2)\), \(\delta=0\), so (21) provides no obstruction. The
full test (20) remains necessary; it must not be replaced by the leading
coefficient alone.

## 6. Exact examples of persistence and loss

The following examples use the same signs and normalization as (2).

### An exceptional survivor for every quadratic perturbation in a family

For \(c\ne0\), \(\delta\ne0\), and arbitrary \(t\in K\), let

\[
H=c(q^4p^2+\delta q^6)+tq^2,\qquad J=qp.
\]

The first-refinement gates vanish and

\[
T_3(H,D_H^2J)=-82944c^3\delta q^{10},\qquad
T_5(H,D_H^2J)=0.
\]

Thus \(S^1(H)=\operatorname{span}\{1,H,qp\}\) and
\(S^2(H)=D_\infty(H)=C_H\), uniformly in \(t\).

### A three-dimensional core that persists

For \(H=q^4p^2+tq^2\), the same \(J=qp\) satisfies
\(D_HJ=2H\). Its static gates vanish, so

\[
S^1(H)=D_\infty(H)=\operatorname{span}\{1,H,qp\}
\]

for every \(t\). This illustrates the zero-obstruction branch of
Theorem 6 for leading type \((4,2)\).

### A lower-degree term that removes the survivor at the second refinement

For \(H=q^4p^2+tq^3\), the polynomial \(J=qp\) still passes the
first refinement, but

\[
T_3(H,D_H^2J)=-4320tq^7,\qquad T_5(H,D_H^2J)=0.
\]

For \(t\ne0\), the core is \(C_H\) and depth two is necessary.
The obstruction has degree seven, illustrating why the full output in
(20) is required when the degree-ten component vanishes.

### A lower-degree term that prevents any first-refinement lift

Let \(H=q^4p^2+\delta q^6+p^3\), with arbitrary \(\delta\in K\).
For the only possible corrected generator
\(J=qp+\alpha q+\beta p\), differentiation gives

\[
\begin{aligned}
T_3(H,D_HJ)={}&-576\alpha q^5-576\beta q^4p
-6480\delta q^3-2160\beta\delta q^2\\
&-720qp^2+288\alpha qp-144\beta p^2,\\
T_5(H,D_HJ)={}&0.
\end{aligned}
\]

The degree-five terms force \(\alpha=\beta=0\). The remaining
coefficient of \(qp^2\) is \(-720\), so no lift exists. Therefore
\(S^1(H)=D_\infty(H)=C_H\), both at \(\delta=0\) and at
\(\delta\ne0\). The leading root pattern alone does not decide
whether an inhomogeneous first-refinement exception survives.

## 7. Rational homogeneous classification, including nonsplit forms

The homogeneous theorem classifies geometric root multiplicities, not just
rationally split polynomials. For rational input, projective multiplicities
can be determined exactly by squarefree factorization of a dehomogenization
together with the missing degree at infinity. An irreducible factor of
degree \(e\) and multiplicity \(m\) contributes \(e\) geometric roots
of multiplicity \(m\). No floating root approximation is required.

The rational interpretations of the homogeneous rows with larger cores
are as follows. Nonzero scalar multiples of a Hamiltonian have the same
spaces by (6).

| Leading homogeneous type | Rational representation | \(S^1(h)=D_\infty(h)\) |
| --- | --- | --- |
| \((6)\) | \(h=cL^6\), with a rational linear complement \(M\) | \(K[L]+M K[L]+M^2K[L]\) |
| \((5,1)\) | \(h=cL^5M\), with independent rational \(L,M\) | \(K[L]+M K[L]\) |
| \((4,2)\) | \(h=cL^4M^2\) | \(\operatorname{span}\{1,LM,h\}\) |
| \((3,3)\) | \(h=cQ^3\), with squarefree rational quadratic \(Q\) | \(K[Q]\) |

Here “rational” means coefficients in \(K=\mathbb Q\); the same
formulas hold over a general characteristic-zero field whenever the
displayed factors are over that field. The unique root of \((6)\), and
the roots of distinct multiplicities in \((5,1)\) and \((4,2)\), are
defined over \(K\); for \((6)\), any independent complement suffices.

For the \((3,3)\) row, the two triple roots can be a nonsplit conjugate
pair. Squarefree factorization supplies a quadratic \(Q\in K[q,p]\)
with \(h=cQ^3\), and \(Q\) has two distinct geometric roots. Over an
algebraic closure, factor \(Q\) into independent linear forms and apply
the monomial theorem and (6), obtaining \(\overline K[Q]\). To descend,
write any member as \(\sum_j a_jQ^j\). The homogeneous degrees \(2j\)
are distinct. If this polynomial lies in \(K[q,p]\), comparison with
any nonzero coefficient of \(Q^j\) shows \(a_j\in K\), for every
\(j\). Therefore

\[
K[q,p]\cap\overline K[Q]=K[Q].
\tag{23}
\]

In particular, \((q^2+p^2)^3\) has homogeneous first refinement and
core \(K[q^2+p^2]\), despite having no rational projective roots over
\(\mathbb Q\).

The six rows in (11) descend as \(C_h\) directly. The remaining
\((4,1,1)\) row uses the rational construction (12): its first
refinement is \(\operatorname{span}\{1,h,uv\}\), its second
refinement and core are \(C_h\), and (21) at \(R=0\) supplies the
failure witness.

## 8. Classifier contract and sufficient depths

For \(H\) of exact total degree six, the extension has this complete
scope:

| Geometric type of \(H_6\) | Lower-degree terms covered | Complete decision |
| --- | --- | --- |
| Any of the six types in (11) | Arbitrary | \(S^1=D_\infty=C_H\) |
| \((4,1,1)\) | Arbitrary | Solve (15); an existing lift gives \(\dim S^1=3\) and nonzero witness (21); always \(S^2=D_\infty=C_H\) |
| \((4,2)\) | Arbitrary | Solve (15), then test (20); the core has dimension two or three; \(S^2=D_\infty\) |
| \((6),(5,1),(3,3)\) | Homogeneous input and addition of constants | Use the symbolic families in Section 7 |

For the last row, arbitrary nonconstant lower-degree perturbations remain
outside this extension. Corollary 2 still applies, but an
infinite-dimensional leading space supplies no finite completeness bound
by itself. A finite search in those cases cannot be reported as the full
polynomial core.

For the eight finite-leading strata, an exact classifier may therefore:

1. Extract \(H_6\) and determine its projective multiplicity pattern.
2. Apply (1) for the six types in (11).
3. In a fourfold type, construct \(J_2\) over the input field and solve
   the full coefficient system (15).
4. If a lift exists, evaluate the full pair (20) and return the basis
   prescribed by Theorem 6. For \((4,1,1)\), the nonzero principal term
   (21) is also an independent structural check of the result.

A nonzero component of (20), together with the vanishing gates at iterates
zero and one, certifies the first failing iterate of that observable and
proves that depth two is necessary for the entire refinement to reach the
core. A report of sufficient depth one does not assert that depth zero
fails: minimality in that case requires an additional static-space
argument. No minimality claim follows merely from the row of the table.

The proof is valid in arbitrary rational coordinates. The returned
polynomials and obstruction are evaluated in the input coordinates;
normalization is an exact method for finding their leading generator.
An implementation must retain the determinant and scaling factors when
it compares a transported obstruction with (21).

## 9. Dependencies and verification boundary

The new ingredients are the filtered identities (7)--(9), transfer by
subtracting \(H\), the exhaustive affine correction system, and the
finite invariant-space argument. Each is proved above using polynomial
differentiation and linear algebra. The formulas in (18), (22), and
Section 6 are direct differentiations under (2).

The homogeneous input is the maintained
[complete sextic theorem](SEXTIC_STRATA_THEOREM.md), with its existing
dependencies:

- Among the six rows in (11), the exact double-root rows use the
  homogeneous degeneration and monomial arguments. The triple-root and
  squarefree rows additionally use their exact finite certificates and
  the inherited all-degree static tail.
- The [squarefree theorem](SQUAREFREE_THEOREM.md) supplies the sixteen
  discriminant identities and the stated static-tail dependence. The
  transfer does not replace those dependencies.
- The \((4,2)\) and \((4,1,1)\) rows use the all-degree fourfold-root
  theorem, its degeneration bound, and its constant degree-two pivot.
- The homogeneous infinite families and the nonsplit interpretation use
  the [monomial proof](../c3_uniform/C3_THEOREM.md) and covariance.

All-degree completeness follows from these theorems and the filtered
proof, rather than from testing many observable degrees. Replaying exact
examples and independently reconstructing output gates checks the
implementation of the classifier within this theorem's scope. Such
replays do not formalize the homogeneous input or the arguments above in
a proof assistant. The separate Lean bridge retains its own declared
boundary.
