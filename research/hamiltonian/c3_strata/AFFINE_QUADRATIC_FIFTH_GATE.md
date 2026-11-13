# All-degree classification for affine quadratic-momentum sextics

For a sextic h and affine A,B over a characteristic-zero field, set
H=h(q)+A(q)p+B(q)p². Let S^r consist of polynomials G for which D^i G
passes both Moyal gates for 0 ≤ i ≤ r. For B'=b1≠0 the classification is:

| Space | Basis or description | Dimension |
| --- | --- | --- |
| S⁰ | Static coefficient equations below | Infinite |
| S¹ | 1, q, p, qp, H, E | 6 |
| S² | 1, q, H | 3 |
| S³ and the persistent core | 1, H | 2 |

The extra partner E is given explicitly below. For constant B, the static
space is K[q]⊕pK[q]⊕p²K[q].

## Proof

Work over a characteristic-zero field. Let h have degree six, with leading
coefficient c6, and A and B be affine. Use D={H,-}, with {q,p}=1.
For odd order n the unscaled operator is the sum over k from 0 to n of
(-1)^k binomial(n,k) times H_(q^(n-k),p^k) G_(q^k,p^(n-k)).
The third order terms come from k=0 and k=2, giving
T3=h''' ∂p³+6 b1 ∂q²∂p. At order five only k=0 survives,
giving T5=h''''' ∂p⁵. All higher odd orders vanish.

T5 forces momentum degree at most four. Write G=sum g_j(q)p^j.
For b1 nonzero, the coefficients of p³, p², p and 1 in T3 yield,
respectively, g4''=0, g3''=0, g2''=-2h'''g4/b1,
and g1''=-h'''g3/b1. There is no condition on g0. For b1=0,
T3 forces momentum degree at most two and the coefficients are arbitrary.
An infinite-dimensional static space follows from arbitrary g0 in both cases.

Translate q so the zero of B is at the origin, writing x=q+b0/b1.
Below, h and A are expressed in x and B=b1*x.
For G in S1, the p⁵ term of DG is (4b1-2B∂x)g4, which
must vanish. On affine g4 this operator has eigenvalues 4b1, 2b1.
After eliminating g4, the p⁴ coefficient of DG is (3b1-2B∂x)g3.
It is affine by the static equations.

To exclude g3, write g3=u+vx. The p² static equation on DG
requires its p³ coefficient to be affine. This coefficient is
(2b1-2B∂x)g2+(3A'-A∂x)g3. At this stage g2 is affine
since g4=0, so the condition is automatic. The p coefficient equation
on DG now reads (DG)_2''=-2h'''(DG)_4/b1, with
(DG)_2=(b1-2B∂x)g1+(2A'-A∂x)g2+3h'g3.
Using g1''=-h'''g3/b1 and differentiating gives
(DG)_2''+2h'''(DG)_4/b1
= 12 h'''g3+2x(h'''g3)' + 6 h''v - 4x h'''v.
Its x⁴ coefficient is 2100 c6 v, forcing v=0.
The remaining x³ coefficient is 2160 c6 u, forcing u=0. 

Now subtract a multiple of H so that g2=μ is constant. Then
G=f(x)+(d+a*x)p+μp². The p³ coefficient of DG is 2μb1,
the p² coefficient is affine, and the p coefficient has second
derivative (2μh'-2B f')''. Consequently the sole remaining
equation is (Bf')''=2μh'''. In centered coordinates this integrates
to Bf'=2μ(h'-h'(0))+C*x. Define
E=b1*p²+2 ∫ (h'(x)-h'(0))/x dx with zero integration constant.
Then S1 is spanned by 1,x,p,xp,H,E and has dimension six.

For S2, the coefficient of p*x³ in T3(D²E) is 51840 b1³ c6.
The T3(D²G) for each of the other five S1 basis vectors is independent
of p. The p*x³ coefficient therefore eliminates E. The x⁴ coefficient
then eliminates xp by its pivot -15120 b1² c6, and the x³ coefficient
eliminates p by its pivot -4320 b1² c6. The surviving 1, x, H pass
both gates through two iterates. For S3, the x⁴ coefficient of T3(D³x)
is 30240 b1³ c6, eliminating x. The remaining 1 and H have zero
Poisson derivative and pass every iterate. Translation preserves the
spaces spanned by the original q, p, qp basis and the indicated H.

The counterexample H=q⁶+qp², G=p²+(12/5)q⁵ is minimal in observable
total degree. Any omitted partner has a nonzero E component. Its degree-six
H component must vanish below degree six, and then the degree-five
term of E cannot cancel against the remaining basis. This minimality
holds for the full nonconstant-B family.

## Replay

Run `python research/hamiltonian/c3_strata/verify_affine_quadratic_refinement.py`
with SymPy 1.14. It checks the symbolic elimination pivots, exact
counterexample and the higher-refinement obstructions. The all-degree
conclusion uses the polynomial coefficient argument above.
