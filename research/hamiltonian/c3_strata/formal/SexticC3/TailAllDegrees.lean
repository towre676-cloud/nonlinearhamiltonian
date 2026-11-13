import SexticC3
import SexticC3.TailAlgClosed

namespace SexticC3

variable {K : Type*} [Field K] [CharZero K] [IsAlgClosed K]

/-- Every positive degree in the normalized squarefree coefficient model. -/
theorem squarefree_kernel_bound (a b c d : K) (n : ℕ) (hn : 1 ≤ n)
    (g : ℕ → K) (h : IsKernel a b c d n g) (hd : delta a b c d ≠ 0) :
    ∀ j ≤ n, g j = if n = 6 then hCoeff a b c d j * g 1 else 0 := by
  by_cases hsmall : n ≤ 16
  · exact finite_kernel_bound a b c d n hn hsmall g h hd
  · intro j hj
    rw [if_neg (by omega)]
    exact StaticTail.normalized_static_tail_algClosed n (by omega) a b c d g
      (fun k u v hk => h ⟨false, k, u, v⟩ hk) hd j hj

end SexticC3
