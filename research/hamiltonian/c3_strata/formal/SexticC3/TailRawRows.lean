import SexticC3.TailRows
namespace SexticC3.StaticTail
set_option linter.unusedTactic false
variable {K : Type*} [Field K]

theorem raw3_0 (n : ℕ) (hn : 17 ≤ n) (a b c d : K) (g : ℕ → K)
    (h : rowValue a b c d n ⟨false, 3, 0, n - 2 + 2⟩ g = 0) :
    (let z : K := n; (-12*z*a + 18*z^2*a - 6*z^3*a) * g 0 + (240 - 120*z) * g 2) = 0 := by
  have he := rowValue_top_split a b c d n 2 3 g (by omega) (by omega) (by omega)
  have hv : 5 + (n - 2) - 3 = n - 2 + 2 := by omega
  dsimp only at he
  norm_num at he
  rw [hv, h] at he
  norm_num [List.range_succ, staticColumn, monomialRow, weight, intCast_falling, fallingPoly, Nat.cast_sub (show 1 ≤ n by omega), Nat.cast_sub (show 2 ≤ n by omega)] at he
  simp (discharger := omega) only [if_pos, if_neg] at he
  norm_num [weight, List.range_succ, intCast_falling, fallingPoly, Nat.cast_sub (show 1 ≤ n by omega), Nat.cast_sub (show 2 ≤ n by omega)] at he
  dsimp only
  linear_combination he

theorem raw3_1 (n : ℕ) (hn : 17 ≤ n) (a b c d : K) (g : ℕ → K)
    (h : rowValue a b c d n ⟨false, 3, 1, n - 3 + 2⟩ g = 0) :
    (let z : K := n; (-48*z*b + 72*z^2*b - 24*z^3*b) * g 0 + (144*a - 228*z*a + 90*z^2*a - 6*z^3*a) * g 1 + (1440 - 360*z) * g 3) = 0 := by
  have he := rowValue_top_split a b c d n 3 3 g (by omega) (by omega) (by omega)
  have hv : 5 + (n - 3) - 3 = n - 3 + 2 := by omega
  dsimp only at he
  norm_num at he
  rw [hv, h] at he
  norm_num [List.range_succ, staticColumn, monomialRow, weight, intCast_falling, fallingPoly, Nat.cast_sub (show 1 ≤ n by omega), Nat.cast_sub (show 2 ≤ n by omega), Nat.cast_sub (show 3 ≤ n by omega)] at he
  simp (discharger := omega) only [if_pos, if_neg] at he
  norm_num [weight, List.range_succ, intCast_falling, fallingPoly, Nat.cast_sub (show 1 ≤ n by omega), Nat.cast_sub (show 2 ≤ n by omega), Nat.cast_sub (show 3 ≤ n by omega)] at he
  dsimp only
  linear_combination he

theorem raw3_2 (n : ℕ) (hn : 17 ≤ n) (a b c d : K) (g : ℕ → K)
    (h : rowValue a b c d n ⟨false, 3, 2, n - 4 + 2⟩ g = 0) :
    (let z : K := n; (-120*z*c + 180*z^2*c - 60*z^3*c) * g 0 + (288*b - 480*z*b + 216*z^2*b - 24*z^3*b) * g 1 + (1008*a - 804*z*a + 162*z^2*a - 6*z^3*a) * g 2 + (4320 - 720*z) * g 4) = 0 := by
  have he := rowValue_top_split a b c d n 4 3 g (by omega) (by omega) (by omega)
  have hv : 5 + (n - 4) - 3 = n - 4 + 2 := by omega
  dsimp only at he
  norm_num at he
  rw [hv, h] at he
  norm_num [List.range_succ, staticColumn, monomialRow, weight, intCast_falling, fallingPoly, Nat.cast_sub (show 1 ≤ n by omega), Nat.cast_sub (show 2 ≤ n by omega), Nat.cast_sub (show 3 ≤ n by omega), Nat.cast_sub (show 4 ≤ n by omega)] at he
  simp (discharger := omega) only [if_pos, if_neg] at he
  norm_num [weight, List.range_succ, intCast_falling, fallingPoly, Nat.cast_sub (show 1 ≤ n by omega), Nat.cast_sub (show 2 ≤ n by omega), Nat.cast_sub (show 3 ≤ n by omega), Nat.cast_sub (show 4 ≤ n by omega)] at he
  dsimp only
  linear_combination he

