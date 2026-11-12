import SexticC3.TailRawRows
namespace SexticC3.StaticTail
variable {K : Type*} [Field K] [CharZero K]

set_option maxRecDepth 8192 in
set_option maxHeartbeats 6000000 in
theorem cleared_e0 (n : ℕ) (hn : 17 ≤ n) (a b c d : K) (g : ℕ → K)
    (h : ∀ k u v, (k = 3 ∨ k = 5) → rowValue a b c d n ⟨false, k, u, v⟩ g = 0) :
    (let z : K := n; g 0 - (1 * g 0 + 0 * g 1) = 0) := by
  dsimp only
  ring

set_option maxRecDepth 8192 in
set_option maxHeartbeats 6000000 in
theorem cleared_e1 (n : ℕ) (hn : 17 ≤ n) (a b c d : K) (g : ℕ → K)
    (h : ∀ k u v, (k = 3 ∨ k = 5) → rowValue a b c d n ⟨false, k, u, v⟩ g = 0) :
    (let z : K := n; g 1 - (0 * g 0 + 1 * g 1) = 0) := by
  dsimp only
  ring

set_option maxRecDepth 8192 in
set_option maxHeartbeats 6000000 in
theorem cleared_e2 (n : ℕ) (hn : 17 ≤ n) (a b c d : K) (g : ℕ → K)
    (h : ∀ k u v, (k = 3 ∨ k = 5) → rowValue a b c d n ⟨false, k, u, v⟩ g = 0) :
    (let z : K := n; (240 - 120*z) * g 2 - ((12*z*a - 18*z^2*a + 6*z^3*a) * (g 0) + (0) * (g 1)) = 0) := by
  let z : K := n
  have e0 := cleared_e0 n hn a b c d g h
  have hr := raw3_0 n hn a b c d g (h 3 0 (n - 2 + 2) (Or.inl rfl))
  linear_combination (1) * hr - (-12*z*a + 18*z^2*a - 6*z^3*a) * e0

set_option maxRecDepth 8192 in
set_option maxHeartbeats 6000000 in
theorem cleared_e3 (n : ℕ) (hn : 17 ≤ n) (a b c d : K) (g : ℕ → K)
    (h : ∀ k u v, (k = 3 ∨ k = 5) → rowValue a b c d n ⟨false, k, u, v⟩ g = 0) :
    (let z : K := n; (1440 - 360*z) * g 3 - ((48*z*b - 72*z^2*b + 24*z^3*b) * (g 0) + (-144*a + 228*z*a - 90*z^2*a + 6*z^3*a) * (g 1)) = 0) := by
  let z : K := n
  have e0 := cleared_e0 n hn a b c d g h
  have e1 := cleared_e1 n hn a b c d g h
  have hr := raw3_1 n hn a b c d g (h 3 1 (n - 3 + 2) (Or.inl rfl))
  linear_combination (1) * hr - (-48*z*b + 72*z^2*b - 24*z^3*b) * e0 - (144*a - 228*z*a + 90*z^2*a - 6*z^3*a) * e1

set_option maxRecDepth 8192 in
set_option maxHeartbeats 6000000 in
theorem cleared_e4 (n : ℕ) (hn : 17 ≤ n) (a b c d : K) (g : ℕ → K)
    (h : ∀ k u v, (k = 3 ∨ k = 5) → rowValue a b c d n ⟨false, k, u, v⟩ g = 0) :
    (let z : K := n; (1036800 - 691200*z + 86400*z^2) * g 4 - ((28800*z*c - 12096*z*a^2 - 57600*z^2*c + 27792*z^2*a^2 + 36000*z^3*c - 22464*z^3*a^2 - 7200*z^4*c + 7812*z^4*a^2 - 1080*z^5*a^2 + 36*z^6*a^2) * (g 0) + (-69120*b + 149760*z*b - 109440*z^2*b + 31680*z^3*b - 2880*z^4*b) * (g 1)) = 0) := by
  let z : K := n
  have e0 := cleared_e0 n hn a b c d g h
  have e1 := cleared_e1 n hn a b c d g h
  have e2 := cleared_e2 n hn a b c d g h
  have hr := raw3_2 n hn a b c d g (h 3 2 (n - 4 + 2) (Or.inl rfl))
  linear_combination (240 - 120*z) * hr - (-28800*z*c + 57600*z^2*c - 36000*z^3*c + 7200*z^4*c) * e0 - (69120*b - 149760*z*b + 109440*z^2*b - 31680*z^3*b + 2880*z^4*b) * e1 - (1008*a - 804*z*a + 162*z^2*a - 6*z^3*a) * e2

set_option maxRecDepth 8192 in
set_option maxHeartbeats 6000000 in
theorem cleared_e5 (n : ℕ) (hn : 17 ≤ n) (a b c d : K) (g : ℕ → K)
    (h : ∀ k u v, (k = 3 ∨ k = 5) → rowValue a b c d n ⟨false, k, u, v⟩ g = 0) :
    (let z : K := n; (3317760000 - 2903040000*z + 725760000*z^2 - 51840000*z^3) * g 5 - ((82944000*z*d - 64696320*z*a*b - 186624000*z^2*d + 166855680*z^2*a*b + 145152000*z^3*d - 162017280*z^3*a*b - 46656000*z^4*d + 75720960*z^4*a*b + 5184000*z^5*d - 17694720*z^5*a*b + 1900800*z^6*a*b - 69120*z^7*a*b) * (g 0) + (-165888000*c + 114462720*a^2 + 414720000*z*c - 298598400*z*a^2 - 383616000*z^2*c + 295522560*z^2*a^2 + 165888000*z^3*c - 142784640*z^3*a^2 - 33696000*z^4*c + 35570880*z^4*a^2 + 2592000*z^5*c - 4410720*z^5*a^2 + 241920*z^6*a^2 - 4320*z^7*a^2) * (g 1)) = 0) := by
  let z : K := n
  have e0 := cleared_e0 n hn a b c d g h
  have e1 := cleared_e1 n hn a b c d g h
  have e2 := cleared_e2 n hn a b c d g h
  have e3 := cleared_e3 n hn a b c d g h
  have hr := raw3_3 n hn a b c d g (h 3 3 (n - 5 + 2) (Or.inl rfl))
  linear_combination (345600 - 259200*z + 43200*z^2) * hr - (-82944000*z*d + 186624000*z^2*d - 145152000*z^3*d + 46656000*z^4*d - 5184000*z^5*d) * e0 - (165888000*c - 414720000*z*c + 383616000*z^2*c - 165888000*z^3*c + 33696000*z^4*c - 2592000*z^5*c) * e1 - (2211840*b - 2557440*z*b + 1019520*z^2*b - 164160*z^3*b + 8640*z^4*b) * e2 - (794880*a - 815040*z*a + 264960*z^2*a - 29520*z^3*a + 720*z^4*a) * e3

end SexticC3.StaticTail
