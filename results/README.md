# Machinery results: enveloped certificates

Every file here is a `machinery-envelope-v1` object. Each one holds the exact model, the certificate, the coefficient domain, the declared hypotheses and scope, and the atlas source ids. `RECEIPTS.json` lists every file with its SHA-256 hash, witness kind, the producer's run time and the checker's summary, together with the exact replay command.

```bash
python3 -B extensions/envelope.py check results/hamiltonian/qp3_plus_q2.json
python3 -B extensions/run_all.py            # replays every envelope listed in RECEIPTS.json
python3 -B extensions/build_results.py      # regenerates this directory deterministically
```

Files larger than 1 MB are stored as deterministic gzip (`mtime=0`). `envelope.py check` reads them directly.

| Directory | Contents |
|---|---|
| `observer/` | The feed-example minimal observer with its hidden-state witness. The rank-perfect but ill-conditioned panel, certified infeasible at γ = 999. A finite-horizon panel with correlated noise. A target-only adaptive decision tree. |
| `hamiltonian/` | All-degree dynamic cores, each with its Weyl receipt embedded: the calibrations `q³`, `qp³`, `qp³+q²`; the W2 strata `qp³+p²` and `qp³+q²+p²`; and `q³p³`, `q²p²`, `q²p³`, `p³+q²`. |
| `structure/` | The triangle primitive and its obstruction functional. DGLA obstruction and lifting certificates for a toy model and the Heisenberg deformation complex. |
| `arithmetic/` | The four handoff Pell fixtures with mod-3 cycles and height counts, and the proper-power unit `17+12√2` at height `10^30`. |

The scope stated in each envelope is the whole claim. Hypotheses that do not appear there are not assumed.
