# Exact polynomial dynamics: capabilities and verification

This package classifies polynomial observables whose classical evolution
continues to agree with their flat Weyl–Moyal evolution. Its central outputs
are complete spaces, exact refinement depths, and explicit witnesses for
failure. The maintained implementation exposes the classification proofs
and independent report verification through a rational-input interface.
A separate Lean development proves the finite normalized-chart statements
and their interpretation as polynomial differential equations.

The [machine-readable scope index](c3_strata/CAPABILITIES.json) records the
implemented families and their individual proof boundaries. It distinguishes
an all-degree mathematical conclusion from a finite regression and from a
theorem compiled by Lean.

## The question and its mathematical content

Fix a polynomial Hamiltonian \(H\) over a field of characteristic zero.
Write \(D_HG=\{H,G\}\). For a sextic Hamiltonian, the nonclassical terms in
the Moyal bracket are exactly the third and fifth alternating contractions.
Thus

\[
S^r(H)=\{G:T_3(H,D_H^iG)=T_5(H,D_H^iG)=0,\quad 0\leq i\leq r\},
\qquad D_\infty(H)=\bigcap_{r\geq0} S^r(H).
\]

The static space \(S^0\) answers whether one bracket agrees. The persistent
core answers whether every classical iterate continues to agree. A large
static space need not produce a large core, and a quadratic observable can
survive one refinement before failing at the next. The software retains this
distinction in its reports instead of collapsing all three questions into
one boolean.

