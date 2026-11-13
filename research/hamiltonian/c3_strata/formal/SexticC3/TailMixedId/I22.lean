import Mathlib.Tactic.Ring
namespace SexticC3.TailElimination
variable {K : Type*} [Field K] [CharZero K]
set_option linter.all false
namespace MixedData

set_option maxRecDepth 8192 in
set_option maxHeartbeats 0 in
theorem identity_22 (z a b c d : K) : ((57600 - 19200*z + 1600*z^(2:ℕ)) * (b^(2:ℕ) + (2/5)*a^(3:ℕ)) : K) = (57600*b^(2:ℕ) + 23040*a^(3:ℕ) - 19200*z*b^(2:ℕ) - 7680*z*a^(3:ℕ) + 1600*z^(2:ℕ)*b^(2:ℕ) + 640*z^(2:ℕ)*a^(3:ℕ) : K) := by ring

end MixedData
end SexticC3.TailElimination
