import SexticC3.ChartTransport
import SexticC3.TailAllDegrees

noncomputable section

namespace SexticC3

variable {K : Type*} [Field K] [CharZero K]

/-- The normalized coefficient bound over any characteristic-zero field. -/
theorem squarefree_kernel_bound_field (a b c d : K) (n : ℕ) (hn : 1 ≤ n)
    (g : ℕ → K) (h : IsKernel a b c d n g) (hd : delta a b c d ≠ 0) :
    ∀ j ≤ n, g j = if n = 6 then hCoeff a b c d j * g 1 else 0 := by
  let f : K →+* AlgebraicClosure K := algebraMap K (AlgebraicClosure K)
  exact StaticTail.kernel_bound_descent f a b c d n g h hd
    (squarefree_kernel_bound (f a) (f b) (f c) (f d) n hn (fun j => f (g j)))

namespace Differential

open MvPolynomial

/-- For a homogeneous observable in the normalized chart, the true
differential gates force zero outside degree six and a scalar multiple
of the Hamiltonian in degree six. -/
theorem squarefree_polynomial_bound (a b c d : K) (n : ℕ) (hn : 1 ≤ n)
    (g : ℕ → K) (hd : delta a b c d ≠ 0)
    (h : FirstRefinement (hamiltonian a b c d) (homogeneous n g)) :
    homogeneous n g = if n = 6 then C (g 1) * hamiltonian a b c d else 0 :=
  polynomial_bound_of_kernel_bound a b c d n g
    (fun hk => squarefree_kernel_bound_field a b c d n hn g hk hd) h

theorem squarefree_firstRefinement_iff_persistent (a b c d : K) (n : ℕ)
    (hn : 1 ≤ n) (g : ℕ → K) (hd : delta a b c d ≠ 0) :
    FirstRefinement (hamiltonian a b c d) (homogeneous n g) ↔
      PersistentCore (hamiltonian a b c d) (homogeneous n g) :=
  firstRefinement_iff_persistent_of_kernel_bound a b c d n g
    (fun hk => squarefree_kernel_bound_field a b c d n hn g hk hd)

/-- In a positive homogeneous degree, first refinement and persistence
agree for a Hamiltonian equipped with an invertible squarefree chart. -/
theorem squarefree_refinement_of_chart (F G : Poly (R := K)) (n : ℕ)
    (hn : 1 ≤ n) (hG : G.IsHomogeneous n) (a b c d u v w x t : K)
    (hdet : u*x-v*w ≠ 0) (ht : t ≠ 0)
    (hchart : C t * linearSub u v w x F = hamiltonian a b c d)
    (hd : delta a b c d ≠ 0) :
    FirstRefinement F G ↔ PersistentCore F G :=
  refinement_of_normalized_chart F G n hG a b c d u v w x t hdet ht hchart
    (fun g hk => squarefree_kernel_bound_field a b c d n hn g hk hd)

/-- The squarefree chart implies first-refinement stability for arbitrary
polynomial observables. Existence of the chart is a separate hypothesis. -/
theorem squarefree_polynomial_refinement_of_chart (F G : Poly (R := K))
    (hF : F.IsHomogeneous 6) (a b c d u v w x t : K)
    (hdet : u*x-v*w ≠ 0) (ht : t ≠ 0)
    (hchart : C t * linearSub u v w x F = hamiltonian a b c d)
    (hd : delta a b c d ≠ 0) :
    FirstRefinement F G ↔ PersistentCore F G :=
  polynomial_refinement_of_normalized_chart F G hF a b c d u v w x t hdet ht hchart
    (fun n hn g hk => squarefree_kernel_bound_field a b c d n hn g hk hd)

end Differential
end SexticC3
