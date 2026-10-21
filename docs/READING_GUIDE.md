# Reading guide

The collection has three useful scales: a treatment for one precise question, a concept family connecting related treatments, and a research note pursuing one question beyond the annual retrospective. Choose the scale that matches what you want to understand.

## Begin with a question

Open the [interactive atlas](../compendium/atlas/output/Mathematics_Atlas_2023_2026.html), select a domain and read its organizing question. A concept family supplies definitions, a theorem with hypotheses, a proof, an exact or explicitly numerical example, connections, limits and further questions. Follow its source buttons to inspect the retained annual treatments. Search and filter by domain, year or mathematical capacity; secondary links preserve genuine overlap between subjects.

The [249-page PDF](../compendium/atlas/output/Mathematics_Atlas_2023_2026_Report.pdf) is the continuous reading edition. It develops the domain synthesis and includes the source index. The HTML companion also contains all 1,051 main treatment bodies and all fourteen supplementary 2023 syntheses. The supplements are separate from the main count and appear under Connections.

Read a theorem's limits together with its statement. A finite example may establish a complete result for its declared finite model while leaving a larger proposed construction unresolved. A capability label indicates what kind of mathematical work the family supports; the interactive contract says which operations the actual interface implements.

## Choose a route

| Interest | Route through the atlas | What to look for |
|---|---|---|
| Exact recovery and experimental design | D14 computation → D15 observability → D12 optimization → D11 inference | A target's factorization through observations; the distinction between existence, stability and cost |
| Local-to-global structure | D04 homological methods → D05 topology and gluing → D06 geometry | Actual differentials, compatible restrictions, nonzero quotient classes and gauge conventions |
| Arithmetic with complete certificates | D01 arithmetic → D02 arithmetic geometry → D14 certification | Reduction to finitely many representatives, local conditions and the difference between generating solutions and proving completeness |
| Spectra, approximation and evolution | D07 analysis → D08 equations → D09 dynamics → D15 inverse problems | Operator domains, spectral decay, error bounds and the coordinates in which an evolution model is valid |
| Counting, probability and decisions | D13 combinatorics → D10 probability → D11 statistics → D12 optimization | The configuration space, sampling law, objective and information discarded by a statistic |
| Symmetry and quantum deformation | D03 algebra → D06 symplectic geometry → D16 quantum structures | Explicit actions, coherence maps, Poisson/Moyal conventions and higher-order compatibility |

The six bridge essays work well after a first pass through two adjacent domains. They prove connections in specified models. They do not replace a comparison theorem merely because two subjects use the same word, such as quotient, energy, spectrum or obstruction.

## Use a lab as a mathematical experiment

Start from the displayed inputs and predict the result before changing a control. Then identify the equation or certificate that explains the result.

For **L01**, compare recovery of $x_1+x_2$ with recovery of $(x_1,x_2)$. The observation map can determine the first target while leaving individual coordinates ambiguous. Read the rank test as a factorization theorem rather than just a successful numerical example.

For **L05**, vary the two integer shears and inspect their ordered commutator. A determinant of one does not force identity. Switch to projections to compare contraction with a commutator norm; the two quantities answer different questions. The lab does not construct a smooth connection or recover curvature on an arbitrary manifold.

For **L06**, inspect every surviving odd derivative order in a monomial Moyal bracket. A zero third-order correction can coexist with a fifth-order correction. Exact integer and rational coefficients prevent a floating tolerance from turning a small value into a false zero.

For **L09**, fill the triangle and compare its first Betti number before and after the attachment. The change comes from an actual boundary map. The lab computes rational homology for its fixed complexes; it does not implement integer torsion, arbitrary persistence or sheaf cohomology.

For **L10**, navigate the negative-Pell recurrence in either direction. The orbit calculation illustrates the result; the reduction proof is what certifies that the stated seeds cover all solutions in scope.

