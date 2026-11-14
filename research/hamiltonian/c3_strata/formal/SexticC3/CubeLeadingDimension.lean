import SexticC3.CubeLeadingCutoff
import SexticC3.CubeLeadingSquare
import Mathlib.Algebra.GeomSum

/-! # The final leading-form dimension argument, in the polynomial ring. -/
noncomputable section
set_option linter.unusedSectionVars false
namespace SexticC3.CubeLeading.Polynomial
open MvPolynomial
variable {K : Type*} [Field K] [CharZero K]

lemma bounded_component {w v : Fin 2 → ℕ} {N n : ℤ} {f : Poly K}
    (hf : Bounded v N f) : Bounded v N (component w n f) := by
  intro m hm
  apply hf m
  contrapose! hm
  simp [coeff_weightedHomogeneousComponent, hm]

lemma pure_momentum_power_coeff (h : Poly K) (hq : X 0 ∣ h-X 1^3) (k : ℕ) :
    bicoeff 0 (3*k) (h^k) = 1 := by
  obtain ⟨g, hg⟩ := hq.trans (sub_dvd_pow_sub_pow h (X 1^3) k)
  have hc := congrArg (bicoeff 0 (3*k)) hg
  simp only [bicoeff_sub, bicoeff_q_mul, if_pos rfl] at hc
  have hp : bicoeff 0 (3*k) (((X 1 : Poly K)^3)^k) = 1 := by
    rw [← pow_mul]
    simp [bicoeff, coeff_X_pow, exponent]
  simp only [hp, ite_true] at hc
  linear_combination hc

lemma leading_power_le_two (w : Fin 2 → ℕ) (f h : Poly K)
    (hP : Bounded ![0, 1] 6 f) (hq : X 0 ∣ h-X 1^3)
    (k : ℕ) (a : K) (ha : a ≠ 0) (he : leadingForm w f = C a*h^k) : k ≤ 2 := by
  have hb : Bounded ![0, 1] 6 (C a*h^k) := by
    rw [← he]; exact bounded_component hP
  have hc : bicoeff 0 (3*k) (C a*h^k) ≠ 0 := by
    rw [bicoeff_C_mul, pure_momentum_power_coeff h hq k, mul_one]; exact ha
  have hn := hb (exponent 0 (3*k)) hc
  norm_num [weight_pair] at hn
  omega

lemma degree_of_leading_form (w : Fin 2 → ℕ) (f g : Poly K) (n : ℤ)
    (he : leadingForm w f = g) (hg : g.IsWeightedHomogeneous (weights w) n)
    (hg0 : g ≠ 0) : (degree w f : ℤ) = n := by
  obtain ⟨m, hm⟩ := MvPolynomial.ne_zero_iff.mp hg0
  have hfm : coeff m (leadingForm w f) ≠ 0 := by rwa [he]
  have hh : (leadingForm w f).IsWeightedHomogeneous (weights w) (degree w f) :=
    weightedHomogeneousComponent_isWeightedHomogeneous _ _
  exact (hh hfm).symm.trans (hg hm)

lemma bounded_component_zero {w : Fin 2 → ℕ} {n : ℤ} {f : Poly K}
    (hb : Bounded w n f) (hz : component w n f = 0) : Bounded w (n-1) f := by
  intro m hm
  have hle := hb m hm
  have hne : Finsupp.weight (weights w) m ≠ n := by
    intro hn
    have hc := congrArg (coeff m) hz
    exact hm (by simpa [coeff_weightedHomogeneousComponent, hn] using hc)
  omega

lemma bounded_zero_constant (w : Fin 2 → ℕ) (hw : ∀ i, 0 < w i)
    (f : Poly K) (hf : Bounded w 0 f) : f = C (coeff 0 f) := by
  apply weight_zero_constant w hw f
  have hh : f.IsWeightedHomogeneous (weights w) 0 := by
    intro m hm
    have hn := hf m hm
    rw [weight_pair] at hn ⊢
    have hp : (0 : ℤ) ≤ (w 0 : ℤ)*m 0+(w 1 : ℤ)*m 1 := by positivity
    omega
  simpa using (form_iff w f 0).mpr hh

