import SexticC3.StaticTail

namespace SexticC3.StaticTail

variable {R S : Type*} [CommRing R] [CommRing S]

theorem map_hCoeff (f : R →+* S) (a b c d : R) (i : ℕ) :
    f (hCoeff a b c d i) = hCoeff (f a) (f b) (f c) (f d) i := by
  unfold hCoeff
  split <;> simp

theorem map_rowValue (f : R →+* S) (a b c d : R) (n : ℕ)
    (r : Row) (g : ℕ → R) :
    f (rowValue a b c d n r g) =
      rowValue (f a) (f b) (f c) (f d) n r (fun j => f (g j)) := by
  unfold rowValue
  generalize rowTerms n r = ts
  induction ts with
  | nil => simp
  | cons t ts ih =>
    have hm : f ((Option.map (hCoeff a b c d) t.inner).getD 1) =
        (Option.map (hCoeff (f a) (f b) (f c) (f d)) t.inner).getD 1 := by
      cases t.inner <;> simp [map_hCoeff]
    simp only [List.map_cons, List.sum_cons, map_add, map_mul, map_intCast, map_hCoeff, hm, ih]

theorem map_delta (f : R →+* S) (a b c d : R) :
    f (delta a b c d) = delta (f a) (f b) (f c) (f d) := by
  simp [delta, map_ofNat]

end SexticC3.StaticTail
