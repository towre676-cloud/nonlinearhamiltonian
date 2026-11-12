import SexticC3.Differential

noncomputable section

namespace SexticC3.Differential

open MvPolynomial

variable {R : Type*} [CommRing R]

/-- The normalized sextic as an actual multivariate polynomial. -/
def hamiltonian (a b c d : R) : Poly (R := R) :=
  (sexticExponents.map fun i => mono i (6-i) (hCoeff a b c d i)).sum

/-- The homogeneous partner polynomial in the certificate's monomial order. -/
def homogeneous (n : Nat) (g : Nat → R) : Poly (R := R) :=
  ((List.range (n+1)).map fun j => mono j (n-j) (g j)).sum

/-- Differential gate, before or after one actual Poisson derivative. -/
def gate (a b c d : R) (n : Nat) (r : Row) (g : Nat → R) : Poly (R := R) :=
  contraction r.order (hamiltonian a b c d)
    (if r.depth then contraction 1 (hamiltonian a b c d) (homogeneous n g)
      else homogeneous n g)

private theorem sum_flatMap {α β : Type*} (xs : List α) (ys : α → List β) (f : β → R) :
    ((xs.flatMap ys).map f).sum = (xs.map fun x => ((ys x).map f).sum).sum := by
  induction xs with
  | nil => simp
  | cons x xs ih => simp [ih]

private theorem sum_filter_scalar (a b c d : R) (g : Nat → R) (xs : List RowTerm) :
    ((xs.filter (·.scalar != 0)).map fun t =>
      (t.scalar : R) * hCoeff a b c d t.outer *
        (t.inner.map (hCoeff a b c d)).getD 1 * g t.partner).sum =
    (xs.map fun t => (t.scalar : R) * hCoeff a b c d t.outer *
        (t.inner.map (hCoeff a b c d)).getD 1 * g t.partner).sum := by
  induction xs with
  | nil => simp
  | cons x xs ih =>
    by_cases hs : x.scalar = 0
    · simp [hs, ih]
    · simp [hs, ih]

/-- The static tensor row is the coefficient of the differential gate. -/
theorem static_row_eq_coefficient (a b c d : R) (n k u v : Nat) (g : Nat → R)
    (hd : inDegree n ⟨false,k,u,v⟩) :
    rowValue a b c d n ⟨false,k,u,v⟩ g =
      coeff (exponent u v) (gate a b c d n ⟨false,k,u,v⟩ g) := by
  unfold rowValue rowTerms
  simp only [hd, not_true_eq_false, ↓reduceIte, Bool.false_eq_true]
  rw [sum_filter_scalar]
  simp only [sum_flatMap, List.map_cons, List.map_nil, List.sum_cons, List.sum_nil,
    add_zero, Option.map_none, Option.getD_none, mul_one]
  unfold gate homogeneous hamiltonian
  simp only [Bool.false_eq_true, ↓reduceIte]
  rw [contraction_sum_right, coeff_list_sum]
  simp only [List.map_map, Function.comp_def]
  congr 1
  apply List.map_congr_left
  intro j hj
  rw [contraction_sum_left, coeff_list_sum]
  simp only [List.map_map, Function.comp_def, contraction_mono_coeff]
  change (sexticExponents.map fun x =>
      (monomialRow k u v x n j : R) * hCoeff a b c d x * 1 * g j).sum = _
  simp only [mul_one]



/-- Polynomial interpretation of the first transvectant used in dynamic rows. -/
theorem poisson_homogeneous (a b c d : R) (n : Nat) (g : Nat → R) :
    contraction 1 (hamiltonian a b c d) (homogeneous n g) =
    ((List.range (n+1)).map fun j =>
      (sexticExponents.map fun h =>
        mono (h+j-1) (n+4-(h+j-1))
          ((weight 1 h n j : R)*hCoeff a b c d h*g j)).sum).sum := by
  unfold homogeneous
  rw [contraction_sum_right]
  simp only [List.map_map, Function.comp_def]
  congr 1
  apply List.map_congr_left
  intro j hj
  unfold hamiltonian
  rw [contraction_sum_left]
  simp only [List.map_map, Function.comp_def]
  congr 1
  apply List.map_congr_left
  intro h hh
  have hj' : j ≤ n := by exact Nat.le_of_lt_succ (List.mem_range.mp hj)
  have hh' : 1 ≤ h ∧ h ≤ 6 := by
    simp [sexticExponents] at hh
    rcases hh with rfl | rfl | rfl | rfl | rfl <;> omega
  exact poisson_mono h n j hh'.1 hh'.2 hj' _ _

