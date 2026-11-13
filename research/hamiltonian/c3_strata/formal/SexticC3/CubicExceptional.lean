import SexticC3.SimpleRootChart

/-! Differential identities for the sixfold-leading Hamiltonian with a cubic
perturbation. The parameter field may be any field of characteristic zero. -/

noncomputable section

namespace SexticC3.CubicExceptional

open MvPolynomial Differential

variable {K : Type*} [Field K]

def cubicHamiltonian (u v w x : K) : Poly (R := K) :=
  mono 6 0 1 + mono 3 0 u + mono 2 1 v + mono 1 2 w + mono 0 3 x

def delta (v w x : K) : K := 3 * x * v - w^2

private theorem mono_add_same (i j : ℕ) (a b : K) :
    mono i j (a + b) = mono i j a + mono i j b :=
  map_add (monomial (exponent i j)) a b

private theorem mono_neg (i j : ℕ) (a : K) : mono i j (-a) = -mono i j a :=
  map_neg (monomial (exponent i j)) a


private theorem poisson_q (u v w x : K) :
    contraction 1 (cubicHamiltonian u v w x) (mono 1 0 1) =
      mono 2 0 (-v) + mono 1 1 (-2*w) + mono 0 2 (-3*x) := by
  norm_num [cubicHamiltonian, contraction, List.range_succ, mixed_add,
    mixed_mono, falling, add_mul, mul_add, map_add, ← mono_neg, ← mono_add_same]
  congr 1 <;> ring_nf

private theorem poisson_q_squared (u v w x : K) :
    contraction 1 (cubicHamiltonian u v w x) (mono 2 0 1) =
      mono 3 0 (-2*v) + mono 2 1 (-4*w) + mono 1 2 (-6*x) := by
  norm_num [cubicHamiltonian, contraction, List.range_succ, mixed_add,
    mixed_mono, falling, add_mul, mul_add, map_add, ← mono_neg, ← mono_add_same]
  congr 1 <;> ring_nf

/-- The third contraction on the first Poisson iterate of q² is the
constant polynomial 48(3xv−w²), including on the boundary x = 0. -/
theorem q_squared_first_defect (u v w x : K) :
    contraction 3 (cubicHamiltonian u v w x)
      (contraction 1 (cubicHamiltonian u v w x) (mono 2 0 1)) =
      C (48 * delta v w x) := by
  rw [poisson_q_squared]
  norm_num [cubicHamiltonian, contraction, List.range_succ, mixed_add, Nat.choose,
    mixed_mono, falling, add_mul, mul_add, ← mono_neg, ← mono_add_same]
  have hC (a : K) : mono 0 0 a = C a := by
    simp only [mono, exponent, Finsupp.single_zero, zero_add, C_apply]
  simp only [hC]
  rw [← map_ofNat (C : K →+* Poly (R := K)) 3]
  simp only [← map_mul, ← map_add, ← map_neg]
  exact congrArg (C : K →+* Poly (R := K)) (by unfold delta; ring)

variable [CharZero K]

/-- The differential first refinement contains q² exactly on Δ = 0. -/
theorem q_squared_firstRefinement_iff (u v w x : K) :
    FirstRefinement (cubicHamiltonian u v w x) (mono 2 0 1) ↔ delta v w x = 0 := by
  have h48 : (48 : K) ≠ 0 := by norm_num
  simp only [FirstRefinement, q_squared_first_defect]
  have gates : contraction 3 (cubicHamiltonian u v w x) (mono 2 0 1) = 0 ∧
      contraction 5 (cubicHamiltonian u v w x) (mono 2 0 1) = 0 ∧
      contraction 5 (cubicHamiltonian u v w x)
        (contraction 1 (cubicHamiltonian u v w x) (mono 2 0 1)) = 0 := by
    rw [poisson_q_squared]
    norm_num [cubicHamiltonian, contraction, List.range_succ, mixed_add, Nat.choose,
      mixed_mono, falling, add_mul, mul_add]
  simp [gates.1, gates.2.1, gates.2.2, C_eq_zero, h48]

theorem q_firstRefinement (u v w x : K) :
    FirstRefinement (cubicHamiltonian u v w x) (mono 1 0 1) := by
  rw [FirstRefinement, poisson_q]
  norm_num [cubicHamiltonian, contraction, List.range_succ, mixed_add, Nat.choose,
    mixed_mono, falling, add_mul, mul_add]

/-- The fifth static gate is exactly a scalar times the fifth p derivative. -/
theorem static_fifth_gate (u v w x : K) (G : Poly (R := K)) :
    contraction 5 (cubicHamiltonian u v w x) G = C (720 : K) * X false * mixed 0 5 G := by
  norm_num [cubicHamiltonian, contraction, List.range_succ, mixed_add, Nat.choose,
    mixed_mono, falling, add_mul, mul_add]
  norm_num [mono_eq_X]

