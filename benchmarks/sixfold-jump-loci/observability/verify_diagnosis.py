"""Check the confirmation freeze and the saved abstention diagnosis.

Audits saved evidence; use run_diagnosis.sh with a clean feature cache to refit.
"""
import hashlib
import json
import re
from pathlib import Path

import numpy as np

from verify_saved import require

HERE = Path(__file__).resolve().parent


def main():
    frozen = re.findall(r"^    ([a-f0-9]{64})  (\S+)$",
                        (HERE / "FREEZE_CONFIRMATION.md").read_text(), re.M)
    expected_files = {"confirm.jsonl", "calibration.jsonl", "frozen.json", "score.json",
                      "fresh_groups.json", "prior.json"}
    require(len(frozen) == 6 and {name for _, name in frozen} == expected_files,
            "Incomplete confirmation freeze")
    for digest, name in frozen:
        require(hashlib.sha256((HERE / "out" / "estimator" / name).read_bytes()).hexdigest() == digest,
                f"Confirmation freeze mismatch: {name}")
    rows = [json.loads(line) for line in (HERE / "out" / "diagnosis" / "features.jsonl").read_text().splitlines()]
    keys = [tuple(r["key"]) for r in rows]
    require(len(keys) == len(set(keys)) == 363, "Missing or duplicate diagnostic features")
    exact = [json.loads(line) for line in (HERE.parent / "reference" / "exact.jsonl").read_text().splitlines()]
    fresh = json.loads((HERE / "out" / "estimator" / "fresh_groups.json").read_text())
    expected_keys = {("val", r["id"]) for r in exact if r["split"] == "validation"}
    expected_keys.update(("orig", r["id"]) for r in exact if r["split"] == "test" and r["stratum"] == "delta")
    expected_keys.update(("fresh", f"{g['group']}|{m}|{rep}") for g in fresh
                         for m in ("on", "eps0.1", "eps0.001", "eps1e-05") for rep in range(6))
    require(set(keys) == expected_keys, "Incorrect diagnostic case grid")
    for row in rows:
        require(row["nl_ok"], f"Nonlinear fit failed: {row['key']}")
        for field in ("weak_guarded", "weak_all", "nl_guarded", "nl_all"):
            values = np.asarray(row[field])
            require(values.shape == (6,) and np.all(np.isfinite(values)) and np.all(values >= 0),
                    f"Invalid distance vector: {row['key']}, {field}")
    report = json.loads((HERE / "out" / "diagnosis" / "report.json").read_text())
    require(report["published_check"] == {"cases": 12, "identical": 12}, "Published predictions disagree")
    for source, count, selective in (("orig", 3, 0), ("fresh", 72, 14)):
        cell = report["pairs"][f"{source}|S0 unchanged|eps0.1"]
        require((cell["n"], cell["forced"], cell["selective"]) == (count, count, selective),
                f"Large-offset diagnosis disagrees: {source}")
    tol = report["rules"]["S0 unchanged"]["tol"]
    cutoff = report["rules"]["S0 unchanged"]["selection"]
    for source, expected_answered in (("orig", 0), ("fresh", 14)):
        sub = [r for r in rows if r["key"][0] == source]
        values = np.asarray([r["weak_guarded"] for r in sub])
        require(np.all(values[:, 2] == values[:, :-1].min(axis=1)),
                f"Delta is not the minimum depth-two distance: {source}")
        ids_on = {r["id"] for r in exact if r["least_depth"] == 2}
        on = [r for r in sub if (r["key"][1] in ids_on if source == "orig" else "|on|" in r["key"][1])]
        require(sum(r["weak_guarded"][2] <= tol * np.exp(-cutoff) for r in on) == expected_answered,
                f"Abstention-bound recount disagrees: {source}")
    print("Six confirmation hashes, 363 diagnostic cases and the abstention mechanism verified.")


if __name__ == "__main__":
    main()
