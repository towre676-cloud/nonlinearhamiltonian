import SexticC3.CubeLeadingSevenEvaluation

/-! Generated exact coefficient equations. Each is derived from the actual
Hamiltonian iterate and the proved static recurrence; no matrix entries are hypotheses. -/
noncomputable section
set_option linter.unusedSectionVars false
namespace SexticC3.CubeLeading.Polynomial
open MvPolynomial
variable {K : Type*} [Field K] [CharZero K]

set_option maxHeartbeats 300000 in
lemma seven_b2_eval_0_0_1 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K) :
    sevenCoefficientAt t x 0 0 1 = 1 * x 2 := by
  norm_num only [sevenCoefficientAt_zero, sevenCoefficients, hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, false_and, and_false, true_and, and_true, if_true, if_false]
  all_goals ring

set_option maxHeartbeats 300000 in
lemma seven_b2_eval_0_0_2 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K) :
    sevenCoefficientAt t x 0 0 2 = 1 * x 5 := by
  norm_num only [sevenCoefficientAt_zero, sevenCoefficients, hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, false_and, and_false, true_and, and_true, if_true, if_false]
  all_goals ring

set_option maxHeartbeats 300000 in
lemma seven_b2_eval_0_0_3 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K) :
    sevenCoefficientAt t x 0 0 3 = 0 := by
  norm_num only [sevenCoefficientAt_zero, sevenCoefficients, hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, false_and, and_false, true_and, and_true, if_true, if_false]
  all_goals ring

set_option maxHeartbeats 300000 in
lemma seven_b2_eval_0_0_4 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K) :
    sevenCoefficientAt t x 0 0 4 = 5 * x 10 := by
  norm_num only [sevenCoefficientAt_zero, sevenCoefficients, hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, false_and, and_false, true_and, and_true, if_true, if_false]
  all_goals ring

set_option maxHeartbeats 300000 in
lemma seven_b2_eval_0_0_5 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K) :
    sevenCoefficientAt t x 0 0 5 = 21 * x 11 := by
  norm_num only [sevenCoefficientAt_zero, sevenCoefficients, hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, false_and, and_false, true_and, and_true, if_true, if_false]
  all_goals ring

set_option maxHeartbeats 300000 in
lemma seven_b2_eval_0_0_6 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K) :
    sevenCoefficientAt t x 0 0 6 = 70 * x 12 := by
  norm_num only [sevenCoefficientAt_zero, sevenCoefficients, hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, false_and, and_false, true_and, and_true, if_true, if_false]
  all_goals ring

set_option maxHeartbeats 300000 in
lemma seven_b2_eval_0_0_7 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K) :
    sevenCoefficientAt t x 0 0 7 = 0 := by
  norm_num only [sevenCoefficientAt_zero, sevenCoefficients, hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, false_and, and_false, true_and, and_true, if_true, if_false]
  all_goals ring

set_option maxHeartbeats 300000 in
lemma seven_b2_eval_0_0_8 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K) :
    sevenCoefficientAt t x 0 0 8 = 0 := by
  norm_num only [sevenCoefficientAt_zero, sevenCoefficients, hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, false_and, and_false, true_and, and_true, if_true, if_false]
  all_goals ring

set_option maxHeartbeats 300000 in
lemma seven_b2_eval_0_0_9 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K) :
    sevenCoefficientAt t x 0 0 9 = 0 := by
  norm_num only [sevenCoefficientAt_zero, sevenCoefficients, hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, false_and, and_false, true_and, and_true, if_true, if_false]
  all_goals ring

set_option maxHeartbeats 300000 in
lemma seven_b2_eval_0_1_0 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K) :
    sevenCoefficientAt t x 0 1 0 = 1 * x 0 := by
  norm_num only [sevenCoefficientAt_zero, sevenCoefficients, hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, false_and, and_false, true_and, and_true, if_true, if_false]
  all_goals ring

set_option maxHeartbeats 300000 in
lemma seven_b2_eval_0_1_1 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K) :
    sevenCoefficientAt t x 0 1 1 = 1 * x 3 := by
  norm_num only [sevenCoefficientAt_zero, sevenCoefficients, hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, false_and, and_false, true_and, and_true, if_true, if_false]
  all_goals ring

set_option maxHeartbeats 300000 in
lemma seven_b2_eval_0_1_2 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K) :
    sevenCoefficientAt t x 0 1 2 = 15 * x 6 := by
  norm_num only [sevenCoefficientAt_zero, sevenCoefficients, hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, false_and, and_false, true_and, and_true, if_true, if_false]
  all_goals ring

set_option maxHeartbeats 300000 in
lemma seven_b2_eval_0_1_3 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K) :
    sevenCoefficientAt t x 0 1 3 = 140 * x 8 := by
  norm_num only [sevenCoefficientAt_zero, sevenCoefficients, hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, false_and, and_false, true_and, and_true, if_true, if_false]
  all_goals ring

set_option maxHeartbeats 300000 in
lemma seven_b2_eval_0_1_4 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K) :
    sevenCoefficientAt t x 0 1 4 = 0 := by
  norm_num only [sevenCoefficientAt_zero, sevenCoefficients, hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, false_and, and_false, true_and, and_true, if_true, if_false]
  all_goals ring

set_option maxHeartbeats 300000 in
lemma seven_b2_eval_0_1_5 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K) :
    sevenCoefficientAt t x 0 1 5 = 0 := by
  norm_num only [sevenCoefficientAt_zero, sevenCoefficients, hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, false_and, and_false, true_and, and_true, if_true, if_false]
  all_goals ring

set_option maxHeartbeats 300000 in
lemma seven_b2_eval_0_1_6 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K) :
    sevenCoefficientAt t x 0 1 6 = 0 := by
  norm_num only [sevenCoefficientAt_zero, sevenCoefficients, hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, false_and, and_false, true_and, and_true, if_true, if_false]
  all_goals ring

set_option maxHeartbeats 300000 in
lemma seven_b2_eval_0_1_7 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K) :
    sevenCoefficientAt t x 0 1 7 = 0 := by
  norm_num only [sevenCoefficientAt_zero, sevenCoefficients, hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, false_and, and_false, true_and, and_true, if_true, if_false]
  all_goals ring

set_option maxHeartbeats 300000 in
lemma seven_b2_eval_0_1_8 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K) :
    sevenCoefficientAt t x 0 1 8 = 0 := by
  norm_num only [sevenCoefficientAt_zero, sevenCoefficients, hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, false_and, and_false, true_and, and_true, if_true, if_false]
  all_goals ring

set_option maxHeartbeats 300000 in
lemma seven_b2_eval_0_2_0 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K) :
    sevenCoefficientAt t x 0 2 0 = 1 * x 1 := by
  norm_num only [sevenCoefficientAt_zero, sevenCoefficients, hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, false_and, and_false, true_and, and_true, if_true, if_false]
  all_goals ring

set_option maxHeartbeats 300000 in
lemma seven_b2_eval_0_2_1 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K) :
    sevenCoefficientAt t x 0 2 1 = 2 * x 4 := by
  norm_num only [sevenCoefficientAt_zero, sevenCoefficients, hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, false_and, and_false, true_and, and_true, if_true, if_false]
  all_goals ring

set_option maxHeartbeats 300000 in
lemma seven_b2_eval_0_2_2 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K) :
    sevenCoefficientAt t x 0 2 2 = 30 * x 7 := by
  norm_num only [sevenCoefficientAt_zero, sevenCoefficients, hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, false_and, and_false, true_and, and_true, if_true, if_false]
  all_goals ring

set_option maxHeartbeats 300000 in
lemma seven_b2_eval_0_2_3 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K) :
    sevenCoefficientAt t x 0 2 3 = 70 * x 9 := by
  norm_num only [sevenCoefficientAt_zero, sevenCoefficients, hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, false_and, and_false, true_and, and_true, if_true, if_false]
  all_goals ring

set_option maxHeartbeats 300000 in
lemma seven_b2_eval_0_2_4 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K) :
    sevenCoefficientAt t x 0 2 4 = 0 := by
  norm_num only [sevenCoefficientAt_zero, sevenCoefficients, hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, false_and, and_false, true_and, and_true, if_true, if_false]
  all_goals ring

set_option maxHeartbeats 300000 in
lemma seven_b2_eval_0_2_5 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K) :
    sevenCoefficientAt t x 0 2 5 = 0 := by
  norm_num only [sevenCoefficientAt_zero, sevenCoefficients, hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, false_and, and_false, true_and, and_true, if_true, if_false]
  all_goals ring

set_option maxHeartbeats 300000 in
lemma seven_b2_eval_0_2_6 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K) :
    sevenCoefficientAt t x 0 2 6 = 0 := by
  norm_num only [sevenCoefficientAt_zero, sevenCoefficients, hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, false_and, and_false, true_and, and_true, if_true, if_false]
  all_goals ring

set_option maxHeartbeats 300000 in
lemma seven_b2_eval_0_2_7 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K) :
    sevenCoefficientAt t x 0 2 7 = 0 := by
  norm_num only [sevenCoefficientAt_zero, sevenCoefficients, hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, false_and, and_false, true_and, and_true, if_true, if_false]
  all_goals ring

set_option maxHeartbeats 300000 in
lemma seven_b2_eval_0_3_0 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K) :
    sevenCoefficientAt t x 0 3 0 = (-1) * x 3 + ((-5) * t.b₂) * x 6 := by
  norm_num only [sevenCoefficientAt_zero, sevenCoefficients, hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, false_and, and_false, true_and, and_true, if_true, if_false]
  all_goals ring

set_option maxHeartbeats 300000 in
lemma seven_b2_eval_0_3_1 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K) :
    sevenCoefficientAt t x 0 3 1 = (-60) * x 6 + ((-140) * t.b₂) * x 8 + ((20 * t.b₁) + (20 * t.c₃)) * x 10 := by
  norm_num only [sevenCoefficientAt_zero, sevenCoefficients, hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, false_and, and_false, true_and, and_true, if_true, if_false]
  all_goals ring

set_option maxHeartbeats 300000 in
lemma seven_b2_eval_0_3_2 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K) :
    sevenCoefficientAt t x 0 3 2 = (-1260) * x 8 + ((210 * t.b₁) + (210 * t.c₃)) * x 11 := by
  norm_num only [sevenCoefficientAt_zero, sevenCoefficients, hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, false_and, and_false, true_and, and_true, if_true, if_false]
  all_goals ring

set_option maxHeartbeats 300000 in
lemma seven_b2_eval_0_3_3 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K) :
    sevenCoefficientAt t x 0 3 3 = ((1400 * t.b₁) + (1400 * t.c₃)) * x 12 := by
  norm_num only [sevenCoefficientAt_zero, sevenCoefficients, hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, false_and, and_false, true_and, and_true, if_true, if_false]
  all_goals ring

set_option maxHeartbeats 300000 in
lemma seven_b2_eval_0_3_4 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K) :
    sevenCoefficientAt t x 0 3 4 = 0 := by
  norm_num only [sevenCoefficientAt_zero, sevenCoefficients, hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, false_and, and_false, true_and, and_true, if_true, if_false]
  all_goals ring

set_option maxHeartbeats 300000 in
lemma seven_b2_eval_0_3_5 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K) :
    sevenCoefficientAt t x 0 3 5 = 0 := by
  norm_num only [sevenCoefficientAt_zero, sevenCoefficients, hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, false_and, and_false, true_and, and_true, if_true, if_false]
  all_goals ring

set_option maxHeartbeats 300000 in
lemma seven_b2_eval_0_3_6 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K) :
    sevenCoefficientAt t x 0 3 6 = 0 := by
  norm_num only [sevenCoefficientAt_zero, sevenCoefficients, hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, false_and, and_false, true_and, and_true, if_true, if_false]
  all_goals ring

set_option maxHeartbeats 300000 in
lemma seven_b2_eval_0_4_0 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K) :
    sevenCoefficientAt t x 0 4 0 = (-1) * x 4 + ((-5) * t.b₂) * x 7 + ((35 * t.b₁) + (35 * t.c₃)) * x 8 := by
  norm_num only [sevenCoefficientAt_zero, sevenCoefficients, hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, false_and, and_false, true_and, and_true, if_true, if_false]
  all_goals ring

set_option maxHeartbeats 300000 in
lemma seven_b2_eval_0_4_1 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K) :
    sevenCoefficientAt t x 0 4 1 = (-60) * x 7 + ((-35) * t.b₂) * x 9 + (10 * t.b₂) * x 10 := by
  norm_num only [sevenCoefficientAt_zero, sevenCoefficients, hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, false_and, and_false, true_and, and_true, if_true, if_false]
  all_goals ring

set_option maxHeartbeats 300000 in
lemma seven_b2_eval_0_4_2 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K) :
    sevenCoefficientAt t x 0 4 2 = (-315) * x 9 + (105 * t.b₂) * x 11 := by
  norm_num only [sevenCoefficientAt_zero, sevenCoefficients, hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, false_and, and_false, true_and, and_true, if_true, if_false]
  all_goals ring

set_option maxHeartbeats 300000 in
lemma seven_b2_eval_0_4_3 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K) :
    sevenCoefficientAt t x 0 4 3 = (700 * t.b₂) * x 12 := by
  norm_num only [sevenCoefficientAt_zero, sevenCoefficients, hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, false_and, and_false, true_and, and_true, if_true, if_false]
  all_goals ring

set_option maxHeartbeats 300000 in
lemma seven_b2_eval_0_4_4 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K) :
    sevenCoefficientAt t x 0 4 4 = 0 := by
  norm_num only [sevenCoefficientAt_zero, sevenCoefficients, hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, false_and, and_false, true_and, and_true, if_true, if_false]
  all_goals ring

set_option maxHeartbeats 300000 in
lemma seven_b2_eval_0_4_5 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K) :
    sevenCoefficientAt t x 0 4 5 = 0 := by
  norm_num only [sevenCoefficientAt_zero, sevenCoefficients, hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, false_and, and_false, true_and, and_true, if_true, if_false]
  all_goals ring

set_option maxHeartbeats 300000 in
lemma seven_b2_eval_0_5_0 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K) :
    sevenCoefficientAt t x 0 5 0 = 18 * x 6 + (196 * t.b₂) * x 8 + ((7 * t.b₁) + (7 * t.c₃)) * x 9 + (((-6) * t.b₁) + ((-6) * t.c₃)) * x 10 + (((-21) * t.b₁ * t.b₂) + ((-21) * t.b₂ * t.c₃)) * x 11 := by
  norm_num only [sevenCoefficientAt_zero, sevenCoefficients, hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, false_and, and_false, true_and, and_true, if_true, if_false]
  all_goals ring

set_option maxHeartbeats 300000 in
lemma seven_b2_eval_0_5_1 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K) :
    sevenCoefficientAt t x 0 5 1 = 1512 * x 8 + (((-252) * t.b₁) + ((-252) * t.c₃)) * x 11 + (((-420) * t.b₁ * t.b₂) + ((-420) * t.b₂ * t.c₃)) * x 12 := by
  norm_num only [sevenCoefficientAt_zero, sevenCoefficients, hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, false_and, and_false, true_and, and_true, if_true, if_false]
  all_goals ring

set_option maxHeartbeats 300000 in
lemma seven_b2_eval_0_5_2 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K) :
    sevenCoefficientAt t x 0 5 2 = (((-3780) * t.b₁) + ((-3780) * t.c₃)) * x 12 := by
  norm_num only [sevenCoefficientAt_zero, sevenCoefficients, hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, false_and, and_false, true_and, and_true, if_true, if_false]
  all_goals ring

set_option maxHeartbeats 300000 in
lemma seven_b2_eval_0_5_3 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K) :
    sevenCoefficientAt t x 0 5 3 = 0 := by
  norm_num only [sevenCoefficientAt_zero, sevenCoefficients, hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, false_and, and_false, true_and, and_true, if_true, if_false]
  all_goals ring

set_option maxHeartbeats 300000 in
lemma seven_b2_eval_0_5_4 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K) :
    sevenCoefficientAt t x 0 5 4 = 0 := by
  norm_num only [sevenCoefficientAt_zero, sevenCoefficients, hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, false_and, and_false, true_and, and_true, if_true, if_false]
  all_goals ring

set_option maxHeartbeats 300000 in
lemma seven_b2_eval_0_6_0 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K) :
    sevenCoefficientAt t x 0 6 0 = 12 * x 7 + (35 * t.b₂) * x 9 + ((-2) * t.b₂) * x 10 + ((-7) * (t.b₂ ^ 2)) * x 11 + ((70 * (t.b₁ ^ 2)) + (70 * (t.c₃ ^ 2)) + (140 * t.b₁ * t.c₃)) * x 12 := by
  norm_num only [sevenCoefficientAt_zero, sevenCoefficients, hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, false_and, and_false, true_and, and_true, if_true, if_false]
  all_goals ring

set_option maxHeartbeats 300000 in
lemma seven_b2_eval_0_6_1 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K) :
    sevenCoefficientAt t x 0 6 1 = 252 * x 9 + ((-84) * t.b₂) * x 11 + ((-140) * (t.b₂ ^ 2)) * x 12 := by
  norm_num only [sevenCoefficientAt_zero, sevenCoefficients, hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, false_and, and_false, true_and, and_true, if_true, if_false]
  all_goals ring

set_option maxHeartbeats 300000 in
lemma seven_b2_eval_0_6_2 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K) :
    sevenCoefficientAt t x 0 6 2 = ((-1260) * t.b₂) * x 12 := by
  norm_num only [sevenCoefficientAt_zero, sevenCoefficients, hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, false_and, and_false, true_and, and_true, if_true, if_false]
  all_goals ring

set_option maxHeartbeats 300000 in
lemma seven_b2_eval_0_6_3 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K) :
    sevenCoefficientAt t x 0 6 3 = 0 := by
  norm_num only [sevenCoefficientAt_zero, sevenCoefficients, hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, false_and, and_false, true_and, and_true, if_true, if_false]
  all_goals ring

set_option maxHeartbeats 300000 in
lemma seven_b2_eval_1_0_2 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K) :
    sevenCoefficientAt t x 1 0 2 = (-3) * x 0 + (2 * t.b₁) * x 5 + ((-15) * t.b₀) * x 6 := by
  rw [sevenCoefficientAt_succ]
  norm_num only [coefficientBracket, coeffDq, coeffDP, coeffQ, coeffP, hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, sub_zero, zero_sub, false_and, and_false, true_and, and_true, if_true, if_false]
  simp only [seven_b2_eval_0_0_1 t hb h4 h5 x, seven_b2_eval_0_0_2 t hb h4 h5 x, seven_b2_eval_0_0_3 t hb h4 h5 x, seven_b2_eval_0_0_4 t hb h4 h5 x, seven_b2_eval_0_0_5 t hb h4 h5 x, seven_b2_eval_0_0_6 t hb h4 h5 x, seven_b2_eval_0_0_7 t hb h4 h5 x, seven_b2_eval_0_0_8 t hb h4 h5 x, seven_b2_eval_0_0_9 t hb h4 h5 x, seven_b2_eval_0_1_0 t hb h4 h5 x, seven_b2_eval_0_1_1 t hb h4 h5 x, seven_b2_eval_0_1_2 t hb h4 h5 x, seven_b2_eval_0_1_3 t hb h4 h5 x, seven_b2_eval_0_1_4 t hb h4 h5 x, seven_b2_eval_0_1_5 t hb h4 h5 x, seven_b2_eval_0_1_6 t hb h4 h5 x, seven_b2_eval_0_1_7 t hb h4 h5 x, seven_b2_eval_0_1_8 t hb h4 h5 x, seven_b2_eval_0_2_0 t hb h4 h5 x, seven_b2_eval_0_2_1 t hb h4 h5 x, seven_b2_eval_0_2_2 t hb h4 h5 x, seven_b2_eval_0_2_3 t hb h4 h5 x, seven_b2_eval_0_2_4 t hb h4 h5 x, seven_b2_eval_0_2_5 t hb h4 h5 x, seven_b2_eval_0_2_6 t hb h4 h5 x, seven_b2_eval_0_2_7 t hb h4 h5 x, seven_b2_eval_0_3_0 t hb h4 h5 x, seven_b2_eval_0_3_1 t hb h4 h5 x, seven_b2_eval_0_3_2 t hb h4 h5 x, seven_b2_eval_0_3_3 t hb h4 h5 x, seven_b2_eval_0_3_4 t hb h4 h5 x, seven_b2_eval_0_3_5 t hb h4 h5 x, seven_b2_eval_0_3_6 t hb h4 h5 x, seven_b2_eval_0_4_0 t hb h4 h5 x, seven_b2_eval_0_4_1 t hb h4 h5 x, seven_b2_eval_0_4_2 t hb h4 h5 x, seven_b2_eval_0_4_3 t hb h4 h5 x, seven_b2_eval_0_4_4 t hb h4 h5 x, seven_b2_eval_0_4_5 t hb h4 h5 x, seven_b2_eval_0_5_0 t hb h4 h5 x, seven_b2_eval_0_5_1 t hb h4 h5 x, seven_b2_eval_0_5_2 t hb h4 h5 x, seven_b2_eval_0_5_3 t hb h4 h5 x, seven_b2_eval_0_5_4 t hb h4 h5 x, seven_b2_eval_0_6_0 t hb h4 h5 x, seven_b2_eval_0_6_1 t hb h4 h5 x, seven_b2_eval_0_6_2 t hb h4 h5 x, seven_b2_eval_0_6_3 t hb h4 h5 x]
  all_goals ring

