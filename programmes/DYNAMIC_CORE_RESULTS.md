# Dynamic exact cores: discovery receipts, all-degree kernels and the first strata

This note records what the W1/W2 milestones established, under exactly which hypotheses, and how each claim is checked. It extends `HAMILTONIAN_CORES.md` (the abstract reduction N001, supplied with the handoff) and does not re-derive the retained static classifications of the published report.

**Setting.** One canonical pair, coefficients in **Q**, the flat Weyl–Moyal convention of the report. For a polynomial `H`, `D = {H,·} = H_q ∂p − H_p ∂q`, and `C_k = T_k(H,·)` for the nonzero odd transvectants with `k ≥ 3`. The dynamic core is

```
D∞(H) = { G ∈ Q[q,p] : C_k D^r G = 0 for all odd k ≥ 3 and all r ≥ 0 }.
```

## 1. The discovery backend (W1)

`extensions/hamiltonian/weyl_groebner.py` computes a finite generating set of the left ideal `I∞ = Σ_{k,s} W₂·C_k D^s` of the Weyl algebra `W₂ = Q[q,p]⟨∂q,∂p⟩`. It alternates left Buchberger completion with reduction of the **right** products `P_i D`, adjoining any nonzero remainder, until every `P_i D` reduces to zero. The term order is the weight `(0,0,1,1)` on `(q,p,∂q,∂p)` refined by total degree and reverse lexicographic order. Because the normal-ordering corrections of `∂^c q^e` divide the leading monomial, `lm(m·f) = m·lm(f)` for every monomial `m`, so left S-polynomials and left reduction behave as in the commutative case.

Every element carries a cofactor expression in the sources `C_k D^s`; cofactors are expanded only for S-polynomials that survive reduction. The exported `weyl-invariant-kernel-v1` receipt contains, for the final interreduced basis:

- `C_k = Σ U_ki P_i` for every nonzero gate (correction containment);
- `P_i = Σ V_iks C_k D^s` (iterated-gate provenance);
- `P_i D = Σ A_il P_l` (right-`D` closure).

The bundled checker `weyl_receipts.verify_certificate` recomputes `H`, `D` and all gates and replays every identity as an operator identity. It does not trust the backend. Together the three families prove that the receipt ideal equals `I∞`, so its polynomial common kernel is `D∞(H)` in **all degrees**: this is the reduction N001. A step, generator or degree budget returns `unknown` and never a partial receipt.

**Calibration.** For `H = q³`, discovery returns exactly the handoff's receipt `P = ∂p³`. For `H = qp³` it returns `P₁ = q∂q³ − 3p∂q²∂p` and `P₂ = p³∂q²∂p + (3/4)p²∂q²`. Both lie in `W₂∂q²`, but `∂q²` reduces to a nonzero normal form, so `I∞(qp³) ⊊ W₂∂q²`. This makes the handoff's caution concrete: equal polynomial kernels do not identify the Weyl ideals.

## 2. From a finite ideal to its polynomial solutions in all degrees

A finite PDE presentation does not by itself classify its polynomial solutions. `weyl_kernel.py` produces, and `check_weyl_kernel.py` independently replays, a `weyl-kernel-v1` **support certificate** with three admissible claim kinds. All three rest on one elementary lemma.

**Lemma (monomial action).** Suppose all normally ordered terms `q^a' p^b' ∂q^c ∂p^d` of `P` have the same shift `(a'−c, b'−d)`. Then `P q^a p^b = ψ(a,b) q^{a+Δa} p^{b+Δb}` with `ψ = Σ coef·(a)_c (b)_d`, and distinct monomials go to distinct monomials. Hence `PG = 0` exactly when `supp G ⊆ Z(ψ) = {(a,b) ∈ N² : ψ(a,b) = 0}`.

**Zero sets.** Write `ψ_i = g·φ_i`, where `g` is a constant times a product of linear forms. The zeros of `g` in `N²` are vertical or horizontal lines, arithmetic progressions `(a₀,b₀)+t(Δa,Δb)`, or finitely many points. Suppose a polynomial identity `Σ λ_i φ_i = U(a)V(b)` holds with nonzero univariate `U` and `V`. Then every common zero of the `φ_i` lies on a line `a = a₀` with `U(a₀)=0`, or on a line `b = b₀` with `V(b₀)=0`. On each such line the restricted `φ_i` either vanish identically or have finitely many integer roots. The checker verifies `ψ_i = gφ_i` and `Σλ_iφ_i = UV` by multiplication. It finds integer roots exactly by the rational root theorem, rebuilds the zero set `Z`, and compares it with the declared one.

- **`monomial_span`.** Every generator acts monomially, so the core is the span of the monomials in `Z`.
- **`finite_support`.** The monomially acting generators already force a finite `Z`, so the core is the exact kernel of **all** generators on `span(Z)`.
- **`degree_bound`.** Fix a positive weight `w`. For every generator take its top weighted symbol `σ_w(P_i)`, the terms of maximal weighted shift. If `G` is in the kernel with top component `G_top`, then the top component of `P_iG` is `σ_w(P_i)G_top`, so it vanishes. When the monomially acting top symbols have a finite common zero set `Z`, every solution satisfies `deg_w G ≤ N = max_{z∈Z} w·z`. The core is then computed exactly on all monomials of weighted degree at most `N`, with images taken in full and no projection. The checker derives `N` itself.

Every certificate embeds its receipt, so the checker also replays the operator identities.

### Certified all-degree cores

Each row below has an enveloped certificate in `results/hamiltonian/`. Each was cross-checked against the baseline independent star-exponential engine (`research/hamiltonian/independent/engine.py`). Sampled core elements stay exact through three further actions of `D`, and low-degree monomials outside the core fail within six.

| `H` | generators | `D∞(H)` | route |
|---|---:|---|---|
| `q³` | 1 | `Q[q] ⊕ pQ[q] ⊕ p²Q[q]` | monomial span |
| `qp³` | 2 | `Q[p] ⊕ qQ[p]` | monomial span |
| `qp³ + q²` | 13 | `span{1, H}` | finite support |
| `qp³ + p²` | 2 | `Q[p] ⊕ qQ[p]` | monomial span |
| `qp³ + q² + p²` | 13 | `span{1, H}` | degree bound, `w=(1,1)`, `N=4` |
| `q³p³` | 1 (`q∂q − p∂p`) | `Q[qp]` | monomial span (progression) |
| `q²p²` | 6 | `Q[qp]` | monomial span (progression) |
| `q²p³` | 6 | `span{1, qp, q²p³}` | monomial span |
| `p³ + q²` | 8 | `span{1, H}` | finite support |

The rows for `q³`, `qp³` and `qp³+q²` lie inside scopes the report already solved or the handoff already derived (N002). They are **calibrations** of the machinery. The other rows are new exact computations of this programme, made under the stated hypotheses and with no literature-priority claim. In particular, `I∞(q³p³) = W₂(q∂q − p∂p)` is a one-generator ideal, so its core is the Euler-type kernel `Q[qp]`.

## 3. Theorem (W2): the quadratic-perturbation strata of `qp³ + αq² + βp²`

**Theorem.** For all `α, β ∈ Q`, with `H_{α,β} = qp³ + αq² + βp²`:

```
D∞(H_{α,β}) = Q[p] ⊕ qQ[p]     if α = 0,
D∞(H_{α,β}) = span_Q{1, H_{α,β}}  if α ≠ 0.
```

The static exact-partner space is the same for every `(α,β)`, because the quadratic terms do not change any gate `C_k` with `k ≥ 3`. So the one-step space never moves. The dynamic core collapses from infinite dimension to dimension two exactly when `α ≠ 0`, whatever the value of `β`. The perturbation `βp²` alone never collapses it.

