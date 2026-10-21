"""S1 acceptance tests: stable obstruction interface, rank oracle on generated complexes, forgeries."""
import copy
import random
import sys
import unittest
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parent)]
import obstruction as O     # noqa: E402
import qlinalg as L         # noqa: E402


def model(n, d, field='Q'):
    return {'field': field, 'dimensions': n, 'differentials': d}


def random_complex(rng, n0, n1, n2):
    d0 = [[F(rng.randint(-2, 2)) for _ in range(n0)] for _ in range(n1)]
    if rng.random() < 0.3:
        d0 = [r[:] for r in d0[:1]] * n1 if n1 else d0     # rank deficient
    left = L.null_basis(L.transpose(d0, n1), n1) if n1 else []
    d1 = []
    for _ in range(n2):
        coeffs = [F(rng.randint(-2, 2)) for _ in left]
        d1.append([sum((c * v[j] for c, v in zip(coeffs, left)), F(0)) for j in range(n1)])
    return d0, d1


class Interface(unittest.TestCase):
    def test_triangle(self):
        tri = model([3, 3], [[[-1, 1, 0], [0, -1, 1], [1, 0, -1]]])
        self.assertEqual(O.solve(tri, 1, [1, 2, -3])['status'], 'solved')
        ob = O.solve(tri, 1, [1, 2, -2])
        self.assertEqual(ob['status'], 'obstructed')
        self.assertEqual(O.check_answer(tri, ob)['answer'], 'obstructed')

    def test_invalid_and_budget(self):
        self.assertEqual(O.solve(model([1, 1], [[[2]]], 'Z'), 1, [1])['status'], 'invalid_model')
        self.assertEqual(O.solve(model([1, 1, 1], [[[1]], [[1]]]), 1, [1])['status'], 'invalid_model')
        self.assertEqual(O.solve(model([1, 1], [[[0.5]]]), 1, [1])['status'], 'invalid_model')
        self.assertEqual(O.solve(model([2, 2], [[[1, 0], [0, 1]]]), 1, [1, 1], max_size=3)['status'], 'unknown')
        self.assertEqual(O.solve(model([1, 2, 1], [[[1], [0]], [[0, 1]]]), 1, [1, 1])['status'], 'not_cocycle')

    def test_rational_answer_is_not_integral(self):
        # Over Q multiplication by 2 is invertible: the class of 1 is a boundary (u = 1/2).
        ans = O.solve(model([1, 1], [[[2]]]), 1, [1])
        self.assertEqual((ans['status'], ans['primitive']['entries']), ('solved', [['1/2']]))

    def test_degree_zero(self):
        m = model([2, 1], [[[1, -1]]])
        self.assertEqual(O.solve(m, 0, [1, 1])['status'], 'obstructed')
        self.assertEqual(O.solve(m, 0, [0, 0])['status'], 'solved')


class RankOracle(unittest.TestCase):
    def test_generated_complexes(self):
        rng = random.Random(1021)
        seen = {'solved': 0, 'obstructed': 0}
        for trial in range(60):
            n0, n1, n2 = rng.randint(0, 3), rng.randint(1, 4), rng.randint(0, 3)
            d0, d1 = random_complex(rng, n0, n1, n2)
            m = model([n0, n1, n2], [L.strs(d0) if n1 else [], L.strs(d1) if n2 else []])
            if n0 == 0:
                m['differentials'][0] = [[] for _ in range(n1)]
            if n2 == 0:
                m['differentials'][1] = []
            z = L.null_basis(d1, n1) if n2 else L.eye(n1)
            for _ in range(3):
                coeffs = [F(rng.randint(-2, 2)) for _ in z]
                b = [sum((c * v[j] for c, v in zip(coeffs, z)), F(0)) for j in range(n1)]
                ans = O.solve(m, 1, [str(x) for x in b])
                # Independent oracle: b is a boundary iff appending it does not raise the rank of d0.
                cols = L.transpose(d0, n0) if n0 else []
                boundary = L.rank(cols + [b], n1) == L.rank(cols, n1) if cols else not any(b)
                self.assertEqual(ans['status'], 'solved' if boundary else 'obstructed', trial)
                seen[ans['status']] += 1
        self.assertGreater(min(seen.values()), 10)


class Forgeries(unittest.TestCase):
    def test_mutated_answers_rejected(self):
        tri = model([3, 3], [[[-1, 1, 0], [0, -1, 1], [1, 0, -1]]])
        ok = O.solve(tri, 1, [1, 2, -3])
        ob = O.solve(tri, 1, [1, 2, -2])
        for ans, path in ((ok, ('primitive', 'entries', 0, 0)), (ob, ('functional', 'entries', 0, 0))):
            bad = copy.deepcopy(ans)
            node = bad
            for key in path[:-1]:
                node = node[key]
            node[path[-1]] = str(F(node[path[-1]]) + 1)
            with self.assertRaises(ValueError):
                O.check_answer(tri, bad)
        bad = copy.deepcopy(ob)
        bad['status'] = 'solved'
        bad['primitive'] = {'rows': 3, 'cols': 1, 'entries': [['0'], ['0'], ['0']]}
        with self.assertRaises(ValueError):
            O.check_answer(tri, bad)


if __name__ == '__main__':
    unittest.main()
