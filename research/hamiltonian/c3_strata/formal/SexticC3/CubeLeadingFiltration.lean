import SexticC3.CubeLeadingPolynomial

/-!
# Weighted polynomial filtration and the concrete stable-space lemma K4

Bounds, homogeneous components and leading forms refer to actual finite
polynomial supports. Finite-dimensionality supplies the bound used in K4.
-/
noncomputable section
set_option linter.unusedSectionVars false
namespace SexticC3.CubeLeading.Polynomial
open MvPolynomial
variable {K : Type*} [Field K] [CharZero K]

def Bounded (w : Fin 2 → ℕ) (n : ℤ) (f : Poly K) : Prop :=
  ∀ m, coeff m f ≠ 0 → Finsupp.weight (weights w) m ≤ n

def boundedSubmodule (w : Fin 2 → ℕ) (n : ℤ) : Submodule K (Poly K) where
  carrier := Bounded w n
  zero_mem' := by intro m hm; simp at hm
  add_mem' := by
    intro f g hf hg m hm
    by_cases hfm : coeff m f = 0
    · apply hg m
      simpa [coeff_add, hfm] using hm
    · exact hf m hfm
  smul_mem' := by
    intro c f hf m hm
    apply hf m
    intro he
    simp [coeff_smul, he] at hm

lemma bounded_mono {w : Fin 2 → ℕ} {a b : ℤ} {f : Poly K}
    (hf : Bounded w a f) (hab : a ≤ b) : Bounded w b f :=
  fun m hm => le_trans (hf m hm) hab

lemma bounded_of_homogeneous {w : Fin 2 → ℕ} {n : ℤ} {f : Poly K}
    (hf : f.IsWeightedHomogeneous (weights w) n) : Bounded w n f :=
  fun _ hm => le_of_eq (hf hm)

lemma bounded_mul {w : Fin 2 → ℕ} {a b : ℤ} {f g : Poly K}
    (hf : Bounded w a f) (hg : Bounded w b g) : Bounded w (a + b) (f * g) := by
  classical
  intro m hm
  rw [coeff_mul] at hm
  obtain ⟨⟨x, y⟩, hxy, hc⟩ := Finset.exists_ne_zero_of_sum_ne_zero hm
  have hx := hf x (left_ne_zero_of_mul hc)
  have hy := hg y (right_ne_zero_of_mul hc)
  rw [← Finset.mem_antidiagonal.mp hxy, map_add]
  change Finsupp.weight (weights w) x + Finsupp.weight (weights w) y ≤ a + b
  omega

