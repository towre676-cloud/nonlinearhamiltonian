"""O3 acceptance tests: Bellman certificates, brute-force tree oracle, unresolved pairs, forgeries."""
import copy
import random
import sys
import unittest
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import adaptive as A          # noqa: E402
import check_adaptive as C    # noqa: E402

SEED_TESTS = [('t1', 1, {'a': 0, 'b': 1, 'c': 1}), ('t2', 2, {'a': 1, 'b': 0, 'c': 1}), ('t4', 4, {'a': 0, 'b': 1, 'c': 2})]


def model(labels, tests):
    return {'states': sorted(labels), 'labels': labels,
            'tests': [{'name': n, 'cost': c, 'outcomes': o} for n, c, o in tests]}


def brute(m):
    """Oracle: enumerate every decision tree explicitly (any test order, strict splits only)."""
    states, labels, tests = C.read(m)

    def trees(T):
        if len({labels[s] for s in T}) == 1:
            yield F(0)
            return
        for c, o in tests:
            fib = C.fibres(T, o)
            if len(fib) < 2:
                continue
            options = [list(trees(f)) for f in fib.values()]
            if any(not x for x in options):
                continue
            # every combination of subtrees is a distinct policy
            def combos(i):
                if i == len(options):
                    yield []
                    return
                for v in options[i]:
                    for rest in combos(i + 1):
                        yield [v] + rest
            for combo in combos(0):
                yield c + max(combo)
    vals = list(trees(states))
    return min(vals) if vals else None


class Fixtures(unittest.TestCase):
    def test_target_only_is_cheaper_than_identification(self):
        full = A.solve(model({'a': 0, 'b': 1, 'c': 2}, SEED_TESTS))
        target = A.solve(model({'a': 0, 'b': 1, 'c': 1}, SEED_TESTS))
        self.assertEqual((full['value'], target['value']), ('3', '1'))

    def test_unresolved_pair(self):
        r = A.solve(model({'a': 0, 'b': 1, 'c': 1}, [('t', 1, {'a': 0, 'b': 0, 'c': 1})]))
        self.assertEqual((r['status'], r['pair']), ('unresolvable', ['a', 'b']))

    def test_single_state_and_constant_labels(self):
        self.assertEqual(A.solve(model({'a': 0}, []))['value'], '0')
        self.assertEqual(A.solve(model({'a': 0, 'b': 0}, SEED_TESTS[:1] and [('t', 1, {'a': 0, 'b': 1})]))['value'], '0')


class Oracle(unittest.TestCase):
    def test_random_tables_match_tree_enumeration(self):
        rng = random.Random(77)
        for trial in range(80):
            n = rng.randint(1, 5)
            names = [chr(97 + i) for i in range(n)]
            labels = {s: rng.randint(0, 2) for s in names}
            tests = [(f't{k}', rng.choice([1, 2, 3, '1/2', '5/2']), {s: rng.randint(0, 2) for s in names})
                     for k in range(rng.randint(1, 3))]
            m = model(labels, tests)
            r = A.solve(m)
            b = brute(m)
            if r['status'] == 'unresolvable':
                self.assertIsNone(b, trial)
            else:
                self.assertEqual(F(r['value']), b, trial)


class Forgeries(unittest.TestCase):
    def test_mutations(self):
        m = model({'a': 0, 'b': 1, 'c': 2}, SEED_TESTS)
        cert = A.solve(m)
        for mutate in (lambda c: c.update(value='2'),
                       lambda c: c['lower_bounds'].update({'a|b|c': '4'}),
                       lambda c: c['lower_bounds'].pop('b|c'),
                       lambda c: c['tree'].update(test=2),
                       lambda c: c.update(status='unresolvable', pair=['a', 'b'])):
            bad = copy.deepcopy(cert)
            mutate(bad)
            with self.assertRaises((ValueError, KeyError)):
                C.check(bad, m)
        with self.assertRaises(ValueError):
            A.solve(model({'a': 0, 'b': 1}, [('t', 0, {'a': 0, 'b': 1})]))     # nonpositive cost
        with self.assertRaises(ValueError):
            A.solve(model({'a': 0, 'b': 1}, [('t', 1, {'a': 0})]))               # missing outcome


if __name__ == '__main__':
    unittest.main()
