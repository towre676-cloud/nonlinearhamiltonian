"""Finite-candidate deterministic MeanBAX pilot, not the SSRL-X reproduction.

Implements the published DAMA heuristic's essential selection steps: score
surrogate maps, retain predicted Pareto designs, randomly query predicted
boundary points. A declared finite design table replaces NSGA-II. Neither
surrogate output nor this selector is a safety certificate.
"""
from __future__ import annotations

import time
import warnings
from collections import deque

import numpy as np


def pareto_indices(values):
    """All nondominated rows for maximization; retain equal objective vectors."""
    values = np.asarray(values, dtype=float)
    if values.ndim != 2 or not np.all(np.isfinite(values)):
        raise ValueError('finite (design, objective) values required')
    return np.array([i for i, row in enumerate(values)
                     if not np.any(np.all(values >= row, axis=1)
                                   & np.any(values > row, axis=1))], dtype=int)


def connected_weighted_score(labels, weights, adjacency, origin):
    """Weighted component containing origin; a lost origin gives zero score."""
    labels = np.asarray(labels)
    weights = np.asarray(weights, dtype=float)
    if labels.ndim != 1 or labels.dtype.kind != 'b':
        raise ValueError('one-dimensional boolean labels required')
    if weights.shape != labels.shape or not np.all(np.isfinite(weights)) or np.any(weights < 0):
        raise ValueError('matching finite nonnegative weights required')
    if len(adjacency) != len(labels) or not 0 <= origin < len(labels):
        raise ValueError('invalid graph/origin')
    for i, neighbors in enumerate(adjacency):
        if any(not isinstance(j, (int, np.integer)) or not 0 <= j < len(labels)
               or i not in adjacency[j] for j in neighbors):
            raise ValueError('undirected graph with valid indices required')
    if not labels[origin]:
        return 0.0
    seen = {int(origin)}
    queue = deque(seen)
    while queue:
        for j in adjacency[queue.popleft()]:
            if labels[j] and j not in seen:
                seen.add(int(j)); queue.append(int(j))
    return float(weights[list(seen)].sum())


class FiniteMeanBAX:
    """Point acquisition from a frozen finite table of design/launch inputs.

    predictions[k] and observed[k] have shape (n_designs, n_launches_k).
    objective_callbacks[k], when provided, maps a boolean launch row to its
    declared objective, e.g. the weighted origin-connected component. Only the
    observed MASK is accepted: truth labels must remain outside acquisition.
    """
    def __init__(self, weights, batch_size=24, seed=42, thresholds=(.75, .94),
                 boundary_ranges=((.4, .75), (.85, .95)), max_designs=300,
                 objective_callbacks=None):
        self.weights = [np.asarray(w, dtype=float) for w in weights]
        if not self.weights or any(w.ndim != 1 or not len(w) or
                not np.all(np.isfinite(w)) or np.any(w < 0) for w in self.weights):
            raise ValueError('nonempty finite nonnegative weight vectors required')
        if len(thresholds) != len(weights) or len(boundary_ranges) != len(weights):
            raise ValueError('one threshold and boundary interval per objective')
        if not isinstance(batch_size, int) or batch_size < 1 or not isinstance(max_designs, int) or max_designs < 1:
            raise ValueError('positive integer batch_size and max_designs required')
        self.thresholds = tuple(float(x) for x in thresholds)
        self.boundary_ranges = tuple(tuple(float(x) for x in r) for r in boundary_ranges)
        if any(not 0 <= x <= 1 for x in self.thresholds) or any(
                len(r) != 2 or not 0 <= r[0] <= r[1] <= 1 for r in self.boundary_ranges):
            raise ValueError('thresholds/boundaries must lie in [0,1]')
        if objective_callbacks is not None and (len(objective_callbacks) != len(weights)
                or any(not callable(fn) for fn in objective_callbacks)):
            raise ValueError('one callable per objective required')
        self.objective_callbacks = objective_callbacks
        self.batch_size = batch_size
        self.max_designs = max_designs
        self.rng = np.random.default_rng(seed)
        self.last_selection = None

    def _validate(self, predictions, observed=None):
        if len(predictions) != len(self.weights):
            raise ValueError('one prediction table per objective required')
        predictions = [np.asarray(p, dtype=float) for p in predictions]
        n = predictions[0].shape[0] if predictions[0].ndim == 2 else 0
        if n == 0 or any(p.shape != (n, len(w)) or not np.all(np.isfinite(p))
                or np.any(p < 0) or np.any(p > 1) for p, w in zip(predictions, self.weights)):
            raise ValueError('finite matching survival predictions in [0,1] required')
        if observed is not None:
            if len(observed) != len(predictions):
                raise ValueError('one observed mask per objective required')
            observed = [np.asarray(o) for o in observed]
            if any(o.shape != p.shape or o.dtype.kind != 'b' for o, p in zip(observed, predictions)):
                raise ValueError('boolean observed masks must match predictions')
        return predictions, observed

    def estimates(self, predictions):
        predictions, _ = self._validate(predictions)
        columns = []
        for k, p in enumerate(predictions):
            labels = p >= self.thresholds[k]
            if self.objective_callbacks is None:
                columns.append(labels @ self.weights[k])
            else:
                values = np.array([self.objective_callbacks[k](row) for row in labels], dtype=float)
                if not np.all(np.isfinite(values)):
                    raise ValueError('objective callback returned nonfinite score')
                columns.append(values)
        return np.column_stack(columns)

    def select(self, predictions, observed):
        started = time.perf_counter()
        predictions, observed = self._validate(predictions, observed)
        estimates = self.estimates(predictions)
        pareto = pareto_indices(estimates)
        chosen_designs = pareto if len(pareto) <= self.max_designs else np.sort(
            self.rng.choice(pareto, self.max_designs, replace=False))
        candidates = []
        for k, p in enumerate(predictions):
            lo, hi = self.boundary_ranges[k]
            for d in chosen_designs:
                candidates.extend((k, int(d), int(j)) for j in np.flatnonzero(
                    (~observed[k][d]) & (p[d] >= lo) & (p[d] <= hi)))
        reason = 'predicted_pareto_boundary'
        if not candidates:
            reason = 'boundary_empty_uniform_unobserved_fallback'
            candidates = [(k, int(d), int(j)) for k, o in enumerate(observed)
                          for d, j in zip(*np.nonzero(~o))]
        count = min(self.batch_size, len(candidates))
        selected = [candidates[i] for i in self.rng.choice(len(candidates), count, replace=False)]
        self.last_selection = {'reason': reason, 'predicted_objectives': estimates.tolist(),
            'predicted_pareto_designs': pareto.tolist(), 'selected_designs': chosen_designs.tolist(),
            'candidate_points': len(candidates), 'selected_queries': [list(q) for q in selected],
            'selection_seconds': time.perf_counter() - started,
            'scope': 'Heuristic acquisition only; predictions never become truth labels.'}
        return selected


