import SexticC3.TailRawRows
import SexticC3.TailScales
namespace SexticC3.StaticTail
variable {K : Type*} [Field K] [CharZero K]
set_option maxHeartbeats 3000000 in
theorem stored_row0 (n : ℕ) (hn : 17 ≤ n) (a b c d : K) (g : ℕ → K)
    (h : ∀ k u v, (k = 3 ∨ k = 5) → rowValue a b c d n ⟨false, k, u, v⟩ g = 0) :
    (let z : K := n; ((-160*z*c + 24*z*a^2 + 20*z^2*c - 5*z^2*a^2) * (g 0) + (240*b - 40*z*b) * (g 1)) = 0) := by
  let z : K := n
  have e0 : g 0 - (1 * g 0 + 0 * g 1) = 0 := by ring
  have e1 : g 1 - (0 * g 0 + 1 * g 1) = 0 := by ring
  have e2 : (240 - 120*z) * g 2 - ((12*z*a - 18*z^2*a + 6*z^3*a) * (g 0) + (0) * (g 1)) = 0 := by
    have hr := raw3_0 n hn a b c d g (h 3 0 (n - 2 + 2) (Or.inl rfl))
    linear_combination (1) * hr - (-12*z*a + 18*z^2*a - 6*z^3*a) * e0
  have e3 : (1440 - 360*z) * g 3 - ((48*z*b - 72*z^2*b + 24*z^3*b) * (g 0) + (-144*a + 228*z*a - 90*z^2*a + 6*z^3*a) * (g 1)) = 0 := by
    have hr := raw3_1 n hn a b c d g (h 3 1 (n - 3 + 2) (Or.inl rfl))
    linear_combination (1) * hr - (-48*z*b + 72*z^2*b - 24*z^3*b) * e0 - (144*a - 228*z*a + 90*z^2*a - 6*z^3*a) * e1
  have e4 : (1036800 - 691200*z + 86400*z^2) * g 4 - ((28800*z*c - 12096*z*a^2 - 57600*z^2*c + 27792*z^2*a^2 + 36000*z^3*c - 22464*z^3*a^2 - 7200*z^4*c + 7812*z^4*a^2 - 1080*z^5*a^2 + 36*z^6*a^2) * (g 0) + (-69120*b + 149760*z*b - 109440*z^2*b + 31680*z^3*b - 2880*z^4*b) * (g 1)) = 0 := by
    have hr := raw3_2 n hn a b c d g (h 3 2 (n - 4 + 2) (Or.inl rfl))
    linear_combination (240 - 120*z) * hr - (-28800*z*c + 57600*z^2*c - 36000*z^3*c + 7200*z^4*c) * e0 - (69120*b - 149760*z*b + 109440*z^2*b - 31680*z^3*b + 2880*z^4*b) * e1 - (1008*a - 804*z*a + 162*z^2*a - 6*z^3*a) * e2
  have f0 : ((-160*z*c + 24*z*a^2 + 20*z^2*c - 5*z^2*a^2) * (g 0) + (240*b - 40*z*b) * (g 1)) = 0 := by
    apply (mul_eq_zero.mp ?_).resolve_left (TailScales.rowScale0 n hn)
    show (1990656000 - 7464960000*z + 11197440000*z^2 - 8584704000*z^3 + 3545856000*z^4 - 746496000*z^5 + 62208000*z^6) * ((-160*z*c + 24*z*a^2 + 20*z^2*c - 5*z^2*a^2) * (g 0) + (240*b - 40*z*b) * (g 1)) = 0
    have hr := raw5_0 n hn a b c d g (h 5 0 (n - 4 + 0) (Or.inr rfl))
    linear_combination (248832000 - 290304000*z + 103680000*z^2 - 10368000*z^3) * hr - (-716636160000*z*c + 2329067520000*z^2*c - 3085516800000*z^3*c + 2169815040000*z^4*c - 875888640000*z^5*c + 202798080000*z^6*c - 24883200000*z^7*c + 1244160000*z^8*c) * e0 - (1433272320000*b - 4658135040000*z*b + 6171033600000*z^2*b - 4339630080000*z^3*b + 1751777280000*z^4*b - 405596160000*z^5*b + 49766400000*z^6*b - 2488320000*z^7*b) * e1 - (17915904000*a - 31352832000*z*a + 21150720000*z^2*a - 6842880000*z^3*a + 1057536000*z^4*a - 62208000*z^5*a) * e2 - (13824000 - 10368000*z + 1728000*z^2) * e4
  exact f0
end SexticC3.StaticTail
