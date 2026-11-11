# Independent verification of supplied sextic reports

The classifier and its public reports have different trust roles. A classifier
finds a result; `verify_sextic_report.py` checks a supplied result against a
separately supplied Hamiltonian. It neither imports producer code nor calls a
classification function. The test suite checks reports in a fresh subprocess
that blocks every producer import, and separately disables classification
functions while checking reports.

Some producer paths and this verifier share the maintained exact defining-star
engine. Scope recognition, elimination, report validation and module comparison
are separate; this is not a claim that every arithmetic layer has two independent
implementations. The receipt identifies the shared engine by its source digest.

```sh
python research/hamiltonian/partner_lab.py sextic-core --schema 2 \
  --H 'q^6+p^2' > report.json
python research/hamiltonian/c3_strata/verify_sextic_report.py report.json \
  --H 'q^6+p^2' --output verified.json
```

The independent input can instead be a canonical term list supplied with
`--input-json input.json`. A different Hamiltonian is rejected even if the
report is otherwise valid. Exit status zero means the declared verification
checks passed; status two means rejection, with a JSON reason. The command
does not overwrite the report.

## What is checked

The verifier binds the input, total degree, homogeneity, dehomogenization
convention, point at infinity, factor reconstruction, geometric multiplicities,
classification family and method. It independently recognizes supported
families, including an `unsupported` result: changing the status to hide an
available classification does not pass.

For finite spaces it checks exact rational linear independence, containment of
the constant and Hamiltonian, defining-star gates, nested refinements, and
invariance under the full Poisson derivation. Gate outputs are never projected
into the input search window. Lift certificates and strict-drop witnesses are
reconstructed from their polynomial coefficients.

For polynomial families it checks the algebra or module itself. A few samples
cannot show that an infinite family is complete. In an adapted chart, equality
with

\[
\mathbb Q[x]\{1,y,\ldots,y^{r-1}\}
\]

is checked by expressing the reported module generators as columns over
\(\mathbb Q[x]\). Their determinant must be a nonzero constant, so the matrix
is invertible over the coefficient ring. Finite extra directions are compared
in the quotient by the whole module. This also accepts equivalent module
bases with high-degree terms that cancel.

The distinction matters for `H=q^6+q^2*p+p^2`. Its static space contains a
generator of total degree ten. Deleting that generator can pass a replay
restricted to total degree six. The exact module-and-quotient check rejects
the omission. This example is retained as an adversarial regression.

For nonconstant coefficients of the squared complementary coordinate, the
verifier rebuilds every finite kernel in the entire weighted envelope of
Theorem D, using independently implemented elimination and the defining star
exponential. The returned receipt records its weights, bound, number of input
monomials and stage dimensions. It checks the next kernel and the full
Poisson invariance of the reported terminal space.

Separable cubic/quartic complements and their supported lower-weight mixed
perturbations use their complete static envelopes. Their independent checkers
reconstruct the static kernel and every exact polynomial preimage. The strict
dispatcher also binds normal-form or weight metadata and every strict-drop
witness. These methods do not run the corresponding producers.

Schema 2 has one stage-based grammar. A report missing `stages` cannot fall
back to the earlier experimental `S1/S2` layout. Unknown stages carry no
space claim. A least-depth claim requires its exact first-failure witness;
the schema-1 adapter retains a sufficient-depth claim.

## Exact serialization and failure behavior

Duplicate JSON keys and nonfinite numbers are rejected when loading the file.
Polynomial exponents and dimensions must be integers, with booleans rejected.
Coefficients use reduced rational strings, never decimal strings or floats.
Zero terms, duplicate monomials, missing mandatory fields, undocumented fields,
incorrect coordinate conventions, malformed lift columns and altered witness
coefficients are rejected. Checks remain active under `python -O`.

Every accepted receipt includes a canonical report digest, the independently
bound Hamiltonian, checks performed, and fingerprints of the verifier, star
engine and named theorem inputs. These identify the checked bytes. They do not
authenticate the report's author or establish publication priority.

## Mathematical and provenance boundary

The exact calculations establish the listed polynomial identities, equality of
finite spaces, algebra/module descriptions and invariant-space conditions.
Their all-degree interpretation uses the cited written theorems: the
homogeneous classification and filtered transfer, and the appropriate
complementary-coordinate results. A finite replay is not a replacement for
those proofs.

The verifier rejects an assertion that the entire public classifier has been
formalized in Lean. The separate Lean project retains its own theorem boundary.
Free-text descriptions and producer-version annotations are carried as
annotations, not authenticated factual claims. The receipt states this
explicitly.

## Reproduction

```sh
python -m unittest discover -s research/hamiltonian/c3_strata \
  -p test_sextic_report.py -v
python research/hamiltonian/c3_strata/test_sextic_report.py --receipt
```

`SEXTIC_REPORT_REPLAY.json` retains the deterministic accepted-case and rejected
corruption ledger. Fixture generation uses the classifier; verification of each
supplied fixture does not. The receipt records this distinction.
