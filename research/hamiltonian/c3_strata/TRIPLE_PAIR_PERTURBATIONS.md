# Arbitrary perturbations of a triple-pair leading sextic

Let \(K\) have characteristic zero and let \(H_6=cQ^3\), where \(c\ne0\)
and \(Q\) is a squarefree homogeneous binary quadratic. Use the
contractions, Poisson derivation and refinement spaces of
[the inhomogeneous theorem](INHOMOGENEOUS_THEOREM.md), equations (2)–(6).
The statement below applies over \(K\) even when \(Q\) does not split there.

## Theorem

Test whether \(H_5=3cQ^2\ell\) for a linear form \(\ell\), allowing zero.
When this holds, set \(J=Q+\ell\). The following exhaust the stratum.

| Condition | First refinement | Second refinement and persistent core |
| --- | --- | --- |
| \(H=F(J)\), \(F\) cubic | \(K[J]\) | \(K[J]\) |
| \(H=F(J)+R\), \(F\) cubic and \(\deg R\le2\), with no cubic composition | \(\operatorname{span}_K\{1,J,H\}\) | \(\operatorname{span}_K\{1,H\}\) |
| All other inputs, including failure of the quintic division | \(\operatorname{span}_K\{1,H\}\) | \(\operatorname{span}_K\{1,H\}\) |

Equivalently, once the quintic division succeeds, subtract \(cJ^3\)
and test whether the remaining quartic and cubic terms can be removed
by subtracting a scalar multiple of \(J^2\). The quartic determines that
scalar. The remaining constant, linear and quadratic terms determine
whether the composition case applies. All assertions concern arbitrary
polynomial observable degree.

## Static constraints in split coordinates

Extend scalars to split \(Q\) and use affine covariance to normalize
the leading form to \(t^3\), where \(t=xy\). For \(x^a y^b\) write
\(P_k(a,b)\) for the coefficient of \(T_k(t^3,x^a y^b)\), whose output
exponents are \((a+3-k,b+3-k)\). Expansion gives
\[
\begin{aligned}
P_3(a,b)&=-6(a-b)(a^2-8ab-3a+b^2-3b+2),\\
P_5(a,b)&=-360ab(a-1)(a-b)(b-1).
\end{aligned}
\]
A term with a negative output exponent is zero. Hence the common
static kernel for \(t^3\) has basis \(t^d\) for \(d\ge0\), together
with monomials of exponents \((1,0),(2,0),(11,1)\) and their swaps.
Each off-diagonal monomial fails the first refinement because its
Poisson image under \(t^3\) has exponents \((a+2,b+2)\), with a
nonzero coefficient and a nonzero fifth contraction. Output exponents
are injective on the monomials for each fixed gate, so the homogeneous
first refinement is exactly \(K[t]\).

For the full inhomogeneous static space there is an exact triangular
constraint at every degree. Write \(G=\sum_i G_i\) by degree. For each
\(m\), in descending order from \(\deg G\) to zero, impose
\[
 T_k(t^3,G_m)=-\sum_{j<6} T_k(H_j,G_{m+6-j}),\qquad k=3,5,
\]
where components outside the range of \(G\) are zero. On each left
side use the two diagonal coefficient rules above. The two right
sides must give the same coefficient of each unknown whenever both
multipliers are nonzero. An output outside the image of a gate must
vanish. The remaining free entries at each step have the listed
homogeneous static exponents. These constraints are necessary and
sufficient since they give every output degree of both gates. They
describe \(S^0\) by degree and do not assert that every free entry
extends through the later constraints.

## All-degree obstruction

Call a term radial if its exponents in split coordinates agree.
If the quintic division succeeds, translate to the center of \(J\),
so \(J\) becomes \(t\) up to scale and a constant. The quintic term
then vanishes. If the division fails, keep the original coordinates.
In those coordinates \(H_5\) contains a monomial with exponents other
than \((3,2),(2,3)\), since those two monomials span \(t^2\) times
the linear forms. This divisibility test descends to \(K\) by exact
polynomial division.

For a non-composition input let \(s\) be the highest nonradial degree
in these coordinates. Choose a nonzero coefficient \(h_{uv}\) of
\(x^u y^v\) in \(H_s\) with \(u\ne v\), avoiding \((3,2),(2,3)\).
Such a choice exists by the quintic test and centering. Let a
nonconstant \(G\in S^1(H)\) have top part \(t^d\), scaled to be
monic. This follows from the leading-component identity and the
homogeneous first space above.

Set \(m=2d+s-6\). For each observable degree \(j>m\) every homogeneous
component \(G_j\) is radial. Indeed, above the first degree at which
a nonradial term of \(H\) can contribute, the higher \(G\) components
already known to be radial pair with radial components of \(H\).
Their odd contractions and Poisson brackets vanish by exchange
symmetry and balance of the exponents. The two static and two first
gates at the corresponding degrees are therefore those of \(t^3\)
on \(G_j\). Descending induction proves the claim, including when
\(m<0\).

