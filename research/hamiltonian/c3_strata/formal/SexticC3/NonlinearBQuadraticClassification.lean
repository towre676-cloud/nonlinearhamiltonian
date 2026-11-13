import SexticC3.NonlinearBQuadraticFirst
import SexticC3.NonlinearBLinear
import SexticC3.NonlinearBObstruction

noncomputable section
namespace SexticC3.NonlinearB
open MvPolynomial Differential
variable {K : Type*} [Field K] [CharZero K]

theorem quadratic_first_p2_relation (c : Parameters K) (hb3 : c.b3=0)
    (hb2 : c.b2≠0) (hh : c.h6≠0) (G : Poly (R := K)) (h : FirstRefinement (H c) G) :
    c.b2*cf G 1 2=c.b1*cf G 2 2 := by
  have h4 := quadratic_first_p4_zero c hb3 hb2 hh G h
  have hz := congrArg (fun F => cf F 0 1) h.1
  rw [third_gate] at hz
  simp only [add_mul,cf_add,cf_sub,cf_zero,at_mono_mul,mixed,
    Function.iterate_succ_apply',Function.iterate_zero_apply,
    at_q_derivative,at_p_derivative] at hz
  norm_num [hb3,h4] at hz
  linear_combination -(1/24:K)*hz

theorem quadratic_normalized_p2_zero (c : Parameters K) (hb3 : c.b3=0)
    (hb2 : c.b2≠0) (hh : c.h6≠0) (G : Poly (R := K))
    (h : FirstRefinement (H c) G) (hn : cf G 2 2=0) : ∀ i, cf G i 2=0 := by
  have hs : Static (H c) G := ⟨h.1,h.2.1⟩
  have hd : Static (H c) (contraction 1 (H c) G) := ⟨h.2.2.1,h.2.2.2⟩
  have hp := quadratic_first_momentum_bound c hb3 hb2 hh G h
  have hdp := quadratic_static_momentum_bound c hb3 hh _ hd
  have higher (i j : ℕ) (hj : 3 ≤ j) : cf G i j=0 := at_above_p_degree G i j (by omega)
  have dhigher (i : ℕ) : cf (contraction 1 (H c) G) i 5=0 := at_above_p_degree _ i 5 (by omega)
  have high := quadratic_static_p2_low_bound c hb3 hb2 hh G hs (fun i => higher i 4 (by omega))
  have h1 := quadratic_first_p2_relation c hb3 hb2 hh G h
  rw [hn,mul_zero] at h1
  have hg1 : cf G 1 2=0 := (mul_eq_zero.mp h1).resolve_left hb2
  have hz := congrArg (fun F => cf F 0 2) hd.1
  rw [third_gate] at hz
  simp only [add_mul,cf_add,cf_sub,cf_zero,at_mono_mul,mixed,
    Function.iterate_succ_apply',Function.iterate_zero_apply,
    at_q_derivative,at_p_derivative] at hz
  norm_num [hb3,dhigher] at hz
  simp only [first_gate,add_mul,cf_add,cf_sub,at_mono_mul,mixed,
    Function.iterate_succ_apply',Function.iterate_zero_apply,
    at_q_derivative,at_p_derivative] at hz
  simp (disch := omega) [hb3,higher,high,hg1,hn] at hz
  ring_nf at hz
  have hg0 : cf G 0 2=0 := by simpa [mul_eq_zero,hb2] using hz
  intro i
  rcases i with _ | i
  · exact hg0
  · rcases i with _ | i
    · exact hg1
    · rcases i with _ | i
      · exact hn
      · exact high _ (by omega)