/-- Cancellation of the highest component proves the full space equality.
The leading-form alternatives are used for all members, including the
remainders after subtracting a multiple of H. -/
theorem space_eq_span_of_two_leading_forms
    (w : Fin 2 → ℕ) (hw : ∀ i, 0 < w i) (H h : Poly K) (d : ℤ)
    (hH : Bounded w d H) (htop : component w d H = h) (hh0 : h ≠ 0)
    (V : Submodule K (Poly K)) (h1 : (1 : Poly K) ∈ V) (hmem : H ∈ V)
    (hlead : ∀ f ∈ V, f ≠ 0 → ∃ a : K, a ≠ 0 ∧
      (leadingForm w f = C a ∨ leadingForm w f = C a*h)) :
    V = Submodule.span K ({1, H} : Set (Poly K)) := by
  have hh : h.IsWeightedHomogeneous (weights w) d := by
    rw [← htop]; exact weightedHomogeneousComponent_isWeightedHomogeneous _ _
  let W := Submodule.span K ({1, H} : Set (Poly K))
  have w1 : (1 : Poly K) ∈ W := Submodule.subset_span (by simp)
  have wH : H ∈ W := Submodule.subset_span (by simp)
  have cmem (a : K) : C a ∈ W := by simpa [← C_mul'] using W.smul_mem a w1
  have mulmem (a : K) : C a*H ∈ W := by simpa [C_mul'] using W.smul_mem a wH
  have claim : ∀ n : ℕ, ∀ f ∈ V, degree w f = n → f ∈ W := by
    intro n
    induction n using Nat.strong_induction_on with
    | h n ih =>
      intro f hf hdeg
      by_cases hf0 : f = 0
      · rw [hf0]; exact W.zero_mem
      obtain ⟨a, ha, hlead | hlead⟩ := hlead f hf hf0
      · have hb := (leadingForm_data w f (C a) 0 hlead
          (isWeightedHomogeneous_C _ _) (by simpa using ha)).1
        rw [bounded_zero_constant w hw f hb]
        exact cmem _
      · have hhom := constant_mul_homogeneous w d a h hh
        have hc : C a*h ≠ 0 := mul_ne_zero (by simpa using ha) hh0
        have hdn := degree_of_leading_form w f _ d hlead hhom hc
        obtain ⟨hb, ht⟩ := leadingForm_data w f _ d hlead hhom hc
        let r := f-C a*H
        have hrV : r ∈ V := V.sub_mem hf (by simpa [C_mul'] using V.smul_mem a hmem)
        have hcH : C a*H ∈ boundedSubmodule w d := by
          rw [C_mul']; exact (boundedSubmodule (K := K) w d).smul_mem a hH
        have hrb : Bounded w d r := by
          change f-C a*H ∈ boundedSubmodule w d
          exact (boundedSubmodule (K := K) w d).sub_mem hb hcH
        have hrt : component w d r = 0 := by
          dsimp [r]
          rw [map_sub]
          have hcm : component w d (C a*H) = C a*h := by
            simpa [C_mul'] using (component w d).map_smul a H
              |>.trans (by rw [htop])
          rw [ht, hcm, sub_self]
        have hrW : r ∈ W := by
          by_cases hr0 : r = 0
          · rw [hr0]; exact W.zero_mem
          have hrlt : degree w r < n := by
            by_contra hn
            have hn' : d-1 < (degree w r : ℤ) := by rw [hdeg] at hdn; omega
            exact leadingForm_ne_zero w r hr0
              (component_beyond_bound (bounded_component_zero hrb hrt) hn')
          exact ih (degree w r) hrlt r hrV rfl
        have hsum := W.add_mem hrW (mulmem a)
        simpa [r] using hsum
  apply le_antisymm
  · intro f hf; exact claim _ f hf rfl
  · apply Submodule.span_le.mpr
    intro f hf
    simp only [Set.mem_insert_iff, Set.mem_singleton_iff] at hf
    rcases hf with rfl | rfl <;> assumption

/-- The dimension argument with its polynomial cutoff and square obstruction
made explicit. Finite-dimensionality is already derived from staticity. -/
theorem static_stable_space_eq_span
    (t : GateParameters K) (w : Fin 2 → ℕ) (hw : ∀ i, 0 < w i)
    (H h : Poly K) (d : ℤ) (hH : Bounded w d H) (htop : component w d H = h)
    (hd : (w 0 : ℤ)+w 1 < d) (hh0 : h ≠ 0) (hrel : IsRelPrime h (pderiv 1 h))
    (hq : X 0 ∣ h-X 1^3) (V : Submodule K (Poly K))
    (h1 : (1 : Poly K) ∈ V) (hmem : H ∈ V)
    (hstatic : ∀ f ∈ V, Static t f) (hP : ∀ f ∈ V, Bounded ![0, 1] 6 f)
    (hstable : ∀ f ∈ V, bracket H f ∈ V)
    (hsquare : ∀ f ∈ V, ∀ a : K, a ≠ 0 → leadingForm w f ≠ C a*h^2) :
    V = Submodule.span K ({1, H} : Set (Poly K)) := by
  letI : FiniteDimensional K V := finite_dimensional_of_weight_bound ![1, 3]
    (by intro i; fin_cases i <;> norm_num) 20 V
    (fun f hf => static_weight_bound_of_momentum_bound t f (hstatic f hf) 6 (hP f hf))
  apply space_eq_span_of_two_leading_forms w hw H h d hH htop hh0 V h1 hmem
  intro f hf hf0
  obtain ⟨k, a, ha, he⟩ := polynomial_leading_forms_of_stable_nonzero
    w hw H h d hH htop hd hh0 hrel V hstable f hf hf0
  have hk := leading_power_le_two w f h (hP f hf) hq k a ha he
  have hk2 : k ≠ 2 := by intro h2; subst k; exact hsquare f hf a ha he
  refine ⟨a, ha, ?_⟩
  have : k = 0 ∨ k = 1 := by omega
  rcases this with rfl | rfl
  · left; simpa using he
  · right; simpa using he

end SexticC3.CubeLeading.Polynomial
