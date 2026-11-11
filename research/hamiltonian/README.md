# Nonlinear Hamiltonians with exact classical–quantum partners

This research package answers the polynomial partner question in several complete scopes. It contains a 35-page mathematical note, a self-contained HTML companion with three working models, an exact standard-library Python classifier, all proofs and exact verification records. Equality is a formal identity in hbar with hbar-independent polynomial observables. Analytic operator domains and global physical flows are outside the stated algebraic results.

The complete results include every cubic Hamiltonian via characteristic-factor multiplicities; exact homogeneous dimensions and constructible bases for every nonzero homogeneous quartic; arbitrary-coefficient Hamiltonians qF(p) in every degree; balanced monomial closed forms; and a terminating all-degree classifier for unequal monomial exponents at least two. The active-partner quotient for a nonconstant monomial Hamiltonian is infinite dimensional exactly when its minimum exponent is at most two. Dynamic cores and multiplication/Lie closure are distinguished. The quadratic perturbation qp^3+q^2 has the same first-bracket partner space as qp^3 but dynamic core span{1,H}. Finite quantum ladders terminate at star powers, while their classical counterparts terminate at ordinary powers.

The note gives full proofs in its overview and appendices. No literature-priority claim is made. The coordinate Lie algebra is classical; Robert's universal-observable theorem and Gotay's quantization classification are respected. The pinned PerfectJet source snapshot records the existing full-space sextic programme through partner degree20 and its archived global solver dependencies. This package does not claim to have rerun msolve or solved the full sextic space in every partner degree.

## Read and explore

Open `output/Nonlinear_Hamiltonian_Partners.pdf` for the note. Open `output/Nonlinear_Hamiltonian_Partners.html` in a modern browser for the same note, embedded mathematics fonts, monomial bracket tester, homogeneous-quartic dimension explorer and exact q^2 flow example. The HTML works offline and makes no external network requests. Integer/rational bracket coefficients are exact; decimal evaluation of the displayed flow identity is labeled floating arithmetic. `output/Nonlinear_Hamiltonian_Partners.md` is the combined authoring source.

## Run exact calculations

Python 3.10 or later is sufficient for the original commands below; they require only the standard library. From this directory:

```bash
python3 -B -X utf8 -S partner_lab.py bracket --H "q*p^3" --G "q^2"
python3 -B -X utf8 -S partner_lab.py kernel --H "q^4+p^4" --degree 6
python3 -B -X utf8 -S partner_lab.py monomial --a 3 --b 5
python3 -B -X utf8 -S partner_lab.py flow --r 0 --steps 4
python3 -B -X utf8 -S partner_lab.py core-demo
```

The parser accepts q,p, integer and rational coefficients, sums, products and nonnegative integer powers. It does not execute arbitrary Python expressions. `kernel` gives the complete homogeneous partner space in one requested degree, including for an inhomogeneous H; it does not assert a complete arbitrary-degree classification. `monomial` uses a proved all-degree classification, including symbolic infinite axes where needed. `core-demo` checks the full polynomial action on the proved six-dimensional reduction, descending through dimensions6,4,2 and checking invariance without projecting away higher terms.

The `sextic-core` command gives an all-degree refinement and dynamical-core
classification for every rational homogeneous binary sextic. It also handles
arbitrary lower-degree perturbations of the eight leading root strata with a
finite-dimensional first refinement. It uses exact SymPy arithmetic:

```bash
python -m pip install -r c3_strata/requirements.txt
python partner_lab.py sextic-core --H "q^6+p^6+q^3+p"
python partner_lab.py sextic-core --H "q^4*p^2+q^6+q^3"
python partner_lab.py sextic-core --H "(q^2+p^2)^3"
```

Run this command without `-S`. The [classifier guide](c3_strata/SEXTIC_CORE_GUIDE.md)
describes the exact input scope, finite bases, infinite-family output,
obstruction witnesses, and unsupported cases. The
[leading-form theorem](c3_strata/INHOMOGENEOUS_THEOREM.md) supplies the all-degree
argument for the supported inhomogeneous cases.

## Replay verification

```bash
python3 -B -X utf8 -S verify_all.py
```

The runner checks `MANIFEST.sha256` when present and replays all seven suites in temporary copies, leaving delivered files unchanged. `RESULTS.json` records the completed run. Selected scopes include5,005 apolar basis triples, a complete1,024-point interpolation certificate,280,270 monomial-grid comparisons,1,144 independent exact assertions,420 independent cubic checks and recovered PerfectJet exact instances. These are heterogeneous checks, not a count of formally certified theorems. All-degree claims are supported by their proofs.

The browser record checks24 interface conditions across1280px,390px and320px, zero external requests, zero JavaScript errors, and3,140 bracket cases compared with the independent Python star-exponential engine. Three visual-review records cover all35 PDF pages plus full samples. `document_audit.json` records the final PDF hash and text-margin audit. Internal screenshots and browser binaries are excluded from the deliverable.

## Contents and rebuilding

`quartic/`, `structural/`, `monomial/` and `independent/` contain final proofs, findings, verifiers and exact receipts. `monomial/classification.py` is the complete exponent algorithm; `complete_table_2_to_12.json` includes55 complete Hamiltonian classifications. `independent/engine.py` expands the defining star exponential with exact Gaussian rational arithmetic, independently of the closed falling-factorial formula. `context/` contains primary references, the pinned source snapshot and evidential boundaries.

The original partner calculus and seven-suite replay are dependency free.
The sextic classifier and maintained C3 certificate replays use SymPy 1.14.0.
Rebuilding typeset HTML/PDF additionally needs Node, Playwright/Chromium, KaTeX0.19.0, markdown-it15.0.3 and markdown-it-texmath1.0.0. Install the three rendering packages under `tmp/render_deps`, install Playwright where Node resolves it, and set `ATLAS_CHROMIUM` to a compatible local Chromium executable. Run `node build_note.js`; `--html-only` preserves the existing PDF. `make_browser_fixtures.py` and `test_browser.js` regenerate the independent browser fixtures and interface checks. These optional rendering dependencies are excluded from the source bundle; the delivered HTML and PDF are already complete.

`MANIFEST.sha256` records the original portable package and the maintained classifier additions; the C3 certificate directories retain their separate integrity records. The package builder excludes exploratory dependencies, caches and temporary renders. Hashes detect accidental changes; they are not mathematical proofs. General higher-degree polynomial Hamiltonians, unrestricted one-step sextic partner spaces, and quartic dynamic-core stratification remain precise research frontiers.

## Maintained sextic refinement results

The [complete root-multiplicity classification](c3_strata/SEXTIC_STRATA_THEOREM.md) covers every nonzero homogeneous binary sextic over a characteristic-zero field. For squarefree forms, S¹ = D∞ = span{1,H}. C3 fails precisely at geometric root type (4,1,1), where S¹ has dimension three and S² = D∞ = span{1,H}. The [squarefree proof](c3_strata/SQUAREFREE_THEOREM.md) combines exact discriminant identities in degrees 1–16 with the inherited static-tail theorem. The [restricted-family C3 theorem](c3_uniform/C3_THEOREM.md) and its replay remain available.
