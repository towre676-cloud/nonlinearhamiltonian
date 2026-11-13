import SexticC3.Differential

noncomputable section

namespace SexticC3.Differential

open MvPolynomial

variable {R : Type*} [CommRing R]

/-- Substitution of the two linear forms given by the rows of a matrix. -/
def linearSub (a b c d : R) : Poly (R := R) →ₐ[R] Poly (R := R) :=
  aeval fun i : Bool =>
    if i then C c * X false + C d * X true else C a * X false + C b * X true

theorem pderiv_linearSub (a b c d : R) (i : Bool) (F : Poly (R := R)) :
    pderiv i (linearSub a b c d F) =
      C (if i then b else a) * linearSub a b c d (pderiv false F) +
      C (if i then d else c) * linearSub a b c d (pderiv true F) := by
  have hv (j : Bool) :
      pderiv i (linearSub a b c d (X j)) =
        C (if i then b else a) * linearSub a b c d (pderiv false (X j)) +
        C (if i then d else c) * linearSub a b c d (pderiv true (X j)) := by
    cases i <;> cases j <;> simp [linearSub, pderiv_X, pderiv_C_mul]
  induction F using MvPolynomial.induction_on with
  | C r => simp [linearSub, aeval_C, algebraMap_apply]
  | add F G hF hG => simp only [map_add, hF, hG]; ring
  | mul_X F j ih =>
    simp only [map_mul, pderiv_mul, ih, hv, map_add]
    ring

private theorem pderiv_commute (F : Poly (R := R)) :
    pderiv false (pderiv true F) = pderiv true (pderiv false F) := by
  induction F using MvPolynomial.induction_on' with
  | monomial e a =>
    rw [← exponent_eta e]
    change pderiv false (pderiv true (mono _ _ a)) = pderiv true (pderiv false (mono _ _ a))
    simp only [pderiv_p_mono, pderiv_q_mono]
    congr 1
    ring
  | add F G hF hG => simp only [map_add, hF, hG]

private theorem q_iterate_p (s : ℕ) (F : Poly (R := R)) :
    (pderiv true)^[s] (pderiv false F) = pderiv false ((pderiv true)^[s] F) := by
  induction s generalizing F with
  | zero => rfl
  | succ s ih =>
    simp only [Function.iterate_succ_apply', ih, pderiv_commute]

private theorem mixed_q (r s : ℕ) (F : Poly (R := R)) :
    mixed r s (pderiv false F) = mixed (r+1) s F := by
  simp only [mixed, q_iterate_p, Function.iterate_succ_apply]

private theorem mixed_p (r s : ℕ) (F : Poly (R := R)) :
    mixed r s (pderiv true F) = mixed r (s+1) F := by
  simp only [mixed, Function.iterate_succ_apply]

private theorem contraction_succ_small (k : ℕ) (hk : k < 5) (F G : Poly (R := R)) :
    contraction (k+1) F G =
      contraction k (pderiv false F) (pderiv true G) -
      contraction k (pderiv true F) (pderiv false G) := by
  have h : k = 0 ∨ k = 1 ∨ k = 2 ∨ k = 3 ∨ k = 4 := by omega
  rcases h with rfl | rfl | rfl | rfl | rfl <;>
    norm_num [contraction, List.range_succ, Nat.choose, mixed_q, mixed_p] <;> ring

theorem contraction_C_mul_left (k : ℕ) (a : R) (F G : Poly (R := R)) :
    contraction k (C a * F) G = C a * contraction k F G := by
  unfold contraction
  induction List.range (k + 1) with
  | nil => simp
  | cons s ss ih =>
    simp only [List.map_cons, List.sum_cons]
    rw [ih, mixed_C_mul]
    ring

/-- Determinant covariance for all orders required by the sextic gates,
including the Poisson bracket at order one. -/
theorem contraction_linearSub (k : ℕ) (hk : k ≤ 5) (a b c d : R) (F G : Poly (R := R)) :
    contraction k (linearSub a b c d F) (linearSub a b c d G) =
      C ((a*d-b*c)^k) * linearSub a b c d (contraction k F G) := by
  induction k generalizing F G with
  | zero => simp [contraction, List.range_succ, mixed]
  | succ k ih =>
    have hs : k < 5 := by omega
    have hle : k ≤ 5 := by omega
    rw [contraction_succ_small k hs, contraction_succ_small k hs F G]
    simp only [pderiv_linearSub, Bool.false_eq_true, if_false, if_true,
      contraction_add_left, contraction_add_right, contraction_C_mul_left,
      contraction_C_mul_right, ih hle, map_sub, pow_succ, map_mul]
    ring

end SexticC3.Differential
