# Conjecture C2 is PROVED: no partners of $H_{\pm 2} = (q^3 \pm p^3)^2$ in any degree $n \ge 15$

*Exact, uniform-in-$n$ rank argument via the perfect-square structure (task line (b), with the chain decomposition of line (c) appearing as the $\mathbb{Z}/3$ charge grading). All computations are exact rational arithmetic. Nothing in the cloned repository was modified; this package is submitted on the branch `muse/sextic-c2-proof`. Deliverables in this directory: `step1_dims_and_identities.py`, `step2_chain_basis.py`, `step3_symbolic.py`, `step4_final_checks.py`, their `.log` files and `*_results.json` outputs.*

---

## PROVED

**Theorem (C2).** Let $\varepsilon = \pm 1$, $F = q^3 + \varepsilon p^3$, and $H = F^2 = q^6 + 2\varepsilon\, q^3p^3 + p^6$ (so $H = H_2$ for $\varepsilon = +1$ and $H = H_{-2}$ for $\varepsilon = -1$). Then for every $n \ge 15$,
$$E_n(H) = \{G \in V_n : T_3(H, G) = T_5(H, G) = 0\} = 0.$$

The argument in fact gives $E_n(H) = 0$ for all $n \ge 9$ (Remark 3), and it *explains* the exceptional degrees $4, 6, 8$ (Remark 4). Conventions: $V_n$ is the space of binary forms of degree $n$ with coefficient $g_c$ on $q^c p^{n-c}$; $T_k$ is the repository's transvectant, $T_k(f,g) = \sum_j (-1)^j \binom{k}{j} (\partial_q^{k-j}\partial_p^j f)(\partial_q^j \partial_p^{k-j} g)$; $\hat C = q\partial_q - p\partial_p$ is the charge operator; $(x)_s = x(x-1)\cdots(x-s+1)$.

### Lemma 1 (the square identities)

For every $G$,
$$T_5(H, G) = 20\; T_2\bigl(F,\, T_3(F, G)\bigr), \qquad T_3(H, G) = 6\, T_2\bigl(F,\, T_1(F,G)\bigr) + 2F\, T_3(F, G) + 216\varepsilon\, \hat C G.$$

*Proof.* Work in the flat Weyl–Moyal algebra, $f \star g = \sum_{k \ge 0} \frac{(i\hbar/2)^k}{k!} T_k(f, g)$ (all series finite on polynomials; the partner gates are the odd $T_k$ precisely because $[f,g]_\star / (i\hbar) = \sum_{k\ \mathrm{odd}} \frac{2(i\hbar)^{k-1}}{2^k k!} T_k(f,g)$). Associativity gives $[F \star F, G]_\star = F \star [F,G]_\star + [F,G]_\star \star F$. Three finiteness facts drive everything:

1. Since $\deg F = 3$, $T_k(F, \cdot) = 0$ for $k \ge 4$, so $[F,G]_\star = i\hbar\, T_1(F,G) + \frac{(i\hbar)^3}{24} T_3(F,G)$ — only two terms.
2. $F \star F = F^2 - \frac{\hbar^2}{8} T_2(F,F)$: the odd terms vanish ($T_1(F,F) = \{F,F\} = 0$, and $T_3(F,F) = 0$ by the $j \leftrightarrow 3-j$ antisymmetry), the terms $k \ge 4$ vanish by degree, and a direct computation gives $T_2(F,F) = 2(\partial_q^2 F)(\partial_p^2 F) - 2(\partial_q\partial_p F)^2 = 2(6q)(6\varepsilon p) = 72\varepsilon\, qp$. Hence $H = F^2 = F \star F + 9\varepsilon\hbar^2 qp$.
3. $[qp, G]_\star = i\hbar\, T_1(qp, G) = -i\hbar\, \hat C G$: odd $T_k(qp, \cdot)$ with $k \ge 3$ vanish because $k$ derivatives cannot be distributed on the degree-2 monomial $qp$ (each term needs $k - j \le 1$ and $j \le 1$), and $T_1(qp, G) = p\,G_p - q\,G_q = -\hat C G$.

