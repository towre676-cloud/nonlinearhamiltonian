# C3: uniform depth-one refinement for the sextic family and monomial sextics

**Date:** November 4, 2026. **Status:** computer-assisted theorem for the complete stated C3 scope, relative to the retained static-tail theorems identified below. No formal proof-assistant certification or literature-priority claim is made.

## Theorem and conventions

Let K be a characteristic-zero field. Work in K[q,p], with

\[
T_k(F,G)=\sum_{j=0}^k(-1)^j\binom{k}{j}
 (\partial_q^{k-j}\partial_p^j F)(\partial_q^j\partial_p^{k-j}G),
\qquad D_H G=T_1(H,G).
\]

For a sextic H define E(H)=ker T_3(H,·) ∩ ker T_5(H,·),

\[
 S^1(H)=\{G\in E(H):D_HG\in E(H)\},\qquad
 D_\infty(H)=\bigcap_{r\ge0}\ker(T_3D_H^r)\cap\ker(T_5D_H^r).
\]

Then for **every** a∈K and H_a=q^6+a q^3p^3+p^6,

\[
\boxed{S^1(H_a)=D_\infty(H_a)=\operatorname{span}_K\{1,H_a\}.}
\]

For every homogeneous monomial sextic H=q^A p^B, A+B=6, A,B≥0,

\[
\boxed{S^1(H)=D_\infty(H).}
\]

The same holds for nonzero scalar multiples of these Hamiltonians. The zero Hamiltonian has the whole polynomial ring as both spaces. All assertions concern polynomial partners in the flat Weyl–Moyal convention. No assertion about general sextics outside the stated family and monomials follows.

The three notions remain distinct: E is the static space; S¹ imposes the gates after one classical derivative; D∞ imposes them after every iterate. The proof computes S¹ and exhibits its invariance, rather than inferring invariance from a bounded number of iterates.

## 1. Finite reduction for the family

D raises homogeneous degree by four; T_3 preserves it and T_5 lowers it by four. Thus all conditions separate by input degree. The retained static results give:

1. If a≠±2, H_a has six simple roots. Indeed x⁶+a x³+1 and its derivative have a common zero exactly when a²=4. The binary-static theorem for sextics says that, in degree n≥17, a sextic with a simple root can have a nonzero static partner only in root types (5,1) or (4,1,1). Neither is possible here. Therefore E_n(H_a)=0 for n≥17.
2. If a=2ε, ε=±1, the retained C2 chain proof for (q³+εp³)² gives E_n=0 for n≥9 (its main theorem already gives the sufficient bound n≥15). In particular E_n=0 for n≥17.

Consequently it suffices to determine S¹_n for 0≤n≤16, uniformly in a. The square parameters are treated by item 2, not by applying a simple-root theorem where it has no hypothesis.

For comparison, the completed static classification is concentrated in the following sectors. This table is retained context; the new finite-rank certificate does not assume that these lists exhaust the low-degree static kernels.

| Degree | Static basis beyond the universal low-degree spaces | Parameter condition |
|---|---|---|
| 0,1,2 | all of V_n | every a |
| 3 | q²p, qp² | a=0 |
| 3 | q³+(a/20)p³ | a²=400 |
| 4 | (qp)² | every a |
| 4 | q³p−(a/10)p⁴; q⁴+(a/5)qp³ | a²=−50 |
| 5 | qp⁴−(7a/40)q⁴p | a²=1600/49 |
| 6 | H_a | every a |
| 8 | G₈=q⁷p+qp⁷−(7a/20)(qp)⁴ | every a |
| 10 | q⁸p²+q²p⁸ | a=0 |
| 12 | q¹²+p¹²+11a(q³p⁹+q⁹p³)+33q⁶p⁶ | a²=−5 |
| 14 | q¹³p+qp¹³+(13a/20)(q⁴p¹⁰+q¹⁰p⁴)+(39/2)(qp)⁷ | a²=−50 |

All other static sectors vanish. In particular the square parameters have the generic static list. The certificate below handles every parameter in the table, as well as every other parameter, in one argument.

## 2. A polynomial certificate for the first refinement

Let V_n have basis q^c p^(n−c), 0≤c≤n. Assemble the polynomial matrix

\[
 M_n(a)=\begin{bmatrix}T_3\ T_5\ T_3D\ T_5D\end{bmatrix}_{V_n}.
\]

The first two blocks have entries linear in a, and the last two have entries at most quadratic in a. Its kernel is precisely S¹_n. Each H monomial has q-exponent congruent to zero modulo three. For any fixed row block (depth d, gate k), the output q-exponent of an input with c≡r is r−d−k modulo three. Hence distinct input residue classes have disjoint output supports inside each row block. This proves the decomposition into three independent blocks; it is not an assumption inferred from observed sparsity.

At n=0 discard the constant column, whose image is zero. At n=6 discard the q⁶ column. This gives a complement to K H_a for **every** a: subtracting the q⁶ coefficient times H_a leaves q⁶ coefficient zero, because H_a has q⁶ coefficient 1. At all other degrees retain every column. Denote the resulting residue blocks by B_{n,r}(a). Each has at most six columns.

