import SexticC3.NonlinearB
import SexticC3.NonlinearBCoefficients

noncomputable section
namespace SexticC3.NonlinearB
open MvPolynomial Differential
variable {K : Type*} [Field K] [CharZero K]

theorem cubic_top_affine (c : Parameters K) (hb : c.b3≠0)
    (G : Poly (R := K)) (n : ℕ)
    (htop : ∀ i j, n+3<j → cf G i j=0)
    (h5 : contraction 5 (H c) G=0) (i : ℕ) : cf G (i+2) (n+3)=0 := by
  have hz := congrArg (fun F => cf F i n) h5
  rw [fifth_gate] at hz
  simp only [add_mul, cf_add, cf_zero, at_mono_mul, mixed,
    Function.iterate_succ_apply', Function.iterate_zero_apply,
    at_q_derivative, at_p_derivative, Nat.add_assoc,
    Nat.sub_zero, Nat.zero_le, and_true, true_and, if_true] at hz
  have higher (k : ℕ) : cf G k (n+5)=0 := htop k (n+5) (by omega)
  simp only [higher, mul_zero, ite_self, zero_add] at hz
  have hi1 : ((i+1 : ℕ) : K)≠0 := Nat.cast_ne_zero.mpr (by omega)
  have hi2 : ((i+2 : ℕ) : K)≠0 := Nat.cast_ne_zero.mpr (by omega)
  have hn1 : ((n+1 : ℕ) : K)≠0 := Nat.cast_ne_zero.mpr (by omega)
  have hn2 : ((n+2 : ℕ) : K)≠0 := Nat.cast_ne_zero.mpr (by omega)
  have hn3 : ((n+3 : ℕ) : K)≠0 := Nat.cast_ne_zero.mpr (by omega)
  norm_cast at hi1 hi2 hn1 hn2 hn3
  have hi1' : (i:K)+1≠0 := by exact_mod_cast (show i+1≠0 by omega)
  have hi2' : (i:K)+2≠0 := by exact_mod_cast (show i+2≠0 by omega)
  have hn1' : (n:K)+1≠0 := by exact_mod_cast (show n+1≠0 by omega)
  have hn2' : (n:K)+2≠0 := by exact_mod_cast (show n+2≠0 by omega)
  have hn3' : (n:K)+3≠0 := by exact_mod_cast (show n+3≠0 by omega)
  simpa [mul_eq_zero, hb, hi1', hi2', hn1', hn2', hn3'] using hz

theorem cubic_top_equations (c : Parameters K) (hb : c.b3≠0)
    (G : Poly (R := K)) (n : ℕ)
    (htop : ∀ i j, n+3<j → cf G i j=0)
    (h : Static (H c) G) :
    ((n:K)-5)*cf G 1 (n+3)=0 ∧
      ((n:K)+1)*c.b3*cf G 0 (n+3)-2*c.b2*cf G 1 (n+3)=0 := by
  have high (i : ℕ) := cubic_top_affine c hb G n htop h.2 i
  have higher (i : ℕ) : cf G i (n+5)=0 := htop i (n+5) (by omega)
  have hz0 := congrArg (fun F => cf F 0 (n+2)) h.1
  have hz1 := congrArg (fun F => cf F 1 (n+2)) h.1
  rw [third_gate] at hz0 hz1
  simp only [add_mul, cf_add, cf_sub, cf_zero, at_mono_mul, mixed,
    Function.iterate_succ_apply', Function.iterate_zero_apply,
    at_q_derivative, at_p_derivative, Nat.add_assoc] at hz0 hz1
  have hsub1 : n+2-1=n+1 := by omega
  have hsub2 : n+2-2=n := by omega
  have hle1 : 1 ≤ n+2 := by omega
  have hle2 : 2 ≤ n+2 := by omega
  norm_num [hsub1,hsub2,hle1,hle2,higher, high 0, high 1, Nat.add_assoc] at hz0 hz1
  have hn2 : (n:K)+2≠0 := by exact_mod_cast (show n+2≠0 by omega)
  have hn3 : (n:K)+3≠0 := by exact_mod_cast (show n+3≠0 by omega)
  constructor
  · have he : (6*c.b3*((n:K)+3)*((n:K)+2))*(((n:K)-5)*cf G 1 (n+3))=0 := by
      linear_combination hz1
    exact (mul_eq_zero.mp he).resolve_left
      (mul_ne_zero (mul_ne_zero (mul_ne_zero (by norm_num) hb) hn3) hn2)
  · have he : (6*((n:K)+3)*((n:K)+2))*
        (((n:K)+1)*c.b3*cf G 0 (n+3)-2*c.b2*cf G 1 (n+3))=0 := by
      linear_combination hz0
    exact (mul_eq_zero.mp he).resolve_left
      (mul_ne_zero (mul_ne_zero (by norm_num) hn3) hn2)

theorem cubic_eighth_resonance_vanishes (c : Parameters K) (hb : c.b3≠0)
    (hh : c.h6≠0) (G : Poly (R := K))
    (htop : ∀ i j, 8<j → cf G i j=0) (h : Static (H c) G) : cf G 1 8=0 := by
  have high (i : ℕ) : cf G (i+2) 8=0 := cubic_top_affine c hb G 5 htop h.2 i
  have h65 : cf G 5 6=0 := by
    have hz := congrArg (fun F => cf F 3 3) h.2
    rw [fifth_gate] at hz
    simp only [add_mul, cf_add, cf_zero, at_mono_mul, mixed,
      Function.iterate_succ_apply', Function.iterate_zero_apply,
      at_q_derivative, at_p_derivative] at hz
    norm_num [high 0, high 1, hb] at hz
    exact hz
  have h66 : cf G 6 6=0 := by
    have hz := congrArg (fun F => cf F 4 3) h.2
    rw [fifth_gate] at hz
    simp only [add_mul, cf_add, cf_zero, at_mono_mul, mixed,
      Function.iterate_succ_apply', Function.iterate_zero_apply,
      at_q_derivative, at_p_derivative] at hz
    norm_num [high 1, high 2, hb] at hz
    exact hz
  have h64 := congrArg (fun F => cf F 2 3) h.2
  rw [fifth_gate] at h64
  simp only [add_mul, cf_add, cf_zero, at_mono_mul, mixed,
    Function.iterate_succ_apply', Function.iterate_zero_apply,
    at_q_derivative, at_p_derivative] at h64
  norm_num [high 0] at h64
  have h34 := congrArg (fun F => cf F 4 5) h.1
  rw [third_gate] at h34
  simp only [add_mul, cf_add, cf_sub, cf_zero, at_mono_mul, mixed,
    Function.iterate_succ_apply', Function.iterate_zero_apply,
    at_q_derivative, at_p_derivative] at h34
  norm_num [high 0, high 1, high 2, h65, h66] at h34
  have hz : 104832*c.h6*cf G 1 8=0 := by
    linear_combination h34 + (1/75 : K)*h64
  exact (mul_eq_zero.mp hz).resolve_left (mul_ne_zero (by norm_num) hh)

/-- No static observable in the cubic-B family has momentum degree above two.
The proof uses the finite support of an arbitrary polynomial, not a degree window. -/
theorem cubic_static_momentum_bound (c : Parameters K) (hb : c.b3≠0)
    (hh : c.h6≠0) (G : Poly (R := K)) (h : Static (H c) G) :
    G.degreeOf true ≤ 2 := by
  by_contra hn
  have hn3 : 3 ≤ G.degreeOf true := by omega
  obtain ⟨n,he⟩ := Nat.exists_eq_add_of_le hn3
  have he' : G.degreeOf true=n+3 := by omega
  have htop (i j : ℕ) (hj : n+3<j) : cf G i j=0 :=
    at_above_p_degree G i j (by omega)
  have high (i : ℕ) := cubic_top_affine c hb G n htop h.2 i
  obtain ⟨hu,hv⟩ := cubic_top_equations c hb G n htop h
  have hu0 : cf G 1 (n+3)=0 := by
    by_cases hn5 : n=5
    · subst n
      exact cubic_eighth_resonance_vanishes c hb hh G htop h
    · have hcast : (n:K)-5≠0 := by
        intro hz
        have heq : (n:K)=5 := sub_eq_zero.mp hz
        have : n=5 := by exact_mod_cast heq
        exact hn5 this
      exact (mul_eq_zero.mp hu).resolve_left hcast
  have hv0 : cf G 0 (n+3)=0 := by
    rw [hu0, mul_zero, sub_zero] at hv
    have hn1 : (n:K)+1≠0 := by exact_mod_cast (show n+1≠0 by omega)
    exact (mul_eq_zero.mp hv).resolve_left (mul_ne_zero hn1 hb)
  have hless : G.degreeOf true < n+3 := by
    rw [degreeOf_lt_iff (by omega)]
    intro m hm
    have hmle := monomial_le_degreeOf true hm
    rw [he'] at hmle
    by_contra hnot
    have hp : m true=n+3 := by omega
    have hmne : coeff m G≠0 := mem_support_iff.mp hm
    apply hmne
    rw [← exponent_eta m, hp]
    change cf G (m false) (n+3)=0
    rcases m false with _ | i
    · exact hv0
    · rcases i with _ | i
      · exact hu0
      · simpa [Nat.add_assoc] using high i
  omega

end SexticC3.NonlinearB
