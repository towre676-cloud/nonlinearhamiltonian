import SexticC3.CubeLeadingFullCriterion

/-! Boundary regressions: each older branch, the E=0 cutoff, the necessary
third refinement at the quadratic restoring point, and the affine converse. -/
noncomputable section
open MvPolynomial
open SexticC3.CubeLeading.Polynomial

private def point (b₂ c₂ c₃ : ℚ) : HamiltonianParameters ℚ where
  b₁ := -c₃
  b₂ := b₂
  b₃ := 0
  c₃ := c₃
  c₄ := 0
  c₅ := 0
  b₀ := 0
  c₀ := 0
  c₁ := 0
  c₂ := c₂

example (f : Poly ℚ) : AllFlatPersistent (shear 1 (hamiltonian (point 1 0 0))) f ↔
    ∃ a b : ℚ, f = C a+C b*shear 1 (hamiltonian (point 1 0 0)) :=
  all_flat_nonaffine_persistent_core _ (by simp [NonAffine, point]) f

example (f : Poly ℚ) : AllFlatPersistent (shear 1 (hamiltonian (point 0 0 1))) f ↔
    ∃ a b : ℚ, f = C a+C b*shear 1 (hamiltonian (point 0 0 1)) :=
  all_flat_nonaffine_persistent_core _ (by simp [NonAffine, point]) f

example (f : Poly ℚ) : AllFlatPersistent (shear 1 (hamiltonian (point 0 1 0))) f ↔
    ∃ a b : ℚ, f = C a+C b*shear 1 (hamiltonian (point 0 1 0)) :=
  all_flat_nonaffine_persistent_core _ (by simp [NonAffine, point]) f

private theorem seventh_static : Static (point 0 0 1).toGateParameters ((X 1 : Poly ℚ)^7) := by
  constructor <;> simp [thirdGate, fifthGate, point, pderiv_pow, pderiv_mul,
    pderiv_X, Pi.single_apply, map_ofNat] <;> norm_num

example : ¬ Static (point 0 0 1).toGateParameters
    (bracket (hamiltonian (point 0 0 1)) ((X 1 : Poly ℚ)^7)) := by
  intro hD
  have hb := seven_first_refinement_momentum_bound (point 0 0 1) rfl rfl rfl
    (by simp [point]) _ seventh_static hD
  have hz := bicoeff_vanish_of_bound hb 0 7 (by norm_num)
  norm_num [bicoeff, coeff_X_pow, exponent] at hz

example : ¬ (∀ f : Poly ℚ, AllFlatPersistent (shear 1 (hamiltonian (point 0 0 0))) f ↔
    ∃ a b : ℚ, f = C a+C b*shear 1 (hamiltonian (point 0 0 0))) := by
  rw [all_flat_core_iff_nonaffine]
  simp [NonAffine, point]

private lemma pderiv_twentyfour (i : Fin 2) : pderiv i (24 : Poly ℚ) = 0 :=
  (pderiv i).map_natCast 24

private def D : Poly ℚ → Poly ℚ := bracket (hamiltonian (point 0 1 0))
private lemma dP : D (X 1) = C 2*X 0 := by
  simp [D, hamiltonian_bracket, point, pderiv_X, Pi.single_apply]
private lemma d2P : D (C 2*X 0) = C (-6)*X 1^2 := by
  simp [D, hamiltonian_bracket, point, pderiv_C_mul, pderiv_X, Pi.single_apply, map_ofNat, map_neg]
  ring
private lemma d3P : D (C (-6)*X 1^2) = C (-24)*X 0*X 1 := by
  simp [D, hamiltonian_bracket, point, pderiv_C_mul, pderiv_pow, pderiv_X,
    Pi.single_apply, map_neg, map_ofNat]
  ring

example : ∀ n : ℕ, n ≤ 2 → Static (point 0 1 0).toGateParameters (D^[n] (X 1)) := by
  intro n hn
  interval_cases n <;>
    simp only [Function.iterate_succ_apply', Function.iterate_zero_apply, dP, d2P]
  · exact momentum_static _
  all_goals constructor <;> simp [thirdGate, fifthGate, point, pderiv_C_mul,
    pderiv_mul, pderiv_pow, pderiv_X, Pi.single_apply, map_neg, map_ofNat]

example : ¬ Static (point 0 1 0).toGateParameters (D^[3] (X 1)) := by
  intro h
  have hz := h.1
  simp only [Function.iterate_succ_apply', Function.iterate_zero_apply, dP, d2P, d3P] at hz
  norm_num [Function.iterate_succ_apply', dP, d2P, d3P, thirdGate, point,
    pderiv_C_mul, pderiv_mul, pderiv_X, Pi.single_apply, pderiv_twentyfour, map_neg, map_ofNat] at hz
