import SexticC3.CubeLeadingSevenEvaluateB2

/-! Generated exact coefficient equations. Each is derived from the actual
Hamiltonian iterate and the proved static recurrence; no matrix entries are hypotheses. -/
noncomputable section
set_option linter.unusedSectionVars false
namespace SexticC3.CubeLeading.Polynomial
open MvPolynomial
variable {K : Type*} [Field K] [CharZero K]

set_option maxHeartbeats 300000 in
lemma seven_b2_row_0 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K)
    (hf : Static t.toGateParameters ((bracket (hamiltonian t))^[1] (sevenCombination t x))) :
    (131040 * t.b₂) * x 12 = 0 := by
  have h := third_recurrence t.toGateParameters _ hf 0 5
  simp only [bicoeff_seven_iterate] at h
  norm_num only [hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, sub_zero, zero_sub, false_and, and_false, true_and, and_true, if_true, if_false] at h
  simp only [seven_b2_eval_1_0_2 t hb h4 h5 x, seven_b2_eval_1_0_3 t hb h4 h5 x, seven_b2_eval_1_0_4 t hb h4 h5 x, seven_b2_eval_1_0_5 t hb h4 h5 x, seven_b2_eval_1_0_6 t hb h4 h5 x, seven_b2_eval_1_0_7 t hb h4 h5 x, seven_b2_eval_1_0_8 t hb h4 h5 x, seven_b2_eval_1_1_1 t hb h4 h5 x, seven_b2_eval_1_1_2 t hb h4 h5 x, seven_b2_eval_1_1_3 t hb h4 h5 x, seven_b2_eval_1_1_4 t hb h4 h5 x, seven_b2_eval_1_1_5 t hb h4 h5 x, seven_b2_eval_1_1_6 t hb h4 h5 x, seven_b2_eval_1_1_7 t hb h4 h5 x, seven_b2_eval_1_2_0 t hb h4 h5 x, seven_b2_eval_1_2_1 t hb h4 h5 x, seven_b2_eval_1_2_2 t hb h4 h5 x, seven_b2_eval_1_2_3 t hb h4 h5 x, seven_b2_eval_1_2_4 t hb h4 h5 x, seven_b2_eval_1_2_5 t hb h4 h5 x, seven_b2_eval_1_2_6 t hb h4 h5 x, seven_b2_eval_1_3_0 t hb h4 h5 x, seven_b2_eval_1_3_1 t hb h4 h5 x, seven_b2_eval_1_3_2 t hb h4 h5 x, seven_b2_eval_1_3_3 t hb h4 h5 x, seven_b2_eval_1_3_4 t hb h4 h5 x, seven_b2_eval_1_3_5 t hb h4 h5 x, seven_b2_eval_1_4_1 t hb h4 h5 x, seven_b2_eval_1_4_2 t hb h4 h5 x, seven_b2_eval_1_4_3 t hb h4 h5 x, seven_b2_eval_1_5_1 t hb h4 h5 x, seven_b2_eval_1_5_2 t hb h4 h5 x, seven_b2_eval_1_5_3 t hb h4 h5 x] at h
  linear_combination h

set_option maxHeartbeats 300000 in
lemma seven_b2_row_1 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K)
    (hf : Static t.toGateParameters ((bracket (hamiltonian t))^[1] (sevenCombination t x))) :
    (-40320) * x 9 + (23940 * t.b₂) * x 11 + ((25200 * (t.b₂ ^ 2)) + (126000 * t.c₂)) * x 12 = 0 := by
  have h := third_recurrence t.toGateParameters _ hf 0 4
  simp only [bicoeff_seven_iterate] at h
  norm_num only [hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, sub_zero, zero_sub, false_and, and_false, true_and, and_true, if_true, if_false] at h
  simp only [seven_b2_eval_1_0_2 t hb h4 h5 x, seven_b2_eval_1_0_3 t hb h4 h5 x, seven_b2_eval_1_0_4 t hb h4 h5 x, seven_b2_eval_1_0_5 t hb h4 h5 x, seven_b2_eval_1_0_6 t hb h4 h5 x, seven_b2_eval_1_0_7 t hb h4 h5 x, seven_b2_eval_1_0_8 t hb h4 h5 x, seven_b2_eval_1_1_1 t hb h4 h5 x, seven_b2_eval_1_1_2 t hb h4 h5 x, seven_b2_eval_1_1_3 t hb h4 h5 x, seven_b2_eval_1_1_4 t hb h4 h5 x, seven_b2_eval_1_1_5 t hb h4 h5 x, seven_b2_eval_1_1_6 t hb h4 h5 x, seven_b2_eval_1_1_7 t hb h4 h5 x, seven_b2_eval_1_2_0 t hb h4 h5 x, seven_b2_eval_1_2_1 t hb h4 h5 x, seven_b2_eval_1_2_2 t hb h4 h5 x, seven_b2_eval_1_2_3 t hb h4 h5 x, seven_b2_eval_1_2_4 t hb h4 h5 x, seven_b2_eval_1_2_5 t hb h4 h5 x, seven_b2_eval_1_2_6 t hb h4 h5 x, seven_b2_eval_1_3_0 t hb h4 h5 x, seven_b2_eval_1_3_1 t hb h4 h5 x, seven_b2_eval_1_3_2 t hb h4 h5 x, seven_b2_eval_1_3_3 t hb h4 h5 x, seven_b2_eval_1_3_4 t hb h4 h5 x, seven_b2_eval_1_3_5 t hb h4 h5 x, seven_b2_eval_1_4_1 t hb h4 h5 x, seven_b2_eval_1_4_2 t hb h4 h5 x, seven_b2_eval_1_4_3 t hb h4 h5 x, seven_b2_eval_1_5_1 t hb h4 h5 x, seven_b2_eval_1_5_2 t hb h4 h5 x, seven_b2_eval_1_5_3 t hb h4 h5 x] at h
  linear_combination h