set_option maxHeartbeats 300000 in
lemma seven_b2_eval_1_0_3 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K) :
    sevenCoefficientAt t x 1 0 3 = (-3) * x 3 + ((-140) * t.b₀) * x 8 + (20 * t.c₁) * x 10 := by
  rw [sevenCoefficientAt_succ]
  norm_num only [coefficientBracket, coeffDq, coeffDP, coeffQ, coeffP, hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, sub_zero, zero_sub, false_and, and_false, true_and, and_true, if_true, if_false]
  simp only [seven_b2_eval_0_0_1 t hb h4 h5 x, seven_b2_eval_0_0_2 t hb h4 h5 x, seven_b2_eval_0_0_3 t hb h4 h5 x, seven_b2_eval_0_0_4 t hb h4 h5 x, seven_b2_eval_0_0_5 t hb h4 h5 x, seven_b2_eval_0_0_6 t hb h4 h5 x, seven_b2_eval_0_0_7 t hb h4 h5 x, seven_b2_eval_0_0_8 t hb h4 h5 x, seven_b2_eval_0_0_9 t hb h4 h5 x, seven_b2_eval_0_1_0 t hb h4 h5 x, seven_b2_eval_0_1_1 t hb h4 h5 x, seven_b2_eval_0_1_2 t hb h4 h5 x, seven_b2_eval_0_1_3 t hb h4 h5 x, seven_b2_eval_0_1_4 t hb h4 h5 x, seven_b2_eval_0_1_5 t hb h4 h5 x, seven_b2_eval_0_1_6 t hb h4 h5 x, seven_b2_eval_0_1_7 t hb h4 h5 x, seven_b2_eval_0_1_8 t hb h4 h5 x, seven_b2_eval_0_2_0 t hb h4 h5 x, seven_b2_eval_0_2_1 t hb h4 h5 x, seven_b2_eval_0_2_2 t hb h4 h5 x, seven_b2_eval_0_2_3 t hb h4 h5 x, seven_b2_eval_0_2_4 t hb h4 h5 x, seven_b2_eval_0_2_5 t hb h4 h5 x, seven_b2_eval_0_2_6 t hb h4 h5 x, seven_b2_eval_0_2_7 t hb h4 h5 x, seven_b2_eval_0_3_0 t hb h4 h5 x, seven_b2_eval_0_3_1 t hb h4 h5 x, seven_b2_eval_0_3_2 t hb h4 h5 x, seven_b2_eval_0_3_3 t hb h4 h5 x, seven_b2_eval_0_3_4 t hb h4 h5 x, seven_b2_eval_0_3_5 t hb h4 h5 x, seven_b2_eval_0_3_6 t hb h4 h5 x, seven_b2_eval_0_4_0 t hb h4 h5 x, seven_b2_eval_0_4_1 t hb h4 h5 x, seven_b2_eval_0_4_2 t hb h4 h5 x, seven_b2_eval_0_4_3 t hb h4 h5 x, seven_b2_eval_0_4_4 t hb h4 h5 x, seven_b2_eval_0_4_5 t hb h4 h5 x, seven_b2_eval_0_5_0 t hb h4 h5 x, seven_b2_eval_0_5_1 t hb h4 h5 x, seven_b2_eval_0_5_2 t hb h4 h5 x, seven_b2_eval_0_5_3 t hb h4 h5 x, seven_b2_eval_0_5_4 t hb h4 h5 x, seven_b2_eval_0_6_0 t hb h4 h5 x, seven_b2_eval_0_6_1 t hb h4 h5 x, seven_b2_eval_0_6_2 t hb h4 h5 x, seven_b2_eval_0_6_3 t hb h4 h5 x]
  all_goals ring

set_option maxHeartbeats 300000 in
lemma seven_b2_eval_1_0_4 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K) :
    sevenCoefficientAt t x 1 0 4 = (-45) * x 6 + (20 * t.b₁) * x 10 + (105 * t.c₁) * x 11 := by
  rw [sevenCoefficientAt_succ]
  norm_num only [coefficientBracket, coeffDq, coeffDP, coeffQ, coeffP, hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, sub_zero, zero_sub, false_and, and_false, true_and, and_true, if_true, if_false]
  simp only [seven_b2_eval_0_0_1 t hb h4 h5 x, seven_b2_eval_0_0_2 t hb h4 h5 x, seven_b2_eval_0_0_3 t hb h4 h5 x, seven_b2_eval_0_0_4 t hb h4 h5 x, seven_b2_eval_0_0_5 t hb h4 h5 x, seven_b2_eval_0_0_6 t hb h4 h5 x, seven_b2_eval_0_0_7 t hb h4 h5 x, seven_b2_eval_0_0_8 t hb h4 h5 x, seven_b2_eval_0_0_9 t hb h4 h5 x, seven_b2_eval_0_1_0 t hb h4 h5 x, seven_b2_eval_0_1_1 t hb h4 h5 x, seven_b2_eval_0_1_2 t hb h4 h5 x, seven_b2_eval_0_1_3 t hb h4 h5 x, seven_b2_eval_0_1_4 t hb h4 h5 x, seven_b2_eval_0_1_5 t hb h4 h5 x, seven_b2_eval_0_1_6 t hb h4 h5 x, seven_b2_eval_0_1_7 t hb h4 h5 x, seven_b2_eval_0_1_8 t hb h4 h5 x, seven_b2_eval_0_2_0 t hb h4 h5 x, seven_b2_eval_0_2_1 t hb h4 h5 x, seven_b2_eval_0_2_2 t hb h4 h5 x, seven_b2_eval_0_2_3 t hb h4 h5 x, seven_b2_eval_0_2_4 t hb h4 h5 x, seven_b2_eval_0_2_5 t hb h4 h5 x, seven_b2_eval_0_2_6 t hb h4 h5 x, seven_b2_eval_0_2_7 t hb h4 h5 x, seven_b2_eval_0_3_0 t hb h4 h5 x, seven_b2_eval_0_3_1 t hb h4 h5 x, seven_b2_eval_0_3_2 t hb h4 h5 x, seven_b2_eval_0_3_3 t hb h4 h5 x, seven_b2_eval_0_3_4 t hb h4 h5 x, seven_b2_eval_0_3_5 t hb h4 h5 x, seven_b2_eval_0_3_6 t hb h4 h5 x, seven_b2_eval_0_4_0 t hb h4 h5 x, seven_b2_eval_0_4_1 t hb h4 h5 x, seven_b2_eval_0_4_2 t hb h4 h5 x, seven_b2_eval_0_4_3 t hb h4 h5 x, seven_b2_eval_0_4_4 t hb h4 h5 x, seven_b2_eval_0_4_5 t hb h4 h5 x, seven_b2_eval_0_5_0 t hb h4 h5 x, seven_b2_eval_0_5_1 t hb h4 h5 x, seven_b2_eval_0_5_2 t hb h4 h5 x, seven_b2_eval_0_5_3 t hb h4 h5 x, seven_b2_eval_0_5_4 t hb h4 h5 x, seven_b2_eval_0_6_0 t hb h4 h5 x, seven_b2_eval_0_6_1 t hb h4 h5 x, seven_b2_eval_0_6_2 t hb h4 h5 x, seven_b2_eval_0_6_3 t hb h4 h5 x]
  all_goals ring

set_option maxHeartbeats 300000 in
lemma seven_b2_eval_1_0_5 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K) :
    sevenCoefficientAt t x 1 0 5 = (-420) * x 8 + (105 * t.b₁) * x 11 + (420 * t.c₁) * x 12 := by
  rw [sevenCoefficientAt_succ]
  norm_num only [coefficientBracket, coeffDq, coeffDP, coeffQ, coeffP, hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, sub_zero, zero_sub, false_and, and_false, true_and, and_true, if_true, if_false]
  simp only [seven_b2_eval_0_0_1 t hb h4 h5 x, seven_b2_eval_0_0_2 t hb h4 h5 x, seven_b2_eval_0_0_3 t hb h4 h5 x, seven_b2_eval_0_0_4 t hb h4 h5 x, seven_b2_eval_0_0_5 t hb h4 h5 x, seven_b2_eval_0_0_6 t hb h4 h5 x, seven_b2_eval_0_0_7 t hb h4 h5 x, seven_b2_eval_0_0_8 t hb h4 h5 x, seven_b2_eval_0_0_9 t hb h4 h5 x, seven_b2_eval_0_1_0 t hb h4 h5 x, seven_b2_eval_0_1_1 t hb h4 h5 x, seven_b2_eval_0_1_2 t hb h4 h5 x, seven_b2_eval_0_1_3 t hb h4 h5 x, seven_b2_eval_0_1_4 t hb h4 h5 x, seven_b2_eval_0_1_5 t hb h4 h5 x, seven_b2_eval_0_1_6 t hb h4 h5 x, seven_b2_eval_0_1_7 t hb h4 h5 x, seven_b2_eval_0_1_8 t hb h4 h5 x, seven_b2_eval_0_2_0 t hb h4 h5 x, seven_b2_eval_0_2_1 t hb h4 h5 x, seven_b2_eval_0_2_2 t hb h4 h5 x, seven_b2_eval_0_2_3 t hb h4 h5 x, seven_b2_eval_0_2_4 t hb h4 h5 x, seven_b2_eval_0_2_5 t hb h4 h5 x, seven_b2_eval_0_2_6 t hb h4 h5 x, seven_b2_eval_0_2_7 t hb h4 h5 x, seven_b2_eval_0_3_0 t hb h4 h5 x, seven_b2_eval_0_3_1 t hb h4 h5 x, seven_b2_eval_0_3_2 t hb h4 h5 x, seven_b2_eval_0_3_3 t hb h4 h5 x, seven_b2_eval_0_3_4 t hb h4 h5 x, seven_b2_eval_0_3_5 t hb h4 h5 x, seven_b2_eval_0_3_6 t hb h4 h5 x, seven_b2_eval_0_4_0 t hb h4 h5 x, seven_b2_eval_0_4_1 t hb h4 h5 x, seven_b2_eval_0_4_2 t hb h4 h5 x, seven_b2_eval_0_4_3 t hb h4 h5 x, seven_b2_eval_0_4_4 t hb h4 h5 x, seven_b2_eval_0_4_5 t hb h4 h5 x, seven_b2_eval_0_5_0 t hb h4 h5 x, seven_b2_eval_0_5_1 t hb h4 h5 x, seven_b2_eval_0_5_2 t hb h4 h5 x, seven_b2_eval_0_5_3 t hb h4 h5 x, seven_b2_eval_0_5_4 t hb h4 h5 x, seven_b2_eval_0_6_0 t hb h4 h5 x, seven_b2_eval_0_6_1 t hb h4 h5 x, seven_b2_eval_0_6_2 t hb h4 h5 x, seven_b2_eval_0_6_3 t hb h4 h5 x]
  all_goals ring

set_option maxHeartbeats 300000 in
lemma seven_b2_eval_1_0_6 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K) :
    sevenCoefficientAt t x 1 0 6 = (420 * t.b₁) * x 12 := by
  rw [sevenCoefficientAt_succ]
  norm_num only [coefficientBracket, coeffDq, coeffDP, coeffQ, coeffP, hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, sub_zero, zero_sub, false_and, and_false, true_and, and_true, if_true, if_false]
  simp only [seven_b2_eval_0_0_1 t hb h4 h5 x, seven_b2_eval_0_0_2 t hb h4 h5 x, seven_b2_eval_0_0_3 t hb h4 h5 x, seven_b2_eval_0_0_4 t hb h4 h5 x, seven_b2_eval_0_0_5 t hb h4 h5 x, seven_b2_eval_0_0_6 t hb h4 h5 x, seven_b2_eval_0_0_7 t hb h4 h5 x, seven_b2_eval_0_0_8 t hb h4 h5 x, seven_b2_eval_0_0_9 t hb h4 h5 x, seven_b2_eval_0_1_0 t hb h4 h5 x, seven_b2_eval_0_1_1 t hb h4 h5 x, seven_b2_eval_0_1_2 t hb h4 h5 x, seven_b2_eval_0_1_3 t hb h4 h5 x, seven_b2_eval_0_1_4 t hb h4 h5 x, seven_b2_eval_0_1_5 t hb h4 h5 x, seven_b2_eval_0_1_6 t hb h4 h5 x, seven_b2_eval_0_1_7 t hb h4 h5 x, seven_b2_eval_0_1_8 t hb h4 h5 x, seven_b2_eval_0_2_0 t hb h4 h5 x, seven_b2_eval_0_2_1 t hb h4 h5 x, seven_b2_eval_0_2_2 t hb h4 h5 x, seven_b2_eval_0_2_3 t hb h4 h5 x, seven_b2_eval_0_2_4 t hb h4 h5 x, seven_b2_eval_0_2_5 t hb h4 h5 x, seven_b2_eval_0_2_6 t hb h4 h5 x, seven_b2_eval_0_2_7 t hb h4 h5 x, seven_b2_eval_0_3_0 t hb h4 h5 x, seven_b2_eval_0_3_1 t hb h4 h5 x, seven_b2_eval_0_3_2 t hb h4 h5 x, seven_b2_eval_0_3_3 t hb h4 h5 x, seven_b2_eval_0_3_4 t hb h4 h5 x, seven_b2_eval_0_3_5 t hb h4 h5 x, seven_b2_eval_0_3_6 t hb h4 h5 x, seven_b2_eval_0_4_0 t hb h4 h5 x, seven_b2_eval_0_4_1 t hb h4 h5 x, seven_b2_eval_0_4_2 t hb h4 h5 x, seven_b2_eval_0_4_3 t hb h4 h5 x, seven_b2_eval_0_4_4 t hb h4 h5 x, seven_b2_eval_0_4_5 t hb h4 h5 x, seven_b2_eval_0_5_0 t hb h4 h5 x, seven_b2_eval_0_5_1 t hb h4 h5 x, seven_b2_eval_0_5_2 t hb h4 h5 x, seven_b2_eval_0_5_3 t hb h4 h5 x, seven_b2_eval_0_5_4 t hb h4 h5 x, seven_b2_eval_0_6_0 t hb h4 h5 x, seven_b2_eval_0_6_1 t hb h4 h5 x, seven_b2_eval_0_6_2 t hb h4 h5 x, seven_b2_eval_0_6_3 t hb h4 h5 x]
  all_goals ring

set_option maxHeartbeats 300000 in
lemma seven_b2_eval_1_0_7 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K) :
    sevenCoefficientAt t x 1 0 7 = 0 := by
  rw [sevenCoefficientAt_succ]
  norm_num only [coefficientBracket, coeffDq, coeffDP, coeffQ, coeffP, hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, sub_zero, zero_sub, false_and, and_false, true_and, and_true, if_true, if_false]
  simp only [seven_b2_eval_0_0_1 t hb h4 h5 x, seven_b2_eval_0_0_2 t hb h4 h5 x, seven_b2_eval_0_0_3 t hb h4 h5 x, seven_b2_eval_0_0_4 t hb h4 h5 x, seven_b2_eval_0_0_5 t hb h4 h5 x, seven_b2_eval_0_0_6 t hb h4 h5 x, seven_b2_eval_0_0_7 t hb h4 h5 x, seven_b2_eval_0_0_8 t hb h4 h5 x, seven_b2_eval_0_0_9 t hb h4 h5 x, seven_b2_eval_0_1_0 t hb h4 h5 x, seven_b2_eval_0_1_1 t hb h4 h5 x, seven_b2_eval_0_1_2 t hb h4 h5 x, seven_b2_eval_0_1_3 t hb h4 h5 x, seven_b2_eval_0_1_4 t hb h4 h5 x, seven_b2_eval_0_1_5 t hb h4 h5 x, seven_b2_eval_0_1_6 t hb h4 h5 x, seven_b2_eval_0_1_7 t hb h4 h5 x, seven_b2_eval_0_1_8 t hb h4 h5 x, seven_b2_eval_0_2_0 t hb h4 h5 x, seven_b2_eval_0_2_1 t hb h4 h5 x, seven_b2_eval_0_2_2 t hb h4 h5 x, seven_b2_eval_0_2_3 t hb h4 h5 x, seven_b2_eval_0_2_4 t hb h4 h5 x, seven_b2_eval_0_2_5 t hb h4 h5 x, seven_b2_eval_0_2_6 t hb h4 h5 x, seven_b2_eval_0_2_7 t hb h4 h5 x, seven_b2_eval_0_3_0 t hb h4 h5 x, seven_b2_eval_0_3_1 t hb h4 h5 x, seven_b2_eval_0_3_2 t hb h4 h5 x, seven_b2_eval_0_3_3 t hb h4 h5 x, seven_b2_eval_0_3_4 t hb h4 h5 x, seven_b2_eval_0_3_5 t hb h4 h5 x, seven_b2_eval_0_3_6 t hb h4 h5 x, seven_b2_eval_0_4_0 t hb h4 h5 x, seven_b2_eval_0_4_1 t hb h4 h5 x, seven_b2_eval_0_4_2 t hb h4 h5 x, seven_b2_eval_0_4_3 t hb h4 h5 x, seven_b2_eval_0_4_4 t hb h4 h5 x, seven_b2_eval_0_4_5 t hb h4 h5 x, seven_b2_eval_0_5_0 t hb h4 h5 x, seven_b2_eval_0_5_1 t hb h4 h5 x, seven_b2_eval_0_5_2 t hb h4 h5 x, seven_b2_eval_0_5_3 t hb h4 h5 x, seven_b2_eval_0_5_4 t hb h4 h5 x, seven_b2_eval_0_6_0 t hb h4 h5 x, seven_b2_eval_0_6_1 t hb h4 h5 x, seven_b2_eval_0_6_2 t hb h4 h5 x, seven_b2_eval_0_6_3 t hb h4 h5 x]
  all_goals ring

set_option maxHeartbeats 300000 in
lemma seven_b2_eval_1_0_8 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K) :
    sevenCoefficientAt t x 1 0 8 = 0 := by
  rw [sevenCoefficientAt_succ]
  norm_num only [coefficientBracket, coeffDq, coeffDP, coeffQ, coeffP, hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, sub_zero, zero_sub, false_and, and_false, true_and, and_true, if_true, if_false]
  simp only [seven_b2_eval_0_0_1 t hb h4 h5 x, seven_b2_eval_0_0_2 t hb h4 h5 x, seven_b2_eval_0_0_3 t hb h4 h5 x, seven_b2_eval_0_0_4 t hb h4 h5 x, seven_b2_eval_0_0_5 t hb h4 h5 x, seven_b2_eval_0_0_6 t hb h4 h5 x, seven_b2_eval_0_0_7 t hb h4 h5 x, seven_b2_eval_0_0_8 t hb h4 h5 x, seven_b2_eval_0_0_9 t hb h4 h5 x, seven_b2_eval_0_1_0 t hb h4 h5 x, seven_b2_eval_0_1_1 t hb h4 h5 x, seven_b2_eval_0_1_2 t hb h4 h5 x, seven_b2_eval_0_1_3 t hb h4 h5 x, seven_b2_eval_0_1_4 t hb h4 h5 x, seven_b2_eval_0_1_5 t hb h4 h5 x, seven_b2_eval_0_1_6 t hb h4 h5 x, seven_b2_eval_0_1_7 t hb h4 h5 x, seven_b2_eval_0_1_8 t hb h4 h5 x, seven_b2_eval_0_2_0 t hb h4 h5 x, seven_b2_eval_0_2_1 t hb h4 h5 x, seven_b2_eval_0_2_2 t hb h4 h5 x, seven_b2_eval_0_2_3 t hb h4 h5 x, seven_b2_eval_0_2_4 t hb h4 h5 x, seven_b2_eval_0_2_5 t hb h4 h5 x, seven_b2_eval_0_2_6 t hb h4 h5 x, seven_b2_eval_0_2_7 t hb h4 h5 x, seven_b2_eval_0_3_0 t hb h4 h5 x, seven_b2_eval_0_3_1 t hb h4 h5 x, seven_b2_eval_0_3_2 t hb h4 h5 x, seven_b2_eval_0_3_3 t hb h4 h5 x, seven_b2_eval_0_3_4 t hb h4 h5 x, seven_b2_eval_0_3_5 t hb h4 h5 x, seven_b2_eval_0_3_6 t hb h4 h5 x, seven_b2_eval_0_4_0 t hb h4 h5 x, seven_b2_eval_0_4_1 t hb h4 h5 x, seven_b2_eval_0_4_2 t hb h4 h5 x, seven_b2_eval_0_4_3 t hb h4 h5 x, seven_b2_eval_0_4_4 t hb h4 h5 x, seven_b2_eval_0_4_5 t hb h4 h5 x, seven_b2_eval_0_5_0 t hb h4 h5 x, seven_b2_eval_0_5_1 t hb h4 h5 x, seven_b2_eval_0_5_2 t hb h4 h5 x, seven_b2_eval_0_5_3 t hb h4 h5 x, seven_b2_eval_0_5_4 t hb h4 h5 x, seven_b2_eval_0_6_0 t hb h4 h5 x, seven_b2_eval_0_6_1 t hb h4 h5 x, seven_b2_eval_0_6_2 t hb h4 h5 x, seven_b2_eval_0_6_3 t hb h4 h5 x]
  all_goals ring

