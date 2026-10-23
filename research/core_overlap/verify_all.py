#!/usr/bin/env python3
"""Replay every overlap checker in an isolated temporary copy.

No optional numerical or symbolic package is needed. Stored receipts are not
silently rewritten. Use --output PATH for a new integrated receipt.
"""
from pathlib import Path
import argparse
import json
import shutil
import subprocess
import sys
import tempfile
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CHECKERS = ['cubic_affine_completeness.py', 'cubic_phase_audit.py',
            'cubic_phase_classification.py', 'higher_restoring.py',
            'cubic_restoring.py', 'cubic_deformation.py',
            'restoring_deformation.py', 'phase_independent_review.py',
            'audit_balanced.py', 'pure_transverse.py', 'pure_quadratic_composition.py',
            'analytic_shear_square.py', 'audit_sector_dynamics.py',
            'shear_composition_complete.py', 'shear_oscillator.py',
            'analytic_potential_classification.py', 'quadratic_frontier.py',
            'quadratic_shear_residual.py', 'affine_shear_potentials.py',
            'constant_quadratic_classification.py',
            'deformation_obstructions.py', 'extension_proof_review.py',
            'audit_balanced_transverse.py', 'audit_composition_recognize.py',
            'depth_verify.py', 'analytic_bridge_check.py', 'canonical_verify.py',
            'review_checks.py', 'integration_verify.py', 'pure_tests.py']


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output', type=Path)
    args = ap.parse_args()
    rows = []
    started = time.monotonic()
    with tempfile.TemporaryDirectory(prefix='core-overlap-replay-') as tmp:
        target = Path(tmp)
        shutil.copytree(HERE, target/'research/core_overlap',
                        ignore=shutil.ignore_patterns('__pycache__', 'output', '*.pdf'))
        shutil.copytree(ROOT/'extensions', target/'extensions',
                        ignore=shutil.ignore_patterns('__pycache__'))
        for checker in CHECKERS:
            tick = time.monotonic()
            result = subprocess.run([sys.executable, '-B', '-S',
                                     str(target/'research/core_overlap'/checker)],
                                    cwd=target, capture_output=True, text=True)
            row = {'checker': checker, 'status': 'passed' if result.returncode == 0 else 'failed',
                   'seconds': round(time.monotonic()-tick, 3)}
            if result.returncode:
                row['output'] = (result.stdout+result.stderr)[-5000:]
            rows.append(row)
        for label, script in (('retained triangular identities', 'check_triangular.py'),
                              ('retained cubic gauge identities', 'check_cubic_phase.py')):
            tick = time.monotonic()
            result = subprocess.run([sys.executable, '-B', '-S',
                                     str(target/'extensions/hamiltonian'/script)],
                                    cwd=target, capture_output=True, text=True)
            rows.append({'checker': label,
                         'status': 'passed' if result.returncode == 0 else 'failed',
                         'seconds': round(time.monotonic()-tick, 3),
                         'summary': (result.stdout+result.stderr)[-3000:]})
        tick = time.monotonic()
        result = subprocess.run([sys.executable, '-B', '-S', '-m', 'unittest', 'test_two_root'],
                                cwd=target/'extensions/hamiltonian', capture_output=True, text=True)
        rows.append({'checker': 'integrated two-root regression suite',
                     'status': 'passed' if result.returncode == 0 else 'failed',
                     'seconds': round(time.monotonic()-tick, 3),
                     'summary': (result.stdout+result.stderr)[-3000:]})
    result = {'status': 'passed' if all(r['status']=='passed' for r in rows) else 'failed',
              'initial_review_commit': 'e91e14da9d59e799ad9ed0331f59b2b500e478e8',
              'base_commit': '35d39be4add03444b49b03fda5324c8fe83a040f',
              'review_branch_base_commit': 'e6ef82d15f63b6addfe380362da539dca9cdde39',
              'extension_base_commit': '4050dbfc484641c2ce8a8ab9a272e91ca4934f55',
              'seconds': round(time.monotonic()-started, 3), 'checks': rows,
              'scope': 'Exact independent identities and finite sanity checks; universal claims rest on written proofs and internal review, historical priority unestablished.'}
    if args.output:
        args.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))
    return 0 if result['status']=='passed' else 1


if __name__ == '__main__':
    raise SystemExit(main())