/-- The third static gate, as a differential equation on the entire polynomial ring. -/
theorem static_third_gate (u v w x : K) (G : Poly (R := K)) :
    contraction 3 (cubicHamiltonian u v w x) G =
      C 6 * ((C 20 * X false^3 + C u) * mixed 0 3 G -
        C v * mixed 1 2 G + C w * mixed 2 1 G - C x * mixed 3 0 G) := by
  norm_num [cubicHamiltonian, contraction, List.range_succ, mixed_add, Nat.choose,
    mixed_mono, falling, add_mul, mul_add]
  norm_num [mono_eq_X, map_mul, map_ofNat]
  ring

/-- The fifth gate forces every monomial in a static partner to have p-degree ≤ 4. -/
theorem static_p_degree_bound (u v w x : K) (G : Poly (R := K))
    (h : contraction 5 (cubicHamiltonian u v w x) G = 0)
    {i j : ℕ} (hj : 5 ≤ j) : coeff (exponent i j) G = 0 := by
  have h720 : (720 : K) ≠ 0 := by norm_num
  have hd : mixed 0 5 G = 0 := by
    simpa [static_fifth_gate, mul_eq_zero, h720, X_ne_zero] using h
  have pderiv_coeff (F : Poly (R := K)) (n : ℕ) :
      coeff (exponent i n) (pderiv true F) =
        coeff (exponent i (n+1)) F * (n+1 : ℕ) := by
    induction F using MvPolynomial.induction_on' with
    | monomial m c =>
      rw [← exponent_eta m]
      change coeff (exponent i n) (pderiv true (mono (m false) (m true) c)) =
        coeff (exponent i (n+1)) (mono (m false) (m true) c) * (n+1 : ℕ)
      rw [pderiv_p_mono]
      simp only [coeff_mono]
      by_cases hz : m true = 0
      · simp [hz]
      · have he : m true - 1 = n ↔ m true = n + 1 := by omega
        simp only [he]
        split_ifs with h
        · rw [h.2, Nat.cast_add, Nat.cast_one]
        · simp
    | add F U ihF ihU =>
      simp [ihF, ihU, add_mul]
  have h_iter (r n : ℕ) :
      coeff (exponent i n) ((pderiv true)^[r] G) = 0 →
        coeff (exponent i (n+r)) G = 0 := by
    induction r generalizing n with
    | zero => simp
    | succ r ih =>
      rw [Function.iterate_succ_apply', pderiv_coeff]
      intro hzero
      have hn : (↑(n+1) : K) ≠ 0 := Nat.cast_ne_zero.mpr (Nat.succ_ne_zero n)
      simpa [Nat.add_assoc, Nat.add_comm 1 r] using
        ih (n+1) ((mul_eq_zero.mp hzero).resolve_right hn)
  have hz := congrArg (coeff (exponent i (j-5))) hd
  simpa [Nat.sub_add_cancel hj] using h_iter 5 (j-5) (by simpa [mixed] using hz)

/-- Substituting p ↦ p − s q, with s = w/(3x), removes the qp² term. -/
theorem shear_normal_form (u v w x : K) (hx : x ≠ 0) :
    linearSub 1 0 (-(w / (3*x))) 1 (cubicHamiltonian u v w x) =
      cubicHamiltonian (u - v*w/(3*x) + 2*w^3/(27*x^2)) (delta v w x / (3*x)) 0 x := by
  have h3x : (3 : K) * x ≠ 0 := mul_ne_zero (by norm_num) hx
  have h27x : (27 : K) * x^2 ≠ 0 := mul_ne_zero (by norm_num) (pow_ne_zero _ hx)
  let s := w / (3*x)
  have hs : 3*x*s = w := by
    simpa [s, mul_comm] using (div_mul_cancel₀ w h3x)
  have hv : delta v w x / (3*x) = v - w*s := by
    dsimp [delta, s]
    field_simp
    ring
  have hu : u - v*w/(3*x) + 2*w^3/(27*x^2) = u - v*s + w*s^2 - x*s^3 := by
    dsimp [s]
    field_simp
    ring
  have hv' : v - w*s = v - 2*w*s + 3*x*s^2 := by
    linear_combination -s * hs
  rw [hu, hv, hv']
  change linearSub 1 0 (-s) 1 _ = _
  simp only [cubicHamiltonian, mono_eq_X, map_add, map_mul, map_pow, linearSub_C,
    linearSub_X_false, linearSub_X_true, map_zero, map_one, zero_mul, one_mul,
    add_zero, pow_zero, mul_one]
  simp only [map_sub, map_add, map_mul, map_pow, map_neg, map_ofNat]
  have hw := congrArg (C : K →+* Poly (R := K)) hs.symm
  rw [hw]
  simp only [map_mul, map_ofNat]
  ring

/-- The normalizing shear preserves the vanishing of every iterated gate
used for the first refinement, second refinement and persistent core. -/
theorem shear_iterated_gate_zero_iff (s : K) (F G : Poly (R := K))
    (i k : ℕ) (hk : k ≤ 5) :
    contraction k (linearSub 1 0 (-s) 1 F)
      ((contraction 1 (linearSub 1 0 (-s) 1 F))^[i] (linearSub 1 0 (-s) 1 G)) = 0 ↔
    contraction k F ((contraction 1 F)^[i] G) = 0 := by
  simpa using iterated_gate_zero_iff 1 0 (-s) 1 1 F G i k hk (by simp) one_ne_zero

end SexticC3.CubicExceptional
