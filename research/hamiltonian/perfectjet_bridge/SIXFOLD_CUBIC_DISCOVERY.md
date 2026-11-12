# Sixfold-leading cubic perturbation: exact bounded discovery

Consider the non-affine sixfold-leading Hamiltonian

\[
H_\lambda=q^6+\lambda p^3,\qquad \lambda\ne0.
\]

This lies outside the previously established affine-complementary-coordinate
classification. The new search uses PerfectJet's exact polynomial operator
tower and independently replays the same kernels with the defining
Weyl--Moyal star-exponential engine.

For the polynomial input space of total degree at most 9, direct exact
calculation at \(\lambda=1,2,-3\) yields

\[
\dim S^0=15,\qquad \dim S^1=4,\qquad \dim S^2=2.
\]

The four surviving first-refinement generators are

\[
1,\ q,\ q^2,\ H_\lambda,
\]

and the second-refinement survivors are

\[
1,\ H_\lambda.
\]

The displayed generators are an exact finite-degree computation for this
family, not an assertion about every degree or all possible parameter values.
The next research step is to prove a uniform degree-independent static-tail
bound and the all-degree second-refinement equality, rather than extrapolate
from a finite experiment.

The script and tests retain the independent-engine comparison and refuse to
promote a finite plateau into an infinite stabilization theorem.

## Additional two-parameter quadratic rank-locus discovery

For the symmetric sextic surface

\[
H_{a,b}=q^6+p^6+a q^3p^3+b(q^4p^2+q^2p^4),
\]

the quadratic correction gates vanish at depth zero because their orders
exceed the partner degree. Exact computation of the depth-one maximal minors
produces the candidate ideal

\[
I_1=(3a^2+64b-192,\ a(b+9),\ (b-3)(b+9)).
\]

Its complex solutions are precisely

\[
(a,b)=(0,3),\ (16,-9),\ (-16,-9).
\]

Exact point replay gives quadratic kernel dimensions

\[
\begin{array}{c|c}
(a,b)&(S^0_2,S^1_2,S^2_2)\\
(0,3)&(3,1,1)\\
(16,-9),(-16,-9)&(3,1,0)\\
\text{generic}&(3,0,0).
\end{array}
\]

A full maximal-minor computation at depth two gives the candidate ideal
\((a,b-3)\), meaning only the cubic-composition point survives two
refinements. The optional `quadratic_incidence.py --full-minors`
recomputes the Gröbner ideals from the defining differential operators;
the default test checks the displayed exact specializations independently
using PerfectJet.

This is a bounded **quadratic** incidence result, not a classification of
all-degree partners or of every sextic. Full-minor computations require
SymPy and may take significantly longer than the standard regression.
