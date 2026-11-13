# All-degree refinement for sixfold Hamiltonians with a weighted cubic leading form

## Scope

Assign weights $\operatorname{wt}q=1$, $\operatorname{wt}p=2$. This note treats, over a field $K$ of characteristic zero,

$$H=q^6+\alpha q^4p+\beta q^2p^2+xp^3+R,\qquad x\ne0,\qquad R\in\operatorname{span}\{q^ip^j:\ i+2j\le5\}.$$

The leading form $H_w=q^6+\alpha q^4p+\beta q^2p^2+xp^3=x\prod_{i=1}^{3}(p-r_iq^2)$ is the general weighted-homogeneous form of weight 6 with a sixfold ordinary leading root; $R$ carries the 12 monomials of lower weight. The family has 15 parameters and is not affine: no linear symplectic map removes $\alpha$ or $\beta$. The [weighted separable theorem](WEIGHTED_SEPARABLE_THEOREM.md) is the slice $\alpha=\beta=0$, and the [complete cubic theorem](COMPLETE_CUBIC_EXCEPTIONAL_THEOREM.md) is the further slice $R=uq^3+vq^2p+wqp^2$; both are recovered below as regressions and neither covers $(\alpha,\beta)\ne(0,0)$. Conventions are those of the cubic theorem: $T_k$ is the unnormalized transvectant, $D_H=T_1(H,\cdot)$, and $S^r(H)$ is the common kernel of $T_3(H,D_H^i\,\cdot)$ and $T_5(H,D_H^i\,\cdot)$ for $0\le i\le r$ on all of $K[q,p]$.

The parameter $(\alpha,\beta,x)$ is a point of the weighted projective plane $\mathbb P(1,2,3)$: the symplectic scaling $q\mapsto q/\mu$, $p\mapsto\mu p$ sends it to $(\alpha\mu^3,\beta\mu^6,x\mu^9)$ up to an overall factor of $H$. Every locus below is weighted-homogeneous for the weights $(1,2,3)$. The cube locus is $\mathcal C=\{3\beta=\alpha^2,\ 27x=\alpha^3\}$, where $H_w=(q^2+\tfrac{\alpha}{3}p)^3$.

## Statements

**Theorem 1 (static tail; proved for every weight).** Let $x\ne0$ and $(\alpha,\beta,x)\notin\mathcal C$. Then every $G\in S^0(H)$ has weighted degree at most 12, so $S^0(H)$ is finite-dimensional with $\dim S^0(H)\le\dim S^0(H_w)\le15$. For the leading form itself, $S^0(H_w)$ has no component in odd weight $\ge 11$ nor in even weight $\ge14$, and none in weight 9 when $\alpha\ne0$. On $\mathcal C$ with $R=0$, $S^0(H_w)$ is infinite-dimensional: it has a nonzero element in every even weight $\ge10$.

**Theorem 2 (leading form; proved by exact finite certificates on top of Theorem 1).** Let $R=0$, $x\ne0$, $(\alpha,\beta,x)\notin\mathcal C$. Put

$$E_{12}=4\alpha^3-9\alpha\beta-27x,\qquad \Delta_w=\beta^2-3\alpha x,\qquad \Gamma_2=12\alpha^2x^2+4\alpha\beta^2x-\beta^4-45\beta x^2 .$$

Then $\dim S^0(H_w)=14+[\alpha=0]+[E_{12}=0]$, the extra elements having weights 9 and 12. The first refinement is $\operatorname{span}\{1,H_w\}$ except on three loci: on $\Delta_w=0$ it gains $q$; on $\Gamma_2=0$ it gains one element of weight 2; and at the two points of $\mathbb P(1,2,3)$ given by $2842\,\beta^6-53565\,\beta^3x^2-245025\,x^4=0$ with $\alpha$ determined by the certificate, it gains one element of weight 4. Off $\mathcal C$, $\Delta_w=\Gamma_2=0$ only at $\alpha=\beta=0$, where $S^1=\operatorname{span}\{1,q,q^2,H_w\}$. In every case

$$S^2(H_w)=D_\infty(H_w)=\operatorname{span}\{1,H_w\}.$$

**Theorem 3 (all lower-weight perturbations; proved from Theorems 1 and 2).** For every $R$ of weight less than 6, $x\ne0$, $(\alpha,\beta,x)\notin\mathcal C$:

