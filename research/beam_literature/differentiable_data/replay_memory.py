"""Verify ingested public data and fit a descriptive memory model.

This simple OLS is deliberately distinct from the authors' robust regression.
It does not remeasure a simulator or establish an accelerator speedup.
"""
from pathlib import Path
import csv
import hashlib
import json
import numpy as np

HERE = Path(__file__).resolve().parent


def main():
    sources = json.loads((HERE / 'sources.json').read_text())
    source = next(s for s in sources if s['resolved_record'] == 17822326)
    files = {f['key']: f for f in source['files']}
    for name in ('analyzed_data.csv', 'memory_data.csv'):
        content = (HERE / name).read_bytes()
        expected = files[name]
        assert len(content) == expected['size']
        assert 'md5:' + hashlib.md5(content).hexdigest() == expected['checksum']
        assert hashlib.sha256(content).hexdigest() == expected['downloaded_sha256']
    rows = list(csv.DictReader((HERE / 'memory_data.csv').open()))
    rows = [row for row in rows if row['differentiable'] == 'True']
    matrix = np.array([[1.0, float(row['n_parts']), float(row['n_grid']) ** 3] for row in rows])
    memory = np.array([float(row['total']) for row in rows])
    coefficients, _, rank, _ = np.linalg.lstsq(matrix, memory, rcond=None)
    assert rank == 3
    relative_residual = float(np.linalg.norm(matrix @ coefficients - memory) / np.linalg.norm(memory))
    assert 0 < relative_residual < 0.01
    result = {
        'status': 'passed_data_ingestion_and_descriptive_fit',
        'source_version': 17822326,
        'rows': len(rows),
        'model': 'total_bytes = intercept + alpha_particle*N + alpha_cell*n_grid**3',
        'ordinary_least_squares_coefficients': coefficients.tolist(),
        'relative_residual': relative_residual,
        'particle_range': [min(int(row['n_parts']) for row in rows), max(int(row['n_parts']) for row in rows)],
        'grid_side_range': [min(int(row['n_grid']) for row in rows), max(int(row['n_grid']) for row in rows)],
        'scope': 'public recorded memory measurements; no simulator execution, optimizer timing or physical certificate',
    }
    (HERE / 'memory_replay.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
