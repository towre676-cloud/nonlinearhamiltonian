# Sharp all-degree classification of two binomial Newton strata

## Theorem and conventions

Let K be a field of characteristic zero. All spaces below are subspaces of
the full polynomial ring K[q,p], without an input-degree cutoff. Put

\[
T_k(F,G)=\sum_{t=0}^k(-1)^t\binom kt
  (\partial_q^{k-t}\partial_p^tF)(\partial_q^t\partial_p^{k-t}G),
\quad D_H=T_1(H,-),
\]
\[
S^r(H)=\{G:T_k(H,D_H^iG)=0\quad(k=3,5;\ 0\le i\le r)\},
\qquad D_\infty(H)=\bigcap_{r\ge0}S^r(H).
\]

**Theorem.** For z,b nonzero, let

\[
H_4=q^6+zqp^4,\quad \operatorname{wt}(q,p)=(4,5),\qquad
H_3=q^6+bq^2p^3,\quad \operatorname{wt}(q,p)=(3,4).
\]

1. Every static partner of H4 has weight at most **44**. Every static
   partner of H3 has weight at most **28**. These bounds are sharp.
2. Each static space has dimension **10**, with the bases below.
3. For each leading form, **S1 = S2 = D-infinity = span{1,H}**.
4. For **every** strictly lower-weight polynomial R, the same first and
   persistent refinement equality holds for H=H4+R or H=H3+R. The same
   sharp uniform static-support bound holds, and **7 <= dim S0(H) <= 10**.
   There is no exceptional first-refinement or core locus inside either
   open stratum z != 0 or b != 0. Static dimension is generically 7;
   dimensions 7,8,9,10 all occur. Section 6 specifies its exceptional
   loci by exact determinantal equations.

These are polynomial-algebra proofs with exact computer-algebra certificates,
not Lean-formalized theorems. The tail proof below is independent of the
historical search through weight 360 and of the earlier conservative bounds
87 and 53. No external peer review is asserted.

## 1. Gates and chains, including zero coefficients

Write (n)_r=n(n-1)...(n-r+1). Direct differentiation gives

\[
\begin{aligned}
T_3(H_4,G)&=120q^3G_{ppp}+36zp^2G_{qqp}-24zqpG_{qqq},\\
T_5(H_4,G)&=720qG_{ppppp}+120zG_{qqqqp},\\
T_3(H_3,G)&=120q^3G_{ppp}-18bp^2G_{qpp}
                         +36bqpG_{qqp}-6bq^2G_{qqq},\\
T_5(H_3,G)&=720qG_{ppppp}-120bG_{qqqpp}.
\end{aligned}
\]

Each gate is homogeneous in the assigned weights, so each homogeneous
component of a static partner is static separately. In one weight the
monomials form one chain

\[
(a_t,j_t)=(a_0-(6-u)t,j_0+vt),\qquad 0\le j_0<v,
\]

where (u,v)=(1,4) or (2,3); gcd(v,6-u)=1. Let x_t be their coefficients.
For a link from (a,j) to (a-5,j+4), the exact two rows are

\[
120(j+4)_3x_{t+1}+12z\,a(a-1)(3j-2a+4)x_t=0,\tag{4a}
\]
\[
720(j+4)_5x_{t+1}+120z(a)_4j x_t=0.\tag{4b}
\]

For a link from (a,j) to (a-4,j+3), put
Q(a,j)=(a-1)(a-2)-6(a-1)j+3j(j-1). The rows are

\[
120(j+3)_3x_{t+1}-6b\,aQ(a,j)x_t=0,\tag{3a}
\]
\[
720(j+3)_5x_{t+1}-120b(a)_3j(j-1)x_t=0.\tag{3b}
\]

At the initial endpoint the unmatched q6 third-gate term gives
(j0)_3 x0=0. Thus **j0 is 0,1,2** in a nonzero chain (in particular the
H4 chain with j0=3 vanishes). The coefficient of x(t+1) in the third
row never vanishes on a link. Therefore x0=0 kills the whole chain, and
every nonzero support is a single prefix x0,...,xm. A zero cannot be
followed by a later nonzero coefficient. An internal zero in the other
third-gate coefficient can terminate the prefix; it cannot restart it.

