import SexticC3.TargetRootMultiplicity
import SexticC3.Discriminant
import Mathlib.FieldTheory.Separable
import Mathlib.LinearAlgebra.Matrix.Determinant.Basic
import Mathlib.Data.Matrix.Notation

noncomputable section

namespace SexticC3.StaticTail

open Polynomial

variable {K : Type*} [Field K] [CharZero K]

private def companion (a b c d : K) : Matrix (Fin 5) (Fin 5) K :=
  !![0, 1, 0, 0, 0;
     0, 0, 1, 0, 0;
     0, 0, 0, 1, 0;
     0, 0, 0, 0, 1;
    -d,-c,-b,-a, 0]

private def derivativeMatrix (a b c d : K) : Matrix (Fin 5) (Fin 5) K :=
  !![c, 2*b, 3*a, 0, 5;
    -5*d, -4*c, -3*b, -2*a, 0;
    0, -5*d, -4*c, -3*b, -2*a;
    2*a*d, 2*a*c, 2*a*b - 5*d, 2*a^2 - 4*c, -3*b;
    3*b*d, 2*a*d + 3*b*c, 2*a*c + 3*b^2, 5*a*b - 5*d, 2*a^2 - 4*c]

private theorem companion_pow_2 (a b c d : K) :
    companion a b c d ^ 2 = !![0, 0, 1, 0, 0;
    0, 0, 0, 1, 0;
    0, 0, 0, 0, 1;
    -d, -c, -b, -a, 0;
    0, -d, -c, -b, -a] := by
  rw [show companion a b c d ^ 2 = companion a b c d ^ 1 * companion a b c d from pow_succ _ _, pow_one]
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [companion, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

private theorem companion_pow_3 (a b c d : K) :
    companion a b c d ^ 3 = !![0, 0, 0, 1, 0;
    0, 0, 0, 0, 1;
    -d, -c, -b, -a, 0;
    0, -d, -c, -b, -a;
    a*d, a*c, a*b - d, a^2 - c, -b] := by
  rw [show companion a b c d ^ 3 = companion a b c d ^ 2 * companion a b c d from pow_succ _ _, companion_pow_2]
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [companion, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

private theorem companion_pow_4 (a b c d : K) :
    companion a b c d ^ 4 = !![0, 0, 0, 0, 1;
    -d, -c, -b, -a, 0;
    0, -d, -c, -b, -a;
    a*d, a*c, a*b - d, a^2 - c, -b;
    b*d, a*d + b*c, a*c + b^2, 2*a*b - d, a^2 - c] := by
  rw [show companion a b c d ^ 4 = companion a b c d ^ 3 * companion a b c d from pow_succ _ _, companion_pow_3]
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [companion, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

private theorem companion_pow_5 (a b c d : K) :
    companion a b c d ^ 5 = !![-d, -c, -b, -a, 0;
    0, -d, -c, -b, -a;
    a*d, a*c, a*b - d, a^2 - c, -b;
    b*d, a*d + b*c, a*c + b^2, 2*a*b - d, a^2 - c;
    -a^2*d + c*d, -a^2*c + b*d + c^2, -a^2*b + a*d + 2*b*c, -a^3 + 2*a*c + b^2, 2*a*b - d] := by
  rw [show companion a b c d ^ 5 = companion a b c d ^ 4 * companion a b c d from pow_succ _ _, companion_pow_4]
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [companion, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

set_option maxHeartbeats 4000000 in
private theorem chartQuintic_aeval_companion (a b c d : K) :
    aeval (companion a b c d) (chartQuintic a b c d) = 0 := by
  simp only [chartQuintic, map_add, map_mul, map_pow, aeval_X, aeval_C]
  rw [companion_pow_5, companion_pow_3, companion_pow_2]
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [companion, Matrix.mul_apply, Fin.sum_univ_succ,
      Matrix.algebraMap_matrix_apply, Matrix.add_apply, Matrix.zero_apply, Matrix.one_apply] <;> ring

set_option maxHeartbeats 4000000 in
private theorem derivative_aeval_companion (a b c d : K) :
    aeval (companion a b c d) (derivative (chartQuintic a b c d)) =
      derivativeMatrix a b c d := by
  have hd : derivative (chartQuintic a b c d) =
      C (5 : K)*X^4 + C (3*a)*X^2 + C (2*b)*X + C c := by
    norm_num [chartQuintic, derivative_add, derivative_C_mul, derivative_X_pow, map_ofNat, map_mul]
    ring
  rw [hd]
  simp only [map_add, map_mul, map_pow, aeval_X, aeval_C]
  rw [companion_pow_4, companion_pow_2]
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [companion, derivativeMatrix, Matrix.mul_apply,
      Fin.sum_univ_succ, Matrix.algebraMap_matrix_apply, Matrix.add_apply,
      Matrix.zero_apply, Matrix.one_apply] <;> ring

set_option maxHeartbeats 1000000 in
private theorem det_four (M : Matrix (Fin 4) (Fin 4) K) :
    M.det = M 0 0 * (M.submatrix Fin.succ (0 : Fin 4).succAbove).det -
      M 0 1 * (M.submatrix Fin.succ (1 : Fin 4).succAbove).det +
      M 0 2 * (M.submatrix Fin.succ (2 : Fin 4).succAbove).det -
      M 0 3 * (M.submatrix Fin.succ (3 : Fin 4).succAbove).det := by
  rw [Matrix.det_succ_row_zero]
  norm_num [Fin.sum_univ_succ, show (2 : Fin 3).succ = (3 : Fin 4) by rfl]
  ring

set_option maxHeartbeats 1000000 in
private theorem det_five (M : Matrix (Fin 5) (Fin 5) K) :
    M.det = M 0 0 * (M.submatrix Fin.succ (0 : Fin 5).succAbove).det -
      M 0 1 * (M.submatrix Fin.succ (1 : Fin 5).succAbove).det +
      M 0 2 * (M.submatrix Fin.succ (2 : Fin 5).succAbove).det -
      M 0 3 * (M.submatrix Fin.succ (3 : Fin 5).succAbove).det +
      M 0 4 * (M.submatrix Fin.succ (4 : Fin 5).succAbove).det := by
  rw [Matrix.det_succ_row_zero]
  norm_num [Fin.sum_univ_succ, show (2 : Fin 3).succ = (3 : Fin 4) by rfl,
    show (3 : Fin 4).succ = (4 : Fin 5) by rfl,
    show (2 : Fin 4).succ = (3 : Fin 5) by rfl]
  ring

set_option maxHeartbeats 4000000 in
private theorem delta_eq_det_derivativeMatrix (a b c d : K) :
    delta a b c d = (derivativeMatrix a b c d).det := by
  have entry00 : derivativeMatrix a b c d (0 : Fin 5) (0 : Fin 5) = c := rfl
  have entry01 : derivativeMatrix a b c d (0 : Fin 5) (1 : Fin 5) = 2*b := rfl
  have entry02 : derivativeMatrix a b c d (0 : Fin 5) (2 : Fin 5) = 3*a := rfl
  have entry03 : derivativeMatrix a b c d (0 : Fin 5) (3 : Fin 5) = 0 := rfl
  have entry04 : derivativeMatrix a b c d (0 : Fin 5) (4 : Fin 5) = 5 := rfl
  have entry10 : derivativeMatrix a b c d (1 : Fin 5) (0 : Fin 5) = -5*d := rfl
  have entry11 : derivativeMatrix a b c d (1 : Fin 5) (1 : Fin 5) = -4*c := rfl
  have entry12 : derivativeMatrix a b c d (1 : Fin 5) (2 : Fin 5) = -3*b := rfl
  have entry13 : derivativeMatrix a b c d (1 : Fin 5) (3 : Fin 5) = -2*a := rfl
  have entry14 : derivativeMatrix a b c d (1 : Fin 5) (4 : Fin 5) = 0 := rfl
  have entry20 : derivativeMatrix a b c d (2 : Fin 5) (0 : Fin 5) = 0 := rfl
  have entry21 : derivativeMatrix a b c d (2 : Fin 5) (1 : Fin 5) = -5*d := rfl
  have entry22 : derivativeMatrix a b c d (2 : Fin 5) (2 : Fin 5) = -4*c := rfl
  have entry23 : derivativeMatrix a b c d (2 : Fin 5) (3 : Fin 5) = -3*b := rfl
  have entry24 : derivativeMatrix a b c d (2 : Fin 5) (4 : Fin 5) = -2*a := rfl
  have entry30 : derivativeMatrix a b c d (3 : Fin 5) (0 : Fin 5) = 2*a*d := rfl
  have entry31 : derivativeMatrix a b c d (3 : Fin 5) (1 : Fin 5) = 2*a*c := rfl
  have entry32 : derivativeMatrix a b c d (3 : Fin 5) (2 : Fin 5) = 2*a*b - 5*d := rfl
  have entry33 : derivativeMatrix a b c d (3 : Fin 5) (3 : Fin 5) = 2*a^2 - 4*c := rfl
  have entry34 : derivativeMatrix a b c d (3 : Fin 5) (4 : Fin 5) = -3*b := rfl
  have entry40 : derivativeMatrix a b c d (4 : Fin 5) (0 : Fin 5) = 3*b*d := rfl
  have entry41 : derivativeMatrix a b c d (4 : Fin 5) (1 : Fin 5) = 2*a*d + 3*b*c := rfl
  have entry42 : derivativeMatrix a b c d (4 : Fin 5) (2 : Fin 5) = 2*a*c + 3*b^2 := rfl
  have entry43 : derivativeMatrix a b c d (4 : Fin 5) (3 : Fin 5) = 5*a*b - 5*d := rfl
  have entry44 : derivativeMatrix a b c d (4 : Fin 5) (4 : Fin 5) = 2*a^2 - 4*c := rfl
  have next4_0 : (0 : Fin 3).succ = (1 : Fin 4) := rfl
  have next4_1 : (1 : Fin 3).succ = (2 : Fin 4) := rfl
  have next4_2 : (2 : Fin 3).succ = (3 : Fin 4) := rfl
  have skip4_0_0 : (0 : Fin 4).succAbove (0 : Fin 3) = (1 : Fin 4) := rfl
  have skip4_0_1 : (0 : Fin 4).succAbove (1 : Fin 3) = (2 : Fin 4) := rfl
  have skip4_0_2 : (0 : Fin 4).succAbove (2 : Fin 3) = (3 : Fin 4) := rfl
  have skip4_1_0 : (1 : Fin 4).succAbove (0 : Fin 3) = (0 : Fin 4) := rfl
  have skip4_1_1 : (1 : Fin 4).succAbove (1 : Fin 3) = (2 : Fin 4) := rfl
  have skip4_1_2 : (1 : Fin 4).succAbove (2 : Fin 3) = (3 : Fin 4) := rfl
  have skip4_2_0 : (2 : Fin 4).succAbove (0 : Fin 3) = (0 : Fin 4) := rfl
  have skip4_2_1 : (2 : Fin 4).succAbove (1 : Fin 3) = (1 : Fin 4) := rfl
  have skip4_2_2 : (2 : Fin 4).succAbove (2 : Fin 3) = (3 : Fin 4) := rfl
  have skip4_3_0 : (3 : Fin 4).succAbove (0 : Fin 3) = (0 : Fin 4) := rfl
  have skip4_3_1 : (3 : Fin 4).succAbove (1 : Fin 3) = (1 : Fin 4) := rfl
  have skip4_3_2 : (3 : Fin 4).succAbove (2 : Fin 3) = (2 : Fin 4) := rfl
  have next5_0 : (0 : Fin 4).succ = (1 : Fin 5) := rfl
  have next5_1 : (1 : Fin 4).succ = (2 : Fin 5) := rfl
  have next5_2 : (2 : Fin 4).succ = (3 : Fin 5) := rfl
  have next5_3 : (3 : Fin 4).succ = (4 : Fin 5) := rfl
  have skip5_0_0 : (0 : Fin 5).succAbove (0 : Fin 4) = (1 : Fin 5) := rfl
  have skip5_0_1 : (0 : Fin 5).succAbove (1 : Fin 4) = (2 : Fin 5) := rfl
  have skip5_0_2 : (0 : Fin 5).succAbove (2 : Fin 4) = (3 : Fin 5) := rfl
  have skip5_0_3 : (0 : Fin 5).succAbove (3 : Fin 4) = (4 : Fin 5) := rfl
  have skip5_1_0 : (1 : Fin 5).succAbove (0 : Fin 4) = (0 : Fin 5) := rfl
  have skip5_1_1 : (1 : Fin 5).succAbove (1 : Fin 4) = (2 : Fin 5) := rfl
  have skip5_1_2 : (1 : Fin 5).succAbove (2 : Fin 4) = (3 : Fin 5) := rfl
  have skip5_1_3 : (1 : Fin 5).succAbove (3 : Fin 4) = (4 : Fin 5) := rfl
  have skip5_2_0 : (2 : Fin 5).succAbove (0 : Fin 4) = (0 : Fin 5) := rfl
  have skip5_2_1 : (2 : Fin 5).succAbove (1 : Fin 4) = (1 : Fin 5) := rfl
  have skip5_2_2 : (2 : Fin 5).succAbove (2 : Fin 4) = (3 : Fin 5) := rfl
  have skip5_2_3 : (2 : Fin 5).succAbove (3 : Fin 4) = (4 : Fin 5) := rfl
  have skip5_3_0 : (3 : Fin 5).succAbove (0 : Fin 4) = (0 : Fin 5) := rfl
  have skip5_3_1 : (3 : Fin 5).succAbove (1 : Fin 4) = (1 : Fin 5) := rfl
  have skip5_3_2 : (3 : Fin 5).succAbove (2 : Fin 4) = (2 : Fin 5) := rfl
  have skip5_3_3 : (3 : Fin 5).succAbove (3 : Fin 4) = (4 : Fin 5) := rfl
  have skip5_4_0 : (4 : Fin 5).succAbove (0 : Fin 4) = (0 : Fin 5) := rfl
  have skip5_4_1 : (4 : Fin 5).succAbove (1 : Fin 4) = (1 : Fin 5) := rfl
  have skip5_4_2 : (4 : Fin 5).succAbove (2 : Fin 4) = (2 : Fin 5) := rfl
  have skip5_4_3 : (4 : Fin 5).succAbove (3 : Fin 4) = (3 : Fin 5) := rfl
  simp only [det_five, det_four, Matrix.det_fin_three, Matrix.submatrix_apply,
    next4_0, next4_1, next4_2, skip4_0_0, skip4_0_1, skip4_0_2, skip4_1_0, skip4_1_1,
    skip4_1_2, skip4_2_0, skip4_2_1, skip4_2_2, skip4_3_0, skip4_3_1, skip4_3_2, next5_0,
    next5_1, next5_2, next5_3, skip5_0_0, skip5_0_1, skip5_0_2, skip5_0_3, skip5_1_0,
    skip5_1_1, skip5_1_2, skip5_1_3, skip5_2_0, skip5_2_1, skip5_2_2, skip5_2_3, skip5_3_0,
    skip5_3_1, skip5_3_2, skip5_3_3, skip5_4_0, skip5_4_1, skip5_4_2, skip5_4_3]
  simp only [entry00, entry01, entry02, entry03, entry04, entry10, entry11, entry12, entry13, entry14, entry20, entry21,
    entry22, entry23, entry24, entry30, entry31, entry32, entry33, entry34, entry40, entry41, entry42, entry43, entry44]
  unfold delta
  ring

/-- Coprimality of a normalized chart quintic with its derivative forces
the stored discriminant to be nonzero. -/
theorem delta_ne_zero_of_separable (a b c d : K) (h : (chartQuintic a b c d).Separable) :
    delta a b c d ≠ 0 := by
  obtain ⟨U, V, hUV⟩ := h
  have hmat := congrArg (aeval (companion a b c d)) hUV
  simp only [map_add, map_mul, map_one, chartQuintic_aeval_companion,
    derivative_aeval_companion, mul_zero, zero_add] at hmat
  have hdet := congrArg Matrix.det hmat
  simp only [Matrix.det_mul, Matrix.det_one] at hdet
  rw [delta_eq_det_derivativeMatrix]
  intro hz
  rw [hz, mul_zero] at hdet
  exact zero_ne_one hdet

end SexticC3.StaticTail
