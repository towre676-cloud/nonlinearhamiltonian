"""O1 acceptance tests for observer-closure-v2: seed fixtures, new edge cases, oracle, forgeries."""
import copy
import itertools
import random
import sys
import unittest
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parent)]
import observer                             # noqa: E402
import check_observer                       # noqa: E402
import observation_closure_reference as seed  # noqa: E402

SEED_MODELS = [
    ('present_is_not_future', dict(dimension=2, actions={'step': [[1, 1], [0, 1]]}, target=[[1, 0]], observation=[[1, 0]]), 2, 'impossible'),
    ('shared_nuisance_stays_hidden', dict(dimension=2, actions={'step': [[1, 0], [0, 1]]}, target=[[0, 1]], observation=[[0, 1]]), 1, 'recoverable'),
    ('shared_nuisance_feeds_target', dict(dimension=2, actions={'step': [[1, 0], [1, 1]]}, target=[[0, 1]], observation=[[0, 1]]), 2, 'impossible'),
    ('multioutput', dict(dimension=2, actions={'step': [[1, 0], [0, 1]]}, target=[[1, 0], [0, 1]], observation=[[1, 0], [0, 1]]), 2, 'recoverable'),
    ('ill_conditioned_but_exact', dict(dimension=2, actions={'step': [[1, 0], [0, 1]]}, target=[[0, 1]], observation=[[1, 0], [0, '1/1000000']]), 1, 'recoverable'),
    ('zero_target_no_sensors', dict(dimension=2, actions={'step': [[1, 1], [0, 1]]}, target=[[0, 0]], observation=[]), 0, 'recoverable'),
    ('empty_alphabet', dict(dimension=2, actions={}, target=[[1, 1]], observation=[[1, 1], [2, 2]]), 1, 'recoverable'),
]


def oracle_rank(model):
    """Brute force: span of G A_w over all words of length <= n (enough by the dimension argument)."""
    n = model['dimension']
    acts = {k: [[F(x) for x in r] for r in v] for k, v in model['actions'].items()}
    g = [[F(x) for x in r] for r in model['target']]
    rows = []
    for k in range(n + 1):
        for w in itertools.product(sorted(acts), repeat=k):
            rows += [check_observer._word_row(r, list(w), acts) for r in g]
    return check_observer._rank(rows, n) if rows else 0


def random_model(rng, n, n_actions, m, k):
    rnd = lambda: rng.choice([0, 0, 1, -1, 2, '1/2', '-3/2'])
    return {'dimension': n,
            'actions': {f'a{i}': [[rnd() for _ in range(n)] for _ in range(n)] for i in range(n_actions)},
            'target': [[rnd() for _ in range(n)] for _ in range(m)],
            'observation': [[rnd() for _ in range(n)] for _ in range(k)]}


class SeedFixtures(unittest.TestCase):
    def test_seed_reference_suite_still_passes_all_26(self):
        self.assertEqual(seed.verify()['checks'], 26)

    def test_seed_models_agree_with_v2(self):
        for name, model, r, status in SEED_MODELS:
            cert = observer.compile_model(model)
            self.assertEqual(cert['rank'], r, name)
            self.assertEqual(cert['panel']['status'], status, name)
            self.assertEqual(seed.compile_model(model)['basis'], cert['basis'], name)

    def test_ill_conditioned_recovery_is_exact_but_amplifies(self):
        cert = observer.compile_model(SEED_MODELS[4][1])
        self.assertEqual(cert['panel']['recovery'], [['0', '1000000']])


