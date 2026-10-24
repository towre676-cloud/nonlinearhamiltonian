"""Verify the pinned source subset, then replay two examples in a fresh directory."""
from pathlib import Path
import argparse
import hashlib
import json
import math
import os
import shutil
import subprocess
import sys
import time


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True,
                        help='New directory to create; existing paths are rejected.')
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    manifest = json.loads((here / 'source_manifest.json').read_text())
    for entry in manifest['files']:
        data = (here / 'source' / entry['path']).read_bytes()
        git_sha = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        if git_sha != entry['git_blob_sha'] or hashlib.sha256(data).hexdigest() != entry['sha256']:
            raise ValueError(f"Source identity mismatch: {entry['path']}")
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    work = output / 'source'
    shutil.copytree(here / 'source', work)
    env = os.environ.copy()
    for key in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS',
                'VECLIB_MAXIMUM_THREADS', 'NUMEXPR_NUM_THREADS'):
        env[key] = '1'
    env.update(PYTHONPATH=str(work / 'src'), MPLBACKEND='Agg',
               MPLCONFIGDIR=str(output / 'matplotlib_cache'))
    receipt = {'pinned_commit': manifest['commit'], 'acceptance_threshold': 1e-12,
               'source_hashes_verified': True, 'replays': []}
    for name in ('fig10_nilpotent_phase', 'fig8_beyond_gaussian'):
        command = [sys.executable, f'experiments/{name}/run.py']
        started = time.perf_counter()
        process = subprocess.run(command, cwd=work, env=env, text=True,
                                 capture_output=True, timeout=120)
        elapsed = time.perf_counter() - started
        (output / f'{name}.stdout.log').write_text(process.stdout)
        (output / f'{name}.stderr.log').write_text(process.stderr)
        process.check_returncode()
        result = json.loads((work / 'experiments' / name / 'results.json').read_text())
        if name.startswith('fig10'):
            metrics = {f'{part}.{key}': result[part][key]
                       for part in ('single_mode', 'two_mode')
                       for key in ('max_module_grid_error', 'max_grid_refinement_gap')}
        else:
            metrics = {key: result[key] for key in ('hom_max_analytic_error',
                       'hom_max_fock_error', 'random_interferometer_max_fock_error')}
        passed = all(math.isfinite(v) and 0 <= v < 1e-12 for v in metrics.values())
        receipt['replays'].append({'experiment': name, 'command': command,
            'returncode': process.returncode, 'wall_seconds': elapsed,
            'metrics': metrics, 'numerical_acceptance_passed': passed, 'result': result})
        (output / 'replay_receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
        if not passed:
            raise ValueError(f'Numerical acceptance failed: {name}')
        print(f'{name}: passed ({elapsed:.3f} s)')
    receipt['all_passed'] = True
    (output / 'replay_receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')


if __name__ == '__main__':
    main()
