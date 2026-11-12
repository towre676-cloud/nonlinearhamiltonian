# PerfectJet kernel-tower bridge

This directory is the first production consumer of PerfectJet's generic exact
polynomial kernel-tower engine.

The maintained nonlinearhamiltonian classifier is **not** replaced. The bridge
keeps the two implementations deliberately distinct:

- `research/hamiltonian/independent/engine.py` expands the defining
  Weyl--Moyal star exponential using standard-library exact arithmetic.
- PerfectJet computes odd transvectants directly, builds repeated polynomial
  constraint towers, and decomposes parameter space into exact constructible
  constant-rank cells.

For a Hamiltonian (H), both paths test the bounded spaces

[
S^r_n(H)=
{Gin V_n:T_3(H,D_H^jG)=T_5(H,D_H^jG)=0, 0le jle r}.
]

`bridge.py` cross-checks all eleven homogeneous root-multiplicity
strata, every homogeneous partner degree 0 through 10, and refinement depths
0 through 2: 121 independent cases, each comparing the complete kernel
dimension sequence.

It also sends the one-parameter family

[
H_delta=q^4p^2+delta q^6
]

through PerfectJet's parametric rank-cell engine. On the quadratic input span
the bounded dimensions are

[
delta
e0:quad 3	o1	o0,
qquad
delta=0:quad 3	o1	o1.
]

Thus the degeneration from the exceptional ((4,1,1)) stratum to ((4,2))
is recovered as an algebraic rank-drop boundary, not merely by sampling.

## Trust boundary

The cross-repository replay is intentionally finite and does not replace the
all-degree theorems in `../c3_strata/SEXTIC_STRATA_THEOREM.md`. In
particular, a bounded PerfectJet plateau is not interpreted as an infinite
stabilization theorem.

The workflow pins an exact PerfectJet commit. Updating that pin is a reviewed
change because the bridge is meant to detect semantic drift between the two
projects.
