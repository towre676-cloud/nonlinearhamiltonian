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

Let `H = H_d + P` with `deg P < d`, where the top homogeneous part `H_d` has at most two distinct roots over Q̄. After §5, these are the only Hamiltonians whose core is not yet determined by the top part alone. For pure tops, §6.8 shows that lower-order terms can also create structure that only non-affine triangular coordinates reveal.

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

### 6.6 Near and pure tops: finiteness reductions (partial)

Use coordinates `(ℓ, m)`, and write `H = Σ_c m^c h_c(ℓ)`. Let `s` be the `m`-degree of `H`, and call `F = m^sφ(ℓ)` the *transverse top*. Outside Theorem P⁺, `s ≥ 2`.

**Lemma F (near tops).** If `H_d = cℓ^{d−1}m` and `D∞(H)` is finite-dimensional, then `D∞(H) = span{1, H}` unless `H` is affine in `m`.

*Proof.*
1. Tops lie in `V`, and `D_{H_d}` maps the top monomials `ℓ^N ↦ Nℓ^{N+d−2}` and `mℓ^{N−1} ↦ (N−d)mℓ^{N+d−3}`.
2. An element whose top has an `ℓ^N` part (`N ≥ 1`), or an `mℓ^{N−1}` part with `N ∉ {2, d}`, therefore generates elements of unbounded degree. So a finite core lies in `span{1, H, G₂}` with `G₂ = ℓm + (linear)`.
3. `G₂ ∈ D∞(H)` forces `{H, G₂} ∈ span{1, H, G₂}`. As in Theorem U, after a translation `H` becomes a weight vector of `ad_{ℓm}` modulo `span{1, ℓm}`. For the near top this means `H = ℓ^{d−1}m + cℓ^{d−2} + γℓm + δ`, which is affine in `m`. ∎

**Theorem T (transverse top).** Suppose `deg φ ≥ 2` and:
- for a near top, `F ∉ K[G]`, i.e. `F` is not of the form `c(m(ℓ+γ))^s`;
- for a pure top, `φ` is not a perfect power `c(ℓ+γ)^{deg φ}`.

Then `D∞(H) = span{1, H}`.

*Proof.*
1. *Finiteness.* For the `m`-degree filtration, `m`-tops of core elements lie in `D∞(F)`.
   - If `deg φ ≠ s`, then `F` has an unequal top and `dim D∞(F) ≤ 3` by Theorem U.
   - If `deg φ = s`, then `D∞(F) = span{1, F}` by Theorem B.
   Either way `D∞(H)` is finite-dimensional.
2. *Near tops.* Lemma F concludes.
3. *Pure tops.*
   - The translation normalizing `F` moves only `ℓ`. So `D∞(F)` contains a quadratic exactly when `φ` is a perfect power, and that quadratic is `m(ℓ+γ)`. Under the hypothesis, `D∞(F) = span{1, F}`.
   - The `m`-tops of core elements are therefore constants or multiples of `F`. After subtracting `cH`, a core element `u` lies in `K[ℓ]`.
   - Then `{H, u} ∈ D∞(H) ⊆ KH ⊕ K[ℓ]`. Its `m^s` part vanishes, so the `H`-coefficient is 0. Its `m^{s−1}` part `±sφu'm^{s−1}` must then vanish, so `u' = 0`. ∎

*Pure tops with `φ` a perfect power, `deg φ ≥ 2`, are not covered.* There `D∞(F)` contains the `m`-homogeneous quadratic `m(ℓ+γ)`, and the reduction above does not exclude core elements `u(ℓ) + κm(ℓ+γ)` with `κ ≠ 0`. A complete treatment needs the next `m`-degree components of `H`. Such elements do occur: see family K3 in §6.8.

**Theorem N (near tops, unequal vertex).** If the Newton polygon of `H` in `(m, ℓ)` has a vertex `m^iℓ^j` with `i, j ≥ 2` and `i ≠ j`, strictly between the total-degree direction and the `m`-degree direction, then `D∞(H) = span{1, H}`.

*Proof.* For the weight that singles out this vertex, the top part is an unequal monomial, whose core has dimension 3 (Theorem M). So `D∞(H)` is finite, and Lemma F concludes. ∎

`check_two_root.py` applies T and N, with exact Newton-polygon vertices (routes `T`, `N`). The tests compare both routes with direct computation.

**What remains open.** Every remaining case has a transverse top `F` with `deg φ ≤ 1`, or `F ∈ K[G]` (near), or `φ` a perfect power (pure), and, for near tops, no unequal Newton-polygon vertex; Theorems Q and Q′ cover the parts of this with a single `m²` term. In random perturbations this is the typical situation. The polygon is then a single edge from the top vertex to `m^A` or `m^Aℓ`. The missing ingredient is a finiteness theorem for these quasi-homogeneous edge polynomials. The binomial `ℓ^{d−1}m + m²` of Theorem Q is the first instance, and its proof by casework in the weight grading suggests the general method.

### 6.7 Near tops (complete): edge finiteness from the top vertex

**Theorem NE.** If `H_d = cℓ^{d−1}m` and `H` is not affine in `m`, then `D∞(H) = span{1, H}`.

*Proof.*
1. *First edge.* In coordinates `(m, ℓ)`, decrease `t` in the weights `w_t = (1, t)` from 1. The top vertex `mℓ^{d−1}` is first tied by monomials of `m`-exponent at least 2; monomials of `m`-exponent at most 1 lie strictly inside. This gives the first Newton-polygon edge
   `E = mℓ^{d−1} + Σ_{s≥1} e_s m^{1+sa}ℓ^{d−1−sb}`,
   with step `(a, −b)`, `b > a ≥ 1` coprime, because the total degree drops along the edge.
2. *Reduction.* By the top-weight lemma for the edge weight, `gr D∞(H)` embeds in `D∞(E)`. Once `D∞(E)` is finite-dimensional, Lemma F gives `span{1, H}`.
3. *The top end.* Let `G` be a weight-homogeneous element of `D∞(E)` of large degree. By Theorem M its top is `gℓ^N` (type α) or `gmℓ^{N−1}` (type β), and its monomials lie on a line of step `(a, −b)`. Let `t` be the first step with `e_t ≠ 0`. The `T₃` recurrence clears the coefficients between steps 0 and `t`. The step-`t` components of `T₃(E, G)` and `T₃(E, {E, G})` are then linear in `(y, e_tg)`, where `y` is the step-`t` coefficient:
   - **[E1] type α:** the determinant is `N a²t²(d−2)(d−1)(at−1)²(at+1)·C_α`. Here `C_α` is cubic in `N` with leading coefficient `3(at(d−1) + bt + 2d − 4) > 0`.
   - **[E2] type β:** the determinant is `a²t²(d−N)(d−2)(d−1)(at+1)²·C_β`. The `N³` coefficient of `C_β` is `−3(at−1)(at(d−1) + bt + 2d − 4)`. For `at = 1` the determinant is `36(d−N)(b−1)(d−2)(d−1)·C′_β`, where the `N²` coefficient of `C′_β` is `−(b+d−1)`.
   - **[E3] type α with `a = t = 1`,** the only degenerate case: the first perturbation `m²ℓ^{d−1−b}` is invisible at first order, exactly as in the `m²` families. At step 2 the components of `T₃(E, D^rG)`, `r = 0..3`, are linear in `(y₂, e₁y₁, e₂g, e₁²g)`. The 4×4 determinant is
     `10368 N²(b−1)³(d−2)²(d−1)(N+d−2)(b+d−1)(b+d−1−N)·Q`,
     where `Q` is quartic in `N` with leading coefficient `−[2b³ + b²(7d−8) + 2b(4d−5)(d−1) + (d−1)²(3d−4)] < 0`. Hence `e₁²g = 0`, and so `g = 0`.
4. *Conclusion.* In every case `g = 0`, which contradicts the choice of the top. So the homogeneous elements of `D∞(E)` have bounded degree, and `D∞(E)` is finite-dimensional. ∎

**What the sextic certificate revealed.** The mechanism is local at the top vertex of the first edge. First order fails only for perturbations of transverse degree 2; second order succeeds there; no case analysis of the far end is needed. The far-end analysis (`mᴬℓ`, `mᴬ`, `(mℓ)^c`) gives the same finiteness for most edges, but it is not needed.

**Certificate.** `check_near_edges.py` (`near-edge-v1`; `results/hamiltonian/near_edge_theorem.json`) recomputes all four determinants with its own polynomial arithmetic in the symbols `(N, d, a, b, t)`. It verifies the stated factorizations by exact division, checks the leading coefficients, and validates the gate and bracket conventions against `weyl_receipts`. `check_two_root.py` now reports every non-affine near top as proved (route `NE`). Theorems Q and T for near tops become special cases. Random near-top Hamiltonians agree with direct computation.

**Pure tops: status of the same method.** For a pure top `ℓᵈ` the core of the top vertex is `W`, so a weight-homogeneous element starts with one of three types: `ℓᴺ`, `mℓ^{N−1}` or `m²ℓ^{N−2}`. The first-order top-end determinants were computed symbolically. Let `u = at` be the `m`-degree of the first perturbation on the first edge.
- All three types close for `u ≥ 4`. For type 0 the factor is `(u−3)(u−2)²(u−1)²`; for type 2 the leading coefficient is `−(u−2)(u−3)`.
- The low cases `u ∈ {1, 2, 3}` need second-order analysis, as `u = 1` did for near tops.

Two further gaps remain:
- **Finiteness does not yet give span{1, H}.** For pure tops, `D_{ℓᵈ}` lowers the `m`-degree of tops instead of making them grow, so Lemma F does not transfer.
- **An affine first edge gives no finiteness.** When the first edge from `ℓᵈ` is `ℓᵈ + cmℓʲ`, finiteness must come from the next edge, a near-type edge from `mℓʲ`. The argument above gives finiteness there.

These three points were the remaining work for pure tops. §6.8 shows why they cannot all be closed: the pure-top conjecture is false, and the failures are exactly the triangular families found there.

### 6.8 Pure tops: the conjecture is false as stated; triangular structures

