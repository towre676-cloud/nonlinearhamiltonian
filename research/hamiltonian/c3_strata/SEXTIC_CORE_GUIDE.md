# Exact sextic refinement and dynamical-core classifier

The command `partner_lab.py sextic-core` turns the complete homogeneous
root-stratum theorem into an exact rational-input calculation. It also applies
the [leading-form transfer theorem](INHOMOGENEOUS_THEOREM.md) to Hamiltonians
with arbitrary lower-degree terms whenever the leading first-refinement space
is finite dimensional.

The output classifies polynomial observables in **all degrees** in the stated
scope. A finite-degree search is not used to infer completeness. The written
theorems supply the upper bounds; exact per-input calculations construct the
spaces and check their witnesses.

## Install and run

From the repository root, using Python 3.10 or later:

```bash
python -m pip install -r research/hamiltonian/c3_strata/requirements.txt
python research/hamiltonian/partner_lab.py sextic-core --H "q^6+p^6+q^3+p"
python research/hamiltonian/partner_lab.py sextic-core --H "q^4*p^2+q^6+q^3"
python research/hamiltonian/partner_lab.py sextic-core --H "(q^2+p^2)^3"
```

The command uses SymPy 1.14.0 for exact rational factorization and small exact
linear systems. Run it without Python's `-S` option. The existing `bracket`,
`kernel`, `monomial`, `flow`, and `core-demo` commands retain their
standard-library-only behavior.

The parser accepts `q`, `p`, integers, rational constants, parentheses, addition,
subtraction, multiplication, division by a nonzero rational constant, and
nonnegative integer powers. Both `^` and `**` denote exponentiation. Decimal
coefficients, symbolic parameters, function calls, and rational functions in
`q,p` are outside the input language. No Python expression is evaluated.

## What is classified

With the repository's flat Weyl–Moyal convention, let

\[
D_HG=T_1(H,G),\qquad
S^r(H)=\{G:T_3(H,D_H^iG)=T_5(H,D_H^iG)=0\ (0\le i\le r)\}.
\]

The persistent core is
\(D_\infty(H)=\bigcap_{r\ge0}S^r(H)\). Thus the first refinement checks both
the initial observable and its first classical derivative. It is a stronger
condition than initial-bracket agreement alone.

| Input | Scope of the returned answer |
| --- | --- |
| `H=0` | The entire polynomial ring, with sufficient refinement depth zero |
| Nonzero homogeneous rational binary sextic | All eleven geometric root patterns |
| A homogeneous rational sextic plus a constant | All eleven patterns; derivatives and refinement spaces are unchanged |
| Total degree six with leading type `(4,2)`, `(4,1,1)`, `(3,2,1)`, `(3,1,1,1)`, `(2,2,2)`, `(2,2,1,1)`, `(2,1,1,1,1)`, or `(1,1,1,1,1,1)` | Arbitrary rational terms of degrees zero through five |
| Sixfold leading form with \(H=f(L)+b(L)M\) in coordinates adapted to the repeated linear factor | Polynomial family over \(\mathbb Q[L]\) with module basis \(1,M,M^2\) for affine \(b\), and \(1,M\) otherwise |
| Fivefold-leading Hamiltonians affine in a complementary coordinate | The all-degree module over the multiplicity-five factor |
| Triple-pair leading forms with a cubic in an affine quadratic generator | The polynomial algebra in that generator |
| Every sixfold-leading Hamiltonian quadratic in a complementary coordinate | Complete core and least depth, mixed infinite/finite refinement stages with `--schema 2`; static S0 is unknown for a nonconstant squared-complement coefficient |
| Sextics affinely equivalent to f(L)+g(M), with deg(f)=6 and deg(g)=3 or 4 | Complete static space, refinement and core with `--schema 2` |
| Sixfold sextics with cubic/quartic weighted leading binomial and arbitrary strictly lower-weight mixed terms | Complete static space, all refinements and least depth with `--schema 2` |
| Other nonconstant perturbations of types (6), (5,1), and (3,3) | An explicit unsupported result |
| Other nonzero total degree | An input error |

The root pattern is geometric: an irreducible rational factor of degree two
and multiplicity three contributes two roots of multiplicity three. No
approximate roots or choices of algebraic embeddings are used. For a nonzero
leading sextic, dehomogenizing as `H6(t,1)` is accompanied by the root at
infinity `[1:0]`, with multiplicity `6 - degree(H6(t,1))`. For zero input, the
empty root pattern and zero infinity multiplicity are sentinel metadata;
the zero form has no projective root divisor.

## Examples and their mathematical meaning

