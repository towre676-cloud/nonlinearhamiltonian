import SexticC3.CubeLeadingFlatCore

/-! Regressions at the E=0 boundary, the excluded affine family, and the
normalization of the original-coordinate flat gates. -/
noncomputable section
open MvPolynomial
open SexticC3.CubeLeading.Polynomial

private def edge : HamiltonianParameters ℚ where
  b₁ := 0
  b₂ := -2
  b₃ := 0
  c₃ := 0
  c₄ := 1
  c₅ := 0
  b₀ := 0
  c₀ := 0
  c₁ := 0
  c₂ := 0

private def affine : HamiltonianParameters ℚ where
  b₁ := 0
  b₂ := 0
  b₃ := 0
  c₃ := 0
  c₄ := 0
  c₅ := 0
  b₀ := 0
  c₀ := 0
  c₁ := 0
  c₂ := 0

private lemma pderiv_seven (i : Fin 2) : pderiv i (7 : Poly ℚ) = 0 :=
  (pderiv i).map_natCast 7

-- Staticity alone does NOT give the six-degree cutoff on E=0.
private theorem edge_seventh_static : Static edge.toGateParameters ((X 1 : Poly ℚ)^7) := by
  constructor <;> simp [thirdGate, fifthGate, edge, pderiv_pow, pderiv_mul,
    pderiv_X, Pi.single_apply, pderiv_seven, map_ofNat] <;> norm_num

-- Applying the Hamiltonian bracket supplies the missing obstruction.
example : ¬ Static edge.toGateParameters
    (bracket (hamiltonian edge) ((X 1 : Poly ℚ)^7)) := by
  intro hD
  have hb := first_refinement_momentum_bound_on_symbol_zero edge (by rfl) (by rfl)
    (by norm_num [edge]) _ edge_seventh_static hD
  have hz := bicoeff_vanish_of_bound hb 0 7 (by norm_num)
  norm_num [bicoeff, coeff_X_pow, exponent] at hz

-- The E=0 point is still inside the quantified original-coordinate theorem.
example (f : Poly ℚ) : AllFlatPersistent (shear 1 (hamiltonian edge)) f ↔
    ∃ a b : ℚ, f = C a+C b*shear 1 (hamiltonian edge) :=
  all_flat_newton_persistent_core edge (Or.inr (Or.inl (by norm_num [edge]))) f

-- At the excluded all-affine point, P² really is a persistent extra partner.
example : AllFlatPersistent (shear 1 (hamiltonian affine)) (shear 1 ((X 1 : Poly ℚ)^2)) := by
  rw [all_flat_persistent_iff, persistent_flat_transport]
  apply kernel_mem_persistentCore
  · constructor <;> simp [thirdGate, fifthGate, affine, pderiv_pow, pderiv_mul,
      pderiv_X, Pi.single_apply, map_ofNat]
  · simp [hamiltonian, affine, ← qP_monomial, bracket, pderiv_pow,
      pderiv_mul, pderiv_X, Pi.single_apply]

example : ¬ ∃ a b : ℚ, (X 1 : Poly ℚ)^2 = C a+C b*hamiltonian affine := by
  rintro ⟨a, b, he⟩
  have h := congrArg (bicoeff 0 2) he
  simp [hamiltonian, affine, ← qP_monomial, bicoeff, coeff_X_pow, coeff_C,
    coeff_C_mul, exponent, Finsupp.single_eq_zero, Finsupp.single_eq_single_iff, eq_comm] at h

-- A factor/sign regression for the third original-coordinate contraction.
example : flatContraction 3 (shear 1 (hamiltonian affine))
    (shear 1 ((X 0 : Poly ℚ)^3)) = C (-36) := by
  rw [flat_third_gate_transport]
  norm_num [thirdGate, affine, pderiv_pow, pderiv_mul, pderiv_X, Pi.single_apply,
    map_ofNat, map_neg]
