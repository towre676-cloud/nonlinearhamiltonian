# Hamiltonian workstream: exact dynamic cores by finite operator certificates

## The decisive enhancement

The strongest next step is an all-degree **operator-closure compiler**. The existing report has solved the static partner spaces for all cubics, homogeneous quartic dimensions, arbitrary-coefficient `qF(p)` Hamiltonians and monomial classification in its stated scopes. Re-enumerating those kernels would mostly repeat completed work. The unresolved question is what remains exact under **every repeated Hamiltonian action**, and how to certify that answer without a false degree cutoff.

For one canonical pair over `Q`, let `R=Q[q,p]`, `D=D_H=H_q ∂p−H_p ∂q`, and `C_j=T_(2j+1)(H,·)` for every nonzero higher odd transvectant. The polynomial Hamiltonian supplies only finitely many nonzero `C_j`. The full dynamic exact core is

$$
\mathcal D_\infty(H)=\{G\in R:C_jD^rG=0\text{ for every }j\ge1,r\ge0\}.
$$

The parent atlas's finite observability machinery treats a parallel expression as an invariant invisible subspace. Here the state space is infinite dimensional and `D` can increase degree. That distinction is precisely why operator algebra is useful: it gives a finite stopping argument without projecting away escaping terms.

## A proved abstract reduction, not an unimplemented solution claim

Let `W₂=Q[q,p]⟨∂q,∂p⟩` be the second Weyl algebra, with `[∂q,q]=[∂p,p]=1` and the remaining coordinate/derivative pairs commuting. Operator multiplication is composition: the right factor acts first. Define **left** ideals

$$
I_r=\sum_{j,\,0\le s\le r}W_2(C_jD^s),\qquad I_\infty=\bigcup_{r\ge0}I_r.
$$

Then `I_(r+1)=I_r+I_rD`. Since `W₂` is left Noetherian, this ascending sequence stabilizes at some finite index `r₀`. At stabilization `I_rD⊆I_r`, and the polynomial common kernel of a finite generating set for `I_r` is exactly `D∞(H)`.

The Noetherian assertion follows from the Bernstein filtration: the associated graded algebra is the commutative polynomial ring in `q,p,ξq,ξp`. Leading symbols of a left ideal form a graded ideal; finite generation there can be lifted and lower-degree remainders removed recursively. Thus every left ideal is finitely generated and ascending chains stabilize. To obtain an algorithm, compute a left Gröbner basis `P₁,…,P_m`, reduce every **right product** `P_iD`, adjoin nonzero remainders, and repeat. Equality `I_(r+1)=I_r` is the stopping criterion. A flat spot in a truncated polynomial kernel is not.

The kernel statement has two short directions. If all `C_jD^s` annihilate `G`, their left multiples annihilate `G`, so the stabilized generators do too. Conversely the stabilized ideal contains all `C_j` and is right-`D` stable. Its common kernel is therefore contained in the one-step partner space and invariant under `D`, hence is contained in every correction-output kernel. No polynomial-degree restriction enters either direction.

This argument is standard filtered/Weyl-algebra reasoning applied to the present dynamic-core problem. It is a newly supplied **abstract reduction in this handoff**, with no literature-priority claim. It does not assert that a Gröbner backend has been implemented, that its complexity is small, that its quotient is holonomic, or that solving the resulting polynomial PDE system has already been classified. A finite PDE presentation can have an infinite-dimensional polynomial solution space.

## Receipts that make a heavy backend independently checkable

The discovery backend may be Macaulay2's WeylAlgebras or Singular/Plural, but its output should be exact identities replayed by the bundled standard-library checker. Do not trust a bare `normal form = 0` log. Export three kinds of receipt for the proposed generators `P_i`:

$$
C_j=\sum_iU_{ji}P_i,\qquad
P_i=\sum_{j,s}V_{ijs}C_jD^s,\qquad
P_iD=\sum_\ell A_{i\ell}P_\ell.
$$

