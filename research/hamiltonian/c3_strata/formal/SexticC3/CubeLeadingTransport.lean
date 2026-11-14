import SexticC3.CubeLeadingPersistent

/-! # The nonlinear shear and the original flat differential operators. -/
noncomputable section
set_option linter.unusedSectionVars false
namespace SexticC3.CubeLeading.Polynomial
open MvPolynomial
variable {K : Type*} [Field K] [CharZero K]

@[simp] lemma pderiv_two (i : Fin 2) : pderiv i (2 : Poly K) = 0 := (pderiv i).map_natCast 2
@[simp] lemma pderiv_three (i : Fin 2) : pderiv i (3 : Poly K) = 0 := (pderiv i).map_natCast 3
@[simp] lemma pderiv_four (i : Fin 2) : pderiv i (4 : Poly K) = 0 := (pderiv i).map_natCast 4
@[simp] lemma pderiv_five (i : Fin 2) : pderiv i (5 : Poly K) = 0 := (pderiv i).map_natCast 5
@[simp] lemma pderiv_six (i : Fin 2) : pderiv i (6 : Poly K) = 0 := (pderiv i).map_natCast 6

lemma pderiv_P_q (f : Poly K) : pderiv 1 (pderiv 0 f) = pderiv 0 (pderiv 1 f) := by
  ext m
  rw [← exponent_ext m]
  change bicoeff (m 0) (m 1) _ = bicoeff (m 0) (m 1) _
  simp only [bicoeff_dq, bicoeff_dP]
  ring

/-- Pull back along P=p+a*q². -/
def shear (a : K) : Poly K →ₐ[K] Poly K := aeval ![X 0, X 1+C a*X 0^2]

@[simp] lemma shear_C (a c : K) : shear a (C c : Poly K) = C c := by simp [shear]
@[simp] lemma shear_q (a : K) : shear a (X 0 : Poly K) = X 0 := by simp [shear]
@[simp] lemma shear_P (a : K) : shear a (X 1 : Poly K) = X 1+C a*X 0^2 := by simp [shear]

lemma shear_comp (a b : K) (f : Poly K) : shear a (shear b f) = shear (a+b) f := by
  have he : (shear a).comp (shear b) = shear (a+b) := by
    ext i : 1
    fin_cases i <;> simp [map_add, map_mul, map_pow] <;> ring
  exact DFunLike.congr_fun he f

@[simp] lemma shear_zero (f : Poly K) : shear 0 f = f := by
  have he : shear (0 : K) = AlgHom.id K (Poly K) := by
    ext i : 1
    fin_cases i <;> simp
  exact DFunLike.congr_fun he f

lemma shear_injective (a : K) : Function.Injective (shear a : Poly K → Poly K) := by
  intro f g he
  have hh := congrArg (shear (-a)) he
  simpa [shear_comp] using hh

lemma pderiv_q_shear (a : K) (f : Poly K) :
    pderiv 0 (shear a f) = shear a (pderiv 0 f+C (2*a)*(X 0*pderiv 1 f)) := by
  induction f using MvPolynomial.induction_on with
  | C c => simp [pderiv_C]
  | add f g hf hg => simp only [map_add, hf, hg, mul_add]; ring
  | mul_X f i ih =>
    fin_cases i <;>
      simp [map_mul, pderiv_mul, pderiv_pow, ih, pderiv_C_mul, pderiv_X,
        Pi.single_apply, map_ofNat] <;> ring

lemma pderiv_P_shear (a : K) (f : Poly K) :
    pderiv 1 (shear a f) = shear a (pderiv 1 f) := by
  induction f using MvPolynomial.induction_on with
  | C c => simp [pderiv_C]
  | add f g hf hg => simp only [map_add, hf, hg]
  | mul_X f i ih =>
    fin_cases i <;>
      simp [map_mul, pderiv_mul, pderiv_pow, ih, pderiv_C_mul, pderiv_X,
        Pi.single_apply] <;> ring

lemma bracket_shear (a : K) (H f : Poly K) :
    bracket (shear a H) (shear a f) = shear a (bracket H f) := by
  simp only [bracket, pderiv_q_shear, pderiv_P_shear, map_sub, map_add, map_mul]
  ring

/-- The transported q derivative; the P derivative stays unchanged. -/
def chartDq (f : Poly K) : Poly K := pderiv 0 f+C 2*(X 0*pderiv 1 f)

def flatMixed (r s : ℕ) (f : Poly K) : Poly K :=
  (pderiv 0)^[r] ((pderiv 1)^[s] f)

