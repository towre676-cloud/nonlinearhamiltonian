# Exact structural machinery: two high-value workstreams

This handoff is grounded in the published `nonlinearhamiltonian` collection. It proposes concrete extensions to the implemented finite examples. It does not label proposed engines as already implemented or claim literature priority for classical constructions. Paths below are relative to the published repository root.

## Recommendation and relation to the other programmes

The strongest structural enhancement is a **certificate-carrying obstruction compiler**. Its output is not merely a rank, a small residual or a similar-looking reduced model: it returns a solution, a nonzero obstruction class, or an explicit violation of the supplied algebraic model. A finite contraction is the central witness:

$$
pi=I_H,\quad di=0,\quad pd=0,\quad I_C-ip=dh+hd.
$$

These identities certify which information a reduction preserves. They supply the same *linear certificate interface* for graph gluing, finite cellular cohomology and order-by-order deformation calculations, while leaving their different coefficient rings and nonlinear structures explicit. The archived models already prove the relevant examples, but the general operations are currently recipes. Turning those recipes into validated arbitrary-input finite operations is a substantial practical expansion of the collection.

The second workstream is an **arithmetic orbit compiler**. It turns a proved reduction interval into a finite seed list and then combines exact unit dynamics with congruence conditions and height cutoffs. Unlike unrestricted Diophantine search, its declared input includes an explicit norm-one unit. A general reduction proof below extends the collection's specific $D=2$ model without pretending that bounded enumeration by itself proves completeness.

The accompanying `extensions/structure/` now supplies a runnable first step: a standard-library rational-complex constructor, a standalone identity checker, primitive-or-obstruction output and six test groups including forty deterministic generated complexes. The checker never imports the constructor or performs elimination. This new seed does not implement the proposed integer, cellular-sheaf or DGLA adapters. `extensions/structure/arithmetic_future_fixtures.json` supplies four independently compared finite arithmetic fixtures for the optional later workstream.

The common standard is a small independent checker with exact arithmetic. This does not identify all these theories: a chain equivalence alone does not preserve a nonlinear Lie bracket, an integral lattice cannot be replaced silently by a rational vector space, and a finite modular orbit does not certify all integer solutions until the reduction theorem has been supplied.

## Workstream A: certified complexes, obstruction classes and finite deformation lifting

### What exists now

The published material already supplies explicit proofs and finite exact tests for chain contractions, signed total complexes, mapping cones, integral torsion, gluing and Maurer–Cartan obstructions. The live L09 model computes rational homology only for its fixed triangle, square and $K_{3,3}$ examples. L05 illustrates ordered shears; it is not a cellular-sheaf solver. The archive explicitly does not implement arbitrary chain complexes, general sheaf cohomology or a general deformation solver.

Read `compendium/readable/families/D04-F02.md`, `D04-F03.md`, `D04-F04.md`, `D05-F01.md`, `D05-F03.md` and `D16-F06.md`. The underlying family definitions are in `compendium/atlas/data/atlas.json`. Exact supporting models are in `compendium/atlas/domains/geometry/verify.py`; read the named checks `G04-chain-contraction`, `G06-obstruction-class` and `G09-homology-and-torsion`. Bridge B02 records the coefficient-system and geometry boundaries.

Useful anchor treatments are `2025:Y25-03-021` (cohomology-preserving blocking), `2025:Y25-10-004` (mapping cone), `2026:Y26-05-002` (contraction and perturbation), `2026:Y26-07-023` (total signs), `2026:Y26-07-021` (integer torsion), `2026:Y26-07-022` (circle local system), `2026:Y26-02-007` and `2026:Y26-05-029` (actual deformation obstruction). The full treatment pages are under `compendium/readable/years/YEAR/SOURCE_ID.md`.

### First theorem to implement and independently check

Let $(C^\bullet,d)$ be a bounded complex of finite-dimensional rational vector spaces. Let $H$ have zero differential, and supply rational matrices $i,p,h$ satisfying the contraction identities above, with the appropriate degrees. For every cocycle $b\in C^k$,

$$
du=b\ \text{is solvable}\quad\Longleftrightarrow\quad p_kb=0.
$$

When $p_kb=0$, a certified primitive is $u=h_kb$. If $p_kb\ne0$, a coordinate functional $\ell$ on $H^k$ can be chosen with $\ell(p_kb)\ne0$. Then $\lambda=\ell p_k$ satisfies

$$
\lambda d^{k-1}=0,\qquad \lambda b\ne0,
$$

