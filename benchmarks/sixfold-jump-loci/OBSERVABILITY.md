# What a noisy trajectory can reveal about the delta jump locus

Benchmark base: this directory as published (exact catalog `reference/exact.jsonl`, theorem source
`sources/SIXFOLD_JUMP_LOCI_THEOREM.md`, row J7, weight 1). Code and outputs are in `observability/`;
`observability/run_all.sh` replays the sensitivity and design calculations in about one minute;
the estimator and diagnostic replay commands appear in sections 7 and 8. The published split,
benchmark data, and scoring are untouched.

Epistemic labels. **[proved]** means a complete argument given here or in Theorem J.
**[analytic, constants uncertified]** means the inequality is proved but its numerical constants were
evaluated in double precision from numerically integrated orbits (outward factor $1+10^{-9}$ only), without
validated enclosure of the orbit or the constants; such a number is evidence, not a certificate.
**[local]** means a first-order (linearised Gaussian) approximation whose remainder is not bounded here.
**[numerical]** means computed evidence. **[prospective]** refers to the comparison fixed in
`observability/PREREGISTRATION.md` before any test-split evaluation.

## 1. The family and its exact depth change

On branch J7 (cubic form off the cube locus) write $H=q^6+\alpha q^4p+\beta q^2p^2+xp^3+R$ with
$\operatorname{wt}R<6$ for $\operatorname{wt}q=1,\ \operatorname{wt}p=2$, and put $\Delta_w=\beta^2-3\alpha x$,
$g_2=3x\,r_{31}-2\beta\,r_{12}$. The 12 depth-two delta members $H_0$ of the benchmark satisfy
$\Delta_w=g_2=0$, $\Gamma_2\neq0$, $\alpha\beta\neq0$, $x=1$, and their partner set is $\{q\}$; the
benchmark near-misses are $H_\varepsilon=H_0+\varepsilon q^3p$. **[proved]** For every rational
$\varepsilon\neq0$, $H_\varepsilon$ stays on J7 (the perturbation has weight 5), keeps $\Delta_w=0$ and
$\Gamma_2\ne0$, and has $g_2=3x\varepsilon\ne0$; by Theorem J the weight-1 row fails, the weight-2 and
$q^2$ rows were already absent, and the weight-4 points are irrational, so the partner set is empty and the
least depth drops from 2 to 1. The obstruction is explicit and linear,
$T_3(H_\varepsilon,D_{H_\varepsilon}q)=48(3\alpha x-\beta^2)\,q+12g_2=36x\varepsilon$, $T_5=0$.
`exact_check.py` confirms the hypotheses and this formula in exact rational arithmetic for all 12 groups at
$\varepsilon\in\{0,\pm\tfrac1{10},\tfrac1{1000},\tfrac1{100000},\tfrac73,-5\}$, and the classifier returns
depth 2 exactly at $\varepsilon=0$. The natural quantity to estimate is therefore the obstruction
coefficient $c=12g_2$, which is $36\varepsilon$ along this family.

## 2. Sensitivity and a controlled expansion

Let $f_H=(H_p,-H_q)$, $x_0(t)$ the $H_0$ orbit from a known initial state, and $g=f_{q^3p}=(q^3,-3q^2p)$.
The sensitivity $z=\partial_\varepsilon x_\varepsilon|_{\varepsilon=0}$ solves
$\dot z=Df_{H_0}(x_0(t))z+g(x_0(t))$, $z(0)=0$, with $Df_H=\begin{pmatrix}H_{pq}&H_{pp}\\-H_{qq}&-H_{qp}\end{pmatrix}$.
Stacking $z(t_k)$ over the 49 sample times and 6 initial states gives $s\in\mathbb R^{588}$ and the mean
expansion $\mu_\varepsilon-\mu_0=\varepsilon s+\rho_\varepsilon$.