Now expand $F \star [F,G]_\star + [F,G]_\star \star F$. In the symmetrised sum only even transvectant orders survive ($T_j(X, F) = (-1)^j T_j(F, X)$), and $j \le 3$ by fact 1's degree bound, so from the $T_1$-part of $[F,G]_\star$ one gets $2i\hbar F T_1(F,G) + \frac{(i\hbar)^3}{4} T_2(F, T_1(F,G))$, and from the $T_3$-part one gets $\frac{(i\hbar)^3}{12} F T_3(F,G) + \frac{(i\hbar)^5}{96} T_2(F, T_3(F,G))$. Adding fact 3's contribution $9\varepsilon\hbar^2 \cdot (-i\hbar \hat C G) = 9\varepsilon (i\hbar)^3 \hat C G$ and matching coefficients of $\hbar^2$ and $\hbar^4$ in $[H,G]_\star/(i\hbar) = T_1(H,G) - \frac{\hbar^2}{24} T_3(H,G) + \frac{\hbar^4}{1920} T_5(H,G)$ against the expansion gives the two identities (the $\hbar^0$ match is the chain rule $T_1(H,G) = 2F\,T_1(F,G)$). $\square$

The point: the sextic gate $T_5$ *factors through the cubic gate* $T_3(F, \cdot)$, and both cubic-side operators are elementary because $F$ has no mixed monomials:

**Corollary (coefficient forms).** With $\mathfrak{D} := T_3(F, \cdot)/6 = \partial_p^3 - \varepsilon \partial_q^3$ and $\mathfrak{L}$ defined by $T_2(F, Y) = 6\mathfrak{L} Y$:
$$(\mathfrak{D} g)_C = (n-C)_3\, g_C - \varepsilon (C+3)_3\, g_{C+3}, \qquad (\mathfrak{L} y)_C = (m-C+1)_2\, y_{C-1} + \varepsilon (C+2)_2\, y_{C+2}$$
($Y \in V_m$ in the second formula), and $T_5(H, G) = 0 \iff \mathfrak{L}(\mathfrak{D} G) = 0$. Moreover, expanding Lemma 1's second identity in the monomial basis (using $T_1(F,G)$'s coefficients $X_j = 3[(n-j+2)g_{j-2} - \varepsilon(j+1)g_{j+1}]$) gives $\Phi := T_3(H, \cdot)$ the form
$$\Phi_K = 120\,(n-K+3)_3\, g_{K-3} \;+\; \varepsilon\, \tilde B(n,K)\, g_K \;-\; 120\,(K+3)_3\, g_{K+3},$$
$$\tilde B(n,K) = 108\bigl[-K(n-K+2)_2 + (n-K)(K+2)_2\bigr] + 12\bigl[(n-K)_3 - K_3\bigr] + 216(2K-n).$$

### Lemma 2 (chains)

$\mathfrak{D}$, $\mathfrak{L}$ and $\Phi$ preserve each **chain** $r \in \{0, 1, 2\}$ (the indices $c \equiv r \pmod 3$) — immediate from the coefficient formulas — hence so do $T_3(H, \cdot)$ and $T_5(H, \cdot)$, and $E_n(H)$ splits as a direct sum over chains. (This is the $\mathbb{Z}/3$ charge grading: the symmetry $(q, p) \mapsto (\omega q, \omega^2 p)$ of $F$.) It suffices to kill each chain part separately. Write $W^{(r)}_n = \{g \text{ on chain } r : \mathfrak{L}\mathfrak{D} g = 0\} \supseteq E_n^{(r)}$.

### Lemma 3 ($\ker \mathfrak{L}$ is explicit, and usually zero)

Let $m \ge 2$ and consider chain $r$ of $V_m$. The equations $(\mathfrak{L} y)_C = 0$ for $C \equiv r+1 \pmod 3$, $0 \le C \le m-1$, are of three kinds: **links** between consecutive chain elements $c, c+3 \le m$, at $C = c+1$: $(m-c)_2\, y_c + \varepsilon (c+3)_2\, y_{c+3} = 0$, with both coefficients nonzero (since $c \le m-3$); a **left singleton**, only for $r = 2$, at $C = 0$: $2\varepsilon\, y_2 = 0$; and a **right singleton**, present iff $(m - r) \bmod 3 = 2$, at $C = c_{\max} + 1$: $(2)_2\, y_{c_{\max}} = 2 y_{c_{\max}} = 0$ (note $(m - c_{\max})_2 = ((m-r) \bmod 3)_2$, which is $2$ exactly in this case and the equation is absent or trivial otherwise).

Consequently: **if $r = 2$ or $(m-r) \bmod 3 = 2$, then $\ker \mathfrak{L}$ on chain $r$ is $0$** (a singleton kills an end element and the links propagate the zero along the chain); **otherwise $\ker \mathfrak{L}$ on chain $r$ is exactly 1-dimensional**, spanned by $y$ with $y_r = 1$ and
$$y_{c+3} = -\varepsilon\, y_c\, \frac{(m-c)_2}{(c+3)_2}$$
(the links are $L - 1$ triangular equations in $L$ unknowns). In terms of $m \bmod 3$: chain $0$ survives iff $m \not\equiv 2$, chain $1$ survives iff $m \not\equiv 0$, chain $2$ never survives. $\square$

