# 2025 Mathematics, Rebuilt Month by Month

This edition develops mathematics recovered from dated2025 conversations. Open `2025_Month_by_Month_Mathematics.html` for full question tables, source attribution, filtering and searchable treatments. The PDF supplies an outlined reading edition. `revised_questions.json` contains the complete machine-readable mapping, and `compendium.json` contains the integrated mathematical developments.

Every treatment has a newly revised question, definitions and assumptions, a precise result, proof or derivation, a worked example, limitations, a further mathematical problem and source provenance. The source month identifies the recovered conversation date, not a claim of new publication or discovery. U means user-attributed retrieved evidence; A means assistant-only evidence; T means a topic or secondary-source fragment. A retrieved summary does not establish a verbatim historical question. Recovery is bounded and does not replace a full conversation export.

Run all supplied mathematical replay programs with Python3. No third-party package or network connection is needed for this verification command:

```text
python3 -X utf8 -S verify_all.py
```

On Windows, double-click `VERIFY_WINDOWS.cmd` or run `py -3 -X utf8 -S verify_all.py`. Each program reports scoped exact calculations or numerical examples. Provenance/schema records are distinguished from mathematical examples. Passing finite checks does not automatically verify every written proof or a cited general theorem. The independent review reports retain the additional human-readable proof audit.

`independent_audit.py` proves nonvanishing and winding numbers for the actual recovered22December oscillator using integer-polynomial Rouche reduction. It independently computes rational Schur-Cohn matrix inertia and a nonzero derivative-Hankel determinant. The continuous minimal linear-realization dimension is eight; arbitrary discrete sample intervals require an additional nonaliasing hypothesis.

The `months` directories retain exact retrieved evidence, newly written treatments, finite verification code, check ledgers, coverage gaps and independent review reports. Missing historical tables, operators, raw measurements or source programs remain missing. Newly stipulated examples are identified within their treatments.

The three figures are calculated from analytic formulas. Their CSV files retain plotted values. The oscillator topology uses a separate exact certificate; the weighted convolution and double-well panels display specified mathematical models and establish no empirical device or machine-learning performance.

Rebuilding the reading editions requires the packages listed in `requirements-build.txt`, suitable DejaVu fonts and the supplied source tree. Run `make_figures.py`, `verify_all.py`, `build_compendium.py` and `document_audit.py` in that order. Building is separate from the portable verification command above.

`MANIFEST.sha256` hashes the packaged files. The release includes an independent replay after extraction into a different directory, with site packages disabled. The package retains classic results, explicit new expositions, exact finite certificates, numerical examples and conjectural extensions with their individual scopes.
