"""S2 acceptance tests: DGLA axioms, Maurer-Cartan lifting, obstructions, forgeries."""
import copy
import sys
import unittest
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parent)]
import dgla as G        # noqa: E402
import check_dgla as C  # noqa: E402
import qlinalg as L     # noqa: E402

TOY = {'schema': 'dgla-v1', 'field': 'Q',
       'basis': [{'degree': 1, 'name': 'e1'}, {'degree': 1, 'name': 'e2'}, {'degree': 2, 'name': 'f'}],
       'differential': [[0, 0, 0]] * 3, 'bracket': [[0, 1, [[2, 1]]]]}
SO3 = {(0, 1): {2: 1}, (1, 2): {0: 1}, (0, 2): {1: -1}}
HEIS = {(0, 1): {2: 1}}

_models = {}


def lie(structure):
    key = repr(sorted(structure.items()))
    if key not in _models:
        _models[key] = G.lie_deformation_dgla(3, structure)
    return _models[key]


class Toy(unittest.TestCase):
    def test_obstructed_and_unobstructed_first_orders(self):
        self.assertEqual(G.lift(TOY, [1, 1, 0], 4)['result']['claim'], 'obstructed')
        self.assertEqual(G.lift(TOY, [1, 0, 0], 5)['result']['order'], 5)

    def test_invalid_models_rejected(self):
        bad = copy.deepcopy(TOY)
        bad['bracket'] = [[0, 0, [[2, 1]]], [2, 2, [[0, 1]]]]       # [f,f] != 0 for even f
        with self.assertRaises(ValueError):
            C.Algebra(bad)
        bad = copy.deepcopy(TOY)
        bad['differential'] = [[0, 0, 0], [1, 0, 0], [0, 0, 0]]     # degree-preserving d
        with self.assertRaises(ValueError):
            C.Algebra(bad)
        bad = copy.deepcopy(TOY)
        bad['field'] = 'Z'
        with self.assertRaises(ValueError):
            C.Algebra(bad)
        with self.assertRaises(ValueError):
            G.lift(TOY, [0, 0, 1], 3)                                # not in L^1 / not a cocycle


class LieDeformations(unittest.TestCase):
    def test_nonjacobi_structure_rejected(self):
        with self.assertRaises(ValueError):
            G.lie_deformation_dgla(3, {(0, 1): {2: 1}, (1, 2): {1: 1}, (0, 2): {0: 1}})

    def test_heisenberg_cohomology_dimension(self):
        m = lie(HEIS)
        A = C.Algebra(m)
        self.assertEqual(A.verify_structure(), 21)
        idx = {k: [i for i in range(A.N) if A.deg[i] == k] for k in (0, 1, 2)}
        d0 = [[A.d[i][j] for j in idx[0]] for i in idx[1]]
        d1 = [[A.d[i][j] for j in idx[1]] for i in idx[2]]
        h1 = len(idx[1]) - L.rank(d1, len(idx[1])) - L.rank(d0, len(idx[0]))
        self.assertEqual(h1, 5)       # the classical value dim H^2(h3, h3) = 5

    def test_abelian_so3_lifts_and_nonjacobi_direction_obstructs(self):
        ab = lie({})
        self.assertEqual(G.lift(ab, G.two_cochain(3, SO3, ab), 4)['result']['claim'], 'lifted')
        bad = G.lift(ab, G.two_cochain(3, {(0, 1): {2: 1}, (1, 2): {1: 1}}, ab), 4)
        self.assertEqual((bad['result']['claim'], bad['result']['intrinsic']), ('obstructed', True))

    def test_heisenberg_obstructions(self):
        m = lie(HEIS)
        x = G.two_cochain(3, {(0, 1): {0: 1}, (0, 2): {1: 1}}, m)
        self.assertEqual(G.lift(m, x, 3)['result']['order'], 2)
        x = G.two_cochain(3, {(0, 1): {1: 1}, (1, 2): {2: 1}}, m)
        r = G.lift(m, x, 4)['result']
        self.assertEqual((r['claim'], r['order'], r['intrinsic']), ('obstructed', 3, False))


class Forgeries(unittest.TestCase):
    def test_mutations(self):
        ok = G.lift(TOY, [1, 0, 0], 3)
        ob = G.lift(TOY, [1, 1, 0], 3)
        bad = copy.deepcopy(ok); bad['jet'][1] = ['0', '1', '0']; bad.pop('result')
        bad['jet'].append(['0', '0', '0'])
        with self.assertRaises(ValueError):
            C.check(bad, TOY)          # x2 = e2 is fine at order 2 but ob_3 = f is not met
        bad = copy.deepcopy(ob); bad['functional'] = ['0', '0', '0']
        with self.assertRaises(ValueError):
            C.check(bad, TOY)
        bad = copy.deepcopy(ob); bad['status'] = 'lifted'; bad['jet'].append(['0', '0', '0'])
        with self.assertRaises(ValueError):
            C.check(bad, TOY)
        other = copy.deepcopy(TOY); other['bracket'] = []
        with self.assertRaises(ValueError):
            C.check(ok, other)


if __name__ == '__main__':
    unittest.main()
