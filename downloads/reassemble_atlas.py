#!/usr/bin/env python3
"""Verify and reassemble the split mathematics atlas archive using Python stdlib.

Run from any directory: python /path/to/downloads/reassemble_atlas.py
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import tempfile

FILENAME = 'Mathematics_Atlas_2023_2026_Source_Bundle.zip'
EXPECTED_SIZE = 22147097
EXPECTED_SHA256 = '69e639d10f90a50180dcee289d31f0a405cafb882705f1813a53c3cf56046475'
BLOCK_SIZE = 1024 * 1024


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(BLOCK_SIZE), b''):
            digest.update(block)
    return digest.hexdigest()


def reassemble(parts_dir: Path, output: Path) -> bool:
    manifest = json.loads((parts_dir / 'parts.json').read_text(encoding='utf-8'))
    if (manifest.get('filename'), manifest.get('size'), manifest.get('sha256')) != (
            FILENAME, EXPECTED_SIZE, EXPECTED_SHA256):
        raise ValueError('The parts index does not match the expected atlas archive.')
    parts = manifest.get('parts')
    if not isinstance(parts, list) or not parts:
        raise ValueError('The parts index has no parts.')
    seen = set()
    for index, part in enumerate(parts, 1):
        name = part.get('filename', '')
        if (name != f'{FILENAME}.part{index:03d}' or Path(name).name != name
                or name in seen or '/' in name or '\\' in name):
            raise ValueError('The parts index has an invalid or repeated filename.')
        if type(part.get('size')) is not int or part['size'] <= 0:
            raise ValueError(f'Invalid part size: {name}')
        if not re.fullmatch(r'[0-9a-f]{64}', str(part.get('sha256', ''))):
            raise ValueError(f'Invalid part hash: {name}')
        seen.add(name)
    if sum(p['size'] for p in parts) != EXPECTED_SIZE:
        raise ValueError('The part sizes do not sum to the archive size.')

    already_correct = (output.is_file() and output.stat().st_size == EXPECTED_SIZE
                       and file_sha256(output) == EXPECTED_SHA256)
    temp_path = None
    writer = None
    try:
        if not already_correct:
            output.parent.mkdir(parents=True, exist_ok=True)
            descriptor, name = tempfile.mkstemp(prefix=f'.{FILENAME}.', suffix='.tmp', dir=output.parent)
            temp_path = Path(name)
            writer = os.fdopen(descriptor, 'wb')
        full_digest = hashlib.sha256()
        full_size = 0
        for part in parts:
            path = parts_dir / part['filename']
            if not path.is_file() or path.stat().st_size != part['size']:
                raise ValueError(f'Missing part or incorrect size: {part["filename"]}')
            part_digest = hashlib.sha256()
            part_size = 0
            with path.open('rb') as source:
                for block in iter(lambda: source.read(BLOCK_SIZE), b''):
                    part_digest.update(block)
                    full_digest.update(block)
                    part_size += len(block)
                    full_size += len(block)
                    if writer is not None:
                        writer.write(block)
            if part_size != part['size'] or part_digest.hexdigest() != part['sha256']:
                raise ValueError(f'Part hash mismatch: {part["filename"]}')
        if full_size != EXPECTED_SIZE or full_digest.hexdigest() != EXPECTED_SHA256:
            raise ValueError('The assembled atlas archive hash does not match.')
        if writer is not None:
            writer.flush()
            os.fsync(writer.fileno())
            writer.close()
            writer = None
            os.replace(temp_path, output)
            temp_path = None
        return already_correct
    finally:
        if writer is not None:
            writer.close()
        if temp_path is not None:
            temp_path.unlink(missing_ok=True)


def main() -> int:
    adjacent = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--parts-dir', type=Path, default=adjacent / 'atlas-source-parts',
                        help='Directory containing parts.json and every archive part.')
    parser.add_argument('--output', type=Path, default=adjacent / FILENAME,
                        help='Destination ZIP; default is adjacent to this script.')
    args = parser.parse_args()
    try:
        existed = reassemble(args.parts_dir, args.output)
    except (OSError, ValueError, TypeError, KeyError, json.JSONDecodeError) as error:
        print(f'Atlas reassembly failed: {error}', file=sys.stderr)
        return 1
    print(('Verified existing archive: ' if existed else 'Reassembled and verified: ') + str(args.output))
    print(f'SHA-256: {EXPECTED_SHA256}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
