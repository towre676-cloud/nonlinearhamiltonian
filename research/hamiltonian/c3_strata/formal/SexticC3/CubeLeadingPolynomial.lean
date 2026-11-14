import SexticC3.CubeLeadingNoSlice
import Mathlib.RingTheory.MvPolynomial.EulerIdentity
import Mathlib.RingTheory.Polynomial.UniqueFactorization
import Mathlib.RingTheory.Coprime.Lemmas
import Mathlib.Algebra.MvPolynomial.Division
import Mathlib.LinearAlgebra.FiniteDimensional.Defs
import Mathlib.Algebra.CharP.Algebra
import Mathlib.Algebra.Algebra.Rat

/-!
# Polynomial realization of the weighted no-slice argument

The operators in this file are Mathlib's actual formal partial derivatives on
`MvPolynomial (Fin 2) K`. Variable 0 is q; variable 1 is P.
-/

noncomputable section
set_option linter.unusedSectionVars false
namespace SexticC3.CubeLeading.Polynomial
open MvPolynomial

variable {K : Type*} [Field K] [CharZero K]
abbrev Poly (K : Type*) [CommSemiring K] := MvPolynomial (Fin 2) K

instance polyCharZero : CharZero (Poly K) :=
  charZero_of_injective_ringHom (f := C) (C_injective _ _)

def weights (w : Fin 2 → ℕ) : Fin 2 → ℤ := fun i => w i

def euler (w : Fin 2 → ℕ) (f : Poly K) : Poly K :=
  (w 0 : Poly K) * (X 0 * pderiv 0 f) + (w 1 : Poly K) * (X 1 * pderiv 1 f)

def bracket (h f : Poly K) : Poly K :=
  pderiv 0 h * pderiv 1 f - pderiv 1 h * pderiv 0 f

lemma weight_pair (w : Fin 2 → ℕ) (m : Fin 2 →₀ ℕ) :
    Finsupp.weight (weights w) m = (w 0 : ℤ) * m 0 + (w 1 : ℤ) * m 1 := by
  simp [Finsupp.weight_apply, Finsupp.sum_fintype, Fin.sum_univ_two, weights,
    nsmul_eq_mul, mul_comm]

lemma euler_monomial (w : Fin 2 → ℕ) (m : Fin 2 →₀ ℕ) (c : K) :
    euler w (monomial m c) =
      C ((Finsupp.weight (weights w) m : ℤ) : K) * monomial m c := by
  simp only [euler, X_mul_pderiv_monomial, nsmul_eq_mul, weight_pair]
  push_cast
  simp only [map_add, map_mul, map_natCast]
  ring

lemma coeff_euler (w : Fin 2 → ℕ) (f : Poly K) (m : Fin 2 →₀ ℕ) :
    coeff m (euler w f) = (Finsupp.weight (weights w) m : K) * coeff m f := by
  classical
  induction f using MvPolynomial.induction_on' with
  | monomial n c =>
    rw [euler_monomial, coeff_C_mul]
    by_cases hn : n = m
    · subst n; rfl
    · simp [coeff_monomial, hn]
  | add f g hf hg =>
    simp only [euler, map_add, mul_add, coeff_add] at *
    linear_combination hf + hg

lemma form_iff (w : Fin 2 → ℕ) (f : Poly K) (n : ℤ) :
    euler w f = (n : Poly K) * f ↔ f.IsWeightedHomogeneous (weights w) n := by
  constructor
  · intro hf m hm
    have he := congrArg (coeff m) hf
    rw [coeff_euler] at he
    have hn : (n : Poly K) = C (n : K) := by simp
    rw [hn, coeff_C_mul] at he
    have he' := mul_right_cancel₀ hm he
    exact_mod_cast he'
  · intro hf
    ext m
    rw [coeff_euler]
    have hn : (n : Poly K) = C (n : K) := by simp
    rw [hn, coeff_C_mul]
    by_cases hm : coeff m f = 0
    · simp [hm]
    · rw [hf hm]

lemma negative_form (w : Fin 2 → ℕ) (n : ℤ) (hn : n < 0) (f : Poly K)
    (hf : euler w f = (n : Poly K) * f) : f = 0 := by
  apply MvPolynomial.ext
  intro m
  simp only [coeff_zero]
  by_contra hm
  have he := (form_iff w f n).mp hf hm
  rw [weight_pair] at he
  have hnonneg : (0 : ℤ) ≤ (w 0 : ℤ) * m 0 + (w 1 : ℤ) * m 1 := by positivity
  omega

lemma euler_mul (w : Fin 2 → ℕ) (f g : Poly K) :
    euler w (f * g) = euler w f * g + f * euler w g := by
  simp only [euler, pderiv_mul]
  ring

lemma bracket_mul (h f g : Poly K) :
    bracket h (f * g) = bracket h f * g + f * bracket h g := by
  simp only [bracket, pderiv_mul]
  ring

