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

**Not covered.** The full six-parameter family `qp³ + aq² + bqp + cp² + dq + ep + f` remains open. After normalizing `a` and `c`, the `qp` coefficient is a continuous modulus. A parametric Weyl Gröbner computation or a structural argument is needed, and finite samples do not substitute for it. Homogeneous quartics are also open: `q⁴ + p⁴` exceeds the default generator budget, and the backend reports `unknown`.

## 4. Commands

```bash
python3 -B extensions/hamiltonian/weyl_groebner.py discover "q*p^3+q^2+p^2" --output R.json
python3 -B extensions/hamiltonian/weyl_kernel.py R.json --output K.json
python3 -B extensions/hamiltonian/check_weyl_kernel.py K.json
python3 -B extensions/envelope.py check results/hamiltonian/qp3_plus_q2_plus_p2.json.gz
python3 -B -m unittest test_weyl_discovery      # from extensions/hamiltonian
```

Measured on the development container: `qp³+q²+p²` takes about 80 s for discovery and about 2 min for classification, most of it replaying the 13-generator receipt. The other rows take seconds.
