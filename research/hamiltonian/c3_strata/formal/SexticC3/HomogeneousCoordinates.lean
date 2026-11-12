import SexticC3.PolynomialBridge
import SexticC3.Covariance
import Mathlib.RingTheory.MvPolynomial.Homogeneous

noncomputable section

namespace SexticC3.Differential

open MvPolynomial

variable {R : Type*} [CommRing R]

theorem exponent_degree (e : Bool →₀ ℕ) : e.degree = e false + e true := by
  classical
  change e.sum (fun _ x => x) = _
  rw [Finsupp.sum_fintype e (fun _ x => x) (fun _ => rfl), Fintype.sum_bool, Nat.add_comm]

private theorem sum_range_lookup (f : ℕ → R) (i m : ℕ) :
    ((List.range m).map (fun j => if j = i then f j else 0)).sum =
      if i < m then f i else 0 := by
  induction m with
  | zero => simp
  | succ m ih =>
    rw [List.range_succ, List.map_append, List.sum_append, ih]
    by_cases he : m = i
    · subst i
      simp
    · have hi : i < m + 1 ↔ i < m := by omega
      simp [he, hi]

theorem coeff_homogeneous (n u v : ℕ) (g : ℕ → R) :
    coeff (exponent u v) (homogeneous n g) =
      if u + v = n then g u else 0 := by
  rw [homogeneous, coeff_list_sum]
  simp only [List.map_map, Function.comp_def, coeff_mono]
  by_cases hv : n-u = v
  · have he : ∀ j, (j = u ∧ n-j = v) ↔ j = u := by
      intro j
      constructor
      · exact And.left
      · intro h
        exact ⟨h, h.symm ▸ hv⟩
    simp only [he, sum_range_lookup]
    have hh : u < n + 1 ↔ u + v = n := by omega
    simp only [hh]
  · have he : ∀ j, ¬ (j = u ∧ n-j = v) := by
      rintro j ⟨rfl, h⟩
      exact hv h
    have hh : u + v ≠ n := by omega
    simp [he, hh]

/-- Every homogeneous binary polynomial has the coefficient-vector presentation
used by the differential bridge. -/
theorem homogeneous_of_isHomogeneous (n : ℕ) (F : Poly (R := R))
    (hF : F.IsHomogeneous n) :
    homogeneous n (fun j => coeff (exponent j (n-j)) F) = F := by
  apply MvPolynomial.ext
  intro e
  rw [← exponent_eta e, coeff_homogeneous]
  have he : (exponent (e false) (e true)).degree = e false + e true := by
    simp [exponent_degree]
  split_ifs with h
  · rw [show n - e false = e true by omega]
  · exact (hF.coeff_eq_zero (he.trans_ne h)).symm

theorem isHomogeneous_linearSub (a b c d : R) (n : ℕ) (F : Poly (R := R))
    (hF : F.IsHomogeneous n) :
    (linearSub a b c d F).IsHomogeneous n := by
  let v : Bool → Poly (R := R) := fun i =>
    if i then C c * X false + C d * X true else C a * X false + C b * X true
  have hv : ∀ i, (v i).IsHomogeneous 1 := by
    intro i
    cases i <;> simp only [v, Bool.false_eq_true, if_false, if_true] <;>
      exact ((isHomogeneous_X R false).C_mul _).add ((isHomogeneous_X R true).C_mul _)
  change (aeval v F).IsHomogeneous n
  simpa only [one_mul] using hF.aeval v hv

end SexticC3.Differential
