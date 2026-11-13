# Affine-momentum sextic boundary: infinite persistent core

**Theorem (characteristic zero, all degrees).** Let \(K\) be a characteristic-zero field, \(h\in K[q]\) have degree six, and \(a,b\in K\). For

\[
H(q,p)=h(q)+(a+bq)p,
\]

the static space and every Hamiltonian refinement coincide:

\[
S^r(H)=D_\infty(H)=K[q]\oplus pK[q]\oplus p^2K[q]\quad(r\ge0).
\]

**Proof.** The transvectants are \(T_3(H,G)=h'''(q)\partial_p^3G\) and \(T_5(H,G)=h'''''(q)\partial_p^5G\), since the \(p\)-dependent term has total degree at most two. Because \(h'''\ne0\) and \(K[q,p]\) is an integral domain, the first equation is equivalent to \(\partial_p^3G=0\), i.e. \(\deg_pG\le2\). The fifth gate then vanishes. Thus \(S^0(H)=K[q]\oplus pK[q]\oplus p^2K[q]\).

The Hamiltonian derivation is \(D_H=(h'(q)+bp)\partial_p-(a+bq)\partial_q\). It preserves the space of polynomials with \(p\)-degree at most two, since \(\partial_p\) lowers that degree, multiplication by \(p\) restores at most one, and the coefficient of \(\partial_q\) is independent of \(p\). Consequently \(D_H^r S^0(H)\subseteq S^0(H)\) for every \(r\), proving the claimed equality of every refinement and the persistent core.

This covers a mixed-coordinate boundary (\(b\ne0\)), extending the pure-coordinate theorem from PR #32. It does not classify general terms \(A(q)p\) of quadratic or higher degree in \(q\), nor higher powers of \(p\). The argument is a human mathematical proof, not yet Lean formalized.
