import SexticC3.NonlinearB
import SexticC3.NonlinearBCoefficients

noncomputable section
namespace SexticC3.NonlinearB
open MvPolynomial Differential
variable {K : Type*} [Field K] [CharZero K]

@[simp] theorem cf_C_mul (a : K) (G : Poly (R := K)) (i j : ℕ) :
    cf (C a*G) i j=a*cf G i j := coeff_C_mul _ _ _

theorem constant_gates (c : Parameters K) (u : K) :
    contraction 1 (H c) (mono 0 0 u)=0 ∧ Static (H c) (mono 0 0 u) := by
  simp only [Static, first_gate, third_gate, fifth_gate, mixed_mono]
  norm_num [falling]

theorem firstRefinement_translate (c : Parameters K) (G : Poly (R := K)) (l u : K) :
    FirstRefinement (H c) (C l*H c+mono 0 0 u+G) ↔ FirstRefinement (H c) G := by
  have hc := constant_gates c u
  simp only [FirstRefinement, contraction_add_right, contraction_C_mul_right,
    contraction_one_self, contraction_three_self, contraction_five_self,
    hc.1, hc.2.1, hc.2.2, mul_zero, zero_add]

theorem firstRefinement_shift (c : Parameters K) (G : Poly (R := K)) (l : K)
    (h : FirstRefinement (H c) G) : FirstRefinement (H c) (G+C l*H c) := by
  have ht := (firstRefinement_translate c G l 0).mpr h
  simpa [add_comm] using ht

theorem constant_energy_persistent (c : Parameters K) (l u : K) :
    PersistentCore (H c) (C l*H c+mono 0 0 u) := by
  have hc := constant_gates c u
  apply core_of_stationary
  all_goals simp [contraction_add_right, contraction_C_mul_right, hc.1, hc.2.1, hc.2.2]

end SexticC3.NonlinearB
