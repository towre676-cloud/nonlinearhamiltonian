import SexticC3.CubeLeadingCoprime
import SexticC3.CubeLeadingFiltration

/-!
# Concrete K3 and K4 for all three cube-leading Newton forms

K4 allows any strictly lower-weight polynomial perturbation and any finite-
dimensional space stable under its actual Hamiltonian bracket. This file does
not identify the Moyal static sector or exclude leading form h².
-/
noncomputable section
set_option linter.unusedSectionVars false
namespace SexticC3.CubeLeading.Polynomial
open MvPolynomial
variable {K : Type*} [Field K] [CharZero K]

lemma case_one_form (c : K) : (caseOne c).IsWeightedHomogeneous (weights ![3, 5]) 15 := by
  apply (form_iff _ _ _).mp
  simp [euler, caseOne, pderiv_pow, pderiv_mul, pderiv_C_mul, pderiv_X, Pi.single_apply]
  ring

lemma case_two_form (c : K) : (caseTwo c).IsWeightedHomogeneous (weights ![2, 3]) 9 := by
  apply (form_iff _ _ _).mp
  simp [euler, caseTwo, pderiv_pow, pderiv_mul, pderiv_C_mul, pderiv_X, Pi.single_apply]
  ring

lemma case_three_form (c : K) : (caseThree c).IsWeightedHomogeneous (weights ![3, 4]) 12 := by
  apply (form_iff _ _ _).mp
  simp [euler, caseThree, pderiv_pow, pderiv_mul, pderiv_C_mul, pderiv_X, Pi.single_apply]
  ring

theorem case_one_no_slice (c : K) (hc : c ≠ 0) (f : Poly K) (n : ℤ)
    (hf : f.IsWeightedHomogeneous (weights ![3, 5]) n) (r : ℕ)
    (hr : (bracket (caseOne c))^[r] f = 0) :
    ∃ (k : ℕ) (a : K), f = C a * (caseOne c)^k :=
  polynomial_no_slice ![3, 5] (by intro i; fin_cases i <;> norm_num)
    _ 15 (case_one_form c) (by norm_num) (binomial_ne_zero c 5 (by decide))
    (case_one_coprime c hc) f n hf r hr

theorem case_two_no_slice (c : K) (hc : c ≠ 0) (f : Poly K) (n : ℤ)
    (hf : f.IsWeightedHomogeneous (weights ![2, 3]) n) (r : ℕ)
    (hr : (bracket (caseTwo c))^[r] f = 0) :
    ∃ (k : ℕ) (a : K), f = C a * (caseTwo c)^k :=
  polynomial_no_slice ![2, 3] (by intro i; fin_cases i <;> norm_num)
    _ 9 (case_two_form c) (by norm_num) (linear_cubic_ne_zero c)
    (case_two_coprime c hc) f n hf r hr

theorem case_three_no_slice (c : K) (hc : c ≠ 0) (f : Poly K) (n : ℤ)
    (hf : f.IsWeightedHomogeneous (weights ![3, 4]) n) (r : ℕ)
    (hr : (bracket (caseThree c))^[r] f = 0) :
    ∃ (k : ℕ) (a : K), f = C a * (caseThree c)^k :=
  polynomial_no_slice ![3, 4] (by intro i; fin_cases i <;> norm_num)
    _ 12 (case_three_form c) (by norm_num) (binomial_ne_zero c 4 (by decide))
    (case_three_coprime c hc) f n hf r hr

theorem stable_space_of_lower_terms (w : Fin 2 → ℕ) (hw : ∀ i, 0 < w i)
    (h lower : Poly K) (d : ℤ) (hh : h.IsWeightedHomogeneous (weights w) d)
    (hlower : Bounded w (d - 1) lower) (hd : (w 0 : ℤ) + w 1 < d)
    (hh0 : h ≠ 0) (hrel : IsRelPrime h (pderiv 1 h))
    (V : Submodule K (Poly K)) [FiniteDimensional K V]
    (hV : ∀ f ∈ V, bracket (h + lower) f ∈ V) :
    ∀ f ∈ V, ∃ (k : ℕ) (a : K), leadingForm w f = C a * h^k := by
  have hbound : Bounded w d (h + lower) :=
    (boundedSubmodule (K := K) w d).add_mem (bounded_of_homogeneous hh)
      (bounded_mono hlower (by omega))
  have htop : component w d (h + lower) = h := by
    rw [map_add, hh.weightedHomogeneousComponent_same,
      component_beyond_bound hlower (by omega), add_zero]
  exact polynomial_leading_forms_of_stable w hw _ h d hbound htop hd hh0 hrel V hV

theorem case_one_stable (c : K) (hc : c ≠ 0) (lower : Poly K)
    (hlower : Bounded ![3, 5] 14 lower)
    (V : Submodule K (Poly K)) [FiniteDimensional K V]
    (hV : ∀ f ∈ V, bracket (caseOne c + lower) f ∈ V) :
    ∀ f ∈ V, ∃ (k : ℕ) (a : K), leadingForm ![3, 5] f = C a * (caseOne c)^k :=
  stable_space_of_lower_terms ![3, 5] (by intro i; fin_cases i <;> norm_num)
    _ lower 15 (case_one_form c) hlower (by norm_num)
    (binomial_ne_zero c 5 (by decide)) (case_one_coprime c hc) V hV

theorem case_two_stable (c : K) (hc : c ≠ 0) (lower : Poly K)
    (hlower : Bounded ![2, 3] 8 lower)
    (V : Submodule K (Poly K)) [FiniteDimensional K V]
    (hV : ∀ f ∈ V, bracket (caseTwo c + lower) f ∈ V) :
    ∀ f ∈ V, ∃ (k : ℕ) (a : K), leadingForm ![2, 3] f = C a * (caseTwo c)^k :=
  stable_space_of_lower_terms ![2, 3] (by intro i; fin_cases i <;> norm_num)
    _ lower 9 (case_two_form c) hlower (by norm_num)
    (linear_cubic_ne_zero c) (case_two_coprime c hc) V hV

theorem case_three_stable (c : K) (hc : c ≠ 0) (lower : Poly K)
    (hlower : Bounded ![3, 4] 11 lower)
    (V : Submodule K (Poly K)) [FiniteDimensional K V]
    (hV : ∀ f ∈ V, bracket (caseThree c + lower) f ∈ V) :
    ∀ f ∈ V, ∃ (k : ℕ) (a : K), leadingForm ![3, 4] f = C a * (caseThree c)^k :=
  stable_space_of_lower_terms ![3, 4] (by intro i; fin_cases i <;> norm_num)
    _ lower 12 (case_three_form c) hlower (by norm_num)
    (binomial_ne_zero c 4 (by decide)) (case_three_coprime c hc) V hV

end SexticC3.CubeLeading.Polynomial
