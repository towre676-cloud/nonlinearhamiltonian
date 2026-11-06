"""Exact regression, certificate rejection, and a separate star-engine witness."""
import copy
import importlib.util
import json
from pathlib import Path
import unittest
import verify as V

HERE = Path(__file__).resolve().parent

class StrataTests(unittest.TestCase):
    def test_full_independent_replay(self):
        result = V.verify()
        self.assertEqual((result['triple_blocks'], result['triple_minors']), (16, 24))

    def test_corrupted_bezout_rejected(self):
        data = json.loads((HERE/'triple_certificate.json').read_text())
        data[0]['bezout'][0] = '0'
        with self.assertRaises(AssertionError):
            V.verify(recs=data)

    def test_missing_degree_rejected(self):
        data = json.loads((HERE/'triple_certificate.json').read_text())
        with self.assertRaises(AssertionError):
            V.verify(recs=data[:-1])

    def test_counterexample_defining_star_exponential(self):
        # Maintained stdlib engine expands the star exponential separately.
        path = HERE.parent/'independent/engine.py'
        spec = importlib.util.spec_from_file_location('strata_star_engine', path)
        E = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(E)
        H = {(4,2):1, (6,0):1}
        G = {(1,1):1}
        DG = E.poisson(H,G)
        D2G = E.poisson(H,DG)
        self.assertEqual(DG, {(4,2):2, (6,0):6})
        self.assertEqual(D2G, {(9,1):-48})
        self.assertTrue(E.exact_partner(H,G))
        self.assertTrue(E.exact_partner(H,DG))  # G is in S^1.
        self.assertFalse(E.exact_partner(H,D2G))  # G is not in S^2 or D_infinity.
        # The hbar^2 coefficient is -T3/24 in these conventions.
        self.assertEqual(E.defects(H,D2G), {2:{(10,0):3456}})
        self.assertEqual(V.T(V.q**4*V.p**2+V.q**6,
                                  -48*V.q**9*V.p,3), -82944*V.q**10)

if __name__ == '__main__':
    unittest.main(verbosity=2)
