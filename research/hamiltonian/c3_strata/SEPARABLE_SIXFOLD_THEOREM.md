# Complete refinement of separable polynomial potentials

## The theorem and its implemented scope

Let `K` be a field of characteristic zero, let `L,M` be independent linear
forms in two variables, and let

\[
 H=f(L)+g(M),\qquad n=\deg f\ge5,\qquad m=\deg g\in\{3,4\}.
\]

Arbitrary lower coefficients are allowed in both polynomials. Translating
either linear coordinate is included by translating the corresponding
univariate polynomial. Let

\[
 T_k(H,G)=\sum_{j=0}^k(-1)^j\binom kj
 (\partial_q^{k-j}\partial_p^jH)(\partial_q^j\partial_p^{k-j}G),
 \qquad D_HG=T_1(H,G).
\]

The static space `S^0` is the kernel of all odd corrections `T_k`, `k>=3`;
`S^r` imposes these conditions on `D_H^i G` for `0<=i<=r`. For sextics the
only potentially nonzero correction gates are `T_3,T_5`. The persistent
core is their intersection over all iterates.

**Theorem.** The following are exact statements in all polynomial degrees.

| Complement degree | Static dimension | First refinement | Persistent core | Least depth |
| --- | ---: | --- | --- | ---: |
| `m=3` | 15 | `span{1,L,L^2,H}` | `span{1,H}=S^2` | 2 |
| `m=4` | 12 | `span{1,H}` | `span{1,H}=S^1` | 1 |

The static bases are given explicitly below. There is no genericity
exception and no condition on the lower coefficients. This includes the
previously unsupported sixfold-leading sextics `q^6+p^3` and `q^6+p^4`,
all their separable rational perturbations, and their rational affine
changes of coordinates. The proof is polynomial differentiation and
comparison of leading coefficients. It does not use the sextic root-strata
classification or its static-tail theorem.

The implementation `separable_sixfold.classify_separable` accepts rational
inputs with `n>=5`; the sextic schema-2 integration uses the wrapper
`classify_separable_sixfold` and requires `n=6`. Its exact preimage
calculation independently cross-checks the closed formulas. No Lean
formalization or literature-priority claim is made here.

## 1. Reduction to a separable chart

In the coordinates `x=L,y=M`, use the standard alternating contraction.
For an invertible linear substitution with determinant `delta`, each
`T_k` acquires the nonzero factor `delta^k`, and its application after `i`
Poisson iterates acquires `delta^(k+i)`. Thus the zero gates and every
refinement space transport under the substitution. This is the ordinary
constant-coefficient chain rule: the alternating bivector is multiplied
by `delta`. Scalar rescaling of `H` similarly multiplies the gate at
iterate `i` by its scalar to the power `i+1`.

It therefore suffices to write

\[
 H=f(x)+g(y),\qquad
 D=f'\partial_y-g'\partial_x,\qquad
 T_3=f'''\partial_y^3-g'''\partial_x^3.
\tag{1}
\]

Since `m<=4` and `f^(5) != 0`,

\[
 T_5(H,G)=f^{(5)}G_{yyyyy}=0
 \quad\Longleftrightarrow\quad \deg_yG\le4.
\tag{2}
\]

The polynomial ring is an integral domain and has characteristic zero,
which justifies both implications. All higher odd gates then vanish:
the `g` contribution has vanished after five derivatives and the `G`
factor in the `f` contribution is differentiated at least five times in
`y`. Consequently `T_3,T_5` characterize the complete static space even
when `n>6`.

Define the linear operator `I_f` on `K[x]` by

\[
 I_f(u)'''=f'''u,\qquad I_f(u)(0)=I_f(u)'(0)=I_f(u)''(0)=0.
\tag{3}
\]

Polynomial antiderivatives exist uniquely with these initial conditions
in characteristic zero.

## 2. Cubic complement: the complete static space

Write

\[
 g(y)=a_3y^3+a_2y^2+a_1y+a_0,\qquad a_3\ne0,
 \quad G=\sum_{j=0}^4 A_j(x)y^j.
\]

Absorb `a_0` into `f`. Equating coefficients in (1) gives

