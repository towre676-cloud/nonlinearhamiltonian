# Binomial Newton strata: finite-tail and refinement classification

The earlier conservative bounds 87 and 53 and their endpoint-forcing outline
are superseded by the complete proof in
[BINOMIAL_NEWTON_SHARP_THEOREM.md](BINOMIAL_NEWTON_SHARP_THEOREM.md).

Over any characteristic-zero field, for every nonzero edge coefficient:

| Leading form | Weights | Sharp static bound | Static dimension | First refinement and persistent core |
|---|---|---:|---:|---|
| q6+z qp4 | (4,5) | 44 | 10 | span{1,H} |
| q6+b q2p3 | (3,4) | 28 | 10 | span{1,H} |

The complete proof includes the exact chain equations, all vanishing-link
and endpoint cases, exclusion of consecutive constrained resonances, ten
explicit symbolic basis elements in each case, and nonzero symbolic
rank-eight minors. The same support bounds and first-refinement equalities
hold for arbitrary strictly lower-weight perturbations; static dimension
can vary from 7 to 10.

`BINOMIAL_NEWTON_SHARP_CERTIFICATE.json` contains every finite weight-block
rank and kernel certificate, symbolic refinement minors, the parameter
matrices defining all static dimension loci, and independent verification
receipts. `verify_binomial_newton_sharp.py` regenerates and checks it.
`verify_binomial_newton.py` retains the older 87/53-window check as a
historical regression; it is not the justification for a tail bound.

No Lean formalization or external peer review is claimed.
