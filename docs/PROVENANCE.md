# Provenance, verification and scope

This repository preserves a retrospective mathematics collection and a subsequent Hamiltonian research package. It provides reading editions, structured treatment records, available discussion material, exact examples, code and verification receipts. Mathematical source payloads and generated reports remain intact; public ancillary metadata has the narrowly documented redaction described below. Repository navigation and indexes are additional editorial material.

Read the [annual treatment index](../compendium/readable/years/INDEX.md) and [domain/family edition](../compendium/readable/README.md) directly on GitHub. The [bibliography](../bibliography/REFERENCES.md) collects references, and the [verification guide](../verification/README.md) documents the portable replay command and audit records.

## What the historical collection contains

The atlas was built from four completed annual source bundles. Their main treatment counts are:

| Annual source | Main treatment bodies |
|---|---:|
| 2023 | 114 |
| 2024 | 237 |
| 2025 | 351 |
| 2026, through 21 October | 349 |
| **Main total** | **1,051** |

Fourteen additional 2023 synthesis bodies are retained separately, making **1,065 retained bodies including supplements**. These are counts of treatments. They are not counts of unique conversations, distinct mathematical ideas, new theorems or discoveries.

The source boundary is the recovered annual material, not a fresh complete export of all account conversations. The collection has no complete verbatim raw transcript. Some records preserve dated retrieval fragments or summaries. Historical evidence fields remain attached to the treatments. Missing dates, definitions, matrices, datasets, source programs and proof bridges remain identified as gaps.

The 2026 cutoff is **21 October 2026**. October is partial, and later months are not inferred. The 2024 package records January as unrecovered and documents other bounded source gaps in its own scope files. A gap in recovery does not imply that no mathematical discussion occurred.

## Attribution and revised mathematics

The annual packages use their retained evidence labels, including:

| Label | Meaning in the recovered records |
|---|---|
| U | User-attributed mathematical content in a retrieved record |
| A | Assistant-attributed mathematical content |
| T | Topic, secondary or fragmentary evidence under the annual package's stated convention |

A U label does not guarantee a verbatim original prompt. A date locates recovered topic evidence; it does not establish when the retrospective proof was invented. Revised questions, corrected statements, proofs and expressly stipulated worked examples are newly authored retrospective exposition unless a record explicitly identifies a literal recovered passage.

The atlas's year-by-year progression fields describe topic continuity supported by source identifiers. They do not assign historical priority to a newly written proof. Similar vocabulary across dates does not establish a single continuous research programme or a mathematical equivalence.

The [discussion archive](../discussions/) is subject to the same distinction. Available text, recovered excerpts, edited discussion and summaries should keep their own labels. This repository does not claim that the discussion collection reproduces every historical conversation verbatim.

## Authoritative data and preservation

Within [the atlas package](../compendium/atlas/), `data/atlas.json` is the authoritative integrated dataset. Its main `corpus` has 1,051 final editorial placements with complete retained source payloads; `supplementary` holds the fourteen 2023 syntheses. The domain classification is an editorial navigation aid. Secondary links and multiple family memberships preserve overlap.

`data/classification_review.json` records final routing. `data/source_corpus_initial_routing.json` preserves the initial staging labels used to allocate review work; those draft labels should not be mistaken for final assignments. Domain chapters, concept families, bridge essays and lab contracts are added atlas synthesis. Source buttons identify the underlying revised annual treatment.

The public packages include the four annual source archives and their downloadable counterparts. The public 2025 archive and affected nested atlas archive copies are **publication derivatives**, rather than byte-identical copies of every original sealed archive. A publication audit found two occurrences of an opaque Library file identifier in the ancillary `root_details.json` retrieval prose. Those occurrences were replaced in the public metadata; the affected archive copies and manifests were updated.

The mathematical treatment payloads, proofs, examples, tables and generated PDF/HTML reports remain intact. The change concerns ancillary retrieval metadata, not the mathematical content or the recovered-prompt attribution rules. [`verification/PUBLICATION_REDACTIONS.md`](../verification/PUBLICATION_REDACTIONS.md) documents the exact redaction boundary and original-versus-public archive hashes. Use that record together with public manifests when comparing versions; an old sealed-archive hash is not the hash of its public derivative.

The repository's folder organization, homepage, reading guide and consolidated indexes do not retrospectively change the generated mathematical reports. GitHub-readable treatment and family pages provide navigable editions of the retained material. They are not evidence of a newly recovered historical transcript.

## What different forms of evidence establish

| Evidence | What it supports | What it does not automatically establish |
|---|---|---|
| Written proof | The stated general conclusion under its declared hypotheses, subject to mathematical review | Formal proof-assistant certification, historical authorship or novelty |
| Exact executable certificate | Its named finite identity, rank, count, instance or explicitly proved reduction | A broader theorem outside the tested or reduced scope |
| Floating numerical example | A numerical value or model demonstration within its stated precision | An exact zero, a proof of a general statement or an empirical performance claim |
| Analytic error bound | A proved bound under its model assumptions | An observed reconstruction error or a fitted empirical guarantee |
| Browser or document test | Interface behavior, rendering, layout or catalogue access in the tested conditions | Mathematical validity of every displayed claim |
| Archived external-solver receipt | The stored verdict and dependency described by its source | A fresh independent rerun or a proof-carrying rational certificate |
| Source excerpt and receipt | The recovered evidence and its attribution boundary | Complete verbatim transcript recovery |
| Hash manifest | Byte integrity against the named manifest | Truth of the mathematics or trustworthiness of a claim merely because it was hashed |

