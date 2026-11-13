import json, os, unittest
from fractions import Fraction as Fr
import exact_observation as EO
import weighted_cubic_form as W
import period_valuation_transfer as PV

HERE = os.path.dirname(os.path.abspath(__file__))


class Engine(unittest.TestCase):
    def test_certificate_roundtrip_and_tamper(self):
        s = EO.ObservationSystem("abc", [("r1", 3, [1, 1, 0]), ("r2", 1, [1, 0, 0]), ("r3", 1, [0, 1, 0]), ("r4", 5, [2, 2, 0])])
        c = s.certificate()
        self.assertEqual((c["rank"], c["panel"], c["panel_cost"]), (2, [1, 2], "2"))
        self.assertEqual(len(EO.verify_certificate(c)), 3)
        bad = json.loads(json.dumps(c)); bad["panel"] = [0, 3]
        self.assertRaises(AssertionError, EO.verify_certificate, bad)
        costly = json.loads(json.dumps(c)); costly["panel"] = [0, 1]; costly["panel_cost"] = "4"
        costly["pivot_minor_determinant"] = "-1"
        self.assertRaises(AssertionError, EO.verify_certificate, costly)
        hidden = json.loads(json.dumps(c)); hidden["kernel_witnesses"] = [["1", "-1", "0"]]
        self.assertRaises(AssertionError, EO.verify_certificate, hidden)

    def test_inexact_input_rejected(self):
        self.assertRaises(TypeError, EO.ObservationSystem, "a", [("r", 1, [0.5])])

    def test_amplification(self):
        s = EO.ObservationSystem("ab", [("r1", 1, [1, 1]), ("r2", 1, [1, Fr(101, 100)])])
        self.assertEqual(s.amplification([0, 1]), 201)


class Hamiltonian(unittest.TestCase):
    def test_strata(self):
        for pt in [(1, 2, 3), (0, 2, 3), (3, 1, 3), (Fr(3, 2), 3, 2), (-6, 3, 1), (0, 0, 5)]:
            self.assertEqual(W.dims(*pt), W.predicted_dims(*pt), pt)

    def test_weight12_gate_certificate_is_E12(self):
        # off E12 the seven weight-12 gate rows identify all seven coefficients; on it one witness appears
        s = W.gate_system(W.hamiltonian(1, 2, 3), W.weight_basis(12), 0)
        c = s.certificate(); EO.verify_certificate(c); self.assertEqual(c["rank"], 7)
        s = W.gate_system(W.hamiltonian(3, 1, 3), W.weight_basis(12), 0)
        c = s.certificate(); EO.verify_certificate(c); self.assertEqual((c["rank"], len(c["kernel_witnesses"])), (6, 1))

    def test_cubic_regression(self):
        self.assertEqual(W.dims(0, 0, 1, {(3, 0): 1, (2, 1): 3, (1, 2): 3}), [15, 4, 2])
        self.assertEqual(W.dims(0, 0, 1, {(3, 0): 1, (2, 1): 2, (1, 2): 3}), [15, 3, 2])

    def test_cube_tail(self):
        h = W.hamiltonian(3, 3, 1)
        self.assertTrue(all(len(W.gate_system(h, W.weight_basis(w), 0).witnesses()) == 1 for w in range(10, 31, 2)))
        self.assertTrue(W.is_cube(6, 12, 8) and not W.is_cube(3, 3, 2))

    def test_lower_terms_checked(self):
        self.assertRaises(ValueError, W.hamiltonian, 1, 1, 1, {(4, 1): 1})


