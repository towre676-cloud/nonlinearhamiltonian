# Existing exact-partner work and literature boundary

This is a read-only recovery of the relevant PerfectJet source and primary literature on 21 October 2026. The repository snapshot is pinned to `494caaf6df145175e11ac65c260b39b6e1aa2765`, tree `d723a6e0d5c985c144ced79e8e4365544ad91e53`. Seven relevant source files are preserved with Git blob hashes and SHA-256 values in `source_snapshot.json`. Pull request 2 is now closed and merged; the older memory that it remained conflicting is stale.

## What the existing repository already has

The authoritative current exposition is `docs/PARTNER_INCIDENCE.md`, integrated via release 0.17.0, and the explicit trust boundary is `docs/SEXTIC_INTEGRATION.md`. For a homogeneous binary sextic f and a homogeneous degree-N form g, its correction-free condition is exactly `(f,g)_3=(f,g)_5=0`. The first transvectant `(f,g)_1` is tested separately to decide whether the pair is active, meaning that its common Poisson/Moyal bracket is nonzero. A zero correction kernel vector is not the same as an active family.

The source constructs the complete rational instance matrix L_N(f) by stacking the third and fifth transvectant matrices. This is linear algebra in g. Its Math Lab interface can compute the full kernel and test each rational basis vector. This exact-instance machinery is stronger than scanning only monomial pairs, because cancellations between the coefficients of a general g are permitted.

The global classification treats the full seven-coefficient sextic space, using the dense root-placement slice `xy(x−y)(x³+px²y+qxy²+ry³)` and a separate classification of degenerate root patterns. The two root-separation factors are removed with a Rabinowitsch variable. Projection determinants define a superset of a rank-drop locus; emptiness of that superset excludes the true locus. Invariant-relation tests and classical orbit separation then identify exceptional classes. Line probes recover exact restrictions of possible hypersurfaces but do not independently certify genericity or exclude components they do not meet.

The archived classification through partner degree 20 is already substantial:

| Partner degree N | Existing stated exceptional locus |
|---|---|
| 3 | B=6A²; kernel dimension at least two exactly for the dihedral class x⁶+y⁶ or a root of multiplicity at least five |
| 4 | Beyond the universal quartic covariant (f,f)₄, the octahedral class xy(x⁴−y⁴) or a root of multiplicity at least five |
| 5 | A root of multiplicity at least four, or x⁶+(40/7)x³y³+y⁶ up to GL₂ over the algebraic closure |
| 6 | Beyond f itself, a root of multiplicity at least four |
| 7,9,11,13,15,17,19 | A root of multiplicity at least four |
| 8 | A root of multiplicity at least four, or the order-three family x⁶+λx³y³+y⁶ and its x³y³ boundary |
| 10 | A root of multiplicity at least four, x³y³, or the class x⁶+y⁶ |
| 12 | A²=25B/96 |
| 14 | A root of multiplicity at least four, x³y³, or the octahedral class |
| 16,18,20 | A root of multiplicity at least four, or x³y³ |

These global results carry a carefully stated external-computation boundary. Characteristic-zero slice verdicts rely on archived msolve results. Singular computations at two primes and a dependency-free modular engine provide supporting checks. A finite-prime emptiness result alone does not prove characteristic-zero emptiness. The present recovery reads the archived receipts; it does not rerun msolve or turn those receipts into independent rational certificates. Degrees 21 and above, proof-carrying rational replay of the solver verdicts, and formal attachment remain open in the current documentation.

Several exact constructions are already present and must not be claimed as new in this follow-up. Every sextic has the quartic correction-free partner `(f,f)₄` and its self-partner f. The family `f_λ=x⁶+λx³y³+y⁶` has the degree-eight partner `xy(x⁶+y⁶−(7λ/20)x³y³)` for every λ. The quintic candidate `xy(x³−y³)` has third gate `72(7λ−40)(x⁴y+xy⁴)` and fifth gate zero, hence the exceptional λ=40/7. These identities are implemented in `src/perfectjet/transvectants.py` and can be checked exactly.

## What the external literature establishes

Didier Robert's *When Poisson and Moyal Brackets are equal?*, arXiv:2207.08798v2 (2 March 2023), gives a strong universal boundary. Theorem 1.1 assumes fixed nonzero Planck parameter (scaled to one), H in a moderate-growth symbol class S^μ_δ with δ<1/2, and equality of the Poisson and Moyal brackets for every Schwartz observable A. It concludes that H has degree at most two. Theorem 4.1 similarly characterizes Hamiltonians for which a universal finite Moyal truncation is exact: retaining terms through order 2m+1 forces degree H≤2m+2. The theorem concerns a universal observable quantifier, so a nonlinear H can still possess a restricted infinite family of exact partners. The author's Poisson sign convention is opposite to the q-first convention used in the atlas; the equality and degree statements are unchanged after consistent sign conversion.

Mark J. Gotay's *On the Groenewold–Van Hove problem for R²ⁿ*, Journal of Mathematical Physics 40 (1999), 2107–2116, arXiv:math-ph/9809015, classifies maximal polynomial Lie subalgebras containing the Heisenberg algebra when n=1. Theorem 8 and Corollary 9 identify, up to isomorphism, the degree-at-most-two algebra and the coordinate algebra C={f(q)p+g(q)}. The latter has arbitrarily high polynomial degrees while remaining affine in one canonical variable. This is a classical structural source of infinite exact sectors. The paper explicitly says that the classification does not extend unchanged to higher dimensions. Its operator-quantization hypotheses and maximal-subalgebra question are stronger and different from finding E(H) for one fixed H.

Peter J. Olver and Jan A. Sanders, *Transvectants, Modular Forms, and the Heisenberg Algebra*, Advances in Applied Mathematics 25 (2000), 252–283, DOI 10.1006/aama.2000.0700, is a primary source for the established relationship among transvectants, classical invariant theory, Heisenberg representations, star products and Moyal brackets. The publisher and author bibliography confirm this relationship. The author PDF is accessible, but its extracted text has broken encoding, so no specific theorem in it is invoked here without visual or independent verification.

## Productive genuinely separate directions for this session

The short monomial identity in the chat motivates an all-degree classification for particular H, not another bounded monomial census. An exact closed description of E(qp^m), its exceptional exponent rays and their disappearance under higher gates would complement the full sextic incidence classification. General qF(p), affine symplectic transport, nonhomogeneous perturbations and several canonical pairs are further structural directions. Statements that require an entire family to be invariant under Hamiltonian evolution are stronger still: a one-step equality `[H,G]_star/(iℏ)={H,G}` need not persist after replacing G with `{H,G}`. For H=qp³, the resonance partner q^(3r+2)p^r is sent to a multiple of q^(3r+2)p^(r+2), which generally leaves the resonance line. Thus exact partner, invariant sector, pairwise exact Lie algebra, and associative star subalgebra must be distinguished.

Affine symplectic covariance of the flat Moyal product is already implemented in `src/perfectjet/moyal.py`. Ordinary pullback by a nonlinear symplectomorphism generally preserves the Poisson bracket but fails to preserve the same flat star product; the source includes an exact nonlinear-shear covariance defect. Consequently a nonlinear canonical change of coordinates cannot automatically transport an exact sector without transporting or correcting the star product as well.

No originality claim is justified by this recovery. A new proof in this session may be mathematically useful and independently checkable while still belonging to an established theory. The research should identify its exact relation to these existing results and keep finite computations, all-degree proofs, external-solver conclusions and open classifications separate.
