"""Replay the small public-data ingestion without downloading bulk datasets.

Checks source-file hashes, a real measured wire-profile ZIP member, and actual
NPY shapes. Does not establish simulator accuracy or closed-loop performance.
"""
from pathlib import Path
import hashlib
import io
import json
import zipfile


def check(root=None):
    import numpy as np
    from scipy.io import loadmat

    root = Path(root) if root else Path(__file__).parent / 'dataset_inspection'
    lattice = json.loads((root / 'storage_lattice_downloads.json').read_text())
    for row in lattice:
        path = root / Path(row['local_path']).name
        assert path.stat().st_size == row['bytes']
        assert hashlib.sha256(path.read_bytes()).hexdigest() == row['sha256']
    ring = loadmat(root / 'at_hmba.mat', squeeze_me=True, struct_as_record=False)['RING'].ravel()
    assert len(ring) == 122
    assert int(ring[0].Periodicity) == 32
    assert float(ring[0].Energy) == 6e9
    wire = json.loads((root / 'sns_extracted_member_manifest.json').read_text())
    data = (root / 'sns_measured_wire_profile_20240819.txt').read_bytes()
    assert hashlib.sha256(data).hexdigest() == wire['member_sha256']
    with zipfile.ZipFile(io.BytesIO((root / 'sns_zip_tail.bin').read_bytes())) as z:
        assert z.read(wire['member']) == data
    rf = np.load(root / 'lansce_run9rf.npy', allow_pickle=False)
    assert rf.shape == (100, 8) and rf.dtype == np.dtype('float32')
    assert np.isfinite(rf).all()
    f = io.BytesIO((root / 'lansce_phase_header.bin').read_bytes())
    version = np.lib.format.read_magic(f)
    reader = np.lib.format.read_array_header_1_0 if version == (1, 0) else np.lib.format.read_array_header_2_0
    shape, fortran, dtype = reader(f)
    assert shape == (100, 48, 15, 256, 256)
    assert dtype == np.dtype('float32') and not fortran
    return {
        'status': 'passed',
        'lattice_files_hash_checked': len(lattice),
        'hmba_cell_elements': len(ring),
        'hmba_periodicity': 32,
        'measured_wire_profile_bytes': len(data),
        'measured_wire_zip_crc_and_sha256': 'passed',
        'lansce_rf_shape': list(rf.shape),
        'lansce_phase_header_shape': list(shape),
        'retained_discrepancy': 'Published README says 500 examples; both actual arrays declare 100.',
        'scope': 'Small-data ingestion and provenance consistency only; no bulk-array, physics or performance validation.'
    }


if __name__ == '__main__':
    print(json.dumps(check(), indent=2))