set_option maxHeartbeats 300000 in
lemma seven_b2_row_2 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K)
    (hf : Static t.toGateParameters ((bracket (hamiltonian t))^[1] (sevenCombination t x))) :
    816480 * x 9 + ((-272160) * t.b₂) * x 11 + ((-470400) * (t.b₂ ^ 2)) * x 12 = 0 := by
  have h := third_recurrence t.toGateParameters _ hf 2 3
  simp only [bicoeff_seven_iterate] at h
  norm_num only [hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, sub_zero, zero_sub, false_and, and_false, true_and, and_true, if_true, if_false] at h
  simp only [seven_b2_eval_1_0_2 t hb h4 h5 x, seven_b2_eval_1_0_3 t hb h4 h5 x, seven_b2_eval_1_0_4 t hb h4 h5 x, seven_b2_eval_1_0_5 t hb h4 h5 x, seven_b2_eval_1_0_6 t hb h4 h5 x, seven_b2_eval_1_0_7 t hb h4 h5 x, seven_b2_eval_1_0_8 t hb h4 h5 x, seven_b2_eval_1_1_1 t hb h4 h5 x, seven_b2_eval_1_1_2 t hb h4 h5 x, seven_b2_eval_1_1_3 t hb h4 h5 x, seven_b2_eval_1_1_4 t hb h4 h5 x, seven_b2_eval_1_1_5 t hb h4 h5 x, seven_b2_eval_1_1_6 t hb h4 h5 x, seven_b2_eval_1_1_7 t hb h4 h5 x, seven_b2_eval_1_2_0 t hb h4 h5 x, seven_b2_eval_1_2_1 t hb h4 h5 x, seven_b2_eval_1_2_2 t hb h4 h5 x, seven_b2_eval_1_2_3 t hb h4 h5 x, seven_b2_eval_1_2_4 t hb h4 h5 x, seven_b2_eval_1_2_5 t hb h4 h5 x, seven_b2_eval_1_2_6 t hb h4 h5 x, seven_b2_eval_1_3_0 t hb h4 h5 x, seven_b2_eval_1_3_1 t hb h4 h5 x, seven_b2_eval_1_3_2 t hb h4 h5 x, seven_b2_eval_1_3_3 t hb h4 h5 x, seven_b2_eval_1_3_4 t hb h4 h5 x, seven_b2_eval_1_3_5 t hb h4 h5 x, seven_b2_eval_1_4_1 t hb h4 h5 x, seven_b2_eval_1_4_2 t hb h4 h5 x, seven_b2_eval_1_4_3 t hb h4 h5 x, seven_b2_eval_1_5_1 t hb h4 h5 x, seven_b2_eval_1_5_2 t hb h4 h5 x, seven_b2_eval_1_5_3 t hb h4 h5 x] at h
  linear_combination h

set_option maxHeartbeats 300000 in
lemma seven_b2_row_3 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K)
    (hf : Static t.toGateParameters ((bracket (hamiltonian t))^[1] (sevenCombination t x))) :
    1632960 * x 8 + (((-272160) * t.b₁) + ((-211680) * t.c₃)) * x 11 + (((-470400) * t.b₁ * t.b₂) + ((-302400) * t.b₂ * t.c₃)) * x 12 = 0 := by
  have h := third_recurrence t.toGateParameters _ hf 1 3
  simp only [bicoeff_seven_iterate] at h
  norm_num only [hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, sub_zero, zero_sub, false_and, and_false, true_and, and_true, if_true, if_false] at h
  simp only [seven_b2_eval_1_0_2 t hb h4 h5 x, seven_b2_eval_1_0_3 t hb h4 h5 x, seven_b2_eval_1_0_4 t hb h4 h5 x, seven_b2_eval_1_0_5 t hb h4 h5 x, seven_b2_eval_1_0_6 t hb h4 h5 x, seven_b2_eval_1_0_7 t hb h4 h5 x, seven_b2_eval_1_0_8 t hb h4 h5 x, seven_b2_eval_1_1_1 t hb h4 h5 x, seven_b2_eval_1_1_2 t hb h4 h5 x, seven_b2_eval_1_1_3 t hb h4 h5 x, seven_b2_eval_1_1_4 t hb h4 h5 x, seven_b2_eval_1_1_5 t hb h4 h5 x, seven_b2_eval_1_1_6 t hb h4 h5 x, seven_b2_eval_1_1_7 t hb h4 h5 x, seven_b2_eval_1_2_0 t hb h4 h5 x, seven_b2_eval_1_2_1 t hb h4 h5 x, seven_b2_eval_1_2_2 t hb h4 h5 x, seven_b2_eval_1_2_3 t hb h4 h5 x, seven_b2_eval_1_2_4 t hb h4 h5 x, seven_b2_eval_1_2_5 t hb h4 h5 x, seven_b2_eval_1_2_6 t hb h4 h5 x, seven_b2_eval_1_3_0 t hb h4 h5 x, seven_b2_eval_1_3_1 t hb h4 h5 x, seven_b2_eval_1_3_2 t hb h4 h5 x, seven_b2_eval_1_3_3 t hb h4 h5 x, seven_b2_eval_1_3_4 t hb h4 h5 x, seven_b2_eval_1_3_5 t hb h4 h5 x, seven_b2_eval_1_4_1 t hb h4 h5 x, seven_b2_eval_1_4_2 t hb h4 h5 x, seven_b2_eval_1_4_3 t hb h4 h5 x, seven_b2_eval_1_5_1 t hb h4 h5 x, seven_b2_eval_1_5_2 t hb h4 h5 x, seven_b2_eval_1_5_3 t hb h4 h5 x] at h
  linear_combination h