def chartMixed (r s : ℕ) (f : Poly K) : Poly K :=
  chartDq^[r] ((pderiv 1)^[s] f)

lemma flatMixed_shear (r s : ℕ) (f : Poly K) :
    flatMixed r s (shear 1 f) = shear 1 (chartMixed r s f) := by
  have hp : ∀ s : ℕ, (pderiv 1)^[s] (shear 1 f) = shear 1 ((pderiv 1)^[s] f) := by
    intro s; induction s with
    | zero => rfl
    | succ s ih => rw [Function.iterate_succ_apply', ih, pderiv_P_shear, Function.iterate_succ_apply']
  unfold flatMixed chartMixed
  rw [hp]
  induction r with
  | zero => rfl
  | succ r ih =>
    rw [Function.iterate_succ_apply', ih, pderiv_q_shear, Function.iterate_succ_apply']
    simp [chartDq]

/-- Unnormalized alternating flat contraction in whichever coordinates the
input polynomials use. -/
def flatContraction (k : ℕ) (H f : Poly K) : Poly K :=
  ∑ r ∈ Finset.range (k+1), C ((-1 : K)^r*(Nat.choose k r : K))*
    flatMixed (k-r) r H*flatMixed r (k-r) f

def chartContraction (k : ℕ) (H f : Poly K) : Poly K :=
  ∑ r ∈ Finset.range (k+1), C ((-1 : K)^r*(Nat.choose k r : K))*
    chartMixed (k-r) r H*chartMixed r (k-r) f

lemma flatContraction_shear (k : ℕ) (H f : Poly K) :
    flatContraction k (shear 1 H) (shear 1 f) = shear 1 (chartContraction k H f) := by
  simp only [flatContraction, chartContraction, map_sum, map_mul, shear_C, flatMixed_shear]


set_option maxHeartbeats 2000000 in
lemma chart_hamiltonian_30 (t : HamiltonianParameters K) :
    chartMixed 3 0 (hamiltonian t) =
    C (6*t.b₃)*X 1 + C 72*X 1*X 0 + C (6*t.b₁) + C (24*t.b₂)*X 0 +
    C (54*t.b₃)*X 0^2 + C (6*t.c₃) + C (24*t.c₄)*X 0 +
    C (60*t.c₅)*X 0^2 + C 48*X 0^3 := by
  simp [chartMixed, chartDq, Function.iterate_succ_apply', hamiltonian, ← qP_monomial,
    pderiv_mul, pderiv_pow, pderiv_C_mul, pderiv_X, Pi.single_apply, map_ofNat]
  ring

set_option maxHeartbeats 2000000 in
lemma chart_hamiltonian_21 (t : HamiltonianParameters K) :
    chartMixed 2 1 (hamiltonian t) =
    C 12*X 1 + C (2*t.b₂) + C (6*t.b₃)*X 0 + C 24*X 0^2 := by
  simp [chartMixed, chartDq, Function.iterate_succ_apply', hamiltonian, ← qP_monomial,
    pderiv_mul, pderiv_pow, pderiv_C_mul, pderiv_X, Pi.single_apply, map_ofNat]
  ring

lemma chart_hamiltonian_12 (t : HamiltonianParameters K) :
    chartMixed 1 2 (hamiltonian t) = C 12*X 0 := by
  simp [chartMixed, chartDq, Function.iterate_succ_apply', hamiltonian, ← qP_monomial,
    pderiv_mul, pderiv_pow, pderiv_C_mul, pderiv_X, Pi.single_apply, map_ofNat]
  ring

lemma chart_hamiltonian_03 (t : HamiltonianParameters K) :
    chartMixed 0 3 (hamiltonian t) = C 6 := by
  simp [chartMixed, Function.iterate_succ_apply', hamiltonian, ← qP_monomial,
    pderiv_mul, pderiv_pow, pderiv_C_mul, pderiv_X, Pi.single_apply, map_ofNat]
  ring

set_option maxHeartbeats 4000000 in
lemma chart_hamiltonian_50 (t : HamiltonianParameters K) :
    chartMixed 5 0 (hamiltonian t) = C (120*(t.b₃+t.c₅))+C 720*X 0 := by
  simp [chartMixed, chartDq, Function.iterate_succ_apply', hamiltonian, ← qP_monomial,
    pderiv_mul, pderiv_pow, pderiv_C_mul, pderiv_X, Pi.single_apply, map_ofNat]
  ring

