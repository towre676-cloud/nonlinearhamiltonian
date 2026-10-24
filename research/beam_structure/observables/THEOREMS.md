# Common adapted observables: precise closure and failure boundaries

These are classical polynomial-algebra statements over the rationals, extended
to real parameters where the displayed divisions are valid. They neither settle
the repository's remaining pure-top conjecture nor claim a new general theory
of finite observable lifting. Invariant-space lifting and observer closure are
established machinery; this contribution makes a specific controlled family,
its minimal summary and its obstructions independently checkable.

Let \(Q=q\), \(P=p+cq^2\) for one fixed shear \(c\). The transformation is
canonical. Use the **physical** generator
\(L_HF=H_PF_Q-H_QF_P\), which is minus the repository convention
\(D=\{H,\cdot\}\). Set

\[
H=P^3/3+\lambda Q+\mu QP,\qquad
A=P^2\partial_Q,\quad B=-\partial_P,\quad
C=Q\partial_Q-P\partial_P.
\]

The physical outputs are \(1,q,p,q^2,qp,p^2\). In adapted coordinates these
are \(1,Q,P-cQ^2,Q^2,QP-cQ^3,P^2-2cQ^2P+c^2Q^4\).

## 1. Minimal common closure is exactly 25 or 9 dimensional

Write
\(V_w=\operatorname{span}\{Q^aP^b:2a+b\leq w\}\).
Each of \(A,B,C\) preserves \(V_w\): \(A\) preserves weighted degree,
\(B\) lowers it, and \(C\) acts diagonally. Thus \(V_8\), which has
\(9+7+5+3+1=25\) monomials, contains every output and is common invariant.

For \(c\ne0\), this dimension is necessary. The three components of
\(p^2\) are \(C\)-eigenvectors with eigenvalues \(-2,1,4\), so

\[
\frac{C^2+C-2}{18c^2}\,p^2=Q^4.
\]

Every invariant space containing the physical outputs therefore contains
\(Q^4\). Next,

\[
A^kQ^4=\frac{4!}{(4-k)!}Q^{4-k}P^{2k},\qquad 0\leq k\leq4.
\]

Powers of \(B\) produce every monomial with the same \(Q\) exponent and
smaller \(P\) exponent. This is all of \(V_8\). Hence \(V_8\) is the
smallest common polynomial space for these outputs and independently allowed
generators. This is a minimality statement for the declared controls, not every
individual fixed \(\lambda,\mu\).

At \(c=0\), the same argument starting from \(q^2=Q^2\) yields exactly
\(V_4\), of dimension \(5+3+1=9\). The nonzero-shear and zero-shear
branches must not be conflated.

The matrices certify the same common space for distance-dependent coefficients
\(\lambda(s),\mu(s)\), with this fixed shear. To interpret them as expectation
evolution, assume the classical flow exists on the interval, the needed moments
exist, and differentiation under the expectation is valid. Self-consistent
distribution-dependent force coefficients need an additional closure argument.

## 2. Adding a quadrupole control forces infinite common closure

The additional Hamiltonian \(Q^2\) has generator \(E=-2Q\partial_P\).
An invariant vector space under \(A,E\) is also invariant under their
commutator. Direct calculation gives

\[
[A,E]=4QP\partial_Q-2P^2\partial_P,\qquad
[A,E]^rP=(-2)^r r!P^{r+1}.
\]

The physical outputs already span \(P=p+cq^2\). Every coefficient in this
sequence is nonzero and its degrees are distinct. Consequently **no finite
common polynomial space** containing the physical outputs is invariant under
the enlarged generator set. This is stronger than finding one failed action
in a guessed finite basis; it does not rule out nonpolynomial representations,
approximate summaries, or sufficient summaries for one finite map word.

## 3. A physical kinetic control also has a sharp shear boundary

Adding the physical Hamiltonian \(p^2=(P-cQ^2)^2\) gives

\[
J=2(P-cQ^2)\partial_Q+4cQ(P-cQ^2)\partial_P.
\]

Its components have \(\operatorname{ad}_C\)-eigenvalues \(-2,1,4\). Thus

\[
\frac{(\operatorname{ad}_C+2)(\operatorname{ad}_C-1)}{18}J
=-4c^2Q^3\partial_P.
\]

