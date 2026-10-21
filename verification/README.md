# Publication verification

`verify_publication.py` audits the complete published collection and replays its mathematical suites. It uses Python 3.10 or later and the standard library. Node.js must also be on `PATH` to check the actual atlas lab engine. It does not contact GitHub or any network service.

From the repository root:

```bash
python3 -B -X utf8 -S verification/verify_publication.py
```

The runner prints a JSON report and returns zero only when all required checks pass. By default it leaves delivered files unchanged. It first verifies component manifests and bundled annual source archives, compares all annual bodies with the atlas, and checks the canonical treatment table. It then runs each annual suite **once**, using temporary copies because those historical programs write fresh local reports. Next it runs the atlas with `--skip-annual`, followed by the Hamiltonian suite once. The two newer runners already create disposable verification copies internally. This avoids launching all four annual suites again through the atlas.

The default layout is:

```text
compendium/years/2023/ ... 2026/
compendium/atlas/
research/hamiltonian/
tables/treatments.csv
discussions/
downloads/
verification/
```

Each annual root contains its complete `compendium.json`, publication `MANIFEST.sha256`, reports and `verify_all.py`. The atlas retains its four annual ZIPs in `sources/`. Their internal manifests, safe member paths and complete payloads are checked. Every file covered by a bundled annual manifest must remain identical in the public annual directory. Any targeted ancillary-metadata redaction is documented in `PUBLICATION_REDACTIONS.md` with original and public-derivative archive hashes; mathematical treatment payloads must remain unchanged. The atlas and Hamiltonian manifests are mandatory too; a repository-wide manifest is checked when present. The checks preserve the sealed source bodies rather than treating a new table as their replacement.

The table must contain exactly 1,065 distinct `uid` values: 1,051 main treatments and fourteen supplementary 2023 syntheses. Required columns are `uid`, `kind` and `source_payload_sha256`. The `kind` values for the main and supplementary sets must be nonempty and disjoint. When available, `year`, `source_id` and `title` are compared too. Each source hash is SHA-256 over UTF-8 JSON serialized with `ensure_ascii=False`, `sort_keys=True` and `separators=(',', ':')`. These are hashes of the complete mathematical source bodies, not only their summaries or metadata. Annual counts must be 114, 237, 351 and 349.

New publication navigation is checked from the root README, `research/hamiltonian/GITHUB_RESEARCH.md`, and Markdown files in `discussions`, `tables`, `verification`, `papers`, `docs`, `bibliography` and `downloads`. Local links must resolve inside the repository. Every delivered PDF beneath the six component roots must have a navigation link, so reports remain discoverable rather than merely existing inside source archives. External literature links are retained but are not fetched by this offline verifier. Historical narrative links inside immutable annual source files are not reinterpreted as new root navigation.

A disclosure scan covers published text files and nested ZIP text members. It reports paths, categories and counts without printing matched identifiers or credentials. Nonsecret historical runtime paths are notes: they can occur in immutable render receipts and do not imply that those paths are required or available on another machine. Access tokens, private keys, signed download links, actual Library identifiers and helper files require review. The scan is a focused publication audit, not a guarantee that arbitrary content is free of every possible secret.

Useful options:

```bash
# Integrity, coverage, navigation and disclosure checks; no suite execution.
python3 verification/verify_publication.py --audit-only

# Run against another extracted repository directory.
python3 verification/verify_publication.py --root /path/to/repository

# Store a report outside the delivered tree.
python3 verification/verify_publication.py --output /tmp/publication-results.json

# Limit annual concurrency; the annual runners parallelize internally.
python3 verification/verify_publication.py --annual-workers 1 --timeout 1200
```

`--table` accepts a repository-relative alternative coverage-table path. `--skip-archive-privacy-scan` is available for faster repeated local audits; its JSON report explicitly records that nested ZIP disclosures were not scanned. It does not disable archive manifests or source-payload comparisons. `--audit-only` never claims that the mathematical suites were replayed. An optional `--output` writes only the requested report; keep that file outside the repository if a byte-for-byte unchanged tree is required.

Passing results establish artifact integrity, complete retained-source coverage and the scoped finite, exact and numerical checks implemented by these suites. They do not establish a complete account transcript, a proof-assistant certification of every prose theorem or a fresh replay of historical research inputs that were never recovered. PDF layout and browser rendering audits remain recorded evidence unless their separate rendering tools are invoked.

The completed publication receipt is [PUBLICATION_CHECKS.json](PUBLICATION_CHECKS.json). Targeted ancillary-metadata redactions and original/public archive hashes are documented in [PUBLICATION_REDACTIONS.md](PUBLICATION_REDACTIONS.md). The receipt combines the six successful mathematical suite runs with the final integrity, source coverage, navigation and disclosure audit; the repository manifest is generated after the receipt to avoid a checksum cycle.
