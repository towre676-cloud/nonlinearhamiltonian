import SexticC3.CubeLeadingPolynomial

/-! # Coprimality of the three Newton leading forms, over any characteristic-zero field. -/
noncomputable section
set_option linter.unusedSectionVars false
namespace SexticC3.CubeLeading.Polynomial
open MvPolynomial
variable {K : Type*} [Field K] [CharZero K]

lemma variables_relprime : IsRelPrime (X 0 : Poly K) (X 1) := by
  have hp : Prime (X 0 : Poly K) := by
    apply (MulEquiv.prime_iff (finSuccEquiv K 1)).mp
    rw [finSuccEquiv_X_zero]
    exact Polynomial.prime_X
  exact hp.irreducible.isRelPrime_iff_not_dvd.mpr (by simp)

lemma binomial_ne_zero (c : K) (n : ℕ) (hn : n ≠ 0) :
    (X 1 : Poly K)^3 + C c * X 0^n ≠ 0 := by
  intro he
  have he' := congrArg (eval ![0, 1]) he
  simp [hn] at he'

lemma linear_cubic_ne_zero (c : K) :
    (X 1 : Poly K)^3 + C c * X 0^3 * X 1 ≠ 0 := by
  intro he
  have he' := congrArg (eval ![0, 1]) he
  simp at he'

/-- A common prime would have to divide both coordinate variables. -/
lemma binomial_coprime (c : K) (hc : c ≠ 0) (n : ℕ) (hn : n ≠ 0) :
    IsRelPrime ((X 1 : Poly K)^3 + C c * X 0^n)
      (pderiv 1 ((X 1 : Poly K)^3 + C c * X 0^n)) := by
  apply (UniqueFactorizationMonoid.isRelPrime_iff_no_prime_factors (binomial_ne_zero c n hn)).mpr
  intro t ht hd hp
  have hu : IsUnit (C c : Poly K) := (IsUnit.mk0 c hc).map C
  have h3 : IsUnit (3 : Poly K) := by simpa using (isUnit_intCast (R := Poly K) 3 (by decide))
  have hd' : t ∣ (3 : Poly K) * X 1^2 := by
    simpa [pderiv_pow, pderiv_C_mul, pderiv_X, Pi.single_apply] using hd
  have htP := hp.dvd_of_dvd_pow ((h3.dvd_mul_left).mp hd')
  have htQn : t ∣ C c * (X 0 : Poly K)^n := by
    have he := dvd_sub ht (dvd_pow htP (by decide : 3 ≠ 0))
    simpa using he
  have htQ := hp.dvd_of_dvd_pow (hu.dvd_mul_left.mp htQn)
  exact hp.not_unit (variables_relprime htQ htP)

lemma linear_cubic_coprime (c : K) (hc : c ≠ 0) :
    IsRelPrime ((X 1 : Poly K)^3 + C c * X 0^3 * X 1)
      (pderiv 1 ((X 1 : Poly K)^3 + C c * X 0^3 * X 1)) := by
  apply (UniqueFactorizationMonoid.isRelPrime_iff_no_prime_factors (linear_cubic_ne_zero c)).mpr
  intro t ht hd hp
  have hu : IsUnit (C c : Poly K) := (IsUnit.mk0 c hc).map C
  have h2 : IsUnit (2 : Poly K) := by simpa using (isUnit_intCast (R := Poly K) 2 (by decide))
  have hd' : t ∣ (3 : Poly K) * X 1^2 + C c * X 0^3 := by
    simpa [pderiv_mul, pderiv_pow, pderiv_C_mul, pderiv_X, Pi.single_apply] using hd
  have hfac : t ∣ (X 1 : Poly K) * (X 1^2 + C c * X 0^3) := by
    convert ht using 1; ring
  have htP : t ∣ (X 1 : Poly K) := by
    rcases hp.dvd_or_dvd hfac with htP | hr
    · exact htP
    · have he : t ∣ (2 : Poly K) * X 1^2 := by
        convert dvd_sub hd' hr using 1; ring
      exact hp.dvd_of_dvd_pow (h2.dvd_mul_left.mp he)
  have htQ3 : t ∣ C c * (X 0 : Poly K)^3 := by
    have he := dvd_sub hd' (dvd_mul_of_dvd_right (dvd_pow htP (by decide : 2 ≠ 0)) 3)
    simpa using he
  have htQ := hp.dvd_of_dvd_pow (hu.dvd_mul_left.mp htQ3)
  exact hp.not_unit (variables_relprime htQ htP)

def caseOne (c : K) : Poly K := X 1^3 + C c * X 0^5
def caseTwo (c : K) : Poly K := X 1^3 + C c * X 0^3 * X 1
def caseThree (c : K) : Poly K := X 1^3 + C c * X 0^4

theorem case_one_coprime (c : K) (hc : c ≠ 0) :
    IsRelPrime (caseOne c) (pderiv 1 (caseOne c)) := binomial_coprime c hc 5 (by decide)
theorem case_two_coprime (c : K) (hc : c ≠ 0) :
    IsRelPrime (caseTwo c) (pderiv 1 (caseTwo c)) := linear_cubic_coprime c hc
theorem case_three_coprime (c : K) (hc : c ≠ 0) :
    IsRelPrime (caseThree c) (pderiv 1 (caseThree c)) := binomial_coprime c hc 4 (by decide)

end SexticC3.CubeLeading.Polynomial
