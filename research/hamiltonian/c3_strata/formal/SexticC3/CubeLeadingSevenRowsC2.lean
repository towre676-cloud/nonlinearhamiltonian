import SexticC3.CubeLeadingSevenEvaluateC2

/-! Generated exact coefficient equations. Each is derived from the actual
Hamiltonian iterate and the proved static recurrence; no matrix entries are hypotheses. -/
noncomputable section
set_option linter.unusedSectionVars false
namespace SexticC3.CubeLeading.Polynomial
open MvPolynomial
variable {K : Type*} [Field K] [CharZero K]

set_option maxHeartbeats 300000 in
lemma seven_c2_row_0 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (hb2 : t.b₂ = 0) (hc3 : t.c₃ = 0) (x : Fin 13 → K)
    (hf : Static t.toGateParameters ((bracket (hamiltonian t))^[1] (sevenCombination t x))) :
    816480 * x 9 = 0 := by
  have h := third_recurrence t.toGateParameters _ hf 2 3
  simp only [bicoeff_seven_iterate] at h
  norm_num only [hb, h4, h5, hb2, hc3, mul_zero, zero_mul, add_zero, zero_add, sub_zero, zero_sub, false_and, and_false, true_and, and_true, if_true, if_false] at h
  simp only [seven_c2_eval_1_0_2 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_0_3 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_0_4 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_0_5 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_0_6 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_0_7 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_1_0 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_1_1 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_1_2 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_1_3 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_1_4 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_1_5 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_1_6 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_2_0 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_2_1 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_2_2 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_2_3 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_2_4 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_2_5 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_2_6 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_3_0 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_3_1 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_3_2 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_3_3 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_3_4 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_4_0 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_4_1 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_4_3 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_5_0 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_5_1 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_5_2 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_5_3 t hb h4 h5 hb2 hc3 x] at h
  linear_combination h

set_option maxHeartbeats 300000 in
lemma seven_c2_row_1 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (hb2 : t.b₂ = 0) (hc3 : t.c₃ = 0) (x : Fin 13 → K)
    (hf : Static t.toGateParameters ((bracket (hamiltonian t))^[1] (sevenCombination t x))) :
    (-40320) * x 9 + (126000 * t.c₂) * x 12 = 0 := by
  have h := third_recurrence t.toGateParameters _ hf 0 4
  simp only [bicoeff_seven_iterate] at h
  norm_num only [hb, h4, h5, hb2, hc3, mul_zero, zero_mul, add_zero, zero_add, sub_zero, zero_sub, false_and, and_false, true_and, and_true, if_true, if_false] at h
  simp only [seven_c2_eval_1_0_2 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_0_3 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_0_4 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_0_5 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_0_6 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_0_7 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_1_0 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_1_1 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_1_2 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_1_3 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_1_4 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_1_5 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_1_6 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_2_0 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_2_1 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_2_2 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_2_3 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_2_4 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_2_5 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_2_6 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_3_0 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_3_1 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_3_2 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_3_3 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_3_4 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_4_0 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_4_1 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_4_3 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_5_0 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_5_1 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_5_2 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_5_3 t hb h4 h5 hb2 hc3 x] at h
  linear_combination h

set_option maxHeartbeats 300000 in
lemma seven_c2_row_2 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (hb2 : t.b₂ = 0) (hc3 : t.c₃ = 0) (x : Fin 13 → K)
    (hf : Static t.toGateParameters ((bracket (hamiltonian t))^[1] (sevenCombination t x))) :
    103680 * x 7 + (1360800 * (t.b₁ ^ 2)) * x 12 = 0 := by
  have h := third_recurrence t.toGateParameters _ hf 2 2
  simp only [bicoeff_seven_iterate] at h
  norm_num only [hb, h4, h5, hb2, hc3, mul_zero, zero_mul, add_zero, zero_add, sub_zero, zero_sub, false_and, and_false, true_and, and_true, if_true, if_false] at h
  simp only [seven_c2_eval_1_0_2 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_0_3 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_0_4 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_0_5 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_0_6 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_0_7 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_1_0 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_1_1 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_1_2 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_1_3 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_1_4 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_1_5 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_1_6 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_2_0 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_2_1 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_2_2 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_2_3 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_2_4 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_2_5 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_2_6 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_3_0 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_3_1 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_3_2 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_3_3 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_3_4 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_4_0 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_4_1 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_4_3 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_5_0 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_5_1 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_5_2 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_5_3 t hb h4 h5 hb2 hc3 x] at h
  linear_combination h