lemma bracket_form (w : Fin 2 → ℕ) (h f : Poly K) (d n : ℤ)
    (hh : h.IsWeightedHomogeneous (weights w) d)
    (hf : f.IsWeightedHomogeneous (weights w) n) :
    (bracket h f).IsWeightedHomogeneous (weights w) (n + (d - w 0 - w 1)) := by
  have h0 := hh.pderiv (i := 0) (n' := d - w 0) (by simp [weights])
  have h1 := hh.pderiv (i := 1) (n' := d - w 1) (by simp [weights])
  have f0 := hf.pderiv (i := 0) (n' := n - w 0) (by simp [weights])
  have f1 := hf.pderiv (i := 1) (n' := n - w 1) (by simp [weights])
  have a : (pderiv 0 h * pderiv 1 f).IsWeightedHomogeneous (weights w)
      (n + (d - w 0 - w 1)) := by convert h0.mul f1 using 1; ring
  have b : (pderiv 1 h * pderiv 0 f).IsWeightedHomogeneous (weights w)
      (n + (d - w 0 - w 1)) := by convert h1.mul f0 using 1; ring
  exact (weightedHomogeneousSubmodule K (weights w) _).sub_mem a b

/-- Every structural identity in `LeadingData` is proved for actual partial derivatives. -/
def leadingData (w : Fin 2 → ℕ) (h : Poly K) (d : ℤ)
    (hh : h.IsWeightedHomogeneous (weights w) d)
    (hpos : 0 < d - w 0 - w 1) (hlt : d - w 0 - w 1 < d) :
    LeadingData (Poly K) where
  h := h
  hP := pderiv 1 h
  qw := (w 0 : Poly K) * X 0
  D := bracket h
  Eu := euler w
  dP := pderiv 1
  d := d
  δ := d - w 0 - w 1
  D_zero := by simp [bracket]
  Eu_zero := by simp [euler]
  D_mul := by intro f; rw [bracket_mul]; simp only [bracket]; ring
  Eu_mul := by intro f; rw [euler_mul, (form_iff w h d).mpr hh]; ring
  cramer := by
    intro f
    have he := (form_iff w h d).mpr hh
    dsimp [euler] at he
    dsimp [euler, bracket]
    linear_combination (pderiv 1 f) * he
  shift := by
    intro n f hf
    exact (form_iff w _ _).mpr (bracket_form w h f d n hh ((form_iff w f n).mp hf))
  neg := by intro n f hn hf; exact negative_form w n hn f hf
  δ_pos := hpos
  δ_lt := hlt

/-- Positive variable weights force the Euler weight-zero space to be K. -/
lemma weight_zero_constant (w : Fin 2 → ℕ) (hw : ∀ i, 0 < w i) (f : Poly K)
    (hf : euler w f = 0) : f = C (coeff 0 f) := by
  classical
  ext m
  by_cases hm : m = 0
  · subst m; simp
  · rw [coeff_C, if_neg (Ne.symm hm)]
    by_contra hc
    have he := (form_iff w f 0).mp (by simpa using hf) hc
    rw [weight_pair] at he
    have h0 := hw 0
    have h1 := hw 1
    have hm0 : m 0 = 0 := by nlinarith
    have hm1 : m 1 = 0 := by nlinarith
    apply hm
    ext i
    fin_cases i <;> simp [hm0, hm1]

/-- Concrete bivariate K3, with the natural nonzero and coprimality hypotheses. -/
theorem polynomial_no_slice (w : Fin 2 → ℕ) (hw : ∀ i, 0 < w i)
    (h : Poly K) (d : ℤ) (hh : h.IsWeightedHomogeneous (weights w) d)
    (hd : (w 0 : ℤ) + w 1 < d) (hh0 : h ≠ 0) (hrel : IsRelPrime h (pderiv 1 h))
    (f : Poly K) (n : ℤ) (hf : f.IsWeightedHomogeneous (weights w) n)
    (r : ℕ) (hr : (bracket h)^[r] f = 0) :
    ∃ (k : ℕ) (c : K), f = C c * h ^ k := by
  have hpos : 0 < d - w 0 - w 1 := by omega
  have hlt : d - w 0 - w 1 < d := by have := hw 0; have := hw 1; omega
  let L := leadingData w h d hh hpos hlt
  obtain ⟨k, c, hc, he⟩ := L.no_slice hh0 hrel r n f ((form_iff w f n).mpr hf) hr
  exact ⟨k, coeff 0 c, by rw [he, ← weight_zero_constant w hw c hc]; rfl⟩

/-- The homogeneous polynomial kernel consists of scalar powers of h. -/
theorem polynomial_kernel_forms (w : Fin 2 → ℕ) (hw : ∀ i, 0 < w i)
    (h : Poly K) (d : ℤ) (hh : h.IsWeightedHomogeneous (weights w) d)
    (hd : (w 0 : ℤ) + w 1 < d) (hh0 : h ≠ 0) (hrel : IsRelPrime h (pderiv 1 h))
    (f : Poly K) (n : ℤ) (hf : f.IsWeightedHomogeneous (weights w) n)
    (hker : bracket h f = 0) : ∃ (k : ℕ) (c : K), f = C c * h^k :=
  polynomial_no_slice w hw h d hh hd hh0 hrel f n hf 1 (by simpa using hker)

/-- There is no homogeneous preimage of a nonzero scalar multiple of h^k. -/
theorem polynomial_no_preimage (w : Fin 2 → ℕ) (hw : ∀ i, 0 < w i)
    (h : Poly K) (d : ℤ) (hh : h.IsWeightedHomogeneous (weights w) d)
    (hd : (w 0 : ℤ) + w 1 < d) (hh0 : h ≠ 0) (hrel : IsRelPrime h (pderiv 1 h))
    (f : Poly K) (n : ℤ) (hf : f.IsWeightedHomogeneous (weights w) n)
    (k : ℕ) (c : K) (hc : c ≠ 0) : bracket h f ≠ C c * h^k := by
  have hpos : 0 < d - w 0 - w 1 := by omega
  have hlt : d - w 0 - w 1 < d := by have := hw 0; have := hw 1; omega
  let L := leadingData w h d hh hpos hlt
  have hC : (C c : Poly K) ≠ 0 := by simpa using hc
  exact L.no_preimage hh0 hrel k n f (C c) ((form_iff w f n).mpr hf)
    (by simp [L, leadingData, euler, pderiv_C]) hC

end SexticC3.CubeLeading.Polynomial
