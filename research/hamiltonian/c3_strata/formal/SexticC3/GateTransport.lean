import SexticC3.Covariance

noncomputable section

namespace SexticC3.Differential

open MvPolynomial

variable {K : Type*} [Field K]

theorem linearSub_C (a b c d t : K) : linearSub a b c d (C t) = C t := by
  simp [linearSub, aeval_C, algebraMap_apply]

@[simp] theorem linearSub_X_false (a b c d : K) :
    linearSub a b c d (X false) = C a * X false + C b * X true := by
  simp [linearSub]

@[simp] theorem linearSub_X_true (a b c d : K) :
    linearSub a b c d (X true) = C c * X false + C d * X true := by
  simp [linearSub]

set_option maxHeartbeats 1500000 in
theorem linearSub_injective (a b c d : K) (hd : a*d-b*c ≠ 0) :
    Function.Injective (linearSub a b c d) := by
  let e := a*d-b*c
  let A := linearSub a b c d
  let B := linearSub (d/e) (-b/e) (-c/e) (a/e)
  have h (x : Bool) : B (A (X x)) = X x := by
    have he : e ≠ 0 := hd
    have hfactor : e⁻¹ * (a*d-b*c) = 1 := inv_mul_cancel₀ he
    have hdiag : a*(d/e) + b*(-c/e) = 1 := by
      rw [div_eq_mul_inv, div_eq_mul_inv]
      linear_combination hfactor
    have hoff : a*(-b/e) + b*(a/e) = 0 := by
      simp only [div_eq_mul_inv]
      ring
    have hrev : c*(d/e) + d*(-c/e) = 0 := by
      simp only [div_eq_mul_inv]
      ring
    have hdiag' : c*(-b/e) + d*(a/e) = 1 := by
      rw [div_eq_mul_inv, div_eq_mul_inv]
      linear_combination hfactor
    cases x
    · rw [show A (X false) = C a * X false + C b * X true from linearSub_X_false ..]
      simp only [map_add, map_mul, show B (C a) = C a from linearSub_C ..,
        show B (C b) = C b from linearSub_C ..]
      rw [show B (X false) = _ from linearSub_X_false ..,
        show B (X true) = _ from linearSub_X_true ..]
      simp only [mul_add, ← mul_assoc, ← C_mul]
      calc
        _ = C (a*(d/e) + b*(-c/e)) * X false +
            C (a*(-b/e) + b*(a/e)) * X true := by
              simp only [map_add]; ring
        _ = _ := by simp [hdiag, hoff]
    · rw [show A (X true) = C c * X false + C d * X true from linearSub_X_true ..]
      simp only [map_add, map_mul, show B (C c) = C c from linearSub_C ..,
        show B (C d) = C d from linearSub_C ..]
      rw [show B (X false) = _ from linearSub_X_false ..,
        show B (X true) = _ from linearSub_X_true ..]
      simp only [mul_add, ← mul_assoc, ← C_mul]
      calc
        _ = C (c*(d/e) + d*(-c/e)) * X false +
            C (c*(-b/e) + d*(a/e)) * X true := by
              simp only [map_add]; ring
        _ = _ := by simp [hrev, hdiag']
  have hBA : B.comp A = AlgHom.id K (Poly (R := K)) := by
    apply MvPolynomial.algHom_ext
    exact h
  intro F G hFG
  have hh := congrArg B hFG
  change (B.comp A) F = (B.comp A) G at hh
  simpa [hBA] using hh

theorem poisson_iterate_linearSub (a b c d t : K) (F G : Poly (R := K)) (i : ℕ) :
    (contraction 1 (C t * linearSub a b c d F))^[i] (linearSub a b c d G) =
      C ((t*(a*d-b*c))^i) * linearSub a b c d ((contraction 1 F)^[i] G) := by
  induction i with
  | zero => simp
  | succ i ih =>
    rw [Function.iterate_succ_apply', Function.iterate_succ_apply', ih,
      contraction_C_mul_left, contraction_C_mul_right,
      contraction_linearSub 1 (by decide), pow_one]
    simp only [← mul_assoc, ← C_mul, pow_succ]
    congr 2
    ring

theorem iterated_gate_linearSub (a b c d t : K) (F G : Poly (R := K))
    (i k : ℕ) (hk : k ≤ 5) :
    contraction k (C t * linearSub a b c d F)
      ((contraction 1 (C t * linearSub a b c d F))^[i] (linearSub a b c d G)) =
      C (t^(i+1)*(a*d-b*c)^(k+i)) *
        linearSub a b c d (contraction k F ((contraction 1 F)^[i] G)) := by
  rw [poisson_iterate_linearSub, contraction_C_mul_left, contraction_C_mul_right,
    contraction_linearSub k hk]
  simp only [← mul_assoc, ← C_mul, mul_pow, pow_succ, pow_add]
  congr 2
  ring

theorem iterated_gate_zero_iff (a b c d t : K) (F G : Poly (R := K))
    (i k : ℕ) (hk : k ≤ 5) (hd : a*d-b*c ≠ 0) (ht : t ≠ 0) :
    contraction k (C t * linearSub a b c d F)
      ((contraction 1 (C t * linearSub a b c d F))^[i] (linearSub a b c d G)) = 0 ↔
        contraction k F ((contraction 1 F)^[i] G) = 0 := by
  rw [iterated_gate_linearSub a b c d t F G i k hk]
  let e := t^(i+1)*(a*d-b*c)^(k+i)
  have hn : e ≠ 0 := mul_ne_zero (pow_ne_zero _ ht) (pow_ne_zero _ hd)
  constructor
  · intro h
    apply linearSub_injective a b c d hd
    change C e * _ = 0 at h
    have hc := congrArg (fun x : Poly (R := K) => C e⁻¹ * x) h
    dsimp only at hc
    rw [← mul_assoc, ← C_mul, inv_mul_cancel₀ hn, C_1, one_mul, mul_zero] at hc
    exact hc.trans (map_zero _).symm
  · intro h
    rw [h, map_zero, mul_zero]

theorem firstRefinement_linearSub_iff (a b c d t : K) (F G : Poly (R := K))
    (hd : a*d-b*c ≠ 0) (ht : t ≠ 0) :
    FirstRefinement (C t * linearSub a b c d F) (linearSub a b c d G) ↔
      FirstRefinement F G := by
  unfold FirstRefinement
  exact and_congr (iterated_gate_zero_iff a b c d t F G 0 3 (by decide) hd ht)
    (and_congr (iterated_gate_zero_iff a b c d t F G 0 5 (by decide) hd ht)
      (and_congr (iterated_gate_zero_iff a b c d t F G 1 3 (by decide) hd ht)
        (iterated_gate_zero_iff a b c d t F G 1 5 (by decide) hd ht)))

theorem persistentCore_linearSub_iff (a b c d t : K) (F G : Poly (R := K))
    (hd : a*d-b*c ≠ 0) (ht : t ≠ 0) :
    PersistentCore (C t * linearSub a b c d F) (linearSub a b c d G) ↔
      PersistentCore F G := by
  unfold PersistentCore
  exact forall_congr' fun i =>
    and_congr (iterated_gate_zero_iff a b c d t F G i 3 (by decide) hd ht)
      (iterated_gate_zero_iff a b c d t F G i 5 (by decide) hd ht)

end SexticC3.Differential
