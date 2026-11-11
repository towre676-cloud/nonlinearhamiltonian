import SexticC3.Discriminant
import SexticC3.Degree1
import SexticC3.Degree2
import SexticC3.Degree3
import SexticC3.Degree4
import SexticC3.Degree5
import SexticC3.Degree6
import SexticC3.Degree7
import SexticC3.Degree8
import SexticC3.Degree9
import SexticC3.Degree10
import SexticC3.Degree11
import SexticC3.Degree12
import SexticC3.Degree13
import SexticC3.Degree14
import SexticC3.Degree15
import SexticC3.Degree16
import SexticC3.Core6
import SexticC3.Exceptional411
import SexticC3.PolynomialBridge

namespace SexticC3

variable {K : Type*} [Field K] [CharZero K] (a b c d : K)

/-- Uniform finite-window bound for the normalized squarefree coefficient model. -/
theorem finite_kernel_bound (n : Nat) (hn₁ : 1 ≤ n) (hn₂ : n ≤ 16)
    (g : Nat → K) (h : IsKernel a b c d n g) (hd : delta a b c d ≠ 0) :
    ∀ j ≤ n, g j = if n = 6 then hCoeff a b c d j * g 1 else 0 := by
  have hn : n = 1 ∨ n = 2 ∨ n = 3 ∨ n = 4 ∨ n = 5 ∨ n = 6 ∨ n = 7 ∨ n = 8 ∨ n = 9 ∨ n = 10 ∨ n = 11 ∨ n = 12 ∨ n = 13 ∨ n = 14 ∨ n = 15 ∨ n = 16 := by omega
  rcases hn with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
  · intro j hj
    have hj' : j = 0 ∨ j = 1 := by omega
    obtain ⟨h0, h1⟩ := Degree1.kernel_bound a b c d g h hd
    rcases hj' with rfl | rfl <;> simp [h0, h1]
  · simpa using Degree2.kernel_bound a b c d g h hd
  · simpa using Degree3.kernel_bound a b c d g h hd
  · simpa using Degree4.kernel_bound a b c d g h hd
  · simpa using Degree5.kernel_bound a b c d g h hd
  · simpa [Degree6.lift1_eq_hCoeff] using Degree6.kernel_bound a b c d g h hd
  · simpa using Degree7.kernel_bound a b c d g h hd
  · simpa using Degree8.kernel_bound a b c d g h hd
  · simpa using Degree9.kernel_bound a b c d g h hd
  · simpa using Degree10.kernel_bound a b c d g h hd
  · simpa using Degree11.kernel_bound a b c d g h hd
  · simpa using Degree12.kernel_bound a b c d g h hd
  · simpa using Degree13.kernel_bound a b c d g h hd
  · simpa using Degree14.kernel_bound a b c d g h hd
  · simpa using Degree15.kernel_bound a b c d g h hd
  · simpa using Degree16.kernel_bound a b c d g h hd

/-- Finite squarefree kernel bound for actual multivariate polynomial gates.
This transports all sixteen certificates through the uniform differential bridge,
with no independent coefficient-model assumption in the hypothesis. -/
theorem finite_differential_kernel_bound (n : Nat) (hn₁ : 1 ≤ n) (hn₂ : n ≤ 16)
    (g : Nat → K)
    (h : Differential.FirstRefinement (Differential.hamiltonian a b c d)
      (Differential.homogeneous n g))
    (hd : delta a b c d ≠ 0) :
    Differential.homogeneous n g =
      if n = 6 then MvPolynomial.C (g 1) * Differential.hamiltonian a b c d else 0 := by
  have hb := finite_kernel_bound a b c d n hn₁ hn₂ g
    (Differential.isKernel_of_firstRefinement a b c d n g h) hd
  rw [Differential.homogeneous_congr n g _ hb]
  by_cases hn : n = 6
  · subst n
    simp only [↓reduceIte]
    exact Differential.homogeneous_hCoeff a b c d (g 1)
  · simp [hn]

/-- Exact finite homogeneous first-refinement classification in the actual
multivariate differential model. -/
theorem finite_differential_kernel_iff (n : Nat) (hn₁ : 1 ≤ n) (hn₂ : n ≤ 16)
    (g : Nat → K) (hd : delta a b c d ≠ 0) :
    Differential.FirstRefinement (Differential.hamiltonian a b c d)
      (Differential.homogeneous n g) ↔
    Differential.homogeneous n g =
      if n = 6 then MvPolynomial.C (g 1) * Differential.hamiltonian a b c d else 0 := by
  constructor
  · intro h
    exact finite_differential_kernel_bound a b c d n hn₁ hn₂ g h hd
  · intro h
    rw [h]
    split_ifs
    · exact Differential.firstRefinement_multiple _ _
    · exact Differential.firstRefinement_zero _

/-- In the certified finite window, the persistent differential core has the
same classification as the first refinement.  This checks all Poisson iterates
for the surviving Hamiltonian multiple. -/
theorem finite_differential_core_iff (n : Nat) (hn₁ : 1 ≤ n) (hn₂ : n ≤ 16)
    (g : Nat → K) (hd : delta a b c d ≠ 0) :
    Differential.PersistentCore (Differential.hamiltonian a b c d)
      (Differential.homogeneous n g) ↔
    Differential.homogeneous n g =
      if n = 6 then MvPolynomial.C (g 1) * Differential.hamiltonian a b c d else 0 := by
  constructor
  · intro h
    exact finite_differential_kernel_bound a b c d n hn₁ hn₂ g
      (Differential.firstRefinement_of_core _ _ h) hd
  · intro h
    rw [h]
    split_ifs
    · exact Differential.persistentCore_multiple _ _
    · exact Differential.persistentCore_zero _

end SexticC3
