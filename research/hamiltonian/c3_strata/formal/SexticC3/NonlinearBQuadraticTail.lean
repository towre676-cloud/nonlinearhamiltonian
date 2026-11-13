import SexticC3.NonlinearB
import SexticC3.NonlinearBCoefficients

noncomputable section
namespace SexticC3.NonlinearB
open MvPolynomial Differential
variable {K : Type*} [Field K] [CharZero K]

theorem quadratic_static_momentum_bound (c : Parameters K) (hb : c.b3=0)
    (hh : c.h6≠0) (G : Poly (R := K)) (h : Static (H c) G) :
    G.degreeOf true ≤ 4 := by
  have hf : (mono 1 0 (720*c.h6)+mono 0 0 (120*c.h5) : Poly (R := K))≠0 := by
    intro hz
    have he := congrArg (fun F => cf F 1 0) hz
    norm_num [cf,coeff_add,coeff_mono,hh] at he
  have hd : mixed 0 5 G=0 := by
    have hz := h.2
    rw [fifth_gate,hb] at hz
    simp only [mul_zero,mono_zero,zero_mul,add_zero] at hz
    exact (mul_eq_zero.mp hz).resolve_left hf
  have hg (i n : ℕ) : cf G i (n+5)=0 := by
    have hz := congrArg (fun F => cf F i n) hd
    simp only [mixed,Function.iterate_succ_apply',Function.iterate_zero_apply,
      at_p_derivative,cf_zero,Nat.add_assoc] at hz
    have hn1 : (n:K)+1≠0 := by exact_mod_cast (show n+1≠0 by omega)
    have hn2 : (n:K)+2≠0 := by exact_mod_cast (show n+2≠0 by omega)
    have hn3 : (n:K)+3≠0 := by exact_mod_cast (show n+3≠0 by omega)
    have hn4 : (n:K)+4≠0 := by exact_mod_cast (show n+4≠0 by omega)
    have hn5 : (n:K)+5≠0 := by exact_mod_cast (show n+5≠0 by omega)
    simpa [mul_eq_zero,hn1,hn2,hn3,hn4,hn5] using hz
  rw [degreeOf_le_iff]
  intro m hm
  by_contra hn
  have h5 : 5 ≤ m true := by omega
  have hz := hg (m false) (m true-5)
  rw [Nat.sub_add_cancel h5] at hz
  have hmne := mem_support_iff.mp hm
  apply hmne
  simpa only [cf,exponent_eta] using hz

theorem quadratic_static_p4_q_bound (c : Parameters K) (hb3 : c.b3=0)
    (hb2 : c.b2≠0) (hh : c.h6≠0) (G : Poly (R := K)) (h : Static (H c) G) :
    ∀ i, 5 ≤ i → cf G i 4=0 := by
  have hp := quadratic_static_momentum_bound c hb3 hh G h
  have higher (i k : ℕ) (hk : 5 ≤ k) : cf G i k=0 := at_above_p_degree G i k (by omega)
  apply column_elimination G 4 5
  intro n hn htop
  obtain ⟨m,hm⟩ := Nat.exists_eq_add_of_le hn
  have hn' : n=m+5 := by omega
  subst n
  have hx : cf G (m+6) 4=0 := htop _ (by omega)
  have hz := congrArg (fun F => cf F (m+4) 3) h.1
  rw [third_gate] at hz
  simp only [add_mul,cf_add,cf_sub,cf_zero,at_mono_mul,mixed,
    Function.iterate_succ_apply',Function.iterate_zero_apply,
    at_q_derivative,at_p_derivative,Nat.add_assoc] at hz
  simp (disch := omega) [hb3,higher,hx,Nat.add_sub_assoc,Nat.add_assoc] at hz
  have he : (48*c.b2*((m:K)+5)*((m:K)+1))*cf G (m+5) 4=0 := by
    linear_combination hz
  have hm1 : (m:K)+1≠0 := by exact_mod_cast (show m+1≠0 by omega)
  have hmn : (m:K)+5≠0 := by exact_mod_cast (show m+5≠0 by omega)
  simpa [Nat.add_comm] using (mul_eq_zero.mp he).resolve_left
    (mul_ne_zero (mul_ne_zero (mul_ne_zero (by norm_num) hb2) hmn) hm1)

