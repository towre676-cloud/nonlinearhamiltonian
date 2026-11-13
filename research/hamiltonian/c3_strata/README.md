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

## Sharp binomial Newton strata

[The two binomial Newton edges](BINOMIAL_NEWTON_SHARP_THEOREM.md) now have
complete endpoint/resonance proofs with sharp static-support bounds 44
and 28, ten explicit static partners each, and symbolic rank-eight minors
proving first-refinement rigidity. Arbitrary lower-weight perturbations
preserve that rigidity. Their static dimensions range from 7 to 10; an
exact finite matrix specifies every exceptional static locus.

`binomial_newton_sharp.classify` gives complete rational static bases within
these proved windows. Replay `verify_binomial_newton_sharp.py --perfectjet
--check BINOMIAL_NEWTON_SHARP_CERTIFICATE.json` with the pinned PerfectJet
revision. The proof and replays are not an end-to-end Lean formalization.