set_option maxHeartbeats 300000 in
lemma seven_c2_row_3 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (hb2 : t.b₂ = 0) (hc3 : t.c₃ = 0) (x : Fin 13 → K)
    (hf : Static t.toGateParameters ((bracket (hamiltonian t))^[1] (sevenCombination t x))) :
    (-12960) * x 7 + (20160 * t.c₂) * x 11 + ((-50400) * (t.b₁ ^ 2)) * x 12 = 0 := by
  have h := third_recurrence t.toGateParameters _ hf 0 3
  simp only [bicoeff_seven_iterate] at h
  norm_num only [hb, h4, h5, hb2, hc3, mul_zero, zero_mul, add_zero, zero_add, sub_zero, zero_sub, false_and, and_false, true_and, and_true, if_true, if_false] at h
  simp only [seven_c2_eval_1_0_2 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_0_3 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_0_4 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_0_5 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_0_6 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_0_7 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_1_0 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_1_1 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_1_2 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_1_3 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_1_4 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_1_5 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_1_6 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_2_0 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_2_1 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_2_2 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_2_3 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_2_4 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_2_5 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_2_6 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_3_0 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_3_1 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_3_2 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_3_3 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_3_4 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_4_0 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_4_1 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_4_3 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_5_0 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_5_1 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_5_2 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_5_3 t hb h4 h5 hb2 hc3 x] at h
  linear_combination h

set_option maxHeartbeats 300000 in
lemma seven_c2_row_4 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (hb2 : t.b₂ = 0) (hc3 : t.c₃ = 0) (x : Fin 13 → K)
    (hf : Static t.toGateParameters ((bracket (hamiltonian t))^[1] (sevenCombination t x))) :
    1632960 * x 8 + ((-272160) * t.b₁) * x 11 = 0 := by
  have h := third_recurrence t.toGateParameters _ hf 1 3
  simp only [bicoeff_seven_iterate] at h
  norm_num only [hb, h4, h5, hb2, hc3, mul_zero, zero_mul, add_zero, zero_add, sub_zero, zero_sub, false_and, and_false, true_and, and_true, if_true, if_false] at h
  simp only [seven_c2_eval_1_0_2 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_0_3 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_0_4 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_0_5 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_0_6 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_0_7 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_1_0 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_1_1 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_1_2 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_1_3 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_1_4 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_1_5 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_1_6 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_2_0 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_2_1 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_2_2 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_2_3 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_2_4 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_2_5 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_2_6 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_3_0 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_3_1 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_3_2 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_3_3 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_3_4 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_4_0 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_4_1 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_4_3 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_5_0 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_5_1 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_5_2 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_5_3 t hb h4 h5 hb2 hc3 x] at h
  linear_combination h

set_option maxHeartbeats 300000 in
lemma seven_c2_row_5 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (hb2 : t.b₂ = 0) (hc3 : t.c₃ = 0) (x : Fin 13 → K)
    (hf : Static t.toGateParameters ((bracket (hamiltonian t))^[1] (sevenCombination t x))) :
    432 * x 3 + (8640 * t.b₁) * x 7 + ((-80640) * t.c₂) * x 8 + ((-5040) * t.c₁) * x 9 + (15120 * t.b₁ * t.c₂) * x 11 = 0 := by
  have h := third_recurrence t.toGateParameters _ hf 1 1
  simp only [bicoeff_seven_iterate] at h
  norm_num only [hb, h4, h5, hb2, hc3, mul_zero, zero_mul, add_zero, zero_add, sub_zero, zero_sub, false_and, and_false, true_and, and_true, if_true, if_false] at h
  simp only [seven_c2_eval_1_0_2 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_0_3 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_0_4 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_0_5 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_0_6 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_0_7 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_1_0 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_1_1 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_1_2 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_1_3 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_1_4 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_1_5 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_1_6 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_2_0 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_2_1 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_2_2 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_2_3 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_2_4 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_2_5 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_2_6 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_3_0 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_3_1 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_3_2 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_3_3 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_3_4 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_4_0 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_4_1 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_4_3 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_5_0 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_5_1 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_5_2 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_5_3 t hb h4 h5 hb2 hc3 x] at h
  linear_combination h

