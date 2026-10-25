"""Behavioral tests for acquisition scope, leakage guards and accounting."""
import unittest

import numpy as np

from finite_meanbax import (FiniteMeanBAX, SurvivalMLP, connected_weighted_score,
                           feature_table, pareto_indices)
from engine_adapter import FiniteTableAlgorithm, FiniteTableOracle


class SelectionTests(unittest.TestCase):
    def test_true_pareto_rule_retains_ties_and_tradeoffs(self):
        self.assertEqual(pareto_indices([[1, 0], [0, 1], [.5, .5], [.4, .4], [1, 0]]).tolist(), [0, 1, 2, 4])

    def test_connected_score_preserves_holes_and_excludes_island(self):
        graph = [[1], [0, 2], [1, 3], [2]]
        self.assertEqual(connected_weighted_score(np.array([1, 1, 0, 1], dtype=bool),
                                                np.ones(4), graph, 0), 2.)
        self.assertEqual(connected_weighted_score(np.array([0, 1, 1, 1], dtype=bool),
                                                np.ones(4), graph, 0), 0.)

    def test_boundary_queries_are_unseen_and_only_from_pareto_designs(self):
        p = [np.array([[.9, .6, .1], [.1, .6, .1]]),
             np.array([[.99, .9, .2], [.1, .9, .1]])]
        observed = [np.zeros((2, 3), dtype=bool), np.zeros((2, 3), dtype=bool)]
        observed[0][0, 1] = True
        policy = FiniteMeanBAX([np.ones(3), np.ones(3)], batch_size=4, seed=3)
        result = policy.select(p, observed)
        self.assertEqual(result, [(1, 0, 1)])
        self.assertEqual(policy.last_selection['predicted_pareto_designs'], [0])

    def test_empty_boundary_fallback_without_replacement_and_exhaustion(self):
        policy = FiniteMeanBAX([np.ones(3)], thresholds=[.75], boundary_ranges=[(.4, .75)], batch_size=50)
        p = [np.ones((2, 3))]; seen = [np.array([[True, False, False], [False, True, False]])]
        result = policy.select(p, seen)
        self.assertEqual(len(result), 4)
        self.assertEqual(len(set(result)), 4)
        self.assertTrue(all(not seen[k][d, j] for k, d, j in result))
        self.assertEqual(policy.select(p, [np.ones((2, 3), dtype=bool)]), [])

    def test_objective_callbacks_change_selected_design(self):
        graph = [[1], [0, 2], [1, 3], [2]]
        # First design has more surviving cells, but the origin is lost.
        p = [np.array([[.1, .9, .9, .9], [.9, .9, .1, .1]])]
        policy = FiniteMeanBAX([np.ones(4)], thresholds=[.75], boundary_ranges=[(.4, .75)],
            objective_callbacks=[lambda row: connected_weighted_score(row, np.ones(4), graph, 0)])
        self.assertEqual(policy.estimates(p).ravel().tolist(), [0, 2])

    def test_nonfinite_out_of_range_and_truth_masks_rejected(self):
        policy = FiniteMeanBAX([np.ones(2)], thresholds=[.75], boundary_ranges=[(.4, .75)])
        for row in [[[np.nan, .5]], [[1.1, .5]], [[-.01, .5]]]:
            with self.assertRaises(ValueError): policy.select([row], [np.zeros((1, 2), dtype=bool)])
        with self.assertRaises(ValueError): policy.select([np.ones((1, 2))], [np.zeros((1, 2), dtype=int)])
        with self.assertRaises(ValueError): FiniteMeanBAX([np.array([-1.])], thresholds=[.75], boundary_ranges=[(.4, .75)])


class AdapterTests(unittest.TestCase):
    def setUp(self):
        self.features = feature_table([[0], [1]], [[0], [.5], [1]])

    def test_cache_is_separate_from_physical_calls(self):
        calls = []
        table = FiniteTableOracle(self.features, lambda d, j: calls.append((d, j)) or .8)
        result = table(np.array([self.features[0, 1], self.features[0, 1], self.features[1, 2]]))
        self.assertTrue(np.all(result == .8))
        self.assertEqual(calls, [(0, 1), (1, 2)])
        self.assertEqual(table.cost_receipt()['cache_hits'], 1)
        self.assertEqual(table.cost_receipt()['successful_physics_rows'], 2)

    def test_failed_queries_are_charged_and_not_observed(self):
        def fail(d, j): raise RuntimeError('injected physical failure')
        table = FiniteTableOracle(self.features, fail)
        with self.assertRaises(RuntimeError): table(self.features[0, :1])
        self.assertFalse(table.observed.any())
        self.assertEqual(table.cost_receipt()['failed_physics_rows'], 1)

    def test_domain_and_duplicate_feature_rejection(self):
        table = FiniteTableOracle(self.features, lambda d, j: 1.)
        with self.assertRaises(ValueError): table([[.1, .2]])
        with self.assertRaises(ValueError): FiniteTableOracle(np.zeros((2, 2, 2)), lambda d, j: 1.)
        self.assertEqual(len(table.events), 0)

    def test_validation_oracle_cannot_enter_learning(self):
        table = FiniteTableOracle(self.features, lambda d, j: 1., phase='validation')
        policy = FiniteMeanBAX([np.ones(3)], thresholds=[.75], boundary_ranges=[(.4, .75)])
        with self.assertRaises(ValueError): FiniteTableAlgorithm([table], policy)

    def test_engine_protocol_maps_indices_back_to_features(self):
        table = FiniteTableOracle(self.features, lambda d, j: 1.)
        policy = FiniteMeanBAX([np.ones(3)], thresholds=[.75], boundary_ranges=[(.4, .75)], batch_size=2)
        algorithm = FiniteTableAlgorithm([table], policy)
        rows = algorithm.propose([lambda x: np.full((len(x), 1), .5)])
        self.assertEqual(rows[0].shape, (2, 2))
        self.assertTrue(np.all(table(rows[0]) == 1))

    def test_mlp_uses_only_supplied_rows_and_bounded_regression(self):
        X = np.linspace(0, 1, 20).reshape(-1, 1)
        model = SurvivalMLP(seed=7, hidden_layer_sizes=(8,), max_iter=200).fit(X, X[:, 0])
        y = model.predict(X)
        self.assertLess(float(np.max(np.abs(y[:, 0] - X[:, 0]))), .08)
        self.assertEqual(model.fit_receipt['rows'], 20)
        self.assertTrue(np.all((y >= 0) & (y <= 1)))
        with self.assertRaises(ValueError): model.fit(X, np.full(20, np.nan))


if __name__ == '__main__':
    unittest.main()