theorem raw3_3 (n : ℕ) (hn : 17 ≤ n) (a b c d : K) (g : ℕ → K)
    (h : rowValue a b c d n ⟨false, 3, 3, n - 5 + 2⟩ g = 0) :
    (let z : K := n; (-240*z*d + 360*z^2*d - 120*z^3*d) * g 0 + (480*c - 840*z*c + 420*z^2*c - 60*z^3*c) * g 1 + (1536*b - 1392*z*b + 360*z^2*b - 24*z^3*b) * g 2 + (3312*a - 1740*z*a + 234*z^2*a - 6*z^3*a) * g 3 + (9600 - 1200*z) * g 5) = 0 := by
  have he := rowValue_top_split a b c d n 5 3 g (by omega) (by omega) (by omega)
  have hv : 5 + (n - 5) - 3 = n - 5 + 2 := by omega
  dsimp only at he
  norm_num at he
  rw [hv, h] at he
  norm_num [List.range_succ, staticColumn, monomialRow, weight, intCast_falling, fallingPoly, Nat.cast_sub (show 1 ≤ n by omega), Nat.cast_sub (show 2 ≤ n by omega), Nat.cast_sub (show 3 ≤ n by omega), Nat.cast_sub (show 4 ≤ n by omega), Nat.cast_sub (show 5 ≤ n by omega)] at he
  simp (discharger := omega) only [if_pos, if_neg] at he
  norm_num [weight, List.range_succ, intCast_falling, fallingPoly, Nat.cast_sub (show 1 ≤ n by omega), Nat.cast_sub (show 2 ≤ n by omega), Nat.cast_sub (show 3 ≤ n by omega), Nat.cast_sub (show 4 ≤ n by omega), Nat.cast_sub (show 5 ≤ n by omega)] at he
  dsimp only
  linear_combination he

theorem raw3_4 (n : ℕ) (hn : 17 ≤ n) (a b c d : K) (g : ℕ → K)
    (h : rowValue a b c d n ⟨false, 3, 4, n - 6 + 2⟩ g = 0) :
    (let z : K := n; (720*d - 1320*z*d + 720*z^2*d - 120*z^3*d) * g 1 + (2160*c - 2160*z*c + 660*z^2*c - 60*z^3*c) * g 2 + (4464*b - 2784*z*b + 504*z^2*b - 24*z^3*b) * g 3 + (7776*a - 3036*z*a + 306*z^2*a - 6*z^3*a) * g 4 + (18000 - 1800*z) * g 6) = 0 := by
  have he := rowValue_top_split a b c d n 6 3 g (by omega) (by omega) (by omega)
  have hv : 5 + (n - 6) - 3 = n - 6 + 2 := by omega
  dsimp only at he
  norm_num at he
  rw [hv, h] at he
  norm_num [List.range_succ, staticColumn, monomialRow, weight, intCast_falling, fallingPoly, Nat.cast_sub (show 1 ≤ n by omega), Nat.cast_sub (show 2 ≤ n by omega), Nat.cast_sub (show 3 ≤ n by omega), Nat.cast_sub (show 4 ≤ n by omega), Nat.cast_sub (show 5 ≤ n by omega), Nat.cast_sub (show 6 ≤ n by omega)] at he
  simp (discharger := omega) only [if_pos, if_neg] at he
  norm_num [weight, List.range_succ, intCast_falling, fallingPoly, Nat.cast_sub (show 1 ≤ n by omega), Nat.cast_sub (show 2 ≤ n by omega), Nat.cast_sub (show 3 ≤ n by omega), Nat.cast_sub (show 4 ≤ n by omega), Nat.cast_sub (show 5 ≤ n by omega), Nat.cast_sub (show 6 ≤ n by omega)] at he
  dsimp only
  linear_combination he

