import Mathlib.Algebra.Divisibility.Units
import Mathlib.Algebra.Algebra.Basic
import Mathlib.Tactic.LinearCombination
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring

/-!
# The no-slice lemma for a weighted leading form (Lemma K3)

Abstract form of Lemma K3 of `CUBE_LEADING_BOUNDARY_THEOREM.md`.  `LeadingData`
records a leading form `h`, the bracket `D = {h, ·}`, the weighted Euler
operator `Eu`, and the identities they satisfy in `K[q, P]`:

* `D` and `Eu` are compatible with multiplication by `h`;
* the Euler–Cramer identity `wq * q * D s = d * h * ∂_P s - Eu s * h_P`
  (proved from the two Euler relations in `CubeLeadingCore.euler_cramer`);
* the bracket raises the weight by `δ = d - wq - wP`, with `0 < δ < d`;
* there is no nonzero form of negative weight.

A *form of weight `w`* is an eigenvector `Eu s = w * s`.  From these identities
alone, in a domain of characteristic zero in which nonzero integers are units
and `h` is relatively prime to `h_P`, the file proves

* `kernel_forms`: a form killed by `D` is a weight-zero element times a power of `h`;
* `no_preimage`: `D s = c * h ^ k` has no solution with `c ≠ 0` of weight zero;
* `no_slice`: a form killed by some power of `D` is a weight-zero element times
  a power of `h`;
* `leading_forms_of_stable`: Lemma K4, the leading forms of a stable set with
  bounded weights are weight-zero elements times powers of `h`.

Nothing here assumes the conclusion: the hypotheses are the structural
identities listed above.  They are *not* instantiated for the bivariate
polynomial ring in this file.
-/

set_option linter.unusedSectionVars false

namespace SexticC3.CubeLeading

structure LeadingData (R : Type*) [CommRing R] where
  h : R
  hP : R
  qw : R
  D : R → R
  Eu : R → R
  dP : R → R
  d : ℤ
  δ : ℤ
  D_zero : D 0 = 0
  Eu_zero : Eu 0 = 0
  D_mul : ∀ s, D (h * s) = h * D s
  Eu_mul : ∀ s, Eu (h * s) = (d : R) * (h * s) + h * Eu s
  cramer : ∀ s, qw * D s = (d : R) * h * dP s - Eu s * hP
  shift : ∀ (w : ℤ) (s : R), Eu s = (w : R) * s → Eu (D s) = ((w + δ : ℤ) : R) * D s
  neg : ∀ (w : ℤ) (s : R), w < 0 → Eu s = (w : R) * s → s = 0
  δ_pos : 0 < δ
  δ_lt : δ < d

variable {R : Type*} [CommRing R] [IsDomain R] [CharZero R] [DecompositionMonoid R]
  [Algebra ℚ R]

theorem isUnit_intCast (n : ℤ) (hn : n ≠ 0) : IsUnit ((n : ℤ) : R) := by
  have h1 : IsUnit ((n : ℤ) : ℚ) := IsUnit.mk0 _ (Int.cast_ne_zero.mpr hn)
  have h2 := h1.map (algebraMap ℚ R)
  simpa using h2

namespace LeadingData

variable (L : LeadingData R)

theorem Eu_scalar_pow (c : R) (hc : L.Eu c = 0) (k : ℕ) :
    L.Eu (c * L.h ^ k) = (((k : ℤ) * L.d : ℤ) : R) * (c * L.h ^ k) := by
  induction k with
  | zero => simp [hc]
  | succ k ih =>
      have e : c * L.h ^ (k + 1) = L.h * (c * L.h ^ k) := by ring
      rw [e, L.Eu_mul, ih]
      push_cast
      ring

/-- Divisibility step: a form of nonzero weight whose bracket is a multiple of
`h` is itself a multiple of `h`. -/
theorem dvd_of_bracket (hrel : IsRelPrime L.h L.hP) (w : ℤ) (hw : w ≠ 0) (s m : R)
    (hs : L.Eu s = (w : R) * s) (hD : L.D s = m * L.h) : L.h ∣ s := by
  have key := L.cramer s
  rw [hs, hD] at key
  have h1 : L.h ∣ ((w : R) * s) * L.hP :=
    ⟨(L.d : R) * L.dP s - L.qw * m, by linear_combination key⟩
  have h2 : L.h ∣ (w : R) * s := hrel.dvd_of_dvd_mul_right h1
  exact (IsUnit.dvd_mul_left (isUnit_intCast w hw)).mp h2

