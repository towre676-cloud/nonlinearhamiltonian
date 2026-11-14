import SexticC3.CubeLeadingCutoff

/-! # The reduced Hamiltonian and the exceptional E=0 cutoff. -/
noncomputable section
set_option linter.unusedSectionVars false
namespace SexticC3.CubeLeading.Polynomial
open MvPolynomial
variable {K : Type*} [Field K] [CharZero K]

structure HamiltonianParameters (K : Type*) extends GateParameters K where
  b₀ : K
  c₀ : K
  c₁ : K
  c₂ : K

def hamiltonian (t : HamiltonianParameters K) : Poly K :=
  monomial (exponent 0 3) 1 +
  monomial (exponent 0 1) t.b₀ + monomial (exponent 1 1) t.b₁ +
  monomial (exponent 2 1) t.b₂ + monomial (exponent 3 1) t.b₃ +
  monomial (exponent 0 0) t.c₀ + monomial (exponent 1 0) t.c₁ +
  monomial (exponent 2 0) t.c₂ + monomial (exponent 3 0) t.c₃ +
  monomial (exponent 4 0) t.c₄ + monomial (exponent 5 0) t.c₅

lemma hamiltonian_bracket (t : HamiltonianParameters K) (f : Poly K) :
    bracket (hamiltonian t) f =
    C t.b₁*(X 1*pderiv 1 f) + C (2*t.b₂)*(X 0*(X 1*pderiv 1 f)) +
    C (3*t.b₃)*(X 0*(X 0*(X 1*pderiv 1 f))) +
    C t.c₁*pderiv 1 f + C (2*t.c₂)*(X 0*pderiv 1 f) +
    C (3*t.c₃)*(X 0*(X 0*pderiv 1 f)) +
    C (4*t.c₄)*(X 0*(X 0*(X 0*pderiv 1 f))) +
    C (5*t.c₅)*(X 0*(X 0*(X 0*(X 0*pderiv 1 f)))) -
    C 3*(X 1*(X 1*pderiv 0 f)) - C t.b₀*pderiv 0 f -
    C t.b₁*(X 0*pderiv 0 f) - C t.b₂*(X 0*(X 0*pderiv 0 f)) -
    C t.b₃*(X 0*(X 0*(X 0*pderiv 0 f))) := by
  simp [hamiltonian, ← qP_monomial, bracket, pderiv_mul, pderiv_pow,
    pderiv_C_mul, pderiv_X, Pi.single_apply, map_ofNat, Derivation.map_natCast]
  ring

set_option maxHeartbeats 2000000 in
lemma hamiltonian_static (t : HamiltonianParameters K) :
    Static t.toGateParameters (hamiltonian t) := by
  constructor <;> simp [thirdGate, fifthGate, hamiltonian, ← qP_monomial,
    pderiv_mul, pderiv_pow, pderiv_C_mul, pderiv_X, Pi.single_apply, map_ofNat, Derivation.map_natCast]
  all_goals simp only [
    show (2 : Poly K) = C (2 : K) by exact (map_ofNat (C : K →+* Poly K) 2).symm,
    show (3 : Poly K) = C (3 : K) by exact (map_ofNat (C : K →+* Poly K) 3).symm,
    show (4 : Poly K) = C (4 : K) by exact (map_ofNat (C : K →+* Poly K) 4).symm,
    show (5 : Poly K) = C (5 : K) by exact (map_ofNat (C : K →+* Poly K) 5).symm,
    pderiv_C, map_zero, mul_zero, zero_mul, add_zero, zero_add]
  all_goals try simp only [map_ofNat]
  all_goals ring

lemma one_static (t : GateParameters K) : Static t (1 : Poly K) := by
  simp [Static, thirdGate, fifthGate, pderiv_one]

/-- On E=0 a high momentum coefficient is excluded in the first refinement
as soon as b₂ is nonzero. This includes the c₄≠0 Newton case on E=0. -/
theorem first_refinement_momentum_bound_on_symbol_zero (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h5 : t.c₅ = 0) (h2 : t.b₂ ≠ 0)
    (f : Poly K) (hf : Static t.toGateParameters f)
    (hDf : Static t.toGateParameters (bracket (hamiltonian t) f)) :
    Bounded ![0, 1] 6 f := by
  classical
  let m := degree ![0, 1] f
  have hbound : Bounded ![0, 1] m f := bounded_degree _ f
  by_cases hm : m ≤ 6
  · exact bounded_mono hbound (by exact_mod_cast hm)
  have hf0 : f ≠ 0 := by intro hz; simp [m, degree, hz] at hm
  have hs : f.support.Nonempty := by simpa [Finset.nonempty_iff_ne_empty, support_eq_empty] using hf0
  obtain ⟨e, he, hmax⟩ := Finset.exists_mem_eq_sup f.support hs
    (fun e => (![0, 1] : Fin 2 → ℕ) 0 * e 0 + (![0, 1] : Fin 2 → ℕ) 1 * e 1)
  have hej : e 1 = m := by simpa [m, degree] using hmax.symm
  have hec : bicoeff (e 0) m f ≠ 0 := by
    simpa [bicoeff, ← hej, exponent_ext] using mem_support_iff.mp he
  obtain ⟨n, hn⟩ : ∃ n : ℕ, m = n+7 := ⟨m-7, by omega⟩
  have vanish (i j : ℕ) : bicoeff (i+1) (j+4) f = 0 :=
    fifth_affine_q_vanish t.toGateParameters (by simp [hb, h5]) f hf i j
  have he0 : e 0 = 0 := by
    by_contra he0
    obtain ⟨i, hi⟩ : ∃ i : ℕ, e 0 = i+1 := ⟨e 0-1, by omega⟩
    apply hec
    simpa [hi, hn, Nat.add_assoc] using vanish i (n+3)
  have ha : bicoeff 0 (n+7) f ≠ 0 := by simpa [he0, hn] using hec
  have high : bicoeff 0 (n+8) f = 0 :=
    bicoeff_vanish_of_bound hbound 0 (n+8) (by simp [hn])
  have hD := fifth_affine_q_vanish t.toGateParameters (by simp [hb, h5])
    _ hDf 0 (n+3)
  simp only [hamiltonian_bracket, bicoeff_add, bicoeff_sub, bicoeff_C_mul,
    bicoeff_q_mul, bicoeff_P_mul, bicoeff_dq, bicoeff_dP] at hD
  norm_num [Nat.add_assoc, hb, h5, high, vanish 0 (n+3), vanish 0 (n+4),
    vanish 1 (n+3), vanish 1 (n+1)] at hD
  have nz : (n : K)+7 ≠ 0 := by exact_mod_cast (show n+7 ≠ 0 by omega)
  have : False := by
    simpa only [add_assoc, show (6 : K)+1=7 by norm_num,
      h2, nz, ha, or_false, false_or] using hD
  exact this.elim


end SexticC3.CubeLeading.Polynomial
