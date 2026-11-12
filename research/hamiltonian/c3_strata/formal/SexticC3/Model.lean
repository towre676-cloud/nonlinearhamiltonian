import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring
import Mathlib.Tactic.LinearCombination
import Mathlib.Data.Nat.Choose.Basic

namespace SexticC3

structure Row where
  depth : Bool
  order : Nat
  qPower : Nat
  pPower : Nat

/-- Coefficient of the r-th derivative of a monomial of exponent e. -/
def falling : Nat → Nat → Nat
  | _, 0 => 1
  | e, r + 1 => e * falling (e - 1) r

/-- The scalar in the unnormalized transvectant on two monomials.
The first monomial has exponents (i, 6-i), the second (j, n-j). -/
def weight (k i n j : Nat) : ℤ :=
  ((List.range (k + 1)).map fun s =>
    (-1 : ℤ)^s * (Nat.choose k s : ℤ) *
    (falling i (k-s) : ℤ) * (falling (6-i) s : ℤ) *
    (falling j s : ℤ) * (falling (n-j) (k-s) : ℤ)).sum

def monomialRow (k u v i n j : Nat) : ℤ :=
  if i+j = u+k ∧ (6-i)+(n-j) = v+k then weight k i n j else 0

def sexticExponents : List Nat := [1, 3, 4, 5, 6]

structure RowTerm where
  partner : Nat
  outer : Nat
  inner : Option Nat
  scalar : ℤ
  deriving DecidableEq

/-- Total-degree support of a homogeneous gate output. -/
def inDegree (n : Nat) (r : Row) : Prop :=
  r.qPower + r.pPower + 2*r.order = 6+n+(if r.depth then 4 else 0)

instance (n : Nat) (r : Row) : Decidable (inDegree n r) :=
  inferInstanceAs (Decidable (_ = _))

/-- A sparse integer tensor for the coefficient row, before inserting a,b,c,d.
The dynamic row composes the static contraction with T₁ on each basis vector. -/
def rowTerms (n : Nat) (r : Row) : List RowTerm :=
  if ¬ inDegree n r then [] else
  let terms : List RowTerm := (List.range (n+1)).flatMap fun j =>
    sexticExponents.flatMap fun i =>
      if r.depth then
        sexticExponents.map fun h =>
          ⟨j, i, some h, weight 1 h n j *
            monomialRow r.order r.qPower r.pPower i (n+4) (h+j-1)⟩
      else
        [⟨j, i, none, monomialRow r.order r.qPower r.pPower i n j⟩]
  terms.filter (·.scalar != 0)

variable {R : Type*} [CommRing R]

/-- Coefficient of q^i p^(6-i) in the normalized Hamiltonian. -/
def hCoeff (a b c d : R) : Nat → R
  | 1 => 1
  | 3 => a
  | 4 => b
  | 5 => c
  | 6 => d
  | _ => 0

def rowValue (a b c d : R) (n : Nat) (r : Row) (g : Nat → R) : R :=
  ((rowTerms n r).map fun t =>
    (t.scalar : R) * hCoeff a b c d t.outer *
      (t.inner.map (hCoeff a b c d)).getD 1 * g t.partner).sum

theorem rowValue_outside_degree (a b c d : R) (n : Nat) (r : Row) (g : Nat → R)
    (h : ¬ inDegree n r) : rowValue a b c d n r g = 0 := by
  simp [rowValue, rowTerms, h]

def IsKernel (a b c d : R) (n : Nat) (g : Nat → R) : Prop :=
  ∀ r : Row, (r.order = 3 ∨ r.order = 5) → rowValue a b c d n r g = 0

/-- The ordered two-by-two determinant used by the certificate. -/
def minor (a₀ a₁ b₀ b₁ : R) : R := a₀ * b₁ - a₁ * b₀

theorem minor_mul_eq_zero {a₀ a₁ b₀ b₁ x y : R}
    (ha : a₀*x + a₁*y = 0) (hb : b₀*x + b₁*y = 0) :
    minor a₀ a₁ b₀ b₁ * x = 0 ∧ minor a₀ a₁ b₀ b₁ * y = 0 := by
  unfold minor
  constructor
  · linear_combination b₁ * ha - a₁ * hb
  · linear_combination a₀ * hb - b₀ * ha

end SexticC3