Every multiplier belongs to `W₂` and acts on the left. The first identities put all correction gates in the candidate ideal; the second prove provenance inside the true iterated correction ideal; the third prove right-`D` closure. Together they identify the candidate ideal with `I∞`, and identify its polynomial common kernel with the dynamic core in **all degrees**. Retaining both containments is essential: closure of an arbitrary larger ideal could certify a proper subspace only.

The bundled `extensions/hamiltonian/weyl_receipts.py` already implements exact normal-ordered arithmetic, operator action, gate construction, receipt replay and rejection of a false closure receipt. It does **not** discover Gröbner bases. Operator rows are `[q_exp,p_exp,dq_exp,dp_exp,"rational"]`; polynomial rows omit derivative exponents. The schema is `weyl-invariant-kernel-v1`. Coefficients are exact rational strings or integers; floats are rejected. Products are checked as operators, not merely on a sampled polynomial grid.

The example `q_cubed_receipt.json` proves an all-degree kernel description for `H=q³`: `C₃=6∂p³`, `D=3q²∂p`, `P=∂p³`, and `PD=DP`. Its polynomial kernel is precisely `A(q)+pB(q)+p²C(q)`. This simple calibration is deliberately within a known solved cubic scope; the deliverable is a working receipt format and checker.

Run from the package root:

```bash
python3 -B extensions/hamiltonian/weyl_receipts.py --self-test
python3 -B extensions/hamiltonian/weyl_receipts.py --check extensions/hamiltonian/q_cubed_receipt.json
python3 -B extensions/hamiltonian/weyl_receipts.py --self-test --existing-engine research/hamiltonian/independent/engine.py
```

The recorded starter run passed 200 operator-composition/action cases, 120 defining-transvectant cases, 40 Hamiltonian-derivation cases, two valid receipts, three deliberately false containment/provenance/closure receipts rejected, and 40 comparisons with the existing independent direct-star engine. These are implementation checks; the abstract all-degree reduction is justified by the proof above.

## First theorem target: a full quadratic-perturbation stratification

Use `H_θ=qp³+a q²+b qp+c p²+dq+ep+f` as the first concrete research family. Its higher correction operators are identical for every `θ`, so every member has the same one-step exact space

$$
\mathcal E(H_\theta)=\mathbb Q[p]\oplus q\mathbb Q[p]\oplus q^2\mathbb Q[q^3p].
$$

The Hamiltonian derivation changes with `θ`, and the dynamic core can change drastically. Produce exact parameter strata **under declared affine-symplectic transformations and nonzero Hamiltonian rescaling**, with a certificate and explicit polynomial solution description on each stratum. Parameter branching must state which coefficients were divided by and retain exceptional loci. Sampled parameter values do not classify the whole family. A comprehensive Gröbner or elimination output needs independent rational operator receipts on every branch and separate proofs of branch coverage.

A useful corollary is already derivable from the existing report. For `H_λ=qp³+λq²`,

$$
\mathcal D_\infty(H_0)=\mathbb Q[p]\oplus q\mathbb Q[p],\qquad
\mathcal D_\infty(H_\lambda)=\operatorname{span}_{\mathbb Q}\{1,H_\lambda\}\quad(\lambda\ne0).
$$

The report proves the cases `λ=0,1`. Over a field extension choose `a⁴=λ` and the linear symplectic pullback `U_a:q↦aq,p↦a⁻¹p`. Then `H_λ=a²U_a(H_1)`. Linear symplectic covariance and nonzero rescaling preserve the dynamic-core construction, so the result transfers; coefficient comparison descends the span to the rational base field. Thus an arbitrarily small nonzero quadratic perturbation preserves the **entire** one-step partner space while collapsing an infinite dynamic core to dimension two. This is a direct corollary, not a new priority claim.

