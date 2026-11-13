import SexticC3.PolynomialBridge
import SexticC3.KernelDescent

noncomputable section

namespace SexticC3.Differential

open MvPolynomial

variable {K : Type*} [Field K]

/-- A normalized coefficient bound yields a theorem about the actual
third- and fifth-order partial-derivative gates. -/
theorem polynomial_bound_of_kernel_bound (a b c d : K) (n : ℕ) (g : ℕ → K)
    (bound : IsKernel a b c d n g →
      ∀ j ≤ n, g j = if n = 6 then hCoeff a b c d j * g 1 else 0)
    (h : FirstRefinement (hamiltonian a b c d) (homogeneous n g)) :
    homogeneous n g = if n = 6 then C (g 1) * hamiltonian a b c d else 0 := by
  have he := bound (isKernel_of_firstRefinement a b c d n g h)
  by_cases hn : n = 6
  · subst n
    simp only [if_true] at he ⊢
    rw [homogeneous_congr 6 g _ he, homogeneous_hCoeff]
  · simp only [hn, if_false] at he ⊢
    rw [homogeneous_congr n g (fun _ => 0) he, homogeneous_zero]

theorem firstRefinement_iff_persistent_of_kernel_bound (a b c d : K) (n : ℕ) (g : ℕ → K)
    (bound : IsKernel a b c d n g →
      ∀ j ≤ n, g j = if n = 6 then hCoeff a b c d j * g 1 else 0) :
    FirstRefinement (hamiltonian a b c d) (homogeneous n g) ↔
      PersistentCore (hamiltonian a b c d) (homogeneous n g) := by
  constructor
  · intro h
    rw [polynomial_bound_of_kernel_bound a b c d n g bound h]
    split_ifs
    · exact persistentCore_multiple _ _
    · exact persistentCore_zero _
  · exact firstRefinement_of_core _ _

end SexticC3.Differential
