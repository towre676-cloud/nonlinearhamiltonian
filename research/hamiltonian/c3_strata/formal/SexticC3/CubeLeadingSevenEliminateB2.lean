import SexticC3.CubeLeadingSevenRowsB2

/-! Generated exact triangular elimination. Every polynomial identity is
replayed by Lean, and each pivot is a power of the stated nonzero parameter. -/
noncomputable section
set_option linter.unusedSectionVars false
namespace SexticC3.CubeLeading.Polynomial
open MvPolynomial
variable {K : Type*} [Field K] [CharZero K]

set_option maxHeartbeats 4000000 in
lemma seven_b2_coordinates_zero (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0) (ht : t.b₂ ≠ 0) (x : Fin 13 → K)
    (hf : ∀ n : ℕ, Static t.toGateParameters ((bracket (hamiltonian t))^[n] (sevenCombination t x))) :
    x = 0 := by
  have e0 := seven_b2_row_0 t hb h4 h5 x (hf 1)
  have e1 := seven_b2_row_1 t hb h4 h5 x (hf 1)
  have e2 := seven_b2_row_2 t hb h4 h5 x (hf 1)
  have e3 := seven_b2_row_3 t hb h4 h5 x (hf 1)
  have e4 := seven_b2_row_4 t hb h4 h5 x (hf 1)
  have e5 := seven_b2_row_5 t hb h4 h5 x (hf 1)
  have e6 := seven_b2_row_6 t hb h4 h5 x (hf 1)
  have e7 := seven_b2_row_7 t hb h4 h5 x (hf 1)
  have e8 := seven_b2_row_8 t hb h4 h5 x (hf 1)
  have e9 := seven_b2_row_9 t hb h4 h5 x (hf 1)
  have e10 := seven_b2_row_10 t hb h4 h5 x (hf 1)
  have e11 := seven_b2_row_11 t hb h4 h5 x (hf 2)
  have e12 := seven_b2_row_12 t hb h4 h5 x (hf 2)
  have z0 : t.b₂ * x 12 = 0 := by
    linear_combination (1 / 131040) * e0
  have z1 : t.b₂ * x 9 + ((-19 / 32) * (t.b₂ ^ 2)) * x 11 = 0 := by
    linear_combination ((-1 / 40320) * t.b₂) * e1 + (((5 / 8) * (t.b₂ ^ 2)) + ((25 / 8) * t.c₂)) * z0
  have z2 : (t.b₂ ^ 2) * x 11 = 0 := by
    linear_combination ((1 / 212625) * t.b₂) * e2 + ((896 / 405) * (t.b₂ ^ 2)) * z0 + (-96 / 25) * z1
  have z3 : (t.b₂ ^ 2) * x 8 = 0 := by
    linear_combination ((1 / 1632960) * (t.b₂ ^ 2)) * e3 + (((5 / 27) * t.c₃ * (t.b₂ ^ 2)) + ((70 / 243) * t.b₁ * (t.b₂ ^ 2))) * z0 + (((1 / 6) * t.b₁) + ((7 / 54) * t.c₃)) * z2
  have z4 : (t.b₂ ^ 2) * x 7 + ((-13 / 54) * (t.b₂ ^ 3)) * x 10 = 0 := by
    linear_combination ((-1 / 12960) * (t.b₂ ^ 2)) * e4 + (((-35 / 9) * t.b₂ * (t.b₁ ^ 2)) + ((-35 / 27) * t.b₀ * (t.b₂ ^ 2)) + ((35 / 27) * t.c₂ * (t.b₂ ^ 2)) + ((-35 / 9) * t.b₁ * t.b₂ * t.c₃)) * z0 + ((-35 / 108) * (t.b₂ ^ 2)) * z1 + (((14 / 9) * t.c₂) + ((455 / 3456) * (t.b₂ ^ 2))) * z2
  have z5 : (t.b₂ ^ 3) * x 10 = 0 := by
    linear_combination ((1 / 7680) * (t.b₂ ^ 2)) * e5 + (((-2835 / 16) * t.b₂ * (t.b₁ ^ 2)) + ((-2835 / 16) * t.b₂ * (t.c₃ ^ 2)) + ((-315 / 16) * t.c₂ * (t.b₂ ^ 2)) + ((-2835 / 8) * t.b₁ * t.b₂ * t.c₃)) * z0 + ((-273 / 8) * (t.b₂ ^ 2)) * z1 + ((-3087 / 256) * (t.b₂ ^ 2)) * z2 + (-27 / 2) * z4
  have z6 : (t.b₂ ^ 3) * x 4 = 0 := by
    linear_combination ((-1 / 576) * (t.b₂ ^ 3)) * e6 + ((35 / 8) * t.c₂ * (t.b₂ ^ 2)) * z1 + (((-105 / 8) * t.b₂ * (t.b₁ ^ 2)) + ((-35 / 8) * t.b₀ * (t.b₂ ^ 2)) + ((1785 / 256) * t.c₂ * (t.b₂ ^ 2)) + ((-105 / 8) * t.b₁ * t.b₂ * t.c₃)) * z2 + (((105 / 2) * t.b₂ * t.c₃) + ((315 / 4) * t.b₁ * t.b₂)) * z3 + ((-5 / 2) * (t.b₂ ^ 2)) * z4 + (((15 / 4) * t.c₂) + ((25 / 108) * (t.b₂ ^ 2))) * z5
  have z7 : (t.b₂ ^ 3) * x 6 = 0 := by
    linear_combination ((1 / 51840) * (t.b₂ ^ 3)) * e7 + (((-35 / 12) * t.b₁ * t.c₂ * (t.b₂ ^ 2)) + ((-35 / 12) * t.c₂ * t.c₃ * (t.b₂ ^ 2))) * z0 + (((-35 / 48) * t.c₃ * (t.b₂ ^ 2)) + ((-7 / 8) * t.b₁ * (t.b₂ ^ 2))) * z1 + (((455 / 1536) * t.c₃ * (t.b₂ ^ 2)) + ((1603 / 2304) * t.b₁ * (t.b₂ ^ 2))) * z2 + ((-301 / 36) * (t.b₂ ^ 2)) * z3 + (((1 / 3) * t.b₁) + ((5 / 24) * t.c₃)) * z5
  have z8 : (t.b₂ ^ 2) * x 3 = 0 := by
    linear_combination ((1 / 432) * (t.b₂ ^ 2)) * e8 + (((-70 / 9) * t.b₁ * (t.b₂ ^ 2)) + ((35 / 3) * t.b₂ * t.c₁)) * z1 + (((-35) * t.b₁ * t.c₂) + ((-35) * t.c₂ * t.c₃) + ((-665 / 144) * t.b₁ * (t.b₂ ^ 2)) + ((665 / 96) * t.b₂ * t.c₁)) * z2 + (((-560 / 9) * (t.b₂ ^ 2)) + ((560 / 3) * t.c₂)) * z3 + (((-20) * t.b₁) + ((-20) * t.c₃)) * z4 + (((50 / 27) * t.c₃) + ((200 / 27) * t.b₁)) * z5 + (-100 / 3) * z7
  have z9 : (t.b₂ ^ 3) * x 1 + ((-2 / 3) * (t.b₂ ^ 4)) * x 5 = 0 := by
    linear_combination ((-1 / 144) * (t.b₂ ^ 3)) * e9 + (((-35) * t.b₂ * t.c₁) + ((70 / 3) * t.b₁ * (t.b₂ ^ 2))) * z3 + (5 * t.b₂ * t.c₂) * z4 + (((-5) * (t.b₁ ^ 2)) + ((-5) * t.b₁ * t.c₃) + ((-5 / 3) * t.b₀ * t.b₂) + ((155 / 54) * t.b₂ * t.c₂)) * z5 + ((-1 / 2) * t.b₂) * z6 + ((15 * t.b₁) + ((45 / 4) * t.c₃)) * z7
  have z10 : (t.b₂ ^ 4) * x 2 + (((-2 / 3) * (t.b₂ ^ 5)) + (2 * t.c₂ * (t.b₂ ^ 3))) * x 5 = 0 := by
    linear_combination ((1 / 12) * (t.b₂ ^ 3)) * e10 + ((-2) * t.c₂) * z6 + ((15 * t.c₁) + ((-10) * t.b₁ * t.b₂)) * z7 + (((-3) * t.b₁ * t.b₂) + ((-3) * t.b₂ * t.c₃)) * z8 + (2 * t.b₂) * z9
  have z11 : (t.b₂ ^ 5) * x 5 = 0 := by
    linear_combination ((1 / 576) * (t.b₂ ^ 3)) * e11 + ((700 * t.b₀ * (t.b₁ ^ 2) * (t.b₂ ^ 3)) + ((-1050) * t.b₀ * t.b₁ * t.c₁ * (t.b₂ ^ 2)) + ((-1050) * t.b₀ * t.c₁ * t.c₃ * (t.b₂ ^ 2)) + ((-1050) * t.b₁ * t.c₁ * t.c₂ * (t.b₂ ^ 2)) + ((-1050) * t.c₁ * t.c₂ * t.c₃ * (t.b₂ ^ 2)) + (700 * t.b₀ * t.b₁ * t.c₃ * (t.b₂ ^ 3))) * z0 + (((-70) * (t.b₂ ^ 2) * (t.c₂ ^ 2)) + (105 * t.b₀ * (t.b₂ ^ 4)) + ((35 / 3) * (t.b₁ ^ 2) * (t.b₂ ^ 3)) + ((-280) * t.b₁ * t.c₁ * (t.b₂ ^ 2)) + ((-945 / 4) * t.c₁ * t.c₃ * (t.b₂ ^ 2)) + ((-595 / 2) * t.b₀ * t.c₂ * (t.b₂ ^ 2))) * z1 + (((-1225 / 16) * (t.b₂ ^ 2) * (t.c₂ ^ 2)) + ((665 / 96) * (t.b₁ ^ 2) * (t.b₂ ^ 3)) + ((1995 / 32) * t.b₀ * (t.b₂ ^ 4)) + (210 * t.b₂ * t.c₂ * (t.b₁ ^ 2)) + (245 * t.b₁ * t.c₁ * (t.b₂ ^ 2)) + (630 * t.b₀ * t.b₂ * (t.b₁ ^ 2)) + ((-2345 / 64) * t.b₀ * t.c₂ * (t.b₂ ^ 2)) + ((2835 / 4) * t.b₀ * t.b₂ * (t.c₃ ^ 2)) + ((12285 / 128) * t.c₁ * t.c₃ * (t.b₂ ^ 2)) + (210 * t.b₁ * t.b₂ * t.c₂ * t.c₃) + ((5355 / 4) * t.b₀ * t.b₁ * t.b₂ * t.c₃)) * z2 + (((-4305 / 2) * t.c₁ * (t.b₂ ^ 2)) + ((35 / 3) * t.b₁ * (t.b₂ ^ 3)) + ((-4200) * t.b₀ * t.b₂ * t.c₃) + ((-3990) * t.b₀ * t.b₁ * t.b₂) + ((-1295) * t.b₁ * t.b₂ * t.c₂) + ((-735) * t.b₂ * t.c₂ * t.c₃)) * z3 + ((215 * t.b₀ * (t.b₂ ^ 2)) + ((75 / 2) * t.c₂ * (t.b₂ ^ 2))) * z4 + (((-20) * (t.c₂ ^ 2)) + ((-65 / 36) * t.c₂ * (t.b₂ ^ 2)) + ((20 / 3) * t.b₂ * (t.b₁ ^ 2)) + ((45 / 2) * t.c₁ * t.c₃) + ((105 / 2) * t.b₁ * t.c₁) + ((745 / 27) * t.b₀ * (t.b₂ ^ 2)) + ((-5 / 2) * t.b₁ * t.b₂ * t.c₃)) * z5 + ((6 * t.b₀) + (7 * t.c₂) + ((5 / 4) * (t.b₂ ^ 2))) * z6 + (((-315 / 2) * t.c₁) + ((-25) * t.b₁ * t.b₂) + ((-225 / 8) * t.b₂ * t.c₃)) * z7 + ((3 / 2) * t.b₂) * z9
  have z12 : (t.b₂ ^ 7) * x 0 = 0 := by
    linear_combination ((-1 / 144) * (t.b₂ ^ 6)) * e12 + ((70 * t.b₀ * t.c₁ * (t.b₂ ^ 5)) + (70 * t.c₁ * t.c₂ * (t.b₂ ^ 5)) + ((-140 / 3) * t.b₀ * t.b₁ * (t.b₂ ^ 6))) * z1 + (((-210) * t.c₁ * (t.b₁ ^ 2) * (t.b₂ ^ 4)) + ((-665 / 24) * t.b₀ * t.b₁ * (t.b₂ ^ 6)) + ((-455 / 16) * t.b₀ * t.c₁ * (t.b₂ ^ 5)) + ((1785 / 16) * t.c₁ * t.c₂ * (t.b₂ ^ 5)) + ((-210) * t.b₀ * t.b₁ * t.c₂ * (t.b₂ ^ 4)) + ((-210) * t.b₀ * t.c₂ * t.c₃ * (t.b₂ ^ 4)) + ((-210) * t.b₁ * t.c₁ * t.c₃ * (t.b₂ ^ 4))) * z2 + ((140 * (t.b₂ ^ 4) * (t.c₂ ^ 2)) + ((-980 / 3) * t.b₀ * (t.b₂ ^ 6)) + (735 * t.c₁ * t.c₃ * (t.b₂ ^ 4)) + (1050 * t.b₀ * t.c₂ * (t.b₂ ^ 4)) + (1050 * t.b₁ * t.c₁ * (t.b₂ ^ 4))) * z3 + (((-35) * t.c₁ * (t.b₂ ^ 5)) + ((-120) * t.b₀ * t.b₁ * (t.b₂ ^ 4)) + ((-105) * t.b₀ * t.c₃ * (t.b₂ ^ 4)) + ((-10) * t.b₁ * t.c₂ * (t.b₂ ^ 4))) * z4 + (((-10) * (t.b₁ ^ 3) * (t.b₂ ^ 3)) + ((175 / 54) * t.c₁ * (t.b₂ ^ 5)) + ((-10) * t.c₃ * (t.b₁ ^ 2) * (t.b₂ ^ 3)) + (40 * t.c₁ * t.c₂ * (t.b₂ ^ 3)) + ((175 / 9) * t.b₀ * t.b₁ * (t.b₂ ^ 4)) + ((175 / 18) * t.b₀ * t.c₃ * (t.b₂ ^ 4)) + ((205 / 27) * t.b₁ * t.c₂ * (t.b₂ ^ 4))) * z5 + (((-7) * t.c₁ * (t.b₂ ^ 3)) + ((-1 / 2) * t.b₁ * (t.b₂ ^ 4))) * z6 + (((-155) * t.b₀ * (t.b₂ ^ 4)) + ((-15) * t.c₂ * (t.b₂ ^ 4)) + (30 * (t.b₁ ^ 2) * (t.b₂ ^ 3)) + ((135 / 4) * t.b₁ * t.c₃ * (t.b₂ ^ 3))) * z7 + (((-1) * (t.b₂ ^ 6)) + ((-6) * t.b₀ * (t.b₂ ^ 4)) + ((-7 / 2) * t.c₂ * (t.b₂ ^ 4))) * z8 + (((-2) * t.b₁ * (t.b₂ ^ 3)) + ((-9 / 2) * t.c₃ * (t.b₂ ^ 3))) * z9 + ((-3) * t.c₃ * (t.b₂ ^ 2)) * z10 + ((6 * t.c₂ * t.c₃) + ((-7 / 2) * t.c₃ * (t.b₂ ^ 2)) + ((8 / 3) * t.b₁ * (t.b₂ ^ 2))) * z11
  have v0 : x 0 = 0 := by
    have hp : (t.b₂ ^ 7) * x 0 = 0 := by
      simpa only [mul_zero, add_zero, zero_add] using z12
    exact (mul_eq_zero.mp hp).resolve_left (pow_ne_zero 7 ht)
  have v5 : x 5 = 0 := by
    have hp : (t.b₂ ^ 5) * x 5 = 0 := by
      simpa only [v0, mul_zero, add_zero, zero_add] using z11
    exact (mul_eq_zero.mp hp).resolve_left (pow_ne_zero 5 ht)
  have v2 : x 2 = 0 := by
    have hp : (t.b₂ ^ 4) * x 2 = 0 := by
      simpa only [v0, v5, mul_zero, add_zero, zero_add] using z10
    exact (mul_eq_zero.mp hp).resolve_left (pow_ne_zero 4 ht)
  have v1 : x 1 = 0 := by
    have hp : (t.b₂ ^ 3) * x 1 = 0 := by
      simpa only [v0, v5, v2, mul_zero, add_zero, zero_add] using z9
    exact (mul_eq_zero.mp hp).resolve_left (pow_ne_zero 3 ht)
  have v3 : x 3 = 0 := by
    have hp : (t.b₂ ^ 2) * x 3 = 0 := by
      simpa only [v0, v5, v2, v1, mul_zero, add_zero, zero_add] using z8
    exact (mul_eq_zero.mp hp).resolve_left (pow_ne_zero 2 ht)
  have v6 : x 6 = 0 := by
    have hp : (t.b₂ ^ 3) * x 6 = 0 := by
      simpa only [v0, v5, v2, v1, v3, mul_zero, add_zero, zero_add] using z7
    exact (mul_eq_zero.mp hp).resolve_left (pow_ne_zero 3 ht)
  have v4 : x 4 = 0 := by
    have hp : (t.b₂ ^ 3) * x 4 = 0 := by
      simpa only [v0, v5, v2, v1, v3, v6, mul_zero, add_zero, zero_add] using z6
    exact (mul_eq_zero.mp hp).resolve_left (pow_ne_zero 3 ht)
  have v10 : x 10 = 0 := by
    have hp : (t.b₂ ^ 3) * x 10 = 0 := by
      simpa only [v0, v5, v2, v1, v3, v6, v4, mul_zero, add_zero, zero_add] using z5
    exact (mul_eq_zero.mp hp).resolve_left (pow_ne_zero 3 ht)
  have v7 : x 7 = 0 := by
    have hp : (t.b₂ ^ 2) * x 7 = 0 := by
      simpa only [v0, v5, v2, v1, v3, v6, v4, v10, mul_zero, add_zero, zero_add] using z4
    exact (mul_eq_zero.mp hp).resolve_left (pow_ne_zero 2 ht)
  have v8 : x 8 = 0 := by
    have hp : (t.b₂ ^ 2) * x 8 = 0 := by
      simpa only [v0, v5, v2, v1, v3, v6, v4, v10, v7, mul_zero, add_zero, zero_add] using z3
    exact (mul_eq_zero.mp hp).resolve_left (pow_ne_zero 2 ht)
  have v11 : x 11 = 0 := by
    have hp : (t.b₂ ^ 2) * x 11 = 0 := by
      simpa only [v0, v5, v2, v1, v3, v6, v4, v10, v7, v8, mul_zero, add_zero, zero_add] using z2
    exact (mul_eq_zero.mp hp).resolve_left (pow_ne_zero 2 ht)
  have v9 : x 9 = 0 := by
    have hp : t.b₂ * x 9 = 0 := by
      simpa only [v0, v5, v2, v1, v3, v6, v4, v10, v7, v8, v11, mul_zero, add_zero, zero_add] using z1
    exact (mul_eq_zero.mp hp).resolve_left ht
  have v12 : x 12 = 0 := by
    have hp : t.b₂ * x 12 = 0 := by
      simpa only [v0, v5, v2, v1, v3, v6, v4, v10, v7, v8, v11, v9, mul_zero, add_zero, zero_add] using z0
    exact (mul_eq_zero.mp hp).resolve_left ht
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
