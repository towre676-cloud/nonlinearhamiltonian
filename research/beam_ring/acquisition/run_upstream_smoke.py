"""Replay pinned official demo and our finite-table adapter on the real Engine.

Upstream source is not redistributed. Supply an independently obtained checkout
at the recorded commit. This is framework integration, not a DAMA result.
"""
from pathlib import Path
import argparse
import contextlib
import io
import json
import os
import subprocess
import sys
import time

import numpy as np

from engine_adapter import (FiniteTableAlgorithm, FiniteTableOracle, UPSTREAM_COMMIT,
                            load_upstream)
from finite_meanbax import FiniteMeanBAX, SurvivalMLP, feature_table


def synthetic_query(design, launch):
    # Explicitly synthetic scope. The physical oracle is integrated by root.
    return 1.0 if launch <= 3 + design else .25


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--upstream-dir', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    Engine = load_upstream(args.upstream_dir)
    env = {**os.environ, 'PYTHONPATH': str(args.upstream_dir.resolve()),
           'OPENBLAS_NUM_THREADS': '1', 'OMP_NUM_THREADS': '1'}
    start = time.perf_counter()
    original = subprocess.run([sys.executable,
        str(args.upstream_dir.resolve() / 'examples/01_basic_optimization.py')],
        cwd=output, env=env, text=True, capture_output=True, check=True, timeout=60)
    official_seconds = time.perf_counter() - start
    (output / 'official_demo.stdout.log').write_text(original.stdout)
    (output / 'official_demo.stderr.log').write_text(original.stderr)
    if 'quadratic: 60 total evaluations' not in original.stdout:
        raise ValueError('official demo did not reach recorded 60 evaluations')

    features = feature_table([[0.], [.5], [1.]], np.linspace(0, 1, 9).reshape(-1, 1))
    table = FiniteTableOracle(features, synthetic_query, seed=9)
    policy = FiniteMeanBAX([np.ones(9) / 9], thresholds=[.75],
                         boundary_ranges=[(.4, .75)], batch_size=3, seed=9)
    config = {'seed': 9, 'max_loops': 3,
        'checkpoint': {'dir': str(output / 'adapter_checkpoints'), 'freq': 1},
        'oracles': [{'name': 'synthetic_survival', 'input_dim': 2, 'n_initial': 8,
            'function': {'class': table},
            'generate': {'class': table.generate, 'params': {'n': 8, 'd': 2}},
            'model': {'class': SurvivalMLP,
                      'params': {'seed': 9, 'hidden_layer_sizes': (8,), 'max_iter': 100}}}],
        'algorithm': {'class': FiniteTableAlgorithm, 'params': {'tables': [table], 'policy': policy}}}
    log = io.StringIO(); start = time.perf_counter()
    with contextlib.redirect_stdout(log):
        engine = Engine(config)
        engine.run()
    adapter_seconds = time.perf_counter() - start
    (output / 'adapter.stdout.log').write_text(log.getvalue())
    physical = table.cost_receipt()
    if engine.evaluators[0].get_eval_count() != physical['successful_physics_rows']:
        raise ValueError('engine and physics adapter counts disagree')
    if physical['cache_hits'] or physical['failed_physics_rows'] or physical['successful_physics_rows'] != 14:
        raise ValueError('unexpected adapter query accounting')
    receipt = {'status': 'passed', 'upstream_commit': UPSTREAM_COMMIT,
        'upstream_code_changed': False, 'source_files_hash_checked': 10,
        'official_demo': {'returncode': original.returncode, 'oracle_evaluations': 60,
            'wall_seconds': official_seconds, 'algorithm': 'upstream GreedySampling with DummyModel'},
        'finite_table_adapter': {'engine': 'unchanged upstream mpbax.core.engine.Engine',
            'wall_seconds': adapter_seconds, 'physical_cost': physical,
            'last_selection': policy.last_selection, 'model_fit': engine.models[0].fit_receipt},
        'scope': 'Synthetic framework/protocol integration only; no physical optimizer gain or DAMA-BAX reproduction.'}
    (output / 'UPSTREAM_REPLAY.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
