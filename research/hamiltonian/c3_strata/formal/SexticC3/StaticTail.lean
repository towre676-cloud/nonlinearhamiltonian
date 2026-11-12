import SexticC3.DeltaData
import Mathlib.Algebra.Polynomial.Derivative
import Mathlib.Algebra.BigOperators.Group.List.Basic

namespace SexticC3.StaticTail

/-- Falling factorial with subtraction in the coefficient ring. -/
def fallingPoly {R : Type*} [CommRing R] (x : R) : Nat → R
  | 0 => 1
  | k + 1 => x * fallingPoly (x - 1) k

theorem intCast_falling (e k : Nat) :
    (falling e k : ℤ) = fallingPoly (e : ℤ) k := by
  induction k generalizing e with
  | zero => rfl
  | succ k ih =>
    cases e with
    | zero => simp [falling, fallingPoly]
    | succ e =>
      simp [falling, fallingPoly, ih, Nat.cast_succ]

theorem weight_three (n j : Nat) (hj : j ≤ n) :
    weight 3 1 n j =
      60 * (j : ℤ) * ((j : ℤ) - 1) * ((n : ℤ) - 2 * (j : ℤ) + 2) := by
  unfold weight
  norm_num [List.range_succ, falling, intCast_falling, fallingPoly, Nat.cast_sub hj]
  ring

theorem weight_five (n j : Nat) (hj : j ≤ n) :
    weight 5 1 n j =
      120 * (j : ℤ) * ((j : ℤ) - 1) * ((j : ℤ) - 2) * ((j : ℤ) - 3) *
        (5 * (n : ℤ) - 6 * (j : ℤ) + 4) := by
  unfold weight
  norm_num [List.range_succ, falling, intCast_falling, fallingPoly, Nat.cast_sub hj]
  ring

/-- Each column at distance at least two from the simple-root edge has a
nonzero static pivot in degree at least seventeen. -/
theorem static_pivot (n j : Nat) (hn : 17 ≤ n) (hj : 2 ≤ j) (hjn : j ≤ n) :
    weight 3 1 n j ≠ 0 ∨ weight 5 1 n j ≠ 0 := by
  by_cases h : (n : ℤ) - 2 * (j : ℤ) + 2 = 0
  · right
    rw [weight_five n j hjn]
    have hj' : (4 : ℤ) ≤ (j : ℤ) := by omega
    exact mul_ne_zero
      (mul_ne_zero (mul_ne_zero (mul_ne_zero (mul_ne_zero (by decide) (by omega))
        (by omega)) (by omega)) (by omega)) (by omega)
  · left
    rw [weight_three n j hjn]
    exact mul_ne_zero (mul_ne_zero (mul_ne_zero (by decide) (by omega)) (by omega)) h


variable {R : Type*} [CommRing R]

/-- One input column of the static transvectant in homogeneous degree n. -/
def staticColumn (a b c d : R) (n k u v j : Nat) : R :=
  ((monomialRow k u v 1 n j : ℤ) : R) +
    (monomialRow k u v 3 n j : R) * a +
    (monomialRow k u v 4 n j : R) * b +
    (monomialRow k u v 5 n j : R) * c +
    (monomialRow k u v 6 n j : R) * d

/-- Coefficient of q^u p^v in the uniform static transvectant on degree n. -/
def staticTransvectant (a b c d : R) (n k : Nat) (g : Nat → R) (u v : Nat) : R :=
  ((List.range (n + 1)).map fun j => staticColumn a b c d n k u v j * g j).sum

private def termValue (a b c d : R) (g : Nat → R) (t : RowTerm) : R :=
  (t.scalar : R) * hCoeff a b c d t.outer *
    (t.inner.map (hCoeff a b c d)).getD 1 * g t.partner

private theorem filter_sum (a b c d : R) (g : Nat → R) (ts : List RowTerm) :
    ((ts.filter (·.scalar != 0)).map (termValue a b c d g)).sum =
      (ts.map (termValue a b c d g)).sum := by
  induction ts with
  | nil => rfl
  | cons t ts ih =>
    by_cases h : t.scalar = 0
    · simp [h, termValue, ih]
    · simp [h, ih]