set_option maxHeartbeats 300000 in
lemma seven_c2_row_6 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (hb2 : t.b₂ = 0) (hc3 : t.c₃ = 0) (x : Fin 13 → K)
    (hf : Static t.toGateParameters ((bracket (hamiltonian t))^[1] (sevenCombination t x))) :
    864 * x 4 + ((-574560) * t.b₁) * x 8 + ((-45360) * t.c₂) * x 9 + (90720 * (t.b₁ ^ 2)) * x 11 + ((-151200) * t.b₁ * t.c₁) * x 12 = 0 := by
  have h := third_recurrence t.toGateParameters _ hf 2 1
  simp only [bicoeff_seven_iterate] at h
  norm_num only [hb, h4, h5, hb2, hc3, mul_zero, zero_mul, add_zero, zero_add, sub_zero, zero_sub, false_and, and_false, true_and, and_true, if_true, if_false] at h
  simp only [seven_c2_eval_1_0_2 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_0_3 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_0_4 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_0_5 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_0_6 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_0_7 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_1_0 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_1_1 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_1_2 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_1_3 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_1_4 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_1_5 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_1_6 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_2_0 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_2_1 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_2_2 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_2_3 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_2_4 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_2_5 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_2_6 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_3_0 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_3_1 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_3_2 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_3_3 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_3_4 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_4_0 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_4_1 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_4_3 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_5_0 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_5_1 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_5_2 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_5_3 t hb h4 h5 hb2 hc3 x] at h
  linear_combination h

set_option maxHeartbeats 300000 in
lemma seven_c2_row_7 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (hb2 : t.b₂ = 0) (hc3 : t.c₃ = 0) (x : Fin 13 → K)
    (hf : Static t.toGateParameters ((bracket (hamiltonian t))^[1] (sevenCombination t x))) :
    (-576) * x 4 + (45360 * t.b₁) * x 8 + (2520 * t.c₂) * x 9 + (2160 * t.c₂) * x 10 + ((-7560) * (t.b₁ ^ 2)) * x 11 = 0 := by
  have h := third_recurrence t.toGateParameters _ hf 0 2
  simp only [bicoeff_seven_iterate] at h
  norm_num only [hb, h4, h5, hb2, hc3, mul_zero, zero_mul, add_zero, zero_add, sub_zero, zero_sub, false_and, and_false, true_and, and_true, if_true, if_false] at h
  simp only [seven_c2_eval_1_0_2 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_0_3 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_0_4 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_0_5 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_0_6 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_0_7 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_1_0 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_1_1 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_1_2 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_1_3 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_1_4 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_1_5 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_1_6 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_2_0 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_2_1 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_2_2 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_2_3 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_2_4 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_2_5 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_2_6 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_3_0 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_3_1 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_3_2 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_3_3 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_3_4 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_4_0 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_4_1 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_4_3 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_5_0 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_5_1 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_5_2 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_5_3 t hb h4 h5 hb2 hc3 x] at h
  linear_combination h

set_option maxHeartbeats 300000 in
lemma seven_c2_row_8 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (hb2 : t.b₂ = 0) (hc3 : t.c₃ = 0) (x : Fin 13 → K)
    (hf : Static t.toGateParameters ((bracket (hamiltonian t))^[1] (sevenCombination t x))) :
    (144 * t.b₁) * x 4 + ((-2160) * t.c₂) * x 6 + ((-720) * t.c₁) * x 7 + ((-5040) * (t.b₁ ^ 2)) * x 8 + (720 * t.b₁ * t.c₂) * x 10 = 0 := by
  have h := third_recurrence t.toGateParameters _ hf 1 0
  simp only [bicoeff_seven_iterate] at h
  norm_num only [hb, h4, h5, hb2, hc3, mul_zero, zero_mul, add_zero, zero_add, sub_zero, zero_sub, false_and, and_false, true_and, and_true, if_true, if_false] at h
  simp only [seven_c2_eval_1_0_2 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_0_3 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_0_4 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_0_5 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_0_6 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_0_7 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_1_0 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_1_1 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_1_2 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_1_3 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_1_4 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_1_5 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_1_6 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_2_0 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_2_1 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_2_2 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_2_3 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_2_4 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_2_5 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_2_6 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_3_0 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_3_1 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_3_2 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_3_3 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_3_4 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_4_0 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_4_1 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_4_3 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_5_0 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_5_1 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_5_2 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_5_3 t hb h4 h5 hb2 hc3 x] at h
  linear_combination h