set_option maxHeartbeats 300000 in
lemma seven_b2_row_4 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K)
    (hf : Static t.toGateParameters ((bracket (hamiltonian t))^[1] (sevenCombination t x))) :
    (-12960) * x 7 + ((-4200) * t.b₂) * x 9 + (3120 * t.b₂) * x 10 + ((4200 * (t.b₂ ^ 2)) + (20160 * t.c₂)) * x 11 + (((-50400) * (t.b₁ ^ 2)) + ((-50400) * t.b₁ * t.c₃) + ((-16800) * t.b₀ * t.b₂) + (16800 * t.b₂ * t.c₂)) * x 12 = 0 := by
  have h := third_recurrence t.toGateParameters _ hf 0 3
  simp only [bicoeff_seven_iterate] at h
  norm_num only [hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, sub_zero, zero_sub, false_and, and_false, true_and, and_true, if_true, if_false] at h
  simp only [seven_b2_eval_1_0_2 t hb h4 h5 x, seven_b2_eval_1_0_3 t hb h4 h5 x, seven_b2_eval_1_0_4 t hb h4 h5 x, seven_b2_eval_1_0_5 t hb h4 h5 x, seven_b2_eval_1_0_6 t hb h4 h5 x, seven_b2_eval_1_0_7 t hb h4 h5 x, seven_b2_eval_1_0_8 t hb h4 h5 x, seven_b2_eval_1_1_1 t hb h4 h5 x, seven_b2_eval_1_1_2 t hb h4 h5 x, seven_b2_eval_1_1_3 t hb h4 h5 x, seven_b2_eval_1_1_4 t hb h4 h5 x, seven_b2_eval_1_1_5 t hb h4 h5 x, seven_b2_eval_1_1_6 t hb h4 h5 x, seven_b2_eval_1_1_7 t hb h4 h5 x, seven_b2_eval_1_2_0 t hb h4 h5 x, seven_b2_eval_1_2_1 t hb h4 h5 x, seven_b2_eval_1_2_2 t hb h4 h5 x, seven_b2_eval_1_2_3 t hb h4 h5 x, seven_b2_eval_1_2_4 t hb h4 h5 x, seven_b2_eval_1_2_5 t hb h4 h5 x, seven_b2_eval_1_2_6 t hb h4 h5 x, seven_b2_eval_1_3_0 t hb h4 h5 x, seven_b2_eval_1_3_1 t hb h4 h5 x, seven_b2_eval_1_3_2 t hb h4 h5 x, seven_b2_eval_1_3_3 t hb h4 h5 x, seven_b2_eval_1_3_4 t hb h4 h5 x, seven_b2_eval_1_3_5 t hb h4 h5 x, seven_b2_eval_1_4_1 t hb h4 h5 x, seven_b2_eval_1_4_2 t hb h4 h5 x, seven_b2_eval_1_4_3 t hb h4 h5 x, seven_b2_eval_1_5_1 t hb h4 h5 x, seven_b2_eval_1_5_2 t hb h4 h5 x, seven_b2_eval_1_5_3 t hb h4 h5 x] at h
  linear_combination h

