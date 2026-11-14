import SexticC3.CubeLeadingStatic

/-!
# Exclusion of square leading forms

These theorems quantify over arbitrary bivariate polynomials. All coefficient
vanishings follow from the actual weighted support; no static basis or bounded
ansatz is substituted for the lower-weight corrections.
-/
noncomputable section
set_option linter.unusedSectionVars false
namespace SexticC3.CubeLeading.Polynomial
open MvPolynomial
variable {K : Type*} [Field K] [CharZero K]

lemma leadingForm_data (w : Fin 2 → ℕ) (f g : Poly K) (n : ℤ)
    (he : leadingForm w f = g) (hg : g.IsWeightedHomogeneous (weights w) n)
    (hg0 : g ≠ 0) : Bounded w n f ∧ component w n f = g := by
  obtain ⟨m, hm⟩ := MvPolynomial.ne_zero_iff.mp hg0
  have hfm : coeff m (leadingForm w f) ≠ 0 := by rwa [he]
  have hhom : (leadingForm w f).IsWeightedHomogeneous (weights w) (degree w f) :=
    weightedHomogeneousComponent_isWeightedHomogeneous _ _
  have ha := hhom hfm
  have hb := hg hm
  have hd : (degree w f : ℤ) = n := ha.symm.trans hb
  exact ⟨by simpa [hd] using bounded_degree w f, by simpa [leadingForm, hd] using he⟩

lemma constant_mul_homogeneous (w : Fin 2 → ℕ) (n : ℤ) (a : K) (f : Poly K)
    (hf : f.IsWeightedHomogeneous (weights w) n) :
    (C a * f).IsWeightedHomogeneous (weights w) n := by
  intro m hm
  rw [coeff_C_mul] at hm
  exact hf (right_ne_zero_of_mul hm)

/-- Case I: the fifth-gate recurrence and two third-gate coefficients are incompatible. -/
theorem case_one_square_excluded (t : GateParameters K) (hc : t.c₅ ≠ 0)
    (f : Poly K) (hf : Static t f) (a : K) (ha : a ≠ 0)
    (hbound : Bounded ![3, 5] 30 f)
    (htop : component ![3, 5] 30 f = C a * (caseOne t.c₅)^2) : False := by
  have zero (i j : ℕ) (hij : 30 < 3*(i : ℤ)+5*j) : bicoeff i j f = 0 :=
    bicoeff_vanish_of_bound hbound i j hij
  have h06 : bicoeff 0 6 f = a := by
    rw [← bicoeff_component ![3, 5] 30 f 0 6 (by norm_num), htop, square_one_expansion]
    simp [bicoeff_monomial]
  have h53 : bicoeff 5 3 f = 2*a*t.c₅ := by
    rw [← bicoeff_component ![3, 5] 30 f 5 3 (by norm_num), htop, square_one_expansion]
    simp [bicoeff_monomial]
  have h34 := fifth_recurrence t f hf 2 0
  have h15 := fifth_recurrence t f hf 0 1
  have h04 := third_recurrence t f hf 0 4
  have h23 := third_recurrence t f hf 2 3
  norm_num [zero 2 5 (by norm_num), zero 1 6 (by norm_num),
    zero 0 7 (by norm_num), zero 3 5 (by norm_num), zero 2 6 (by norm_num),
    h06, h53] at h34 h15 h04 h23
  have obstruction : (480 : K)*a*t.c₅ = 0 := by
    linear_combination -h23 - 2*h04 + 100*h15 + (300 : K)*h34
  exact (mul_ne_zero (mul_ne_zero (by norm_num) ha) hc) obstruction

/-- Case II is already excluded by a coefficient of the fifth gate. -/
theorem case_two_square_excluded (t : GateParameters K) (hc : t.b₃ ≠ 0)
    (f : Poly K) (hf : Static t f) (a : K) (ha : a ≠ 0)
    (hbound : Bounded ![2, 3] 18 f)
    (htop : component ![2, 3] 18 f = C a * (caseTwo t.b₃)^2) : False := by
  have h25 : bicoeff 2 5 f = 0 := bicoeff_vanish_of_bound hbound 2 5 (by norm_num)
  have h34 : bicoeff 3 4 f = 2*a*t.b₃ := by
    rw [← bicoeff_component ![2, 3] 18 f 3 4 (by norm_num), htop, square_two_expansion]
    simp [bicoeff_monomial]
  have h := fifth_recurrence t f hf 2 0
  norm_num [h25, h34] at h
  exact h.elim ha hc

