import SexticC3.GateTransport
import SexticC3.GradedRefinement
import SexticC3.PolynomialKernel

noncomputable section

namespace SexticC3.Differential

open MvPolynomial

variable {K : Type*} [Field K]

/-- An exhibited normalized chart carries the all-degree coefficient
bound back to the original polynomial, in each homogeneous degree. -/
theorem refinement_of_normalized_chart (F G : Poly (R := K)) (n : ℕ)
    (hG : G.IsHomogeneous n) (a b c d u v w x t : K)
    (hdet : u*x-v*w ≠ 0) (ht : t ≠ 0)
    (hchart : C t * linearSub u v w x F = hamiltonian a b c d)
    (bound : ∀ g : ℕ → K, IsKernel a b c d n g →
      ∀ j ≤ n, g j = if n = 6 then hCoeff a b c d j * g 1 else 0) :
    FirstRefinement F G ↔ PersistentCore F G := by
  let A := linearSub u v w x
  let g : ℕ → K := fun j => coeff (exponent j (n-j)) (A G)
  have hg : homogeneous n g = A G :=
    homogeneous_of_isHomogeneous n _ (isHomogeneous_linearSub u v w x n G hG)
  have h := firstRefinement_iff_persistent_of_kernel_bound a b c d n g (bound g)
  rw [hg, ← hchart] at h
  exact (firstRefinement_linearSub_iff u v w x t F G hdet ht).symm.trans
    (h.trans (persistentCore_linearSub_iff u v w x t F G hdet ht))

/-- Transport the result to every polynomial observable once a normalized
chart and the normalized positive-degree bounds have been supplied. -/
theorem polynomial_refinement_of_normalized_chart (F G : Poly (R := K))
    (hF : F.IsHomogeneous 6) (a b c d u v w x t : K)
    (hdet : u*x-v*w ≠ 0) (ht : t ≠ 0)
    (hchart : C t * linearSub u v w x F = hamiltonian a b c d)
    (bound : ∀ n ≥ 1, ∀ g : ℕ → K, IsKernel a b c d n g →
      ∀ j ≤ n, g j = if n = 6 then hCoeff a b c d j * g 1 else 0) :
    FirstRefinement F G ↔ PersistentCore F G := by
  apply firstRefinement_iff_persistent_of_homogeneous F G hF
  intro n hn P hP h
  exact (refinement_of_normalized_chart F P n hP a b c d u v w x t hdet ht hchart
    (bound n hn)).mp h

/-- The homogeneous bound transports the actual observable, including
the scalar in the Hamiltonian direction. -/
theorem homogeneous_shape_of_normalized_chart (F G : Poly (R := K)) (n : ℕ)
    (hG : G.IsHomogeneous n) (a b c d u v w x t : K)
    (hdet : u*x-v*w ≠ 0) (ht : t ≠ 0)
    (hchart : C t * linearSub u v w x F = hamiltonian a b c d)
    (bound : ∀ g : ℕ → K, IsKernel a b c d n g →
      ∀ j ≤ n, g j = if n = 6 then hCoeff a b c d j * g 1 else 0)
    (h : FirstRefinement F G) :
    ∃ s : K, G = if n = 6 then C s * F else 0 := by
  let A := linearSub u v w x
  let g : ℕ → K := fun j => coeff (exponent j (n-j)) (A G)
  have hg : homogeneous n g = A G :=
    homogeneous_of_isHomogeneous n _ (isHomogeneous_linearSub u v w x n G hG)
  have hnorm := (firstRefinement_linearSub_iff u v w x t F G hdet ht).mpr h
  rw [hchart, ← hg] at hnorm
  have hp := polynomial_bound_of_kernel_bound a b c d n g (bound g) hnorm
  rw [hg, ← hchart] at hp
  refine ⟨g 1*t, ?_⟩
  apply linearSub_injective u v w x hdet
  by_cases hn : n = 6
  · simpa only [hn, if_true, map_mul, linearSub_C, C_mul, mul_assoc] using hp
  · simpa only [hn, if_false, map_zero] using hp

/-- With a normalized chart and the positive-degree bound, every
observable in first refinement is a constant plus a multiple of F. -/
theorem polynomial_shape_of_normalized_chart (F G : Poly (R := K))
    (hF : F.IsHomogeneous 6) (a b c d u v w x t : K)
    (hdet : u*x-v*w ≠ 0) (ht : t ≠ 0)
    (hchart : C t * linearSub u v w x F = hamiltonian a b c d)
    (bound : ∀ n ≥ 1, ∀ g : ℕ → K, IsKernel a b c d n g →
      ∀ j ≤ n, g j = if n = 6 then hCoeff a b c d j * g 1 else 0)
    (h : FirstRefinement F G) :
    ∃ r s : K, G = C r + C s * F := by
  have hshape (n : ℕ) (hn : 1 ≤ n) :
      ∃ s : K, homogeneousComponent n G = if n = 6 then C s * F else 0 :=
    homogeneous_shape_of_normalized_chart F _ n (homogeneousComponent_isHomogeneous n G)
      a b c d u v w x t hdet ht hchart (bound n hn)
      (firstRefinement_homogeneousComponent F G hF h n)
  obtain ⟨s, hs⟩ := hshape 6 (by decide)
  simp only [if_true] at hs
  refine ⟨coeff 0 G, s, ?_⟩
  apply MvPolynomial.ext
  intro e
  rw [coeff_add]
  by_cases he0 : e.degree = 0
  · have he6 : e.degree ≠ 6 := by omega
    rw [(hF.C_mul s).coeff_eq_zero he6, add_zero, ← homogeneousComponent_zero,
      coeff_homogeneousComponent, if_pos he0]
  · rw [(isHomogeneous_C Bool (coeff 0 G)).coeff_eq_zero he0, zero_add, ← hs,
      coeff_homogeneousComponent]
    by_cases he6 : e.degree = 6
    · rw [if_pos he6]
    · rw [if_neg he6]
      obtain ⟨r, hr⟩ := hshape e.degree (by omega)
      simp only [he6, if_false] at hr
      have hz := congrArg (coeff e) hr
      simpa only [coeff_homogeneousComponent, if_true, coeff_zero] using hz

end SexticC3.Differential
