import SexticC3.CubeLeadingSevenBasis

/-! Generated scalar evaluation table, proved from the polynomial coefficients. -/
noncomputable section
set_option linter.unusedSectionVars false
namespace SexticC3.CubeLeading.Polynomial
open MvPolynomial
variable {K : Type*} [Field K] [CharZero K]

def sevenCoefficients (t : HamiltonianParameters K) (x : Fin 13 → K) : Coefficients K :=
  fun i j => x 0 * (if 1=i ∧ 0=j then 1 else 0) +
    x 1 * (if 2=i ∧ 0=j then 1 else 0) +
    x 2 * (if 0=i ∧ 1=j then 1 else 0) +
    x 3 * (if 3=i ∧ 0=j then (-1) else 0) +
    x 3 * (if 1=i ∧ 1=j then 1 else 0) +
    x 4 * (if 4=i ∧ 0=j then (-1) else 0) +
    x 4 * (if 2=i ∧ 1=j then 2 else 0) +
    x 5 * (if 0=i ∧ 2=j then 1 else 0) +
    x 6 * (if 5=i ∧ 0=j then 18 else 0) +
    x 6 * (if 3=i ∧ 1=j then (-60) else 0) +
    x 6 * (if 3=i ∧ 0=j then ((-5) * t.b₂) else 0) +
    x 6 * (if 1=i ∧ 2=j then 15 else 0) +
    x 7 * (if 6=i ∧ 0=j then 12 else 0) +
    x 7 * (if 4=i ∧ 1=j then (-60) else 0) +
    x 7 * (if 4=i ∧ 0=j then ((-5) * t.b₂) else 0) +
    x 7 * (if 2=i ∧ 2=j then 30 else 0) +
    x 8 * (if 7=i ∧ 0=j then (-216) else 0) +
    x 8 * (if 5=i ∧ 1=j then 1512 else 0) +
    x 8 * (if 5=i ∧ 0=j then (196 * t.b₂) else 0) +
    x 8 * (if 4=i ∧ 0=j then ((35 * t.b₁) + (35 * t.c₃)) else 0) +
    x 8 * (if 3=i ∧ 2=j then (-1260) else 0) +
    x 8 * (if 3=i ∧ 1=j then ((-140) * t.b₂) else 0) +
    x 8 * (if 1=i ∧ 3=j then 140 else 0) +
    x 9 * (if 8=i ∧ 0=j then (-27) else 0) +
    x 9 * (if 6=i ∧ 1=j then 252 else 0) +
    x 9 * (if 6=i ∧ 0=j then (35 * t.b₂) else 0) +
    x 9 * (if 5=i ∧ 0=j then ((7 * t.b₁) + (7 * t.c₃)) else 0) +
    x 9 * (if 4=i ∧ 2=j then (-315) else 0) +
    x 9 * (if 4=i ∧ 1=j then ((-35) * t.b₂) else 0) +
    x 9 * (if 2=i ∧ 3=j then 70 else 0) +
    x 10 * (if 6=i ∧ 0=j then ((-2) * t.b₂) else 0) +
    x 10 * (if 5=i ∧ 0=j then (((-6) * t.b₁) + ((-6) * t.c₃)) else 0) +
    x 10 * (if 4=i ∧ 1=j then (10 * t.b₂) else 0) +
    x 10 * (if 3=i ∧ 1=j then ((20 * t.b₁) + (20 * t.c₃)) else 0) +
    x 10 * (if 0=i ∧ 4=j then 5 else 0) +
    x 11 * (if 8=i ∧ 0=j then (9 * t.b₂) else 0) +
    x 11 * (if 7=i ∧ 0=j then ((36 * t.b₁) + (36 * t.c₃)) else 0) +
    x 11 * (if 6=i ∧ 1=j then ((-84) * t.b₂) else 0) +
    x 11 * (if 6=i ∧ 0=j then ((-7) * (t.b₂ ^ 2)) else 0) +
    x 11 * (if 5=i ∧ 1=j then (((-252) * t.b₁) + ((-252) * t.c₃)) else 0) +
    x 11 * (if 5=i ∧ 0=j then (((-21) * t.b₁ * t.b₂) + ((-21) * t.b₂ * t.c₃)) else 0) +
    x 11 * (if 4=i ∧ 2=j then (105 * t.b₂) else 0) +
    x 11 * (if 3=i ∧ 2=j then ((210 * t.b₁) + (210 * t.c₃)) else 0) +
    x 11 * (if 0=i ∧ 5=j then 21 else 0) +
    x 12 * (if 10=i ∧ 0=j then ((-36) * t.b₂) else 0) +
    x 12 * (if 9=i ∧ 0=j then (((-180) * t.b₁) + ((-180) * t.c₃)) else 0) +
    x 12 * (if 8=i ∧ 1=j then (540 * t.b₂) else 0) +
    x 12 * (if 8=i ∧ 0=j then (85 * (t.b₂ ^ 2)) else 0) +
    x 12 * (if 7=i ∧ 1=j then ((2160 * t.b₁) + (2160 * t.c₃)) else 0) +
    x 12 * (if 7=i ∧ 0=j then ((340 * t.b₁ * t.b₂) + (340 * t.b₂ * t.c₃)) else 0) +
    x 12 * (if 6=i ∧ 2=j then ((-1260) * t.b₂) else 0) +
    x 12 * (if 6=i ∧ 1=j then ((-140) * (t.b₂ ^ 2)) else 0) +
    x 12 * (if 6=i ∧ 0=j then ((70 * (t.b₁ ^ 2)) + (70 * (t.c₃ ^ 2)) + (140 * t.b₁ * t.c₃)) else 0) +
    x 12 * (if 5=i ∧ 2=j then (((-3780) * t.b₁) + ((-3780) * t.c₃)) else 0) +
    x 12 * (if 5=i ∧ 1=j then (((-420) * t.b₁ * t.b₂) + ((-420) * t.b₂ * t.c₃)) else 0) +
    x 12 * (if 4=i ∧ 3=j then (700 * t.b₂) else 0) +
    x 12 * (if 3=i ∧ 3=j then ((1400 * t.b₁) + (1400 * t.c₃)) else 0) +
    x 12 * (if 0=i ∧ 6=j then 70 else 0)