set_option maxHeartbeats 300000 in
lemma seven_b2_eval_1_1_1 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K) :
    sevenCoefficientAt t x 1 1 1 = (2 * t.b₂) * x 2 + ((-4) * t.b₀) * x 4 + (4 * t.c₂) * x 5 + (30 * t.c₁) * x 6 := by
  rw [sevenCoefficientAt_succ]
  norm_num only [coefficientBracket, coeffDq, coeffDP, coeffQ, coeffP, hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, sub_zero, zero_sub, false_and, and_false, true_and, and_true, if_true, if_false]
  simp only [seven_b2_eval_0_0_1 t hb h4 h5 x, seven_b2_eval_0_0_2 t hb h4 h5 x, seven_b2_eval_0_0_3 t hb h4 h5 x, seven_b2_eval_0_0_4 t hb h4 h5 x, seven_b2_eval_0_0_5 t hb h4 h5 x, seven_b2_eval_0_0_6 t hb h4 h5 x, seven_b2_eval_0_0_7 t hb h4 h5 x, seven_b2_eval_0_0_8 t hb h4 h5 x, seven_b2_eval_0_0_9 t hb h4 h5 x, seven_b2_eval_0_1_0 t hb h4 h5 x, seven_b2_eval_0_1_1 t hb h4 h5 x, seven_b2_eval_0_1_2 t hb h4 h5 x, seven_b2_eval_0_1_3 t hb h4 h5 x, seven_b2_eval_0_1_4 t hb h4 h5 x, seven_b2_eval_0_1_5 t hb h4 h5 x, seven_b2_eval_0_1_6 t hb h4 h5 x, seven_b2_eval_0_1_7 t hb h4 h5 x, seven_b2_eval_0_1_8 t hb h4 h5 x, seven_b2_eval_0_2_0 t hb h4 h5 x, seven_b2_eval_0_2_1 t hb h4 h5 x, seven_b2_eval_0_2_2 t hb h4 h5 x, seven_b2_eval_0_2_3 t hb h4 h5 x, seven_b2_eval_0_2_4 t hb h4 h5 x, seven_b2_eval_0_2_5 t hb h4 h5 x, seven_b2_eval_0_2_6 t hb h4 h5 x, seven_b2_eval_0_2_7 t hb h4 h5 x, seven_b2_eval_0_3_0 t hb h4 h5 x, seven_b2_eval_0_3_1 t hb h4 h5 x, seven_b2_eval_0_3_2 t hb h4 h5 x, seven_b2_eval_0_3_3 t hb h4 h5 x, seven_b2_eval_0_3_4 t hb h4 h5 x, seven_b2_eval_0_3_5 t hb h4 h5 x, seven_b2_eval_0_3_6 t hb h4 h5 x, seven_b2_eval_0_4_0 t hb h4 h5 x, seven_b2_eval_0_4_1 t hb h4 h5 x, seven_b2_eval_0_4_2 t hb h4 h5 x, seven_b2_eval_0_4_3 t hb h4 h5 x, seven_b2_eval_0_4_4 t hb h4 h5 x, seven_b2_eval_0_4_5 t hb h4 h5 x, seven_b2_eval_0_5_0 t hb h4 h5 x, seven_b2_eval_0_5_1 t hb h4 h5 x, seven_b2_eval_0_5_2 t hb h4 h5 x, seven_b2_eval_0_5_3 t hb h4 h5 x, seven_b2_eval_0_5_4 t hb h4 h5 x, seven_b2_eval_0_6_0 t hb h4 h5 x, seven_b2_eval_0_6_1 t hb h4 h5 x, seven_b2_eval_0_6_2 t hb h4 h5 x, seven_b2_eval_0_6_3 t hb h4 h5 x]
  all_goals ring

set_option maxHeartbeats 300000 in
lemma seven_b2_eval_1_1_2 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K) :
    sevenCoefficientAt t x 1 1 2 = (-6) * x 1 + (4 * t.b₂) * x 5 + (15 * t.b₁) * x 6 + ((-60) * t.b₀) * x 7 + (420 * t.c₁) * x 8 := by
  rw [sevenCoefficientAt_succ]
  norm_num only [coefficientBracket, coeffDq, coeffDP, coeffQ, coeffP, hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, sub_zero, zero_sub, false_and, and_false, true_and, and_true, if_true, if_false]
  simp only [seven_b2_eval_0_0_1 t hb h4 h5 x, seven_b2_eval_0_0_2 t hb h4 h5 x, seven_b2_eval_0_0_3 t hb h4 h5 x, seven_b2_eval_0_0_4 t hb h4 h5 x, seven_b2_eval_0_0_5 t hb h4 h5 x, seven_b2_eval_0_0_6 t hb h4 h5 x, seven_b2_eval_0_0_7 t hb h4 h5 x, seven_b2_eval_0_0_8 t hb h4 h5 x, seven_b2_eval_0_0_9 t hb h4 h5 x, seven_b2_eval_0_1_0 t hb h4 h5 x, seven_b2_eval_0_1_1 t hb h4 h5 x, seven_b2_eval_0_1_2 t hb h4 h5 x, seven_b2_eval_0_1_3 t hb h4 h5 x, seven_b2_eval_0_1_4 t hb h4 h5 x, seven_b2_eval_0_1_5 t hb h4 h5 x, seven_b2_eval_0_1_6 t hb h4 h5 x, seven_b2_eval_0_1_7 t hb h4 h5 x, seven_b2_eval_0_1_8 t hb h4 h5 x, seven_b2_eval_0_2_0 t hb h4 h5 x, seven_b2_eval_0_2_1 t hb h4 h5 x, seven_b2_eval_0_2_2 t hb h4 h5 x, seven_b2_eval_0_2_3 t hb h4 h5 x, seven_b2_eval_0_2_4 t hb h4 h5 x, seven_b2_eval_0_2_5 t hb h4 h5 x, seven_b2_eval_0_2_6 t hb h4 h5 x, seven_b2_eval_0_2_7 t hb h4 h5 x, seven_b2_eval_0_3_0 t hb h4 h5 x, seven_b2_eval_0_3_1 t hb h4 h5 x, seven_b2_eval_0_3_2 t hb h4 h5 x, seven_b2_eval_0_3_3 t hb h4 h5 x, seven_b2_eval_0_3_4 t hb h4 h5 x, seven_b2_eval_0_3_5 t hb h4 h5 x, seven_b2_eval_0_3_6 t hb h4 h5 x, seven_b2_eval_0_4_0 t hb h4 h5 x, seven_b2_eval_0_4_1 t hb h4 h5 x, seven_b2_eval_0_4_2 t hb h4 h5 x, seven_b2_eval_0_4_3 t hb h4 h5 x, seven_b2_eval_0_4_4 t hb h4 h5 x, seven_b2_eval_0_4_5 t hb h4 h5 x, seven_b2_eval_0_5_0 t hb h4 h5 x, seven_b2_eval_0_5_1 t hb h4 h5 x, seven_b2_eval_0_5_2 t hb h4 h5 x, seven_b2_eval_0_5_3 t hb h4 h5 x, seven_b2_eval_0_5_4 t hb h4 h5 x, seven_b2_eval_0_6_0 t hb h4 h5 x, seven_b2_eval_0_6_1 t hb h4 h5 x, seven_b2_eval_0_6_2 t hb h4 h5 x, seven_b2_eval_0_6_3 t hb h4 h5 x]
  all_goals ring

set_option maxHeartbeats 300000 in
lemma seven_b2_eval_1_1_3 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K) :
    sevenCoefficientAt t x 1 1 3 = (-12) * x 4 + (280 * t.b₁) * x 8 + ((-140) * t.b₀) * x 9 + (40 * t.c₂) * x 10 := by
  rw [sevenCoefficientAt_succ]
  norm_num only [coefficientBracket, coeffDq, coeffDP, coeffQ, coeffP, hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, sub_zero, zero_sub, false_and, and_false, true_and, and_true, if_true, if_false]
  simp only [seven_b2_eval_0_0_1 t hb h4 h5 x, seven_b2_eval_0_0_2 t hb h4 h5 x, seven_b2_eval_0_0_3 t hb h4 h5 x, seven_b2_eval_0_0_4 t hb h4 h5 x, seven_b2_eval_0_0_5 t hb h4 h5 x, seven_b2_eval_0_0_6 t hb h4 h5 x, seven_b2_eval_0_0_7 t hb h4 h5 x, seven_b2_eval_0_0_8 t hb h4 h5 x, seven_b2_eval_0_0_9 t hb h4 h5 x, seven_b2_eval_0_1_0 t hb h4 h5 x, seven_b2_eval_0_1_1 t hb h4 h5 x, seven_b2_eval_0_1_2 t hb h4 h5 x, seven_b2_eval_0_1_3 t hb h4 h5 x, seven_b2_eval_0_1_4 t hb h4 h5 x, seven_b2_eval_0_1_5 t hb h4 h5 x, seven_b2_eval_0_1_6 t hb h4 h5 x, seven_b2_eval_0_1_7 t hb h4 h5 x, seven_b2_eval_0_1_8 t hb h4 h5 x, seven_b2_eval_0_2_0 t hb h4 h5 x, seven_b2_eval_0_2_1 t hb h4 h5 x, seven_b2_eval_0_2_2 t hb h4 h5 x, seven_b2_eval_0_2_3 t hb h4 h5 x, seven_b2_eval_0_2_4 t hb h4 h5 x, seven_b2_eval_0_2_5 t hb h4 h5 x, seven_b2_eval_0_2_6 t hb h4 h5 x, seven_b2_eval_0_2_7 t hb h4 h5 x, seven_b2_eval_0_3_0 t hb h4 h5 x, seven_b2_eval_0_3_1 t hb h4 h5 x, seven_b2_eval_0_3_2 t hb h4 h5 x, seven_b2_eval_0_3_3 t hb h4 h5 x, seven_b2_eval_0_3_4 t hb h4 h5 x, seven_b2_eval_0_3_5 t hb h4 h5 x, seven_b2_eval_0_3_6 t hb h4 h5 x, seven_b2_eval_0_4_0 t hb h4 h5 x, seven_b2_eval_0_4_1 t hb h4 h5 x, seven_b2_eval_0_4_2 t hb h4 h5 x, seven_b2_eval_0_4_3 t hb h4 h5 x, seven_b2_eval_0_4_4 t hb h4 h5 x, seven_b2_eval_0_4_5 t hb h4 h5 x, seven_b2_eval_0_5_0 t hb h4 h5 x, seven_b2_eval_0_5_1 t hb h4 h5 x, seven_b2_eval_0_5_2 t hb h4 h5 x, seven_b2_eval_0_5_3 t hb h4 h5 x, seven_b2_eval_0_5_4 t hb h4 h5 x, seven_b2_eval_0_6_0 t hb h4 h5 x, seven_b2_eval_0_6_1 t hb h4 h5 x, seven_b2_eval_0_6_2 t hb h4 h5 x, seven_b2_eval_0_6_3 t hb h4 h5 x]
  all_goals ring

set_option maxHeartbeats 300000 in
lemma seven_b2_eval_1_1_4 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K) :
    sevenCoefficientAt t x 1 1 4 = (-180) * x 7 + (40 * t.b₂) * x 10 + (210 * t.c₂) * x 11 := by
  rw [sevenCoefficientAt_succ]
  norm_num only [coefficientBracket, coeffDq, coeffDP, coeffQ, coeffP, hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, sub_zero, zero_sub, false_and, and_false, true_and, and_true, if_true, if_false]
  simp only [seven_b2_eval_0_0_1 t hb h4 h5 x, seven_b2_eval_0_0_2 t hb h4 h5 x, seven_b2_eval_0_0_3 t hb h4 h5 x, seven_b2_eval_0_0_4 t hb h4 h5 x, seven_b2_eval_0_0_5 t hb h4 h5 x, seven_b2_eval_0_0_6 t hb h4 h5 x, seven_b2_eval_0_0_7 t hb h4 h5 x, seven_b2_eval_0_0_8 t hb h4 h5 x, seven_b2_eval_0_0_9 t hb h4 h5 x, seven_b2_eval_0_1_0 t hb h4 h5 x, seven_b2_eval_0_1_1 t hb h4 h5 x, seven_b2_eval_0_1_2 t hb h4 h5 x, seven_b2_eval_0_1_3 t hb h4 h5 x, seven_b2_eval_0_1_4 t hb h4 h5 x, seven_b2_eval_0_1_5 t hb h4 h5 x, seven_b2_eval_0_1_6 t hb h4 h5 x, seven_b2_eval_0_1_7 t hb h4 h5 x, seven_b2_eval_0_1_8 t hb h4 h5 x, seven_b2_eval_0_2_0 t hb h4 h5 x, seven_b2_eval_0_2_1 t hb h4 h5 x, seven_b2_eval_0_2_2 t hb h4 h5 x, seven_b2_eval_0_2_3 t hb h4 h5 x, seven_b2_eval_0_2_4 t hb h4 h5 x, seven_b2_eval_0_2_5 t hb h4 h5 x, seven_b2_eval_0_2_6 t hb h4 h5 x, seven_b2_eval_0_2_7 t hb h4 h5 x, seven_b2_eval_0_3_0 t hb h4 h5 x, seven_b2_eval_0_3_1 t hb h4 h5 x, seven_b2_eval_0_3_2 t hb h4 h5 x, seven_b2_eval_0_3_3 t hb h4 h5 x, seven_b2_eval_0_3_4 t hb h4 h5 x, seven_b2_eval_0_3_5 t hb h4 h5 x, seven_b2_eval_0_3_6 t hb h4 h5 x, seven_b2_eval_0_4_0 t hb h4 h5 x, seven_b2_eval_0_4_1 t hb h4 h5 x, seven_b2_eval_0_4_2 t hb h4 h5 x, seven_b2_eval_0_4_3 t hb h4 h5 x, seven_b2_eval_0_4_4 t hb h4 h5 x, seven_b2_eval_0_4_5 t hb h4 h5 x, seven_b2_eval_0_5_0 t hb h4 h5 x, seven_b2_eval_0_5_1 t hb h4 h5 x, seven_b2_eval_0_5_2 t hb h4 h5 x, seven_b2_eval_0_5_3 t hb h4 h5 x, seven_b2_eval_0_5_4 t hb h4 h5 x, seven_b2_eval_0_6_0 t hb h4 h5 x, seven_b2_eval_0_6_1 t hb h4 h5 x, seven_b2_eval_0_6_2 t hb h4 h5 x, seven_b2_eval_0_6_3 t hb h4 h5 x]
  all_goals ring

set_option maxHeartbeats 300000 in
lemma seven_b2_eval_1_1_5 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K) :
    sevenCoefficientAt t x 1 1 5 = (-420) * x 9 + (210 * t.b₂) * x 11 + (840 * t.c₂) * x 12 := by
  rw [sevenCoefficientAt_succ]
  norm_num only [coefficientBracket, coeffDq, coeffDP, coeffQ, coeffP, hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, sub_zero, zero_sub, false_and, and_false, true_and, and_true, if_true, if_false]
  simp only [seven_b2_eval_0_0_1 t hb h4 h5 x, seven_b2_eval_0_0_2 t hb h4 h5 x, seven_b2_eval_0_0_3 t hb h4 h5 x, seven_b2_eval_0_0_4 t hb h4 h5 x, seven_b2_eval_0_0_5 t hb h4 h5 x, seven_b2_eval_0_0_6 t hb h4 h5 x, seven_b2_eval_0_0_7 t hb h4 h5 x, seven_b2_eval_0_0_8 t hb h4 h5 x, seven_b2_eval_0_0_9 t hb h4 h5 x, seven_b2_eval_0_1_0 t hb h4 h5 x, seven_b2_eval_0_1_1 t hb h4 h5 x, seven_b2_eval_0_1_2 t hb h4 h5 x, seven_b2_eval_0_1_3 t hb h4 h5 x, seven_b2_eval_0_1_4 t hb h4 h5 x, seven_b2_eval_0_1_5 t hb h4 h5 x, seven_b2_eval_0_1_6 t hb h4 h5 x, seven_b2_eval_0_1_7 t hb h4 h5 x, seven_b2_eval_0_1_8 t hb h4 h5 x, seven_b2_eval_0_2_0 t hb h4 h5 x, seven_b2_eval_0_2_1 t hb h4 h5 x, seven_b2_eval_0_2_2 t hb h4 h5 x, seven_b2_eval_0_2_3 t hb h4 h5 x, seven_b2_eval_0_2_4 t hb h4 h5 x, seven_b2_eval_0_2_5 t hb h4 h5 x, seven_b2_eval_0_2_6 t hb h4 h5 x, seven_b2_eval_0_2_7 t hb h4 h5 x, seven_b2_eval_0_3_0 t hb h4 h5 x, seven_b2_eval_0_3_1 t hb h4 h5 x, seven_b2_eval_0_3_2 t hb h4 h5 x, seven_b2_eval_0_3_3 t hb h4 h5 x, seven_b2_eval_0_3_4 t hb h4 h5 x, seven_b2_eval_0_3_5 t hb h4 h5 x, seven_b2_eval_0_3_6 t hb h4 h5 x, seven_b2_eval_0_4_0 t hb h4 h5 x, seven_b2_eval_0_4_1 t hb h4 h5 x, seven_b2_eval_0_4_2 t hb h4 h5 x, seven_b2_eval_0_4_3 t hb h4 h5 x, seven_b2_eval_0_4_4 t hb h4 h5 x, seven_b2_eval_0_4_5 t hb h4 h5 x, seven_b2_eval_0_5_0 t hb h4 h5 x, seven_b2_eval_0_5_1 t hb h4 h5 x, seven_b2_eval_0_5_2 t hb h4 h5 x, seven_b2_eval_0_5_3 t hb h4 h5 x, seven_b2_eval_0_5_4 t hb h4 h5 x, seven_b2_eval_0_6_0 t hb h4 h5 x, seven_b2_eval_0_6_1 t hb h4 h5 x, seven_b2_eval_0_6_2 t hb h4 h5 x, seven_b2_eval_0_6_3 t hb h4 h5 x]
  all_goals ring

set_option maxHeartbeats 300000 in
lemma seven_b2_eval_1_1_6 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K) :
    sevenCoefficientAt t x 1 1 6 = (840 * t.b₂) * x 12 := by
  rw [sevenCoefficientAt_succ]
  norm_num only [coefficientBracket, coeffDq, coeffDP, coeffQ, coeffP, hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, sub_zero, zero_sub, false_and, and_false, true_and, and_true, if_true, if_false]
  simp only [seven_b2_eval_0_0_1 t hb h4 h5 x, seven_b2_eval_0_0_2 t hb h4 h5 x, seven_b2_eval_0_0_3 t hb h4 h5 x, seven_b2_eval_0_0_4 t hb h4 h5 x, seven_b2_eval_0_0_5 t hb h4 h5 x, seven_b2_eval_0_0_6 t hb h4 h5 x, seven_b2_eval_0_0_7 t hb h4 h5 x, seven_b2_eval_0_0_8 t hb h4 h5 x, seven_b2_eval_0_0_9 t hb h4 h5 x, seven_b2_eval_0_1_0 t hb h4 h5 x, seven_b2_eval_0_1_1 t hb h4 h5 x, seven_b2_eval_0_1_2 t hb h4 h5 x, seven_b2_eval_0_1_3 t hb h4 h5 x, seven_b2_eval_0_1_4 t hb h4 h5 x, seven_b2_eval_0_1_5 t hb h4 h5 x, seven_b2_eval_0_1_6 t hb h4 h5 x, seven_b2_eval_0_1_7 t hb h4 h5 x, seven_b2_eval_0_1_8 t hb h4 h5 x, seven_b2_eval_0_2_0 t hb h4 h5 x, seven_b2_eval_0_2_1 t hb h4 h5 x, seven_b2_eval_0_2_2 t hb h4 h5 x, seven_b2_eval_0_2_3 t hb h4 h5 x, seven_b2_eval_0_2_4 t hb h4 h5 x, seven_b2_eval_0_2_5 t hb h4 h5 x, seven_b2_eval_0_2_6 t hb h4 h5 x, seven_b2_eval_0_2_7 t hb h4 h5 x, seven_b2_eval_0_3_0 t hb h4 h5 x, seven_b2_eval_0_3_1 t hb h4 h5 x, seven_b2_eval_0_3_2 t hb h4 h5 x, seven_b2_eval_0_3_3 t hb h4 h5 x, seven_b2_eval_0_3_4 t hb h4 h5 x, seven_b2_eval_0_3_5 t hb h4 h5 x, seven_b2_eval_0_3_6 t hb h4 h5 x, seven_b2_eval_0_4_0 t hb h4 h5 x, seven_b2_eval_0_4_1 t hb h4 h5 x, seven_b2_eval_0_4_2 t hb h4 h5 x, seven_b2_eval_0_4_3 t hb h4 h5 x, seven_b2_eval_0_4_4 t hb h4 h5 x, seven_b2_eval_0_4_5 t hb h4 h5 x, seven_b2_eval_0_5_0 t hb h4 h5 x, seven_b2_eval_0_5_1 t hb h4 h5 x, seven_b2_eval_0_5_2 t hb h4 h5 x, seven_b2_eval_0_5_3 t hb h4 h5 x, seven_b2_eval_0_5_4 t hb h4 h5 x, seven_b2_eval_0_6_0 t hb h4 h5 x, seven_b2_eval_0_6_1 t hb h4 h5 x, seven_b2_eval_0_6_2 t hb h4 h5 x, seven_b2_eval_0_6_3 t hb h4 h5 x]
  all_goals ring

