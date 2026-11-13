# Binomial Newton strata: finite-tail and refinement classification

**Scope.** Let \(K\) be a characteristic-zero field and \(S^0(H)=\ker T_3(H,-)\cap\ker T_5(H,-)\). These statements concern the **weighted-homogeneous leading forms**, not arbitrary perturbations. The finite-tail arguments are human proofs awaiting independent mathematical review; the finite calculations are exact, not Lean formalizations.

## Proposed Theorems 8–9

For \(H_4=q^6+zqp^4\), \(z\ne0\), with weights \((4,5)\), every polynomial static partner has weighted degree at most **87**. The exact graded kernel calculation gives \(\dim S^0(H_4)=10\), with occupied weights \(0,4,5,8,9,10,14,20,24,44\), each of multiplicity one.

For \(H_3=q^6+bq^2p^3\), \(b\ne0\), with weights \((3,4)\), every polynomial static partner has weighted degree at most **53**. The exact graded kernel calculation gives \(\dim S^0(H_3)=10\), with occupied weights \(0,3,4,6,7,8,12,16,18,28\), each of multiplicity one.

In each case the computed first and second refinements are exactly \(\operatorname{span}\{1,H\}\), and hence so is the persistent core. This is checked by computing the static kernel in each occupied weight and applying \(D_H=T_1(H,-)\), followed by both gates at depths 1 and 2. No additional static weight survives the first refinement. Parameter normalization by invertible diagonal changes over an algebraic closure gives the same dimensions for every nonzero coefficient; rank is preserved under scalar extension.

## Finite-tail proof outline

Write \(H=q^6+\lambda q^up^v\) with \((u,v)=(1,4)\) or \((2,3)\), and \(d=6-u\). Each weighted chain has exponents \((a_t,j_t)=(a_0-dt,j_0+vt)\), with \(0\le j_0<v\). The \(q^6\) term in the third gate has coefficient \(120(j_t)_3\), so a vanished coefficient propagates to every later position. The first nonzero coefficient must therefore initiate a gapless chain.

Compatibility of the third and fifth gates on interior links gives the respective resonance polynomials

\[
P_4(a,j)=5a^2+6aj-19a-9j^2-21j+18,
\]
\[
P_3(a,j)=7a^2+18aj-21a-9j^2-9j+14.
\]

Their successive-link differences are

\[
P_4(a,j)-P_4(a-5,j+4)=2(13a+51j+64)>0,
\]
\[
P_3(a,j)-P_3(a-4,j+3)=2(a+63j+64)>0
\]

for nonnegative exponents. Thus two consecutive interior links cannot both be resonant. For the first family, a starting exponent \(a_0\ge19\) forces four nonzero links; for the second, \(a_0\ge16\) does the same. This contradicts consecutive-resonance exclusion and gives the conservative bounds \(4(18)+5(3)=87\) and \(3(15)+4(2)=53\).

The final dimensions and refinement claims are **finite exact calculations** below these bounds. The proof's endpoint-forcing case analysis remains a human argument and should be separately reviewed before describing the result as fully certified.

## Scope and limitations

These results close the two binomial leading-form experiments, assuming the finite-tail argument passes review. They do not classify arbitrary lower-weight perturbations, establish sharp tail bounds, or constitute Lean proofs. Do not infer full 21-parameter completeness from these leading-form calculations alone.
