import SexticC3.Model
import Mathlib.Algebra.MvPolynomial.PDeriv
import Mathlib.Algebra.MvPolynomial.CommRing

/-!
The coefficient tensor's falling factors are the coefficients of Mathlib's
formal partial derivatives.  The variables are `false = q` and `true = p`.
-/
noncomputable section

namespace SexticC3.Differential

open MvPolynomial

variable {R : Type*} [CommRing R]

abbrev Poly := MvPolynomial Bool R

def exponent (i j : Nat) : Bool →₀ Nat :=
  Finsupp.single false i + Finsupp.single true j

def mono (i j : Nat) (c : R) : Poly (R := R) := monomial (exponent i j) c

@[simp] theorem exponent_false (i j : Nat) : exponent i j false = i := by simp [exponent]
@[simp] theorem exponent_true (i j : Nat) : exponent i j true = j := by simp [exponent]

theorem exponent_injective : Function.Injective (fun ij : Nat × Nat => exponent ij.1 ij.2) := by
  intro a b h
  have hq := congrArg (fun e => e false) h
  have hp := congrArg (fun e => e true) h
  simp only [exponent_false, exponent_true] at hq hp
  exact Prod.ext hq hp

@[simp] theorem exponent_eq (i j u v : Nat) : exponent i j = exponent u v ↔ i = u ∧ j = v := by
  constructor
  · intro h
    have h' := @exponent_injective (i,j) (u,v) h
    exact ⟨congrArg Prod.fst h', congrArg Prod.snd h'⟩
  · rintro ⟨rfl, rfl⟩
    rfl

theorem exponent_sub_q (i j : Nat) :
    exponent i j - Finsupp.single false 1 = exponent (i-1) j := by
  ext x
  cases x <;> simp [exponent]

theorem exponent_sub_p (i j : Nat) :
    exponent i j - Finsupp.single true 1 = exponent i (j-1) := by
  ext x
  cases x <;> simp [exponent]

@[simp] theorem pderiv_q_mono (i j : Nat) (c : R) :
    pderiv false (mono i j c) = mono (i-1) j (c * i) := by
  simp [mono, pderiv_monomial, exponent_sub_q]

@[simp] theorem pderiv_p_mono (i j : Nat) (c : R) :
    pderiv true (mono i j c) = mono i (j-1) (c * j) := by
  simp [mono, pderiv_monomial, exponent_sub_p]

theorem iterated_q_mono (r i j : Nat) (c : R) :
    (pderiv false)^[r] (mono i j c) = mono (i-r) j (c * (falling i r : R)) := by
  induction r generalizing i c with
  | zero => simp [falling]
  | succ r ih =>
    rw [Function.iterate_succ_apply, pderiv_q_mono, ih]
    simp [falling, Nat.sub_sub, Nat.cast_mul, mul_assoc, Nat.add_comm]

theorem iterated_p_mono (r i j : Nat) (c : R) :
    (pderiv true)^[r] (mono i j c) = mono i (j-r) (c * (falling j r : R)) := by
  induction r generalizing j c with
  | zero => simp [falling]
  | succ r ih =>
    rw [Function.iterate_succ_apply, pderiv_p_mono, ih]
    simp [falling, Nat.sub_sub, Nat.cast_mul, mul_assoc, Nat.add_comm]

/-- The mixed formal partial derivative ∂q^r ∂p^s. -/
def mixed (r s : Nat) (F : Poly (R := R)) : Poly (R := R) :=
  (pderiv false)^[r] ((pderiv true)^[s] F)

theorem mixed_mono (r s i j : Nat) (c : R) :
    mixed r s (mono i j c) =
      mono (i-r) (j-s) (c * (falling i r : R) * (falling j s : R)) := by
  rw [mixed, iterated_p_mono, iterated_q_mono]
  congr 1
  ring

@[simp] theorem mono_zero (i j : Nat) : mono i j (0 : R) = 0 := by simp [mono]

