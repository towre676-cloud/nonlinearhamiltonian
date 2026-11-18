"""Audit the frozen estimator payload without rerunning nonlinear fits.

Checks byte integrity, case completeness and independent headline recounts.
This does not certify optimization, chronology or statistical generalization.
"""
import hashlib
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
D = HERE / "out" / "estimator"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def main():
    hashes = {
        HERE / "estimator.py": "de755e00b563ecf13d0ac3b4683d534e7b954c1d1e02c308c9c995db68b08ad8",
        HERE / "fastode.py": "9907807a81dd01f1b07dc49319091e6483a94b65a742ce17942890f010ddcb21",
        D / "frozen.json": "1f664cf2068ec1e6043540db013a34ce042d82ce38958a6800e39ec44cf22963",
        D / "fresh_groups.json": "7dc80970ccbf0a0ce9e4a2a59cee65bf92b90bf16003f63ccb8ba43b2a8c5821",
    }
    for path, expected in hashes.items():
        require(hashlib.sha256(path.read_bytes()).hexdigest() == expected,
                f"Frozen hash mismatch: {path.name}")
    rows = [json.loads(line) for line in (D / "confirm.jsonl").read_text().splitlines()]
    key = lambda r: (r["phase"], r["group"], r["design"], r["sigma"], r["rep"], r["member"])
    index = {key(r): r for r in rows}
    require(len(rows) == len(index) == 912, "Missing or duplicate confirmation cases")
    fresh = {r["group"] for r in rows if r["phase"] == "fresh"}
    transfer = {r["group"] for r in rows if r["phase"] == "transfer"}
    require(len(fresh) == 12 and len(transfer) == 3 and not fresh & transfer,
            "Incorrect confirmation group partition")
    members = ("on", "eps0.1", "eps0.001", "eps1e-05")
    expected_keys = set()
    for phase, groups in (("fresh", fresh), ("transfer", transfer)):
        for group in groups:
            for design in "AB":
                for sigma, reps in ((1e-5, 6), (1e-3, 2)):
                    if phase == "transfer" and sigma == 1e-3:
                        continue
                    for rep in range(reps):
                        expected_keys.update((phase, group, design, sigma, rep, m) for m in members)
    require(set(index) == expected_keys, "Unexpected confirmation case grid")
    for row in rows:
        for field in ("lam", "c_hat", "se_c", "c_true", "chi2_red"):
            require(math.isfinite(row[field]), f"Nonfinite {field}: {key(row)}")
        require(row["se_c"] > 0 and row["lam"] >= -1e-6,
                f"Invalid fit statistic: {key(row)}")
    frozen = json.loads((D / "frozen.json").read_text())
    for design, pair_counts, fp, covered in (
        ("A", (66, 13, 1), 6, 273), ("B", (71, 54, 0), 1, 275)
    ):
        crit = frozen["cells"][f"{design}|1e-05"]["lam_crit"]
        subset = [r for r in rows if r["phase"] == "fresh" and r["design"] == design and r["sigma"] == 1e-5]
        require(sum(r["lam"] > crit for r in subset if r["member"] == "on") == fp,
                f"False-positive recount mismatch: {design}")
        require(sum(abs(r["c_hat"] - r["c_true"]) <= frozen["interval_z"] * r["se_c"] for r in subset) == covered,
                f"Coverage recount mismatch: {design}")
        for member, count in zip(members[1:], pair_counts):
            correct = sum(index["fresh", g, design, 1e-5, rep, "on"]["lam"] <= crit
                          and index["fresh", g, design, 1e-5, rep, member]["lam"] > crit
                          for g in fresh for rep in range(6))
            require(correct == count, f"Pair recount mismatch: {design}, {member}")
    print("Frozen hashes, 912-case grid, fit statistics and headline recounts verified.")


if __name__ == "__main__":
    main()
