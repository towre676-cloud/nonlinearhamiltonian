import SexticC3.CubeLeadingSevenBasis

/-! Reconstruction from the finite jet, after the all-degree cutoff. -/
noncomputable section
set_option linter.unusedSectionVars false
namespace SexticC3.CubeLeading.Polynomial
open MvPolynomial
variable {K : Type*} [Field K] [CharZero K]

set_option maxHeartbeats 1500000 in
lemma seven_reconstruct_normalized (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0)
    (f : Poly K) (hf : Static t.toGateParameters f)
    (hP : Bounded ![0, 1] 6 f) (h00 : bicoeff 0 0 f = 0) (h03 : bicoeff 0 3 f = 0) :
    ∃ x : Fin 13 → K, f = sevenCombination t x := by
  let x : Fin 13 → K := fun k =>
    bicoeff (sevenIndices k).1 (sevenIndices k).2 f / (sevenScales k : K)
  refine ⟨x, static_eq_of_initial_jet t.toGateParameters f (sevenCombination t x)
    hf (seven_combination_static t hb h4 h5 x) 6 hP
    (seven_combination_momentum_bound t x) ?_⟩
  intro i j hi hj
  rw [seven_combination_initial t x i j hi hj]
  have vanish (i j : ℕ) : bicoeff (i+1) (j+4) f = 0 :=
    fifth_affine_q_vanish t.toGateParameters (by simp [hb, h5]) f hf i j
  interval_cases i <;> interval_cases j <;>
    norm_num [x, Prod.ext_iff, Fin.sum_univ_succ, sevenIndices, sevenScales, h00, h03,
      vanish 0 0, vanish 0 1, vanish 0 2, vanish 1 0, vanish 1 1, vanish 1 2] <;> ring

end SexticC3.CubeLeading.Polynomial
