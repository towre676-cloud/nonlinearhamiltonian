import SexticC3.CubeLeadingSevenEvaluateC3

/-! Generated exact coefficient equations. Each is derived from the actual
Hamiltonian iterate and the proved static recurrence; no matrix entries are hypotheses. -/
noncomputable section
set_option linter.unusedSectionVars false
namespace SexticC3.CubeLeading.Polynomial
open MvPolynomial
variable {K : Type*} [Field K] [CharZero K]

set_option maxHeartbeats 300000 in
lemma seven_c3_row_0 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (hb2 : t.b₂ = 0) (x : Fin 13 → K)
    (hf : Static t.toGateParameters ((bracket (hamiltonian t))^[1] (sevenCombination t x))) :
    816480 * x 9 = 0 := by
  have h := third_recurrence t.toGateParameters _ hf 2 3
  simp only [bicoeff_seven_iterate] at h
  norm_num only [hb, h4, h5, hb2, mul_zero, zero_mul, add_zero, zero_add, sub_zero, zero_sub, false_and, and_false, true_and, and_true, if_true, if_false] at h
  simp only [seven_c3_eval_1_0_2 t hb h4 h5 hb2 x, seven_c3_eval_1_0_3 t hb h4 h5 hb2 x, seven_c3_eval_1_0_4 t hb h4 h5 hb2 x, seven_c3_eval_1_0_5 t hb h4 h5 hb2 x, seven_c3_eval_1_1_2 t hb h4 h5 hb2 x, seven_c3_eval_1_1_3 t hb h4 h5 hb2 x, seven_c3_eval_1_1_4 t hb h4 h5 hb2 x, seven_c3_eval_1_1_5 t hb h4 h5 hb2 x, seven_c3_eval_1_1_6 t hb h4 h5 hb2 x, seven_c3_eval_1_1_7 t hb h4 h5 hb2 x, seven_c3_eval_1_2_0 t hb h4 h5 hb2 x, seven_c3_eval_1_2_1 t hb h4 h5 hb2 x, seven_c3_eval_1_2_2 t hb h4 h5 hb2 x, seven_c3_eval_1_2_3 t hb h4 h5 hb2 x, seven_c3_eval_1_2_4 t hb h4 h5 hb2 x, seven_c3_eval_1_2_5 t hb h4 h5 hb2 x, seven_c3_eval_1_2_6 t hb h4 h5 hb2 x, seven_c3_eval_1_3_1 t hb h4 h5 hb2 x, seven_c3_eval_1_3_2 t hb h4 h5 hb2 x, seven_c3_eval_1_3_4 t hb h4 h5 hb2 x, seven_c3_eval_1_3_5 t hb h4 h5 hb2 x, seven_c3_eval_1_3_6 t hb h4 h5 hb2 x, seven_c3_eval_1_4_0 t hb h4 h5 hb2 x, seven_c3_eval_1_4_1 t hb h4 h5 hb2 x, seven_c3_eval_1_4_2 t hb h4 h5 hb2 x, seven_c3_eval_1_4_3 t hb h4 h5 hb2 x, seven_c3_eval_1_4_4 t hb h4 h5 hb2 x, seven_c3_eval_1_5_0 t hb h4 h5 hb2 x, seven_c3_eval_1_5_3 t hb h4 h5 hb2 x, seven_c3_eval_1_6_1 t hb h4 h5 hb2 x, seven_c3_eval_1_6_2 t hb h4 h5 hb2 x, seven_c3_eval_1_6_3 t hb h4 h5 hb2 x] at h
  linear_combination h

set_option maxHeartbeats 300000 in
lemma seven_c3_row_1 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (hb2 : t.b₂ = 0) (x : Fin 13 → K)
    (hf : Static t.toGateParameters ((bracket (hamiltonian t))^[1] (sevenCombination t x))) :
    (-540) * x 7 + (630 * t.c₂) * x 11 = 0 := by
  have h := fifth_recurrence t.toGateParameters _ hf 0 0
  simp only [bicoeff_seven_iterate] at h
  norm_num only [hb, h4, h5, hb2, mul_zero, zero_mul, add_zero, zero_add, sub_zero, zero_sub, false_and, and_false, true_and, and_true, if_true, if_false] at h
  simp only [seven_c3_eval_1_0_2 t hb h4 h5 hb2 x, seven_c3_eval_1_0_3 t hb h4 h5 hb2 x, seven_c3_eval_1_0_4 t hb h4 h5 hb2 x, seven_c3_eval_1_0_5 t hb h4 h5 hb2 x, seven_c3_eval_1_1_2 t hb h4 h5 hb2 x, seven_c3_eval_1_1_3 t hb h4 h5 hb2 x, seven_c3_eval_1_1_4 t hb h4 h5 hb2 x, seven_c3_eval_1_1_5 t hb h4 h5 hb2 x, seven_c3_eval_1_1_6 t hb h4 h5 hb2 x, seven_c3_eval_1_1_7 t hb h4 h5 hb2 x, seven_c3_eval_1_2_0 t hb h4 h5 hb2 x, seven_c3_eval_1_2_1 t hb h4 h5 hb2 x, seven_c3_eval_1_2_2 t hb h4 h5 hb2 x, seven_c3_eval_1_2_3 t hb h4 h5 hb2 x, seven_c3_eval_1_2_4 t hb h4 h5 hb2 x, seven_c3_eval_1_2_5 t hb h4 h5 hb2 x, seven_c3_eval_1_2_6 t hb h4 h5 hb2 x, seven_c3_eval_1_3_1 t hb h4 h5 hb2 x, seven_c3_eval_1_3_2 t hb h4 h5 hb2 x, seven_c3_eval_1_3_4 t hb h4 h5 hb2 x, seven_c3_eval_1_3_5 t hb h4 h5 hb2 x, seven_c3_eval_1_3_6 t hb h4 h5 hb2 x, seven_c3_eval_1_4_0 t hb h4 h5 hb2 x, seven_c3_eval_1_4_1 t hb h4 h5 hb2 x, seven_c3_eval_1_4_2 t hb h4 h5 hb2 x, seven_c3_eval_1_4_3 t hb h4 h5 hb2 x, seven_c3_eval_1_4_4 t hb h4 h5 hb2 x, seven_c3_eval_1_5_0 t hb h4 h5 hb2 x, seven_c3_eval_1_5_3 t hb h4 h5 hb2 x, seven_c3_eval_1_6_1 t hb h4 h5 hb2 x, seven_c3_eval_1_6_2 t hb h4 h5 hb2 x, seven_c3_eval_1_6_3 t hb h4 h5 hb2 x] at h
  linear_combination h