@[simp] theorem mono_mul (i j u v : Nat) (a b : R) :
    mono i j a * mono u v b = mono (i+u) (j+v) (a*b) := by
  have he : exponent i j + exponent u v = exponent (i+u) (j+v) := by
    ext x
    cases x <;> simp [exponent]
  simp only [mono, monomial_mul, he]

@[simp] theorem coeff_mono (u v i j : Nat) (c : R) :
    coeff (exponent u v) (mono i j c) = if i = u ∧ j = v then c else 0 := by
  simp only [mono, coeff_monomial, exponent_eq]

/-- The unnormalized alternating differential contraction, using Mathlib
partial derivatives.  No tensor coefficients occur in this definition. -/
def contraction (k : Nat) (F G : Poly (R := R)) : Poly (R := R) :=
  ((List.range (k+1)).map fun s =>
    C ((-1 : R)^s * (Nat.choose k s : R)) *
      mixed (k-s) s F * mixed s (k-s) G).sum


@[simp] theorem C_mul_mono (i j : Nat) (a b : R) :
    C a * mono i j b = mono i j (a*b) := by
  exact C_mul_monomial

theorem falling_eq_descFactorial (i r : Nat) : falling i r = i.descFactorial r := by
  induction r generalizing i with
  | zero => rfl
  | succ r ih =>
    cases i with
    | zero => simp [falling, Nat.zero_descFactorial_succ]
    | succ i =>
      rw [falling, ih]
      simpa only [Nat.succ_eq_add_one, Nat.add_sub_cancel] using
        (Nat.succ_descFactorial_succ i r).symm

theorem falling_eq_zero_of_lt {i r : Nat} (h : i < r) : falling i r = 0 := by
  rw [falling_eq_descFactorial]
  exact Nat.descFactorial_of_lt h

/-- One summand in the differential contraction has the tensor's coefficient.
The zero cases are essential: natural-number subtraction in monomial exponents
must never turn an over-differentiated monomial into a spurious contribution. -/
theorem contraction_term_coeff (k s u v i n j : Nat) (hs : s ≤ k) (a b : R) :
    coeff (exponent u v)
      (C ((-1 : R)^s * (Nat.choose k s : R)) *
        mixed (k-s) s (mono i (6-i) a) * mixed s (k-s) (mono j (n-j) b)) =
    if i+j = u+k ∧ (6-i)+(n-j) = v+k then
      ((-1 : R)^s * (Nat.choose k s : R) *
        (falling i (k-s) : R) * (falling (6-i) s : R) *
        (falling j s : R) * (falling (n-j) (k-s) : R)) * a * b else 0 := by
  by_cases h1 : k-s ≤ i
  · by_cases h2 : s ≤ 6-i
    · by_cases h3 : s ≤ j
      · by_cases h4 : k-s ≤ n-j
        · rw [mixed_mono, mixed_mono, C_mul_mono, mono_mul, coeff_mono]
          have he : (i-(k-s)+(j-s) = u ∧ (6-i-s)+(n-j-(k-s)) = v) ↔
              (i+j = u+k ∧ (6-i)+(n-j) = v+k) := by omega
          simp only [he]
          split_ifs <;> ring
        · have hz := falling_eq_zero_of_lt (Nat.lt_of_not_ge h4)
          simp [mixed_mono, hz]
      · have hz := falling_eq_zero_of_lt (Nat.lt_of_not_ge h3)
        simp [mixed_mono, hz]
    · have hz := falling_eq_zero_of_lt (Nat.lt_of_not_ge h2)
      simp [mixed_mono, hz]
  · have hz := falling_eq_zero_of_lt (Nat.lt_of_not_ge h1)
    simp [mixed_mono, hz]



theorem coeff_list_sum (u v : Nat) (xs : List (Poly (R := R))) :
    coeff (exponent u v) xs.sum = (xs.map (coeff (exponent u v))).sum := by
  induction xs with
  | nil => simp
  | cons x xs ih => simp [ih]

