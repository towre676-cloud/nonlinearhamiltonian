# Quadratic and cubic momentum coefficients: all-degree refinement theorem

Let K be a field of characteristic zero, let h in K[q] have degree six,
let A=a0+a1 q, and let B in K[q] have degree d=2 or d=3. Set

    H=h(q)+A(q)p+B(q)p^2,
    T_n(H,G)=sum_{i=0}^n (-1)^i binomial(n,i)
                (partial_q^{n-i} partial_p^i H)
                (partial_q^i partial_p^{n-i} G),
    D=T_1(H,-), S^0=ker T_3 intersect ker T_5,
    S^r={G : D^i G in S^0 for 0<=i<=r},
    D_infinity=intersection_{r>=0} S^r.

There are no higher nonzero odd gates because H has total degree six.
All spaces below concern arbitrary polynomial observables, without a degree
cutoff. The complete first-refinement, second-refinement and persistent-core
classifications below are also formalized in Lean 4.19.0 / Mathlib v4.19.0.
The formal proofs use the existing `SexticC3.Differential` operators on
Mathlib's bivariate polynomial ring; no classification or cutoff is assumed.
The result has not undergone independent peer review.

## Theorem

For d=2, write B=b2 q^2+b1 q+b0 with b2 nonzero and x=q+b1/(2b2).

    S^1=span_K{1,H,xp},     S^2=D_infinity=span_K{1,H}.

For d=3, write B=b3 q^3+b2 q^2+b1 q+b0 with b3 nonzero and

    Delta=b2^2-3 b3 b1.

If Delta is nonzero,

    S^1=D_infinity=span_K{1,H}.

If Delta=0, set x=q+b2/(3b3). Then

    S^1=span_K{1,H,xp},     S^2=D_infinity=span_K{1,H}.

Thus Delta=0 is an exceptional algebraic hypersurface for the first refinement
in this family. It does not enlarge the persistent core. The ordinary cubic
discriminant of B is not the relevant condition: 4 Delta is the discriminant
of B'. In particular B=q^3+1 is exceptional despite having distinct roots,
whereas B=q^3+q is not exceptional.

The static space is infinite-dimensional in every case, since it contains K[q].
For cubic B there is the stronger complete description

    S^0={f(q)+p(lambda A+aq+e)+p^2(lambda B+mu):
         f in K[q], lambda,a,e,mu in K}.

## 1. Exact operators and the true fifth-gate threshold