set_option maxHeartbeats 300000 in
lemma seven_b2_row_5 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K)
    (hf : Static t.toGateParameters ((bracket (hamiltonian t))^[1] (sevenCombination t x))) :
    103680 * x 7 + (262080 * t.b₂) * x 9 + ((-17280) * t.b₂) * x 10 + ((-63000) * (t.b₂ ^ 2)) * x 11 + ((1360800 * (t.b₁ ^ 2)) + (1360800 * (t.c₃ ^ 2)) + (151200 * t.b₂ * t.c₂) + (2721600 * t.b₁ * t.c₃)) * x 12 = 0 := by
  have h := third_recurrence t.toGateParameters _ hf 2 2
  simp only [bicoeff_seven_iterate] at h
  norm_num only [hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, sub_zero, zero_sub, false_and, and_false, true_and, and_true, if_true, if_false] at h
  simp only [seven_b2_eval_1_0_2 t hb h4 h5 x, seven_b2_eval_1_0_3 t hb h4 h5 x, seven_b2_eval_1_0_4 t hb h4 h5 x, seven_b2_eval_1_0_5 t hb h4 h5 x, seven_b2_eval_1_0_6 t hb h4 h5 x, seven_b2_eval_1_0_7 t hb h4 h5 x, seven_b2_eval_1_0_8 t hb h4 h5 x, seven_b2_eval_1_1_1 t hb h4 h5 x, seven_b2_eval_1_1_2 t hb h4 h5 x, seven_b2_eval_1_1_3 t hb h4 h5 x, seven_b2_eval_1_1_4 t hb h4 h5 x, seven_b2_eval_1_1_5 t hb h4 h5 x, seven_b2_eval_1_1_6 t hb h4 h5 x, seven_b2_eval_1_1_7 t hb h4 h5 x, seven_b2_eval_1_2_0 t hb h4 h5 x, seven_b2_eval_1_2_1 t hb h4 h5 x, seven_b2_eval_1_2_2 t hb h4 h5 x, seven_b2_eval_1_2_3 t hb h4 h5 x, seven_b2_eval_1_2_4 t hb h4 h5 x, seven_b2_eval_1_2_5 t hb h4 h5 x, seven_b2_eval_1_2_6 t hb h4 h5 x, seven_b2_eval_1_3_0 t hb h4 h5 x, seven_b2_eval_1_3_1 t hb h4 h5 x, seven_b2_eval_1_3_2 t hb h4 h5 x, seven_b2_eval_1_3_3 t hb h4 h5 x, seven_b2_eval_1_3_4 t hb h4 h5 x, seven_b2_eval_1_3_5 t hb h4 h5 x, seven_b2_eval_1_4_1 t hb h4 h5 x, seven_b2_eval_1_4_2 t hb h4 h5 x, seven_b2_eval_1_4_3 t hb h4 h5 x, seven_b2_eval_1_5_1 t hb h4 h5 x, seven_b2_eval_1_5_2 t hb h4 h5 x, seven_b2_eval_1_5_3 t hb h4 h5 x] at h
  linear_combination h

set_option maxHeartbeats 300000 in
lemma seven_b2_row_6 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K)
    (hf : Static t.toGateParameters ((bracket (hamiltonian t))^[1] (sevenCombination t x))) :
    (-576) * x 4 + ((-1440) * t.b₂) * x 7 + ((30240 * t.c₃) + (45360 * t.b₁)) * x 8 + (2520 * t.c₂) * x 9 + ((480 * (t.b₂ ^ 2)) + (2160 * t.c₂)) * x 10 + (((-7560) * (t.b₁ ^ 2)) + ((-7560) * t.b₁ * t.c₃) + ((-2520) * t.b₀ * t.b₂) + (2520 * t.b₂ * t.c₂)) * x 11 = 0 := by
  have h := third_recurrence t.toGateParameters _ hf 0 2
  simp only [bicoeff_seven_iterate] at h
  norm_num only [hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, sub_zero, zero_sub, false_and, and_false, true_and, and_true, if_true, if_false] at h
  simp only [seven_b2_eval_1_0_2 t hb h4 h5 x, seven_b2_eval_1_0_3 t hb h4 h5 x, seven_b2_eval_1_0_4 t hb h4 h5 x, seven_b2_eval_1_0_5 t hb h4 h5 x, seven_b2_eval_1_0_6 t hb h4 h5 x, seven_b2_eval_1_0_7 t hb h4 h5 x, seven_b2_eval_1_0_8 t hb h4 h5 x, seven_b2_eval_1_1_1 t hb h4 h5 x, seven_b2_eval_1_1_2 t hb h4 h5 x, seven_b2_eval_1_1_3 t hb h4 h5 x, seven_b2_eval_1_1_4 t hb h4 h5 x, seven_b2_eval_1_1_5 t hb h4 h5 x, seven_b2_eval_1_1_6 t hb h4 h5 x, seven_b2_eval_1_1_7 t hb h4 h5 x, seven_b2_eval_1_2_0 t hb h4 h5 x, seven_b2_eval_1_2_1 t hb h4 h5 x, seven_b2_eval_1_2_2 t hb h4 h5 x, seven_b2_eval_1_2_3 t hb h4 h5 x, seven_b2_eval_1_2_4 t hb h4 h5 x, seven_b2_eval_1_2_5 t hb h4 h5 x, seven_b2_eval_1_2_6 t hb h4 h5 x, seven_b2_eval_1_3_0 t hb h4 h5 x, seven_b2_eval_1_3_1 t hb h4 h5 x, seven_b2_eval_1_3_2 t hb h4 h5 x, seven_b2_eval_1_3_3 t hb h4 h5 x, seven_b2_eval_1_3_4 t hb h4 h5 x, seven_b2_eval_1_3_5 t hb h4 h5 x, seven_b2_eval_1_4_1 t hb h4 h5 x, seven_b2_eval_1_4_2 t hb h4 h5 x, seven_b2_eval_1_4_3 t hb h4 h5 x, seven_b2_eval_1_5_1 t hb h4 h5 x, seven_b2_eval_1_5_2 t hb h4 h5 x, seven_b2_eval_1_5_3 t hb h4 h5 x] at h
  linear_combination h

