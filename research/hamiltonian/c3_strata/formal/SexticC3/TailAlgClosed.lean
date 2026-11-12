import SexticC3.TailCharts
import Mathlib.FieldTheory.IsAlgClosed.Basic
namespace SexticC3.StaticTail
variable {K : Type*} [Field K] [CharZero K]

/-- Static-tail exclusion over an algebraically closed field of characteristic zero. -/
theorem normalized_static_tail_algClosed [IsAlgClosed K]
    (n : ℕ) (hn : 17 ≤ n) (a b c d : K) (g : ℕ → K)
    (h : ∀ k u v, (k = 3 ∨ k = 5) → rowValue a b c d n ⟨false, k, u, v⟩ g = 0)
    (hd : delta a b c d ≠ 0) : ∀ j ≤ n, g j = 0 :=
  normalized_static_tail n hn a b c d g
    (fun _ hm q => IsAlgClosed.exists_pow_nat_eq q hm) h hd

end SexticC3.StaticTail
