import Mathlib.Tactic.Ring
namespace SexticC3.TailElimination
variable {K : Type*} [Field K] [CharZero K]
set_option linter.all false
namespace MixedData

set_option maxRecDepth 8192 in
set_option maxHeartbeats 0 in
theorem identity_73 (z a b c d : K) : (-2773647360*z^(4:ℕ) + 3345960960*z^(5:ℕ) - 1744035840*z^(6:ℕ) + 512440320*z^(7:ℕ) - 92705280*z^(8:ℕ) + 10556160*z^(9:ℕ) - 737280*z^(10:ℕ) + 28800*z^(11:ℕ) - 480*z^(12:ℕ) : K) = ((-352*z^(4:ℕ) + 156*z^(5:ℕ) - 22*z^(6:ℕ) + z^(7:ℕ)) * (-9953280 + 10004480*z - 4061840*z^(2:ℕ) + 851000*z^(3:ℕ) - 96560*z^(4:ℕ) + 484352*z^(4:ℕ)*c + 5570*z^(5:ℕ) - 444160*z^(5:ℕ)*c - 125*z^(6:ℕ) + 167184*z^(6:ℕ)*c - 33080*z^(7:ℕ)*c + 3632*z^(8:ℕ)*c - 210*z^(9:ℕ)*c + 5*z^(10:ℕ)*c) + (-484352*z^(4:ℕ) + 444160*z^(5:ℕ) - 167184*z^(6:ℕ) + 33080*z^(7:ℕ) - 3632*z^(8:ℕ) + 210*z^(9:ℕ) - 5*z^(10:ℕ)) * (12960 - 5500*z + 710*z^(2:ℕ) - 25*z^(3:ℕ) - 352*z^(4:ℕ)*c + 156*z^(5:ℕ)*c - 22*z^(6:ℕ)*c + z^(7:ℕ)*c) : K) := by ring

end MixedData
end SexticC3.TailElimination
