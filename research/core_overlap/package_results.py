#!/usr/bin/env python3
"""Build a portable source bundle and exact byte manifests after verification."""
from pathlib import Path
import hashlib
import shutil
import zipfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
NAME = 'Exact_Core_Overlap_20261022.zip'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def files_below(path):
    return sorted(p for p in path.rglob('*') if p.is_file()
                  and '__pycache__' not in p.parts and p.suffix != '.pyc')


def main():
    own = [p for p in files_below(HERE) if p.name != 'MANIFEST.sha256']
    (HERE/'MANIFEST.sha256').write_text(''.join(
        sha(p)+'  '+p.relative_to(HERE).as_posix()+'\n' for p in own))
    selected = files_below(HERE) + files_below(ROOT/'extensions')
    selected += [ROOT/'README.md'] + files_below(ROOT/'programmes')
    selected = sorted(set(selected))
    archive = ROOT/'downloads'/NAME
    archive.parent.mkdir(exist_ok=True)
    bundle_records = []
    with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED,
                         compresslevel=9) as z:
        for p in selected:
            relative = p.relative_to(ROOT).as_posix()
            data = p.read_bytes()
            entry = zipfile.ZipInfo(relative, date_time=(2026, 10, 22, 0, 0, 0))
            entry.compress_type = zipfile.ZIP_DEFLATED
            entry.external_attr = 0o100644 << 16
            z.writestr(entry, data)
            bundle_records.append(hashlib.sha256(data).hexdigest()+'  '+relative+'\n')
        entry = zipfile.ZipInfo('BUNDLE_MANIFEST.sha256', date_time=(2026, 10, 22, 0, 0, 0))
        entry.compress_type = zipfile.ZIP_DEFLATED
        z.writestr(entry, ''.join(bundle_records).encode())
    checksum = archive.with_name(NAME+'.sha256')
    checksum.write_text(sha(archive)+'  '+NAME+'\n')
    # Preserve the original manifest population and add this reviewed package.
    entries = set()
    for line in (ROOT/'MANIFEST.sha256').read_text().splitlines():
        if line:
            entries.add(line.split('  ', 1)[1])
    entries.update(p.relative_to(ROOT).as_posix() for p in selected)
    entries.update([archive.relative_to(ROOT).as_posix(), checksum.relative_to(ROOT).as_posix()])
    entries.discard('MANIFEST.sha256')
    (ROOT/'MANIFEST.sha256').write_text(''.join(
        sha(ROOT/name)+'  '+name+'\n' for name in sorted(entries)))
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
    delivery = ROOT.parent
    for p in [HERE/'output/pdf/Exact_Core_Overlap_Research.pdf', archive]:
        target = delivery/p.name
        shutil.copyfile(p, target)
        assert sha(p) == sha(target)
        print(target, target.stat().st_size)


if __name__ == '__main__':
    main()