The certificate `family_certificate.json` lists, for each of the 47 nonempty blocks, square maximal minors d_i(a) and rational-coefficient polynomials u_i(a) satisfying

\[
\boxed{\sum_i u_i(a)d_i(a)=1\quad\text{in }\mathbb Q[a].}
\]

There are 101 recorded minors in total. For any parameter a₀ in any characteristic-zero extension, not all d_i(a₀) can vanish, since their displayed linear combination is 1. Thus each B_{n,r}(a₀) is injective. This is an exact all-parameter rank argument, including algebraic and transcendental parameters; it is not a grid test or a generic-rank assertion with unspecified exceptions.

For example, for degree 1 and either nonempty residue block the selected minors are

\[
 d_1=-864(a^2+50),\qquad d_2=12960(a^2-40),
\]

and the explicit identity is

\[
 -d_1/77760-d_2/1166400=1.
\]

Thus even at a²=−50, where one gate coefficient vanishes, the complementary gate detects the direction. At n=6,r=0 a selected minor is the nonzero constant 10,368,000.

It follows that S¹_n=0 for n∉{0,6}, and S¹_0=K·1, S¹_6=K·H_a, throughout 0≤n≤16. The static-tail results extend this to all degrees. Both 1 and H_a are killed by D, and both are static partners (antisymmetry gives T_k(H_a,H_a)=0 for odd k). Hence their span is invariant and lies in D∞. Since always D∞⊆S¹, equality follows. This proves the family theorem.

Two simple exact operator calculations illustrate the dynamical mechanism. For G₄=(qp)²,

\[
 DG_4=12(q^7p-qp^7),\qquad
 T_3(H_a,DG_4)=-604800q^4p^4+12096a(q^7p+qp^7).
\]

The constant coefficient −604800 detects G₄ for every a. For G₈ from the static table,

\[
 DG_8=6(q^{12}-p^{12})-\frac{132a}{5}(q^9p^3-q^3p^9),
\]

\[
 T_3(H_a,DG_8)=
 -66528a(q^{12}+p^{12})+3193344a q^6p^6
 -38016(4a^2+25)(q^9p^3+q^3p^9).
\]

The coefficients a and 4a²+25 cannot vanish together, so G₈ never survives. This includes a=±2 explicitly. The full minor certificate supplies the corresponding simultaneous injectivity statements where several static basis vectors can mix.

## 3. Monomial sextics: a symbolic all-degree proof

Write m=q^c p^e, c,e≥0. Define

\[
 \psi_k(c,e)=\sum_{j=0}^k(-1)^j\binom{k}{j}(A)_{k-j}(B)_j(c)_j(e)_{k-j}.
\]

Whenever its coefficient is nonzero, T_k(H,m)=ψ_k(c,e)q^(c+A−k)p^(e+B−k), and

\[
 Dm=(Ae-Bc)q^{c+A-1}p^{e+B-1}.
\]

Terms needing negative exponents have zero derivative coefficients and are omitted. For each fixed operator, distinct input monomials have distinct output monomials. Therefore no cancellation between different inputs can conceal a failed gate, either statically or after one D-step. We may classify and test individual monomials. The swap q↔p exchanges A and B and changes harmless operator signs, so assume A≥B.

The exact factors are:

| (A,B) | ψ₃(c,e) | ψ₅(c,e) |
|---|---|---|
| (6,0) | 120e(e−1)(e−2) | 720(e)₅ |
| (5,1) | −60e(e−1)(c−e+2) | −120(e)₄(5c−e+4) |
| (4,2) | 24e[c²−3ce+2c+e²−3e+2] | 240ce(e−1)(e−2)(2c−e+1) |
| (3,3) | −6(c−e)[c²−8ce−3c+e²−3e+2] | −360ce(c−1)(c−e)(e−1) |

These are polynomial identities for all exponents, verified by expansion in `monomial_proof.py`.

For (6,0), ψ₃=0 precisely when e≤2. D lowers e, so the entire static strip is invariant.

For (5,1), outside e≤1, ψ₃=0 forces c=e−2. The cases e=2,3 give (c,e)=(0,2),(1,3). If e≥4, ψ₅ would also force 5c−e+4=0, but substituting c=e−2 gives 4e−6>0. Thus those two monomials are the only static extras. Their T₃D coefficients are −4800 and −20160, respectively, so both die in one step. The strip e≤1 is invariant since D preserves e.

For (4,2), put Q=c²−3ce+2c+e²−3e+2. The permanent static line is e=0. If e>0, ψ₅ forces c=0, e=1, e=2, or e=2c+1. The corresponding Q restrictions are (e−1)(e−2), c(c−1), c(c−4), and −c(c+3). Nonnegative integer solutions give only (0,1),(0,2),(1,1),(4,2). For e=0 the exact first-gate coefficient is