set_option maxHeartbeats 300000 in
lemma seven_c3_row_2 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (hb2 : t.b₂ = 0) (x : Fin 13 → K)
    (hf : Static t.toGateParameters ((bracket (hamiltonian t))^[1] (sevenCombination t x))) :
    1632960 * x 8 + (((-272160) * t.b₁) + ((-211680) * t.c₃)) * x 11 = 0 := by
  have h := third_recurrence t.toGateParameters _ hf 1 3
  simp only [bicoeff_seven_iterate] at h
  norm_num only [hb, h4, h5, hb2, mul_zero, zero_mul, add_zero, zero_add, sub_zero, zero_sub, false_and, and_false, true_and, and_true, if_true, if_false] at h
  simp only [seven_c3_eval_1_0_2 t hb h4 h5 hb2 x, seven_c3_eval_1_0_3 t hb h4 h5 hb2 x, seven_c3_eval_1_0_4 t hb h4 h5 hb2 x, seven_c3_eval_1_0_5 t hb h4 h5 hb2 x, seven_c3_eval_1_1_2 t hb h4 h5 hb2 x, seven_c3_eval_1_1_3 t hb h4 h5 hb2 x, seven_c3_eval_1_1_4 t hb h4 h5 hb2 x, seven_c3_eval_1_1_5 t hb h4 h5 hb2 x, seven_c3_eval_1_1_6 t hb h4 h5 hb2 x, seven_c3_eval_1_1_7 t hb h4 h5 hb2 x, seven_c3_eval_1_2_0 t hb h4 h5 hb2 x, seven_c3_eval_1_2_1 t hb h4 h5 hb2 x, seven_c3_eval_1_2_2 t hb h4 h5 hb2 x, seven_c3_eval_1_2_3 t hb h4 h5 hb2 x, seven_c3_eval_1_2_4 t hb h4 h5 hb2 x, seven_c3_eval_1_2_5 t hb h4 h5 hb2 x, seven_c3_eval_1_2_6 t hb h4 h5 hb2 x, seven_c3_eval_1_3_1 t hb h4 h5 hb2 x, seven_c3_eval_1_3_2 t hb h4 h5 hb2 x, seven_c3_eval_1_3_4 t hb h4 h5 hb2 x, seven_c3_eval_1_3_5 t hb h4 h5 hb2 x, seven_c3_eval_1_3_6 t hb h4 h5 hb2 x, seven_c3_eval_1_4_0 t hb h4 h5 hb2 x, seven_c3_eval_1_4_1 t hb h4 h5 hb2 x, seven_c3_eval_1_4_2 t hb h4 h5 hb2 x, seven_c3_eval_1_4_3 t hb h4 h5 hb2 x, seven_c3_eval_1_4_4 t hb h4 h5 hb2 x, seven_c3_eval_1_5_0 t hb h4 h5 hb2 x, seven_c3_eval_1_5_3 t hb h4 h5 hb2 x, seven_c3_eval_1_6_1 t hb h4 h5 hb2 x, seven_c3_eval_1_6_2 t hb h4 h5 hb2 x, seven_c3_eval_1_6_3 t hb h4 h5 hb2 x] at h
  linear_combination h

