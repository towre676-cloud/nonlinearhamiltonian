# BNL public-model qualification result

This is an independently frozen numerical confirmation on a historical public BNL CB65pm lattice, not an operating-machine claim. The physical sector is fixed-energy transverse tracking: 3 GeV, delta=0, no RF/radiation/space charge/errors or added mechanical apertures. Sixteen small-core launches and forty-eight wide launches were generated using seed 20261024 before any outputs. Every method used 256 full turns. All fifteen variants and the accuracy gate were fixed before this confirmation ran.

The frozen sources and helper hashes were checked unchanged after execution. The native source parser gives ten integration steps despite the Elegant file specifying forty; direct step refinement was essential. Native40 and native80 agree on 63 of 64 survival labels; point 48 remains unresolved. Qualification requires zero disagreements on the agreed labels and core position/momentum errors at most 1 micrometre / 1 microradian against native80.

| Method | Qualifies | Tracking seconds | First-workload seconds | Label errors on agreed reference | Core position error (m) |
|---|---|---:|---:|---|---:|
| native2 | False | 1.452735 | 1.558404 | [17, 33, 40, 50, 57, 62] | 0.00027550732789175344 |
| native4 | False | 2.896532 | 3.005802 | [33] | 0.0001777075021582218 |
| native10 | False | 6.611080 | 6.708978 | [33] | 0.00010166332330882851 |
| native20 | False | 12.948143 | 13.068855 | [33] | 6.253227084453498e-06 |
| native40 | True | 25.238835 | 25.343228 | [] | 3.6659355534191716e-07 |
| native80 | True | 49.550408 | 49.659339 | [] | 0.0 |
| fused10 | False | 1.598872 | 1.994098 | [33] | 0.00010166332338286563 |
| fused2 | False | 0.439912 | 0.796914 | [] | 0.00010168518109115868 |
| fused4 | False | 1.041329 | 1.401313 | [33] | 0.00010166465723711028 |
| analytic10 | True | 2.573241 | 2.676299 | [] | 2.439570357741337e-08 |
| analytic2 | False | 1.698597 | 1.802678 | [33] | 1.147400589335745e-08 |
| analytic4 | False | 1.909820 | 2.010941 | [33] | 2.304312066476349e-08 |
| fused40_s10 | True | 1.855952 | 2.204581 | [] | 3.666294018407211e-07 |
| fused40_s2 | True | 1.550006 | 1.906800 | [] | 3.888035757776935e-07 |
| fused40_s4 | True | 1.257812 | 1.664867 | [] | 3.679825201384143e-07 |

The strongest qualified existing method in the independent 256-turn confirmation is built-in QuadLinearPass/BendLinearPass with ten sextupole steps (`analytic10`). It costs 2.67630 seconds for construction, warmup and one tracking batch. The guarded compiled candidate `fused40_s4` costs 1.66487 seconds including an allocated clean 0.127988-second kernel build, native construction, map compilation, warmup and all guard-triggered native fallbacks: an observed 1.6075-fold first-workload gain. Tracking with fallback alone is 2.57324 versus 1.25781 seconds, an observed 2.0458-fold ratio. Twenty-five particles per repeat fall back; those calls are charged.

Comparing only with forty-step uniform tracking gives about 15.22-fold savings, but the existing analytic baseline already produces most of that reduction. We should not advertise 15-fold improvement over the best existing method. All coarse native variants and low-step analytic variants that fail accuracy remain in the table.

Reference40/80 generation costs 75.00257 seconds, separately from online work. A one-off calculation that must generate this qualification reference does not have an all-in speedup. Conditional amortization over future fresh workloads is arithmetic, not a measured deployment result; exact duplicate queries can be cached by an ordinary method and do not count as new tasks. Cold interpreter/package startup and report serialization are not included in the per-method workload timer.

The gain is confined to this finite frozen batch and nominal model. It does not prove a uniform phase-space error bound, present NSLS-II operating equivalence, six-dimensional evolution, RF/radiation/collective behavior, or an end-to-end tuning gain. Source-bound arrays, cost logs, all variants and the unresolved reference point are retained. A useful BNL staff request would be to replay the kernel with an approved current lattice and acceptance/accuracy contract. No outreach was sent.

## Longer post-selection backcheck

A separately frozen post-selection backcheck reused the original 128 launches at 512 turns and existing40/80 references; it is explicitly not another independent confirmation. The selected fused40_s4 candidate passes all 128 agreed labels and the same core gate, with maximum core position error 0.7257 micrometres and momentum error 0.06346 microradians. All 53 guard fallbacks per repeat are charged. Its tracking median is 3.29408 seconds; first-workload cost is 3.66249 seconds including a copy of the kernel build cost.

The analytic10 comparator takes 10.13972 seconds including construction/warmup, but fails one agreed survival label, index 41. Therefore the original two-method backcheck does not report a quality-matched speedup ratio. Stronger analytic integration settings were then evaluated through the separately frozen comparator addendum described below. The independent 64-point confirmation retains its finite-test 1.6075-fold first-workload gain; the original longer two-method check demonstrates candidate robustness on a broader sample. The subsequent ordinary-comparator extension supplies a separate post-selection ratio, as detailed below.

Run the portable, offline array/source/gate/accounting checker with `python verify_results.py --data-root /path/to/evidence --output /tmp/bnl-check.json`. It needs NumPy and starts no new tracking.

## Additional declared comparators and refinement diagnosis

A later, prospectively serialized post-selection addendum evaluated analytic20 and analytic40 on the entire 128-point / 512-turn backcheck. Both pass the original numerical gate; analytic20 is the faster additional ordinary comparator at 14.13526 seconds including construction/warmup (one measured tracking repeat), versus 3.66249 seconds for the already selected candidate (three repeats). The resulting observed post-selection ratio is 3.8595. This is not an independent confirmation and must not replace the frozen 256-turn 1.6075-fold result as such.

The requested single-point diagnostic exposes nonmonotonic refinement. For backcheck point 41, native 40/80 survive, native 160 loses the particle at turn 185, and native 320 survives; analytic 20/40 survive. For confirmation point 48, native 40 loses, native 80/160/320 survive, analytic 20 loses and analytic 40 survives. Neither pairwise agreement nor the highest tried level proves physical convergence. No original consensus labels or gates were rewritten. The loss-label/turn/element diagnostic arrays were derived from retained JSON records; full final-state coordinate arrays for those single-point runs were not separately retained.

Portable live relaunches can use run_relocated.py with explicit source/runtime/compiler/output paths; it checks the original lattice hash. Before a new performance experiment, measure a fresh local plugin build receipt rather than reusing this host's build timing. Offline verification requires only NumPy and uses relative evidence paths.
