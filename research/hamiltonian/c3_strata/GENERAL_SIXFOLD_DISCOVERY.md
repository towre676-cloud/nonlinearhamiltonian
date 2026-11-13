# General non-affine sixfold-leading discovery engine

For an arbitrary rational sextic with a sixfold leading root, make a
rational symplectic coordinate change so the leading homogeneous part
is \(q^6\). The remaining perturbation is arbitrary in degree at most 5:

\[
H=q^6+\sum_{i+j\le5}c_{ij}q^ip^j.
\]

There are 21 lower-order coefficient parameters (including the harmless
constant). This module can accept any chosen symbolic subfamily; a complete
21-parameter all-degree classification is **not** claimed.

## Universal leading-degree theorem

For every degree \(N\), the highest-degree homogeneous part of
\(T_3(H,G)=0\) is exactly

\[
120q^3\partial_p^3 G_N=0.
\]

Therefore the leading term of any nonzero static partner satisfies

\[
G_N=Aq^N+Bq^{N-1}p+Cq^{N-2}p^2
\]

with the natural omissions when \(N<2\). This is valid for all \(N\)
and all lower-order perturbations, not a finite sample. It supplies the
degree filtration for subsequent recurrence and exceptional-locus work.

## General exact discovery API

`general_sixfold_discovery.py` constructs the *untruncated*
rational/symbolic observation matrix

[
mathcal O_{N,r}(H)=(T_3(H,D^j(-)),T_5(H,D^j(-)))_{0le jle r},
quad D=T_1(H,-),
]

on all input polynomials of degree at most (N). It can compute the
entire determinantal ideal defining the locus of rank at most a chosen
threshold. An exact minor budget is enforced **before computation**:
the engine rejects searches it cannot finish rather than silently
subsample minors and claim completeness. Exact rational specializations
record kernel bases and dimensions.

For the two-parameter non-affine family

[
H_{a,b}=q^6+ap^3+bqp^2,
]

the complete degree-(le2), depth-one rank-(le3) ideal is

[
oxed{(a^3b^2)}.
]

Its algebraic zero set is the union of the parameter axes (a=0) and
(b=0). This is a complete **bounded incidence** classification for
that window, not an all-degree theorem about (H_{a,b}).

| Parameters | (dim S^1_{le2}) | (dim S^2_{le2}) |
|---|---:|---:|
| (a=b=0) | 6 | 6 |
| (a=1,b=0) | 3 | 1 |
| (a=0,b=1) | 4 | 2 |
| (a=b=1) | 2 | 1 |

An independent verifier expands the defining Weyl–Moyal star exponential
and checks these dimensions against the direct transvectant engine.

## Next mathematical obligations

1. Use the leading-term restriction to derive a *uniform recurrence* for
   static partners under generic lower-degree coefficients.
2. Establish all-degree tail injectivity and its exceptional parameter
   varieties, rather than infer an infinite tail from bounded matrix ranks.
3. Resolve the remaining coefficient strata of the full 21-parameter
   family, with rational covariance and independently replayed certificates.
4. Translate the universal leading-degree lemma and determinantal
   certificates into Lean, then prove the associated all-degree recurrence.

In particular this engine discovers exact **finite-window loci**, and does
not automatically turn them into global classifications.
