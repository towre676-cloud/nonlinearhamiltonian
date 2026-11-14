import SexticC3.CubeLeadingDimension
import SexticC3.CubeLeadingHamiltonian

/-!
# Classification in the three new Newton strata

This file uses the two explicitly defined transported differential equations.
Identification with original-coordinate flat contractions is separate.
-/
noncomputable section
set_option linter.unusedSectionVars false
namespace SexticC3.CubeLeading.Polynomial
open MvPolynomial
variable {K : Type*} [Field K] [CharZero K]

lemma bounded_monomial (w : Fin 2 → ℕ) (n : ℤ) (i j : ℕ) (a : K)
    (hij : (w 0 : ℤ)*i+(w 1 : ℤ)*j ≤ n) :
    Bounded w n (monomial (exponent i j) a) := by
  apply bounded_mono (bounded_of_homogeneous
    (isWeightedHomogeneous_monomial (weights w) (exponent i j) a rfl))
  simpa [weight_pair] using hij

lemma component_monomial (w : Fin 2 → ℕ) (n : ℤ) (i j : ℕ) (a : K) :
    component w n (monomial (exponent i j) a) =
      if n = (w 0 : ℤ)*i+(w 1 : ℤ)*j then monomial (exponent i j) a else 0 := by
  rw [weightedHomogeneousComponent_of_mem
    (isWeightedHomogeneous_monomial (weights w) (exponent i j) a rfl)]
  simp [weight_pair]

lemma hamiltonian_case_one_bound (t : HamiltonianParameters K) :
    Bounded ![3, 5] 15 (hamiltonian t) := by
  change hamiltonian t ∈ boundedSubmodule ![3, 5] 15
  unfold hamiltonian
  repeat' apply (boundedSubmodule (K := K) ![3, 5] 15).add_mem
  all_goals exact bounded_monomial _ _ _ _ _ (by norm_num)

lemma hamiltonian_case_two_bound (t : HamiltonianParameters K) (h5 : t.c₅ = 0) :
    Bounded ![2, 3] 9 (hamiltonian t) := by
  change hamiltonian t ∈ boundedSubmodule ![2, 3] 9
  simp only [hamiltonian, h5, monomial_zero, add_zero]
  repeat' apply (boundedSubmodule (K := K) ![2, 3] 9).add_mem
  all_goals exact bounded_monomial _ _ _ _ _ (by norm_num)

lemma hamiltonian_case_three_bound (t : HamiltonianParameters K) (h5 : t.c₅ = 0)
    (hb : t.b₃ = 0) : Bounded ![3, 4] 12 (hamiltonian t) := by
  change hamiltonian t ∈ boundedSubmodule ![3, 4] 12
  simp only [hamiltonian, h5, hb, monomial_zero, add_zero]
  repeat' apply (boundedSubmodule (K := K) ![3, 4] 12).add_mem
  all_goals exact bounded_monomial _ _ _ _ _ (by norm_num)

lemma hamiltonian_case_one_top (t : HamiltonianParameters K) :
    component ![3, 5] 15 (hamiltonian t) = caseOne t.c₅ := by
  simp only [hamiltonian, map_add, component_monomial]
  norm_num [← qP_monomial, caseOne]

lemma hamiltonian_case_two_top (t : HamiltonianParameters K) :
    component ![2, 3] 9 (hamiltonian t) = caseTwo t.b₃ := by
  simp only [hamiltonian, map_add, component_monomial]
  norm_num [← qP_monomial, caseTwo]

lemma hamiltonian_case_three_top (t : HamiltonianParameters K) :
    component ![3, 4] 12 (hamiltonian t) = caseThree t.c₄ := by
  simp only [hamiltonian, map_add, component_monomial]
  norm_num [← qP_monomial, caseThree]

theorem case_one_static_stable (t : HamiltonianParameters K) (hc : t.c₅ ≠ 0)
    (V : Submodule K (Poly K)) (h1 : (1 : Poly K) ∈ V) (hH : hamiltonian t ∈ V)
    (hs : ∀ f ∈ V, Static t.toGateParameters f)
    (hD : ∀ f ∈ V, bracket (hamiltonian t) f ∈ V) :
    V = Submodule.span K ({1, hamiltonian t} : Set (Poly K)) := by
  refine static_stable_space_eq_span t.toGateParameters ![3, 5]
    (by intro i; fin_cases i <;> norm_num) _ (caseOne t.c₅) 15
    (hamiltonian_case_one_bound t) (hamiltonian_case_one_top t)
    (by norm_num) (binomial_ne_zero t.c₅ 5 (by decide)) (case_one_coprime t.c₅ hc)
    (by refine ⟨C t.c₅*X 0^4, ?_⟩; dsimp [caseOne]; ring)
    V h1 hH hs ?_ hD ?_
  · intro f hf
    exact static_momentum_bound t.toGateParameters (fun hz => hc hz.2.1) f (hs f hf)
  · intro f hf a ha
    exact case_one_no_square_leading t.toGateParameters hc f (hs f hf) a ha