**Proposition 1 [proved].** Let $K$ be the box $|q|\le Q,\ |p|\le P$ containing the $H_0$ orbit with margin
$m$, and on $K$ let $L_1\ge\|Df_{H_0}\|$, $B_2\ge\|D^2f_{H_0}\|$, $M_g\ge|g|$, $L_g\ge\|Dg\|$. Put
$D(t)=M_g(e^{L_1t}-1)/L_1$. If $|\varepsilon|D(T)\le m$ then $|x_\varepsilon(t)-x_0(t)|\le|\varepsilon|D(t)$ and
$|x_\varepsilon(t)-x_0(t)-\varepsilon z(t)|\le\varepsilon^2C(t)$, with
$C(t)=\int_0^te^{L_1(t-\tau)}\bigl(\tfrac12B_2D(\tau)^2+L_gD(\tau)\bigr)d\tau$; hence
$\|\rho_\varepsilon\|\le\varepsilon^2C_{\rm tot}$, $C_{\rm tot}=(\sum_kC(t_k)^2)^{1/2}$ over all samples.
*Proof.* Grönwall on $\dot x_\varepsilon-\dot x_0=f(x_\varepsilon)-f(x_0)+\varepsilon g(x_\varepsilon)$ gives the first
bound and keeps $x_\varepsilon$ in $K$ by continuity. For $e=x_\varepsilon-x_0-\varepsilon z$ one has
$\dot e=Df(x_0)e+r+\varepsilon(g(x_\varepsilon)-g(x_0))$ with $|r|\le\tfrac12B_2|x_\varepsilon-x_0|^2$ by Taylor on
the convex box, and Grönwall again. $\square$

**Worked constants [analytic, constants uncertified].** For test group `1ae54b`, $m=0.05$, the six boxes give
$L_1\le3.18$, $B_2\le14.4$, $M_g\le0.215$, $L_g\le1.22$, $C_{\rm tot}=0.0310$, and $\|s\|=0.1540$. The orbit-box condition
$|\varepsilon|D(T)\le m$ was checked through $|\varepsilon|=0.5$ (largest value of $|\varepsilon|D(T)$ over the six boxes
$0.0261\le0.05$; it holds through 0.6 and fails by 1.0), so the bound applies on $|\varepsilon|\le0.5$, and on that
range the remainder is at most 10% of $|\varepsilon|\|s\|$ for $|\varepsilon|\le0.1\|s\|/C_{\rm tot}\approx0.4965$ (use $0.496$ as a conservative rounded threshold). The actual remainders from the benchmark's own exact near-miss
tracks are $2.41\times10^{-5},\ 2.41\times10^{-9},\ 2.40\times10^{-13}$ at $\varepsilon=10^{-1},10^{-3},10^{-5}$, about
$13\times$ below the bound, and across all 12 groups the relative linearisation error at $\varepsilon=0.1$ is at
most $2.0\times10^{-3}$ [numerical].

**Proposition 2 (vanishing signal) [proved].** With $x\ne0$, $z\equiv0$ on a time interval iff the initial
state is an equilibrium of $H_0$ on $\{q=0\}$. Indeed $z\equiv0$ forces $g(x_0(t))\equiv0$, i.e. $q\equiv0$, so
$H_p(0,p(t))=c_{01}+2c_{02}p+3xp^2\equiv0$, which forces $p$ constant. For every initial state $z(t)=t\,g(q_0,p_0)+O(t^2)$, with
$\|g(q,p)\|=|q|^2\sqrt{q^2+9p^2}$. A small $q_0\ne0$ therefore suppresses the leading coefficient by the factor
$q_0^2$ without changing the leading order in $t$; only at $q_0=0$ exactly does the $t$ term vanish. The
benchmark state $(-0.08,-0.37)$ has a suppressed coefficient of this kind. Whether some symmetry of a
particular $H_0$ can make $s$ vanish at the sample times for a non-equilibrium state is not analysed here.

## 3. Known background: the discrimination limit