The pure-top part of the two-root conjecture of §6.4 is **false**. The smallest counterexample is `H = (q³ + p)²`. It is a pure top `q⁶` that lies outside Theorems P⁺, Q′ and T, yet
`D∞(H) ⊇ span{1, q, q², q³ + p, q(q³ + p), (q³ + p)²}`,
which has dimension 6. This containment is exact: the span is `D`-invariant and every gate kills it. Direct computation at depth 10 finds exactly this span up to degree 11. The extra elements come from **triangular coordinates** `(Q, P) = (q, p + w(q))`. This map is symplectic but not affine, so the flat gates are not covariant under it, and Theorem P⁺ does not see these structures.

**Theorem X (triangular transvectant formula).** Write `f̃ = f∘τ` with `τ(q, p) = (q, p + w(q))`. Then
`Σ_k (tᵏ/k!) T_k(h̃, g̃)∘τ⁻¹ = exp( t(∂_{Q₁}∂_{P₂} − ∂_{P₁}∂_{Q₂}) + Σ_{j≥2} tʲ (w⁽ʲ⁾(Q)/j!)(∂_{P₁}∂_{P₂}ʲ + (−1)ʲ∂_{P₁}ʲ∂_{P₂}) ) h(1)g(2)`
on the diagonal. The coefficients `w⁽ʲ⁾(Q)` are frozen, i.e. not differentiated.

*Proof.*
1. Take `h = e^{δQ+αP}` and `g = e^{γQ+βP}`. The `p`-derivatives act as `α` and `β`, so `T_k` becomes `(β∂_{q₁} − α∂_{q₂})ᵏ` on the diagonal. This is the `k`-th `t`-derivative along the line `(q + tβ, q − tα)`.
2. Along that line the exponent is `t(δβ − γα) + α[w(q+tβ) − w(q)] + β[w(q−tα) − w(q)]`, and its `t`-linear `w`-terms cancel.
3. Both sides are bilinear differential operators that agree on exponentials, so they agree on polynomials. ∎

The flat part is the usual one. The **correction** `Φ` collects the terms `j ≥ 2`. For `deg w = 2` it is `c t²∂_{P₁}∂_{P₂}(∂_{P₁}+∂_{P₂})`, which is even in `t`.

**Theorem K (triangular families; containments proved).** Let `P = p + w(q)` and `Q = q`. Each statement holds up to affine changes of coordinates.
- **K1** (`deg w = 2`). If `H = F(P) + λQ`, then `K[P] + KQ ⊆ D∞(H)`.
  - *Proof.* The correction is even in `t`, and the flat part vanishes on `K[P] × K[P]`. So `T_k(F(P), G(P)) = 0` for every odd `k`. `Q` is linear. Finally, `{H, Pⁿ} = λnPⁿ⁻¹` and `{H, Q} = −F′(P)`. ∎
- **K1′** (`deg w = 2`). If `H = F(P) + λQ + μQP` with `μ ≠ 0` and `deg F ≥ 3`, normalized so that `F` has no `P^{deg F − 1}` term, then `span{1, P, P², H} ⊆ D∞(H)`. If `deg F = 3`, the span also contains `Q`, and if in addition `λ = 0`, it contains `PH`.
  - *Proof.* The gates of `F(P)` vanish on `K[P]` as in K1, and `Q` is linear. In Theorem X, the factor `QP` absorbs at most one `∂_Q` and one `∂_P`. So every odd term of `T_k(QP, g)`, `k ≥ 3`, with `g ∈ K[P]` is `∂_{Q₁}∂_{P₂}·∂_{P₁}∂_{P₂}²`. It differentiates `g` three times in `P`, and so vanishes for `g ∈ span{1, P, P²}`.
  - The brackets are `{H, P} = λ + μP` and, for `deg F = 3`, `{H, Q} = −F′(P) − μQ`, which lies in the span.
  - For `PH`, take `H = P³ + aP + b + μQP`. Then `T_k(H, PH)` is bilinear, so it has degree at most 2 in each of `μ`, `a` and `b`. It depends on `w` only through `c = w″/2`, also with degree at most 2. The checker verifies the identity on a 3⁴ tensor grid, which proves it for all values. ∎
- **K2** (any `w`). If `H = h(Q, P)` with `h` quadratic, then `τ*K[Q, P]_{≤2} = span{1, Q, Q², P, QP, P²} ⊆ D∞(H)`.
  - *Proof.* In the coefficient of `tᵏ`, `k ≥ 3`, every term of Theorem X has total derivative order at least `k + 1 ≥ 4`. Split over two quadratics, some factor is differentiated three times; this includes the order-4 term `t³(∂_{P₁}∂_{P₂}³ − ∂_{P₁}³∂_{P₂})`. Brackets of quadratics are quadratic. ∎
- **K3** (twisted squares, `m`-degree 2). Let `Q = ℓ − γ`, `G = Qm + v(ℓ)` with `v` any polynomial, and `k ≥ 1`. Suppose `H = cQ^{k−2}G² + r` is a polynomial, where:
  - for `k ≥ 2`, `r ∈ span{1, Q^{k−2}}`;
  - for `k = 1`, `r` is rational with `Qr` of degree at most 2.

  Then `span{1, G, H} ⊆ D∞(H)` (for `k ≥ 2`), respectively `span{1, Q, G, H} ⊆ D∞(H)` (for `k = 1`).
  - *Proof.* `G` is affine in `m` with a linear `m`-coefficient. Hence `T_j(G, f) = v⁽ʲ⁾∂_mʲf` for `j ≥ 3`, which vanishes on `H` because `H` has `m`-degree 2. The brackets `{H, G} = (k−2)c(H − r) + Qr′` and `{H, Q} = −2cQ^{k−1}G` close the span under the conditions on `r`. ∎

The transverse tops of these families are exactly the cases that Theorem T leaves out:
- K1, K1′ and K2 have `φ` constant. K2 has `deg w = d/2`, the boundary that Q′ excludes; K1 and K1′ have `deg w = 2`.
- K3 has `φ = c(ℓ−γ)ᵏ`. This is linear (`k = 1`) or a perfect power (`k ≥ 2`).

The element `G = (ℓ−γ)m + v` is the quadratic-like element anticipated in §6.6.

**Active dynamics also survives.** In K1 with `λ ≠ 0`, `D` maps `Pⁿ ↦ λnPⁿ⁻¹`, so `𝒜(H)` is infinite-dimensional. Examples are `(q² + p)³ + q` and `(q² + p)³ − 2(q² + p) + q`. So the statement in §6.4 that pure tops have an infinite active sector only in the structures of Theorem P⁺ is false. In K2 and K3 the active part is nonzero but finite: `Q`, `QP` or `G` move under `D`.

**Conjectured cores.** Write `e = deg w`.

| family | conjectured `D∞(H)` | direct check |
|---|---|---|
| K1, `deg F ≥ 3` | `K[P] + KQ` (proved, §6.10) | `(q²+p)³+q`: 8 = 8 up to degree 12 |
| K1 ∩ K2 (`e = 2`, `h = cP² + λQ + μ`) | `K[P] + τ*K[Q,P]_{≤2}` | `(q²+p)²`: 9 = 9 up to degree 11 |
| K1′, `deg F ≥ 4` | `span{1, P, P², H}` | `(q²+p)⁴ − q(q²+p)`, with or without `+ q`: 4 = 4 up to degree 11 |
| K1′, `deg F = 3` | `span{1, Q, P, P², H}`, plus `PH` if `λ = 0` | `(q²+p)³ + q(q²+p)`: 6 = 6 up to degree 12 |
| K2 otherwise | `τ*K[Q,P]_{≤2}` (dimension 6) | `(q³+p)²`: 6 = 6 up to degree 11 |
| K3, `k = 1` | `span{1, Q, G, H}` | `q(p+q²)²+q`: 4 = 4 up to degree 11 |
| K3, `k ≥ 2` | `span{1, G, H}` | `q³(p+q²)²+q`: 3 = 3 up to degree 11 |

**The cubic-phase case is richer.** Suppose the transverse top is constant and the completed power `w` has degree 2. Then `τ` is implemented by the cubic phase `exp(icq̂³/ħ)`. By Theorem X the gates in `(Q, P)` are the flat gates deformed by the single even term `ct²∂_{P₁}∂_{P₂}(∂_{P₁}+∂_{P₂})`. In this case the families above are not exhaustive. (§6.9 develops this case. It gives a gauge form, a Witt-cocycle obstruction and the family K4, and it classifies the sector affine in `Q` inside `τ*V`.) For example, `H = P²(P² + Q)` with `P = p + q²` has
`D∞(H) ⊇ span{1, P(P² + Q), H}`
by direct computation up to degree 11. Classifying this case is a separate problem: the core is the largest `D`-invariant subspace killed by the deformed gates, and the flat cores of `h` in `(Q, P)` are the natural candidates. In the random searches the generic cubic-phase Hamiltonian still has core `span{1, H}`, e.g. `(q²+p)³ + q²`.

**Conjecture P004 (pure tops, corrected).** Let `H_d = cℓᵈ`. Suppose:
- `H` lies outside the structures of Theorem P⁺;
- after an affine change of coordinates, `H` lies outside K1, K1′, K2 and K3;
- `H` is not in the cubic-phase case, unless `h` is affine in `Q` and outside K4 (§6.9).

Then `D∞(H) = span{1, H}`. In the families, `D∞(H)` is the span in the table above.

*Evidence.*
- *Random searches.* About 330 random pure tops of degree 4–8 were drawn: triangular normal forms with `m`-degree 2, 3 and 4, transverse tops `φ ∈ {1, ℓ, ℓ², ℓ³, ℓ+1}`, and random lower terms. Every Hamiltonian with a core larger than `span{1, H}` lies in K1, K1′, K2 or K3, with the predicted dimension. K1′ was found when these samples were rechecked.
- *Structured grid.* `F ∈ {P³, P³ + P, P⁴}` was combined with up to two of the terms `Q, QP, Q², QP², Q²P, Q³`, for `e = 2` and `e = 3`, giving 110 Hamiltonians. All match, except `P⁴ + QP²` with `e = 2`, the cubic-phase example above.
- *Near misses.* Each of the following has core `span{1, H}`:
  - `(q³+p)³`, where K1 needs `e = 2`;
  - `(q²+p)³ + q²`, which is a cubic-phase case;
  - `(q³+p)² + q³`;
  - `q(p+q²)² + q²`;
  - `q²(p+q²)² + q`.
