# bosonic-gsim small replays

Pinned upstream commit: `4eddbc9c838f7164520ae2ed06d1778beacd906a` (main, authored 2026-08-19). Source tree: `2a515fa9603bf1bb6c7c3bdf4109c3fc7854b0bd`. Source: <https://github.com/TimothyHeightman/bosonic-gsim>. Companion paper: <https://arxiv.org/abs/2608.17094>. Acquired through read-only GitHub connector. Twenty-one source/configuration/reference files were fetched; each was validated against its exact upstream Git blob identity and recorded with SHA256 in `source_manifest.json`. Original `source/` remains unchanged. No installation was required. Upstream Apache-2.0 license is retained at `source/LICENSE`.

Commands, from a writable copy of `source/`, with `PYTHONPATH=src`, `MPLBACKEND=Agg` and BLAS-related thread counts fixed to one:

```sh
python experiments/fig10_nilpotent_phase/run.py
python experiments/fig8_beyond_gaussian/run.py
```

For an isolated replay that first verifies source hashes, run `python replay.py --output /tmp/bosonic-gsim-replay`. Dependencies: NumPy, SciPy, Matplotlib and PyYAML; see recorded versions in the receipt.

Fig10 exited 0 in 3.964 seconds, including imports, scaling measurements and PDF output. Single-mode coefficient propagation agreed with the FFT grid within 1.9984014443252818e-15; grid refinement changed results by at most 3.1086244689504383e-15. Two-mode errors were 1.8648277366750676e-17 and 4.0766001685454967e-17 respectively. The final non-Gaussian fourth cumulant was 0.4833225568470616.

Fig8 exited 0 in 0.819 seconds. Twelve four-mode random interferometers, seed 3, agreed with the independent truncated-Fock implementation within 5.551115123125783e-16. Hong–Ou–Mandel analytic and Fock checks also agreed below 5e-16.

All seven reported numerical errors passed a separately applied 1e-12 acceptance threshold. Full outputs, timings, environment, commands and caveats are in `replay_receipt.json`; the generated result files and stdout/stderr logs are retained. Timings are evidence from one host and are not portable performance guarantees.

These are successful reproductions of an existing external method's small examples. They establish neither a new mathematical theorem nor a speedup from our project. FFT/Fock checks use floating point and are not exact-arithmetic proof certificates. Full repository tests and the large raw-production suite were not run. This is a minimal source subset, not a complete upstream checkout.
