import Mathlib.Tactic.LinearCombination
import Mathlib.Tactic.Ring

/-!
# Euler–Cramer identity for the cube-leading core

For a weighted-homogeneous leading form `h` of weight `d` and a form `s` of
weight `w`, with weights `(wq, wP)`, the Euler relations turn the Poisson
bracket `{h, s} = h_q s_P - h_P s_q` into the divisibility statement used in
the core-closure theorem: `wq * q * {h, s} = d * h * s_P - w * s * h_P`.
Hence if `{h, s}` is a multiple of `h`, then `h` divides `w * s * h_P`.
The identities are stated in an arbitrary commutative ring, with the partial
derivatives as free elements constrained only by the Euler relations, so they
apply verbatim to the bivariate polynomial ring.
-/

namespace SexticC3.CubeLeading

variable {R : Type*} [CommRing R]

theorem euler_cramer (q P h s hq hP sq sP wq wP d w : R)
    (eh : wq * q * hq + wP * P * hP = d * h)
    (es : wq * q * sq + wP * P * sP = w * s) :
    wq * q * (hq * sP - hP * sq) = d * h * sP - w * s * hP := by
  linear_combination sP * eh - hP * es

theorem euler_cramer' (q P h s hq hP sq sP wq wP d w : R)
    (eh : wq * q * hq + wP * P * hP = d * h)
    (es : wq * q * sq + wP * P * sP = w * s) :
    wP * P * (hq * sP - hP * sq) = w * s * hq - d * h * sq := by
  linear_combination hq * es - sq * eh

/-- If the bracket is a multiple `m * h` of the leading form, then `h` divides
`w * s * h_P`. -/
theorem leading_form_dvd (q P h s hq hP sq sP wq wP d w m : R)
    (eh : wq * q * hq + wP * P * hP = d * h)
    (es : wq * q * sq + wP * P * sP = w * s)
    (hb : hq * sP - hP * sq = m * h) :
    h ∣ w * s * hP := by
  refine ⟨d * sP - wq * q * m, ?_⟩
  have key := euler_cramer q P h s hq hP sq sP wq wP d w eh es
  rw [hb] at key
  linear_combination key

/-- Case I: a sixth-power partner needs `3 b₃ + 5 c₅ = 0`, and its `q^5 P^3`
coefficient needs `3 b₃ + 10 c₅ = c₅`; together they force `c₅ = 0`. -/
theorem case_one_obstruction {K : Type*} [Field K] [CharZero K] (b₃ c₅ : K)
    (h₁ : 3 * b₃ + 5 * c₅ = 0) (h₂ : 2 * (3 * b₃ + 10 * c₅) = 2 * c₅) : c₅ = 0 := by
  have h : (8 : K) * c₅ = 0 := by linear_combination h₂ - 2 * h₁
  rcases mul_eq_zero.mp h with h | h
  · norm_num at h
  · exact h

end SexticC3.CubeLeading
