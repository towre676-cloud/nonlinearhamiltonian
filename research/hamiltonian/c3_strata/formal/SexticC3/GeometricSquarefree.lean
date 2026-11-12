import SexticC3.SimpleRootChart
import SexticC3.TargetRootMultiplicity
import Mathlib.FieldTheory.IsAlgClosed.Basic
import Mathlib.FieldTheory.Separable

noncomputable section

namespace SexticC3.Differential

open MvPolynomial

variable {K : Type*} [Field K] [CharZero K]

/-- Every projective root in the coefficient field has nonzero gradient.
Over an algebraically closed field this is the simple-root condition at
every projective root. -/
def SimpleProjectiveRoots (F : Poly (R := K)) : Prop :=
  ∀ u v : K, u ≠ 0 ∨ v ≠ 0 → atPoint u v F = 0 →
    atPoint u v (pderiv false F) ≠ 0 ∨ atPoint u v (pderiv true F) ≠ 0

theorem atPoint_linearSub_apply (a b c d u v : K) (F : Poly (R := K)) :
    atPoint u v (linearSub a b c d F) = atPoint (a*u+b*v) (c*u+d*v) F := by
  have h : (atPoint u v).comp (linearSub a b c d).toRingHom =
      atPoint (a*u+b*v) (c*u+d*v) := by
    apply MvPolynomial.ringHom_ext
    · intro x
      simp [atPoint, linearSub_C]
    · intro i
      cases i <;> simp [atPoint, linearSub_X_false, linearSub_X_true]
  exact DFunLike.congr_fun h F

