import SexticC3.CubeLeadingFlatCore

/-! # All-degree reduction on the older seven-parameter stratum. -/
noncomputable section
set_option linter.unusedSectionVars false
namespace SexticC3.CubeLeading.Polynomial
open MvPolynomial
variable {K : Type*} [Field K] [CharZero K]

/-- First-refinement staticity gives the cutoff on the entire non-affine
seven-parameter stratum, including the infinite-static-sector locus. -/
theorem seven_first_refinement_momentum_bound (t : HamiltonianParameters K)
    (hb : t.b₃ = 0) (h4 : t.c₄ = 0) (h5 : t.c₅ = 0)
    (hnon : t.b₂ ≠ 0 ∨ t.c₃ ≠ 0 ∨ t.c₂ ≠ 0)
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
  have nz : (n : K)+7 ≠ 0 := by exact_mod_cast (show n+7 ≠ 0 by omega)
  have hD := fifth_affine_q_vanish t.toGateParameters (by simp [hb, h5]) _ hDf 0 (n+3)
  simp only [hamiltonian_bracket, bicoeff_add, bicoeff_sub, bicoeff_C_mul,
    bicoeff_q_mul, bicoeff_P_mul, bicoeff_dq, bicoeff_dP] at hD
  norm_num [Nat.add_assoc, hb, h5, high, vanish 0 (n+3), vanish 0 (n+4),
    vanish 1 (n+3), vanish 1 (n+1)] at hD
  have hb2 : t.b₂ = 0 := by
    simpa only [add_assoc, show (6 : K)+1=7 by norm_num, nz, ha, or_false] using hD
  have hD3 := fifth_affine_q_vanish t.toGateParameters (by simp [hb, h5]) _ hDf 1 (n+2)
  simp only [hamiltonian_bracket, bicoeff_add, bicoeff_sub, bicoeff_C_mul,
    bicoeff_q_mul, bicoeff_P_mul, bicoeff_dq, bicoeff_dP] at hD3
  norm_num [Nat.add_assoc, hb, h4, h5, hb2, vanish 1 (n+2), vanish 1 (n+3),
    vanish 0 (n+3), vanish 2 n, vanish 2 (n+2)] at hD3
  have hc3 : t.c₃ = 0 := by
    simpa only [add_assoc, show (6 : K)+1=7 by norm_num, nz, ha, or_false] using hD3
  have hD2 := fifth_affine_q_vanish t.toGateParameters (by simp [hb, h5]) _ hDf 0 (n+2)
  simp only [hamiltonian_bracket, bicoeff_add, bicoeff_sub, bicoeff_C_mul,
    bicoeff_q_mul, bicoeff_P_mul, bicoeff_dq, bicoeff_dP] at hD2
  norm_num [Nat.add_assoc, hb, h4, h5, hb2, hc3, vanish 0 (n+2), vanish 0 (n+3),
    vanish 1 n, vanish 1 (n+2)] at hD2
  have hc2 : t.c₂ = 0 := by
    simpa only [add_assoc, show (6 : K)+1=7 by norm_num, nz, ha, or_false] using hD2
  exact (hnon.elim (fun h => h hb2) (fun h => h.elim (fun h => h hc3) (fun h => h hc2))).elim

/-- The third recurrence determines a bounded-momentum static polynomial from
its first three q coefficients in each momentum degree. -/
theorem static_zero_of_initial_jet (t : GateParameters K) (f : Poly K)
    (hf : Static t f) (N : ℕ) (hP : Bounded ![0, 1] N f)
    (hjet : ∀ i j : ℕ, i < 3 → j ≤ N → bicoeff i j f = 0) : f = 0 := by
  have claim : ∀ m : ℕ, ∀ j : ℕ, N+1-j = m → ∀ i : ℕ, bicoeff i j f = 0 := by
    intro m
    induction m using Nat.strong_induction_on with
    | h m ih =>
      intro j hj i
      by_cases hjN : N < j
      · exact bicoeff_vanish_of_bound hP i j (by norm_num; exact_mod_cast hjN)
      have higher (r : ℕ) (hr : j < r) (s : ℕ) : bicoeff s r f = 0 :=
        ih (N+1-r) (by omega) r rfl s
      by_cases hi : i < 3
      · exact hjet i j hi (by omega)
      obtain ⟨r, hr⟩ : ∃ r : ℕ, i = r+3 := ⟨i-3, by omega⟩
      rw [hr]
      have h := third_recurrence t f hf r j
      simp only [higher (j+1) (by omega), higher (j+2) (by omega),
        higher (j+3) (by omega), ite_self, mul_zero, add_zero, sub_zero] at h
      have n1 : (r : K)+1 ≠ 0 := by exact_mod_cast (show r+1 ≠ 0 by omega)
      have n2 : (r : K)+2 ≠ 0 := by exact_mod_cast (show r+2 ≠ 0 by omega)
      have n3 : (r : K)+3 ≠ 0 := by exact_mod_cast (show r+3 ≠ 0 by omega)
      exact (mul_eq_zero.mp h).resolve_left (mul_ne_zero (mul_ne_zero n1 n2) n3)
  ext m
  rw [← exponent_ext m]
  exact claim _ (m 1) rfl (m 0)

theorem static_eq_of_initial_jet (t : GateParameters K) (f g : Poly K)
    (hf : Static t f) (hg : Static t g) (N : ℕ)
    (hfP : Bounded ![0, 1] N f) (hgP : Bounded ![0, 1] N g)
    (hjet : ∀ i j : ℕ, i < 3 → j ≤ N → bicoeff i j f = bicoeff i j g) : f = g := by
  apply sub_eq_zero.mp
  apply static_zero_of_initial_jet t (f-g) ((staticSubmodule t).sub_mem hf hg) N
    ((boundedSubmodule (K := K) ![0, 1] N).sub_mem hfP hgP)
  intro i j hi hj
  simp only [bicoeff_sub, hjet i j hi hj, sub_self]

end SexticC3.CubeLeading.Polynomial