$$S^2(H)=D_\infty(H)=\operatorname{span}\{1,H\},\qquad \dim S^r(H)\le\dim S^r(H_w)\ \ (r=0,1).$$

In particular $S^1(H)=\operatorname{span}\{1,H\}$ whenever $\Delta_w\Gamma_2\ne0$ and $(\alpha,\beta,x)$ is not one of the two weight-4 points. If $\Delta_w=0$, $\Gamma_2\ne0$, then $S^1(H)$ is $\operatorname{span}\{1,q,H\}$ when $T_3(H,H_p)=T_5(H,H_p)=0$ and $\operatorname{span}\{1,H\}$ otherwise.

**Theorem 4 (quadric commutant; proved).** Let $Q=cp+\varphi(q)$ with $c\ne0$ and $\deg\varphi\le2$. Then $T_k(f(Q),g(Q))=0$ for every odd $k$ and all polynomials $f,g$. Consequently $K[Q]\subset D_\infty(H)$ for every $H\in K[Q]$; on the cube locus with $R=0$ this gives $K[q^2+\tfrac{\alpha}{3}p]\subset D_\infty(H_w)$. The statement fails for cubic $\varphi$.

## Proof of Theorem 1

Because $T_k$ lowers weight by exactly $3k$, the gates of $H_w$ are graded, and the top weighted component of any $G\in S^0(H)$ lies in $S^0(H_w)$. It therefore suffices to bound the weights occurring in $S^0(H_w)$. Write a weight-$d$ polynomial as $G=\sum_{j=0}^{M}g_j\,q^{d-2j}p^j$, $M=\lfloor d/2\rfloor$, and $g_j=0$ outside that range. Direct differentiation with symbolic exponents gives

$$T_5(H_w,G)=720\,q\,\partial_p^5G-120\,\alpha\,\partial_q\partial_p^4G,$$

$$T_3(H_w,G)=(120q^3+24\alpha qp)\,G_{ppp}-(36\alpha q^2+12\beta p)\,G_{qpp}+12\beta q\,G_{qqp}-6x\,G_{qqq}.$$

The coefficient of $q^{d-2m+1}p^{m-5}$ in the fifth gate, after dividing by $120(m-1)(m-2)(m-3)(m-4)$, is the two-term row

$$6m\,g_m=\alpha\,(d-2m+2)\,g_{m-1}\qquad(5\le m\le M+1),\tag{F}$$

and the coefficient of $q^{d-3-2k}p^{k}$ in the third gate is the four-term row

$$120(k+3)(k+2)(k+1)g_{k+3}+12\alpha(k+2)(k+1)(8k-3d+12)g_{k+2}+12\beta(d-2k-2)(k+1)(d-3k-3)g_{k+1}-6x(d-2k)(d-2k-1)(d-2k-2)g_k=0.\tag{T}$$

Suppose $\alpha\ne0$. If $d$ is odd and $d\ge9$, row (F) at $m=M+1$ reads $\alpha g_M=0$, and descending through (F), whose factors $d-2m+2$ are odd, gives $g_m=0$ for all $m\ge4$. If $d$ is even, (F) expresses $g_5,\dots,g_8$ through $g_4$. Substituting three consecutive rows (F) into (T) at $k=4$ and at $k=5$ gives

$$(d-8)(d-10)\,B(4)\,g_4=0,\qquad(d-10)(d-12)\,B(5)\,g_5=0,$$

$$B(k)=\tfrac19\alpha^3(14k+16-4d)+2\alpha\beta(d-3k-3)-6x(d-2k-1).$$

For even $d\ge14$ all four numerical factors are nonzero, and $g_4\ne0$ forces $g_5\ne0$ and $B(4)=B(5)=0$. Since $B$ is affine in $k$, this is $\tfrac{14}{9}\alpha^3-6\alpha\beta+12x=0$ together with $(d+3)\,\alpha\,(\alpha^2-3\beta)=0$, that is, $(\alpha,\beta,x)\in\mathcal C$. Off $\mathcal C$ therefore $g_m=0$ for $m\ge4$ in both parities. Rows (T) at $k=3,2,1,0$ then read $x(d-2k)(d-2k-1)(d-2k-2)g_k=0$ successively, so $G=0$ when $d\ge9$.

If $\alpha=0$, (F) gives $g_m=0$ for $m\ge5$, row (T) at $k=4$ gives $x(d-8)(d-9)(d-10)g_4=0$, and the same descent gives $G=0$ for $d\ge11$.

