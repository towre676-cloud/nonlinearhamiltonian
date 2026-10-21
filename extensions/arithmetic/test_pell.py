"""A1 acceptance tests: handoff fixtures, bounded brute-force oracle, rejections, forgeries."""
import copy
import json
import random
import sys
import unittest
from math import isqrt
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import pell as P         # noqa: E402
import check_pell as C   # noqa: E402

FIXTURES = json.loads((HERE.parent / 'structure/arithmetic_future_fixtures.json').read_text())['cases']


def brute(D, N, Y, flt=None):
    """Independent oracle: every x, y >= 0 with y <= Y and x^2 - D y^2 = N."""
    pts = []
    for y in range(Y + 1):
        s = N + D * y * y
        if s >= 0 and isqrt(s) ** 2 == s:
            pts.append((isqrt(s), y))
    acc = [p for p in pts if flt and [p[0] % flt['modulus'], p[1] % flt['modulus']] in flt['accept']]
    return pts, acc


def y_div(q):
    return {'modulus': q, 'accept': [[x, 0] for x in range(q)]}


class Fixtures(unittest.TestCase):
    def test_handoff_fixtures(self):
        for case in FIXTURES:
            m = {'D': case['D'], 'N': case['N'], 'unit': case['unit'], 'filter': y_div(3), 'height': case['height_bound']}
            cert = P.compile_model(m)
            self.assertEqual(cert['seeds'], case['seeds'])
            self.assertEqual(cert['height_count']['nonnegative_branch'], case['population'])
            self.assertEqual(cert['height_count']['accepted'], case['y_divisible_by_3_population'])
            for cyc, ref in zip(cert['cycles'], case['full_state_cycles_mod_3']):
                self.assertEqual((cyc['states'], cyc['period'], cyc['accepted_indices']),
                                 (ref['states'], ref['period'], ref['accepted_indices']))

    def test_proper_power_unit_has_more_seeds_same_points(self):
        base = P.compile_model({'D': 2, 'N': -7, 'unit': [3, 2], 'height': 10 ** 6})
        sq = P.compile_model({'D': 2, 'N': -7, 'unit': [17, 12], 'height': 10 ** 6})
        self.assertEqual(sq['seeds'], [[1, 2], [5, 4], [11, 8], [31, 22]])
        self.assertEqual(base['height_count']['nonnegative_branch'], sq['height_count']['nonnegative_branch'])

    def test_empty_seed_list_is_a_complete_negative(self):
        cert = P.compile_model({'D': 3, 'N': 2, 'unit': [2, 1], 'height': 1000})   # x^2 - 3y^2 = 2 has no solution
        self.assertEqual((cert['seeds'], cert['height_count']['nonnegative_branch']), ([], 0))
        self.assertEqual(brute(3, 2, 1000)[0], [])


class Oracle(unittest.TestCase):
    def test_random_models_match_bruteforce(self):
        rng = random.Random(20261021)
        units = {2: (3, 2), 3: (2, 1), 5: (9, 4), 6: (5, 2), 7: (8, 3), 10: (19, 6), 11: (10, 3), 13: (649, 180)}
        for trial in range(60):
            D = rng.choice(sorted(units))
            a, b = units[D]
            if rng.random() < 0.3:
                a, b = a * a + D * b * b, 2 * a * b          # squared unit: a proper power
            N = rng.choice([n for n in range(-40, 41) if n])
            q = rng.choice([2, 3, 4, 5, 7])
            flt = {'modulus': q, 'accept': sorted([rng.randrange(q), rng.randrange(q)] for _ in range(3))}
            Y = rng.choice([50, 300, 2000])
            cert = P.compile_model({'D': D, 'N': N, 'unit': [a, b], 'filter': flt, 'height': Y})
            pts, acc = brute(D, N, Y, flt)
            self.assertEqual(cert['height_count']['nonnegative_branch'], len(pts), (D, N, a, b))
            self.assertEqual(cert['height_count']['accepted'], len(acc), (D, N, a, b))


class Rejections(unittest.TestCase):
    def test_invalid_models(self):
        for m in ({'D': 4, 'N': 1, 'unit': [3, 1]}, {'D': -2, 'N': 1, 'unit': [3, 2]}, {'D': 2, 'N': 0, 'unit': [3, 2]},
                  {'D': 2, 'N': 1, 'unit': [3, 1]}, {'D': 2, 'N': 1, 'unit': [1, 0]}, {'D': 2.0, 'N': 1, 'unit': [3, 2]}):
            with self.assertRaises(ValueError):
                P.compile_model(m)

    def test_budgets(self):
        self.assertEqual(P.compile_model({'D': 2, 'N': -7, 'unit': [3, 2], 'filter': y_div(1000)}, max_states=10)['status'], 'unknown')
        self.assertEqual(P.compile_model({'D': 13, 'N': 10 ** 9, 'unit': [649, 180]}, max_window=100)['status'], 'unknown')

    def test_forgeries(self):
        m = {'D': 5, 'N': -4, 'unit': [9, 4], 'filter': y_div(3), 'height': 1000}
        cert = P.compile_model(m)
        for mutate in (lambda c: c['seeds'].pop(), lambda c: c['seeds'].append([29, 13]),
                       lambda c: c['cycles'][0]['accepted_indices'].append(1),
                       lambda c: c['cycles'][0]['states'].pop(),
                       lambda c: c['height_count'].update(nonnegative_branch=9),
                       lambda c: c.update(window_end_exclusive=3)):
            bad = copy.deepcopy(cert)
            mutate(bad)
            with self.assertRaises((ValueError, IndexError)):
                C.check(bad, m)


if __name__ == '__main__':
    unittest.main()