If \(c\ne0\), any common invariant space must be invariant under
\(E_4=Q^3\partial_P\) and \(T=A^3E_4\). But

\[
T(P^n)=6nP^{n+5},\qquad
T^rP=6^r\!\prod_{j=0}^{r-1}(1+5j)P^{1+5r}.
\]

Again the nonzero degrees grow without bound. For \(c=0\), the extra generator
is only \(2P\partial_Q\), which preserves \(V_4\). The obstruction therefore
requires nonzero shear. The tests evaluate generic sparse-polynomial
commutators, not only the displayed coefficient recurrence.

## 4. Positive particle clouds expose the missing physical information

At points \((Q,P)=(i,j)\), \(i=0,1\), \(j=0,\ldots,7\), use signed weights

\[
w_{ij}=(-1)^{8-i-j}\binom7j.
\]

The positive and negative parts each have total mass 128. Dividing each part by
128 gives two probability laws, realizable as 128 equally weighted particles
each. Their difference is the normalized finite-difference functional
\(\Delta_Q\Delta_P^7/128\). It annihilates every monomial in \(V_8\):
terms with no \(Q\) factor vanish under \(\Delta_Q\), while terms with a
\(Q\) factor have \(P\)-degree at most six.

Apply a \(Q^2\) kick of duration \(s\), followed by cubic transport of duration
\(t\):

\[
P_1=P-2sQ,\quad Q_2=Q+tP_1^2,\quad
p_2=P_1-cQ_2^2.
\]

The only part of \(p_2^2\) that survives the difference functional is the
\(c^2t^4P_1^8\) term, so

\[
\mathbb E_+[p_2^2]-\mathbb E_-[p_2^2]=-630s c^2t^4.
\]

For \(c=1,s=1/7,t=1/3\), this is \(-10/9\). The future means, position
variance and position-momentum covariance remain equal. The common position
variance is \(270763/28812\), and the projected squared-emittance difference
is exactly \(-1353815/129654\). Therefore the added control can hide a future
physical second-moment/emittance difference from the entire original 25-moment
summary. These are finite positive laws in arbitrary canonical units, not smooth
Vlasov densities, measured beams, or a finite phase-density-cap construction.

## 5. A common quadratic backbone and a conditional residual bound

For \(a\ne0\), completing the square in
\(H=ap^2+bq^2+cq^2p+dq^4\) with
\(P=p+\alpha q^2\), \(\alpha=c/(2a)\), gives

\[
H=aP^2+bQ^2+\Delta Q^4,\qquad
\Delta=d-\frac{c^2}{4a}.
\]

The backbone is quadratic exactly on \(4ad=c^2\). For a family of controls,
one proposed shear is shared only if every cross coefficient satisfies
\(c_i=2a_i\alpha\), including \(c_i=0\) whenever \(a_i=0\). Failure of this
test rejects that shear route, not every possible adapted representation.

The residual physical generator is
\(L_\Delta F=-4\Delta Q^3\partial_PF\). On an independently valid rectangle
\(|Q|\leq R,|P|\leq S\), coefficient absolute values give an exact rational
local bound for each polynomial. In particular the residual force is bounded
by \(4|\Delta|R^3\). This is a local conditional estimate, not a demonstrated
trajectory enclosure; support validation, numerical errors and amplification
remain separate obligations.

## Executable evidence and limits

The compiler discovers reachable spans by exact rational row reduction and
emits generator-action matrices and output reconstructions. Its checker checks
the polynomial identities without rerunning discovery. Ten tests cover zero
and nonzero shears, canonical reconstruction, minimality recipes, all-degree
obstruction recurrences, the positive-cloud witness, parameter routes and
corrupt-certificate rejection.

A separate finite-word pullback stays exact when a global common closure fails.
The saved demonstration needs 25 initial monomials within the original family
and 81 after adding an extra quadrupole in the declared longer word. The latter
is a sufficient monomial set, not a minimality claim or an infinite-time model.

All statements here are classical. Invariance does not mean membership in the
quantum-exact Moyal core, and no quantum/classical agreement is inferred. No
real-beam accuracy, space-charge closure or tenfold runtime gain is established.
