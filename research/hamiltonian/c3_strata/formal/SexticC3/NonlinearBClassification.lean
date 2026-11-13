import SexticC3.NonlinearBCubicClassification
import SexticC3.NonlinearBQuadraticClassification

/-! All-degree classification of affine-A, quadratic/cubic-B sextic Hamiltonians. -/
noncomputable section
namespace SexticC3.NonlinearB
open MvPolynomial Differential
variable {K : Type*} [Field K] [CharZero K]

theorem affinePartner_scale (a r : K) :
    affinePartner a (a*r)=C a*affinePartner 1 r := by
  simp [affinePartner,mul_add]

theorem cubic_regular_first_classification (c : Parameters K)
    (hb : c.b3≠0) (hh : c.h6≠0) (hd : delta c≠0) (G : Poly (R := K)) :
    FirstRefinement (H c) G ↔ ∃ l u : K, G=C l*H c+mono 0 0 u := by
  rw [cubic_first_classification c hb hh]
  constructor
  · rintro ⟨l,u,a,e,heq,ha,hda⟩
    have ha0 := (mul_eq_zero.mp hda).resolve_right hd
    have he0 : e=0 := by
      rw [ha0,zero_mul] at ha
      have hz : (3*c.b3)*e=0 := by linear_combination -ha
      exact (mul_eq_zero.mp hz).resolve_left (mul_ne_zero (by norm_num) hb)
    exact ⟨l,u,by simpa [ha0,he0,affinePartner] using heq⟩
  · rintro ⟨l,u,rfl⟩
    exact ⟨l,u,0,0,by simp [affinePartner],by simp,by simp⟩

theorem cubic_exceptional_first_classification (c : Parameters K)
    (hb : c.b3≠0) (hh : c.h6≠0) (hd : delta c=0) (G : Poly (R := K)) :
    FirstRefinement (H c) G ↔ ∃ l u a : K,
      G=C l*H c+mono 0 0 u+C a*affinePartner 1 (c.b2/(3*c.b3)) := by
  rw [cubic_first_classification c hb hh]
  constructor
  · rintro ⟨l,u,a,e,heq,ha,_⟩
    have he : e=a*(c.b2/(3*c.b3)) := by
      have h3b : (3:K)*c.b3≠0 := mul_ne_zero (by norm_num) hb
      apply (mul_right_cancel₀ h3b)
      field_simp
      linear_combination -ha
    refine ⟨l,u,a,?_⟩
    simpa [he,affinePartner_scale] using heq
  · rintro ⟨l,u,a,rfl⟩
    refine ⟨l,u,a,a*(c.b2/(3*c.b3)),by rw [affinePartner_scale],?_,by simp [hd]⟩
    field_simp
    ring

theorem quadratic_centered_first_classification (c : Parameters K)
    (hb3 : c.b3=0) (hb2 : c.b2≠0) (hh : c.h6≠0) (G : Poly (R := K)) :
    FirstRefinement (H c) G ↔ ∃ l u a : K,
      G=C l*H c+mono 0 0 u+C a*affinePartner 1 (c.b1/(2*c.b2)) := by
  rw [quadratic_first_classification c hb3 hb2 hh]
  constructor
  · rintro ⟨l,u,a,e,heq,ha⟩
    have he : e=a*(c.b1/(2*c.b2)) := by
      have h2b : (2:K)*c.b2≠0 := mul_ne_zero (by norm_num) hb2
      apply (mul_right_cancel₀ h2b)
      field_simp
      linear_combination -ha
    refine ⟨l,u,a,?_⟩
    simpa [he,affinePartner_scale] using heq
  · rintro ⟨l,u,a,rfl⟩
    refine ⟨l,u,a,a*(c.b1/(2*c.b2)),by rw [affinePartner_scale],?_⟩
    field_simp
    ring

/-- The combined complete core theorem: B has degree two or three. -/
theorem nonlinear_B_persistent_classification (c : Parameters K) (hh : c.h6≠0)
    (hb : c.b3≠0 ∨ (c.b3=0 ∧ c.b2≠0)) (G : Poly (R := K)) :
    PersistentCore (H c) G ↔ ∃ l u : K, G=C l*H c+mono 0 0 u := by
  rcases hb with hb | ⟨hb3,hb2⟩
  · exact cubic_persistent_classification c hb hh G
  · exact quadratic_persistent_classification c hb3 hb2 hh G

end SexticC3.NonlinearB
