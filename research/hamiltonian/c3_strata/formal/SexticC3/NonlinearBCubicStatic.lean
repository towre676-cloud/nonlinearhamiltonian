import SexticC3.NonlinearBCubicTail

noncomputable section
namespace SexticC3.NonlinearB
open MvPolynomial Differential
variable {K : Type*} [Field K] [CharZero K]

theorem cubic_static_p2_q_bound (c : Parameters K) (hb : c.b3≠0)
    (hh : c.h6≠0) (G : Poly (R := K)) (h : Static (H c) G) :
    ∀ i, 4 ≤ i → cf G i 2=0 := by
  have hp := cubic_static_momentum_bound c hb hh G h
  have higher (i : ℕ) : cf G i 4=0 := at_above_p_degree G i 4 (by omega)
  apply column_elimination G 2 4
  intro n hn htop
  obtain ⟨m,hm⟩ := Nat.exists_eq_add_of_le hn
  have hn' : n=m+4 := by omega
  subst n
  have h1 : cf G (m+5) 2=0 := htop _ (by omega)
  have h2 : cf G (m+6) 2=0 := htop _ (by omega)
  have hz := congrArg (fun F => cf F (m+4) 1) h.1
  rw [third_gate] at hz
  simp only [add_mul, cf_add, cf_sub, cf_zero, at_mono_mul, mixed,
    Function.iterate_succ_apply', Function.iterate_zero_apply,
    at_q_derivative, at_p_derivative, Nat.add_assoc] at hz
  norm_num [higher, h1, h2, Nat.add_sub_assoc, Nat.add_assoc] at hz
  have he : (36*c.b3*((m:K)+4)*((m:K)+1))*cf G (m+4) 2=0 := by
    linear_combination hz
  have hm1 : (m:K)+1≠0 := by exact_mod_cast (show m+1≠0 by omega)
  have hm4 : (m:K)+4≠0 := by exact_mod_cast (show m+4≠0 by omega)
  simpa [Nat.add_comm] using (mul_eq_zero.mp he).resolve_left
    (mul_ne_zero (mul_ne_zero (mul_ne_zero (by norm_num) hb) hm4) hm1)

theorem cubic_static_p1_q_bound (c : Parameters K) (hb : c.b3≠0)
    (hh : c.h6≠0) (G : Poly (R := K)) (h : Static (H c) G) :
    ∀ i, 2 ≤ i → cf G i 1=0 := by
  have hp := cubic_static_momentum_bound c hb hh G h
  have higher (i : ℕ) : cf G i 3=0 := at_above_p_degree G i 3 (by omega)
  apply column_elimination G 1 2
  intro n hn htop
  obtain ⟨m,hm⟩ := Nat.exists_eq_add_of_le hn
  have hn' : n=m+2 := by omega
  subst n
  have h1 : cf G (m+3) 1=0 := htop _ (by omega)
  have h2 : cf G (m+4) 1=0 := htop _ (by omega)
  have hz := congrArg (fun F => cf F (m+2) 0) h.1
  rw [third_gate] at hz
  simp only [add_mul, cf_add, cf_sub, cf_zero, at_mono_mul, mixed,
    Function.iterate_succ_apply', Function.iterate_zero_apply,
    at_q_derivative, at_p_derivative, Nat.add_assoc] at hz
  norm_num [higher, h1, h2, Nat.add_sub_assoc, Nat.add_assoc] at hz
  have hm1 : (m:K)+1≠0 := by exact_mod_cast (show m+1≠0 by omega)
  have hm2 : (m:K)+2≠0 := by exact_mod_cast (show m+2≠0 by omega)
  simpa [hb,hm1,hm2,Nat.add_comm] using hz

theorem cubic_static_p2_relations (c : Parameters K) (hb : c.b3≠0)
    (hh : c.h6≠0) (G : Poly (R := K)) (h : Static (H c) G) :
    c.b3*cf G 2 2=c.b2*cf G 3 2 ∧ c.b3*cf G 1 2=c.b1*cf G 3 2 := by
  have hp := cubic_static_momentum_bound c hb hh G h
  have higher (i : ℕ) : cf G i 4=0 := at_above_p_degree G i 4 (by omega)
  have h4 := cubic_static_p2_q_bound c hb hh G h 4 (by omega)
  have hz1 := congrArg (fun F => cf F 1 1) h.1
  have hz2 := congrArg (fun F => cf F 2 1) h.1
  rw [third_gate] at hz1 hz2
  simp only [add_mul, cf_add, cf_sub, cf_zero, at_mono_mul, mixed,
    Function.iterate_succ_apply', Function.iterate_zero_apply,
    at_q_derivative, at_p_derivative] at hz1 hz2
  norm_num [higher, h4] at hz1 hz2
  constructor
  · linear_combination -(1/72:K)*hz2
  · linear_combination -(1/72:K)*hz1

end SexticC3.NonlinearB
