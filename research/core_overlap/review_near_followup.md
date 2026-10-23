# Bounded review of Claude's subsequent near-edge theorem

This read-only follow-up inspected commit
`268d553eb6a4434afeaf5fcb4689a6294e5ab688`, specifically Theorem NE in
`programmes/DYNAMIC_CORE_RESULTS.md` section 6.7 and the new checker
`extensions/hamiltonian/check_near_edges.py`. It supplements the overlap
review; it is not a claim that the remaining pure-top conjecture is true.

**Assessment:** the near-top theorem is supported by the determinant
identities and the filtration argument, subject to the two explicit proof
clarifications below. Neither clarification supplies a counterexample to
Theorem NE. The unrestricted pure-top conjecture still has the exact
counterexamples recorded in the overlap package.

The checker was extracted, unchanged, with its PBW arithmetic dependency
to a temporary directory. Its full replay passed: `E1`, `E2`,
`E2_at1`, `E3`, and `E4`, including 150 direct operator grid checks.
The run took approximately 0.44 seconds. No current worktree source file
was overwritten during this review.

## First-edge and lattice issues

The first edge has a strictly positive weight. A lower monomial of
transverse exponent at most one cannot tie `m ell^(d-1)` as the ratio of
the positive weights is decreased from one. A non-affine monomial has
exponent at least two and ties at a positive ratio below one. Thus the
primitive edge step `(a,-b)` satisfies `b>a>=1`.

A weight-homogeneous polynomial is supported on a single primitive
lattice line. Its total-degree top lies in the near monomial core
`K[ell]+mK[ell]`, so it has one of the two stated types. Different
transverse congruence classes, including the two possibilities when the
primitive step has transverse size greater than one, are precisely the
separate alpha and beta cases. No half-integer step or unaccounted coset
is needed.

The determinant at fixed edge parameters is a nonzero polynomial in the
top ordinary degree `N`. Its displayed leading coefficient is nonzero
for all admissible integer parameters. It therefore has only finitely
many exceptional degrees. An explicit uniform bound in all edge
parameters is not needed for the finiteness assertion. Since the core of
the edge Hamiltonian is graded by a positive edge weight, a common bound
on the ordinary degrees of its homogeneous elements bounds the entire
core and makes it finite-dimensional.

The first nonzero edge coefficient may occur after a gap. This does not
introduce additional terms into the first-order determinant: at step
`t`, every term of `C3(E,G)` or `C3(E,D_E G)` uses only `G_0` and `G_t`,
because all intermediate edge coefficients of `E` vanish. In the
second-order exceptional case `a=t=1`, the four declared unknowns
`y2,e1*y1,e2*g,e1^2*g` cover every contribution. If the formal second
edge monomial does not exist, its coefficient `e2` is simply zero; an
invertible four-column system still forces `e1^2*g=0`.

## Clarification 1: intermediate coefficients need not all clear

The sentence asserting that the third-gate recurrence clears every
coefficient between steps zero and `t` is stronger than necessary and is
not always true. For alpha type with `a=1` and `t>=2`, the intermediate
monomial `m ell^(N-b)` is in the static near strip and passes every gate
of the unperturbed near monomial. It is not forced to vanish by that
recurrence.

The first-order determinant remains valid because this intermediate
coefficient cannot occur in either step-`t` equation. The sentence should
be replaced by the decoupling argument in the preceding paragraph. The
exceptional second-order calculation already includes its first-step
coefficient explicitly.

## Clarification 2: separate the cubic case in Lemma F

The proof of Lemma F, used after edge finiteness, should separate degree
three. For the near cubic top `m ell^2`, the top derivation has the finite
chain

```
m -> -2m ell -> 2m ell^2 -> 0.
```

Thus the lemma's stated unbounded-chain argument for every degree
`N` outside `{2,d}` is not valid at `d=3,N=1`. For `d>=4`, the argument
works: the only positive-degree chain starting points that can encounter
the stationary top degree `d` are `N=2` and `N=d`.

Theorem NE at degree three is already Theorem Q. Every non-affine
perturbation of a near cubic has a nonzero `m^2` term and otherwise terms
affine in `m`; that is exactly the degree-three case covered by the
retained binomial certificate. Stating "degree three follows from
Theorem Q; apply Lemma F's chain argument for degree at least four"
repairs the dependency without new computation or assumptions.

With these clarifications, no conceptual blocker was found in the
near-top completion. This bounded review checked the proof mechanism
and replayed its symbolic identities; it does not establish historical
priority or replace external mathematical review.