and is an exact separating witness proving that $b$ is not a boundary. The proof is one line of the contraction identity: $b-ipb=dhb+hdb=dhb$. Necessity follows from $pd=0$. The small checker needs matrix multiplication and exact rational arithmetic, rather than trust in the basis-reduction algorithm that generated the certificate.

This gives three different return types: `solved` with a primitive; `obstructed` with a cocycle class and separating functional; and `invalid_model` with an entry witnessing $d^{k+1}d^k\ne0$ or an invalid certificate identity. An invalid complex must never be assigned a Betti vector as though its quotient existed.

### Exact implementation target

Represent rational coefficients as normalized numerator/denominator pairs and serialize matrix dimensions explicitly. Validate the entire complex before computing invariants. Use exact elimination to split each degree into boundaries, chosen cohomology representatives and a complement mapped isomorphically onto the next boundaries. Construct $i,p,h$ from those splittings and retain all matrices. The independent checker must not import the constructor or reuse its elimination routines.

Implement finite graph incidence and finite cellular coefficient systems as adapters into this kernel. For a graph, return either a root-gauge potential or a cycle-period witness. For a cellular coefficient system, construct the actual restriction/transport matrices and require the face-composition identities that make $d^2=0$. A graph's ordinary cycle rank is not the dimension of cohomology for every local system.

For a circle with rank-one nonzero transports $r_j$, verify the exact result controlled by $h=\prod_jr_j$: both $H^0$ and $H^1$ have dimension one for $h=1$, and both vanish for $h\ne1$. Test the archived rational triples $(2,3,1/6)$ and $(2,3,1)$, which have identical underlying graph but different cohomology.

### Integer adapter: retain torsion with unimodular witnesses

Keep this adapter distinct from rational contraction. For a chain complex of free integer modules with $d_k:C_k\to C_{k-1}$, compute a Smith certificate

$$
U d_k V=\operatorname{diag}(s_1,\ldots,s_r,0),\qquad \det U,\det V\in\{\pm1\}.
$$

The last columns $K=V[:,r:]$ form an integer basis of $\ker d_k$. In the transformed coordinates $V^{-1}d_{k+1}$, the first $r$ rows must be zero. Write the remaining rows as $B$, so $d_{k+1}=KB$. A second Smith certificate $PBQ=\operatorname{diag}(t_j,0)$ gives

$$
H_k\cong\mathbb Z^{n_k-r-\operatorname{rank}B}\oplus\bigoplus_{t_j>1}\mathbb Z/t_j.
$$

Every reported torsion relation must include a chain witness: the generator is $KP^{-1}e_j$ and $d_{k+1}Qe_j=t_jKP^{-1}e_j$. Verify both unimodular transformations, the divisibility conditions on Smith diagonals, and these actual relations. Computing $\operatorname{coker}d_{k+1}$ in the wrong ambient group is a mandatory negative test. Rational rank alone cannot detect the $\mathbb Z/2$ class of the archived $\mathbb{RP}^2$ cellular model.

### Deformation adapter: compute a class, not only a defect vector

For a finite differential graded Lie algebra over $\mathbb Q$, verify $d^2=0$, graded skew symmetry, graded Jacobi and the differential derivation law on the supplied basis. Set

$$
\alpha(t)=\sum_{n\ge1}a_nt^n,\qquad
d\alpha+\tfrac12[\alpha,\alpha]=0.
$$

At order $n$ the next equation is

$$
da_n=b_n,\qquad b_n=-\tfrac12\sum_{i+j=n}[a_i,a_j].
$$

After the lower orders have been solved, the Bianchi identity $dR+[\alpha,R]=0$ for $R=d\alpha+[\alpha,\alpha]/2$ shows that $db_n=0$. Apply the contraction interface: output the class $p_2b_n$, a separating witness when it is nonzero, or a correction $a_n=h_2b_n+i_1z_n$ when it vanishes. The cohomology parameter $z_n$ must either remain explicit or be fixed by a declared branch convention. Choosing $z_n=0$ produces a particular lift, not a classification of all lifts. Gauge equivalence requires its actual degree-zero action; do not claim a moduli quotient when that action has not been implemented.

The archived finite fixture has $L^1=\mathbb Qa\oplus\mathbb Qb$, $L^2=\mathbb Qc$, $db=c$, $da=0$, $[a,a]=2c$ and all other relevant brackets zero. The nonzero defect $c$ is exact and $\alpha=ta-t^2b$ solves the equation exactly. Removing $b$ leaves a genuine nonzero obstruction class. Both cases must be accepted as different outcomes by the same checker.

