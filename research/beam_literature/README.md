# Beam-method literature and data review

Read [RECOMMENDATION.md](RECOMMENDATION.md) for the decision and
[NEXT_PUSH_SPEC.md](NEXT_PUSH_SPEC.md) for the prospective experiment.
[SOURCE_CATALOG.json](SOURCE_CATALOG.json) contains 73 method-source records
covering 81 distinct primary URL strings. [datasets.md](datasets.md) and
[datasets_catalog.json](datasets_catalog.json) cover 12 public asset groups,
including access and licensing gaps. Repeated source records are cross-checks,
not independent publications.

The selected next experiment adopts multipointBAX for independent nonlinear
storage-ring particle tracking, using a public HMBA lattice. No new optimizer,
tenfold reproduction or facility deployment is claimed. Particle-in-Fourier
is a separate, promising full-solver reproduction for long-time space charge.
The earlier beam-matching evidence remains unchanged.

[CORE_VS_TRACTABILITY.md](CORE_VS_TRACTABILITY.md) gives the direct mathematical
fit audit: exact Moyal/Poisson agreement does not imply finite observable closure.
The included exact-integer checker verifies thirteen instances of the proved
recurrence. The bosonic-gsim quantum workflow is close prior art, not a new
method proposed by this review. Its two small seeded quantum examples were
also executed, with source hashes and residuals recorded in
`bosonic_gsim_replay/`; they do not establish an industrial speedup.

Small licensed original data, provenance metadata and descriptive replays are
included. Large ARES/SNS/LANSCE archives and unlicensed weights are not bundled.
The original FBPIC archive is included with attribution and publisher checksum.
No downloaded pickle/model was executed. Third-party code retained for source
inspection has its own license; its training has not been run.

From the repository root, install the data dependencies in a separate Python
environment and replay the ingestion:

```sh
python -m pip install -r research/beam_literature/requirements-data.txt
python research/beam_literature/replay_ingestion.py
```

The optional public-ring feasibility probe requires the additional dependencies:

```sh
python -m pip install -r research/beam_literature/requirements-ring.txt
python research/beam_literature/smoke_public_ring.py
```

It expands all 32 HMBA cells and compares batched with individual particle
tracking. Its saved timings exclude installation, cold import and warm-up;
they are not an optimization or industrial speedup. RF, radiation, space charge
and errors are off. Existing research verification is a separate command under
`research/beam_integration/replay_all.py` in the full project.

The literature performance numbers were source-audited rather than rerun.
[RESEARCH_CLAIMS.json](RESEARCH_CLAIMS.json) preserves that boundary.