set_option maxHeartbeats 300000 in
lemma seven_b2_eval_1_1_7 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K) :
    sevenCoefficientAt t x 1 1 7 = 0 := by
  rw [sevenCoefficientAt_succ]
  norm_num only [coefficientBracket, coeffDq, coeffDP, coeffQ, coeffP, hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, sub_zero, zero_sub, false_and, and_false, true_and, and_true, if_true, if_false]
  simp only [seven_b2_eval_0_0_1 t hb h4 h5 x, seven_b2_eval_0_0_2 t hb h4 h5 x, seven_b2_eval_0_0_3 t hb h4 h5 x, seven_b2_eval_0_0_4 t hb h4 h5 x, seven_b2_eval_0_0_5 t hb h4 h5 x, seven_b2_eval_0_0_6 t hb h4 h5 x, seven_b2_eval_0_0_7 t hb h4 h5 x, seven_b2_eval_0_0_8 t hb h4 h5 x, seven_b2_eval_0_0_9 t hb h4 h5 x, seven_b2_eval_0_1_0 t hb h4 h5 x, seven_b2_eval_0_1_1 t hb h4 h5 x, seven_b2_eval_0_1_2 t hb h4 h5 x, seven_b2_eval_0_1_3 t hb h4 h5 x, seven_b2_eval_0_1_4 t hb h4 h5 x, seven_b2_eval_0_1_5 t hb h4 h5 x, seven_b2_eval_0_1_6 t hb h4 h5 x, seven_b2_eval_0_1_7 t hb h4 h5 x, seven_b2_eval_0_1_8 t hb h4 h5 x, seven_b2_eval_0_2_0 t hb h4 h5 x, seven_b2_eval_0_2_1 t hb h4 h5 x, seven_b2_eval_0_2_2 t hb h4 h5 x, seven_b2_eval_0_2_3 t hb h4 h5 x, seven_b2_eval_0_2_4 t hb h4 h5 x, seven_b2_eval_0_2_5 t hb h4 h5 x, seven_b2_eval_0_2_6 t hb h4 h5 x, seven_b2_eval_0_2_7 t hb h4 h5 x, seven_b2_eval_0_3_0 t hb h4 h5 x, seven_b2_eval_0_3_1 t hb h4 h5 x, seven_b2_eval_0_3_2 t hb h4 h5 x, seven_b2_eval_0_3_3 t hb h4 h5 x, seven_b2_eval_0_3_4 t hb h4 h5 x, seven_b2_eval_0_3_5 t hb h4 h5 x, seven_b2_eval_0_3_6 t hb h4 h5 x, seven_b2_eval_0_4_0 t hb h4 h5 x, seven_b2_eval_0_4_1 t hb h4 h5 x, seven_b2_eval_0_4_2 t hb h4 h5 x, seven_b2_eval_0_4_3 t hb h4 h5 x, seven_b2_eval_0_4_4 t hb h4 h5 x, seven_b2_eval_0_4_5 t hb h4 h5 x, seven_b2_eval_0_5_0 t hb h4 h5 x, seven_b2_eval_0_5_1 t hb h4 h5 x, seven_b2_eval_0_5_2 t hb h4 h5 x, seven_b2_eval_0_5_3 t hb h4 h5 x, seven_b2_eval_0_5_4 t hb h4 h5 x, seven_b2_eval_0_6_0 t hb h4 h5 x, seven_b2_eval_0_6_1 t hb h4 h5 x, seven_b2_eval_0_6_2 t hb h4 h5 x, seven_b2_eval_0_6_3 t hb h4 h5 x]
  all_goals ring

set_option maxHeartbeats 300000 in
lemma seven_b2_eval_1_2_0 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K) :
    sevenCoefficientAt t x 1 2 0 = ((-1) * t.b₂) * x 0 + ((-2) * t.b₁) * x 1 + (3 * t.c₃) * x 2 + ((2 * t.c₂) + (3 * t.b₀)) * x 3 + (2 * t.c₁) * x 4 + (15 * t.b₀ * t.b₂) * x 6 := by
  rw [sevenCoefficientAt_succ]
  norm_num only [coefficientBracket, coeffDq, coeffDP, coeffQ, coeffP, hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, sub_zero, zero_sub, false_and, and_false, true_and, and_true, if_true, if_false]
  simp only [seven_b2_eval_0_0_1 t hb h4 h5 x, seven_b2_eval_0_0_2 t hb h4 h5 x, seven_b2_eval_0_0_3 t hb h4 h5 x, seven_b2_eval_0_0_4 t hb h4 h5 x, seven_b2_eval_0_0_5 t hb h4 h5 x, seven_b2_eval_0_0_6 t hb h4 h5 x, seven_b2_eval_0_0_7 t hb h4 h5 x, seven_b2_eval_0_0_8 t hb h4 h5 x, seven_b2_eval_0_0_9 t hb h4 h5 x, seven_b2_eval_0_1_0 t hb h4 h5 x, seven_b2_eval_0_1_1 t hb h4 h5 x, seven_b2_eval_0_1_2 t hb h4 h5 x, seven_b2_eval_0_1_3 t hb h4 h5 x, seven_b2_eval_0_1_4 t hb h4 h5 x, seven_b2_eval_0_1_5 t hb h4 h5 x, seven_b2_eval_0_1_6 t hb h4 h5 x, seven_b2_eval_0_1_7 t hb h4 h5 x, seven_b2_eval_0_1_8 t hb h4 h5 x, seven_b2_eval_0_2_0 t hb h4 h5 x, seven_b2_eval_0_2_1 t hb h4 h5 x, seven_b2_eval_0_2_2 t hb h4 h5 x, seven_b2_eval_0_2_3 t hb h4 h5 x, seven_b2_eval_0_2_4 t hb h4 h5 x, seven_b2_eval_0_2_5 t hb h4 h5 x, seven_b2_eval_0_2_6 t hb h4 h5 x, seven_b2_eval_0_2_7 t hb h4 h5 x, seven_b2_eval_0_3_0 t hb h4 h5 x, seven_b2_eval_0_3_1 t hb h4 h5 x, seven_b2_eval_0_3_2 t hb h4 h5 x, seven_b2_eval_0_3_3 t hb h4 h5 x, seven_b2_eval_0_3_4 t hb h4 h5 x, seven_b2_eval_0_3_5 t hb h4 h5 x, seven_b2_eval_0_3_6 t hb h4 h5 x, seven_b2_eval_0_4_0 t hb h4 h5 x, seven_b2_eval_0_4_1 t hb h4 h5 x, seven_b2_eval_0_4_2 t hb h4 h5 x, seven_b2_eval_0_4_3 t hb h4 h5 x, seven_b2_eval_0_4_4 t hb h4 h5 x, seven_b2_eval_0_4_5 t hb h4 h5 x, seven_b2_eval_0_5_0 t hb h4 h5 x, seven_b2_eval_0_5_1 t hb h4 h5 x, seven_b2_eval_0_5_2 t hb h4 h5 x, seven_b2_eval_0_5_3 t hb h4 h5 x, seven_b2_eval_0_5_4 t hb h4 h5 x, seven_b2_eval_0_6_0 t hb h4 h5 x, seven_b2_eval_0_6_1 t hb h4 h5 x, seven_b2_eval_0_6_2 t hb h4 h5 x, seven_b2_eval_0_6_3 t hb h4 h5 x]
  all_goals ring

set_option maxHeartbeats 300000 in
lemma seven_b2_eval_1_2_1 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K) :
    sevenCoefficientAt t x 1 2 1 = t.b₂ * x 3 + ((-2) * t.b₁) * x 4 + (6 * t.c₃) * x 5 + ((60 * t.c₂) + (180 * t.b₀)) * x 6 + (60 * t.c₁) * x 7 + (420 * t.b₀ * t.b₂) * x 8 + (((-60) * t.b₀ * t.b₁) + ((-60) * t.b₀ * t.c₃)) * x 10 := by
  rw [sevenCoefficientAt_succ]
  norm_num only [coefficientBracket, coeffDq, coeffDP, coeffQ, coeffP, hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, sub_zero, zero_sub, false_and, and_false, true_and, and_true, if_true, if_false]
  simp only [seven_b2_eval_0_0_1 t hb h4 h5 x, seven_b2_eval_0_0_2 t hb h4 h5 x, seven_b2_eval_0_0_3 t hb h4 h5 x, seven_b2_eval_0_0_4 t hb h4 h5 x, seven_b2_eval_0_0_5 t hb h4 h5 x, seven_b2_eval_0_0_6 t hb h4 h5 x, seven_b2_eval_0_0_7 t hb h4 h5 x, seven_b2_eval_0_0_8 t hb h4 h5 x, seven_b2_eval_0_0_9 t hb h4 h5 x, seven_b2_eval_0_1_0 t hb h4 h5 x, seven_b2_eval_0_1_1 t hb h4 h5 x, seven_b2_eval_0_1_2 t hb h4 h5 x, seven_b2_eval_0_1_3 t hb h4 h5 x, seven_b2_eval_0_1_4 t hb h4 h5 x, seven_b2_eval_0_1_5 t hb h4 h5 x, seven_b2_eval_0_1_6 t hb h4 h5 x, seven_b2_eval_0_1_7 t hb h4 h5 x, seven_b2_eval_0_1_8 t hb h4 h5 x, seven_b2_eval_0_2_0 t hb h4 h5 x, seven_b2_eval_0_2_1 t hb h4 h5 x, seven_b2_eval_0_2_2 t hb h4 h5 x, seven_b2_eval_0_2_3 t hb h4 h5 x, seven_b2_eval_0_2_4 t hb h4 h5 x, seven_b2_eval_0_2_5 t hb h4 h5 x, seven_b2_eval_0_2_6 t hb h4 h5 x, seven_b2_eval_0_2_7 t hb h4 h5 x, seven_b2_eval_0_3_0 t hb h4 h5 x, seven_b2_eval_0_3_1 t hb h4 h5 x, seven_b2_eval_0_3_2 t hb h4 h5 x, seven_b2_eval_0_3_3 t hb h4 h5 x, seven_b2_eval_0_3_4 t hb h4 h5 x, seven_b2_eval_0_3_5 t hb h4 h5 x, seven_b2_eval_0_3_6 t hb h4 h5 x, seven_b2_eval_0_4_0 t hb h4 h5 x, seven_b2_eval_0_4_1 t hb h4 h5 x, seven_b2_eval_0_4_2 t hb h4 h5 x, seven_b2_eval_0_4_3 t hb h4 h5 x, seven_b2_eval_0_4_4 t hb h4 h5 x, seven_b2_eval_0_4_5 t hb h4 h5 x, seven_b2_eval_0_5_0 t hb h4 h5 x, seven_b2_eval_0_5_1 t hb h4 h5 x, seven_b2_eval_0_5_2 t hb h4 h5 x, seven_b2_eval_0_5_3 t hb h4 h5 x, seven_b2_eval_0_5_4 t hb h4 h5 x, seven_b2_eval_0_6_0 t hb h4 h5 x, seven_b2_eval_0_6_1 t hb h4 h5 x, seven_b2_eval_0_6_2 t hb h4 h5 x, seven_b2_eval_0_6_3 t hb h4 h5 x]
  all_goals ring

set_option maxHeartbeats 300000 in
lemma seven_b2_eval_1_2_2 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K) :
    sevenCoefficientAt t x 1 2 2 = 9 * x 3 + (90 * t.b₂) * x 6 + ((840 * t.c₂) + (3780 * t.b₀)) * x 8 + (210 * t.c₁) * x 9 + (((-630) * t.b₀ * t.b₁) + ((-630) * t.b₀ * t.c₃)) * x 11 := by
  rw [sevenCoefficientAt_succ]
  norm_num only [coefficientBracket, coeffDq, coeffDP, coeffQ, coeffP, hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, sub_zero, zero_sub, false_and, and_false, true_and, and_true, if_true, if_false]
  simp only [seven_b2_eval_0_0_1 t hb h4 h5 x, seven_b2_eval_0_0_2 t hb h4 h5 x, seven_b2_eval_0_0_3 t hb h4 h5 x, seven_b2_eval_0_0_4 t hb h4 h5 x, seven_b2_eval_0_0_5 t hb h4 h5 x, seven_b2_eval_0_0_6 t hb h4 h5 x, seven_b2_eval_0_0_7 t hb h4 h5 x, seven_b2_eval_0_0_8 t hb h4 h5 x, seven_b2_eval_0_0_9 t hb h4 h5 x, seven_b2_eval_0_1_0 t hb h4 h5 x, seven_b2_eval_0_1_1 t hb h4 h5 x, seven_b2_eval_0_1_2 t hb h4 h5 x, seven_b2_eval_0_1_3 t hb h4 h5 x, seven_b2_eval_0_1_4 t hb h4 h5 x, seven_b2_eval_0_1_5 t hb h4 h5 x, seven_b2_eval_0_1_6 t hb h4 h5 x, seven_b2_eval_0_1_7 t hb h4 h5 x, seven_b2_eval_0_1_8 t hb h4 h5 x, seven_b2_eval_0_2_0 t hb h4 h5 x, seven_b2_eval_0_2_1 t hb h4 h5 x, seven_b2_eval_0_2_2 t hb h4 h5 x, seven_b2_eval_0_2_3 t hb h4 h5 x, seven_b2_eval_0_2_4 t hb h4 h5 x, seven_b2_eval_0_2_5 t hb h4 h5 x, seven_b2_eval_0_2_6 t hb h4 h5 x, seven_b2_eval_0_2_7 t hb h4 h5 x, seven_b2_eval_0_3_0 t hb h4 h5 x, seven_b2_eval_0_3_1 t hb h4 h5 x, seven_b2_eval_0_3_2 t hb h4 h5 x, seven_b2_eval_0_3_3 t hb h4 h5 x, seven_b2_eval_0_3_4 t hb h4 h5 x, seven_b2_eval_0_3_5 t hb h4 h5 x, seven_b2_eval_0_3_6 t hb h4 h5 x, seven_b2_eval_0_4_0 t hb h4 h5 x, seven_b2_eval_0_4_1 t hb h4 h5 x, seven_b2_eval_0_4_2 t hb h4 h5 x, seven_b2_eval_0_4_3 t hb h4 h5 x, seven_b2_eval_0_4_4 t hb h4 h5 x, seven_b2_eval_0_4_5 t hb h4 h5 x, seven_b2_eval_0_5_0 t hb h4 h5 x, seven_b2_eval_0_5_1 t hb h4 h5 x, seven_b2_eval_0_5_2 t hb h4 h5 x, seven_b2_eval_0_5_3 t hb h4 h5 x, seven_b2_eval_0_5_4 t hb h4 h5 x, seven_b2_eval_0_6_0 t hb h4 h5 x, seven_b2_eval_0_6_1 t hb h4 h5 x, seven_b2_eval_0_6_2 t hb h4 h5 x, seven_b2_eval_0_6_3 t hb h4 h5 x]
  all_goals ring

set_option maxHeartbeats 300000 in
lemma seven_b2_eval_1_2_3 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K) :
    sevenCoefficientAt t x 1 2 3 = 540 * x 6 + (1960 * t.b₂) * x 8 + (70 * t.b₁) * x 9 + (((-180) * t.b₁) + ((-120) * t.c₃)) * x 10 + (((-4200) * t.b₀ * t.b₁) + ((-4200) * t.b₀ * t.c₃)) * x 12 := by
  rw [sevenCoefficientAt_succ]
  norm_num only [coefficientBracket, coeffDq, coeffDP, coeffQ, coeffP, hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, sub_zero, zero_sub, false_and, and_false, true_and, and_true, if_true, if_false]
  simp only [seven_b2_eval_0_0_1 t hb h4 h5 x, seven_b2_eval_0_0_2 t hb h4 h5 x, seven_b2_eval_0_0_3 t hb h4 h5 x, seven_b2_eval_0_0_4 t hb h4 h5 x, seven_b2_eval_0_0_5 t hb h4 h5 x, seven_b2_eval_0_0_6 t hb h4 h5 x, seven_b2_eval_0_0_7 t hb h4 h5 x, seven_b2_eval_0_0_8 t hb h4 h5 x, seven_b2_eval_0_0_9 t hb h4 h5 x, seven_b2_eval_0_1_0 t hb h4 h5 x, seven_b2_eval_0_1_1 t hb h4 h5 x, seven_b2_eval_0_1_2 t hb h4 h5 x, seven_b2_eval_0_1_3 t hb h4 h5 x, seven_b2_eval_0_1_4 t hb h4 h5 x, seven_b2_eval_0_1_5 t hb h4 h5 x, seven_b2_eval_0_1_6 t hb h4 h5 x, seven_b2_eval_0_1_7 t hb h4 h5 x, seven_b2_eval_0_1_8 t hb h4 h5 x, seven_b2_eval_0_2_0 t hb h4 h5 x, seven_b2_eval_0_2_1 t hb h4 h5 x, seven_b2_eval_0_2_2 t hb h4 h5 x, seven_b2_eval_0_2_3 t hb h4 h5 x, seven_b2_eval_0_2_4 t hb h4 h5 x, seven_b2_eval_0_2_5 t hb h4 h5 x, seven_b2_eval_0_2_6 t hb h4 h5 x, seven_b2_eval_0_2_7 t hb h4 h5 x, seven_b2_eval_0_3_0 t hb h4 h5 x, seven_b2_eval_0_3_1 t hb h4 h5 x, seven_b2_eval_0_3_2 t hb h4 h5 x, seven_b2_eval_0_3_3 t hb h4 h5 x, seven_b2_eval_0_3_4 t hb h4 h5 x, seven_b2_eval_0_3_5 t hb h4 h5 x, seven_b2_eval_0_3_6 t hb h4 h5 x, seven_b2_eval_0_4_0 t hb h4 h5 x, seven_b2_eval_0_4_1 t hb h4 h5 x, seven_b2_eval_0_4_2 t hb h4 h5 x, seven_b2_eval_0_4_3 t hb h4 h5 x, seven_b2_eval_0_4_4 t hb h4 h5 x, seven_b2_eval_0_4_5 t hb h4 h5 x, seven_b2_eval_0_5_0 t hb h4 h5 x, seven_b2_eval_0_5_1 t hb h4 h5 x, seven_b2_eval_0_5_2 t hb h4 h5 x, seven_b2_eval_0_5_3 t hb h4 h5 x, seven_b2_eval_0_5_4 t hb h4 h5 x, seven_b2_eval_0_6_0 t hb h4 h5 x, seven_b2_eval_0_6_1 t hb h4 h5 x, seven_b2_eval_0_6_2 t hb h4 h5 x, seven_b2_eval_0_6_3 t hb h4 h5 x]
  all_goals ring

set_option maxHeartbeats 300000 in
lemma seven_b2_eval_1_2_4 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K) :
    sevenCoefficientAt t x 1 2 4 = 11340 * x 8 + (((-1890) * t.b₁) + ((-1575) * t.c₃)) * x 11 := by
  rw [sevenCoefficientAt_succ]
  norm_num only [coefficientBracket, coeffDq, coeffDP, coeffQ, coeffP, hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, sub_zero, zero_sub, false_and, and_false, true_and, and_true, if_true, if_false]
  simp only [seven_b2_eval_0_0_1 t hb h4 h5 x, seven_b2_eval_0_0_2 t hb h4 h5 x, seven_b2_eval_0_0_3 t hb h4 h5 x, seven_b2_eval_0_0_4 t hb h4 h5 x, seven_b2_eval_0_0_5 t hb h4 h5 x, seven_b2_eval_0_0_6 t hb h4 h5 x, seven_b2_eval_0_0_7 t hb h4 h5 x, seven_b2_eval_0_0_8 t hb h4 h5 x, seven_b2_eval_0_0_9 t hb h4 h5 x, seven_b2_eval_0_1_0 t hb h4 h5 x, seven_b2_eval_0_1_1 t hb h4 h5 x, seven_b2_eval_0_1_2 t hb h4 h5 x, seven_b2_eval_0_1_3 t hb h4 h5 x, seven_b2_eval_0_1_4 t hb h4 h5 x, seven_b2_eval_0_1_5 t hb h4 h5 x, seven_b2_eval_0_1_6 t hb h4 h5 x, seven_b2_eval_0_1_7 t hb h4 h5 x, seven_b2_eval_0_1_8 t hb h4 h5 x, seven_b2_eval_0_2_0 t hb h4 h5 x, seven_b2_eval_0_2_1 t hb h4 h5 x, seven_b2_eval_0_2_2 t hb h4 h5 x, seven_b2_eval_0_2_3 t hb h4 h5 x, seven_b2_eval_0_2_4 t hb h4 h5 x, seven_b2_eval_0_2_5 t hb h4 h5 x, seven_b2_eval_0_2_6 t hb h4 h5 x, seven_b2_eval_0_2_7 t hb h4 h5 x, seven_b2_eval_0_3_0 t hb h4 h5 x, seven_b2_eval_0_3_1 t hb h4 h5 x, seven_b2_eval_0_3_2 t hb h4 h5 x, seven_b2_eval_0_3_3 t hb h4 h5 x, seven_b2_eval_0_3_4 t hb h4 h5 x, seven_b2_eval_0_3_5 t hb h4 h5 x, seven_b2_eval_0_3_6 t hb h4 h5 x, seven_b2_eval_0_4_0 t hb h4 h5 x, seven_b2_eval_0_4_1 t hb h4 h5 x, seven_b2_eval_0_4_2 t hb h4 h5 x, seven_b2_eval_0_4_3 t hb h4 h5 x, seven_b2_eval_0_4_4 t hb h4 h5 x, seven_b2_eval_0_4_5 t hb h4 h5 x, seven_b2_eval_0_5_0 t hb h4 h5 x, seven_b2_eval_0_5_1 t hb h4 h5 x, seven_b2_eval_0_5_2 t hb h4 h5 x, seven_b2_eval_0_5_3 t hb h4 h5 x, seven_b2_eval_0_5_4 t hb h4 h5 x, seven_b2_eval_0_6_0 t hb h4 h5 x, seven_b2_eval_0_6_1 t hb h4 h5 x, seven_b2_eval_0_6_2 t hb h4 h5 x, seven_b2_eval_0_6_3 t hb h4 h5 x]
  all_goals ring