private def staticTerms (n k u v j : Nat) : List RowTerm :=
  sexticExponents.map fun i => ⟨j, i, none, monomialRow k u v i n j⟩

private theorem static_sum (a b c d : R) (g : Nat → R) (n k u v : Nat)
    (js : List Nat) :
    ((js.flatMap (staticTerms n k u v)).map (termValue a b c d g)).sum =
      (js.map fun j => staticColumn a b c d n k u v j * g j).sum := by
  induction js with
  | nil => rfl
  | cons j js ih =>
    simp only [List.flatMap_cons, List.map_append, List.sum_append, ih,
      List.map_cons, List.sum_cons]
    simp [staticTerms, sexticExponents, termValue, hCoeff, staticColumn]
    ring

theorem rowValue_static (a b c d : R) (n k u v : Nat) (g : Nat → R)
    (hd : u + v + 2 * k = 6 + n) :
    rowValue a b c d n ⟨false, k, u, v⟩ g =
      staticTransvectant a b c d n k g u v := by
  have h : inDegree n ⟨false, k, u, v⟩ := by simpa [inDegree] using hd
  unfold rowValue rowTerms
  rw [if_neg (not_not_intro h)]
  change (((List.range (n + 1)).flatMap (staticTerms n k u v)).filter
    (·.scalar != 0) |>.map (termValue a b c d g)).sum = _
  rw [filter_sum]
  exact static_sum a b c d g n k u v _

private theorem column_above (a b c d : R) (n k u v j : Nat)
    (h : u + k < 1 + j) : staticColumn a b c d n k u v j = 0 := by
  have h1 : 1+j ≠ u+k := by omega
  have h3 : 3+j ≠ u+k := by omega
  have h4 : 4+j ≠ u+k := by omega
  have h5 : 5+j ≠ u+k := by omega
  have h6 : 6+j ≠ u+k := by omega
  simp [staticColumn, monomialRow, h1, h3, h4, h5, h6]

private theorem column_at (a b c d : R) (n k u v j : Nat)
    (hq : 1 + j = u + k) (hp : 5 + (n-j) = v + k) :
    staticColumn a b c d n k u v j = (weight k 1 n j : R) := by
  have h3 : 3+j ≠ u+k := by omega
  have h4 : 4+j ≠ u+k := by omega
  have h5 : 5+j ≠ u+k := by omega
  have h6 : 6+j ≠ u+k := by omega
  simp [staticColumn, monomialRow, hq, hp, h3, h4, h5, h6]

/-- The static row at this index splits into its edge pivot and lower columns. -/
theorem rowValue_top_split (a b c d : R) (n j k : Nat) (g : Nat → R)
    (hj : j ≤ n) (hjk : k ≤ 1 + j) (hp : k ≤ 5 + (n-j)) :
    let u := 1 + j - k
    let v := 5 + (n-j) - k
    rowValue a b c d n ⟨false, k, u, v⟩ g =
      ((List.range j).map fun i => staticColumn a b c d n k u v i * g i).sum +
        (weight k 1 n j : R) * g j := by
  dsimp only
  let u := 1 + j - k
  let v := 5 + (n-j) - k
  have hd : u + v + 2 * k = 6 + n := by dsimp [u, v]; omega
  rw [rowValue_static a b c d n k u v g hd]
  unfold staticTransvectant
  have cut : ∀ m, j + 1 ≤ m →
      ((List.range m).map fun i => staticColumn a b c d n k u v i * g i).sum =
        ((List.range (j + 1)).map fun i => staticColumn a b c d n k u v i * g i).sum := by
    intro m
    induction m with
    | zero => omega
    | succ m ih =>
      intro hm
      by_cases he : m = j
      · subst m
        rfl
      · rw [List.range_succ, List.map_append, List.sum_append, ih (by omega)]
        simp [column_above a b c d n k u v m (by dsimp [u]; omega)]
  rw [cut (n + 1) (by omega), List.range_succ, List.map_append, List.sum_append]
  simp [column_at a b c d n k u v j (by dsimp [u]; omega) (by dsimp [v]; omega)]
  rfl