set_option maxHeartbeats 300000 in
lemma seven_c3_row_3 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (hb2 : t.b₂ = 0) (x : Fin 13 → K)
    (hf : Static t.toGateParameters ((bracket (hamiltonian t))^[1] (sevenCombination t x))) :
    (-4354560) * x 8 + ((725760 * t.b₁) + (725760 * t.c₃)) * x 11 = 0 := by
  have h := third_recurrence t.toGateParameters _ hf 3 2
  simp only [bicoeff_seven_iterate] at h
  norm_num only [hb, h4, h5, hb2, mul_zero, zero_mul, add_zero, zero_add, sub_zero, zero_sub, false_and, and_false, true_and, and_true, if_true, if_false] at h
  simp only [seven_c3_eval_1_0_2 t hb h4 h5 hb2 x, seven_c3_eval_1_0_3 t hb h4 h5 hb2 x, seven_c3_eval_1_0_4 t hb h4 h5 hb2 x, seven_c3_eval_1_0_5 t hb h4 h5 hb2 x, seven_c3_eval_1_1_2 t hb h4 h5 hb2 x, seven_c3_eval_1_1_3 t hb h4 h5 hb2 x, seven_c3_eval_1_1_4 t hb h4 h5 hb2 x, seven_c3_eval_1_1_5 t hb h4 h5 hb2 x, seven_c3_eval_1_1_6 t hb h4 h5 hb2 x, seven_c3_eval_1_1_7 t hb h4 h5 hb2 x, seven_c3_eval_1_2_0 t hb h4 h5 hb2 x, seven_c3_eval_1_2_1 t hb h4 h5 hb2 x, seven_c3_eval_1_2_2 t hb h4 h5 hb2 x, seven_c3_eval_1_2_3 t hb h4 h5 hb2 x, seven_c3_eval_1_2_4 t hb h4 h5 hb2 x, seven_c3_eval_1_2_5 t hb h4 h5 hb2 x, seven_c3_eval_1_2_6 t hb h4 h5 hb2 x, seven_c3_eval_1_3_1 t hb h4 h5 hb2 x, seven_c3_eval_1_3_2 t hb h4 h5 hb2 x, seven_c3_eval_1_3_4 t hb h4 h5 hb2 x, seven_c3_eval_1_3_5 t hb h4 h5 hb2 x, seven_c3_eval_1_3_6 t hb h4 h5 hb2 x, seven_c3_eval_1_4_0 t hb h4 h5 hb2 x, seven_c3_eval_1_4_1 t hb h4 h5 hb2 x, seven_c3_eval_1_4_2 t hb h4 h5 hb2 x, seven_c3_eval_1_4_3 t hb h4 h5 hb2 x, seven_c3_eval_1_4_4 t hb h4 h5 hb2 x, seven_c3_eval_1_5_0 t hb h4 h5 hb2 x, seven_c3_eval_1_5_3 t hb h4 h5 hb2 x, seven_c3_eval_1_6_1 t hb h4 h5 hb2 x, seven_c3_eval_1_6_2 t hb h4 h5 hb2 x, seven_c3_eval_1_6_3 t hb h4 h5 hb2 x] at h
  linear_combination h

set_option maxHeartbeats 300000 in
lemma seven_c3_row_4 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (hb2 : t.b₂ = 0) (x : Fin 13 → K)
    (hf : Static t.toGateParameters ((bracket (hamiltonian t))^[1] (sevenCombination t x))) :
    432 * x 3 + ((8640 * t.b₁) + (8640 * t.c₃)) * x 7 + ((-80640) * t.c₂) * x 8 + ((-5040) * t.c₁) * x 9 + ((15120 * t.b₁ * t.c₂) + (15120 * t.c₂ * t.c₃)) * x 11 = 0 := by
  have h := third_recurrence t.toGateParameters _ hf 1 1
  simp only [bicoeff_seven_iterate] at h
  norm_num only [hb, h4, h5, hb2, mul_zero, zero_mul, add_zero, zero_add, sub_zero, zero_sub, false_and, and_false, true_and, and_true, if_true, if_false] at h
  simp only [seven_c3_eval_1_0_2 t hb h4 h5 hb2 x, seven_c3_eval_1_0_3 t hb h4 h5 hb2 x, seven_c3_eval_1_0_4 t hb h4 h5 hb2 x, seven_c3_eval_1_0_5 t hb h4 h5 hb2 x, seven_c3_eval_1_1_2 t hb h4 h5 hb2 x, seven_c3_eval_1_1_3 t hb h4 h5 hb2 x, seven_c3_eval_1_1_4 t hb h4 h5 hb2 x, seven_c3_eval_1_1_5 t hb h4 h5 hb2 x, seven_c3_eval_1_1_6 t hb h4 h5 hb2 x, seven_c3_eval_1_1_7 t hb h4 h5 hb2 x, seven_c3_eval_1_2_0 t hb h4 h5 hb2 x, seven_c3_eval_1_2_1 t hb h4 h5 hb2 x, seven_c3_eval_1_2_2 t hb h4 h5 hb2 x, seven_c3_eval_1_2_3 t hb h4 h5 hb2 x, seven_c3_eval_1_2_4 t hb h4 h5 hb2 x, seven_c3_eval_1_2_5 t hb h4 h5 hb2 x, seven_c3_eval_1_2_6 t hb h4 h5 hb2 x, seven_c3_eval_1_3_1 t hb h4 h5 hb2 x, seven_c3_eval_1_3_2 t hb h4 h5 hb2 x, seven_c3_eval_1_3_4 t hb h4 h5 hb2 x, seven_c3_eval_1_3_5 t hb h4 h5 hb2 x, seven_c3_eval_1_3_6 t hb h4 h5 hb2 x, seven_c3_eval_1_4_0 t hb h4 h5 hb2 x, seven_c3_eval_1_4_1 t hb h4 h5 hb2 x, seven_c3_eval_1_4_2 t hb h4 h5 hb2 x, seven_c3_eval_1_4_3 t hb h4 h5 hb2 x, seven_c3_eval_1_4_4 t hb h4 h5 hb2 x, seven_c3_eval_1_5_0 t hb h4 h5 hb2 x, seven_c3_eval_1_5_3 t hb h4 h5 hb2 x, seven_c3_eval_1_6_1 t hb h4 h5 hb2 x, seven_c3_eval_1_6_2 t hb h4 h5 hb2 x, seven_c3_eval_1_6_3 t hb h4 h5 hb2 x] at h
  linear_combination h

