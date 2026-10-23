# Mathematics Retrospective and Hamiltonian Research

A mathematical reading collection spanning recovered topics from **2023 through 21 October 2026**: four annual volumes, a domain atlas, searchable question tables, executable examples and a focused study of nonlinear Hamiltonians with exact classical–quantum partners.

The collection develops questions into definitions, precise results, proofs or derivations, worked examples, limitations and further problems. It connects arithmetic, algebra, geometry, topology, analysis, dynamics, probability, inference, optimization, computation and quantum structures through explicit constructions.

**Read directly on GitHub:** [annual treatment index](compendium/readable/years/INDEX.md), [domains and concept families](compendium/readable/README.md), [bibliography](bibliography/REFERENCES.md) and [verification guide](verification/README.md).

For interactive exploration, open the [mathematics atlas](compendium/atlas/output/Mathematics_Atlas_2023_2026.html), or read its [249-page report](compendium/atlas/output/Mathematics_Atlas_2023_2026_Report.pdf). The atlas organizes **1,051 main treatment bodies and 14 supplementary 2023 synthesis bodies** into **16 domains, 71 concept families, six cross-domain bridges and ten working mathematical models**. These are treatment counts, rather than counts of unique conversations or distinct discoveries.

## Read the collection

| Work | Reading edition | Searchable or interactive edition | Main treatments |
|---|---|---|---:|
| 2023 mathematics compendium | [PDF](compendium/years/2023/2023_Mathematics_Compendium.pdf) | [HTML](compendium/years/2023/2023_Mathematics_Compendium.html) | 114 |
| 2024 mathematics, month by month | [PDF](compendium/years/2024/2024_Month_by_Month_Mathematics.pdf) | [HTML](compendium/years/2024/2024_Month_by_Month_Mathematics.html) | 237 |
| 2025 mathematics, month by month | [PDF](compendium/years/2025/2025_Month_by_Month_Mathematics.pdf) | [HTML](compendium/years/2025/2025_Month_by_Month_Mathematics.html) | 351 |
| 2026 mathematics through 21 October | [PDF](compendium/years/2026/2026_Month_by_Month_Mathematics.pdf) | [HTML](compendium/years/2026/2026_Month_by_Month_Mathematics.html) | 349 |
| Mathematics atlas, 2023–2026 | [249-page PDF](compendium/atlas/output/Mathematics_Atlas_2023_2026_Report.pdf) | [Interactive HTML](compendium/atlas/output/Mathematics_Atlas_2023_2026.html) | 1,051 + 14 supplements |
| Nonlinear Hamiltonian partners | [35-page PDF](research/hamiltonian/output/Nonlinear_Hamiltonian_Partners.pdf) | [Interactive HTML](research/hamiltonian/output/Nonlinear_Hamiltonian_Partners.html) | Focused research note |

Download an HTML edition and open it locally in a modern browser to use its controls. The atlas and Hamiltonian companions work offline. GitHub's source preview may show the HTML source rather than run it.

The [reading guide](docs/READING_GUIDE.md) offers routes through the mathematics. The [provenance guide](docs/PROVENANCE.md) explains source attribution, reconstruction, verification and the external-solver boundary. The [discussions](discussions/) retain available retrospective discussion material; the [tables](tables/) provide direct question/result mappings. [Downloads](downloads/) collect portable source bundles and their integrity records. The GitHub-readable editions provide direct access to treatments and domain families without downloading the HTML companions.

## Mathematical routes

**Recover what matters.** A target can descend through an observation map even when the full hidden state is unrecoverable. Quotients, kernel conditions, experimental design and shared uncertainty connect algebra to inverse problems and decisions.

**Build a global object from local data.** Boundary maps, Čech differences, cycle periods and transport matrices turn gluing into explicit consistency equations. Homology, torsion, sheaf coefficients, holonomy and curvature retain their distinct definitions.

**Follow information through transformations.** Spectral cutoffs balance bias against amplified noise. Persistence records features that disappear before a terminal space is reached. Generating functions and graph censuses show how exact summaries can still lose distinctions.

**Compare classical and deformed dynamics.** A leading Poisson bracket can agree with a Moyal bracket while a later correction survives. The Hamiltonian note develops complete classifications in stated polynomial scopes, then distinguishes one-step equality from invariance under repeated evolution.

These routes are supported by theorems and small models. The atlas does not assert that every subject is an instance of one universal theory.

## Interactive mathematics

The ten atlas labs implement target factorization and probe selection; finite selection and ranking; graph-energy census collisions; diagonal spectral cutoff bounds; shear loops and alternating projections; exact monomial Moyal brackets; cyclotomic phase fibres; shared uncertainty; rational homology of fixed complexes; and negative-Pell orbit navigation.

Every lab states its inputs, arithmetic and limits. Exact integer or rational answers are distinguished from floating evaluations and analytic error bounds. A domain's capacity tags describe mathematical operations supported by its content; they do not imply that a general solver has been implemented. Arbitrary persistence, integral homology, sheaf cohomology, geometric curvature reconstruction and several other broader operations remain documented recipes or research problems.

## The Hamiltonian research note

The [22 October overlap study](research/core_overlap/README.md) disproves the
blanket pure-top conjecture in the extension programme and classifies new
finite and infinite exact sectors. It includes the quartic
`H=(p+q²)²` with active exact observables, complete nonlinear-composition
families, and sharp finite
stopping rules for analytic and polygamma Hamiltonians. The proofs,
independent exact checkers, and a [research PDF](research/core_overlap/output/pdf/Exact_Core_Overlap_Research.pdf)
state their scopes and leave historical priority open.