set_option maxHeartbeats 300000 in
lemma seven_c2_row_9 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (hb2 : t.b₂ = 0) (hc3 : t.c₃ = 0) (x : Fin 13 → K)
    (hf : Static t.toGateParameters ((bracket (hamiltonian t))^[1] (sevenCombination t x))) :
    (36 * t.b₁) * x 3 + (24 * t.c₂) * x 4 + (24 * t.c₂) * x 5 + ((-180) * t.c₁) * x 6 = 0 := by
  have h := third_recurrence t.toGateParameters _ hf 0 0
  simp only [bicoeff_seven_iterate] at h
  norm_num only [hb, h4, h5, hb2, hc3, mul_zero, zero_mul, add_zero, zero_add, sub_zero, zero_sub, false_and, and_false, true_and, and_true, if_true, if_false] at h
  simp only [seven_c2_eval_1_0_2 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_0_3 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_0_4 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_0_5 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_0_6 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_0_7 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_1_0 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_1_1 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_1_2 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_1_3 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_1_4 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_1_5 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_1_6 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_2_0 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_2_1 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_2_2 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_2_3 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_2_4 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_2_5 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_2_6 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_3_0 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_3_1 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_3_2 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_3_3 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_3_4 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_4_0 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_4_1 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_4_3 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_5_0 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_5_1 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_5_2 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_5_3 t hb h4 h5 hb2 hc3 x] at h
  linear_combination h

set_option maxHeartbeats 300000 in
lemma seven_c2_row_10 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (hb2 : t.b₂ = 0) (hc3 : t.c₃ = 0) (x : Fin 13 → K)
    (hf : Static t.toGateParameters ((bracket (hamiltonian t))^[1] (sevenCombination t x))) :
    (-144) * x 1 + (2160 * t.b₁) * x 6 + (720 * t.c₂) * x 7 + ((-5040) * t.c₁) * x 8 + ((-720) * (t.b₁ ^ 2)) * x 10 = 0 := by
  have h := third_recurrence t.toGateParameters _ hf 0 1
  simp only [bicoeff_seven_iterate] at h
  norm_num only [hb, h4, h5, hb2, hc3, mul_zero, zero_mul, add_zero, zero_add, sub_zero, zero_sub, false_and, and_false, true_and, and_true, if_true, if_false] at h
  simp only [seven_c2_eval_1_0_2 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_0_3 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_0_4 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_0_5 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_0_6 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_0_7 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_1_0 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_1_1 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_1_2 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_1_3 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_1_4 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_1_5 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_1_6 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_2_0 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_2_1 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_2_2 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_2_3 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_2_4 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_2_5 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_2_6 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_3_0 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_3_1 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_3_2 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_3_3 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_3_4 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_4_0 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_4_1 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_4_3 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_5_0 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_5_1 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_5_2 t hb h4 h5 hb2 hc3 x, seven_c2_eval_1_5_3 t hb h4 h5 hb2 hc3 x] at h
  linear_combination h

set_option maxHeartbeats 300000 in
lemma seven_c2_row_11 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (hb2 : t.b₂ = 0) (hc3 : t.c₃ = 0) (x : Fin 13 → K)
    (hf : Static t.toGateParameters ((bracket (hamiltonian t))^[2] (sevenCombination t x))) :
    ((-72) * t.c₂) * x 0 + ((-72) * t.c₁) * x 1 + (((-288) * t.b₀ * t.b₁) + ((-96) * t.b₁ * t.c₂)) * x 4 + (120 * t.b₁ * t.c₂) * x 5 + ((720 * (t.c₂ ^ 2)) + (3600 * t.b₁ * t.c₁) + (3960 * t.b₀ * t.c₂)) * x 6 + ((1440 * t.b₀ * t.c₁) + (1440 * t.c₁ * t.c₂)) * x 7 + (((-10080) * (t.c₁ ^ 2)) + (10080 * t.b₀ * (t.b₁ ^ 2))) * x 8 + (((-1440) * t.c₁ * (t.b₁ ^ 2)) + ((-1440) * t.b₀ * t.b₁ * t.c₂)) * x 10 = 0 := by
  have h := third_recurrence t.toGateParameters _ hf 0 0
  simp only [bicoeff_seven_iterate] at h
  norm_num only [hb, h4, h5, hb2, hc3, mul_zero, zero_mul, add_zero, zero_add, sub_zero, zero_sub, false_and, and_false, true_and, and_true, if_true, if_false] at h
  simp only [seven_c2_eval_2_0_2 t hb h4 h5 hb2 hc3 x, seven_c2_eval_2_0_3 t hb h4 h5 hb2 hc3 x, seven_c2_eval_2_0_4 t hb h4 h5 hb2 hc3 x, seven_c2_eval_2_1_1 t hb h4 h5 hb2 hc3 x, seven_c2_eval_2_1_2 t hb h4 h5 hb2 hc3 x, seven_c2_eval_2_1_3 t hb h4 h5 hb2 hc3 x, seven_c2_eval_2_2_1 t hb h4 h5 hb2 hc3 x, seven_c2_eval_2_3_0 t hb h4 h5 hb2 hc3 x, seven_c2_eval_2_3_1 t hb h4 h5 hb2 hc3 x, seven_c2_eval_2_4_0 t hb h4 h5 hb2 hc3 x] at h
  linear_combination h

