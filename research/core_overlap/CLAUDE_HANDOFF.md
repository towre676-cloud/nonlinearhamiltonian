# Handoff: exact nonlinear sectors and deformation obstructions

The continuation is based on published review commit `4050dbf`, which preserves
Claude's complete near-top theorem at `268d553`. The retained sealed compendium
and Hamiltonian baselines are unchanged. Historical priority remains unestablished.

## Closed questions in this package

Theorem CQ now classifies EVERY `A*p^2+B(q)*p+C(q)` with nonzero constant A.
Complete the square, then use the unified phase diagram in
`constant_quadratic_classification.md` and its exact classifier. QR closes
quadratic shears with nonlinear residuals; AFP supplies affine shears with
sharp depths seven for cubic residuals and five otherwise. Variable A(q)
is the remaining quadratic-momentum frontier.

Balanced total tops (B), near tops (NE), unequal tops, and top parts with at least
three roots are already classified under the retained hypotheses. Do not spend a
new push repeating those proofs. The former blanket pure collapse P003 is false.
Pure cores can be finite active, finite stationary, or infinite active.

For `Q=p+u(q)`, `deg u>=3`, `H=P(Q)+epsilon*q`, `deg P>=3`, Theorem SCP closes
the missing composition case: `ker C3 intersect ker C3D=span{1,H}`. QC remains
the infinite quadratic-shear family; SS/SO handle quadratic compositions.

Theorem SO adds `kappa*q^2/2` to the squared-shear Hamiltonian. For `deg u>=3`
the full core is exactly the quadratic sector in `(q,Q)` and depth two is sharp.
For a quadratic shear and nonzero kappa the same sector has sharp depth three;
zero kappa retains the infinite QC core. At nonzero kappa its six-dimensional
action has characteristic polynomial `z^2(z^2+2A*kappa)(z^2+8A*kappa)` and minimal
polynomial with one z factor. Exact flow and retained observer certificates replay.

Theorem QF completely classifies `H=A(p+u(q))^2+V(q)`, `A!=0`, `deg u>=3`, for
EVERY polynomial V, including the former resonant-degree boundary. Core dimension
is six for degree V at most two and two otherwise. The sharp third-gate depths
are two, six, and four for degree V at most two, equal to three, and at least four.
The two initial gate tests bound momentum degree by two; the third gives a proved
six-dimensional ambient space. Independent rank/closure certificates classify the
maximal invariant part of that space with no silently discarded output.

Theorem AP classifies every analytic potential for `H=q*p^(-1/4)+V(p)` on a
positive connected interval. An extra cubic exists exactly for
`V=c0+a*p^(-1/4)+b*p^(3/4)+c*p^(5/2)`; its full core is the affine strip plus
`R*(H-c0)^3`. The general active profile `a_*p^(-1/4)+b_*p` has a necessary and
sufficient global compatibility system; four-dimensional compatible potential
spaces are proved only on regular charts where the stated denominators do not
vanish. No global matching theorem across those singular charts is claimed.

For `H_t=(p+q^2)^2+t*q^2/2`, Theorem DO gives dimension seven for first-order
liftable initial observables and dimension six for second-order/formal liftables,
with arbitrary polynomial corrections allowed at each order. Its exact graded
observation cokernel has a `K[t]/(t^2)` summand in degree three and one `K[t]/(t)`
summand in every higher degree (plus the declared free cokernel summands). This
is literal algebraic torsion of an explicitly specified presentation, not a new
Nijenhuis tensor. Explicit all-degree coefficient functionals certify failure.

## Remaining productive frontiers

General nonconstant quadratic momentum coefficient `a(q)` is not classified by
QF; PP covers only its stated perfect-power stratum. Quadratic shears with nonlinear residual potentials are now closed by QR;
arbitrary higher transverse-degree pure perturbations still require their own proof. Recognizer failure means unclassified, never collapse.

For the broader pure-edge analysis, isolate first transverse jumps one, two,
and three, and retain exact determinant vanishing loci. Finiteness of a pure
core does not imply dimension two. Nonlinear canonical changes require the
protected-sector argument or explicit transformed gates; canonical brackets
alone do not preserve the original flat Moyal product.

The next analytic target is global extension of active cubic-preserving potentials
across singular regular-chart boundaries, and explicit normal forms for exceptional
F. The first integral `F F''-5(F')^2-3lambda F'=C` supplies a quadrature route.
Pole classes such as polygamma are already rigid under the stated continuation
hypotheses; adding more examples there is less valuable than classifying the
algebraic singularity boundary.

## Reproduction

Run `python3 -B research/core_overlap/verify_all.py` from the repository root.
Each new checker emits JSON and documents its optional receipt-output argument. The five theorem notes and
`extension_proof_review.md` state the complete hypotheses; the exact checkers
supplement their all-degree proofs. The portable bundle includes extensions and
all sources needed for its standard-library replay. Retained annual archives
require the full repository. Finite matrices never establish unbounded claims.