theorem raw3_5 (n : ℕ) (hn : 17 ≤ n) (a b c d : K) (g : ℕ → K)
    (h : rowValue a b c d n ⟨false, 3, 5, n - 7 + 2⟩ g = 0) :
    (let z : K := n; (2880*d - 3120*z*d + 1080*z^2*d - 120*z^3*d) * g 2 + (5760*c - 4080*z*c + 900*z^2*c - 60*z^3*c) * g 3 + (9792*b - 4656*z*b + 648*z^2*b - 24*z^3*b) * g 4 + (15120*a - 4692*z*a + 378*z^2*a - 6*z^3*a) * g 5 + (30240 - 2520*z) * g 7) = 0 := by
  have he := rowValue_top_split a b c d n 7 3 g (by omega) (by omega) (by omega)
  have hv : 5 + (n - 7) - 3 = n - 7 + 2 := by omega
  dsimp only at he
  norm_num at he
  rw [hv, h] at he
  norm_num [List.range_succ, staticColumn, monomialRow, weight, intCast_falling, fallingPoly, Nat.cast_sub (show 1 ≤ n by omega), Nat.cast_sub (show 2 ≤ n by omega), Nat.cast_sub (show 3 ≤ n by omega), Nat.cast_sub (show 4 ≤ n by omega), Nat.cast_sub (show 5 ≤ n by omega), Nat.cast_sub (show 6 ≤ n by omega), Nat.cast_sub (show 7 ≤ n by omega)] at he
  simp (discharger := omega) only [if_pos, if_neg] at he
  norm_num [weight, List.range_succ, intCast_falling, fallingPoly, Nat.cast_sub (show 1 ≤ n by omega), Nat.cast_sub (show 2 ≤ n by omega), Nat.cast_sub (show 3 ≤ n by omega), Nat.cast_sub (show 4 ≤ n by omega), Nat.cast_sub (show 5 ≤ n by omega), Nat.cast_sub (show 6 ≤ n by omega), Nat.cast_sub (show 7 ≤ n by omega)] at he
  dsimp only
  linear_combination he

theorem raw3_6 (n : ℕ) (hn : 17 ≤ n) (a b c d : K) (g : ℕ → K)
    (h : rowValue a b c d n ⟨false, 3, 6, n - 8 + 2⟩ g = 0) :
    (let z : K := n; (7200*d - 5640*z*d + 1440*z^2*d - 120*z^3*d) * g 3 + (12000*c - 6600*z*c + 1140*z^2*c - 60*z^3*c) * g 4 + (18240*b - 7008*z*b + 792*z^2*b - 24*z^3*b) * g 5 + (26064*a - 6708*z*a + 450*z^2*a - 6*z^3*a) * g 6 + (47040 - 3360*z) * g 8) = 0 := by
  have he := rowValue_top_split a b c d n 8 3 g (by omega) (by omega) (by omega)
  have hv : 5 + (n - 8) - 3 = n - 8 + 2 := by omega
  dsimp only at he
  norm_num at he
  rw [hv, h] at he
  norm_num [List.range_succ, staticColumn, monomialRow, weight, intCast_falling, fallingPoly, Nat.cast_sub (show 1 ≤ n by omega), Nat.cast_sub (show 2 ≤ n by omega), Nat.cast_sub (show 3 ≤ n by omega), Nat.cast_sub (show 4 ≤ n by omega), Nat.cast_sub (show 5 ≤ n by omega), Nat.cast_sub (show 6 ≤ n by omega), Nat.cast_sub (show 7 ≤ n by omega), Nat.cast_sub (show 8 ≤ n by omega)] at he
  simp (discharger := omega) only [if_pos, if_neg] at he
  norm_num [weight, List.range_succ, intCast_falling, fallingPoly, Nat.cast_sub (show 1 ≤ n by omega), Nat.cast_sub (show 2 ≤ n by omega), Nat.cast_sub (show 3 ≤ n by omega), Nat.cast_sub (show 4 ≤ n by omega), Nat.cast_sub (show 5 ≤ n by omega), Nat.cast_sub (show 6 ≤ n by omega), Nat.cast_sub (show 7 ≤ n by omega), Nat.cast_sub (show 8 ≤ n by omega)] at he
  dsimp only
  linear_combination he

