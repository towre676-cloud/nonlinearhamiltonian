"""Full exact replay, hostile-certificate rejection, and covariance regression."""
import copy
import json
from pathlib import Path
import unittest
import sympy as s
import verify_squarefree as V


class SquarefreeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads((Path(__file__).parent/'squarefree_certificate.json').read_text())
        cls.discriminant = V.unpack(cls.data['discriminant'])

    def test_all_sixteen_exact_discriminant_identities(self):
        result = V.verify(self.data, progress=False)
        self.assertEqual(result['degrees'], 16)
        self.assertEqual(result['discriminant_power'], 1)

    def test_missing_degree_rejected(self):
        data = copy.deepcopy(self.data)
        data['records'].pop()
        with self.assertRaises(V.CertificateError):
            V.verify(data, progress=False)

    def test_false_discriminant_rejected(self):
        data = copy.deepcopy(self.data)
        data['discriminant'] = []
        with self.assertRaises(V.CertificateError):
            V.verify(data, progress=False)

    def test_corrupted_ideal_identity_rejected(self):
        record = copy.deepcopy(self.data['records'][0])
        record['derived'][0]['polynomial'] = []
        with self.assertRaises(V.CertificateError):
            V.verify_record(record, self.discriminant)

    def test_circular_identity_rejected(self):
        record = copy.deepcopy(self.data['records'][0])
        record['derived'][0]['terms'][0][0] = len(record['minor_rows'])
        with self.assertRaises(V.CertificateError):
            V.verify_record(record, self.discriminant)

    def test_missing_resonant_pivot_rejected(self):
        record = copy.deepcopy(self.data['records'][1])
        record['pivot_rows'] = []
        with self.assertRaises(V.CertificateError):
            V.verify_record(record, self.discriminant)

    def test_changed_kernel_reconstruction_rejected(self):
        record = copy.deepcopy(self.data['records'][1])
        record['kernel_lift'][2][0] = []
        with self.assertRaises(V.CertificateError):
            V.verify_record(record, self.discriminant)

    def test_wrong_minor_order_rejected(self):
        record = copy.deepcopy(self.data['records'][0])
        record['minor_rows'][0] = record['minor_rows'][0][:1]
        with self.assertRaises(V.CertificateError):
            V.verify_record(record, self.discriminant)

    def test_gl2_covariance_including_first_iterate(self):
        q, p = V.q, V.p
        h = q*p**5+2*q**3*p**3+3*q**4*p**2+5*q**5*p+7*q**6
        g = p**3+q**2*p
        substitution = {q: 2*q+p, p: 3*q+4*p}  # determinant 5
        pull = lambda f: s.expand(f.subs(substitution, simultaneous=True))
        for k in (1, 3, 5):
            self.assertEqual(s.expand(V.transvectant(pull(h), pull(g), k)
                                     - 5**k*pull(V.transvectant(h, g, k))), 0)
        for k in (3, 5):
            self.assertEqual(s.expand(V.transvectant(pull(h), V.transvectant(pull(h), pull(g), 1), k)
                                     - 5**(k+1)*pull(V.transvectant(h, V.transvectant(h, g, 1), k))), 0)

    def test_nonsplit_squarefree_discriminant(self):
        # H=q(p^5+q^5) has six distinct geometric roots; no rational splitting is assumed.
        self.assertEqual(self.discriminant.subs({V.a: 0, V.b: 0, V.c: 0, V.d: 1}), 3125)
        self.assertNotEqual(s.discriminant(s.Symbol('x')**6+1, s.Symbol('x')), 0)

    def test_elimination_recovers_known_fourfold_failure(self):
        q, p = V.q, V.p
        h = q*(p-q/8)**4*(p+q/2)
        g = (p-q/8)*(p+9*q/8)
        dg = V.transvectant(h, g, 1)
        d2g = V.transvectant(h, dg, 1)
        for f in (g, dg):
            for k in (3, 5):
                self.assertEqual(V.transvectant(h, f, k), 0)
        expected = -s.Rational(2025, 134217728)*(8*p-q)**10
        self.assertEqual(s.expand(V.transvectant(h, d2g, 3)-expected), 0)
        self.assertNotEqual(s.expand(expected), 0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
