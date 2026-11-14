import SexticC3.CubeLeadingSevenEliminateB2
import SexticC3.CubeLeadingSevenEliminateC3
import SexticC3.CubeLeadingSevenEliminateC2
import SexticC3.CubeLeadingSevenReconstruction

/-! The all-degree persistent core on the seven-parameter stratum. -/
noncomputable section
set_option linter.unusedSectionVars false
namespace SexticC3.CubeLeading.Polynomial
open MvPolynomial
variable {K : Type*} [Field K] [CharZero K]

@[simp] lemma bicoeff_C (i j : ℕ) (a : K) :
    bicoeff i j (C a) = if 0=i ∧ 0=j then a else 0 := by
  rw [show C a = monomial (exponent 0 0) a by simp [exponent]]
  exact bicoeff_monomial _ _ _ _ _

lemma constants_hamiltonian_mem (t : HamiltonianParameters K) :
    1 ∈ persistentCore t ∧ hamiltonian t ∈ persistentCore t :=
  ⟨kernel_mem_persistentCore t 1 (one_static _) (by simp [bracket, pderiv_one]),
   kernel_mem_persistentCore t (hamiltonian t) (hamiltonian_static t) (by unfold bracket; ring)⟩

lemma seven_normalized_core_zero (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0)
    (hnon : t.b₂ ≠ 0 ∨ t.c₃ ≠ 0 ∨ t.c₂ ≠ 0)
    (f : Poly K) (hf : f ∈ persistentCore t)
    (h00 : bicoeff 0 0 f = 0) (h03 : bicoeff 0 3 f = 0) : f = 0 := by
  have hstatic := persistentCore_static t f hf
  have hP := seven_first_refinement_momentum_bound t hb h4 h5 hnon f hstatic
    (persistentCore_static t _ (persistentCore_stable t f hf))
  obtain ⟨x, rfl⟩ := seven_reconstruct_normalized t hb h4 h5 f hstatic hP h00 h03
  have hs := (mem_persistentCore t _).mp hf
  have hx : x = 0 := by
    by_cases hb2 : t.b₂ = 0
    · by_cases hc3 : t.c₃ = 0
      · have hc2 : t.c₂ ≠ 0 := by simpa [hb2, hc3] using hnon
        exact seven_c2_coordinates_zero t hb h4 h5 hb2 hc3 hc2 x hs
      · exact seven_c3_coordinates_zero t hb h4 h5 hb2 hc3 x hs
    · exact seven_b2_coordinates_zero t hb h4 h5 hb2 x hs
  simp [hx, sevenCombination]

/-- No normalization, finite support bound, or finite-dimensionality hypothesis
is supplied: the all-degree cutoff and exact row eliminations prove them. -/
theorem seven_persistent_core (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0)
    (hnon : t.b₂ ≠ 0 ∨ t.c₃ ≠ 0 ∨ t.c₂ ≠ 0) :
    persistentCore t = Submodule.span K ({1, hamiltonian t} : Set (Poly K)) := by
  obtain ⟨h1, hH⟩ := constants_hamiltonian_mem t
  have hC (a : K) : C a ∈ persistentCore t := by
    simpa only [← C_mul', mul_one] using (persistentCore t).smul_mem a h1
  apply le_antisymm
  · intro f hf
    let b := bicoeff 0 3 f
    let a := bicoeff 0 0 f-b*t.c₀
    let g := f-C b*hamiltonian t-C a
    have hg : g ∈ persistentCore t := (persistentCore t).sub_mem
      ((persistentCore t).sub_mem hf (by simpa only [C_mul'] using (persistentCore t).smul_mem b hH)) (hC a)
    have h00 : bicoeff 0 0 g = 0 := by
      simp [g, a, hamiltonian, bicoeff_monomial]
    have h03 : bicoeff 0 3 g = 0 := by
      simp [g, b, hamiltonian, bicoeff_monomial]
    have hz := seven_normalized_core_zero t hb h4 h5 hnon g hg h00 h03
    rw [Submodule.mem_span_pair]
    refine ⟨a,b,?_⟩
    simp only [← C_mul', mul_one]
    linear_combination -hz
  · apply Submodule.span_le.mpr
    intro f hf
    rcases hf with rfl | rfl
    · exact h1
    · exact hH

end SexticC3.CubeLeading.Polynomial