theorem raw3_7 (n : ℕ) (hn : 17 ≤ n) (a b c d : K) (g : ℕ → K)
    (h : rowValue a b c d n ⟨false, 3, 7, n - 9 + 2⟩ g = 0) :
    (let z : K := n; (14400*d - 8880*z*d + 1800*z^2*d - 120*z^3*d) * g 4 + (21600*c - 9720*z*c + 1380*z^2*c - 60*z^3*c) * g 5 + (30528*b - 9840*z*b + 936*z^2*b - 24*z^3*b) * g 6 + (41328*a - 9084*z*a + 522*z^2*a - 6*z^3*a) * g 7 + (69120 - 4320*z) * g 9) = 0 := by
  have he := rowValue_top_split a b c d n 9 3 g (by omega) (by omega) (by omega)
  have hv : 5 + (n - 9) - 3 = n - 9 + 2 := by omega
  dsimp only at he
  norm_num at he
  rw [hv, h] at he
  norm_num [List.range_succ, staticColumn, monomialRow, weight, intCast_falling, fallingPoly, Nat.cast_sub (show 1 ≤ n by omega), Nat.cast_sub (show 2 ≤ n by omega), Nat.cast_sub (show 3 ≤ n by omega), Nat.cast_sub (show 4 ≤ n by omega), Nat.cast_sub (show 5 ≤ n by omega), Nat.cast_sub (show 6 ≤ n by omega), Nat.cast_sub (show 7 ≤ n by omega), Nat.cast_sub (show 8 ≤ n by omega), Nat.cast_sub (show 9 ≤ n by omega)] at he
  simp (discharger := omega) only [if_pos, if_neg] at he
  norm_num [weight, List.range_succ, intCast_falling, fallingPoly, Nat.cast_sub (show 1 ≤ n by omega), Nat.cast_sub (show 2 ≤ n by omega), Nat.cast_sub (show 3 ≤ n by omega), Nat.cast_sub (show 4 ≤ n by omega), Nat.cast_sub (show 5 ≤ n by omega), Nat.cast_sub (show 6 ≤ n by omega), Nat.cast_sub (show 7 ≤ n by omega), Nat.cast_sub (show 8 ≤ n by omega), Nat.cast_sub (show 9 ≤ n by omega)] at he
  dsimp only
  linear_combination he

theorem raw5_0 (n : ℕ) (hn : 17 ≤ n) (a b c d : K) (g : ℕ → K)
    (h : rowValue a b c d n ⟨false, 5, 0, n - 4⟩ g = 0) :
    (let z : K := n; (-2880*z*c + 6000*z^2*c - 4200*z^3*c + 1200*z^4*c - 120*z^5*c) * g 0 + (5760*b - 12000*z*b + 8400*z^2*b - 2400*z^3*b + 240*z^4*b) * g 1 + (17280*a - 18720*z*a + 6480*z^2*a - 720*z^3*a) * g 2 + (57600 - 14400*z) * g 4) = 0 := by
  have he := rowValue_top_split a b c d n 4 5 g (by omega) (by omega) (by omega)
  have hv : 5 + (n - 4) - 5 = n - 4 := by omega
  dsimp only at he
  norm_num at he
  rw [h] at he
  norm_num [List.range_succ, staticColumn, monomialRow, weight, intCast_falling, fallingPoly, Nat.cast_sub (show 1 ≤ n by omega), Nat.cast_sub (show 2 ≤ n by omega), Nat.cast_sub (show 3 ≤ n by omega), Nat.cast_sub (show 4 ≤ n by omega)] at he
  simp (discharger := omega) only [if_pos, if_neg] at he
  norm_num [weight, List.range_succ, intCast_falling, fallingPoly, Nat.cast_sub (show 1 ≤ n by omega), Nat.cast_sub (show 2 ≤ n by omega), Nat.cast_sub (show 3 ≤ n by omega), Nat.cast_sub (show 4 ≤ n by omega)] at he
  norm_num [show Nat.choose 5 2 = 10 by decide, show Nat.choose 5 3 = 10 by decide] at he
  dsimp only
  linear_combination he

