"""O2 acceptance tests: noise-aware panels, exhaustive oracle, counterexamples, forgeries."""
import copy
import random
import sys
import unittest
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parent)]
import panels          # noqa: E402
import check_panel     # noqa: E402
import observer        # noqa: E402


def model(sensors, noise, targets, g2, contract='per_target', n=2):
    return {'dimension': n, 'sensors': [{'name': f's{i}', 'row': r, 'cost': c} for i, (r, c) in enumerate(sensors)],
            'noise': noise, 'targets': targets, 'contract': contract, 'gamma_squared': g2}


EYE2 = [[1, 0], [0, 1]]


class Counterexamples(unittest.TestCase):
    def test_rank_perfect_but_ill_conditioned(self):
        sensors = [([1, 0], 1), ([0, '1/1000'], 1)]
        t = {'mode': 'explicit', 'matrices': [[[0, 1]]]}
        cert, res = panels.solve(model(sensors, EYE2, t, str(999 ** 2)))
        self.assertEqual(res['claim'], 'infeasible')
        cert, res = panels.solve(model(sensors, EYE2, t, str(1000 ** 2)))
        self.assertEqual((res['claim'], res['sensors']), ('optimal', [1]))

    def test_correlated_noise_changes_the_answer(self):
        sensors = [([1, 0], 1), ([1, 0], 1)]
        t = {'mode': 'explicit', 'matrices': [[[1, 0]]]}
        g2 = '2/3'
        _, ind = panels.solve(model(sensors, EYE2, t, g2))
        _, pos = panels.solve(model(sensors, [[1, '1/2'], ['1/2', 1]], t, g2))
        _, neg = panels.solve(model(sensors, [[1, '-1/2'], ['-1/2', 1]], t, '1/4'))
        self.assertEqual(ind['claim'], 'optimal')        # independent bars: averaging gives J = 2
        self.assertEqual(pos['claim'], 'infeasible')     # correlation 1/2: J = 4/3 only
        self.assertEqual(neg['claim'], 'optimal')        # anticorrelation: J = 4

    def test_stacked_and_per_target_are_different_contracts(self):
        sensors = [([1, 0], 1), ([0, 1], 1)]
        t = {'mode': 'explicit', 'matrices': [[[1, 0]], [[1, 0]]]}
        _, per = panels.solve(model(sensors, EYE2, t, '3/2'))
        _, st = panels.solve(model(sensors, EYE2, t, '3/2', 'stacked'))
        self.assertEqual((per['claim'], st['claim']), ('optimal', 'infeasible'))

    def test_finite_horizon_future_target_needs_hidden_coordinate(self):
        t = {'mode': 'finite_horizon', 'actions': {'feed': [[1, 0], [1, 1]]}, 'target': [[0, 1]], 'horizon': 0}
        sensors = [([1, 0], 1), ([0, 1], 1)]
        _, now = panels.solve(model(sensors, EYE2, t, 1))
        t['horizon'] = 1
        _, later = panels.solve(model(sensors, EYE2, t, 2))
        self.assertEqual(now['sensors'], [1])
        self.assertEqual(later['sensors'], [0, 1])

    def test_large_cap_cannot_repair_hidden_direction(self):
        t = {'mode': 'explicit', 'matrices': [[[0, 1]]]}
        _, res = panels.solve(model([([1, 0], 1)], [[1]], t, str(10 ** 30)))
        self.assertEqual(res['claim'], 'infeasible')


class Oracle(unittest.TestCase):
    def test_random_menus_match_exhaustive_search(self):
        rng = random.Random(4242)
        claims = {'optimal': 0, 'infeasible': 0}
        for trial in range(70):
            n, k = rng.randint(1, 3), rng.randint(1, 6)
            rnd = lambda: rng.choice([0, 0, 1, -1, 2, '1/2'])
            sensors = [([rnd() for _ in range(n)], rng.randint(0, 5)) for _ in range(k)]
            A = [[F(rng.randint(-2, 2)) for _ in range(k)] for _ in range(k)]
            R = [[sum(A[i][t] * A[j][t] for t in range(k)) + (k if i == j else 0) for j in range(k)] for i in range(k)]
            R = [[str(x) for x in r] for r in R]
            t = {'mode': 'explicit', 'matrices': [[[rnd() for _ in range(n)]] for _ in range(rng.randint(1, 2))]}
            m = model(sensors, R, t, rng.choice(['1', '4', '20', '1/3']), rng.choice(['per_target', 'stacked']), n)
            cert, res = panels.solve(m)
            best = panels.exhaustive(m)
            claims[res['claim']] += 1
            if best is None:
                self.assertEqual(res['claim'], 'infeasible', trial)
            else:
                self.assertEqual((res['claim'], F(res['cost'])), ('optimal', best[0]), trial)
        self.assertGreater(min(claims.values()), 5)

    def test_budget_gives_incomplete_with_lower_bound(self):
        sensors = [([1, 0], 3), ([0, 1], 2), ([1, 1], 1), ([1, -1], 1)]
        t = {'mode': 'explicit', 'matrices': [EYE2]}
        cert, res = panels.solve(model(sensors, [[1 if i == j else 0 for j in range(4)] for i in range(4)], t, 4), max_nodes=2)
        self.assertEqual(res['claim'], 'incomplete')
        self.assertIn('lower_bound', res)


