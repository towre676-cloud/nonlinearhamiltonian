import SexticC3.StaticTail

namespace SexticC3.TailDegreeFactors

/-- Horner coefficients in increasing degree order. -/
def eval {R : Type*} [CommRing R] (x : R) : List ℤ → R
  | [] => 0
  | c :: cs => (c : R) + x * eval x cs

private def addConstant (c : ℤ) : List ℤ → List ℤ
  | [] => [c]
  | a :: as => (c + a) :: as

private theorem eval_addConstant {R : Type*} [CommRing R] (x : R) (c : ℤ)
    (cs : List ℤ) : eval x (addConstant c cs) = (c : R) + eval x cs := by
  cases cs <;> simp [addConstant, eval, Int.cast_add, add_assoc]

/-- Multiplication by X + 17 in the coefficient representation. -/
private def mulShift : List ℤ → List ℤ
  | [] => []
  | a :: as => (17 * a) :: addConstant a (mulShift as)

private theorem eval_mulShift {R : Type*} [CommRing R] (x : R) (cs : List ℤ) :
    eval x (mulShift cs) = (x + 17) * eval x cs := by
  induction cs with
  | nil => simp [mulShift, eval]
  | cons c cs ih =>
    simp only [mulShift, eval, eval_addConstant, ih, Int.cast_mul, Int.reduceNeg, Int.cast_ofNat]
    ring

/-- Coefficients after substituting X + 17 for X. -/
def shift : List ℤ → List ℤ
  | [] => []
  | c :: cs => addConstant c (mulShift (shift cs))

theorem eval_shift {R : Type*} [CommRing R] (x : R) (cs : List ℤ) :
    eval x (shift cs) = eval (x + 17) cs := by
  induction cs with
  | nil => rfl
  | cons c cs ih => simp only [shift, eval_addConstant, eval_mulShift, ih, eval]

def positiveCoefficients : List ℤ → Bool
  | [] => false
  | c :: cs => decide (0 < c) && cs.all fun a => decide (0 ≤ a)

private theorem eval_nonneg (x : ℤ) (hx : 0 ≤ x) (cs : List ℤ)
    (h : cs.all (fun a => decide (0 ≤ a)) = true) : 0 ≤ eval x cs := by
  induction cs with
  | nil => simp [eval]
  | cons c cs ih =>
    simp only [List.all_cons, Bool.and_eq_true, decide_eq_true_eq] at h
    simpa only [eval, Int.cast_id] using add_nonneg h.1 (mul_nonneg hx (ih h.2))

private theorem eval_pos (x : ℤ) (hx : 0 ≤ x) (cs : List ℤ)
    (h : positiveCoefficients cs = true) : 0 < eval x cs := by
  cases cs with
  | nil => simp [positiveCoefficients] at h
  | cons c cs =>
    simp only [positiveCoefficients, Bool.and_eq_true, decide_eq_true_eq] at h
    simpa only [eval, Int.cast_id] using add_pos_of_pos_of_nonneg h.1
      (mul_nonneg hx (eval_nonneg x hx cs h.2))

private theorem eval_cast {R : Type*} [CommRing R] (x : ℤ) (cs : List ℤ) :
    (↑(eval x cs : ℤ) : R) = eval (x : R) cs := by
  induction cs with
  | nil => simp [eval]
  | cons c cs ih => simp only [eval, Int.cast_id, Int.cast_add, Int.cast_mul, ih]

/-- A positive constant and nonnegative higher coefficients after shifting
certify nonvanishing at every integer degree at least seventeen. -/
theorem eval_ne_zero {K : Type*} [Field K] [CharZero K] (cs : List ℤ)
    (h : positiveCoefficients (shift cs) = true) (n : ℕ) (hn : 17 ≤ n) :
    eval (n : K) cs ≠ 0 := by
  have hpos := eval_pos ((n : ℤ) - 17) (by omega) (shift cs) h
  rw [eval_shift, sub_add_cancel] at hpos
  have hnz : (↑(eval (n : ℤ) cs : ℤ) : K) ≠ 0 := Int.cast_ne_zero.mpr (ne_of_gt hpos)
  simpa only [eval_cast, Int.cast_natCast] using hnz

end SexticC3.TailDegreeFactors
