import SexticC3.GeometricSquarefree
import SexticC3.PolynomialDescent
import Mathlib.FieldTheory.IsAlgClosed.AlgebraicClosure

noncomputable section

namespace SexticC3.Differential

open MvPolynomial

variable {K : Type*} [Field K] [CharZero K]

/-- The exact interface between the normalized certificate and the
geometric proof. The bound is supplied for separable chart quintics. -/
def SeparableChartBound (L : Type*) [Field L] : Prop :=
  ∀ (a b c d : L) (n : ℕ), 1 ≤ n → ∀ g : ℕ → L,
    (StaticTail.chartQuintic a b c d).Separable → IsKernel a b c d n g →
    ∀ j ≤ n, g j = if n = 6 then hCoeff a b c d j * g 1 else 0

theorem geometric_shape_of_separableChartBound [IsAlgClosed K] (hbound : SeparableChartBound K)
    (F G : Poly (R := K)) (hF : F.IsHomogeneous 6) (hs : SimpleProjectiveRoots F)
    (hG : FirstRefinement F G) : ∃ r s : K, G = C r + C s * F := by
  obtain ⟨v,x,hvx,hroot⟩ := exists_projective_root F hF
  obtain ⟨u,w,t,a,b,c,d,hdet,ht,hchart⟩ :=
    normalize_simple_projective_root F hF v x hvx hroot (hs v x hvx hroot)
  have hsimple := simpleProjectiveRoots_linearSub F hs u v w x t hdet ht
  rw [hchart] at hsimple
  have hsep := separable_chartQuintic_of_simpleProjectiveRoots a b c d hsimple
  exact polynomial_shape_of_normalized_chart F G hF a b c d u v w x t hdet ht hchart
    (fun n hn g hk => hbound a b c d n hn g hsep hk) hG

theorem firstRefinement_iff_shape_of_separableChartBound
    (hbound : SeparableChartBound (AlgebraicClosure K)) (F G : Poly (R := K))
    (hF : F.IsHomogeneous 6)
    (hs : SimpleProjectiveRoots (map (algebraMap K (AlgebraicClosure K)) F)) :
    FirstRefinement F G ↔ ∃ r s : K, G = C r + C s * F := by
  constructor
  · intro hG
    let f : K →+* AlgebraicClosure K := algebraMap K (AlgebraicClosure K)
    have hne : F ≠ 0 := by
      intro h
      rw [h, map_zero] at hs
      have h' := hs 1 0 (Or.inl one_ne_zero) (map_zero _)
      simpa only [map_zero, ne_self_iff_false, or_self] using h'
    obtain ⟨r,s,h⟩ := geometric_shape_of_separableChartBound hbound (map f F) (map f G)
      (hF.map f) hs (firstRefinement_map f F G hG)
    exact polynomial_shape_descent f F G hF hne r s h
  · rintro ⟨r,s,rfl⟩
    exact firstRefinement_of_core _ _
      (persistentCore_add _ _ _ (persistentCore_constant F r) (persistentCore_multiple F s))

end SexticC3.Differential