- *Proved part of the classification.* Theorem P⁺ gives the strips. For `m`-degree 2 with constant `φ`, Theorem Q′ covers `deg w < d/2`, and K2 sits at `deg w = d/2`. Theorem T gives `span{1, H}` when `φ` has degree at least 2 and is not a perfect power. What remains open:
- the upper bounds in the families;
- `span{1, H}` for pure tops with `φ` constant, linear or a perfect power outside the families;
- the classification of the cubic-phase case.

**Certificate.** `check_triangular.py` (`triangular-pure-v1`; `results/hamiltonian/triangular_theorem.json`) checks the following:
- **[X1]** Theorem X against `weyl_receipts` on a grid of random `h`, `g` and `w`, for `k ≤ 7`. With the correction removed the check fails.
- **[K1], [K1′], [K2], [K3]** The families on random grids. Each check is exact: the stated span is `D`-invariant and killed by every gate. For K1 the tower is truncated at `P⁶`.

`detect` recognises the families for any pure top. It works in the root coordinates `(ℓ, m)`, reads the transverse top and completes the square or `s`-th power. `certify` records explicit generators, and `check` re-verifies them exactly: they must be independent, `D`-invariant, killed by every gate, and more than two. The enveloped counterexamples are `results/hamiltonian/triangular_*.json`. `check_two_root.py` reports these Hamiltonians on routes `K1`, `K1'`, `K2`, `K1+K2` and `K3`. For these routes the stated span is proved to lie in the core, and equality is marked conjectural. Other cubic-phase Hamiltonians go to the route `pure, cubic phase`, whose core is reported as open. The tests compare every route, including random affine images, with direct computation up to degree `d + 2` at depth 8.

### 6.9 The cubic phase: gauge form, a Witt-cocycle obstruction and the affine sector

Suppose the transverse top is constant and the completed power `w` has degree 2. Write `c = w″/2`, `P = p + w(q)` and `Q = q`. In this case the correction in Theorem X has a single term. That term is a coboundary, because `xy(x+y) = ((x+y)³ − x³ − y³)/3`.

**Theorem G (gauge form).** Let `S_s = exp(s∂_P³)` and `s = ct²/3`. Then
`Σ_k (tᵏ/k!) T_k(h̃, g̃)∘τ⁻¹ = S_s[ Σ_a (tᵃ/a!) T^flat_a(S_{−s}h, S_{−s}g) ]`,
where `T^flat` are the flat transvectants in `(Q, P)`.

*Proof.* By the identity above, `exp(ct²∂_{P₁}∂_{P₂}(∂_{P₁}+∂_{P₂}))` on the diagonal equals `S_s∘mult∘(S_{−s}⊗S_{−s})`. The flat operator has constant coefficients and commutes with this. ∎

So the cubic phase is the flat problem, conjugated by the `ħ`-dependent operator `exp(cħ²∂_P³/3)`; here `t` plays the role of `ħ`. `S_s` is even in `t`. Hence `G` is killed by every gate of `H̃` exactly when, as series in `t`,
`flat-odd(S_{−s}h, S_{−s}g) = t·S_{−s}{h, g}`.

**Theorem A₀ (affine criterion).** Let `h = a(P) + Qb(P)` and `g = α(P) + Qβ(P)` be affine in `Q`. Their flat odd part is `t{·,·}`. Therefore `T_k(h̃, g̃) = 0` for all odd `k ≥ 3` if and only if `S_s{S_{−s}h, S_{−s}g} = {h, g}` for all `s`. This is in turn equivalent to `Δ(S_sh, S_sg) = 0` for all `s`, where `Δ(X, Y) = ∂³{X, Y} − {∂³X, Y} − {X, ∂³Y}`.

On functions affine in `Q` the bracket is
`{X, Y} = (bα′ − a′β) + Q(bβ′ − b′β)`.
This is the Witt algebra of vector fields `b∂_P` acting on functions. In these terms
- `Δ_Witt = 3(b′β‴ − b‴β′)`;
- `Δ_fun = 3(b′α‴ + b″α″ − a‴β′ − a″β″)`.

`Δ_Witt` is the density of the Gelfand–Fuchs cocycle. The obstruction to exactness in the cubic phase is therefore the failure of `∂³` to be a derivation of the Witt algebra. On `sl₂ = span{1, P, P²}` that failure vanishes. For `b, β ∈ sl₂` the all-order condition reduces to two conditions:
- `b′α″ − β′a″ ∈ K`;
- `deg(b″α − β″a) ≤ 4`.

**Lemma W (Witt obstruction).** If `deg b ≥ 3`, every element of `D∞(H̃)` that is affine in `Q` lies in `span{1, H̃}`.

*Proof.*
1. `Δ_Witt = 0` gives `b′β″ − b″β′ = κ`. So `β′ = b′(λ + κ∫b′⁻²)`, which is a polynomial only for `κ = 0`, because `b′⁻²` decays faster than `1/P`.
2. So `β′ = λb′`. Subtract `λh`.
3. Then `Δ_fun = 3(b′α″)′ = 0` forces `b′α″ ∈ K`, hence `α″ = 0`, and `g ∈ span{1, P, Q}`.
4. `{H, P} = b` and `{H, Q} = −a′ − Qb′` leave that span. ∎

**Theorem K4 (twisted quartic).** Let `b = μ(P−r)(P−r′)` and
`a = A(P−r)³(P−r′) + c₂(P−r)² + c₁(P−r) + c₀`, with `Aμ ≠ 0`, and `h = a + Qb`. Then
`G = A(P−r)³ + c₂(P−r) + μQ(P−r)`
satisfies `{H, G} = −μ(H + (r′−r)G) + const`, and `span{1, G, H} ⊆ D∞(H̃)`.

In the normal form, where `a` has no `P³` term, the condition is `r′ = −3r`:
`h = AP⁴ + (degree ≤ 2 in P) + μQ(P−r)(P+3r)`.
The case `r = 0` is `P²(P² + Q)`, the exception of §6.8.

*Proof.* Centre at `r`.
- `b` and `β = μ(P−r)` lie in `sl₂`, so `Δ_Witt = 0`.
- `b′α″ − β′a″ = −2μc₂` is constant.
- `S_s` adds only terms of degree at most 1 in `P`, and `Δ` vanishes on them.
- The bracket is a direct computation. ∎

**Theorem A (the affine sector inside `τ*V`, `V = K[P] + QK[P]`).** Let `h = a + Qb` with `deg a = f ≥ 3`. Then `D∞(H̃) ∩ τ*V` is as follows.

| `b` | `D∞(H̃) ∩ τ*V` |
|---|---|
| constant | `K[P] + KQ` (K1) |
| linear, root `r` | `span{1, P, P², H}`; plus `Q` if `f = 3`; plus `(P−r)H` if `f = 3` and `a = A(P−r)³ + O(P−r)`; in the normal form this means `r = 0` (K1′) |
| quadratic | `span{1, G, H}` if K4 holds, otherwise `span{1, H}` |
| degree ≥ 3 | `span{1, H}` (Lemma W) |

*Proof.*
1. *`b` constant.* The first-order condition `(a″β′)′ = 0` gives `β′ = 0`. Every `α + β₀Q` passes, and `K[P] + KQ` is `D`-invariant.
2. *`b ∈ sl₂` nonconstant.* Then `β ∈ sl₂`, and the two conditions above apply.
   - Elements with `β = 0` are the constants when `b` is quadratic, and `span{1, P, P²}` when `b` is linear.
   - The `Witt` projection of `D∞ ∩ τ*V` is an `ad_b`-invariant subspace of `sl₂` that contains `b`. The invariant subspaces are solved one by one.
3. *`b` linear, root 0.*
   - For `β = 1`: `Pα′ + α − a′ ∈ span{1, P, P²}`, so `f = 3`.
   - For `β = P²`: `Pα′ − α − a′P²` has `Pⁱ⁺¹`-coefficient `i(i−3)aᵢ/(i+1)`. So `a₂ = a₄ = 0`, and hence `f = 3`.
4. *`b = P²`.* After subtracting `h`, `β` is linear, and `deg α ≤ 4`.
   - If `B = span{P², P}`, closure gives `α = (a − a₀ − a₁P)/P + x₀`. The first condition then becomes `Pα̃″ − 2α̃′ ∈ K`, which forces `a ∈ span{1, P, P², P⁴}`.
   - `B = sl₂` would need `f = 2`.
5. *Distinct roots, normalized to `b = P² − 1`.* The invariant subspaces are spanned by `b` and the eigenvectors `(P∓1)²` of `ad_b`.
   - The eigen-element equation is the ODE `bα′ − 2α = a′(P−1)² + const`. Its polynomial solutions, together with the two conditions above, give `f = 4` and `a₃ = −2a₄`. This is K4 with `r = 1`, `r′ = −1`; the computation was done exactly for `f = 3, 4, 5`, and the second condition rules out `f > 5`.
   - Both eigenvectors at once are incompatible.
6. *`deg b ≥ 3`.* This is Lemma W. ∎

*Open part (largely closed in §6.10: Lemmas C and C2 prove the containment except for linear `b` with `f = 3`).* It remains to show that `D∞(H̃) ⊆ τ*V` in the affine sector, i.e. that no core element has `Q`-degree 2 or more. Direct computation at depth 10 up to degree 11 confirms this for:
- K4 with `r = 0` and with `r = 1`;
- K1′ with `f = 4`;
- an affine non-K4 Hamiltonian.

A random search of 60 affine cubic-phase Hamiltonians of degree 8–10 agrees with the table, with no counterexample: K1 10, K1′ 13, K4 4, and `span{1, H}` 33. Cubic-phase Hamiltonians that are not affine in `Q`, such as `P³ + Q²`, remain open.

**Certificate.** `check_cubic_phase.py` (`cubic-phase-v1`; `results/hamiltonian/cubic_phase_theorem.json`) checks:
- **[G1]** Theorem G against Theorem X;
- **[G2]** the `Δ` formulas on the monomial basis up to degree 8;
- **[G3]** Theorem A₀ against `weyl_receipts`;
- **[W]** Lemma W on instances;
- **[K4]** the general K4 family on random `r`, `r′`, `w`;
- **[A]** the Theorem A table on instances. Here `D∞ ∩ τ*V` is computed directly.

