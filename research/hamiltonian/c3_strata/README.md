# Sextic root-multiplicity refinement

See [SEXTIC_STRATA_THEOREM.md](SEXTIC_STRATA_THEOREM.md) for the complete classification and proof dependencies. The [squarefree theorem](SQUAREFREE_THEOREM.md) closes the remaining stratum using exact discriminant membership in all sixteen reduced determinantal ideals. This extends the maintained research without replacing the [restricted-family theorem](../c3_uniform/C3_THEOREM.md).

From the repository root, with Python 3 and SymPy 1.14.0:

```bash
python -m unittest discover -s research/hamiltonian/c3_strata -p test_strata.py -v
python -m unittest discover -s research/hamiltonian/c3_strata -p test_squarefree.py -v
python research/hamiltonian/c3_uniform/inputs/check_binary_static.py research/hamiltonian/c3_uniform/inputs/binary_static_d6.json
python research/hamiltonian/c3_uniform/monomial_proof.py
```

To regenerate the earlier certificates, run `triple.py` and `squarefree_sample.py` from this directory. `verify.py` works from any working directory, returns a summary and does not overwrite evidence.

The new `squarefree_certificate.py` works from any directory and accepts `--output PATH`; `verify_squarefree.py [CERTIFICATE]` independently replays its 151 intermediate identities and 16 discriminant identities. The 185 selected reduced minors prove the result for every squarefree sextic, not just a generic open set. `squarefree_experiments.py` separately records exact partner-chart elimination and modular diagnostics; those experiments are not theorem dependencies.

The proposed CI workflow retains both existing suites and adds the squarefree suite. `REPLAY.json` retains the earlier integration receipt; `SQUAREFREE_REPLAY.json` records this extension's local verification. Publication, hosted checks, and merging await user approval.
