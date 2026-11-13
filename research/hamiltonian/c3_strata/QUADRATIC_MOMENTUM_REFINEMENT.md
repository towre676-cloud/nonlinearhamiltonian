# Exact first three refinements for separable quadratic-momentum sextics

Let \(K\) be a characteristic-zero field, \(c\in K^\times\), and \(h\in K[q]\) with \(\deg h=6\). Set \(H=h(q)+cp^2\), \(D_H=h'(q)\partial_p-2cp\partial_q\), and define \(S^r\) by requiring \(D_H^iG\in S^0=\ker T_3(H,-)\cap\ker T_5(H,-)\) for \(0\le i\le r\).

**Theorem.** For this entire family:

\[
\begin{aligned}
S^0&=\{f(q)+p g(q)+p^2k(q):f,g,k\in K[q]\},\\
S^1&=\{f(q)+p g(q)+\kappa p^2:f,g\in K[q],\ \kappa\in K\},\\
S^2&=\{f(q)+p(a+bq)+\kappa p^2:f\in K[q],\ a,b,\kappa\in K\},\\
S^3&=\{(\kappa/c)h(q)+u+vq+wq^2+p(a+bq)+\kappa p^2:
u,v,w,a,b,\kappa\in K\}.
\end{aligned}
\]

In particular \(\dim_K S^3=6\), despite \(\dim_K S^0=\infty\). These are complete, all-degree descriptions of the first four spaces, **not** a classification of the persistent core.

**Proof.** Because the only nonzero third-order derivatives of \(H\) are pure \(q\)-derivatives of \(h\), \(T_3(H,G)=h'''(q)\partial_p^3G\). Since \(h'''\ne0\), the static condition is precisely \(\deg_pG\le2\), which also annihilates \(T_5\).

For \(G=f+pg+p^2k\), the coefficient of \(p^3\) in \(DG\) is \(-2ck'\); hence \(G\in S^1\) exactly when \(k'=0\). After setting \(k=\kappa\), the coefficient of \(p^3\) in \(D^2G\) is \(4c^2g''\), giving \(S^2\). With \(g=a+bq\), the coefficient of \(p^3\) in \(D^3G\) is \(8c^2\kappa h'''-8c^3f'''\). Thus \(G\in S^3\) precisely when \(f'''=(\kappa/c)h'''\), which integrates three times in characteristic zero to the displayed quadratic remainder.

The calculations use no finite degree truncation, and all reverse implications hold because the static gates vanish exactly on polynomials of \(p\)-degree at most two.

**Open:** compute \(S^4,S^5,\ldots\), identify the persistent core, and formalize the full argument in Lean. Do not infer \(D_\infty=\operatorname{span}\{1,H\}\) from the above alone.