\[
 A_4'''=A_3'''=A_2'''=0,\qquad
 A_1'''=\frac4{a_3}f'''A_4,\qquad
 A_0'''=\frac1{a_3}f'''A_3.
\tag{4}
\]

These equations are sufficient as well as necessary. Thus `S^0` has the
following fifteen basis elements, with `u=1,x,x^2` in each displayed group:

\[
 u,\quad uy,\quad uy^2,\quad
 uy^3+\frac{I_f(u)}{a_3},\quad
 uy^4+\frac{4yI_f(u)}{a_3}.
\tag{5}
\]

Spanning follows by integrating (4); independence follows successively
from the coefficients of `y^4,y^3,y^2,y,1`. The coefficient bounds are

\[
 \deg A_0,\deg A_1\le n+2,\qquad
 \deg A_2,\deg A_3,\deg A_4\le2.
\tag{6}
\]

For a sextic potential this places the entire static space in a
27-monomial envelope. This is a theorem-derived envelope, not a trial
search cutoff.

## 3. Cubic complement: first refinement and core

Let `G` satisfy (4), and suppose `DG` also lies in the static space. Its
`y^6` coefficient is `-3a_3 A_4'`; after that vanishes its `y^5`
coefficient is `-3a_3 A_3'`. Equation (2) therefore makes `A_4,A_3`
constant. We can write

\[
 A_1=\frac{4A_4}{a_3}f+U,\quad
 A_0=\frac{A_3}{a_3}f+V,\qquad \deg U,\deg V\le2.
\]

The `y^3` coefficient of `DG` is

\[
 -8A_4f'-3a_3U'-2a_2A_2'.
\]

It must have degree at most two by (4). Since `deg f'=n-1>=4`,
`A_4=0`, and hence `A_1=U` is quadratic at most. Let `B_j` denote the
`y^j` coefficients of `DG`, and put

\[
 C=A_2-\frac{a_2A_3}{a_3},\qquad
 W=U-\frac{a_1A_3}{a_3}.
\]

The static equation `B_1'''=4f'''B_4/a_3`, using

\[
 B_4=-3a_3 A_2',\qquad
 B_1=2Cf'-2a_2V'-a_1U',
\]

reduces to

\[
 Cf^{(4)}+9C'f'''+3C''f''=0.
\tag{7}
\]

If a nonzero polynomial `C` has degree `j` in `{0,1,2}`, the leading
coefficient on the left, divided by the nonzero leading coefficients of
`C,f` and by `n(n-1)`, is

\[
 (n-2)(n-3)+9j(n-2)+3j(j-1).
\tag{8}
\]

For `n>=5` and `j=0,1,2` this is a nonzero positive integer, and hence is
nonzero in `K`. Thus `C=0`. The remaining static equation
`B_0'''=f'''B_3/a_3` reduces to

\[
 Wf^{(4)}+6W'f'''+3W''f''=0.
\tag{9}
\]

The same leading-coefficient argument applies, replacing `9` by `6` in
(8), so `W=0`. We have proved

\[
 G=\frac{A_3}{a_3}H+V(x),\qquad \deg V\le2.
\]

Conversely, `1,H,x,x^2` and their first Poisson derivatives pass the
static gates directly, so

\[
 S^1=\operatorname{span}\{1,x,x^2,H\}.
\tag{10}
\]

For a member `cH+V(x)` of this space, `D(cH+V)=-g'V'`. If this lies
again in (10), its `y^3` coefficient forces the Hamiltonian coefficient
there to vanish, and its `y^2` coefficient then forces `V'=0`. Hence
`S^2=span{1,H}`. This space is killed by `D`, so it is the persistent core.

The depth is sharp: `x` lies in `S^1`, while

\[
 T_3(H,D^2x)=6a_3 f^{(4)}(6a_3y+2a_2)\ne0.
\tag{11}
\]

Both factors are nonzero for every allowed potential and cubic complement.

## 4. Quartic complement: the complete static space

Now write `g=a_4y^4+a_3y^3+a_2y^2+a_1y`, with `a_4 != 0`.
Equation (2) again gives `G=sum_(j=0)^4 A_j y^j`. The coefficients of
`y^5,y^4,y^3,y^2` in `T_3=0` give successively

\[
 A_4'''=A_3'''=A_2'''=A_1'''=0.
\]

The last two equations give

\[
 A_0'''=\frac1{a_4}f'''A_4,\qquad
 A_3=\frac{a_3}{a_4}A_4.
\tag{12}
\]

