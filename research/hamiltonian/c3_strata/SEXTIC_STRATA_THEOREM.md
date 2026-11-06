# Sextic refinement by root multiplicity: a counterexample and complete repeated-root classification

November 5, 2026. Maintained integration of the repeated-root extension, alongside the completed restricted-family theorem in `../c3_uniform/C3_THEOREM.md`. All polynomial identities and certificates use characteristic zero and the flat Weyl–Moyal conventions of the source. The statements below are mathematical proofs with computer-assisted finite rank steps, relative to the inherited static-tail and monomial theorems. They are not proof-assistant formalizations.

## Main result

**C3 is false for arbitrary homogeneous binary sextics.** An explicit rational counterexample is

\[
H=q^4p^2+q^6,\qquad G=qp.
\]

With \(D=T_1(H,\cdot)\),

\[
DG=2q^4p^2+6q^6,\qquad D^2G=-48q^9p,
\]
\[
T_3(H,G)=T_5(H,G)=T_3(H,DG)=T_5(H,DG)=0,
\qquad T_3(H,D^2G)=-82944q^{10}\ne0.
\]

Thus \(G\in S^1(H)\setminus D_\infty(H)\). Over the algebraic closure, H has root pattern (4,1,1). The two simple roots need not be rational: this counterexample itself has rational coefficients and a rational partner.

**Theorem.** For every nonzero homogeneous binary sextic with a repeated geometric root, the classification below holds. In particular C3 holds in every repeated-root stratum except (4,1,1). In that exceptional stratum \(S^2=D_\infty=\operatorname{span}\{1,H\}\), while \(S^1\) has dimension three. Here \(S^r\) imposes both gates after all iterates from zero through r.

The table gives normal forms over an algebraic closure, up to invertible linear substitution and nonzero scalar multiplication. Write C=span{1,H}.

| Root multiplicities | Normal form / representative | S¹ | D∞ | Status |
|---|---|---|---|---|
| (6) | q⁶ | K[q]+pK[q]+p²K[q] | same | inherited monomial theorem + covariance |
| (5,1) | q⁵p | K[q]+pK[q] | same | inherited monomial theorem + covariance |
| (4,2) | q⁴p² | span{1,qp,H} | same | inherited monomial theorem + covariance |
| (4,1,1) | q⁴(p²+δq²), δ≠0 | span{1,qp,H} | C | new all-degree theorem; C3 fails |
| (3,3) | q³p³ | K[qp] | same | inherited monomial theorem + covariance |
| (3,2,1) | e.g. q³p²(p−q) | C | C | new all-degree double-root argument |
| (3,1,1,1) | q³p(p−q)(p−tq), t≠0,1 | C | C | new uniform certificate + inherited tail |
| (2,2,2) | e.g. q²p²(p−q)² | C | C | new all-degree double-root argument |
| (2,2,1,1) | e.g. q²p²(p−q)(p−2q) | C | C | new all-degree double-root argument |
| (2,1,1,1,1) | e.g. q²p(p−q)(p−2q)(p−3q) | C | C | new all-degree double-root argument |
| (1,1,1,1,1,1) | general squarefree sextic | unresolved in degrees ≤16 | unresolved | inherited tail; one exact sample and generic-open reduction below |

For a field K that does not split H, interpret the normal-form table after scalar extension and descend the corresponding subspaces. All core conclusions C descend immediately. Kernel computations commute with field extensions degree by degree. No splitting assumption is needed for the rational counterexample. H=0 has the full polynomial ring as every refinement and invariant space.

## 1. Covariance and an all-degree degeneration bound

For A∈GL₂,
\[
T_k(F\circ A,G\circ A)=\det(A)^k T_k(F,G)\circ A.
\]
This follows by applying the chain rule to the alternating contraction defining each transvectant. Iterating D adds one determinant factor per iterate. Nonzero scalar multiples of H similarly multiply each gate by a nonzero scalar. Consequently every Sʳ and D∞ transforms covariantly; GL₂, rather than only determinant-one substitutions, is sufficient for the zero conditions.

