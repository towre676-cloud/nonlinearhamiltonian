"""Exact closure, obstruction, reconstruction and counterexample checks."""
import copy
from fractions import Fraction as F
from math import factorial
import unittest

from compiler import (check_certificate, compile_family, controlled_generators,
                      finite_word_pullback, first_missing_image, hidden_cloud_witness,
                      physical_outputs, quadratic_backbone, residual_observable_bound)
from compiler import shared_backbone
from polynomial import (ONE, P, Q, add, decode, derivative, evaluate, monomial,
                        multiply, physical_lie, power, scale, substitute)


class ObservableTests(unittest.TestCase):
    def test_nonzero_and_zero_shear_dimensions(self):
        for c in [F(0), F(1), F(-3, 2), F(7, 11)]:
            certificate = compile_family(c)
            self.assertEqual(certificate['dimension'], 9 if c == 0 else 25)
            self.assertEqual(check_certificate(certificate)['status'], 'passed')

    def test_corrupt_action_and_output_rejected(self):
        certificate = compile_family()
        corrupt = copy.deepcopy(certificate)
        corrupt['actions']['cubic_transport'][0][0] = '1'
        with self.assertRaises(ValueError):
            check_certificate(corrupt)
        corrupt = copy.deepcopy(certificate)
        corrupt['output_coordinates']['p2'][0] = '999'
        with self.assertRaises(ValueError):
            check_certificate(corrupt)
        corrupt = copy.deepcopy(certificate)
        corrupt['basis'][0] = corrupt['basis'][1]
        with self.assertRaises(ValueError):
            check_certificate(corrupt)

    def test_physical_reconstruction_under_canonical_shear(self):
        for c in [F(0), F(2, 3), F(-3)]:
            outputs = physical_outputs(c)
            for q, p in [(F(2, 7), F(-5, 3)), (F(-1), F(4)), (F(0), F(2))]:
                adapted_p = p+c*q*q
                expected = {'one': 1, 'q': q, 'p': p, 'q2': q*q, 'qp': q*p, 'p2': p*p}
                for name, value in expected.items():
                    self.assertEqual(evaluate(outputs[name], q, adapted_p), value)

    def test_common_control_minimality_construction(self):
        c = F(5, 7)
        generators = controlled_generators()
        C = lambda f: physical_lie(generators['mu'], f)
        A = lambda f: physical_lie(generators['cubic_transport'], f)
        B = lambda f: physical_lie(generators['lambda'], f)
        p2 = physical_outputs(c)['p2']
        extracted = scale(add(C(C(p2)), C(p2), scale(p2, -2)), 1/(18*c*c))
        self.assertEqual(extracted, power(Q, 4))
        f = extracted
        for k in range(5):
            a, highest_p = 4-k, 2*k
            g = f
            for j in range(highest_p+1):
                expected = monomial(a, highest_p-j,
                    F(factorial(4), factorial(4-k))*(-1)**j*F(factorial(highest_p), factorial(highest_p-j)))
                self.assertEqual(g, expected)
                g = B(g)
            f = A(f)

    def test_quadrupole_general_infinite_closure_replay(self):
        A = lambda f: physical_lie(scale(power(P, 3), F(1, 3)), f)
        E = lambda f: physical_lie(power(Q, 2), f)
        commutator = lambda f: add(A(E(f)), scale(E(A(f)), -1))
        f = P
        for r in range(10):
            self.assertEqual(f, monomial(0, r+1, (-2)**r*factorial(r)))
            f = commutator(f)
        self.assertFalse(first_missing_image(compile_family(), power(Q, 2))['closed'])

    def test_physical_p2_general_infinite_closure_replay(self):
        for c in [F(1), F(-2, 3)]:
            A = lambda f: physical_lie(scale(power(P, 3), F(1, 3)), f)
            C = lambda f: physical_lie(multiply(Q, P), f)
            J = lambda f: physical_lie(physical_outputs(c)['p2'], f)
            ad1 = lambda f: add(C(J(f)), scale(J(C(f)), -1))
            ad2 = lambda f: add(C(ad1(f)), scale(ad1(C(f)), -1))
            projected = lambda f: scale(add(ad2(f), ad1(f), scale(J(f), -2)), F(1, 18))
            for n in range(1, 8):
                self.assertEqual(projected(power(P, n)), monomial(3, n-1, -4*c*c*n))
            E4 = lambda f: scale(projected(f), -1/(4*c*c))
            T = lambda f: A(A(A(E4(f))))
            f, coefficient = P, F(1)
            for r in range(7):
                self.assertEqual(f, monomial(0, 1+5*r, coefficient))
                f = T(f)
                coefficient *= 6*(1+5*r)
            self.assertFalse(first_missing_image(compile_family(c), physical_outputs(c)['p2'])['closed'])
        self.assertTrue(first_missing_image(compile_family(0), power(P, 2))['closed'])

    def test_positive_probability_missing_information_witness(self):
        for t in [F(0), F(1, 7), F(-3, 2)]:
            receipt = hidden_cloud_witness(t)
            self.assertEqual(F(receipt['future_expectation_plus_minus_difference']), -630*t)
            self.assertEqual(F(receipt['future_physical_second_moment_difference']), -F(70, 9)*t)
        self.assertEqual(F(hidden_cloud_witness()['future_physical_second_moment_difference']), -F(10, 9))

    def test_shared_shear_parameter_route_and_failure(self):
        records = [(2, 3, 4, 2), (3, 1, 6, 4), (0, 1, 0, 0)]
        self.assertTrue(shared_backbone(records, 1)['shared_shear_verified'])
        failed = shared_backbone(records, 2)
        self.assertFalse(failed['shared_shear_verified'])
        self.assertEqual(failed['remaining_Q2P_coefficient'], '-4')

    def test_completion_of_square_and_residual_support_bound(self):
        for a, b, c, d in [(F(2), F(3), F(4), F(2)), (F(-2), F(1), F(3), F(7)),
                           (F(1, 3), F(-2), F(1, 5), F(2, 7))]:
            certificate = quadratic_backbone(a, b, c, d)
            self.assertEqual(F(certificate['delta']), d-c*c/(4*a))
            if 4*a*d == c*c:
                self.assertTrue(certificate['quadratic'])
            f = add(monomial(2, 2), monomial(1, 3, F(-2, 3)))
            defect, bound = residual_observable_bound(f, F(certificate['delta']), 2, 3)
            for q in [F(-2), F(-1, 2), F(0), F(2)]:
                for p in [F(-3), F(1, 7), F(3)]:
                    self.assertLessEqual(abs(evaluate(defect, q, p)), bound)
        with self.assertRaises(ValueError):
            quadratic_backbone(0, 1, 1, 1)
        with self.assertRaises(ValueError):
            residual_observable_bound(P, 1, -1, 1)

    def test_finite_word_pullback_matches_individual_particles(self):
        c = F(2, 3)
        outputs = physical_outputs(c)
        maps = [(add(Q, scale(power(P, 2), F(1, 5))), P),
                (Q, add(P, monomial(0, 0, F(-2, 7)))) ,
                (scale(Q, F(3, 2)), scale(P, F(2, 3))),
                (add(Q, scale(power(P, 2), F(-2, 9))), P)]
        receipt = finite_word_pullback(outputs, maps)
        self.assertEqual(receipt['maximum_weight'], 8)
        for q, p in [(F(1), F(2)), (F(-2, 3), F(4, 5)), (F(0), F(-7, 3))]:
            qf, pf = q, p
            for q_image, p_image in maps:
                qf, pf = evaluate(q_image, qf, pf), evaluate(p_image, qf, pf)
            for name, poly in outputs.items():
                self.assertEqual(evaluate(decode(receipt['pulled_outputs'][name]), q, p),
                                 evaluate(poly, qf, pf))
        # A declared finite word remains exactly compilable after closure fails.
        extended_maps = maps+[(Q, add(P, scale(Q, F(-1, 3))))]+maps
        extended = finite_word_pullback(outputs, extended_maps)
        self.assertGreater(extended['maximum_weight'], 8)


if __name__ == '__main__':
    unittest.main()
