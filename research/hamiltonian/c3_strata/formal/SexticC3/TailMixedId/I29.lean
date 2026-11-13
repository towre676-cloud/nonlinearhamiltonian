import Mathlib.Tactic.Ring
namespace SexticC3.TailElimination
variable {K : Type*} [Field K] [CharZero K]
set_option linter.all false
namespace MixedData

set_option maxRecDepth 8192 in
set_option maxHeartbeats 0 in
theorem identity_29 (z a b c d : K) : (14515200 - 17971200*z + 9374400*z^(2:ℕ) - 2666400*z^(3:ℕ) + 445600*z^(4:ℕ) - 43600*z^(5:ℕ) + 2300*z^(6:ℕ) - 50*z^(7:ℕ) : K) = ((1) * (14515200 - 17971200*z + 9374400*z^(2:ℕ) - 2666400*z^(3:ℕ) + 445600*z^(4:ℕ) + 484352*z^(4:ℕ)*c - 43600*z^(5:ℕ) - 444160*z^(5:ℕ)*c + 2300*z^(6:ℕ) + 167184*z^(6:ℕ)*c - 50*z^(7:ℕ) - 33080*z^(7:ℕ)*c + 3632*z^(8:ℕ)*c - 210*z^(9:ℕ)*c + 5*z^(10:ℕ)*c) + (-484352*z^(4:ℕ) + 444160*z^(5:ℕ) - 167184*z^(6:ℕ) + 33080*z^(7:ℕ) - 3632*z^(8:ℕ) + 210*z^(9:ℕ) - 5*z^(10:ℕ)) * (c) : K) := by ring

end MixedData
end SexticC3.TailElimination
