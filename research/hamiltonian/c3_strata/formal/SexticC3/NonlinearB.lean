import SexticC3.SimpleRootChart

/-!
Exact nonlinear quadratic-momentum gates on Mathlib's bivariate polynomial
ring. All parameters range over an arbitrary characteristic-zero field.
-/
noncomputable section

namespace SexticC3.NonlinearB

open MvPolynomial Differential

variable {K : Type*} [Field K] [CharZero K]

structure Parameters (K : Type*) where
  h0 : K
  h1 : K
  h2 : K
  h3 : K
  h4 : K
  h5 : K
  h6 : K
  a0 : K
  a1 : K
  b0 : K
  b1 : K
  b2 : K
  b3 : K

def H (c : Parameters K) : Poly (R := K) :=
  mono 0 0 c.h0 + mono 1 0 c.h1 + mono 2 0 c.h2 + mono 3 0 c.h3 +
  mono 4 0 c.h4 + mono 5 0 c.h5 + mono 6 0 c.h6 +
  mono 0 1 c.a0 + mono 1 1 c.a1 +
  mono 0 2 c.b0 + mono 1 2 c.b1 + mono 2 2 c.b2 + mono 3 2 c.b3

def delta (c : Parameters K) : K := c.b2^2 - 3*c.b3*c.b1

def affinePartner (a e : K) : Poly (R := K) := mono 1 1 a + mono 0 1 e

def Static (F G : Poly (R := K)) : Prop :=
  contraction 3 F G = 0 ∧ contraction 5 F G = 0

def Refinement (F : Poly (R := K)) (r : ℕ) (G : Poly (R := K)) : Prop :=
  ∀ i ≤ r, Static F ((contraction 1 F)^[i] G)

private theorem mono_add_same (i j : ℕ) (a b : K) :
    mono i j (a+b) = mono i j a + mono i j b :=
  map_add (monomial (exponent i j)) a b

private theorem mono_neg (i j : ℕ) (a : K) : mono i j (-a) = -mono i j a :=
  map_neg (monomial (exponent i j)) a

/-- The fifth gate on every polynomial observable, including the new cubic-B term. -/
theorem first_gate (c : Parameters K) (G : Poly (R := K)) :
    contraction 1 (H c) G =
      (mono 0 0 c.h1 + mono 1 0 (2*c.h2) + mono 2 0 (3*c.h3) +
        mono 3 0 (4*c.h4) + mono 4 0 (5*c.h5) + mono 5 0 (6*c.h6) +
        mono 0 1 c.a1 + mono 0 2 c.b1 + mono 1 2 (2*c.b2) +
        mono 2 2 (3*c.b3)) * mixed 0 1 G -
      (mono 0 0 c.a0 + mono 1 0 c.a1 + mono 0 1 (2*c.b0) +
        mono 1 1 (2*c.b1) + mono 2 1 (2*c.b2) + mono 3 1 (2*c.b3)) * mixed 1 0 G := by
  norm_num [H, contraction, List.range_succ, Nat.choose, mixed_add, mixed_mono,
    falling, add_mul, mul_add, ← mono_neg, ← mono_add_same]
  simp only [mono_eq_X, map_mul, map_neg, map_ofNat]
  ring

/-- The fifth gate on every polynomial observable, including the new cubic-B term. -/
theorem fifth_gate (c : Parameters K) (G : Poly (R := K)) :
    contraction 5 (H c) G =
      (mono 1 0 (720*c.h6) + mono 0 0 (120*c.h5)) * mixed 0 5 G +
      mono 0 0 (120*c.b3) * mixed 2 3 G := by
  norm_num [H, contraction, List.range_succ, Nat.choose, mixed_add, mixed_mono,
    falling, add_mul, mul_add, ← mono_neg, ← mono_add_same]
  simp only [mono_eq_X, map_mul, map_neg, map_ofNat]
  ring

