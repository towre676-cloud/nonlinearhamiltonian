"""Refresh the Hamiltonian manifest and build the portable source bundle."""
from hashlib import sha256
import json
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "MANIFEST.sha256"
OUT = ROOT / "output" / "Nonlinear_Hamiltonian_Partners_Source_Bundle.zip"
PREFIX = "Nonlinear_Hamiltonian_Partners"
PACKAGE_PATH = "research/hamiltonian"


def main():
    names = sorted(line.split("  ", 1)[1] for line in MANIFEST.read_text().splitlines())
    if len(set(names)) != len(names):
        raise ValueError("Hamiltonian manifest contains duplicate paths")
    files = {name: (ROOT / name).read_bytes() for name in names}
    files[MANIFEST.name] = "".join(
        f"{sha256(data).hexdigest()}  {name}\n" for name, data in files.items()
    ).encode()
    MANIFEST.write_bytes(files[MANIFEST.name])
    OUT.parent.mkdir(parents=True, exist_ok=True)
    members = {f"{PACKAGE_PATH}/{name}": data for name, data in files.items()}
    members["README.md"] = files["SOURCE_BUNDLE_README.md"]
    with ZipFile(OUT, "w", ZIP_DEFLATED, compresslevel=9) as bundle:
        for name, data in sorted(members.items()):
            member = ZipInfo(f"{PREFIX}/{name}")
            member.create_system = 3
            member.external_attr = 0o100644 << 16
            bundle.writestr(member, data, compress_type=ZIP_DEFLATED, compresslevel=9)
    print(json.dumps({"files": len(members), "bytes": OUT.stat().st_size,
                      "sha256": sha256(OUT.read_bytes()).hexdigest()}))


if __name__ == "__main__":
    main()