`check_two_root.py` uses the following routes:
- `K4` for the new family;
- `pure, cubic phase affine` for the rest of the affine sector, reported as `span{1, H}`, proved inside `τ*V` and conjectured in full;
- `pure, cubic phase` for non-affine cubic-phase Hamiltonians, whose core is open.

### 6.10 Gauge form for every shear: why quadratic shears are special

§6.9 treated quadratic shears. The same mechanism works for every shear `w`, and it explains the phase diagram of triangular cores.

**Theorem GG (gauge form, every `w`).** Let
`S_t = exp( Σ_{n≥1} t^{2n} w^{(2n)}(Q) ∂_P^{2n+1}/(2n+1)! )`.
This is a `P`-differential operator whose coefficients depend on `Q`. Then
`Σ_k (tᵏ/k!) T_k(h̃, g̃)∘τ⁻¹ = S_t ∘ M^flat_t ∘ (S_t⁻¹ ⊗ S_t⁻¹)`.

*Proof.* Conjugation by `exp(iU(q̂)/ħ)`, with `U′ = w`, multiplies the Weyl kernel `K(x, y)` by `exp(i(U(x) − U(y))/ħ)`. Expanding about the midpoint, the linear term is the shift `p ↦ p + w(q)`. The odd higher terms give `S_t`, with `t` in place of `ħ`. Conjugation is an algebra automorphism, so the pulled-back product is the gauge transform of the flat one. ∎ `check_gauge.py` [GG] verifies the identity exactly against Theorem X for `deg w ≤ 6` and `k ≤ 7`.

Three consequences:
- **Exactness is flat exactness up to gauge, for every shear.** `G ∈ D∞(H̃)` if and only if, for every `r`, `flat-odd(S_t⁻¹h, S_t⁻¹g_r) = t·S_t⁻¹{h, g_r}`, where `g_r = D^r g`.
- **What singles out the quadratic shear.** `S_t` always exists. It has constant coefficients exactly when `deg w ≤ 2`, and then it maps `K[P]` to itself, which keeps the infinite towers of K1. For `deg w ≥ 3` its coefficients `w″(Q), w⁽⁴⁾(Q), …` depend on `Q`. The gauge then moves functions of `P` off `K[P]`, so the towers break.
- **What survives every shear.** `S_t` fixes every function of `P`-degree at most 2. This is the mechanism behind K2.

**Third-gate formula.** The `t³` coefficient of Theorem GG is
`T₃(h̃, g̃)∘τ⁻¹ = T₃^flat(h, g) + w″·Δ(h, g) + w‴·Λ(h, g)`,
where `Δ(h, g) = ∂³{h, g} − {∂³h, g} − {h, ∂³g}` and `Λ(h, g) = h_P g_PPP − h_PPP g_P`.
- The `w″Δ` term is a coboundary. It is removable exactly when `w″` is constant, which is Theorem G.
- The `w‴Λ` term is antisymmetric. It is the genuine remainder that higher shears add.

`check_gauge.py` [T3] verifies the formula exactly.

**Theorem AE (higher shears, affine sector).** Let `deg w ≥ 3` and `h = a(P) + Qb(P)` with `deg a ≥ 3` and `deg b < deg a`. Then the part of `D∞(H̃)` affine in `Q` is `span{1, H̃}`.

*Proof.* Only `T₃` is used, at depth at most 2.
1. For `g = α + Qβ` the flat term vanishes. So `T₃ = ω(Δ_f + QΔ_W) + ω′(L₀ + QL₁ + Q²L₂)`, where `ω = w″` has degree `m ≥ 1` and
   - `L₀ = a′α‴ − a‴α′`;
   - `L₁ = a′β‴ + b′α‴ − a‴β′ − b‴α′`;
   - `L₂ = Δ_W/3`.
2. Compare coefficients of powers of `Q`.
   - The top power gives `Δ_W = 0`.
   - The next powers give `Δ_f + mL₁ = 0` and `L₀ = 0`, centring `Q` at the root of `ω` when `ω` is a perfect power. Otherwise they also give `L₁ = Δ_f = 0`.
3. `L₀ = 0` forces `α = λa + const`, by a Wronskian argument that needs `deg a′ ≥ 2`. Subtract `λh`.
4. In the generic branch, `L₁ = 0` gives `β = μa + c`. Then `Δ_W = 0` and `Δ_f = 0` force `μ = 0`.
5. In the perfect-power branch, `β′` solves `ma′β‴ − 3a″β″ − (3+m)a‴β′ = 0`. With `Δ_W = 0` and the closure under `D`, this forces `β` to be constant.
6. Finally `{H, Q} = −a′ − Qb′` leaves `span{1, Q, H}`. ∎

**Lemma C (Q-degree containment, constant `b`).** If `h = a(P) + λQ` with `deg a ≥ 3` and `deg w ≥ 2`, every element of `D∞(H̃)` has `Q`-degree at most 1 in `(Q, P)`.

*Proof.* Suppose `g` has `Q`-degree `j ≥ 2`, with top coefficient `γ(P)`. Let `m = deg w″`.
1. The flat part of `T₃` lowers the `Q`-degree by at least 2. So the coefficient of `Q^{j+m−1}` in `T₃` gives
   `ma′γ‴ − 3ja″γ″ − (3j+m)a‴γ′ = 0`.
2. *Case `m = 0`.* This reads `(a″γ′)′ = 0`, so `γ` is constant. The next coefficient makes the second coefficient `γ₁` constant as well. The `Q^{j−1}` coefficient of `{H, g}` is then `−ja′γ`, which must also be constant. So `γ = 0`.
3. *Case `m ≥ 1`.* Nonzero polynomial solutions `γ′` all have one degree `d*(j)`. This is the positive root of `md² − (m + 3j(f−2))d − (3j+m)(f−2)(f−3)`, and it increases with `j`.
   - The closure `{H, g}` produces a level-`(j−1)` top coefficient. Its degree is `d*(j) + f − 1`, or `f − 2` when `γ` is constant. Neither equals `d*(j−1)`, because `d*(j−1) ≠ f − 2`: substituting `d = f − 2` leaves the residual `−3(j−1)(f−2)(2f−5) ≠ 0`.
   - When `λ ≠ 0`, `γ′` and `γ″` would both solve the same equation, so `γ` is constant and the same argument applies. ∎

**Lemma C2 (containment for other `b`).** Let `Γ_j` be the space of `Q^j`-coefficients of core elements of `Q`-degree at most `j`. Two facts hold:
- `Γ_j` is invariant under `L_j: γ ↦ bγ′ − jb′γ`, the part of `D` that preserves `Q`-degree.
- By the top coefficient of `T₃`, `Γ_j` lies in the polynomial solutions of
  `(3+m)b′γ‴ + 3(1−j)b″γ″ − (3j+m)b‴γ′ = 0`.

For `j ≥ 2` these force `Γ_j = 0` in the following cases.
- **`b` quadratic.** Write `b = μ(u² − δ)` with `u = P − p₀`. The solutions are `span{1, u, u^{N}}`, where `N = j + 1` in the cubic phase and `N = 3(j−1)/(3+m) + 2` in general. `L_j u^N` has leading coefficient `(N − 2j)μ ≠ 0`. In addition `L_j1 = −2jμu` and `L_ju = μ((1−2j)u² − δ)`. No nonzero subspace survives.
- **`deg b = n ≥ 3`.** The polynomial solutions are at most one-dimensional, `γ′ ∝ b′^k` with `k = (3j+m)/(3+m)`, since the other indicial exponent at infinity is `2 − n < 0`. `L_j` raises the degree of `∫b′^k`, because `(n−1)k + 1 − jn ≠ 0` for `j ≥ 2`. And `L_j1 = −jb′`.
- **`b` linear, cubic phase, `f = deg a ≥ 4`.**
  - The tops are `u^k` with `k ≤ 2`, and they are eigenvectors of `L_j`.
  - The ladder `(D − μ(k−j))g` excludes `k = 0` and `k = 2`.
  - For `k = 1`, the `Q^{j−2}` equation requires `e^{sX}[(e^{−sX}a′)(e^{−sX}γ₁)] − a′γ₁` to be linear in `s`. Here `X = ∂_P³` and `γ₁ = (j/μ)a + (quadratic)`. But its `s²` coefficient has leading term `(j/μ)a_f²·9f²(f−3)(f−2)(f−1)²(2f−5)·P^{2f−7}`, which is nonzero for `f ≥ 4`.

Consequences:
- **Exact cores now proved.**
  - K4 is exact: `D∞ = span{1, G, H}`.
  - K1′ is exact for `deg a ≥ 4`: `D∞ = span{1, P, P², H}`.
  - Every other cubic-phase Hamiltonian affine in `Q` has `D∞ = span{1, H}`.
  - Higher shears affine in `Q` with `deg b ≠ 1` have `D∞ = span{1, H}`.
- **Still open.** The case `b` linear remains for `f = 3` in the cubic phase (the 6-dimensional K1′ sector) and for higher shears.
  - For the cubic case `f = 3`, a symbolic elimination with `j` as a formal parameter finds no element of `Q`-degree `j ≥ 2`. It used the gates `T₃`, `T₅` at depth 2 on the top four `Q`-levels, for every top `u^k`, generic `(r, a₁)` and the special values `(0,0), (0,1), (1,0), (1,−3), (1/2, 2)`. This is computation, not a proof.

**Corollary K1c (now proved).** Let `deg F ≥ 3`.
- For `deg w = 2`: `D∞(F(P) + λq) = K[P] + Kq` exactly. This is K1, now with equality, by Theorem A and Lemma C.
- For `deg w ≥ 3`: `D∞(F(P) + λq) = span{1, H}`, by Theorem AE and Lemma C.

The second statement is the shear-composition collapse that a parallel line of work derived by a leading-operator argument. The proof here is independent, through the gauge form.

`check_two_root.py` uses three routes here:
- `K1` is now marked proved.
- The new route `RS` is a proved `span{1, H}`.
- `RS` also covers higher shears affine in `Q` with `deg b ≥ 2` (Lemma C2).
- `higher shear affine` covers linear `b`. It reports `span{1, H}`, proved for elements affine in `Q` and conjectured in full.
- K4 and K1′ with `deg a ≥ 4` are now proved routes, and `pure, cubic phase affine` is proved too.

