# Sextic root-multiplicity refinement

See [SEXTIC_STRATA_THEOREM.md](SEXTIC_STRATA_THEOREM.md) for the full classification, proof dependencies and open squarefree locus. This extends the maintained research without replacing the [restricted-family theorem](../c3_uniform/C3_THEOREM.md).

From the repository root, with Python 3 and SymPy 1.14.0:

```bash
python -m unittest discover -s research/hamiltonian/c3_strata -p test_strata.py -v
python research/hamiltonian/c3_uniform/inputs/check_binary_static.py research/hamiltonian/c3_uniform/inputs/binary_static_d6.json
python research/hamiltonian/c3_uniform/monomial_proof.py
```

To regenerate certificates, run `triple.py` and `squarefree_sample.py` from this directory. `verify.py` works from any working directory, returns a summary and does not overwrite evidence. The CI workflow runs both the existing restricted-family suite and this extension. `REPLAY.json` records local verification; hosted execution awaits approval to push.