**Proposition 3 [proved].** Under i.i.d. $N(0,\sigma^2)$ coordinate noise with $\mu_0$ and $\mu_\varepsilon$
known and equal priors, the optimal single-case accuracy is $\Phi(d/2\sigma)$ with $d=\|\mu_\varepsilon-\mu_0\|$
(the repository's oracle), and by Proposition 1
$\Phi\bigl((|\varepsilon|\|s\|-\varepsilon^2C_{\rm tot})/2\sigma\bigr)\le{\rm acc}\le\Phi\bigl((|\varepsilon|\|s\|+\varepsilon^2C_{\rm tot})/2\sigma\bigr)$.
Locally the Fisher information for $\varepsilon$ is $\|s\|^2/\sigma^2$. For the delta groups $\|s\|$ lies in
$[0.149,0.157]$, so at $\sigma=10^{-5},\ \varepsilon=10^{-3}$ one has $d/2\sigma\approx7.7$ and accuracy
indistinguishable from 1, consistent with the 99.92% middle-offset oracle in `IDENTIFICATION.md`.

## 4. Unknown background: the efficient signal

A real estimator does not know $H_0$; it must decide whether the data come from *some* point of the locus.
Let $J$ be the stacked trajectory Jacobian over a coefficient library and $T$ a basis of the locus tangent.
**[local]** The efficient signal per unit $\varepsilon$ is $\|s_\perp\|=\|(I-P_{JT})s\|$, the Schur complement
$I_{\rm eff}=s^\top s-s^\top JT(T^\top J^\top JT)^{-1}T^\top J^\top s$; the GLRT for the normal coordinate has
standard error $\sigma/\|s_\perp\|$, and the attainable binary accuracy is $\Phi(|\varepsilon|\|s_\perp\|/2\sigma)$.
The signal disappears exactly when $s\in\operatorname{span}(JT)$, i.e. when some tangent change of the
locus reproduces the first-order trajectory change at every sample. I computed four regimes. *Generator*
uses the benchmark's own 7-dimensional delta generator family; *J7* uses the full 12-dimensional germ of
the delta locus in the 14-monomial weighted library (constraints $\Delta_w=g_2=0$; within the study's
degree-5 library the same germ also forces the weight-$>6$ coefficients to vanish, giving the same
tangent); *J7+IC* adds the 12 initial-state coordinates as nuisance; *plug-in* is the study's route,
an unconstrained degree-5 fit (20 monomials) followed by a delta-method test of $g_2=0$ alone.

| Group (test) | known $\|s\|$ | generator | J7 | J7+IC | plug-in |
| --- | ---: | ---: | ---: | ---: | ---: |
| 1ae54b | 0.154 | 0.0859 | 0.00372 | 0.00240 | 0.000886 |
| 3e55e9 | 0.154 | 0.0804 | 0.0110 | 0.00659 | 0.00104 |
| 90e2c8 | 0.149 | 0.0800 | 0.00527 | 0.00319 | 0.000847 |

Across all 12 groups the J7 signal ranges over $[0.0037,0.0149]$ (median 0.0081), the plug-in over
$[0.00064,0.0035]$ (median 0.0014) [numerical]. Passing from the oracle to an estimator that knows only
the locus costs a factor 10–40 in signal; discarding the known constraints costs a further factor 4–10.
At $\sigma=10^{-5}$ the local Gaussian accuracy $\Phi(|\varepsilon|\|s_\perp\|/2\sigma)$, averaged over the test
groups, is 1.00 (known), 0.63 (J7), 0.58 (J7+IC) and 0.52 (plug-in) at $\varepsilon=10^{-3}$, and 1.00 in all four
regimes at $\varepsilon=10^{-1}$ [local]. These are linearised limits: they are the exact Bayes accuracies of the
Gaussian experiment obtained by replacing the locus image by its tangent plane, not finite-noise bounds for
the nonlinear composite problem, which would need explicit least-favourable nearby hypotheses and control of
the curvature of the locus image.

**Consequence for the identification study.** For this stratum, the middle-offset gap between the 99.92%
oracle and the estimators is, to first order, an information gap: the oracle uses the background, and in the
linearised experiment no test that does not know it exceeds about 63% at $\varepsilon=10^{-3}$ under the
published initial states [local]. The
large-offset selective-coverage gap is at $\varepsilon=10^{-1}$: even the plug-in route predicts essentially perfect
discrimination at $\sigma=10^{-5}$ while the guarded selective rule completed no delta pair.
Section 8 shows that its forced decisions already separated all three original large-offset pairs;
abstention on the on-locus members caused the selective loss. Why the benchmark
initial states are so poor is visible in the least-squares mimic of $s$ by the tangent: the cosine between
$s$ and $\operatorname{span}(JT)$ is 0.9997, 0.9974, 0.9994 on the three test groups, and the mimic is
dominated by the pure-potential directions $q^5,q^4,q^3,q^2$ [numerical]. One might guess that the $p$-parity of the Hamiltonian terms ($q^3p$ odd, the mimicking potential terms even)
explains this, and that orbits visiting nearby $q$ with opposite momenta separate them. That is a conjecture
only: the sensitivities are transported by the background flow, which has no $p$-reflection symmetry, so
parity of the terms does not imply parity or alignment of the trajectory sensitivities.

## 5. A design under a fixed budget [prospective]

Keeping the 49 uniform samples on $[0,0.18]$ and six initial states, I chose states by coordinate exchange
from a $0.05$ grid restricted to the benchmark's own maximal radius $0.4904$, maximizing the mean of
$\log I_{\rm eff}$ (J7, known states) over the 9 train and validation delta groups only. The selected
states are $(-0.30,0.35),(-0.30,-0.30),(0.35,-0.30),(0.10,0.40),(0.25,-0.10),(0.39,0.26)$; the first pair
has equal $q$ and opposite-sign $p$. The comparison and its success rule were then fixed in writing.

| Test group | $I_{\rm eff}$ ratio, J7 | ratio, J7+IC | ratio, known $\|s\|^2$ | plug-in signal A → B |
| --- | ---: | ---: | ---: | --- |
| 1ae54b | 199 | 123 | 1.09 | 0.000886 → 0.000674 |
| 3e55e9 | 42.9 | 31.9 | 1.13 | 0.00104 → 0.00256 |
| 90e2c8 | 169 | 111 | 1.12 | 0.000847 → 0.00197 |

The preregistered criterion (all ratios above 1, geometric mean at least 2) is met with geometric mean
113. The design does not work by amplitude: the known-background information rises only 9–13%. It works
by breaking the tangent confounding, and the plug-in route does not benefit reliably, so the design pays
only for an estimator that imposes the locus constraints. Under the design the resolvable offset at
$\sigma=10^{-5}$ for a two-sided 5% test with 95% power falls from $3.3$–$9.7\times10^{-3}$ to
$0.50$–$0.69\times10^{-3}$, and the local-model accuracy at $\varepsilon=10^{-3}$ rises from 0.63 to 0.998
[local]. Achieved performance from observed data alone is the subject of section 7. The preregistered Monte Carlo on `1ae54b` ($\sigma=10^{-5}$, 40 replicates, nonlinear
Gauss–Newton fit of the 13-parameter model started at the true locus point) gave empirical standard errors
$2.41\times10^{-3}$ (A) and $1.68\times10^{-4}$ (B) against predictions $2.69\times10^{-3}$ and
$1.90\times10^{-4}$, rejection rates 0.025 for both at $\varepsilon=0$, and 0.975 (A, predicted 0.961) and
1.0 (B) at $\varepsilon=10^{-2}$ [numerical]. Starting at the truth makes this a check of the local
calculus, not an estimator evaluation; a single seed set was used for both designs.

## 6. Exact membership is not testable; what is

**Proposition 4 [proved].** For any decision rule $\delta$ on the observations and any $\varepsilon$,
$\bigl|P_{H_0}(\delta=2)-P_{H_\varepsilon}(\delta=2)\bigr|\le\operatorname{TV}=2\Phi(d_\varepsilon/2\sigma)-1\le
2\Phi\bigl((|\varepsilon|\|s\|+\varepsilon^2C_{\rm tot})/2\sigma\bigr)-1\to0$ as $\varepsilon\to0$. Hence no rule
answers "depth 2" with probability at least $\gamma$ on the locus while keeping that answer's probability
below $\gamma-\eta$ on every depth-one alternative, for any $\eta>0$. This holds even with the background
known; with it unknown, $|\varepsilon|\|s_\perp\|$ is the first-order distance after
projecting out the locus tangent, not an exact nonlinear distance. The depth-one set is
dense at every locus point along $q^3p$, so finite noisy data cannot certify exact membership, and a
nearby rational polynomial passing a residual test certifies only itself.

**A usable replacement.** Estimate the obstruction coefficient $c=12g_2$ (here $36\varepsilon$) with standard
error $\mathrm{se}=12\cdot3x\,\sigma/\|s_\perp\|$ from the constrained fit, write $z=z_{1-\alpha/2}$, and answer in
three ways, with this priority. Answer "depth 1" when the interval $\hat c\pm z\,\mathrm{se}$ excludes 0; on the
locus this happens with probability exactly $\alpha$ in the Gaussian model. Otherwise answer "$|c|<\eta$"
when the interval lies in $(-\eta,\eta)$; when $|c|\ge\eta$ this answer requires $\hat c$ to fall more than
$z\,\mathrm{se}$ short of $c$ on the side of 0, which has probability at most $\alpha/2$. Otherwise abstain. Never
answer "exactly depth 2". In the
known-background case these error rates are exact up to the explicit $\varepsilon^2C_{\rm tot}$ shift of the
mean [proved]; with unknown background they hold to first order [local]. At $c=0$, interval containment alone has probability
$\Pr(\mathrm{CI}\subset(-\eta,\eta))=\max\{0,2\Phi(\eta/\mathrm{se}-z)-1\}$. With the priority of "depth 1" included, the
probability of the answer "$|c|<\eta$" at $c=0$ is $\Pr(|\hat c|<\min(\eta-z\,\mathrm{se},\,z\,\mathrm{se}))
=\max\{0,2\Phi(\min(\eta/\mathrm{se}-z,\,z))-1\}$, which never exceeds $1-\alpha$. For a target $1-\beta$ with $\beta\ge\alpha$
the required margin is therefore $\eta=(z_{1-\alpha/2}+z_{1-\beta/2})\,\mathrm{se}$ [proved, Gaussian model]; which is the quantitative content of "observable margin" and the
quantity a design should minimise. The margin is declared in the obstruction coordinate $c$, not as a
geometric distance in coefficient space: along this family $|c|=36|x||\varepsilon|$, and converting it to a
distance from the locus in any coefficient norm requires a declared normalisation and a local comparison
bound between $|g_2|$ and that distance, which is not supplied here.

## 7. A constrained estimator from observed data alone

**Estimator.** `observability/estimator.py` fits two nested models by nonlinear least squares on the observed
tracks, with the six initial states as nuisance parameters and the stated noise level as the likelihood scale:
the locus model (12 locus coordinates, $\alpha=\beta^2/3x$ and $r_{31}=2\beta r_{12}/3x$ imposed) and the
transverse model (one more coordinate $\varepsilon$ along $q^3p$). The profile statistic is
$\Lambda=(\mathrm{RSS}_0-\mathrm{RSS}_1)/\sigma^2$, and the obstruction estimate is $\hat c=36\hat x\hat\varepsilon$ with a
delta-method standard error. Starts are deterministic and observation-based: the study's own weak degree-5
fit projected to the locus, a weak fit in the weighted library, the same with ridge $10^{-2}$ toward a prior
averaged from benchmark *training* trajectories of training-labelled delta members, and that prior itself;
the locus model starts from the best transverse fit and from the weak fit, and the transverse model is refit
from the best locus fit, which guarantees $\Lambda\ge0$ up to tolerance. No start uses generating coefficients,
the true locus point or the true perturbation. The model integrator is a vectorised fixed-step RK4 with
exact variational equations (agreement with DOP853 to $4\times10^{-12}$); the data are simulated separately
with DOP853, so the fit does not share the generator's integrator. The comparator ("plug-in") is the study's
analytic route made nonlinear: an unconstrained degree-5 trajectory fit (20 coefficients plus initial states)
from the study's weak start, followed by a Wald test of $g_2=0$. It is a reimplementation, not the
repository's guarded weak-locus pipeline. The separate diagnostic in section 8 reruns that actual
pipeline on the fresh design-A observations.

**Freezing.** All settings, the prior, and the thresholds were fixed using only train and validation
on-locus groups (9 groups, 4 noise replicates per design and noise level), then hashed in
`observability/PREREGISTRATION_ESTIMATOR.md` before any confirmation fit. The threshold is
$\lambda_{\rm crit}=\max(3.84,\ q_{0.95}(\Lambda))$ on that set; it stayed at 3.84 except for design B at
$\sigma=10^{-5}$, where 5 of 36 calibration statistics exceeded 3.84 and the threshold rose to 7.03. The margin
$\eta$ (in the obstruction coordinate $c$) is the calibration 95th percentile of $|\hat c|+1.96\,\mathrm{se}_c$: at
$\sigma=10^{-5}$ it is 0.333 for A and 0.070 for B, i.e. $|\varepsilon|$-equivalents $9.2\times10^{-3}$ and
$1.95\times10^{-3}$.

**Confirmation [numerical, prospective].** Twelve fresh delta groups were generated with seed 20261118 (exact
depths 2 and 1 verified by the theorem classifier), each with its on-locus member and three near-misses, under
both designs, with 6 independent noise replicates at $\sigma=10^{-5}$ and 2 at $\sigma=10^{-3}$; noise seeds are
disjoint from calibration. A complete pair is correct when the on-locus member is called 2 and the near-miss 1.
The "predicted" column is the local efficient-information prediction for this exact test (fitted initial
states, frozen threshold), averaged over the same pairs. Intervals are Wilson 95% over pairs; the cluster
bootstrap over the 12 groups is given for the two primary cells.

| $\sigma=10^{-5}$, fresh, 72 pairs per cell | constrained, forced | predicted | plug-in, forced |
| --- | ---: | ---: | ---: |
| A, $\varepsilon=10^{-1}$ | 66 (0.92; 0.83–0.96) | 0.95 | 70 (0.97; 0.90–0.99) |
| B, $\varepsilon=10^{-1}$ | 71 (0.99; 0.93–1.00) | 0.99 | 67 (0.93; 0.85–0.97) |
| A, $\varepsilon=10^{-3}$ | 13 (0.18; 0.11–0.29) | 0.085 | 4 (0.06; 0.02–0.13) |
| B, $\varepsilon=10^{-3}$ | 54 (0.75; 0.64–0.84) | 0.71 | 6 (0.08; 0.04–0.17) |
| A, $\varepsilon=10^{-5}$ | 1 (0.01) | 0.048 | 2 (0.03) |
| B, $\varepsilon=10^{-5}$ | 0 (0.00) | 0.008 | 2 (0.03) |

Clustered by group, the design-B constrained rate at $\varepsilon=10^{-3}$ is 0.75 (bootstrap 0.64–0.88, per-group
rates 0.5–1.0, no group below 0.5) against 0.18 for A (0.08–0.28, five groups at 0). On the locus the forced rule
said "depth 1" in 6/72 cases under A (8.3%, Wilson 3.9–17%, above the nominal 5%) and 1/72 under B; the plug-in
did so in 2/72 and 5/72. The 95% interval for $c$ covered the true value in 273/288 (A) and 275/288 (B)
fresh cases at $\sigma=10^{-5}$, and 93/96 and 91/96 at $\sigma=10^{-3}$. Optimisation: no start failed and no case
had $\Lambda<0$ or reduced $\chi^2>1.5$ among the 576 fresh and 144 transfer fits at $\sigma=10^{-5}$; at $\sigma=10^{-3}$
8 of 192 cases had at least one start abort on a finite-time blow-up, each rescued by another start. At
$\sigma=10^{-3}$ the constrained rule completed 19/24 pairs at $\varepsilon=10^{-1}$ under B (predicted 0.84)
against 4/24 under A (predicted 0.08), and nothing was resolvable at smaller offsets under either design. The
three previously examined test groups, rerun as a transfer check with 6 replicates, agree: 16/18 and 18/18 at
$\varepsilon=10^{-1}$, and 0/18 against 14/18 at $\varepsilon=10^{-3}$, for A and B.

**Selective rule.** The implementation gives "depth 1" priority through the profile test ($\Lambda>\lambda_{\rm crit}$) rather than through interval exclusion. The likelihood-ratio and Wald statistics are locally
equivalent under regularity, but the calibrated profile threshold can differ from $z^2$;
therefore the implemented priority need not coincide with exclusion by the reported 95% interval. With the three-way rule, design B answered every fresh $\sigma=10^{-5}$ pair. At
$\varepsilon=10^{-5}$ it answers "$|c|<\eta$" for both members, which is correct in the rule's own terms
($|c|=3.6\times10^{-4}<\eta$) though it scores as a wrong depth pair. Rule-semantic errors (a "depth 1" on the
locus, or "$|c|<\eta$" when $|c|\ge\eta$) occurred 1 time per 72 under B and 6 per 72 under A in each magnitude
block, the latter being the six on-locus false positives counted once per block.

**Reading.** First, the published observation design carries usable information at $\varepsilon=10^{-1}$: with the
published initial states, both a locus-constrained fit and an unconstrained trajectory fit in the study's own
degree-5 library complete 92–97% of fresh pairs at $\sigma=10^{-5}$. This does not by itself explain why the
guarded rule failed on its original three groups; section 8 diagnoses that directly.
Second, the redesigned initial states deliver most of the predicted gain from observed data alone, raising
complete-pair accuracy at $\varepsilon=10^{-3}$ from 0.18 to 0.75 against local predictions of 0.085 and 0.71; the
gain appears only when the estimator imposes the locus, since the unconstrained plug-in stays near 0.08.
Third, the local calculus is a reasonable but not exact guide: under design A the on-locus false-positive rate
was 6/72 (Wilson 3.9–17%, compatible with the nominal 5%), and the achieved $\varepsilon=10^{-3}$ rate exceeded its
prediction by a similar margin. That pattern suggests some miscalibration of the $\chi^2_1$ reference under the
confounded design; it does not establish a heavier null.
The limits are those of the design: one stratum, one perturbation axis, a known stratum hypothesis and known
noise level, fresh groups drawn from the benchmark's own generator distribution rather than a shifted one, and
replicates nested within 12 groups.

Replay: `sh observability/run_estimator.sh` (about 45 minutes on 2 cores; requires `python generate.py data`
for the training-trajectory prior).

## 8. Why the guarded pipeline lost the $\varepsilon=10^{-1}$ delta pairs (diagnostic)

The confirmation records were hashed in `observability/FREEZE_CONFIRMATION.md` before this section's work;
nothing here changes them. `observability/diagnose.py` runs the repository's own functions (`fit_field`,
`distances`, `tolerance`, `locus_prediction`, `selection_threshold`) at 49 frames and $\sigma=10^{-5}$ on identical
observations: the 12 original benchmark test delta cases, and the 288 fresh design-A observations of section 7,
regenerated from the frozen seeds (a refit of one case reproduced its frozen $\Lambda$ to all printed digits).
Each stage is replaced alone, and each replacement is recalibrated by the repository's own procedure on the
benchmark validation split. The unchanged pipeline reproduced the published guarded forced and selective
predictions on all 12 original delta cases. No nonlinear fit failed.

