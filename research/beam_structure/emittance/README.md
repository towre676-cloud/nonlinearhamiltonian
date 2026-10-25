# Residual-force emittance component

[THEORY.md](THEORY.md) states the identities, conditional predictor and physical
boundary. `exact.py` uses only Python integer/Fraction arithmetic; `predictor.py`
propagates conditional emittance radii through a permitted map word. They do
not depend on the older beam folders. The independent proof review is retained
in `review_note.md`.

Run exact tests from the repository root:

```sh
python -B -m unittest discover -s research/beam_structure/emittance -p 'test_*.py'
```

Run the compact NumPy retrospective replay:

```sh
python -B research/beam_structure/emittance/physical_diagnostics.py --output /tmp/emittance-physical-replay.json
```

`physical_inputs.json` is a compact extract of the earlier completed 63-run
reference. It preserves source hashes and moment conventions; it neither needs
nor contains the 9 MB particle snapshots. Regenerating this extract requires the
older reference files and can be done with `prepare_physical_inputs.py`.

Run all component verification, saving the receipt to an explicit destination:

```sh
python -B research/beam_structure/emittance/replay.py --output /tmp/emittance-replay.json
```

The 14 exact tests cover 240 weighted scalar clouds, 90 two-plane clouds,
sharpness, signed reduction, centering, coupling, invalid premises and a
composed conditional word. Physical numbers are floating-point diagnostics,
not rigorous error enclosures. Supplied future-force premises remain conditional;
no industrial speedup is claimed.