Suppose H has a root of exact multiplicity m, moved to q=0. Normalize its leading term to qᵐp⁶⁻ᵐ and set
\[
H_u=u^{-m}H(uq,p)=q^mp^{6-m}+u a_1q^{m+1}p^{5-m}+\cdots.
\]
This is a polynomial family extending to u=0. For every u≠0 it is linearly equivalent to H up to a nonzero scalar. In each degree n, construct
\[
M_n(H)=\begin{bmatrix}T_3\\T_5\\T_3D_H\\T_5D_H\end{bmatrix}_{V_n}.
\]
Its entries are polynomial in H's coefficients. A nonzero minor at u=0 remains a nonzero polynomial in u, so it is nonzero for some u≠0. All nonzero fibers have the same rank. Therefore, for **every n**, independently,
\[
\dim S^1_n(H)\le\dim S^1_n(q^mp^{6-m}).
\]
This is an unbounded-degree theorem, not a finite extrapolation. In characteristic zero the field is infinite, so the nonzero minor polynomial has a nonzero parameter value off its finite zero set. For mixed-degree G, the argument applies componentwise: D raises degree by four, T₃ preserves degree and T₅ lowers it by four. For each fixed gate and iterate, distinct input degrees therefore cannot cancel. Thus the polynomial spaces are the direct sums of the homogeneous kernels. For m=2 or m=4 the inherited monomial theorem bounds the dimension by one in degrees 0,2,6 and by zero in every other degree. Constants and H already occupy degrees 0 and 6. Only degree two remains to classify.

## 2. Exact double roots: only (4,2) has a quadratic survivor

For an exact double root at q=0 write
\[
H=q^2(p^4+bqp^3+cq^2p^2+dq^3p+eq^4).
\]
Use columns p²,qp,q² for M₂. The q⁰p⁶ row of T₃D is (−1920,0,0). The q²p⁴ row, after the first coefficient vanishes, is (1440b,−5760). A nonzero quadratic survivor must therefore be proportional to
\[
G=qp+(b/4)q^2.
\]
Three further rows on this vector are
\[
-480(3b^2-8c),\quad
2880(9b^3-34bc+60d),\quad
-720(b^2c-8bd+32e).
\]
Their vanishing successively forces
\[
c=3b^2/8,\quad d=b^3/16,\quad e=b^4/256.
\]
Conversely these substitutions kill every row, and give exactly
\[
H=q^2(p+bq/4)^4.
\]
This is the (4,2) orbit. Every exact-double-root sextic outside it has S¹=C, hence D∞=C, since D annihilates 1 and H. This proves all four table rows with an exact double root other than the previously solved (4,2) row, without any static-tail input.

## 3. Exact fourfold roots: complete counterexample stratum

Write
\[
H=q^4(p^2+bqp+cq^2).
\]
Completing the square by P=p+bq/2 puts H into q⁴(P²+δq²), δ=c−b²/4. The substitution has determinant one. The degree-two matrix forces the p² coefficient to vanish and leaves precisely G=qP. In the completed-square coordinates, its rows (T₃D,q⁴p²) and (T₃D,q⁶) on columns (p²,q²) are (−5760,0) and (11520δ,−1920). Their determinant is the constant 11059200, proving the upper bound uniformly even at δ=0; a generic-rank calculation alone would not suffice. Direct identities, with p denoting the new P, are
\[
DG=2H+4\delta q^6,\quad D^2G=-48\delta q^9p,
\quad T_3(H,D^2G)=-82944\delta q^{10}.
\]
Both gates vanish on G and DG for every δ. The degeneration bound proves that there are no other degrees or independent survivors. Thus S¹=span{1,G,H} for every δ. At δ=0 this is the invariant (4,2) case. At δ≠0 it is exactly (4,1,1): the noncore quadratic dies at the second refinement, establishing S²=D∞=C. This proves failure throughout the entire exceptional geometric stratum, not just at one sampled Hamiltonian.

## 4. Triple roots with three remaining simple roots

Over the algebraic closure, send the triple root and two simple roots to q=0, p=0, and p=q. The resulting normal form is
\[
H_t=q^3p(p-q)(p-tq),\qquad t\ne0,1.
\]
The existing simple-root theorem excludes static partners in n≥17 because this pattern is neither (5,1) nor (4,1,1). It also applies at t=0,1, whose pattern is (3,2,1). Thus only n=0,…,16 require certificates, uniformly in t.

