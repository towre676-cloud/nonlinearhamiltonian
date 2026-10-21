#!/usr/bin/env python3
"""Run every extension test suite and seed check; replay every envelope in results/.

Emits one JSON report. Exit status 0 only if everything passed.
Usage: python3 -B extensions/run_all.py [--skip-results] [--quick]
  --quick skips the slow Weyl discovery suite (about a minute) and results replay.
"""
from __future__ import annotations
import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

SUITES = [
    ('O1 observer v2', 'observer', 'test_observer'),
    ('O2 noise-aware panels', 'observer', 'test_panels'),
    ('O3 adaptive Bellman', 'observer', 'test_adaptive'),
    ('W1 Weyl discovery and kernels', 'hamiltonian', 'test_weyl_discovery'),
    ('W2 six-parameter top reduction', 'hamiltonian', 'test_top_reduction'),
    ('S0 contraction seed', 'structure', 'test_contraction_seed'),
    ('S1 obstruction interface', 'structure', 'test_obstruction'),
    ('S2 DGLA lifting', 'structure', 'test_dgla'),
    ('S3 integer Smith cohomology', 'structure', 'test_smith'),
    ('A1 Pell orbits', 'arithmetic', 'test_pell'),
    ('A2 fundamental units', 'arithmetic', 'test_units'),
    ('C0 envelopes', '.', 'test_envelope'),
]
SEEDS = [
    ('seed observer reference (26 checks)', ['extensions/observer/observation_closure_reference.py', 'verify']),
    ('seed Weyl receipts vs baseline star engine',
     ['extensions/hamiltonian/weyl_receipts.py', '--self-test', '--existing-engine',
      'research/hamiltonian/independent/engine.py', '--check', 'extensions/hamiltonian/q_cubed_receipt.json']),
    ('seed counterexamples', ['extensions/counterexamples.py']),
]


def run(cmd, cwd):
    t = time.time()
    p = subprocess.run([sys.executable, '-B'] + cmd, cwd=cwd, capture_output=True, text=True)
    return p.returncode, (p.stdout + p.stderr)[-3000:], round(time.time() - t, 1)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--skip-results', action='store_true')
    ap.add_argument('--quick', action='store_true')
    a = ap.parse_args()
    report = {'status': 'passed', 'suites': [], 'seeds': [], 'results': []}
    for name, sub, mod in SUITES:
        if a.quick and mod in ('test_weyl_discovery', 'test_top_reduction'):
            report['suites'].append({'name': name, 'status': 'skipped (quick)'})
            continue
        code, out, sec = run(['-m', 'unittest', mod], HERE / sub)
        tail = [l for l in out.splitlines() if l.startswith('Ran ') or l in ('OK',) or l.startswith('FAILED')]
        report['suites'].append({'name': name, 'status': 'passed' if code == 0 else 'failed', 'seconds': sec,
                                 'summary': ' '.join(tail), **({'output': out} if code else {})})
    for name, cmd in SEEDS:
        code, out, sec = run(cmd, ROOT)
        report['seeds'].append({'name': name, 'status': 'passed' if code == 0 else 'failed', 'seconds': sec,
                                **({'output': out} if code else {})})
    if not (a.skip_results or a.quick):
        idx = json.loads((ROOT / 'results/RECEIPTS.json').read_text())['results']
        for r in idx:
            code, out, sec = run(['extensions/envelope.py', 'check', r['file']], ROOT)
            report['results'].append({'file': r['file'], 'status': 'passed' if code == 0 else 'failed',
                                      'seconds': sec, **({'output': out} if code else {})})
    groups = report['suites'] + report['seeds'] + report['results']
    if any(g['status'] == 'failed' for g in groups):
        report['status'] = 'failed'
    print(json.dumps(report, indent=1))
    sys.exit(0 if report['status'] == 'passed' else 1)


if __name__ == '__main__':
    main()
