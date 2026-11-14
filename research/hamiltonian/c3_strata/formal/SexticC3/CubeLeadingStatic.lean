import SexticC3.CubeLeadingNewton
import SexticC3.CubeLeadingGate

/-!
# Coefficients of the transported cube-leading static equations

The operators below use actual Mathlib partial derivatives in the `(q,P)`
chart. Their relation to the original-coordinate flat contractions is a
separate chart-transport obligation.
-/
noncomputable section
set_option linter.unusedSectionVars false
namespace SexticC3.CubeLeading.Polynomial
open MvPolynomial
variable {K : Type*} [Field K] [CharZero K]

/-- Exponent of `q^i P^j`. -/
def exponent (i j : ℕ) : Fin 2 →₀ ℕ :=
  Finsupp.single 0 i + Finsupp.single 1 j

@[simp] lemma exponent_zero (i j : ℕ) : exponent i j 0 = i := by simp [exponent]
@[simp] lemma exponent_one (i j : ℕ) : exponent i j 1 = j := by simp [exponent]

lemma exponent_ext (m : Fin 2 →₀ ℕ) : exponent (m 0) (m 1) = m := by
  ext x
  fin_cases x <;> simp

lemma exponent_injective : Function.Injective (fun x : ℕ × ℕ => exponent x.1 x.2) := by
  intro a b h
  exact Prod.ext (by simpa using congrArg (fun m => m 0) h)
    (by simpa using congrArg (fun m => m 1) h)

@[simp] lemma exponent_eq (i j r s : ℕ) : exponent i j = exponent r s ↔ i = r ∧ j = s :=
  ⟨fun h => ⟨by simpa using congrArg (fun m => m 0) h,
    by simpa using congrArg (fun m => m 1) h⟩, by rintro ⟨rfl, rfl⟩; rfl⟩

def bicoeff (i j : ℕ) (f : Poly K) : K := coeff (exponent i j) f

@[simp] lemma bicoeff_add (i j : ℕ) (f g : Poly K) :
    bicoeff i j (f + g) = bicoeff i j f + bicoeff i j g := coeff_add _ _ _
@[simp] lemma bicoeff_sub (i j : ℕ) (f g : Poly K) :
    bicoeff i j (f - g) = bicoeff i j f - bicoeff i j g := coeff_sub _ _ _ _
@[simp] lemma bicoeff_zero (i j : ℕ) : bicoeff i j (0 : Poly K) = 0 := rfl
@[simp] lemma bicoeff_C_mul (i j : ℕ) (c : K) (f : Poly K) :
    bicoeff i j (C c * f) = c * bicoeff i j f := coeff_C_mul _ _ _

lemma coeff_X_pderiv (m : Fin 2 →₀ ℕ) (i : Fin 2) (f : Poly K) :
    coeff m (X i * pderiv i f) = (m i : K) * coeff m f := by
  classical
  induction f using MvPolynomial.induction_on' with
  | monomial n c =>
    rw [X_mul_pderiv_monomial, nsmul_eq_mul,
      show (n i : Poly K) = C (n i : K) by simp, coeff_C_mul]
    by_cases hn : n = m
    · subst n; simp [nsmul_eq_mul]
    · simp [nsmul_eq_mul, coeff_monomial, hn]
  | add f g hf hg =>
    simp only [map_add, mul_add, coeff_add] at *
    linear_combination hf + hg

lemma coeff_pderiv (m : Fin 2 →₀ ℕ) (i : Fin 2) (f : Poly K) :
    coeff m (pderiv i f) = ((m i : K) + 1) * coeff (Finsupp.single i 1 + m) f := by
  rw [← coeff_X_mul m i (pderiv i f), coeff_X_pderiv]
  simp [add_comm]

@[simp] lemma bicoeff_dq (i j : ℕ) (f : Poly K) :
    bicoeff i j (pderiv 0 f) = ((i : K) + 1) * bicoeff (i+1) j f := by
  have he : Finsupp.single 0 1 + exponent i j = exponent (i+1) j := by
    ext x; fin_cases x <;> simp [add_comm]
  simp [bicoeff, coeff_pderiv, he]

@[simp] lemma bicoeff_dP (i j : ℕ) (f : Poly K) :
    bicoeff i j (pderiv 1 f) = ((j : K) + 1) * bicoeff i (j+1) f := by
  have he : Finsupp.single 1 1 + exponent i j = exponent i (j+1) := by
    ext x; fin_cases x <;> simp [add_comm]
  simp [bicoeff, coeff_pderiv, he]

