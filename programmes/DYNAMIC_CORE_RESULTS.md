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

The results below prove the conjecture for every odd degree. For even degree they prove it in every stratum except the types `(1^d)` and `(d/2, 1^{d/2})` with `d ≥ 8`.

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

**Coverage.**
- *Odd `d`.* A form with at least three roots either has a root of multiplicity in `[2, d−2]` or is squarefree. So R1, R2 and R3 prove the conjecture **for every odd degree**. Degree 7 is now fully classified.
- *Even `d`.* The forms not covered by R1 have all multiplicities in `{1, d/2}`, that is types `(1^d)` and `(d/2, 1^{d/2})`.
  - `d = 4`: these are §3c, where `(2,1,1)` was certified individually.
  - `d = 6`: these are §3d, Route C.
  - **Open: even `d ≥ 8`, types `(1^d)` and `(d/2, 1^{d/2})`.** In degree 8 these are `(1⁸)` and `(4,1,1,1,1)`.

**Evidence in degrees 7 and 8.** For one representative of every root type, and for two random squarefree forms, the direct dimensions of `{G : C_kD^rG = 0, r ≤ 3}` were computed in degrees 1–16 (`d = 7`) and 1–18 (`d = 8`). They agree exactly with the predicted cores, including `(1⁸)` and `(4,1,1,1,1)`. No counterexample appeared. This is evidence, not proof. The sextic proof of static finiteness at a simple root (§3d) needed an elimination tree in four local coefficients. The degree-independent mechanism for even degree, which would replace that tree, has not been identified. In odd degree it is the apolar kernel of `T_d`.

### 5.3 Perturbation corollary

**Corollary P.** Let `H = H_d + P` with `deg P < d`. If `D∞(H_d) = span{1, H_d}`, then `D∞(H) = span{1, H}`.

*Proof.* Use the weight `(1,1)` in the top-weight lemma. The top part of any `G ∈ D∞(H)` lies in `span{1, H_d}`, so `G` has degree 0 or `d`. In degree `d`, `G − cH ∈ D∞(H)` has lower degree, so it is a constant. ∎

Combined with §§3c, 3d and 5.2, this covers every Hamiltonian whose top homogeneous part has at least three distinct roots and lies in a proved stratum. That includes perturbations that change the one-step exactness space, since lower terms of degree at least 3 change the gates.

**Executable coverage (`root-rigidity-v1`; checker `check_root_rigidity.py`).**
- Given a rational `H`, the certificate declares a square-free decomposition of `H_d(x, 1)`. The checker verifies the product, square-freeness and coprimality.
- It derives the root type over Q̄, including the root at `(1:0)`.
- It selects the route (monomial, R1, R2, R3, W3, W4 or open) and reports the core and the active part.
- Five examples are enveloped under `results/hamiltonian/rigidity_*.json`. One of them is an open squarefree octic, which the checker reports as open rather than guessing.
- The tests recover root types of random forms and reject forged decompositions. They also check that random lower-order perturbations of proved tops leave exactly `span{1, H}` in the direct computation.

### 5.4 Scope and positioning

The question here is different from theorems that ask when exactness holds for *every* observable, which force `H` to be quadratic. Here `H` is a fixed nonlinear Hamiltonian, and the object is its maximal polynomial sector of exact repeated evolution. Any priority claim would need a focused literature review. None is made.

On effective finite determination:
- For monomials, Theorem M gives an explicit stopping rule: `C₃` and depth 3.
- For R1–R3, the proofs give explicit static or one-step bounds. Examples are `n ≥ (d−1)(d−2) + 3` for R2 and `n ≥ 4` with one `D`-step for R3; below these bounds the chain argument applies.
- A general decision procedure with a proved stopping rule for arbitrary `H` remains open. Operator-ideal certificates (§1) and classifications of polynomial solutions remain distinct claims.

## 4. Commands

```bash
python3 -B extensions/hamiltonian/weyl_groebner.py discover "q*p^3+q^2+p^2" --output R.json
python3 -B extensions/hamiltonian/weyl_kernel.py R.json --output K.json
python3 -B extensions/hamiltonian/check_weyl_kernel.py K.json
python3 -B extensions/envelope.py check results/hamiltonian/qp3_plus_q2_plus_p2.json.gz
python3 -B -m unittest test_weyl_discovery      # from extensions/hamiltonian
```

Measured on the development container: `qp³+q²+p²` takes about 80 s for discovery and about 2 min for classification, most of it replaying the 13-generator receipt. The other rows take seconds.
