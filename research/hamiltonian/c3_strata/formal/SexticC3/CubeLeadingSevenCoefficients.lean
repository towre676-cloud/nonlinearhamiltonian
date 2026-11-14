import SexticC3.CubeLeadingSevenReduction

/-! Coefficient-level evaluation of the actual Hamiltonian iterates. -/
noncomputable section
set_option linter.unusedSectionVars false
namespace SexticC3.CubeLeading.Polynomial
open MvPolynomial
variable {K : Type*} [Field K] [CharZero K]

@[simp] lemma bicoeff_neg (i j : ℕ) (f : Poly K) : bicoeff i j (-f) = -bicoeff i j f := by
  simp [bicoeff]

abbrev Coefficients (K : Type*) := ℕ → ℕ → K
def polynomialCoefficients (f : Poly K) : Coefficients K := fun i j => bicoeff i j f
def coeffDq (a : Coefficients K) : Coefficients K := fun i j => ((i : K)+1)*a (i+1) j
def coeffDP (a : Coefficients K) : Coefficients K := fun i j => ((j : K)+1)*a i (j+1)
def coeffQ (a : Coefficients K) : Coefficients K := fun i j => if i=0 then 0 else a (i-1) j
def coeffP (a : Coefficients K) : Coefficients K := fun i j => if j=0 then 0 else a i (j-1)

def coefficientBracket (t : HamiltonianParameters K) (a : Coefficients K) : Coefficients K :=
  fun i j =>
    t.b₁*coeffP (coeffDP a) i j + (2*t.b₂)*coeffQ (coeffP (coeffDP a)) i j +
    (3*t.b₃)*coeffQ (coeffQ (coeffP (coeffDP a))) i j +
    t.c₁*coeffDP a i j + (2*t.c₂)*coeffQ (coeffDP a) i j +
    (3*t.c₃)*coeffQ (coeffQ (coeffDP a)) i j +
    (4*t.c₄)*coeffQ (coeffQ (coeffQ (coeffDP a))) i j +
    (5*t.c₅)*coeffQ (coeffQ (coeffQ (coeffQ (coeffDP a)))) i j -
    3*coeffP (coeffP (coeffDq a)) i j - t.b₀*coeffDq a i j -
    t.b₁*coeffQ (coeffDq a) i j - t.b₂*coeffQ (coeffQ (coeffDq a)) i j -
    t.b₃*coeffQ (coeffQ (coeffQ (coeffDq a))) i j

lemma coefficients_bracket (t : HamiltonianParameters K) (f : Poly K) :
    polynomialCoefficients (bracket (hamiltonian t) f) =
      coefficientBracket t (polynomialCoefficients f) := by
  funext i j
  simp only [polynomialCoefficients, hamiltonian_bracket, bicoeff_add, bicoeff_sub,
    bicoeff_C_mul, bicoeff_q_mul, bicoeff_P_mul, bicoeff_dq, bicoeff_dP,
    coefficientBracket, coeffQ, coeffP, coeffDq, coeffDP]

lemma bicoeff_iterated_bracket (t : HamiltonianParameters K) (f : Poly K) (n i j : ℕ) :
    bicoeff i j ((bracket (hamiltonian t))^[n] f) =
      ((coefficientBracket t)^[n] (polynomialCoefficients f)) i j := by
  have he : polynomialCoefficients ((bracket (hamiltonian t))^[n] f) =
      (coefficientBracket t)^[n] (polynomialCoefficients f) := by
    induction n with
    | zero => rfl
    | succ n ih => rw [Function.iterate_succ_apply', coefficients_bracket, ih, Function.iterate_succ_apply']
  exact congrFun (congrFun he i) j

lemma pderiv_q_monomial (i j : ℕ) (c : K) :
  pderiv 0 (monomial (exponent i j) c) = monomial (exponent (i-1) j) ((i : K)*c) := by
  have he : exponent i j - Finsupp.single 0 1 = exponent (i-1) j := by
    ext x; fin_cases x <;> simp
  simp [pderiv_monomial, he, smul_monomial, nsmul_eq_mul, mul_comm]
lemma pderiv_P_monomial (i j : ℕ) (c : K) :
  pderiv 1 (monomial (exponent i j) c) = monomial (exponent i (j-1)) ((j : K)*c) := by
  have he : exponent i j - Finsupp.single 1 1 = exponent i (j-1) := by
    ext x; fin_cases x <;> simp
  simp [pderiv_monomial, he, smul_monomial, nsmul_eq_mul, mul_comm]

end SexticC3.CubeLeading.Polynomial
