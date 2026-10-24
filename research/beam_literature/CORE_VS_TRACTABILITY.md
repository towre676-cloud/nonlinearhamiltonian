# Exact cores and computational tractability are separate questions

Fit audit, 24 October 2026. This note does not change any classification status
or settle the remaining pure-top conjecture. It identifies a necessary boundary
between the formal polynomial theorems and a fast physical simulator.

Use the repository convention
\(D(F)=\{H,F\}=H_qF_p-H_pF_q\). Dynamic-core membership requires
\(T_k(H,D^rF)=0\) for every odd \(k\geq3\) and every \(r\geq0\).
It equates the formal Moyal and Poisson iterates on that observable. It does
not by itself bound the size of its orbit or the cost of a requested expectation.

## An all-degree counterexample to the finite-closure inference

Take \(H=qp^3\) and \(F=q\). Direct differentiation gives

\[
D(qp^m)=(m-3)qp^{m+2},\qquad
D^r q=c_rqp^{2r},\quad c_r=\prod_{j=0}^{r-1}(2j-3).
\]

Every factor is nonzero for integral \(j\). Distinct powers of \(p\) make
these iterates linearly independent over \(\mathbb Q\). Thus no finite-dimensional
polynomial space containing \(q\) can be invariant under this \(D\).

At the same time, the only potentially nonzero higher odd gate is

\[
T_3(H,\cdot)=18p\,\partial_q^2\partial_p-6q\,\partial_q^3.
\]

It annihilates every displayed iterate, which is affine in \(q\). All odd
\(T_k\) with \(k\geq5\) vanish identically since \(\deg H=4\). Therefore
\(q\) belongs to the exact dynamic core at every depth while its polynomial
orbit is infinite-dimensional. This also agrees with the existing monomial
classification; no new maximal-core classification is claimed.

[check_core_vs_tractability.py](check_core_vs_tractability.py) independently
checks thirteen iterates using generic sparse-polynomial derivatives and
arbitrary-precision integers. Its finite replay supports the implementation;
the formulas above establish the all-degree statement. This is formal algebra,
with no claim about global flow, selfadjointness of unbounded operators, or
efficient state preparation and measurement.

## The faithful quantum application already has close prior art

[Bärligea et al., August 2026](https://arxiv.org/html/2608.17094v1) study
observable-seeded reachable modules beyond Gaussian dynamics. A small invariant
module and tractable input overlaps permit finite observable propagation;
polynomial-phase examples are already included. Their
[Apache-2.0 implementation](https://github.com/TimothyHeightman/bosonic-gsim)
provides seeded small experiments. We executed its pinned Fig8 and Fig10
examples: the four-mode Fock comparison residual was \(5.56\times10^{-16}\)
or smaller, and the single-mode phase/grid residual was below
\(2.00\times10^{-15}\). Receipts and source identities accompany the review.
These small replays do not reproduce the largest production results; large raw
production data and cluster job scripts are not distributed.

The possible extension is a certified search for additional useful modules,
including the ledger-proved sheared kinetic families. That remains a research
target. For the actual controls and observables, establish a small **common**
invariant space, affordable initial moments, and valid domain assumptions.
Charge discovery, compilation and readout as well as propagation. Compare with
bosonic-gsim, applicable analytic formulas and specialized simulators, rather
than only a large Fock cutoff. New exact sectors need not improve this best
existing workflow. A gauge-conjugated Gaussian oscillator is already amenable
to analytic conjugation; merely presenting it in nonlinear coordinates would
not establish a new simulation method.

Non-Gaussian small formal sectors do exist in the catalogue. For example,
\(H=q^2p^3\) preserves \(\operatorname{span}\{1,qp,H\}\), since
\(D(qp)=-H\) and \(D(H)=0\); its higher odd gates vanish there by degree
and antisymmetry. But this readout has the elementary formal evolution
\(qp-tH\). A useful common controlled or dissipative module, and a demanding
industrial query for which that sector beats existing methods, have not been
demonstrated. Being outside a paper's displayed examples is insufficient.

For approximate sectors, the
[October 2026 readout-aware Heisenberg preprint](https://arxiv.org/html/2610.26222v1)
is relevant prior art on how discarded terms affect the requested expectation.
Its setting and assumptions require separate checks before transfer to
unbounded bosonic dynamics.

## Why the ring recommendation is a separate engineering experiment

Storage-ring aperture tracking is classical already. Its survival indicator
is not a polynomial observable, and a composed multimode lattice is not one
autonomous binary polynomial Hamiltonian. The Moyal-core theorem does not itself
reduce that tracking cost. MultipointBAX instead selects fewer expensive
trajectories to evaluate. Its adoption is a plausible engineering route with
published precedent; it is not a speedup derived from our classification.

Keep both goals explicit: test BAX for a complete engineering gain, and test
additional certified quantum observable modules for a faithful use of the
mathematics. Neither has yet established our own tenfold result.
