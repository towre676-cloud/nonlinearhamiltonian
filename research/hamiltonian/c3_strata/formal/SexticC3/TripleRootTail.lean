import SexticC3.TailCharts
import SexticC3.TargetRootMultiplicity
import SexticC3.ChartTransport
import Mathlib.FieldTheory.IsAlgClosed.Basic

noncomputable section

namespace SexticC3.StaticTail

variable {K : Type*} [Field K] [CharZero K]

set_option maxHeartbeats 5000000 in
/-- The normalized static tail vanishes if the complementary quintic
has an exactly triple root. No discriminant nonvanishing is assumed. -/
theorem normalized_static_tail_of_triple_root (n : ℕ) (hn : 17 ≤ n) (a b c d x : K)
    (g : ℕ → K)
    (roots : ∀ m : ℕ, 0 < m → ∀ q : K, ∃ l : K, l ^ m = q)
    (h : ∀ k u v, (k = 3 ∨ k = 5) → rowValue a b c d n ⟨false, k, u, v⟩ g = 0)
    (hm : (chartQuintic a b c d).rootMultiplicity x = 3) :
    ∀ j ≤ n, g j = 0 := by
  intro j hj
  by_contra hjz
  have hedge : g 0 ≠ 0 ∨ g 1 ≠ 0 := by
    by_contra he
    push_neg at he
    exact hjz (kernel_zero_of_edge_zero a b c d n hn g h he.1 he.2 j hj)
  obtain ⟨s0, s1, s2, s3, s4, s5⟩ := stored_rows n hn a b c d g h
  have ht := chart_targets n hn a b c d (g 0) (g 1) roots hedge (by
    refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩
    · linear_combination s0
    · linear_combination s1
    · linear_combination s2
    · linear_combination s3
    · linear_combination s4
    · linear_combination s5)
  obtain ⟨h0, h1, h2⟩ := ht
  apply rootMultiplicity_ne_three_of_targets a b c d x _ _ _ hm
  · linear_combination h0
  · linear_combination h1
  · linear_combination h2

end SexticC3.StaticTail

namespace SexticC3.Differential

open MvPolynomial

variable {K : Type*} [Field K] [CharZero K] [IsAlgClosed K]

/-- An exactly triple root in an exhibited normalized chart rules out
every first-refinement observable of homogeneous degree at least seventeen. -/
theorem tripleRoot_highDegree_zero_of_chart (F G : Poly (R := K)) (n : ℕ)
    (hn : 17 ≤ n) (hG : G.IsHomogeneous n) (a b c d u v w x t r : K)
    (hdet : u*x-v*w ≠ 0) (ht : t ≠ 0)
    (hchart : C t * linearSub u v w x F = hamiltonian a b c d)
    (hm : (StaticTail.chartQuintic a b c d).rootMultiplicity r = 3)
    (h : FirstRefinement F G) : G = 0 := by
  obtain ⟨s, hs⟩ := homogeneous_shape_of_normalized_chart F G n hG
    a b c d u v w x t hdet ht hchart (by
      intro g hk j hj
      rw [if_neg (by omega)]
      exact StaticTail.normalized_static_tail_of_triple_root n hn a b c d r g
        (fun _ hm q => IsAlgClosed.exists_pow_nat_eq q hm)
        (fun k u v h => hk ⟨false, k, u, v⟩ h) hm j hj) h
  simpa only [if_neg (show n ≠ 6 by omega)] using hs

end SexticC3.Differential
