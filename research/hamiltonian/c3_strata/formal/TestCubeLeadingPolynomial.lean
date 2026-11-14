import SexticC3.CubeLeadingNewton

/-! Boundary regressions for the concrete K3/K4 hypotheses. -/
open MvPolynomial SexticC3.CubeLeading.Polynomial

-- At the excluded coefficient c=0, q is killed by two brackets but not one.
example :
    bracket (caseOne (0 : ℚ)) (bracket (caseOne (0 : ℚ)) (X 0)) = 0 ∧
    bracket (caseOne (0 : ℚ)) (X 0) ≠ 0 := by
  constructor
  · simp [bracket, caseOne, pderiv_pow, pderiv_mul, pderiv_X, Pi.single_apply]
    rw [show (3 : Poly ℚ) = C (3 : ℚ) by exact (map_ofNat (C : ℚ →+* Poly ℚ) 3).symm]
    exact pderiv_C
  · simp [bracket, caseOne, pderiv_pow, pderiv_mul, pderiv_X, Pi.single_apply]

-- Cancellation of the leading bracket does not imply cancellation of D_H.
example :
    bracket (caseOne (1 : ℚ)) (caseOne (1 : ℚ)) = 0 ∧
    bracket (caseOne (1 : ℚ) + X 0) (caseOne (1 : ℚ)) = 3 * X 1^2 := by
  constructor
  · simp [bracket]; ring
  · simp [bracket, caseOne, pderiv_pow, pderiv_mul, pderiv_X, Pi.single_apply]
    ring
