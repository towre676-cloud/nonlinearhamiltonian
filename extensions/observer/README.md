# Exact observer seed

This Python-standard-library seed implements finite rational target-word closure, a minimal linear observer certificate, and a static initial-sensor factorization or explicit invisible-state witness. It is new executable handoff material for the proposed enhancement programme. It does not implement general noisy sensor optimization, a general adaptive experiment editor, nonlinear observability or unrestricted robust dynamics.

From the handoff package root, if the files are placed under `extensions/observer/`:

```bash
python3 -B extensions/observer/observation_closure_reference.py verify
python3 -B extensions/observer/observation_closure_reference.py compile extensions/observer/observation_example.json --output observer_certificate.json
python3 -B extensions/observer/observation_closure_reference.py check observer_certificate.json --input extensions/observer/observation_example.json
```

On Windows, replace `python3` with `py -3`. Python 3.10 or later suffices. Inputs accept exact integer or rational strings; floating JSON numbers are rejected. A chronological word `[a,b]` acts on the state by `A_b A_a`, and the basis provenance uses the corresponding target row `G A_b A_a`.

The example observes the current difference coordinate `d` but permits an action `d'=c+d`. The compiler returns a two-dimensional future-target observer and a hidden initial state changing `c` while leaving the initial observation fixed. Its future output witness is explicit. Replace the observation matrix with the two coordinate rows to obtain a valid recovery certificate. These are different tasks even though the present target is recovered in both.

The independent certificate checker verifies word provenance, exact basis rank, all action-intertwining identities, the target factorization, and either the recovery identity or the invisible-state witness. The proof in `programmes/TARGET_OBSERVERS.md` explains why these finite identities prove the stated all-word conclusion. Supplying `--input` binds the certificate to the intended input model; without it the checker verifies the encoded model only. Diagnostic rank-history logs are not additional proof objects.

When sensor rows are redundant the exported recovery matrix is one exact solution; it is not claimed to minimize an operator norm or correlated-noise amplification. Those require the majorization/PSD layer specified in the programme. The 26 verification checks include hand-auditable closure, shared-nuisance, action-order, ill-conditioning, zero-target, corrupted-certificate and finite decision-cost fixtures. Several checks deliberately establish limits of stronger claims rather than general implementations of those extensions.