**Proof.** Four steps.

1. *Covariance.* For `g ∈ GL₂(K)` acting linearly on `(q,p)`, the transvectants satisfy `T_k(F∘g, G∘g) = det(g)^k·T_k(F,G)∘g`. This holds because `T_k` is the `k`-th power of the omega operator `∂q₁∂p₂ − ∂p₁∂q₂` restricted to the diagonal; the gate formula in `weyl_receipts.gate` is exactly this expansion. Hence `D_{H∘g}(G∘g) = det(g)·(D_H G)∘g` and `C_k^{H∘g}(G∘g) = det(g)^k (C_k^H G)∘g`, so `D∞(H∘g) = D∞(H)∘g`. Nonzero rescaling `H ↦ cH` multiplies every operator by a power of `c`, and adding a constant changes nothing.
2. *Normal forms over Q̄.* Substitute `(q,p) ↦ (sq, tp)` and divide by `st³`. This gives `qp³ + (αs/t³)q² + (β/(st))p²`. If `αβ ≠ 0`, take `t⁴ = αβ` and `s = t³/α` to reach `(1,1)`. If `α ≠ 0 = β`, take `s = t³/α` to reach `(1,0)`. If `α = 0 ≠ β`, take `s = β/t` to reach `(0,1)`. Otherwise the form is already `(0,0)`.
3. *Certified normal forms.* Over Q the four certificates give `D∞ = Q[p]⊕qQ[p]` for `(0,0)` and `(0,1)`, and `span{1,H}` for `(1,0)` and `(1,1)`. Each certified core is the common kernel of finitely many operators with rational coefficients, so it commutes with extension to Q̄.
4. *Transport and descent.* The diagonal substitution maps `Q̄[p] ⊕ qQ̄[p]` to itself, and it maps `span{1, H_nf}` to `span{1, H_{α,β}}`. This gives `D∞_{Q̄}(H_{α,β})`. The Q-core is a Q-form of it, so `D∞_Q(H_{α,β}) = D∞_{Q̄}(H_{α,β}) ∩ Q[q,p]`, which is the stated space. ∎

The theorem reproduces the handoff corollary N002 (`β = 0`) as a special case. Its coverage of the parameter plane is proved by the normal-form argument, not by sampling. The only divisions are by `α`, `β` and `t`, each made on a branch where that quantity is nonzero. The exceptional locus is `α = 0`, and within it `β = 0` and `β ≠ 0` give the same core.

## 3b. Theorem: the full six-parameter quadratic perturbation family

**Lemma (top-weight reduction).** Fix a positive integer weight `w` on `(q,p)`. Write `H = H_w + H_<`, where `H_w` holds the terms of maximal weight `h` and every term of `H_<` has strictly smaller weight. If `G ∈ D∞(H)` has top weighted component `G_top`, then `G_top ∈ D∞(H_w)`.

*Proof.* `D_H` and every gate `C_k(H)` are linear in `H`. Their top weighted parts are `D_{H_w}` and `C_k(H_w)`, and every other part has strictly smaller weighted shift. In `C_k(H) D_H^r G`, the component of weighted degree `deg_w G + r·s_D + s_k` is therefore exactly `C_k(H_w) D_{H_w}^r G_top`. Since the whole expression is zero, so is this component. The odd orders `k` that `H_w` can have are among those considered for `H`. ∎

The lemma says that the associated graded of `D∞(H)`, for the weighted filtration, embeds in `D∞(H_w)`. Two consequences follow.

- **Finite top core.** If `D∞(H_w) = span{1, H_w}` with `h > 0`, then `dim D∞(H) ≤ 2`. Since `1` and `H` always lie in `D∞(H)`, it follows that `D∞(H) = span{1, H}`.
- **Line core.** If `D∞(H_w) = V` is spanned by `w`-homogeneous monomials and `V ⊆ D∞(H)`, then `D∞(H) = V`. Indeed, any `G ∈ D∞(H)` has `G_top ∈ V ⊆ D∞(H)`, so `G − G_top ∈ D∞(H)` has lower weighted degree, and the descent ends in `V`.

**Theorem.** For all rational `a, b, c, d, e, f`, with `H = qp³ + aq² + bqp + cp² + dq + ep + f`:

```
D∞(H) = Q[p] ⊕ qQ[p]   if a = 0,
D∞(H) = span_Q{1, H}    if a ≠ 0.
```

*Proof.* Take `w = (3,1)`. The term `qp³` has weight 6, `q²` has weight 6, `qp` has 4, `q` has 3, `p²` has 2, `p` has 1 and the constant has 0.

- If `a ≠ 0`, then `H_w = qp³ + aq²` and `D∞(H_w) = span{1, H_w}` by §3. The finite-top consequence gives the claim.
- If `a = 0`, then `H_w = qp³` and `D∞(qp³) = V = Q[p] ⊕ qQ[p]`, which is spanned by monomials. It remains to show `V ⊆ D∞(H)`.
  - The gates `C_k(H)` with `k ≥ 3` coincide with those of `qp³`, because the remaining terms are at most quadratic. They kill `V`.
  - `D_H(g + qh) = (p³ + bp + d)(g′ + qh′) − (3qp² + bq + 2cp + e)h` lies again in `V`.
  - So every iterate of an element of `V` stays in `V`, where the gates vanish, and the line-core consequence gives the claim. ∎

This contains the §3 theorem (`b = d = e = f = 0`) and the corollary N002. The parameter space is covered by the proof, not by sampling, and no division by a parameter occurs. The only exceptional locus is `a = 0`.

**Certificates.** `extensions/hamiltonian/check_top_reduction.py` (format `weyl-top-reduction-v1`) checks any instance of the lemma.

- It recomputes the weighted top part and replays the embedded all-degree certificate for `D∞(H_w)`.
- For line cores it proves `V ⊆ D∞(H)` symbolically in the `p`-exponent `j`: every gate kills `q^i p^j`, and `D_H` maps `q^i p^j` into `V`, for all `j`.
- The tests certify 16 random members of the family. They cross-check each one with the baseline star engine and refuse the wrong weight `(1,1)`, under which the line core of `qp³` is not preserved by the `q²` term.
- Two direct Gröbner certificates with `a = 0`, `qp³ + qp + p² + q + p` and `qp³ + 2qp − p² + 3q`, independently give `Q[p] ⊕ qQ[p]`.

## 3c. Homogeneous quartics

For a homogeneous `H`, the operators `D` and `C_k` are homogeneous, so `D∞(H)` is graded by degree. Both the static exactness condition and the dynamic core are `GL₂`-covariant, with `T_k(F∘g, G∘g) = det(g)^k T_k(F,G)∘g`. Over Q̄ the root types are:

- `(4)`, `(3,1)`, `(2,2)` and `(2,1,1)`, each a single class;
- distinct roots, where `H` is equivalent to a multiple of `H_λ = q⁴ + λq²p² + p⁴` with `λ² ≠ 4`.

**All-degree certificates** (`weyl-kernel-v1`; files under `results/hamiltonian/`):

| type | representative | `D∞(H)` |
|---|---|---|
| (4) | `q⁴` | `Q[q] ⊕ pQ[q] ⊕ p²Q[q]`, which equals `E(q⁴)` |
| (3,1) | `q³p` | `Q[q] ⊕ pQ[q]`. The exceptional static monomials `q^c p^{3c+2}` drop out. |
| (2,2) | `q²p²` | `Q[qp]` |
| (2,1,1) | `q³p + q²p²` | `span{1, H}` |
| distinct, `λ = 0` | `q⁴ + p⁴` | `span{1, H}` |
| distinct, `λ = 1` | `q⁴ + q²p² + p⁴` | `span{1, H}`, from 22 generators and 23 minutes of discovery |
| distinct, `λ = −1` | `q⁴ − q²p² + p⁴` | `span{1, H}`, from 22 generators |