set_option maxHeartbeats 300000 in
lemma seven_c3_row_5 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (hb2 : t.b₂ = 0) (x : Fin 13 → K)
    (hf : Static t.toGateParameters ((bracket (hamiltonian t))^[1] (sevenCombination t x))) :
    (-576) * x 4 + ((30240 * t.c₃) + (45360 * t.b₁)) * x 8 + (2520 * t.c₂) * x 9 + (2160 * t.c₂) * x 10 + (((-7560) * (t.b₁ ^ 2)) + ((-7560) * t.b₁ * t.c₃)) * x 11 = 0 := by
  have h := third_recurrence t.toGateParameters _ hf 0 2
  simp only [bicoeff_seven_iterate] at h
  norm_num only [hb, h4, h5, hb2, mul_zero, zero_mul, add_zero, zero_add, sub_zero, zero_sub, false_and, and_false, true_and, and_true, if_true, if_false] at h
  simp only [seven_c3_eval_1_0_2 t hb h4 h5 hb2 x, seven_c3_eval_1_0_3 t hb h4 h5 hb2 x, seven_c3_eval_1_0_4 t hb h4 h5 hb2 x, seven_c3_eval_1_0_5 t hb h4 h5 hb2 x, seven_c3_eval_1_1_2 t hb h4 h5 hb2 x, seven_c3_eval_1_1_3 t hb h4 h5 hb2 x, seven_c3_eval_1_1_4 t hb h4 h5 hb2 x, seven_c3_eval_1_1_5 t hb h4 h5 hb2 x, seven_c3_eval_1_1_6 t hb h4 h5 hb2 x, seven_c3_eval_1_1_7 t hb h4 h5 hb2 x, seven_c3_eval_1_2_0 t hb h4 h5 hb2 x, seven_c3_eval_1_2_1 t hb h4 h5 hb2 x, seven_c3_eval_1_2_2 t hb h4 h5 hb2 x, seven_c3_eval_1_2_3 t hb h4 h5 hb2 x, seven_c3_eval_1_2_4 t hb h4 h5 hb2 x, seven_c3_eval_1_2_5 t hb h4 h5 hb2 x, seven_c3_eval_1_2_6 t hb h4 h5 hb2 x, seven_c3_eval_1_3_1 t hb h4 h5 hb2 x, seven_c3_eval_1_3_2 t hb h4 h5 hb2 x, seven_c3_eval_1_3_4 t hb h4 h5 hb2 x, seven_c3_eval_1_3_5 t hb h4 h5 hb2 x, seven_c3_eval_1_3_6 t hb h4 h5 hb2 x, seven_c3_eval_1_4_0 t hb h4 h5 hb2 x, seven_c3_eval_1_4_1 t hb h4 h5 hb2 x, seven_c3_eval_1_4_2 t hb h4 h5 hb2 x, seven_c3_eval_1_4_3 t hb h4 h5 hb2 x, seven_c3_eval_1_4_4 t hb h4 h5 hb2 x, seven_c3_eval_1_5_0 t hb h4 h5 hb2 x, seven_c3_eval_1_5_3 t hb h4 h5 hb2 x, seven_c3_eval_1_6_1 t hb h4 h5 hb2 x, seven_c3_eval_1_6_2 t hb h4 h5 hb2 x, seven_c3_eval_1_6_3 t hb h4 h5 hb2 x] at h
  linear_combination h

set_option maxHeartbeats 300000 in
lemma seven_c3_row_6 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (hb2 : t.b₂ = 0) (x : Fin 13 → K)
    (hf : Static t.toGateParameters ((bracket (hamiltonian t))^[1] (sevenCombination t x))) :
    ((144 * t.b₁) + (216 * t.c₃)) * x 4 + (72 * t.c₃) * x 5 + ((-2160) * t.c₂) * x 6 + ((-720) * t.c₁) * x 7 + (((-5040) * (t.b₁ ^ 2)) + ((-5040) * t.b₁ * t.c₃)) * x 8 + ((720 * t.b₁ * t.c₂) + (720 * t.c₂ * t.c₃)) * x 10 = 0 := by
  have h := third_recurrence t.toGateParameters _ hf 1 0
  simp only [bicoeff_seven_iterate] at h
  norm_num only [hb, h4, h5, hb2, mul_zero, zero_mul, add_zero, zero_add, sub_zero, zero_sub, false_and, and_false, true_and, and_true, if_true, if_false] at h
  simp only [seven_c3_eval_1_0_2 t hb h4 h5 hb2 x, seven_c3_eval_1_0_3 t hb h4 h5 hb2 x, seven_c3_eval_1_0_4 t hb h4 h5 hb2 x, seven_c3_eval_1_0_5 t hb h4 h5 hb2 x, seven_c3_eval_1_1_2 t hb h4 h5 hb2 x, seven_c3_eval_1_1_3 t hb h4 h5 hb2 x, seven_c3_eval_1_1_4 t hb h4 h5 hb2 x, seven_c3_eval_1_1_5 t hb h4 h5 hb2 x, seven_c3_eval_1_1_6 t hb h4 h5 hb2 x, seven_c3_eval_1_1_7 t hb h4 h5 hb2 x, seven_c3_eval_1_2_0 t hb h4 h5 hb2 x, seven_c3_eval_1_2_1 t hb h4 h5 hb2 x, seven_c3_eval_1_2_2 t hb h4 h5 hb2 x, seven_c3_eval_1_2_3 t hb h4 h5 hb2 x, seven_c3_eval_1_2_4 t hb h4 h5 hb2 x, seven_c3_eval_1_2_5 t hb h4 h5 hb2 x, seven_c3_eval_1_2_6 t hb h4 h5 hb2 x, seven_c3_eval_1_3_1 t hb h4 h5 hb2 x, seven_c3_eval_1_3_2 t hb h4 h5 hb2 x, seven_c3_eval_1_3_4 t hb h4 h5 hb2 x, seven_c3_eval_1_3_5 t hb h4 h5 hb2 x, seven_c3_eval_1_3_6 t hb h4 h5 hb2 x, seven_c3_eval_1_4_0 t hb h4 h5 hb2 x, seven_c3_eval_1_4_1 t hb h4 h5 hb2 x, seven_c3_eval_1_4_2 t hb h4 h5 hb2 x, seven_c3_eval_1_4_3 t hb h4 h5 hb2 x, seven_c3_eval_1_4_4 t hb h4 h5 hb2 x, seven_c3_eval_1_5_0 t hb h4 h5 hb2 x, seven_c3_eval_1_5_3 t hb h4 h5 hb2 x, seven_c3_eval_1_6_1 t hb h4 h5 hb2 x, seven_c3_eval_1_6_2 t hb h4 h5 hb2 x, seven_c3_eval_1_6_3 t hb h4 h5 hb2 x] at h
  linear_combination h

