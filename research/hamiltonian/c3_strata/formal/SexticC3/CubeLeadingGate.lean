import Mathlib.Algebra.Polynomial.Derivative
import Mathlib.Tactic.LinearCombination
import Mathlib.Tactic.Ring

/-!
# Degree obstruction for the cube-leading boundary

In the chart `P = p + q^2` the transported third gate of
`H = P^3 + B(q) P + C(q)` acts on a function of the chart momentum by
`T_3(H, g(P)) = 6 * E * g'''`, and after the fifth gate the static equations
force a product `e * g'''` to have degree at most three for a nonzero
coefficient `e`.  The lemmas below are the all-degree step: they bound the
degree of `g` for every polynomial `g`, with no support hypothesis.
-/

namespace SexticC3.CubeLeading

open Polynomial

variable {K : Type*} [Field K] [CharZero K]

theorem natDegree_le_succ_of_derivative (g : K[X]) (n : ℕ)
    (h : (derivative g).natDegree ≤ n) : g.natDegree ≤ n + 1 := by
  by_cases h0 : g.natDegree = 0
  · omega
  · obtain ⟨m, hm⟩ := Nat.exists_eq_succ_of_ne_zero h0
    have hg : g ≠ 0 := by
      intro hz
      simp [hz] at h0
    have hc : (derivative g).coeff m ≠ 0 := by
      rw [coeff_derivative]
      have h1 : g.coeff (m + 1) ≠ 0 := by
        rw [← Nat.succ_eq_add_one, ← hm]
        exact leadingCoeff_ne_zero.mpr hg
      have h2 : ((m : K) + 1) ≠ 0 := by
        have : ((m + 1 : ℕ) : K) ≠ 0 := Nat.cast_ne_zero.mpr (by omega)
        simpa using this
      exact mul_ne_zero h1 h2
    have := le_natDegree_of_ne_zero hc
    omega

theorem natDegree_le_of_iterate_derivative (k n : ℕ) (g : K[X])
    (h : (derivative^[k] g).natDegree ≤ n) : g.natDegree ≤ n + k := by
  induction k generalizing g with
  | zero => simpa using h
  | succ k ih =>
      rw [Function.iterate_succ_apply] at h
      have h1 := ih (derivative g) h
      have h2 := natDegree_le_succ_of_derivative g (n + k) h1
      omega

/-- The decisive gate lemma: a nonzero multiplier cannot hide a high third
derivative.  With `e` a nonzero coefficient of the transported gate symbol and
`d = 3` this gives `natDegree g ≤ 6`. -/
theorem gate_degree_bound (e g : K[X]) (d : ℕ) (he : e ≠ 0)
    (h : (e * derivative^[3] g).natDegree ≤ d) : g.natDegree ≤ d + 3 := by
  apply natDegree_le_of_iterate_derivative 3 d g
  by_cases hg : derivative^[3] g = 0
  · simp [hg]
  · rw [natDegree_mul he hg] at h
    omega

theorem static_function_degree_le_six (e g : K[X]) (he : e ≠ 0)
    (h : (e * derivative^[3] g).natDegree ≤ 3) : g.natDegree ≤ 6 :=
  gate_degree_bound e g 3 he h

/-- Non-resonance of the top coefficient.  With `β = b₃ + c₅`, the coefficient
of `u^(m-2)` in the reduced gate is `m (m-1) (2 β (m-1) - b₃ (m-2))`.  When the
`q^2` coefficient `3 b₃ + 10 c₅` of the gate symbol vanishes, its vanishing
forces `b₃ = 0` in every degree `m`. -/
theorem top_coefficient_nonresonant (b₃ c₅ : K) (m : ℕ)
    (h₁ : 3 * b₃ + 10 * c₅ = 0)
    (h₂ : 2 * (b₃ + c₅) * ((m : K) - 1) - b₃ * ((m : K) - 2) = 0) :
    b₃ = 0 := by
  have h : b₃ * (2 * (m : K) + 3) = 0 := by
    linear_combination 5 * h₂ - ((m : K) - 1) * h₁
  have hm : (2 * (m : K) + 3) ≠ 0 := by
    have : ((2 * m + 3 : ℕ) : K) ≠ 0 := Nat.cast_ne_zero.mpr (by omega)
    simpa using this
  rcases mul_eq_zero.mp h with h | h
  · exact h
  · exact absurd h hm

end SexticC3.CubeLeading
