import SexticC3.ChartTransport
import Mathlib.RingTheory.MvPolynomial.EulerIdentity

noncomputable section

namespace SexticC3.Differential

open MvPolynomial

variable {K : Type*} [Field K] [CharZero K]

theorem mono_eq_X (i j : ℕ) (r : K) :
    mono i j r = C r * X false ^ i * X true ^ j := by
  unfold mono exponent
  rw [monomial_add_single]
  congr 1
  simpa using (monomial_add_single (s := (0 : Bool →₀ ℕ)) (n := false) (e := i) (a := r))

theorem linearSub_comp (a b c d u v w x : K) :
    (linearSub a b c d).comp (linearSub u v w x) =
      linearSub (u*a+v*c) (u*b+v*d) (w*a+x*c) (w*b+x*d) := by
  apply MvPolynomial.algHom_ext
  intro i
  cases i <;>
    simp only [AlgHom.comp_apply, linearSub_X_false, linearSub_X_true, map_add,
      map_mul, linearSub_C] <;> ring

/-- The shear p ↦ p+s q removes the second coefficient after a simple
root has been put at q=0. The first two coefficients encode the root
condition and its simplicity. -/
theorem normalize_edge_coefficients (g : ℕ → K) (h0 : g 0 = 0) (h1 : g 1 ≠ 0) :
    ∃ s t a b c d : K, t ≠ 0 ∧
      C t * linearSub 1 0 s 1 (homogeneous 6 g) = hamiltonian a b c d := by
  let s := -(g 2 / (5*g 1))
  let t := (g 1)⁻¹
  let a := t*(10*g 1*s^2+4*g 2*s+g 3)
  let b := t*(10*g 1*s^3+6*g 2*s^2+3*g 3*s+g 4)
  let c := t*(5*g 1*s^4+4*g 2*s^3+3*g 3*s^2+2*g 4*s+g 5)
  let d := t*(g 1*s^5+g 2*s^4+g 3*s^3+g 4*s^2+g 5*s+g 6)
  refine ⟨s, t, a, b, c, d, inv_ne_zero h1, ?_⟩
  have he : 5*g 1*s+g 2 = 0 := by
    have hn : (5 : K)*g 1 ≠ 0 := mul_ne_zero (by norm_num) h1
    have hs : (g 2 / (5*g 1)) * (5*g 1) = g 2 := div_mul_cancel₀ _ hn
    dsimp [s]
    linear_combination -hs
  have ht : t * g 1 = 1 := inv_mul_cancel₀ h1
  calc
    _ = C (t*g 1) * X false * X true^5 +
          C (t*(5*g 1*s+g 2)) * X false^2 * X true^4 +
          C a * X false^3 * X true^3 + C b * X false^4 * X true^2 +
          C c * X false^5 * X true + C d * X false^6 := by
      norm_num [homogeneous, List.range_succ, h0, mono_eq_X, linearSub_C, map_add,
        map_mul, map_pow, linearSub_X_false, linearSub_X_true]
      simp only [a, b, c, d, map_mul, map_add, map_pow, map_ofNat]
      ring
    _ = _ := by
      rw [ht, he]
      norm_num [hamiltonian, sexticExponents, hCoeff, mono_eq_X]
      ring

/-- Evaluate a binary polynomial at a pair of scalars. -/
def atPoint (u v : K) : Poly (R := K) →+* K := eval (fun i : Bool => if i then v else u)

private theorem atPoint_linearSub (a b c d : K) (F : Poly (R := K)) :
    atPoint 0 1 (linearSub a b c d F) = atPoint b d F := by
  have h : (atPoint 0 1).comp (linearSub a b c d).toRingHom = atPoint b d := by
    apply MvPolynomial.ringHom_ext
    · intro x
      simp [atPoint, linearSub_C]
    · intro i
      cases i <;> simp [atPoint, linearSub_X_false, linearSub_X_true]
  exact DFunLike.congr_fun h F

private theorem atPoint_edge (g : ℕ → K) :
    atPoint 0 1 (homogeneous 6 g) = g 0 := by
  norm_num [atPoint, homogeneous, mono_eq_X, List.range_succ, map_pow]