set_option maxHeartbeats 300000 in
lemma seven_b2_row_7 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K)
    (hf : Static t.toGateParameters ((bracket (hamiltonian t))^[1] (sevenCombination t x))) :
    51840 * x 6 + (433440 * t.b₂) * x 8 + ((37800 * t.c₃) + (45360 * t.b₁)) * x 9 + (((-17280) * t.b₁) + ((-10800) * t.c₃)) * x 10 + (((-63000) * t.b₁ * t.b₂) + ((-37800) * t.b₂ * t.c₃)) * x 11 + ((151200 * t.b₁ * t.c₂) + (151200 * t.c₂ * t.c₃)) * x 12 = 0 := by
  have h := third_recurrence t.toGateParameters _ hf 1 2
  simp only [bicoeff_seven_iterate] at h
  norm_num only [hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, sub_zero, zero_sub, false_and, and_false, true_and, and_true, if_true, if_false] at h
  simp only [seven_b2_eval_1_0_2 t hb h4 h5 x, seven_b2_eval_1_0_3 t hb h4 h5 x, seven_b2_eval_1_0_4 t hb h4 h5 x, seven_b2_eval_1_0_5 t hb h4 h5 x, seven_b2_eval_1_0_6 t hb h4 h5 x, seven_b2_eval_1_0_7 t hb h4 h5 x, seven_b2_eval_1_0_8 t hb h4 h5 x, seven_b2_eval_1_1_1 t hb h4 h5 x, seven_b2_eval_1_1_2 t hb h4 h5 x, seven_b2_eval_1_1_3 t hb h4 h5 x, seven_b2_eval_1_1_4 t hb h4 h5 x, seven_b2_eval_1_1_5 t hb h4 h5 x, seven_b2_eval_1_1_6 t hb h4 h5 x, seven_b2_eval_1_1_7 t hb h4 h5 x, seven_b2_eval_1_2_0 t hb h4 h5 x, seven_b2_eval_1_2_1 t hb h4 h5 x, seven_b2_eval_1_2_2 t hb h4 h5 x, seven_b2_eval_1_2_3 t hb h4 h5 x, seven_b2_eval_1_2_4 t hb h4 h5 x, seven_b2_eval_1_2_5 t hb h4 h5 x, seven_b2_eval_1_2_6 t hb h4 h5 x, seven_b2_eval_1_3_0 t hb h4 h5 x, seven_b2_eval_1_3_1 t hb h4 h5 x, seven_b2_eval_1_3_2 t hb h4 h5 x, seven_b2_eval_1_3_3 t hb h4 h5 x, seven_b2_eval_1_3_4 t hb h4 h5 x, seven_b2_eval_1_3_5 t hb h4 h5 x, seven_b2_eval_1_4_1 t hb h4 h5 x, seven_b2_eval_1_4_2 t hb h4 h5 x, seven_b2_eval_1_4_3 t hb h4 h5 x, seven_b2_eval_1_5_1 t hb h4 h5 x, seven_b2_eval_1_5_2 t hb h4 h5 x, seven_b2_eval_1_5_3 t hb h4 h5 x] at h
  linear_combination h

