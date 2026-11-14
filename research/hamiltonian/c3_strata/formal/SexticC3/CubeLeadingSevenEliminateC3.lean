import SexticC3.CubeLeadingSevenRowsC3

/-! Generated exact triangular elimination. Every polynomial identity is
replayed by Lean, and each pivot is a power of the stated nonzero parameter. -/
noncomputable section
set_option linter.unusedSectionVars false
namespace SexticC3.CubeLeading.Polynomial
open MvPolynomial
variable {K : Type*} [Field K] [CharZero K]

set_option maxHeartbeats 4000000 in
lemma seven_c3_coordinates_zero (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (hb2 : t.b₂ = 0) (ht : t.c₃ ≠ 0) (x : Fin 13 → K)
    (hf : ∀ n : ℕ, Static t.toGateParameters ((bracket (hamiltonian t))^[n] (sevenCombination t x))) :
    x = 0 := by
  have e0 := seven_c3_row_0 t hb h4 h5 hb2 x (hf 1)
  have e1 := seven_c3_row_1 t hb h4 h5 hb2 x (hf 1)
  have e2 := seven_c3_row_2 t hb h4 h5 hb2 x (hf 1)
  have e3 := seven_c3_row_3 t hb h4 h5 hb2 x (hf 1)
  have e4 := seven_c3_row_4 t hb h4 h5 hb2 x (hf 1)
  have e5 := seven_c3_row_5 t hb h4 h5 hb2 x (hf 1)
  have e6 := seven_c3_row_6 t hb h4 h5 hb2 x (hf 1)
  have e7 := seven_c3_row_7 t hb h4 h5 hb2 x (hf 1)
  have e8 := seven_c3_row_8 t hb h4 h5 hb2 x (hf 1)
  have e9 := seven_c3_row_9 t hb h4 h5 hb2 x (hf 1)
  have e10 := seven_c3_row_10 t hb h4 h5 hb2 x (hf 2)
  have e11 := seven_c3_row_11 t hb h4 h5 hb2 x (hf 2)
  have e12 := seven_c3_row_12 t hb h4 h5 hb2 x (hf 1)
  have e13 := seven_c3_row_13 t hb h4 h5 hb2 x (hf 1)
  have z0 : 1 * x 9 = 0 := by
    linear_combination (1 / 816480) * e0
  have z1 : 1 * x 7 + ((-7 / 6) * t.c₂) * x 11 = 0 := by
    linear_combination (-1 / 540) * e1
  have z2 : 1 * x 8 + (((-7 / 54) * t.c₃) + ((-1 / 6) * t.b₁)) * x 11 = 0 := by
    linear_combination (1 / 1632960) * e2
  have z3 : t.c₃ * x 11 = 0 := by
    linear_combination (1 / 161280) * e3 + 27 * z2
  have z4 : t.c₃ * x 3 = 0 := by
    linear_combination ((1 / 432) * t.c₃) * e4 + ((35 / 3) * t.c₁ * t.c₃) * z0 + (((-20) * (t.c₃ ^ 2)) + ((-20) * t.b₁ * t.c₃)) * z1 + ((560 / 3) * t.c₂ * t.c₃) * z2 + (((-2765 / 81) * t.c₂ * t.c₃) + ((-245 / 9) * t.b₁ * t.c₂)) * z3
  have z5 : 1 * x 4 + ((-15 / 4) * t.c₂) * x 10 = 0 := by
    linear_combination (-1 / 576) * e5 + ((35 / 8) * t.c₂) * z0 + (((105 / 2) * t.c₃) + ((315 / 4) * t.b₁)) * z2 + (((35 / 6) * t.b₁) + ((245 / 36) * t.c₃)) * z3
  have z6 : (t.c₃ ^ 2) * x 5 + ((-30) * t.c₂ * t.c₃) * x 6 + (((85 / 4) * t.c₂ * (t.c₃ ^ 2)) + ((35 / 2) * t.b₁ * t.c₂ * t.c₃)) * x 10 = 0 := by
    linear_combination ((1 / 72) * t.c₃) * e6 + (10 * t.c₁ * t.c₃) * z1 + ((70 * t.b₁ * (t.c₃ ^ 2)) + (70 * t.c₃ * (t.b₁ ^ 2))) * z2 + (((35 / 3) * (t.b₁ ^ 3)) + ((35 / 3) * t.c₁ * t.c₂) + ((245 / 27) * t.b₁ * (t.c₃ ^ 2)) + ((560 / 27) * t.c₃ * (t.b₁ ^ 2))) * z3 + (((-3) * (t.c₃ ^ 2)) + ((-2) * t.b₁ * t.c₃)) * z5
  have z7 : t.c₃ * x 1 + (((-45 / 4) * (t.c₃ ^ 2)) + ((-15) * t.b₁ * t.c₃)) * x 6 + ((5 * t.b₁ * (t.c₃ ^ 2)) + (5 * t.c₃ * (t.b₁ ^ 2))) * x 10 = 0 := by
    linear_combination ((-1 / 144) * t.c₃) * e7 + (5 * t.c₂ * t.c₃) * z1 + ((-35) * t.c₁ * t.c₃) * z2 + (((35 / 6) * (t.c₂ ^ 2)) + ((-245 / 54) * t.c₁ * t.c₃) + ((-35 / 6) * t.b₁ * t.c₁)) * z3
  have z8 : 1 * x 6 + (((-5 / 24) * t.c₃) + ((-1 / 3) * t.b₁)) * x 10 + (((35 / 12) * t.b₁ * t.c₂) + ((35 / 12) * t.c₂ * t.c₃)) * x 12 = 0 := by
    linear_combination (1 / 51840) * e8 + (((-35 / 48) * t.c₃) + ((-7 / 8) * t.b₁)) * z0
  have z9 : t.c₃ * x 10 + (((-2590 / 9) * t.b₁ * t.c₂) + ((-2590 / 9) * t.c₂ * t.c₃)) * x 12 = 0 := by
    linear_combination (1 / 3240) * e9 + (((532 / 9) * t.b₁) + ((742 / 9) * t.c₃)) * z0 + 8 * z8
  have z10 : (t.c₃ ^ 2) * x 2 + (((1925 / 2) * t.c₂ * (t.c₃ ^ 4)) + ((-71225 / 54) * t.b₁ * t.c₁ * (t.c₂ ^ 2)) + ((-71225 / 54) * t.c₁ * t.c₃ * (t.c₂ ^ 2)) + ((-6475 / 18) * t.c₂ * t.c₃ * (t.b₁ ^ 3)) + ((6125 / 36) * t.c₂ * (t.b₁ ^ 2) * (t.c₃ ^ 2)) + ((53725 / 36) * t.b₁ * t.c₂ * (t.c₃ ^ 3))) * x 12 = 0 := by
    linear_combination ((-1 / 432) * t.c₃) * e10 + (((70 / 3) * t.b₀ * t.c₁ * t.c₃) + ((70 / 3) * t.c₁ * t.c₂ * t.c₃)) * z0 + (((-35) * t.b₀ * (t.c₃ ^ 2)) + ((-40) * t.b₀ * t.b₁ * t.c₃) + ((-10 / 3) * t.b₁ * t.c₂ * t.c₃)) * z1 + ((245 * t.c₁ * (t.c₃ ^ 2)) + ((140 / 3) * t.c₃ * (t.c₂ ^ 2)) + (350 * t.b₀ * t.c₂ * t.c₃) + (350 * t.b₁ * t.c₁ * t.c₃)) * z2 + (((-35 / 3) * t.c₁ * (t.b₁ ^ 2)) + ((35 / 9) * t.b₁ * (t.c₂ ^ 2)) + ((490 / 81) * t.c₃ * (t.c₂ ^ 2)) + ((1715 / 54) * t.c₁ * (t.c₃ ^ 2)) + ((-3535 / 54) * t.b₀ * t.c₂ * t.c₃) + ((-175 / 3) * t.b₀ * t.b₁ * t.c₂) + ((875 / 54) * t.b₁ * t.c₁ * t.c₃)) * z3 + (((-2) * t.b₀) + ((-7 / 6) * t.c₂)) * z4 + ((-7 / 3) * t.c₁ * t.c₃) * z5 + (((-3 / 2) * t.c₃) + ((-2 / 3) * t.b₁)) * z7 + (((-135 / 8) * (t.c₃ ^ 3)) + ((-75 / 4) * t.b₁ * (t.c₃ ^ 2))) * z8 + (((-225 / 64) * (t.c₃ ^ 3)) + ((-65 / 32) * t.b₁ * (t.c₃ ^ 2)) + ((5 / 4) * t.c₃ * (t.b₁ ^ 2)) + ((55 / 12) * t.c₁ * t.c₂)) * z9
  have z11 : (t.c₃ ^ 2) * x 0 + (((12950 / 3) * (t.b₁ ^ 3) * (t.c₂ ^ 2)) + ((63875 / 6) * (t.c₂ ^ 2) * (t.c₃ ^ 3)) + (25025 * t.b₁ * (t.c₂ ^ 2) * (t.c₃ ^ 2)) + ((112175 / 6) * t.c₃ * (t.b₁ ^ 2) * (t.c₂ ^ 2)) + ((235900 / 27) * t.b₀ * t.c₂ * (t.c₃ ^ 3)) + ((151900 / 27) * t.b₀ * t.c₂ * t.c₃ * (t.b₁ ^ 2)) + ((387800 / 27) * t.b₀ * t.b₁ * t.c₂ * (t.c₃ ^ 2))) * x 12 = 0 := by
    linear_combination ((-1 / 216) * t.c₃) * e11 + (((-140 / 3) * t.c₃ * (t.c₁ ^ 2)) + ((140 / 3) * t.b₀ * t.b₁ * (t.c₃ ^ 2)) + ((140 / 3) * t.b₀ * t.c₃ * (t.b₁ ^ 2))) * z0 + ((70 * t.c₁ * (t.c₃ ^ 2)) + ((80 / 3) * t.c₃ * (t.c₂ ^ 2)) + ((220 / 3) * t.b₁ * t.c₁ * t.c₃) + ((260 / 3) * t.b₀ * t.c₂ * t.c₃)) * z1 + (((140 / 3) * t.c₃ * (t.b₁ ^ 3)) + ((140 / 3) * (t.b₁ ^ 2) * (t.c₃ ^ 2)) + ((-840) * t.b₀ * t.c₁ * t.c₃) + ((-2800 / 3) * t.c₁ * t.c₂ * t.c₃)) * z2 + (((70 / 9) * (t.b₁ ^ 4)) + ((280 / 9) * (t.c₂ ^ 3)) + ((490 / 81) * (t.b₁ ^ 2) * (t.c₃ ^ 2)) + ((910 / 9) * t.b₀ * (t.c₂ ^ 2)) + ((1120 / 81) * t.c₃ * (t.b₁ ^ 3)) + (70 * t.b₁ * t.c₁ * t.c₂) + ((280 / 9) * t.b₀ * t.c₁ * t.c₃) + ((8155 / 81) * t.c₁ * t.c₂ * t.c₃)) * z3 + t.c₁ * z4 + (((-3) * t.b₁ * (t.c₃ ^ 2)) + ((-4 / 3) * t.c₃ * (t.b₁ ^ 2))) * z5 + ((3 * t.c₃) + ((4 / 3) * t.b₁)) * z6 + ((-4 / 3) * t.c₂) * z7 + ((135 * t.c₂ * (t.c₃ ^ 2)) + (200 * t.b₀ * (t.c₃ ^ 2)) + (120 * t.b₀ * t.b₁ * t.c₃) + (120 * t.b₁ * t.c₂ * t.c₃)) * z8 + (((-15) * t.c₂ * (t.b₁ ^ 2)) + ((-285 / 8) * t.c₂ * (t.c₃ ^ 2)) + ((-85 / 3) * t.b₀ * (t.c₃ ^ 2)) + ((-195 / 4) * t.b₁ * t.c₂ * t.c₃) + ((-55 / 3) * t.b₀ * t.b₁ * t.c₃)) * z9
  have z12 : t.c₃ * x 12 = 0 := by
    linear_combination (1 / 10206000) * (27*e12+4*e13)
  have v12 : x 12 = 0 := by
    have hp : t.c₃ * x 12 = 0 := by
      simpa only [mul_zero, add_zero, zero_add] using z12
    exact (mul_eq_zero.mp hp).resolve_left ht
  have v0 : x 0 = 0 := by
    have hp : (t.c₃ ^ 2) * x 0 = 0 := by
      simpa only [v12, mul_zero, add_zero, zero_add] using z11
    exact (mul_eq_zero.mp hp).resolve_left (pow_ne_zero 2 ht)
  have v2 : x 2 = 0 := by
    have hp : (t.c₃ ^ 2) * x 2 = 0 := by
      simpa only [v12, v0, mul_zero, add_zero, zero_add] using z10
    exact (mul_eq_zero.mp hp).resolve_left (pow_ne_zero 2 ht)
  have v10 : x 10 = 0 := by
    have hp : t.c₃ * x 10 = 0 := by
      simpa only [v12, v0, v2, mul_zero, add_zero, zero_add] using z9
    exact (mul_eq_zero.mp hp).resolve_left ht
  have v6 : x 6 = 0 := by
    have hp : 1 * x 6 = 0 := by
      simpa only [v12, v0, v2, v10, mul_zero, add_zero, zero_add] using z8
    simpa using hp
  have v1 : x 1 = 0 := by
    have hp : t.c₃ * x 1 = 0 := by
      simpa only [v12, v0, v2, v10, v6, mul_zero, add_zero, zero_add] using z7
    exact (mul_eq_zero.mp hp).resolve_left ht
  have v5 : x 5 = 0 := by
    have hp : (t.c₃ ^ 2) * x 5 = 0 := by
      simpa only [v12, v0, v2, v10, v6, v1, mul_zero, add_zero, zero_add] using z6
    exact (mul_eq_zero.mp hp).resolve_left (pow_ne_zero 2 ht)
  have v4 : x 4 = 0 := by
    have hp : 1 * x 4 = 0 := by
      simpa only [v12, v0, v2, v10, v6, v1, v5, mul_zero, add_zero, zero_add] using z5
    simpa using hp
  have v3 : x 3 = 0 := by
    have hp : t.c₃ * x 3 = 0 := by
      simpa only [v12, v0, v2, v10, v6, v1, v5, v4, mul_zero, add_zero, zero_add] using z4
    exact (mul_eq_zero.mp hp).resolve_left ht
  have v11 : x 11 = 0 := by
    have hp : t.c₃ * x 11 = 0 := by
      simpa only [v12, v0, v2, v10, v6, v1, v5, v4, v3, mul_zero, add_zero, zero_add] using z3
    exact (mul_eq_zero.mp hp).resolve_left ht
  have v8 : x 8 = 0 := by
    have hp : 1 * x 8 = 0 := by
      simpa only [v12, v0, v2, v10, v6, v1, v5, v4, v3, v11, mul_zero, add_zero, zero_add] using z2
    simpa using hp
  have v7 : x 7 = 0 := by
    have hp : 1 * x 7 = 0 := by
      simpa only [v12, v0, v2, v10, v6, v1, v5, v4, v3, v11, v8, mul_zero, add_zero, zero_add] using z1
    simpa using hp
  have v9 : x 9 = 0 := by
    have hp : 1 * x 9 = 0 := by
      simpa only [v12, v0, v2, v10, v6, v1, v5, v4, v3, v11, v8, v7, mul_zero, add_zero, zero_add] using z0
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