Let \(z\) denote the coefficient of \(x^{d+u-3}y^{d+v-3}\) in \(G_m\),
interpreted as zero for negative exponents. In degree \(2d+s-2\)
of \(D_HG\), the coefficient of \(x^{d+u-1}y^{d+v-1}\) is
\[
 (u-v)(d h_{uv}-3z).
\]
This is the top possible degree of the Poisson image. The first
gates therefore require this component to pass the homogeneous
static gates. For \(d\ge3\) both output exponents here are at least
two, so \(P_5\ne0\). For \(d=2\), the exponents are \((1+u,1+v)\).
If one equals one, the other is between two and six, so \(P_3\ne0\).
Otherwise \(P_5\ne0\). In every case \(d\ge2\), we obtain
\(z=d h_{uv}/3\). A missing monomial already contradicts this identity.

If the monomial exists, the corresponding static third gate is
the coefficient of \(x^{d+u-3}y^{d+v-3}\) in \(T_3(H,G)\). Substituting
the forced value of \(z\), it is \(h_{uv} C_{uv}(d)\), where
\[
 C_{uv}(d)=d(d-3)(u-v)
 \left[d\big((u-v)^2-3(u+v)+14\big)-6uv+12(u+v)-24\right].
\]
This follows by adding \(dP_3(d+u-3,d+v-3)/3\) to the third contraction
coefficient of \((x^u y^v,t^d)\). For \(u>v\) and \(u+v\le5\)
the factors \(C_{uv}(d)/(d(d-3))\) are as follows. Swapping \(u,v\)
negates them.

| \((u,v)\) | Factor |
| --- | --- |
| \((1,0)\) | \(12(d-1)\) |
| \((2,0)\) | \(24d\) |
| \((2,1)\) | \(6d\) |
| \((3,0)\) | \(6(7d+6)\) |
| \((3,1)\) | \(12(d+1)\) |
| \((3,2)\) | \(0\) |
| \((4,0)\) | \(24(3d+4)\) |
| \((4,1)\) | \(12(2d+3)\) |
| \((5,0)\) | \(60(2d+3)\) |

The selected exponent pair excludes the zero row and its swap.
Thus the only possible degree with \(d\ge2\) is \(d=3\), where
subtracting a multiple of \(H\) reduces the degree. This argument
uses a coefficient polynomial in the observable exponent, with no
degree cutoff.

## The quadratic and the persistent core

It remains to check \(d=1\). If \(s=5\), use the chosen transverse
quintic monomial. Its coefficient in \(D_HG\) cannot be canceled by
\(D_{t^3}G_1\), since the latter gives exponents \((3,2)\) or \((2,3)\).
Its degree-five output fails the homogeneous static gates, by the
static list. Hence no quadratic survives.

In the centered case \(s\le4\), \(G_1=0\) by the descending
argument above, so the only candidate is \(t\) modulo constants.
If \(s=3\) or \(4\), any nonradial monomial of degree \(s\) in
\(D_Ht\) fails the homogeneous static list. If \(s\le2\), \(t\) and
\(D_Ht\) both have degree at most two and pass the static gates.
Here \(D_Ht\) is nonzero and nonradial, so it lies outside
\(\operatorname{span}\{1,t,H\}\). Since \(S^2\) consists of the
elements of \(S^1\) whose Poisson images also belong to \(S^1\),
this removes the extra direction at the second refinement.
The constants and \(H\) are invariant. With no nonradial term
the composition theorem applies, as in Section 11 of the
inhomogeneous theorem.

In the split case with \(H=t^3+x\), the quadratic \(t\) survives the
first refinement but has \(T_5(H,D_H^2t)=12960x\). Also \(t^2\)
passes both static gates but has \(T_3(H,D_H(t^2))=216x^2y\).
This supplies explicit counterexamples to both a universal
two-dimensional first space and equality of the static and first
spaces for these perturbations.

The computations over a splitting extension yield the stated
spaces over \(K\). Each spanning vector in the finite cases is
defined over \(K\), and a polynomial over \(K\) in their extension
span belongs to their \(K\)-span by coefficient comparison in the
distinct degrees. For a composition, the same comparison applies
to the distinct degrees of the powers of \(J\).

## Replay

The classifier retains the existing composition branch. Schema 2
covers all remaining triple-pair inputs and supplies the exact
first or second obstruction for a quadratic. The regression tests
check the obstruction using the defining star expansion and
compare independently computed bounded kernels. Those comparisons
are regression evidence. The all-degree upper bound is the
coefficient argument above. No Lean formalization is claimed.
