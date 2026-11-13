# Complete refinement classification for separable quadratic-momentum sextics

Let \(K\) be a characteristic-zero field, \(c\in K^\times\), and \(h\in K[q]\) have degree six. Set \(H=h(q)+cp^2\) and \(D_H=h'(q)\partial_p-2cp\partial_q\). Define \(S^r\) by requiring \(D_H^iG\in S^0=\ker T_3(H,-)\cap\ker T_5(H,-)\) for \(0\le i\le r\).

**All-degree theorem.** For this entire family:

\[
\begin{aligned}
S^0&=\{f(q)+p g(q)+p^2k(q):f,g,k\in K[q]\},\\
S^1&=\{f(q)+p g(q)+\kappa p^2:f,g\in K[q],\ \kappa\in K\},\\
S^2&=\{f(q)+p(a+bq)+\kappa p^2:f\in K[q],\ a,b,\kappa\in K\},\\
S^3&=\{(\kappa/c)h(q)+u+vq+wq^2+p(a+bq)+\kappa p^2:u,v,w,a,b,\kappa\in K\},\\
S^4&=\{(\kappa/c)h(q)+u+vq+wq^2+\kappa p^2:u,v,w,\kappa\in K\},\\
S^5&=D_\infty(H)=\operatorname{span}_K\{1,H\}.
\end{aligned}
\]

Thus the dimensions of \(S^0,S^1,S^2\) are infinite; \(\dim S^3=6\), \(\dim S^4=4\), and \(\dim S^5=2\). All later refinements equal \(S^5\).

**Proof.** Since \(T_3(H,G)=h'''(q)\partial_p^3G\) and \(h'''\ne0\), the static condition is exactly \(\deg_pG\le2\), which also annihilates \(T_5\).

For \(G=f+pg+p^2k\), the coefficient of \(p^3\) in \(DG\) is \(-2ck'\), so \(S^1\) requires \(k=\kappa\). The coefficient of \(p^3\) in \(D^2G\) is then \(4c^2g''\), giving \(g=a+bq\) at \(S^2\). With \(g=a+bq\), the coefficient of \(p^3\) in \(D^3G\) is \(8c^2\kappa h'''-8c^3f'''\), giving \(f=(\kappa/c)h+u+vq+wq^2\).

For such \(G\in S^3\), direct differentiation gives

\[
[p^3]D_H^4G=-8c^3\big((a+bq)h^{(4)}+5b h^{(3)}\big).
\]

The leading coefficient of \(q^3\) is nonzero unless \(b=0\), because \(h^{(3)}\) has degree three and \(h^{(4)}\) degree two. Then \(a=0\), proving the \(S^4\) description.

For \(G\in S^4\), the remaining condition is

\[
[p^3]D_H^5G=16c^4\big((v+2wq)h^{(4)}+10w h^{(3)}\big).
\]

Its leading coefficient of \(q^3\) forces \(w=0\), then \(v=0\). Thus \(S^5=\{u+(\kappa/c)H\}\). Both \(1\) and \(H\) are fixed by the Hamiltonian derivation and annihilated by the odd gates, so every later refinement equals this space.

The proof is polynomial-algebraic in all degrees; no finite truncation is used. The coefficient identities have symbolic regression tests. This is not yet Lean-formalized, and it does not classify momentum-quadratic terms with nonconstant coefficient \(B(q)\).
