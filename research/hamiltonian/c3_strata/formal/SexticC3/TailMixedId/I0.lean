import Mathlib.Tactic.Ring
namespace SexticC3.TailElimination
variable {K : Type*} [Field K] [CharZero K]
set_option linter.all false
namespace MixedData

set_option linter.unusedVariables false
set_option maxRecDepth 8192 in
set_option maxHeartbeats 0 in
theorem identity_0 (z a b c d : K) : (32256000*c - 8432640*a^(2:ℕ) - 25344000*z*d - 29184000*z*c + 7557120*z*a^(2:ℕ) + 18624000*z^(2:ℕ)*d + 10208000*z^(2:ℕ)*c + 4085760*z^(2:ℕ)*a*c - 2585280*z^(2:ℕ)*a^(2:ℕ) - 612864*z^(2:ℕ)*a^(3:ℕ) - 4992000*z^(3:ℕ)*d - 1712000*z^(3:ℕ)*c - 3559680*z^(3:ℕ)*a*c + 424160*z^(3:ℕ)*a^(2:ℕ) + 585024*z^(3:ℕ)*a^(3:ℕ) + 576000*z^(4:ℕ)*d + 136000*z^(4:ℕ)*c + 1178560*z^(4:ℕ)*a*c - 33360*z^(4:ℕ)*a^(2:ℕ) - 214896*z^(4:ℕ)*a^(3:ℕ) - 24000*z^(5:ℕ)*d - 4000*z^(5:ℕ)*c - 186080*z^(5:ℕ)*a*c + 1000*z^(5:ℕ)*a^(2:ℕ) + 37880*z^(5:ℕ)*a^(3:ℕ) + 14000*z^(6:ℕ)*a*c - 3180*z^(6:ℕ)*a^(3:ℕ) - 400*z^(7:ℕ)*a*c + 100*z^(7:ℕ)*a^(3:ℕ) : K) = ((240 - 40*z) * (134400*c - 35136*a^(2:ℕ) - 105600*z*d - 99200*z*c + 25536*z*a*b + 25632*z*a^(2:ℕ) + 60000*z^(2:ℕ)*d + 26000*z^(2:ℕ)*c - 19056*z^(2:ℕ)*a*b - 6500*z^(2:ℕ)*a^(2:ℕ) - 10800*z^(3:ℕ)*d - 2800*z^(3:ℕ)*c + 4984*z^(3:ℕ)*a*b + 684*z^(3:ℕ)*a^(2:ℕ) + 600*z^(4:ℕ)*d + 100*z^(4:ℕ)*c - 540*z^(4:ℕ)*a*b - 25*z^(4:ℕ)*a^(2:ℕ) + 20*z^(5:ℕ)*a*b) + (-25536*z*a + 19056*z^(2:ℕ)*a - 4984*z^(3:ℕ)*a + 540*z^(4:ℕ)*a - 20*z^(5:ℕ)*a) * (240*b - 160*z*c - 40*z*b + 24*z*a^(2:ℕ) + 20*z^(2:ℕ)*c - 5*z^(2:ℕ)*a^(2:ℕ)) : K) := by ring

end MixedData
end SexticC3.TailElimination
