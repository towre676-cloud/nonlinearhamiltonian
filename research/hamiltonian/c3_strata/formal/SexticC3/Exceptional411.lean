import SexticC3.Model

namespace SexticC3.Exceptional411

variable {K : Type*} [Field K]

/-- Coefficient of the order-k contraction with q^4 p^2 + δ q^6.
The second argument is a list of (q exponent, coefficient) pairs in degree n. -/
def contraction (δ : K) (k n u v : Nat) (g : List (Nat × K)) : K :=
  (g.map fun (j, a) =>
    ((monomialRow k u v 4 n j : K) + δ * (monomialRow k u v 6 n j : K)) * a).sum

def partner : List (Nat × K) := [(1, 1)]

def first (δ : K) : List (Nat × K) := [(4, 2), (6, 6 * δ)]

def second (δ : K) : List (Nat × K) := [(9, -48 * δ)]

theorem first_iterate (δ : K) (u v : Nat) :
    contraction δ 1 2 u v partner =
      (if u = 4 ∧ v = 2 then 2 else 0) +
      (if u = 6 ∧ v = 0 then 6 * δ else 0) := by
  have h₄ : weight 1 4 2 1 = 2 := by decide
  have h₆ : weight 1 6 2 1 = 6 := by decide
  by_cases a : u = 4 ∧ v = 2 <;> by_cases b : u = 6 ∧ v = 0 <;>
    simp only [contraction, partner, List.map, List.sum_cons, List.sum_nil,
      monomialRow, h₄, h₆, one_mul, mul_one, add_zero] <;>
    simp only [show (4 + 1 = u + 1 ∧ (6 - 4) + (2 - 1) = v + 1) ↔
      u = 4 ∧ v = 2 by omega,
      show (6 + 1 = u + 1 ∧ (6 - 6) + (2 - 1) = v + 1) ↔
        u = 6 ∧ v = 0 by omega, a, b, if_true, if_false] <;> simp <;> ring

theorem second_iterate (δ : K) (u v : Nat) :
    contraction δ 1 6 u v (first δ) = if u = 9 ∧ v = 1 then -48 * δ else 0 := by
  have h₄₄ : weight 1 4 6 4 = 0 := by decide
  have h₄₆ : weight 1 4 6 6 = -12 := by decide
  have h₆₄ : weight 1 6 6 4 = 12 := by decide
  have h₆₆ : weight 1 6 6 6 = 0 := by decide
  by_cases h : u = 9 ∧ v = 1 <;>
    simp only [contraction, first, List.map, List.sum_cons, List.sum_nil,
      monomialRow, h₄₄, h₄₆, h₆₄, h₆₆, ite_self, Int.cast_zero, zero_add, mul_zero,
      show (6 + 4 = u + 1 ∧ (6 - 6) + (6 - 4) = v + 1) ↔
        u = 9 ∧ v = 1 by omega,
      show (4 + 6 = u + 1 ∧ (6 - 4) + (6 - 6) = v + 1) ↔
        u = 9 ∧ v = 1 by omega, h, if_true, if_false] <;> simp <;> ring

theorem static_gates (δ : K) (u v k : Nat) (hk : k = 3 ∨ k = 5) :
    contraction δ k 2 u v partner = 0 ∧ contraction δ k 6 u v (first δ) = 0 := by
  rcases hk with rfl | rfl <;>
    simp [contraction, partner, first, monomialRow,
      show weight 3 4 2 1 = 0 by decide, show weight 3 6 2 1 = 0 by decide,
      show weight 3 4 6 4 = 0 by decide, show weight 3 4 6 6 = 0 by decide,
      show weight 3 6 6 4 = 0 by decide, show weight 3 6 6 6 = 0 by decide,
      show weight 5 4 2 1 = 0 by decide, show weight 5 6 2 1 = 0 by decide,
      show weight 5 4 6 4 = 0 by decide, show weight 5 4 6 6 = 0 by decide,
      show weight 5 6 6 4 = 0 by decide, show weight 5 6 6 6 = 0 by decide]

theorem second_obstruction (δ : K) (u v : Nat) :
    contraction δ 3 10 u v (second δ) =
      if u = 10 ∧ v = 0 then -82944 * δ else 0 := by
  have h₄ : weight 3 4 10 9 = 1728 := by decide
  have h₆ : weight 3 6 10 9 = 0 := by decide
  by_cases h : u = 10 ∧ v = 0 <;>
    simp only [contraction, second, List.map, List.sum_cons, List.sum_nil,
      monomialRow, h₄, h₆, ite_self, Int.cast_zero, mul_zero, add_zero,
      show (4 + 9 = u + 3 ∧ (6 - 4) + (10 - 9) = v + 3) ↔
        u = 10 ∧ v = 0 by omega, h, if_true, if_false] <;> simp <;> ring

theorem second_obstruction_nonzero [CharZero K] (δ : K) (hδ : δ ≠ 0) :
    contraction δ 3 10 10 0 (second δ) ≠ 0 := by
  rw [second_obstruction]
  simp only [and_self, if_true]
  exact mul_ne_zero (by norm_num) hδ

end SexticC3.Exceptional411