| Stage (pairs at $\varepsilon=10^{-1}$) | original, forced | original, selective | fresh, forced | fresh, selective |
| --- | ---: | ---: | ---: | ---: |
| unchanged pipeline | 3/3 | 0/3 (0 answered) | 72/72 | 14/72 (14 answered) |
| nonlinear trajectory-fit coefficients | 3/3 | 0/3 (0 answered) | 72/72 | 11/72 (11 answered) |
| branch supplied, published tolerance, no abstention | 3/3 | — | 72/72 | — |
| threshold-free: $d_\delta(\text{on})<d_\delta(\text{off})$ | 3/3 | | 72/72 | |

**Coefficient recovery is not responsible.** Replacing the weak coefficients and their uncertainty with the
nonlinear trajectory fit leaves all large-offset forced pairs correct. On the original groups,
selective pairs remain unanswered; on the fresh groups, selective completions change from 14 to 11
out of 72. Thus this replacement does not recover the lost selective coverage.

**The branch guard is not responsible.** For every original and fresh case, with either coefficient source, the
guard's eligible set was {delta, origin, gamma}, so the delta test was always evaluated.

**The selective cutoff causes the observed loss.** The continuous delta distance separates every pair. The on-locus median is
0.98 (original) and 0.96 (fresh), and the near-miss median is 10.1 and 19.9, against the frozen tolerance
1.778. The forced decisions are therefore all correct. The loss is the selective step. By the definition in
`locus_prediction`, a depth-2 answer has confidence at most $\log(\text{tol}/d_2)$. With the frozen selection
cutoff 0.805 it is answered only if $d_2\le1.778\,e^{-0.805}=0.795$ [algebraic identity of the rule]. Noisy
on-locus members sit near the whitened noise floor $d_2\approx1$. None of the 3 original on-locus members met
the cutoff (median distance 0.98), and 14 of 72 fresh ones did. So the near-miss is answered and the
depth-2 member abstains, and the pair counts as wrong. Here $d_2$ is the minimum over the
eligible depth-two distances; it equals the delta distance for every original and fresh case in this diagnostic. The cutoff is chosen on validation pooled over all
strata to reach 80% accuracy, and it is tighter than the delta distances can meet at this noise level.