The continuation completes the higher shear-composition case, classifies
exact nonlinear oscillator sectors and their sharp stopping depths, and
classifies the analytic potentials preserving the fractional cubic.
Every polynomial Hamiltonian `A*p^2+B(q)*p+C(q)` with nonzero constant A
is now classified, including infinite and finite sectors and sharp
third-gate stopping depths up to seven. Exact all-degree bounds and
parameter-polynomial certificates establish the remaining branches.
The oscillator deformation
also separates first-order from second-order lifting obstructions in all
observable degrees. See the [research overview](research/core_overlap/README.md)
and its portable, standard-library replay bundle.

The cubic-phase continuation completes every affine Hamiltonian
`H=a(P)+q*b(P)`, `P=p+w(q)`, degree w two, including K1-prime and K4
upper bounds and a four-dimensional low-degree boundary. For every
polynomial F of degree at least three, adding a nonzero quadratic
restoring force to F(P) leaves exactly span{1,H}, sharply at third-gate
depth three. The associated formal deformation has three first-order
liftable initial observables and two second-order/formal ones; its
uniform finite-weight Smith law records one delayed t² obstruction.
General non-affine cubic-phase Hamiltonians remain open beyond the stated
classes. The [complete affine table](research/core_overlap/cubic_phase_classification.md)
and [restoring deformation theorem](research/core_overlap/restoring_deformation.md)
state the hypotheses and all-degree proofs.


The [Hamiltonian package](research/hamiltonian/) studies, for a fixed polynomial Hamiltonian $H$, those $\hbar$-independent polynomial observables $G$ for which

$$
\frac{H\star G-G\star H}{i\hbar}=\{H,G\}
$$

as a formal identity under the stated flat Weyl–Moyal convention. Its complete results include every cubic Hamiltonian in its declared setting, homogeneous dimensions and constructible bases for nonzero homogeneous quartics, arbitrary-coefficient Hamiltonians $qF(p)$, balanced monomial formulas and a terminating all-degree classification for unequal monomial exponents at least two. The note states the field, homogeneity and equivalence hypotheses for each result.

One-step partners, active partners with nonzero bracket, dynamically invariant cores, pairwise exact Lie algebras and associative star subalgebras are separate objects. The note gives examples where one-step equality fails under further evolution. Its exact classifier and three interactive models make the distinction inspectable.

The package also preserves a pinned **PerfectJet** source snapshot describing existing full-space sextic work through partner degree 20. Some of those existing global conclusions depend on archived **msolve** verdicts. This collection reads and preserves the receipts and replays its declared exact instances; it does **not** claim to have rerun msolve or solved unrestricted sextic partners in every degree. See [provenance](docs/PROVENANCE.md#the-perfectjet-and-msolve-boundary).

## Reproduce the scoped checks

The delivered reading editions are already built. From the repository root, run the [portable publication verifier](verification/verify_publication.py):

```bash
python3 -B -X utf8 -S verification/verify_publication.py
```

It replays each of the four annual suites once, the atlas with `--skip-annual`, the Hamiltonian package once, and the publication audit. The [verification guide](verification/README.md) explains requirements, outputs and scope. Python 3.10 or later runs the mathematical code; Node.js runs the atlas's actual JavaScript lab-engine checks.

For a component-only replay of the atlas, start at the repository root:

```bash
cd compendium/atlas
python3 -B -X utf8 -S verify_all.py
```

Node runs the actual atlas lab-engine regression checks. If unavailable, the runner records that part as not run. The annual and domain mathematical Python checks use the standard library. The atlas's `--skip-annual` option reruns its integration, domain and lab checks without replaying the four annual suites.

For the Hamiltonian package, from the repository root:

```bash
cd research/hamiltonian
python3 -B -X utf8 -S verify_all.py
python3 -B -X utf8 -S partner_lab.py bracket --H "q*p^3" --G "q^2"
```

Its mathematical classifier and replay suites need only Python's standard library. Optional rebuilding, browser testing and PDF rendering have separate dependencies documented in the package READMEs. A passing finite computation certifies its named calculation; the written proofs support the stated general results. Hash manifests establish byte integrity, not mathematical truth.

## Source and authorship boundaries

The annual retrospectives were reconstructed from bounded recovered material. The collection has no complete verbatim raw transcript of the historical conversations. A dated fragment locates a topic; it does not establish the verbatim original question or date the invention of a proof. Revised questions, proofs and new worked examples are retrospective developments, with the original evidence fields retained.

The mathematical source payloads and generated annual, atlas and Hamiltonian reports remain intact. Public ancillary metadata has one narrowly documented redaction: two occurrences of an opaque Library file identifier were removed from 2025 retrieval prose in `root_details.json`. The public 2025 ZIP and affected nested atlas archive copies are publication derivatives with updated manifests. [Publication redactions](verification/PUBLICATION_REDACTIONS.md) records the changed metadata and original-versus-public hashes.

Repository navigation, tables and discussion indexes provide additional routes into the retained material. Classical results, new exposition, explicit computations, conditional conclusions and open extensions keep their individual scopes. The collection makes no blanket claim of novelty or literature priority.