class EdgeCases(unittest.TestCase):
    def test_redundant_and_duplicate_sensors(self):
        m = dict(dimension=3, actions={'s': [[1, 0, 0], [0, 1, 0], [0, 0, 1]]}, target=[[1, 1, 0]],
                 observation=[[1, 0, 0], [1, 0, 0], [0, 1, 0], [2, 1, 0], [0, 0, 0]])
        cert = observer.compile_model(m)
        self.assertEqual((cert['rank'], cert['panel']['status']), (1, 'recoverable'))

    def test_noncommuting_actions_order_matters(self):
        m = dict(dimension=3, actions={'a': [[0, 1, 0], [0, 0, 0], [0, 0, 1]], 'b': [[1, 0, 0], [0, 0, 1], [0, 0, 0]]},
                 target=[[1, 0, 0]], observation=[[1, 0, 0]])
        cert = observer.compile_model(m)
        self.assertEqual(cert['rank'], oracle_rank(m))
        acts = {k: [[F(x) for x in r] for r in v] for k, v in m['actions'].items()}
        g = [F(1), F(0), F(0)]
        self.assertNotEqual(check_observer._word_row(g, ['a', 'b'], acts), check_observer._word_row(g, ['b', 'a'], acts))

    def test_zero_target_with_sensors(self):
        cert = observer.compile_model(dict(dimension=2, actions={'s': [[0, 1], [1, 0]]}, target=[[0, 0], [0, 0]],
                                           observation=[[1, 1]]))
        self.assertEqual((cert['rank'], cert['panel']['status']), (0, 'recoverable'))

    def test_hidden_state_is_a_real_counterexample(self):
        rng = random.Random(1021)
        found = 0
        for _ in range(60):
            m = random_model(rng, 3, 2, 1, 1)
            cert = observer.compile_model(m)
            if cert['panel']['status'] != 'impossible':
                continue
            found += 1
            v = [F(x) for x in cert['panel']['invisible_state']]
            acts = {k: [[F(x) for x in r] for r in a] for k, a in m['actions'].items()}
            w = cert['panel']['lost_target_word']
            row = check_observer._word_row([F(x) for x in m['target'][w['target_row']]], w['word'], acts)
            self.assertNotEqual(sum(a * b for a, b in zip(row, v)), 0)
            self.assertTrue(all(sum(F(a) * b for a, b in zip(h, v)) == 0 for h in m['observation']))
        self.assertGreater(found, 5)

    def test_floats_rejected(self):
        with self.assertRaises(ValueError):
            observer.compile_model(dict(dimension=1, actions={}, target=[[0.5]]))

    def test_budget_returns_unknown(self):
        self.assertEqual(observer.compile_model(dict(dimension=3, actions={}, target=[[1, 0, 0]]), max_dimension=2)['status'], 'unknown')


class Oracle(unittest.TestCase):
    def test_random_models_match_bruteforce_minimal_dimension(self):
        rng = random.Random(20261021)
        for trial in range(80):
            m = random_model(rng, rng.randint(1, 4), rng.randint(0, 3), rng.randint(1, 2), rng.randint(0, 3))
            cert = observer.compile_model(m)
            self.assertEqual(cert['rank'], oracle_rank(m), trial)
            # Panel claim agrees with the kernel criterion ker H subset ker Q.
            h = [[F(x) for x in r] for r in m['observation']]
            q = [[F(x) for x in r] for r in cert['basis']]
            n = m['dimension']
            ok = check_observer._rank(h + q, n) == check_observer._rank(h, n) if h else not q
            self.assertEqual(cert['panel']['status'] == 'recoverable', ok, trial)


class Forgeries(unittest.TestCase):
    def setUp(self):
        self.model = dict(dimension=3, actions={'a': [[0, 1, 0], [0, 0, 1], [0, 0, 0]], 'b': [[1, 0, 0], [0, 2, 0], [0, 0, 3]]},
                          target=[[1, 0, 0]], observation=[[1, 0, 0], [0, 1, 0]])
        self.cert = observer.compile_model(self.model)

    def rejects(self, mutate, model=None):
        bad = copy.deepcopy(self.cert)
        mutate(bad)
        with self.assertRaises((ValueError, KeyError, TypeError, IndexError)):
            check_observer.check(bad, model or self.model)

    def test_all_mutations_rejected(self):
        self.assertEqual(check_observer.check(self.cert, self.model)['status'], 'passed')
        self.rejects(lambda c: c['basis_words'][1].update(word=['b']))
        self.rejects(lambda c: c['target_factor'][0].__setitem__(0, '2'))
        self.rejects(lambda c: c['quotient_actions']['a'][0].__setitem__(0, '1'))
        self.rejects(lambda c: c.update(coefficient_domain='Z'))
        self.rejects(lambda c: c.update(word_convention='left-to-right'))
        self.rejects(lambda c: c.update(rank=1))
        self.rejects(lambda c: c['basis'].append(c['basis'][0]))
        self.rejects(lambda c: c['panel'].update(invisible_state=['0', '0', '0']))
        self.rejects(lambda c: c['panel'].update(output_difference='5'))
        self.rejects(lambda c: c.update(format='observer-closure-v1'))
        other = copy.deepcopy(self.model)
        other['target'] = [[0, 1, 0]]
        self.rejects(lambda c: None, other)


if __name__ == '__main__':
    unittest.main()
