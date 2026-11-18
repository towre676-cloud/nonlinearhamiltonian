# Prospective comparison (written before any test-split evaluation)

Written 2026-11-18T03:46:58Z. Design file: out/design.json, SHA-256 ed3569660a31b077f836d3926a53afa7bcb7abb6f158c65285bdc5b4adb148d4.

Designs. A = benchmark initial states (6 states, 49 uniform samples on [0, 0.18]).
B = six initial states chosen by coordinate exchange from a 0.05 grid restricted to the benchmark's
maximal radius 0.4904, maximizing the mean over the 9 train+validation delta groups of
log I_eff, where I_eff is the Schur-complement information for the q^3p coefficient against the
12-dimensional J7 delta-locus tangent (initial states known). Same sample times and budget (294 samples).

Primary outcome. For each of the 3 test delta groups (1ae54b, 3e55e9, 90e2c8), ratio I_eff(B)/I_eff(A).
Success: all three ratios exceed 1 and their geometric mean is at least 2.

Secondary outcomes. (i) The same ratio when the six initial states are also unknown nuisance parameters.
(ii) Ratio of the known-background information ||s||^2. (iii) Monte Carlo on group 1ae54b only, sigma = 1e-5,
eps in {0, 1e-2} along q^3p, 40 noise replicates per design and eps, seeds 0..39: nonlinear Gauss-Newton
fit of the 13-parameter model (12 locus coordinates plus free r31) started at the true locus point;
report the empirical SD of eps_hat against sigma/||s_perp||, and the rejection rate of |z| > 1.96.
The Monte Carlo is a local check (initialized at truth), not an estimator evaluation.
