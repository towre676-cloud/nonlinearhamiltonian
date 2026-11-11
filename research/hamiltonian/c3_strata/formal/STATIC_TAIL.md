# Static tail in the normalized simple-root chart

The input is a degree-(n) coefficient vector (g_j) in the basis
(q^jp^{n-j}). A static kernel vector satisfies the depth-zero rows of
orders three and five from `SexticC3.Model`. For a sextic with a chosen
simple root, the written proof sends that root to (q=0), rescales the
coefficient of (qp^5) to one, and uses (pmapsto p+u q) to remove
the coefficient of (q^2p^4), which changes by (5u). This is the
coefficient order in the Lean model. The Python certificate exchanges
the names of (q,p), so its index (t) is also the distance from
the simple-root edge. Swapping the variables changes both odd
transvectants by a sign and preserves the vanishing conditions.

## Checked by Lean

- The uniform static coefficient operator agrees with the existing
  sparse rows. In degree (n), for the (qp^5) column contribution
  at index (j), the pivots are
  [
  60j(j-1)(n-2j+2),qquad
  120j(j-1)(j-2)(j-3)(5n-6j+4).
  ]
  Contributions from all other Hamiltonian terms have input index
  less than (j) in that row. For (2le jle n) and (nge17),
  if the third-order factor vanishes, (n=2j-2), the fifth-order
  linear factor becomes (4j-6), and (jge4). Induction proves that
  a static kernel vector with (g_0=g_1=0) vanishes throughout
  (0le jle n).
- For (2le jle9), the third-order pivot alone is nonzero.
  `reconstruct_eq` proves forward substitution through index nine.
  `reconstructed_fifth_rows` proves that all six order-five rows
  at output indices (0,ldots,5) vanish on the reconstruction of
  a static kernel vector. These rows require indices at most nine.
- The three target polynomials are (b^2+2a^3/5),
  (c+3a^2/20), and (d+ab/50). When all vanish, the normalized
  quintic factors as ((X-r)^4(X+4r)), with (r=0) if (a=0)
  and (r=-b/(2a)) otherwise. Lean also proves `delta a b c d = 0`
  directly by substitution in the discriminant from the finite bridge.
- The dehomogenized polynomial operator for (partial_p) is
  (nF-XF'). Lean checks its action on each monomial, with
  (partial_q) represented by the ordinary polynomial derivative.
  The static row agreement above is with the coefficient model.

The reduction and target results hold over any characteristic-zero
field in this chart. The row agreement and row split hold over a
commutative ring. No discriminant hypothesis is needed for the reduction.

## Remaining obligations

1. Prove the normalized chart change from a geometric simple root and
   covariance of the actual polynomial gates. Prove the complete
   iterated differential-operator correspondence with the coefficient
   rows, including the sign when exchanging the variables.
2. Express the six reconstructed rows as linear forms in (g_0,g_1).
   Check their cleared numerators against the six stored pairs
   ((A_t,B_t)), with the recorded row scale. Derive the torus weights
   and prove that the nine systems cover all nonzero edge pairs over an
   algebraically closed field. The mixed system uses (g_0=g_1) after
   scaling. The other eight use the first nonzero Hamiltonian parameter
   normalized to one in each single-coordinate system. The parameter
   origin already satisfies the target equations.
3. Replay the 181 elimination steps in Lean. A sparse rational
   polynomial can be rendered as a sum of rational coefficients times
   powers of ((n,a,b,c,d)). A derived identity is a polynomial linear
   combination of earlier zeros, a factorization branches by the
   field zero-product law, and a target leaf cancels a nonzero
   degree-only factor. Check the identities with ring normalization
   over an arbitrary characteristic-zero field. The independent Python
   replay reports 31 contradictions and two target leaves. An exact
   rational diagnostic found 53 distinct degree-only polynomials up to
   leading-coefficient normalization, all with nonnegative coefficients
   after (n=17+m) and strictly positive constant term. This gives a
   route to proving nonvanishing over the integers before transporting
   it to the field. The diagnostic and elimination are outside the
   current Lean proof.
4. Combine the replay with `delta_zero_of_targets` to exclude a
   nonzero static vector in the squarefree tail. For the triple-root
   application, transport the explicit factorization and rule out both
   permitted multiplicity types. Assemble the geometric, descent and
   grading results separately for the complete classification.

## Reproduction

From this directory with the pinned Lean toolchain and Mathlib cache:

```sh
lake build SexticC3
lake env lean Audit.lean
```

The audit includes fourteen new theorems. The finite generated modules,
the independent Python checker, and the existing certificate data are
untouched.