set_option maxHeartbeats 300000 in
lemma seven_c3_row_7 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (hb2 : t.b₂ = 0) (x : Fin 13 → K)
    (hf : Static t.toGateParameters ((bracket (hamiltonian t))^[1] (sevenCombination t x))) :
    (-144) * x 1 + ((1620 * t.c₃) + (2160 * t.b₁)) * x 6 + (720 * t.c₂) * x 7 + ((-5040) * t.c₁) * x 8 + (((-720) * (t.b₁ ^ 2)) + ((-720) * t.b₁ * t.c₃)) * x 10 = 0 := by
  have h := third_recurrence t.toGateParameters _ hf 0 1
  simp only [bicoeff_seven_iterate] at h
  norm_num only [hb, h4, h5, hb2, mul_zero, zero_mul, add_zero, zero_add, sub_zero, zero_sub, false_and, and_false, true_and, and_true, if_true, if_false] at h
  simp only [seven_c3_eval_1_0_2 t hb h4 h5 hb2 x, seven_c3_eval_1_0_3 t hb h4 h5 hb2 x, seven_c3_eval_1_0_4 t hb h4 h5 hb2 x, seven_c3_eval_1_0_5 t hb h4 h5 hb2 x, seven_c3_eval_1_1_2 t hb h4 h5 hb2 x, seven_c3_eval_1_1_3 t hb h4 h5 hb2 x, seven_c3_eval_1_1_4 t hb h4 h5 hb2 x, seven_c3_eval_1_1_5 t hb h4 h5 hb2 x, seven_c3_eval_1_1_6 t hb h4 h5 hb2 x, seven_c3_eval_1_1_7 t hb h4 h5 hb2 x, seven_c3_eval_1_2_0 t hb h4 h5 hb2 x, seven_c3_eval_1_2_1 t hb h4 h5 hb2 x, seven_c3_eval_1_2_2 t hb h4 h5 hb2 x, seven_c3_eval_1_2_3 t hb h4 h5 hb2 x, seven_c3_eval_1_2_4 t hb h4 h5 hb2 x, seven_c3_eval_1_2_5 t hb h4 h5 hb2 x, seven_c3_eval_1_2_6 t hb h4 h5 hb2 x, seven_c3_eval_1_3_1 t hb h4 h5 hb2 x, seven_c3_eval_1_3_2 t hb h4 h5 hb2 x, seven_c3_eval_1_3_4 t hb h4 h5 hb2 x, seven_c3_eval_1_3_5 t hb h4 h5 hb2 x, seven_c3_eval_1_3_6 t hb h4 h5 hb2 x, seven_c3_eval_1_4_0 t hb h4 h5 hb2 x, seven_c3_eval_1_4_1 t hb h4 h5 hb2 x, seven_c3_eval_1_4_2 t hb h4 h5 hb2 x, seven_c3_eval_1_4_3 t hb h4 h5 hb2 x, seven_c3_eval_1_4_4 t hb h4 h5 hb2 x, seven_c3_eval_1_5_0 t hb h4 h5 hb2 x, seven_c3_eval_1_5_3 t hb h4 h5 hb2 x, seven_c3_eval_1_6_1 t hb h4 h5 hb2 x, seven_c3_eval_1_6_2 t hb h4 h5 hb2 x, seven_c3_eval_1_6_3 t hb h4 h5 hb2 x] at h
  linear_combination h