set_option maxHeartbeats 300000 in
lemma seven_b2_eval_1_2_5 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K) :
    sevenCoefficientAt t x 1 2 5 = (((-12600) * t.b₁) + ((-11340) * t.c₃)) * x 12 := by
  rw [sevenCoefficientAt_succ]
  norm_num only [coefficientBracket, coeffDq, coeffDP, coeffQ, coeffP, hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, sub_zero, zero_sub, false_and, and_false, true_and, and_true, if_true, if_false]
  simp only [seven_b2_eval_0_0_1 t hb h4 h5 x, seven_b2_eval_0_0_2 t hb h4 h5 x, seven_b2_eval_0_0_3 t hb h4 h5 x, seven_b2_eval_0_0_4 t hb h4 h5 x, seven_b2_eval_0_0_5 t hb h4 h5 x, seven_b2_eval_0_0_6 t hb h4 h5 x, seven_b2_eval_0_0_7 t hb h4 h5 x, seven_b2_eval_0_0_8 t hb h4 h5 x, seven_b2_eval_0_0_9 t hb h4 h5 x, seven_b2_eval_0_1_0 t hb h4 h5 x, seven_b2_eval_0_1_1 t hb h4 h5 x, seven_b2_eval_0_1_2 t hb h4 h5 x, seven_b2_eval_0_1_3 t hb h4 h5 x, seven_b2_eval_0_1_4 t hb h4 h5 x, seven_b2_eval_0_1_5 t hb h4 h5 x, seven_b2_eval_0_1_6 t hb h4 h5 x, seven_b2_eval_0_1_7 t hb h4 h5 x, seven_b2_eval_0_1_8 t hb h4 h5 x, seven_b2_eval_0_2_0 t hb h4 h5 x, seven_b2_eval_0_2_1 t hb h4 h5 x, seven_b2_eval_0_2_2 t hb h4 h5 x, seven_b2_eval_0_2_3 t hb h4 h5 x, seven_b2_eval_0_2_4 t hb h4 h5 x, seven_b2_eval_0_2_5 t hb h4 h5 x, seven_b2_eval_0_2_6 t hb h4 h5 x, seven_b2_eval_0_2_7 t hb h4 h5 x, seven_b2_eval_0_3_0 t hb h4 h5 x, seven_b2_eval_0_3_1 t hb h4 h5 x, seven_b2_eval_0_3_2 t hb h4 h5 x, seven_b2_eval_0_3_3 t hb h4 h5 x, seven_b2_eval_0_3_4 t hb h4 h5 x, seven_b2_eval_0_3_5 t hb h4 h5 x, seven_b2_eval_0_3_6 t hb h4 h5 x, seven_b2_eval_0_4_0 t hb h4 h5 x, seven_b2_eval_0_4_1 t hb h4 h5 x, seven_b2_eval_0_4_2 t hb h4 h5 x, seven_b2_eval_0_4_3 t hb h4 h5 x, seven_b2_eval_0_4_4 t hb h4 h5 x, seven_b2_eval_0_4_5 t hb h4 h5 x, seven_b2_eval_0_5_0 t hb h4 h5 x, seven_b2_eval_0_5_1 t hb h4 h5 x, seven_b2_eval_0_5_2 t hb h4 h5 x, seven_b2_eval_0_5_3 t hb h4 h5 x, seven_b2_eval_0_5_4 t hb h4 h5 x, seven_b2_eval_0_6_0 t hb h4 h5 x, seven_b2_eval_0_6_1 t hb h4 h5 x, seven_b2_eval_0_6_2 t hb h4 h5 x, seven_b2_eval_0_6_3 t hb h4 h5 x]
  all_goals ring

set_option maxHeartbeats 300000 in
lemma seven_b2_eval_1_2_6 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K) :
    sevenCoefficientAt t x 1 2 6 = 0 := by
  rw [sevenCoefficientAt_succ]
  norm_num only [coefficientBracket, coeffDq, coeffDP, coeffQ, coeffP, hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, sub_zero, zero_sub, false_and, and_false, true_and, and_true, if_true, if_false]
  simp only [seven_b2_eval_0_0_1 t hb h4 h5 x, seven_b2_eval_0_0_2 t hb h4 h5 x, seven_b2_eval_0_0_3 t hb h4 h5 x, seven_b2_eval_0_0_4 t hb h4 h5 x, seven_b2_eval_0_0_5 t hb h4 h5 x, seven_b2_eval_0_0_6 t hb h4 h5 x, seven_b2_eval_0_0_7 t hb h4 h5 x, seven_b2_eval_0_0_8 t hb h4 h5 x, seven_b2_eval_0_0_9 t hb h4 h5 x, seven_b2_eval_0_1_0 t hb h4 h5 x, seven_b2_eval_0_1_1 t hb h4 h5 x, seven_b2_eval_0_1_2 t hb h4 h5 x, seven_b2_eval_0_1_3 t hb h4 h5 x, seven_b2_eval_0_1_4 t hb h4 h5 x, seven_b2_eval_0_1_5 t hb h4 h5 x, seven_b2_eval_0_1_6 t hb h4 h5 x, seven_b2_eval_0_1_7 t hb h4 h5 x, seven_b2_eval_0_1_8 t hb h4 h5 x, seven_b2_eval_0_2_0 t hb h4 h5 x, seven_b2_eval_0_2_1 t hb h4 h5 x, seven_b2_eval_0_2_2 t hb h4 h5 x, seven_b2_eval_0_2_3 t hb h4 h5 x, seven_b2_eval_0_2_4 t hb h4 h5 x, seven_b2_eval_0_2_5 t hb h4 h5 x, seven_b2_eval_0_2_6 t hb h4 h5 x, seven_b2_eval_0_2_7 t hb h4 h5 x, seven_b2_eval_0_3_0 t hb h4 h5 x, seven_b2_eval_0_3_1 t hb h4 h5 x, seven_b2_eval_0_3_2 t hb h4 h5 x, seven_b2_eval_0_3_3 t hb h4 h5 x, seven_b2_eval_0_3_4 t hb h4 h5 x, seven_b2_eval_0_3_5 t hb h4 h5 x, seven_b2_eval_0_3_6 t hb h4 h5 x, seven_b2_eval_0_4_0 t hb h4 h5 x, seven_b2_eval_0_4_1 t hb h4 h5 x, seven_b2_eval_0_4_2 t hb h4 h5 x, seven_b2_eval_0_4_3 t hb h4 h5 x, seven_b2_eval_0_4_4 t hb h4 h5 x, seven_b2_eval_0_4_5 t hb h4 h5 x, seven_b2_eval_0_5_0 t hb h4 h5 x, seven_b2_eval_0_5_1 t hb h4 h5 x, seven_b2_eval_0_5_2 t hb h4 h5 x, seven_b2_eval_0_5_3 t hb h4 h5 x, seven_b2_eval_0_5_4 t hb h4 h5 x, seven_b2_eval_0_6_0 t hb h4 h5 x, seven_b2_eval_0_6_1 t hb h4 h5 x, seven_b2_eval_0_6_2 t hb h4 h5 x, seven_b2_eval_0_6_3 t hb h4 h5 x]
  all_goals ring

set_option maxHeartbeats 300000 in
lemma seven_b2_eval_1_3_0 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K) :
    sevenCoefficientAt t x 1 3 0 = ((-2) * t.b₂) * x 1 + ((3 * t.b₁) + (3 * t.c₃)) * x 3 + ((4 * t.b₀) + (4 * t.c₂)) * x 4 + (((-60) * t.c₁) + (15 * t.b₁ * t.b₂)) * x 6 + (20 * t.b₀ * t.b₂) * x 7 + (((-140) * t.b₀ * t.b₁) + ((-140) * t.b₀ * t.c₃) + ((-140) * t.b₂ * t.c₁)) * x 8 + ((20 * t.b₁ * t.c₁) + (20 * t.c₁ * t.c₃)) * x 10 := by
  rw [sevenCoefficientAt_succ]
  norm_num only [coefficientBracket, coeffDq, coeffDP, coeffQ, coeffP, hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, sub_zero, zero_sub, false_and, and_false, true_and, and_true, if_true, if_false]
  simp only [seven_b2_eval_0_0_1 t hb h4 h5 x, seven_b2_eval_0_0_2 t hb h4 h5 x, seven_b2_eval_0_0_3 t hb h4 h5 x, seven_b2_eval_0_0_4 t hb h4 h5 x, seven_b2_eval_0_0_5 t hb h4 h5 x, seven_b2_eval_0_0_6 t hb h4 h5 x, seven_b2_eval_0_0_7 t hb h4 h5 x, seven_b2_eval_0_0_8 t hb h4 h5 x, seven_b2_eval_0_0_9 t hb h4 h5 x, seven_b2_eval_0_1_0 t hb h4 h5 x, seven_b2_eval_0_1_1 t hb h4 h5 x, seven_b2_eval_0_1_2 t hb h4 h5 x, seven_b2_eval_0_1_3 t hb h4 h5 x, seven_b2_eval_0_1_4 t hb h4 h5 x, seven_b2_eval_0_1_5 t hb h4 h5 x, seven_b2_eval_0_1_6 t hb h4 h5 x, seven_b2_eval_0_1_7 t hb h4 h5 x, seven_b2_eval_0_1_8 t hb h4 h5 x, seven_b2_eval_0_2_0 t hb h4 h5 x, seven_b2_eval_0_2_1 t hb h4 h5 x, seven_b2_eval_0_2_2 t hb h4 h5 x, seven_b2_eval_0_2_3 t hb h4 h5 x, seven_b2_eval_0_2_4 t hb h4 h5 x, seven_b2_eval_0_2_5 t hb h4 h5 x, seven_b2_eval_0_2_6 t hb h4 h5 x, seven_b2_eval_0_2_7 t hb h4 h5 x, seven_b2_eval_0_3_0 t hb h4 h5 x, seven_b2_eval_0_3_1 t hb h4 h5 x, seven_b2_eval_0_3_2 t hb h4 h5 x, seven_b2_eval_0_3_3 t hb h4 h5 x, seven_b2_eval_0_3_4 t hb h4 h5 x, seven_b2_eval_0_3_5 t hb h4 h5 x, seven_b2_eval_0_3_6 t hb h4 h5 x, seven_b2_eval_0_4_0 t hb h4 h5 x, seven_b2_eval_0_4_1 t hb h4 h5 x, seven_b2_eval_0_4_2 t hb h4 h5 x, seven_b2_eval_0_4_3 t hb h4 h5 x, seven_b2_eval_0_4_4 t hb h4 h5 x, seven_b2_eval_0_4_5 t hb h4 h5 x, seven_b2_eval_0_5_0 t hb h4 h5 x, seven_b2_eval_0_5_1 t hb h4 h5 x, seven_b2_eval_0_5_2 t hb h4 h5 x, seven_b2_eval_0_5_3 t hb h4 h5 x, seven_b2_eval_0_5_4 t hb h4 h5 x, seven_b2_eval_0_6_0 t hb h4 h5 x, seven_b2_eval_0_6_1 t hb h4 h5 x, seven_b2_eval_0_6_2 t hb h4 h5 x, seven_b2_eval_0_6_3 t hb h4 h5 x]
  all_goals ring

set_option maxHeartbeats 300000 in
lemma seven_b2_eval_1_3_1 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K) :
    sevenCoefficientAt t x 1 3 1 = ((90 * t.c₃) + (120 * t.b₁)) * x 6 + ((120 * t.c₂) + (240 * t.b₀)) * x 7 + (((-2520) * t.c₁) + (280 * t.b₁ * t.b₂)) * x 8 + (140 * t.b₀ * t.b₂) * x 9 + (((-40) * (t.b₁ ^ 2)) + ((-40) * t.b₀ * t.b₂) + ((-40) * t.b₁ * t.c₃)) * x 10 + ((420 * t.b₁ * t.c₁) + (420 * t.c₁ * t.c₃)) * x 11 := by
  rw [sevenCoefficientAt_succ]
  norm_num only [coefficientBracket, coeffDq, coeffDP, coeffQ, coeffP, hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, sub_zero, zero_sub, false_and, and_false, true_and, and_true, if_true, if_false]
  simp only [seven_b2_eval_0_0_1 t hb h4 h5 x, seven_b2_eval_0_0_2 t hb h4 h5 x, seven_b2_eval_0_0_3 t hb h4 h5 x, seven_b2_eval_0_0_4 t hb h4 h5 x, seven_b2_eval_0_0_5 t hb h4 h5 x, seven_b2_eval_0_0_6 t hb h4 h5 x, seven_b2_eval_0_0_7 t hb h4 h5 x, seven_b2_eval_0_0_8 t hb h4 h5 x, seven_b2_eval_0_0_9 t hb h4 h5 x, seven_b2_eval_0_1_0 t hb h4 h5 x, seven_b2_eval_0_1_1 t hb h4 h5 x, seven_b2_eval_0_1_2 t hb h4 h5 x, seven_b2_eval_0_1_3 t hb h4 h5 x, seven_b2_eval_0_1_4 t hb h4 h5 x, seven_b2_eval_0_1_5 t hb h4 h5 x, seven_b2_eval_0_1_6 t hb h4 h5 x, seven_b2_eval_0_1_7 t hb h4 h5 x, seven_b2_eval_0_1_8 t hb h4 h5 x, seven_b2_eval_0_2_0 t hb h4 h5 x, seven_b2_eval_0_2_1 t hb h4 h5 x, seven_b2_eval_0_2_2 t hb h4 h5 x, seven_b2_eval_0_2_3 t hb h4 h5 x, seven_b2_eval_0_2_4 t hb h4 h5 x, seven_b2_eval_0_2_5 t hb h4 h5 x, seven_b2_eval_0_2_6 t hb h4 h5 x, seven_b2_eval_0_2_7 t hb h4 h5 x, seven_b2_eval_0_3_0 t hb h4 h5 x, seven_b2_eval_0_3_1 t hb h4 h5 x, seven_b2_eval_0_3_2 t hb h4 h5 x, seven_b2_eval_0_3_3 t hb h4 h5 x, seven_b2_eval_0_3_4 t hb h4 h5 x, seven_b2_eval_0_3_5 t hb h4 h5 x, seven_b2_eval_0_3_6 t hb h4 h5 x, seven_b2_eval_0_4_0 t hb h4 h5 x, seven_b2_eval_0_4_1 t hb h4 h5 x, seven_b2_eval_0_4_2 t hb h4 h5 x, seven_b2_eval_0_4_3 t hb h4 h5 x, seven_b2_eval_0_4_4 t hb h4 h5 x, seven_b2_eval_0_4_5 t hb h4 h5 x, seven_b2_eval_0_5_0 t hb h4 h5 x, seven_b2_eval_0_5_1 t hb h4 h5 x, seven_b2_eval_0_5_2 t hb h4 h5 x, seven_b2_eval_0_5_3 t hb h4 h5 x, seven_b2_eval_0_5_4 t hb h4 h5 x, seven_b2_eval_0_6_0 t hb h4 h5 x, seven_b2_eval_0_6_1 t hb h4 h5 x, seven_b2_eval_0_6_2 t hb h4 h5 x, seven_b2_eval_0_6_3 t hb h4 h5 x]
  all_goals ring

set_option maxHeartbeats 300000 in
lemma seven_b2_eval_1_3_2 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K) :
    sevenCoefficientAt t x 1 3 2 = 12 * x 4 + (120 * t.b₂) * x 7 + ((840 * t.b₁) + (840 * t.c₃)) * x 8 + ((420 * t.c₂) + (1260 * t.b₀)) * x 9 + (((-210) * (t.b₁ ^ 2)) + ((-420) * t.b₀ * t.b₂) + ((-210) * t.b₁ * t.c₃)) * x 11 + ((4200 * t.b₁ * t.c₁) + (4200 * t.c₁ * t.c₃)) * x 12 := by
  rw [sevenCoefficientAt_succ]
  norm_num only [coefficientBracket, coeffDq, coeffDP, coeffQ, coeffP, hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, sub_zero, zero_sub, false_and, and_false, true_and, and_true, if_true, if_false]
  simp only [seven_b2_eval_0_0_1 t hb h4 h5 x, seven_b2_eval_0_0_2 t hb h4 h5 x, seven_b2_eval_0_0_3 t hb h4 h5 x, seven_b2_eval_0_0_4 t hb h4 h5 x, seven_b2_eval_0_0_5 t hb h4 h5 x, seven_b2_eval_0_0_6 t hb h4 h5 x, seven_b2_eval_0_0_7 t hb h4 h5 x, seven_b2_eval_0_0_8 t hb h4 h5 x, seven_b2_eval_0_0_9 t hb h4 h5 x, seven_b2_eval_0_1_0 t hb h4 h5 x, seven_b2_eval_0_1_1 t hb h4 h5 x, seven_b2_eval_0_1_2 t hb h4 h5 x, seven_b2_eval_0_1_3 t hb h4 h5 x, seven_b2_eval_0_1_4 t hb h4 h5 x, seven_b2_eval_0_1_5 t hb h4 h5 x, seven_b2_eval_0_1_6 t hb h4 h5 x, seven_b2_eval_0_1_7 t hb h4 h5 x, seven_b2_eval_0_1_8 t hb h4 h5 x, seven_b2_eval_0_2_0 t hb h4 h5 x, seven_b2_eval_0_2_1 t hb h4 h5 x, seven_b2_eval_0_2_2 t hb h4 h5 x, seven_b2_eval_0_2_3 t hb h4 h5 x, seven_b2_eval_0_2_4 t hb h4 h5 x, seven_b2_eval_0_2_5 t hb h4 h5 x, seven_b2_eval_0_2_6 t hb h4 h5 x, seven_b2_eval_0_2_7 t hb h4 h5 x, seven_b2_eval_0_3_0 t hb h4 h5 x, seven_b2_eval_0_3_1 t hb h4 h5 x, seven_b2_eval_0_3_2 t hb h4 h5 x, seven_b2_eval_0_3_3 t hb h4 h5 x, seven_b2_eval_0_3_4 t hb h4 h5 x, seven_b2_eval_0_3_5 t hb h4 h5 x, seven_b2_eval_0_3_6 t hb h4 h5 x, seven_b2_eval_0_4_0 t hb h4 h5 x, seven_b2_eval_0_4_1 t hb h4 h5 x, seven_b2_eval_0_4_2 t hb h4 h5 x, seven_b2_eval_0_4_3 t hb h4 h5 x, seven_b2_eval_0_4_4 t hb h4 h5 x, seven_b2_eval_0_4_5 t hb h4 h5 x, seven_b2_eval_0_5_0 t hb h4 h5 x, seven_b2_eval_0_5_1 t hb h4 h5 x, seven_b2_eval_0_5_2 t hb h4 h5 x, seven_b2_eval_0_5_3 t hb h4 h5 x, seven_b2_eval_0_5_4 t hb h4 h5 x, seven_b2_eval_0_6_0 t hb h4 h5 x, seven_b2_eval_0_6_1 t hb h4 h5 x, seven_b2_eval_0_6_2 t hb h4 h5 x, seven_b2_eval_0_6_3 t hb h4 h5 x]
  all_goals ring

