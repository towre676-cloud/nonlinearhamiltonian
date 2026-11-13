import SexticC3.NonlinearBQuadraticTail

noncomputable section
namespace SexticC3.NonlinearB
open MvPolynomial Differential
variable {K : Type*} [Field K] [CharZero K]

theorem quadratic_static_p2_low_bound (c : Parameters K) (hb3 : c.b3=0)
    (hb2 : c.b2≠0) (hh : c.h6≠0) (G : Poly (R := K)) (h : Static (H c) G)
    (forcing : ∀ i, cf G i 4=0) : ∀ i, 3 ≤ i → cf G i 2=0 := by
  have hp := quadratic_static_momentum_bound c hb3 hh G h
  have higher (i k : ℕ) (hk : 5 ≤ k) : cf G i k=0 := at_above_p_degree G i k (by omega)
  apply column_elimination G 2 3
  intro n hn htop
  obtain ⟨m,hm⟩ := Nat.exists_eq_add_of_le hn
  have hn' : n=m+3 := by omega
  subst n
  have hx : cf G (m+4) 2=0 := htop _ (by omega)
  have hz := congrArg (fun F => cf F (m+2) 1) h.1
  rw [third_gate] at hz
  simp only [add_mul,cf_add,cf_sub,cf_zero,at_mono_mul,mixed,
    Function.iterate_succ_apply',Function.iterate_zero_apply,
    at_q_derivative,at_p_derivative,Nat.add_assoc] at hz
  simp (disch := omega) [hb3,higher,hx,forcing,Nat.add_sub_assoc,Nat.add_assoc] at hz
  have hm1 : (m:K)+1≠0 := by exact_mod_cast (show m+1≠0 by omega)
  have hmn : (m:K)+3≠0 := by exact_mod_cast (show m+3≠0 by omega)
  have he : (24*c.b2*((m:K)+3)*((m:K)+1))*cf G (m+3) 2=0 := by
    linear_combination hz
  simpa [Nat.add_comm] using (mul_eq_zero.mp he).resolve_left
    (mul_ne_zero (mul_ne_zero (mul_ne_zero (by norm_num) hb2) hmn) hm1)

theorem quadratic_static_p1_low_bound (c : Parameters K) (hb3 : c.b3=0)
    (hb2 : c.b2≠0) (hh : c.h6≠0) (G : Poly (R := K)) (h : Static (H c) G)
    (forcing : ∀ i, cf G i 3=0) : ∀ i, 2 ≤ i → cf G i 1=0 := by
  have hp := quadratic_static_momentum_bound c hb3 hh G h
  have higher (i k : ℕ) (hk : 5 ≤ k) : cf G i k=0 := at_above_p_degree G i k (by omega)
  apply column_elimination G 1 2
  intro n hn htop
  obtain ⟨m,hm⟩ := Nat.exists_eq_add_of_le hn
  have hn' : n=m+2 := by omega
  subst n
  have hx : cf G (m+3) 1=0 := htop _ (by omega)
  have hz := congrArg (fun F => cf F (m+1) 0) h.1
  rw [third_gate] at hz
  simp only [add_mul,cf_add,cf_sub,cf_zero,at_mono_mul,mixed,
    Function.iterate_succ_apply',Function.iterate_zero_apply,
    at_q_derivative,at_p_derivative,Nat.add_assoc] at hz
  simp (disch := omega) [hb3,higher,hx,forcing,Nat.add_sub_assoc,Nat.add_assoc] at hz
  have hm1 : (m:K)+1≠0 := by exact_mod_cast (show m+1≠0 by omega)
  have hmn : (m:K)+2≠0 := by exact_mod_cast (show m+2≠0 by omega)
  simpa [hb2,hm1,hmn,Nat.add_comm] using hz

theorem quadratic_static_p4_top_zero (c : Parameters K) (hb3 : c.b3=0)
    (hb2 : c.b2≠0) (hh : c.h6≠0) (G : Poly (R := K)) (h : Static (H c) G)
    (ht : cf G 4 4=0) : ∀ i, 1 ≤ i → cf G i 4=0 := by
  have hp := quadratic_static_momentum_bound c hb3 hh G h
  have higher (i k : ℕ) (hk : 5 ≤ k) : cf G i k=0 := at_above_p_degree G i k (by omega)
  have high := quadratic_static_p4_q_bound c hb3 hb2 hh G h
  apply column_elimination G 4 1
  intro n hn htop
  by_cases hnHigh : 5 ≤ n
  · exact high n hnHigh
  by_cases hnTop : n=4
  · simpa [hnTop] using ht
  have hnSmall : n<4 := by omega
  have hx := htop (n+1) (by omega)
  have hz := congrArg (fun F => cf F (n-1) 3) h.1
  rw [third_gate] at hz
  simp only [add_mul,cf_add,cf_sub,cf_zero,at_mono_mul,mixed,
    Function.iterate_succ_apply',Function.iterate_zero_apply,
    at_q_derivative,at_p_derivative] at hz
  interval_cases n <;> norm_num [hb3,higher,hx,hb2] at hz ⊢ <;>
    ring_nf at hz <;> simpa [mul_eq_zero,hb2] using hz