set_option maxHeartbeats 300000 in
lemma seven_c3_row_8 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (hb2 : t.b₂ = 0) (x : Fin 13 → K)
    (hf : Static t.toGateParameters ((bracket (hamiltonian t))^[1] (sevenCombination t x))) :
    51840 * x 6 + ((37800 * t.c₃) + (45360 * t.b₁)) * x 9 + (((-17280) * t.b₁) + ((-10800) * t.c₃)) * x 10 + ((151200 * t.b₁ * t.c₂) + (151200 * t.c₂ * t.c₃)) * x 12 = 0 := by
  have h := third_recurrence t.toGateParameters _ hf 1 2
  simp only [bicoeff_seven_iterate] at h
  norm_num only [hb, h4, h5, hb2, mul_zero, zero_mul, add_zero, zero_add, sub_zero, zero_sub, false_and, and_false, true_and, and_true, if_true, if_false] at h
  simp only [seven_c3_eval_1_0_2 t hb h4 h5 hb2 x, seven_c3_eval_1_0_3 t hb h4 h5 hb2 x, seven_c3_eval_1_0_4 t hb h4 h5 hb2 x, seven_c3_eval_1_0_5 t hb h4 h5 hb2 x, seven_c3_eval_1_1_2 t hb h4 h5 hb2 x, seven_c3_eval_1_1_3 t hb h4 h5 hb2 x, seven_c3_eval_1_1_4 t hb h4 h5 hb2 x, seven_c3_eval_1_1_5 t hb h4 h5 hb2 x, seven_c3_eval_1_1_6 t hb h4 h5 hb2 x, seven_c3_eval_1_1_7 t hb h4 h5 hb2 x, seven_c3_eval_1_2_0 t hb h4 h5 hb2 x, seven_c3_eval_1_2_1 t hb h4 h5 hb2 x, seven_c3_eval_1_2_2 t hb h4 h5 hb2 x, seven_c3_eval_1_2_3 t hb h4 h5 hb2 x, seven_c3_eval_1_2_4 t hb h4 h5 hb2 x, seven_c3_eval_1_2_5 t hb h4 h5 hb2 x, seven_c3_eval_1_2_6 t hb h4 h5 hb2 x, seven_c3_eval_1_3_1 t hb h4 h5 hb2 x, seven_c3_eval_1_3_2 t hb h4 h5 hb2 x, seven_c3_eval_1_3_4 t hb h4 h5 hb2 x, seven_c3_eval_1_3_5 t hb h4 h5 hb2 x, seven_c3_eval_1_3_6 t hb h4 h5 hb2 x, seven_c3_eval_1_4_0 t hb h4 h5 hb2 x, seven_c3_eval_1_4_1 t hb h4 h5 hb2 x, seven_c3_eval_1_4_2 t hb h4 h5 hb2 x, seven_c3_eval_1_4_3 t hb h4 h5 hb2 x, seven_c3_eval_1_4_4 t hb h4 h5 hb2 x, seven_c3_eval_1_5_0 t hb h4 h5 hb2 x, seven_c3_eval_1_5_3 t hb h4 h5 hb2 x, seven_c3_eval_1_6_1 t hb h4 h5 hb2 x, seven_c3_eval_1_6_2 t hb h4 h5 hb2 x, seven_c3_eval_1_6_3 t hb h4 h5 hb2 x] at h
  linear_combination h

set_option maxHeartbeats 300000 in
lemma seven_c3_row_9 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (hb2 : t.b₂ = 0) (x : Fin 13 → K)
    (hf : Static t.toGateParameters ((bracket (hamiltonian t))^[1] (sevenCombination t x))) :
    (-25920) * x 6 + (((-267120) * t.c₃) + ((-191520) * t.b₁)) * x 9 + ((8640 * t.b₁) + (8640 * t.c₃)) * x 10 + (((-1008000) * t.b₁ * t.c₂) + ((-1008000) * t.c₂ * t.c₃)) * x 12 = 0 := by
  have h := third_recurrence t.toGateParameters _ hf 3 1
  simp only [bicoeff_seven_iterate] at h
  norm_num only [hb, h4, h5, hb2, mul_zero, zero_mul, add_zero, zero_add, sub_zero, zero_sub, false_and, and_false, true_and, and_true, if_true, if_false] at h
  simp only [seven_c3_eval_1_0_2 t hb h4 h5 hb2 x, seven_c3_eval_1_0_3 t hb h4 h5 hb2 x, seven_c3_eval_1_0_4 t hb h4 h5 hb2 x, seven_c3_eval_1_0_5 t hb h4 h5 hb2 x, seven_c3_eval_1_1_2 t hb h4 h5 hb2 x, seven_c3_eval_1_1_3 t hb h4 h5 hb2 x, seven_c3_eval_1_1_4 t hb h4 h5 hb2 x, seven_c3_eval_1_1_5 t hb h4 h5 hb2 x, seven_c3_eval_1_1_6 t hb h4 h5 hb2 x, seven_c3_eval_1_1_7 t hb h4 h5 hb2 x, seven_c3_eval_1_2_0 t hb h4 h5 hb2 x, seven_c3_eval_1_2_1 t hb h4 h5 hb2 x, seven_c3_eval_1_2_2 t hb h4 h5 hb2 x, seven_c3_eval_1_2_3 t hb h4 h5 hb2 x, seven_c3_eval_1_2_4 t hb h4 h5 hb2 x, seven_c3_eval_1_2_5 t hb h4 h5 hb2 x, seven_c3_eval_1_2_6 t hb h4 h5 hb2 x, seven_c3_eval_1_3_1 t hb h4 h5 hb2 x, seven_c3_eval_1_3_2 t hb h4 h5 hb2 x, seven_c3_eval_1_3_4 t hb h4 h5 hb2 x, seven_c3_eval_1_3_5 t hb h4 h5 hb2 x, seven_c3_eval_1_3_6 t hb h4 h5 hb2 x, seven_c3_eval_1_4_0 t hb h4 h5 hb2 x, seven_c3_eval_1_4_1 t hb h4 h5 hb2 x, seven_c3_eval_1_4_2 t hb h4 h5 hb2 x, seven_c3_eval_1_4_3 t hb h4 h5 hb2 x, seven_c3_eval_1_4_4 t hb h4 h5 hb2 x, seven_c3_eval_1_5_0 t hb h4 h5 hb2 x, seven_c3_eval_1_5_3 t hb h4 h5 hb2 x, seven_c3_eval_1_6_1 t hb h4 h5 hb2 x, seven_c3_eval_1_6_2 t hb h4 h5 hb2 x, seven_c3_eval_1_6_3 t hb h4 h5 hb2 x] at h
  linear_combination h