Hence off $\mathcal C$ the static space of $H_w$ lives in weights $d\le8$ and $d\in\{9,10,12\}$. Its total dimension is read from the exact determinantal ideals of those weights: 14 generically, 15 on $\alpha=0$ and on $E_{12}=0$, which are disjoint for $x\ne0$.

On $\mathcal C$, $B\equiv0$, so for even $d\ge10$ the sequence $g_m=g_4\prod_{i=5}^{m}\alpha(d-2i+2)/(6i)$ satisfies every row (F) and every row (T) with $k\ge4$, and rows (T) for $k=3,2,1,0$ determine $g_3,\dots,g_0$ uniquely because $x\ne0$. This is a nonzero static partner in each even weight $\ge10$.

## Proof of Theorems 2 and 3

By Theorem 1, $S^r(H_w)\subset S^0(H_w)$ is supported in weights $\le12$ and is graded, so the classification is a finite list of exact rank statements, one per weight and depth, valid for all parameters at once. Rank is unchanged by extension of scalars and by the scaling above, so it suffices to work in the chart $x=1$ over $\mathbb Q[\alpha,\beta]$. For each weight $w\le12$ and each depth the certificate records maximal minors of the gate matrix whose ideal is the unit ideal, or contains the cube ideal $(3\alpha-\beta^2,\ \beta^3-27)$, or, in the four exceptional cases, is generated by the stated polynomial. Weights 1 and 2 at depth 1 are a single entry and a single $2\times2$ determinant, nonzero constant multiples of $\Delta_w$ and of $\Gamma_2$; at depth 2 every weight in $\{1,2,4\}$ has rank-drop ideal containing the cube ideal, and weights $\ge5$ already have full rank at depth 1 off $\mathcal C$, apart from $H_w$ itself in weight 6. This gives Theorem 2.

For Theorem 3, let $G\in S^r(H)$ with top weighted component $G_{\rm top}$. The top component of $D_HG$ is $D_{H_w}G_{\rm top}$ when that is nonzero, so by induction $G_{\rm top}\in S^r(H_w)$. Passing to the associated graded space is dimension-preserving, which gives $\dim S^r(H)\le\dim S^r(H_w)$. Since $1$ and $H$ always lie in $D_\infty(H)$ and $\dim S^2(H_w)=2$, the second refinement is $\operatorname{span}\{1,H\}$. On $\Delta_w=0$ a third element of $S^1(H)$ has top component $q$, hence equals $q$ modulo constants, and $q\in S^1(H)$ means exactly that $D_Hq=-H_p$ is static.

## Proof of Theorem 4

It suffices to treat $f=e^{sQ}$, $g=e^{tQ}$ as formal series in $s,t$. Put $h_m(s)=e^{-s\varphi}\partial_q^me^{s\varphi}$, so that $\sum_m h_m(s)z^m/m!=e^{s(\varphi(q+z)-\varphi(q))}$. Since $\partial_p$ acts on $e^{sQ}$ as multiplication by $sc$,

$$T_k(e^{sQ},e^{tQ})=e^{(s+t)Q}\,c^k\sum_{j=0}^{k}(-1)^j\binom kj s^jt^{k-j}\,h_{k-j}(s)\,h_j(t)=:e^{(s+t)Q}P_k,$$

$$\sum_{k\ge0}P_k\frac{u^k}{k!}=\exp\bigl(s[\varphi(q+cut)-\varphi(q)]+t[\varphi(q-cus)-\varphi(q)]\bigr)=\exp\bigl(\tfrac12\varphi''c^2u^2\,st(s+t)\bigr)$$

for quadratic $\varphi$, the terms linear in $u$ cancelling. The right side is even in $u$, so $P_k=0$ for odd $k$. For cubic $\varphi$ the exponent acquires the odd term $\tfrac16\varphi^{(3)}c^3u^3\,st(t^2-s^2)$, and indeed $T_3((p+q^3)^3,(p+q^3)^2)\ne0$.

## A separation principle used above

The step from Theorem 2 to Theorem 3 is not specific to Hamiltonians. Let an observation map $\mathcal O$ on a graded model space be the sum of a part $\mathcal O_0$ homogeneous for the grading and parts of strictly lower degree. Then the leading components of $\ker\mathcal O$ lie in $\ker\mathcal O_0$, so $\dim\ker\mathcal O\le\dim\ker\mathcal O_0$, and if $\ker\mathcal O_0$ is supported in degrees at most $D$ then so is $\ker\mathcal O$. A finite exact certificate for the leading observation family therefore separates the entire lower-order perturbation class, here 12 further parameters, with no additional computation. The same inclusion holds for iterated observations $\mathcal O\circ D^i$ when $D$ is filtered with homogeneous leading part.