For an independent direct check when `λ≠0`, set `Y=q+p³/(2λ)`. The finite global reduction used in the report becomes the candidate span `{1,p,p²,Y,pY,H_λ}` with

$$
Dp=2\lambda Y,\quad DY=\frac{3p^5}{2\lambda},\quad
Dp^2=4\lambda pY,\quad D(pY)=2H_\lambda+\frac{2p^6}{\lambda}.
$$

The outside terms remove `Y,pY`, and invariance then removes `p,p²`. Transferring the report's proved all-degree reduction, rather than merely observing these six vectors, is what establishes the complete answer. This is a regression/calibration branch before tackling all six quadratic/lower coefficients.

## Follow-on theorem target: homogeneous quartic dynamic-core moduli

The static Hilbert function `dim E_n=2+1_(e divides n−2)` is complete and must remain a regression theorem, not be rediscovered. The next questions concern the pair `(E(H),D∞(H))` and its stable exact Lie sectors. Begin with the distinct-root normal form `q⁴+λq²p²+p⁴`, retain `λ=±2` as square strata, and include fourth-power and repeated-root boundary forms separately. Root multiplicity alone does not determine partner bases. Seek invariant certificates whose parameter denominators expose exceptional loci; then solve their polynomial common kernels and prove completeness. Do not announce a “generic two-dimensional core” from finite degree tests; even its correct candidate and hypotheses require a proof.

The Hessian is a canonical active one-step partner for nonsquare quartics, but it need not remain exact under the next action. The existing `H=q⁴+p⁴`, `G=q²p²` counterexample and the exact second-action correction must remain in the negative fixture set. Ordinary powers `H^r` need not be exact, whereas star powers have a different role. A Poisson centralizer cannot simply be inserted into the exact core without the correction gates.

## Acceptance gates for Claude Code

The first commit should retain the baseline replay and add the receipt schema, operator checker tests and a discoverer adapter behind an optional dependency. The second should export and independently replay a nontrivial right-`D` closure receipt beyond `q³`, with both ideal containments and a written derivation of its polynomial solutions. The third should establish the `λ` corollary and then one additional quadratic-perturbation stratum, with explicit denominator branches and a machine-readable certificate. A full six-parameter classification is a stretch objective; unresolved branches remain unresolved rather than inferred from random tests.

For every claimed dynamic core, test automatic members `1,H`, all correction gates, every proposed generator's action, covariance under rational affine-symplectic maps, and negative fixtures where the first bracket agrees but the second does not. Check that deliberately corrupted provenance, correction-containment and closure multipliers fail. A resource limit returns `incomplete`, never a classification. Do not infer equality of Weyl ideals from equality of their polynomial solution spaces: in particular the known polynomial core for `qp³` does not by itself prove `I∞=W₂∂q²`.

The existing pinned PerfectJet sextic work through degree 20 and its archived msolve dependencies remain prior work with the declared trust boundary. This workstream neither reruns those verdicts nor classifies all sextics in all degrees. Higher-degree arbitrary full-polynomial partners, multiple canonical pairs and nonlinear coordinate changes belong to later explicitly scoped work.

## Primary implementation references checked for this handoff

Macaulay2's official WeylAlgebras documentation describes the available Weyl/D-module operations, including weighted left Gröbner bases. Its `gbw` documentation states the left-ideal convention and distinguishes ordinary positive-weight Buchberger calculations from cases needing adapted algorithms. These references support the proposed optional discovery adapter, not a claim that it has run here.

https://macaulay2.com/doc/Macaulay2/share/doc/Macaulay2/WeylAlgebras/html/index.html

https://www.macaulay2.com/doc/Macaulay2-1.25.11/share/doc/Macaulay2/WeylAlgebras/html/_gbw.html

The primary research paper *Universal Groebner Bases in Weyl Algebras* supplies related general left-ideal Gröbner-basis foundations; its existence theorem does not make the present parameter classification automatic.

https://arxiv.org/abs/1011.5159
