import Mathlib.Tactic.Ring
namespace SexticC3.TailElimination
variable {K : Type*} [Field K] [CharZero K]
set_option linter.all false
namespace MixedData

set_option maxRecDepth 8192 in
set_option maxHeartbeats 0 in
theorem identity_70 (z a b c d : K) : (-17218560*z^(4:ℕ) + 16666880*z^(5:ℕ) - 6569600*z^(6:ℕ) + 1347200*z^(7:ℕ) - 151040*z^(8:ℕ) + 8720*z^(9:ℕ) - 200*z^(10:ℕ) : K) = ((z^(4:ℕ)) * (-9953280 + 10004480*z - 4061840*z^(2:ℕ) + 851000*z^(3:ℕ) - 96560*z^(4:ℕ) + 484352*z^(4:ℕ)*c + 5570*z^(5:ℕ) - 444160*z^(5:ℕ)*c - 125*z^(6:ℕ) + 167184*z^(6:ℕ)*c - 33080*z^(7:ℕ)*c + 3632*z^(8:ℕ)*c - 210*z^(9:ℕ)*c + 5*z^(10:ℕ)*c) + (-484352*z^(4:ℕ) + 444160*z^(5:ℕ) - 167184*z^(6:ℕ) + 33080*z^(7:ℕ) - 3632*z^(8:ℕ) + 210*z^(9:ℕ) - 5*z^(10:ℕ)) * (15 + z^(4:ℕ)*c) : K) := by ring

end MixedData
end SexticC3.TailElimination
