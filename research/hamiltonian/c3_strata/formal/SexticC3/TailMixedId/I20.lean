import Mathlib.Tactic.Ring
namespace SexticC3.TailElimination
variable {K : Type*} [Field K] [CharZero K]
set_option linter.all false
namespace MixedData

set_option maxRecDepth 8192 in
set_option maxHeartbeats 0 in
theorem identity_20 (z a b c d : K) : (c + (3/20)*a^(2:ℕ) : K) = (((3/20)*a) * (a) + (1) * (c) : K) := by ring

end MixedData
end SexticC3.TailElimination