| Hamiltonian | First refinement | Persistent core | Sufficient depth |
| --- | --- | --- | ---: |
| `q^6+p^6+q^3+p` | `span{1,H}` | `span{1,H}` | 1 |
| `q^4*p^2+q^6+q^3` | `span{1,qp,H}` | `span{1,H}` | 2 |
| `q^4*p^2+q^6+p^3` | `span{1,H}` | `span{1,H}` | 1 |
| `q^4*p^2+q^2` | `span{1,qp,H}` | `span{1,qp,H}` | 1 |
| `q^4*p^2+q^3` | `span{1,qp,H}` | `span{1,H}` | 2 |
| `(q^2+p^2)^3` | `Q[q^2+p^2]` | `Q[q^2+p^2]` | 1 |
| `p^6` | `Q[p] + q Q[p] + q^2 Q[p]` | The same space | 1 |

The two lower-degree perturbations of the `(4,1,1)` leading form illustrate
why a homogeneous root label alone does not decide the first refinement of an
inhomogeneous Hamiltonian. The classifier solves all relevant coefficient
equations for the possible affine correction to its quadratic leading
survivor.

The `(4,2)` leading form has three possible outcomes: no quadratic lift;
a quadratic lift that fails at the second refinement; or a lift whose span
with `1,H` is invariant. For example, if `H=q^4*p^2+q^2`, then
`D_H(qp)=2H`, so the extra observable remains in the core. If
`H=q^4*p^2+q^3`, then

\[
T_3(H,D_H^2(qp))=-4320q^7\ne0.
\]

When the returned sufficient depth is two, the nonzero obstruction proves
that depth one does not suffice. A sufficient depth of one is not a claim
that `S^0` differs from the core for every particular input.

## JSON result

The default schema identifier is `hamiltonian-sextic-core/1`. Pass
`--schema 2` on the CLI or `schema=2` to `classify_sextic` to opt in to
`hamiltonian-sextic-core/2`, which adds the complete quadratic-complement and separable cubic/quartic-complement families.

```sh
python research/hamiltonian/partner_lab.py sextic-core --schema 2 --H '(q*p+q^3)^2'
```

This example has a three-dimensional core. For `q^6+q^2*p^2`, the first
refinement is three-dimensional and the second refinement drops to
`span{1,H}`. The full quadratic family also includes infinite intermediate
spaces: `q^6+p^2` has least depth five, while
`(p+q^3)^2+q^3` has least depth six.

Schema 2 has `classification.stages`, indexed from zero, and
`classification.depth = {"value": r, "kind": "least" | "sufficient"}`.
A stage is either `classified` with its exact `space`, or `unknown` with
`space: null` and a reason. The space kinds are `finite_basis`,
`polynomial_family`, and `module_plus_finite`. A `module_plus_finite` space
adds the rational `finite_span` to the stated polynomial module.
`classification.Dinf` gives the persistent core. A least-depth claim includes
an exact `sharpness_witness` whose first nonzero defect occurs at that depth.
Schema 1 still uses the following established fields:

| Field | Meaning |
| --- | --- |
| `status` | `classified` or `unsupported` |
| `input` | The original polynomial; its scale and lower-degree terms are preserved |
| `leading.terms` | The homogeneous degree-six part |
| `leading.geometric_root_pattern` | Root multiplicities over an algebraic closure, in decreasing order |
| `leading.infinity_multiplicity` | Multiplicity at `[1:0]` in the declared dehomogenization |
| `leading.factorization` | Rational homogeneous factors, their multiplicities, geometric degrees, and exact scalar |
| `classification.S1`, `classification.S2`, `classification.Dinf` | The first refinement, second refinement, and persistent core |
| `classification.sufficient_refinement_depth` | A depth at which the refinement equals the core |
| `quadratic_lift` | The leading quadratic and its linear correction, or an exact certificate that no correction exists |
| `obstruction` | A surviving first-refinement observable and its nonzero second-iterate correction, when present |
| `proof_boundary` | The all-degree theorem dependencies and the exact computational scope |

In schema 2, legacy obstruction and lift records live inside `classification`.
For the complete quadratic family, its sharpness witness and square first
integral have their own named fields. Schema 2 supersedes the earlier narrow
weight-six/weight-seven stage shape from PR #16; the default schema-1
contract remains unchanged.

A polynomial is an ordered list of records with keys `q`, `p`, and
`coefficient`. The coefficient is a rational string, such as `"-7/3"`.
An empty term list represents zero.

A finite space has `kind: "finite_basis"`, an integer `dimension`, and a
list of basis polynomials. An infinite space has
`kind: "polynomial_family"`, `dimension: null`, a finite list of
`coefficient_generators`, and a finite `module_basis`. Its elements are the
sums of arbitrary polynomials in the coefficient generators multiplied by
the module basis elements. In the `(3,3)` case the coefficient generator is
a rational quadratic, including when its two geometric roots do not split
over the rationals.