set_option maxHeartbeats 2000000 in
lemma chart_hamiltonian_41 (t : HamiltonianParameters K) :
    chartMixed 4 1 (hamiltonian t) = C 72 := by
  simp [chartMixed, chartDq, Function.iterate_succ_apply', hamiltonian, ← qP_monomial,
    pderiv_mul, pderiv_pow, pderiv_C_mul, pderiv_X, Pi.single_apply, map_ofNat]
  ring

lemma chart_hamiltonian_32 (t : HamiltonianParameters K) :
    chartMixed 3 2 (hamiltonian t) = 0 := by
  simp [chartMixed, chartDq, Function.iterate_succ_apply', hamiltonian, ← qP_monomial,
    pderiv_mul, pderiv_pow, pderiv_C_mul, pderiv_X, Pi.single_apply, map_ofNat]

lemma chart_hamiltonian_23 (t : HamiltonianParameters K) :
    chartMixed 2 3 (hamiltonian t) = 0 := by
  simp [chartMixed, chartDq, Function.iterate_succ_apply', hamiltonian, ← qP_monomial,
    pderiv_mul, pderiv_pow, pderiv_C_mul, pderiv_X, Pi.single_apply, map_ofNat]

lemma chart_hamiltonian_14 (t : HamiltonianParameters K) :
    chartMixed 1 4 (hamiltonian t) = 0 := by
  simp [chartMixed, chartDq, Function.iterate_succ_apply', hamiltonian, ← qP_monomial,
    pderiv_mul, pderiv_pow, pderiv_C_mul, pderiv_X, Pi.single_apply, map_ofNat]

lemma chart_hamiltonian_05 (t : HamiltonianParameters K) :
    chartMixed 0 5 (hamiltonian t) = 0 := by
  simp [chartMixed, chartDq, Function.iterate_succ_apply', hamiltonian, ← qP_monomial,
    pderiv_mul, pderiv_pow, pderiv_C_mul, pderiv_X, Pi.single_apply, map_ofNat]

set_option maxHeartbeats 2000000 in
lemma chart_third_gate (t : HamiltonianParameters K) (f : Poly K) :
    chartContraction 3 (hamiltonian t) f = C (-6)*thirdGate t.toGateParameters f := by
  simp only [chartContraction, Finset.sum_range_succ, Finset.sum_range_zero]
  norm_num only [Nat.choose, Nat.sub_self, Nat.sub_zero, Nat.reduceSub, Nat.cast_ofNat,
    pow_zero, pow_one, neg_one_sq, one_mul, zero_add,
    chart_hamiltonian_30, chart_hamiltonian_21, chart_hamiltonian_12, chart_hamiltonian_03]
  simp [chartMixed, chartDq, Function.iterate_succ_apply', thirdGate,
    pderiv_mul, pderiv_C_mul, pderiv_X, Pi.single_apply, pderiv_P_q, map_ofNat]
  ring

lemma chart_fifth_gate (t : HamiltonianParameters K) (f : Poly K) :
    chartContraction 5 (hamiltonian t) f = C (-120)*fifthGate t.toGateParameters f := by
  simp only [chartContraction, Finset.sum_range_succ, Finset.sum_range_zero]
  norm_num only [Nat.choose, Nat.sub_self, Nat.sub_zero, Nat.reduceSub, Nat.cast_ofNat,
    pow_zero, pow_one, neg_one_sq, one_mul, zero_add,
    chart_hamiltonian_50, chart_hamiltonian_41, chart_hamiltonian_32,
    chart_hamiltonian_23, chart_hamiltonian_14, chart_hamiltonian_05, mul_zero, zero_mul, add_zero]
  simp [chartMixed, chartDq, Function.iterate_succ_apply', fifthGate, map_ofNat]
  ring

/-- Exact third flat-gate transport, for every polynomial partner. -/
theorem flat_third_gate_transport (t : HamiltonianParameters K) (f : Poly K) :
    flatContraction 3 (shear 1 (hamiltonian t)) (shear 1 f) =
      shear 1 (C (-6)*thirdGate t.toGateParameters f) := by
  rw [flatContraction_shear, chart_third_gate]

/-- Exact fifth flat-gate transport, for every polynomial partner. -/
theorem flat_fifth_gate_transport (t : HamiltonianParameters K) (f : Poly K) :
    flatContraction 5 (shear 1 (hamiltonian t)) (shear 1 f) =
      shear 1 (C (-120)*fifthGate t.toGateParameters f) := by
  rw [flatContraction_shear, chart_fifth_gate]

end SexticC3.CubeLeading.Polynomial
