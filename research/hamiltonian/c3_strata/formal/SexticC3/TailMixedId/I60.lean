import Mathlib.Tactic.Ring
namespace SexticC3.TailElimination
variable {K : Type*} [Field K] [CharZero K]
set_option linter.all false
namespace MixedData

set_option maxRecDepth 8192 in
set_option maxHeartbeats 0 in
theorem identity_60 (z a b c d : K) : ((z^(8:ℕ)) * (c + (3/20)*a^(2:ℕ)) : K) = (z^(8:ℕ)*c + (3/20)*z^(8:ℕ)*a^(2:ℕ) : K) := by ring

end MixedData
end SexticC3.TailElimination
