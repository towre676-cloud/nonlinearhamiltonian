# Static tail in the normalized simple-root chart

The input is a degree-$n$ coefficient vector $g_j$ in the basis
$q^jp^{n-j}$. Static kernel vectors satisfy the depth-zero rows of
orders three and five from the Lean coefficient model. For a chosen
simple root, the written proof moves it to $q=0$, rescales the
coefficient of $qp^5$ to one, and shears $p$ by $u q$ to remove
the $q^2p^4$ coefficient, which changes by $5u$. The Python
certificate uses the opposite names for the two variables. Its
index $t$ still measures distance from the simple-root edge.
Swapping variables changes the signs of both odd transvectants.

## Checked by Lean

- In the edge column $j$, the order-three and order-five pivots
  are $60j(j-1)(n-2j+2)$ and
  $120j(j-1)(j-2)(j-3)(5n-6j+4)$. The other Hamiltonian terms in
  each row contribute only at input indices below $j$. If the
  third-order pivot vanishes at $n=2j-2$, then $j\ge4$ for
  $n\ge17$ and the fifth-order linear factor equals $4j-6$.
  Thus the first two coefficients determine the whole static kernel vector.
- The third-order pivot alone is nonzero through index nine.
  The reconstruction satisfies the six fifth-order equations
  at output indices zero through five. TailRows proves linearity
  and constructs the two entries of each row by evaluating the two
  coordinate vectors. Any nonzero static partner gives a nonzero
  vector annihilated by all six linear forms.
- TailDegreeFactors proves that a strictly positive constant
  and nonnegative higher coefficients after $n=17+m$ imply
  nonvanishing at every integer $n\ge17$. TailDegreeFactorData
  checks this condition for all 53 primitive integer representatives
  extracted from the Python replay. The extraction clears denominators,
  divides by common integer content, and fixes the leading sign.
  Lean checks the resulting list using kernel reduction.
- TailRawRows verifies all eight third-order and six fifth-order
  polynomial equations used by the Python recurrence. TailScales
  proves that each of the six exact stored row scales is nonzero.
  TailFirstRow matches the first stored polynomial row to the gates.
- TailEliminationAxes verifies 31 steps and nine contradiction
  leaves across the eight normalized single-coordinate charts.
  Each theorem takes the corresponding six stored polynomial
  equations as hypotheses.
- TailTransport proves that coefficient rows, including iterate
  rows, and the discriminant commute with a ring homomorphism.
- The targets $b^2+2a^3/5$, $c+3a^2/20$, and $d+ab/50$
  imply the factorization $(X-r)^4(X+4r)$ and the vanishing of
  the discriminant used in the finite Lean bridge. Here $r=0$
  if $a=0$ and $r=-b/(2a)$ otherwise.
- The dehomogenized operator for the $p$ derivative is $nF-XF'$.
  Lean checks its action on monomials. The $q$ derivative in this
  chart is the ordinary polynomial derivative. The static row
  agreement is with the coefficient model.

- TailCleared05 through TailCleared8 prove the cleared recurrences
  for $g_2,\dots,g_8$ in terms of $g_0,g_1$. TailRow1 through
  TailRow4 match stored rows one through four to the gates using
  those recurrences and the recorded row scales. TailRow5 matches
  the last row by eliminating $g_9$ between the third-order row at
  pivot nine and the fifth-order row at $q^5$. With $M$ a constant
  multiple of the least common multiple of the cleared pivots of
  $g_4,\dots,g_7$, the combination equals $\rho$ times the stored
  row, where $\rho=-96745881600000(z-12)(z-6)(z-4)(z-2)^4(z-1)^2$
  and $z=n$. Lean cancels $\rho$ from $n\ge17$ and characteristic
  zero, so this row uses neither the recorded scale nor a closed
  form for $g_9$. TailStoredRows collects all six rows as
  `stored_rows`.
- TailMixedDegrees and the 81 modules under TailMixedId check the
  degree factors and polynomial identities of the mixed chart.
  `identity_9` is assembled from 42 chunk products and seven
  monomial bins under TailMixedId/I9c. TailMixedPruned replays the
  mixed elimination as `TailElimination.mixed`.
- TailCharts proves the torus normalization and coverage of the
  nine systems as `chart_targets`, given roots of every positive
  order, and derives `normalized_static_tail`. TailAlgClosed
  specializes it to algebraically closed fields. TailAllDegrees
  combines it with `finite_kernel_bound` as
  `squarefree_kernel_bound`, the kernel bound in every positive
  degree of the normalized squarefree coefficient model.

The reduction, degree-factor and target results hold over any
characteristic-zero field. The uniform static row agreement and
row split hold over any commutative ring.

## Remaining obligations

1. Prove the normalized chart change from a geometric simple root
   and covariance of the polynomial gates. Prove the iterated
   differential-operator correspondence with the coefficient rows.
2. For the triple-root application, transport the explicit
   factorization and rule out both permitted multiplicity types.
   Assemble the geometric, descent, and grading results for the
   complete classification.

The row comparison, chart coverage, mixed-chart replay and the
combination with discriminant vanishing, formerly items two to four,
are checked in the normalized coefficient model.

## Reproduction

From this directory with the pinned Lean and Mathlib dependencies:

~~~sh
lake build SexticC3 SexticC3.TailAllDegrees SexticC3.TailChartAxes
lake env lean Audit.lean
python generate_tail_degree_factors.py | cmp - SexticC3/TailDegreeFactorData.lean
python generate_tail_elimination.py --scales | cmp - SexticC3/TailScales.lean
python generate_tail_elimination.py --axes | cmp - SexticC3/TailEliminationAxes.lean
python generate_tail_row_comparison.py --raw | cmp - SexticC3/TailRawRows.lean
~~~

The finite generated modules, independent Python checker, and existing
certificate data are untouched.
