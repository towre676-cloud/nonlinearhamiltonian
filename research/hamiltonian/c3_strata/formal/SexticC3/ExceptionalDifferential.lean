import SexticC3.GateTransport
import SexticC3.Exceptional411

noncomputable section

namespace SexticC3.Differential

open MvPolynomial

variable {K : Type*} [Field K]

/-- The exceptional root pattern's polynomial Hamiltonian and quadratic partner. -/
def exceptionalHamiltonian (δ : K) : Poly (R := K) := mono 4 2 1 + mono 6 0 δ

def exceptionalPartner : Poly (R := K) := mono 1 1 1

private def fromPairs (n : ℕ) (g : List (ℕ × K)) : Poly (R := K) :=
  (g.map fun (j, a) => mono j (n-j) a).sum

private theorem exceptional_partner_eq :
    (exceptionalPartner : Poly (R := K)) = fromPairs 2 Exceptional411.partner := by
  simp [exceptionalPartner, fromPairs, Exceptional411.partner]

private theorem exceptional_coefficient (δ : K) (k n u v : ℕ) (g : List (ℕ × K)) :
    coeff (exponent u v) (contraction k (exceptionalHamiltonian δ) (fromPairs n g)) =
      Exceptional411.contraction δ k n u v g := by
  unfold fromPairs Exceptional411.contraction
  induction g with
  | nil => simp
  | cons x xs ih =>
    obtain ⟨j,a⟩ := x
    simp only [List.map_cons, List.sum_cons, contraction_add_right, coeff_add, ih]
    congr 1
    change coeff (exponent u v)
      (contraction k (mono 4 (6-4) 1 + mono 6 (6-6) δ) (mono j (n-j) a)) = _
    rw [contraction_add_left, coeff_add, contraction_mono_coeff, contraction_mono_coeff]
    ring

private theorem exceptional_first_iterate (δ : K) :
    contraction 1 (exceptionalHamiltonian δ) exceptionalPartner =
      fromPairs 6 (Exceptional411.first δ) := by
  apply MvPolynomial.ext
  intro e
  rw [← exponent_eta e, exceptional_partner_eq]
  change coeff (exponent (e false) (e true))
    (contraction 1 (exceptionalHamiltonian δ) (fromPairs 2 Exceptional411.partner)) = _
  rw [exceptional_coefficient, Exceptional411.first_iterate]
  simp [fromPairs, Exceptional411.first, coeff_mono, eq_comm]

private theorem exceptional_second_iterate (δ : K) :
    contraction 1 (exceptionalHamiltonian δ) (fromPairs 6 (Exceptional411.first δ)) =
      fromPairs 10 (Exceptional411.second δ) := by
  apply MvPolynomial.ext
  intro e
  rw [← exponent_eta e, exceptional_coefficient, Exceptional411.second_iterate]
  simp [fromPairs, Exceptional411.second, coeff_mono, eq_comm]

theorem exceptional_firstRefinement (δ : K) :
    FirstRefinement (exceptionalHamiltonian δ) exceptionalPartner := by
  have h (k : ℕ) (hk : k = 3 ∨ k = 5) :
      contraction k (exceptionalHamiltonian δ) exceptionalPartner = 0 ∧
      contraction k (exceptionalHamiltonian δ) (fromPairs 6 (Exceptional411.first δ)) = 0 := by
    constructor <;> apply MvPolynomial.ext <;> intro e
    · rw [← exponent_eta e, exceptional_partner_eq]
      change coeff (exponent (e false) (e true))
        (contraction k (exceptionalHamiltonian δ) (fromPairs 2 Exceptional411.partner)) = _
      rw [exceptional_coefficient, (Exceptional411.static_gates δ _ _ k hk).1, coeff_zero]
    · rw [← exponent_eta e, exceptional_coefficient,
        (Exceptional411.static_gates δ _ _ k hk).2, coeff_zero]
  rw [FirstRefinement, exceptional_first_iterate]
  exact ⟨(h 3 (Or.inl rfl)).1, (h 5 (Or.inr rfl)).1, (h 3 (Or.inl rfl)).2, (h 5 (Or.inr rfl)).2⟩

/-- The exact third-order obstruction on the second Poisson iterate. -/
theorem exceptional_second_gate (δ : K) :
    contraction 3 (exceptionalHamiltonian δ)
      ((contraction 1 (exceptionalHamiltonian δ))^[2] exceptionalPartner) =
      mono 10 0 (-82944 * δ) := by
  simp only [Function.iterate_succ_apply', Function.iterate_zero_apply,
    exceptional_first_iterate, exceptional_second_iterate]
  apply MvPolynomial.ext
  intro e
  rw [← exponent_eta e, exceptional_coefficient, Exceptional411.second_obstruction]
  simp [coeff_mono, eq_comm]

theorem exceptional_not_persistent [CharZero K] (δ : K) (hd : δ ≠ 0) :
    ¬ PersistentCore (exceptionalHamiltonian δ) exceptionalPartner := by
  intro h
  have he := (h 2).1
  rw [exceptional_second_gate] at he
  have hz := congrArg (coeff (exponent 10 0)) he
  have hδ : (-82944 : K) * δ ≠ 0 := mul_ne_zero (by norm_num) hd
  exact hδ (by simpa [coeff_mono] using hz)

/-- The explicit obstruction survives any invertible linear substitution
and nonzero rescaling of the exceptional Hamiltonian. -/
theorem exceptional_obstruction_of_chart [CharZero K] (δ a b c d t : K)
    (hδ : δ ≠ 0) (hdet : a*d-b*c ≠ 0) (ht : t ≠ 0) :
    ∃ G : Poly (R := K),
      FirstRefinement (C t * linearSub a b c d (exceptionalHamiltonian δ)) G ∧
      ¬ PersistentCore (C t * linearSub a b c d (exceptionalHamiltonian δ)) G := by
  refine ⟨linearSub a b c d exceptionalPartner, ?_, ?_⟩
  · exact (firstRefinement_linearSub_iff a b c d t _ _ hdet ht).mpr
      (exceptional_firstRefinement δ)
  · intro h
    exact exceptional_not_persistent δ hδ
      ((persistentCore_linearSub_iff a b c d t _ _ hdet ht).mp h)

end SexticC3.Differential