set_option maxHeartbeats 300000 in
lemma seven_c3_row_10 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (hb2 : t.b₂ = 0) (x : Fin 13 → K)
    (hf : Static t.toGateParameters ((bracket (hamiltonian t))^[2] (sevenCombination t x))) :
    (((-648) * t.c₃) + ((-288) * t.b₁)) * x 1 + ((-432) * t.c₃) * x 2 + (((-864) * t.b₀) + ((-504) * t.c₂)) * x 3 + ((-1008) * t.c₁) * x 4 + ((4320 * (t.b₁ ^ 2)) + (4860 * t.b₁ * t.c₃)) * x 6 + (((-17280) * t.b₀ * t.b₁) + ((-15120) * t.b₀ * t.c₃) + ((-1440) * t.b₁ * t.c₂)) * x 7 + ((20160 * (t.c₂ ^ 2)) + (105840 * t.c₁ * t.c₃) + (151200 * t.b₀ * t.c₂) + (151200 * t.b₁ * t.c₁)) * x 8 + ((10080 * t.b₀ * t.c₁) + (10080 * t.c₁ * t.c₂)) * x 9 + (((-1440) * (t.b₁ ^ 3)) + ((-1440) * t.c₃ * (t.b₁ ^ 2)) + (5760 * t.c₁ * t.c₂)) * x 10 + (((-30240) * t.c₁ * (t.b₁ ^ 2)) + ((-30240) * t.b₀ * t.b₁ * t.c₂) + ((-30240) * t.b₀ * t.c₂ * t.c₃) + ((-30240) * t.b₁ * t.c₁ * t.c₃)) * x 11 = 0 := by
  have h := third_recurrence t.toGateParameters _ hf 0 1
  simp only [bicoeff_seven_iterate] at h
  norm_num only [hb, h4, h5, hb2, mul_zero, zero_mul, add_zero, zero_add, sub_zero, zero_sub, false_and, and_false, true_and, and_true, if_true, if_false] at h
  simp only [seven_c3_eval_2_0_4 t hb h4 h5 hb2 x, seven_c3_eval_2_1_2 t hb h4 h5 hb2 x, seven_c3_eval_2_1_3 t hb h4 h5 hb2 x, seven_c3_eval_2_2_1 t hb h4 h5 hb2 x, seven_c3_eval_2_3_1 t hb h4 h5 hb2 x, seven_c3_eval_2_4_0 t hb h4 h5 hb2 x] at h
  linear_combination h

set_option maxHeartbeats 300000 in
lemma seven_c3_row_11 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (hb2 : t.b₂ = 0) (x : Fin 13 → K)
    (hf : Static t.toGateParameters ((bracket (hamiltonian t))^[2] (sevenCombination t x))) :
    ((-216) * t.c₃) * x 0 + ((-288) * t.c₂) * x 1 + (216 * t.c₁) * x 3 + (((-288) * (t.b₁ ^ 2)) + ((-648) * t.b₁ * t.c₃)) * x 4 + ((648 * (t.c₃ ^ 2)) + (288 * t.b₁ * t.c₃)) * x 5 + ((12960 * t.c₂ * t.c₃) + (21600 * t.b₁ * t.c₂) + (25920 * t.b₀ * t.b₁) + (43200 * t.b₀ * t.c₃)) * x 6 + ((5760 * (t.c₂ ^ 2)) + (15120 * t.c₁ * t.c₃) + (15840 * t.b₁ * t.c₁) + (18720 * t.b₀ * t.c₂)) * x 7 + ((10080 * (t.b₁ ^ 3)) + ((-201600) * t.c₁ * t.c₂) + ((-181440) * t.b₀ * t.c₁) + (10080 * t.c₃ * (t.b₁ ^ 2))) * x 8 + (((-10080) * (t.c₁ ^ 2)) + (10080 * t.b₀ * (t.b₁ ^ 2)) + (10080 * t.b₀ * t.b₁ * t.c₃)) * x 9 + (((-15120) * t.b₀ * (t.c₃ ^ 2)) + ((-8640) * t.b₀ * (t.b₁ ^ 2)) + ((-7200) * t.c₂ * (t.b₁ ^ 2)) + ((-23760) * t.b₀ * t.b₁ * t.c₃) + ((-7200) * t.b₁ * t.c₂ * t.c₃)) * x 10 + ((30240 * t.b₀ * t.b₁ * t.c₁) + (30240 * t.b₀ * t.c₁ * t.c₃) + (30240 * t.b₁ * t.c₁ * t.c₂) + (30240 * t.c₁ * t.c₂ * t.c₃)) * x 11 = 0 := by
  have h := third_recurrence t.toGateParameters _ hf 1 0
  simp only [bicoeff_seven_iterate] at h
  norm_num only [hb, h4, h5, hb2, mul_zero, zero_mul, add_zero, zero_add, sub_zero, zero_sub, false_and, and_false, true_and, and_true, if_true, if_false] at h
  simp only [seven_c3_eval_2_0_4 t hb h4 h5 hb2 x, seven_c3_eval_2_1_2 t hb h4 h5 hb2 x, seven_c3_eval_2_1_3 t hb h4 h5 hb2 x, seven_c3_eval_2_2_1 t hb h4 h5 hb2 x, seven_c3_eval_2_3_1 t hb h4 h5 hb2 x, seven_c3_eval_2_4_0 t hb h4 h5 hb2 x] at h
  linear_combination h

