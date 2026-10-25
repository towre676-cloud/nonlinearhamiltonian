# Improvement 1: Independent Moyal partner checker

## What was built

An independent, standard-library-only checker for correction-free Moyal
partners, in `moyal_partner_checker.py`. It does not import or reuse the
repository classifier. It implements the bidifferential operator
D(f, g) = (dq f)(dp g) - (dp f)(dq g) exactly over the rationals, and
checks D^(2m+1)(H, G) = 0 for every m >= 1, so the Moyal bracket equals
the Poisson bracket with no hbar corrections.

## What was verified, with three independent routes

1. D-operator method in `moyal_partner_checker.py`.
2. Shift-operator method in a temporary cross-check script
   (f(q + a dp, p - a dq) applied to g, a = i*hbar/2).
3. The repository's own `partner_lab.py` in the locally cloned
   `nonlinearhamiltonian/research/hamiltonian` directory.

All three agree on every instance tested.

### Instances

- H = q*p^3, G = q^2: Poisson bracket -6*q^2*p^2, no hbar corrections,
  correction-free.
- H = q*p^3, G = q^5*p: Poisson bracket -14*q^5*p^3, no hbar
  corrections, correction-free. This is a non-trivial cancellation case,
  not just a vanishing-derivative case.
- H = q*p^3, G = q^2*p: Poisson bracket -5*q^2*p^3, plus an
  hbar^2 term -3/2*p, so NOT correction-free. This negative control
  confirms the checker does not label everything correction-free.
- Monomial partners of H = q*p^3 with total degree <= 6:
  p, p^2, p^3, p^4, p^5, p^6; q*p, q*p^2, q*p^3, q*p^4, q*p^5, q*p^6;
  q, q^2, q^5*p. (q^2*p is excluded, as above.)
- Homogeneous kernel for H = q^4 + p^4 at degree 6: dimension 3,
  with basis (up to scaling) p^6 + 5*q^4*p^2, q*p^5 + q^5*p, and
  5*q^2*p^4 + q^6. The repository kernel command returns dimension 3
  with the same basis up to the same scaling.

## What this is NOT

- It is not a proof of the sextic partner classification above
  degree 20, and it is not a complete arbitrary-degree classification.
- It is not a dynamic-core classification. Dynamic cores, analytic
  operator domains, and global flows remain outside this checker.
- It does not change any existing repository file. It is a new,
  independently checkable tool, intended for a separate branch.

## Next steps for this branch

- Run the checker against the repository kernel for a wider set of
  quartic Hamiltonians and degrees, and record any mismatch as a
  failure, not as a silent adjustment.
- Use the same checker as the template for a sextic monomial-sector
  extension, degree by degree, with each degree's kernel recorded
  separately and without invoking an external solver.

## Branch

This file and report are committed on the branch
`muse/moyal-independent-checker` in
towre676-cloud/nonlinearhamiltonian, for review by pull request
rather than by a direct push to main.
