"""Our adapters for the unchanged, separately obtained upstream mpBAX Engine.

The upstream framework is generic. Using it is not a reproduction of the DAMA
paper's acquisition strategy. The finite-table policy is in finite_meanbax.py.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys
import time

import numpy as np

try:
    from .finite_meanbax import FiniteMeanBAX
except ImportError:
    from finite_meanbax import FiniteMeanBAX


UPSTREAM_COMMIT = '82766c7fb22ec675025d6485ce11761cdc7a6056'


def load_upstream(source_dir):
    """Check selected pinned upstream files, then import its actual Engine."""
    source_dir = Path(source_dir).resolve()
    manifest = json.loads(Path(__file__).with_name('UPSTREAM_SOURCE.json').read_text())
    if manifest['commit'] != UPSTREAM_COMMIT:
        raise ValueError('unexpected upstream source pin')
    for row in manifest['files']:
        data = (source_dir / row['path']).read_bytes()
        blob = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        if blob != row['git_blob_sha'] or hashlib.sha256(data).hexdigest() != row['sha256']:
            raise ValueError('upstream source mismatch: ' + row['path'])
    # Refuse silent reuse of an earlier different source checkout.
    loaded = sys.modules.get('mpbax')
    if loaded is not None and Path(loaded.__file__).resolve().parent != source_dir / 'mpbax':
        raise ValueError('different mpbax checkout already imported')
    sys.path.insert(0, str(source_dir))
    from mpbax.core.engine import Engine
    return Engine


class FiniteTableOracle:
    """mpBAX X->Y adapter around a fixed physical query table.

    feature_grid has shape (design, launch, feature); query(design, launch)
    returns a normalized survival fraction. Duplicate queries are served from
    this adapter's cache and explicitly counted. Failed calls remain charged
    attempts and never set the observed mask. Validation uses a separate object.
    """
    def __init__(self, feature_grid, query, phase='learning', seed=42):
        features = np.asarray(feature_grid, dtype=float)
        if features.ndim != 3 or not np.all(np.isfinite(features)) or min(features.shape) < 1:
            raise ValueError('nonempty finite (design,launch,feature) table required')
        if not callable(query) or phase not in ('learning', 'validation'):
            raise ValueError('callable query and declared phase required')
        self.features = features.copy()
        self.query = query
        self.phase = phase
        self.rng = np.random.default_rng(seed)
        self.observed = np.zeros(features.shape[:2], dtype=bool)
        self.values = np.full(features.shape[:2], np.nan)
        self.events = []
        self._lookup = {}
        for d in range(features.shape[0]):
            for j in range(features.shape[1]):
                key = tuple(features[d, j])
                if key in self._lookup:
                    raise ValueError('feature rows must uniquely identify a physical query')
                self._lookup[key] = (d, j)

    def __call__(self, X):
        X = np.asarray(X, dtype=float)
        if X.ndim != 2 or X.shape[1] != self.features.shape[2] or not np.all(np.isfinite(X)):
            raise ValueError('finite (point,feature) rows required')
        indices = []
        for row in X:
            try:
                indices.append(self._lookup[tuple(row)])
            except KeyError as exc:
                raise ValueError('query is outside frozen finite feature table') from exc
        values = []
        for d, j in indices:
            if self.observed[d, j]:
                values.append(self.values[d, j])
                self.events.append({'design': d, 'launch': j, 'phase': self.phase,
                                    'status': 'cache_hit', 'physics_seconds': 0.0})
                continue
            start = time.perf_counter()
            event = {'design': d, 'launch': j, 'phase': self.phase, 'status': 'failed'}
            try:
                value = float(self.query(d, j))
                if not np.isfinite(value) or not 0 <= value <= 1:
                    raise ValueError('physical callback must return normalized survival in [0,1]')
                self.values[d, j] = value
                self.observed[d, j] = True
                event['status'] = 'acquired'
                values.append(value)
            except Exception as exc:
                event['error'] = type(exc).__name__ + ': ' + str(exc)
                raise
            finally:
                event['physics_seconds'] = time.perf_counter() - start
                self.events.append(event)
        return np.array(values, dtype=float).reshape(-1, 1)

    def generate(self, n, d=None):
        """Upstream custom initial-data generator, without replacement."""
        if d is not None and d != self.features.shape[2]:
            raise ValueError('feature dimension mismatch')
        available = np.argwhere(~self.observed)
        if not isinstance(n, int) or n < 0 or n > len(available):
            raise ValueError('initial count exceeds unobserved table')
        chosen = available[self.rng.choice(len(available), n, replace=False)]
        return np.array([self.features[i, j] for i, j in chosen], dtype=float).reshape(n, self.features.shape[2])

    def cost_receipt(self):
        return {'phase': self.phase, 'requested_rows': len(self.events),
            'successful_physics_rows': sum(e['status'] == 'acquired' for e in self.events),
            'failed_physics_rows': sum(e['status'] == 'failed' for e in self.events),
            'cache_hits': sum(e['status'] == 'cache_hit' for e in self.events),
            'physics_seconds': sum(e['physics_seconds'] for e in self.events)}


class FiniteTableAlgorithm:
    """Upstream Engine protocol bridge; delegates acquisition to FiniteMeanBAX."""
    def __init__(self, tables, policy):
        if not tables or not isinstance(policy, FiniteMeanBAX):
            raise ValueError('table adapters and FiniteMeanBAX policy required')
        if any(t.phase != 'learning' for t in tables):
            raise ValueError('validation oracle cannot enter learning acquisition')
        self.tables = tables
        self.policy = policy

    def propose(self, fn_pred_list):
        if len(fn_pred_list) != len(self.tables):
            raise ValueError('one predictor per oracle required')
        predictions = []
        for fn, table in zip(fn_pred_list, self.tables):
            features = table.features
            pred = np.asarray(fn(features.reshape(-1, features.shape[2])))
            if pred.shape != (features.shape[0] * features.shape[1], 1):
                raise ValueError('one survival-fraction prediction per point required')
            predictions.append(pred[:, 0].reshape(features.shape[:2]))
        queries = self.policy.select(predictions, [t.observed for t in self.tables])
        return [np.array([table.features[d, j] for k, d, j in queries if k == i], dtype=float)
                .reshape(-1, table.features.shape[2]) for i, table in enumerate(self.tables)]