lemma bounded_pderiv {w : Fin 2 → ℕ} {n : ℤ} {f : Poly K}
    (hf : Bounded w n f) (i : Fin 2) : Bounded w (n - w i) (pderiv i f) := by
  classical
  conv_rhs => rw [f.as_sum, map_sum]
  apply (boundedSubmodule w (n - w i)).sum_mem
  intro m hm
  have hmon := isWeightedHomogeneous_monomial (weights w) m (coeff m f) rfl
  have hd := hmon.pderiv (i := i) (n' := Finsupp.weight (weights w) m - w i)
    (by simp [weights])
  apply bounded_mono (bounded_of_homogeneous hd)
  have := hf m (mem_support_iff.mp hm)
  omega

abbrev component (w : Fin 2 → ℕ) (n : ℤ) : Poly K →ₗ[K] Poly K :=
  weightedHomogeneousComponent (weights w) n

lemma component_pderiv (w : Fin 2 → ℕ) (n : ℤ) (i : Fin 2) (f : Poly K) :
    component w (n - w i) (pderiv i f) = pderiv i (component w n f) := by
  classical
  induction f using MvPolynomial.induction_on' with
  | monomial m c =>
    have hm := isWeightedHomogeneous_monomial (weights w) m c rfl
    have hd := hm.pderiv (i := i) (n' := Finsupp.weight (weights w) m - w i)
      (by simp [weights])
    rw [weightedHomogeneousComponent_of_mem hd, weightedHomogeneousComponent_of_mem hm]
    by_cases he : n = Finsupp.weight (weights w) m
    · simp [he]
    · simp [he, sub_left_inj]
  | add f g hf hg => simp only [map_add, hf, hg]

lemma component_mul_top {w : Fin 2 → ℕ} {a b : ℤ} {f g : Poly K}
    (hf : Bounded w a f) (hg : Bounded w b g) :
    component w (a + b) (f * g) = component w a f * component w b g := by
  classical
  ext m
  simp only [component, coeff_weightedHomogeneousComponent, coeff_mul]
  by_cases he : Finsupp.weight (weights w) m = a + b
  · rw [if_pos he]
    apply Finset.sum_congr rfl
    intro xy hxy
    by_cases hx : coeff xy.1 f = 0
    · simp [hx]
    by_cases hy : coeff xy.2 g = 0
    · simp [hy]
    have ha := hf xy.1 hx
    have hb := hg xy.2 hy
    have he' : Finsupp.weight (weights w) xy.1 + Finsupp.weight (weights w) xy.2 = a + b := by
      rw [← map_add, Finset.mem_antidiagonal.mp hxy, he]
    have hx' : Finsupp.weight (weights w) xy.1 = a := by omega
    have hy' : Finsupp.weight (weights w) xy.2 = b := by omega
    simp [hx', hy']
  · rw [if_neg he]
    symm
    apply Finset.sum_eq_zero
    intro xy hxy
    by_cases hx : Finsupp.weight (weights w) xy.1 = a
    · have hy : Finsupp.weight (weights w) xy.2 ≠ b := by
        intro hy
        apply he
        rw [← Finset.mem_antidiagonal.mp hxy, map_add, hx, hy]
      simp [hy]
    · simp [hx]

lemma bounded_bracket {w : Fin 2 → ℕ} {d n : ℤ} {H f : Poly K}
    (hH : Bounded w d H) (hf : Bounded w n f) :
    Bounded w (n + (d - w 0 - w 1)) (bracket H f) := by
  have ha := bounded_mul (bounded_pderiv hH 0) (bounded_pderiv hf 1)
  have hb := bounded_mul (bounded_pderiv hH 1) (bounded_pderiv hf 0)
  have ea : d - w 0 + (n - w 1) = n + (d - w 0 - w 1) := by ring
  have eb : d - w 1 + (n - w 0) = n + (d - w 0 - w 1) := by ring
  rw [ea] at ha
  rw [eb] at hb
  exact (boundedSubmodule (K := K) w (n + (d - w 0 - w 1))).sub_mem ha hb

/-- Top-weight transport for the actual Poisson bracket, including arbitrary lower terms. -/
theorem component_bracket_top {w : Fin 2 → ℕ} {d n : ℤ} {H f : Poly K}
    (hH : Bounded w d H) (hf : Bounded w n f) :
    component w (n + (d - w 0 - w 1)) (bracket H f) =
      bracket (component w d H) (component w n f) := by
  have ea : n + (d - w 0 - w 1) = (d - w 0) + (n - w 1) := by ring
  have eb : n + (d - w 0 - w 1) = (d - w 1) + (n - w 0) := by ring
  unfold bracket
  rw [map_sub]
  conv_lhs => lhs; rw [ea, component_mul_top (bounded_pderiv hH 0) (bounded_pderiv hf 1)]
  conv_lhs => rhs; rw [eb, component_mul_top (bounded_pderiv hH 1) (bounded_pderiv hf 0)]
  simp only [component_pderiv]

def degree (w : Fin 2 → ℕ) (f : Poly K) : ℕ :=
  f.support.sup (fun m => w 0 * m 0 + w 1 * m 1)

lemma bounded_degree (w : Fin 2 → ℕ) (f : Poly K) : Bounded w (degree w f) f := by
  intro m hm
  have he : w 0 * m 0 + w 1 * m 1 ≤ degree w f :=
    Finset.le_sup (f := fun m => w 0 * m 0 + w 1 * m 1) (mem_support_iff.mpr hm)
  rw [weight_pair]
  exact_mod_cast he

/-- This bound is derived from finite-dimensionality, not supplied by the caller. -/
theorem finite_dimensional_bounded (w : Fin 2 → ℕ) (V : Submodule K (Poly K))
    [FiniteDimensional K V] : ∃ N : ℤ, ∀ f ∈ V, Bounded w N f := by
  classical
  obtain ⟨s, hs⟩ := (V.fg_iff_finiteDimensional.mpr inferInstance)
  let N := s.sup (degree w)
  refine ⟨N, ?_⟩
  have hle : V ≤ boundedSubmodule w N := by
    rw [← hs]
    apply Submodule.span_le.mpr
    intro f hf
    exact bounded_mono (bounded_degree w f) (by exact_mod_cast (Finset.le_sup hf : degree w f ≤ N))
  exact fun f hf => hle hf

lemma component_beyond_bound {w : Fin 2 → ℕ} {N n : ℤ} {f : Poly K}
    (hf : Bounded w N f) (hn : N < n) : component w n f = 0 := by
  classical
  ext m
  rw [coeff_weightedHomogeneousComponent, coeff_zero]
  split_ifs with hm
  · by_contra hc
    have := hf m hc
    omega
  · rfl

/-- The highest weighted component, defined from the actual support. -/
def leadingForm (w : Fin 2 → ℕ) (f : Poly K) : Poly K :=
  component w (degree w f) f

lemma leadingForm_ne_zero (w : Fin 2 → ℕ) (f : Poly K) (hf : f ≠ 0) :
    leadingForm w f ≠ 0 := by
  classical
  have hs : f.support.Nonempty := by
    simpa [Finset.nonempty_iff_ne_empty, support_eq_empty] using hf
  obtain ⟨m, hm, he⟩ := Finset.exists_mem_eq_sup f.support hs
    (fun m => w 0 * m 0 + w 1 * m 1)
  intro hz
  have hc := congrArg (coeff m) hz
  have he' : Finsupp.weight (weights w) m = (degree w f : ℤ) := by
    rw [weight_pair]
    exact_mod_cast he.symm
  simp [leadingForm, coeff_weightedHomogeneousComponent, he', mem_support_iff.mp hm] at hc

/-- K4 for a genuine finite-dimensional polynomial space stable under the actual
Hamiltonian bracket. Neither boundedness nor leading-operator compatibility is assumed. -/
theorem polynomial_leading_forms_of_stable
    (w : Fin 2 → ℕ) (hw : ∀ i, 0 < w i) (H h : Poly K) (d : ℤ)
    (hH : Bounded w d H) (htop : component w d H = h)
    (hd : (w 0 : ℤ) + w 1 < d) (hh0 : h ≠ 0)
    (hrel : IsRelPrime h (pderiv 1 h))
    (V : Submodule K (Poly K)) [FiniteDimensional K V]
    (hV : ∀ f ∈ V, bracket H f ∈ V) :
    ∀ f ∈ V, ∃ (k : ℕ) (c : K), leadingForm w f = C c * h^k := by
  intro f hf
  obtain ⟨N, hN⟩ := finite_dimensional_bounded w V
  let δ : ℤ := d - w 0 - w 1
  let n : ℤ := degree w f
  have hδ : 0 < δ := by dsimp [δ]; omega
  have claim : ∀ m : ℕ,
      (bracket H)^[m] f ∈ V ∧
      Bounded w (n + m * δ) ((bracket H)^[m] f) ∧
      component w (n + m * δ) ((bracket H)^[m] f) =
        (bracket h)^[m] (leadingForm w f) := by
    intro m
    induction m with
    | zero =>
      simp only [Function.iterate_zero, id_eq, Nat.cast_zero, zero_mul, add_zero]
      exact ⟨hf, bounded_degree w f, rfl⟩
    | succ m ih =>
      obtain ⟨hmem, hbound, hcomp⟩ := ih
      have he : n + ((m + 1 : ℕ) : ℤ) * δ = (n + m * δ) + (d - w 0 - w 1) := by
        dsimp [δ]; push_cast; ring
      rw [Function.iterate_succ_apply', he]
      refine ⟨hV _ hmem, bounded_bracket hH hbound, ?_⟩
      rw [component_bracket_top hH hbound, htop, hcomp, Function.iterate_succ_apply']
  let m := (N - n).toNat + 1
  obtain ⟨hmem, _, hcomp⟩ := claim m
  have hlarge : N < n + (m : ℤ) * δ := by
    have hnat := Int.self_le_toNat (N - n)
    have hnonneg : (0 : ℤ) ≤ (N - n).toNat := by positivity
    dsimp [m]
    push_cast
    nlinarith
  have hnil : (bracket h)^[m] (leadingForm w f) = 0 := by
    rw [← hcomp]
    exact component_beyond_bound (hN _ hmem) hlarge
  have hh : h.IsWeightedHomogeneous (weights w) d := by
    rw [← htop]
    exact weightedHomogeneousComponent_isWeightedHomogeneous _ _
  exact polynomial_no_slice w hw h d hh hd hh0 hrel (leadingForm w f) n
    (weightedHomogeneousComponent_isWeightedHomogeneous _ _) m hnil

/-- Nonzero elements have a nonzero scalar leading coefficient. -/
theorem polynomial_leading_forms_of_stable_nonzero
    (w : Fin 2 → ℕ) (hw : ∀ i, 0 < w i) (H h : Poly K) (d : ℤ)
    (hH : Bounded w d H) (htop : component w d H = h)
    (hd : (w 0 : ℤ) + w 1 < d) (hh0 : h ≠ 0)
    (hrel : IsRelPrime h (pderiv 1 h))
    (V : Submodule K (Poly K)) [FiniteDimensional K V]
    (hV : ∀ f ∈ V, bracket H f ∈ V) (f : Poly K) (hf : f ∈ V) (hf0 : f ≠ 0) :
    ∃ (k : ℕ) (c : K), c ≠ 0 ∧ leadingForm w f = C c * h^k := by
  obtain ⟨k, c, he⟩ := polynomial_leading_forms_of_stable w hw H h d hH htop hd hh0 hrel V hV f hf
  refine ⟨k, c, ?_, he⟩
  intro hc
  apply leadingForm_ne_zero w f hf0
  simp [he, hc]


end SexticC3.CubeLeading.Polynomial
