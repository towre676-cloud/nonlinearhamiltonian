# Sextic C3 theorem handoff

Read **C3_THEOREM.md** for the complete statement, proof, scope and dependencies.

Python 3.11+ and SymPy 1.14.0 were used. Install with `python -m pip install -r requirements.txt` if needed.

From this directory run:

```
python verify_certificate.py
python monomial_proof.py
python -m unittest discover -s . -p test_c3.py -v
```

Regenerate the family certificate with `python family_certificate.py`. The verifier is independent of that producer and should be run after regeneration.

The static tail can be replayed separately:

```
python inputs/check_binary_static.py inputs/binary_static_d6.json
python inputs/step4_final_checks.py
```

`verification.json`, `monomial_certificate.json`, `static_tail_verification.json`, and `regression_tests.log` record the completed checks. All supplied inputs are pinned by provenance and checksums. No GitHub branch or canonical documentation has been changed by this handoff.