theorem case_two_static_stable (t : HamiltonianParameters K) (h5 : t.c₅ = 0)
    (hc : t.b₃ ≠ 0) (V : Submodule K (Poly K))
    (h1 : (1 : Poly K) ∈ V) (hH : hamiltonian t ∈ V)
    (hs : ∀ f ∈ V, Static t.toGateParameters f)
    (hD : ∀ f ∈ V, bracket (hamiltonian t) f ∈ V) :
    V = Submodule.span K ({1, hamiltonian t} : Set (Poly K)) := by
  refine static_stable_space_eq_span t.toGateParameters ![2, 3]
    (by intro i; fin_cases i <;> norm_num) _ (caseTwo t.b₃) 9
    (hamiltonian_case_two_bound t h5) (hamiltonian_case_two_top t)
    (by norm_num) (linear_cubic_ne_zero t.b₃) (case_two_coprime t.b₃ hc)
    (by refine ⟨C t.b₃*X 0^2*X 1, ?_⟩; dsimp [caseTwo]; ring)
    V h1 hH hs ?_ hD ?_
  · intro f hf
    exact static_momentum_bound t.toGateParameters (fun hz => hc hz.1) f (hs f hf)
  · intro f hf a ha
    exact case_two_no_square_leading t.toGateParameters hc f (hs f hf) a ha

theorem case_three_static_stable (t : HamiltonianParameters K) (h5 : t.c₅ = 0)
    (hb : t.b₃ = 0) (hc : t.c₄ ≠ 0) (V : Submodule K (Poly K))
    (h1 : (1 : Poly K) ∈ V) (hH : hamiltonian t ∈ V)
    (hs : ∀ f ∈ V, Static t.toGateParameters f)
    (hD : ∀ f ∈ V, bracket (hamiltonian t) f ∈ V) :
    V = Submodule.span K ({1, hamiltonian t} : Set (Poly K)) := by
  refine static_stable_space_eq_span t.toGateParameters ![3, 4]
    (by intro i; fin_cases i <;> norm_num) _ (caseThree t.c₄) 12
    (hamiltonian_case_three_bound t h5 hb) (hamiltonian_case_three_top t)
    (by norm_num) (binomial_ne_zero t.c₄ 4 (by decide)) (case_three_coprime t.c₄ hc)
    (by refine ⟨C t.c₄*X 0^3, ?_⟩; dsimp [caseThree]; ring)
    V h1 hH hs ?_ hD ?_
  · intro f hf
    by_cases hE : t.b₃ = 0 ∧ t.c₅ = 0 ∧ t.b₁+t.c₃ = 0 ∧ 2*t.b₂+4*t.c₄ = 0
    · have h2 : t.b₂ ≠ 0 := by
        intro hz
        have he := hE.2.2.2
        norm_num [hz] at he
        exact hc he
      exact first_refinement_momentum_bound_on_symbol_zero t hb h5 h2 f (hs f hf)
        (hs _ (hD f hf))
    · exact static_momentum_bound t.toGateParameters hE f (hs f hf)
  · intro f hf a ha
    exact case_three_no_square_leading t.toGateParameters hb h5 hc f (hs f hf) a ha

/-- The three new Newton cases, joined without a cutoff or finite-dimensionality
hypothesis. The static equations and Hamiltonian bracket are concrete. -/
theorem newton_static_stable_eq_span (t : HamiltonianParameters K)
    (hnew : t.b₃ ≠ 0 ∨ t.c₄ ≠ 0 ∨ t.c₅ ≠ 0)
    (V : Submodule K (Poly K)) (h1 : (1 : Poly K) ∈ V) (hH : hamiltonian t ∈ V)
    (hs : ∀ f ∈ V, Static t.toGateParameters f)
    (hD : ∀ f ∈ V, bracket (hamiltonian t) f ∈ V) :
    V = Submodule.span K ({1, hamiltonian t} : Set (Poly K)) := by
  by_cases h5 : t.c₅ = 0
  · by_cases hb : t.b₃ = 0
    · apply case_three_static_stable t h5 hb _ V h1 hH hs hD
      tauto
    · exact case_two_static_stable t h5 hb V h1 hH hs hD
  · exact case_one_static_stable t h5 V h1 hH hs hD

end SexticC3.CubeLeading.Polynomial
