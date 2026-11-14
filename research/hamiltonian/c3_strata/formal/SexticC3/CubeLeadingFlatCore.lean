import SexticC3.CubeLeadingTransport

/-! # Persistent-core classification in the original (q,p) coordinates. -/
noncomputable section
set_option linter.unusedSectionVars false
namespace SexticC3.CubeLeading.Polynomial
open MvPolynomial
variable {K : Type*} [Field K] [CharZero K]

/-- The persistent intersection of the two relevant flat static gates. -/
def FlatPersistent (H f : Poly K) : Prop := ∀ n : ℕ,
  flatContraction 3 H ((bracket H)^[n] f) = 0 ∧
  flatContraction 5 H ((bracket H)^[n] f) = 0

lemma iterate_bracket_shear (a : K) (H f : Poly K) (n : ℕ) :
    (bracket (shear a H))^[n] (shear a f) = shear a ((bracket H)^[n] f) := by
  induction n with
  | zero => rfl
  | succ n ih => rw [Function.iterate_succ_apply', ih, bracket_shear, Function.iterate_succ_apply']

lemma static_flat_transport (t : HamiltonianParameters K) (f : Poly K) :
    (flatContraction 3 (shear 1 (hamiltonian t)) (shear 1 f) = 0 ∧
     flatContraction 5 (shear 1 (hamiltonian t)) (shear 1 f) = 0) ↔
      Static t.toGateParameters f := by
  rw [flat_third_gate_transport, flat_fifth_gate_transport]
  have hmap (g : Poly K) : shear 1 g = 0 ↔ g = 0 := by
    constructor
    · intro he
      apply shear_injective (1 : K)
      simpa using he
    · rintro rfl
      exact (shear (1 : K)).map_zero
  rw [hmap, hmap]
  have h6 : (C (-6) : Poly K) ≠ 0 := by
    norm_num [map_neg, map_ofNat]
  have h120 : (C (-120) : Poly K) ≠ 0 := by
    norm_num [map_neg, map_ofNat]
  simp only [mul_eq_zero, h6, h120, false_or, Static]

lemma persistent_flat_transport (t : HamiltonianParameters K) (f : Poly K) :
    FlatPersistent (shear 1 (hamiltonian t)) (shear 1 f) ↔ f ∈ persistentCore t := by
  rw [mem_persistentCore]
  simp only [FlatPersistent, iterate_bracket_shear, static_flat_transport]