**Theorem (degenerate root types).** Each of the root types `(4)`, `(3,1)`, `(2,2)` and `(2,1,1)` is a single `GL₂(Q̄)` class. The certificates above therefore classify `D∞(H)` for **every** rational quartic of that type, by transport through Q̄ and descent: the core is a common kernel of rational operators, so it commutes with field extension. In each case:

- type `(4)`, `H = cL⁴`: `D∞ = ⊕_{j≤2} M^j Q[L]`, with `M` any complementary linear form;
- type `(3,1)`, `H = cL³M`: `D∞ = Q[L] ⊕ M·Q[L]`;
- type `(2,2)`, `H = cQ²` with `Q` a nondegenerate binary quadratic: `D∞ = Q[Q]`;
- type `(2,1,1)`: `D∞ = span{1, H}`.

**Per-degree theorem for all distinct-root quartics.** Let `S^R_n(λ) = {G ∈ V_n : C₃D^rG = 0 for r ≤ R}`, which contains `D∞(H_λ)_n`. For each degree `n` the certificate `quartic-rigidity-v1` (checker `check_quartic_rigidity.py`) records:

- several maximal minors of the defining matrix, as exact polynomials in `λ`;
- the factorization of their gcd;
- the exact rank of the matrix over `Q[x]/(f)` for every factor `f`.

The checker recomputes all of these with its own determinant, interpolation and number-field code. As a result, for **every** `λ ∈ Q̄` and every certified degree:

- `D∞(H)_n = 0` for `n ∉ {0, 4}`, and `D∞(H)_4 = Q̄·H`, for every quartic `H` over Q̄ with distinct roots;
- the only exceptional factor is `λ² − 4`, the square stratum, where the extra kernel is the genuine core `Q̄[q² ± p²]` in even degrees;
- the equianharmonic class `λ² = −12` (j = 0, rational form `q⁴ + qp³`) is not exceptional, but it needs depth `R = 3` in degree 1 and `R = 2` in degree 3. There, linear forms survive two further actions of `D` and cubics survive one. Every other degree needs only `R = 1`.

The per-degree certificate in `results/` covers degrees 1–12.

**Theorem (distinct roots, all degrees).** Let `H` be a binary quartic with four distinct roots, over Q or over any field of characteristic zero. Then `D∞(H) = span{1, H}`.

Together with the theorem for degenerate root types, this classifies the dynamic core of **every** nonzero homogeneous quartic.

*Proof.* Work over Q̄ with `H = c·H_λ`, `λ² ≠ 4`. Since `D∞(H)_n ⊆ S^1_n`, it suffices to show `S^1_n = 0` for all `n ≥ 8`; the per-degree theorem handles `n ≤ 12`.

Write `G = Σ_t h_t q^{n−t}p^t ∈ V_n`. Then:

1. *Parity splitting.* `T₃(H_λ,·)` moves the index `t` by `−3`, `−1` or `+1`, and `D = {H_λ,·}` moves it by `−1`, `+1` or `+3`. Both moves are odd, so `S^1_n` splits into the two parity classes of `t`.
2. *Static recurrence.* The equation `T₃(H_λ, G) = 0` at output index `t` reads, exactly,
   `24(t+3)(t+2)(t+1) h_{t+3} + 12λ(n−1−t)(t+1)(n−2−2t) h_{t+1} − 24(n+1−t)(n−t)(n−1−t) h_{t−1} = 0`.
   Its leading coefficient never vanishes. So every `h_t` is determined by `h_0` and `h_2` in the class of `q^n`, and by `h_1` in the other class.
3. *Top equations.* `DG` has coefficients `d_s = 4(s+1)h_{s+1} + 2λ(2s−2−n)h_{s−1} − 4(n−s+3)h_{s−3}`. The top equations of `T₃(H_λ, DG) = 0` (output indices `t ≤ 4`) are linear in the free top coefficients, with coefficients polynomial in `(n, λ)`. They use only `h_t` with `t ≤ 8` and `d_s` with `s ≤ 7`, so they are exact for every `n ≥ 8`.
4. *Odd class.* The coefficients `c₁(n,λ)` and `c₃(n,λ)` of `h_1` in the equations at `t = 1` and `t = 3` have formal resultant `R₁(n) = Res_λ(c₁, c₃)`, a nonzero polynomial of degree 17. Its integer roots are `−1, 0, 1, 2, 3`, with multiplicity. Deflating them leaves a quadratic with no integer roots inside its Fujiwara bound. A nonzero formal resultant excludes a common factor even where a leading coefficient vanishes, so for `n ≥ 4` and every `λ`, `h_1 = 0`.
5. *Other class.* The 2×2 minors `m₀₁` and `m₀₂` of the system in `(h_0, h_2)`, from the equations at `t = 0, 2, 4`, are both divisible by `λ² − 4`. The resultant `R₂(n)` of the quotients has degree 32 and integer roots `−6, −1, 0, 1, 2, 3, 4` only. So for `n ≥ 5` and `λ² ≠ 4`, `h_0 = h_2 = 0`.
6. *Conclusion.* By step 2, every coefficient then vanishes, so `G = 0`. Hence `D∞(H)_n = 0` for all `n ∉ {0, 4}` and `D∞(H)_4 = Q̄·H`. The result descends to Q because the core is a common kernel of rational operators. ∎

The equation for `λ = 2` vanishes identically in `n`. That is the square stratum, whose genuine core `Q̄[q² ± p²]` is excluded by hypothesis.

**Certificate.** The certificate `quartic-uniform-v1` (checker `check_quartic_uniform.py`; file `results/hamiltonian/quartic_all_degrees_theorem.json`) checks every step.

- It re-derives the top equations with its own polynomial arithmetic.
- It recomputes both resultants by interpolation at the Sylvester degree bounds (19 and 34).
- It verifies the divisibility by `λ² − 4` and determines all integer roots exactly.
- It enforces the validity bound `n ≥ 8`.
- It replays the embedded per-degree certificate for degrees 1–12.

The tests compare the symbolic top equations with direct computation of `T₃∘D` on binary forms for `8 ≤ n ≤ 20` at random `λ`, and reject six forged certificates.

**A second, independent proof in degrees `4k`.** This route uses classical invariant theory instead of monomials.

- Let `f = H`, `Δ` its Hessian and `T = {f, Δ}`. Every covariant of the quartic is a polynomial in `f`, `Δ`, `T` and the invariants. The syzygy is `T² = −(16/9)Δ³ + I f²Δ + J f³`.
- A dimension count shows that `E_{4k}` consists exactly of the forms `Φ(f, Δ)` that solve `T₃(f, Φ) = 0`.
- The two operators involved have the closed forms `T₃(f, f^aΔ^b) = T·[−⅓a(a−1)(4a+1+6b) f^{a−2}Δ^b + (3/16)b(b−1)(2b−1) I f^aΔ^{b−2} + (3/8)b(b−1)(b−2) J f^{a+1}Δ^{b−3}]`, together with the companion formula for `T₃(f, T·f^aΔ^b)`. Its 17 covariant constants were determined by an exact, overdetermined fit.
- Writing `ψ₀`, `ψ₁` for the coefficients of `Δ^k` and `fΔ^{k−1}` in `Φ`, the two top equations are triangular. The coefficient `c₀₀ = −I k²(4k+1)/2` forces `ψ₀ = 0`, and then `c₁₁ ∝ I(k−1)(72k³ − 34k² − k + 3)` forces `ψ₁ = 0`. When `I = 0`, the corresponding `J`-coefficients take over.

