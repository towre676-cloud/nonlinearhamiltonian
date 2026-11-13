import Mathlib.Tactic.Ring
namespace SexticC3.TailElimination
variable {K : Type*} [Field K] [CharZero K]
set_option linter.all false
namespace MixedData

set_option maxRecDepth 8192 in
set_option maxHeartbeats 0 in
theorem identity_59 (z a b c d : K) : ((57600*z^(16:ℕ) - 19200*z^(17:ℕ) + 1600*z^(18:ℕ)) * (b^(2:ℕ) + (2/5)*a^(3:ℕ)) : K) = (57600*z^(16:ℕ)*b^(2:ℕ) + 23040*z^(16:ℕ)*a^(3:ℕ) - 19200*z^(17:ℕ)*b^(2:ℕ) - 7680*z^(17:ℕ)*a^(3:ℕ) + 1600*z^(18:ℕ)*b^(2:ℕ) + 640*z^(18:ℕ)*a^(3:ℕ) : K) := by ring

end MixedData
end SexticC3.TailElimination
