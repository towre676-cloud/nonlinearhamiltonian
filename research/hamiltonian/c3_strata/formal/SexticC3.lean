import SexticC3.Discriminant
import SexticC3.Degree1
import SexticC3.Degree2
import SexticC3.Degree3
import SexticC3.Degree4
import SexticC3.Degree5
import SexticC3.Degree6
import SexticC3.Degree7
import SexticC3.Degree8
import SexticC3.Degree9
import SexticC3.Degree10
import SexticC3.Degree11
import SexticC3.Degree12
import SexticC3.Degree13
import SexticC3.Degree14
import SexticC3.Degree15
import SexticC3.Degree16
import SexticC3.Core6
import SexticC3.Exceptional411
import SexticC3.StaticTail

namespace SexticC3

variable {K : Type*} [Field K] [CharZero K] (a b c d : K)

/-- Uniform finite-window bound for the normalized squarefree coefficient model. -/
theorem finite_kernel_bound (n : Nat) (hn₁ : 1 ≤ n) (hn₂ : n ≤ 16)
    (g : Nat → K) (h : IsKernel a b c d n g) (hd : delta a b c d ≠ 0) :
    ∀ j ≤ n, g j = if n = 6 then hCoeff a b c d j * g 1 else 0 := by
  have hn : n = 1 ∨ n = 2 ∨ n = 3 ∨ n = 4 ∨ n = 5 ∨ n = 6 ∨ n = 7 ∨ n = 8 ∨ n = 9 ∨ n = 10 ∨ n = 11 ∨ n = 12 ∨ n = 13 ∨ n = 14 ∨ n = 15 ∨ n = 16 := by omega
  rcases hn with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
  · intro j hj
    have hj' : j = 0 ∨ j = 1 := by omega
    obtain ⟨h0, h1⟩ := Degree1.kernel_bound a b c d g h hd
    rcases hj' with rfl | rfl <;> simp [h0, h1]
  · simpa using Degree2.kernel_bound a b c d g h hd
  · simpa using Degree3.kernel_bound a b c d g h hd
  · simpa using Degree4.kernel_bound a b c d g h hd
  · simpa using Degree5.kernel_bound a b c d g h hd
  · simpa [Degree6.lift1_eq_hCoeff] using Degree6.kernel_bound a b c d g h hd
  · simpa using Degree7.kernel_bound a b c d g h hd
  · simpa using Degree8.kernel_bound a b c d g h hd
  · simpa using Degree9.kernel_bound a b c d g h hd
  · simpa using Degree10.kernel_bound a b c d g h hd
  · simpa using Degree11.kernel_bound a b c d g h hd
  · simpa using Degree12.kernel_bound a b c d g h hd
  · simpa using Degree13.kernel_bound a b c d g h hd
  · simpa using Degree14.kernel_bound a b c d g h hd
  · simpa using Degree15.kernel_bound a b c d g h hd
  · simpa using Degree16.kernel_bound a b c d g h hd

end SexticC3