theorem form_div (hh : L.h ≠ 0) (w : ℤ) (s : R)
    (hs : L.Eu (L.h * s) = (w : R) * (L.h * s)) :
    L.Eu s = ((w - L.d : ℤ) : R) * s := by
  have e := L.Eu_mul s
  rw [hs] at e
  apply mul_left_cancel₀ hh
  push_cast
  linear_combination -e

theorem kernel_forms (hh : L.h ≠ 0) (hrel : IsRelPrime L.h L.hP) :
    ∀ (n : ℕ) (w : ℤ), w ≤ n → ∀ s : R, L.Eu s = (w : R) * s → L.D s = 0 →
      ∃ (k : ℕ) (c : R), L.Eu c = 0 ∧ s = c * L.h ^ k := by
  have small : ∀ (w : ℤ), w ≤ 0 → ∀ s : R, L.Eu s = (w : R) * s →
      ∃ (k : ℕ) (c : R), L.Eu c = 0 ∧ s = c * L.h ^ k := by
    intro w hw s hs
    rcases lt_or_eq_of_le hw with hlt | heq
    · exact ⟨0, 0, L.Eu_zero, by simp [L.neg w s hlt hs]⟩
    · refine ⟨0, s, ?_, by simp⟩
      rw [hs, heq]
      simp
  intro n
  induction n with
  | zero =>
      intro w hw s hs _
      exact small w (by simpa using hw) s hs
  | succ n ih =>
      intro w hw s hs hD
      by_cases hw0 : w ≤ 0
      · exact small w hw0 s hs
      · have hwne : w ≠ 0 := by omega
        obtain ⟨s1, rfl⟩ := L.dvd_of_bracket hrel w hwne s 0 hs (by simpa using hD)
        have hs1 := L.form_div hh w s1 hs
        have hD1 : L.D s1 = 0 := by
          have e := L.D_mul s1
          rw [hD] at e
          exact (mul_eq_zero.mp e.symm).resolve_left hh
        have hd := L.δ_pos
        have hd' := L.δ_lt
        have hle : w - L.d ≤ (n : ℤ) := by
          push_cast at hw
          omega
        obtain ⟨k, c, hc, hk⟩ := ih (w - L.d) hle s1 hs1 hD1
        exact ⟨k + 1, c, hc, by rw [hk]; ring⟩

