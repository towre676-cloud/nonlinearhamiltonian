# Sextic root-multiplicity refinement

See [SEXTIC_STRATA_THEOREM.md](SEXTIC_STRATA_THEOREM.md) for the complete classification and proof dependencies. The [squarefree theorem](SQUAREFREE_THEOREM.md) closes the remaining stratum using exact discriminant membership in all sixteen reduced determinantal ideals. This extends the maintained research without replacing the [restricted-family theorem](../c3_uniform/C3_THEOREM.md).

The [inhomogeneous theorem](INHOMOGENEOUS_THEOREM.md) transfers finite
leading-form refinement spaces to Hamiltonians with arbitrary lower-degree
terms. The [exact classifier](SEXTIC_CORE_GUIDE.md) exposes the complete
homogeneous table and these supported inhomogeneous cases through
`partner_lab.py sextic-core`. It returns rational bases or symbolic infinite
families, sufficient refinement depth, and an exact obstruction when an extra
first-refinement observable fails at the second refinement.

From the repository root, with Python 3 and SymPy 1.14.0:

```bash
python -m unittest discover -s research/hamiltonian/c3_strata -p test_strata.py -v
python -m unittest discover -s research/hamiltonian/c3_strata -p test_squarefree.py -v
python research/hamiltonian/c3_uniform/inputs/check_binary_static.py research/hamiltonian/c3_uniform/inputs/binary_static_d6.json
python research/hamiltonian/c3_uniform/monomial_proof.py
python -m unittest discover -s research/hamiltonian/c3_strata -p test_sextic_core.py -v
python research/hamiltonian/c3_strata/verify_sextic_core.py
```

To regenerate the earlier certificates, run `triple.py` and `squarefree_sample.py` from this directory. `verify.py` works from any working directory, returns a summary and does not overwrite evidence.

The new `squarefree_certificate.py` works from any directory and accepts `--output PATH`; `verify_squarefree.py [CERTIFICATE]` independently replays its 151 intermediate identities and 16 discriminant identities. The 185 selected reduced minors prove the result for every squarefree sextic, not just a generic open set. `squarefree_experiments.py` separately records exact partner-chart elimination and modular diagnostics; those experiments are not theorem dependencies.

The CI workflow retains the uniform, repeated-root, and squarefree suites and
adds the classifier checks. `REPLAY.json` and `SQUAREFREE_REPLAY.json` retain
their historical scopes. The [classifier replay receipt](SEXTIC_CORE_REPLAY.json)
reports its actual bounded checks separately from the written all-degree
proofs and their inherited dependencies. None of the new Python results is
an end-to-end Lean theorem.


## Complete extension families and report verification

[Quadratic complements](QUADRATIC_SIXFOLD_THEOREM.md) have a complete core
classification, exact stages and least-depth witnesses. [Separable cubic
and quartic complements](SEPARABLE_SIXFOLD_THEOREM.md) have complete static
spaces and sharp depth bounds; their potential-degree theorem extends beyond
sextics. Both sextic families use the explicit stages of schema 2.

The supplied-report verifier `verify_sextic_report.py` checks a report
against a separately supplied input. It validates complete polynomial
modules and reconstructs the finite weighted boxes used in the bounding
theorems. Its adversarial tests reject omissions and false metadata as well
as incorrect polynomial identities.

The [Lean development](formal/README.md) has a separate compilation and
axiom-audit workflow. Its finite and differential semantics remain distinct
from the complete geometric all-degree theorem. Use
`python research/hamiltonian/reproduce_sextic.py --list` from the repository
root to inspect every maintained reproduction suite.
