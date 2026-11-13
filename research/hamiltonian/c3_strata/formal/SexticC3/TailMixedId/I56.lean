import Mathlib.Tactic.Ring
namespace SexticC3.TailElimination
variable {K : Type*} [Field K] [CharZero K]
set_option linter.all false
namespace MixedData

set_option maxRecDepth 8192 in
set_option maxHeartbeats 0 in
theorem identity_56 (z a b c d : K) : (57600*z^(16:ℕ)*b^(2:ℕ) + 23040*z^(16:ℕ)*a^(3:ℕ) - 19200*z^(17:ℕ)*b^(2:ℕ) - 7680*z^(17:ℕ)*a^(3:ℕ) + 1600*z^(18:ℕ)*b^(2:ℕ) + 640*z^(18:ℕ)*a^(3:ℕ) : K) = ((240*z^(16:ℕ)*b + 160*z^(17:ℕ)*c - 40*z^(17:ℕ)*b - 24*z^(17:ℕ)*a^(2:ℕ) - 20*z^(18:ℕ)*c + 5*z^(18:ℕ)*a^(2:ℕ)) * (240*b - 160*z*c - 40*z*b + 24*z*a^(2:ℕ) + 20*z^(2:ℕ)*c - 5*z^(2:ℕ)*a^(2:ℕ)) + (1728000*z^(10:ℕ) - 528000*z^(11:ℕ) + 39000*z^(12:ℕ) - 172800*z^(12:ℕ)*a + 52800*z^(13:ℕ)*a + 76800*z^(14:ℕ)*c - 3900*z^(14:ℕ)*a + 17280*z^(14:ℕ)*a^(2:ℕ) - 25600*z^(15:ℕ)*c - 5280*z^(15:ℕ)*a^(2:ℕ) + 2000*z^(16:ℕ)*c - 7680*z^(16:ℕ)*a*c + 390*z^(16:ℕ)*a^(2:ℕ) + 576*z^(16:ℕ)*a^(3:ℕ) + 2560*z^(17:ℕ)*a*c - 240*z^(17:ℕ)*a^(3:ℕ) - 200*z^(18:ℕ)*a*c + 25*z^(18:ℕ)*a^(3:ℕ)) * (10 + z^(2:ℕ)*a) + (-1152000*z^(10:ℕ) + 352000*z^(11:ℕ) - 26000*z^(12:ℕ) + 25600*z^(14:ℕ)*c - 6400*z^(15:ℕ)*c + 400*z^(16:ℕ)*c) * (15 + z^(4:ℕ)*c) : K) := by ring

end MixedData
end SexticC3.TailElimination