For arbitrary polynomial h,A,B, direct expansion gives

    T_3(H,G)=(h'''+A'''p+B'''p^2)G_ppp
             -3(A''+2B''p)G_qpp+6B'G_qqp,
    T_5(H,G)=(h^(5)+A^(5)p+B^(5)p^2)G_ppppp
             -5(A^(4)+2B^(4)p)G_qpppp+20B'''G_qqppp.

Here A is affine and B has degree at most three, so

    T_3(H,G)=(h'''+B'''p^2)G_ppp-6B''pG_qpp+6B'G_qqp,
    T_5(H,G)=h^(5)G_ppppp+20B'''G_qqppp.

Quadratic B changes the third gate but leaves the fifth gate equal to
h^(5) partial_p^5. The extra fifth-gate term starts at cubic B.

## 2. Cubic B: a resonance excludes every p-degree above two

Write G=sum_j g_j(q)p^j and suppose its p-degree is N>=3. The coefficient
of p^(N-3) in T_5 is 20 B''' N(N-1)(N-2)g_N'', since g_(N+2)=0.
Consequently g_N=uq+v. The coefficient of p^(N-1) in T_3, divided by N,
is

    (N-1)(N-2)B'''g_N-6(N-1)B''g_N'+6B'g_N''.

It forces

    (N-8)u=0,     (N-2)b3 v-2b2 u=0.

The only possible nonzero case is N=8, with g_8=u(q+b2/(3b3)), u nonzero.
Let h6 be the leading coefficient of h. The coefficient of p^3 in T_5 is

    6720 h^(5) g_8+14400 b3 g_6''=0.

It forces the leading term of g_6 to be -28 h6 u q^4/b3.
The coefficient of q^4 p^5 in T_3 is then

    40320 h6 u-2304 b3(-28 h6 u/b3)=104832 h6 u,

which cannot vanish. Thus deg_p G<=2. This argument does not truncate q
or p; it excludes every putative top p-degree.

For G=f+gp+kp^2 the exact static equations are

    B'k''-B''k'=0,     B'g''-A''k'=0.

The first says (k'/B')'=0 in K(q), hence k=lambda B+mu. The second gives
g=lambda A+aq+e. This proves the asserted complete cubic static space.

## 3. Quadratic B: high static partners cannot survive one derivative

Now B'' is a nonzero constant and T_5 forces deg_p G<=4. The third gate gives

    B'g_4''-3B''g_4'=0,     B'g_3''-2B''g_3'=0,
    B'g_2''-B''g_2'=-2h'''g_4,     B'g_1''=-h'''g_3.

Put t=B' and delta=t^2-2B''B, which is constant. The first two equations give
g_4=u4+v4 t^4 and g_3=u3+v3 t^3.

For G in S^1, the p^5 coefficient of DG must vanish:

    4B'g_4-2Bg_4'=0.

Equivalently (g_4/B^2)'=0, so g_4=C B^2. Substitution into its static equation
gives 2C B' delta=0. If delta is nonzero, g_4=0. If delta=0, translate to
B=b x^2. Write g_4=c x^4 and h=h6 x^6+lower terms. The forced g_2 has
leading term -(5/2)(h6 c/b)x^8. Therefore the p^3 coefficient of DG has
leading term 54 h6 c x^9. But a static p^3 coefficient must be a linear
combination of 1 and x^3. Hence c=0, also on this square-B locus.

With g_4=0, g_2=lambda B+mu. The p^4 coefficient of DG is

    3B'g_3-2Bg_3'=3u3 t+3v3 delta t^2.

For DG to be static this must lie in span{1,t^4}. Thus u3=0 and v3 delta=0.
For delta nonzero, g_3=0. For delta=0, write g_3=c x^3. The forced g_1 has
leading term -(10/7)(h6 c/b)x^7. The p^2 coefficient of DG then has leading
term (246/7)h6 c x^8. Its p^4 coefficient is zero, so staticity requires its
p^2 coefficient to lie in span{1,B}, of degree at most two. Again c=0.

All terms involving affine A have lower q-degree than the leading terms
just used. This proves S^1 is contained in the p-degree-at-most-two sector
for every quadratic B, including the square-B locus.

## 4. Exact first refinement and its exceptional hypersurface

For either d=2 or d=3, the previous steps allow us to write any G in S^1 as

    G=lambda H+r(q)+L(q)p+mu p^2,    L=aq+e.

The coefficient of p^2 in T_3(H,DG) is

    24mu(2B'B'''-3(B'')^2).

For degree d>=2 the polynomial in parentheses has leading coefficient

    -d^2(d-1)(d+1)b_d^2,

so mu=0. The remaining coefficients of DG are

    [p^0]DG=h'L-Ar',
    [p^1]DG=A'L-aA-2Br',
    [p^2]DG=B'L-2aB.

The static equations for DG give

    L B''=(a+nu)B' for some nu in K,     (Br')''=0.

As deg B>=2, the latter forces r'=0. A nonzero L must have a nonzero slope;
comparison of highest degrees gives nu=(d-2)a. Thus the exact condition is

    L B''=(d-1)a B'.

For d=2, its solutions are precisely the multiples of B'. For d=3, a nonzero
solution exists exactly when B' is a constant times a square of an affine
polynomial, namely Delta=0. It is then a multiple of x=q+b2/(3b3).
Conversely these conditions make DG static, proving all stated S^1 equalities.

## 5. The extra observable always disappears at the second refinement

Whenever there is an extra direction, write B=b x^d+c, x=q-r, d in {2,3}.
Then

    D(xp)=xh'+(xA'-A)p+((d-2)b x^d-2c)p^2.