theorem raw5_1 (n : ℕ) (hn : 17 ≤ n) (a b c d : K) (g : ℕ → K)
    (h : rowValue a b c d n ⟨false, 5, 1, n - 5⟩ g = 0) :
    (let z : K := n; (-17280*z*d + 36000*z^2*d - 25200*z^3*d + 7200*z^4*d - 720*z^5*d) * g 0 + (28800*c - 62880*z*c + 48000*z^2*c - 16200*z^3*c + 2400*z^4*c - 120*z^5*c) * g 1 + (80640*b - 98880*z*b + 42720*z^2*b - 7680*z^3*b + 480*z^4*b) * g 2 + (155520*a - 116640*z*a + 28080*z^2*a - 2160*z^3*a) * g 3 + (374400 - 72000*z) * g 5) = 0 := by
  have he := rowValue_top_split a b c d n 5 5 g (by omega) (by omega) (by omega)
  have hv : 5 + (n - 5) - 5 = n - 5 := by omega
  dsimp only at he
  norm_num at he
  rw [h] at he
  norm_num [List.range_succ, staticColumn, monomialRow, weight, intCast_falling, fallingPoly, Nat.cast_sub (show 1 ≤ n by omega), Nat.cast_sub (show 2 ≤ n by omega), Nat.cast_sub (show 3 ≤ n by omega), Nat.cast_sub (show 4 ≤ n by omega), Nat.cast_sub (show 5 ≤ n by omega)] at he
  simp (discharger := omega) only [if_pos, if_neg] at he
  norm_num [weight, List.range_succ, intCast_falling, fallingPoly, Nat.cast_sub (show 1 ≤ n by omega), Nat.cast_sub (show 2 ≤ n by omega), Nat.cast_sub (show 3 ≤ n by omega), Nat.cast_sub (show 4 ≤ n by omega), Nat.cast_sub (show 5 ≤ n by omega)] at he
  norm_num [show Nat.choose 5 2 = 10 by decide, show Nat.choose 5 3 = 10 by decide] at he
  dsimp only
  linear_combination he

theorem raw5_2 (n : ℕ) (hn : 17 ≤ n) (a b c d : K) (g : ℕ → K)
    (h : rowValue a b c d n ⟨false, 5, 2, n - 6⟩ g = 0) :
    (let z : K := n; (86400*d - 197280*z*d + 162000*z^2*d - 61200*z^3*d + 10800*z^4*d - 720*z^5*d) * g 1 + (230400*c - 310080*z*c + 154800*z^2*c - 35400*z^3*c + 3600*z^4*c - 120*z^5*c) * g 2 + (432000*b - 381600*z*b + 120240*z^2*b - 15840*z^3*b + 720*z^4*b) * g 3 + (691200*a - 397440*z*a + 73440*z^2*a - 4320*z^3*a) * g 4 + (1382400 - 216000*z) * g 6) = 0 := by
  have he := rowValue_top_split a b c d n 6 5 g (by omega) (by omega) (by omega)
  have hv : 5 + (n - 6) - 5 = n - 6 := by omega
  dsimp only at he
  norm_num at he
  rw [h] at he
  norm_num [List.range_succ, staticColumn, monomialRow, weight, intCast_falling, fallingPoly, Nat.cast_sub (show 1 ≤ n by omega), Nat.cast_sub (show 2 ≤ n by omega), Nat.cast_sub (show 3 ≤ n by omega), Nat.cast_sub (show 4 ≤ n by omega), Nat.cast_sub (show 5 ≤ n by omega), Nat.cast_sub (show 6 ≤ n by omega)] at he
  simp (discharger := omega) only [if_pos, if_neg] at he
  norm_num [weight, List.range_succ, intCast_falling, fallingPoly, Nat.cast_sub (show 1 ≤ n by omega), Nat.cast_sub (show 2 ≤ n by omega), Nat.cast_sub (show 3 ≤ n by omega), Nat.cast_sub (show 4 ≤ n by omega), Nat.cast_sub (show 5 ≤ n by omega), Nat.cast_sub (show 6 ≤ n by omega)] at he
  norm_num [show Nat.choose 5 2 = 10 by decide, show Nat.choose 5 3 = 10 by decide] at he
  dsimp only
  linear_combination he

