import Mathlib.Tactic.Ring
namespace SexticC3.TailElimination
variable {K : Type*} [Field K] [CharZero K]
set_option linter.all false
namespace MixedData

set_option maxRecDepth 8192 in
set_option maxHeartbeats 0 in
theorem identity_65 (z a b c d : K) : (-5955287040*z^(4:ℕ) + 6009423360*z^(5:ℕ) - 2553159680*z^(6:ℕ) + 598122880*z^(7:ℕ) - 85029760*z^(8:ℕ) + 7596640*z^(9:ℕ) - 423520*z^(10:ℕ) + 13720*z^(11:ℕ) - 200*z^(12:ℕ) : K) = ((z^(4:ℕ)) * (-3269099520 + 3444695040*z - 1521443360*z^(2:ℕ) + 369185440*z^(3:ℕ) - 54147880*z^(4:ℕ) + 179079168*z^(4:ℕ)*c + 4960420*z^(5:ℕ) - 170981888*z^(5:ℕ)*c - 280240*z^(6:ℕ) + 68781088*z^(6:ℕ)*c + 8995*z^(7:ℕ) - 15262496*z^(7:ℕ)*c - 125*z^(8:ℕ) + 2058792*z^(8:ℕ)*c - 175748*z^(9:ℕ)*c + 9552*z^(10:ℕ)*c - 315*z^(11:ℕ)*c + 5*z^(12:ℕ)*c) + (-179079168*z^(4:ℕ) + 170981888*z^(5:ℕ) - 68781088*z^(6:ℕ) + 15262496*z^(7:ℕ) - 2058792*z^(8:ℕ) + 175748*z^(9:ℕ) - 9552*z^(10:ℕ) + 315*z^(11:ℕ) - 5*z^(12:ℕ)) * (15 + z^(4:ℕ)*c) : K) := by ring

end MixedData
end SexticC3.TailElimination
