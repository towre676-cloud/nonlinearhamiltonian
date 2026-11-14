import SexticC3.CubeLeadingSevenCoefficients

/-! An actual extra persistent partner on the affine locus. -/
noncomputable section
set_option linter.unusedSectionVars false
namespace SexticC3.CubeLeading.Polynomial
open MvPolynomial
variable {K : Type*} [Field K] [CharZero K]

lemma static_stable_le_persistentCore (t : HamiltonianParameters K)
    (W : Submodule K (Poly K))
    (hs : ∀ f ∈ W, Static t.toGateParameters f)
    (hD : ∀ f ∈ W, bracket (hamiltonian t) f ∈ W) : W ≤ persistentCore t := by
  intro f hf
  rw [mem_persistentCore]
  intro n
  apply hs
  induction n with
  | zero => exact hf
  | succ n ih => simpa only [Function.iterate_succ_apply'] using hD _ ih

lemma momentum_static (t : GateParameters K) : Static t (X 1) := by
  constructor <;> simp [thirdGate, fifthGate, pderiv_X, Pi.single_apply]

lemma affine_momentum_bracket (t : HamiltonianParameters K)
    (hb2 : t.b₂ = 0) (hb3 : t.b₃ = 0) (hc2 : t.c₂ = 0)
    (hc3 : t.c₃ = 0) (hc4 : t.c₄ = 0) (hc5 : t.c₅ = 0) :
    bracket (hamiltonian t) (X 1) = C t.b₁ * X 1 + C t.c₁ := by
  simp [hamiltonian_bracket, pderiv_X, Pi.single_apply, hb2, hb3, hc2, hc3, hc4, hc5]

/-- The polynomial P is persistent when B and C are affine. -/
theorem affine_momentum_persistent (t : HamiltonianParameters K)
    (hb2 : t.b₂ = 0) (hb3 : t.b₃ = 0) (hc2 : t.c₂ = 0)
    (hc3 : t.c₃ = 0) (hc4 : t.c₄ = 0) (hc5 : t.c₅ = 0) :
    X 1 ∈ persistentCore t := by
  let W := Submodule.span K ({1, X 1} : Set (Poly K))
  have h1 : (1 : Poly K) ∈ W := Submodule.subset_span (by simp)
  have hP : (X 1 : Poly K) ∈ W := Submodule.subset_span (by simp)
  have hs : W ≤ staticSubmodule t.toGateParameters := by
    apply Submodule.span_le.mpr
    intro f hf
    rcases hf with rfl | rfl
    · exact one_static _
    · exact momentum_static _
  apply static_stable_le_persistentCore t W (fun f hf => hs hf) _ hP
  intro f hf
  obtain ⟨a,b,rfl⟩ := Submodule.mem_span_pair.mp hf
  change bracketLinear (hamiltonian t) (a • 1+b • X 1) ∈ W
  rw [map_add, map_smul, map_smul]
  have hz : bracketLinear (hamiltonian t) 1 = 0 := by simp [bracketLinear, bracket]
  have hDP : bracketLinear (hamiltonian t) (X 1) = C t.b₁ * X 1+C t.c₁ :=
    affine_momentum_bracket t hb2 hb3 hc2 hc3 hc4 hc5
  rw [hz, hDP, smul_zero, zero_add]
  apply W.smul_mem
  apply W.add_mem
  · simpa only [C_mul'] using W.smul_mem t.b₁ hP
  · simpa only [← C_mul', mul_one] using W.smul_mem t.c₁ h1

end SexticC3.CubeLeading.Polynomial
