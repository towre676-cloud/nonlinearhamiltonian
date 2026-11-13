import SexticC3.NonlinearBClassification

open SexticC3 SexticC3.Differential SexticC3.NonlinearB
open MvPolynomial

set_option maxHeartbeats 2000000

def cubicExample (b0 b1 : ℚ) : Parameters ℚ :=
  ⟨0,0,0,0,0,0,1,0,0,b0,b1,0,1⟩

def quadraticExample : Parameters ℚ :=
  ⟨11,-1,0,7,0,-3,2,-2,3,1,4,4,0⟩

example : FirstRefinement (H (cubicExample 1 0)) (affinePartner 1 0) := by
  have h := (cubic_centered_partner_iff (cubicExample 1 0) (by norm_num [cubicExample])).mpr
    (by norm_num [NonlinearB.delta,cubicExample])
  simpa [cubicExample] using h

example : ¬FirstRefinement (H (cubicExample 0 1)) (affinePartner 1 0) := by
  have h := cubic_centered_partner_iff (cubicExample 0 1) (by norm_num [cubicExample])
  simpa [cubicExample,NonlinearB.delta] using h

example (G : Poly (R := ℚ)) :
    FirstRefinement (H (cubicExample 0 1)) G ↔
      ∃ l u : ℚ, G=C l*H (cubicExample 0 1)+mono 0 0 u := by
  exact cubic_regular_first_classification _ (by norm_num [cubicExample])
    (by norm_num [cubicExample]) (by norm_num [NonlinearB.delta,cubicExample]) G

example : FirstRefinement (H quadraticExample) (affinePartner 1 (1/2)) := by
  have h := quadratic_centered_partner quadraticExample
    (by norm_num [quadraticExample]) (by norm_num [quadraticExample])
  have hr : quadraticExample.b1/(2*quadraticExample.b2)=(1/2:ℚ) := by
    norm_num [quadraticExample]
  rw [hr] at h
  exact h

example : ¬PersistentCore (H quadraticExample) (affinePartner 1 (1/2)) := by
  exact quadratic_partner_not_persistent _ _ (by norm_num [quadraticExample])
    (by norm_num [quadraticExample]) (by norm_num [quadraticExample])

example (G : Poly (R := ℚ)) : PersistentCore (H quadraticExample) G ↔
    ∃ l u : ℚ, G=C l*H quadraticExample+mono 0 0 u := by
  exact quadratic_persistent_classification _ (by norm_num [quadraticExample])
    (by norm_num [quadraticExample]) (by norm_num [quadraticExample]) G

example (G : Poly (R := ℚ)) (h : Static (H (cubicExample 1 0)) G) :
    G.degreeOf true ≤ 2 := by
  exact cubic_static_momentum_bound _ (by norm_num [cubicExample])
    (by norm_num [cubicExample]) G h

example (G : Poly (R := ℚ)) (h : FirstRefinement (H quadraticExample) G) :
    G.degreeOf true ≤ 2 := by
  exact quadratic_first_momentum_bound _ (by norm_num [quadraticExample])
    (by norm_num [quadraticExample]) (by norm_num [quadraticExample]) G h
