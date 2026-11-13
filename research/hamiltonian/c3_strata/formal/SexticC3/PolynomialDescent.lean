import SexticC3.HomogeneousCoordinates

noncomputable section

namespace SexticC3.Differential

open MvPolynomial

variable {K L : Type*} [Field K] [Field L]

theorem map_pderiv (f : K →+* L) (x : Bool) (F : Poly (R := K)) :
    map f (pderiv x F) = pderiv x (map f F) := by
  induction F using MvPolynomial.induction_on' with
  | monomial e a => simp [pderiv_monomial, map_monomial]
  | add F G hF hG => simp [hF,hG]

private theorem map_iterate_pderiv (f : K →+* L) (x : Bool) (i : ℕ) (F : Poly (R := K)) :
    map f ((pderiv x)^[i] F) = (pderiv x)^[i] (map f F) := by
  induction i with
  | zero => rfl
  | succ i ih => simp only [Function.iterate_succ_apply', map_pderiv, ih]

theorem map_contraction (f : K →+* L) (k : ℕ) (F G : Poly (R := K)) :
    map f (contraction k F G) = contraction k (map f F) (map f G) := by
  unfold contraction
  induction List.range (k+1) with
  | nil => simp
  | cons s ss ih =>
    simp only [List.map_cons, List.sum_cons, map_add]
    rw [ih]
    simp only [map_mul, map_C, map_pow, map_neg, map_one, map_natCast, mixed, map_iterate_pderiv]

theorem firstRefinement_map (f : K →+* L) (F G : Poly (R := K))
    (h : FirstRefinement F G) : FirstRefinement (map f F) (map f G) := by
  unfold FirstRefinement
  rw [← map_contraction, ← map_contraction, ← map_contraction f 1,
    ← map_contraction f 3, ← map_contraction f 5, h.1, h.2.1, h.2.2.1, h.2.2.2]
  simp

/-- A constant-plus-Hamiltonian expression over an extension field
descends by extracting a nonzero degree-six coefficient of F. -/
theorem polynomial_shape_descent (f : K →+* L) (F G : Poly (R := K))
    (hF : F.IsHomogeneous 6) (hn : F ≠ 0) (r s : L)
    (h : map f G = C r + C s * map f F) : ∃ u v : K, G = C u + C v * F := by
  obtain ⟨e,he⟩ := exists_coeff_ne_zero hn
  have hd := hF he
  have he0 : e ≠ 0 := by
    intro hz
    subst e
    norm_num [exponent_degree] at hd
  have hF0 : coeff 0 F = 0 := hF.coeff_eq_zero (by norm_num [exponent_degree])
  have hr := congrArg (coeff 0) h
  have hs := congrArg (coeff e) h
  simp only [coeff_map, coeff_add, coeff_C, if_true, coeff_C_mul, hF0, map_zero, mul_zero,
    add_zero] at hr
  simp only [coeff_map, coeff_add, coeff_C, if_neg (Ne.symm he0), coeff_C_mul, zero_add] at hs
  let v := coeff e G / coeff e F
  have hv : f v = s := by
    dsimp [v]
    rw [map_div₀, hs, mul_div_cancel_right₀ _ ((map_ne_zero f).mpr he)]
  refine ⟨coeff 0 G, v, ?_⟩
  apply map_injective f f.injective
  simpa only [map_add, map_mul, map_C, hr, hv] using h

end SexticC3.Differential
