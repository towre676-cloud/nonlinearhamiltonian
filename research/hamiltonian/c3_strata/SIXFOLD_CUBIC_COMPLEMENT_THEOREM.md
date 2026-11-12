# All-degree sixfold cubic-complement classification

**Theorem (characteristic zero).** Let \(L,M\in\mathbb Q[q,p]_1\) be linearly independent, \(a,b\in\mathbb Q^\times\), and \(c\in\mathbb Q\). For

\[
H=aL^6+bM^3+c,\qquad D=\{H,-\},
\]

write \(S^r=\{G\in\mathbb Q[q,p]:T_3(H,D^jG)=T_5(H,D^jG)=0,\ 0\le j\le r\}\). Then

\[
S^0=\text{a 15-dimensional rational vector space},\qquad
S^1=\operatorname{span}_{\mathbb Q}\{1,L,L^2,H\},
\qquad S^2=D_\infty=\operatorname{span}_{\mathbb Q}\{1,H\}.
\]

This is an **all-polynomial-degree** theorem, not an extrapolation from a finite degree search. A constant shift does not affect the operators. A rational invertible linear coordinate change reduces to \(H=q^6+\lambda p^3\), with \(\lambda\ne0\), and nonzero scalar rescaling of the Hamiltonian does not change any kernel.

## Static gate: a global degree bound

For \(H=q^6+\lambda p^3\), the only nontrivial odd gates are

\[
T_5(H,G)=720q\,\partial_p^5G,\qquad
T_3(H,G)=120q^3\,\partial_p^3G-6\lambda\,\partial_q^3G.
\]

Thus \(G=\sum_{j=0}^4g_j(q)p^j\). The second gate gives

\[
g_2'''=g_3'''=g_4'''=0,\quad
g_0'''=\frac{120}{\lambda}q^3g_3,\quad
g_1'''=\frac{480}{\lambda}q^3g_4.
\]

Consequently every static partner is a unique linear combination of the following fifteen polynomials:

\[
\begin{aligned}
&1,q,q^2,\quad p,qp,q^2p,\quad p^2,qp^2,q^2p^2,\\
& p^3+q^6/\lambda,\quad qp^3+\frac{4}{7\lambda}q^7,\quad
q^2p^3+\frac{5}{14\lambda}q^8,\\
& p^4+\frac4\lambda q^6p,\quad
qp^4+\frac{16}{7\lambda}q^7p,\quad
q^2p^4+\frac{10}{7\lambda}q^8p.
\end{aligned}
\]

This establishes the global finite-dimensional reduction before any matrix calculation.

## First refinement: an exact nonzero minor

Form the coefficient matrix of \((T_3(H,DG),T_5(H,DG))\) on these fifteen columns. Columns \(1,q,q^2,p^3+q^6/\lambda\) vanish. On the remaining eleven columns, the eleven rows of the \(T_3\) gate with output monomials

\[
q^2,\ q^2p,\ q^2p^3,\ q^3,\ q^3p,\ q^3p^2,\ q^3p^3,\
q^4,\ q^4p,\ q^4p^2,\ q^4p^3
\]

have determinant

\[
\boxed{2^{54}3^{38}5^{12}\cdot11\cdot17^2\,\lambda^{11}}\ne0.
\]

Therefore the first-refinement kernel has exactly dimension four. Since the four displayed surviving columns satisfy the gates identically, \(S^1=\langle1,q,q^2,H\rangle\).

## Second refinement: exact obstruction

On the ordered first-refinement basis \((1,q,q^2,p^3+q^6/\lambda)\), the nonzero rows of the second-iterate \(T_3\) matrix are

\[
\begin{array}{c|rrrr}
\text{output monomial}&1&q&q^2&p^3+q^6/\lambda\\
pq^2&0&12960\lambda^2&0&0\\
pq^3&0&0&103680\lambda^2&0
\end{array}
\]

and all \(T_5\) rows vanish. Thus \(S^2=\langle1,H\rangle\). Since \(D(1)=D(H)=0\), this is invariant and equals \(D_\infty\).

## Proof boundary

The proof uses exact polynomial identities, characteristic-zero differentiation, an explicit rational nonzero minor, and symplectic covariance. It is not yet a Lean formalization. The independent Python verifier reproduces the static basis, determinant, and second-iterate obstruction, rather than relying on bounded polynomial sampling.
