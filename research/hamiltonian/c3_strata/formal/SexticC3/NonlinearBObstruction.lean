import SexticC3.NonlinearB
import SexticC3.NonlinearBCoefficients

noncomputable section
namespace SexticC3.NonlinearB
open MvPolynomial Differential
variable {K : Type*} [Field K] [CharZero K]

theorem cubic_affine_second_coefficient (c : Parameters K) (a e : K) :
    cf (contraction 3 (H c) (contraction 1 (H c)
      (contraction 1 (H c) (affinePartner a e)))) 8 0 =
      -60480*c.b3^2*c.h6*a := by
  rw [poisson_affinePartner, third_gate]
  simp only [add_mul, cf_add, cf_sub, at_mono_mul, mixed,
    Function.iterate_succ_apply', Function.iterate_zero_apply,
    at_q_derivative, at_p_derivative]
  norm_num only
  simp only [first_gate, add_mul, cf_add, cf_sub, at_mono_mul, mixed,
    Function.iterate_succ_apply', Function.iterate_zero_apply,
    at_q_derivative, at_p_derivative]
  norm_num [cf, firstPartner, coeff_add, coeff_mono]
  ring

theorem quadratic_affine_second_coefficient (c : Parameters K) (a e : K) (hb : c.b3=0) :
    cf (contraction 3 (H c) (contraction 1 (H c)
      (contraction 1 (H c) (affinePartner a e)))) 6 0 =
      -36288*c.b2^2*c.h6*a := by
  rw [poisson_affinePartner, third_gate]
  simp only [add_mul, cf_add, cf_sub, at_mono_mul, mixed,
    Function.iterate_succ_apply', Function.iterate_zero_apply,
    at_q_derivative, at_p_derivative]
  norm_num only
  simp only [first_gate, add_mul, cf_add, cf_sub, at_mono_mul, mixed,
    Function.iterate_succ_apply', Function.iterate_zero_apply,
    at_q_derivative, at_p_derivative]
  norm_num [cf, firstPartner, coeff_add, coeff_mono, hb]
  ring

set_option maxHeartbeats 4000000 in
set_option maxRecDepth 10000 in
/-- A top coefficient proves failure at the second refinement for every cubic B. -/
theorem cubic_second_obstruction (c : Parameters K) (r : K) :
    cf (contraction 3 (H c) (contraction 1 (H c)
      (contraction 1 (H c) (affinePartner 1 r)))) 8 0 =
      -60480*c.b3^2*c.h6 := by
  rw [poisson_affinePartner, third_gate]
  simp only [add_mul, cf_add, cf_sub, at_mono_mul, mixed,
    Function.iterate_succ_apply', Function.iterate_zero_apply,
    at_q_derivative, at_p_derivative]
  norm_num only
  simp only [first_gate, add_mul, cf_add, cf_sub, at_mono_mul, mixed,
    Function.iterate_succ_apply', Function.iterate_zero_apply,
    at_q_derivative, at_p_derivative]
  norm_num [cf, firstPartner, coeff_add, coeff_mono]
  ring

set_option maxHeartbeats 4000000 in
set_option maxRecDepth 10000 in
/-- The analogous quadratic-B obstruction is independent of all lower coefficients. -/
theorem quadratic_second_obstruction (c : Parameters K) (r : K) (hb : c.b3=0) :
    cf (contraction 3 (H c) (contraction 1 (H c)
      (contraction 1 (H c) (affinePartner 1 r)))) 6 0 =
      -36288*c.b2^2*c.h6 := by
  rw [poisson_affinePartner, third_gate]
  simp only [add_mul, cf_add, cf_sub, at_mono_mul, mixed,
    Function.iterate_succ_apply', Function.iterate_zero_apply,
    at_q_derivative, at_p_derivative]
  norm_num only
  simp only [first_gate, add_mul, cf_add, cf_sub, at_mono_mul, mixed,
    Function.iterate_succ_apply', Function.iterate_zero_apply,
    at_q_derivative, at_p_derivative]
  norm_num [cf, firstPartner, coeff_add, coeff_mono, hb]
  ring

theorem cubic_partner_not_second (c : Parameters K) (r : K)
    (hb : c.b3≠0) (hh : c.h6≠0) : ¬Refinement (H c) 2 (affinePartner 1 r) := by
  intro h
  have hz := congrArg (fun P => cf P 8 0) (h 2 le_rfl).1
  simp only [Function.iterate_succ_apply', Function.iterate_zero_apply,
    cubic_second_obstruction, cf, coeff_zero] at hz
  exact (mul_ne_zero (mul_ne_zero (by norm_num) (pow_ne_zero 2 hb)) hh) hz

theorem quadratic_partner_not_second (c : Parameters K) (r : K)
    (hb3 : c.b3=0) (hb2 : c.b2≠0) (hh : c.h6≠0) :
    ¬Refinement (H c) 2 (affinePartner 1 r) := by
  intro h
  have hz := congrArg (fun P => cf P 6 0) (h 2 le_rfl).1
  simp only [Function.iterate_succ_apply', Function.iterate_zero_apply,
    quadratic_second_obstruction c r hb3, cf, coeff_zero] at hz
  exact (mul_ne_zero (mul_ne_zero (by norm_num) (pow_ne_zero 2 hb2)) hh) hz

theorem cubic_partner_not_persistent (c : Parameters K) (r : K)
    (hb : c.b3≠0) (hh : c.h6≠0) : ¬PersistentCore (H c) (affinePartner 1 r) := by
  intro h
  exact cubic_partner_not_second c r hb hh (fun i _ => h i)

theorem quadratic_partner_not_persistent (c : Parameters K) (r : K)
    (hb3 : c.b3=0) (hb2 : c.b2≠0) (hh : c.h6≠0) :
    ¬PersistentCore (H c) (affinePartner 1 r) := by
  intro h
  exact quadratic_partner_not_second c r hb3 hb2 hh (fun i _ => h i)

end SexticC3.NonlinearB
