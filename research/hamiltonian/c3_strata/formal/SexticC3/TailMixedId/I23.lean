import Mathlib.Tactic.Ring
namespace SexticC3.TailElimination
variable {K : Type*} [Field K] [CharZero K]
set_option linter.all false
namespace MixedData

set_option maxRecDepth 8192 in
set_option maxHeartbeats 0 in
theorem identity_23 (z a b c d : K) : ((1) * (c + (3/20)*a^(2:ℕ)) : K) = (c + (3/20)*a^(2:ℕ) : K) := by ring

end MixedData
end SexticC3.TailElimination