**The sl₂ picture of the cubic-phase exceptions.** Let `R = Q + κ(P−r)²` be quadratic. Then `{σR, τR} = (στ′ − σ′τ)R`. So `sl₂·R = {σR : σ ∈ span{1, P, P²}}` is a copy of `sl₂` (Witt bracket), and the Witt obstruction `Δ_Witt` vanishes on it. The exceptional affine cores of Theorem A are exactly built from it.

| family | Hamiltonian | core |
|---|---|---|
| K1′, special case | `H = μ(P−r)R + c`, `deg c ≤ 1`, `f = 3` | `sl₂·R ⊕ sl₂·1` (dimension 6) |
| K4 | `H = μ(P−r)(P−r′)R + c`, `deg c ≤ 2` | `span{1, (P−r)R, H}` |

K4's condition `a ≡ A(P−r)³(P−r′) mod deg ≤ 2` says exactly that `H ≡ bR` modulo functions of `P` of degree at most 2, with `b(r) = 0`.

In the affine sector of the cubic phase, exceptional exact dynamics is therefore an `sl₂` acting on a quadratic. The quadratic is the part the gauge cannot see, and `sl₂` is the part on which the Witt obstruction vanishes.

**Certificate.** `check_gauge.py` (`gauge-shear-v1`; `results/hamiltonian/gauge_shear_theorem.json`) checks:
- **[GG]**, **[T3]**: the two identities above;
- **[AE]**: Theorem AE on instances;
- **[K1c]**: the K1 core dimensions for `deg w = 2`, and `span{1, H}` for `deg w = 3`, by direct computation;
- **[C2]**: the `s²`-coefficient identity at `f = 4, …, 16`. That coefficient is a polynomial in `f` of degree at most 8, so this proves it. Also checked are full core dimensions for K4, quadratic `b`, `deg b = 3`, K1′ with `f = 4`, and a higher shear with quadratic `b`.

### 6.11 The shear phase diagram

Take a pure top with constant transverse top, written in its triangular normal form `H = h(q, p + w(q))`. Suppose `h = a(P) + Qb(P)` is affine in `Q`, with `deg a = f ≥ 3` and `deg b < f`. Sections 6.2 and 6.8–6.10 then determine `D∞(H)` completely as a function of the degree of the shear and of `b`. The table shows how each additional degree of shear removes one layer of exact dynamics.

| shear | `b` constant | `b` linear | `b` quadratic | `deg b ≥ 3` |
|---|---|---|---|---|
| `deg w ≤ 1` (flat) | `W = ⊕_{j≤2} Q^jK[P]` | `V = K[P] + QK[P]` | `V` | `V` |
| `deg w = 2` (cubic phase) | `K[P] + KQ` (K1) | `span{1, P, P², H}` (K1′, `f ≥ 4`); for `f = 3`, `sl₂`-type cores of dimension 5 or 6 | `span{1, (P−r)R, H}` if K4, else `span{1, H}` | `span{1, H}` |
| `deg w ≥ 3` | `span{1, H}` | `span{1, H}` inside `τ*V` (conjectured in full) | `span{1, H}` | `span{1, H}` |

Every entry is proved except two:
- the `f = 3` cubic-phase entry, where containment in `τ*V` is supported by symbolic-`j` elimination;
- the linear-`b` entry for higher shears.

The sources are as follows.
- Row 1 is Theorem P⁺ with the roles of the variables exchanged: `τ` is affine, and `h` is affine in `Q` with a pure `P`-top.
- Row 2 is Theorem A together with Lemmas C and C2.
- Row 3 is Theorem AE together with Lemmas C and C2.

**Reading the diagram through the gauge.** The three rows are three behaviours of the gauge operator `S_t` of Theorem GG.
- **Flat.** `S_t = 1`. The flat strip structures survive, including elements of `Q`-degree 2.
- **Cubic phase.** `S_t = exp(ct²∂_P³/3)` has constant coefficients. It preserves `K[P]` but conjugates the flat bracket by a Witt-type defect. So towers in `P` survive (K1). The `Q`-direction keeps only the `sl₂` remnants on which the Gelfand–Fuchs density vanishes (K1′, K4, the `sl₂·R` picture).
- **Higher shears.** `S_t` has `Q`-dependent coefficients `w″(Q), w⁽⁴⁾(Q), …`. The antisymmetric remainder `w‴Λ` of the third gate then removes everything except the constants and `H`.

The quadratic-in-`P` structures of K2 sit outside this table, since `h` is not affine in `Q` there. They survive every shear because `S_t` fixes functions of `P`-degree at most 2.

**Certificate depth.** All the upper bounds in rows 2 and 3 use only the third gate `C₃`.
- Theorem AE applies it to an element and to its first bracket.
- Lemmas C and C2 apply it to an element and to finitely many of its brackets, at most `deg_P γ + 2` of them.

So in these rows a finite set of conditions `C₃D^r`, with `r` bounded in terms of the degrees of `h`, already cuts out the core. The lower bounds, i.e. the containments, are exact invariant-span certificates.

### 6.12 Non-affine normal forms: binomial edges collapse

The non-affine sector is the case where `h` has `Q`-degree at least 2 in its triangular normal form. It is controlled by the first Newton edge of `h` from the vertex `P^s`.

**Theorem NA.** Let `deg w = e ≥ 2` and let `h` have `P`-degree `s ≥ 2`. Assume:
- the first edge of the Newton polygon of `h` from `P^s` (coordinates: `Q`-exponent `i`, `P`-exponent `j`) contains exactly one other monomial, `cQ^d`, where `d ≥ 2` if `s ≥ 3` and `d ≥ 3` if `s = 2`;
- its slope `α = s/d` satisfies `α > 1/2` when `e = 2`, or `α > 1/e` when `e ≥ 3`.

Then `D∞(H) = span{1, H}`.

*Proof.* Weight `Q` by `α` and `P` by 1.
1. *Which part of the gate dominates.* In Theorem X, the flat factor `A` lowers the weight by `α + 1` per power of `t`. The corrections lower it by less exactly when `α > 1/2` (for `e = 2`), respectively when `αe > 1`. So the top of `T₃` is `w″Δ + w‴Λ` for the monomial shear `w = Q^e`, and the top of `H` is `E = P^s + cQ^d`.
2. *The top gate is diagonal.* The `Q^d` term contributes nothing, and on monomials
   `C₃^top(Q^iP^j) = e(e−1)s·j(j+s−3)·[(e−2)(j−s) − 3(s−1)i]·Q^{i+e−3}P^{j+s−4}`.
   For `e = 2` this reads `−6s(s−1)·i·j(j+s−3)·Q^{i−1}P^{j+s−4}`.
3. *Its kernel.* The kernel is spanned by monomials:
   - for `e = 2`: `K[P] ⊕ K[Q]`;
   - for `e ≥ 3`: `K[Q]`, `P^s`, and `Q^iP^{s+3(s−1)i/(e−2)}`.
4. *Closure under `D`.* We have `{E, Q^iP^j} = djQ^{i+d−1}P^{j−1} − siQ^{i−1}P^{j+s−1}`. Every kernel monomial other than 1 and the pair `P^s, Q^d` has an image outside the kernel that no other monomial can cancel. So the top core is `span{1, E}`.
5. *Conclusion.* The top-weight lemma gives `dim D∞(H) ≤ 2`. ∎

*The case `s = 2`.* Here the kernel of `C₃^top` also contains the monomials `Q^iP`. Their images `dQ^{i+d−1} − 2iQ^{i−1}P²` leave the kernel for `i ≥ 2`, and no other monomial can cancel them. For `e ≥ 3` the monomials `Q^iP^{2+3i/(e−2)}` with `i ≥ 1` are eliminated the same way. The remaining chains are followed to the end:
- `P → Q^{d−1}`;
- `Q → P`;
- `Q² → QP → dQ^d − 2P²`.

None of them closes for `d ≥ 3`. ∎

**The `m`-degree-2 tops with constant transverse top are now classified, apart from the upper bound for K2.** These are `H = c(p + w(q))² + r(q)`.

| condition | `D∞(H)` | source |
|---|---|---|
| `deg w < deg r / 2` | `span{1, H}` | Q′ |
| `deg r ≤ 2` | contains the six quadratics in `(q, P)` | K2; equality conjectural |
| `3 ≤ deg r < 2 deg w` | `span{1, H}` | NA |
| `deg r = 2 deg w` | `span{1, H}` | NB |

The case `deg r = 2 deg w` is the edge `P² + cQ^{2e}`, where flat and correction terms tie. It is now proved: Theorem NB. The remarks below record how it was first approached.
- On monomials the top gate splits into two parts. The first is a diagonal part, `e(e−1)j(j−1)[2(e−2)(j−2) − 6i]·Q^{i+e−3}P^{j−2}`, with the same free monomials as NA. The second is a shift part, `c(2e)(2e−1)(2e−2)·j(j−1)(j−2)·Q^{i+2e−3}P^{j−3}`.
- So the kernel is no longer spanned by monomials, but the `P`-top of every kernel element is one of the NA free monomials.
- The top problem, solved weight by weight up to weight 7 for `e = 2, 3` and `c ∈ {1, −1, 2, −1/4}`, gives `span{1, E}` in every case.
- Full cores computed directly, e.g. `(q²+p)² + q⁴` and `(q³+p)² + q⁶`, are `span{1, H}`.

The general proof is Theorem NB.

Examples:
- `(q² + p)³ + q²` and `(q² + p)⁴ + q³ + (q² + p)` collapse to `span{1, H}`. Both were previously reported as open cubic-phase cases.
- `(q³ + p)³ + q²` collapses as well.
- The quartic `(q² + p)² + q³` collapses, as does `(q³ + p)² + q⁴`.

**Theorem NE (general first edges).** Let `s ≥ 3`, and let the first edge `E` of `h` from `P^s` satisfy two conditions:
- its slope is above the threshold (`α > 1/2` for `e = 2`, `αe > 1` for `e ≥ 3`);
- `κ = s − 1 − α > 0`.