theorem simpleProjectiveRoots_linearSub (F : Poly (R := K)) (hF : SimpleProjectiveRoots F)
    (a b c d t : K) (hdet : a*d-b*c ≠ 0) (ht : t ≠ 0) :
    SimpleProjectiveRoots (C t * linearSub a b c d F) := by
  intro u v hv hroot
  let x := a*u+b*v
  let y := c*u+d*v
  have hxy : x ≠ 0 ∨ y ≠ 0 := by
    by_contra h
    push_neg at h
    have hu : (a*d-b*c)*u = 0 := by
      dsimp [x,y] at h
      linear_combination d*h.1-b*h.2
    have hv' : (a*d-b*c)*v = 0 := by
      dsimp [x,y] at h
      linear_combination a*h.2-c*h.1
    exact hv.elim
      (fun h => h ((mul_eq_zero.mp hu).resolve_left hdet))
      (fun h => h ((mul_eq_zero.mp hv').resolve_left hdet))
  have he : ∀ q : K, atPoint u v (C q) = q := fun q => by simp [atPoint]
  rw [map_mul, he, atPoint_linearSub_apply] at hroot
  have hsource := hF x y hxy ((mul_eq_zero.mp hroot).resolve_left ht)
  by_contra h
  push_neg at h
  obtain ⟨hq,hp⟩ := h
  simp only [pderiv_C_mul, pderiv_linearSub, Bool.false_eq_true, if_false, if_true,
    map_mul, map_add, he, atPoint_linearSub_apply] at hq hp
  have hq' := (mul_eq_zero.mp hq).resolve_left ht
  have hp' := (mul_eq_zero.mp hp).resolve_left ht
  have hA : (a*d-b*c) * atPoint x y (pderiv false F) = 0 := by
    linear_combination d*hq'-c*hp'
  have hB : (a*d-b*c) * atPoint x y (pderiv true F) = 0 := by
    linear_combination a*hp'-b*hq'
  exact hsource.elim
    (fun h => h ((mul_eq_zero.mp hA).resolve_left hdet))
    (fun h => h ((mul_eq_zero.mp hB).resolve_left hdet))

private def dehomP : Poly (R := K) →ₐ[K] Polynomial K :=
  aeval fun i : Bool => if i then Polynomial.X else 1

private theorem eval_dehomP (F : Poly (R := K)) (v : K) :
    Polynomial.eval v (dehomP F) = atPoint 1 v F := by
  have h : (Polynomial.evalRingHom v).comp (dehomP (K := K)).toRingHom = atPoint 1 v := by
    apply MvPolynomial.ringHom_ext
    · intro c
      simp [dehomP, aeval_C, Polynomial.algebraMap_apply, atPoint]
    · intro i
      cases i <;> simp [dehomP, atPoint]
  exact DFunLike.congr_fun h F

private theorem dehomP_hamiltonian (a b c d : K) :
    dehomP (hamiltonian a b c d) = StaticTail.chartQuintic a b c d := by
  norm_num [dehomP, hamiltonian, sexticExponents, hCoeff, mono_eq_X,
    aeval_C, Polynomial.algebraMap_apply, StaticTail.chartQuintic, map_pow]
  ring

private theorem dehomP_pderiv_hamiltonian (a b c d : K) :
    dehomP (pderiv true (hamiltonian a b c d)) =
      (StaticTail.chartQuintic a b c d).derivative := by
  norm_num [dehomP, hamiltonian, sexticExponents, hCoeff, pderiv_p_mono, mono_eq_X,
    aeval_C, Polynomial.algebraMap_apply, StaticTail.chartQuintic, map_pow,
    Polynomial.derivative_add, Polynomial.derivative_C_mul, Polynomial.derivative_X_pow]
  simp only [map_ofNat]
  ring

/-- A homogeneous binary sextic over an algebraically closed field has
a projective root. -/
theorem exists_projective_root [IsAlgClosed K] (F : Poly (R := K))
    (hF : F.IsHomogeneous 6) : ∃ v x : K, (v ≠ 0 ∨ x ≠ 0) ∧ atPoint v x F = 0 := by
  let g : ℕ → K := fun j => coeff (exponent j (6-j)) F
  have hg : homogeneous 6 g = F := homogeneous_of_isHomogeneous 6 F hF
  by_cases h0 : g 0 = 0
  · refine ⟨0,1,Or.inr one_ne_zero,?_⟩
    rw [← hg]
    simpa [atPoint, homogeneous, mono_eq_X, List.range_succ, map_pow] using h0
  · have hcoeff : (dehomP F).coeff 6 = g 0 := by
      rw [← hg]
      norm_num [dehomP, homogeneous, mono_eq_X, List.range_succ, map_pow, aeval_C,
        Polynomial.algebraMap_apply, Polynomial.coeff_C_mul, Polynomial.coeff_X_pow]
    have hd : (dehomP F).degree ≠ 0 := by
      intro he
      have hn := Polynomial.le_natDegree_of_ne_zero (show (dehomP F).coeff 6 ≠ 0 from hcoeff ▸ h0)
      rw [Polynomial.natDegree_eq_of_degree_eq_some (show (dehomP F).degree = (0 : ℕ) from he)] at hn
      omega
    obtain ⟨x,hx⟩ := IsAlgClosed.exists_root _ hd
    exact ⟨1,x,Or.inl one_ne_zero,(eval_dehomP F x).symm.trans hx⟩

private theorem separable_of_no_common_root [IsAlgClosed K] (f : Polynomial K) (hf : f ≠ 0)
    (h : ∀ x, f.IsRoot x → ¬f.derivative.IsRoot x) : f.Separable := by
  classical
  let g := EuclideanDomain.gcd f f.derivative
  have hleft : g ∣ f := EuclideanDomain.gcd_dvd_left _ _
  have hright : g ∣ f.derivative := EuclideanDomain.gcd_dvd_right _ _
  have hg : g ≠ 0 := by
    intro hz
    rw [hz, zero_dvd_iff] at hleft
    exact hf hleft
  have hdeg : g.degree = 0 := by
    by_contra hn
    obtain ⟨x,hx⟩ := IsAlgClosed.exists_root g hn
    exact h x (hx.dvd hleft) (hx.dvd hright)
  obtain ⟨r,hr⟩ := Polynomial.natDegree_eq_zero.mp (Polynomial.natDegree_eq_of_degree_eq_some hdeg)
  have hr0 : r ≠ 0 := by
    intro hz
    apply hg
    simpa [hz] using hr.symm
  have hbez := EuclideanDomain.gcd_eq_gcd_ab f f.derivative
  change g = _ at hbez
  rw [← hr] at hbez
  refine ⟨Polynomial.C r⁻¹ * EuclideanDomain.gcdA f f.derivative,
    Polynomial.C r⁻¹ * EuclideanDomain.gcdB f f.derivative, ?_⟩
  calc
    _ = Polynomial.C r⁻¹ * (f * EuclideanDomain.gcdA f f.derivative +
        f.derivative * EuclideanDomain.gcdB f f.derivative) := by ring
    _ = 1 := by rw [← hbez, ← map_mul, inv_mul_cancel₀ hr0, map_one]

theorem separable_chartQuintic_of_simpleProjectiveRoots [IsAlgClosed K] (a b c d : K)
    (h : SimpleProjectiveRoots (hamiltonian a b c d)) :
    (StaticTail.chartQuintic a b c d).Separable := by
  apply separable_of_no_common_root
  · intro hz
    have h5 := congrArg (fun p : Polynomial K => p.coeff 5) hz
    norm_num [StaticTail.chartQuintic, Polynomial.coeff_C_mul, Polynomial.coeff_X_pow] at h5
  · intro x hx hp
    have hroot : atPoint 1 x (hamiltonian a b c d) = 0 := by
      rw [← eval_dehomP, dehomP_hamiltonian]
      exact hx
    have hp' : atPoint 1 x (pderiv true (hamiltonian a b c d)) = 0 := by
      rw [← eval_dehomP, dehomP_pderiv_hamiltonian]
      exact hp
    have hF : (hamiltonian a b c d : Poly (R := K)).IsHomogeneous 6 := by
      have hh := homogeneous_hCoeff a b c d 1
      simp only [C_1, one_mul] at hh
      rw [← hh]
      unfold homogeneous
      apply list_sum_homogeneous
      intro P hP
      obtain ⟨j,hj,rfl⟩ := List.mem_map.mp hP
      apply isHomogeneous_monomial
      have hj' := List.mem_range.mp hj
      simp [exponent_degree]
      omega
    have he := congrArg (atPoint 1 x) hF.sum_X_mul_pderiv
    simp only [Fintype.sum_bool, map_add, map_mul, map_nsmul, hroot, hp', nsmul_zero,
      mul_zero, zero_add] at he
    have hq : atPoint 1 x (pderiv false (hamiltonian a b c d)) = 0 := by
      simpa [atPoint] using he
    exact (h 1 x (Or.inl one_ne_zero) hroot).elim (fun h => h hq) (fun h => h hp')

end SexticC3.Differential