theorem intCast_list_sum (xs : List ℤ) : (xs.sum : R) = (xs.map fun x : ℤ => (x : R)).sum := by
  induction xs with
  | nil => simp
  | cons x xs ih => simp [ih]

theorem list_sum_mul (xs : List R) (c : R) : xs.sum * c = (xs.map (fun x => x*c)).sum := by
  induction xs with
  | nil => simp
  | cons x xs ih => simp [add_mul, ih]

/-- The existing tensor's monomial row is the coefficient of the actual
alternating partial-derivative contraction in every order and degree. -/
theorem contraction_mono_coeff (k u v i n j : Nat) (a b : R) :
    coeff (exponent u v)
      (contraction k (mono i (6-i) a) (mono j (n-j) b)) =
        (monomialRow k u v i n j : R) * a * b := by
  rw [contraction, coeff_list_sum]
  simp only [List.map_map, Function.comp_def]
  have hsums : ((List.range (k+1)).map fun s =>
      coeff (exponent u v)
        (C ((-1 : R)^s * (Nat.choose k s : R)) *
          mixed (k-s) s (mono i (6-i) a) * mixed s (k-s) (mono j (n-j) b))).sum =
      ((List.range (k+1)).map fun s =>
        if i+j = u+k ∧ (6-i)+(n-j) = v+k then
          ((-1 : R)^s * (Nat.choose k s : R) *
            (falling i (k-s) : R) * (falling (6-i) s : R) *
            (falling j s : R) * (falling (n-j) (k-s) : R)) * a * b else 0).sum := by
    congr 1
    apply List.map_congr_left
    intro s hs
    exact contraction_term_coeff k s u v i n j (by exact Nat.le_of_lt_succ (List.mem_range.mp hs)) a b
  rw [hsums]
  unfold monomialRow
  split_ifs with h
  · rw [weight, intCast_list_sum, list_sum_mul, list_sum_mul]
    simp only [List.map_map, Function.comp_def, Int.cast_mul, Int.cast_pow,
      Int.cast_neg, Int.cast_one, Int.cast_natCast]
  · simp [h]



theorem weight_eq_zero_of_q_lt (k i n j : Nat) (h : i+j < k) : weight k i n j = 0 := by
  unfold weight
  apply List.sum_eq_zero
  intro x hx
  obtain ⟨s, hs, rfl⟩ := List.mem_map.mp hx
  have hs' : s ≤ k := by exact Nat.le_of_lt_succ (List.mem_range.mp hs)
  by_cases hq : i < k-s
  · simp [falling_eq_zero_of_lt hq]
  · have hj : j < s := by omega
    simp [falling_eq_zero_of_lt hj]

theorem weight_eq_zero_of_p_lt (k i n j : Nat) (h : (6-i)+(n-j) < k) : weight k i n j = 0 := by
  unfold weight
  apply List.sum_eq_zero
  intro x hx
  obtain ⟨s, hs, rfl⟩ := List.mem_map.mp hx
  have hs' : s ≤ k := by exact Nat.le_of_lt_succ (List.mem_range.mp hs)
  by_cases hp : 6-i < s
  · simp [falling_eq_zero_of_lt hp]
  · have hj : n-j < k-s := by omega
    simp [falling_eq_zero_of_lt hj]

theorem exponent_eta (e : Bool →₀ Nat) : exponent (e false) (e true) = e := by
  ext x
  cases x <;> simp