At the last nonzero term (a,j), BOTH outgoing edge coefficients must
vanish, whether or not the monomial chain itself has ended. Expressions
with a negative target exponent are absent; their falling-factorial
coefficients are already zero. Thus the terminal conditions are exactly

\[
a(a-1)(3j-2a+4)=0,\quad(a)_4j=0 \quad(H_4),\tag{4t}
\]
\[
aQ(a,j)=0,\quad(a)_3j(j-1)=0 \quad(H_3).\tag{3t}
\]

Solving these in nonnegative integers gives the COMPLETE terminal lists:

| Form | Terminal pairs (a,j) |
|---|---|
| H4 | (0,j),(1,j) for any j>=0; also (2,0) |
| H3 | (0,j) for any j>=0; also (1,0),(1,1),(2,0),(2,3),(8,1) |

For (4t), the fifth row forces a<=3 or j=0. Substitution in the third
row yields the list (a=3 would require j=2/3). For (3t), split a<=2
or j<=1 and use

\[
Q(1,j)=3j(j-1),\quad Q(2,j)=3j(j-3),\quad
Q(a,0)=(a-1)(a-2),\quad Q(a,1)=(a-1)(a-8).
\]

This is an all-exponent endpoint argument, not a search.

## 2. All admissible resonance patterns

On an H4 link with j>=1, a>=5 and x_t != 0, eliminate x(t+1) from
(4a,b); division is only by nonzero factors. The necessary compatibility is

\[
P_4(a,j)=5(a-2)(a-3)-3(j+1)(3j-2a+4)
       =5a^2+6aj-19a-9j^2-21j+18=0.
\]

The fifth row is identically zero on the first link when j=0, so no
P4 condition may be imposed there. Similarly an H3 link with j>=2,
a>=4 and x_t != 0 requires

\[
P_3(a,j)=10(a-1)(a-2)-3Q(a,j)
       =7a^2+18aj-21a-9j^2-9j+14=0.
\]

For j=0 or 1 the fifth row is identically zero. Crucially,

\[
P_4(a,j)-P_4(a-5,j+4)=2(13a+51j+64)>0,
\]
\[
P_3(a,j)-P_3(a-4,j+3)=2(a+63j+64)>0
\]

for nonnegative integer a,j. The positivity is an integer statement;
characteristic zero embeds those nonzero integers in K. Hence two
successive constrained links cannot both be resonant.

The possible numbers m of nonzero links are now globally bounded:

| Form | Initial j0 | Maximum m |
|---|---:|---:|
| H4 | 0 | 2 |
| H4 | 1 or 2 | 1 |
| H3 | 0 or 1 | 2 |
| H3 | 2 | 1 |

Combine these bounds with the terminal lists. For H4 a one-link prefix
ends at a=0 or 1, hence starts at a0=5 or 6. At j0=0 both survive.
At j0=1 the P4 values for a0=5,6 are 48,90; at j0=2 they are
30,78, so none survives. A two-link prefix must have j0=0 and a0=10
or 11; its second-link P4 values are -60 and 0 respectively. Thus
only (a0,j0,m)=(11,0,2) survives.

For H3 a one-link prefix has the following possible starts:
(4,0),(6,0),(4,1),(4,2). The first three have no fifth-row constraint
and survive. The last has P3(4,2)=132 and fails. A two-link prefix
must start at (8,0) or (8,1); the second-link values P3(4,3) and
P3(4,4) both equal 150 and both fail.

Zero-link prefixes are precisely terminal pairs with j0<=2. Thus all
surviving patterns, including monomial and degenerate initial-link cases, are

| Form | Zero links: (a0,j0) | One link: (a0,j0) | Two links: (a0,j0) |
|---|---|---|---|
| H4 | (0,0),(1,0),(2,0),(0,1),(1,1),(0,2),(1,2) | (5,0),(6,0) | (11,0) |
| H3 | (0,0),(1,0),(2,0),(0,1),(1,1),(8,1),(0,2) | (4,0),(6,0),(4,1) | none |

