# Lean bridge for squarefree sextic certificates

This is an optional Lean 4.19.0 / Mathlib v4.19.0 project next to the
maintained Python verifier. The source is the repository's
`squarefree-sextic-discriminant-v1` certificate at main commit
`f122ebc948ac5ddc296fc805d40fa50f0c565c94`. Its SHA-256 with LF line endings is
`2faae6b7a3e9d1202fb6e9f9d6f645a37a6f18e865c42a0bb5aa2f065a12462a`.

## What is represented

The certificate encodes each polynomial as a list of exponent vectors in
`(a,b,c,d)` order paired with exact rational strings. The translator emits
polynomial expressions in four indeterminates, interpreted in an arbitrary
characteristic-zero field. Each normalization by Mathlib's `ring` tactic
produces a proof term checked by the Lean kernel. An intermediate node uses
only earlier nodes or selected residual minors. The final equality is also
expanded into a direct linear combination of the selected generators.

The partner basis has column `j` equal to `q^j p^(n-j)`. The Hamiltonian is
`q p^5 + a q^3 p^3 + b q^4 p^2 + c q^5 p + d q^6`. Rows use iterate depth,
gate order, q exponent and p exponent in that order. Lean computes a
monomial coefficient by applying the falling factors for each derivative
and multiplying by the signed binomial coefficient, using the unnormalized
transvectant convention. At depth one it composes that coefficient
formula with the first transvectant, which raises degree by four.

The existing independent verifier rebuilds the four gate blocks by literal
symbolic differentiation, checks the triangular pivots and lift, recomputes
the discriminant, and replays the intermediate and final identities. The
translator uses its row expressions as normalization hints. Each hint is
then an equality that Lean proves from its own coefficient formula. The
parser and transcriber determine which certificate data are represented. The
generated identities and kernel bounds are proved from their Lean definitions.

Degree six is the smallest record by number of generators, number of
intermediate identities, and serialized size. It uses four order-one
generators, four intermediate identities, and five triangular pivots. The
second lifted column is the Hamiltonian. Lean derives the four generators
\(1080a^2+7200c\), \(17280ab+864000d\), \(51840a\), and \(259200b\)
from the recorded lift and the recomputed rows.

Across degrees 1 through 16, Lean checks 185 selected generators,
151 intermediate identities, and 16 discriminant identities. The
degree-two pivot occurs in the depth-one \(T_3D_H\) block because the
static pivot vanishes. All final identities use the first power of the
discriminant. The representation is a polynomial linear combination
verified over every characteristic-zero field.

`finite_kernel_bound` combines all 16 degree-specific bounds. Under
a nonzero discriminant, the finite gate kernels are zero in degrees
1 through 16 except degree six, where the kernel is the span of the
normalized Hamiltonian. These conclusions concern coordinates `0`
through `n`, the homogeneous partner basis.

`Exceptional411` independently evaluates the contractions for
\(H=q^4p^2+\delta q^6\) and \(G=qp\). It verifies both gates on
\(G\) and \(D_HG\), then checks the nonzero second-iterate coefficient
\(-82944\delta\) when \(\delta\ne0\).

The discriminant calculation constructs multiplication by \(f'\) modulo
the monic quintic \(f=x^5+ax^3+bx^2+cx+d\). It checks the signed determinant
expansion and its equality to the stored polynomial. The determinant of
that multiplication map is the monic resultant, and the quintic sign
\((-1)^{5\cdot4/2}\) is positive. The general algebraic identification with
Mathlib polynomial roots is a separate dependency.

## Reproduction

From this directory with elan installed:

```sh
lake exe cache get Mathlib.Tactic.NormNum Mathlib.Tactic.Ring Mathlib.Tactic.LinearCombination Mathlib.Data.Nat.Choose.Basic
lake build
lake env lean Audit.lean
```

The audit fails if a checked declaration uses any axiom outside
`propext`, `Classical.choice` and `Quot.sound`. It also checks
`Degree6.lift1_eq_hCoeff`, which identifies the lift used by the upper bound
with the Hamiltonian used by the converse.

To regenerate the checked-in Lean statements, install SymPy 1.14.0 and
run `python generate.py`. Building the Lean project does not run Python.

## Verification scope

`Audit.lean` checks the finite identities and kernel bounds, the aggregate
bound, and the exceptional iterate and gate calculations. The existing
Python verifier independently replays all sixteen squarefree records.
The remaining geometric and all-degree dependencies are listed in
[THEOREM_BOUNDARY.md](THEOREM_BOUNDARY.md).
