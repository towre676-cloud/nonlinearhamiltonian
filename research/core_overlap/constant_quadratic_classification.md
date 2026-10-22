# Complete constant-quadratic momentum classification

Fix one canonical pair over a characteristic-zero field and the original
flat Weyl convention. Let

\[
\begin{aligned}
H&=A p^2+B(q)p+C(q),\qquad A\ne0\text{ constant},\\
u&=\frac{B(q)}{2A},\qquad Q=p+u(q),\qquad
V=C(q)-\frac{B(q)^2}{4A}.
\end{aligned}
\]

Thus `H=AQ^2+V` exactly. The constant term of `u` is retained in this
normalization. Put `m=deg u`, `n=deg V`, and use degree `-1` for the
zero polynomial. Write `D={H,.}`, `C3=T3(H,.)`, and

\[
 K_r(H)=\bigcap_{j=0}^r\ker(C_3D^j)
 \quad\text{inside }K[q,p].
\]

**Theorem CQ.** The following alternatives exhaust every such polynomial
Hamiltonian. In every row the displayed core equals `K_r(H)` for the
displayed depth, and every positive depth is sharp.

Write \(V_2=\operatorname{span}\{1,q,Q,q^2,qQ,Q^2\}\) and
\(T_2=K[Q]+\operatorname{span}\{q,qQ,q^2\}\).

| Shear degree | Residual degree | Full core | Dimension | Sharp depth |
|---|---|---|---|---|
| \(m\le1\) | \(n\le2\) | \(K[q,p]\) | infinite | \(0\) |
| \(m\le1\) | \(n=3\) | \(\operatorname{span}\{1,H\}\) | \(2\) | \(7\) |
| \(m\le1\) | \(n\ge4\) | \(\operatorname{span}\{1,H\}\) | \(2\) | \(5\) |
| \(m=2\) | \(n\le1\) | \(T_2\) | infinite | \(2\) |
| \(m=2\) | \(n=2\) | \(V_2\) | \(6\) | \(3\) |
| \(m\ge3\) | \(n\le2\) | \(V_2\) | \(6\) | \(2\) |
| \(m\ge2\) | \(n=3\) | \(\operatorname{span}\{1,H\}\) | \(2\) | \(6\) |
| \(m\ge2\) | \(n\ge4\) | \(\operatorname{span}\{1,H\}\) | \(2\) | \(4\) |

This is a complete classification in the constant-leading-coefficient
quadratic momentum scope, including Hamiltonians whose top need not be
pure. A variable coefficient of `p^2`, higher momentum degree, analytic
nonpolynomial observables, and more canonical pairs remain outside it.
No statement depends on sampled stabilization or a finite degree cutoff.

## Proof and dependencies

Completion of the square is an exact polynomial identity and does not
assert nonlinear covariance of the flat Weyl product. Each non-affine
shear branch instead uses its independently differentiated operators in
the original coordinates.

For `m<=1`, the shear is affine symplectic. If `n<=2`, `H` is quadratic,
so every higher odd gate vanishes. For nonlinear residuals, the complete
affine-shear potential theorem in `affine_shear_potentials.md` gives
dimension two and the respective sharp depths seven and five.

For `m=2,n<=1`, this is exactly the retained parabolic quadratic
composition theorem QC, with composition polynomial `P(z)=Az^2` and
linear forcing `V(q)`. Its proof gives the third-gate depths zero
through two as a complete criterion. The witness `q^3` passes depths
zero and one and fails at depth two by `-288A^3u''`.
Explicitly, with \(L=\partial_q\partial_Q^2\), the two successive
commutators with \(D=-2AQ\partial_q+V'\partial_Q\) are
\(-4A\partial_q^2\partial_Q\) and \(8A^2\partial_q^3\).
Their common polynomial kernel is exactly \(T_2\), since \(V'\) is
constant in this row. This also proves the uniform depth claim directly.

For `m=2,n=2` and `m>=3,n<=2`, the oscillator theorem in
`shear_oscillator.md` gives the six-dimensional sector. For `m=2`,
the coefficient `kappa=V''` is nonzero and the sharp depth is three.
For `m>=3`, the sharp depth is two, including zero oscillator strength.

For `m>=3,n>=3`, the all-degree six-dimensional upper reduction and
full-output invariant-kernel proof in `quadratic_frontier.md` give
`span{1,H}`, with sharp depth six for cubic residuals and four for
higher residuals. For `m=2,n>=3`, the complete nonlinear-residual
quadratic-shear theorem in `quadratic_shear_residual.md` gives the same
answer and depths. Its cubic case has a parameter-polynomial minor
certificate valid for every residual parameter, rather than just
sampled parameter values. These alternatives exhaust the integer
degree pairs and prove the table.

For each finite row the code also gives an exact basis in the original
coordinates and its Hamiltonian derivation matrix. The two-dimensional
cores are stationary. The six-dimensional cores carry the already
proved exact oscillator, hyperbolic, or nilpotent dynamics. In the
infinite QC row, linear forcing makes the polynomial tower active.

## Exact classifier and replay contract

`constant_quadratic_classification.py` accepts rational coefficients
directly as a sparse polynomial dictionary, or via its CLI as JSON rows
`[q_exponent,p_exponent,"rational coefficient"]`. Exponents must be
nonnegative integers. Floating-point coefficients or exponents,
fractional or negative powers, variable `p^2` coefficients, and higher
momentum degree are rejected before normalization.

The returned `CQ` record includes the case, core, dimension, normalized
`Q,V,A`, both degrees, exact finite basis where applicable, derivation
matrix, sharp third-gate depth, linked proof, and finite stopping
equality. This is a finite exact theorem-application record, even when
the classified core is infinite-dimensional; it is not a claim that
the returned finite matrix represents every polynomial observable.
`check_certificate` independently recovers the normal form and checks
the branch metadata and finite-basis gate identities. The all-degree
upper bound remains the stated written proof dependency.

The optional `--with-certificate` delegates to the existing QF, QR,
SO, QC, or affine-shear branch machinery for additional receipts where
available. The standard-library self-test covers every row, uses exact
original-coordinate gates and brackets, checks finite-basis closure and
sharp witnesses, and rejects altered theorem applications and invalid
scope inputs.

Example commands, from the repository root:

```sh
python3 -B research/core_overlap/constant_quadratic_classification.py
python3 -B research/core_overlap/constant_quadratic_classification.py --classify H.json
python3 -B research/core_overlap/constant_quadratic_classification.py --classify H.json --with-certificate
python3 -B research/core_overlap/constant_quadratic_classification.py --check-certificate application.json
```

The result organizes the component fixed-Hamiltonian classifications;
it does not claim to introduce completion of the square, nonlinear
canonical transformations, or the established general quantization
obstruction. Historical priority of the exact complete scope and sharp
depth table remains unestablished.
