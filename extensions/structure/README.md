# Exact rational contraction seed

This starter implements arbitrary bounded finite complexes over **Q** and a small independent certificate checker. It constructs rational cohomology representatives and an explicit contraction, then returns a primitive or an exact obstruction witness for a cocycle. It does not compute integral torsion, general sheaf inputs, nonlinear deformation moduli, spectra or analytic convergence.

Run from this directory with Python 3.10 or later:

```bash
python3 -B -m unittest -v test_contraction_seed.py
python3 -B contraction_seed.py triangle.json --output triangle_certificate.json
python3 -B check_contraction.py triangle.json triangle_certificate.json
python3 -B contraction_seed.py triangle.json --degree 1 --cocycle '[1,2,-3]'
python3 -B contraction_seed.py triangle.json --degree 1 --cocycle '[1,2,-2]'
```

The final two commands produce a primitive and a nonzero quotient class with a separating functional respectively. The checker never imports the constructor or runs Gaussian elimination: it checks exact matrix identities. The constructor imports only the checker's exact matrix arithmetic and validation functions. Fractions are serialized as rational strings; floating coefficients are rejected. Matrix dimensions are explicit so zero-dimensional degrees remain meaningful.

The primary theorem is `pi=I`, `di=0`, `pd=0`, `I-ip=dh+hd`. For a cocycle b, the equation du=b is solvable exactly when pb=0; hb is then a primitive. Otherwise a nonzero coordinate row of pb gives a functional annihilating every boundary and detecting b. The proof and enhancement plan are in `../../programmes/OBSTRUCTIONS_AND_ARITHMETIC.md`.

The current reduction algorithm favors clarity and checkability. It repeatedly performs exact elimination and has no promised large-instance performance. Enforce a problem-size budget in any user-facing integration. Future adapters must validate their actual coefficient maps and chain relations before using this kernel. A Q-acyclic complex need not be acyclic over Z: multiplication by two already gives a torsion counterexample.