theorem raw5_3 (n : ℕ) (hn : 17 ≤ n) (a b c d : K) (g : ℕ → K)
    (h : rowValue a b c d n ⟨false, 5, 3, n - 7⟩ g = 0) :
    (let z : K := n; (518400*d - 751680*z*d + 417600*z^2*d - 111600*z^3*d + 14400*z^4*d - 720*z^5*d) * g 2 + (950400*c - 946080*z*c + 355200*z^2*c - 61800*z^3*c + 4800*z^4*c - 120*z^5*c) * g 3 + (1497600*b - 1038720*z*b + 258240*z^2*b - 26880*z^3*b + 960*z^4*b) * g 4 + (2160000*a - 1008000*z*a + 151200*z^2*a - 7200*z^3*a) * g 5 + (3830400 - 504000*z) * g 7) = 0 := by
  have he := rowValue_top_split a b c d n 7 5 g (by omega) (by omega) (by omega)
  have hv : 5 + (n - 7) - 5 = n - 7 := by omega
  dsimp only at he
  norm_num at he
  rw [h] at he
  norm_num [List.range_succ, staticColumn, monomialRow, weight, intCast_falling, fallingPoly, Nat.cast_sub (show 1 ≤ n by omega), Nat.cast_sub (show 2 ≤ n by omega), Nat.cast_sub (show 3 ≤ n by omega), Nat.cast_sub (show 4 ≤ n by omega), Nat.cast_sub (show 5 ≤ n by omega), Nat.cast_sub (show 6 ≤ n by omega), Nat.cast_sub (show 7 ≤ n by omega)] at he
  simp (discharger := omega) only [if_pos, if_neg] at he
  norm_num [weight, List.range_succ, intCast_falling, fallingPoly, Nat.cast_sub (show 1 ≤ n by omega), Nat.cast_sub (show 2 ≤ n by omega), Nat.cast_sub (show 3 ≤ n by omega), Nat.cast_sub (show 4 ≤ n by omega), Nat.cast_sub (show 5 ≤ n by omega), Nat.cast_sub (show 6 ≤ n by omega), Nat.cast_sub (show 7 ≤ n by omega)] at he
  norm_num [show Nat.choose 5 2 = 10 by decide, show Nat.choose 5 3 = 10 by decide] at he
  dsimp only
  linear_combination he

