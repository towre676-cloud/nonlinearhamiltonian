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
trust boundary includes the JSON parser and the source transcription from
the pinned byte stream.

Degree six is the smallest record by number of generators, number of
intermediate identities, and serialized size. It uses four order-one
generators, four intermediate identities, and five triangular pivots. The
second lifted column is the Hamiltonian. Lean derives the four generators
\(1080a^2+7200c\), \(17280ab+864000d\), \(51840a\), and \(259200b\)
from the recorded lift and the recomputed rows.

| Degree | Selected generators | Intermediate identities | Constant pivots |
| --- | ---: | ---: | ---: |
| 6 | 4 order-one entries | 4 | 5 |
| 1 | 21 order-two minors | 10 | 0 |
| 2 | 15 order-two minors | 9 | 1 |

The degree-two pivot occurs in the depth-one \(T_3D_H\) block because the
static pivot vanishes. All three final identities use the first power of
the discriminant. The representation is a polynomial linear combination
verified over every characteristic-zero field. The Lean declarations use
coefficient functions and field identities as their interface.

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

To regenerate the checked-in Lean statements, install SymPy 1.14.0 and
run `python generate.py`. Building the Lean project does not run Python.

## Local verification

Lean 4.19.0 compiled all project modules and `Audit.lean`. The eleven audited
theorems depend only on `propext`, `Classical.choice` and `Quot.sound`.
The finite gate kernels under a nonzero discriminant are zero in degrees one
and two and the span of the normalized Hamiltonian in degree six. The
existing Python verifier independently replayed all sixteen records, and the
eleven squarefree and four strata tests passed. The generated Lean files
were byte-identical on regeneration.