This reproduces the theorem for `n ≡ 0 (mod 4)` and `n ≡ 2 (mod 4)` (since `D` is injective into degree `n+2`), for `k ≥ 7`. `extensions/hamiltonian/covariant_route.py` reproduces every ingredient of this route. The certified theorem relies on the monomial route above.

## 3d. Homogeneous quintics and sextics

**Theorem (W4).** Let `H` be a nonzero binary form of degree `d ∈ {5, 6}` over a field `K` of characteristic zero, for example `K = Q`. Write `ℓ, m` for independent linear forms and `Q₂` for a nondegenerate quadratic form. Then:

| root type | form of `H` | `D∞(H)` |
|---|---|---|
| `(d)` | `cℓ^d` | `⊕_{j≤2} m^j K[ℓ]` |
| `(d−1, 1)` | `cℓ^{d−1}m` | `K[ℓ] ⊕ m·K[ℓ]` |
| `(d−2, 2)` | `cℓ^{d−2}m²` | `span{1, ℓm, H}` |
| `(3, 3)`, sextics only | `cQ₂³` | `K[Q₂]` |
| every other type (at least three distinct roots) | | `span{1, H}` |

For a rational `H`, the forms `ℓ`, `m` and `Q₂` in the table can be taken rational. In the first three rows the roots have different multiplicities, so each root is Galois-stable. In the fourth row `Q₂` is defined up to a scalar by `H`. With the quartic theorems of §3c, this classifies the dynamic core of every binary form of degree at most 6.

The proof uses three routes. Every type falls under exactly one of them.

**Route A: monomial classes.** The first four rows are single `GL₂(K̄)` classes. The all-degree certificates `quintic_q5`, `quintic_q4p`, `q2p3`, `sextic_q6`, `sextic_q5p`, `sextic_q4p2` and `q3p3` (`weyl-kernel-v1`, monomial span) give the cores of the representatives. The cores transport by covariance and descend as in §3.

**Route B: a root of multiplicity 2 or `d − 2`.** This covers quintic types `(3,1,1)`, `(2,2,1)`, `(2,1,1,1)` and sextic types `(4,1,1)`, `(3,2,1)`, `(2,2,2)`, `(2,2,1,1)`, `(2,1,1,1,1)`. Each has at least three distinct roots.

1. Move the root to `(1:0)`. On forms of one degree, the weight `(2,1)` orders monomials by their `q`-exponent. The top part of `H` is then `q^{d−μ}p^μ` with `μ ∈ {2, d−2}`.
2. By the top-weight lemma (§3b), the leading monomial of every `G ∈ D∞(H)` lies in `D∞(q^{d−2}p²)`, up to the swap `q ↔ p`. That core is `span{1, qp, q^{d−2}p²}` (Route A).
3. Hence `D∞(H)_n = 0` for `n ∉ {0, 2, d}`, and `D∞(H)_d = K·H`.
4. For `G ∈ D∞(H)_2`, `{H, G} ∈ D∞(H)_d = K·H`.
   - If `{H, G} = 0`, then `G` lies in the centralizer (lemma below), which has no quadratic elements because `H` has at least three distinct roots.
   - `{H, G} = cH` with `c ≠ 0` is impossible by the sl₂ lemma.
5. So `D∞(H) = span{1, H}`.

**Route C: types `(1⁵)`, `(1⁶)` and `(3,1,1,1)`.** These have a simple root and no root of multiplicity `≥ d − 2`.

1. *Static finiteness.* The certificates `binary_static_d5` and `binary_static_d6` (`binary-static-v1`) prove the following. If `H` of degree `d` has a simple root and `E_n(H) = {G : T₃(H,G) = T₅(H,G) = 0} ≠ 0` for some `n ≥ N₀`, then `H` has type `(d−1, 1)` or `(d−2, 1, 1)`. The bound is `N₀ = 10` for `d = 5` and `N₀ = 17` for `d = 6`. Since `D∞(H)_n ⊆ E_n(H)`, it follows that `D∞(H)_n = 0` for `n ≥ N₀`.
2. *Chain argument.* Let `G ∈ D∞(H)_n`. Then `D^rG ∈ D∞(H)_{n + r(d−2)}`, which vanishes for large `r`. Take `r` minimal with `D^rG = 0`. If `r ≥ 1`, then `F = D^{r−1}G` is a nonzero element of `ker D ∩ D∞(H)`.
   - Because `H` is not a proper power, `ker D = K[H]`.
   - `H^j ∉ D∞(H)` for `j ≥ 2`. At a simple root, the top part of `H^j` is `(q^{d−1}p)^j`, and `p^j` with `j ≥ 2` does not occur in `D∞(q^{d−1}p) = K[q] ⊕ pK[q]`.
   - So `F` is a constant or `cH`. A constant forces `n = 0`. If `F = cH` with `r ≥ 2`, then `D^{r−2}G` is a quadratic with `{H, D^{r−2}G} = cH`, `c ≠ 0`, which the sl₂ lemma excludes.
   - Hence `G ∈ span{1, H}`.

**Lemma (centralizer).** Write `H = aR^g` with `R` not a proper power. Then `{H, G} = 0` implies `G ∈ K[R]`.

*Proof.* For homogeneous `G` of degree `k`, the degree-0 function `f = G^d/H^k` satisfies `{H, f} = 0`, so `∇f ∥ ∇H`. Euler's relation gives `x·∇f = 0` and `x·∇H = dH ≠ 0`, so `∇f = 0` and `G^d = cH^k`. Unique factorization then gives `G ∝ R^s`, because the multiplicities of `R` have gcd 1. ∎

**Lemma (sl₂).** If `H` has at least three distinct roots, no quadratic `G` satisfies `{H, G} = cH` with `c ≠ 0`.

*Proof.* Quadratic forms span `sl₂` under the bracket, and `ad G` acts on `V_d` as that element.
- A nilpotent element acts nilpotently, so it has no eigenvalue `c ≠ 0`. Hence `G` is semisimple.
- Then `G = λℓm` over `K̄`, and `ad(ℓm)` multiplies `ℓ^a m^b` by a nonzero multiple of `a − b`.
- Its eigenvectors with a given eigenvalue are therefore single monomials `ℓ^a m^{d−a}`, which have at most two distinct roots. ∎

**The static certificate (`binary-static-v1`; checker `check_binary_static.py`).**

1. *Normal form.* Move the simple root to `(1:0)` and normalize by the stabilizer. This gives `H = q^{d−1}p + Σ_{j≥3} h_j q^{d−j}p^j`, and the residual torus acts by `h_j ↦ λ^{j−1}h_j`.
2. *Static top lemma.* The static space of `q^{d−1}p` in degree `n ≥ N₀` is `span{qⁿ, q^{n−1}p}`. The checker re-derives the two gate-coefficient factorizations, `(b)₂[db − 2d + 6 − 3n]` and `(b)₄[(d−5)(b−4) − 5(n−b)]`, and their common zeros. So every nonzero `G ∈ E_n(H)` has `(g₀, g₁) ≠ 0`.
3. *Top equations.* The `T₃` equations determine `g₂, g₃, …` from `(g₀, g₁)`, with denominators that are polynomials in `n`. The `T₅` equations at output indices `0..R−1` (`R = 4` for quintics, `R = 6` for sextics) then give a matrix `M(n, h)` of size `R × 2`.
4. *Cases.* A kernel vector of `M(n, h)` has `g₁ = 0`, or `g₀ = 0`, or, after the torus, `g₀ = g₁`. In the first two cases the first nonzero `h_j` is normalized to 1. Each case is a polynomial system over `Q[n]`.
5. *Elimination trees.* For each system the certificate gives a tree of explicit identities:
   - derived polynomials as combinations of known ones;
   - factorizations `c(n)·∏q_i^{m_i}`, with `c(n) ≠ 0` for `n ≥ N₀`, that branch on `q_i = 0`;
   - leaves that are either a polynomial in `n` with no integer root `≥ N₀`, or identities `c_j(n)·J_j = Σ(multipliers)·(known)`.