Every pattern has at most one scalar degree of freedom because (4a) or
(3a) recursively determines every next coefficient. This enumerates all
resonance patterns compatible with a polynomial static partner. Isolated
integer solutions of P4=0 or P3=0 with inadmissible endpoints are not
claimed to have been separately parametrized, and are not needed.

## 3. Exact bases and sharp support

Solving those ten prefixes gives the following bases. Every displayed
coefficient is an identity for the symbolic nonzero parameter.

\[
\begin{split}
S^0(H_4)=\operatorname{span}_K\{&1,q,p,q^2,qp,p^2,qp^2,\quad
q^5+\tfrac z2p^4,\quad H_4,\\
&q^{11}+\tfrac{33z}{4}q^6p^4-\tfrac{33z^2}{112}qp^8\}.
\end{split}
\]

The occupied weights, each of multiplicity one, are
0,4,5,8,9,10,14,20,24,44. In particular the last polynomial attains
the bound 44.

\[
S^0(H_3)=\operatorname{span}_K\{1,q,p,q^2,qp,p^2,\quad
q^4+\tfrac b5p^3,\quad q^4p-\tfrac b{10}p^4,\quad H_3,\quad q^8p\}.
\]

The occupied weights, each of multiplicity one, are
0,3,4,6,7,8,12,16,18,28. The monomial q8p attains the bound 28.

Thus the global support theorem is already proved before computing any
finite matrix. The stored rational certificates cover EVERY weight 0..44
or 0..28, including zero kernels and empty monomial spaces. They provide
the matrix entries, a nonzero rank minor and an independent kernel basis.
The minor is the rank lower bound; the kernel basis gives the matching
upper bound. No interpolation of the tail is used.

## 4. First refinement: explicit symbolic rank-eight minors

Use the ordered bases in Section 3, numbered 0..9. Columns 0 and 8
(1 and H) are killed by D_H. On the eight other columns select these
rows of T3(H,D_H G):

| Column polynomial, H4 | Selected monomial | Coefficient |
|---|---|---:|
| $q$ | $q^4$ | $-2880z$ |
| $p$ | $q^3p$ | $-5760z$ |
| $q^2$ | $q^5$ | $-5760z$ |
| $qp$ | $q^4p$ | $-25920z$ |
| $p^2$ | $q^3p^2$ | $5760z$ |
| $qp^2$ | $q^4p^2$ | $-36000z$ |
| $q^5+(z/2)p^4$ | $q^8$ | $-5760z$ |
| weight-44 basis polynomial | $q^{14}$ | $110880z$ |

| Column polynomial, H3 | Selected monomial | Coefficient |
|---|---|---:|
| $q$ | $qp^2$ | $-216b^2$ |
| $p$ | $q^4$ | $-720b$ |
| $q^2$ | $q^2p^2$ | $-1728b^2$ |
| $qp$ | $q^5$ | $-5040b$ |
| $p^2$ | $q^4p$ | $15840b$ |
| $q^4+(b/5)p^3$ | $q^4p^2$ | $1080b^2$ |
| $q^4p-(b/10)p^4$ | $q^8$ | $-27072b$ |
| $q^8p$ | $q^{12}$ | $-77616b$ |

The selected 8x8 matrices are diagonal: the input weights are distinct
and the composite T3 D shifts weight by a fixed amount (12 or 8).
Their diagonal products are nonzero rational constants times $z^8$ or $b^{11}$.
Therefore rank is exactly eight over every characteristic-zero field
for every allowed parameter, with no algebraic-closure normalization
needed. S1=span{1,H}; D kills both, proving S2 and the persistent result.
The certificate stores the complete symbolic products and all eight rows.

## 5. Arbitrary lower-weight perturbations

Let N be 24 or 18 and w=wq+wp. The gate T_k(H,-) is filtered of
degree N-kw, and D_H is filtered of degree N-w. For a polynomial G
with top weighted component g, the component of nominal top weight in
T_k(H,D_H^iG) is exactly T_k(H0,D_H0^i g). This statement includes
the case that this component is zero. Hence

\[
\operatorname{gr}S^r(H)\hookrightarrow S^r(H_0).
\]