class Periods(unittest.TestCase):
    def test_weight_51_collision(self):
        left, right = (1, 1, 1, 1, 1, 5, 5, 12, 24), (2, 2, 2, 2, 3, 3, 12, 25)
        self.assertTrue(PV.collision_report(left, right, 2)["indistinguishable"])
        r3 = PV.collision_report(left, right, 3)
        self.assertFalse(r3["indistinguishable"]); self.assertEqual(r3["cheapest_separator"][0], 3)

    def test_direct_coefficients_agree_with_valuations(self):
        from math import factorial
        def coeff(w, m):
            v = factorial(m * sum(w))
            for a in w:
                v //= factorial(m * a)
            return v
        left, right = (1, 1, 1, 1, 1, 5, 5, 12, 24), (2, 2, 2, 2, 3, 3, 12, 25)
        self.assertEqual([coeff(left, m) == coeff(right, m) for m in (1, 2, 3)], [True, True, False])

    def test_kernel_and_panel_certificate(self):
        s = PV.valuation_system(12, 1)
        c = s.certificate(); EO.verify_certificate(c)
        self.assertEqual(c["rank"] + len(c["kernel_witnesses"]), 12)
        # weight 9 one-coefficient ambiguity is a kernel vector
        u = PV.difference_vector((1, 1, 1, 3, 3), (1, 2, 2, 2, 2), 12)
        self.assertEqual(sum(a * b for a, b in zip(u, range(1, 13))), 0)


class Sensors(unittest.TestCase):
    """Third client: the 7x7 reader matrix of Singularity's volume-eight certificate
    (independent_checks/height_series/vol8_reader_certificate.json at d18fbb2), embedded verbatim."""
    PANEL = [2, 6, 8, 18, 22, 28, 30]
    MATRIX = [[0, 0, 0, 1, -12, 0, 0], [0, 1, -10, 55, -220, 0, 0], [1, -9, 45, -165, 495, 0, 3],
              [-56, 84, -120, 165, -220, -70, -84], [-8, 9, -10, 11, -12, 14, 18],
              [0, 0, 0, 0, 0, 5, 6], [0, 0, 0, 0, 0, -1, -1]]

    def test_volume_eight_reader_gain(self):
        s = EO.ObservationSystem(range(7), [(("coeff", e), 1, r) for e, r in zip(self.PANEL, self.MATRIX)])
        self.assertEqual(EO.det(self.MATRIX), 224000)
        self.assertEqual(s.amplification(list(range(7))), Fr(133, 10))
        EO.verify_certificate(s.certificate())


class QuarticEdge(unittest.TestCase):
    def test_strata(self):
        import quartic_edge as QE
        for pt in [(1, 3), (0, 3), (12, 6), (6, -6), (4, Fr(3, 2)), (4, Fr(-3, 5)), (2, Fr(-1, 10)), (2, 1)]:
            self.assertEqual(QE.dims(*pt), QE.predicted_dims(*pt), pt)

    def test_square_locus_has_no_tail_and_weights_checked(self):
        import quartic_edge as QE
        h = QE.hamiltonian(2, 1)
        self.assertFalse(any(QE.gate_system(h, QE.weight_basis(w), 0).witnesses() for w in range(21, 61) if QE.weight_basis(w)))
        self.assertRaises(ValueError, QE.hamiltonian, 1, 1, {(3, 2): 1})


class GenericStratum(unittest.TestCase):
    def test_leading_form_and_full_family(self):
        import generic_sixfold_stratum as GS
        self.assertEqual(GS.dims(GS.hamiltonian(1)), [10, 2, 2])
        basis, ker = GS.refinement(GS.hamiltonian(Fr(-7, 3)), 0)
        support = sorted({basis[i] for v in ker for i, c in enumerate(v) if c})
        self.assertEqual(support, sorted([(a, b) for a in range(3) for b in range(3)] + [(6, 0), (0, 5)]))
        full = GS.hamiltonian(Fr(2, 3), {m: Fr((3 * m[0] + 5 * m[1]) % 7 - 3, 2) for m in GS.LOWER})
        d = GS.dims(full)
        self.assertTrue(d[0] <= 10 and d[1:] == [2, 2])
        self.assertRaises(ValueError, GS.hamiltonian, 0)


if __name__ == "__main__":
    unittest.main()