\[
 (Ae-Bc)\psi_3(c+A-1,e+B-1)=-48c(c+2)(c+3),
\]

which is nonzero for every c>0. The other noncore static directions (0,1),(0,2) have coefficients −576, −5760. The survivors are 1, qp, H. They are invariant because D1=DH=0 and D(qp)=2H.

For (3,3), the entire diagonal c=e is killed by D and by the odd gates. Off the diagonal, ψ₅ forces c∈{0,1} or e∈{0,1}. Restricting Q=c²−8ce−3c+e²−3e+2 to c=0 gives (e−1)(e−2), and to c=1 gives e(e−11); reflection covers the other cases. Hence the only static extras are (0,1),(0,2),(1,0),(2,0),(1,11),(11,1). Their T₃D coefficients are, in that order, −864, −4320, −864, −4320, −324000, −324000. Every one is nonzero.

Thus every static monomial outside the displayed invariant spaces is detected already by T₃D; T₅D is not needed in this monomial proof. The invariant cores, now also proved to equal S¹, are:

| H | S¹(H)=D∞(H) |
|---|---|
| q⁶ | K[q]+pK[q]+p²K[q] |
| q⁵p | K[q]+pK[q] |
| q⁴p² | span{1,qp,q⁴p²} |
| q³p³ | K[qp] |
| q²p⁴, qp⁵, p⁶ | swaps of the preceding appropriate rows |

This proves C3 for all seven monomials and every homogeneous degree, independently of a finite-degree extrapolation or the previously proved core classification.

## 4. Verification, dependencies, and limits

`family_certificate.py` is the producer. It computes gate coefficients by falling-factorial sums, selects minors, and constructs Bézout coefficients. `verify_certificate.py` does not import the producer: it rebuilds the operators by literal symbolic differentiation and recomputes all determinants using the signed permutation formula, without calling a matrix determinant routine. It checks the exact row/column conventions, completeness of the 47 blocks, all 101 determinants, and every Bézout identity. Its completed result is in `verification.json`.

`test_c3.py` supplies seven executable regression tests: full certificate replay; rejection of a corrupted Bézout coefficient; rejection of a missing block; the all-exponent monomial identities and a 23,247-monomial search through total degree 80, including all seven sextics; 32 random exact operator comparisons against the separate differentiation engine; all rational and quadratic exceptional static partners and their nonzero T₃D images; and replay of the retained static-tail certificate. The 32 comparisons each test T₁,T₃,T₅. Randomness has a fixed seed. The counterexample searches supplement the identities; they do not establish the unbounded claims.

The static simple-root input is supplied as its extracted `binary-static-v1` payload, with the original repository checker. It was replayed successfully: 181 certificate steps, threshold 17, 31 contradictions, and two target branches. The square-tail input is the merged C2 proof, with its symbolic identity script and results. Its determinant factors are −216n(n−1)²(n−2)(n−6)(n+8) and −54(n−1)²(n−2)²(n−8)(n+8); these were replayed symbolically. The C2 mathematical chain argument is retained as a theorem input, not silently replaced by finite numerical testing. Its full written derivation is included.

Base source: `towre676-cloud/nonlinearhamiltonian`, main commit `660cf921e2836191aa3233d94094a274e836baa7`. Relevant source paths are `research/hamiltonian/independent/SEXTIC_FAMILIES.md`, `SEXTIC_C2_PROOF.md`, and `extensions/hamiltonian/check_binary_static.py`. Copied inputs are identified in `INPUT_PROVENANCE.json`; new files and retained inputs are covered by `SHA256SUMS`.

The new family argument is a finite, independently replayable polynomial-identity proof combined with established all-degree static tails. The monomial argument is a direct symbolic all-degree proof. There is no remaining C3 case within these two scopes, subject to those stated static inputs and ordinary exact symbolic computation. What remains outside this result is a proof-assistant formalization and a shorter conceptual replacement for the 101-minor family certificate. The companion classification below covers the remaining geometric root strata.

## Complete root-strata classification

The [maintained root-multiplicity classification](../c3_strata/SEXTIC_STRATA_THEOREM.md) extends the research beyond this theorem's scope. Arbitrary sextic C3 is false: H=q⁴p²+q⁶ and G=qp satisfy both static gates through DG, but T₃(H,D²G)=−82944q¹⁰. The repeated-root strata satisfy C3 except (4,1,1), where S²=D∞=span{1,H} and S¹ has dimension three. These conclusions combine written all-degree degeneration arguments, symbolic quadratic identities, a uniform triple-root certificate, and the stated inherited monomial and static-tail inputs. They do not weaken or replace the restricted-family and monomial results above. The [squarefree theorem](../c3_strata/SQUAREFREE_THEOREM.md) now covers every squarefree binary sextic over every characteristic-zero field. It combines exact discriminant identities in degrees 1–16 with the inherited static tail from degree 17. Together the results establish (4,1,1) as the sole geometric root stratum where C3 fails.