class SurvivalMLP:
    """Small CPU surrogate; deliberately different from the paper neural field.

    Refit all observed survival fractions using sklearn's L-BFGS MLP. Outputs
    are clipped to [0,1], not calibrated survival probabilities. Diagnostics
    preserve nonconvergence warnings. No pickled weights are downloaded.
    """
    def __init__(self, input_dim=None, seed=42, hidden_layer_sizes=(32, 32), max_iter=150):
        self.input_dim = input_dim
        self.seed = seed
        self.hidden_layer_sizes = tuple(hidden_layer_sizes)
        self.max_iter = max_iter
        self.model = None
        self.fit_receipt = None

    def fit(self, X, Y):
        from sklearn.exceptions import ConvergenceWarning
        from sklearn.neural_network import MLPRegressor
        X = np.asarray(X, dtype=float); Y = np.asarray(Y, dtype=float)
        if Y.ndim == 2 and Y.shape[1] == 1:
            Y = Y[:, 0]
        if X.ndim != 2 or not len(X) or Y.shape != (len(X),) or not np.all(np.isfinite(X)) \
                or not np.all(np.isfinite(Y)) or np.any(Y < 0) or np.any(Y > 1):
            raise ValueError('finite feature rows and matching normalized survival targets required')
        if self.input_dim is not None and X.shape[1] != self.input_dim:
            raise ValueError('feature dimension mismatch')
        self.input_dim = X.shape[1]
        self.model = MLPRegressor(hidden_layer_sizes=self.hidden_layer_sizes, solver='lbfgs',
            random_state=self.seed, max_iter=self.max_iter, tol=1e-6, alpha=1e-3)
        start = time.perf_counter()
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter('always', ConvergenceWarning)
            self.model.fit(X, Y)
        self.fit_receipt = {'training_seconds': time.perf_counter() - start, 'rows': len(X),
            'features': self.input_dim, 'iterations': int(self.model.n_iter_),
            'warnings': [str(w.message) for w in caught], 'loss': float(self.model.loss_),
            'implementation': 'sklearn MLPRegressor, L-BFGS, clipped regression'}
        return self

    def train(self, X, Y, metadata=None):
        self.fit(X, Y)

    def predict(self, X):
        X = np.asarray(X, dtype=float)
        if self.model is None:
            raise RuntimeError('fit before predict')
        if X.ndim != 2 or X.shape[1] != self.input_dim or not np.all(np.isfinite(X)):
            raise ValueError('finite feature rows with matching dimension required')
        return np.clip(self.model.predict(X), 0, 1).reshape(-1, 1)

    def save(self, filepath):
        # Engine compatibility for locally generated models only. Do not load
        # checkpoints from untrusted sources.
        import pickle
        from pathlib import Path
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'wb') as handle:
            pickle.dump(self, handle)

    def get_best_model_snapshot(self):
        return None


def feature_table(design_features, launch_features):
    """Return (design, launch, concatenated_feature) table in stable order."""
    designs = np.asarray(design_features, dtype=float)
    launches = np.asarray(launch_features, dtype=float)
    if designs.ndim != 2 or launches.ndim != 2 or not np.all(np.isfinite(designs)) \
            or not np.all(np.isfinite(launches)):
        raise ValueError('finite two-dimensional feature arrays required')
    return np.concatenate([np.broadcast_to(designs[:, None, :], (len(designs), len(launches), designs.shape[1])),
        np.broadcast_to(launches[None, :, :], (len(designs), len(launches), launches.shape[1]))], axis=2)
