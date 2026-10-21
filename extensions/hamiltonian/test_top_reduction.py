"""Six-parameter qp^3 family: top-weight reduction certificates, star-engine cross-checks,
adversarial weights and forgeries."""
import copy
import importlib.util
import random
import sys
import unittest
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
import weyl_receipts as W          # noqa: E402
import weyl_groebner as G          # noqa: E402
import top_reduction as T          # noqa: E402
import check_top_reduction as C    # noqa: E402

spec = importlib.util.spec_from_file_location('baseline_engine', ROOT / 'research/hamiltonian/independent/engine.py')
E = importlib.util.module_from_spec(spec)
spec.loader.exec_module(E)


def family(a, b, c, d, e, f):
    H = {(1, 3): F(1), (2, 0): F(a), (1, 1): F(b), (0, 2): F(c), (1, 0): F(d), (0, 1): F(e), (0, 0): F(f)}
    return W.tidy(H)


def exact_through(H, g, depth):
    for _ in range(depth + 1):
        if E.defects(H, g):
            return False
        g = E.poisson(H, g)
    return True


class SixParameterFamily(unittest.TestCase):
    def test_random_instances(self):
        rng = random.Random(3)
        vals = [0, 1, -1, 2, '1/2', '-3/4', 5]
        seen = {'finite': 0, 'lines': 0}
        for trial in range(16):
            a = 0 if trial % 2 else rng.choice([1, -1, 2, '1/3'])
            H = family(a, *(rng.choice(vals) for _ in range(5)))
            meta, cert = T.reduce(H, (3, 1))
            self.assertEqual(meta['status'], 'certified', (trial, H))
            self.assertEqual(meta['claim'], 'lines' if a == 0 else 'finite')
            self.assertEqual(C.check(cert)['status'], 'passed')
            seen[meta['claim']] += 1
            # Independent star-engine evidence for the conclusion.
            if a == 0:
                for j in range(4):
                    self.assertTrue(exact_through(H, {(1, j): F(1)}, 3))
                self.assertFalse(exact_through(H, {(2, 0): F(1)}, 4))
            else:
                self.assertTrue(exact_through(H, H, 3))
                self.assertFalse(exact_through(H, {(0, 1): F(1)}, 4))
        self.assertEqual(seen, {'finite': 8, 'lines': 8})

    def test_wrong_weight_is_not_transferable(self):
        # With weight (1,1) the top part of qp^3+q^2 is qp^3, whose core has lines that
        # D_H does not preserve: the checker must refuse the transfer.
        meta, cert = T.reduce(family(1, 0, 0, 0, 0, 0), (1, 1))
        self.assertEqual((meta['status'], cert), ('not_transferable', None))

    def test_forgeries(self):
        meta, fin = T.reduce(family(1, 2, 3, 0, 1, 0), (3, 1))
        meta, lin = T.reduce(family(0, 2, 3, 1, 1, 0), (3, 1))
        cases = []
        b = copy.deepcopy(fin); b['hamiltonian'].append([3, 0, '1']); cases.append(b)     # top part changes
        b = copy.deepcopy(fin); b['claim'] = 'lines'; cases.append(b)
        b = copy.deepcopy(lin); b['claim'] = 'finite'; cases.append(b)
        b = copy.deepcopy(lin); b['hamiltonian'] = [r for r in b['hamiltonian']] + [[2, 0, '1']]; cases.append(b)
        b = copy.deepcopy(fin); b['weight'] = [0, 1]; cases.append(b)
        b = copy.deepcopy(fin); b['top_certificate']['claim']['basis'] = b['top_certificate']['claim']['basis'][:1]
        cases.append(b)
        for bad in cases:
            with self.assertRaises((ValueError, KeyError)):
                C.check(bad)


if __name__ == '__main__':
    unittest.main()