variable {K : Type*} [Field K] [CharZero K]

private theorem zero_of_pivot (a b c d : K) (n j k : Nat) (g : Nat → K)
    (h : ∀ k u v, (k = 3 ∨ k = 5) → rowValue a b c d n ⟨false, k, u, v⟩ g = 0)
    (hk : k = 3 ∨ k = 5) (hj : j ≤ n) (hjk : k ≤ 1 + j) (hp : k ≤ 5 + (n-j))
    (hw : weight k 1 n j ≠ 0) (hz : ∀ i < j, g i = 0) :
    g j = 0 := by
  let u := 1 + j - k
  let v := 5 + (n-j) - k
  have he := rowValue_top_split a b c d n j k g hj hjk hp
  change rowValue a b c d n ⟨false, k, u, v⟩ g = _ at he
  rw [h k u v hk] at he
  have hs : ((List.range j).map fun i => staticColumn a b c d n k u v i * g i) =
      (List.range j).map (fun _ => (0 : K)) :=
    List.map_congr_left fun i hi => by rw [hz i (List.mem_range.mp hi), mul_zero]
  rw [hs] at he
  simp at he
  exact he.resolve_left hw

/-- The first two coefficients determine every high-degree static partner
in the normalized simple-root chart. This uses only the depth-zero rows
of the existing coefficient model. -/
theorem kernel_zero_of_edge_zero (a b c d : K) (n : Nat) (hn : 17 ≤ n)
    (g : Nat → K)
    (h : ∀ k u v, (k = 3 ∨ k = 5) → rowValue a b c d n ⟨false, k, u, v⟩ g = 0)
    (h0 : g 0 = 0) (h1 : g 1 = 0) : ∀ j ≤ n, g j = 0 := by
  intro j
  induction j using Nat.strong_induction_on with
  | h j ih =>
    intro hj
    by_cases hj2 : 2 ≤ j
    · have hz : ∀ i < j, g i = 0 := fun i hi => ih i hi (by omega)
      by_cases hw : weight 3 1 n j = 0
      · have hres : (n : ℤ) - 2 * (j : ℤ) + 2 = 0 := by
          rw [weight_three n j hj] at hw
          exact (mul_eq_zero.mp hw).resolve_left
            (mul_ne_zero (mul_ne_zero (by decide) (by omega)) (by omega))
        exact zero_of_pivot a b c d n j 5 g h (Or.inr rfl) hj (by omega)
          (by omega) ((static_pivot n j hn hj2 hj).resolve_left (not_not_intro hw)) hz
      · exact zero_of_pivot a b c d n j 3 g h (Or.inl rfl) hj (by omega)
          (by omega) hw hz
    · have hsmall : j = 0 ∨ j = 1 := by omega
      rcases hsmall with rfl | rfl
      · exact h0
      · exact h1


/-- At the six-row certificate cutoff the T₃ pivots alone are nonzero.
Its six T₅ rows use input coefficients only through index nine. -/
theorem certificate_pivot (n j : Nat) (hn : 17 ≤ n) (hj : 2 ≤ j) (hmax : j ≤ 9) :
    weight 3 1 n j ≠ 0 := by
  rw [weight_three n j (by omega)]
  exact mul_ne_zero (mul_ne_zero (mul_ne_zero (by decide) (by omega)) (by omega)) (by omega)

/-- The precise forward substitution needed before deriving the six T₅ rows. -/
theorem certificate_top_equation (a b c d : K) (n j : Nat) (g : Nat → K)
    (hn : 17 ≤ n) (hj : 2 ≤ j) (hmax : j ≤ 9)
    (h : rowValue a b c d n ⟨false, 3, j - 2, n - j + 2⟩ g = 0) :
    g j =
      -((List.range j).map fun i =>
        staticColumn a b c d n 3 (j - 2) (n - j + 2) i * g i).sum /
        (weight 3 1 n j : K) := by
  have he := rowValue_top_split a b c d n j 3 g (by omega) (by omega) (by omega)
  dsimp only at he
  rw [show 1 + j - 3 = j - 2 by omega,
    show 5 + (n - j) - 3 = n - j + 2 by omega, h] at he
  apply (eq_div_iff (Int.cast_ne_zero.mpr (certificate_pivot n j hn hj hmax))).2
  linear_combination -he

