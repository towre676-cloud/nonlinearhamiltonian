# Mathematics Atlas · 2023–21 October 2026

This package combines four completed retrospective mathematics volumes into 16 domains, 71 developed concept families, six explicit cross-domain bridges and ten interactive worked models. It preserves 1,051 main treatment bodies and 14 additional 2023 synthesis bodies. The 249-page PDF contains the domain synthesis, definitions, theorems, proofs, examples, limits, questions, capacity contracts and complete source index. The self-contained HTML companion contains the full text of every retained treatment and works offline in a modern browser.

The source boundary is the four supplied annual bundles, not a complete fresh export of all account conversations. Historical dates identify topics; revised proofs and new atlas calculations are retrospective. Missing dates are labeled unavailable. Historical evidence fields are retained without reinterpretation. The 2026 boundary is 21 October 2026.

## Reading and interacting

Open `output/Mathematics_Atlas_2023_2026.html` in a modern browser. Start with a domain, read a concept family and follow source buttons to the original revised treatment. Search and filter by domain, source year or mathematical capacity. Secondary domain links preserve overlap. The fourteen supplementary 2023 syntheses are under Connections and remain separate from the main count.

The labs implement fixed, explicit models: target factorization and probe selection; six-item exact selection and rank/unrank; graph-energy census collisions; diagonal spectral cutoff bounds; shear transport and line projections; exact monomial Moyal brackets; conductor-1680 phase fibres; shared uncertainty; rational homology of fixed complexes; and negative-Pell orbit navigation. Each states its controls, arithmetic and limits. A chapter capacity is not a claim to a general deployed solver. Integer/rational results, floating evaluations, analytic upper bounds and research recipes are distinguished.

## Data authority and source preservation

`data/atlas.json` is the authoritative integrated dataset. Its `corpus` has 1,051 final editorial placements with complete unchanged source payloads. Its `supplementary` has fourteen unchanged 2023 annual syntheses. Chapters, families, bridges and lab contracts are added atlas content. `data/classification_review.json` records final routing reasons. `data/source_corpus_initial_routing.json` preserves the initial staging dataset used to allocate review work; its draft labels are not the final domain assignments. Use `atlas.json` for analysis or further development.

`domains/*/families.json` and `chapters.json` are the final reviewed authoring inputs. Earlier draft generators are intentionally excluded because final reviews made direct corrections. `sources/` retains the four original ZIP files unchanged. New bounded sextic Moyal calculations are explicitly labeled atlas synthesis and cover monomials only, not arbitrary polynomial subspaces.

## Replaying mathematical checks

Python 3.10 or later is sufficient for the annual and domain mathematical checks. Node.js is required to replay the actual browser lab engine. Run from the extracted package root:

```bash
python3 -B -X utf8 -S verify_all.py
```

The runner checks the package manifest when present, confirms all source payloads against the annual archives, and uses a temporary directory for source extraction and verification outputs. It replays all four annual suites, six domain suites, independent lab fixtures and the engine regression checks. It leaves delivered files unchanged. `--skip-annual` reruns only integration/domain/lab checks. If Node is missing, the output explicitly records the engine checks as not run. The delivered `RESULTS.json` was produced with Node available and every suite passing.

The four original annual suites comprise 61 verifier programs and 1,173 heterogeneous scoped records; one record is proof-only. These counts are not numbers of formally proved theorems. The independent lab suite checks 1,513 cases, including invalid inputs. Engine regression checks cover 457 assertions. Browser checks cover desktop 1280px and mobile 390px/320px layouts, filters, full proof panels and all ten labs. Another browser sweep opens all 1,065 source bodies, all 71 families, all 16 domains and every capacity filter. PDF visual review covers all 249 pages through indexed contact sheets and full-page samples, with a separate text/margin audit.

## Rebuilding the deliverables

To extract local annual sources for a rebuild, run `python3 materialize_sources.py`. Then run `python3 build_atlas.py`. PDF rebuilding needs ReportLab and DejaVu Sans fonts at the path named in the builder. HTML building needs only Python. Domain verification uses the standard library; the optional PDF audit/render scripts need PyMuPDF and Pillow.

`test_interface.js` and `test_catalogue.js` need Playwright and a compatible local Chromium. Set `ATLAS_CHROMIUM` to that executable, or let the scripts use their local development path. The browser binary and temporary screenshots are not part of the deliverable. Mathematical engine replay needs Node only. `data/interface_checks.json`, `data/catalogue_browser_checks.json`, `data/lab_independent_checks.json` and `data/document_audit.json` record the completed checks; domain review records name their scope and PDF hash.

`MANIFEST.sha256` covers all delivered files except itself. `package_results.py` builds a fresh portable ZIP from the reviewed inputs and outputs. Integrity checks detect accidental changes; a hash is not a mathematical proof. Neither finite checks nor this synthesis certify unrecovered historical inputs, arbitrary nonlinear inverse problems, unspecified braid generators or all prose claims by formal proof.

## Public derivative

This public copy includes a targeted redaction of two Library-file identifier occurrences in ancillary 2025 retrieval metadata. All mathematical source bodies remain unchanged. See [PUBLICATION_NOTICE.md](PUBLICATION_NOTICE.md) for original and derivative archive provenance; this notice qualifies older statements that every original ZIP byte stream is retained unchanged.