For `e = 2` assume also that `E` contains a monomial of `Q`-exponent at least 2. Then `D∞(H) = span{1, H}`.

*Proof.*
1. *The top gates in closed form.* On the diagonal two identities hold, where `d = ∂_P`:
   - `B^m(a⊗b) = d^m(a^{(m)}b^{(m)})`;
   - `(∂₂ − ∂₁)B^m(a⊗b) = d^m(a^{(m)}b^{(m+1)} − a^{(m+1)}b^{(m)})`.

   With the gauge form, the top gates vanish on `g` exactly when, for every `m ≥ 1`:
   - (`e = 2`) `{E^{(m)}, g^{(m)}}` has `P`-degree less than `m`;
   - (`e ≥ 3`) `3Q{E^{(m)}, g^{(m)}} + m(e−2)(E^{(m)}g^{(m+1)} − E^{(m+1)}g^{(m)})` has `P`-degree less than `m`.

   For `e = 2` this is the statement that `exp(s∂_P³)` intertwines the bracket on the top core.
2. *Finiteness.* The normal form has no `P^{s−1}` term, so `E^{(s−1)} = s!c₀P`. The condition at `m = s − 1` then does the following:
   - for `e = 2`, it bounds the `P`-degree of the `Q`-dependent monomials of a top-core element by `2s − 3`;
   - for `e ≥ 3`, it excludes every monomial of `P`-degree at least `2s − 2` outside one ray, and `D` excludes the ray.

   The `P`-top of `Dg` is `−s·i·Q^{i−1}P^{j+s−1}`, and nothing cancels it. Following `Dg` and `D²g` kills all weights `≥ 3s − 2` for `e = 2`, and all weights `> 2s − 3` for `e ≥ 3`. For `e = 2` the monomial of `Q`-exponent at least 2 in `E` is what removes pure powers of `P`.
3. *Nilpotency.* So the top core `V` is finite-dimensional. `D` raises the weight by `κ > 0`, hence is nilpotent on `V`.
4. *The kernel of `D`.* `ker D` is the Poisson centralizer `K[G]` of `E`, where `E = cG^k`. The `m = 1` condition on `G^m` produces `(k−m)km·G^{k+m−3}G_P{G, G_P}`. For `e ≥ 3` it is `(k−m)km·G^{k+m−3}G_P[3Q{G, G_P} − (e−2)G_P²]`. Both have positive `P`-degree for `m ∉ {0, k}`.
5. *No longer chains.* A chain of length at least 2 would need `g` of weight `α + 1` with `{E, g} = λE`, `λ ≠ 0`. Solving the eigen-equations monomial by monomial leaves two possibilities:
   - `α ∈ Z`, `E = P^m(P^α + κ′Q)^a` and `g = P(P^α + κ′Q)`. These are excluded by the `m = 1` condition: in the variables `(R, P)` with `R = P^α + κ′Q` it is a sum of at most three terms, which cannot equal a power of `R − P^α`. For `e ≥ 3` its `Q⁰`-part is proportional to `α − (s−1) ≠ 0`.
   - `α = 1` with `g` quadratic. This is excluded by the `Q⁰`-part of the `m = 1` condition, because `E` has no `QP^{s−1}` term.

   So `V = span{1, E}`. ∎

The extra hypothesis for `e = 2` is necessary. First edges whose only `Q`-terms are linear in `Q` are exactly where the exceptional cores K1′ and K4 live.

**Theorem NB (the boundary edge).** Let `s = 2` and `h = c₀P² + cQ^{2e} + (lower)` with `deg w = e ≥ 2`, so that the slope is `1/e`. Then `D∞(H) = span{1, H}`.

*Proof.*
1. *Reduction to a flat problem.* At slope `1/e` every term of Theorem X is top. The top problem is therefore the flat core of `F = (p + q^e)² + cq^{2e}`, which is quasi-homogeneous for the weights `(1, e)`.
2. *The third gate.* For `u = g_pp`, `T₃` is the first-order equation `[2(e−2)p + 4γ(2e−1)q^e]u_p = 6q·u_q`, where `γ = 1 + c`. So `u = q^aL^ν`, with `L = 2p + 2γq^e`, `ν = 3(W − 2e)/(4e−2)` and `a = ν(e−2)/3`.
3. *The fifth gate.* `T₅` requires `(ν−2)(e−4) = 5a` and `(ν−2)K(e) = 0`, where `K(e) = (2e)₅ − 2(e)₅ − 10e(e)₄ = 20e²(e−1)²(e−2)`. For `e ≥ 3` only `ν ∈ {0, 1}` survive.
4. *Closure under `D`, for `e ≥ 3`.* Every remaining candidate is eliminated except 1 and `F`. This uses `β² − 4γ = −4c ≠ 0`.
5. *The case `e = 2`.* Here every `ν` survives, because `L` is itself a quadratic-shear coordinate. But `D(L^n) = −8cn·qpL^{n−1}` has `p`-degree `n`, so `D` removes all weights `≥ 6`. The weights up to 7 were solved exactly in `c`: the maximal minors vanish only at `c = 0`. ∎

Together with Q′, K2 and NA, this settles the `m`-degree-2 tops with constant transverse top, apart from the upper bound for K2.

**Theorem NT (threshold edges, `e ≥ 3`).** Let `s ≥ 3` and `deg w = e ≥ 3`, and let the first edge of `h` from `P^s` have slope exactly `1/e`. Then `D∞(H) = span{1, H}`.

*Proof.*
1. *Reduction to a flat problem.* Give `q` weight 1 and `p` weight `e`. The edge is `E = Σ_k e_k Q^{ek}P^{s−k}`, and the top of `H` is `F = E(p + w_e q^e, q^e) = Σ_k c_k q^{ek}p^{s−k}`. The flat gates are homogeneous, so by the top-weight lemma it suffices to show that the flat core of `F` is `span{1, F}`. The normal form has no `P^{s−1}` term, so `c₀ = e₀` and `c₁ = s·w_e·e₀ ≠ 0`.
2. *Top end.* Take a weight-homogeneous core element `g = Σ_j x_j q^{i+ej}p^{N−j}` with `0 ≤ i < e`, and order the outputs by `p`-degree. The leading output of `T₃(F, g)` is `−(s)₃(i)₃ x₀`, so a top term with `q`-exponent `≥ 3` is impossible. It therefore suffices to show `x₀ = 0` whenever `(i, N) ∉ {(0, 0), (0, s)}`. Once `x₀ = 0`, the next term has `q`-exponent `≥ e ≥ 3` and dies too. For `(i, N) = (0, s)`, subtract `x₀F` first.
3. *Step 1.* At the next `p`-degree, each of `T₃g`, `T₃Dg`, `T₃D²g` and `T₅g` gives one linear equation in `(x₁, c₁x₀)`, with closed-form coefficients. The relevant 2×2 minors, with `b = e`, are:
   - type `i = 0`, pair `(T₃g, T₃Dg)`: `b²Ns²(s−N)(b−3)(b−2)²(b−1)²(s−2)(s−1)(N+s−3)`;
   - type `i = 1`, pair `(T₃Dg, T₃D²g)`: a nonzero constant times `(N−1)(N+s−1)(N+2s−4)`. At `N = 1` the pair `(T₃g, T₃D²g)` takes over; its factor `(2−b)N + bs + s − 3` equals `(b+1)(s−1)` there;
   - type `i = 2`, pairs `(T₃g, T₃D²g)` and `(T₃Dg, T₃D²g)`: nonzero constants times cubics `f₁₃(N)` and `f₂₃(N)`. Their resultant is `4(b−3)(b+1)(s−2)(s−1)³B(b, s)`, and `B(4+x, 3+y)` has only positive coefficients. The `x₁`-entry of `T₃D²g` is nonzero for `b ≥ 3`, so the two cubics cannot vanish together.

   For `e ≥ 4`, some minor is nonzero at every `N`, so `c₁x₀ = 0`.
4. *The case `e = 3`.*
   - Types 1 and 2 still close at step 1. The minors are `288s²(s−2)(s−1)²(3N² + 3(s−3)N − (s−2))` and `2880s⁴(s−2)(s−1)²(3N² + 9Ns − 15N + 6s² − 19s + 14)`. The first factor is negative at `N = 0` and positive for `N ≥ 1`; the second is positive.
   - Type 0 needs step 2. `T₃g` gives `x₁ = λx₀` with `λ = N(N−1)(N−2)/((s)₃)`. The step-2 rows of `T₃Dg` and `T₃D²g` then eliminate `x₂` and the coefficient `c₂/c₁²` together, leaving
     `25920·N s⁴(s−N)(s−1)²(s−2)(N+s−3)·(3N² + 6(s−3)N − 10(s−2))·x₀ = 0`.
     The last factor is `5 − 4s < 0` at `N = 1` and is positive for `N ≥ 2`. ∎

Only `T₃`, `T₅` and depth `R ≤ 2` are used.

*The case `e = 2`* is the cubic phase, which Conjecture P004 excludes. It is not closed by these steps:
- Type 2 closes at step 1, with minor `−576s²(s−2)(s−1)³(N+s−2)`.
- Type 1 closes at step 2 for `N ≥ 1`. The eliminant `N(N+s−3)(N+2s−4)(8N²s − 11N² + 8Ns² − 33Ns + 28N − 2s² + 7s − 5)` is nonzero there. At `N = 0` (that is, `g = q`) it fails exactly when `c₂/c₁² = (s−1)/(2s)`, i.e. when `E` has no `Q⁴P^{s−2}` term.
- Type 0 at step 3 has a one-dimensional kernel in the extended unknowns `(x₀, c₂x₀, c₃x₀, x₁, c₂x₁, x₂, x₃)`. That kernel is consistent precisely at the binomial point `(c₂, c₃)/c₁^{2,3} = (C(s,2)/s², C(s,3)/s³)`, with `g = (p + q²/s)^N`.

These `e = 2` computations were done in scratch with exact symbolic algebra and are not yet in a checker. So for `e = 2` the obstruction lives exactly where `F` agrees with `(p + q²/s)^s` to the order examined. A proof needs a first-deviation argument at the first nonzero `e_k` (`k ≥ 2`). Direct computation finds `span{1, F}` in every sampled case.