6. *The locus `J = 0`.* The common zero locus of `J` (three generators for sextics, two for quintics) is `h = 0` (type `(d−1,1)`) together with the type-`(d−2,1,1)` points. The checker verifies this in `Q[a]/(a² − α)`, with `α = −1/6` and `−1/10`.

The trees were searched for with sympy, which the producer `binary_static.py` uses and nothing else does. The checker uses only exact integer and rational arithmetic, and it re-derives `M(n, h)` independently. The two certificates have 52 and 181 steps.

The type `(4,1,1)` genuinely has a nonzero static space in every degree, which is why it appears in the conclusion. Its dynamic core is still finite, by Route B. For `(3,1,1,1)` the static space is nonzero in degree 12 (`E₁₂ ≠ 0`), which is below the sextic bound `N₀ = 17`. The chain argument needs nothing in degrees below `N₀`.

**Tests** (`test_binary_static.py`):
- the stored certificates pass, and eight forgeries are rejected;
- the evaluated top matrix agrees with direct static spaces computed from the gates;
- for one representative of every quintic and sextic root type, the direct dimensions of `{G : C_kD^rG = 0, r ≤ 3}` in degrees 1–12 equal the classified core. This last test is a consistency check, not part of the proof.

## 5. Arbitrary degree: monomials, root rigidity and active dynamics

**Active part.** Define `𝒜(H) = D∞(H) / (D∞(H) ∩ ker ad_H)`. It counts the observables that actually evolve while staying quantum–classical exact at every iteration. The stationary ones are quotiented out. An infinite core can be entirely stationary (`K[qp]` for `q^kp^k`). A two-dimensional core `span{1, H}` has `𝒜 = 0`.

**Conjecture (root rigidity).** If a homogeneous binary form `H` of degree `d ≥ 3` over a field of characteristic zero has at least three distinct roots, then `D∞(H) = span{1, H}`. In that case `𝒜(H) = 0`.

**The conjecture is proved in every degree** (§5.5, Main Theorem). R1, R2 and R3 cover the odd degrees. Theorem SR covers every form with a simple root, in all degrees. With R1, that is every form with at least three distinct roots.

### 5.1 The monomial theorem (all exponents)

**Theorem M.** Let `H = q^a p^b` with `a ≥ b`, `d = a + b ≥ 3`. Then:

| case | `D∞(H)` | `𝒜(H)` |
|---|---|---|
| `b = 0` | `Q[q] ⊕ pQ[q] ⊕ p²Q[q]` | `pQ[q] ⊕ p²Q[q]` |
| `b = 1` | `Q[q] ⊕ pQ[q]` | `D∞ / span{1, H}`, infinite |
| `a = b ≥ 2` | `Q[qp]` | 0 |
| `a > b ≥ 2` | `span{1, qp, H}` | `Q·qp` (`{H, qp} = (a−b)H`) |

*Proof.*
1. *Support.* `D` and every gate `C_k` map a monomial to a multiple of a monomial by a fixed shift. So `D∞(H)` is spanned by the monomials it contains. The monomial `q^c p^e` lies in `D∞(H)` exactly when the gate coefficients `ψ_k` vanish at every point `(c + r(a−1), e + r(b−1))` of its D-ray. The ray runs up to the first `r` with `δ_r = (ae − bc) + r(b − a) = 0`, or forever if there is none.
2. *Only `T₃` is needed.* Along a ray, `ψ₃` is a cubic in `r` with leading coefficient `(a−1)(b−1)(a−b)(a+b−2)` and `r²`-coefficient `−3(a−1)(b−1)(a+b−2)(ae − a − bc + b)`. On the power line, `ψ₃(λa, λb) = −2abλ(a−b)(λ−1)(λ(a+b) + a + b − 3)`. For `b ≤ 1` the gate factors as `a(a−1)y(y−1)[(a−2)(y−2) − 3x]` (`b = 1`) or `(a)₃(y)₃` (`b = 0`).
3. *Case `a > b ≥ 2`.* At most three points of any ray pass `T₃`, so the ray ends after at most three points. Its endpoint lies on the power line and must be 1 or `H`. This leaves exactly 1, `qp` and `H`.
4. *Other cases.* They follow from the same factorizations (`check_monomial_theorem.py` docstring, steps M1–M3). ∎

The proof also gives an effective stopping rule: `D∞(q^ap^b) = {G : C₃D^rG = 0, r = 0, …, 3}`. The checker `check_monomial_theorem.py` (`monomial-theorem-v1`; `results/hamiltonian/monomial_theorem.json`) verifies the identities in the symbols `a, b, c, e, r, λ` with exact arithmetic. The tests compare the predicted cores with direct dimensions for every `q^ap^b` with `3 ≤ d ≤ 9`, in degrees up to 12. This theorem replaces the per-monomial Gröbner certificates of §§2, 3c and 3d as the logical foundation, though those certificates remain as independent cross-checks.

**Corollary (one or two root directions, all degrees).** Transport by `GL₂(K̄)` gives the core of every homogeneous `H` of degree `d ≥ 3` with at most two distinct roots: `cℓ^d`, `cℓ^{d−1}m`, `cQ₂^{d/2}` (balanced) and `cℓ^am^b` with `a ≠ b`, `a, b ≥ 2`. **Active exact dynamics exists (`𝒜(H) ≠ 0`) for such `H` exactly when `H` is not a balanced power.** It is infinite-dimensional for `cℓ^d` and `cℓ^{d−1}m`, and one-dimensional (spanned by `ℓm`) for unequal powers.

### 5.2 Rigidity theorems

The *sl₂ lemma* and the *centralizer lemma* of §3d hold in every degree.

**Theorem R1 (intermediate multiplicity).** If `H` has at least three distinct roots and some root of multiplicity `μ` with `2 ≤ μ ≤ d − 2` and `μ ≠ d/2`, then `D∞(H) = span{1, H}`.

*Proof.* Move that root to `(1:0)`. The top part for the weight `(2,1)` is `q^{d−μ}p^μ`, an unequal power with both exponents at least 2. By Theorem M its core is `span{1, qp, q^{d−μ}p^μ}`. The top-weight lemma and the two lemmas then conclude as in Route B of §3d. ∎

**Theorem R2 (odd degree, squarefree).** If `d ≥ 5` is odd and `H` is squarefree, then `D∞(H) = span{1, H}`. Moreover `E_n(H) = {G : T₃(H,G) = T_d(H,G) = 0} = 0` for `n ≥ (d−1)(d−2) + 3`.

*Proof.*
1. *`T_d` is a gate.* Since `d` is odd, `T_d` is a gate, and `T_d(H, G) = d!·H(∂_p, −∂_q)G`. Its kernel on `V_n` is the span of the powers `L_iⁿ` of the linear factors of `H`, because `H(∂)` is surjective, being dual to multiplication by `H`.
2. *`T₃` on those powers.* `T₃(H, Σc_iL_iⁿ) = (n)₃ Σ c_i τ_i L_i^{n−3}`, where `τ_i = ∂_{v_i}³H` and `v_i` is the root of `L_i`. Here `τ_i ≠ 0`, because `τ_i` vanishes only at roots of multiplicity at least `d − 2 ≥ 3`.
3. *Independence.* The spaces `L_i^N V_{d−3}` are independent once `N ≥ (d−1)(d−2)`, by apolarity and a dimension count. So `c_iτ_i = 0`, hence `c_i = 0`.
4. *Chain argument* (§3d, Route C):
   - `ker D = K[H]`;
   - `H^j ∉ D∞` for `j ≥ 2`, by the top-weight lemma at a simple root and Theorem M with `b = 1`;
   - the sl₂ lemma excludes quadratics.
   ∎

