# Arbitrary polynomial momentum-affine Hamiltonians have infinite persistent cores

**Theorem (characteristic zero).** Let \(h,A\in K[q]\) be arbitrary polynomials and \(H=h(q)+A(q)p\). With \(S^0(H)=\ker T_3(H,-)\cap\ker T_5(H,-)\) and successive refinements defined by requiring repeated Hamiltonian derivatives to remain in \(S^0\), we have

\[
K[q]\oplus pK[q]\subseteq S^r(H)\quad\text{for every }r\ge0,
\qquad K[q]\oplus pK[q]\subseteq D_\infty(H).
\]

Thus \(D_\infty(H)\) is infinite-dimensional, without any restriction on \(\deg A\).

**Proof.** Let \(V=K[q]\oplus pK[q]\). Every \(G=f(q)+pg(q)\in V\) has total \(p\)-degree at most one. Since \(H\) also has \(p\)-degree at most one, every summand in \(T_k(H,G)\) for \(k\ge3\) contains at least two \(p\)-derivatives of either \(H\) or \(G\), and therefore vanishes. In particular \(V\subseteq S^0(H)\).

The Hamiltonian derivation satisfies

\[
D_HG=T_1(H,G)
=h'(q)g(q)-A(q)f'(q)+p\bigl(A'(q)g(q)-A(q)g'(q)\bigr).
\]

Thus \(D_H(V)\subseteq V\). Induction gives \(D_H^r(V)\subseteq V\subseteq S^0(H)\) for every \(r\), proving the claim.

**Important scope.** This is an **inclusion**, not an equality assertion for arbitrary \(A\). The special case \(\deg A\le1\) has the stronger equality \(S^r(H)=K[q]\oplus pK[q]\oplus p^2K[q]\) from PR #33, assuming \(\deg h=6\). This theorem does not classify arbitrary momentum-quadratic Hamiltonians or the entire 21-parameter sixfold-leading family.