The other labs expose similarly declared finite counting, approximation or uncertainty models. An analytic upper bound is not an observed error measurement, and a finite enumeration is not an asymptotic complexity theorem.

## Read chronologically

The annual volumes preserve the retrospective order and evidence fields. Each is useful on its own:

| Year | PDF | HTML | Scope |
|---|---|---|---|
| 2023 | [Compendium](../compendium/years/2023/2023_Mathematics_Compendium.pdf) | [Searchable edition](../compendium/years/2023/2023_Mathematics_Compendium.html) | 114 main treatments, with fourteen additional retained synthesis bodies |
| 2024 | [Month-by-month volume](../compendium/years/2024/2024_Month_by_Month_Mathematics.pdf) | [Searchable edition](../compendium/years/2024/2024_Month_by_Month_Mathematics.html) | 237 treatments; recovery gaps remain labeled |
| 2025 | [Month-by-month volume](../compendium/years/2025/2025_Month_by_Month_Mathematics.pdf) | [Searchable edition](../compendium/years/2025/2025_Month_by_Month_Mathematics.html) | 351 treatments with dated provenance and scoped developments |
| 2026 | [Month-by-month volume](../compendium/years/2026/2026_Month_by_Month_Mathematics.pdf) | [Searchable edition](../compendium/years/2026/2026_Month_by_Month_Mathematics.html) | 349 treatments through 21 October; October is partial |

Use the [tables](../tables/) when you want a direct question/result mapping, then follow the treatment identifier into its volume. In atlas data, a main source key has a year prefix, such as `2023:M040`, so identifiers remain unambiguous across annual packages.

Dates record the topic's recovered historical location. The mathematical exposition was revised for the retrospective. The [discussion collection](../discussions/) supplies available discussion and editorial context under its stated attribution rules; it should not be read as a complete verbatim export of the historical conversations.

## Continue into the Hamiltonian question

Read the [35-page note](../research/hamiltonian/output/Nonlinear_Hamiltonian_Partners.pdf), or use its [offline interactive edition](../research/hamiltonian/output/Nonlinear_Hamiltonian_Partners.html). The question fixes a polynomial $H$ and asks which polynomial $G$, independent of $\hbar$, have identical formal Poisson and normalized Weyl–Moyal brackets.

Begin with the convention and quantifiers. Equality for selected partners of one nonlinear Hamiltonian differs from equality for every observable. Distinguish these objects before reading a classification:

| Object | Required property |
|---|---|
| Exact partner | One bracket has no Moyal correction |
| Active partner | It is exact and its common bracket is nonzero |
| Dynamic core | Repeated Hamiltonian action stays within the exact-partner space |
| Pairwise exact Lie sector | The required bracket identities and Lie closure hold throughout the sector |
| Associative star algebra | Closure also holds under the star product |

Then read the complete cubic and homogeneous-quartic scopes, the $qF(p)$ and monomial results, and the perturbation and ladder examples. The exact classifier computes brackets and requested homogeneous kernels; an individual kernel computation does not by itself classify all partner degrees. All-degree statements have separate proofs.

The pinned PerfectJet snapshot places the work alongside an existing full-space sextic programme. Read its archived solver boundary before citing the global degree-at-most-20 classification as a freshly reproduced calculation. The [provenance guide](PROVENANCE.md#the-perfectjet-and-msolve-boundary) states what was replayed and what remains an external dependency.

## Trace a claim to its support

For any result, inspect its statement, proof and example; identify whether the example is exact, floating or conditional; then find the verifier and its scoped receipt. Historical attribution is a separate question, answered by source excerpts and evidence labels. Byte integrity is another separate question, answered by manifests.

Package READMEs contain replay and rebuilding commands. Mathematical replay is intentionally lighter than publication rebuilding. Read [PROVENANCE.md](PROVENANCE.md) before interpreting counts of checks, archived solver outputs or a historical topic date as stronger evidence than they provide.
