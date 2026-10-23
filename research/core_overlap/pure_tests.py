"""Independent finite-dimensional cross-checks of the pure transverse theorem."""
from fractions import Fraction as F
from pathlib import Path
import sys
import unittest

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parents[1]/'extensions'/'hamiltonian'),
               str(HERE.parents[1]/'extensions')]
import pure_transverse as P
from test_root_rigidity import filtered_dim


class PurePerfectPower(unittest.TestCase):
    def test_structural_receipts(self):
        self.assertEqual(P.self_test()['status'], 'passed')

    def test_exact_dimensions_independent_pbw_engine(self):
        H, J = P.family()
        shifted, _ = P.family(gamma=F(1, 2), beta=2, delta=-3)
        varied, _ = P.family(a=2, u={3: -1, 2: 1}, coeffs=(2, -1, 3))
        cases = [(H, 3), (shifted, 3), (varied, 3),
                 (P.add(H, {(0, 1): F(1)}), 2),
                 ({(7, 0): F(1), (3, 2): F(1)}, 2),
                 ({(7, 0): F(1), (2, 3): F(1)}, 2)]
        for A, dim in cases:
            result = P.classify(A)
            self.assertEqual(result['dimension'], dim)
            N = max(sum(k) for k in A) + 1
            self.assertEqual(filtered_dim(A, N, 8), dim, (A, result))

    def test_rational_differentiation_and_scope(self):
        self.assertEqual(P.deriv({(3, 2): F(1, 7)}, 2, 1), {(1, 1): F(12, 7)})
        # Balanced transverse powers and multi-root phi are explicitly outside.
        self.assertIsNone(P.classify({(8, 0): 1, (3, 3): 1}))
        self.assertIsNone(P.classify({(8, 0): 1, (3, 2): 1, (1, 2): 1}))


if __name__ == '__main__':
    unittest.main()