/-- Full monomial action of the differential contraction. -/
theorem contraction_mono (k i n j : Nat) (a b : R) :
    contraction k (mono i (6-i) a) (mono j (n-j) b) =
      mono (i+j-k) ((6-i)+(n-j)-k) ((weight k i n j : R)*a*b) := by
  apply MvPolynomial.ext
  intro e
  rw [← exponent_eta e, contraction_mono_coeff, coeff_mono]
  unfold monomialRow
  by_cases hq : k ≤ i+j
  · by_cases hp : k ≤ (6-i)+(n-j)
    · have he : (i+j = e false+k ∧ (6-i)+(n-j) = e true+k) ↔
          (i+j-k = e false ∧ (6-i)+(n-j)-k = e true) := by omega
      simp only [he]
      split_ifs <;> simp
    · rw [weight_eq_zero_of_p_lt k i n j (Nat.lt_of_not_ge hp)]
      split_ifs <;> simp
  · rw [weight_eq_zero_of_q_lt k i n j (Nat.lt_of_not_ge hq)]
    split_ifs <;> simp



theorem iterated_pderiv_add (x : Bool) (r : Nat) (F G : Poly (R := R)) :
    (pderiv x)^[r] (F+G) = (pderiv x)^[r] F + (pderiv x)^[r] G := by
  induction r with
  | zero => rfl
  | succ r ih => simp [Function.iterate_succ_apply', ih, map_add]

theorem iterated_pderiv_zero (x : Bool) (r : Nat) :
    (pderiv x)^[r] (0 : Poly (R := R)) = 0 := by
  induction r with
  | zero => rfl
  | succ r ih => simp [Function.iterate_succ_apply', ih]

@[simp] theorem mixed_add (r s : Nat) (F G : Poly (R := R)) :
    mixed r s (F+G) = mixed r s F + mixed r s G := by
  simp [mixed, iterated_pderiv_add]

@[simp] theorem mixed_zero (r s : Nat) : mixed r s (0 : Poly (R := R)) = 0 := by
  simp [mixed, iterated_pderiv_zero]

@[simp] theorem contraction_add_left (k : Nat) (F G U : Poly (R := R)) :
    contraction k (F+G) U = contraction k F U + contraction k G U := by
  simp [contraction, mul_add, add_mul, List.sum_map_add]

@[simp] theorem contraction_add_right (k : Nat) (F G U : Poly (R := R)) :
    contraction k F (G+U) = contraction k F G + contraction k F U := by
  simp [contraction, mul_add, add_mul, List.sum_map_add]

@[simp] theorem contraction_zero_left (k : Nat) (G : Poly (R := R)) : contraction k 0 G = 0 := by
  simp [contraction]

@[simp] theorem contraction_zero_right (k : Nat) (F : Poly (R := R)) : contraction k F 0 = 0 := by
  simp [contraction]

theorem contraction_sum_left (k : Nat) (Fs : List (Poly (R := R))) (G : Poly) :
    contraction k Fs.sum G = (Fs.map (fun F => contraction k F G)).sum := by
  induction Fs with
  | nil => simp
  | cons F Fs ih => simp [ih]

theorem contraction_sum_right (k : Nat) (F : Poly (R := R)) (Gs : List Poly) :
    contraction k F Gs.sum = (Gs.map (fun G => contraction k F G)).sum := by
  induction Gs with
  | nil => simp
  | cons G Gs ih => simp [ih]

/-- The first contraction in the exact homogeneous degree used by rowTerms. -/
theorem poisson_mono (h n j : Nat) (hh₁ : 1 ≤ h) (hh₆ : h ≤ 6) (hj : j ≤ n) (a b : R) :
    contraction 1 (mono h (6-h) a) (mono j (n-j) b) =
      mono (h+j-1) (n+4-(h+j-1)) ((weight 1 h n j : R)*a*b) := by
  rw [contraction_mono]
  by_cases hs : h+j ≤ n+5
  · have hp : (6-h)+(n-j)-1 = n+4-(h+j-1) := by omega
    rw [hp]
  · have he : h = 6 ∧ j = n := by omega
    rcases he with ⟨rfl, rfl⟩
    rw [weight_eq_zero_of_p_lt 1 6 j j (by omega)]
    simp



/-- Vanishing of the two Moyal correction gates on G and its first Poisson iterate. -/
def FirstRefinement (F G : Poly (R := R)) : Prop :=
  contraction 3 F G = 0 ∧ contraction 5 F G = 0 ∧
    contraction 3 F (contraction 1 F G) = 0 ∧
    contraction 5 F (contraction 1 F G) = 0

/-- Vanishing of the correction gates on every Poisson iterate. -/
def PersistentCore (F G : Poly (R := R)) : Prop :=
  ∀ i : Nat, contraction 3 F ((contraction 1 F)^[i] G) = 0 ∧
    contraction 5 F ((contraction 1 F)^[i] G) = 0

@[simp] theorem contraction_one_self (F : Poly (R := R)) : contraction 1 F F = 0 := by
  norm_num [contraction, List.range_succ, Nat.choose]
  ring

@[simp] theorem contraction_three_self (F : Poly (R := R)) : contraction 3 F F = 0 := by
  norm_num [contraction, List.range_succ, Nat.choose]
  ring

@[simp] theorem contraction_five_self (F : Poly (R := R)) : contraction 5 F F = 0 := by
  norm_num [contraction, List.range_succ, Nat.choose]
  ring

theorem iterated_pderiv_C_mul (x : Bool) (r : Nat) (a : R) (F : Poly) :
    (pderiv x)^[r] (C a * F) = C a * (pderiv x)^[r] F := by
  induction r with
  | zero => rfl
  | succ r ih => simp [Function.iterate_succ_apply', ih, pderiv_C_mul]

@[simp] theorem mixed_C_mul (r s : Nat) (a : R) (F : Poly) :
    mixed r s (C a * F) = C a * mixed r s F := by
  simp [mixed, iterated_pderiv_C_mul]

private theorem list_mul_sum (a : Poly (R := R)) (Fs : List Poly) :
    a * Fs.sum = (Fs.map fun F => a*F).sum := by
  induction Fs with
  | nil => simp
  | cons F Fs ih => simp [mul_add, ih]

theorem contraction_C_mul_right (k : Nat) (a : R) (F G : Poly) :
    contraction k F (C a*G) = C a * contraction k F G := by
  unfold contraction
  rw [list_mul_sum]
  simp only [List.map_map, Function.comp_def, mixed_C_mul]
  congr 1
  apply List.map_congr_left
  intro s hs
  ring

@[simp] theorem firstRefinement_zero (F : Poly (R := R)) : FirstRefinement F 0 := by
  simp [FirstRefinement]

theorem firstRefinement_multiple (F : Poly (R := R)) (a : R) : FirstRefinement F (C a*F) := by
  simp [FirstRefinement, contraction_C_mul_right]

theorem firstRefinement_of_core (F G : Poly (R := R)) (h : PersistentCore F G) :
    FirstRefinement F G := by
  exact ⟨(h 0).1, (h 0).2, (h 1).1, (h 1).2⟩

theorem iterated_poisson_zero (F : Poly (R := R)) (i : Nat) :
    (contraction 1 F)^[i] 0 = 0 := by
  induction i with
  | zero => rfl
  | succ i ih => simp [Function.iterate_succ_apply', ih]

theorem core_of_stationary (F G : Poly (R := R))
    (h3 : contraction 3 F G = 0) (h5 : contraction 5 F G = 0)
    (h1 : contraction 1 F G = 0) : PersistentCore F G := by
  intro i
  cases i with
  | zero => exact ⟨h3, h5⟩
  | succ i => simp [Function.iterate_succ_apply, h1, iterated_poisson_zero]

@[simp] theorem persistentCore_zero (F : Poly (R := R)) : PersistentCore F 0 := by
  apply core_of_stationary <;> simp

theorem persistentCore_multiple (F : Poly (R := R)) (a : R) : PersistentCore F (C a*F) := by
  apply core_of_stationary <;> simp [contraction_C_mul_right]

end SexticC3.Differential