Finite success through order $N$ is not all-order existence. The retained scalar example $s^{13}=0$ passes through order twelve and fails at thirteen. A useful stronger theorem milestone is formal existence when $H^2=0$ in the stated $t$-adically complete setting: the closed defect is exact at every recursive order. That is a classical formal conclusion, with no analytic convergence assertion. A comparison of deformation problems requires bracket-compatible or explicitly transferred higher structure; a chain equivalence of the underlying complexes alone is insufficient.

### Deliverables and acceptance criteria

Create a documented exact-complex schema; a constructor; a separate small checker; graph and cellular adapters; an integer Smith adapter with witnesses; and a finite-order DGLA adapter. Export operation results as typed JSON carrying coefficients, basis conventions, equations, witnesses and scope. The first user interface should expose `validate`, `cohomology`, `primitive-or-obstruction`, `compare-complexes` and `lift-to-order`, with exact examples and explicit unsupported-operation messages.

Acceptance requires all archived fixtures replayed through the new APIs; equivalent complexes related by an added contractible pair giving the same cohomology; actual verification of a supplied chain homotopy; both sides of the exceptional perturbation $d_\epsilon e=(1+\epsilon)u$ with failure at $\epsilon=-1$; a nonzero harmonic class correctly reported as nonzero despite zero Laplacian residual; correct torsion for the projective-plane cellular model; inconsistent cellular face data rejected; and a forged witness rejected by the independent checker. Use deterministic generated small complexes and exact basis changes to cover more than the hand-written examples. Report dimensions, coefficient bit sizes and runtime as workload-specific measurements. Do not promise efficient arbitrary-size Smith reduction or symbolic classification for every parameter family.

## Workstream B: exact arithmetic orbit and congruence compiler

### What exists now

The $D=2$ Pell and norm $-7$ models have complete written reduction proofs, exact arithmetic checks and a live two-seed negative-Pell navigator. Positive-Pell and congruence-filter controls are explicitly extensions, not current UI capabilities. The live model does not solve general quadratic norm equations.

Read `compendium/readable/families/D01-F04.md`, bridge B06, and `compendium/atlas/domains/arithmetic/verify.py`, especially `L10 Pell invariants, seed interval and modular filter`. Source anchors are `2024:Y24-03-024`, `2026:Y26-05-005`, `2026:Y26-09-029` and `2026:Y26-10-006`.

### General reduction derivation supplied for implementation

Fix a nonsquare integer $D>0$, an integer $N\ne0$, and a supplied integer unit $\epsilon=a+b\sqrt D>1$ with $a,b>0$ and $a^2-Db^2=1$. Work in the declared order $\mathbb Z[\sqrt D]$, with integer coordinates. The unit need not be the fundamental unit. A proper power gives more representatives, but still a complete classification under its own cyclic action. No assertion about the full ring of integers, all units, ideal classes or general Diophantine equations is implicit.

For $\alpha=x+y\sqrt D>0$ of norm $N$, choose the unique integer $j$ such that $\beta=\alpha\epsilon^{-j}$ lies in

$$
[\sqrt{|N|},\epsilon\sqrt{|N|}).
$$

Multiplication and inverse multiplication preserve integer coordinates because the unit matrix is

$$
A=\begin{pmatrix}a&Db\\ b&a\end{pmatrix},\qquad
A^{-1}=\begin{pmatrix}a&-Db\\-b&a\end{pmatrix}.
$$

The conjugate of $\beta$ is $N/\beta$, so

$$
x_\beta=(\beta+N/\beta)/2,\qquad
y_\beta=(\beta-N/\beta)/(2\sqrt D).
$$

If $N>0$, the reduced seed has $x>0$, $y\ge0$ and

$$
0\le y<b\sqrt N\quad\Longleftrightarrow\quad y^2<b^2N.
$$

If $N=-m<0$, it has $x\ge0$, $y>0$ and

$$
0<y<a\sqrt{m/D}\quad\Longleftrightarrow\quad Dy^2<a^2m.
$$

These are exact integer search bounds. In the first case enumerate such $y$ and test whether $N+Dy^2$ is a square; in the second test whether $Dy^2-m$ is a nonnegative square. The positive square root gives the canonical $x$. The bounds are equivalent to the half-open interval on the relevant branch: the coordinate functions are increasing there. Lower endpoints $y=0$ for positive norm and $x=0$ for negative norm are permitted; the upper endpoint is excluded. No floating logarithm or radical comparison is needed.

Every solution with $\alpha>0$ therefore belongs to exactly one listed seed times a signed power of $\epsilon$. Overall negation covers $\alpha<0$. For the nonnegative-coordinate branch the reduced seed followed by $j\ge0$ suffices. This is the general reduction argument; the finite square tests verify the representatives only after that argument has established their search bound. It is a classical mechanism expressed here as a constructive certificate specification, not a priority claim.

