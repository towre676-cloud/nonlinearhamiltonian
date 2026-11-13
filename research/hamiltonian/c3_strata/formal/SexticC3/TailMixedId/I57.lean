import Mathlib.Tactic.Ring
namespace SexticC3.TailElimination
variable {K : Type*} [Field K] [CharZero K]
set_option linter.all false
namespace MixedData

set_option maxRecDepth 8192 in
set_option maxHeartbeats 0 in
theorem identity_57 (z a b c d : K) : (z^(8:ℕ)*c + (3/20)*z^(8:ℕ)*a^(2:ℕ) : K) = ((-(3/2)*z^(4:ℕ) + (3/20)*z^(6:ℕ)*a) * (10 + z^(2:ℕ)*a) + (z^(4:ℕ)) * (15 + z^(4:ℕ)*c) : K) := by ring

end MixedData
end SexticC3.TailElimination
