"""All-degree separable theorem regressions and supplied-certificate corruption tests."""
import copy
from fractions import Fraction as F
import json
from pathlib import Path
import subprocess
import sys
import unittest
from unittest import mock

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from partner_lab import parse
import separable_sixfold as C
import verify_separable_sixfold as V


class SeparableCoreTests(unittest.TestCase):
    def test_complete_independent_corpus(self):
        receipt = V.verify()
        self.assertEqual(receipt["status"], "PASS")
        self.assertEqual(receipt["classified_inputs"], 15)
        self.assertEqual(receipt["potential_degrees"], [5, 6, 7, 8])
        self.assertEqual(json.loads(json.dumps(receipt)), receipt)

    def test_sixfold_wrapper_preserves_scope(self):
        for expression in ("q^5+p^3", "q^7+p^4", "q^8+p^3"):
            H = parse(expression)
            self.assertEqual(C.classify_separable(H)["status"], "classified")
            self.assertEqual(C.classify_separable_sixfold(H)["status"], "out_of_scope")
        H = parse("q^6+p^3")
        self.assertEqual(C.classify_separable(H), C.classify_separable_sixfold(H))

    def test_scope_rejects_mixed_and_other_complements(self):
        for expression in ("q^6+p^3+q*p", "q^6+(q+1)*p^3", "q^6+p^5", "q^6+p^2", "q^6+p^6", "q^4+p^3"):
            with self.subTest(H=expression):
                H = parse(expression)
                self.assertEqual(C.classify_separable(H)["status"], "out_of_scope")
                self.assertIsNone(V.normalize(H))

    def test_exact_input_contract(self):
        for bad in (None, {(6, 0): 1.0, (0, 3): 1}, {(6, 0): True}, {(True, 5): 1}, {(-1, 7): F(1)}):
            with self.subTest(H=bad):
                with self.assertRaises((TypeError, ValueError)):
                    C.classify_separable(bad)

    def test_least_depth_witness_identities(self):
        for n in (5, 6, 7, 8):
            f = parse(f"q^{n}+2*q^3-q")
            for m in (3, 4):
                g = parse(f"3*p^{m}+2*p^2-p")
                H = V.E.add(f, g)
                q = parse("q")
                dq = V.E.poisson(H, q)
                if m == 3:
                    self.assertFalse(V.E.defects(H, dq))
                    d2q = V.E.poisson(H, dq)
                    actual = V.E.scale(V.E.defects(H, d2q)[2], -24)
                    expected = V.E.multiply(V.E.derivative(g, p=3),
                                           V.E.multiply(V.E.derivative(f, q=4), V.E.derivative(g, p=2)))
                else:
                    actual = V.E.scale(V.E.defects(H, dq)[2], -24)
                    expected = V.E.scale(V.E.multiply(V.E.derivative(f, q=3), V.E.derivative(g, p=4)), -1)
                self.assertEqual(actual, expected)
                self.assertTrue(actual)

    def test_supplied_verification_does_not_call_producer(self):
        H = parse("q^6+p^3+2*p^2-q")
        report = C.classify_separable(H)
        with mock.patch.object(C, "classify_separable", side_effect=AssertionError("producer called")):
            self.assertEqual(V.check_report(H, report)["status"], "PASS")

    def test_independent_normalizer_preserves_input(self):
        H = parse("q^6/3+2*p^3-7*p^2+q")
        before = dict(H)
        self.assertIsNotNone(V.normalize(H))
        self.assertEqual(H, before)
        self.assertTrue(all(type(value) is F for value in H.values()))

    def test_suppressed_or_corrupted_claims_rejected(self):
        H = parse("q^6+p^3+2*p^2-q")
        original = C.classify_separable(H)
        def missing_stage(r):
            r["classification"]["stages"].pop(1)
        def missing_core(r):
            r["classification"]["Dinf"]["basis"] = r["classification"]["Dinf"]["basis"][:1]
            r["classification"]["Dinf"]["dimension"] = 1
        def hidden_static(r):
            space = r["classification"]["stages"][0]["space"]
            space["basis"].pop()
            space["dimension"] -= 1
        mutations = [
            missing_stage, missing_core, hidden_static,
            lambda r: r.update(status="unsupported"),
            lambda r: r["classification"]["depth"].update(value=True),
            lambda r: r["classification"]["depth"].update(value=1),
            lambda r: r["classification"]["coordinates"].update(determinant="0"),
            lambda r: r["classification"]["normal_form"].update(f=[]),
            lambda r: r["classification"]["normal_form"].update(degree_g=4),
            lambda r: r["classification"].update(drop_witnesses=[]),
            lambda r: r["classification"].update(sharpness_witness=None),
            lambda r: r["classification"]["drop_witnesses"][0].update(DiG=[]),
            lambda r: r["classification"]["drop_witnesses"][0].update(T3=[]),
            lambda r: r["proof_boundary"].update(formalized=True),
        ]
        for index, mutate in enumerate(mutations):
            with self.subTest(mutation=index):
                report = copy.deepcopy(original)
                mutate(report)
                with self.assertRaises(V.VerificationError):
                    V.check_report(H, report)

    def test_corruption_rejection_under_optimized_python(self):
        code = """
import sys
sys.path[:0]=[sys.argv[1],sys.argv[2]]
from partner_lab import parse
from separable_sixfold import classify_separable
from verify_separable_sixfold import check_report,VerificationError
H=parse('q^6+p^4')
r=classify_separable(H)
r['classification']['stages'][0]['space']['basis'].pop()
r['classification']['stages'][0]['space']['dimension']-=1
try: check_report(H,r)
except VerificationError: pass
else: raise RuntimeError('corruption accepted')
"""
        subprocess.run([sys.executable, "-O", "-c", code, str(HERE.parent), str(HERE)], check=True)


if __name__ == "__main__":
    unittest.main()
