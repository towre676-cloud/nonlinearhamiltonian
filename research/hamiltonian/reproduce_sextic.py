#!/usr/bin/env python3
"""Reproduce the maintained sextic proof, classifier and Lean evidence.

Run --list to inspect the suites. --suite all requires Lean as well as Python;
missing tools fail the requested suite rather than silently skipping it.
This runner does not install dependencies or modify retained certificates.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import platform
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FORMAL = ROOT / "c3_strata" / "formal"
PY = sys.executable
RETAINED = {
    "c3_strata/verify_sextic_core.py": "SEXTIC_CORE_REPLAY.json",
    "c3_strata/verify_quadratic_sixfold.py": "QUADRATIC_SIXFOLD_REPLAY.json",
    "c3_strata/verify_quadratic_sixfold_models.py": "QUADRATIC_SIXFOLD_MODELS_REPLAY.json",
    "c3_strata/verify_sextic_core_v2.py": "SEXTIC_CORE_V2_REPLAY.json",
}
WRITING_SCRIPTS = {
    "c3_uniform/verify_certificate.py",
    "c3_uniform/monomial_proof.py",
    "c3_uniform/inputs/step4_final_checks.py",
}


def python(*args):
    return [PY, "-B", *args]


def tests(pattern):
    return python("-m", "unittest", "discover", "-s", "c3_strata", "-p", pattern, "-v")


SUITES = {
    "foundations": [
        ("uniform certificates", python("c3_uniform/verify_certificate.py"), ROOT),
        ("all-degree monomial identities", python("c3_uniform/monomial_proof.py"), ROOT),
        ("uniform rejection and operator regressions", python("-m", "unittest", "discover",
             "-s", "c3_uniform", "-p", "test_c3.py", "-v"), ROOT),
        ("static-tail elimination", python("c3_uniform/inputs/check_binary_static.py",
                                         "c3_uniform/inputs/binary_static_d6.json"), ROOT),
        ("symbolic static-tail identities", python("c3_uniform/inputs/step4_final_checks.py"), ROOT),
        ("repeated-root regressions", tests("test_strata.py"), ROOT),
        ("squarefree certificates and rejection tests", tests("test_squarefree.py"), ROOT),
    ],
    "classifier": [
        ("exact sextic classifier", tests("test_sextic_core.py"), ROOT),
        ("classifier inputs and bounded kernels", python("c3_strata/verify_sextic_core.py"), ROOT),
        ("portable original commands", python("-X", "utf8", "-S", "verify_cli.py"), ROOT),
    ],
    "quadratic": [
        ("quadratic family and schema-2 regressions", tests("test_quadratic_sixfold.py"), ROOT),
        ("symbolic proof-step audit", python("c3_strata/audit_quadratic_sixfold_steps.py"), ROOT),
        ("constant quadratic coefficient replay", python("c3_strata/verify_quadratic_sixfold.py"), ROOT),
        ("weighted model and parameter certificates", python("c3_strata/verify_quadratic_sixfold_models.py"), ROOT),
        ("schema-2 stage replay", python("c3_strata/verify_sextic_core_v2.py"), ROOT),
    ],
    "separable": [
        ("separable-family proof and coordinate regressions", tests("test_separable_sixfold.py"), ROOT),
        ("mixed weighted-family proof and coordinate regressions", tests("test_weighted_separable.py"), ROOT),
    ],
    "reports": [
        ("independent report acceptance and adversarial rejection", tests("test_sextic_report.py"), ROOT),
        ("public classifier/verifier handoff", tests("test_platform_cli.py"), ROOT),
    ],
    "lean": [
        ("Lean kernel compilation", ["lake", "build"], FORMAL),
        ("Lean axiom allowlist", ["lake", "env", "lean", "Audit.lean"], FORMAL),
    ],
}


def source_hashes():
    """Bind the receipt to maintained source, excluding caches and receipts."""
    paths = [ROOT / name for name in ("partner_lab.py", "sextic_core.py", "quadratic_sixfold.py",
                                     "separable_sixfold.py", "weighted_separable.py", "reproduce_sextic.py",
                                     "independent/engine.py")]
    for directory in (ROOT / "c3_strata", ROOT / "c3_uniform"):
        paths.extend(p for p in directory.rglob("*")
                     if p.is_file() and p.suffix in (".py", ".lean", ".md", ".toml")
                     and not any(part in (".lake", "__pycache__") for part in p.parts))
    paths.extend((FORMAL / "lean-toolchain", FORMAL / "lake-manifest.json"))
    paths.extend(ROOT / name for name in (
        "c3_uniform/requirements.txt", "c3_strata/requirements.txt",
        "c3_uniform/family_certificate.json", "c3_uniform/monomial_certificate.json",
        "c3_uniform/inputs/binary_static_d6.json", "c3_strata/triple_certificate.json",
        "c3_strata/squarefree_certificate.json", "c3_strata/squarefree_sample.json"))
    return {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(set(paths)) if p.is_file()}


def run_check(command, cwd):
    """Isolate legacy scripts that write receipts next to their sources."""
    if not WRITING_SCRIPTS.intersection(command):
        return subprocess.run(command, cwd=cwd, capture_output=True, text=True, timeout=3600)
    with tempfile.TemporaryDirectory(prefix="hamiltonian-replay-") as temporary:
        replay_root = Path(temporary)
        shutil.copytree(ROOT / "c3_uniform", replay_root / "c3_uniform",
                        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        run = subprocess.run(command, cwd=replay_root, capture_output=True, text=True, timeout=3600)
        if run.returncode == 0 and "c3_uniform/inputs/step4_final_checks.py" in command:
            # The inherited script prints booleans without failing on false.
            # Its output file, rather than process success alone, is the check.
            result = json.loads((replay_root / "c3_uniform/inputs/step4_results.json").read_text())
            identities = result.get("identities", {})
            expected = {f"P_delta_identity_{i}" for i in range(3)}
            if set(identities) != expected or any(value is not True for value in identities.values()):
                run.returncode = 1
                run.stderr += "\nSymbolic static-tail identities failed."
        return run


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--list", action="store_true", help="show the exact available checks")
    parser.add_argument("--suite", action="append", choices=[*SUITES, "all"],
                        help="repeat for several suites; all includes Lean")
    parser.add_argument("--output", type=Path, help="write the structured reproduction receipt")
    args = parser.parse_args(argv)
    if args.list:
        print(json.dumps({name: [label for label, _, _ in jobs] for name, jobs in SUITES.items()}, indent=2))
        return 0
    if not args.suite:
        parser.error("select --suite NAME or --suite all; use --list to inspect the checks")
    selected = list(SUITES) if "all" in args.suite else list(dict.fromkeys(args.suite))
    records = []
    for name in selected:
        for label, command, cwd in SUITES[name]:
            print(f"[{name}] {label}", file=sys.stderr, flush=True)
            start = time.monotonic()
            try:
                run = run_check(command, cwd)
                code, stdout, stderr = run.returncode, run.stdout, run.stderr
            except (OSError, ValueError, subprocess.TimeoutExpired) as exc:
                code, stdout, stderr = 1, "", str(exc)
            if code == 0:
                for script, retained in RETAINED.items():
                    if script in command:
                        try:
                            expected = json.loads((ROOT / "c3_strata" / retained).read_text())
                            if json.loads(stdout) != expected:
                                raise ValueError("replay differs from the complete retained receipt")
                        except (OSError, ValueError) as exc:
                            code = 1
                            stderr += f"\n{retained}: {exc}"
            # unittest discovery succeeds with zero tests: that is not a replay.
            if "unittest" in command and "Ran 0 tests" in stderr:
                code = 1
                stderr += "\nRequested regression suite contained no tests."
            record = {"suite": name, "check": label, "return_code": code,
                      "status": "PASS" if code == 0 else "FAIL",
                      "duration_seconds": round(time.monotonic() - start, 3),
                      "stdout": stdout, "stderr": stderr}
            records.append(record)
            print(f"[{name}] {record['status']} {label}", file=sys.stderr, flush=True)
    receipt = {
        "schema": "hamiltonian-sextic-reproduction/1",
        "status": "PASS" if all(row["return_code"] == 0 for row in records) else "FAIL",
        "requested_suites": selected,
        "not_run": [name for name in SUITES if name not in selected],
        "python_version": platform.python_version(),
        "lean_toolchain": (FORMAL / "lean-toolchain").read_text().strip(),
        "source_sha256": source_hashes(),
        "checks": records,
        "proof_boundary": {
            "end_to_end_classification_formalized": False,
            "python": "Exact replays accompany the stated written all-degree proofs.",
            "lean": "Kernel checking and axiom audits cover the named formal declarations; see formal/THEOREM_BOUNDARY.md.",
        },
    }
    encoded = json.dumps(receipt, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded)
        print(json.dumps({"status": receipt["status"], "checks": len(records),
                          "receipt": str(args.output)}))
    else:
        print(encoded, end="")
    return 0 if receipt["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