Passing computations and written proofs work together. A proof may reduce an infinite problem to a finite check, making that finite certificate decisive in the stated scope. A long list of sampled examples without such a reduction does not prove an all-degree theorem.

## Atlas and annual replay

From the repository root, the [portable publication verifier](../verification/verify_publication.py) runs:

```bash
python3 -B -X utf8 -S verification/verify_publication.py
```

It executes the four annual suites once each, the atlas with `--skip-annual`, the Hamiltonian suite once, and the publication audit. The [verification guide](../verification/README.md) documents requirements and result locations. This top-level command avoids counting a second atlas-triggered replay of the annual suites as additional mathematical evidence.

The atlas's `verify_all.py` checks source preservation and integration, replays the four annual suites and six domain suites, tests independent lab fixtures, and runs the actual JavaScript engine regression checks when Node.js is available. It uses temporary copies so replay does not rewrite the delivered material. Its result records distinguish an omitted environment-dependent check from a passed one.

The original annual suites comprise **61 verifier programs and 1,173 heterogeneous scoped records**, including one proof-only record. These counts are not numbers of formally proved theorems. The atlas records independent lab, engine, browser, catalogue and PDF audits separately. The final atlas PDF has **249 pages**; visual reviews name the PDF hash and the pages actually inspected.

The ten atlas labs are finite, explicitly declared constructions. Their contracts distinguish implemented controls from documented mathematical recipes. In particular, rational homology of a few fixed complexes does not implement integral homology or arbitrary persistent homology; a finite shear loop does not reconstruct a general geometric connection or curvature.

For commands and dependencies, read the [atlas README](../compendium/atlas/README.md) and each [annual package](../compendium/years/). Mathematical replay and document rebuilding are separate workflows.

## Hamiltonian research scope

The [Hamiltonian package](../research/hamiltonian/) fixes the flat Weyl–Moyal convention and studies equality of the normalized star commutator and Poisson bracket as a formal identity in $\hbar$, with $H$ and $G$ independent of $\hbar$. The note's individual results specify coefficient field, degree, homogeneity and equivalence hypotheses. Its polynomial identities do not assert analytic operator-domain results or completeness of global physical flows.

The delivered note has **35 pages**. Its mathematical replay uses seven suites and includes independent exact star-exponential comparisons, interpolation certificates, cubic and monomial checks, and recovered exact instances. The package README records their heterogeneous counts. General results in complete scopes are supported by proofs; repeated finite tests are not substituted for all-degree arguments.

Exact partners, active partners, dynamic cores, pairwise exact Lie algebras and associative star algebras are distinct. A partner whose first bracket has no quantum correction can leave the partner space under repeated evolution. The report gives an explicit perturbation example and states its remaining classification frontiers.

## The PerfectJet and msolve boundary

The research package preserves seven relevant files from **`towre676-cloud/PerfectJet`**, pinned to commit **`494caaf6df145175e11ac65c260b39b6e1aa2765`**. The read-only snapshot's file paths, Git blob hashes and SHA-256 values are recorded in [`context/source_snapshot.json`](../research/hamiltonian/context/source_snapshot.json). Its retained mathematical status and literature comparison appear in [`context/existing_work.md`](../research/hamiltonian/context/existing_work.md).

That existing source treats correction-free homogeneous sextic partners using the third and fifth transvectant equations. For a supplied rational sextic and requested partner degree, exact kernel computation is a finite linear-algebra problem in the partner coefficients. It permits coefficient cancellations in general partners and is stronger than a monomial-pair census. Activity, meaning a nonzero common first bracket, is tested separately.

The existing global exceptional-locus classification through **partner degree 20** has a separate trust boundary. Its characteristic-zero slice verdicts depend on **archived msolve results**. Modular computations and finite-prime checks provide support under the source's stated scope. Finite-prime emptiness by itself does not prove characteristic-zero emptiness.

The present package reads and preserves those archived verdicts. It replays its declared exact recovered instances and covariance identities. It does **not** claim a fresh msolve execution, a new independent rational certificate for every global verdict, a classification of all sextics in all partner degrees, or formal attachment of the archived solver conclusions. Degrees 21 and above and proof-carrying replay of those global solver verdicts remain explicit frontiers in the retained source.

The source snapshot is an external-work reference with a fixed commit boundary. Its existing sextic results and constructions are not presented as newly discovered by this retrospective. The [primary literature references](../research/hamiltonian/context/references.json) also distinguish universal-observable no-go results and established coordinate Lie sectors from restricted partner classifications for one fixed nonlinear Hamiltonian.

## Novelty and reuse

The collection contains classical mathematics, corrected expositions, new examples and calculations, scoped research results and unresolved extensions. A new exposition or independently checked proof may still belong to established theory. No blanket novelty, priority or comprehensive literature-search claim is made.

When citing or extending a result, retain its hypotheses, coefficient conventions, evidence labels and computational dependency. Cite the relevant original mathematical reference when the treatment supplies one, alongside the particular report, source identifier and package version used here.
