import Mathlib.Tactic.Ring
namespace SexticC3.TailElimination
variable {K : Type*} [Field K] [CharZero K]
set_option linter.all false
namespace MixedData

set_option maxRecDepth 8192 in
set_option maxHeartbeats 0 in
theorem identity_19 (z a b c d : K) : (57600*b^(2:ℕ) + 23040*a^(3:ℕ) - 19200*z*b^(2:ℕ) - 7680*z*a^(3:ℕ) + 1600*z^(2:ℕ)*b^(2:ℕ) + 640*z^(2:ℕ)*a^(3:ℕ) : K) = ((240*b + 160*z*c - 40*z*b - 24*z*a^(2:ℕ) - 20*z^(2:ℕ)*c + 5*z^(2:ℕ)*a^(2:ℕ)) * (240*b - 160*z*c - 40*z*b + 24*z*a^(2:ℕ) + 20*z^(2:ℕ)*c - 5*z^(2:ℕ)*a^(2:ℕ)) + (23040*a^(2:ℕ) - 7680*z*a^(2:ℕ) - 7680*z^(2:ℕ)*a*c + 640*z^(2:ℕ)*a^(2:ℕ) + 576*z^(2:ℕ)*a^(3:ℕ) + 2560*z^(3:ℕ)*a*c - 240*z^(3:ℕ)*a^(3:ℕ) - 200*z^(4:ℕ)*a*c + 25*z^(4:ℕ)*a^(3:ℕ)) * (a) + (25600*z^(2:ℕ)*c - 6400*z^(3:ℕ)*c + 400*z^(4:ℕ)*c) * (c) : K) := by ring

end MixedData
end SexticC3.TailElimination