**Theorem NV (vertex-adjacent rigidity).** Let `F` be weight-homogeneous with vertex `p^s` (`s ≥ 3`) and vertex-adjacent monomial `c·q^B p^{s−K}` with `c ≠ 0`, `B ≥ 4` and `K ≥ 1`; every other monomial has lower `p`-degree. Then the flat core of `F` is `span{1, F}`.

*Proof.* Take `g` and its top coefficient `x₀` as in the proof of Theorem NT.
1. *Level `K`.* Only two products contribute at output level `K` (the `p`-degree `K` below the top): `p^s ⊗ x₁q^{i+B}p^{N−K}` and `cq^Bp^{s−K} ⊗ x₀q^ip^N`. Intermediate terms of `g` meet no monomial of `F` there. So each `T₃D^rg` gives a linear equation in `(x₁, c·x₀)` with closed-form coefficients.
2. *The minors.* Each of the following pairs has a minor whose factors do not involve `K`:
   - type 0, pair `(T₃g, T₃Dg)`: `N(s−N)(N+s−3)` times `(B−3)` and nonzero factors;
   - type 1, pair `(T₃Dg, T₃D²g)`: `(N−1)(N+s−1)(N+2s−4)`. At `N = 1` the pair `(T₃g, T₃D²g)` gives `(B+K)(s−1)(s−2)`;
   - type 2, pair `(T₃D²g, T₃D³g)`: `(N+s−2)(N+2s−2)(N+3s−5)`.
3. *Conclusion.* Therefore `x₀ = 0` unless `(i, N) ∈ {(0, 0), (0, s)}`. The next surviving term of `g` either has `q`-exponent `≥ 3` and dies, or is again of type 1 or 2, and the argument repeats. ∎

*The case `B = 3`, `K = 2`.* Here `F = p^s + q³p^{s−2} + cq⁶p^{s−4} + …` with lattice step `(3, 2)`.
- Types 1 and 2 close at level 2. The minors are `−144s²(s−2)(s−1)·f₁` and `−1440s⁴(s−2)(s−1)·f₂`, where
  - `f₁ = 6N²s − 9N² + 6Ns² − 24Ns + 21N − (s−1)(s−2)` is negative at `N = 0` and positive for `N ≥ 1`;
  - `f₂ = 6N²s − 9N² + 18Ns² − 54Ns + 39N + 4(s−1)(s−2)(3s−4)` is positive.
- Type 0 closes at level 4. After `x₁ = λx₀`, the `T₃Dg`/`T₃D²g` pair eliminates `x₂` and `c` together, leaving `12960·N s⁴(s−N)(s−2)(s−1)(N+s−3)·f₀·x₀ = 0`. Here `f₀ = 6N²s − 9N² + 12Ns² − 54Ns + 51N − 16s² + 60s − 50`, which equals `−4(s−1)(s−2)` at `N = 1` and is positive for `N ≥ 2`.

**Corollary (edges below the threshold; flat lower terms).** Let `s ≥ 3`.
- If the first edge of the normal form `h` from `P^s` has slope `K/B < 1/e` with `e = deg w ≥ 2`, then `D∞(H) = span{1, H}`. The shear terms then have lower weight, so the top problem is the flat core of the edge. The normal form has `K ≥ 2`, so `B > eK ≥ 4` automatically.
- If `deg w ≤ 1`, the shear is affine-symplectic and the flat gates are invariant. A pure top forces the first-edge slope `K/B < 1`, and the normal form forces `K ≥ 2`. So either `B ≥ 4`, or `(B, K) = (3, 2)`, and both cases give `D∞(H) = span{1, H}`. Every flat-lower-terms pure top therefore collapses.

With `K = 1`, Theorem NV re-proves NT for `e ≥ 4`, using depth 3 in place of the resultant argument. Theorem NV uses only `T₃` and depth `R ≤ 3`.


**Certificate depth across the families.** Direct computation in degrees up to `d + 1` shows that the third gate alone (`K = 3`) cuts out every core listed. The number of brackets needed is:
- `R = 1` for K1, K1′, K4 and RS;
- `R = 2` for K2, K1+K2, K3 and non-family affine cubic-phase Hamiltonians.

For the quadratic-shear oscillator `(q² + p)² + κq²/2` with `κ ≠ 0`, `R = 3` is needed up to degree 8, while `κ = 0` keeps the infinite tower. For the cubic shear `(q³ + p)² + q²/2`, `R = 2` suffices. This agrees with the depth jump found in the parallel line of work.

`check_gauge.py` covers these theorems as follows:
- **[NA]** the monomial formula on a grid of `(e, s, d, i, j)`, plus three instances computed directly;
- **[TG]** the two diagonal identities and the closed form of the cubic-phase top gates, on random polynomials;
- **[GE]** non-binomial edges (cubic phase and `e = 3`), whose full cores are computed directly;
- **[BE]** the identity for `K(e)`, verified at 9 values of `e`, plus boundary flat cores for `e = 2, 3, 4` and several `c`;
- **[NV32]** the `B = 3`, `K = 2` rows against the gates, the three eliminants as exact identities, the sign facts (positivity after shifting), and three flat instances;
- **[NV]** three parts:
  - the closed-form level-`K` rows, compared with the gates on a box in `(B, K, s, N)`;
  - the four minors, as exact polynomial identities in `(N, B, s, K)`;
  - flat cores of four weighted forms, including `p⁴ − q⁴p²` and one with an intermediate lattice step;
- **[NT]** five parts:
  - the closed-form step-1 rows, compared with the gates on a `9 × 7 × 7` box in `(b, s, N)`;
  - the `e = 3` step-2 rows, on a box in `(N, s)` at two values of `c`;
  - every minor and the `e = 3` eliminant, as exact polynomial identities in `(N, b, s)` or `(N, s, c)`;
  - the resultant identity, on a `13 × 19` box (enough for its degrees), and positivity of `B(4+x, 3+y)`;
  - flat cores of threshold forms for `e = 3, 4, 5`.

`check_two_root.py` reports these Hamiltonians on the proved routes `NA`, `NE`, `NB`, `NT` and `NV`.

### 6.14 Upper bounds: K2, K1+K2, K1′ with `f = 3`, linear `b`, perfect-power transverse tops

All four results below use the same device. Some grading makes `D` weight-preserving to leading order, with top part `D₀`. The top components of core elements of weight `n` form a `D₀`-invariant space `V_n`. The leading part of `T₃` (or of the top gates) cuts this space down. When `D₀` is diagonalizable with simple spectrum, `V_n` is spanned by the eigenvectors it contains, and those can be tested one at a time.

**Theorem K2U (K2 and K1+K2 are exact).** Let `h = αP² + γQ² + λQ + c` with `α ≠ 0`, in the normal form (no `P`-linear terms), and `deg w = e ≥ 2`.
- If `e ≥ 3`, or `e = 2` and `γ ≠ 0`, then `D∞(H) = τ*K[Q, P]_{≤2}` (dimension 6).
- If `e = 2` and `γ = 0` (K1+K2), then `D∞(H) = K[P] + τ*K[Q, P]_{≤2}`.

*Proof.*
1. *The third gate.* Since `h` is quadratic, `T₃^flat(h, ·) = 0`. The third-gate formula gives `T₃ = −6αw''·g_{PPQ} + 2αw'''·P·g_{PPP}`.
2. *Top components.* Grade by total degree in `(Q, P)`. The top part of `D` is `D₀ = 2αP∂_Q − 2γQ∂_P`, which preserves degree. For `u = ∂_P²g_n`, the leading part of `T₃` says `3Q∂_Qu = (e−2)P∂_Pu`, so `u` is supported on monomials `QᵃPᵇ` with `3a = (e−2)b`. For `e = 2` the condition is `∂_Qu = 0`.
3. *`e ≥ 3`.*
   - If `γ ≠ 0`, `D₀` is diagonal on `z^a z̄^b` with `z = P + i√γ Q`, with simple spectrum.
   - If `γ = 0`, `D₀` is nilpotent, and its kernel in degree `n` is `KPⁿ`.
   - Either way `V_n ≠ 0` would contain a vector whose `∂_P²` has `P^{n−2}`-coefficient `n(n−1) ≠ 0`. That monomial violates `3a = (e−2)b` unless `n = 2`. So core elements have degree `≤ 2`.
4. *`e = 2`.* The condition is `∂_P²g_n ∈ K[P]`, i.e. `g_n ∈ span{Pⁿ, Q^{n−1}P, Qⁿ}`.
   - For `γ ≠ 0`, no `z^a z̄^b` lies in this span when `n ≥ 3`. Its `QP^{n−1}` coefficient is `i√γ(a−b)` and its `Q²P^{n−2}` coefficient is `−γ((a−b)² − n)/2`.
   - For `γ = 0`, `D₀ = 2αP∂_Q` pushes `Q^{n−1}P` and `Qⁿ` onto `Q^{n−2}P²`, so `V_n ⊆ KPⁿ`. With the containment of §6.8 this gives equality. ∎

**Theorem LB (linear `b`, higher shears).** Let `deg w = e ≥ 3` and `h = a(P) + Q·b(P)` with `deg a = f ≥ 3` and `b` linear. Then `D∞(H) = span{1, H}`.

*Proof.*
1. *Grading.* Give `Q` weight `f − 1` and `P` weight 1. The top of `h` is `E = a_fPᶠ + μQP` (normalize `a_f = μ = 1`). The slope `f − 1` lies above the threshold, so the top gates are the closed forms of Theorem NE (1). Here `s − 1 − α = 0`, so `D₀ = {E, ·}` preserves weight.
2. *Eigenvectors.* With `R = Q + P^{f−1}` we have `E = PR`, `{E, P} = P` and `{E, R} = −R`. Hence `D₀(PʳRʲ) = (r − j)PʳRʲ`. The weight-`n` space has the basis `φⱼ = P^{rⱼ}Rʲ` with `rⱼ = n − (f−1)j`, and the eigenvalues `n − fj` are distinct. So `V_n` is spanned by some of the `φⱼ`.
3. *The order-1 top gate.* On a monomial,
   `C₁(QⁱPʳ) = (e+1)r(r−1)Q^{i+1}P^{r−2} + f·r[(e−2)(r−f) − 3(f−1)i]QⁱP^{r+f−3}`,
   and `C₁(g)` must have `P`-degree 0.
   - For `φⱼ` the output `P^{n+f−3}` comes only from the term `Pⁿ`, with coefficient `f·n(e−2)(n−f)`. This forces `n ∈ {0, f}`.
   - The output `Q^{j+1}P^{rⱼ−2}` comes only from the leading term. This forces `rⱼ ≤ 2`.
   - Together these leave only `φ₀ = 1` (`n = 0`) and `φ₁ = PR = E` (`n = f`). So the top core is `span{1, E}`. ∎

