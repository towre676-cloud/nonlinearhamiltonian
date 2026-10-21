"""Fundamental-unit certificates: brute-force oracle, classical values, Pell integration, forgeries."""
import copy
import sys
import unittest
from math import isqrt
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import units as U          # noqa: E402
import check_units as C    # noqa: E402
import pell as P           # noqa: E402
import check_pell as CP    # noqa: E402


def brute(D, sign):
    """Smallest y >= 1 with D y^2 + sign a square (independent enumeration)."""
    y = 1
    while True:
        s = D * y * y + sign
        if s > 0 and isqrt(s) ** 2 == s:
            return [isqrt(s), y]
        y += 1


class Units(unittest.TestCase):
    def test_bruteforce_oracle(self):
        for D in range(2, 120):
            if isqrt(D) ** 2 == D:
                continue
            cert, _ = U.fundamental(D)
            if cert['norm_one_unit'][1] > 10 ** 5:
                continue          # brute force is only feasible for small solutions
            plus = brute(D, 1)
            self.assertEqual(cert['norm_one_unit'], plus, D)
            # The fundamental unit has norm -1 exactly when x^2 - D y^2 = -1 has a smaller solution.
            if cert['result']['norm'] == -1:
                self.assertEqual(cert['unit'], brute(D, -1), D)
            else:
                self.assertEqual(cert['unit'], plus, D)

    def test_classical_values(self):
        self.assertEqual(U.fundamental(61)[0]['unit'], [29718, 3805])
        self.assertEqual(U.fundamental(61)[0]['norm_one_unit'], [1766319049, 226153980])
        self.assertEqual(U.fundamental(991)[0]['norm_one_unit'][0], 379516400906811930638014896080)

    def test_forgeries(self):
        cert, model = U.fundamental(2)
        cert.pop('result')
        for mutate in (lambda c: c.update(unit=[17, 12]),          # a proper power is not fundamental
                       lambda c: c.update(norm_one_unit=[99, 70]),
                       lambda c: c.update(unit=[3, 2])):
            bad = copy.deepcopy(cert)
            mutate(bad)
            with self.assertRaises(ValueError):
                C.check(bad, model)
        with self.assertRaises(ValueError):
            U.fundamental(49)

    def test_pell_with_fundamental_unit(self):
        m = {'D': 2, 'N': -7, 'unit': 'fundamental', 'height': 1000}
        cert = P.compile_model(m)
        self.assertEqual((cert['seeds'], cert['height_count']['nonnegative_branch']), ([[1, 2], [5, 4]], 8))
        self.assertIn('full norm-one unit group', cert['result']['scope'])
        bad = copy.deepcopy(cert)
        bad['unit_certificate']['norm_one_unit'] = [577, 408]
        with self.assertRaises(ValueError):
            CP.check(bad, m)


if __name__ == '__main__':
    unittest.main()
