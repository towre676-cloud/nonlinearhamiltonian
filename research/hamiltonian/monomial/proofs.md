# Monomial Hamiltonians: exact partner spaces and the boundary of infinite noncommuting families

Work over a characteristic-zero field k and use the canonical Weyl–Moyal product. A partner is always an ordinary, hbar-independent polynomial. Set E(H)={G in k[q,p]:[H,G]_star/(i hbar)={H,G}}. This is a linear space; neither ordinary multiplication nor arbitrary Poisson brackets are assumed to preserve it. Write P_2 for the polynomials of total degree at most two.

## The exponent-basis reduction

For H=q^a p^b and G=q^c p^d, define

S_k(a,b;c,d)=sum_(j=0)^k (-1)^j binom(k,j)(a)_(k-j)(b)_j(c)_j(d)_(k-j),

where (n)_r is a falling factorial, zero for r>n. The normalized Moyal bracket is the finite sum over odd k of (-1)^((k-1)/2) hbar^(k-1) S_k q^(a+c-k)p^(b+d-k)/(2^(k-1)k!). Thus G is exact if and only if every S_k for odd k>=3 vanishes. For a fixed H and a fixed correction order, distinct partner exponent pairs have distinct output exponents. Consequently no cancellation between different monomials of G is possible at that order. E(H) is exactly the linear span of the admissible exponent pairs. Distinct correction orders also have distinct hbar powers; cancellation between them is not allowed by the definition.

The Poisson coefficient is ad-bc. The distinction between exact partners and commuting partners is therefore completely visible on this basis.

## Complete effective classification for unequal exponents a,b>=2

Let D=a+b. The following algorithm is complete over all nonnegative partner exponents; it has no partner-degree cutoff. A coordinate-axis algebra is retained symbolically when a=2 or b=2. The supplied classification.py implements this algorithm using integer polynomial arithmetic and the integer-root theorem.

If D is odd, only j=b can survive in S_D, hence

S_D=(-1)^b D! (c)_b(d)_a.

Every partner therefore has c<b or d<a. If c is fixed, S_3 is a cubic in d with leading coefficient (a)_3; if a=2, its degree is two with leading coefficient -6bc, nonzero unless c=0. In that exceptional case every p^d is exact and the whole algebra k[p] is recorded symbolically. The swapped assertion applies when d is fixed and b=2. All remaining strip candidates are the nonnegative integer roots of finitely many nonzero cubic or quadratic polynomials.

If D is even, precisely j=b-1,b can survive in S_(D-1), giving

S_(D-1)=(-1)^(b-1)(D-1)!(c)_(b-1)(d)_(a-1)[b(d-a+1)-a(c-b+1)].

Thus every partner has c<b-1, d<a-1, or lies on b(d+1)=a(c+1). The strips are handled as above. On the affine line, put g=gcd(a,b), A=a/g and B=b/g. Its nonnegative integer points are exactly c=Bn-1, d=An-1 with n>=1, because A and B are coprime and unequal. S_3 on that line is a nonzero polynomial of degree at most three. One direct proof of nonvanishing is to evaluate its polynomial continuation at n=0, so c=d=-1: the result is

-6(a-b)[a^2+b^2-3(a+b)+2].

This is nonzero for unequal a,b>=2 of the same parity. Indeed the bracket is positive for the smallest such pairs (2,4) and (3,5), and increases thereafter in either exponent. Evaluating the polynomial at n=0 is only an identity test; n=0 is not an admissible partner. Therefore only finitely many additional line candidates occur. Finally, every candidate is checked against every odd correction order. The strip/line argument proves completeness, while the final checks prove sufficiency.

A nonnegative integer root of a nonzero integer polynomial is either zero or a positive divisor of its first nonzero coefficient after removing powers of the variable. This gives a terminating exact root routine. The table complete_table_2_to_12.json applies the complete procedure to every unequal pair 2<=a<b<=12. It does not truncate the partner degree.

Examples are E(q^2p^3)=k[p]+span{q,qp,q^2,q^2p^3,q^8p}, and E(q^2p^8)=k[p]+span{q,qp,q^2,q^2p^8,q^3p}. The complete algorithm gives E(q^3p^4)=P_2+span{q^3p^4,qp^14} and E(q^4p^5)=P_2+span{q^4p^5}. These are complete fixed-H classifications, justified by the finite candidate theorem. Patterns observed across a finite Hamiltonian table are not asserted as universal closed formulae.

## Closed classification for balanced monomials

For H=(qp)^m the complete answer is

E((qp)^2)=k[q]+k[p]+k[qp],