With Theorem AE and Lemma C2 this completes the higher-shear affine sector: `D∞(H) = span{1, H}` for every `b`.

**Theorem K1P (K1′ with `f = 3`).** Let `deg w = 2` and `h = aP³ + bP + λQ + μQP` with `aμ ≠ 0`. Then `D∞(H) = span{1, Q, P, P², H}`, together with `PH` exactly when `λ = 0`.

*Proof.*
1. *The top core.* Give `Q` weight 2 and `P` weight 1, so `E = aP³ + μQP`. The cubic-phase top gates require that `{E^{(m)}, g^{(m)}}` has `P`-degree `< m`.
   - `m = 2` leaves, in weight `n`, only `Pⁿ` and monomials `QʲPʳ` with `r ≤ 3`.
   - `m = 1`: `μg_{PP} − 6aP·g_{PQ} ∈ K[Q]`. This kills `Pⁿ` for `n ≥ 6`. It leaves at most `Q^{n/2}` for even `n ≥ 6` and nothing for odd `n ≥ 7`.
   - `D₀`-invariance removes `Q^{n/2}`, because its image contains `Q^{n/2−1}P²`.
   - For `n = 5` the single candidate is not a `D₀`-eigenvector, so it is removed too.
   - In weights `≤ 4` what survives is `1, P, P², Q, E, PE`. So `dim D∞(H) ≤ 6`.
2. *The element `PH`.* Modulo the five known core elements, a core element of weight 4 is `c·PH + κP³`. The twisted third gate gives:
   - `T₃(PH) = −36aλ` and `T₃(P³) = 36μ`, which forces `κ = aλc/μ`;
   - then `T₃(D(cPH + κP³)) = 72aλμ·c`.

   So for `λ ≠ 0` we get `c = 0`. For `λ = 0`, `PH` is in the core by §6.8. ∎

**Theorem TP (perfect-power transverse tops, `s ≥ 3`).** Let `H` be a pure top with `m`-degree `s ≥ 3` and transverse top `φ = c(ℓ+γ)ᵏ`, where `2 ≤ k ≠ s`. Then `D∞(H) = span{1, H}`.

*Proof.* Put `Q = ℓ + γ`.
1. *`m`-tops.* In the `m`-degree filtration the top is the monomial `QᵏMˢ` (writing `M = m`). By Theorem M its core is `span{1, QM, QᵏMˢ}`. So, after subtracting a multiple of `H`, a core element is `g = κQm + u(Q)`.
2. *Gates.* For `j ≥ 3`, `T_j(H, g) = ±∂_m^jH·u^{(j)}`. With `j = 3 ≤ s` this forces `deg u ≤ 2`.
3. *Total degree.* The pure top `H_d = cQ^d` has `d > k + s`. The degree-`d` part of `Dg` is `cdκQ^d`. Its `m^s`-part fixes the `H`-coefficient of `Dg` as `κ(k−s)`. Comparing gives `κ(d − k + s) = 0`, so `κ = 0`.
4. *Conclusion.* Then `Dg = −H_m·u'` has `m^{s−1}`-coefficient `−sQᵏu'`. Since `s − 1 ≥ 2` this must vanish, so `u' = 0`. ∎

`check_gauge.py` covers these as follows:
- **[K2U]** the reduced third gate on random instances, and two full cores;
- **[LB]** the monomial formula for `C₁` and the eigenvector identity on grids, the top core computed for four `(f, e)`, and two full cores;
- **[K1P]** the top cores up to weight 16 for two `(a, μ)`, and the `PH` obstruction values on random instances;
- **[TP]** three full cores.

`check_two_root.py` now reports K2, K1+K2 and K1′ as proved, sends higher-shear Hamiltonians with linear `b` to the proved route `RS`, and perfect-power transverse tops with `s ≥ 3` and `k ≠ s` to the proved route `TP`.

### 6.13 Context (literature check, preliminary)

A first literature check located the following. No priority is claimed for any statement in §§6.8–6.12, and a careful reading of the primary sources is still pending.

- **All observables versus one sector.** D. Robert, *When Poisson and Moyal brackets are equal?* (arXiv:2207.08798), shows the following. If the Moyal and Poisson brackets of `H` agree with every Schwartz observable, then `H` is a polynomial of degree at most 2. `D∞(H)` asks a different question with different quantifiers: what is the largest observable sector with exact agreement along the whole Hamiltonian flow, for a fixed nonlinear `H`. Robert's theorem is the statement that this sector is everything only when `H` is quadratic.
- **Nonlinear canonical transformations in Weyl quantization.** Weyl quantization has a restricted covariance under some nonlinear canonical transformations; see arXiv:quant-ph/0011076 and arXiv:quant-ph/0605236. Transforming the star product to new coordinates makes observables transform classically (Błaszak–Domański, arXiv:1208.2835). A coordinate change in the Moyal product was worked out to third order in arXiv:hep-th/0007072.

  Theorem GG is an explicit closed form of this phenomenon for triangular maps `(q, p) ↦ (q, p + w(q))`. The gauge operator is `S_t = exp(Σ t^{2n}w^{(2n)}(Q)∂_P^{2n+1}/(2n+1)!)`. What the present work uses it for is new relative to the sources checked: reading off exact sectors, the constant-coefficient criterion `deg w ≤ 2`, and the third-gate formula.
- **The Gelfand–Fuchs cocycle.** The cocycle on vector fields of the line is classical; for background see e.g. arXiv:math/0502372. Its density appears in §6.9 as the Witt part of the cubic-phase obstruction. The search found no source that connects it to exactness of Moyal evolution.

These references come from a first search. Before any external positioning they need to be read in full, especially quant-ph/0605236 and hep-th/0007072.

### 6.4 The decision procedure and what remains open

`check_two_root.py` (`two-root-perturbation-v1`) decides, for any rational `H` with a two-root top:
- it recomputes the top type from a verified square-free decomposition;
- it solves for the translation `τ` exactly and tests the normal forms;
- it reports the core, the active part, and whether the answer is proved or conjectural. The proved routes are:
  - Theorems U, P⁺, Q, Q′, B, NE and T;
  - K1, K1′ (`deg a ≥ 4`) and K4;
  - RS, NA and the affine cubic phase (§§6.9–6.12);
- for the other triangular families (K1′ with `deg a = 3`, K2, K3) it reports a span that is proved to lie in the core, with equality marked conjectural.

Enveloped examples are `results/hamiltonian/tworoot_*.json` and `binomial_*.json`.

The tests generate random members of every route and random affine changes of coordinates (degrees 3–5 in the suite; degrees 3–6 at depth 10 in a longer run). Each is compared with direct dimensions of `{G : deg G ≤ d+1, C_kD^rG = 0, r ≤ 8}`. Depth matters: with three gates the qp³+q² family shows spurious extra elements, and one Q′ instance needs depth 8.

**Conjecture (two-root tops), status.** As originally stated, the conjecture says: let `H_d` be pure, near or balanced, and suppose `H` has none of the structures of Theorem P⁺; then `D∞(H) = span{1, H}`.
- **Balanced tops:** true, by Theorem B (§6.5).
- **Near tops:** true, by Theorem NE (§6.7).
- **Pure tops:** false. The counterexample `(q³ + p)²` and the triangular families K1, K1′, K2, K3 are in §6.8, and the corrected pure-top statement is Conjecture P004 there.

**Where the pure-top classification stands.** Write the top in coordinates `(ℓ, m)`. Let `s` be the `m`-degree and `φ` the transverse top. When `φ` is constant, write `h` and `w` for the triangular normal form.

Proved:
- `s ≤ 1` (Theorem P⁺).
- `deg φ ≥ 2` and not a perfect power (Theorem T).
- `φ` constant, with `h` affine in `Q`: the whole shear phase diagram of §6.11, except linear `b` (the 6-dimensional K1′ sector for `f = 3`, and higher shears).
- `φ` constant, with `h` non-affine: every first edge above the slope threshold (Theorems NA and NE), every edge at the threshold for `deg w ≥ 3` (Theorem NT), every edge below the threshold and every flat-lower-terms top (Theorem NV), and the whole `m`-degree-2 range `deg r ≥ 3` (Theorems NA and NB).
  For `s ≥ 3` this covers every non-affine normal form unless `deg w = 2`. A non-affine `h` has `s − 1 − α > 0` automatically, and every slope is above, at or below the threshold. Inside the cubic phase (`deg w = 2`), which P004 excludes, the cases left are threshold edges and first edges whose `Q`-terms are all linear in `Q`.
- `s = 2` with `deg w < deg r/2` (Theorem Q′).

Open, but supported by direct computation and top-problem solutions:
- threshold edges in the cubic phase `deg w = 2` (§6.12, after Theorem NT);
- `φ` linear or a perfect power outside K3;
- the upper bounds for K2, K3 and K1′ with `f = 3`.

With §5 this gives a statement of when **active** exact dynamics survives a lower-order perturbation. It is conditional on Conjecture P004 in the open regions just listed:
- three or more roots in the top: never (proved);
- unequal top: a single active quadratic `G`, exactly in the normal form of Theorem U (proved);
- near top: an infinite active sector exactly when `H` is affine in `m` (proved, Theorems P⁺ and NE);
- pure top:
  - an infinite active sector in the affine or strip structures of Theorem P⁺ (proved);
  - an infinite active sector also in the triangular family K1 with `λ ≠ 0`, e.g. `(q² + p)³ + q` (proved, §6.8);
  - a nonzero finite active part in K1′, K2, K3 and K4 (K4 and K1′ with `deg a ≥ 4` exact, the others containment);
  - none otherwise (proved for Q′, T, RS, NA and the affine cubic phase; conjectural in the open regions);
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