set_option maxHeartbeats 300000 in
lemma seven_c3_row_12 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (hb2 : t.b₂ = 0) (x : Fin 13 → K)
    (hf : Static t.toGateParameters ((bracket (hamiltonian t))^[1] (sevenCombination t x))) :
    (((-2419200) * t.b₁) + ((-2041200) * t.c₃)) * x 12 = 0 := by
  have h := third_recurrence t.toGateParameters _ hf 1 4
  simp only [bicoeff_seven_iterate] at h
  norm_num only [hb, h4, h5, hb2, mul_zero, zero_mul, add_zero, zero_add, sub_zero, zero_sub, false_and, and_false, true_and, and_true, if_true, if_false] at h
  simp only [seven_c3_eval_1_0_2 t hb h4 h5 hb2 x, seven_c3_eval_1_0_3 t hb h4 h5 hb2 x, seven_c3_eval_1_0_4 t hb h4 h5 hb2 x, seven_c3_eval_1_0_5 t hb h4 h5 hb2 x, seven_c3_eval_1_1_2 t hb h4 h5 hb2 x, seven_c3_eval_1_1_3 t hb h4 h5 hb2 x, seven_c3_eval_1_1_4 t hb h4 h5 hb2 x, seven_c3_eval_1_1_5 t hb h4 h5 hb2 x, seven_c3_eval_1_1_6 t hb h4 h5 hb2 x, seven_c3_eval_1_1_7 t hb h4 h5 hb2 x, seven_c3_eval_1_2_0 t hb h4 h5 hb2 x, seven_c3_eval_1_2_1 t hb h4 h5 hb2 x, seven_c3_eval_1_2_2 t hb h4 h5 hb2 x, seven_c3_eval_1_2_3 t hb h4 h5 hb2 x, seven_c3_eval_1_2_4 t hb h4 h5 hb2 x, seven_c3_eval_1_2_5 t hb h4 h5 hb2 x, seven_c3_eval_1_2_6 t hb h4 h5 hb2 x, seven_c3_eval_1_3_1 t hb h4 h5 hb2 x, seven_c3_eval_1_3_2 t hb h4 h5 hb2 x, seven_c3_eval_1_3_4 t hb h4 h5 hb2 x, seven_c3_eval_1_3_5 t hb h4 h5 hb2 x, seven_c3_eval_1_3_6 t hb h4 h5 hb2 x, seven_c3_eval_1_4_0 t hb h4 h5 hb2 x, seven_c3_eval_1_4_1 t hb h4 h5 hb2 x, seven_c3_eval_1_4_2 t hb h4 h5 hb2 x, seven_c3_eval_1_4_3 t hb h4 h5 hb2 x, seven_c3_eval_1_4_4 t hb h4 h5 hb2 x, seven_c3_eval_1_5_0 t hb h4 h5 hb2 x, seven_c3_eval_1_5_3 t hb h4 h5 hb2 x, seven_c3_eval_1_6_1 t hb h4 h5 hb2 x, seven_c3_eval_1_6_2 t hb h4 h5 hb2 x, seven_c3_eval_1_6_3 t hb h4 h5 hb2 x] at h
  linear_combination h

set_option maxHeartbeats 300000 in
lemma seven_c3_row_13 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (hb2 : t.b₂ = 0) (x : Fin 13 → K)
    (hf : Static t.toGateParameters ((bracket (hamiltonian t))^[1] (sevenCombination t x))) :
    ((16329600 * t.b₁) + (16329600 * t.c₃)) * x 12 = 0 := by
  have h := third_recurrence t.toGateParameters _ hf 3 3
  simp only [bicoeff_seven_iterate] at h
  norm_num only [hb, h4, h5, hb2, mul_zero, zero_mul, add_zero, zero_add, sub_zero, zero_sub, false_and, and_false, true_and, and_true, if_true, if_false] at h
  simp only [seven_c3_eval_1_0_2 t hb h4 h5 hb2 x, seven_c3_eval_1_0_3 t hb h4 h5 hb2 x, seven_c3_eval_1_0_4 t hb h4 h5 hb2 x, seven_c3_eval_1_0_5 t hb h4 h5 hb2 x, seven_c3_eval_1_1_2 t hb h4 h5 hb2 x, seven_c3_eval_1_1_3 t hb h4 h5 hb2 x, seven_c3_eval_1_1_4 t hb h4 h5 hb2 x, seven_c3_eval_1_1_5 t hb h4 h5 hb2 x, seven_c3_eval_1_1_6 t hb h4 h5 hb2 x, seven_c3_eval_1_1_7 t hb h4 h5 hb2 x, seven_c3_eval_1_2_0 t hb h4 h5 hb2 x, seven_c3_eval_1_2_1 t hb h4 h5 hb2 x, seven_c3_eval_1_2_2 t hb h4 h5 hb2 x, seven_c3_eval_1_2_3 t hb h4 h5 hb2 x, seven_c3_eval_1_2_4 t hb h4 h5 hb2 x, seven_c3_eval_1_2_5 t hb h4 h5 hb2 x, seven_c3_eval_1_2_6 t hb h4 h5 hb2 x, seven_c3_eval_1_3_1 t hb h4 h5 hb2 x, seven_c3_eval_1_3_2 t hb h4 h5 hb2 x, seven_c3_eval_1_3_4 t hb h4 h5 hb2 x, seven_c3_eval_1_3_5 t hb h4 h5 hb2 x, seven_c3_eval_1_3_6 t hb h4 h5 hb2 x, seven_c3_eval_1_4_0 t hb h4 h5 hb2 x, seven_c3_eval_1_4_1 t hb h4 h5 hb2 x, seven_c3_eval_1_4_2 t hb h4 h5 hb2 x, seven_c3_eval_1_4_3 t hb h4 h5 hb2 x, seven_c3_eval_1_4_4 t hb h4 h5 hb2 x, seven_c3_eval_1_5_0 t hb h4 h5 hb2 x, seven_c3_eval_1_5_3 t hb h4 h5 hb2 x, seven_c3_eval_1_6_1 t hb h4 h5 hb2 x, seven_c3_eval_1_6_2 t hb h4 h5 hb2 x, seven_c3_eval_1_6_3 t hb h4 h5 hb2 x] at h
  linear_combination h

end SexticC3.CubeLeading.Polynomial