set_option maxHeartbeats 1500000 in
lemma seven_coefficients_eq (t : HamiltonianParameters K) (x : Fin 13 → K) :
    polynomialCoefficients (sevenCombination t x) = sevenCoefficients t x := by
  funext i j
  simp only [polynomialCoefficients, sevenCombination, bicoeff_sum, bicoeff_C_mul,
    Fin.sum_univ_succ, Fin.sum_univ_zero, sevenBasis, Matrix.cons_val_zero,
    Matrix.cons_val_succ, bicoeff_add, bicoeff_monomial, sevenCoefficients,
    mul_add, add_zero, add_assoc]
  rfl

def sevenCoefficientAt (t : HamiltonianParameters K) (x : Fin 13 → K) (n : ℕ) : Coefficients K :=
  (coefficientBracket t)^[n] (sevenCoefficients t x)

lemma sevenCoefficientAt_zero (t : HamiltonianParameters K) (x : Fin 13 → K) :
    sevenCoefficientAt t x 0 = sevenCoefficients t x := rfl

lemma sevenCoefficientAt_succ (t : HamiltonianParameters K) (x : Fin 13 → K) (n : ℕ) :
    sevenCoefficientAt t x (n+1) = coefficientBracket t (sevenCoefficientAt t x n) := by
  simp only [sevenCoefficientAt, Function.iterate_succ_apply']

lemma bicoeff_seven_iterate (t : HamiltonianParameters K) (x : Fin 13 → K) (n i j : ℕ) :
    bicoeff i j ((bracket (hamiltonian t))^[n] (sevenCombination t x)) =
      sevenCoefficientAt t x n i j := by
  rw [bicoeff_iterated_bracket, seven_coefficients_eq]
  rfl

end SexticC3.CubeLeading.Polynomial
