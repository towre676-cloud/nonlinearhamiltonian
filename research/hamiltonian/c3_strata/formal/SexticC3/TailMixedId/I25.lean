import Mathlib.Tactic.Ring
namespace SexticC3.TailElimination
variable {K : Type*} [Field K] [CharZero K]
set_option linter.all false
namespace MixedData

set_option maxRecDepth 8192 in
set_option maxHeartbeats 0 in
theorem identity_25 (z a b c d : K) : (1848268800 - 2476224000*z + 1437321600*z^(2:ℕ) - 473885600*z^(3:ℕ) + 97700400*z^(4:ℕ) - 13051200*z^(5:ℕ) + 1129200*z^(6:ℕ) - 61050*z^(7:ℕ) + 1875*z^(8:ℕ) - 25*z^(9:ℕ) : K) = ((1) * (1848268800 - 2476224000*z + 1437321600*z^(2:ℕ) - 473885600*z^(3:ℕ) + 97700400*z^(4:ℕ) + 63551488*z^(4:ℕ)*c - 13051200*z^(5:ℕ) - 65034752*z^(5:ℕ)*c + 1129200*z^(6:ℕ) + 28343264*z^(6:ℕ)*c - 61050*z^(7:ℕ) - 6866480*z^(7:ℕ)*c + 1875*z^(8:ℕ) + 1010536*z^(8:ℕ)*c - 25*z^(9:ℕ) - 92384*z^(9:ℕ)*c + 5112*z^(10:ℕ)*c - 156*z^(11:ℕ)*c + 2*z^(12:ℕ)*c) + (-63551488*z^(4:ℕ) + 65034752*z^(5:ℕ) - 28343264*z^(6:ℕ) + 6866480*z^(7:ℕ) - 1010536*z^(8:ℕ) + 92384*z^(9:ℕ) - 5112*z^(10:ℕ) + 156*z^(11:ℕ) - 2*z^(12:ℕ)) * (c) : K) := by ring

end MixedData
end SexticC3.TailElimination
