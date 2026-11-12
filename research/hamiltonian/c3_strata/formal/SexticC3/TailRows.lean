import SexticC3.StaticTail

namespace SexticC3.StaticTail

variable {K : Type*} [Field K]

private theorem sum_linear (x y : K) (f g c : Nat → K) (is : List Nat) :
    (is.map fun i => c i * (x * f i + y * g i)).sum =
      x * (is.map fun i => c i * f i).sum + y * (is.map fun i => c i * g i).sum := by
  induction is with
  | nil => simp
  | cons i is ih =>
    simp only [List.map_cons, List.sum_cons, ih]
    ring

/-- Reconstruction is linear in the two coefficients at the simple-root edge. -/
theorem reconstruct_linear (a b c d : K) (n m : Nat) (x y : K) (i : Nat) :
    reconstruct a b c d n x y m i =
      x * reconstruct a b c d n 1 0 m i + y * reconstruct a b c d n 0 1 m i := by
  induction m generalizing i with
  | zero =>
    by_cases h₀ : i = 0 <;> by_cases h₁ : i = 1 <;> simp [reconstruct, h₀, h₁]
  | succ m ih =>
    by_cases he : i = m + 2
    · simp only [reconstruct, if_pos he]
      have hm :
          (List.range (m + 2)).map (fun j =>
            staticColumn a b c d n 3 m (n - (m + 2) + 2) j *
              reconstruct a b c d n x y m j) =
          (List.range (m + 2)).map (fun j =>
            staticColumn a b c d n 3 m (n - (m + 2) + 2) j *
              (x * reconstruct a b c d n 1 0 m j + y * reconstruct a b c d n 0 1 m j)) :=
        List.map_congr_left fun j _ => by rw [ih j]
      rw [hm, sum_linear]
      ring
    · simpa only [reconstruct, if_neg he] using ih i

/-- The two entries of one of the six reconstructed fifth-order rows.
Each is computed by a single reconstruction on a coordinate vector. -/
noncomputable def fifthRowPair (a b c d : K) (n t : Nat) : K × K :=
  (rowValue a b c d n ⟨false, 5, t, n - (t + 4)⟩ (reconstruct a b c d n 1 0 8),
   rowValue a b c d n ⟨false, 5, t, n - (t + 4)⟩ (reconstruct a b c d n 0 1 8))

theorem reconstructed_fifth_row_linear (a b c d : K) (n t : Nat)
    (hn : 17 ≤ n) (ht : t < 6) (x y : K) :
    rowValue a b c d n ⟨false, 5, t, n - (t + 4)⟩ (reconstruct a b c d n x y 8) =
      x * (fifthRowPair a b c d n t).1 + y * (fifthRowPair a b c d n t).2 := by
  have hd : t + (n - (t + 4)) + 2 * 5 = 6 + n := by omega
  unfold fifthRowPair
  simp only [rowValue_static _ _ _ _ _ _ _ _ _ hd, staticTransvectant]
  have hm :
      (List.range (n + 1)).map (fun j =>
        staticColumn a b c d n 5 t (n - (t + 4)) j * reconstruct a b c d n x y 8 j) =
      (List.range (n + 1)).map (fun j =>
        staticColumn a b c d n 5 t (n - (t + 4)) j *
          (x * reconstruct a b c d n 1 0 8 j + y * reconstruct a b c d n 0 1 8 j)) :=
    List.map_congr_left fun j _ => by rw [reconstruct_linear]
  rw [hm, sum_linear]

variable [CharZero K]

/-- A nonzero static partner yields a nonzero vector in the common kernel
of the six explicitly defined linear rows. -/
theorem exists_nonzero_edge_kernel (a b c d : K) (n : Nat) (hn : 17 ≤ n)
    (g : Nat → K) (h : ∀ k u v, (k = 3 ∨ k = 5) →
      rowValue a b c d n ⟨false, k, u, v⟩ g = 0)
    (hg : ∃ j ≤ n, g j ≠ 0) :
    ∃ x y : K, (x ≠ 0 ∨ y ≠ 0) ∧ ∀ t < 6,
      x * (fifthRowPair a b c d n t).1 + y * (fifthRowPair a b c d n t).2 = 0 := by
  refine ⟨g 0, g 1, ?_, ?_⟩
  · by_contra he
    push_neg at he
    obtain ⟨j, hj, hjnz⟩ := hg
    exact hjnz (kernel_zero_of_edge_zero a b c d n hn g h he.1 he.2 j hj)
  · intro t ht
    rw [← reconstructed_fifth_row_linear a b c d n t hn ht]
    exact reconstructed_fifth_rows a b c d n g hn h t ht

end SexticC3.StaticTail
