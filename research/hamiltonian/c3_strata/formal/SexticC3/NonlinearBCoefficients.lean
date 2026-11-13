import SexticC3.SimpleRootChart

noncomputable section
namespace SexticC3.NonlinearB
open MvPolynomial Differential
variable {K : Type*} [Field K] [CharZero K]

abbrev cf (G : Poly (R := K)) (i j : ℕ) : K := coeff (exponent i j) G

@[simp] theorem cf_add (G F : Poly (R := K)) (i j : ℕ) :
    cf (G+F) i j=cf G i j+cf F i j := coeff_add _ _ _
@[simp] theorem cf_sub (G F : Poly (R := K)) (i j : ℕ) :
    cf (G-F) i j=cf G i j-cf F i j := coeff_sub _ _ _ _
@[simp] theorem cf_zero (i j : ℕ) : cf (0 : Poly (R := K)) i j=0 := coeff_zero _

theorem at_q_derivative (G : Poly (R := K)) (i j : ℕ) :
    cf (pderiv false G) i j = cf G (i+1) j * (i+1 : ℕ) := by
  induction G using MvPolynomial.induction_on' with
  | monomial m c =>
    rw [← exponent_eta m]
    change cf (pderiv false (mono (m false) (m true) c)) i j =
      cf (mono (m false) (m true) c) (i+1) j * (i+1 : ℕ)
    rw [pderiv_q_mono]
    simp only [cf, coeff_mono]
    by_cases hz : m false=0
    · simp [hz]
    · have he : m false-1=i ↔ m false=i+1 := by omega
      simp only [he]
      split_ifs with h
      · rw [h.1, Nat.cast_add, Nat.cast_one]
      · simp
  | add F G ihF ihG => simp [cf, ihF, ihG, add_mul] at *

theorem at_p_derivative (G : Poly (R := K)) (i j : ℕ) :
    cf (pderiv true G) i j = cf G i (j+1) * (j+1 : ℕ) := by
  induction G using MvPolynomial.induction_on' with
  | monomial m c =>
    rw [← exponent_eta m]
    change cf (pderiv true (mono (m false) (m true) c)) i j =
      cf (mono (m false) (m true) c) i (j+1) * (j+1 : ℕ)
    rw [pderiv_p_mono]
    simp only [cf, coeff_mono]
    by_cases hz : m true=0
    · simp [hz]
    · have he : m true-1=j ↔ m true=j+1 := by omega
      simp only [he]
      split_ifs with h
      · rw [h.2, Nat.cast_add, Nat.cast_one]
      · simp
  | add F G ihF ihG => simp [cf, ihF, ihG, add_mul] at *

theorem at_mono_mul (G : Poly (R := K)) (i j u v : ℕ) (c : K) :
    cf (mono u v c * G) i j =
      if u ≤ i ∧ v ≤ j then c*cf G (i-u) (j-v) else 0 := by
  have he : exponent u v ≤ exponent i j ↔ u ≤ i ∧ v ≤ j := by
    constructor
    · intro h
      exact ⟨by simpa using h false, by simpa using h true⟩
    · rintro ⟨hu,hv⟩ x
      cases x <;> simp [hu,hv]
  have hs : exponent i j-exponent u v=exponent (i-u) (j-v) := by
    ext x
    cases x <;> simp [exponent]
  simp only [cf, mono, coeff_monomial_mul', he, hs]

theorem at_above_p_degree (G : Poly (R := K)) (i j : ℕ) (h : G.degreeOf true < j) :
    cf G i j=0 := by
  by_contra hn
  have hs : exponent i j ∈ G.support := mem_support_iff.mpr hn
  have hd := monomial_le_degreeOf true hs
  simp only [exponent_true] at hd
  omega

theorem at_above_q_degree (G : Poly (R := K)) (i j : ℕ) (h : G.degreeOf false < i) :
    cf G i j=0 := by
  by_contra hn
  have hs : exponent i j ∈ G.support := mem_support_iff.mpr hn
  have hd := monomial_le_degreeOf false hs
  simp only [exponent_false] at hd
  omega

/-- Descending coefficient elimination on a finite-support polynomial column. -/
theorem column_elimination (G : Poly (R := K)) (j bound : ℕ)
    (pivot : ∀ n, bound ≤ n → (∀ m, n<m → cf G m j=0) → cf G n j=0) :
    ∀ i, bound ≤ i → cf G i j=0 := by
  have aux (k : ℕ) : ∀ i, G.degreeOf false < i+k → bound ≤ i → cf G i j=0 := by
    induction k with
    | zero =>
      intro i hi _
      exact at_above_q_degree G i j (by omega)
    | succ k ih =>
      intro i hi hb
      apply pivot i hb
      intro m hm
      apply ih m <;> omega
  intro i hi
  exact aux (G.degreeOf false+1) i (by omega) hi

end SexticC3.NonlinearB
