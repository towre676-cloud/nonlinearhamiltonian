# Nonlinear Hamiltonians: reproducible source bundle

This archive contains the maintained polynomial classification, mathematical
proofs, exact report verifiers, finite Lean development, and the original
research note and interactive HTML companion. It preserves the repository
path `research/hamiltonian/` because proof dependencies and source fingerprints
are identified relative to that layout.

Start in the extracted `Nonlinear_Hamiltonian_Partners` directory. Python
3.10 or later is required. The maintained classifier uses SymPy 1.14.0:

```bash
python -m pip install -r research/hamiltonian/c3_strata/requirements.txt
python research/hamiltonian/partner_lab.py sextic-core --schema 2 \
  --H 'q^6+p^3+q*p^2' > result.json
python research/hamiltonian/c3_strata/verify_sextic_report.py result.json \
  --H 'q^6+p^3+q*p^2'
python research/hamiltonian/reproduce_sextic.py --list
python research/hamiltonian/reproduce_sextic.py --suite classifier --suite reports
```

The broader `separable-core` and `weighted-core` commands handle the stated
families in potential degrees at least five. Unsupported inputs return an
explicit scope result; bounded computation is not used to claim a general
classification.

Read `research/hamiltonian/RESEARCH_CAPABILITIES.md` for the exact theorem
scopes and the distinction between written all-degree proofs, finite
computational checks, and Lean theorems. The finite Lean project is in
`research/hamiltonian/c3_strata/formal/`. Its `lean-toolchain` and
`lake-manifest.json` pin Lean and Mathlib; installing the Lean toolchain and
fetching those dependencies requires internet access. Toolchain binaries and
caches are intentionally absent from this source archive.

With `lake` available, all maintained checks can be run together:

```bash
python research/hamiltonian/reproduce_sextic.py --suite all --output reproduction.json
```

`all` includes Lean and fails if the requested toolchain is unavailable.
Partial runs record the suites not requested. This is not an end-to-end
formalization of the complete geometric all-degree classification.

The original seven-suite verification is dependency free:

```bash
python -B -X utf8 -S research/hamiltonian/verify_all.py
```

The package manifest hashes all delivered research sources and retained
receipts. The original reading editions are
`research/hamiltonian/output/Nonlinear_Hamiltonian_Partners.pdf` and
`research/hamiltonian/output/Nonlinear_Hamiltonian_Partners.html`. New
classification results are documented in the maintained Markdown theorem
files rather than retroactively inserted into that original note.