theorem quadratic_static_p3_q_bound (c : Parameters K) (hb3 : c.b3=0)
    (hb2 : c.b2≠0) (hh : c.h6≠0) (G : Poly (R := K)) (h : Static (H c) G) :
    ∀ i, 4 ≤ i → cf G i 3=0 := by
  have hp := quadratic_static_momentum_bound c hb3 hh G h
  have higher (i k : ℕ) (hk : 5 ≤ k) : cf G i k=0 := at_above_p_degree G i k (by omega)
  apply column_elimination G 3 4
  intro n hn htop
  obtain ⟨m,hm⟩ := Nat.exists_eq_add_of_le hn
  have hn' : n=m+4 := by omega
  subst n
  have hx : cf G (m+5) 3=0 := htop _ (by omega)
  have hz := congrArg (fun F => cf F (m+3) 2) h.1
  rw [third_gate] at hz
  simp only [add_mul,cf_add,cf_sub,cf_zero,at_mono_mul,mixed,
    Function.iterate_succ_apply',Function.iterate_zero_apply,
    at_q_derivative,at_p_derivative,Nat.add_assoc] at hz
  simp (disch := omega) [hb3,higher,hx,Nat.add_sub_assoc,Nat.add_assoc] at hz
  have he : (36*c.b2*((m:K)+4)*((m:K)+1))*cf G (m+4) 3=0 := by
    linear_combination hz
  have hm1 : (m:K)+1≠0 := by exact_mod_cast (show m+1≠0 by omega)
  have hmn : (m:K)+4≠0 := by exact_mod_cast (show m+4≠0 by omega)
  simpa [Nat.add_comm] using (mul_eq_zero.mp he).resolve_left
    (mul_ne_zero (mul_ne_zero (mul_ne_zero (by norm_num) hb2) hmn) hm1)

theorem quadratic_static_p2_q_bound (c : Parameters K) (hb3 : c.b3=0)
    (hb2 : c.b2≠0) (hh : c.h6≠0) (G : Poly (R := K)) (h : Static (H c) G) :
    ∀ i, 9 ≤ i → cf G i 2=0 := by
  have hp := quadratic_static_momentum_bound c hb3 hh G h
  have higher (i k : ℕ) (hk : 5 ≤ k) : cf G i k=0 := at_above_p_degree G i k (by omega)
  have forcing := quadratic_static_p4_q_bound c hb3 hb2 hh G h
  apply column_elimination G 2 9
  intro n hn htop
  obtain ⟨m,hm⟩ := Nat.exists_eq_add_of_le hn
  have hn' : n=m+9 := by omega
  subst n
  have hx : cf G (m+10) 2=0 := htop _ (by omega)
  have hz := congrArg (fun F => cf F (m+8) 1) h.1
  rw [third_gate] at hz
  simp only [add_mul,cf_add,cf_sub,cf_zero,at_mono_mul,mixed,
    Function.iterate_succ_apply',Function.iterate_zero_apply,
    at_q_derivative,at_p_derivative,Nat.add_assoc] at hz
  simp (disch := omega) [hb3,higher,hx,forcing,Nat.add_sub_assoc,Nat.add_assoc] at hz
  have he : (24*c.b2*((m:K)+9)*((m:K)+7))*cf G (m+9) 2=0 := by
    linear_combination hz
  have hm1 : (m:K)+7≠0 := by exact_mod_cast (show m+7≠0 by omega)
  have hmn : (m:K)+9≠0 := by exact_mod_cast (show m+9≠0 by omega)
  simpa [Nat.add_comm] using (mul_eq_zero.mp he).resolve_left
    (mul_ne_zero (mul_ne_zero (mul_ne_zero (by norm_num) hb2) hmn) hm1)

theorem quadratic_static_p1_q_bound (c : Parameters K) (hb3 : c.b3=0)
    (hb2 : c.b2≠0) (hh : c.h6≠0) (G : Poly (R := K)) (h : Static (H c) G) :
    ∀ i, 8 ≤ i → cf G i 1=0 := by
  have hp := quadratic_static_momentum_bound c hb3 hh G h
  have higher (i k : ℕ) (hk : 5 ≤ k) : cf G i k=0 := at_above_p_degree G i k (by omega)
  have forcing := quadratic_static_p3_q_bound c hb3 hb2 hh G h
  apply column_elimination G 1 8
  intro n hn htop
  obtain ⟨m,hm⟩ := Nat.exists_eq_add_of_le hn
  have hn' : n=m+8 := by omega
  subst n
  have hx : cf G (m+9) 1=0 := htop _ (by omega)
  have hz := congrArg (fun F => cf F (m+7) 0) h.1
  rw [third_gate] at hz
  simp only [add_mul,cf_add,cf_sub,cf_zero,at_mono_mul,mixed,
    Function.iterate_succ_apply',Function.iterate_zero_apply,
    at_q_derivative,at_p_derivative,Nat.add_assoc] at hz
  simp (disch := omega) [hb3,higher,hx,forcing,Nat.add_sub_assoc,Nat.add_assoc] at hz
  have hm1 : (m:K)+7≠0 := by exact_mod_cast (show m+7≠0 by omega)
  have hmn : (m:K)+8≠0 := by exact_mod_cast (show m+8≠0 by omega)
  simpa [hb2,hm1,hmn,Nat.add_comm] using hz

end SexticC3.NonlinearB