### Lemma 4 (the space cut out by $T_5$)

On chain $r$ of $V_n$ ($n \ge 3$), $\ker \mathfrak{D}$ is exactly 1-dimensional: the equations $(\mathfrak{D} g)_C = 0$ ($C \equiv r$, $0 \le C \le n-3$) are $L - 1$ links in $L$ unknowns, the top equation is the only one containing the top coefficient $g_t$ ($t$ = largest chain index), and all link coefficients are nonzero ($(n-C)_3 \ge (3)_3 = 6$ and $(C+3)_3 \ge 6$). A basis element $\kappa^{(r)}$ is given, with $g_t = 1$, by the downward recursion $g_C = \varepsilon (C+3)_3\, g_{C+3} / (n-C)_3$.

Hence, with $m = n - 3$: in the killed cases of Lemma 3, $W^{(r)}_n = \operatorname{span}\{\kappa^{(r)}\}$; in the surviving cases, $W^{(r)}_n = \operatorname{span}\{\kappa^{(r)}, \pi^{(r)}\}$, where $Y^{(r)}$ is Lemma 3's basis of $\ker \mathfrak{L}$ on chain $r$ of $V_{n-3}$ renormalised to **top coefficient $1$** (its top index is $t - 3$) and $\pi^{(r)}$ is the explicit preimage defined by $\pi_t = 0$ and $(\mathfrak{D}\pi)_C = Y_C$ solved descending ($ (n-C)_3 \ne 0$ at every step). Independence: $\kappa$ has top coefficient $1$, $\pi$ has top coefficient $0$ and $\pi \ne 0$ since $\mathfrak{D}\pi = Y \ne 0$; and any $g \in W^{(r)}_n$ has $\mathfrak{D} g = \lambda Y$ (resp. $0$), so $g - \lambda \pi \in \ker \mathfrak{D}$. $\square$

Note the surviving cases have $\delta := (n - r) \bmod 3 \in \{0, 1\}$: for $r = 0$ survival means $n \not\equiv 2 \pmod 3$ and $\delta = n \bmod 3$; for $r = 1$ survival means $n \not\equiv 0 \pmod 3$ and $\delta = (n-1) \bmod 3$.

### Lemma 5 (the top two coefficients of $\Phi$ are closed forms)

Let $\delta = (n-r) \bmod 3$ and $t = n - \delta$ (the top chain index). With the normalisations of Lemma 4:
$$\Phi_t\bigl(\kappa^{(r)}\bigr) = 108\, \varepsilon\, P_\delta(n), \qquad P_0 = n(n-1)(n-2),\quad P_1 = (n-1)(n-2)^2,\quad P_2 = (n-1)(n-2)(n-4);$$
$$\Phi_t\bigl(\pi^{(r)}\bigr) = 120;$$
$$\Phi_{t-3}\bigl(\kappa^{(r)}\bigr) = \frac{120\, t_3 (t-3)_3 + \tilde B(n, t-3)\, t_3}{(\delta+3)_3} - 120\, t_3, \qquad \Phi_{t-3}\bigl(\pi^{(r)}\bigr) = \varepsilon\left\{ 120\left[\frac{-(t-3)_2}{(\delta+3)_2} + \frac{(t-3)_3}{(\delta+3)_3}\right] + \frac{\tilde B(n, t-3)}{(\delta+3)_3} \right\}.$$

*Derivation.* At $K = t$ the $\Phi$ formula involves only $g_{t-3}, g_t$ (as $g_{t+3} = 0$). For $\kappa$: the $\mathfrak{D}$-equation at $C = t-3$ gives $g_{t-3} = \varepsilon t_3 / (\delta+3)_3$ (using $n - t = \delta$), so $\Phi_t(\kappa) = 120\varepsilon t_3 + \varepsilon \tilde B(n, t)$, and the polynomial identity $120 t_3 + \tilde B(n, t) = 108 P_\delta(n)$ (with $t = n - \delta$) holds for each $\delta \in \{0, 1, 2\}$ by direct expansion (verified symbolically, `step4`). For $\pi$: $g_t = 0$ and $g_{t-3} = Y_{t-3}/(\delta+3)_3 = 1/(\delta+3)_3$ from $(\mathfrak{D}\pi)_{t-3} = Y_{t-3}$, so $\Phi_t(\pi) = 120 (\delta+3)_3 \cdot \frac{1}{(\delta+3)_3} = 120$. At $K = t-3$ one uses additionally $g_{t-6}(\kappa) = t_3(t-3)_3 / [(\delta+3)_3 (\delta+6)_3]$ (two $\mathfrak{D}$-steps down), $Y_{t-6} = -\varepsilon (t-3)_2 / (\delta+3)_2$ (the $\mathfrak{L}$-link at $C = t-5$, using $m - t + 6 = \delta + 3$), and $\pi_{t-6} = [Y_{t-6} + \varepsilon (t-3)_3 \pi_{t-3}] / (\delta+6)_3$ (the $\mathfrak{D}$-equation at $C = t-6$); substituting into the $\Phi$ formula and simplifying gives the stated expressions. All steps are valid for $n \ge 15$ (chains have length $\ge 5$, $t \ge 13$). $\square$