theorem no_preimage (hh : L.h ≠ 0) (hrel : IsRelPrime L.h L.hP) :
    ∀ (k : ℕ) (w : ℤ) (s c : R), L.Eu s = (w : R) * s → L.Eu c = 0 → c ≠ 0 →
      L.D s = c * L.h ^ k → False := by
  intro k
  induction k with
  | zero =>
      intro w s c hs hc hc0 hD
      have hD' : L.D s = c := by simpa using hD
      have e := L.shift w s hs
      rw [hD', hc] at e
      have hz : ((w + L.δ : ℤ) : R) = 0 := by
        rcases mul_eq_zero.mp e.symm with h | h
        · exact h
        · exact absurd h hc0
      have hw : w + L.δ = 0 := by exact_mod_cast hz
      have hneg : w < 0 := by have := L.δ_pos; omega
      have s0 := L.neg w s hneg hs
      rw [s0, L.D_zero] at hD'
      exact hc0 hD'.symm
  | succ k ih =>
      intro w s c hs hc hc0 hD
      have e := L.shift w s hs
      rw [hD, L.Eu_scalar_pow c hc (k + 1)] at e
      have hne : c * L.h ^ (k + 1) ≠ 0 := mul_ne_zero hc0 (pow_ne_zero _ hh)
      have hz : ((((k + 1 : ℕ) : ℤ) * L.d : ℤ) : R) = ((w + L.δ : ℤ) : R) :=
        mul_right_cancel₀ hne e
      have hw : (((k + 1 : ℕ) : ℤ) * L.d) = w + L.δ := by exact_mod_cast hz
      have hd := L.δ_pos
      have hd' := L.δ_lt
      have hkd : (0 : ℤ) ≤ (k : ℤ) * L.d := mul_nonneg (by positivity) (by linarith)
      have hwne : w ≠ 0 := by
        push_cast at hw
        intro h0
        nlinarith
      have hD2 : L.D s = (c * L.h ^ k) * L.h := by rw [hD]; ring
      obtain ⟨s1, rfl⟩ := L.dvd_of_bracket hrel w hwne s (c * L.h ^ k) hs hD2
      have hs1 := L.form_div hh w s1 hs
      have hD1 : L.D s1 = c * L.h ^ k := by
        have e2 := L.D_mul s1
        rw [hD] at e2
        apply mul_left_cancel₀ hh
        rw [← e2]
        ring
      exact ih (w - L.d) s1 c hs1 hc hc0 hD1

/-- Lemma K3: a form annihilated by a power of the bracket is a weight-zero
element times a power of the leading form. -/
theorem no_slice (hh : L.h ≠ 0) (hrel : IsRelPrime L.h L.hP) :
    ∀ (n : ℕ) (w : ℤ) (t : R), L.Eu t = (w : R) * t → L.D^[n] t = 0 →
      ∃ (k : ℕ) (c : R), L.Eu c = 0 ∧ t = c * L.h ^ k := by
  intro n
  induction n with
  | zero =>
      intro w t _ ht
      exact ⟨0, 0, L.Eu_zero, by simpa using ht⟩
  | succ n ih =>
      intro w t hw ht
      rw [Function.iterate_succ_apply] at ht
      obtain ⟨k, c, hc, hk⟩ := ih (w + L.δ) (L.D t) (L.shift w t hw) ht
      by_cases hc0 : c = 0
      · have hD : L.D t = 0 := by rw [hk, hc0]; simp
        exact L.kernel_forms hh hrel w.toNat w (Int.self_le_toNat w) t hw hD
      · exact (L.no_preimage hh hrel k w t c hw hc hc0 hk).elim

/-- Lemma K4, abstractly.  Let `DH` be an operator whose leading part is the
bracket `L.D`: whenever `L.D (lead G) ≠ 0`, the leading form of `DH G` is
`L.D (lead G)` and the weight goes up by `δ`.  If `V` is `DH`-stable with
weights bounded above, every leading form of `V` is a weight-zero element times
a power of `h`.  Nilpotence is derived for the induced leading operation, not
assumed for `DH`. -/
theorem leading_forms_of_stable (hh : L.h ≠ 0) (hrel : IsRelPrime L.h L.hP)
    (DH lead : R → R) (wt : R → ℤ) (V : Set R) (N : ℤ)
    (hV : ∀ G ∈ V, DH G ∈ V) (hN : ∀ G ∈ V, wt G ≤ N)
    (hlead : ∀ G, L.D (lead G) ≠ 0 →
      lead (DH G) = L.D (lead G) ∧ wt (DH G) = wt G + L.δ)
    (hform : ∀ G, L.Eu (lead G) = (wt G : R) * lead G) :
    ∀ G ∈ V, ∃ (k : ℕ) (c : R), L.Eu c = 0 ∧ lead G = c * L.h ^ k := by
  intro G hG
  suffices hm : ∃ m : ℕ, L.D^[m] (lead G) = 0 by
    obtain ⟨m, hm⟩ := hm
    exact L.no_slice hh hrel m (wt G) (lead G) (hform G) hm
  by_contra hall
  push_neg at hall
  have claim : ∀ m : ℕ, DH^[m] G ∈ V ∧ lead (DH^[m] G) = L.D^[m] (lead G) ∧
      wt (DH^[m] G) = wt G + (m : ℤ) * L.δ := by
    intro m
    induction m with
    | zero => simp [hG]
    | succ m ih =>
        obtain ⟨h1, h2, h3⟩ := ih
        have hne : L.D (lead (DH^[m] G)) ≠ 0 := by
          rw [h2]
          have hm1 := hall (m + 1)
          rwa [Function.iterate_succ_apply'] at hm1
        obtain ⟨h4, h5⟩ := hlead (DH^[m] G) hne
        refine ⟨?_, ?_, ?_⟩
        · rw [Function.iterate_succ_apply']
          exact hV _ h1
        · rw [Function.iterate_succ_apply', h4, h2]
          exact (Function.iterate_succ_apply' _ _ _).symm
        · rw [Function.iterate_succ_apply', h5, h3]
          push_cast
          ring
  obtain ⟨h1, _, h3⟩ := claim ((N - wt G).toNat + 1)
  have hb := hN _ h1
  rw [h3] at hb
  have hδ := L.δ_pos
  have ht : N - wt G ≤ ((N - wt G).toNat : ℤ) := Int.self_le_toNat _
  have hpos : (0 : ℤ) ≤ ((N - wt G).toNat : ℤ) := by positivity
  push_cast at hb
  nlinarith

end LeadingData

end SexticC3.CubeLeading