private theorem atPoint_edge_derivative (g : ℕ → K) :
    atPoint 0 1 (pderiv false (homogeneous 6 g)) = g 1 := by
  norm_num [atPoint, homogeneous, List.range_succ, pderiv_q_mono, mono_eq_X, map_pow]

private theorem edge_chart (F : Poly (R := K)) (hF : F.IsHomogeneous 6)
    (u v w x : K) (hdet : u*x-v*w ≠ 0) (hroot : atPoint v x F = 0)
    (hsimple : u * atPoint v x (pderiv false F) + w * atPoint v x (pderiv true F) ≠ 0) :
    ∃ u' w' t a b c d : K, u'*x-v*w' ≠ 0 ∧ t ≠ 0 ∧
      C t * linearSub u' v w' x F = hamiltonian a b c d := by
  let A := linearSub u v w x
  let g : ℕ → K := fun j => coeff (exponent j (6-j)) (A F)
  have hg : homogeneous 6 g = A F :=
    homogeneous_of_isHomogeneous 6 _ (isHomogeneous_linearSub u v w x 6 F hF)
  have h0 : g 0 = 0 := by
    rw [← atPoint_edge g, hg]
    exact (atPoint_linearSub u v w x F).trans hroot
  have h1 : g 1 ≠ 0 := by
    rw [← atPoint_edge_derivative g, hg]
    change atPoint 0 1 (pderiv false (linearSub u v w x F)) ≠ 0
    rw [pderiv_linearSub]
    simpa only [Bool.false_eq_true, if_false, map_add, map_mul, atPoint_linearSub,
      show ∀ c : K, atPoint 0 1 (C c) = c from fun c => by simp [atPoint]] using hsimple
  obtain ⟨s,t,a,b,c,d,ht,hchart⟩ := normalize_edge_coefficients g h0 h1
  rw [hg] at hchart
  have hc := DFunLike.congr_fun (linearSub_comp (1 : K) 0 s 1 u v w x) F
  simp only [AlgHom.comp_apply, mul_one, mul_zero, zero_add, add_zero] at hc
  refine ⟨u+v*s,w+x*s,t,a,b,c,d,?_,ht,?_⟩
  · convert hdet using 1 <;> ring
  · exact (congrArg (fun Y : Poly (R := K) => C t * Y) hc).symm.trans hchart

/-- Move a nonzero root with nonvanishing gradient to q=0 and shear away
the quadratic edge coefficient. The resulting chart retains the given root
as the second column of the coordinate matrix. -/
theorem normalize_simple_projective_root (F : Poly (R := K)) (hF : F.IsHomogeneous 6)
    (v x : K) (hpoint : v ≠ 0 ∨ x ≠ 0) (hroot : atPoint v x F = 0)
    (hsimple : atPoint v x (pderiv false F) ≠ 0 ∨ atPoint v x (pderiv true F) ≠ 0) :
    ∃ u w t a b c d : K, u*x-v*w ≠ 0 ∧ t ≠ 0 ∧
      C t * linearSub u v w x F = hamiltonian a b c d := by
  have he := congrArg (atPoint v x) hF.sum_X_mul_pderiv
  simp only [Fintype.sum_bool, map_add, map_mul, map_nsmul, hroot, nsmul_zero] at he
  have hEuler :
      x * atPoint v x (pderiv true F) + v * atPoint v x (pderiv false F) = 0 := by
    simpa [atPoint] using he
  by_cases hx : x = 0
  · have hv := hpoint.resolve_right (fun h => h hx)
    have hq : atPoint v x (pderiv false F) = 0 := by
      apply (mul_eq_zero.mp _).resolve_left hv
      simpa [hx] using hEuler
    exact edge_chart F hF 0 v 1 x (by simpa using hv) hroot
      (by simpa using hsimple.resolve_left (fun h => h hq))
  · have hq : atPoint v x (pderiv false F) ≠ 0 := by
      intro hq
      have hp : atPoint v x (pderiv true F) = 0 := by
        apply (mul_eq_zero.mp _).resolve_left hx
        simpa [hq] using hEuler
      exact hsimple.elim (fun h => h hq) (fun h => h hp)
    exact edge_chart F hF 1 v 0 x (by simpa using hx) hroot (by simpa using hq)

end SexticC3.Differential