/-- All-degree classification for the three new Newton strata, stated entirely
with the actual original-coordinate flat contractions and Hamiltonian bracket.
The partner is an arbitrary polynomial; no cutoff, dimension or kernel
classification is supplied as a hypothesis. -/
theorem flat_newton_persistent_core (t : HamiltonianParameters K)
    (hnew : t.b₃ ≠ 0 ∨ t.c₄ ≠ 0 ∨ t.c₅ ≠ 0) (f : Poly K) :
    FlatPersistent (shear 1 (hamiltonian t)) f ↔
      ∃ a b : K, f = C a+C b*shear 1 (hamiltonian t) := by
  constructor
  · intro hf
    let g := shear (-1) f
    have hfg : shear 1 g = f := by simp [g, shear_comp]
    have hg : g ∈ persistentCore t := (persistent_flat_transport t g).mp (by rwa [hfg])
    rw [newton_persistent_core t hnew, Submodule.mem_span_pair] at hg
    obtain ⟨a, b, he⟩ := hg
    refine ⟨a, b, ?_⟩
    have he' := congrArg (shear 1) he
    simp only [map_add, ← C_mul', map_mul, map_one, mul_one, shear_C, hfg] at he'
    exact he'.symm
  · rintro ⟨a, b, rfl⟩
    have hg : C a+C b*hamiltonian t ∈ persistentCore t := by
      rw [newton_persistent_core t hnew, Submodule.mem_span_pair]
      exact ⟨a, b, by simp [← C_mul']⟩
    have h := (persistent_flat_transport t _).mpr hg
    simpa using h


lemma bounded_pow {w : Fin 2 → ℕ} {n : ℤ} {f : Poly K}
    (hf : Bounded w n f) (k : ℕ) : Bounded w ((k : ℤ)*n) (f^k) := by
  induction k with
  | zero => simpa using bounded_of_homogeneous (isWeightedHomogeneous_C (weights w) (1 : K))
  | succ k ih =>
    have hb := bounded_mul ih hf
    convert hb using 1 <;> simp [pow_succ, Nat.cast_add, add_mul]

lemma bounded_iterate_pderiv {w : Fin 2 → ℕ} {n : ℤ} {f : Poly K}
    (hf : Bounded w n f) (i : Fin 2) (k : ℕ) :
    Bounded w (n-(k : ℤ)*w i) ((pderiv i)^[k] f) := by
  induction k with
  | zero => simpa using hf
  | succ k ih =>
    have hb := bounded_pderiv ih i
    convert hb using 1 <;> simp [Function.iterate_succ_apply', Nat.cast_add, add_mul] <;> ring

lemma bounded_negative_zero {w : Fin 2 → ℕ} {n : ℤ} {f : Poly K}
    (hf : Bounded w n f) (hn : n < 0) : f = 0 := by
  ext m
  simp only [coeff_zero]
  by_contra hc
  have h := hf m hc
  rw [weight_pair] at h
  have hp : (0 : ℤ) ≤ (w 0 : ℤ)*m 0+(w 1 : ℤ)*m 1 := by positivity
  omega

lemma original_hamiltonian_total_bound (t : HamiltonianParameters K) :
    Bounded ![1, 1] 6 (shear 1 (hamiltonian t)) := by
  have qpow (i : ℕ) : Bounded ![1, 1] i ((X 0 : Poly K)^i) := by
    simpa [← qP_monomial] using bounded_monomial (K := K) ![1, 1] i i 0 1 (by norm_num)
  have Pbound : Bounded ![1, 1] 2 ((X 1 : Poly K)+X 0^2) :=
    (boundedSubmodule _ _).add_mem
      (by simpa [← qP_monomial] using bounded_monomial (K := K) ![1, 1] 2 0 1 1 (by norm_num))
      (qpow 2)
  have mon (i j : ℕ) (a : K) (hij : i+2*j ≤ 6) :
      Bounded ![1, 1] 6 (shear 1 (monomial (exponent i j) a)) := by
    have hp := bounded_mul (qpow i) (bounded_pow Pbound j)
    have hp' : Bounded ![1, 1] ((i : ℤ)+j*2)
        (C a*(X 0^i*((X 1 : Poly K)+X 0^2)^j)) := by
      simpa only [C_mul'] using (boundedSubmodule (K := K) ![1, 1] ((i : ℤ)+j*2)).smul_mem a hp
    apply bounded_mono (by simpa [← qP_monomial, map_mul, map_pow, mul_assoc] using hp')
    have hij' : (i : ℤ)+2*j ≤ 6 := by exact_mod_cast hij
    linarith
  change shear 1 (hamiltonian t) ∈ boundedSubmodule ![1, 1] 6
  simp only [hamiltonian, map_add]
  repeat' apply (boundedSubmodule (K := K) ![1, 1] 6).add_mem
  all_goals exact mon _ _ _ (by decide)

/-- All higher contractions vanish, because the original Hamiltonian has total
degree at most six. The partner is unrestricted. -/
theorem higher_flat_gates_zero (t : HamiltonianParameters K) (f : Poly K)
    (k : ℕ) (hk : 6 < k) : flatContraction k (shear 1 (hamiltonian t)) f = 0 := by
  unfold flatContraction
  apply Finset.sum_eq_zero
  intro r hr
  have hrk : r ≤ k := by have := Finset.mem_range.mp hr; omega
  have hb := bounded_iterate_pderiv
    (bounded_iterate_pderiv (original_hamiltonian_total_bound t) 1 r) 0 (k-r)
  have hz : flatMixed (k-r) r (shear 1 (hamiltonian t)) = 0 :=
    bounded_negative_zero hb (by norm_num; omega)
  rw [hz, mul_zero, zero_mul]

/-- All odd flat gates, including those of order greater than six. -/
def AllFlatPersistent (H f : Poly K) : Prop := ∀ n k : ℕ, 3 ≤ k → Odd k →
  flatContraction k H ((bracket H)^[n] f) = 0

lemma all_flat_persistent_iff (t : HamiltonianParameters K) (f : Poly K) :
    AllFlatPersistent (shear 1 (hamiltonian t)) f ↔
      FlatPersistent (shear 1 (hamiltonian t)) f := by
  constructor
  · intro h n
    exact ⟨h n 3 (by decide) (by decide), h n 5 (by decide) (by decide)⟩
  · intro h n k h3 hk
    by_cases h6 : 6 < k
    · exact higher_flat_gates_zero t _ k h6
    · have hc : k = 3 ∨ k = 5 := by obtain ⟨r, hr⟩ := hk; omega
      rcases hc with rfl | rfl
      · exact (h n).1
      · exact (h n).2

/-- Theorem K for all polynomial degrees and all odd flat gates, over every
characteristic-zero field, in the original (q,p) coordinates. -/
theorem all_flat_newton_persistent_core (t : HamiltonianParameters K)
    (hnew : t.b₃ ≠ 0 ∨ t.c₄ ≠ 0 ∨ t.c₅ ≠ 0) (f : Poly K) :
    AllFlatPersistent (shear 1 (hamiltonian t)) f ↔
      ∃ a b : K, f = C a+C b*shear 1 (hamiltonian t) := by
  rw [all_flat_persistent_iff, flat_newton_persistent_core t hnew]

end SexticC3.CubeLeading.Polynomial