set_option maxHeartbeats 300000 in
lemma seven_b2_eval_1_3_3 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K) :
    sevenCoefficientAt t x 1 3 3 = 720 * x 7 + (700 * t.b₂) * x 9 + ((-120) * t.b₂) * x 10 + ((-2800) * t.b₀ * t.b₂) * x 12 := by
  rw [sevenCoefficientAt_succ]
  norm_num only [coefficientBracket, coeffDq, coeffDP, coeffQ, coeffP, hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, sub_zero, zero_sub, false_and, and_false, true_and, and_true, if_true, if_false]
  simp only [seven_b2_eval_0_0_1 t hb h4 h5 x, seven_b2_eval_0_0_2 t hb h4 h5 x, seven_b2_eval_0_0_3 t hb h4 h5 x, seven_b2_eval_0_0_4 t hb h4 h5 x, seven_b2_eval_0_0_5 t hb h4 h5 x, seven_b2_eval_0_0_6 t hb h4 h5 x, seven_b2_eval_0_0_7 t hb h4 h5 x, seven_b2_eval_0_0_8 t hb h4 h5 x, seven_b2_eval_0_0_9 t hb h4 h5 x, seven_b2_eval_0_1_0 t hb h4 h5 x, seven_b2_eval_0_1_1 t hb h4 h5 x, seven_b2_eval_0_1_2 t hb h4 h5 x, seven_b2_eval_0_1_3 t hb h4 h5 x, seven_b2_eval_0_1_4 t hb h4 h5 x, seven_b2_eval_0_1_5 t hb h4 h5 x, seven_b2_eval_0_1_6 t hb h4 h5 x, seven_b2_eval_0_1_7 t hb h4 h5 x, seven_b2_eval_0_1_8 t hb h4 h5 x, seven_b2_eval_0_2_0 t hb h4 h5 x, seven_b2_eval_0_2_1 t hb h4 h5 x, seven_b2_eval_0_2_2 t hb h4 h5 x, seven_b2_eval_0_2_3 t hb h4 h5 x, seven_b2_eval_0_2_4 t hb h4 h5 x, seven_b2_eval_0_2_5 t hb h4 h5 x, seven_b2_eval_0_2_6 t hb h4 h5 x, seven_b2_eval_0_2_7 t hb h4 h5 x, seven_b2_eval_0_3_0 t hb h4 h5 x, seven_b2_eval_0_3_1 t hb h4 h5 x, seven_b2_eval_0_3_2 t hb h4 h5 x, seven_b2_eval_0_3_3 t hb h4 h5 x, seven_b2_eval_0_3_4 t hb h4 h5 x, seven_b2_eval_0_3_5 t hb h4 h5 x, seven_b2_eval_0_3_6 t hb h4 h5 x, seven_b2_eval_0_4_0 t hb h4 h5 x, seven_b2_eval_0_4_1 t hb h4 h5 x, seven_b2_eval_0_4_2 t hb h4 h5 x, seven_b2_eval_0_4_3 t hb h4 h5 x, seven_b2_eval_0_4_4 t hb h4 h5 x, seven_b2_eval_0_4_5 t hb h4 h5 x, seven_b2_eval_0_5_0 t hb h4 h5 x, seven_b2_eval_0_5_1 t hb h4 h5 x, seven_b2_eval_0_5_2 t hb h4 h5 x, seven_b2_eval_0_5_3 t hb h4 h5 x, seven_b2_eval_0_5_4 t hb h4 h5 x, seven_b2_eval_0_6_0 t hb h4 h5 x, seven_b2_eval_0_6_1 t hb h4 h5 x, seven_b2_eval_0_6_2 t hb h4 h5 x, seven_b2_eval_0_6_3 t hb h4 h5 x]
  all_goals ring

set_option maxHeartbeats 300000 in
lemma seven_b2_eval_1_3_4 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K) :
    sevenCoefficientAt t x 1 3 4 = 3780 * x 9 + ((-1260) * t.b₂) * x 11 := by
  rw [sevenCoefficientAt_succ]
  norm_num only [coefficientBracket, coeffDq, coeffDP, coeffQ, coeffP, hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, sub_zero, zero_sub, false_and, and_false, true_and, and_true, if_true, if_false]
  simp only [seven_b2_eval_0_0_1 t hb h4 h5 x, seven_b2_eval_0_0_2 t hb h4 h5 x, seven_b2_eval_0_0_3 t hb h4 h5 x, seven_b2_eval_0_0_4 t hb h4 h5 x, seven_b2_eval_0_0_5 t hb h4 h5 x, seven_b2_eval_0_0_6 t hb h4 h5 x, seven_b2_eval_0_0_7 t hb h4 h5 x, seven_b2_eval_0_0_8 t hb h4 h5 x, seven_b2_eval_0_0_9 t hb h4 h5 x, seven_b2_eval_0_1_0 t hb h4 h5 x, seven_b2_eval_0_1_1 t hb h4 h5 x, seven_b2_eval_0_1_2 t hb h4 h5 x, seven_b2_eval_0_1_3 t hb h4 h5 x, seven_b2_eval_0_1_4 t hb h4 h5 x, seven_b2_eval_0_1_5 t hb h4 h5 x, seven_b2_eval_0_1_6 t hb h4 h5 x, seven_b2_eval_0_1_7 t hb h4 h5 x, seven_b2_eval_0_1_8 t hb h4 h5 x, seven_b2_eval_0_2_0 t hb h4 h5 x, seven_b2_eval_0_2_1 t hb h4 h5 x, seven_b2_eval_0_2_2 t hb h4 h5 x, seven_b2_eval_0_2_3 t hb h4 h5 x, seven_b2_eval_0_2_4 t hb h4 h5 x, seven_b2_eval_0_2_5 t hb h4 h5 x, seven_b2_eval_0_2_6 t hb h4 h5 x, seven_b2_eval_0_2_7 t hb h4 h5 x, seven_b2_eval_0_3_0 t hb h4 h5 x, seven_b2_eval_0_3_1 t hb h4 h5 x, seven_b2_eval_0_3_2 t hb h4 h5 x, seven_b2_eval_0_3_3 t hb h4 h5 x, seven_b2_eval_0_3_4 t hb h4 h5 x, seven_b2_eval_0_3_5 t hb h4 h5 x, seven_b2_eval_0_3_6 t hb h4 h5 x, seven_b2_eval_0_4_0 t hb h4 h5 x, seven_b2_eval_0_4_1 t hb h4 h5 x, seven_b2_eval_0_4_2 t hb h4 h5 x, seven_b2_eval_0_4_3 t hb h4 h5 x, seven_b2_eval_0_4_4 t hb h4 h5 x, seven_b2_eval_0_4_5 t hb h4 h5 x, seven_b2_eval_0_5_0 t hb h4 h5 x, seven_b2_eval_0_5_1 t hb h4 h5 x, seven_b2_eval_0_5_2 t hb h4 h5 x, seven_b2_eval_0_5_3 t hb h4 h5 x, seven_b2_eval_0_5_4 t hb h4 h5 x, seven_b2_eval_0_6_0 t hb h4 h5 x, seven_b2_eval_0_6_1 t hb h4 h5 x, seven_b2_eval_0_6_2 t hb h4 h5 x, seven_b2_eval_0_6_3 t hb h4 h5 x]
  all_goals ring

set_option maxHeartbeats 300000 in
lemma seven_b2_eval_1_3_5 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K) :
    sevenCoefficientAt t x 1 3 5 = ((-8400) * t.b₂) * x 12 := by
  rw [sevenCoefficientAt_succ]
  norm_num only [coefficientBracket, coeffDq, coeffDP, coeffQ, coeffP, hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, sub_zero, zero_sub, false_and, and_false, true_and, and_true, if_true, if_false]
  simp only [seven_b2_eval_0_0_1 t hb h4 h5 x, seven_b2_eval_0_0_2 t hb h4 h5 x, seven_b2_eval_0_0_3 t hb h4 h5 x, seven_b2_eval_0_0_4 t hb h4 h5 x, seven_b2_eval_0_0_5 t hb h4 h5 x, seven_b2_eval_0_0_6 t hb h4 h5 x, seven_b2_eval_0_0_7 t hb h4 h5 x, seven_b2_eval_0_0_8 t hb h4 h5 x, seven_b2_eval_0_0_9 t hb h4 h5 x, seven_b2_eval_0_1_0 t hb h4 h5 x, seven_b2_eval_0_1_1 t hb h4 h5 x, seven_b2_eval_0_1_2 t hb h4 h5 x, seven_b2_eval_0_1_3 t hb h4 h5 x, seven_b2_eval_0_1_4 t hb h4 h5 x, seven_b2_eval_0_1_5 t hb h4 h5 x, seven_b2_eval_0_1_6 t hb h4 h5 x, seven_b2_eval_0_1_7 t hb h4 h5 x, seven_b2_eval_0_1_8 t hb h4 h5 x, seven_b2_eval_0_2_0 t hb h4 h5 x, seven_b2_eval_0_2_1 t hb h4 h5 x, seven_b2_eval_0_2_2 t hb h4 h5 x, seven_b2_eval_0_2_3 t hb h4 h5 x, seven_b2_eval_0_2_4 t hb h4 h5 x, seven_b2_eval_0_2_5 t hb h4 h5 x, seven_b2_eval_0_2_6 t hb h4 h5 x, seven_b2_eval_0_2_7 t hb h4 h5 x, seven_b2_eval_0_3_0 t hb h4 h5 x, seven_b2_eval_0_3_1 t hb h4 h5 x, seven_b2_eval_0_3_2 t hb h4 h5 x, seven_b2_eval_0_3_3 t hb h4 h5 x, seven_b2_eval_0_3_4 t hb h4 h5 x, seven_b2_eval_0_3_5 t hb h4 h5 x, seven_b2_eval_0_3_6 t hb h4 h5 x, seven_b2_eval_0_4_0 t hb h4 h5 x, seven_b2_eval_0_4_1 t hb h4 h5 x, seven_b2_eval_0_4_2 t hb h4 h5 x, seven_b2_eval_0_4_3 t hb h4 h5 x, seven_b2_eval_0_4_4 t hb h4 h5 x, seven_b2_eval_0_4_5 t hb h4 h5 x, seven_b2_eval_0_5_0 t hb h4 h5 x, seven_b2_eval_0_5_1 t hb h4 h5 x, seven_b2_eval_0_5_2 t hb h4 h5 x, seven_b2_eval_0_5_3 t hb h4 h5 x, seven_b2_eval_0_5_4 t hb h4 h5 x, seven_b2_eval_0_6_0 t hb h4 h5 x, seven_b2_eval_0_6_1 t hb h4 h5 x, seven_b2_eval_0_6_2 t hb h4 h5 x, seven_b2_eval_0_6_3 t hb h4 h5 x]
  all_goals ring

set_option maxHeartbeats 300000 in
lemma seven_b2_eval_1_4_1 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K) :
    sevenCoefficientAt t x 1 4 1 = (60 * t.b₂) * x 6 + ((180 * t.b₁) + (180 * t.c₃)) * x 7 + (((-7560) * t.b₀) + ((-5040) * t.c₂) + (140 * (t.b₂ ^ 2))) * x 8 + (((-630) * t.c₁) + (105 * t.b₁ * t.b₂)) * x 9 + (((-50) * t.b₁ * t.b₂) + ((-20) * t.b₂ * t.c₃)) * x 10 + ((210 * t.b₂ * t.c₁) + (840 * t.b₁ * t.c₂) + (840 * t.c₂ * t.c₃) + (1260 * t.b₀ * t.b₁) + (1260 * t.b₀ * t.c₃)) * x 11 + ((2100 * t.b₀ * t.b₁ * t.b₂) + (2100 * t.b₀ * t.b₂ * t.c₃)) * x 12 := by
  rw [sevenCoefficientAt_succ]
  norm_num only [coefficientBracket, coeffDq, coeffDP, coeffQ, coeffP, hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, sub_zero, zero_sub, false_and, and_false, true_and, and_true, if_true, if_false]
  simp only [seven_b2_eval_0_0_1 t hb h4 h5 x, seven_b2_eval_0_0_2 t hb h4 h5 x, seven_b2_eval_0_0_3 t hb h4 h5 x, seven_b2_eval_0_0_4 t hb h4 h5 x, seven_b2_eval_0_0_5 t hb h4 h5 x, seven_b2_eval_0_0_6 t hb h4 h5 x, seven_b2_eval_0_0_7 t hb h4 h5 x, seven_b2_eval_0_0_8 t hb h4 h5 x, seven_b2_eval_0_0_9 t hb h4 h5 x, seven_b2_eval_0_1_0 t hb h4 h5 x, seven_b2_eval_0_1_1 t hb h4 h5 x, seven_b2_eval_0_1_2 t hb h4 h5 x, seven_b2_eval_0_1_3 t hb h4 h5 x, seven_b2_eval_0_1_4 t hb h4 h5 x, seven_b2_eval_0_1_5 t hb h4 h5 x, seven_b2_eval_0_1_6 t hb h4 h5 x, seven_b2_eval_0_1_7 t hb h4 h5 x, seven_b2_eval_0_1_8 t hb h4 h5 x, seven_b2_eval_0_2_0 t hb h4 h5 x, seven_b2_eval_0_2_1 t hb h4 h5 x, seven_b2_eval_0_2_2 t hb h4 h5 x, seven_b2_eval_0_2_3 t hb h4 h5 x, seven_b2_eval_0_2_4 t hb h4 h5 x, seven_b2_eval_0_2_5 t hb h4 h5 x, seven_b2_eval_0_2_6 t hb h4 h5 x, seven_b2_eval_0_2_7 t hb h4 h5 x, seven_b2_eval_0_3_0 t hb h4 h5 x, seven_b2_eval_0_3_1 t hb h4 h5 x, seven_b2_eval_0_3_2 t hb h4 h5 x, seven_b2_eval_0_3_3 t hb h4 h5 x, seven_b2_eval_0_3_4 t hb h4 h5 x, seven_b2_eval_0_3_5 t hb h4 h5 x, seven_b2_eval_0_3_6 t hb h4 h5 x, seven_b2_eval_0_4_0 t hb h4 h5 x, seven_b2_eval_0_4_1 t hb h4 h5 x, seven_b2_eval_0_4_2 t hb h4 h5 x, seven_b2_eval_0_4_3 t hb h4 h5 x, seven_b2_eval_0_4_4 t hb h4 h5 x, seven_b2_eval_0_4_5 t hb h4 h5 x, seven_b2_eval_0_5_0 t hb h4 h5 x, seven_b2_eval_0_5_1 t hb h4 h5 x, seven_b2_eval_0_5_2 t hb h4 h5 x, seven_b2_eval_0_5_3 t hb h4 h5 x, seven_b2_eval_0_5_4 t hb h4 h5 x, seven_b2_eval_0_6_0 t hb h4 h5 x, seven_b2_eval_0_6_1 t hb h4 h5 x, seven_b2_eval_0_6_2 t hb h4 h5 x, seven_b2_eval_0_6_3 t hb h4 h5 x]
  all_goals ring

set_option maxHeartbeats 300000 in
lemma seven_b2_eval_1_4_2 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K) :
    sevenCoefficientAt t x 1 4 2 = (-270) * x 6 + ((-4200) * t.b₂) * x 8 + ((525 * t.b₁) + (525 * t.c₃)) * x 9 + ((90 * t.b₁) + (90 * t.c₃)) * x 10 + ((315 * t.b₁ * t.b₂) + (525 * t.b₂ * t.c₃)) * x 11 + ((2100 * t.b₂ * t.c₁) + (8400 * t.b₁ * t.c₂) + (8400 * t.c₂ * t.c₃) + (18900 * t.b₀ * t.b₁) + (18900 * t.b₀ * t.c₃)) * x 12 := by
  rw [sevenCoefficientAt_succ]
  norm_num only [coefficientBracket, coeffDq, coeffDP, coeffQ, coeffP, hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, sub_zero, zero_sub, false_and, and_false, true_and, and_true, if_true, if_false]
  simp only [seven_b2_eval_0_0_1 t hb h4 h5 x, seven_b2_eval_0_0_2 t hb h4 h5 x, seven_b2_eval_0_0_3 t hb h4 h5 x, seven_b2_eval_0_0_4 t hb h4 h5 x, seven_b2_eval_0_0_5 t hb h4 h5 x, seven_b2_eval_0_0_6 t hb h4 h5 x, seven_b2_eval_0_0_7 t hb h4 h5 x, seven_b2_eval_0_0_8 t hb h4 h5 x, seven_b2_eval_0_0_9 t hb h4 h5 x, seven_b2_eval_0_1_0 t hb h4 h5 x, seven_b2_eval_0_1_1 t hb h4 h5 x, seven_b2_eval_0_1_2 t hb h4 h5 x, seven_b2_eval_0_1_3 t hb h4 h5 x, seven_b2_eval_0_1_4 t hb h4 h5 x, seven_b2_eval_0_1_5 t hb h4 h5 x, seven_b2_eval_0_1_6 t hb h4 h5 x, seven_b2_eval_0_1_7 t hb h4 h5 x, seven_b2_eval_0_1_8 t hb h4 h5 x, seven_b2_eval_0_2_0 t hb h4 h5 x, seven_b2_eval_0_2_1 t hb h4 h5 x, seven_b2_eval_0_2_2 t hb h4 h5 x, seven_b2_eval_0_2_3 t hb h4 h5 x, seven_b2_eval_0_2_4 t hb h4 h5 x, seven_b2_eval_0_2_5 t hb h4 h5 x, seven_b2_eval_0_2_6 t hb h4 h5 x, seven_b2_eval_0_2_7 t hb h4 h5 x, seven_b2_eval_0_3_0 t hb h4 h5 x, seven_b2_eval_0_3_1 t hb h4 h5 x, seven_b2_eval_0_3_2 t hb h4 h5 x, seven_b2_eval_0_3_3 t hb h4 h5 x, seven_b2_eval_0_3_4 t hb h4 h5 x, seven_b2_eval_0_3_5 t hb h4 h5 x, seven_b2_eval_0_3_6 t hb h4 h5 x, seven_b2_eval_0_4_0 t hb h4 h5 x, seven_b2_eval_0_4_1 t hb h4 h5 x, seven_b2_eval_0_4_2 t hb h4 h5 x, seven_b2_eval_0_4_3 t hb h4 h5 x, seven_b2_eval_0_4_4 t hb h4 h5 x, seven_b2_eval_0_4_5 t hb h4 h5 x, seven_b2_eval_0_5_0 t hb h4 h5 x, seven_b2_eval_0_5_1 t hb h4 h5 x, seven_b2_eval_0_5_2 t hb h4 h5 x, seven_b2_eval_0_5_3 t hb h4 h5 x, seven_b2_eval_0_5_4 t hb h4 h5 x, seven_b2_eval_0_6_0 t hb h4 h5 x, seven_b2_eval_0_6_1 t hb h4 h5 x, seven_b2_eval_0_6_2 t hb h4 h5 x, seven_b2_eval_0_6_3 t hb h4 h5 x]
  all_goals ring

set_option maxHeartbeats 300000 in
lemma seven_b2_eval_1_4_3 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K) :
    sevenCoefficientAt t x 1 4 3 = (-22680) * x 8 + ((3780 * t.b₁) + (3780 * t.c₃)) * x 11 + ((9800 * t.b₁ * t.b₂) + (10500 * t.b₂ * t.c₃)) * x 12 := by
  rw [sevenCoefficientAt_succ]
  norm_num only [coefficientBracket, coeffDq, coeffDP, coeffQ, coeffP, hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, sub_zero, zero_sub, false_and, and_false, true_and, and_true, if_true, if_false]
  simp only [seven_b2_eval_0_0_1 t hb h4 h5 x, seven_b2_eval_0_0_2 t hb h4 h5 x, seven_b2_eval_0_0_3 t hb h4 h5 x, seven_b2_eval_0_0_4 t hb h4 h5 x, seven_b2_eval_0_0_5 t hb h4 h5 x, seven_b2_eval_0_0_6 t hb h4 h5 x, seven_b2_eval_0_0_7 t hb h4 h5 x, seven_b2_eval_0_0_8 t hb h4 h5 x, seven_b2_eval_0_0_9 t hb h4 h5 x, seven_b2_eval_0_1_0 t hb h4 h5 x, seven_b2_eval_0_1_1 t hb h4 h5 x, seven_b2_eval_0_1_2 t hb h4 h5 x, seven_b2_eval_0_1_3 t hb h4 h5 x, seven_b2_eval_0_1_4 t hb h4 h5 x, seven_b2_eval_0_1_5 t hb h4 h5 x, seven_b2_eval_0_1_6 t hb h4 h5 x, seven_b2_eval_0_1_7 t hb h4 h5 x, seven_b2_eval_0_1_8 t hb h4 h5 x, seven_b2_eval_0_2_0 t hb h4 h5 x, seven_b2_eval_0_2_1 t hb h4 h5 x, seven_b2_eval_0_2_2 t hb h4 h5 x, seven_b2_eval_0_2_3 t hb h4 h5 x, seven_b2_eval_0_2_4 t hb h4 h5 x, seven_b2_eval_0_2_5 t hb h4 h5 x, seven_b2_eval_0_2_6 t hb h4 h5 x, seven_b2_eval_0_2_7 t hb h4 h5 x, seven_b2_eval_0_3_0 t hb h4 h5 x, seven_b2_eval_0_3_1 t hb h4 h5 x, seven_b2_eval_0_3_2 t hb h4 h5 x, seven_b2_eval_0_3_3 t hb h4 h5 x, seven_b2_eval_0_3_4 t hb h4 h5 x, seven_b2_eval_0_3_5 t hb h4 h5 x, seven_b2_eval_0_3_6 t hb h4 h5 x, seven_b2_eval_0_4_0 t hb h4 h5 x, seven_b2_eval_0_4_1 t hb h4 h5 x, seven_b2_eval_0_4_2 t hb h4 h5 x, seven_b2_eval_0_4_3 t hb h4 h5 x, seven_b2_eval_0_4_4 t hb h4 h5 x, seven_b2_eval_0_4_5 t hb h4 h5 x, seven_b2_eval_0_5_0 t hb h4 h5 x, seven_b2_eval_0_5_1 t hb h4 h5 x, seven_b2_eval_0_5_2 t hb h4 h5 x, seven_b2_eval_0_5_3 t hb h4 h5 x, seven_b2_eval_0_5_4 t hb h4 h5 x, seven_b2_eval_0_6_0 t hb h4 h5 x, seven_b2_eval_0_6_1 t hb h4 h5 x, seven_b2_eval_0_6_2 t hb h4 h5 x, seven_b2_eval_0_6_3 t hb h4 h5 x]
  all_goals ring