The problem concerns a fixed Hamiltonian and a restricted sector of
observables. Robert's theorem shows that agreement with every sufficiently
regular observable forces the Hamiltonian to be quadratic under its stated
symbol hypotheses. Gotay's work concerns the obstruction to quantizing the
entire polynomial Poisson algebra and the classification of quantizable
subalgebras. Neither statement directly supplies the fixed-Hamiltonian
refinement classification developed here. These are scope distinctions, not
a claim that the classical foundations are new. See
[Robert, arXiv:2207.08798v2](https://arxiv.org/abs/2207.08798v2) and
[Gotay, arXiv:math-ph/9809015](https://arxiv.org/abs/math-ph/9809015).

## What can be classified now

The [homogeneous theorem](c3_strata/SEXTIC_STRATA_THEOREM.md) covers every
geometric root-multiplicity stratum of a binary sextic. The
[filtered extension](c3_strata/INHOMOGENEOUS_THEOREM.md) permits arbitrary
lower-degree terms in all eight leading strata with finite-dimensional first
refinement. It also treats particular infinite-leading families by direct
all-degree arguments.

| Family | Exact information returned | Mathematical source |
| --- | --- | --- |
| All eleven homogeneous sextic root types, including nonsplit factors and roots at infinity | Finite bases or infinite polynomial families; first refinement, second refinement and core | Homogeneous root-strata theorem |
| Arbitrary lower terms in the eight finite-leading strata | Unique possible affine correction to the quadratic survivor, inconsistency certificates, and nonzero second-iterate obstructions | Filtered leading-form theorem |
| Sixfold or fivefold leading form, affine in a complementary coordinate | Complete polynomial modules, including the distinction between affine and nonlinear coefficients | Affine-complement theorems |
| Triple-pair leading form, cubic in an affine quadratic generator | Recovery of the generator and its full polynomial algebra | Quadratic-composition theorem |
| Sixfold leading form, quadratic in a complementary coordinate | Mixed infinite and finite stages, complete core, least depth and sharpness witness | [Quadratic-complement Theorems A–E](c3_strata/QUADRATIC_SIXFOLD_THEOREM.md) |
| Rational affine transforms of \(f(L)+g(M)\), \(\deg f\ge5\), \(\deg g=3\) or \(4\) | Complete static space, exact first refinement, core and least depth | [Separable-family theorem](c3_strata/SEPARABLE_SIXFOLD_THEOREM.md) |
| Arbitrary mixed terms strictly below the weighted leading binomial \(aL^n+bM^m\), \(n\ge5,m=3,4\) | A proved finite static envelope, every exact stage, core and least depth | [Weighted-perturbation theorem](c3_strata/WEIGHTED_SEPARABLE_THEOREM.md) |

The sextic command requires total degree six. The separate `separable-core`
and `weighted-core` commands expose the broader potential-degree theorems. Degree refers to the
input Hamiltonian; completeness of a classified space is not restricted to
observables below that degree.

### Representative exact outcomes

| Hamiltonian | First refinement | Persistent core | Depth |
| --- | --- | --- | --- |
| \(q^6+p^6+q^3+p\) | \(\operatorname{span}\{1,H\}\) | Same | 1 is sufficient |
| \(q^4p^2+q^6\) | \(\operatorname{span}\{1,qp,H\}\) | \(\operatorname{span}\{1,H\}\) | 2, least |
| \(q^4p^2+q^2\) | \(\operatorname{span}\{1,qp,H\}\) | Same | 1 is sufficient |
| \(q^6+p^2\) | Infinite dimensional | \(\operatorname{span}\{1,H\}\) | 5, least |
| \((p+q^3)^2+q^3\) | Infinite dimensional | \(\operatorname{span}\{1,H\}\) | 6, least |
| \((p+q^3)^2\) | Infinite dimensional | Six-dimensional quadratic sector in \(q,P=p+q^3\) | 2, least |
| \((qp+q^3)^2\) | \(\operatorname{span}\{1,qp+q^3,H\}\) | Same | 1, least |
| \(q^6+p^3\) | \(\operatorname{span}\{1,q,q^2,H\}\) | \(\operatorname{span}\{1,H\}\) | 2, least |
| \(q^6+p^4\) | \(\operatorname{span}\{1,H\}\) | Same | 1, least |
| \(q^6+p^3+qp^2\) | Dimension 3 | \(\operatorname{span}\{1,H\}\) | 2, least |
| \(q^6+p^3+q^3p\) | \(\operatorname{span}\{1,H\}\) | Same | 1, least |

These examples expose different mechanisms. In the fourfold-root example,
the obstruction is
\(T_3(H,D_H^2(qp))=-82944q^{10}\). In the constant quadratic-complement
family, repeated preimages of the static space can take six steps to reach
the core. In the variable quadratic-complement family, a third core direction
exists precisely when the explicit square criterion of Theorem E holds.
The cubic and quartic separable families have static dimensions 15 and 12
respectively, followed by the exact collapses displayed above.

This core is different from the ordinary algebra of classical first
integrals. For \(H=q^6+p^2\), \(D_H(H^2)=0\), but
\(T_3(H,H^2)=2880q^3p\ne0\). Thus ordinary \(H^2\) is conserved
classically and still fails even the static classical–Moyal agreement test.
The exact CLI reports a Moyal defect \(-120\hbar^2q^3p\). The distinction
explains why returning \(\operatorname{span}\{1,H\}\) is meaningful even
though all ordinary powers of \(H\) Poisson-commute with it.

For the mixed theorem, use weights
\((w_L,w_M)=(m/d,n/d)\), \(d=\gcd(n,m)\), and require every remainder
monomial to have weight below \(nm/d\). The complete static space lies in
weight at most \((4n+2m)/d\). In the sextic cubic/quartic cases those bounds
are only 10 and 16. These new separable and weighted results have direct
proofs and do not inherit the older sextic static-tail or geometric
root-stratum argument.

## Generate a result and check it independently

From the repository root:

```bash
python -m pip install -r research/hamiltonian/c3_strata/requirements.txt
python research/hamiltonian/partner_lab.py sextic-core --schema 2 \
  --H '(p+q^3)^2+q^3' > result.json
python research/hamiltonian/c3_strata/verify_sextic_report.py result.json \
  --H '(p+q^3)^2+q^3'
python research/hamiltonian/partner_lab.py separable-core --H 'q^7+p^3+q'
python research/hamiltonian/partner_lab.py weighted-core --H 'q^8+p^3+q*p'
```

The checker receives the intended input separately from the report. This
prevents a report from establishing its own input identity merely by carrying
internally consistent claims about a different Hamiltonian. It validates the
serialized exact arithmetic, factor reconstruction, geometric root type,
method, spaces, depth, witnesses and the specified theorem identifiers and
formalization flags. It does not authenticate producer provenance or arbitrary
free-text annotations.

Schema 1 remains the default sextic interface. Schema 2 expresses an indexed
sequence of refinement stages, allows an explicitly unknown static stage,
and distinguishes a least depth from a sufficient depth. An unknown stage
asserts no space. Unsupported inputs return no classification rather than an
extrapolation from a bounded calculation. See the
[API guide](c3_strata/SEXTIC_CORE_GUIDE.md) for the report contract.

### What makes the verification useful

The maintained classifier uses exact rational arithmetic. Several producer
paths use explicit contraction formulas, while the checker expands the
defining star product. The quadratic producer and its checker intentionally
share that exact star engine. The supplied-report checker independently
implements scope recognition, elimination and module comparison, reconstructs
spaces and invariance conditions, and does not import the producer modules.
This is independent verification of the supplied claims, with a pinned shared
arithmetic dependency in some families.

For nonconstant quadratic coefficients, Theorem D bounds the entire first
refinement by a finite weighted box. Reconstructing kernels in that full box
therefore tests the complete space conditional on the written bounding
theorem. It is stronger than comparing a few low-degree observations.

Infinite modules require their own checks. A static generator can have
degree ten even when the Hamiltonian has degree six, so a degree-six spot
check can overlook its deletion. The maintained report verifier checks the
module structure and finite quotient exactly. Its adversarial regressions
exercise omitted generators, altered depth, hidden obstructions, malformed
arithmetic and unsupported claims. Those checks concern the implementation;
the source theorems remain the mathematical completeness argument.

## Formal proof and continuous reproduction

The [Lean project](c3_strata/formal/README.md) uses Lean 4.19.0 and a pinned
Mathlib revision. Its finite squarefree development checks all sixteen
homogeneous partner degrees, including the exceptional Hamiltonian line in
degree six, and the explicit second-iterate obstruction in type \((4,1,1)\).
The transcriber emits polynomial identities that Lean proves from its own
definitions; the producer's answer is not accepted as an axiom.

The differential bridge proves, for sextic Hamiltonian monomials in every
contraction order and homogeneous partner degree, that the stored monomial
tensor equals the coefficients computed from Mathlib's actual multivariate
partial derivatives. Both static rows and rows
after one Poisson iterate are transported through that theorem. Consequently
the finite first-refinement and persistent-core statements now apply directly
to polynomials in the normalized chart; the persistent-core converse covers
every Poisson iterate. The axiom audit covers 75 named declarations.

The formal project has its own hosted workflow. That workflow regenerates
the checked source, compiles the Lean project, and runs an axiom audit allowing
only `propext`, `Classical.choice` and `Quot.sound`. A successful Python job
does not substitute for this Lean job. The exact semantic and geometric
boundary is maintained in
[THEOREM_BOUNDARY.md](c3_strata/formal/THEOREM_BOUNDARY.md).

One reproduction command lists and runs the maintained suites:

```bash
python research/hamiltonian/reproduce_sextic.py --list
python research/hamiltonian/reproduce_sextic.py --suite classifier --suite reports
python research/hamiltonian/reproduce_sextic.py --suite all --output reproduction.json
```

`all` includes Lean and fails if the requested toolchain is missing. A
partial run records which suites were not run. Receipts bind the result to
source hashes and preserve each check's return status. The extension workflow
also compares complete deterministic replay output with the retained
receipts. The portable source bundle contains the maintained proof sources
and verifiers, while excluding toolchain binaries and caches.

## The durable research advantage

The public repository can be copied. Its continuing value rests on the
accumulated classification, explicit certificates, independent validators,
formal semantics and a working interface that keeps their claims aligned.
An additional family is most useful when it arrives with an all-degree
argument, a detector valid under rational coordinate changes, exact outputs,
rejection tests, and integration into continuous reproduction.

This makes the package useful in three concrete ways: as a source of exact
benchmark Hamiltonians for symbolic or semiclassical software; as a classifier
for deciding whether an observable's classical evolution remains in an exact
quantum sector; and as a certificate-producing case study for formal algebra.
It does not supply a general spectral solver or numerical physical
predictions. Formal power-series agreement is distinct from analytic operator
domains or convergence of global flows.

A focused literature check against Robert and Gotay establishes the relevant
scope distinctions; it does not establish worldwide priority for every
classification statement. The appropriate public claim is the precise
theorem and reproducible artifact. Independent review can strengthen that
claim without changing its scope.

## Open boundaries

The complete geometric, all-degree C3 theorem is not yet formalized in Lean.
The remaining dependencies include the all-degree tail, coordinate covariance,
root normalization and descent, and assembly of the repeated-root arguments.
The formal boundary document identifies which finite statements and semantic
bridges are already kernel checked.

The classifier also does not cover arbitrary lower terms in all three
infinite-leading sextic strata. Complementary degree at least three is
implemented for the separable cubic and quartic families and their strict
lower-weight mixed perturbations. General mixed coefficients outside those
two weight cones remain unsupported. The static space for a nonconstant quadratic coefficient
remains unknown even when its first refinement and core are completely
classified. These are explicit mathematical frontiers, not failures concealed
by a finite search.