theorem quadratic_static_p3_top_zero (c : Parameters K) (hb3 : c.b3=0)
    (hb2 : c.b2≠0) (hh : c.h6≠0) (G : Poly (R := K)) (h : Static (H c) G)
    (ht : cf G 3 3=0) : ∀ i, 1 ≤ i → cf G i 3=0 := by
  have hp := quadratic_static_momentum_bound c hb3 hh G h
  have higher (i k : ℕ) (hk : 5 ≤ k) : cf G i k=0 := at_above_p_degree G i k (by omega)
  have high := quadratic_static_p3_q_bound c hb3 hb2 hh G h
  apply column_elimination G 3 1
  intro n hn htop
  by_cases hnHigh : 4 ≤ n
  · exact high n hnHigh
  by_cases hnTop : n=3
  · simpa [hnTop] using ht
  have hnSmall : n<3 := by omega
  have hx := htop (n+1) (by omega)
  have hz := congrArg (fun F => cf F (n-1) 2) h.1
  rw [third_gate] at hz
  simp only [add_mul,cf_add,cf_sub,cf_zero,at_mono_mul,mixed,
    Function.iterate_succ_apply',Function.iterate_zero_apply,
    at_q_derivative,at_p_derivative] at hz
  interval_cases n <;> norm_num [hb3,higher,hx,hb2] at hz ⊢ <;>
    ring_nf at hz <;> simpa [mul_eq_zero,hb2] using hz

theorem quadratic_first_p4_zero (c : Parameters K) (hb3 : c.b3=0)
    (hb2 : c.b2≠0) (hh : c.h6≠0) (G : Poly (R := K))
    (h : FirstRefinement (H c) G) : ∀ i, cf G i 4=0 := by
  have hs : Static (H c) G := ⟨h.1,h.2.1⟩
  have hd : Static (H c) (contraction 1 (H c) G) := ⟨h.2.2.1,h.2.2.2⟩
  have hp := quadratic_static_momentum_bound c hb3 hh G hs
  have hdp := quadratic_static_momentum_bound c hb3 hh _ hd
  have higher (i j : ℕ) (hj : 5 ≤ j) : cf G i j=0 := at_above_p_degree G i j (by omega)
  have h4 := quadratic_static_p4_q_bound c hb3 hb2 hh G hs
  have h3 := quadratic_static_p3_q_bound c hb3 hb2 hh G hs
  have h2 := quadratic_static_p2_q_bound c hb3 hb2 hh G hs
  have hd3 := quadratic_static_p3_q_bound c hb3 hb2 hh _ hd
  have e1 := congrArg (fun F => cf F 7 1) hs.1
  rw [third_gate] at e1
  simp only [add_mul,cf_add,cf_sub,cf_zero,at_mono_mul,mixed,
    Function.iterate_succ_apply',Function.iterate_zero_apply,
    at_q_derivative,at_p_derivative] at e1
  simp (disch := omega) [hb3,h4,h2] at e1
  have e2 := hd3 9 (by omega)
  rw [first_gate] at e2
  simp only [add_mul,cf_add,cf_sub,cf_zero,at_mono_mul,mixed,
    Function.iterate_succ_apply',Function.iterate_zero_apply,
    at_q_derivative,at_p_derivative] at e2
  simp (disch := omega) [hb3,h4,h3,h2,higher] at e2
  have ht : cf G 4 4=0 := by
    have hz : 54*c.h6*cf G 4 4=0 := by linear_combination e2+(1/96:K)*e1
    exact (mul_eq_zero.mp hz).resolve_left (mul_ne_zero (by norm_num) hh)
  have high := quadratic_static_p4_top_zero c hb3 hb2 hh G hs ht
  have e0 : cf (contraction 1 (H c) G) 1 5=0 := at_above_p_degree _ 1 5 (by omega)
  rw [first_gate] at e0
  simp only [add_mul,cf_add,cf_sub,cf_zero,at_mono_mul,mixed,
    Function.iterate_succ_apply',Function.iterate_zero_apply,
    at_q_derivative,at_p_derivative] at e0
  simp (disch := omega) [hb3,high,higher,hb2] at e0
  intro i
  by_cases hi : i=0
  · simpa [hi] using e0
  · exact high i (by omega)

theorem quadratic_first_D_p4_top_zero (c : Parameters K) (hb3 : c.b3=0)
    (hb2 : c.b2≠0) (hh : c.h6≠0) (G : Poly (R := K))
    (h : FirstRefinement (H c) G) : cf (contraction 1 (H c) G) 4 4=0 := by
  have hs : Static (H c) G := ⟨h.1,h.2.1⟩
  have hp := quadratic_static_momentum_bound c hb3 hh G hs
  have higher (i j : ℕ) (hj : 5 ≤ j) : cf G i j=0 := at_above_p_degree G i j (by omega)
  have h4 := quadratic_first_p4_zero c hb3 hb2 hh G h
  have h3 := quadratic_static_p3_q_bound c hb3 hb2 hh G hs
  rw [first_gate]
  simp only [add_mul,cf_add,cf_sub,cf_zero,at_mono_mul,mixed,
    Function.iterate_succ_apply',Function.iterate_zero_apply,
    at_q_derivative,at_p_derivative]
  simp (disch := omega) [hb3,h4,h3,higher]

