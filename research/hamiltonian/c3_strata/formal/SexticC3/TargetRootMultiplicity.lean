import SexticC3.StaticTail
import Mathlib.Algebra.Polynomial.RingDivision

noncomputable section

namespace SexticC3.StaticTail

open Polynomial

variable {K : Type*} [Field K] [CharZero K]

def chartQuintic (a b c d : K) : K[X] :=
  X^5 + C a * X^3 + C b * X^2 + C c * X + C d

/-- The exceptional target quintic cannot have an exactly triple root. -/
theorem rootMultiplicity_ne_three_of_targets (a b c d x : K)
    (hb : b^2 + (2/5 : K) * a^3 = 0)
    (hc : c + (3/20 : K) * a^2 = 0)
    (hd : d + (1/50 : K) * a*b = 0) :
    (chartQuintic a b c d).rootMultiplicity x ≠ 3 := by
  classical
  obtain ⟨r, hr⟩ := target_factorization a b c d hb hc hd
  change chartQuintic a b c d = _ at hr
  rw [show X + 4 * C r = X - C (-(4*r)) by
    simp [map_neg, map_mul, map_ofNat, sub_neg_eq_add]] at hr
  rw [hr, rootMultiplicity_mul (mul_ne_zero (pow_ne_zero _ (X_sub_C_ne_zero _))
    (X_sub_C_ne_zero _))]
  by_cases hx : x = r
  · subst x
    rw [rootMultiplicity_X_sub_C_pow, rootMultiplicity_X_sub_C]
    split_ifs <;> decide
  · rw [rootMultiplicity_eq_zero (p := (X - C r)^4)
      (fun hp => hx (by
        change eval x ((X - C r)^4) = 0 at hp
        rw [eval_pow] at hp
        simpa [sub_eq_zero] using (pow_eq_zero hp : eval x (X - C r) = 0))), rootMultiplicity_X_sub_C]
    split_ifs <;> decide

end SexticC3.StaticTail
