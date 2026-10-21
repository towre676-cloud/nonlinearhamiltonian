# 2024 Mathematics, Rebuilt Month by Month

Open 2024_Month_by_Month_Mathematics.html for the searchable edition or the matching PDF for the typeset edition. The coverage table and twelve month sections distinguish developed mathematics from source gaps. Every treatment includes a newly revised question, definitions, a result, a proof or derivation, a worked example, scope and a further question.

The historical material consists of retrieved dated fragments, not a complete conversation export. January remains unrecovered after four searches. U means user-attributed content in a retrieval result, not necessarily a verbatim prompt; A means assistant-only mathematical content; T means a dated topic fragment. Newly written formulations are not assigned to the historical user. SOURCE_SCOPE.json records the missing parts of March's equation list and the exclusion of a query-echo retrieval.

Run python verify_all.py with Python 3.10 or newer from the extracted package directory. On Windows, double-click VERIFY_WINDOWS.cmd, which enables UTF-8 and tries the Python launcher before the python command. The mathematical verifier programs use only the standard library and do not need network access. The runner writes verification_summary.json. Provenance/schema checks, exact finite checks and floating-point examples remain explicitly scoped in their individual reports.

The months directory contains developed entries, source receipts, coverage reports and verifiers. March's classical formula catalog is a separate entries file that the root loader incorporates automatically. compendium.json holds the integrated text; revised_questions.json is the complete machine-readable question/result table. Figures and their finite data are included under figures.

The package distinguishes supplied mathematical proofs from executable examples and cited literature. It does not claim mathematical novelty, complete transcript recovery, or proofs of RH, BSD or a general Langlands correspondence. The scope paragraphs are part of each result.

Optional rebuilding requires reportlab, Pillow, matplotlib and pypdf. Run python make_figures.py, python build_compendium.py and python check_documents.py to regenerate the documents and structural checks. Rebuilding the PDF currently expects DejaVu fonts in the standard Linux path; adapt the font path on another operating system. These dependencies are unnecessary for reading the completed files or replaying the mathematical verifiers.

MANIFEST.sha256 records the exact packaged file bytes. The release was also extracted into a fresh directory and its supplied verifiers replayed there. Relocation receipts document that test; the final report identifies the exact check counts and preserves their limitations.