**A second calibration fragility.** With the branch supplied and the tolerance recalibrated by validation
macro recall on the 12 validation delta cases alone, the chosen tolerance fell to 0.75. Most on-locus members
were then called depth 1 (85% of fresh, all 3 original), and the pair rate collapsed to 11/72. With 3 depth-2
members, and with near-misses at $10^{-5}$ that are indistinguishable from the locus, this particular recalibration is unstable evidence for choosing
a tolerance, not a general impossibility theorem about calibration.

**Scope.** These are diagnostic ablations on the same observations, not an improved estimator. A rule that
drops or re-specifies the abstention step would need its own frozen calibration and a new confirmation sample.
At $\varepsilon=10^{-3}$ and $10^{-5}$ under design A, the threshold-free ordering is near chance on the fresh
observations (0.51 and 0.53 weak, 0.54 and 0.44 nonlinear), consistent with the information limit of section
4. The 3/3 ordering at $10^{-3}$ on the original groups is too small a sample to say otherwise.

Replay: `sh observability/run_diagnosis.sh` (about four minutes on two cores for a clean feature replay).
The script resumes existing diagnostic features. Remove `observability/out/diagnosis/features.jsonl`
in a clean copy to regenerate all 363 fits; `python observability/analyse_diagnosis.py` alone
rebuilds the report from saved features. This diagnostic does not change the estimator or its frozen confirmation.

## Limits

Everything here concerns one stratum and one perturbation axis; the other four strata, the closures of
other branches' loci near these points, and correlated or non-Gaussian noise are not analysed. The
unknown-background statements are first-order. The initial local design comparison uses three public-split test groups. Section 7 adds 12 fresh
generator-distribution groups; section 8 reuses the original and fresh design-A observations for diagnosis,
not a new confirmation of an improved rule.