/-- Reconstruct successive coefficients from the T₃ pivots, starting
with the two free coefficients. Only stages up to eight are used. -/
noncomputable def reconstruct (a b c d : K) (n : Nat) (x y : K) :
    Nat → Nat → K
  | 0, i => if i = 0 then x else if i = 1 then y else 0
  | m + 1, i =>
    if i = m + 2 then
      -((List.range (m + 2)).map fun j =>
        staticColumn a b c d n 3 m (n - (m + 2) + 2) j *
          reconstruct a b c d n x y m j).sum / (weight 3 1 n (m + 2) : K)
    else reconstruct a b c d n x y m i

theorem reconstruct_eq (a b c d : K) (n : Nat) (g : Nat → K) (hn : 17 ≤ n)
    (h : ∀ u v, rowValue a b c d n ⟨false, 3, u, v⟩ g = 0)
    (m : Nat) (hm : m ≤ 8) :
    ∀ i ≤ m + 1, reconstruct a b c d n (g 0) (g 1) m i = g i := by
  induction m with
  | zero =>
    intro i hi
    have hsmall : i = 0 ∨ i = 1 := by omega
    rcases hsmall with rfl | rfl <;> simp [reconstruct]
  | succ m ih =>
    intro i hi
    by_cases he : i = m + 2
    · subst i
      rw [reconstruct, if_pos rfl]
      have hmap :
          (List.range (m + 2)).map (fun j =>
            staticColumn a b c d n 3 m (n - (m + 2) + 2) j *
              reconstruct a b c d n (g 0) (g 1) m j) =
          (List.range (m + 2)).map (fun j =>
            staticColumn a b c d n 3 m (n - (m + 2) + 2) j * g j) :=
        List.map_congr_left fun j hj => by
          have := List.mem_range.mp hj
          rw [ih (by omega) j (by omega)]
      rw [hmap]
      symm
      simpa using certificate_top_equation a b c d n (m + 2) g hn (by omega)
        (by omega) (h m (n - (m + 2) + 2))
    · rw [reconstruct, if_neg he]
      exact ih (by omega) i (by omega)

/-- The six T₅ equations in the static-tail certificate, evaluated
on the coefficients reconstructed from the T₃ equations. -/
theorem reconstructed_fifth_rows (a b c d : K) (n : Nat) (g : Nat → K)
    (hn : 17 ≤ n)
    (h : ∀ k u v, (k = 3 ∨ k = 5) → rowValue a b c d n ⟨false, k, u, v⟩ g = 0)
    (t : Nat) (ht : t < 6) :
    rowValue a b c d n ⟨false, 5, t, n - (t + 4)⟩
      (reconstruct a b c d n (g 0) (g 1) 8) = 0 := by
  have split (f : Nat → K) := rowValue_top_split a b c d n (t + 4) 5 f
    (by omega) (by omega) (by omega)
  dsimp only at split
  have hq : 1 + (t + 4) - 5 = t := by omega
  have hp : 5 + (n - (t + 4)) - 5 = n - (t + 4) := by omega
  simp only [hq, hp] at split
  have he := reconstruct_eq a b c d n g hn (fun u v => h 3 u v (Or.inl rfl)) 8 (by decide)
  rw [split, ← h 5 t (n - (t + 4)) (Or.inr rfl), split, he (t + 4) (by omega)]
  congr 2
  apply List.map_congr_left
  intro i hi
  have := List.mem_range.mp hi
  rw [he i (by omega)]

