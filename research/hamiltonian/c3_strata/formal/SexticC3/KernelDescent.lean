import SexticC3.TailTransport
import Mathlib.FieldTheory.IsAlgClosed.AlgebraicClosure

namespace SexticC3.StaticTail

variable {K L : Type*} [Field K] [Field L]

theorem isKernel_map (f : K →+* L) (a b c d : K) (n : ℕ) (g : ℕ → K)
    (h : IsKernel a b c d n g) :
    IsKernel (f a) (f b) (f c) (f d) n (fun j => f (g j)) := by
  intro r hr
  rw [← map_rowValue, h r hr, map_zero]

theorem kernel_bound_descent (f : K →+* L) (a b c d : K) (n : ℕ) (g : ℕ → K)
    (h : IsKernel a b c d n g) (hd : delta a b c d ≠ 0)
    (bound : IsKernel (f a) (f b) (f c) (f d) n (fun j => f (g j)) →
      delta (f a) (f b) (f c) (f d) ≠ 0 →
      ∀ j ≤ n, f (g j) = if n = 6 then hCoeff (f a) (f b) (f c) (f d) j * f (g 1) else 0) :
    ∀ j ≤ n, g j = if n = 6 then hCoeff a b c d j * g 1 else 0 := by
  have hdelta : delta (f a) (f b) (f c) (f d) ≠ 0 := by
    rw [← map_delta]
    exact (map_ne_zero f).mpr hd
  intro j hj
  apply f.injective
  have he := bound (isKernel_map f a b c d n g h) hdelta j hj
  by_cases hn : n = 6
  · simpa only [hn, if_true, map_mul, map_hCoeff] using he
  · simpa only [hn, if_false, map_zero] using he

end SexticC3.StaticTail
