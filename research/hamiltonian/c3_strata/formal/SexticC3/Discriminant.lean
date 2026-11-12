import SexticC3.DeltaData

namespace SexticC3

variable {R : Type*} [CommRing R]

/-- Remainder coefficients in increasing degree. -/
abbrev Remainder (R : Type*) := R × R × R × R × R

/-- Multiplication by x modulo the monic quintic. -/
def mulX (a b c d : R) (r : Remainder R) : Remainder R :=
  let (r₀,r₁,r₂,r₃,r₄) := r
  (-d*r₄, r₀-c*r₄, r₁-b*r₄, r₂-a*r₄, r₃)

def entries (r : Remainder R) : List R :=
  let (r₀,r₁,r₂,r₃,r₄) := r
  [r₀,r₁,r₂,r₃,r₄]

/-- Columns of multiplication by the derivative, stored as rows.
The determinant is unchanged by transposition. -/
def multiplicationRows (a b c d : R) : List (List R) :=
  let r₀ : Remainder R := (c, 2*b, 3*a, 0, 5)
  let r₁ := mulX a b c d r₀
  let r₂ := mulX a b c d r₁
  let r₃ := mulX a b c d r₂
  let r₄ := mulX a b c d r₃
  [r₀,r₁,r₂,r₃,r₄].map entries

/-- The signed column choices after a list of earlier selections.
The sign counts inversions against the earlier choices. -/
def choices (used : List Nat) : Nat → List (ℤ × List Nat)
  | 0 => [(1, [])]
  | n + 1 =>
    [0,1,2,3,4].flatMap fun j =>
      if used.contains j then [] else
        (choices (j :: used) n).map fun (s,js) =>
          (s * (-1)^used.countP (· > j), j :: js)

def firstColumn (j : Nat) : List (ℤ × List Nat) :=
  (choices [j] 4).map fun (s,js) => (s, j :: js)

def detPart (a b c d : R) (j : Nat) : R :=
  ((firstColumn j).map fun (s, js) =>
    (s : R) * ((multiplicationRows a b c d).zipWith
      (fun row index => row[index]?.getD 0) js).foldr (· * ·) 1).sum

/-- Determinant of multiplication by f' in the quintic remainder algebra.
The quintic discriminant sign (-1)^(5·4/2) is +1. -/
def derivativeMultiplicationDet (a b c d : R) : R :=
  detPart a b c d 0 + detPart a b c d 1 + detPart a b c d 2 +
    detPart a b c d 3 + detPart a b c d 4

set_option maxHeartbeats 2000000 in
private theorem part0 (a b c d : R) : detPart a b c d 0 = -12*a^4*b*c*d + 16*a^4*c^3 - 4*a^3*b^2*c^2 - 60*a^3*c*d^2 + 84*a^2*b*c^2*d - 128*a^2*c^4 - 81*a*b^3*c*d + 144*a*b^2*c^3 + 400*a*c^2*d^2 - 27*b^4*c^2 + 225*b^2*c*d^2 - 720*b*c^3*d + 256*c^5 := by
  have h : firstColumn 0 = [
    (1, [0, 1, 2, 3, 4]), (-1, [0, 1, 2, 4, 3]), (-1, [0, 1, 3, 2, 4]), (1, [0, 1, 3, 4, 2]),
    (1, [0, 1, 4, 2, 3]), (-1, [0, 1, 4, 3, 2]), (-1, [0, 2, 1, 3, 4]), (1, [0, 2, 1, 4, 3]),
    (1, [0, 2, 3, 1, 4]), (-1, [0, 2, 3, 4, 1]), (-1, [0, 2, 4, 1, 3]), (1, [0, 2, 4, 3, 1]),
    (1, [0, 3, 1, 2, 4]), (-1, [0, 3, 1, 4, 2]), (-1, [0, 3, 2, 1, 4]), (1, [0, 3, 2, 4, 1]),
    (1, [0, 3, 4, 1, 2]), (-1, [0, 3, 4, 2, 1]), (-1, [0, 4, 1, 2, 3]), (1, [0, 4, 1, 3, 2]),
    (1, [0, 4, 2, 1, 3]), (-1, [0, 4, 2, 3, 1]), (-1, [0, 4, 3, 1, 2]), (1, [0, 4, 3, 2, 1])] := by decide
  norm_num [detPart, h, multiplicationRows, mulX, entries, List.foldr] <;> ring

set_option maxHeartbeats 2000000 in
private theorem part1 (a b c d : R) : detPart a b c d 1 = -48*a^4*b*c*d + 16*a^3*b^3*d + 160*a^2*b^2*d^2 + 352*a^2*b*c^2*d - 468*a*b^3*c*d - 500*a*b*d^3 + 108*b^5*d + 1200*b^2*c*d^2 - 640*b*c^3*d := by
  have h : firstColumn 1 = [
    (-1, [1, 0, 2, 3, 4]), (1, [1, 0, 2, 4, 3]), (1, [1, 0, 3, 2, 4]), (-1, [1, 0, 3, 4, 2]),
    (-1, [1, 0, 4, 2, 3]), (1, [1, 0, 4, 3, 2]), (1, [1, 2, 0, 3, 4]), (-1, [1, 2, 0, 4, 3]),
    (-1, [1, 2, 3, 0, 4]), (1, [1, 2, 3, 4, 0]), (1, [1, 2, 4, 0, 3]), (-1, [1, 2, 4, 3, 0]),
    (-1, [1, 3, 0, 2, 4]), (1, [1, 3, 0, 4, 2]), (1, [1, 3, 2, 0, 4]), (-1, [1, 3, 2, 4, 0]),
    (-1, [1, 3, 4, 0, 2]), (1, [1, 3, 4, 2, 0]), (1, [1, 4, 0, 2, 3]), (-1, [1, 4, 0, 3, 2]),
    (-1, [1, 4, 2, 0, 3]), (1, [1, 4, 2, 3, 0]), (1, [1, 4, 3, 0, 2]), (-1, [1, 4, 3, 2, 0])] := by decide
  norm_num [detPart, h, multiplicationRows, mulX, entries, List.foldr] <;> ring