For r=0 this proves the support bound and dimension at most ten.
All polynomials of ordinary degree at most two, and H, are always static,
giving seven independent partners. For r=1 the only allowed top weights
are 0 and N. If top(G)=tH0, subtract tH; the remaining first-refinement
element has lower weight and must be constant. Therefore S1(H)=span{1,H}
and all later spaces agree. This argument proves the result for ALL
lower coefficients simultaneously, not only the tested examples.

The original 21-coefficient family has exactly these two open strata:

* c05=0, c14=z!=0: all 19 other coefficients are arbitrary lower-weight
  terms for (4,5).
* c05=c14=0, c23=b!=0: all 18 other coefficients are arbitrary lower-weight
  terms for (3,4).

These counts include the constant. In these weights every strictly lower
monomial already has ordinary degree <=5, so there is no extra hidden
restriction on R. The uniform bounds 44 and 28 remain sharp because R=0
is permitted. A given perturbation can have smaller support.

## 6. Static exceptional loci: exact determinantal description

The refined dimension never jumps, but the static dimension does. Here is
an exact finite specification of ALL static dimension loci, without a
claim of an irreducible decomposition into smaller polynomial factors.

Let M be 44 or 28. Use all n monomials q^a p^j of weight <=M as columns;
n=60 for H4 and n=43 for H3. Rows are (k,r,s), k=3,5, with r,s>=0
and wq*r+wp*s <= M+N-k(wq+wp). Write H=sum h_uv q^u p^v, with
h60=1, the edge coefficient nonzero, and the lower h_uv arbitrary. Set

\[
\mathcal M_{(k,r,s),(a,j)}
=\sum_{\substack{u+a-k=r\\v+j-k=s}}
h_{uv}\sum_{t=0}^k(-1)^t\binom kt
(u)_{k-t}(v)_t(a)_t(j)_{k-t}.
\tag{M}
\]

This is an explicitly specified matrix with polynomial entries over Q.
By the support theorem, S0(H)=ker M exactly, so

\[
\dim S^0(H)\ge d
\quad\Longleftrightarrow\quad
\text{every }(n-d+1)\text{-minor of }\mathcal M\text{ vanishes},
\quad d=8,9,10.
\]

Dimension exactly d is the corresponding closed locus minus the next
one, restricted to the nonzero edge coefficient. These equations cover
all parameters in any characteristic-zero field. Coefficients of total
degree <=2 do not occur in M and do not affect the static loci.

The following exact witnesses, with z=b=1, show that every possible
dimension is attained:

| Static dimension | R for H4 | R for H3 |
|---:|---|---|
| 7 | $q^3+q^2p$ | $q^3+p^4$ |
| 8 | $q^2p$ | $q^3$ |
| 9 | $q^3$ | $q^4$ |
| 10 | 0 | 0 |

Each has an exact matrix, kernel and nonzero rank minor in the certificate.
The dimension-seven witnesses prove the dimension >=8 locus is proper,
so the generic static dimension is seven. The dimension-ten prediction
for arbitrary lower perturbations would be false; these are exact
counterexamples to that stronger statement. No predicted support bound
or refined-dimension statement failed. `binomial_newton_sharp.classify`
returns the complete rational static basis for any admissible rational
input, together with the justified first and persistent basis.

## 7. Repository reconciliation and remaining boundaries

