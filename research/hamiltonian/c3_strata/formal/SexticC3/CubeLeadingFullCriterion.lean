import SexticC3.CubeLeadingSevenCore
import SexticC3.CubeLeadingAffineConverse

/-! The ten-parameter persistent-core criterion, for all polynomial degrees
and all odd flat gates in the original coordinates. -/
noncomputable section
set_option linter.unusedSectionVars false
namespace SexticC3.CubeLeading.Polynomial
open MvPolynomial
variable {K : Type*} [Field K] [CharZero K]

/-- At least one of B and C is non-affine. -/
def NonAffine (t : HamiltonianParameters K) : Prop :=
  t.b₂ ≠ 0 ∨ t.b₃ ≠ 0 ∨ t.c₂ ≠ 0 ∨ t.c₃ ≠ 0 ∨ t.c₄ ≠ 0 ∨ t.c₅ ≠ 0

theorem nonaffine_persistent_core (t : HamiltonianParameters K) (hn : NonAffine t) :
    persistentCore t = Submodule.span K ({1, hamiltonian t} : Set (Poly K)) := by
  by_cases hnew : t.b₃ ≠ 0 ∨ t.c₄ ≠ 0 ∨ t.c₅ ≠ 0
  · exact newton_persistent_core t hnew
  · push_neg at hnew
    obtain ⟨hb,h4,h5⟩ := hnew
    apply seven_persistent_core t hb h4 h5
    simp only [NonAffine, hb, h4, h5, ne_eq, not_true_eq_false, false_or, or_false] at hn
    tauto

lemma momentum_not_in_hamiltonian_span (t : HamiltonianParameters K) :
    (X 1 : Poly K) ∉ Submodule.span K ({1, hamiltonian t} : Set (Poly K)) := by
  intro h
  obtain ⟨a,b,he⟩ := Submodule.mem_span_pair.mp h
  simp only [← C_mul', mul_one] at he
  have h3 := congrArg (bicoeff 0 3) he
  have h1 := congrArg (bicoeff 0 1) he
  have hX : (X 1 : Poly K) = monomial (exponent 0 1) 1 := by simp [exponent, X]
  have hb : b = 0 := by simpa [hamiltonian, hX, bicoeff_monomial] using h3
  simpa [hamiltonian, hX, bicoeff_monomial, hb] using h1

/-- Exact iff criterion on all ten parameters. -/
theorem persistent_core_iff_nonaffine (t : HamiltonianParameters K) :
    persistentCore t = Submodule.span K ({1, hamiltonian t} : Set (Poly K)) ↔ NonAffine t := by
  constructor
  · intro he
    by_contra hn
    simp only [NonAffine, not_or, not_not] at hn
    obtain ⟨hb2,hb3,hc2,hc3,hc4,hc5⟩ := hn
    have hp := affine_momentum_persistent t hb2 hb3 hc2 hc3 hc4 hc5
    rw [he] at hp
    exact momentum_not_in_hamiltonian_span t hp
  · exact nonaffine_persistent_core t

lemma flat_core_from_chart (t : HamiltonianParameters K)
    (hc : persistentCore t = Submodule.span K ({1, hamiltonian t} : Set (Poly K)))
    (f : Poly K) :
    AllFlatPersistent (shear 1 (hamiltonian t)) f ↔
      ∃ a b : K, f = C a+C b*shear 1 (hamiltonian t) := by
  rw [all_flat_persistent_iff]
  constructor
  · intro hf
    let g := shear (-1) f
    have hfg : shear 1 g = f := by simp [g, shear_comp]
    have hg : g ∈ persistentCore t := (persistent_flat_transport t g).mp (by rwa [hfg])
    rw [hc, Submodule.mem_span_pair] at hg
    obtain ⟨a,b,he⟩ := hg
    refine ⟨a,b,?_⟩
    have he' := congrArg (shear 1) he
    simp only [map_add, ← C_mul', map_mul, map_one, mul_one, shear_C, hfg] at he'
    exact he'.symm
  · rintro ⟨a,b,rfl⟩
    have hg : C a+C b*hamiltonian t ∈ persistentCore t := by
      rw [hc, Submodule.mem_span_pair]
      exact ⟨a,b,by simp [← C_mul']⟩
    simpa using (persistent_flat_transport t _).mpr hg

/-- Full classification, in the original q,p coordinates, over every
characteristic-zero field. The partner f is unrestricted. -/
theorem all_flat_nonaffine_persistent_core (t : HamiltonianParameters K)
    (hn : NonAffine t) (f : Poly K) :
    AllFlatPersistent (shear 1 (hamiltonian t)) f ↔
      ∃ a b : K, f = C a+C b*shear 1 (hamiltonian t) :=
  flat_core_from_chart t (nonaffine_persistent_core t hn) f

/-- The full ten-parameter iff, including the explicit affine counterpartner. -/
theorem all_flat_core_iff_nonaffine (t : HamiltonianParameters K) :
    (∀ f : Poly K, AllFlatPersistent (shear 1 (hamiltonian t)) f ↔
      ∃ a b : K, f = C a+C b*shear 1 (hamiltonian t)) ↔ NonAffine t := by
  constructor
  · intro hall
    by_contra hn
    simp only [NonAffine, not_or, not_not] at hn
    obtain ⟨hb2,hb3,hc2,hc3,hc4,hc5⟩ := hn
    have hp := affine_momentum_persistent t hb2 hb3 hc2 hc3 hc4 hc5
    have hf := (persistent_flat_transport t (X 1)).mpr hp
    have ha := (all_flat_persistent_iff t _).mpr hf
    obtain ⟨a,b,he⟩ := (hall _).mp ha
    have he' := congrArg (shear (-1)) he
    have heP : (X 1 : Poly K) = C a+C b*hamiltonian t := by
      simpa [shear_comp] using he'
    apply momentum_not_in_hamiltonian_span t
    rw [Submodule.mem_span_pair]
    exact ⟨a,b,by simpa [← C_mul'] using heP.symm⟩
  · intro hn f
    exact all_flat_nonaffine_persistent_core t hn f

end SexticC3.CubeLeading.Polynomial