**Theorem R3 (squarefree cubic).** `D∞(H) = span{1, H}`.

*Proof.* Here `E_n = span{L_iⁿ}`, which is three-dimensional, so static finiteness fails and one step of `D` is used instead. For `G = Σc_iL_iⁿ`, `DG = nΣc_iL_iⁿM_i` with `∂_{v_i}H = L_iM_i` and `M_i(v_i) ≠ 0`. If `DG ∈ E_{n+1} = span{L_i^{n+1}}`, independence of the spaces `L_iⁿV₁` (`n ≥ 4`) forces `c_iM_i ∝ L_i`, hence `c_i = 0`. So `D∞(H)_n = 0` for `n ≥ 4`, and the chain argument concludes. ∎

**Coverage before §5.5.**
- *Odd `d`.* R1, R2 and R3 together cover every odd degree.
- *Even `d`.* R1 leaves the types `(1^d)` and `(d/2, 1^{d/2})`. Degrees 4 and 6 were handled in §§3c and 3d. §5.5 closes the remaining cases in every degree.

### 5.5 Simple-root rigidity and the complete classification

**What the sextic certificate shows.**
- *Leading-order degeneracy.* The second entry of each row of the static top matrix has the same monomial support as the first entry of the previous row. To leading order in `n` the two are proportional (ratio `≈ 5n²`), so the static system is degenerate at leading order. The rank information sits in subleading terms, which is why the elimination tree needed 181 steps.
- *The exceptional locus.* The tree's multiple-root leaves are the type-`(d−2,1,1)` points. There the static space is genuinely nonzero in every degree, while the dynamic core is finite.
- *The fix.* One application of `D` removes that locus. With the dynamic equation `T₃(H, {H, G}) = 0` added, the local system becomes **triangular in a weight grading**, and the elimination collapses to two determinants with closed forms in `(n, d, j)`.

**Theorem SR.** Let `H` be a form of degree `d ≥ 3` with a simple root, not of the form `cℓ^{d−1}m`. Then `S_n(H) = {G ∈ V_n : T₃(H, G) = 0, T₃(H, {H, G}) = 0}` is zero for all `n ≥ N₀(d)`. In particular `D∞(H)_n = 0` for `n ≥ N₀(d)`.

*Proof.*
1. *Normal form.* Move the simple root to `(1:0)`, scale, and shear: `H = q^{d−1}p + Σ_{j≥3} h_j q^{d−j}p^j`.
2. *Top.* By the monomial theorem (`b = 1`), `C₃` with at most one bracket kills no monomial `q^cp^e` with `e ≥ 2`. So `G = Σ g_t q^{n−t}p^t` has `(g₀, g₁) ≠ 0`.
3. *Weights.* Give `h_j` weight `j−1` and `g_t` weight `t`. The equations at output index `τ` are weighted homogeneous of weight `τ + 2`.
4. *Induction on `j`.* Assume `h₃ = … = h_{j−1} = 0`. Then the `T₃` recurrence gives `g₂ = … = g_{j−2} = 0`. The equations of weight `j−1` (and `j`) are linear in the unknowns `y = g_{j−1}`, `z = g_j` and `h_j`:
   - if `g₀ ≠ 0`, the pair (`T₃(H,G)`, `T₃(H,DG)`) in the unknowns `(y, h_jg₀)` has determinant `Δ₀ = −jn(d−2)(d−1)(j−2)²(j−1)²(d+n−3)·K₀`;
   - if `g₀ = 0`, the pair in `(z, h_jg₁)` has determinant `Δ₁ = −j²(d−2)(d−1)(d−n)(j−2)(j−1)²(d+n−3)·K₁`.
5. *Nonvanishing.* `K₀` and `K₁` are quadratics in `n` with leading coefficients `±3(dj + d − 4) ≠ 0`. So for `n ≥ N₀(d)` both determinants are nonzero, which forces `h_j = 0`.
6. *Conclusion.* By induction every `h_j = 0`, so `H = q^{d−1}p`, which is excluded. ∎

**Certificate.** The checker `check_simple_root.py` (`simple-root-rigidity-v1`; `results/hamiltonian/simple_root_rigidity.json`) does the following.
- It derives the four equations symbolically in `(n, d, j)` with its own polynomial arithmetic.
- It proves that no other contribution reaches the same output index for any integer `j ≥ 3`.
- It validates all 1000 coefficient values against direct operator arithmetic (`weyl_receipts`) on a product grid larger than the degrees.
- It verifies both factorizations and the leading coefficients of `K₀` and `K₁`.
- It tabulates `N₀(d)` exactly for `d ≤ 40`: `N₀ = 4, 5, 8, 11, 14, 19, 24, 29` for `d = 3, …, 10`, and `N₀(40) = 509`. The growth is roughly `d²/3`.

Direct computation confirms that `S_n(H) = 0` beyond `N₀(d)`, in fact everywhere except degrees 2 and `d`. The tested forms are `(4,1,1)` and `(1⁶)` in degree 6, and `(4,1,1,1,1)` and `(1⁸)` in degree 8.

**Main Theorem (root rigidity, all degrees).** Let `H` be a homogeneous binary form of degree `d ≥ 3` over a field of characteristic zero.
- If `H` has at least three distinct roots, then `D∞(H) = span{1, H}` and `𝒜(H) = 0`. No nonstationary polynomial observable evolves exactly under repeated Weyl–Moyal and classical evolution.
- If `H` has at most two distinct roots, `D∞(H)` is the monomial-class core of §5.1, and `𝒜(H) ≠ 0` unless `H` is a balanced power.

*Proof of the first part.*
- *If `H` has a simple root:* Theorem SR gives `D∞(H)_n = 0` for `n ≥ N₀(d)`. The chain argument of §3d then concludes: `H` is not a proper power, `H^j ∉ D∞` by the top-weight lemma at the simple root, and the sl₂ lemma excludes quadratics.
- *If `H` has no simple root:* every multiplicity is at least 2. With at least three roots, every multiplicity is at most `d − 4`, and not all can equal `d/2`. So some root has multiplicity `μ ∈ [2, d−2]` with `μ ≠ d/2`, and Theorem R1 applies. ∎

With Corollary P this gives `D∞(H) = span{1, H}` for **every** polynomial Hamiltonian whose top homogeneous part has at least three distinct roots. `check_root_rigidity.py` now routes every such `H` to SR or R1. No open stratum remains.

*A second route for `(d/2, 1^{d/2})`, recorded but not certified.* At the root of multiplicity `μ = d/2`, the top-weight lemma leaves a single coefficient `g₀`. The `T₃` and `T₅` equations then give `h_jg₀Φ_j(m) = 0` inductively, with `n = 2m` and
`Φ_j = −8jm(j−1)(j+1)(m−1)(m−μ)(2m+2μ−7)·Q(j,m,μ) / (T₃ recurrence coefficient)`.
The coefficients of `m³` and `m²` in `Q` vanish together only for `μ = 2` (or `μ = ½`).

### 5.3 Perturbation corollary

**Corollary P.** Let `H = H_d + P` with `deg P < d`. If `D∞(H_d) = span{1, H_d}`, then `D∞(H) = span{1, H}`.

*Proof.* Use the weight `(1,1)` in the top-weight lemma. The top part of any `G ∈ D∞(H)` lies in `span{1, H_d}`, so `G` has degree 0 or `d`. In degree `d`, `G − cH ∈ D∞(H)` has lower degree, so it is a constant. ∎

