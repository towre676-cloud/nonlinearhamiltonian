# Constrained estimator: frozen before confirmation

Written 2026-11-18T04:01:32Z, before any confirmation fit was run.
Frozen thresholds: out/estimator/frozen.json, SHA-256 1f664cf2068ec1e6043540db013a34ce042d82ce38958a6800e39ec44cf22963.
Estimator code: estimator.py SHA-256 de755e00b563ecf13d0ac3b4683d534e7b954c1d1e02c308c9c995db68b08ad8; fastode.py SHA-256 9907807a81dd01f1b07dc49319091e6483a94b65a742ce17942890f010ddcb21.
Fresh groups: out/estimator/fresh_groups.json SHA-256 7dc80970ccbf0a0ce9e4a2a59cee65bf92b90bf16003f63ccb8ba43b2a8c5821
(generator seed 20261118, 12 delta groups, exact depths verified by the theorem classifier).

Settings frozen in estimator.py: trf least squares, x_scale=jac, tolerances 1e-12, max_nfev 60, bound
0.05 <= x <= 20; initial states fitted as nuisance from a Legendre-smoothed start; four deterministic starts for
the transverse model (study weak D5 fit, weighted-library weak fit, the latter with ridge 1e-2 toward a prior
built from benchmark training trajectories and training labels only, and that prior itself); two starts for the
locus model (best transverse fit with eps removed, and the weak fit); one transverse refit from the best locus fit.
No start uses generating coefficients, the true locus point, or the true perturbation. Noise sigma is the
stated level of each case.

Calibration used only train and validation on-locus groups (9 groups, 4 noise replicates per design and sigma).
Confirmation: (a) transfer check on the 3 previously examined test groups, all 4 members, both designs,
sigma = 1e-5, 6 replicates; (b) 12 fresh groups, all 4 members, both designs, sigma = 1e-5 with 6 replicates
and sigma = 1e-3 with 2 replicates. Noise seeds are SHA-256 of the case key, disjoint from calibration.
Primary questions: complete-pair accuracy at eps = 1e-1 (estimator failure) and at eps = 1e-3, sigma = 1e-5
(design A versus B), for the constrained forced rule. Secondary: selective rule, plug-in, false positives on the
locus, 95% interval coverage for c, optimisation failures, and the local efficient-information prediction
(J7 locus with fitted initial states) of the rejection rate at the frozen threshold.