E((qp)^3)=k[qp]+P_2+span{qp^11,q^11p},

E((qp)^m)=k[qp]+P_2 for every integer m>=4.

For m<=1 the Hamiltonian has degree at most two and every polynomial is exact. The sums displayed above are vector-space sums, not assertions of directness or multiplication closure.

To prove this, put n=c+d, t=cd, and define Q_3=(m-2)(n-1)(n-2)-2(2m-1)t. Direct expansion gives S_3=m(m-1)(d-c)Q_3. The diagonal c=d makes every odd S_k vanish by pairing j with k-j. For m=2, Q_3=-6cd, so the off-diagonal solutions are precisely the two coordinate axes, proving the quartic formula.

For m=3, the only further correction is S_5=360(c)_2(d)_2(d-c). Off the diagonal, one exponent must be at most one. At c=0, S_3=6(d)_3, giving d=0,1,2. At c=1, S_3=6d(d-1)(d-11), giving d=0,1,11. Swapping c,d completes the sextic classification. In particular the degree-twelve exceptional partners are genuine; checking only low partner degrees would miss them.

For m>=4, write S_5=m(m-1)(m-2)(d-c)P_5, where

P_5=(m-3)(m-4)(n-1)(n-2)(n-3)(n-4)
-4(2m-3)[(m-3)n^2-5(m-4)n+5(2m-7)]t
+4(2m-1)(2m-3)t^2.

The following exact polynomial identity is a short elimination certificate:

(2m-1)P_5+3(n-1)(n-2)(2m+n-7)(2m^2+mn-6m-4n+12)=Q_3 R,

R=(2m-3)[mn^2-7mn-4mt+18m-4n^2+34n+2t-66].

If c!=d and S_3=0, then Q_3=0. For n>2 and m>=4, every factor of the second term is strictly positive: the last factor equals 2(m^2-3m+6)+(m-4)n. Therefore P_5 cannot vanish. This excludes every off-diagonal partner of total degree above two. Quadratic partners and diagonal partners are already known to be sufficient, completing the proof for all m. The verifier checks the displayed elimination identity by exact multivariate polynomial coefficient comparison, not numerical substitution.

## Finiteness and the criterion for large noncommuting families

For unequal a,b>=3, all candidate strip and line polynomials above are nonzero, and there is no symbolic coordinate axis. Hence E(q^a p^b) is finite-dimensional. Balanced a=b>=3 has an infinite-dimensional E(H), but its unbounded family k[qp] commutes classically and under the star commutator. Its space of noncommuting directions has dimension six for m=3 and four for m>=4, measured as E(H)/(E(H) intersect ker{H,-}).

Consequently a nonlinear monomial Hamiltonian q^a p^b of degree at least three has an infinite-dimensional space of noncommuting exact partner directions if and only if min(a,b)<=2. If a=1 or 2, use G=p^r, r>=1: these are exact because H has q-degree at most two, and their distinct nonzero Poisson images are ar q^(a-1)p^(b+r-1). If a=0, use G=qp^r; exactness follows from q-degree one of G, and the nonzero images -b p^(b+r-1) are distinct. Swap coordinates for b<=2. The preceding finite/balanced classification proves necessity for min(a,b)>=3. This criterion concerns monomial Hamiltonians and fixed canonical coordinates; it is not a classification of every nonlinear polynomial Hamiltonian.

## Ordinary powers are not automatic partners

For c=ar,d=br, exact expansion yields

S_3(a,b;ar,br)=-2ab r(a-b)(r-1)[(a+b)(r+1)-3].

For unequal a,b>=2 and integer r>=2 this is nonzero. Although {H,H^r}=0, the ordinary symbol H^r fails to commute in the Moyal sense. Star powers are hbar-dependent objects and do not supply the hbar-independent partners asked for here. More generally, when unequal a,b>=3, any exact classically commuting monomial is constant or H itself: the classical condition ad-bc=0 permits rational r, and the displayed factor leaves only r=0 or 1 for nonnegative exponents. Thus E(H) intersect ker{H,-}=span{1,H}. This is one concrete reason the exact-partner space should not be assumed to be an ordinary polynomial algebra.

## Scope

The balanced classifications and the infinite-noncommuting-family criterion are proved universal statements. The strip/affine-line procedure is a complete effective algorithm for each unequal a,b>=2. The supplied 55-Hamiltonian table is a finite application of that complete algorithm, while its independent bounded grid comparison is a regression check of the implementation. None of these claims establishes a universal closed formula for all unequal exponent pairs, a classification under nonlinear canonical transformations, or a new mathematical priority claim.