Base inspected: nonlinearhamiltonian
`a36cc7abd81b2b079dd72bb2b6fd94aead2f8389`.
The older generic-stratum table still labelled these rows finite
experiments. However `BINOMIAL_NEWTON_FINITE_TAIL.md` already proposed
these SAME two leading-form classifications using conservative bounds
87/53; `BINOMIAL_PERTURBATION_RIGIDITY.md` (PR #31) already gave the
conditional transfer for these SAME families. This contribution supplies
the complete endpoint analysis, sharp bounds, explicit symbolic bases and
minors, and independent replays. It is a completion and strengthening of
that existing work, not a claim that PR #31 concerned different edges.

The following audit distinguishes persistent-core coverage from a full
closed-form classification of every static space. Older 'open' paragraphs
elsewhere can be stale; the named theorem, with its own evidence limits,
is the intended dependency. Results outside the two new rows have not
been independently re-proved by this contribution.

| Next nonzero coefficient after earlier entries vanish | Weighted leading form | Current justified scope / remaining boundary |
|---|---|---|
| c05 | q6+y p5, (5,6) | Generic-stratum Theorem 6: S1=core=span{1,H}. |
| c14 | q6+z qp4, (4,5) | This theorem: sharp static bound 44, S1=core; no refined exceptions. |
| c23 | q6+b q2p3, (3,4) | This theorem: sharp static bound 28, S1=core; no refined exceptions. |
| c04 | q6+gamma q3p2+y p4, (2,3) | Weighted cubic-form Theorem 5: S2=core; S1 may jump. |
| c32, with c04=0 | q6+gamma q3p2, (2,3) | Quadratic-sixfold Lemma 5/Theorem D contains a finite S1 bound 26 and leading-model dimensions (3,2,2). Separation therefore also gives S2=core for arbitrary strictly lower-weight terms, including qp3 and p3. Infinite S0 is not a finite-tail claim. |
| c13 | q6+c qp3, (3,5) | Generic-stratum Theorem 7: S2=core; exact S1 survival test. |
| c03 | q6+alpha q4p+beta q2p2+x p3, (1,2) | Weighted cubic-form Theorems 1–3 cover the complement of 3beta=alpha2, 27x=alpha3. The separate [cube-leading boundary theorem](CUBE_LEADING_BOUNDARY_THEOREM.md) supplies weight-12 finite first refinement and stabilization by depth 14 outside its explicit infinite-core family; it classifies the core for deg B<=2, deg C<=3, with the remaining parameter strata still open. |
| All p-degree >=3 coefficients zero | h(q)+A(q)p+B(q)p2 | Quadratic-sixfold Theorems A–E give the stated quadratic cases, boxes and square-composition exception; inhomogeneous Section 10 gives the affine cases. A full static-space formula for nonconstant B is not supplied there; the later static-sector note is only an intersection theorem. |

Thus neither the old claim that the c32 core boundary is wholly open nor
an unqualified assertion of complete 21-parameter refinement classification
is appropriate. On the weighted cubic cube locus the arbitrary-degree
reduction is now proved by the separate cube-leading boundary theorem.
Its unresolved core problem is the explicit parameter stratification where
at least one of b3, c4, c5 is nonzero; a nonempty open subset and several
special parameter points are already covered. Its quadratic-B branch also
has a remaining first-refinement jump-locus question even though its core is
classified.
Closed-form static loci for the other strata, full refinement towers on
infinite-static branches, and end-to-end Lean formalization remain separate
tasks. Nothing here assumes nonlinear coordinate changes preserve the flat
Moyal product.

## 8. Reproduction and evidence

From the repository root, install SymPy 1.14.0 and the PerfectJet revision
in `BINOMIAL_NEWTON_PERFECTJET_PIN.txt`, or put that checkout's `src` on
PYTHONPATH. Then run:

```sh
python research/hamiltonian/c3_strata/verify_binomial_newton_sharp.py --perfectjet --check research/hamiltonian/c3_strata/BINOMIAL_NEWTON_SHARP_CERTIFICATE.json
python research/hamiltonian/c3_strata/verify_binomial_newton.py
```

Use `--write PATH` to regenerate the certificate instead of comparing it.
Omitting `--perfectjet` performs the sparse/SymPy checks and explicitly
records that the PerfectJet checks were not run; it cannot reproduce the
committed fully checked receipt.

The verifier checks the symbolic exponent identities; the complete finite
endpoint case list after the proved link bound; all 74 weight blocks;
symbolic bases and rank-eight minors; every finite-window gate column at
depths zero and one by direct SymPy differentiation and PerfectJet at
parameters 1,2,-3/2; PerfectJet's full Weyl-star defect on each static basis
element and its first two iterates; and eight perturbation rank/tower
certificates. Three corrupted certificates must be rejected. Outputs of
gates and evolution are NEVER projected back into the input window.

The proof of the infinite tail is the algebra in Sections 1–2. The finite
matrix certificates complete the computation after that proof; the
independent implementations test the formulas and the implementation.
Passing replays do not amount to a proof-assistant check of the prose.
