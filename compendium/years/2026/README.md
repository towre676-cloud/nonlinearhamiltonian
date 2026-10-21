# 2026 mathematics, rebuilt month by month

This edition covers recovered mathematical conversations dated1January through21October2026. October is partial. It is a reconstruction from bounded retrieved fragments, not an exhaustive export of all conversations. Each treatment retains its source date, exact returned excerpt, receipt locator and speaker-evidence label. Original user prompts remain unavailable unless recovered literally; the revised questions and expositions are newly authored.

Open `2026_Month_by_Month_Mathematics.html` for full question tables, search, month filtering and source excerpts. The PDF offers a continuous reading edition with month and treatment outlines. `compendium.json` contains all developments and `revised_questions.json` contains the revised-question table.

## Offline verification

From this extracted directory, run:

```sh
python3 -X utf8 -S verify_all.py
```

On Windows use `py -3 -X utf8 -S verify_all.py` or double-click `VERIFY_WINDOWS.cmd`. Verification requires only Python3.10+ and its standard library. It replays the monthly finite certificates and scoped numerical examples and validates the entry schema. Each report states whether its calculation is exact, floating numerical, provenance-related or a finite test of a more general written result. It does not certify every proof or replay missing historical repositories, Lean projects or large datasets.

`verification_summary.json` records program returns and deduplicated scoped check records. Source and document audits are separate in `document_checks.json`. `MANIFEST.sha256` lists the packaged bytes. The final package was also replayed after extraction into a fresh directory.

## Rebuilding the reading editions

Install the packages in `requirements-build.txt`, then run `make_figures.py`, `build_compendium.py`, `document_audit.py` and `render_review.py`. These optional publication operations require matplotlib, numpy, ReportLab, Pillow, pypdf and PyMuPDF; the offline mathematical verifiers do not. The PDF builder also expects the DejaVu Sans fonts at its configured font path; adjust that path for another operating system. Full visual review reports and independent mathematical reviews are retained when available.

## Authorship and limits

U means retrieved user-attributed mathematical content; A means assistant-only evidence; T means a secondary or topic fragment. A U label does not promise literal original wording. Source excerpts describe historical topics and claims. The new proofs and explicitly stipulated worked examples are separate. Missing definitions, matrices, datasets and proof bridges remain recorded gaps. Earlier-year retrospectives and retrieval-query echoes are excluded as new2026 mathematical evidence.

References support the specific background and dependencies stated in each treatment. Classical results, finite certificates, conditional conclusions, floating examples and open extensions retain their stated scopes.

The FreeLIP supplement is stronger than a sample replay: `freelip_certificate.json` and `verify_freelip.py` prove the stated raw-output uniqueness for all states by checking all126integer lattice bases and exact rational dual bounds. The630decoder fixtures separately test the implementation. Accepted-output/rejection claims are explicitly excluded.
