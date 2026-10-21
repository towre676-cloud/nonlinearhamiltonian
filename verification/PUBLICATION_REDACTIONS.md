# Publication redactions and archive provenance

On 21 October 2026 the public derivative replaced **two occurrences** of an opaque Library file identifier in ancillary retrieval metadata. No identifier values are recorded here. The direct public path is `compendium/years/2025/months/12/root_details.json`; inside the 2025 archive the member is `2025_Mathematics/months/12/root_details.json`. The replacement label states that a Library file identifier was redacted for publication. Mathematical text and all canonical source bodies remain unchanged.

The original retained archives were read-only inputs outside this repository. Their checksums below identify the originals without republishing the identifiers. Public derivative archives and manifests were rebuilt consistently.

| Archive | Original retained SHA-256 | Public derivative SHA-256 |
|---|---|---|
| 2025 source bundle | `de0061ccdba1d1abc59bc0682144f9de6010e2856eaed0a3354b427206058f44` | `b8586483c403bf7d30b507b03cd0ec942d2f4dd00d3667c023f0fae01e5f4627` |
| Atlas source bundle | `8ef89da6f7aa23020dc11768d445f566306ab0482438a084c73f53c086e8265e` | `69e639d10f90a50180dcee289d31f0a405cafb882705f1813a53c3cf56046475` |

The public 2025 ZIP appears at `compendium/atlas/sources/2025_Mathematics_Source_Bundle.zip` and `downloads/2025_Mathematics_Source_Bundle.zip`. The public atlas ZIP at `downloads/Mathematics_Atlas_2023_2026_Source_Bundle.zip` contains that same redacted annual ZIP. The complete list of affected integrity and notice paths is in [publication_redactions.json](publication_redactions.json).

The 2025 and atlas manifests now describe the public derivatives. The atlas README and its bundled publication notice explicitly qualify the original historical wording about unchanged ZIP bytes. The SHA-256 hashes of `compendium/years/2025/compendium.json` and `compendium/atlas/data/atlas.json` were checked unchanged, so all 1,051 main treatments and fourteen supplementary treatments retain their exact source payloads. Root table hashes are checked independently by the publication verifier.

The annual and atlas checkers were inspected for hard-coded archive hashes. They compare compendium payload hashes and manifests; the payload hashes remain unchanged and no mathematical or source-provenance hash was loosened. Strict public manifest/source equality remains required. Nonsecret temporary or workspace paths in old render receipts are retained as historical notes, rather than altered as though they were credentials.
