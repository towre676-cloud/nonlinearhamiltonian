import SexticC3.CubeLeadingSevenRowsC2

/-! Generated exact triangular elimination. Every polynomial identity is
replayed by Lean, and each pivot is a power of the stated nonzero parameter. -/
noncomputable section
set_option linter.unusedSectionVars false
namespace SexticC3.CubeLeading.Polynomial
open MvPolynomial
variable {K : Type*} [Field K] [CharZero K]

set_option maxHeartbeats 4000000 in
lemma seven_c2_coordinates_zero (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (hb2 : t.b₂ = 0) (hc3 : t.c₃ = 0) (ht : t.c₂ ≠ 0) (x : Fin 13 → K)
    (hf : ∀ n : ℕ, Static t.toGateParameters ((bracket (hamiltonian t))^[n] (sevenCombination t x))) :
    x = 0 := by
  have e0 := seven_c2_row_0 t hb h4 h5 hb2 hc3 x (hf 1)
  have e1 := seven_c2_row_1 t hb h4 h5 hb2 hc3 x (hf 1)
  have e2 := seven_c2_row_2 t hb h4 h5 hb2 hc3 x (hf 1)
  have e3 := seven_c2_row_3 t hb h4 h5 hb2 hc3 x (hf 1)
  have e4 := seven_c2_row_4 t hb h4 h5 hb2 hc3 x (hf 1)
  have e5 := seven_c2_row_5 t hb h4 h5 hb2 hc3 x (hf 1)
  have e6 := seven_c2_row_6 t hb h4 h5 hb2 hc3 x (hf 1)
  have e7 := seven_c2_row_7 t hb h4 h5 hb2 hc3 x (hf 1)
  have e8 := seven_c2_row_8 t hb h4 h5 hb2 hc3 x (hf 1)
  have e9 := seven_c2_row_9 t hb h4 h5 hb2 hc3 x (hf 1)
  have e10 := seven_c2_row_10 t hb h4 h5 hb2 hc3 x (hf 1)
  have e11 := seven_c2_row_11 t hb h4 h5 hb2 hc3 x (hf 2)
  have e12 := seven_c2_row_12 t hb h4 h5 hb2 hc3 x (hf 3)
  have z0 : 1 * x 9 = 0 := by
    linear_combination (1 / 816480) * e0
  have z1 : t.c₂ * x 12 = 0 := by
    linear_combination (1 / 126000) * e1 + (8 / 25) * z0
  have z2 : t.c₂ * x 7 = 0 := by
    linear_combination ((1 / 103680) * t.c₂) * e2 + ((-105 / 8) * (t.b₁ ^ 2)) * z1
  have z3 : (t.c₂ ^ 2) * x 11 = 0 := by
    linear_combination ((1 / 20160) * t.c₂) * e3 + ((5 / 2) * (t.b₁ ^ 2)) * z1 + (9 / 14) * z2
  have z4 : (t.c₂ ^ 2) * x 8 = 0 := by
    linear_combination ((1 / 1632960) * (t.c₂ ^ 2)) * e4 + ((1 / 6) * t.b₁) * z3
  have z5 : t.c₂ * x 3 = 0 := by
    linear_combination ((1 / 432) * t.c₂) * e5 + ((35 / 3) * t.c₁ * t.c₂) * z0 + ((-20) * t.b₁) * z2 + ((-35) * t.b₁) * z3 + (560 / 3) * z4
  have z6 : (t.c₂ ^ 2) * x 4 = 0 := by
    linear_combination ((1 / 864) * (t.c₂ ^ 2)) * e6 + ((105 / 2) * (t.c₂ ^ 3)) * z0 + (175 * t.b₁ * t.c₁ * t.c₂) * z1 + ((-105) * (t.b₁ ^ 2)) * z3 + (665 * t.b₁) * z4
  have z7 : (t.c₂ ^ 3) * x 10 = 0 := by
    linear_combination ((1 / 2160) * (t.c₂ ^ 2)) * e7 + ((-7 / 6) * (t.c₂ ^ 3)) * z0 + ((7 / 2) * (t.b₁ ^ 2)) * z3 + ((-21) * t.b₁) * z4 + (4 / 15) * z6
  have z8 : (t.c₂ ^ 3) * x 6 = 0 := by
    linear_combination ((-1 / 2160) * (t.c₂ ^ 2)) * e8 + ((-1 / 3) * t.c₁ * t.c₂) * z2 + ((-7 / 3) * (t.b₁ ^ 2)) * z4 + ((1 / 15) * t.b₁) * z6 + ((1 / 3) * t.b₁) * z7
  have z9 : (t.c₂ ^ 4) * x 5 = 0 := by
    linear_combination ((1 / 24) * (t.c₂ ^ 3)) * e9 + ((-3 / 2) * t.b₁ * (t.c₂ ^ 2)) * z5 + ((-1) * (t.c₂ ^ 2)) * z6 + ((15 / 2) * t.c₁) * z8
  have z10 : (t.c₂ ^ 3) * x 1 = 0 := by
    linear_combination ((-1 / 144) * (t.c₂ ^ 3)) * e10 + (5 * (t.c₂ ^ 3)) * z2 + ((-35) * t.c₁ * t.c₂) * z4 + ((-5) * (t.b₁ ^ 2)) * z7 + (15 * t.b₁) * z8
  have z11 : (t.c₂ ^ 4) * x 0 = 0 := by
    linear_combination ((-1 / 72) * (t.c₂ ^ 3)) * e11 + ((20 * t.c₁ * (t.c₂ ^ 3)) + (20 * t.b₀ * t.c₁ * (t.c₂ ^ 2))) * z2 + (((-140) * t.c₂ * (t.c₁ ^ 2)) + (140 * t.b₀ * t.c₂ * (t.b₁ ^ 2))) * z4 + (((-4 / 3) * t.b₁ * (t.c₂ ^ 2)) + ((-4) * t.b₀ * t.b₁ * t.c₂)) * z6 + (((-20) * t.c₁ * (t.b₁ ^ 2)) + ((-20) * t.b₀ * t.b₁ * t.c₂)) * z7 + ((10 * (t.c₂ ^ 2)) + (50 * t.b₁ * t.c₁) + (55 * t.b₀ * t.c₂)) * z8 + ((5 / 3) * t.b₁) * z9 + ((-1) * t.c₁) * z10
  have z12 : (t.c₂ ^ 5) * x 2 = 0 := by
    linear_combination ((-1 / 144) * (t.c₂ ^ 3)) * e12 + ((105 * (t.c₁ ^ 2) * (t.c₂ ^ 4)) + ((-105) * (t.b₀ ^ 2) * (t.b₁ ^ 2) * (t.c₂ ^ 3)) + (210 * t.b₀ * (t.c₁ ^ 2) * (t.c₂ ^ 3))) * z0 + (((-180) * (t.b₀ ^ 2) * (t.c₂ ^ 3)) + ((-90) * t.b₀ * (t.c₂ ^ 4)) + ((-45) * t.b₁ * t.c₁ * (t.c₂ ^ 3)) + ((-315) * t.b₀ * t.b₁ * t.c₁ * (t.c₂ ^ 2))) * z2 + (((-315) * t.c₂ * (t.b₁ ^ 2) * (t.c₁ ^ 2)) + ((-630) * t.b₀ * t.b₁ * t.c₁ * (t.c₂ ^ 2)) + ((-315) * t.b₁ * t.c₁ * t.c₂ * (t.b₀ ^ 2))) * z3 + ((420 * t.c₁ * (t.c₂ ^ 3)) + ((-105) * t.b₀ * t.c₂ * (t.b₁ ^ 3)) + (1365 * t.b₁ * t.c₂ * (t.c₁ ^ 2)) + (1890 * t.c₁ * t.c₂ * (t.b₀ ^ 2)) + (3780 * t.b₀ * t.c₁ * (t.c₂ ^ 2))) * z4 + (((-3 / 2) * t.c₁ * (t.c₂ ^ 3)) + ((9 / 4) * (t.b₁ ^ 3) * (t.c₂ ^ 2)) + ((-9 / 2) * t.b₀ * t.c₁ * (t.c₂ ^ 2))) * z5 + (((-3) * t.c₂ * (t.c₁ ^ 2)) + ((13 / 6) * (t.b₁ ^ 2) * (t.c₂ ^ 2)) + (3 * t.b₀ * t.c₂ * (t.b₁ ^ 2))) * z6 + (((-15) * t.c₁ * (t.b₁ ^ 3)) + (30 * t.c₂ * (t.c₁ ^ 2)) + (90 * (t.b₀ ^ 2) * (t.b₁ ^ 2)) + (105 * t.b₀ * t.c₂ * (t.b₁ ^ 2))) * z7 + (((-270) * t.b₁ * (t.b₀ ^ 2)) + ((-15) * t.b₁ * (t.c₂ ^ 2)) + ((115 / 4) * t.c₁ * (t.b₁ ^ 2)) + ((-330) * t.b₀ * t.b₁ * t.c₂)) * z8 + ((19 / 6) * (t.b₁ ^ 2)) * z9 + (((-2) * (t.c₂ ^ 2)) + ((-4) * t.b₁ * t.c₁) + (4 * t.b₀ * t.c₂)) * z10 + ((-2) * t.b₁) * z11
  have v2 : x 2 = 0 := by
    have hp : (t.c₂ ^ 5) * x 2 = 0 := by
      simpa only [mul_zero, add_zero, zero_add] using z12
    exact (mul_eq_zero.mp hp).resolve_left (pow_ne_zero 5 ht)
  have v0 : x 0 = 0 := by
    have hp : (t.c₂ ^ 4) * x 0 = 0 := by
      simpa only [v2, mul_zero, add_zero, zero_add] using z11
    exact (mul_eq_zero.mp hp).resolve_left (pow_ne_zero 4 ht)
  have v1 : x 1 = 0 := by
    have hp : (t.c₂ ^ 3) * x 1 = 0 := by
      simpa only [v2, v0, mul_zero, add_zero, zero_add] using z10
    exact (mul_eq_zero.mp hp).resolve_left (pow_ne_zero 3 ht)
  have v5 : x 5 = 0 := by
    have hp : (t.c₂ ^ 4) * x 5 = 0 := by
      simpa only [v2, v0, v1, mul_zero, add_zero, zero_add] using z9
    exact (mul_eq_zero.mp hp).resolve_left (pow_ne_zero 4 ht)
  have v6 : x 6 = 0 := by
    have hp : (t.c₂ ^ 3) * x 6 = 0 := by
      simpa only [v2, v0, v1, v5, mul_zero, add_zero, zero_add] using z8
    exact (mul_eq_zero.mp hp).resolve_left (pow_ne_zero 3 ht)
  have v10 : x 10 = 0 := by
    have hp : (t.c₂ ^ 3) * x 10 = 0 := by
      simpa only [v2, v0, v1, v5, v6, mul_zero, add_zero, zero_add] using z7
    exact (mul_eq_zero.mp hp).resolve_left (pow_ne_zero 3 ht)
  have v4 : x 4 = 0 := by
    have hp : (t.c₂ ^ 2) * x 4 = 0 := by
      simpa only [v2, v0, v1, v5, v6, v10, mul_zero, add_zero, zero_add] using z6
    exact (mul_eq_zero.mp hp).resolve_left (pow_ne_zero 2 ht)
  have v3 : x 3 = 0 := by
    have hp : t.c₂ * x 3 = 0 := by
      simpa only [v2, v0, v1, v5, v6, v10, v4, mul_zero, add_zero, zero_add] using z5
    exact (mul_eq_zero.mp hp).resolve_left ht
  have v8 : x 8 = 0 := by
    have hp : (t.c₂ ^ 2) * x 8 = 0 := by
      simpa only [v2, v0, v1, v5, v6, v10, v4, v3, mul_zero, add_zero, zero_add] using z4
    exact (mul_eq_zero.mp hp).resolve_left (pow_ne_zero 2 ht)
  have v11 : x 11 = 0 := by
    have hp : (t.c₂ ^ 2) * x 11 = 0 := by
      simpa only [v2, v0, v1, v5, v6, v10, v4, v3, v8, mul_zero, add_zero, zero_add] using z3
    exact (mul_eq_zero.mp hp).resolve_left (pow_ne_zero 2 ht)
  have v7 : x 7 = 0 := by
    have hp : t.c₂ * x 7 = 0 := by
      simpa only [v2, v0, v1, v5, v6, v10, v4, v3, v8, v11, mul_zero, add_zero, zero_add] using z2
    exact (mul_eq_zero.mp hp).resolve_left ht
  have v12 : x 12 = 0 := by
    have hp : t.c₂ * x 12 = 0 := by
      simpa only [v2, v0, v1, v5, v6, v10, v4, v3, v8, v11, v7, mul_zero, add_zero, zero_add] using z1
    exact (mul_eq_zero.mp hp).resolve_left ht
  have v9 : x 9 = 0 := by
    have hp : 1 * x 9 = 0 := by
      simpa only [v2, v0, v1, v5, v6, v10, v4, v3, v8, v11, v7, v12, mul_zero, add_zero, zero_add] using z0
    simpa using hp
  funext k
  fin_cases k
  · exact v0
  · exact v1
  · exact v2
  · exact v3
  · exact v4
  · exact v5
  · exact v6
  · exact v7
  · exact v8
  · exact v9
  · exact v10
  · exact v11
  · exact v12

end SexticC3.CubeLeading.Polynomial
