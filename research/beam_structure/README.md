# Structural beam mathematics: executable first build

This standalone contribution implements the 24 October handoff in two separate
components. [Emittance](emittance/README.md) cancels the least-squares linear
force before bounding projected-emittance change. [Observables](observables/README.md)
discovers and independently checks a common adapted polynomial representation,
and gives explicit information-loss witnesses when extra controls break it.

[THEOREM_INDEX.md](THEOREM_INDEX.md) identifies proof boundaries. The complete
claim ledger is [CLAIMS.json](CLAIMS.json); each component also retains its own
proofs, source hashes and receipts. The original atlas, historical publication
and unresolved pure-top classification are unchanged.

Run the new build's offline checks from the repository root:

```sh
python research/beam_structure/replay_build.py --output /tmp/beam-build-replay.json
```

This runs 54 tests, replays the compact physical-moment diagnostics and exact
observable certificates, and audits the saved live-ring campaign. It does not
start new particle tracking. Requirements are declared in `requirements.txt`.
The ring prototype and its limitations are documented separately in
[../beam_ring/README.md](../beam_ring/README.md).

The prospective predictor is conditional on valid evolving residual-force
bounds; the retained physical replay is retrospective. The exact adapted
representation concerns a prescribed classical family, with one shared shear;
ordinary physical kinetic/quadrupole controls can force infinite common
polynomial closure. None of these statements establishes an industrial speedup.

New files were built in an isolated worktree so parallel research can integrate
by directory. Existing theorem and publication files were not overwritten.