If this belonged to span{1,H,xp}, its p^2 coefficient would force the H
coefficient to be d-2 and would also force c=0. The p^0 coefficient would
then require xh'-(d-2)h to be constant. Its leading coefficient is
(8-d)h6, which is nonzero. Thus D(xp) is not in S^1. Since D1=DH=0,
S^2=span{1,H} and this space persists forever.

## 6. Correction to the existing affine boundary

The merged NONCONSTANT_QUADRATIC_STATIC_SECTOR.md correctly describes
S^0 intersect V2, but its claim that [p^3]DG=2mu B' forces mu=0 is false
for affine B: a static observable need not belong to V2.

At H=q^6+qp^2 take J=p^2+(12/5)q^5. Directly,

    DJ=2p^3-12q^5p,
    T_3(H,J)=T_5(H,J)=T_3(H,DJ)=T_5(H,DJ)=0,
    T_3(H,D^2 J)=51840 p q^3.

Thus J is in S^1 but not S^2. It also disproves the former dimension-five S^1
claim in PR #38 at head 0027d76cdedc5f3745d8f736a733d52e7d7fa879. That PR
has since been corrected: the inspected head 11ed745bcc78da6240e6ba39762c7db22a475173
includes the extra direction and gives dimension six. PR #37's reported
dimension six for this example is consistent with the replay.
The new proof above does not depend on the false affine inference.

## Verification and limits

Run `python research/hamiltonian/c3_strata/verify_nonlinear_B.py` with SymPy.
It checks the full operator formulas, general static equations, symbolic
resonance and leading-term obstructions, the exceptional-locus converse,
and the affine counterexample. Independent sparse monomial contractions
then compute exact bounded kernels for representative regular and exceptional
parameters, including shifted polynomials and nonzero affine A.

The bounded calculations are regression checks only. The all-degree argument
is Sections 2-5, not extrapolation from those matrices. Scope is affine A and
quadratic/cubic B; this does not classify nonlinear A, higher-degree B,
all sixfold-leading perturbations, or the complete 21-parameter family.

## Lean theorem map

The entry point is `formal/SexticC3/NonlinearBClassification.lean`.

| Mathematical statement | Lean theorem |
|---|---|
| Exact derivative operators | `first_gate`, `third_gate`, `fifth_gate` |
| Cubic static momentum cutoff | `cubic_static_momentum_bound` |
| Quadratic first-refinement momentum cutoff | `quadratic_first_momentum_bound` |
| Cubic exceptional hypersurface | `cubic_exceptional_locus` |
| Generic cubic first refinement | `cubic_regular_first_classification` |
| Exceptional cubic first refinement | `cubic_exceptional_first_classification` |
| Quadratic first refinement | `quadratic_centered_first_classification` |
| Complete second refinements | `cubic_second_classification`, `quadratic_second_classification` |
| Combined persistent core | `nonlinear_B_persistent_classification` |

All names are in namespace `SexticC3.NonlinearB`. The family is represented by
thirteen field coefficients; `h6≠0` enforces sextic h, while `b3≠0` or
`b3=0 ∧ b2≠0` enforces the two B degrees. The first-refinement theorems are
equalities for every `MvPolynomial Bool K`, with no observable-degree bound
in their hypotheses. The quadratic proof eliminates the high coefficients
directly, without dividing by the quadratic discriminant; square-B cases
are included.

From `formal/`, run:

```sh
lake build +SexticC3.NonlinearBClassification:olean
lake env lean AuditNonlinearB.lean
lake env lean RegressionNonlinearB.lean
```

The audit covers all 73 public theorems in the eleven new modules and rejects
axioms outside `propext`, `Classical.choice`, and `Quot.sound`. No `sorry`,
admitted theorem, added axiom, or native-decide certificate is used. Eight
focused Lean regressions cover generic and exceptional cubic cases, a shifted
quadratic square, cutoffs, and persistent-core consequences.