/-- The third gate includes B'' and B''' even though A remains affine. -/
theorem third_gate (c : Parameters K) (G : Poly (R := K)) :
    contraction 3 (H c) G =
      (mono 3 0 (120*c.h6) + mono 2 0 (60*c.h5) + mono 1 0 (24*c.h4) +
        mono 0 0 (6*c.h3) + mono 0 2 (6*c.b3)) * mixed 0 3 G -
      (mono 1 1 (36*c.b3) + mono 0 1 (12*c.b2)) * mixed 1 2 G +
      (mono 2 0 (18*c.b3) + mono 1 0 (12*c.b2) + mono 0 0 (6*c.b1)) * mixed 2 1 G := by
  norm_num [H, contraction, List.range_succ, Nat.choose, mixed_add, mixed_mono,
    falling, add_mul, mul_add, ← mono_neg, ← mono_add_same]
  simp only [mono_eq_X, map_mul, map_neg, map_ofNat]
  ring

theorem affinePartner_static (c : Parameters K) (a e : K) :
    Static (H c) (affinePartner a e) := by
  simp only [Static, third_gate, fifth_gate, affinePartner, mixed_add, mixed_mono]
  norm_num [falling]

def firstPartner (c : Parameters K) (a e : K) : Poly (R := K) :=
  mono 0 0 (e*c.h1) + mono 1 0 (a*c.h1+2*e*c.h2) +
  mono 2 0 (2*a*c.h2+3*e*c.h3) + mono 3 0 (3*a*c.h3+4*e*c.h4) +
  mono 4 0 (4*a*c.h4+5*e*c.h5) + mono 5 0 (5*a*c.h5+6*e*c.h6) +
  mono 6 0 (6*a*c.h6) + mono 0 1 (e*c.a1-a*c.a0) +
  mono 0 2 (e*c.b1-2*a*c.b0) + mono 1 2 (2*e*c.b2-a*c.b1) +
  mono 2 2 (3*e*c.b3) + mono 3 2 (a*c.b3)

theorem poisson_affinePartner (c : Parameters K) (a e : K) :
    contraction 1 (H c) (affinePartner a e) = firstPartner c a e := by
  norm_num [H, affinePartner, firstPartner, contraction, List.range_succ,
    Nat.choose, mixed_add, mixed_mono, falling, add_mul, mul_add,
    ← mono_neg, ← mono_add_same]
  simp only [mono_eq_X, map_mul, map_add, map_sub, map_neg, map_ofNat]
  ring

/-- Exact coefficient equations for every affine-in-q momentum partner. -/
theorem first_third_gate (c : Parameters K) (a e : K) :
    contraction 3 (H c) (contraction 1 (H c) (affinePartner a e)) =
      mono 2 1 (72*c.b3*(a*c.b2-3*e*c.b3)) +
      mono 1 1 (144*c.b3*(a*c.b1-e*c.b2)) +
      mono 0 1 (24*(a*c.b1*c.b2+e*(3*c.b1*c.b3-2*c.b2^2))) := by
  rw [poisson_affinePartner, third_gate]
  norm_num [firstPartner, mixed_add, mixed_mono, falling,
    add_mul, mul_add, ← mono_neg, ← mono_add_same]
  simp only [mono_eq_X, map_mul, map_add, map_sub, map_neg, map_pow, map_ofNat]
  ring

theorem first_fifth_gate (c : Parameters K) (a e : K) :
    contraction 5 (H c) (contraction 1 (H c) (affinePartner a e)) = 0 := by
  rw [poisson_affinePartner, fifth_gate]
  norm_num [firstPartner, mixed_add, mixed_mono, falling]

theorem affinePartner_first_iff_coefficients (c : Parameters K) (a e : K) :
    FirstRefinement (H c) (affinePartner a e) ↔
      72*c.b3*(a*c.b2-3*e*c.b3)=0 ∧
      144*c.b3*(a*c.b1-e*c.b2)=0 ∧
      24*(a*c.b1*c.b2+e*(3*c.b1*c.b3-2*c.b2^2))=0 := by
  have hs := affinePartner_static c a e
  simp only [FirstRefinement, hs.1, hs.2, first_third_gate, first_fifth_gate,
    and_true, true_and]
  constructor
  · intro hz
    have h2 := congrArg (coeff (exponent 2 1)) hz
    have h1 := congrArg (coeff (exponent 1 1)) hz
    have h0 := congrArg (coeff (exponent 0 1)) hz
    norm_num only [coeff_add, coeff_zero, coeff_mono, and_self,
      and_true, true_and, false_and, and_false, if_true, if_false,
      zero_add, add_zero] at h2 h1 h0
    exact ⟨h2,h1,h0⟩
  · rintro ⟨h2,h1,h0⟩
    simp [h2,h1,h0]

/-- The cubic exceptional equations for the actual differential first refinement. -/
theorem cubic_affinePartner_iff (c : Parameters K) (hb : c.b3 ≠ 0) (a e : K) :
    FirstRefinement (H c) (affinePartner a e) ↔
      a*c.b2=3*e*c.b3 ∧ a*delta c=0 := by
  rw [affinePartner_first_iff_coefficients]
  have h72 : (72 : K)*c.b3 ≠ 0 := mul_ne_zero (by norm_num) hb
  have h144 : (144 : K)*c.b3 ≠ 0 := mul_ne_zero (by norm_num) hb
  constructor
  · rintro ⟨h2,h1,_⟩
    have he := (mul_eq_zero.mp h2).resolve_left h72
    have hf := (mul_eq_zero.mp h1).resolve_left h144
    refine ⟨sub_eq_zero.mp he, ?_⟩
    dsimp [delta]
    linear_combination c.b2*he-3*c.b3*hf
  · rintro ⟨he,hd⟩
    have h3b : (3 : K)*c.b3 ≠ 0 := mul_ne_zero (by norm_num) hb
    have hf : a*c.b1-e*c.b2=0 := by
      apply (mul_eq_zero.mp (show (3*c.b3)*(a*c.b1-e*c.b2)=0 by
        dsimp [delta] at hd
        linear_combination c.b2*he-hd)).resolve_left h3b
    have hed : e*delta c=0 := by
      apply (mul_eq_zero.mp (show (3*c.b3)*(e*delta c)=0 by
        linear_combination c.b2*hd-delta c*he)).resolve_left h3b
    refine ⟨by rw [he]; ring, by rw [hf]; ring, ?_⟩
    dsimp [delta] at hed
    linear_combination 24*c.b2*hf-24*hed

/-- On cubic B, a nonzero affine partner exists exactly on the discriminant of B'. -/
theorem cubic_exceptional_locus (c : Parameters K) (hb : c.b3 ≠ 0) :
    (∃ a e : K, a ≠ 0 ∧ FirstRefinement (H c) (affinePartner a e)) ↔ delta c=0 := by
  constructor
  · rintro ⟨a,e,ha,h⟩
    exact (mul_eq_zero.mp ((cubic_affinePartner_iff c hb a e).mp h).2).resolve_left ha
  · intro hd
    refine ⟨1,c.b2/(3*c.b3),one_ne_zero,?_⟩
    apply (cubic_affinePartner_iff c hb _ _).mpr
    constructor
    · have h3b : (3 : K)*c.b3 ≠ 0 := mul_ne_zero (by norm_num) hb
      field_simp; ring
    · simp [hd]

theorem cubic_centered_partner_iff (c : Parameters K) (hb : c.b3 ≠ 0) :
    FirstRefinement (H c) (affinePartner 1 (c.b2/(3*c.b3))) ↔ delta c=0 := by
  rw [cubic_affinePartner_iff c hb]
  have he : (1:K)*c.b2=3*(c.b2/(3*c.b3))*c.b3 := by field_simp; ring
  simp [he]

theorem quadratic_affinePartner_iff (c : Parameters K)
    (hb3 : c.b3=0) (hb2 : c.b2≠0) (a e : K) :
    FirstRefinement (H c) (affinePartner a e) ↔ a*c.b1=2*e*c.b2 := by
  rw [affinePartner_first_iff_coefficients]
  simp only [hb3, mul_zero, zero_mul, sub_zero, zero_sub, true_and]
  have h24 : (24:K)*c.b2≠0 := mul_ne_zero (by norm_num) hb2
  have he : 24*(a*c.b1*c.b2+e*(-(2*c.b2^2)))=(24*c.b2)*(a*c.b1-2*e*c.b2) := by ring
  rw [he]
  simp [h24, sub_eq_zero]

theorem quadratic_centered_partner (c : Parameters K)
    (hb3 : c.b3=0) (hb2 : c.b2≠0) :
    FirstRefinement (H c) (affinePartner 1 (c.b1/(2*c.b2))) := by
  apply (quadratic_affinePartner_iff c hb3 hb2 _ _).mpr
  field_simp; ring

end SexticC3.NonlinearB