theorem raw5_4 (n : ℕ) (hn : 17 ≤ n) (a b c d : K) (g : ℕ → K)
    (h : rowValue a b c d n ⟨false, 5, 4, n - 8⟩ g = 0) :
    (let z : K := n; (1814400*d - 1982880*z*d + 846000*z^2*d - 176400*z^3*d + 18000*z^4*d - 720*z^5*d) * g 3 + (2822400*c - 2244480*z*c + 678000*z^2*c - 95400*z^3*c + 6000*z^4*c - 120*z^5*c) * g 4 + (4032000*b - 2306400*z*b + 474000*z^2*b - 40800*z^3*b + 1200*z^4*b) * g 5 + (5443200*a - 2138400*z*a + 270000*z^2*a - 10800*z^3*a) * g 6 + (8870400 - 1008000*z) * g 8) = 0 := by
  have he := rowValue_top_split a b c d n 8 5 g (by omega) (by omega) (by omega)
  have hv : 5 + (n - 8) - 5 = n - 8 := by omega
  dsimp only at he
  norm_num at he
  rw [h] at he
  norm_num [List.range_succ, staticColumn, monomialRow, weight, intCast_falling, fallingPoly, Nat.cast_sub (show 1 ≤ n by omega), Nat.cast_sub (show 2 ≤ n by omega), Nat.cast_sub (show 3 ≤ n by omega), Nat.cast_sub (show 4 ≤ n by omega), Nat.cast_sub (show 5 ≤ n by omega), Nat.cast_sub (show 6 ≤ n by omega), Nat.cast_sub (show 7 ≤ n by omega), Nat.cast_sub (show 8 ≤ n by omega)] at he
  simp (discharger := omega) only [if_pos, if_neg] at he
  norm_num [weight, List.range_succ, intCast_falling, fallingPoly, Nat.cast_sub (show 1 ≤ n by omega), Nat.cast_sub (show 2 ≤ n by omega), Nat.cast_sub (show 3 ≤ n by omega), Nat.cast_sub (show 4 ≤ n by omega), Nat.cast_sub (show 5 ≤ n by omega), Nat.cast_sub (show 6 ≤ n by omega), Nat.cast_sub (show 7 ≤ n by omega), Nat.cast_sub (show 8 ≤ n by omega)] at he
  norm_num [show Nat.choose 5 2 = 10 by decide, show Nat.choose 5 3 = 10 by decide] at he
  dsimp only
  linear_combination he

theorem raw5_5 (n : ℕ) (hn : 17 ≤ n) (a b c d : K) (g : ℕ → K)
    (h : rowValue a b c d n ⟨false, 5, 5, n - 9⟩ g = 0) :
    (let z : K := n; (4838400*d - 4279680*z*d + 1490400*z^2*d - 255600*z^3*d + 21600*z^4*d - 720*z^5*d) * g 4 + (6854400*c - 4550880*z*c + 1152000*z^2*c - 136200*z^3*c + 7200*z^4*c - 120*z^5*c) * g 5 + (9192960*b - 4478400*z*b + 784800*z^2*b - 57600*z^3*b + 1440*z^4*b) * g 6 + (11854080*a - 4021920*z*a + 438480*z^2*a - 15120*z^3*a) * g 7 + (18144000 - 1814400*z) * g 9) = 0 := by
  have he := rowValue_top_split a b c d n 9 5 g (by omega) (by omega) (by omega)
  have hv : 5 + (n - 9) - 5 = n - 9 := by omega
  dsimp only at he
  norm_num at he
  rw [h] at he
  norm_num [List.range_succ, staticColumn, monomialRow, weight, intCast_falling, fallingPoly, Nat.cast_sub (show 1 ≤ n by omega), Nat.cast_sub (show 2 ≤ n by omega), Nat.cast_sub (show 3 ≤ n by omega), Nat.cast_sub (show 4 ≤ n by omega), Nat.cast_sub (show 5 ≤ n by omega), Nat.cast_sub (show 6 ≤ n by omega), Nat.cast_sub (show 7 ≤ n by omega), Nat.cast_sub (show 8 ≤ n by omega), Nat.cast_sub (show 9 ≤ n by omega)] at he
  simp (discharger := omega) only [if_pos, if_neg] at he
  norm_num [weight, List.range_succ, intCast_falling, fallingPoly, Nat.cast_sub (show 1 ≤ n by omega), Nat.cast_sub (show 2 ≤ n by omega), Nat.cast_sub (show 3 ≤ n by omega), Nat.cast_sub (show 4 ≤ n by omega), Nat.cast_sub (show 5 ≤ n by omega), Nat.cast_sub (show 6 ≤ n by omega), Nat.cast_sub (show 7 ≤ n by omega), Nat.cast_sub (show 8 ≤ n by omega), Nat.cast_sub (show 9 ≤ n by omega)] at he
  norm_num [show Nat.choose 5 2 = 10 by decide, show Nat.choose 5 3 = 10 by decide] at he
  dsimp only
  linear_combination he

end SexticC3.StaticTail
