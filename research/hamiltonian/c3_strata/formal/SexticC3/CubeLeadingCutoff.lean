import SexticC3.CubeLeadingStatic

/-! # All-degree momentum cutoff from the actual static recurrences. -/
noncomputable section
set_option linter.unusedSectionVars false
namespace SexticC3.CubeLeading.Polynomial
open MvPolynomial
variable {K : Type*} [Field K] [CharZero K]

lemma fifth_vanish (t : GateParameters K) (f : Poly K) (hf : Static t f)
    (i j : ℕ) (hz : bicoeff i (j+5) f = 0) : bicoeff (i+1) (j+4) f = 0 := by
  have h := fifth_recurrence t f hf i j
  rw [hz, mul_zero] at h
  exact (mul_eq_zero.mp h).resolve_left
    (mul_ne_zero (by norm_num) (by exact_mod_cast (show i+1 ≠ 0 by omega)))

lemma fifth_affine_q_vanish (t : GateParameters K) (hβ : t.b₃+t.c₅ = 0)
    (f : Poly K) (hf : Static t f) (i j : ℕ) : bicoeff (i+1) (j+4) f = 0 := by
  have h := fifth_recurrence t f hf i j
  rw [hβ, zero_mul, zero_mul] at h
  exact (mul_eq_zero.mp h).resolve_left
    (mul_ne_zero (by norm_num) (by exact_mod_cast (show i+1 ≠ 0 by omega)))