set_option maxHeartbeats 300000 in
lemma seven_b2_eval_1_5_1 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K) :
    sevenCoefficientAt t x 1 5 1 = (120 * t.b₂) * x 7 + (((-7560) * t.c₃) + ((-6048) * t.b₁)) * x 8 + (((-1512) * t.b₀) + ((-1260) * t.c₂) + (70 * (t.b₂ ^ 2))) * x 9 + ((-20) * (t.b₂ ^ 2)) * x 10 + ((1008 * (t.b₁ ^ 2)) + (1260 * (t.c₃ ^ 2)) + (420 * t.b₂ * t.c₂) + (504 * t.b₀ * t.b₂) + (2268 * t.b₁ * t.c₃)) * x 11 + (((-7560) * t.b₁ * t.c₁) + ((-7560) * t.c₁ * t.c₃) + (840 * t.b₀ * (t.b₂ ^ 2)) + (1680 * t.b₂ * (t.b₁ ^ 2)) + (1680 * t.b₁ * t.b₂ * t.c₃)) * x 12 := by
  rw [sevenCoefficientAt_succ]
  norm_num only [coefficientBracket, coeffDq, coeffDP, coeffQ, coeffP, hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, sub_zero, zero_sub, false_and, and_false, true_and, and_true, if_true, if_false]
  simp only [seven_b2_eval_0_0_1 t hb h4 h5 x, seven_b2_eval_0_0_2 t hb h4 h5 x, seven_b2_eval_0_0_3 t hb h4 h5 x, seven_b2_eval_0_0_4 t hb h4 h5 x, seven_b2_eval_0_0_5 t hb h4 h5 x, seven_b2_eval_0_0_6 t hb h4 h5 x, seven_b2_eval_0_0_7 t hb h4 h5 x, seven_b2_eval_0_0_8 t hb h4 h5 x, seven_b2_eval_0_0_9 t hb h4 h5 x, seven_b2_eval_0_1_0 t hb h4 h5 x, seven_b2_eval_0_1_1 t hb h4 h5 x, seven_b2_eval_0_1_2 t hb h4 h5 x, seven_b2_eval_0_1_3 t hb h4 h5 x, seven_b2_eval_0_1_4 t hb h4 h5 x, seven_b2_eval_0_1_5 t hb h4 h5 x, seven_b2_eval_0_1_6 t hb h4 h5 x, seven_b2_eval_0_1_7 t hb h4 h5 x, seven_b2_eval_0_1_8 t hb h4 h5 x, seven_b2_eval_0_2_0 t hb h4 h5 x, seven_b2_eval_0_2_1 t hb h4 h5 x, seven_b2_eval_0_2_2 t hb h4 h5 x, seven_b2_eval_0_2_3 t hb h4 h5 x, seven_b2_eval_0_2_4 t hb h4 h5 x, seven_b2_eval_0_2_5 t hb h4 h5 x, seven_b2_eval_0_2_6 t hb h4 h5 x, seven_b2_eval_0_2_7 t hb h4 h5 x, seven_b2_eval_0_3_0 t hb h4 h5 x, seven_b2_eval_0_3_1 t hb h4 h5 x, seven_b2_eval_0_3_2 t hb h4 h5 x, seven_b2_eval_0_3_3 t hb h4 h5 x, seven_b2_eval_0_3_4 t hb h4 h5 x, seven_b2_eval_0_3_5 t hb h4 h5 x, seven_b2_eval_0_3_6 t hb h4 h5 x, seven_b2_eval_0_4_0 t hb h4 h5 x, seven_b2_eval_0_4_1 t hb h4 h5 x, seven_b2_eval_0_4_2 t hb h4 h5 x, seven_b2_eval_0_4_3 t hb h4 h5 x, seven_b2_eval_0_4_4 t hb h4 h5 x, seven_b2_eval_0_4_5 t hb h4 h5 x, seven_b2_eval_0_5_0 t hb h4 h5 x, seven_b2_eval_0_5_1 t hb h4 h5 x, seven_b2_eval_0_5_2 t hb h4 h5 x, seven_b2_eval_0_5_3 t hb h4 h5 x, seven_b2_eval_0_5_4 t hb h4 h5 x, seven_b2_eval_0_6_0 t hb h4 h5 x, seven_b2_eval_0_6_1 t hb h4 h5 x, seven_b2_eval_0_6_2 t hb h4 h5 x, seven_b2_eval_0_6_3 t hb h4 h5 x]
  all_goals ring

set_option maxHeartbeats 300000 in
lemma seven_b2_eval_1_5_2 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K) :
    sevenCoefficientAt t x 1 5 2 = (-216) * x 7 + ((-630) * t.b₂) * x 9 + (36 * t.b₂) * x 10 + (126 * (t.b₂ ^ 2)) * x 11 + ((10080 * (t.b₁ ^ 2)) + (11340 * (t.c₃ ^ 2)) + (4200 * t.b₂ * t.c₂) + (7560 * t.b₀ * t.b₂) + (21420 * t.b₁ * t.c₃)) * x 12 := by
  rw [sevenCoefficientAt_succ]
  norm_num only [coefficientBracket, coeffDq, coeffDP, coeffQ, coeffP, hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, sub_zero, zero_sub, false_and, and_false, true_and, and_true, if_true, if_false]
  simp only [seven_b2_eval_0_0_1 t hb h4 h5 x, seven_b2_eval_0_0_2 t hb h4 h5 x, seven_b2_eval_0_0_3 t hb h4 h5 x, seven_b2_eval_0_0_4 t hb h4 h5 x, seven_b2_eval_0_0_5 t hb h4 h5 x, seven_b2_eval_0_0_6 t hb h4 h5 x, seven_b2_eval_0_0_7 t hb h4 h5 x, seven_b2_eval_0_0_8 t hb h4 h5 x, seven_b2_eval_0_0_9 t hb h4 h5 x, seven_b2_eval_0_1_0 t hb h4 h5 x, seven_b2_eval_0_1_1 t hb h4 h5 x, seven_b2_eval_0_1_2 t hb h4 h5 x, seven_b2_eval_0_1_3 t hb h4 h5 x, seven_b2_eval_0_1_4 t hb h4 h5 x, seven_b2_eval_0_1_5 t hb h4 h5 x, seven_b2_eval_0_1_6 t hb h4 h5 x, seven_b2_eval_0_1_7 t hb h4 h5 x, seven_b2_eval_0_1_8 t hb h4 h5 x, seven_b2_eval_0_2_0 t hb h4 h5 x, seven_b2_eval_0_2_1 t hb h4 h5 x, seven_b2_eval_0_2_2 t hb h4 h5 x, seven_b2_eval_0_2_3 t hb h4 h5 x, seven_b2_eval_0_2_4 t hb h4 h5 x, seven_b2_eval_0_2_5 t hb h4 h5 x, seven_b2_eval_0_2_6 t hb h4 h5 x, seven_b2_eval_0_2_7 t hb h4 h5 x, seven_b2_eval_0_3_0 t hb h4 h5 x, seven_b2_eval_0_3_1 t hb h4 h5 x, seven_b2_eval_0_3_2 t hb h4 h5 x, seven_b2_eval_0_3_3 t hb h4 h5 x, seven_b2_eval_0_3_4 t hb h4 h5 x, seven_b2_eval_0_3_5 t hb h4 h5 x, seven_b2_eval_0_3_6 t hb h4 h5 x, seven_b2_eval_0_4_0 t hb h4 h5 x, seven_b2_eval_0_4_1 t hb h4 h5 x, seven_b2_eval_0_4_2 t hb h4 h5 x, seven_b2_eval_0_4_3 t hb h4 h5 x, seven_b2_eval_0_4_4 t hb h4 h5 x, seven_b2_eval_0_4_5 t hb h4 h5 x, seven_b2_eval_0_5_0 t hb h4 h5 x, seven_b2_eval_0_5_1 t hb h4 h5 x, seven_b2_eval_0_5_2 t hb h4 h5 x, seven_b2_eval_0_5_3 t hb h4 h5 x, seven_b2_eval_0_5_4 t hb h4 h5 x, seven_b2_eval_0_6_0 t hb h4 h5 x, seven_b2_eval_0_6_1 t hb h4 h5 x, seven_b2_eval_0_6_2 t hb h4 h5 x, seven_b2_eval_0_6_3 t hb h4 h5 x]
  all_goals ring

set_option maxHeartbeats 300000 in
lemma seven_b2_eval_1_5_3 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K) :
    sevenCoefficientAt t x 1 5 3 = (-4536) * x 9 + (1512 * t.b₂) * x 11 + (3920 * (t.b₂ ^ 2)) * x 12 := by
  rw [sevenCoefficientAt_succ]
  norm_num only [coefficientBracket, coeffDq, coeffDP, coeffQ, coeffP, hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, sub_zero, zero_sub, false_and, and_false, true_and, and_true, if_true, if_false]
  simp only [seven_b2_eval_0_0_1 t hb h4 h5 x, seven_b2_eval_0_0_2 t hb h4 h5 x, seven_b2_eval_0_0_3 t hb h4 h5 x, seven_b2_eval_0_0_4 t hb h4 h5 x, seven_b2_eval_0_0_5 t hb h4 h5 x, seven_b2_eval_0_0_6 t hb h4 h5 x, seven_b2_eval_0_0_7 t hb h4 h5 x, seven_b2_eval_0_0_8 t hb h4 h5 x, seven_b2_eval_0_0_9 t hb h4 h5 x, seven_b2_eval_0_1_0 t hb h4 h5 x, seven_b2_eval_0_1_1 t hb h4 h5 x, seven_b2_eval_0_1_2 t hb h4 h5 x, seven_b2_eval_0_1_3 t hb h4 h5 x, seven_b2_eval_0_1_4 t hb h4 h5 x, seven_b2_eval_0_1_5 t hb h4 h5 x, seven_b2_eval_0_1_6 t hb h4 h5 x, seven_b2_eval_0_1_7 t hb h4 h5 x, seven_b2_eval_0_1_8 t hb h4 h5 x, seven_b2_eval_0_2_0 t hb h4 h5 x, seven_b2_eval_0_2_1 t hb h4 h5 x, seven_b2_eval_0_2_2 t hb h4 h5 x, seven_b2_eval_0_2_3 t hb h4 h5 x, seven_b2_eval_0_2_4 t hb h4 h5 x, seven_b2_eval_0_2_5 t hb h4 h5 x, seven_b2_eval_0_2_6 t hb h4 h5 x, seven_b2_eval_0_2_7 t hb h4 h5 x, seven_b2_eval_0_3_0 t hb h4 h5 x, seven_b2_eval_0_3_1 t hb h4 h5 x, seven_b2_eval_0_3_2 t hb h4 h5 x, seven_b2_eval_0_3_3 t hb h4 h5 x, seven_b2_eval_0_3_4 t hb h4 h5 x, seven_b2_eval_0_3_5 t hb h4 h5 x, seven_b2_eval_0_3_6 t hb h4 h5 x, seven_b2_eval_0_4_0 t hb h4 h5 x, seven_b2_eval_0_4_1 t hb h4 h5 x, seven_b2_eval_0_4_2 t hb h4 h5 x, seven_b2_eval_0_4_3 t hb h4 h5 x, seven_b2_eval_0_4_4 t hb h4 h5 x, seven_b2_eval_0_4_5 t hb h4 h5 x, seven_b2_eval_0_5_0 t hb h4 h5 x, seven_b2_eval_0_5_1 t hb h4 h5 x, seven_b2_eval_0_5_2 t hb h4 h5 x, seven_b2_eval_0_5_3 t hb h4 h5 x, seven_b2_eval_0_5_4 t hb h4 h5 x, seven_b2_eval_0_6_0 t hb h4 h5 x, seven_b2_eval_0_6_1 t hb h4 h5 x, seven_b2_eval_0_6_2 t hb h4 h5 x, seven_b2_eval_0_6_3 t hb h4 h5 x]
  all_goals ring

set_option maxHeartbeats 300000 in
lemma seven_b2_eval_2_0_4 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K) :
    sevenCoefficientAt t x 2 0 4 = 18 * x 1 + ((-12) * t.b₂) * x 5 + ((-225) * t.b₁) * x 6 + (360 * t.b₀) * x 7 + ((-3360) * t.c₁) * x 8 + ((80 * (t.b₁ ^ 2)) + ((-40) * t.b₀ * t.b₂)) * x 10 + (((-210) * t.b₀ * t.c₂) + (945 * t.b₁ * t.c₁)) * x 11 + (2100 * (t.c₁ ^ 2)) * x 12 := by
  rw [sevenCoefficientAt_succ]
  norm_num only [coefficientBracket, coeffDq, coeffDP, coeffQ, coeffP, hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, sub_zero, zero_sub, false_and, and_false, true_and, and_true, if_true, if_false]
  simp only [seven_b2_eval_1_0_2 t hb h4 h5 x, seven_b2_eval_1_0_3 t hb h4 h5 x, seven_b2_eval_1_0_4 t hb h4 h5 x, seven_b2_eval_1_0_5 t hb h4 h5 x, seven_b2_eval_1_0_6 t hb h4 h5 x, seven_b2_eval_1_0_7 t hb h4 h5 x, seven_b2_eval_1_0_8 t hb h4 h5 x, seven_b2_eval_1_1_1 t hb h4 h5 x, seven_b2_eval_1_1_2 t hb h4 h5 x, seven_b2_eval_1_1_3 t hb h4 h5 x, seven_b2_eval_1_1_4 t hb h4 h5 x, seven_b2_eval_1_1_5 t hb h4 h5 x, seven_b2_eval_1_1_6 t hb h4 h5 x, seven_b2_eval_1_1_7 t hb h4 h5 x, seven_b2_eval_1_2_0 t hb h4 h5 x, seven_b2_eval_1_2_1 t hb h4 h5 x, seven_b2_eval_1_2_2 t hb h4 h5 x, seven_b2_eval_1_2_3 t hb h4 h5 x, seven_b2_eval_1_2_4 t hb h4 h5 x, seven_b2_eval_1_2_5 t hb h4 h5 x, seven_b2_eval_1_2_6 t hb h4 h5 x, seven_b2_eval_1_3_0 t hb h4 h5 x, seven_b2_eval_1_3_1 t hb h4 h5 x, seven_b2_eval_1_3_2 t hb h4 h5 x, seven_b2_eval_1_3_3 t hb h4 h5 x, seven_b2_eval_1_3_4 t hb h4 h5 x, seven_b2_eval_1_3_5 t hb h4 h5 x, seven_b2_eval_1_4_1 t hb h4 h5 x, seven_b2_eval_1_4_2 t hb h4 h5 x, seven_b2_eval_1_4_3 t hb h4 h5 x, seven_b2_eval_1_5_1 t hb h4 h5 x, seven_b2_eval_1_5_2 t hb h4 h5 x, seven_b2_eval_1_5_3 t hb h4 h5 x]
  all_goals ring

set_option maxHeartbeats 300000 in
lemma seven_b2_eval_2_1_2 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K) :
    sevenCoefficientAt t x 2 1 2 = ((-6) * t.b₂) * x 0 + (6 * t.b₁) * x 1 + ((-18) * t.c₃) * x 2 + (((-36) * t.b₀) + ((-30) * t.c₂)) * x 3 + ((-48) * t.c₁) * x 4 + (12 * t.b₁ * t.b₂) * x 5 + ((15 * (t.b₁ ^ 2)) + ((-330) * t.b₀ * t.b₂)) * x 6 + ((-60) * t.b₀ * t.b₁) * x 7 + (((-7560) * (t.b₀ ^ 2)) + ((-2520) * t.b₀ * t.c₂) + (1260 * t.b₁ * t.c₁)) * x 8 + ((-840) * t.b₀ * t.c₁) * x 9 + (240 * t.c₁ * t.c₂) * x 10 + ((1260 * t.b₁ * (t.b₀ ^ 2)) + (1260 * t.c₃ * (t.b₀ ^ 2))) * x 11 := by
  rw [sevenCoefficientAt_succ]
  norm_num only [coefficientBracket, coeffDq, coeffDP, coeffQ, coeffP, hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, sub_zero, zero_sub, false_and, and_false, true_and, and_true, if_true, if_false]
  simp only [seven_b2_eval_1_0_2 t hb h4 h5 x, seven_b2_eval_1_0_3 t hb h4 h5 x, seven_b2_eval_1_0_4 t hb h4 h5 x, seven_b2_eval_1_0_5 t hb h4 h5 x, seven_b2_eval_1_0_6 t hb h4 h5 x, seven_b2_eval_1_0_7 t hb h4 h5 x, seven_b2_eval_1_0_8 t hb h4 h5 x, seven_b2_eval_1_1_1 t hb h4 h5 x, seven_b2_eval_1_1_2 t hb h4 h5 x, seven_b2_eval_1_1_3 t hb h4 h5 x, seven_b2_eval_1_1_4 t hb h4 h5 x, seven_b2_eval_1_1_5 t hb h4 h5 x, seven_b2_eval_1_1_6 t hb h4 h5 x, seven_b2_eval_1_1_7 t hb h4 h5 x, seven_b2_eval_1_2_0 t hb h4 h5 x, seven_b2_eval_1_2_1 t hb h4 h5 x, seven_b2_eval_1_2_2 t hb h4 h5 x, seven_b2_eval_1_2_3 t hb h4 h5 x, seven_b2_eval_1_2_4 t hb h4 h5 x, seven_b2_eval_1_2_5 t hb h4 h5 x, seven_b2_eval_1_2_6 t hb h4 h5 x, seven_b2_eval_1_3_0 t hb h4 h5 x, seven_b2_eval_1_3_1 t hb h4 h5 x, seven_b2_eval_1_3_2 t hb h4 h5 x, seven_b2_eval_1_3_3 t hb h4 h5 x, seven_b2_eval_1_3_4 t hb h4 h5 x, seven_b2_eval_1_3_5 t hb h4 h5 x, seven_b2_eval_1_4_1 t hb h4 h5 x, seven_b2_eval_1_4_2 t hb h4 h5 x, seven_b2_eval_1_4_3 t hb h4 h5 x, seven_b2_eval_1_5_1 t hb h4 h5 x, seven_b2_eval_1_5_2 t hb h4 h5 x, seven_b2_eval_1_5_3 t hb h4 h5 x]
  all_goals ring

set_option maxHeartbeats 300000 in
lemma seven_b2_eval_2_1_3 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K) :
    sevenCoefficientAt t x 2 1 3 = ((-24) * t.b₂) * x 3 + ((-12) * t.b₁) * x 4 + ((-36) * t.c₃) * x 5 + (((-2160) * t.b₀) + ((-720) * t.c₂)) * x 6 + ((-1080) * t.c₁) * x 7 + ((560 * (t.b₁ ^ 2)) + ((-7280) * t.b₀ * t.b₂)) * x 8 + ((-420) * t.b₀ * t.b₁) * x 9 + ((240 * t.b₁ * t.c₂) + (280 * t.b₂ * t.c₁) + (600 * t.b₀ * t.c₃) + (720 * t.b₀ * t.b₁)) * x 10 + (1680 * t.c₁ * t.c₂) * x 11 + ((8400 * t.b₁ * (t.b₀ ^ 2)) + (8400 * t.c₃ * (t.b₀ ^ 2))) * x 12 := by
  rw [sevenCoefficientAt_succ]
  norm_num only [coefficientBracket, coeffDq, coeffDP, coeffQ, coeffP, hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, sub_zero, zero_sub, false_and, and_false, true_and, and_true, if_true, if_false]
  simp only [seven_b2_eval_1_0_2 t hb h4 h5 x, seven_b2_eval_1_0_3 t hb h4 h5 x, seven_b2_eval_1_0_4 t hb h4 h5 x, seven_b2_eval_1_0_5 t hb h4 h5 x, seven_b2_eval_1_0_6 t hb h4 h5 x, seven_b2_eval_1_0_7 t hb h4 h5 x, seven_b2_eval_1_0_8 t hb h4 h5 x, seven_b2_eval_1_1_1 t hb h4 h5 x, seven_b2_eval_1_1_2 t hb h4 h5 x, seven_b2_eval_1_1_3 t hb h4 h5 x, seven_b2_eval_1_1_4 t hb h4 h5 x, seven_b2_eval_1_1_5 t hb h4 h5 x, seven_b2_eval_1_1_6 t hb h4 h5 x, seven_b2_eval_1_1_7 t hb h4 h5 x, seven_b2_eval_1_2_0 t hb h4 h5 x, seven_b2_eval_1_2_1 t hb h4 h5 x, seven_b2_eval_1_2_2 t hb h4 h5 x, seven_b2_eval_1_2_3 t hb h4 h5 x, seven_b2_eval_1_2_4 t hb h4 h5 x, seven_b2_eval_1_2_5 t hb h4 h5 x, seven_b2_eval_1_2_6 t hb h4 h5 x, seven_b2_eval_1_3_0 t hb h4 h5 x, seven_b2_eval_1_3_1 t hb h4 h5 x, seven_b2_eval_1_3_2 t hb h4 h5 x, seven_b2_eval_1_3_3 t hb h4 h5 x, seven_b2_eval_1_3_4 t hb h4 h5 x, seven_b2_eval_1_3_5 t hb h4 h5 x, seven_b2_eval_1_4_1 t hb h4 h5 x, seven_b2_eval_1_4_2 t hb h4 h5 x, seven_b2_eval_1_4_3 t hb h4 h5 x, seven_b2_eval_1_5_1 t hb h4 h5 x, seven_b2_eval_1_5_2 t hb h4 h5 x, seven_b2_eval_1_5_3 t hb h4 h5 x]
  all_goals ring