private theorem target_parameters (a b c d : K)
    (hb : b^2 + (2/5 : K) * a^3 = 0)
    (hc : c + (3/20 : K) * a^2 = 0)
    (hd : d + (1/50 : K) * a*b = 0) :
    ∃ r : K, a = -10*r^2 ∧ b = 20*r^3 ∧ c = -15*r^4 ∧ d = 4*r^5 := by
  by_cases ha : a = 0
  · have hb' : b = 0 := by
      simpa [ha, pow_two] using hb
    have hc' : c = 0 := by simpa [ha] using hc
    have hd' : d = 0 := by simpa [ha] using hd
    exact ⟨0, by simp [ha, hb', hc', hd']⟩
  · let r := -b / (2*a)
    have hden : (2 : K) * a ≠ 0 := mul_ne_zero (by norm_num) ha
    have he : r * (2*a) = -b := div_mul_cancel₀ _ hden
    have h₂ : a = -10*r^2 := by
      apply mul_right_cancel₀ (pow_ne_zero 2 hden)
      calc
        a * (2*a)^2 = -10 * b^2 := by linear_combination 10 * hb
        _ = (-10*r^2) * (2*a)^2 := by rw [← neg_sq b, ← he]; ring
    have h₃ : b = 20*r^3 := by
      linear_combination he - 2*r*h₂
    have h₄ : c = -15*r^4 := by
      rw [h₂] at hc
      linear_combination hc
    have h₅ : d = 4*r^5 := by
      rw [h₂, h₃] at hd
      linear_combination hd
    exact ⟨r, h₂, h₃, h₄, h₅⟩

/-- The elimination targets give a fourth power factor in the normalized
quintic, including the fifth power at the origin. -/
theorem target_factorization (a b c d : K)
    (hb : b^2 + (2/5 : K) * a^3 = 0)
    (hc : c + (3/20 : K) * a^2 = 0)
    (hd : d + (1/50 : K) * a*b = 0) :
    ∃ r : K,
      Polynomial.X^5 + Polynomial.C a * Polynomial.X^3 +
          Polynomial.C b * Polynomial.X^2 + Polynomial.C c * Polynomial.X +
          Polynomial.C d = (Polynomial.X - Polynomial.C r)^4 *
            (Polynomial.X + 4 * Polynomial.C r) := by
  obtain ⟨r, ha, hb', hc', hd'⟩ := target_parameters a b c d hb hc hd
  refine ⟨r, ?_⟩
  rw [ha, hb', hc', hd']
  simp [map_mul, map_pow, map_neg, map_ofNat]
  ring

/-- Both target leaves force the same discriminant used by the finite
Lean bridge to vanish. This step needs no geometric discriminant theorem. -/
theorem delta_zero_of_targets (a b c d : K)
    (hb : b^2 + (2/5 : K) * a^3 = 0)
    (hc : c + (3/20 : K) * a^2 = 0)
    (hd : d + (1/50 : K) * a*b = 0) : delta a b c d = 0 := by
  obtain ⟨r, ha, hb', hc', hd'⟩ := target_parameters a b c d hb hc hd
  rw [ha, hb', hc', hd']
  unfold delta
  ring

/-- Set p = 1 in a degree-n homogeneous coefficient vector. -/
noncomputable def dehomogenize (n : Nat) (g : Nat → R) : Polynomial R :=
  ((List.range (n+1)).map fun j => Polynomial.monomial j (g j)).sum

/-- The p derivative after setting p = 1. The q derivative in this
chart is Mathlib's ordinary polynomial derivative. -/
noncomputable def pDerivative (n : Nat) (f : Polynomial R) : Polynomial R :=
  Polynomial.C (n : R) * f - Polynomial.X * Polynomial.derivative f

theorem pDerivative_monomial (n j : Nat) (hj : j ≤ n) (x : R) :
    pDerivative n (Polynomial.monomial j x) =
      Polynomial.monomial j ((↑(n-j) : R) * x) := by
  cases j with
  | zero => simp [pDerivative, Polynomial.derivative_monomial, Polynomial.C_mul_monomial]
  | succ j =>
    rw [pDerivative, Polynomial.derivative_monomial_succ, Polynomial.X_mul_monomial,
      Polynomial.C_mul_monomial, ← Polynomial.monomial_sub, Nat.cast_sub hj]
    congr 1
    push_cast
    ring

end SexticC3.StaticTail