/-- The dynamic tensor row is the coefficient after the actual Poisson iterate. -/
theorem dynamic_row_eq_coefficient (a b c d : R) (n k u v : Nat) (g : Nat → R)
    (hd : inDegree n ⟨true,k,u,v⟩) :
    rowValue a b c d n ⟨true,k,u,v⟩ g =
      coeff (exponent u v) (gate a b c d n ⟨true,k,u,v⟩ g) := by
  unfold rowValue rowTerms
  simp only [hd, not_true_eq_false, ↓reduceIte]
  rw [sum_filter_scalar]
  simp only [sum_flatMap, List.map_map, Function.comp_def,
    Option.map_some, Option.getD_some, Int.cast_mul]
  unfold gate
  simp only [↓reduceIte]
  rw [poisson_homogeneous, contraction_sum_right, coeff_list_sum]
  simp only [List.map_map, Function.comp_def]
  congr 1
  apply List.map_congr_left
  intro j hj
  unfold hamiltonian
  rw [contraction_sum_left, coeff_list_sum]
  simp only [List.map_map, Function.comp_def]
  congr 1
  apply List.map_congr_left
  intro i hi
  rw [contraction_sum_right, coeff_list_sum]
  simp only [List.map_map, Function.comp_def, contraction_mono_coeff]
  congr 1
  apply List.map_congr_left
  intro h hh
  change (weight 1 h n j : R) * (monomialRow k u v i (n+4) (h+j-1) : R) *
      hCoeff a b c d i * hCoeff a b c d h * g j = _
  ring

/-- In supported homogeneous degree, rowValue is a coefficient of the actual
gate for either iterate depth. -/
theorem row_eq_coefficient (a b c d : R) (n : Nat) (r : Row) (g : Nat → R)
    (hd : inDegree n r) :
    rowValue a b c d n r g = coeff (exponent r.qPower r.pPower) (gate a b c d n r g) := by
  rcases r with ⟨depth,k,u,v⟩
  cases depth
  · exact static_row_eq_coefficient a b c d n k u v g hd
  · exact dynamic_row_eq_coefficient a b c d n k u v g hd

/-- Passing the four genuine differential gates implies the checked coefficient
kernel.  Coefficients outside homogeneous support are handled by Model.lean. -/
theorem isKernel_of_differential_gates (a b c d : R) (n : Nat) (g : Nat → R)
    (h : ∀ r : Row, (r.order = 3 ∨ r.order = 5) → gate a b c d n r g = 0) :
    IsKernel a b c d n g := by
  intro r hk
  by_cases hd : inDegree n r
  · rw [row_eq_coefficient a b c d n r g hd, h r hk]
    simp
  · exact rowValue_outside_degree a b c d n r g hd



theorem homogeneous_congr (n : Nat) (g f : Nat → R) (h : ∀ j ≤ n, g j = f j) :
    homogeneous n g = homogeneous n f := by
  unfold homogeneous
  congr 1
  apply List.map_congr_left
  intro j hj
  rw [h j (Nat.le_of_lt_succ (List.mem_range.mp hj))]

@[simp] theorem homogeneous_zero (n : Nat) : homogeneous n (fun _ => (0 : R)) = 0 := by
  simp [homogeneous]

theorem homogeneous_hCoeff (a b c d t : R) :
    homogeneous 6 (fun j => hCoeff a b c d j * t) = C t * hamiltonian a b c d := by
  norm_num [homogeneous, hamiltonian, sexticExponents, hCoeff, List.range_succ,
    mul_add, C_mul_mono]
  simp only [mul_comm]



/-- The row-independent four-gate predicate supplies the actual gate hypothesis. -/
theorem gates_of_firstRefinement (a b c d : R) (n : Nat) (g : Nat → R)
    (h : FirstRefinement (hamiltonian a b c d) (homogeneous n g)) :
    ∀ r : Row, (r.order = 3 ∨ r.order = 5) → gate a b c d n r g = 0 := by
  intro r hk
  rcases r with ⟨depth,k,u,v⟩
  change k = 3 ∨ k = 5 at hk
  cases depth <;> rcases hk with rfl | rfl
  · exact h.1
  · exact h.2.1
  · exact h.2.2.1
  · exact h.2.2.2

theorem isKernel_of_firstRefinement (a b c d : R) (n : Nat) (g : Nat → R)
    (h : FirstRefinement (hamiltonian a b c d) (homogeneous n g)) :
    IsKernel a b c d n g :=
  isKernel_of_differential_gates a b c d n g (gates_of_firstRefinement a b c d n g h)

end SexticC3.Differential