@[simp] lemma bicoeff_q_mul (i j : ℕ) (f : Poly K) :
    bicoeff i j (X 0 * f) = if i = 0 then 0 else bicoeff (i-1) j f := by
  have he : exponent i j - Finsupp.single 0 1 = exponent (i-1) j := by
    ext x; fin_cases x <;> simp
  simp [bicoeff, coeff_X_mul', Finsupp.mem_support_iff, he]

@[simp] lemma bicoeff_P_mul (i j : ℕ) (f : Poly K) :
    bicoeff i j (X 1 * f) = if j = 0 then 0 else bicoeff i (j-1) f := by
  have he : exponent i j - Finsupp.single 1 1 = exponent i (j-1) := by
    ext x; fin_cases x <;> simp
  simp [bicoeff, coeff_X_mul', Finsupp.mem_support_iff, he]

/-- The parameters actually occurring in the third and fifth static gates. -/
structure GateParameters (K : Type*) where
  b₁ : K
  b₂ : K
  b₃ : K
  c₃ : K
  c₄ : K
  c₅ : K

/-- `-T₃/6` in the nonlinear chart. This is NOT the flat contraction in `(q,P)`. -/
def thirdGate (t : GateParameters K) (f : Poly K) : Poly K :=
  pderiv 0 (pderiv 0 (pderiv 0 f)) +
  C 6 * pderiv 0 (pderiv 1 f) +
  C 6 * (X 1 * pderiv 0 (pderiv 1 (pderiv 1 f))) +
  C t.b₂ * pderiv 0 (pderiv 1 (pderiv 1 f)) +
  C (3*t.b₃) * (X 0 * pderiv 0 (pderiv 1 (pderiv 1 f))) -
  C t.b₃ * (X 1 * pderiv 1 (pderiv 1 (pderiv 1 f))) -
  C (t.b₁+t.c₃) * pderiv 1 (pderiv 1 (pderiv 1 f)) -
  C (2*t.b₂+4*t.c₄) * (X 0 * pderiv 1 (pderiv 1 (pderiv 1 f))) -
  C (3*t.b₃+10*t.c₅) * (X 0 * (X 0 * pderiv 1 (pderiv 1 (pderiv 1 f))))

/-- `-T₅/120`. Multiplying the equation by a nonzero scalar changes no kernel. -/
def fifthGate (t : GateParameters K) (f : Poly K) : Poly K :=
  C 3 * pderiv 0 (pderiv 1 (pderiv 1 (pderiv 1 (pderiv 1 f)))) -
  C (t.b₃+t.c₅) * pderiv 1 (pderiv 1 (pderiv 1 (pderiv 1 (pderiv 1 f))))

/-- The actual two differential equations in the chart. -/
def Static (t : GateParameters K) (f : Poly K) : Prop :=
  thirdGate t f = 0 ∧ fifthGate t f = 0

/-- The fifth-gate recurrence, for every pair of coefficient indices. -/
theorem fifth_recurrence (t : GateParameters K) (f : Poly K) (hf : Static t f)
    (i j : ℕ) :
    3 * ((i : K)+1) * bicoeff (i+1) (j+4) f =
      (t.b₃+t.c₅) * ((j : K)+5) * bicoeff i (j+5) f := by
  have h := congrArg (bicoeff i j) hf.2
  simp only [fifthGate, bicoeff_sub, bicoeff_C_mul, bicoeff_dq, bicoeff_dP,
    bicoeff_zero] at h
  push_cast at h
  have hn (r : ℕ) (hr : r ≠ 0) : (r : K) ≠ 0 := Nat.cast_ne_zero.mpr hr
  have h1 : (j : K)+1 ≠ 0 := by exact_mod_cast (show j+1 ≠ 0 by omega)
  have h2 : (j : K)+2 ≠ 0 := by exact_mod_cast (show j+2 ≠ 0 by omega)
  have h3 : (j : K)+3 ≠ 0 := by exact_mod_cast (show j+3 ≠ 0 by omega)
  have h4 : (j : K)+4 ≠ 0 := by exact_mod_cast (show j+4 ≠ 0 by omega)
  apply (mul_left_cancel₀ (mul_ne_zero (mul_ne_zero (mul_ne_zero h1 h2) h3) h4))
  linear_combination h


lemma bicoeff_q_dq (i j : ℕ) (f : Poly K) :
    bicoeff i j (X 0 * pderiv 0 f) = (i : K) * bicoeff i j f := by
  simpa [bicoeff] using coeff_X_pderiv (exponent i j) 0 f

lemma bicoeff_P_dP (i j : ℕ) (f : Poly K) :
    bicoeff i j (X 1 * pderiv 1 f) = (j : K) * bicoeff i j f := by
  simpa [bicoeff] using coeff_X_pderiv (exponent i j) 1 f

lemma bicoeff_P_dq_dPP (i j : ℕ) (f : Poly K) :
    bicoeff i j (X 1 * pderiv 0 (pderiv 1 (pderiv 1 f))) =
      (j : K)*((j : K)+1)*((i : K)+1)*bicoeff (i+1) (j+1) f := by
  cases j with
  | zero => simp
  | succ j => simp; ring

/-- The complete third-gate coefficient recurrence, without a degree cutoff. -/
theorem third_recurrence (t : GateParameters K) (f : Poly K) (hf : Static t f)
    (i j : ℕ) :
    ((i : K)+1)*((i : K)+2)*((i : K)+3)*bicoeff (i+3) j f +
    6*((j : K)+1)^2*((i : K)+1)*bicoeff (i+1) (j+1) f +
    t.b₂*((j : K)+1)*((j : K)+2)*((i : K)+1)*bicoeff (i+1) (j+2) f +
    t.b₃*((j : K)+1)*((j : K)+2)*(3*(i : K)-(j : K))*bicoeff i (j+2) f -
    ((j : K)+1)*((j : K)+2)*((j : K)+3)*
      ((t.b₁+t.c₃)*bicoeff i (j+3) f +
       (2*t.b₂+4*t.c₄)*(if i = 0 then 0 else bicoeff (i-1) (j+3) f) +
       (3*t.b₃+10*t.c₅)*(if i < 2 then 0 else bicoeff (i-2) (j+3) f)) = 0 := by
  have h := congrArg (bicoeff i j) hf.1
  simp only [thirdGate, bicoeff_add, bicoeff_sub, bicoeff_C_mul,
    bicoeff_P_dq_dPP, bicoeff_q_dq, bicoeff_P_dP,
    bicoeff_q_mul, bicoeff_dq, bicoeff_dP, bicoeff_zero] at h
  rcases i with _ | _ | i
  · norm_num at h ⊢
    linear_combination h
  · norm_num at h ⊢
    linear_combination h
  · have hi : ¬ i+1+1 < 2 := by omega
    norm_num [hi, Nat.add_assoc] at h ⊢
    linear_combination h

lemma bicoeff_vanish_of_bound {w : Fin 2 → ℕ} {n : ℤ} {f : Poly K}
    (hf : Bounded w n f) (i j : ℕ)
    (hij : n < (w 0 : ℤ)*i + (w 1 : ℤ)*j) : bicoeff i j f = 0 := by
  by_contra hc
  have hm := hf (exponent i j) hc
  simp only [weight_pair, exponent_zero, exponent_one] at hm
  omega

lemma bicoeff_component (w : Fin 2 → ℕ) (n : ℤ) (f : Poly K) (i j : ℕ)
    (hij : (w 0 : ℤ)*i + (w 1 : ℤ)*j = n) :
    bicoeff i j (component w n f) = bicoeff i j f := by
  simp [bicoeff, coeff_weightedHomogeneousComponent, weight_pair, hij]

lemma bicoeff_monomial (i j r s : ℕ) (c : K) :
    bicoeff i j (monomial (exponent r s) c) = if r = i ∧ s = j then c else 0 := by
  simp [bicoeff, coeff_monomial]

lemma qP_monomial (r s : ℕ) (c : K) :
    C c * (X 0 : Poly K)^r * X 1^s = monomial (exponent r s) c := by
  simp [X_pow_eq_monomial, C_mul_monomial, monomial_mul, exponent]

lemma square_one_expansion (c a : K) :
    C a * (caseOne c)^2 = monomial (exponent 0 6) a +
      monomial (exponent 5 3) (2*a*c) + monomial (exponent 10 0) (a*c^2) := by
  simp only [← qP_monomial, caseOne, map_mul, map_pow, map_ofNat]
  ring

lemma square_two_expansion (c a : K) :
    C a * (caseTwo c)^2 = monomial (exponent 0 6) a +
      monomial (exponent 3 4) (2*a*c) + monomial (exponent 6 2) (a*c^2) := by
  simp only [← qP_monomial, caseTwo, map_mul, map_pow, map_ofNat]
  ring

lemma square_three_expansion (c a : K) :
    C a * (caseThree c)^2 = monomial (exponent 0 6) a +
      monomial (exponent 4 3) (2*a*c) + monomial (exponent 8 0) (a*c^2) := by
  simp only [← qP_monomial, caseThree, map_mul, map_pow, map_ofNat]
  ring

end SexticC3.CubeLeading.Polynomial
