# Residual-force emittance transport

This component implements an established least-squares force separation and its
exact finite-kick consequences. It is not a novelty claim for rms force
projection. Sacherer's 1971 rms-envelope treatment explicitly uses a
least-squares linear force component; our deliverable is executable exact
arithmetic, a conditional predictor interface and source-bound physical replay.
Primary source: [RMS Envelope Equations with Space Charge](https://proceedings.jacow.org/p71/PDF/PAC1971_1105.PDF), pp. 1105–1107.

## One-plane identity and sharp radius

All variables below are centered with respect to one nonnegative probability
measure that is unchanged by the kick. Suppose second moments are finite and
positions stay fixed under \(p^+=p+hF\). Write

\[
a=E[x^2]>0,\quad b=E[xp],\quad
u=p-(b/a)x,\quad g=F-(E[xF]/a)x.
\]

Then \(E[xu]=E[xg]=0\), and

\[
\varepsilon^2=aE[u^2],\qquad
(\varepsilon^+)^2=\varepsilon^2+2haE[ug]+h^2aE[g^2].
\]

Indeed the post-kick momentum residual is \(u+hg\). The reverse triangle
inequality in \(L^2\) therefore proves

\[
|\varepsilon^+-\varepsilon|\le |h|\sqrt{aE[g^2]},\qquad
|E[ug]|^2\le E[u^2]E[g^2].
\]

The constant one is sharp even for a force depending only on position: take the
equal-weight cloud \(x\in\{-1,0,1\}\), \(p=x^2\), \(F=2x^2\), and
\(h=1/2\), centering internally. A position-affine force has \(g=0\) and
preserves this projected emittance exactly. The signed term can reduce
emittance; replacing it by a positive growth term loses information. If
\(a=0\), both projected emittances are zero for this fixed-position kick; the
implemented regression chart rejects that degenerate case rather than dividing
by zero.

These identities do not assume a continuum density or independently moving
particles. They apply to a common weighted empirical measure too. Loss,
resampling, changed weights or mispaired particles require separate treatment.
For a physical beam the momentum and longitudinal variable must match the
stated paraxial canonical convention; arbitrary slopes are not interchangeable.

## A conditional predictor that cancels before bounding

Because
\(aE[g^2]=a\operatorname{Var}(F)-\operatorname{Cov}(x,F)^2\), valid bounds
\(a\le A\), \(\operatorname{Var}(F)\le L\), and
\(\operatorname{Cov}(x,F)\in[m_-,m_+]\) yield

\[
h^2aE[g^2]\le h^2(AL-m_*^2),\quad
m_* = \min_{m\in[m_-,m_+]}|m|.
\]

`predictor.residual_radius_squared` computes this rational expression and rejects
inconsistent negative upper bounds. An interval containing zero gives no
correlation cancellation. Force means must first be removed; uncentered tensor
entries cannot simply be substituted for centered covariance when centroids
are nonzero.

For successive fixed-position kicks separated by uncoupled determinant-one
linear maps, sum the individual radius upper bounds. `predictor.propagate`
returns an outward rational interval for the exit projected emittance. Every
kick needs a separate explicit force-bound premise; the routine never invents
its coverage. Coupled maps, loss and resampling are rejected. This is a genuine
compositional algebraic predictor, but its physical usefulness still depends on
inexpensively producing valid evolving moment bounds.

The ideal round continuum specialization gives a direct interface to the
existing radial certificates. Set \(t=r^2/R^2\), \(\mu=E[t]\),
\(M(t)=\Pr(T\le t)\), and
\(F=\kappa q M(t)/r^2\). Using the round virial
\(E[xF_x]=\kappa/4\), per plane

\[
aE[g_x^2]=\frac{\kappa^2}{4}
\left(\mu E[M(t)^2/t]-\frac14\right).
\]

`round_profile_radius_squared` uses a valid upper bound for the force factor.
It vanishes on a uniform disk. This is the existing round shape defect written
as a local emittance radius, not a new general round-beam classification.
Roundness, the continuum field, tails/support and its discrepancy from PIC must
still be justified; quadrupole evolution does not automatically preserve them.

## Two-plane Schur complement

For centered \(q,p,F\in\mathbb R^2\), use
\(A=E[qq^T]>0\), \(S=E[qp^T]\), \(P=E[pp^T]\),
\(M=E[qF^T]\), \(N=E[pF^T]\), \(L=E[FF^T]\).
Define

\[
U=P-S^TA^{-1}S,\quad G=L-M^TA^{-1}M,\quad
C=N-S^TA^{-1}M.
\]

These are the covariances of the momentum and force residuals after projecting
onto both positions. They satisfy

\[
\begin{pmatrix}U&C\\C^T&G\end{pmatrix}\succeq0,\qquad
U^+=U+h(C+C^T)+h^2G,\qquad
\det\Sigma=\det A\det U.
\]

The exact checker verifies all principal minors of the joint Gram matrix; just
checking diagonal entries or leading minors is insufficient for semidefiniteness.
For any fixed vector \(v\), reverse-triangle reasoning also bounds the change
in \(\sqrt{v^TUv}\) by \(|h|\sqrt{v^TGv}\). No general determinant error
radius is asserted from this directional statement.

For any linear force \(F=Kq\), \(G=C=0\) and the full covariance determinant
is preserved by the unit-determinant block shear. The map is canonical only
when \(K\) is symmetric. Crucially this does **not** preserve each projected
emittance when planes couple. For independent unit-variance Rademacher
\(x,p_x,y,p_y\), the canonical kick \(F=(y,x)\), \(h=1\), keeps the full
determinant at one while each projected squared emittance changes from one to
two. Projected objectives must use the own-plane scalar residual, which retains
this coupling. Singular \(A\) is rejected; no unstated pseudoinverse theorem is
used.

## Physical replay and remaining obstruction

The compact `physical_inputs.json` records 63 completed reference runs, their
last measured kick, exit covariance and original source hashes. The replay
inverts the final known external slice and recovers pre-kick centered moments
using the stored force tensors. No new PIC solves or large NPZs are required.
It checks 126 plane kicks; the largest relative scalar identity residual is
below \(5.7\times10^{-15}\), and the Schur update residual is below
\(8.6\times10^{-15}\) on the recorded host.

For the production settings, replacing the full force radius by the residual
radius gives factors 5.36–5.40 (Gaussian), 2.76–3.31 (halo), 120.08–136.38 (KV),
and 6.55–12.16 (six waterbag settings). These are floating-point retrospective
radius comparisons at one sampled kick per run. They are not exact certificates,
trajectory-wide gains, predictor coverage, or speedups.

The remaining physical obstruction is inexpensive, valid control of the
**evolving** residual-force variance and its signed momentum correlation,
including numerical and continuum-to-PIC discrepancies. First and second
moments alone do not supply those bounds. The code exposes the required
premises and makes cancellation explicit; it does not hide this missing step.
