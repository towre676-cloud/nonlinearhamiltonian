import Mathlib.Tactic.Ring
namespace SexticC3.TailElimination
variable {K : Type*} [Field K] [CharZero K]
set_option linter.all false
namespace MixedData

set_option maxRecDepth 8192 in
set_option maxHeartbeats 0 in
theorem identity_24 (z a b c d : K) : ((-6082560000*z + 5483520000*z^(2:ℕ) - 1943040000*z^(3:ℕ) + 337920000*z^(4:ℕ) - 28800000*z^(5:ℕ) + 960000*z^(6:ℕ)) * (d + (1/50)*a*b) : K) = (-6082560000*z*d - 121651200*z*a*b + 5483520000*z^(2:ℕ)*d + 109670400*z^(2:ℕ)*a*b - 1943040000*z^(3:ℕ)*d - 38860800*z^(3:ℕ)*a*b + 337920000*z^(4:ℕ)*d + 6758400*z^(4:ℕ)*a*b - 28800000*z^(5:ℕ)*d - 576000*z^(5:ℕ)*a*b + 960000*z^(6:ℕ)*d + 19200*z^(6:ℕ)*a*b : K) := by ring

end MixedData
end SexticC3.TailElimination