theorem quadratic_normalized_p0_constant (c : Parameters K) (hb3 : c.b3=0)
    (hb2 : c.b2≠0) (hh : c.h6≠0) (G : Poly (R := K))
    (h : FirstRefinement (H c) G) (hn : cf G 2 2=0) :
    ∀ i, 1 ≤ i → cf G i 0=0 := by
  have hs : Static (H c) G := ⟨h.1,h.2.1⟩
  have hd : Static (H c) (contraction 1 (H c) G) := ⟨h.2.2.1,h.2.2.2⟩
  have hp := quadratic_first_momentum_bound c hb3 hb2 hh G h
  have higher (i j : ℕ) (hj : 3 ≤ j) : cf G i j=0 := at_above_p_degree G i j (by omega)
  have hp2 := quadratic_normalized_p2_zero c hb3 hb2 hh G h hn
  have hp1 := quadratic_static_p1_low_bound c hb3 hb2 hh G hs (fun i => higher i 3 (by omega))
  have hd3 (i : ℕ) : cf (contraction 1 (H c) G) i 3=0 := by
    rw [first_gate]
    simp only [add_mul,cf_add,cf_sub,at_mono_mul,mixed,
      Function.iterate_succ_apply',Function.iterate_zero_apply,
      at_q_derivative,at_p_derivative]
    simp (disch := omega) [hp2,higher,hb3]
  have hdp1 := quadratic_static_p1_low_bound c hb3 hb2 hh _ hd hd3
  apply column_elimination G 0 1
  intro n hn1 htop
  obtain ⟨m,hm⟩ := Nat.exists_eq_add_of_le hn1
  have hn' : n=m+1 := by omega
  subst n
  have hz := hdp1 (m+2) (by omega)
  rw [first_gate] at hz
  simp only [add_mul,cf_add,cf_sub,cf_zero,at_mono_mul,mixed,
    Function.iterate_succ_apply',Function.iterate_zero_apply,
    at_q_derivative,at_p_derivative,Nat.add_assoc] at hz
  have hx2 := htop (m+2) (by omega)
  have hx3 := htop (m+3) (by omega)
  norm_num [hb3,hp2,hp1 (m+2) (by omega),hp1 (m+3) (by omega),
    hx2,hx3,Nat.add_sub_assoc,Nat.add_assoc] at hz
  have hm1 : (m:K)+1≠0 := by exact_mod_cast (show m+1≠0 by omega)
  simpa [hb2,hm1,Nat.add_comm] using hz

theorem quadratic_normalized_first_shape (c : Parameters K) (hb3 : c.b3=0) (hb2 : c.b2≠0) (hh : c.h6≠0)
    (G : Poly (R := K)) (h : FirstRefinement (H c) G) (hn : cf G 2 2=0) :
    G=mono 0 0 (cf G 0 0)+affinePartner (cf G 1 1) (cf G 0 1) := by
  have hs : Static (H c) G := ⟨h.1,h.2.1⟩
  have hp := quadratic_first_momentum_bound c hb3 hb2 hh G h
  have hp2 := quadratic_normalized_p2_zero c hb3 hb2 hh G h hn
  have hp1 := quadratic_static_p1_low_bound c hb3 hb2 hh G hs (quadratic_first_p3_zero c hb3 hb2 hh G h)
  have hp0 := quadratic_normalized_p0_constant c hb3 hb2 hh G h hn
  apply MvPolynomial.ext
  intro m
  rw [← exponent_eta m]
  change cf G (m false) (m true)=_
  rcases m true with _ | j
  · by_cases hi : m false=0
    · simp [cf, affinePartner, coeff_mono, hi]
    · have hz := hp0 (m false) (by omega)
      simp [cf, affinePartner, coeff_mono, hi, Ne.symm hi, hz]
  · rcases j with _ | j
    · by_cases hi0 : m false=0
      · simp [cf, affinePartner, coeff_mono, hi0]
      · by_cases hi1 : m false=1
        · simp [cf, affinePartner, coeff_mono, hi1]
        · have hz := hp1 (m false) (by omega)
          simp [cf, affinePartner, coeff_mono, hi0,hi1,Ne.symm hi0,Ne.symm hi1,hz]
    · rcases j with _ | j
      · simp [cf, affinePartner, coeff_mono, hp2]
      · have hz := at_above_p_degree G (m false) (j+3) (by omega)
        change cf G (m false) (j+3)=cf _ (m false) (j+3)
        simp [cf, affinePartner, coeff_mono, hz]


