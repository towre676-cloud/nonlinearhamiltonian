import SexticC3.CubeLeadingClassification

/-! # The persistent core of the concrete transported static equations. -/
noncomputable section
set_option linter.unusedSectionVars false
namespace SexticC3.CubeLeading.Polynomial
open MvPolynomial
variable {K : Type*} [Field K] [CharZero K]

lemma thirdGate_add (t : GateParameters K) (f g : Poly K) :
    thirdGate t (f+g) = thirdGate t f+thirdGate t g := by
  simp only [thirdGate, map_add, mul_add]
  ring
lemma fifthGate_add (t : GateParameters K) (f g : Poly K) :
    fifthGate t (f+g) = fifthGate t f+fifthGate t g := by
  simp only [fifthGate, map_add, mul_add]
  ring
lemma thirdGate_C_mul (t : GateParameters K) (a : K) (f : Poly K) :
    thirdGate t (C a*f) = C a*thirdGate t f := by
  simp only [thirdGate, pderiv_C_mul]
  ring
lemma fifthGate_C_mul (t : GateParameters K) (a : K) (f : Poly K) :
    fifthGate t (C a*f) = C a*fifthGate t f := by
  simp only [fifthGate, pderiv_C_mul]
  ring

/-- Both static equations are kernels of actual linear differential operators. -/
def staticSubmodule (t : GateParameters K) : Submodule K (Poly K) where
  carrier := Static t
  zero_mem' := by constructor <;> simp [thirdGate, fifthGate]
  add_mem' := by
    intro f g hf hg
    constructor
    · rw [thirdGate_add, hf.1, hg.1, add_zero]
    · rw [fifthGate_add, hf.2, hg.2, add_zero]
  smul_mem' := by
    intro a f hf
    rw [← C_mul']
    constructor
    · rw [thirdGate_C_mul, hf.1, mul_zero]
    · rw [fifthGate_C_mul, hf.2, mul_zero]

def bracketLinear (H : Poly K) : Module.End K (Poly K) where
  toFun := bracket H
  map_add' := by intro f g; simp only [bracket, map_add]; ring
  map_smul' := by
    intro a f
    simp only [← C_mul', bracket, pderiv_C_mul, RingHom.id_apply]
    ring

/-- Membership means that every Hamiltonian iterate satisfies both static gates. -/
def persistentCore (t : HamiltonianParameters K) : Submodule K (Poly K) :=
  ⨅ n : ℕ, (staticSubmodule t.toGateParameters).comap (bracketLinear (hamiltonian t)^n)

lemma mem_persistentCore (t : HamiltonianParameters K) (f : Poly K) :
    f ∈ persistentCore t ↔ ∀ n : ℕ, Static t.toGateParameters
      ((bracket (hamiltonian t))^[n] f) := by
  simp only [persistentCore, Submodule.mem_iInf, Submodule.mem_comap, Module.End.pow_apply]
  rfl

lemma persistentCore_static (t : HamiltonianParameters K) (f : Poly K)
    (hf : f ∈ persistentCore t) : Static t.toGateParameters f :=
  (mem_persistentCore t f).mp hf 0

lemma persistentCore_stable (t : HamiltonianParameters K) (f : Poly K)
    (hf : f ∈ persistentCore t) : bracket (hamiltonian t) f ∈ persistentCore t := by
  apply (mem_persistentCore _ _).mpr
  intro n
  simpa only [Function.iterate_succ_apply] using (mem_persistentCore _ _).mp hf (n+1)

lemma kernel_mem_persistentCore (t : HamiltonianParameters K) (f : Poly K)
    (hf : Static t.toGateParameters f) (hker : bracket (hamiltonian t) f = 0) :
    f ∈ persistentCore t := by
  apply (mem_persistentCore _ _).mpr
  intro n
  cases n with
  | zero => exact hf
  | succ n =>
    rw [Function.iterate_succ_apply, hker]
    have hz : (bracket (hamiltonian t))^[n] 0 = 0 := by
      simpa [Module.End.pow_apply, bracketLinear] using (bracketLinear (hamiltonian t)^n).map_zero
    rw [hz]
    exact (staticSubmodule t.toGateParameters).zero_mem

/-- The joined three-case all-degree theorem for the transported equations.
No finite-dimensionality, momentum bound or classification is assumed. -/
theorem newton_persistent_core (t : HamiltonianParameters K)
    (hnew : t.b₃ ≠ 0 ∨ t.c₄ ≠ 0 ∨ t.c₅ ≠ 0) :
    persistentCore t = Submodule.span K ({1, hamiltonian t} : Set (Poly K)) := by
  apply newton_static_stable_eq_span t hnew (persistentCore t)
  · exact kernel_mem_persistentCore t 1 (one_static _) (by simp [bracket, pderiv_one])
  · exact kernel_mem_persistentCore t (hamiltonian t) (hamiltonian_static t) (by unfold bracket; ring)
  · exact persistentCore_static t
  · exact persistentCore_stable t

end SexticC3.CubeLeading.Polynomial