set_option maxHeartbeats 2000000 in
private theorem part2 (a b c d : R) : detPart a b c d 2 = 108*a^5*d^2 - 12*a^4*b*c*d - 780*a^3*c*d^2 + 585*a^2*b^2*d^2 + 144*a^2*b*c^2*d - 81*a*b^3*c*d - 1125*a*b*d^3 + 1200*a*c^2*d^2 := by
  have h : firstColumn 2 = [
    (1, [2, 0, 1, 3, 4]), (-1, [2, 0, 1, 4, 3]), (-1, [2, 0, 3, 1, 4]), (1, [2, 0, 3, 4, 1]),
    (1, [2, 0, 4, 1, 3]), (-1, [2, 0, 4, 3, 1]), (-1, [2, 1, 0, 3, 4]), (1, [2, 1, 0, 4, 3]),
    (1, [2, 1, 3, 0, 4]), (-1, [2, 1, 3, 4, 0]), (-1, [2, 1, 4, 0, 3]), (1, [2, 1, 4, 3, 0]),
    (1, [2, 3, 0, 1, 4]), (-1, [2, 3, 0, 4, 1]), (-1, [2, 3, 1, 0, 4]), (1, [2, 3, 1, 4, 0]),
    (1, [2, 3, 4, 0, 1]), (-1, [2, 3, 4, 1, 0]), (-1, [2, 4, 0, 1, 3]), (1, [2, 4, 0, 3, 1]),
    (1, [2, 4, 1, 0, 3]), (-1, [2, 4, 1, 3, 0]), (-1, [2, 4, 3, 0, 1]), (1, [2, 4, 3, 1, 0])] := by decide
  norm_num [detPart, h, multiplicationRows, mulX, entries, List.foldr] <;> ring

set_option maxHeartbeats 2000000 in
private theorem part3 (a b c d : R) : detPart a b c d 3 = 0 := by
  have h : firstColumn 3 = [
    (-1, [3, 0, 1, 2, 4]), (1, [3, 0, 1, 4, 2]), (1, [3, 0, 2, 1, 4]), (-1, [3, 0, 2, 4, 1]),
    (-1, [3, 0, 4, 1, 2]), (1, [3, 0, 4, 2, 1]), (1, [3, 1, 0, 2, 4]), (-1, [3, 1, 0, 4, 2]),
    (-1, [3, 1, 2, 0, 4]), (1, [3, 1, 2, 4, 0]), (1, [3, 1, 4, 0, 2]), (-1, [3, 1, 4, 2, 0]),
    (-1, [3, 2, 0, 1, 4]), (1, [3, 2, 0, 4, 1]), (1, [3, 2, 1, 0, 4]), (-1, [3, 2, 1, 4, 0]),
    (-1, [3, 2, 4, 0, 1]), (1, [3, 2, 4, 1, 0]), (1, [3, 4, 0, 1, 2]), (-1, [3, 4, 0, 2, 1]),
    (-1, [3, 4, 1, 0, 2]), (1, [3, 4, 1, 2, 0]), (1, [3, 4, 2, 0, 1]), (-1, [3, 4, 2, 1, 0])] := by decide
  norm_num [detPart, h, multiplicationRows, mulX, entries, List.foldr] <;> ring

set_option maxHeartbeats 2000000 in
private theorem part4 (a b c d : R) : detPart a b c d 4 = -60*a^3*c*d^2 + 80*a^2*b^2*d^2 - 20*a^2*b*c^2*d - 2125*a*b*d^3 + 400*a*c^2*d^2 + 825*b^2*c*d^2 - 240*b*c^3*d + 3125*d^4 := by
  have h : firstColumn 4 = [
    (1, [4, 0, 1, 2, 3]), (-1, [4, 0, 1, 3, 2]), (-1, [4, 0, 2, 1, 3]), (1, [4, 0, 2, 3, 1]),
    (1, [4, 0, 3, 1, 2]), (-1, [4, 0, 3, 2, 1]), (-1, [4, 1, 0, 2, 3]), (1, [4, 1, 0, 3, 2]),
    (1, [4, 1, 2, 0, 3]), (-1, [4, 1, 2, 3, 0]), (-1, [4, 1, 3, 0, 2]), (1, [4, 1, 3, 2, 0]),
    (1, [4, 2, 0, 1, 3]), (-1, [4, 2, 0, 3, 1]), (-1, [4, 2, 1, 0, 3]), (1, [4, 2, 1, 3, 0]),
    (1, [4, 2, 3, 0, 1]), (-1, [4, 2, 3, 1, 0]), (-1, [4, 3, 0, 1, 2]), (1, [4, 3, 0, 2, 1]),
    (1, [4, 3, 1, 0, 2]), (-1, [4, 3, 1, 2, 0]), (-1, [4, 3, 2, 0, 1]), (1, [4, 3, 2, 1, 0])] := by decide
  norm_num [detPart, h, multiplicationRows, mulX, entries, List.foldr] <;> ring

theorem delta_eq_derivativeMultiplicationDet (a b c d : R) :
    delta a b c d = derivativeMultiplicationDet a b c d := by
  simp only [delta, derivativeMultiplicationDet, part0, part1, part2, part3, part4]
  ring

end SexticC3