/-- Complete quadratic-B first-refinement classification for arbitrary polynomials. -/
theorem quadratic_first_classification (c : Parameters K) (hb3 : c.b3=0) (hb2 : c.b2≠0) (hh : c.h6≠0)
    (G : Poly (R := K)) : FirstRefinement (H c) G ↔
    ∃ l u a e : K, G=C l*H c+mono 0 0 u+affinePartner a e ∧
      a*c.b1=2*e*c.b2 := by
  constructor
  · intro h
    let l := cf G 2 2/c.b2
    let R := G+C (-l)*H c
    have hR : FirstRefinement (H c) R := firstRefinement_shift c G (-l) h
    have hn : cf R 2 2=0 := by
      simp only [R, cf_add, cf_C_mul]
      have hc : cf (H c) 2 2=c.b2 := by norm_num [cf,H,coeff_add,coeff_mono]
      rw [hc]
      dsimp [l]
      field_simp
    have shape := quadratic_normalized_first_shape c hb3 hb2 hh R hR hn
    have heq : G=C l*H c+mono 0 0 (cf R 0 0)+
        affinePartner (cf R 1 1) (cf R 0 1) := by
      rw [add_assoc, ← shape]
      dsimp [R]
      simp only [map_neg]
      ring
    refine ⟨l,cf R 0 0,cf R 1 1,cf R 0 1,heq,?_⟩
    rw [heq,firstRefinement_translate] at h
    exact (quadratic_affinePartner_iff c hb3 hb2 _ _).mp h
  · rintro ⟨l,u,a,e,rfl,ha⟩
    apply (firstRefinement_translate c _ l u).mpr
    exact (quadratic_affinePartner_iff c hb3 hb2 a e).mpr ha

/-- The complete second refinement is the constant-energy span. -/
theorem quadratic_second_classification (c : Parameters K) (hb3 : c.b3=0) (hb2 : c.b2≠0) (hh : c.h6≠0)
    (G : Poly (R := K)) : Refinement (H c) 2 G ↔
    ∃ l u : K, G=C l*H c+mono 0 0 u := by
  constructor
  · intro h
    have hfirst : FirstRefinement (H c) G :=
      ⟨(h 0 (by omega)).1,(h 0 (by omega)).2,(h 1 (by omega)).1,(h 1 (by omega)).2⟩
    obtain ⟨l,u,a,e,heq,ha⟩ := (quadratic_first_classification c hb3 hb2 hh G).mp hfirst
    have hz := congrArg (fun P => cf P 6 0) (h 2 le_rfl).1
    have hc := constant_gates c u
    simp only [heq,Function.iterate_succ_apply',Function.iterate_zero_apply,
      contraction_add_right,contraction_C_mul_right,contraction_one_self,
      hc.1,mul_zero,zero_add,contraction_zero_right,
      quadratic_affine_second_coefficient c a e hb3,cf_zero] at hz
    have ha0 : a=0 := (mul_eq_zero.mp hz).resolve_left
      (mul_ne_zero (mul_ne_zero (by norm_num) (pow_ne_zero 2 hb2)) hh)
    have he0 : e=0 := by
      rw [ha0,zero_mul] at ha
      have hz : (2*c.b2)*e=0 := by linear_combination -ha
      exact (mul_eq_zero.mp hz).resolve_left (mul_ne_zero (by norm_num) hb2)
    refine ⟨l,u,?_⟩
    simpa [ha0,he0,affinePartner] using heq
  · rintro ⟨l,u,rfl⟩
    exact fun i _ => constant_energy_persistent c l u i

/-- End-to-end quadratic-B persistent-core theorem for the actual derivative operators. -/
theorem quadratic_persistent_classification (c : Parameters K) (hb3 : c.b3=0) (hb2 : c.b2≠0) (hh : c.h6≠0)
    (G : Poly (R := K)) : PersistentCore (H c) G ↔
    ∃ l u : K, G=C l*H c+mono 0 0 u := by
  constructor
  · intro h
    exact (quadratic_second_classification c hb3 hb2 hh G).mp (fun i _ => h i)
  · rintro ⟨l,u,rfl⟩
    exact constant_energy_persistent c l u

end SexticC3.NonlinearB