set_option maxHeartbeats 300000 in
lemma seven_b2_row_8 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K)
    (hf : Static t.toGateParameters ((bracket (hamiltonian t))^[1] (sevenCombination t x))) :
    432 * x 3 + (14400 * t.b₂) * x 6 + ((8640 * t.b₁) + (8640 * t.c₃)) * x 7 + (((-80640) * t.c₂) + (26880 * (t.b₂ ^ 2))) * x 8 + (((-5040) * t.c₁) + (3360 * t.b₁ * t.b₂)) * x 9 + (((-5280) * t.b₁ * t.b₂) + ((-2880) * t.b₂ * t.c₃)) * x 10 + ((15120 * t.b₁ * t.c₂) + (15120 * t.c₂ * t.c₃)) * x 11 = 0 := by
  have h := third_recurrence t.toGateParameters _ hf 1 1
  simp only [bicoeff_seven_iterate] at h
  norm_num only [hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, sub_zero, zero_sub, false_and, and_false, true_and, and_true, if_true, if_false] at h
  simp only [seven_b2_eval_1_0_2 t hb h4 h5 x, seven_b2_eval_1_0_3 t hb h4 h5 x, seven_b2_eval_1_0_4 t hb h4 h5 x, seven_b2_eval_1_0_5 t hb h4 h5 x, seven_b2_eval_1_0_6 t hb h4 h5 x, seven_b2_eval_1_0_7 t hb h4 h5 x, seven_b2_eval_1_0_8 t hb h4 h5 x, seven_b2_eval_1_1_1 t hb h4 h5 x, seven_b2_eval_1_1_2 t hb h4 h5 x, seven_b2_eval_1_1_3 t hb h4 h5 x, seven_b2_eval_1_1_4 t hb h4 h5 x, seven_b2_eval_1_1_5 t hb h4 h5 x, seven_b2_eval_1_1_6 t hb h4 h5 x, seven_b2_eval_1_1_7 t hb h4 h5 x, seven_b2_eval_1_2_0 t hb h4 h5 x, seven_b2_eval_1_2_1 t hb h4 h5 x, seven_b2_eval_1_2_2 t hb h4 h5 x, seven_b2_eval_1_2_3 t hb h4 h5 x, seven_b2_eval_1_2_4 t hb h4 h5 x, seven_b2_eval_1_2_5 t hb h4 h5 x, seven_b2_eval_1_2_6 t hb h4 h5 x, seven_b2_eval_1_3_0 t hb h4 h5 x, seven_b2_eval_1_3_1 t hb h4 h5 x, seven_b2_eval_1_3_2 t hb h4 h5 x, seven_b2_eval_1_3_3 t hb h4 h5 x, seven_b2_eval_1_3_4 t hb h4 h5 x, seven_b2_eval_1_3_5 t hb h4 h5 x, seven_b2_eval_1_4_1 t hb h4 h5 x, seven_b2_eval_1_4_2 t hb h4 h5 x, seven_b2_eval_1_4_3 t hb h4 h5 x, seven_b2_eval_1_5_1 t hb h4 h5 x, seven_b2_eval_1_5_2 t hb h4 h5 x, seven_b2_eval_1_5_3 t hb h4 h5 x] at h
  linear_combination h

set_option maxHeartbeats 300000 in
lemma seven_b2_row_9 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K)
    (hf : Static t.toGateParameters ((bracket (hamiltonian t))^[1] (sevenCombination t x))) :
    (-144) * x 1 + ((-72) * t.b₂) * x 4 + (96 * t.b₂) * x 5 + ((1620 * t.c₃) + (2160 * t.b₁)) * x 6 + (720 * t.c₂) * x 7 + (((-5040) * t.c₁) + (3360 * t.b₁ * t.b₂)) * x 8 + (((-720) * (t.b₁ ^ 2)) + ((-720) * t.b₁ * t.c₃) + ((-240) * t.b₀ * t.b₂) + (240 * t.b₂ * t.c₂)) * x 10 = 0 := by
  have h := third_recurrence t.toGateParameters _ hf 0 1
  simp only [bicoeff_seven_iterate] at h
  norm_num only [hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, sub_zero, zero_sub, false_and, and_false, true_and, and_true, if_true, if_false] at h
  simp only [seven_b2_eval_1_0_2 t hb h4 h5 x, seven_b2_eval_1_0_3 t hb h4 h5 x, seven_b2_eval_1_0_4 t hb h4 h5 x, seven_b2_eval_1_0_5 t hb h4 h5 x, seven_b2_eval_1_0_6 t hb h4 h5 x, seven_b2_eval_1_0_7 t hb h4 h5 x, seven_b2_eval_1_0_8 t hb h4 h5 x, seven_b2_eval_1_1_1 t hb h4 h5 x, seven_b2_eval_1_1_2 t hb h4 h5 x, seven_b2_eval_1_1_3 t hb h4 h5 x, seven_b2_eval_1_1_4 t hb h4 h5 x, seven_b2_eval_1_1_5 t hb h4 h5 x, seven_b2_eval_1_1_6 t hb h4 h5 x, seven_b2_eval_1_1_7 t hb h4 h5 x, seven_b2_eval_1_2_0 t hb h4 h5 x, seven_b2_eval_1_2_1 t hb h4 h5 x, seven_b2_eval_1_2_2 t hb h4 h5 x, seven_b2_eval_1_2_3 t hb h4 h5 x, seven_b2_eval_1_2_4 t hb h4 h5 x, seven_b2_eval_1_2_5 t hb h4 h5 x, seven_b2_eval_1_2_6 t hb h4 h5 x, seven_b2_eval_1_3_0 t hb h4 h5 x, seven_b2_eval_1_3_1 t hb h4 h5 x, seven_b2_eval_1_3_2 t hb h4 h5 x, seven_b2_eval_1_3_3 t hb h4 h5 x, seven_b2_eval_1_3_4 t hb h4 h5 x, seven_b2_eval_1_3_5 t hb h4 h5 x, seven_b2_eval_1_4_1 t hb h4 h5 x, seven_b2_eval_1_4_2 t hb h4 h5 x, seven_b2_eval_1_4_3 t hb h4 h5 x, seven_b2_eval_1_5_1 t hb h4 h5 x, seven_b2_eval_1_5_2 t hb h4 h5 x, seven_b2_eval_1_5_3 t hb h4 h5 x] at h
  linear_combination h

