import SexticC3.HomogeneousCoordinates
import Mathlib.RingTheory.MvPolynomial.EulerIdentity

noncomputable section

namespace SexticC3.Differential

open MvPolynomial

variable {R : Type*} [CommRing R]

theorem homogeneous_zero_degree (F : Poly (R := R)) (h : F.IsHomogeneous 0) :
    F = C (coeff 0 F) := by
  have hmem := homogeneousComponent_of_mem (m := 0) ((mem_homogeneousSubmodule 0 F).mpr h)
  simpa using hmem.symm

private theorem iterated_isHomogeneous (x : Bool) (r n : ℕ) (F : Poly (R := R))
    (hF : F.IsHomogeneous n) : ((pderiv x)^[r] F).IsHomogeneous (n-r) := by
  induction r with
  | zero => simpa using hF
  | succ r ih =>
    rw [Function.iterate_succ_apply', Nat.sub_succ]
    exact ih.pderiv

private theorem iterated_eq_zero (x : Bool) (r n : ℕ) (F : Poly (R := R))
    (hF : F.IsHomogeneous n) (h : n < r) : (pderiv x)^[r] F = 0 := by
  induction r with
  | zero => omega
  | succ r ih =>
    rw [Function.iterate_succ_apply']
    by_cases he : n < r
    · rw [ih he, map_zero]
    · have hh := iterated_isHomogeneous x r n F hF
      rw [show n-r = 0 by omega] at hh
      rw [homogeneous_zero_degree _ hh, pderiv_C]

private theorem mixed_isHomogeneous (r s n : ℕ) (F : Poly (R := R))
    (hF : F.IsHomogeneous n) : (mixed r s F).IsHomogeneous (n-s-r) :=
  iterated_isHomogeneous false r (n-s) _ (iterated_isHomogeneous true s n F hF)

private theorem mixed_eq_zero (r s n : ℕ) (F : Poly (R := R))
    (hF : F.IsHomogeneous n) (h : n < r+s) : mixed r s F = 0 := by
  unfold mixed
  by_cases hs : n < s
  · rw [iterated_eq_zero true s n F hF hs, iterated_pderiv_zero]
  · exact iterated_eq_zero false r (n-s) _ (iterated_isHomogeneous true s n F hF) (by omega)

theorem list_sum_homogeneous (n : ℕ) (xs : List (Poly (R := R)))
    (h : ∀ F ∈ xs, F.IsHomogeneous n) : xs.sum.IsHomogeneous n := by
  induction xs with
  | nil => exact isHomogeneous_zero Bool R n
  | cons F xs ih =>
    exact (h F (by simp)).add (ih fun G hG => h G (by simp [hG]))

theorem contraction_isHomogeneous (k m n : ℕ) (F G : Poly (R := R))
    (hF : F.IsHomogeneous m) (hG : G.IsHomogeneous n) (hm : k ≤ m) (hn : k ≤ n) :
    (contraction k F G).IsHomogeneous (m+n-2*k) := by
  unfold contraction
  apply list_sum_homogeneous
  intro P hP
  obtain ⟨s, hs, rfl⟩ := List.mem_map.mp hP
  have hs' := List.mem_range.mp hs
  have h := ((mixed_isHomogeneous (k-s) s m F hF).C_mul ((-1 : R)^s * (Nat.choose k s : R))).mul
    (mixed_isHomogeneous s (k-s) n G hG)
  convert h using 1
  omega

theorem contraction_eq_zero_of_degree_lt (k n : ℕ) (F G : Poly (R := R))
    (hG : G.IsHomogeneous n) (hn : n < k) : contraction k F G = 0 := by
  unfold contraction
  apply List.sum_eq_zero
  intro P hP
  obtain ⟨s, hs, rfl⟩ := List.mem_map.mp hP
  have hs' := List.mem_range.mp hs
  rw [mixed_eq_zero s (k-s) n G hG (by omega), mul_zero]

private def gateMap (F : Poly (R := R)) (k : ℕ) : Poly (R := R) →+ Poly (R := R) where
  toFun := contraction k F
  map_zero' := contraction_zero_right k F
  map_add' := contraction_add_right k F

private theorem component_gate_zero (L : Poly (R := R) →+ Poly (R := R)) (G : Poly)
    (valid : ℕ → Prop) [DecidablePred valid] (degree : ℕ → ℕ)
    (hzero : ∀ n P, P.IsHomogeneous n → ¬valid n → L P = 0)
    (hdegree : ∀ n P, P.IsHomogeneous n → valid n → (L P).IsHomogeneous (degree n))
    (hinj : ∀ n m, valid n → valid m → degree n = degree m → n = m)
    (hG : L G = 0) (n : ℕ) : L (homogeneousComponent n G) = 0 := by
  classical
  by_cases hv : valid n
  · by_cases hn : n ≤ G.totalDegree
    · let s := Finset.range (G.totalDegree+1)
      have hsum : ∑ j ∈ s, L (homogeneousComponent j G) = 0 := by
        rw [← map_sum, sum_homogeneousComponent, hG]
      have hc := congrArg (homogeneousComponent (degree n)) hsum
      rw [map_sum, map_zero] at hc
      have hsingle : (∑ j ∈ s, homogeneousComponent (degree n) (L (homogeneousComponent j G))) =
          homogeneousComponent (degree n) (L (homogeneousComponent n G)) := by
        apply Finset.sum_eq_single_of_mem n (by simp [s, Nat.lt_succ_iff, hn])
        intro j _ hj
        by_cases hvalid : valid j
        · rw [homogeneousComponent_of_mem (hdegree j _ (homogeneousComponent_isHomogeneous _ _) hvalid)]
          exact if_neg (fun he => hj (hinj n j hv hvalid he).symm)
        · rw [hzero j _ (homogeneousComponent_isHomogeneous _ _) hvalid, map_zero]
      rw [hsingle, homogeneousComponent_of_mem (hdegree n _ (homogeneousComponent_isHomogeneous _ _) hv),
        if_pos rfl] at hc
      exact hc
    · rw [homogeneousComponent_eq_zero n G (by omega), map_zero]
  · exact hzero n _ (homogeneousComponent_isHomogeneous _ _) hv

theorem firstRefinement_homogeneousComponent (F G : Poly (R := R)) (hF : F.IsHomogeneous 6)
    (h : FirstRefinement F G) (n : ℕ) :
    FirstRefinement F (homogeneousComponent n G) := by
  have hs (k : ℕ) (hk : k ≤ 6) (hz : contraction k F G = 0) :
      contraction k F (homogeneousComponent n G) = 0 :=
    component_gate_zero (gateMap F k) G (fun j => k ≤ j) (fun j => 6+j-2*k)
      (fun j P hp hv => contraction_eq_zero_of_degree_lt k j F P hp (by omega))
      (fun j P hp hv => contraction_isHomogeneous k 6 j F P hF hp hk hv)
      (fun j l hj hl he => by dsimp at he; omega) hz n
  have hd (k : ℕ) (hk : k ≤ 5) (hz : contraction k F (contraction 1 F G) = 0) :
      contraction k F (contraction 1 F (homogeneousComponent n G)) = 0 :=
    component_gate_zero ((gateMap F k).comp (gateMap F 1)) G (fun j => 1 ≤ j)
      (fun j => 6+(j+4)-2*k)
      (fun j P hp hv => by
        change contraction k F (contraction 1 F P) = 0
        rw [contraction_eq_zero_of_degree_lt 1 j F P hp (by omega), contraction_zero_right])
      (fun j P hp hv => by
        change (contraction k F (contraction 1 F P)).IsHomogeneous (6+(j+4)-2*k)
        have hP := contraction_isHomogeneous 1 6 j F P hF hp (by decide) hv
        rw [show 6+j-2*1 = j+4 by omega] at hP
        exact contraction_isHomogeneous k 6 (j+4) F _ hF hP (by omega) (by omega))
      (fun j l hj hl he => by dsimp at he; omega) hz n
  exact ⟨hs 3 (by decide) h.1, hs 5 (by decide) h.2.1,
    hd 3 (by decide) h.2.2.1, hd 5 (by decide) h.2.2.2⟩

theorem persistentCore_constant (F : Poly (R := R)) (c : R) :
    PersistentCore F (C c) := by
  apply core_of_stationary
  all_goals
    apply contraction_eq_zero_of_degree_lt _ 0
    · exact isHomogeneous_C Bool c
    · decide

theorem persistentCore_add (F G U : Poly (R := R))
    (hG : PersistentCore F G) (hU : PersistentCore F U) : PersistentCore F (G+U) := by
  have hi (i : ℕ) :
      (contraction 1 F)^[i] (G+U) = (contraction 1 F)^[i] G + (contraction 1 F)^[i] U := by
    induction i with
    | zero => rfl
    | succ i ih => simp only [Function.iterate_succ_apply', ih, contraction_add_right]
  intro i
  rw [hi, contraction_add_right, contraction_add_right, (hG i).1, (hU i).1, (hG i).2, (hU i).2]
  simp

theorem persistentCore_sum {ι : Type*} (F : Poly (R := R)) (s : Finset ι)
    (P : ι → Poly (R := R)) (h : ∀ j ∈ s, PersistentCore F (P j)) :
    PersistentCore F (∑ j ∈ s, P j) := by
  classical
  induction s using Finset.induction_on with
  | empty => simpa using persistentCore_zero F
  | insert j s hj ih =>
    rw [Finset.sum_insert hj]
    exact persistentCore_add F _ _ (h j (by simp)) (ih fun i hi => h i (by simp [hi]))

/-- A homogeneous first-refinement theorem implies the polynomial one,
since each gate separates the input degrees and constants are stationary. -/
theorem firstRefinement_iff_persistent_of_homogeneous (F G : Poly (R := R))
    (hF : F.IsHomogeneous 6)
    (hpos : ∀ n ≥ 1, ∀ P : Poly (R := R), P.IsHomogeneous n →
      FirstRefinement F P → PersistentCore F P) :
    FirstRefinement F G ↔ PersistentCore F G := by
  constructor
  · intro h
    rw [← sum_homogeneousComponent G]
    apply persistentCore_sum
    intro n _
    by_cases hn : n = 0
    · subst n
      rw [homogeneousComponent_zero]
      exact persistentCore_constant _ _
    · exact hpos n (by omega) _ (homogeneousComponent_isHomogeneous n G)
        (firstRefinement_homogeneousComponent F G hF h n)
  · exact firstRefinement_of_core _ _

end SexticC3.Differential