### End of proof

Let $n \ge 15$ and $G \in E_n(H)$. By Lemma 2 each chain part $G^{(r)}$ lies in $W^{(r)}_n$ and satisfies $\Phi(G^{(r)}) = 0$.

*Killed case* (Lemma 3 with $m = n-3$): $G^{(r)} = \lambda \kappa^{(r)}$, and $0 = \Phi_t(G^{(r)}) = \lambda \cdot 108 \varepsilon P_\delta(n)$. The roots of $P_0, P_1, P_2$ lie in $\{0, 1, 2, 4\}$, so $P_\delta(n) \ne 0$ for $n \ge 15$; hence $\lambda = 0$.

*Surviving case* ($\delta \in \{0, 1\}$ by Lemma 4's note): $G^{(r)} = \lambda \kappa^{(r)} + \mu \pi^{(r)}$, and the two functionals $\Phi_t, \Phi_{t-3}$ give a $2 \times 2$ system whose determinant, from Lemma 5's closed forms, is
$$\det\nolimits_0(n) = -216\, n\, (n-1)^2 (n-2) (n-6) (n+8), \qquad \det\nolimits_1(n) = -54\, (n-1)^2 (n-2)^2 (n-8) (n+8)$$
(the factorisation is exact symbolic algebra on Lemma 5's formulas, `step3`/`step4`; the determinant is the same for $\varepsilon = +1$ and $\varepsilon = -1$, the two $\varepsilon$'s in the $\kappa$-column and $\pi$-row cancelling). The roots of $\det_0$ are $\{-8, 0, 1, 2, 6\}$ and of $\det_1$ are $\{-8, 1, 2, 8\}$; both are nonzero for $n \ge 15$. Hence $\lambda = \mu = 0$.

Every chain part vanishes, so $G = 0$. $\blacksquare$

**Remark 3 (range).** The only places the size of $n$ is used are: Lemma 3 needs $m = n - 3 \ge 2$; Lemmas 4–5 need the chain indices $t, t-3, t-6$ and the equation indices $t-3, t-5, t-6$ to be in range, which holds for $n \ge 9$; and the nonvanishing of $P_\delta$ and $\det_\delta$, which holds for $n \ge 5$ resp. $n \ge 7$ ($\delta = 0$) and $n \ge 9$ ($\delta = 1$). So the same argument proves $E_n(H_{\pm 2}) = 0$ for all $n \ge 9$, matching the computed tables ($E_n = 0$ for $9 \le n \le 14$ was previously known only by computation through degree 30/120).

**Remark 4 (the proof sees the small-degree partners).** The closed forms vanish exactly where they must. At $n = 4$: chain $2$, $\delta = 2$, $P_2(4) = 0$ — the partner $(qp)^2$. At $n = 6$: chain $0$ is 2-dimensional and $\det_0(6) = 0$ through the factor $(n - 6)$ — the partner $H$ itself, whose monomials $q^6, q^3p^3, p^6$ all lie in chain $0$. At $n = 8$: chain $1$ is 2-dimensional and $\det_1(8) = 0$ through the factor $(n-8)$ — the partner $G_8 = q^7p + qp^7 - \frac{7}{10}(qp)^4$-type element, all of whose monomials have $c \equiv 1 \pmod 3$. Degrees $0, 1, 2$ are exceptional for the trivial reason that both gates differentiate $G$ more times than its degree (and appear as roots of $P_0, P_1$). The factor $(n + 8)$ in both determinants has no partner meaning (negative root).

---

## COMPUTED EVIDENCE (machine verification of the proved statements)

Every step of the proof that involves a formula was additionally verified by exact rational computation (`sextic_lib` machinery, the repository's own conventions); these are confirmations of the proved statements above, not substitutes for them:

1. **Identities (Lemma 1).** Verified exactly on 191 random rational $G$ (96 at $\varepsilon = +1$, 95 at $\varepsilon = -1$; degrees $0$–$20$ plus $25, 30, 37$): `step1`, all three identities $T_1, T_3, T_5$ hold in every trial. Single-gate dimensions for $n \le 40$: $\dim \ker T_5$ cycles $4, 5, 4$ by $n \bmod 3 = 0, 1, 2$ — exactly the count Lemmas 3–4 predict ($3$ from $\ker \mathfrak{D}$ plus $1$ or $2$ from $\ker \mathfrak{L}$) — and $E_n = 0$ for $9 \le n \le 40$, $E_n \ne 0$ exactly at $n \in \{0, 1, 2, 4, 6, 8\}$. (Side observation, not used: $\dim \ker T_3(H_{\pm 2}, \cdot)$ is $1$ at every even $n \ge 4$ and $3$ at $n = 17$; those kernel elements are killed by $T_5$, which is why the proof must combine the gates as it does.)
2. **Chain basis (Lemmas 3–4).** For all $5 \le n \le 63$ and both $\varepsilon$: every constructed $\kappa^{(r)}, \pi^{(r)}$ was checked to lie in $\ker T_5(H, \cdot)$ via the library transvectant, the full $W_n$ basis was checked independent, and its dimension was checked against $\dim \ker T_5$ computed by raw rank: `step2`, all pass.
3. **$\Phi$ coefficient formula (Corollary).** Verified against the library's $T_3(H, \cdot)$ on random $G$ for $n \le 25$, both $\varepsilon$: `step3(a)`, exact agreement.
4. **Top closed forms and determinants (Lemma 5, end of proof).** $\Phi_t(\kappa) = 108\varepsilon P_\delta(n)$, $\Phi_t(\pi) = 120$, and $\det_\delta(n)$ were checked against the $\Phi$-values extracted from the constructed bases for **all** $n = 15, \dots, 63$, all chains, both $\varepsilon$: `step3(b),(c)`, exact agreement in every case (e.g. at $n = 15, r = 0$: $\Phi_t(\kappa) = 294840 = 108 \cdot 15 \cdot 14 \cdot 13$ and $\det = -1{,}708{,}892{,}640 = -216 \cdot 15 \cdot 14^2 \cdot 13 \cdot 9 \cdot 23$).
5. **Polynomial identities.** $120 t_3 + \tilde B(n, t) = 108 P_\delta(n)$ for $\delta = 0, 1, 2$ and the determinant factorisations are pure symbolic identities (sympy, exact): `step4`. These are proofs, listed here only for reproducibility.

The pre-existing evidence (exact computation through degree 30 in PR #6; through degree 120 with a mod-$10007$ rank check in `~/workspace/research/expansions/sextic_pm2_tail/`) is now superseded by the proof.

## OBSTRUCTION / SCOPE

No obstruction remains for C2 — the proof closes. For the record, the two places where the naive approaches genuinely fail, and what the proof does and does not cover:

- **Why line (a) alone (family resultants at $a = \pm 2$) was not the route taken:** the per-degree minors $\rho_n(a)$ of the family analysis are polynomials in $a$ whose values at $a = \pm 2$ are not visibly nonzero uniformly in $n$ from any computed factorisation; the proof instead exploits the square structure at $a = \pm 2$ itself (line (b)), where the $T_5$ gate collapses to $\mathfrak{L}\mathfrak{D}$ and the surviving kernel is at most 2-dimensional per chain. Line (c)'s symmetry is present but only through the $\mathbb{Z}/3$ chain grading.
- **The argument is special to the perfect-square case.** It uses $\deg F = 3$ and the absence of mixed monomials in $F$ (which makes $\mathfrak{D}$ constant-coefficient and $\mathfrak{L}$ linear-coefficient). It says nothing about $a \ne \pm 2$ (settled by the repository's simple-root certificate plus computation) and does not reprove that case.
- **C3 (depth-one death of static partners) is untouched**: this is a statement about the static spaces $E_n$ only; the dynamic core conclusion $D_\infty(H_{\pm 2}) = \operatorname{span}\{1, H\}$ in degrees $\le 16$ was already certified in PR #6 and is neither reproved nor extended here.
- The proof is an explicit rank/certificate argument (the two top output coefficients of $\Phi$ per chain, with completely factored resultants $P_\delta$ and $\det_\delta$). It offers no invariant-theoretic explanation of *why* the factorisations are so clean (e.g. whether $\det_\delta$'s factors $(n-6)$, $(n-8)$ reflect a representation-theoretic feature of the $(2,2,2)$ root configuration); that remains an open interpretive question, not a gap in the proof.
