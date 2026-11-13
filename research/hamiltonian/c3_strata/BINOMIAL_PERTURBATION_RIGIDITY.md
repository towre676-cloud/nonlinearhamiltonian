# Perturbation rigidity for the two binomial Newton strata

**Proposed Theorem 10 (characteristic zero; all polynomial degrees).**

Let \(K\) be a characteristic-zero field. Consider either

1. \(H=q^6+zqp^4+R\), \(z\in K^\times\), with \(\mathrm{wt}(q,p)=(4,5)\) and \(\mathrm{wt}(R)<24\), or
2. \(H=q^6+bq^2p^3+R\), \(b\in K^\times\), with \(\mathrm{wt}(q,p)=(3,4)\) and \(\mathrm{wt}(R)<18\).

Assume the finite-tail and exact first-refinement classifications of the corresponding weighted leading forms from the merged binomial-strata result (Theorems 8–9): \(S^1(H_0)=K\cdot1+K\cdot H_0\).

Then **for every** lower-weight perturbation \(R\), with no restriction on the number of its coefficients,

\[
S^1(H)=S^2(H)=D_\infty(H)=K\cdot1+K\cdot H.
\]

Furthermore \(\dim_K S^0(H)\le10\), with all static partners of weighted degree at most 87 and 53, respectively.

## Proof

Write \(F_d\) for the polynomials of weighted degree at most \(d\). Let \(N=\mathrm{wt}(H_0)\) and \(\sigma(G)\) denote the highest nonzero weighted homogeneous part of \(G\). The transvectant \(T_k(H,-)\) maps \(F_d\) into \(F_{d+N-k(w_q+w_p)}\), with associated-graded map \(T_k(H_0,-)\). The Hamiltonian derivation \(D_H=T_1(H,-)\) is likewise filtered, with associated-graded map \(D_{H_0}\).

For any \(G\in S^1(H)\), the two static equations \(T_3(H,G)=T_5(H,G)=0\) imply that \(\sigma(G)\in S^0(H_0)\). Applying both static gates to \(D_HG\) and taking top homogeneous components (including the possibility that the nominal top component vanishes) gives \(T_k(H_0,D_{H_0}\sigma(G))=0\), for \(k=3,5\). Therefore \(\sigma(G)\in S^1(H_0)\).

By the leading-form classification, \(S^1(H_0)=K\cdot1+K\cdot H_0\), supported only in weights \(0,N\). Thus the highest weight of a nonzero \(G\in S^1(H)\) must be either 0 or \(N\). If it is 0, \(G\) is constant. If it is \(N\), there is a \(c\in K\) such that \(\sigma(G)=cH_0\). Since \(H\in S^1(H)\) (all odd transvectants of \(H\) with itself vanish and \(D_HH=0\)), \(G-cH\in S^1(H)\) has weight strictly less than \(N\). Its leading weight, if nonzero, would have to be 0 or \(N\), so it must be constant. Hence \(G=cH+d\).

Conversely \(1,H\in S^r(H)\) for all \(r\ge0\), and \(S^{r+1}(H)\subseteq S^r(H)\). Therefore all later refinements and the persistent core equal their span.

The same associated-graded injection \(\mathrm{gr}\,S^0(H)\hookrightarrow S^0(H_0)\) gives the dimension and finite-weight bounds.

## Scope and audit requirements

The filtered argument is an all-degree mathematical proof **conditional on** the earlier finite-tail and refinement classifications of the two leading forms. It does not make those antecedent results Lean-formal, and it does not cover parameter boundaries \(z=0\) or \(b=0\), nor leading forms with multiple terms at the same Newton weight. The claimed dimensions and bounds therefore inherit the independent-review status of Theorems 8–9.

This theorem upgrades the two binomial leading-form classifications to arbitrary lower-weight perturbations, without asserting a complete classification of every sixfold-leading Hamiltonian.