set_option maxHeartbeats 300000 in
lemma seven_b2_row_10 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K)
    (hf : Static t.toGateParameters ((bracket (hamiltonian t))^[1] (sevenCombination t x))) :
    ((-24) * t.b₂) * x 1 + (12 * t.b₂) * x 2 + ((36 * t.b₁) + (36 * t.c₃)) * x 3 + (24 * t.c₂) * x 4 + ((8 * (t.b₂ ^ 2)) + (24 * t.c₂)) * x 5 + (((-180) * t.c₁) + (120 * t.b₁ * t.b₂)) * x 6 = 0 := by
  have h := third_recurrence t.toGateParameters _ hf 0 0
  simp only [bicoeff_seven_iterate] at h
  norm_num only [hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, sub_zero, zero_sub, false_and, and_false, true_and, and_true, if_true, if_false] at h
  simp only [seven_b2_eval_1_0_2 t hb h4 h5 x, seven_b2_eval_1_0_3 t hb h4 h5 x, seven_b2_eval_1_0_4 t hb h4 h5 x, seven_b2_eval_1_0_5 t hb h4 h5 x, seven_b2_eval_1_0_6 t hb h4 h5 x, seven_b2_eval_1_0_7 t hb h4 h5 x, seven_b2_eval_1_0_8 t hb h4 h5 x, seven_b2_eval_1_1_1 t hb h4 h5 x, seven_b2_eval_1_1_2 t hb h4 h5 x, seven_b2_eval_1_1_3 t hb h4 h5 x, seven_b2_eval_1_1_4 t hb h4 h5 x, seven_b2_eval_1_1_5 t hb h4 h5 x, seven_b2_eval_1_1_6 t hb h4 h5 x, seven_b2_eval_1_1_7 t hb h4 h5 x, seven_b2_eval_1_2_0 t hb h4 h5 x, seven_b2_eval_1_2_1 t hb h4 h5 x, seven_b2_eval_1_2_2 t hb h4 h5 x, seven_b2_eval_1_2_3 t hb h4 h5 x, seven_b2_eval_1_2_4 t hb h4 h5 x, seven_b2_eval_1_2_5 t hb h4 h5 x, seven_b2_eval_1_2_6 t hb h4 h5 x, seven_b2_eval_1_3_0 t hb h4 h5 x, seven_b2_eval_1_3_1 t hb h4 h5 x, seven_b2_eval_1_3_2 t hb h4 h5 x, seven_b2_eval_1_3_3 t hb h4 h5 x, seven_b2_eval_1_3_4 t hb h4 h5 x, seven_b2_eval_1_3_5 t hb h4 h5 x, seven_b2_eval_1_4_1 t hb h4 h5 x, seven_b2_eval_1_4_2 t hb h4 h5 x, seven_b2_eval_1_4_3 t hb h4 h5 x, seven_b2_eval_1_5_1 t hb h4 h5 x, seven_b2_eval_1_5_2 t hb h4 h5 x, seven_b2_eval_1_5_3 t hb h4 h5 x] at h
  linear_combination h

set_option maxHeartbeats 300000 in
lemma seven_b2_row_11 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K)
    (hf : Static t.toGateParameters ((bracket (hamiltonian t))^[2] (sevenCombination t x))) :
    ((-864) * t.b₂) * x 1 + (((-4032) * t.c₂) + ((-3456) * t.b₀) + ((-720) * (t.b₂ ^ 2))) * x 4 + (1152 * (t.b₂ ^ 2)) * x 5 + ((90720 * t.c₁) + (14400 * t.b₁ * t.b₂) + (16200 * t.b₂ * t.c₃)) * x 6 + (((-123840) * t.b₀ * t.b₂) + ((-21600) * t.b₂ * t.c₂)) * x 7 + (((-6720) * t.b₁ * (t.b₂ ^ 2)) + (423360 * t.c₂ * t.c₃) + (745920 * t.b₁ * t.c₂) + (1239840 * t.b₂ * t.c₁) + (2298240 * t.b₀ * t.b₁) + (2419200 * t.b₀ * t.c₃)) * x 8 + ((40320 * (t.c₂ ^ 2)) + ((-60480) * t.b₀ * (t.b₂ ^ 2)) + ((-6720) * t.b₂ * (t.b₁ ^ 2)) + (136080 * t.c₁ * t.c₃) + (161280 * t.b₁ * t.c₁) + (171360 * t.b₀ * t.c₂)) * x 9 + ((11520 * (t.c₂ ^ 2)) + ((-30240) * t.b₁ * t.c₁) + ((-12960) * t.c₁ * t.c₃) + ((-3840) * t.b₂ * (t.b₁ ^ 2)) + (6240 * t.c₂ * (t.b₂ ^ 2)) + (13920 * t.b₀ * (t.b₂ ^ 2)) + (1440 * t.b₁ * t.b₂ * t.c₃)) * x 10 + (((-408240) * t.b₀ * (t.c₃ ^ 2)) + ((-362880) * t.b₀ * (t.b₁ ^ 2)) + ((-120960) * t.c₂ * (t.b₁ ^ 2)) + (20160 * t.b₂ * (t.c₂ ^ 2)) + ((-771120) * t.b₀ * t.b₁ * t.c₃) + ((-236880) * t.b₁ * t.b₂ * t.c₁) + ((-136080) * t.b₂ * t.c₁ * t.c₃) + ((-120960) * t.b₁ * t.c₂ * t.c₃) + ((-80640) * t.b₀ * t.b₂ * t.c₂)) * x 11 + (((-403200) * t.b₀ * t.b₂ * (t.b₁ ^ 2)) + (604800 * t.b₀ * t.b₁ * t.c₁) + (604800 * t.b₀ * t.c₁ * t.c₃) + (604800 * t.b₁ * t.c₁ * t.c₂) + (604800 * t.c₁ * t.c₂ * t.c₃) + ((-403200) * t.b₀ * t.b₁ * t.b₂ * t.c₃)) * x 12 = 0 := by
  have h := third_recurrence t.toGateParameters _ hf 1 1
  simp only [bicoeff_seven_iterate] at h
  norm_num only [hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, sub_zero, zero_sub, false_and, and_false, true_and, and_true, if_true, if_false] at h
  simp only [seven_b2_eval_2_0_4 t hb h4 h5 x, seven_b2_eval_2_1_2 t hb h4 h5 x, seven_b2_eval_2_1_3 t hb h4 h5 x, seven_b2_eval_2_1_4 t hb h4 h5 x, seven_b2_eval_2_2_2 t hb h4 h5 x, seven_b2_eval_2_2_3 t hb h4 h5 x, seven_b2_eval_2_3_1 t hb h4 h5 x, seven_b2_eval_2_4_1 t hb h4 h5 x] at h
  linear_combination h