Therefore the twelve static basis elements are, for `u=1,x,x^2`,

\[
 u,\quad uy,\quad uy^2,\quad
 u\left(y^4+\frac{a_3}{a_4}y^3\right)+\frac{I_f(u)}{a_4}.
\tag{13}
\]

The proof of independence and spanning is the same coefficient argument
as above. The coefficient bounds are `deg A_0<=n+2` and `deg A_j<=2`
for `1<=j<=4`, a 21-monomial envelope for sextic potentials.

## 5. Quartic complement: depth one

Suppose `G,DG` both satisfy (12). The `y^7` coefficient of `DG` forces
`A_4'=0`, and then `A_3'=0`. Its `y^5` coefficient forces `A_2'=0`.
Write `A_0=A_4 f/a_4+V` with `deg V<=2`. The coefficients `B_j` of `DG`
then satisfy

\[
 B_4=-4a_4A_1',\qquad
 B_3=-4a_4V'-3a_3A_1'.
\]

The relation `B_3=a_3B_4/a_4` becomes `4a_4V'=a_3A_1'`. Next

\[
 B_1=2\left(A_2-\frac{a_2A_4}{a_4}\right)f'
       -2a_2V'-a_1A_1'
\]

must have degree at most two, so `A_2=a_2A_4/a_4`. Put
`W=A_1-a_1A_4/a_4`. The remaining equation `B_0'''=f'''B_4/a_4`
is

\[
 Wf^{(4)}+7W'f'''+3W''f''=0.
\tag{14}
\]

Its leading-coefficient test is (8) with `9` replaced by `7`, so `W=0`.
Consequently `A_1=a_1A_4/a_4`, `V'=0`, and `G=A_4H/a_4+constant`.
The converse is immediate. Thus `S^1=span{1,H}=D_infinity`.

The static space contains `x`, but

\[
 T_3(H,Dx)=-24a_4 f'''\ne0,
\tag{15}
\]

so the least depth is exactly one.

## 6. Complete recognition under rational affine transformations

For a rational input of degree `n>=5`, its leading form must be a nonzero
multiple of `L^n`. Such a rational linear form is recovered exactly from
the highest coefficients and checked by expansion. Choose any independent
linear complement `M`. If the input has degree `m=3` or `4` in `M`, its
top coefficient must be a nonzero constant `a_m`.

If the input is `f(L)+g(N)` with `N=alpha M+beta L+gamma`, `alpha!=0`,
absorb `alpha,gamma` into `g`. It can then be written using
`N=M+tL`. The coefficient of `M^(m-1)` is affine in `L`, with linear
coefficient `m a_m t`. This recovers `t` uniquely. Substitute
`M=N-tL` and require every mixed monomial to vanish. This condition is
necessary and sufficient for the claimed separation. Translations of
`L` are already absorbed into `f`. This proves that the detector covers
every rational affine-coordinate image of the stated family.

## 7. Exact certificates and independent replay

The producer constructs (5) or (13), then computes successive full
polynomial preimages

\[
 V_{r+1}=V_r\cap D^{-1}(V_r),\qquad V_0=S^0.
\]

Induction gives `V_r=S^r`. No projection of `D` is made. For an
independent basis `B`, the next space is obtained from the nullspace of
the coefficient matrix `[D B | -B]`; the first coordinates of each
relation specify its member of `V_r`. Equality of successive dimensions
in this descending chain implies equality of spaces and `D`-invariance.
The implementation checks the dimensions against the closed theorem,
checks the final core contains `1,H`, and retains a nonzero obstruction
for every strict drop.

The supplied-report verifier reconstructs the normal form independently,
builds `S^0` from the defining star exponential in the proven monomial
envelope (6) or (12), and uses a separately implemented rational
elimination algorithm for every preimage. It checks the supplied stage
spaces, depth, terminal invariance, all witness iterates, and each stored
contraction. Neither classifier output nor a reported `PASS` is accepted
as evidence without this replay.

These checks validate concrete exact instances and their certificates.
The unbounded-degree completeness comes from the proof in Sections 1--5,
whose domain is characteristic zero. The code domain is rational
coefficients. General mixed cubic or quartic complements and fifth-degree
complements are outside this theorem.
