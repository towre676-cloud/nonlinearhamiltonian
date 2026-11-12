"""Mixed weighted-family completeness, scope, and supplied-certificate tests."""
import copy
from fractions import Fraction as F
from pathlib import Path
import subprocess
import sys
import unittest
from unittest import mock

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from partner_lab import parse
import weighted_separable as C
import verify_weighted_separable as V


class WeightedSeparableTests(unittest.TestCase):
    def test_independent_mixed_corpus(self):
        receipt = V.verify()
        self.assertEqual(receipt["status"], "PASS")
        self.assertEqual(receipt["classified_inputs"], 15)
        self.assertEqual({item["potential_degree"] for item in receipt["checks"]}, {5, 6, 7, 8})

    def test_cubic_first_space_can_have_all_three_dimensions(self):
        for expression, dimensions in (
                ("q^6+p^3+q*p", [15, 4, 2]),
                ("q^6+p^3+q*p^2", [15, 3, 2]),
                ("q^6+p^3+q^3*p", [15, 2]),
                ("q^6+p^4+q*p^3", [10, 2]),
                ("q^6+p^4+q^4*p+q^2*p^2", [9, 2])):
            with self.subTest(H=expression):
                H = parse(expression)
                report = C.classify_weighted_separable(H)
                self.assertEqual(V.check_report(H, report)["stage_dimensions"], dimensions)

    def test_strict_weight_boundary_and_nonzero_edge_coefficients(self):
        for expression in ("q^6+p^3+q^4*p", "q^6+p^3+q^2*p^2", "q^6+p^4+q^3*p^2",
                           "q^6+q*p^3", "q^6+p^5", "q^6", "q^4+p^3"):
            with self.subTest(H=expression):
                H = parse(expression)
                self.assertEqual(C.classify_weighted_separable(H)["status"], "out_of_scope")
                self.assertIsNone(V.normalize(H))

    def test_normalizer_preserves_fraction_inputs(self):
        H = parse("q^6/3-2*p^3+q*p^2/5")
        before = dict(H)
        self.assertIsNotNone(V.normalize(H))
        self.assertEqual(H, before)
        self.assertTrue(all(type(value) is F for value in H.values()))

    def test_supplied_certificate_is_checked_without_producer(self):
        H = parse("q^6+p^4+q*p^3")
        report = C.classify_weighted_separable(H)
        with mock.patch.object(C, "classify_weighted_separable", side_effect=AssertionError("producer called")):
            self.assertEqual(V.check_report(H, report)["status"], "PASS")

    def test_higher_degree_checks_all_odd_gates(self):
        H = parse("q^8+p^4+q*p^3")
        report = C.classify_weighted_separable(H)
        self.assertEqual(set(report["classification"]["drop_witnesses"][0]["gates"]), {"3", "5", "7"})
        self.assertEqual(V.check_report(H, report)["potential_degree"], 8)
        report["classification"]["drop_witnesses"][0]["gates"].pop("7")
        with self.assertRaisesRegex(V.VerificationError, "odd-gate"):
            V.check_report(H, report)
        self.assertEqual(C.classify_weighted_separable_sixfold(H)["status"], "out_of_scope")

    def test_corrupted_envelope_and_stage_claims_rejected(self):
        H = parse("q^6+p^3+q*p^2")
        original = C.classify_weighted_separable(H)
        def incomplete_static(r):
            space = r["classification"]["stages"][0]["space"]
            space["basis"].pop()
            space["dimension"] -= 1
        mutations = [
            incomplete_static,
            lambda r: r["classification"]["weighted_model"].update(static_bound=9),
            lambda r: r["classification"]["weighted_model"]["weights"].update(M=3),
            lambda r: r["classification"]["weighted_model"].update(lower=[]),
            lambda r: r["classification"]["weighted_model"].update(leading=[]),
            lambda r: r["classification"]["depth"].update(value=1),
            lambda r: r["classification"]["stages"].pop(1),
            lambda r: r["classification"].update(drop_witnesses=[]),
            lambda r: r["classification"]["drop_witnesses"][0].update(DiG=[]),
            lambda r: r["classification"]["drop_witnesses"][0]["gates"].update({"3": []}),
            lambda r: r["proof_boundary"].update(formalized=True),
        ]
        for index, mutate in enumerate(mutations):
            with self.subTest(mutation=index):
                report = copy.deepcopy(original)
                mutate(report)
                with self.assertRaises(V.VerificationError):
                    V.check_report(H, report)

    def test_corruption_rejected_under_optimized_python(self):
        code = """
import sys
sys.path[:0]=[sys.argv[1],sys.argv[2]]
from partner_lab import parse
from weighted_separable import classify_weighted_separable
from verify_weighted_separable import check_report,VerificationError
H=parse('q^6+p^4+q*p^3')
r=classify_weighted_separable(H)
r['classification']['weighted_model']['static_bound']=15
try: check_report(H,r)
except VerificationError: pass
else: raise RuntimeError('corruption accepted')
"""
        subprocess.run([sys.executable, "-O", "-c", code, str(HERE.parent), str(HERE)], check=True)


if __name__ == "__main__":
    unittest.main()