## The quartic Newton edge

The same method applies to the other edge of the Newton polygon that carries an interior lattice point. Take weights $\operatorname{wt}q=2$, $\operatorname{wt}p=3$ and

$$H=q^6+\gamma q^3p^2+yp^4+R,\qquad y\ne0,\qquad \operatorname{wt}R<12,\ \deg R\le5 .$$

The leading form $H_e=q^6+\gamma q^3p^2+yp^4$ is the general weighted-homogeneous form of weight 12; the slice $\gamma=0$ is covered by the weighted separable theorem. The invariant of the scaling is $\gamma^2/y$.

**Theorem 5 (proved for every weight; finite part by exact certificates).** Let $y\ne0$. Every static partner of $H$ has weighted degree at most 20, and

$$\dim S^0(H_e)=10+2[\gamma=0]+[3\gamma^2=-80y]+[3\gamma^2=32y]+[\gamma^2=-6y]+[\gamma^2=24y],$$

the extra elements having weights $7$ and $16$, $9$, $11$, $18$, $20$ respectively. The first refinement of $H_e$ is $\operatorname{span}\{1,H_e\}$ unless $\gamma^2=-40y$, where it gains $p$. For every admissible $R$,

$$S^2(H)=D_\infty(H)=\operatorname{span}\{1,H\},\qquad\dim S^r(H)\le\dim S^r(H_e)\ (r=0,1).$$

There is no analogue of the cube locus: on $\gamma^2=4y$, where $H_e=(q^3+\tfrac{\gamma}{2}p^2)^2$, the static space is the generic one, in agreement with Theorem 4, whose hypothesis fails for $q^3+cp^2$.

*Proof.* Write a weight-$d$ polynomial as $\sum_j g_j\,q^{i}p^{j}$ with $i=(d-3j)/2$, $j\equiv d\pmod 2$. With symbolic exponents,

$$T_5(H_e,G)=720\,q\,\partial_p^5G+120\,\gamma\,\partial_q^2\partial_p^3G,\qquad T_3(H_e,G)=(120q^3+6\gamma p^2)G_{ppp}-36\gamma qp\,G_{qpp}+18\gamma q^2G_{qqp}-24yp\,G_{qqq}.$$

For $j\ge3$ the fifth gate gives the two-term row $6(j+2)(j+1)\,g_{j+2}=-\gamma\,i(i-1)\,g_j$, and for $j\ge1$ the third gate gives

$$120(j+2)(j+1)j\,g_{j+2}+\gamma j\bigl[6(j-1)(j-2)-36i(j-1)+18i(i-1)\bigr]g_j-24y(i+3)(i+2)(i+1)\,g_{j-2}=0 .$$

Let $\gamma\ne0$ and let $j_0\in\{3,4\}$ have the parity of $d$. By the two-term rows $g_{j_0}=0$ forces $g_j=0$ for all $j\ge3$, while $g_{j_0}\ne0$ forces $g_j\ne0$ up to the top index. In the second case, substituting the two-term rows at $j-2$ and $j$ into the third-gate row at $j$ gives, for every $j\ge j_0+2$ in the range,

$$N(d,j)=\gamma^2\bigl[\tfrac13i(i-1)-(j-1)(j-2)+6i(j-1)\bigr]-24y(i+1)(j-1)=0 .$$

As a polynomial in $j$, $N$ has degree at most 2 with leading coefficient $\tfrac14(144y-37\gamma^2)$ and linear coefficient $-\tfrac12(d+5)(24y-5\gamma^2)$, which vanish together only for $\gamma=y=0$. So $N$ has at most 2 roots, whereas for $d\ge33$ there are at least 3 admissible indices $j$. Hence $g_j=0$ for $j\ge3$, and the third-gate rows at $j=4,3,2$ then give $y(i+3)(i+2)(i+1)g_{j-2}=0$, so $G=0$. If $\gamma=0$ the fifth gate gives $g_j=0$ for $j\ge5$ and the same descent gives $G=0$ for $d\ge18$. The weights $d\le34$ are settled exactly in the chart $y=1$ over $\mathbb Q[\gamma]$: in each weight and depth the greatest common divisor of maximal minors is a nonzero constant, except for the seven polynomials in the statement, whose roots are confirmed as genuine rank drops at rational representatives of each value of $\gamma^2/y$. The passage to $R\ne0$ is the separation principle. $\qquad\blacksquare$