Combined with §§3c, 3d and 5.2, this covers every Hamiltonian whose top homogeneous part has at least three distinct roots and lies in a proved stratum. That includes perturbations that change the one-step exactness space, since lower terms of degree at least 3 change the gates.

**Executable coverage (`root-rigidity-v1`; checker `check_root_rigidity.py`).**
- Given a rational `H`, the certificate declares a square-free decomposition of `H_d(x, 1)`. The checker verifies the product, square-freeness and coprimality.
- It derives the root type over Q̄, including the root at `(1:0)`.
- It selects the route (monomial, R1, R2, R3, W3, W4 or open) and reports the core and the active part.
- Five examples are enveloped under `results/hamiltonian/rigidity_*.json`, including a squarefree octic, now covered by SR.
- The tests recover root types of random forms and reject forged decompositions. They also check that random lower-order perturbations of proved tops leave exactly `span{1, H}` in the direct computation.

### 5.4 Scope and positioning

The question here is different from theorems that ask when exactness holds for *every* observable, which force `H` to be quadratic. Here `H` is a fixed nonlinear Hamiltonian, and the object is its maximal polynomial sector of exact repeated evolution. Any priority claim would need a focused literature review. None is made.

On effective finite determination:
- For monomials, Theorem M gives an explicit stopping rule: `C₃` and depth 3.
- For R1–R3, the proofs give explicit static or one-step bounds. Examples are `n ≥ (d−1)(d−2) + 3` for R2 and `n ≥ 4` with one `D`-step for R3; below these bounds the chain argument applies.
- For homogeneous `H` the classification is now a decision procedure: compute the root type. Theorem SR also gives a stopping rule, one gate and one bracket beyond `N₀(d)`. A general decision procedure for arbitrary inhomogeneous `H` (top part with at most two roots) remains open. Operator-ideal certificates (§1) and classifications of polynomial solutions remain distinct claims.

## 6. Inhomogeneous Hamiltonians whose top part has at most two roots

Let `H = H_d + P` with `deg P < d`, where the top homogeneous part `H_d` has at most two distinct roots over Q̄. After §5, these are the only Hamiltonians whose core is not yet determined by the top part alone.

Two facts are used throughout:
- `D∞` is covariant under affine maps. Translations commute with the constant-coefficient operators `D` and `T_k`, and `GL₂` acts as in §3.
- The gates `C_k`, `k ≥ 3`, see only `H_{≥3}`. Quadratic and linear terms enter only through `D`.

Write `ℓ, m` for the root forms of `H_d`, or a root form and a complementary form, and let `v` be the direction with `∂_vℓ = 0`. Four top types occur:
- **pure:** `cℓ^d`;
- **near:** `cℓ^{d−1}m`;
- **balanced:** `cQ^{d/2}`;
- **unequal:** `cℓ^am^b` with `a > b ≥ 2`.

### 6.1 Unequal tops (complete)

**Theorem U.** Let `H_d = cℓ^am^b` with `a > b ≥ 2`. Let `τ` be the unique translation with `(H∘τ)_{d−1} = 0`.
- If `H∘τ ∈ ℓ^{a−b}K[ℓm] + Kℓm + K`, then `D∞(H) = span{1, H, G}` with `G = (ℓm)∘τ^{−1}`, and `𝒜(H) = K·G`.
- Otherwise `D∞(H) = span{1, H}`.

*Proof.*
1. *Three dimensions at most.* For the weight `(1,1)` the top part is `H_d`, whose core is `span{1, ℓm, H_d}` (Theorem M). So `dim D∞(H) ≤ 3`, and a third element must be a quadratic `G = ℓm + (linear) + c`.
2. *When the quadratic survives.* `span{1, H, G}` is killed by every gate: `G` has degree 2 and `T_k(H, H) = 0` for odd `k`. So `G ∈ D∞(H)` exactly when `{H, G} ∈ span{1, H, G}`.
3. *Normal form.* Translate so that `G = ℓm`, and use coordinates with `ℓ = q`, `m = p`. Then `ad_{qp}` multiplies `q^ip^j` by `i − j`. The condition says every monomial of `H` has `i − j = a − b`, unless it is `qp` or a constant. Such monomials of degree `d − 1` would need `2i = 2a − 1`, which is impossible, so the translation is the one that kills `H_{d−1}`. ∎

### 6.2 Positive structures (pure, near, balanced)

**Theorem P⁺.**
1. **Strip `W`.** For a pure top, if `∂_vH_{≥3} = 0` and `∂_v²H₂ = 0`, i.e. `H ∈ K[ℓ] + Kℓm + Km`, then `D∞(H) = W = ⊕_{j≤2} m^jK[ℓ]`.
2. **Affine strip `V`.** For a pure top outside case 1, or for a near top: if `∂_v²H = 0`, i.e. `H` is affine in `m`, then `D∞(H) = V = K[ℓ] ⊕ mK[ℓ]`.
3. **Stationary tower.** For a balanced top, if `H ∈ K[G]` for a quadratic `G` with leading part `Q`, then `D∞(H) = K[G]`, and every element is stationary.

*Proof.*
- *Containment `V ⊆ D∞(H)`.* In coordinates `(ℓ, m)`, a term of `T_k(H, G)` pairs `∂_m^aH` with `∂_m^bG`, where `a + b = k ≥ 3`, so it vanishes for `H, G` affine in `m`. Also `{H, V} ⊆ V`.
- *Containment `W ⊆ D∞(H)`.* `T_k(f(ℓ), G) ∝ f^{(k)}(ℓ)∂_m^kG = 0` on `W`. The brackets with `K[ℓ]`, `ℓ²`, `ℓm` and linear forms do not raise the `m`-degree.
- *Containment `K[G] ⊆ D∞(H)`.* After a translation `G = Q ≅ qp`, and `T_k((qp)^a, (qp)^c) ∝ ψ_k(c, c) = 0` by the antisymmetry of §5.1.
- *Equality in cases 1 and 3.* The top cores are `W` and `K[qp]` (Theorem M), and the line-core argument of §3b applies.
- *Equality in case 2.* Use the `m`-degree filtration. The `m`-top of `H` is `m·g(ℓ)` with `deg g ≥ 2`; outside case 1, `deg g ≤ 1` would put a pure top into case 1. The core of `m·g(ℓ)` is graded by `m`-degree, and its homogeneous elements `m^ku(ℓ)` have top `m^kℓ^{deg u}`. By Theorem M (near type) this forces `k ≤ 1`. So every element of `D∞(H)` has `m`-degree at most 1. ∎

### 6.3 The `m²`-perturbation families

**Theorem Q (near tops, all `d ≥ 3`).** Let `H_d = cℓ^{d−1}m`. If `∂_v²H` is a nonzero constant, i.e. `H = cℓ^{d−1}m + αm² + (terms affine in m)` with `α ≠ 0`, then `D∞(H) = span{1, H}`.

**Theorem Q′ (pure tops, all `d ≥ 3`).** Let `H_d = cℓ^d`. If `H = f(ℓ) + m·g(ℓ) + γm²` with `γ ≠ 0` and `deg g < d/2`, then `D∞(H) = span{1, H}`.

*Reduction.* For the weight `(d−1, 1)` on `(m, ℓ)` (Theorem Q), respectively `(2, d)` on `(ℓ, m)` (Theorem Q′), the top part is a binomial: `ℓ^{d−1}m + αm²`, respectively `ℓ^d + γm²`. The torus scales both binomials to `qp^{d−1} + q²` and `q^d + p²`. By the finite-top consequence of the top-weight lemma, it suffices to show that each binomial has core `span{1, F}`.