theorem quadratic_first_p3_zero (c : Parameters K) (hb3 : c.b3=0)
    (hb2 : c.b2≠0) (hh : c.h6≠0) (G : Poly (R := K))
    (h : FirstRefinement (H c) G) : ∀ i, cf G i 3=0 := by
  have hs : Static (H c) G := ⟨h.1,h.2.1⟩
  have hd : Static (H c) (contraction 1 (H c) G) := ⟨h.2.2.1,h.2.2.2⟩
  have hp := quadratic_static_momentum_bound c hb3 hh G hs
  have higher (i j : ℕ) (hj : 5 ≤ j) : cf G i j=0 := at_above_p_degree G i j (by omega)
  have h4 := quadratic_first_p4_zero c hb3 hb2 hh G h
  have h3 := quadratic_static_p3_q_bound c hb3 hb2 hh G hs
  have h2 := quadratic_static_p2_low_bound c hb3 hb2 hh G hs h4
  have h1 := quadratic_static_p1_q_bound c hb3 hb2 hh G hs
  have hd4t := quadratic_first_D_p4_top_zero c hb3 hb2 hh G h
  have hd4 := quadratic_static_p4_top_zero c hb3 hb2 hh _ hd hd4t
  have hd2 := quadratic_static_p2_q_bound c hb3 hb2 hh _ hd
  have e1 := congrArg (fun F => cf F 6 0) hs.1
  rw [third_gate] at e1
  simp only [add_mul,cf_add,cf_sub,cf_zero,at_mono_mul,mixed,
    Function.iterate_succ_apply',Function.iterate_zero_apply,
    at_q_derivative,at_p_derivative] at e1
  simp (disch := omega) [hb3,h3,h1] at e1
  have e2 := congrArg (fun F => cf F 7 1) hd.1
  rw [third_gate] at e2
  simp only [add_mul,cf_add,cf_sub,cf_zero,at_mono_mul,mixed,
    Function.iterate_succ_apply',Function.iterate_zero_apply,
    at_q_derivative,at_p_derivative] at e2
  simp (disch := omega) [hb3,hd4,hd2,hb2] at e2
  replace e2 : cf (contraction 1 (H c) G) 8 2=0 := by
    have hz : 1152*c.b2*cf (contraction 1 (H c) G) 8 2=0 := by linear_combination e2
    exact (mul_eq_zero.mp hz).resolve_left (mul_ne_zero (by norm_num) hb2)
  rw [first_gate] at e2
  simp only [add_mul,cf_add,cf_sub,cf_zero,at_mono_mul,mixed,
    Function.iterate_succ_apply',Function.iterate_zero_apply,
    at_q_derivative,at_p_derivative] at e2
  simp (disch := omega) [hb3,h4,h3,h2,h1,higher] at e2
  have ht : cf G 3 3=0 := by
    have hz : 246*c.h6*cf G 3 3=0 := by linear_combination 7*e2+(1/6:K)*e1
    exact (mul_eq_zero.mp hz).resolve_left (mul_ne_zero (by norm_num) hh)
  have high := quadratic_static_p3_top_zero c hb3 hb2 hh G hs ht
  have e0 := hd4 1 (by omega)
  rw [first_gate] at e0
  simp only [add_mul,cf_add,cf_sub,cf_zero,at_mono_mul,mixed,
    Function.iterate_succ_apply',Function.iterate_zero_apply,
    at_q_derivative,at_p_derivative] at e0
  simp (disch := omega) [hb3,h4,high,higher,hb2] at e0
  intro i
  by_cases hi : i=0
  · simpa [hi] using e0
  · exact high i (by omega)

theorem quadratic_first_momentum_bound (c : Parameters K) (hb3 : c.b3=0)
    (hb2 : c.b2≠0) (hh : c.h6≠0) (G : Poly (R := K))
    (h : FirstRefinement (H c) G) : G.degreeOf true ≤ 2 := by
  have hp := quadratic_static_momentum_bound c hb3 hh G ⟨h.1,h.2.1⟩
  have h4 := quadratic_first_p4_zero c hb3 hb2 hh G h
  have h3 := quadratic_first_p3_zero c hb3 hb2 hh G h
  rw [degreeOf_le_iff]
  intro m hm
  have hmle := monomial_le_degreeOf true hm
  have hmne := mem_support_iff.mp hm
  by_contra hn
  have hmj : m true=3 ∨ m true=4 := by omega
  apply hmne
  rw [← exponent_eta m]
  rcases hmj with hj | hj
  · simpa only [hj] using h3 (m false)
  · simpa only [hj] using h4 (m false)

end SexticC3.NonlinearB
