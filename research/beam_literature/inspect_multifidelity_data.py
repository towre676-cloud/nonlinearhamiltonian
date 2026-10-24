#!/usr/bin/env python3
"""Inspect the pinned public FBPIC archive without executing pickle payloads.

This checks an archived dataset, not the FBPIC solver or optimization gains.
Inputs are retained in their encoded coordinates: no unverified unit decoding.
"""
from pathlib import Path
import argparse
import hashlib
import io
import json
import urllib.request
import zipfile

import numpy as np

HERE = Path(__file__).resolve().parent
URL = 'https://zenodo.org/records/7565882/files/DataSet.zip?download=1'
MD5 = 'e729cb8f0c1a5c6399050a0a23974d3b'
SHA256 = '83522f2fac3bc5dc0670f44936b8f337601e5a93090ec3e1a4c57d43c0165eb8'


def inspect(path):
    raw = Path(path).read_bytes()
    if len(raw) != 248015 or hashlib.md5(raw).hexdigest() != MD5:
        raise ValueError('Archive byte size or publisher MD5 mismatch')
    if hashlib.sha256(raw).hexdigest() != SHA256:
        raise ValueError('Pinned archive SHA256 mismatch')
    arrays = {}
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        if z.testzip() is not None:
            raise ValueError('Archive CRC failure')
        for name in z.namelist():
            if name.endswith('.npy'):
                a = np.load(io.BytesIO(z.read(name)), allow_pickle=False)
                if a.ndim != 2 or not np.isfinite(a).all():
                    raise ValueError('Unexpected dimension or nonfinite array')
                arrays[name] = a
    x = arrays['DataSet/Combined/train_x.npy']
    y = arrays['DataSet/Combined/train_obj.npy']
    if x.shape != (2443, 5) or y.shape != (2443, 3):
        raise ValueError('Published combined array shape mismatch')
    if np.any(x < 0) or np.any(x > 1):
        raise ValueError('Encoded input outside observed unit cube')
    groups, controls = {}, {}
    for i, row in enumerate(x):
        groups.setdefault(tuple(row), []).append(i)
        controls.setdefault(tuple(row[:4]), []).append(i)
    conflicts = [
        {'encoded_input': list(key), 'row_indices': rows,
         'objectives': y[rows].tolist()}
        for key, rows in groups.items()
        if len(np.unique(y[rows], axis=0)) > 1
    ]
    cross = [rows for rows in controls.values()
             if len(set(x[rows, 4])) > 1]
    significant_cross = [rows for rows in controls.values()
                         if np.ptp(x[rows, 4]) >= .05]
    paired = []
    for rows in significant_cross:
        rows = np.asarray(rows)
        values = x[rows, 4]
        low, high = values.min(), values.max()
        low_rows = rows[np.abs(values-low) <= 1e-12]
        high_rows = rows[np.abs(values-high) <= 1e-12]
        paired.append({
            'first_four_encoded_inputs': x[rows[0], :4].tolist(),
            'lowest_encoded_fidelity': float(low),
            'highest_encoded_fidelity': float(high),
            'low_row_indices': low_rows.tolist(), 'high_row_indices': high_rows.tolist(),
            'mean_low_objectives': y[low_rows].mean(axis=0).tolist(),
            'mean_high_objectives': y[high_rows].mean(axis=0).tolist(),
        })
    f = x[:, 4]
    zero = y[:, 0] == 0
    penalty = (y[:, 1] == -300) & (y[:, 2] == -1000)
    if not np.array_equal(zero, penalty):
        raise ValueError('Observed zero-charge penalty convention changed')
    summary = {
        'status': 'passed_archive_and_array_consistency',
        'archive': {'bytes': len(raw), 'publisher_md5': MD5, 'sha256': SHA256},
        'source': 'https://zenodo.org/records/7565882',
        'license_from_live_record_api': 'CC-BY-4.0',
        'arrays': {
            name: {'shape': list(a.shape), 'dtype': str(a.dtype),
                   'finite': True, 'column_min': a.min(axis=0).tolist(),
                   'column_max': a.max(axis=0).tolist()}
            for name, a in sorted(arrays.items())
        },
        'combined': {
            'rows': len(x), 'unique_encoded_inputs': len(groups),
            'unique_input_output_pairs': len(np.unique(np.c_[x, y], axis=0)),
            'unique_first_four_input_tuples': len(controls),
            'repeated_first_four_input_groups': sum(len(v) > 1 for v in controls.values()),
            'groups_with_distinct_fidelity_values': len(cross),
            'groups_with_fidelity_spread_at_least_0p05': len(significant_cross),
            'conflicting_exact_input_groups': len(conflicts),
            'rows_in_conflicting_exact_input_groups': sum(len(c['row_indices']) for c in conflicts),
            'conflicts': conflicts,
            'substantive_cross_fidelity_groups': paired,
            'paired_charge_increases_at_highest_fidelity': sum(
                r['mean_high_objectives'][0] > r['mean_low_objectives'][0] for r in paired),
            'paired_charge_decreases_at_highest_fidelity': sum(
                r['mean_high_objectives'][0] < r['mean_low_objectives'][0] for r in paired),
            'substantive_paired_groups_all_at_unit_cube_corners': all(
                all(v in (0., 1.) for v in r['first_four_encoded_inputs']) for r in paired),
            'fidelity_histogram': {
                'edges': [0, .25, .5, .75, 1],
                'counts': np.histogram(f, bins=[0, .25, .5, .75, 1])[0].tolist(),
                'exact_zero': int((f == 0).sum()), 'exact_one': int((f == 1).sum()),
                'convention': 'left-closed bins, final bin includes one',
            },
            'zero_charge_penalty_rows': int(zero.sum()),
            'objective_distance_and_bandwidth_nonpositive': bool(np.all(y[:, 1:] <= 0)),
            'encoded_inputs_are_in_unit_cube': True,
        },
        'boundaries': [
            'No raw particle trajectories, per-row elapsed costs, seed IDs, or run IDs occur in the ZIP.',
            'The record names physical columns, but supplied input numbers are encoded in [0,1]; physical decoding is not embedded.',
            'Repeated exact encoded inputs have distinct outputs; the cause is not identified by this archive.',
            'Cross-fidelity correlation is not a uniform physical error certificate.',
            'This finite adaptively sampled table is not an unrestricted simulation oracle.',
        ],
    }
    return summary


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--archive', type=Path, default=HERE / 'multifidelity_data/DataSet.zip')
    p.add_argument('--download', action='store_true')
    p.add_argument('--output', type=Path)
    args = p.parse_args()
    if args.download:
        with urllib.request.urlopen(URL, timeout=60) as response:
            raw = response.read()
        if len(raw) != 248015 or hashlib.sha256(raw).hexdigest() != SHA256:
            raise ValueError('Downloaded bytes do not match pinned source')
        args.archive.parent.mkdir(parents=True, exist_ok=True)
        args.archive.write_bytes(raw)
    result = inspect(args.archive)
    if args.output:
        args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: result['combined'][k] for k in
                      ['rows', 'unique_encoded_inputs', 'conflicting_exact_input_groups',
                       'groups_with_distinct_fidelity_values', 'zero_charge_penalty_rows']}, indent=2))


if __name__ == '__main__':
    main()