*`F = q^d + p²`, all `d ≥ 3`.*
1. The static space of `q^d` is `W`. Write `D₁ = {q^d, ·}` and `D₂ = {p², ·} : q^ip^j ↦ −2iq^{i−1}p^{j+1}`.
2. For `u ∈ D∞(F)`:
   - `Du ∈ W` forces the `p²`-part of `u` to be a multiple of `p²`;
   - applying the same to `Du` forces the `p`-part into `span{p, qp}`;
   - applying it once more forces the `p⁰`-part into `span{1, q, q²} + Kq^d`, with the `q^d` coefficient equal to the `p²` coefficient.
3. So `u ∈ KF + (degree ≤ 2)`. One or two more applications of `D` kill the quadratic part: compare the coefficients of `q^d` and `p²`, which must agree in multiples of `F`, giving `(d+2)b = 0`. For `d = 3` this takes four steps. ∎

*`F = qp^{d−1} + q²`, `d ≥ 5`.*
1. *Static space.* The gates are those of `qp^{d−1}`. Their kernel is `V ⊕ Kq² ⊕ Kq³p^{(d−3)/3}`, where the last term is present only if `3 | d`. The checks of `T₃` and `T₅` exclude every monomial with `q`-exponent at least 4.
2. *Weight grading.* `F` is homogeneous for the weight `(d−1, 1)`, so `D∞(F)` is spanned by weight-homogeneous elements. In weight `W` the candidates are `x p^W + y qp^{W−d+1} + z q² + t q³p^c`.
3. *First constraints.* Requiring `DG` and `D²G` to stay in the static space forces `t = 0`, `y = 0` outside the weights `d−1, d, 2d−2`, and `y = z` in weight `2d−2`.
4. *Exceptional weights.* The remaining weights `1, 2, d−1, d, 2d−2` reduce to each other along the `D`-chain and end in `G ∈ span{1, F}`. ∎

*Certificates for small `d`.* The binomials not covered by these arguments, and two cross-checks, are certified with the Gröbner engine. Each gives core `span{1, F}`:
- `qp²+q²` (d = 3) and `q⁴+p²`;
- `qp³+q²` (d = 4), already in W2;
- `qp⁴+q²` and `q⁵+p²`, cross-checks of the general arguments;
- `p³+q²` (d = 3, Q′), retained.

### 6.5 Balanced tops (complete)

**Theorem B.** Let `H_d = cQ^μ` with `Q` a nondegenerate quadratic form and `d = 2μ ≥ 4`. Then `D∞(H) = K[G]` if `H ∈ K[G]` for a quadratic `G` with leading part `Q`, and `D∞(H) = span{1, H}` otherwise.

*Proof.*
1. *Setup.* Work over Q̄ with `H_d = (qp)^μ`. If `D∞(H) ≠ span{1, H}`, there is `G ∈ D∞(H)` with top `(qp)^s`, `1 ≤ s < μ`; subtract multiples of `H` to arrange this. Translate `H` so that `H_{d−1}` has no `q^μp^{μ−1}` and no `q^{μ−1}p^μ` term. This is possible because a translation adds `μ(qp)^{μ−1}(x₀p + y₀q)`.
2. *Weights.* Give `H_{d−k}` and `G_{2s−k}` weight `k`. A monomial `q^xp^y` is *diagonal* if `x = y`. Diagonal forms Poisson-commute and have zero odd transvectants with each other.
3. *Induction on the weight.* Assume the off-diagonal parts vanish below weight `k`. Then only `(H_d, Y)` and `(X, (qp)^s)` contribute at weight `k`, where `X` and `Y` are the off-diagonal parts of `H_{d−k}` and `G_{2s−k}`.
   - *The bracket.* `{H, G}` has nothing below weight `k`, so its weight-`k` component is its top and must be diagonal. But that component is off-diagonal, since `ad_{qp}` acts diagonally on monomials. So it vanishes, which gives `Y = (s/μ)(qp)^{s−μ}X` monomial by monomial.
   - *The gate.* The `T₃` equation then multiplies each off-diagonal monomial of `X` by `Ω = s(s−μ)(x−y)·R`, where, with `u = x−y` and `k = 2μ−(x+y)`,
     `R = A(s+μ) − (3/2)(u² + k² + 2k − 4)`,  `A = u² + 3k − 4`.
4. *Nonvanishing.* The index conditions give `s, μ ≥ (k+|u|)/2`. With `a = |u|`,
   `2A(k+a) − 3(u² + k² + 2k − 4) = (a−1)(2a−1)(a+1) + (k−1)(2a² + 6a + 3k − 11) > 0` unless `a = k = 1`.
   So `R ≠ 0`, except on the two translation monomials, which step 1 removed. Hence `X = 0` at every weight.
5. *Conclusion.* After the translation, `H ∈ K[qp]`. ∎

Only the gate `T₃` and the top of one bracket are used. The argument does not depend on Newton polygons, so it covers the "box" perturbations `i, j ≤ μ` that the weight method of §6.3 could not reach. The checker `check_balanced.py` (`balanced-top-v1`; `results/hamiltonian/balanced_top_theorem.json`) verifies the factorization of `Ω`, the positivity identity and the antisymmetry exactly. It also checks the `T₃` convention against `weyl_receipts` on a grid. `check_two_root.py` now reports balanced tops outside `K[G]` as proved (route `B`).

### 6.4 The decision procedure and what remains open

`check_two_root.py` (`two-root-perturbation-v1`) decides, for any rational `H` with a two-root top:
- it recomputes the top type from a verified square-free decomposition;
- it solves for the translation `τ` exactly and tests the normal forms;
- it reports the core, the active part, and whether the answer is proved (Theorems U, P⁺, Q, Q′) or conjectural.

Enveloped examples are `results/hamiltonian/tworoot_*.json` and `binomial_*.json`.

The tests generate random members of every route and random affine changes of coordinates (degrees 3–5 in the suite; degrees 3–6 at depth 10 in a longer run). Each is compared with direct dimensions of `{G : deg G ≤ d+1, C_kD^rG = 0, r ≤ 8}`. Depth matters: with three gates the qp³+q² family shows spurious extra elements, and one Q′ instance needs depth 8.

**Conjecture (two-root tops).** Let `H_d` be pure, near or balanced, and suppose `H` has none of the structures of Theorem P⁺. Then `D∞(H) = span{1, H}`.

Theorem B (§6.5) proves it for every balanced top, and Theorems Q and Q′ prove it for the `m²` families. What remains open is pure and near tops whose non-affine part is not a single `m²` term. The conjecture is supported by every computed case, including random perturbations with cubic terms.

With §5 this gives a complete statement of when **active** exact dynamics survives a lower-order perturbation, conditional only on the conjecture above:
- three or more roots in the top: never (proved);
- unequal top: a single active quadratic `G`, exactly in the normal form of Theorem U (proved);
- pure or near top: an infinite active sector exactly in the affine or strip structures of Theorem P⁺ (proved);
- balanced top: never (proved, Theorem B).

## 4. Commands

```bash
python3 -B extensions/hamiltonian/weyl_groebner.py discover "q*p^3+q^2+p^2" --output R.json
python3 -B extensions/hamiltonian/weyl_kernel.py R.json --output K.json
python3 -B extensions/hamiltonian/check_weyl_kernel.py K.json
python3 -B extensions/envelope.py check results/hamiltonian/qp3_plus_q2_plus_p2.json.gz
python3 -B -m unittest test_weyl_discovery      # from extensions/hamiltonian
```

Measured on the development container: `qp³+q²+p²` takes about 80 s for discovery and about 2 min for classification, most of it replaying the 13-generator receipt. The other rows take seconds.