`triple_certificate.json` gives 16 nonempty blocks, one per n=1,…,16, and **24 exact maximal minors**. The entire matrix is used: no residue splitting from Hₐ is assumed. At n=6, delete the q³p³ column, a complement to H_t for every t because that coefficient is always 1. At n=0 the constant is the sole column and is identically killed.

For each complement Bₙ(t), the recorded row minors dᵢ(t) and rational polynomials uᵢ(t) satisfy
\[
\sum_i u_i(t)d_i(t)=1\quad\text{in }\mathbb Q[t].
\]
Hence every complement is injective at every characteristic-zero parameter, including algebraic and transcendental values. The tail then proves S¹=D∞=C in all degrees. `verify.py` independently rebuilds the matrices by literal symbolic differentiation, recomputes each determinant using Bareiss elimination, and checks all Bézout identities. The producer uses falling-factorial coefficient sums and domain-based determinants.

## 5. What remains: the squarefree stratum

The only unclassified geometric multiplicity stratum is (1,1,1,1,1,1). The inherited static theorem gives Eₙ=0 for n≥17 throughout it. The remaining question is finite but multivariate: for n≤16, is ker Mₙ always the core, or can some squarefree forms have an extra survivor? If an extra survivor occurs, its dynamical invariance must be tested; an extra survivor alone does not establish failure of C3.

The exact rational squarefree example
\[
H=\prod_{i=1}^{6}(q-ip)
\]
has S¹=D∞=C. `squarefree_sample.json` records a nonzero integer maximal minor for every degree complement n=1,…,16. This is a theorem for this specific Hamiltonian, using the inherited tail, and is independently replayed. It is not a uniform squarefree classification.

These same 16 minors, viewed as polynomials in seven sextic coefficients on the chart where the q⁶ coefficient is nonzero, prove the result on a nonempty Zariski-open subset of sextic coefficient space. Their product is nonzero because it is nonzero at the displayed example. Intersecting with the nonzero-discriminant locus gives an explicit finite certificate description of a nonempty open squarefree set where S¹=C. This does not exclude exceptional squarefree coefficient loci. The precise remaining obligation is to cover those loci by further minors/identities or exhibit a squarefree exceptional partner and determine its subsequent iterates. No universal claim is made there.

## Reproduction and trust boundary

Run from this directory with Python 3 and SymPy:

```
python triple.py
python squarefree_sample.py
python -m unittest discover -s . -p test_strata.py -v
python ../c3_uniform/inputs/check_binary_static.py ../c3_uniform/inputs/binary_static_d6.json
python ../c3_uniform/monomial_proof.py
```

The producer uses falling-factorial coefficients; the independent verifier uses literal differentiation and imports no producer code. `REPLAY.json` records the integration replay. `PROVENANCE.json` pins the PR #9 source, base main commit, regenerated certificate hashes and shared inherited inputs. The maintained inputs in `../c3_uniform/` are reused rather than duplicated. `test_strata.py` also checks the rational witness through the maintained standard-library star-exponential engine, and rejects a missing block or corrupted Bézout identity. The existing restricted-family theorem and its tests remain valid and separate.

The all-degree degeneration, covariance, root normal forms, monomial zero-locus exhaustion and degree-two elimination are mathematical arguments, supported by exact identities; they are not proof-assistant formalizations. The simple-root tail uses a computer-assisted elimination certificate and its written local-normal-form and top-equation argument in `extensions/hamiltonian/check_binary_static.py` (repository-root path). Its replay verifies threshold 17, 181 steps, 31 contradictions and two target branches; these are symbolic identities with an integer-degree bound, not samples of high degrees. It applies to (3,1,1,1), including boundary parameters t=0,1 of type (3,2,1), and to squarefree forms. It is not applied to (2,2,2), (4,1,1), or the monomial rows: those use degeneration and the monomial theorem. The square-tail C2 theorem for the restricted family is not a new dependency of this extension.

General squarefree exceptional loci, formal verification of the symbolic engines and mathematical reductions, and independent external review remain open. The 16 squarefree sample minors prove a specific example and a nonempty open set, never a complete squarefree classification. No new proof depends on the restricted family's 47 blocks or changes its conclusion.
