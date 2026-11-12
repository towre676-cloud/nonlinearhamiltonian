import Mathlib.Tactic.Ring
namespace SexticC3.TailElimination
variable {K : Type*} [Field K] [CharZero K]
set_option linter.all false
namespace MixedData

set_option maxRecDepth 8192 in
set_option maxHeartbeats 0 in
theorem identity_50 (z a b c d : K) : (18240*z^(4:ℕ) - 7840*z^(5:ℕ) + 1040*z^(6:ℕ) - 40*z^(7:ℕ) : K) = ((z^(4:ℕ)) * (12960 - 5500*z + 710*z^(2:ℕ) - 25*z^(3:ℕ) - 352*z^(4:ℕ)*c + 156*z^(5:ℕ)*c - 22*z^(6:ℕ)*c + z^(7:ℕ)*c) + (352*z^(4:ℕ) - 156*z^(5:ℕ) + 22*z^(6:ℕ) - z^(7:ℕ)) * (15 + z^(4:ℕ)*c) : K) := by ring

end MixedData
end SexticC3.TailElimination
