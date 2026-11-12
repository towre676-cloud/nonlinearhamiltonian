import SexticC3.TailAllDegrees
import SexticC3.GeometricComposition
import SexticC3.ChartDiscriminant

noncomputable section

namespace SexticC3.Differential

open MvPolynomial

variable {K : Type*} [Field K] [CharZero K]

theorem separableChartBound_algClosed [IsAlgClosed K] : SeparableChartBound K := by
  intro a b c d n hn g hsep hk
  exact squarefree_kernel_bound a b c d n hn g hk
    (StaticTail.delta_ne_zero_of_separable a b c d hsep)

/-- Geometric squarefreeness is tested on the algebraic closure. The
classification is returned over the original characteristic-zero field. -/
theorem squarefree_firstRefinement_iff_shape (F G : Poly (R := K))
    (hF : F.IsHomogeneous 6)
    (hs : SimpleProjectiveRoots (map (algebraMap K (AlgebraicClosure K)) F)) :
    FirstRefinement F G ↔ ∃ r s : K, G = C r + C s * F :=
  firstRefinement_iff_shape_of_separableChartBound separableChartBound_algClosed F G hF hs

theorem squarefree_firstRefinement_iff_core (F G : Poly (R := K))
    (hF : F.IsHomogeneous 6)
    (hs : SimpleProjectiveRoots (map (algebraMap K (AlgebraicClosure K)) F)) :
    FirstRefinement F G ↔ PersistentCore F G := by
  constructor
  · intro h
    obtain ⟨r,s,rfl⟩ := (squarefree_firstRefinement_iff_shape F G hF hs).mp h
    exact persistentCore_add _ _ _ (persistentCore_constant F r) (persistentCore_multiple F s)
  · exact firstRefinement_of_core _ _

/-- Every observable persists for the zero Hamiltonian. -/
theorem zero_hamiltonian_persistentCore (G : Poly (R := K)) : PersistentCore 0 G := by
  intro i
  simp only [contraction_zero_left, and_self]

end SexticC3.Differential