set_option maxHeartbeats 300000 in
lemma seven_b2_eval_2_1_4 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K) :
    sevenCoefficientAt t x 2 1 4 = (-54) * x 3 + ((-900) * t.b₂) * x 6 + ((-540) * t.b₁) * x 7 + (((-45360) * t.b₀) + ((-9240) * t.c₂)) * x 8 + ((-3360) * t.c₁) * x 9 + (280 * t.b₁ * t.b₂) * x 10 + ((1680 * t.b₁ * t.c₂) + (1890 * t.b₂ * t.c₁) + (6930 * t.b₀ * t.c₃) + (7560 * t.b₀ * t.b₁)) * x 11 + (8400 * t.c₁ * t.c₂) * x 12 := by
  rw [sevenCoefficientAt_succ]
  norm_num only [coefficientBracket, coeffDq, coeffDP, coeffQ, coeffP, hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, sub_zero, zero_sub, false_and, and_false, true_and, and_true, if_true, if_false]
  simp only [seven_b2_eval_1_0_2 t hb h4 h5 x, seven_b2_eval_1_0_3 t hb h4 h5 x, seven_b2_eval_1_0_4 t hb h4 h5 x, seven_b2_eval_1_0_5 t hb h4 h5 x, seven_b2_eval_1_0_6 t hb h4 h5 x, seven_b2_eval_1_0_7 t hb h4 h5 x, seven_b2_eval_1_0_8 t hb h4 h5 x, seven_b2_eval_1_1_1 t hb h4 h5 x, seven_b2_eval_1_1_2 t hb h4 h5 x, seven_b2_eval_1_1_3 t hb h4 h5 x, seven_b2_eval_1_1_4 t hb h4 h5 x, seven_b2_eval_1_1_5 t hb h4 h5 x, seven_b2_eval_1_1_6 t hb h4 h5 x, seven_b2_eval_1_1_7 t hb h4 h5 x, seven_b2_eval_1_2_0 t hb h4 h5 x, seven_b2_eval_1_2_1 t hb h4 h5 x, seven_b2_eval_1_2_2 t hb h4 h5 x, seven_b2_eval_1_2_3 t hb h4 h5 x, seven_b2_eval_1_2_4 t hb h4 h5 x, seven_b2_eval_1_2_5 t hb h4 h5 x, seven_b2_eval_1_2_6 t hb h4 h5 x, seven_b2_eval_1_3_0 t hb h4 h5 x, seven_b2_eval_1_3_1 t hb h4 h5 x, seven_b2_eval_1_3_2 t hb h4 h5 x, seven_b2_eval_1_3_3 t hb h4 h5 x, seven_b2_eval_1_3_4 t hb h4 h5 x, seven_b2_eval_1_3_5 t hb h4 h5 x, seven_b2_eval_1_4_1 t hb h4 h5 x, seven_b2_eval_1_4_2 t hb h4 h5 x, seven_b2_eval_1_4_3 t hb h4 h5 x, seven_b2_eval_1_5_1 t hb h4 h5 x, seven_b2_eval_1_5_2 t hb h4 h5 x, seven_b2_eval_1_5_3 t hb h4 h5 x]
  all_goals ring

set_option maxHeartbeats 300000 in
lemma seven_b2_eval_2_2_2 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K) :
    sevenCoefficientAt t x 2 2 2 = (((-54) * t.c₃) + ((-27) * t.b₁)) * x 3 + (((-108) * t.c₂) + ((-72) * t.b₀)) * x 4 + (12 * (t.b₂ ^ 2)) * x 5 + ((2160 * t.c₁) + ((-90) * t.b₁ * t.b₂)) * x 6 + ((-720) * t.b₀ * t.b₂) * x 7 + (((-2520) * t.b₀ * t.c₃) + ((-1260) * t.b₀ * t.b₁) + (1680 * t.b₁ * t.c₂) + (8400 * t.b₂ * t.c₁)) * x 8 + (((-3780) * (t.b₀ ^ 2)) + ((-2100) * t.b₀ * t.c₂) + (210 * t.b₁ * t.c₁)) * x 9 + ((240 * (t.c₂ ^ 2)) + ((-720) * t.b₁ * t.c₁) + ((-360) * t.c₁ * t.c₃)) * x 10 + ((630 * t.b₀ * (t.b₁ ^ 2)) + (1260 * t.b₂ * (t.b₀ ^ 2)) + (630 * t.b₀ * t.b₁ * t.c₃)) * x 11 + (((-25200) * t.b₀ * t.b₁ * t.c₁) + ((-25200) * t.b₀ * t.c₁ * t.c₃)) * x 12 := by
  rw [sevenCoefficientAt_succ]
  norm_num only [coefficientBracket, coeffDq, coeffDP, coeffQ, coeffP, hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, sub_zero, zero_sub, false_and, and_false, true_and, and_true, if_true, if_false]
  simp only [seven_b2_eval_1_0_2 t hb h4 h5 x, seven_b2_eval_1_0_3 t hb h4 h5 x, seven_b2_eval_1_0_4 t hb h4 h5 x, seven_b2_eval_1_0_5 t hb h4 h5 x, seven_b2_eval_1_0_6 t hb h4 h5 x, seven_b2_eval_1_0_7 t hb h4 h5 x, seven_b2_eval_1_0_8 t hb h4 h5 x, seven_b2_eval_1_1_1 t hb h4 h5 x, seven_b2_eval_1_1_2 t hb h4 h5 x, seven_b2_eval_1_1_3 t hb h4 h5 x, seven_b2_eval_1_1_4 t hb h4 h5 x, seven_b2_eval_1_1_5 t hb h4 h5 x, seven_b2_eval_1_1_6 t hb h4 h5 x, seven_b2_eval_1_1_7 t hb h4 h5 x, seven_b2_eval_1_2_0 t hb h4 h5 x, seven_b2_eval_1_2_1 t hb h4 h5 x, seven_b2_eval_1_2_2 t hb h4 h5 x, seven_b2_eval_1_2_3 t hb h4 h5 x, seven_b2_eval_1_2_4 t hb h4 h5 x, seven_b2_eval_1_2_5 t hb h4 h5 x, seven_b2_eval_1_2_6 t hb h4 h5 x, seven_b2_eval_1_3_0 t hb h4 h5 x, seven_b2_eval_1_3_1 t hb h4 h5 x, seven_b2_eval_1_3_2 t hb h4 h5 x, seven_b2_eval_1_3_3 t hb h4 h5 x, seven_b2_eval_1_3_4 t hb h4 h5 x, seven_b2_eval_1_3_5 t hb h4 h5 x, seven_b2_eval_1_4_1 t hb h4 h5 x, seven_b2_eval_1_4_2 t hb h4 h5 x, seven_b2_eval_1_4_3 t hb h4 h5 x, seven_b2_eval_1_5_1 t hb h4 h5 x, seven_b2_eval_1_5_2 t hb h4 h5 x, seven_b2_eval_1_5_3 t hb h4 h5 x]
  all_goals ring

set_option maxHeartbeats 300000 in
lemma seven_b2_eval_2_2_3 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K) :
    sevenCoefficientAt t x 2 2 3 = ((-60) * t.b₂) * x 4 + (((-1350) * t.c₃) + ((-540) * t.b₁)) * x 6 + (((-4320) * t.b₀) + ((-2520) * t.c₂)) * x 7 + ((68040 * t.c₁) + (840 * t.b₁ * t.b₂)) * x 8 + ((70 * (t.b₁ ^ 2)) + ((-4060) * t.b₀ * t.b₂)) * x 9 + ((180 * (t.b₁ ^ 2)) + (480 * t.b₁ * t.c₃) + (520 * t.b₂ * t.c₂) + (720 * t.b₀ * t.b₂)) * x 10 + ((1680 * (t.c₂ ^ 2)) + ((-11340) * t.b₁ * t.c₁) + ((-8820) * t.c₁ * t.c₃)) * x 11 + (((-4200) * t.b₀ * (t.b₁ ^ 2)) + (8400 * t.b₂ * (t.b₀ ^ 2)) + ((-4200) * t.b₀ * t.b₁ * t.c₃)) * x 12 := by
  rw [sevenCoefficientAt_succ]
  norm_num only [coefficientBracket, coeffDq, coeffDP, coeffQ, coeffP, hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, sub_zero, zero_sub, false_and, and_false, true_and, and_true, if_true, if_false]
  simp only [seven_b2_eval_1_0_2 t hb h4 h5 x, seven_b2_eval_1_0_3 t hb h4 h5 x, seven_b2_eval_1_0_4 t hb h4 h5 x, seven_b2_eval_1_0_5 t hb h4 h5 x, seven_b2_eval_1_0_6 t hb h4 h5 x, seven_b2_eval_1_0_7 t hb h4 h5 x, seven_b2_eval_1_0_8 t hb h4 h5 x, seven_b2_eval_1_1_1 t hb h4 h5 x, seven_b2_eval_1_1_2 t hb h4 h5 x, seven_b2_eval_1_1_3 t hb h4 h5 x, seven_b2_eval_1_1_4 t hb h4 h5 x, seven_b2_eval_1_1_5 t hb h4 h5 x, seven_b2_eval_1_1_6 t hb h4 h5 x, seven_b2_eval_1_1_7 t hb h4 h5 x, seven_b2_eval_1_2_0 t hb h4 h5 x, seven_b2_eval_1_2_1 t hb h4 h5 x, seven_b2_eval_1_2_2 t hb h4 h5 x, seven_b2_eval_1_2_3 t hb h4 h5 x, seven_b2_eval_1_2_4 t hb h4 h5 x, seven_b2_eval_1_2_5 t hb h4 h5 x, seven_b2_eval_1_2_6 t hb h4 h5 x, seven_b2_eval_1_3_0 t hb h4 h5 x, seven_b2_eval_1_3_1 t hb h4 h5 x, seven_b2_eval_1_3_2 t hb h4 h5 x, seven_b2_eval_1_3_3 t hb h4 h5 x, seven_b2_eval_1_3_4 t hb h4 h5 x, seven_b2_eval_1_3_5 t hb h4 h5 x, seven_b2_eval_1_4_1 t hb h4 h5 x, seven_b2_eval_1_4_2 t hb h4 h5 x, seven_b2_eval_1_4_3 t hb h4 h5 x, seven_b2_eval_1_5_1 t hb h4 h5 x, seven_b2_eval_1_5_2 t hb h4 h5 x, seven_b2_eval_1_5_3 t hb h4 h5 x]
  all_goals ring

set_option maxHeartbeats 300000 in
lemma seven_b2_eval_2_3_1 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K) :
    sevenCoefficientAt t x 2 3 1 = ((-36) * t.c₃) * x 1 + (36 * t.c₂) * x 3 + (24 * t.c₁) * x 4 + (24 * t.b₂ * t.c₃) * x 5 + (((-240) * (t.b₁ ^ 2)) + ((-240) * t.b₀ * t.b₂) + ((-90) * t.b₁ * t.c₃) + (360 * t.b₂ * t.c₂)) * x 6 + (((-1200) * t.b₀ * t.b₁) + ((-1080) * t.b₀ * t.c₃) + ((-240) * t.b₁ * t.c₂) + (240 * t.b₂ * t.c₁)) * x 7 + ((3360 * (t.c₂ ^ 2)) + (30240 * (t.b₀ ^ 2)) + ((-560) * t.b₀ * (t.b₂ ^ 2)) + ((-560) * t.b₂ * (t.b₁ ^ 2)) + (4200 * t.c₁ * t.c₃) + (6720 * t.b₁ * t.c₁) + (35280 * t.b₀ * t.c₂)) * x 8 + ((1680 * t.c₁ * t.c₂) + (5040 * t.b₀ * t.c₁) + ((-700) * t.b₀ * t.b₁ * t.b₂)) * x 9 + ((80 * (t.b₁ ^ 3)) + (80 * t.c₃ * (t.b₁ ^ 2)) + (80 * t.b₀ * t.b₂ * t.c₃) + (280 * t.b₀ * t.b₁ * t.b₂)) * x 10 + (((-5040) * t.b₁ * (t.b₀ ^ 2)) + ((-5040) * t.c₃ * (t.b₀ ^ 2)) + ((-1260) * t.c₁ * (t.b₁ ^ 2)) + ((-5880) * t.b₀ * t.b₁ * t.c₂) + ((-5880) * t.b₀ * t.c₂ * t.c₃) + ((-1680) * t.b₀ * t.b₂ * t.c₁) + ((-1260) * t.b₁ * t.c₁ * t.c₃)) * x 11 + ((8400 * t.b₁ * (t.c₁ ^ 2)) + (8400 * t.c₃ * (t.c₁ ^ 2)) + ((-8400) * t.b₁ * t.b₂ * (t.b₀ ^ 2)) + ((-8400) * t.b₂ * t.c₃ * (t.b₀ ^ 2))) * x 12 := by
  rw [sevenCoefficientAt_succ]
  norm_num only [coefficientBracket, coeffDq, coeffDP, coeffQ, coeffP, hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, sub_zero, zero_sub, false_and, and_false, true_and, and_true, if_true, if_false]
  simp only [seven_b2_eval_1_0_2 t hb h4 h5 x, seven_b2_eval_1_0_3 t hb h4 h5 x, seven_b2_eval_1_0_4 t hb h4 h5 x, seven_b2_eval_1_0_5 t hb h4 h5 x, seven_b2_eval_1_0_6 t hb h4 h5 x, seven_b2_eval_1_0_7 t hb h4 h5 x, seven_b2_eval_1_0_8 t hb h4 h5 x, seven_b2_eval_1_1_1 t hb h4 h5 x, seven_b2_eval_1_1_2 t hb h4 h5 x, seven_b2_eval_1_1_3 t hb h4 h5 x, seven_b2_eval_1_1_4 t hb h4 h5 x, seven_b2_eval_1_1_5 t hb h4 h5 x, seven_b2_eval_1_1_6 t hb h4 h5 x, seven_b2_eval_1_1_7 t hb h4 h5 x, seven_b2_eval_1_2_0 t hb h4 h5 x, seven_b2_eval_1_2_1 t hb h4 h5 x, seven_b2_eval_1_2_2 t hb h4 h5 x, seven_b2_eval_1_2_3 t hb h4 h5 x, seven_b2_eval_1_2_4 t hb h4 h5 x, seven_b2_eval_1_2_5 t hb h4 h5 x, seven_b2_eval_1_2_6 t hb h4 h5 x, seven_b2_eval_1_3_0 t hb h4 h5 x, seven_b2_eval_1_3_1 t hb h4 h5 x, seven_b2_eval_1_3_2 t hb h4 h5 x, seven_b2_eval_1_3_3 t hb h4 h5 x, seven_b2_eval_1_3_4 t hb h4 h5 x, seven_b2_eval_1_3_5 t hb h4 h5 x, seven_b2_eval_1_4_1 t hb h4 h5 x, seven_b2_eval_1_4_2 t hb h4 h5 x, seven_b2_eval_1_4_3 t hb h4 h5 x, seven_b2_eval_1_5_1 t hb h4 h5 x, seven_b2_eval_1_5_2 t hb h4 h5 x, seven_b2_eval_1_5_3 t hb h4 h5 x]
  all_goals ring

set_option maxHeartbeats 300000 in
lemma seven_b2_eval_2_4_1 (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (x : Fin 13 → K) :
    sevenCoefficientAt t x 2 4 1 = (54 * t.c₃) * x 3 + (48 * t.c₂) * x 4 + (((-540) * t.c₁) + ((-300) * t.b₁ * t.b₂) + (450 * t.b₂ * t.c₃)) * x 6 + (((-540) * (t.b₁ ^ 2)) + ((-840) * t.b₀ * t.b₂) + ((-540) * t.b₁ * t.c₃) + (360 * t.b₂ * t.c₂)) * x 7 + (((-5880) * t.b₂ * t.c₁) + ((-700) * t.b₁ * (t.b₂ ^ 2)) + (8400 * t.c₂ * t.c₃) + (18480 * t.b₁ * t.c₂) + (52920 * t.b₀ * t.b₁) + (60480 * t.b₀ * t.c₃)) * x 8 + ((1680 * (t.c₂ ^ 2)) + (7560 * (t.b₀ ^ 2)) + ((-490) * t.b₀ * (t.b₂ ^ 2)) + ((-315) * t.b₂ * (t.b₁ ^ 2)) + (2310 * t.c₁ * t.c₃) + (2940 * t.b₁ * t.c₁) + (11340 * t.b₀ * t.c₂)) * x 9 + ((140 * t.b₀ * (t.b₂ ^ 2)) + (180 * t.b₁ * t.c₁) + (180 * t.c₁ * t.c₃) + (190 * t.b₂ * (t.b₁ ^ 2)) + (100 * t.b₁ * t.b₂ * t.c₃)) * x 10 + (((-10080) * t.b₀ * (t.c₃ ^ 2)) + ((-8820) * t.b₀ * (t.b₁ ^ 2)) + ((-3360) * t.c₂ * (t.b₁ ^ 2)) + ((-2520) * t.b₂ * (t.b₀ ^ 2)) + ((-18900) * t.b₀ * t.b₁ * t.c₃) + ((-3780) * t.b₀ * t.b₂ * t.c₂) + ((-3360) * t.b₁ * t.c₂ * t.c₃) + ((-420) * t.b₁ * t.b₂ * t.c₁) + (630 * t.b₂ * t.c₁ * t.c₃)) * x 11 + (((-4200) * (t.b₀ ^ 2) * (t.b₂ ^ 2)) + (4200 * t.b₂ * (t.c₁ ^ 2)) + ((-14700) * t.b₀ * t.b₂ * (t.b₁ ^ 2)) + (33600 * t.b₁ * t.c₁ * t.c₂) + (33600 * t.c₁ * t.c₂ * t.c₃) + (75600 * t.b₀ * t.b₁ * t.c₁) + (75600 * t.b₀ * t.c₁ * t.c₃) + ((-14700) * t.b₀ * t.b₁ * t.b₂ * t.c₃)) * x 12 := by
  rw [sevenCoefficientAt_succ]
  norm_num only [coefficientBracket, coeffDq, coeffDP, coeffQ, coeffP, hb, h4, h5, mul_zero, zero_mul, add_zero, zero_add, sub_zero, zero_sub, false_and, and_false, true_and, and_true, if_true, if_false]
  simp only [seven_b2_eval_1_0_2 t hb h4 h5 x, seven_b2_eval_1_0_3 t hb h4 h5 x, seven_b2_eval_1_0_4 t hb h4 h5 x, seven_b2_eval_1_0_5 t hb h4 h5 x, seven_b2_eval_1_0_6 t hb h4 h5 x, seven_b2_eval_1_0_7 t hb h4 h5 x, seven_b2_eval_1_0_8 t hb h4 h5 x, seven_b2_eval_1_1_1 t hb h4 h5 x, seven_b2_eval_1_1_2 t hb h4 h5 x, seven_b2_eval_1_1_3 t hb h4 h5 x, seven_b2_eval_1_1_4 t hb h4 h5 x, seven_b2_eval_1_1_5 t hb h4 h5 x, seven_b2_eval_1_1_6 t hb h4 h5 x, seven_b2_eval_1_1_7 t hb h4 h5 x, seven_b2_eval_1_2_0 t hb h4 h5 x, seven_b2_eval_1_2_1 t hb h4 h5 x, seven_b2_eval_1_2_2 t hb h4 h5 x, seven_b2_eval_1_2_3 t hb h4 h5 x, seven_b2_eval_1_2_4 t hb h4 h5 x, seven_b2_eval_1_2_5 t hb h4 h5 x, seven_b2_eval_1_2_6 t hb h4 h5 x, seven_b2_eval_1_3_0 t hb h4 h5 x, seven_b2_eval_1_3_1 t hb h4 h5 x, seven_b2_eval_1_3_2 t hb h4 h5 x, seven_b2_eval_1_3_3 t hb h4 h5 x, seven_b2_eval_1_3_4 t hb h4 h5 x, seven_b2_eval_1_3_5 t hb h4 h5 x, seven_b2_eval_1_4_1 t hb h4 h5 x, seven_b2_eval_1_4_2 t hb h4 h5 x, seven_b2_eval_1_4_3 t hb h4 h5 x, seven_b2_eval_1_5_1 t hb h4 h5 x, seven_b2_eval_1_5_2 t hb h4 h5 x, seven_b2_eval_1_5_3 t hb h4 h5 x]
  all_goals ring

end SexticC3.CubeLeading.Polynomial