For $(D,N,a,b)=(2,-7,3,2)$ the bound is $2y^2<63$, so $y=1,\ldots,5$ and the seeds are exactly $(1,2),(5,4)$. For $(3,-2,2,1)$ the seed is $(1,1)$. For $(5,-4,9,4)$ the seeds are $(1,1),(4,2),(11,5)$. The latter deliberately uses the declared integer-coordinate order and unit; do not replace it with a half-integral unit without changing the input model.

### Exact modular filters and height counts

Reduce the full state $(x,y)$ modulo a positive integer $q$. Since $\det A=1$, the map is a permutation, so the orbit is periodic with no transient tail. For every seed, enumerate the full cycle, its period $P$, and accepted index residues $J\subseteq\{0,\ldots,P-1\}$. Repeated $x$ coordinates alone do not establish a full-state period.

For the nonnegative-coordinate branch, find the largest index $M(Y)$ satisfying $y_j\le Y$ by exact recurrence or matrix exponentiation and integer comparison, using exponential bracketing followed by binary search. Count accepted indices without iterating to the height:

$$
\#\{0\le j\le M(Y):j\bmod P\in J\}
=\sum_{r\in J,\ r\le M(Y)}\left(1+\left\lfloor\frac{M(Y)-r}{P}\right\rfloor\right).
$$

For each fixed seed $y_j\sim c\epsilon^j$, giving the corresponding height population $(|J|/P)\log Y/\log\epsilon+O(1)$. Sum over the proved seed list. This asymptotic concerns the specified one-sided branch and filter. Signed powers for negative norm have a two-sided height interval and need their own counting convention. The exact count must not depend on rounding the displayed logarithm.

Multiple congruence filters can be tested on a common modulus or combined with a proved phase/period construction. Do not identify periods with moduli or invoke CRT without checking the compatibility conditions. The finite-state enumeration can be expensive when $q$ is large; the first release should declare a state budget and return a resource-limit status rather than silently truncate a cycle.

### Certificates, fixtures and acceptance

The certificate should contain $(D,N,a,b)$, the declared order and sign branch, the unit identity, the derived seed-bound tag and exact endpoint inequalities, every square-tested seed, complete modular cycle witnesses, accepted indices and exact height-count endpoints. The checker independently verifies norms, seed enumeration under the proved bound, bijective unit transport, cycle closure and counts. A seed generator without a valid reduction bound must be labeled exploratory and must not emit `complete`.

The accompanying `extensions/structure/arithmetic_future_fixtures.json` is a small exact fixture set. Its height-$1000$ populations in the nonnegative-coordinate branch are: $D=2,N=-7$, eight solutions and zero with $y\equiv0\pmod3$; $D=2,N=1$, five solutions including $(1,0)$ and three accepted; $D=3,N=-2$, six solutions and two accepted; $D=5,N=-4$, eight solutions and zero accepted. These finite comparisons support implementations; the reduction proof supplies the all-height conclusion.

Acceptance requires reproduction of the existing $D=2$ model, both negative-norm seeds retained, exact endpoint handling, a chosen unit that is a proper power tested without a false fundamental-unit claim, signed and one-sided branches distinguished, no-period-tail checks on the full modular state, and exact height counts independently compared with bounded integer square enumeration. Reject square or nonpositive $D$, zero norm, an invalid claimed unit, malformed residues and an exhausted state/seed budget. An empty seed list is a complete negative conclusion only after the declared reduction bound has been fully exhausted.

The first implementation scope should use supplied units and modest derived seed bounds. Finding minimal units and treating the maximal order are later adapters with their own proofs. This compiler does not solve arbitrary elliptic, higher-genus or unrestricted polynomial Diophantine equations.

## Execution priority for Claude Code

Build Workstream A's rational certificate kernel first, because it upgrades the widest set of current recipes. Add integer homology as a deliberately separate coefficient adapter, then finite-order deformation lifting with an explicit class-versus-vector interface. Workstream B can proceed independently as a sharply scoped complete-classification demonstration. Reuse archived examples as regression fixtures, but retain independent checker code and counterexamples. Update the domain capability contracts only after the corresponding operation is implemented and tested; do not retag a recipe as live merely because it now has a task specification.

No current theorem in the source collection should be overwritten by a stronger unproved statement. Put conjectures, intended theorem targets and completed derivations in distinct status fields. Commit source, proofs, fixtures, receipts and capability-contract changes together after relevant checks pass.