set_option maxHeartbeats 300000 in
lemma seven_b2_row_12 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K)
    (hf : Static t.toGateParameters ((bracket (hamiltonian t))^[2] (sevenCombination t x))) :
    ((-144) * t.b₂) * x 0 + (((-648) * t.c₃) + ((-288) * t.b₁)) * x 1 + ((-432) * t.c₃) * x 2 + (((-864) * t.b₀) + ((-504) * t.c₂) + ((-144) * (t.b₂ ^ 2))) * x 3 + (((-1008) * t.c₁) + ((-72) * t.b₁ * t.b₂)) * x 4 + ((216 * t.b₂ * t.c₃) + (576 * t.b₁ * t.b₂)) * x 5 + ((4320 * (t.b₁ ^ 2)) + ((-22320) * t.b₀ * t.b₂) + ((-2160) * t.b₂ * t.c₂) + (4860 * t.b₁ * t.c₃)) * x 6 + (((-17280) * t.b₀ * t.b₁) + ((-15120) * t.b₀ * t.c₃) + ((-5040) * t.b₂ * t.c₁) + ((-1440) * t.b₁ * t.c₂)) * x 7 + ((20160 * (t.c₂ ^ 2)) + ((-47040) * t.b₀ * (t.b₂ ^ 2)) + (105840 * t.c₁ * t.c₃) + (151200 * t.b₀ * t.c₂) + (151200 * t.b₁ * t.c₁)) * x 8 + ((10080 * t.b₀ * t.c₁) + (10080 * t.c₁ * t.c₂) + ((-6720) * t.b₀ * t.b₁ * t.b₂)) * x 9 + (((-1440) * (t.b₁ ^ 3)) + ((-1440) * t.c₃ * (t.b₁ ^ 2)) + (1680 * t.c₁ * (t.b₂ ^ 2)) + (5760 * t.c₁ * t.c₂) + (1440 * t.b₁ * t.b₂ * t.c₂) + (5040 * t.b₀ * t.b₂ * t.c₃) + (6960 * t.b₀ * t.b₁ * t.b₂)) * x 10 + (((-30240) * t.c₁ * (t.b₁ ^ 2)) + ((-30240) * t.b₀ * t.b₁ * t.c₂) + ((-30240) * t.b₀ * t.c₂ * t.c₃) + ((-30240) * t.b₁ * t.c₁ * t.c₃) + ((-10080) * t.b₀ * t.b₂ * t.c₁) + (10080 * t.b₂ * t.c₁ * t.c₂)) * x 11 = 0 := by
  have h := third_recurrence t.toGateParameters _ hf 0 1
  simp only [bicoeff_seven_iterate] at h
  norm_num only [hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, sub_zero, zero_sub, false_and, and_false, true_and, and_true, if_true, if_false] at h
  simp only [seven_b2_eval_2_0_4 t hb h4 h5 x, seven_b2_eval_2_1_2 t hb h4 h5 x, seven_b2_eval_2_1_3 t hb h4 h5 x, seven_b2_eval_2_1_4 t hb h4 h5 x, seven_b2_eval_2_2_2 t hb h4 h5 x, seven_b2_eval_2_2_3 t hb h4 h5 x, seven_b2_eval_2_3_1 t hb h4 h5 x, seven_b2_eval_2_4_1 t hb h4 h5 x] at h
  linear_combination h

end SexticC3.CubeLeading.Polynomial