Status: the tail argument is a human proof whose row formulas and identity for $N$ are replayed symbolically; the finite part is an exact computer-algebra certificate replayed by `verify_quartic_edge.py` (9 checks); the elimination identity and the non-vanishing of the obstruction are formalized as `QuarticEdge.row_elimination` and `QuarticEdge.obstruction_coefficients`, with the same three axioms; the theorem itself is not formalized.

## Evidence classes

| Claim | Status |
| --- | --- |
| Rows (F), (T) and the identity behind $B(k)$ | Symbolic identity in $(k,d,\alpha,\beta,x)$ and in symbolic exponents, replayed by `verify_weighted_cubic_form.py` |
| A nonzero tail forces the cube locus | Formalized: `WeightedCubicForm.tail_collapse` and its three lemmas in `formal/SexticC3/WeightedCubicForm.lean`, axioms `propext`, `Quot.sound`, `Classical.choice`; receipt in `formal/AuditWeightedCubicForm.output.txt` |
| Theorem 1 as a statement about polynomials | Human proof above; the passage from the gates to rows (F), (T) is computer-checked symbolically but not formalized |
| Theorem 2 | Exact computer-algebra certificate (`WEIGHTED_CUBIC_FORM_CERTIFICATE.json`, 33 stored minors plus complete minor ideals in the small weights), replayed with Gröbner bases by an independent script; not formalized |
| Theorem 3 | Human proof from Theorems 1 and 2; spot-checked on random 15-parameter members |
| Theorem 4 | Human proof above; the vanishing is replayed symbolically for $k=1,3,5,7$ and on explicit powers, including the cubic counterexample |

The existing results serve as regressions and are not new here: at $\alpha=\beta=0$ the engine returns $\dim S^0=15$, $S^1$ of dimension 4 or 3 according to $3xv=w^2$, and $S^2$ of dimension 2.

## Reuse

`exact_observation.py` is the domain-independent part: exact rank, kernel witnesses, minimum-cost identifying panels with a matroid exchange certificate, and sup-norm error amplification. The Moyal gate matrices are one client. `period_valuation_transfer.py` is a second client with no Hamiltonian content: the prime-valuation matrix of period-fingerprint-lab's fixed-prefix ambiguity theorem. It reproduces the weight-51 terminal collision $(1,1,1,1,1,5,5,12,24)$ against $(2,2,2,2,3,3,12,25)$ as a kernel vector for 2 supported coefficients and returns the cheapest separating observation, the 2-adic valuation at the third coefficient. A third client is the $7\times7$ reader matrix of Singularity's volume-eight certificate, embedded in the tests: the engine returns determinant 224000 and worst-case gain $133/10$, the stored values, which PerfectJet's `observation_design` also returns. PerfectJet's module optimizes coefficient panels and certifies $\ell_1$ sensor optima; the engine here adds kernel witnesses, minimum-cost panels over arbitrary rational rows and the exchange certificate, and does not replace it.

## Not claimed

The boundary $x=0$, the full refinement tower on the cube locus beyond Theorem 4, Hamiltonians whose Newton polygon has more than one edge above the cubic one (for instance $q^6+q^4p+p^4$, or any term $qp^3$, $q^5p$, $p^5$ combined with the above), the boundary $y=0$ of the quartic edge, and the strata of the 21-parameter family between these edges and the generic stratum $c_{05}\ne0$, which is settled in [GENERIC_SIXFOLD_STRATUM_THEOREM.md](GENERIC_SIXFOLD_STRATUM_THEOREM.md), remain open. The two weight-4 points are defined over $\mathbb Q(\sqrt{11377})$ and were located by an exact ideal computation, not examined individually. Theorems 2 and 3 are not formalized in Lean.

## Replay

~~~sh
python verify_weighted_cubic_form.py          # 46 checks, writes WEIGHTED_CUBIC_FORM_REPLAY.json
python verify_quartic_edge.py                 # 9 checks, about 2 minutes
python -m unittest test_weighted_cubic_form   # 16 tests
cd formal && lake build SexticC3.WeightedCubicForm && lake env lean AuditWeightedCubicForm.lean
~~~