/-- Case III: a coefficient of the third gate forces the nonzero q⁴ coefficient to vanish. -/
theorem case_three_square_excluded (t : GateParameters K) (hb : t.b₃ = 0)
    (h5 : t.c₅ = 0) (hc : t.c₄ ≠ 0) (f : Poly K) (hf : Static t f)
    (a : K) (ha : a ≠ 0) (hbound : Bounded ![3, 4] 24 f)
    (htop : component ![3, 4] 24 f = C a * (caseThree t.c₄)^2) : False := by
  have zero (i j : ℕ) (hij : 24 < 3*(i : ℤ)+4*j) : bicoeff i j f = 0 :=
    bicoeff_vanish_of_bound hbound i j hij
  have h43 : bicoeff 4 3 f = 2*a*t.c₄ := by
    rw [← bicoeff_component ![3, 4] 24 f 4 3 (by norm_num), htop, square_three_expansion]
    simp [bicoeff_monomial]
  have h := third_recurrence t f hf 3 2
  norm_num [hb, h5, h43, zero 6 2 (by norm_num), zero 4 4 (by norm_num),
    zero 3 5 (by norm_num), zero 2 5 (by norm_num)] at h
  exact h.elim ha hc

/-- No finite support restriction on the lower corrections is assumed. -/
theorem case_one_no_square_leading (t : GateParameters K) (hc : t.c₅ ≠ 0)
    (f : Poly K) (hf : Static t f) (a : K) (ha : a ≠ 0) :
    leadingForm ![3, 5] f ≠ C a * (caseOne t.c₅)^2 := by
  intro he
  have hh := (case_one_form t.c₅).mul (case_one_form t.c₅)
  rw [← pow_two] at hh
  obtain ⟨hb, ht⟩ := leadingForm_data ![3, 5] f _ 30 he
    (constant_mul_homogeneous _ _ a _ hh)
    (mul_ne_zero (by simpa using ha) (pow_ne_zero _ (binomial_ne_zero t.c₅ 5 (by decide))))
  exact case_one_square_excluded t hc f hf a ha hb ht

theorem case_two_no_square_leading (t : GateParameters K) (hc : t.b₃ ≠ 0)
    (f : Poly K) (hf : Static t f) (a : K) (ha : a ≠ 0) :
    leadingForm ![2, 3] f ≠ C a * (caseTwo t.b₃)^2 := by
  intro he
  have hh := (case_two_form t.b₃).mul (case_two_form t.b₃)
  rw [← pow_two] at hh
  obtain ⟨hb, ht⟩ := leadingForm_data ![2, 3] f _ 18 he
    (constant_mul_homogeneous _ _ a _ hh)
    (mul_ne_zero (by simpa using ha) (pow_ne_zero _ (linear_cubic_ne_zero t.b₃)))
  exact case_two_square_excluded t hc f hf a ha hb ht

theorem case_three_no_square_leading (t : GateParameters K) (hb : t.b₃ = 0)
    (h5 : t.c₅ = 0) (hc : t.c₄ ≠ 0) (f : Poly K) (hf : Static t f)
    (a : K) (ha : a ≠ 0) :
    leadingForm ![3, 4] f ≠ C a * (caseThree t.c₄)^2 := by
  intro he
  have hh := (case_three_form t.c₄).mul (case_three_form t.c₄)
  rw [← pow_two] at hh
  obtain ⟨hbound, ht⟩ := leadingForm_data ![3, 4] f _ 24 he
    (constant_mul_homogeneous _ _ a _ hh)
    (mul_ne_zero (by simpa using ha) (pow_ne_zero _ (binomial_ne_zero t.c₄ 4 (by decide))))
  exact case_three_square_excluded t hb h5 hc f hf a ha hbound ht

end SexticC3.CubeLeading.Polynomial
