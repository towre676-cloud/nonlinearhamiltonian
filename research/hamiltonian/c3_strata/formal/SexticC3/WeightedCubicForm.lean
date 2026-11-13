import Mathlib.Tactic.Ring
import Mathlib.Tactic.LinearCombination
import Mathlib.Algebra.Field.Basic
import Mathlib.Algebra.CharZero.Defs

/-!
# Weighted cubic-form sixfold Hamiltonians: collapse of the static tail

For `H = q^6 + α q^4 p + β q^2 p^2 + x p^3` and a weighted-homogeneous
`G = Σ g_j q^(d-2j) p^j`, the fifth Moyal gate gives the two-term rows
`6 m g_m = α (d - 2m + 2) g_(m-1)` (`m ≥ 5`) and the third gate gives the
four-term rows used below (`k = 4, 5`).  These theorems are the algebraic core
of the all-degree bound: a nonzero tail forces `H = (q^2 + (α/3) p)^3`.
-/

namespace WeightedCubicForm
variable {K : Type*} [Field K] [CharZero K]

/-- The affine-in-`k` obstruction after eliminating the tail. -/
def bracket (α β x d k : K) : K :=
  α ^ 3 * (14 * k + 16 - 4 * d) / 9 + 2 * α * β * (d - 3 * k - 3) - 6 * x * (d - 2 * k - 1)

/-- Third-gate row `k = 4` after substituting the three fifth-gate rows. -/
theorem row_four (α β x d g4 g5 g6 g7 : K)
    (e5 : 30 * g5 = α * (d - 8) * g4) (e6 : 36 * g6 = α * (d - 10) * g5)
    (e7 : 42 * g7 = α * (d - 12) * g6)
    (r4 : -6*g4*x*(d - 10)*(d - 9)*(d - 8) + 60*g5*β*(d - 15)*(d - 10) + 360*g6*α*(44 - 3*d) + 25200*g7 = 0) :
    (d - 8) * (d - 10) * bracket α β x d 4 * g4 = 0 := by
  unfold bracket
  linear_combination r4 - (600) * e7 - (40*α*(18 - d)/3) * e6 - (2*(-2*d^2*α^2 + 9*d^2*β + 56*d*α^2 - 225*d*β - 360*α^2 + 1350*β)/9) * e5

/-- Third-gate row `k = 5` after substituting the three fifth-gate rows. -/
theorem row_five (α β x d g5 g6 g7 g8 : K)
    (e6 : 36 * g6 = α * (d - 10) * g5) (e7 : 42 * g7 = α * (d - 12) * g6)
    (e8 : 48 * g8 = α * (d - 14) * g7)
    (r5 : -6*g5*x*(d - 12)*(d - 11)*(d - 10) + 72*g6*β*(d - 18)*(d - 12) + 504*g7*α*(52 - 3*d) + 40320*g8 = 0) :
    (d - 10) * (d - 12) * bracket α β x d 5 * g5 = 0 := by
  unfold bracket
  linear_combination r5 - (840) * e8 - (8*α*(43 - 2*d)) * e7 - (2*(-2*d^2*α^2 + 9*d^2*β + 67*d*α^2 - 270*d*β - 516*α^2 + 1944*β)/9) * e6

/-- If both obstructions vanish, the weighted leading form is a perfect cube. -/
theorem cube_of_brackets (α β x d : K) (hα : α ≠ 0) (hd : d + 3 ≠ 0)
    (h4 : bracket α β x d 4 = 0) (h5 : bracket α β x d 5 = 0) :
    3 * β = α ^ 2 ∧ 27 * x = α ^ 3 := by
  unfold bracket at h4 h5
  have key : (d + 3) * α * (α ^ 2 - 3 * β) = 0 := by
    linear_combination (3*(11 - d)/2) * h4 + (3*(d - 9)/2) * h5
  have hβ : α ^ 2 - 3 * β = 0 := by
    rcases mul_eq_zero.mp key with h | h
    · rcases mul_eq_zero.mp h with h | h
      · exact absurd h hd
      · exact absurd h hα
    · exact h
  have hβ' : 3 * β = α ^ 2 := by linear_combination -hβ
  refine ⟨hβ', ?_⟩
  linear_combination (9 / 4 : K) * h5 - (9 / 4 : K) * h4 + (9 * α / 2) * hβ'

/-- **Tail collapse.**  In weight `d` outside `{-3, 8, 10, 12}`, a solution of the
fifth-gate rows `m = 5,…,8` and the third-gate rows `k = 4, 5` with `g4 ≠ 0`
exists only on the cube locus `3 β = α^2`, `27 x = α^3`. -/
theorem tail_collapse (α β x d g4 g5 g6 g7 g8 : K) (hα : α ≠ 0)
    (hd3 : d + 3 ≠ 0) (hd8 : d - 8 ≠ 0) (hd10 : d - 10 ≠ 0) (hd12 : d - 12 ≠ 0)
    (e5 : 30 * g5 = α * (d - 8) * g4) (e6 : 36 * g6 = α * (d - 10) * g5)
    (e7 : 42 * g7 = α * (d - 12) * g6) (e8 : 48 * g8 = α * (d - 14) * g7)
    (r4 : -6*g4*x*(d - 10)*(d - 9)*(d - 8) + 60*g5*β*(d - 15)*(d - 10) + 360*g6*α*(44 - 3*d) + 25200*g7 = 0)
    (r5 : -6*g5*x*(d - 12)*(d - 11)*(d - 10) + 72*g6*β*(d - 18)*(d - 12) + 504*g7*α*(52 - 3*d) + 40320*g8 = 0)
    (hg : g4 ≠ 0) : 3 * β = α ^ 2 ∧ 27 * x = α ^ 3 := by
  have h4 := row_four α β x d g4 g5 g6 g7 e5 e6 e7 r4
  have h5 := row_five α β x d g5 g6 g7 g8 e6 e7 e8 r5
  have hg5 : g5 ≠ 0 := by
    intro h
    have : α * (d - 8) * g4 = 0 := by rw [← e5, h, mul_zero]
    exact (mul_ne_zero (mul_ne_zero hα hd8) hg) this
  have b4 : bracket α β x d 4 = 0 := by
    rcases mul_eq_zero.mp h4 with h | h
    · rcases mul_eq_zero.mp h with h | h
      · rcases mul_eq_zero.mp h with h | h
        · exact absurd h hd8
        · exact absurd h hd10
      · exact h
    · exact absurd h hg
  have b5 : bracket α β x d 5 = 0 := by
    rcases mul_eq_zero.mp h5 with h | h
    · rcases mul_eq_zero.mp h with h | h
      · rcases mul_eq_zero.mp h with h | h
        · exact absurd h hd10
        · exact absurd h hd12
      · exact h
    · exact absurd h hg5
  exact cube_of_brackets α β x d hα hd3 b4 b5

end WeightedCubicForm