For an inhomogeneous quadratic lift, the report includes either a nonzero
two-by-two minor proving uniqueness or a nonzero three-by-three augmented
minor proving inconsistency. Each selected row identifies its gate and
monomial coefficient, so it can be reconstructed directly from the input.
All equations, including rows outside the certificate, are checked when a
lift is returned.

An unsupported result retains the exact input and leading-root analysis.
Schema 1 sets `S1`, `S2`, `Dinf`, and the sufficient depth to `null`.
Schema 2 sets its depth, stages, core, and witness fields to `null`.
The CLI prints that JSON and exits with status 2. Successful classifications exit with status 0.
Malformed input is reported as an argument error with status 2.

## Python API

The same calculation is available from `sextic_core.classify_sextic(H)`.
Use `classify_sextic(H, schema=2)` or `classify_sextic_v2(H)` for the complete
stage interface. Both schema-2 entry points return the same report.
The input is a mapping from exponent pairs to `fractions.Fraction` or integer
coefficients, matching the existing sparse engine. For example, from the
`research/hamiltonian` directory:

```python
from fractions import Fraction
from sextic_core import classify_sextic

result = classify_sextic({(4, 2): Fraction(1), (3, 0): Fraction(1)})
print(result["classification"]["S1"]["dimension"])    # 3
print(result["classification"]["Dinf"]["dimension"])  # 2
```

The API rejects floating coefficients, boolean exponents or coefficients,
negative exponents, and malformed monomial keys. It does not parse strings.

## Independent replay and the proof boundary

From the repository root:

```bash
python -m unittest discover -s research/hamiltonian/c3_strata -p test_sextic_core.py -v
python research/hamiltonian/c3_strata/verify_sextic_core.py
python -B -X utf8 -S research/hamiltonian/verify_cli.py
```

The schema-1 classifier evaluates explicit odd-transvectant contractions. The
replay uses the maintained defining star-exponential engine to check the same
observable and its iterates. Some schema-2 producers, including the quadratic
helper, also use that engine; their independent supplied-report checker has
separate scope recognition and space-comparison logic. In these conventions, the
`hbar^2` coefficient is `-T3/24`, and its `hbar^4` coefficient is `T5/1920`.
The checks include nonsplit factors, the point at infinity, rational changes
of coordinates, affine translations, scalar changes, finite-dimensional
kernels, infinite-family samples, and unsupported inputs.

The retained [replay receipt](SEXTIC_CORE_REPLAY.json) records the cases,
counts, and source digests for the delivered implementation.

These finite checks validate the implementation and witnesses. Completeness
in unbounded observable degree rests on the theorem identified for each family.
The [homogeneous theorem](SEXTIC_STRATA_THEOREM.md) and
[filtered extension](INHOMOGENEOUS_THEOREM.md) use the inherited monomial,
static-tail, covariance and descent arguments where stated. The
[quadratic](QUADRATIC_SIXFOLD_THEOREM.md),
[separable](SEPARABLE_SIXFOLD_THEOREM.md) and
[weighted](WEIGHTED_SEPARABLE_THEOREM.md) classifications supply their own
all-degree arguments; the latter two do not inherit the old static-tail proof.
The output explicitly records `formalized: false`: the complete classifier
is not an end-to-end Lean formalization. The separate finite Lean bridge
keeps its own stated scope. No literature-priority claim is made.


## Verify a supplied report

The dedicated checker takes the intended input separately and does not call
the classifier to establish the report's correctness:

```bash
python research/hamiltonian/partner_lab.py sextic-core --schema 2 --H 'q^6+p^3' > result.json
python research/hamiltonian/c3_strata/verify_sextic_report.py result.json --H 'q^6+p^3'
```

It rejects malformed or omitted claims, validates the exact module structure,
and reconstructs the theorem's full finite bounding space where applicable.
The acceptance receipt distinguishes all-degree conclusions conditional on
written theorems from compiled Lean results. Hashes bind source versions;
they do not prove a theorem.

The broader separable theorem, valid for potential degree at least five, is
available independently of the sextic interface:

```bash
python research/hamiltonian/partner_lab.py separable-core --H 'q^7+p^3+q'
```

See [the research capabilities](../RESEARCH_CAPABILITIES.md) for examples,
complete reproduction commands and the remaining classification boundaries.

The `weighted-core --H` command also accepts the mixed lower-weight family
for potential degrees above six. See [the weighted theorem](WEIGHTED_SEPARABLE_THEOREM.md)
for its exact cone, complete envelope and all-odd-gate treatment.