set_option maxHeartbeats 300000 in
lemma seven_c2_row_12 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (hb2 : t.b₂ = 0) (hc3 : t.c₃ = 0) (x : Fin 13 → K)
    (hf : Static t.toGateParameters ((bracket (hamiltonian t))^[3] (sevenCombination t x))) :
    ((-288) * t.b₁ * t.c₂) * x 0 + (((-288) * (t.c₂ ^ 2)) + ((-576) * t.b₁ * t.c₁) + (576 * t.b₀ * t.c₂)) * x 1 + ((-144) * (t.c₂ ^ 2)) * x 2 + ((324 * (t.b₁ ^ 3)) + ((-648) * t.b₀ * t.c₁) + ((-216) * t.c₁ * t.c₂)) * x 3 + (((-432) * (t.c₁ ^ 2)) + (312 * t.c₂ * (t.b₁ ^ 2)) + (432 * t.b₀ * (t.b₁ ^ 2))) * x 4 + (456 * t.c₂ * (t.b₁ ^ 2)) * x 5 + (((-38880) * t.b₁ * (t.b₀ ^ 2)) + ((-2160) * t.b₁ * (t.c₂ ^ 2)) + (4140 * t.c₁ * (t.b₁ ^ 2)) + ((-47520) * t.b₀ * t.b₁ * t.c₂)) * x 6 + (((-25920) * t.c₂ * (t.b₀ ^ 2)) + ((-12960) * t.b₀ * (t.c₂ ^ 2)) + ((-45360) * t.b₀ * t.b₁ * t.c₁) + ((-6480) * t.b₁ * t.c₁ * t.c₂)) * x 7 + (((-15120) * t.b₀ * (t.b₁ ^ 3)) + (60480 * t.c₁ * (t.c₂ ^ 2)) + (196560 * t.b₁ * (t.c₁ ^ 2)) + (272160 * t.c₁ * (t.b₀ ^ 2)) + (544320 * t.b₀ * t.c₁ * t.c₂)) * x 8 + (((-15120) * (t.b₀ ^ 2) * (t.b₁ ^ 2)) + (15120 * t.c₂ * (t.c₁ ^ 2)) + (30240 * t.b₀ * (t.c₁ ^ 2))) * x 9 + (((-2160) * t.c₁ * (t.b₁ ^ 3)) + (4320 * t.c₂ * (t.c₁ ^ 2)) + (12960 * (t.b₀ ^ 2) * (t.b₁ ^ 2)) + (15120 * t.b₀ * t.c₂ * (t.b₁ ^ 2))) * x 10 + (((-45360) * (t.b₁ ^ 2) * (t.c₁ ^ 2)) + ((-45360) * t.b₁ * t.c₁ * (t.b₀ ^ 2)) + ((-90720) * t.b₀ * t.b₁ * t.c₁ * t.c₂)) * x 11 = 0 := by
  have h := third_recurrence t.toGateParameters _ hf 0 0
  simp only [bicoeff_seven_iterate] at h
  norm_num only [hb, h4, h5, hb2, hc3, mul_zero, zero_mul, add_zero, zero_add, sub_zero, zero_sub, false_and, and_false, true_and, and_true, if_true, if_false] at h
  simp only [seven_c2_eval_3_0_3 t hb h4 h5 hb2 hc3 x, seven_c2_eval_3_1_1 t hb h4 h5 hb2 hc3 x, seven_c2_eval_3_3_0 t hb h4 h5 hb2 hc3 x] at h
  linear_combination h

end SexticC3.CubeLeading.Polynomial