/-- A static polynomial whose highest momentum degree is at least seven can
exist only on the locus where the gate symbol E vanishes identically. -/
theorem high_momentum_forces_symbol_zero (t : GateParameters K) (f : Poly K)
    (hf : Static t f) (n : ℕ) (hbound : Bounded ![0, 1] (n+7) f)
    (ha : bicoeff 0 (n+7) f ≠ 0) :
    t.b₃ = 0 ∧ t.c₅ = 0 ∧ t.b₁+t.c₃ = 0 ∧ 2*t.b₂+4*t.c₄ = 0 := by
  have z (i j : ℕ) (hj : n+7 < j) : bicoeff i j f = 0 :=
    bicoeff_vanish_of_bound hbound i j (by norm_num; exact_mod_cast hj)
  have z0 (i : ℕ) : bicoeff (i+1) (n+7) f = 0 := by
    simpa [Nat.add_assoc] using fifth_vanish t f hf i (n+3) (by simpa [Nat.add_assoc] using z i (n+8) (by omega))
  have z1 (i : ℕ) : bicoeff (i+2) (n+6) f = 0 := by
    simpa [Nat.add_assoc] using fifth_vanish t f hf (i+1) (n+2) (by simpa [Nat.add_assoc] using z0 i)
  have z2 (i : ℕ) : bicoeff (i+3) (n+5) f = 0 := by
    simpa [Nat.add_assoc] using fifth_vanish t f hf (i+2) (n+1) (by simpa [Nat.add_assoc] using z1 i)
  have z3 (i : ℕ) : bicoeff (i+4) (n+4) f = 0 := by
    simpa [Nat.add_assoc] using fifth_vanish t f hf (i+3) n (by simpa [Nat.add_assoc] using z2 i)
  have nz (r : ℕ) (hr : 0 < r) : (n : K) + r ≠ 0 := by
    exact_mod_cast (show n+r ≠ 0 by omega)
  have nz5 : (n : K)+5 ≠ 0 := by simpa using nz 5 (by decide)
  have nz6 : (n : K)+6 ≠ 0 := by simpa using nz 6 (by decide)
  have nz7 : (n : K)+7 ≠ 0 := by simpa using nz 7 (by decide)
  have hE := third_recurrence t f hf 2 (n+4)
  norm_num [Nat.add_assoc, z0 0, z0 1, z1 0, z1 1, z2 0, z3 1] at hE
  have hE2 : 3*t.b₃+10*t.c₅ = 0 := by
    simpa only [add_assoc, show (4 : K)+1=5 by norm_num, show (4 : K)+2=6 by norm_num, show (4 : K)+3=7 by norm_num, neg_eq_zero, mul_eq_zero, nz5, nz6,
      nz7, ha, false_or, or_false] using hE
  have hR := third_recurrence t f hf 0 (n+5)
  have hF := fifth_recurrence t f hf 0 (n+2)
  norm_num [Nat.add_assoc, z2 0, z0 0, z 0 (n+8) (by omega)] at hR hF
  have htop : (n+7 : K)*(n+6)*
      (2*(t.b₃+t.c₅)*(n+6)-t.b₃*(n+5))*bicoeff 0 (n+7) f = 0 := by
    linear_combination hR - 2*((n : K)+6)^2*hF
  have htop' : 2*(t.b₃+t.c₅)*(n+6)-t.b₃*(n+5) = 0 := by
    simpa only [mul_eq_zero, nz7, nz6, ha,
      false_or, or_false] using htop
  have hb : t.b₃ = 0 := top_coefficient_nonresonant t.b₃ t.c₅ (n+7) hE2 (by
    push_cast; linear_combination htop')
  have hc : t.c₅ = 0 := by simpa [hb] using hE2
  have vanish (i j : ℕ) : bicoeff (i+1) (j+4) f = 0 :=
    fifth_affine_q_vanish t (by rw [hb, hc]; ring) f hf i j
  have hA := third_recurrence t f hf 0 (n+4)
  have hB := third_recurrence t f hf 1 (n+4)
  norm_num [Nat.add_assoc, hb, hc, vanish 2 n, vanish 3 n,
    vanish 0 (n+1), vanish 1 (n+1), vanish 0 (n+2), vanish 1 (n+2),
    z0 0] at hA hB
  refine ⟨hb, hc, ?_, ?_⟩
  · simpa only [add_assoc, show (4 : K)+1=5 by norm_num, show (4 : K)+2=6 by norm_num, show (4 : K)+3=7 by norm_num, neg_eq_zero, mul_eq_zero, nz5, nz6,
      nz7, ha, false_or, or_false] using hA
  · simpa only [add_assoc, show (4 : K)+1=5 by norm_num, show (4 : K)+2=6 by norm_num, show (4 : K)+3=7 by norm_num, neg_eq_zero, mul_eq_zero, nz5, nz6,
      nz7, ha, false_or, or_false] using hB

/-- Every static solution has momentum degree at most six when E is nonzero.
There is no input support cutoff. -/
theorem static_momentum_bound (t : GateParameters K)
    (hE : ¬ (t.b₃ = 0 ∧ t.c₅ = 0 ∧ t.b₁+t.c₃ = 0 ∧ 2*t.b₂+4*t.c₄ = 0))
    (f : Poly K) (hf : Static t f) : Bounded ![0, 1] 6 f := by
  classical
  let m := degree ![0, 1] f
  have hb : Bounded ![0, 1] m f := bounded_degree _ f
  by_cases hm : m ≤ 6
  · exact bounded_mono hb (by exact_mod_cast hm)
  have hfn : f ≠ 0 := by intro hz; simp [m, degree, hz] at hm
  have hs : f.support.Nonempty := by simpa [Finset.nonempty_iff_ne_empty, support_eq_empty] using hfn
  obtain ⟨e, he, hmax⟩ := Finset.exists_mem_eq_sup f.support hs
    (fun e => (![0, 1] : Fin 2 → ℕ) 0 * e 0 + (![0, 1] : Fin 2 → ℕ) 1 * e 1)
  have hej : e 1 = m := by simpa [m, degree] using hmax.symm
  have hec : bicoeff (e 0) m f ≠ 0 := by
    simpa [bicoeff, ← hej, exponent_ext] using mem_support_iff.mp he
  obtain ⟨n, hn⟩ : ∃ n : ℕ, m = n+7 := ⟨m-7, by omega⟩
  have he0 : e 0 = 0 := by
    by_contra he0
    obtain ⟨i, hi⟩ : ∃ i : ℕ, e 0 = i+1 := ⟨e 0-1, by omega⟩
    apply hec
    rw [hi, hn]
    apply (show bicoeff (i+1) (n+7) f = 0 from ?_)
    have hz : bicoeff i (n+8) f = 0 := bicoeff_vanish_of_bound hb i (n+8) (by simp [hn])
    simpa [Nat.add_assoc] using fifth_vanish t f hf i (n+3) (by simpa [Nat.add_assoc] using hz)
  have ha : bicoeff 0 (n+7) f ≠ 0 := by simpa [he0, hn] using hec
  exact (hE (high_momentum_forces_symbol_zero t f hf n (by simpa [hn] using hb) ha)).elim


/-- A convenient common bound (not claimed sharp). It is enough to derive
finite-dimensionality and follows from the third recurrence alone. -/
theorem static_weight_bound_of_momentum_bound (t : GateParameters K) (f : Poly K)
    (hf : Static t f) (M : ℕ) (hP : Bounded ![0, 1] M f) :
    Bounded ![1, 3] (3*M+2) f := by
  classical
  let d := degree ![1, 3] f
  have hd : Bounded ![1, 3] d f := bounded_degree _ f
  by_cases hle : d ≤ 3*M+2
  · exact bounded_mono hd (by exact_mod_cast hle)
  have hf0 : f ≠ 0 := by intro hz; simp [d, degree, hz] at hle
  have hs : f.support.Nonempty := by simpa [Finset.nonempty_iff_ne_empty, support_eq_empty] using hf0
  obtain ⟨e, he, hmax⟩ := Finset.exists_mem_eq_sup f.support hs
    (fun e => (![1, 3] : Fin 2 → ℕ) 0 * e 0 + (![1, 3] : Fin 2 → ℕ) 1 * e 1)
  have hweight : e 0 + 3*e 1 = d := by simpa [d, degree] using hmax.symm
  have hp : e 1 ≤ M := by
    have := hP e (mem_support_iff.mp he)
    norm_num [weight_pair] at this
    exact_mod_cast this
  obtain ⟨i, hi⟩ : ∃ i : ℕ, e 0 = i+3 := ⟨e 0-3, by omega⟩
  let j := e 1
  have hij : i+3+3*j = d := by simpa [j, hi] using hweight
  have hc : bicoeff (i+3) j f ≠ 0 := by
    simpa [bicoeff, ← hi, j, exponent_ext] using mem_support_iff.mp he
  have zero (r s : ℕ) (hrs : d < r+3*s) : bicoeff r s f = 0 :=
    bicoeff_vanish_of_bound hd r s (by norm_num; exact_mod_cast hrs)
  have h := third_recurrence t f hf i j
  have z1 := zero (i+1) (j+1) (by omega)
  have z2 := zero (i+1) (j+2) (by omega)
  have z3 := zero i (j+2) (by omega)
  have z4 := zero i (j+3) (by omega)
  have z5 := zero (i-1) (j+3) (by omega)
  have z6 := zero (i-2) (j+3) (by omega)
  simp only [z1, z2, z3, z4, z5, z6, ite_self, mul_zero, add_zero, sub_zero] at h
  have n1 : (i : K)+1 ≠ 0 := by exact_mod_cast (show i+1 ≠ 0 by omega)
  have n2 : (i : K)+2 ≠ 0 := by exact_mod_cast (show i+2 ≠ 0 by omega)
  have n3 : (i : K)+3 ≠ 0 := by exact_mod_cast (show i+3 ≠ 0 by omega)
  exact ((mul_ne_zero (mul_ne_zero (mul_ne_zero n1 n2) n3) hc) h).elim

/-- Any uniform bound with positive variable weights gives a finite-dimensional
polynomial subspace. This is proved by an injective finite coefficient map. -/
theorem finite_dimensional_of_weight_bound (w : Fin 2 → ℕ) (hw : ∀ i, 0 < w i)
    (N : ℕ) (V : Submodule K (Poly K)) (hV : ∀ f ∈ V, Bounded w N f) :
    FiniteDimensional K V := by
  classical
  let L : V →ₗ[K] ((Fin (N+1) × Fin (N+1)) → K) :=
    { toFun := fun f ij => bicoeff ij.1 ij.2 f.val
      map_add' := by intros; ext; simp
      map_smul' := by intros; ext; simp [bicoeff, coeff_smul] }
  apply FiniteDimensional.of_injective L
  intro f g hfg
  apply Subtype.ext
  ext m
  by_cases hm : m 0 ≤ N ∧ m 1 ≤ N
  · have h := congrFun hfg (⟨m 0, by omega⟩, ⟨m 1, by omega⟩)
    simpa [L, bicoeff, exponent_ext] using h
  · have vanish (p : V) : coeff m p.val = 0 := by
      by_contra hc
      have h := hV p.val p.property m hc
      rw [weight_pair] at h
      have h0 := hw 0
      have h1 := hw 1
      have q : (m 0 : ℤ) ≤ (w 0 : ℤ)*m 0 := by exact_mod_cast (Nat.le_mul_of_pos_left (m 0) h0)
      have p : (m 1 : ℤ) ≤ (w 1 : ℤ)*m 1 := by exact_mod_cast (Nat.le_mul_of_pos_left (m 1) h1)
      have qn : (0 : ℤ) ≤ m 0 := by positivity
      have pn : (0 : ℤ) ≤ m 1 := by positivity
      have hM : m 0 ≤ N ∧ m 1 ≤ N := by
        constructor
        · exact_mod_cast (by omega : (m 0 : ℤ) ≤ N)
        · exact_mod_cast (by omega : (m 1 : ℤ) ≤ N)
      exact hm hM
    rw [vanish f, vanish g]

/-- The whole static sector is finite-dimensional off E=0. -/
theorem static_subspace_finite_dimensional (t : GateParameters K)
    (hE : ¬ (t.b₃ = 0 ∧ t.c₅ = 0 ∧ t.b₁+t.c₃ = 0 ∧ 2*t.b₂+4*t.c₄ = 0))
    (V : Submodule K (Poly K)) (hV : ∀ f ∈ V, Static t f) : FiniteDimensional K V := by
  apply finite_dimensional_of_weight_bound ![1, 3] (by intro i; fin_cases i <;> norm_num) 20 V
  intro f hf
  exact static_weight_bound_of_momentum_bound t f (hV f hf) 6
    (static_momentum_bound t hE f (hV f hf))

end SexticC3.CubeLeading.Polynomial
