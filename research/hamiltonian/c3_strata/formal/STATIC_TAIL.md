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
- The targets $b^2+2a^3/5$, $c+3a^2/20$, and $d+ab/50$
  imply the factorization $(X-r)^4(X+4r)$ and the vanishing of
  the discriminant used in the finite Lean bridge. Here $r=0$
  if $a=0$ and $r=-b/(2a)$ otherwise.
- The dehomogenized operator for the $p$ derivative is $nF-XF'$.
  Lean checks its action on monomials. The $q$ derivative in this
  chart is the ordinary polynomial derivative. The static row
  agreement is with the coefficient model.

The reduction, degree-factor and target results hold over any
characteristic-zero field. The uniform static row agreement and
row split hold over any commutative ring.

## Remaining obligations

1. Prove the normalized chart change from a geometric simple root
   and covariance of the polynomial gates. Prove the iterated
   differential-operator correspondence with the coefficient rows.
2. Match the six proved linear forms to the six stored pairs
   $(A_t,B_t)$ after clearing denominators and accounting for the
   recorded row scales. Derive the torus weights and prove that the
   nine systems cover all nonzero edge pairs over an algebraically
   closed field. The mixed system normalizes $g_0=g_1$. Each
   single-coordinate system normalizes the first nonzero Hamiltonian
   parameter to one. The parameter origin already satisfies the targets.
3. Replay the 181 elimination steps in Lean. Render each sparse
   polynomial as a sum of rational coefficients times powers of
   $(n,a,b,c,d)$. Check the linear combinations and factorizations
   by ring normalization, use the field zero-product law to branch,
   and match each degree-only factor to its primitive integer
   representative with a proved nonzero scale. The independent
   Python replay reports 31 contradiction leaves and two target leaves.
4. Combine the replay with discriminant vanishing to exclude nonzero
   static vectors in the squarefree tail. For the triple-root
   application, transport the explicit factorization and rule out
   both permitted multiplicity types. Assemble the geometric,
   descent, and grading results for the complete classification.

## Reproduction

From this directory with the pinned Lean and Mathlib dependencies:

~~~sh
lake build SexticC3
lake env lean Audit.lean
python generate_tail_degree_factors.py | cmp - SexticC3/TailDegreeFactorData.lean
~~~

The finite generated modules, independent Python checker, and existing
certificate data are untouched.