class Metric(unittest.TestCase):
    def test_rotation_has_all_time_metric_and_shear_does_not_with_identity(self):
        rot = {'dimension': 2, 'actions': {'r': [[0, -1], [1, 0]]}, 'target': [[1, 0]]}
        obs = observer.compile_model(rot)
        m = model([([1, 0], 1), ([0, 1], 1)], EYE2, {'mode': 'explicit', 'matrices': [[[1, 0]]]}, 1)
        cert = panels.metric(m, obs, [[1, 0], [0, 1]], [0, 1])
        self.assertEqual(check_panel.check_metric(cert, m)['claim'], 'all_time_bound_sufficient')
        shear = {'dimension': 2, 'actions': {'s': [[1, 1], [0, 1]]}, 'target': [[1, 0]]}
        self.assertIsNone(panels.metric(m, observer.compile_model(shear), [[1, 0], [0, 1]], [0, 1]))


class MetricSearch(unittest.TestCase):
    def setUp(self):
        self.m = model([([1, 0], 1), ([0, 1], 1)], EYE2, {'mode': 'explicit', 'matrices': [[[1, 0]]]}, 100)

    def test_finite_group_found(self):
        obs = observer.compile_model({'dimension': 2, 'actions': {'r': [[0, -1], [1, 0]], 's': [[1, 0], [0, -1]]},
                                      'target': [[1, 0]]})
        cert, how = panels.metric_search(self.m, obs, [0, 1])
        self.assertTrue(how.startswith('finite semigroup'))
        self.assertEqual(check_panel.check_metric(cert, self.m)['claim'], 'all_time_bound_sufficient')

    def test_contractive_family_found(self):
        obs = observer.compile_model({'dimension': 2, 'actions': {'a': [['1/2', '1/2'], [0, '1/2']],
                                                                  'b': [['1/3', 0], ['1/3', '1/3']]},
                                      'target': [[1, 0]]})
        cert, how = panels.metric_search(self.m, obs, [0, 1])
        self.assertIsNotNone(cert, how)
        self.assertEqual(check_panel.check_metric(cert, self.m)['status'], 'passed')

    def test_unbounded_and_jointly_unstable_give_no_certificate(self):
        shear = observer.compile_model({'dimension': 2, 'actions': {'s': [[1, 1], [0, 1]]}, 'target': [[1, 0]]})
        self.assertEqual(panels.metric_search(self.m, shear, [0, 1]), (None, 'no_certificate'))
        # Each action is nilpotent-plus-1/2 (spectral radius 1/2), yet their product has an eigenvalue > 1.
        pair = observer.compile_model({'dimension': 2, 'actions': {'a': [['1/2', 2], [0, '1/2']], 'b': [['1/2', 0], [2, '1/2']]},
                                       'target': [[1, 0]]})
        self.assertEqual(panels.metric_search(self.m, pair, [0, 1], max_len=6)[1], 'no_certificate')


class Forgeries(unittest.TestCase):
    def setUp(self):
        sensors = [([1, 0], 3), ([0, 1], 2), ([1, 1], 1), ([0, '1/10'], 1)]
        self.m = model(sensors, [[2, 1, 0, 0], [1, 2, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]],
                       {'mode': 'explicit', 'matrices': [[[1, 0]], [[0, 1]]]}, 3)
        self.cert, self.res = panels.solve(self.m)

    def rejects(self, mutate, m=None):
        bad = copy.deepcopy(self.cert)
        mutate(bad)
        with self.assertRaises((ValueError, KeyError, TypeError, IndexError)):
            check_panel.check(bad, m or self.m)

    def find(self, kind):
        def walk(t):
            if t['kind'] == kind:
                return t
            for c in t.get('children', []):
                r = walk(c)
                if r:
                    return r
        return walk

    def test_mutations(self):
        self.assertEqual(self.res['claim'], 'optimal')
        def bump_ldl(c):
            leaf = self.find('feasible')(c['tree'])
            leaf['ldl'][0]['d'][0] = str(F(leaf['ldl'][0]['d'][0]) + 1)
        self.rejects(bump_ldl)
        self.rejects(lambda c: c['optimum'].update(cost='0'))
        self.rejects(lambda c: c.update(status='infeasible'))
        self.rejects(lambda c: c.update(tie_policy='all_optima'))
        self.rejects(lambda c: c['tree'].update(kind='open'))
        def drop_child(c):
            c['tree']['children'][1] = {'include': [], 'exclude': [0], 'kind': 'cost'}
        if self.cert['tree']['kind'] == 'branch':
            self.rejects(drop_child)
        other = copy.deepcopy(self.m)
        other['gamma_squared'] = '1/100'
        self.rejects(lambda c: None, other)
        notpd = copy.deepcopy(self.m)
        notpd['noise'][0][1] = notpd['noise'][1][0] = 3
        with self.assertRaises(ValueError):
            panels.solve(notpd)


if __name__ == '__main__':
    unittest.main()
