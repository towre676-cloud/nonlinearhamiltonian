"""Fast regressions for QUADRATIC_SIXFOLD_THEOREM.md (one case per regime).

The full fifteen-case replay with covariance is verify_quadratic_sixfold.py.
"""
import json
from pathlib import Path
import subprocess
import sys
import unittest
from fractions import Fraction as F

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import verify_quadratic_sixfold as Q


class QuadraticSixfoldTests(unittest.TestCase):
    def run_case(self, index, dims, sharp, core):
        name, f, b = Q.CASES[index]
        report = Q.check_case(name, f, b, 6, len(dims) - 1)
        self.assertEqual(report["bounded_dimensions"], dims)
        self.assertEqual(report["sharp_depth"], sharp)
        self.assertEqual(report["core_dimension"], core)

    def test_calibration(self):
        self.run_case(0, [18, 14, 10, 6, 4, 2, 2], 5, 2)

    def test_generic_nonlinear(self):
        self.run_case(3, [15, 10, 6, 4, 2, 2], 4, 2)
        self.run_case(13, [14, 10, 6, 4, 2, 2], 4, 2)

    def test_cubic_potential_depth_six(self):
        self.run_case(9, [14, 10, 6, 5, 4, 3, 2, 2], 6, 2)

    def test_hidden_quadratic_core(self):
        self.run_case(12, [14, 10, 6, 6, 6], 2, 6)

    def test_wrong_space_is_rejected(self):
        name, f, b = Q.CASES[9]
        original = Q.SHARP_DEPTH["cubic_potential"]
        Q.SHARP_DEPTH["cubic_potential"] = 4
        try:
            with self.assertRaises(Q.V.VerificationError):
                Q.check_case(name, f, b, 6, 2)
        finally:
            Q.SHARP_DEPTH["cubic_potential"] = original

    def test_committed_receipt(self):
        path = Path(__file__).with_name("QUADRATIC_SIXFOLD_REPLAY.json")
        receipt = json.loads(path.read_text())
        self.assertEqual(receipt["status"], "PASS")
        self.assertEqual(len(receipt["cases"]), 15)
        self.assertEqual(len(receipt["rational_affine_covariance"]), 5)
        self.assertEqual(receipt["source_sha256"], Q.source_hashes())
        self.assertEqual([row["dimension"] for row in receipt["static_probes"]],
                         [28, 28, 26, 26, 26, 26])
        self.assertEqual(
            [c["regime"] for c in receipt["cases"]], Q.EXPECTED_REGIME)

    def test_static_extras(self):
        name, f, b = Q.CASES[4]
        f, b = Q.uni(f), Q.uni(b)
        H = Q.hamiltonian(f, b)
        extras = Q.static_extras(f, b)
        self.assertEqual([Q.V.total_degree(G) for G in extras], [6, 10])
        self.assertEqual([Q.first_failure(H, G) for G in extras], [1, 1])
        self.assertEqual(Q.static_extras(f, Q.uni(Q.CASES[5][2])), [])


class ClassifierTests(unittest.TestCase):
    def classify(self, text):
        import partner_lab
        import quadratic_sixfold as C
        return C.classify_quadratic_sixfold(partner_lab.parse(text))

    def test_regimes(self):
        expected = {
            "q^6+p^2": ("affine_shift", 5, 2),
            "q^6+q^2*p+p^2": ("generic_nonlinear", 4, 2),
            "(p+q^3)^2+q^3": ("cubic_potential", 6, 2),
            "(p+q^3)^2": ("hidden_quadratic", 2, 6),
            "(q+2*p)^6+3*q^2+q*p": ("affine_shift", 5, 2),
            "p^6+q^2+p^3*q": ("generic_nonlinear", 4, 2),
            "q^6+q*p^2": ("variable_top_coefficient", 3, 2),
            "q^6+(q^3+q+1)*p^2": ("variable_top_coefficient", 1, 2),
            "q^6+q^2*p^2+2*q^4*p": ("variable_top_coefficient", 1, 3),
            "q^6+q^2*p^2+2*q^4*p+q": ("variable_top_coefficient", 2, 2),
        }
        for text, (regime, depth, core) in expected.items():
            report = self.classify(text)
            self.assertEqual(report["status"], "classified", text)
            self.assertEqual((report["regime"], report["least_depth"],
                              report["Dinf"]["dimension"]), (regime, depth, core), text)
            self.assertEqual(json.loads(json.dumps(report)), report)

    def test_out_of_scope_makes_no_claims(self):
        for text in ("q^6+p^3", "q^6+q*p", "q^6+p^6+p^2", "q^4+p^2", "q^6+q*p^3+p^2"):
            report = self.classify(text)
            self.assertEqual(report["status"], "out_of_scope", text)
            self.assertNotIn("stages", report)
            self.assertNotIn("Dinf", report)

    def test_committed_models_receipt(self):
        path = Path(__file__).with_name("QUADRATIC_SIXFOLD_MODELS_REPLAY.json")
        receipt = json.loads(path.read_text())
        self.assertEqual(receipt["status"], "PASS")
        self.assertEqual([m["dimensions_S1_to_S4"] for m in receipt["certified_models"]],
                         [[6, 3, 2, 2], [5, 3, 2, 2], [3, 2, 2, 2], [3, 2, 2, 2], [3, 2, 2, 2]])
        self.assertEqual(receipt["discriminant_family"]["S2_exceptional_factor"],
                         "(t - 2)*(t + 2)")
        self.assertEqual(len(receipt["classifier_checks"]), 30)
        self.assertEqual(receipt["source_sha256"],
                         Q.source_hashes(Path(__file__).with_name("verify_quadratic_sixfold_models.py"),
                                         Path(__file__).resolve().parents[1] / "quadratic_sixfold.py"))

    def test_theorem_e_criterion(self):
        base = "((q-3)*p+2*(q-3)^3+q+2)^2"
        for text, square in ((base, True), ("3*" + base + "-7", True), (base + "+p^2", False),
                             (base + "+p", False), (base + "+q^2", False),
                             (base + "+(q-3)*p", False), ("q^6+q^2*p^2+q^4*p", False)):
            report = self.classify(text)
            self.assertEqual(report["square_first_integral"] is not None, square, text)
            self.assertEqual(report["Dinf"]["dimension"], 3 if square else 2, text)

    def test_sharpness_witnesses(self):
        for text in ("q^6+p^2", "(p+q^3)^2+q^3", "(p+q^3)^2", "q^6+q*p^2",
                     "q^6+(q^3+q+1)*p^2", "q^6+q^2*p^2+2*q^4*p"):
            import partner_lab
            report = self.classify(text)
            witness = report["sharpness_witness"]
            G = Q.V.polynomial(witness["G"])
            self.assertEqual(Q.first_failure(partner_lab.parse(text), G),
                             report["least_depth"], text)
            self.assertEqual(witness["first_failing_iterate"], report["least_depth"])


class SchemaTwoTests(unittest.TestCase):
    def test_schema_one_is_unchanged_and_default(self):
        import partner_lab
        H = partner_lab.parse("q^6+q+p+p^2")
        self.assertEqual(Q.V.C.classify_sextic(H)["status"], "unsupported")
        self.assertEqual(Q.V.C.classify_sextic(H)["schema"], "hamiltonian-sextic-core/1")
        cli = Path(__file__).resolve().parents[1] / "partner_lab.py"
        for flags, status, code in (([], "unsupported", 2), (["--schema", "2"], "classified", 0)):
            result = subprocess.run([sys.executable, str(cli), "sextic-core", "--H",
                                     "q^6+q+p+p^2", *flags], capture_output=True, text=True)
            self.assertEqual(result.returncode, code, result.stderr)
            self.assertEqual(json.loads(result.stdout)["status"], status)

    def test_stage_kinds_and_unknown_static_stage(self):
        import partner_lab
        import verify_sextic_core_v2 as W
        cases = {
            "q^6+p^2": ["polynomial_family", "module_plus_finite", "module_plus_finite",
                        "finite_basis", "finite_basis", "finite_basis"],
            "q^6+q^2*p+p^2": ["module_plus_finite", "module_plus_finite", "finite_basis",
                              "finite_basis", "finite_basis"],
            "q^6+q*p^2": [None, "finite_basis", "finite_basis", "finite_basis"],
        }
        for text, kinds in cases.items():
            H = partner_lab.parse(text)
            report = Q.V.C.classify_sextic_v2(H)
            stages = report["classification"]["stages"]
            self.assertEqual([None if s["space"] is None else s["space"]["kind"]
                              for s in stages], kinds, text)
            self.assertEqual(report["classification"]["depth"],
                             {"value": len(kinds) - 1, "kind": "least"})
            W.check_report_v2(H, report)
        self.assertEqual(stages[0]["status"], "unknown")
        self.assertTrue(stages[0]["reason"])

    def test_schema_one_results_carry_over(self):
        import verify_sextic_core_v2 as W
        H = {(4, 2): F(1), (6, 0): F(1)}
        first, second = Q.V.C.classify_sextic(H), Q.V.C.classify_sextic_v2(H)
        spaces = second["classification"]
        self.assertEqual(spaces["stages"][1]["space"], first["classification"]["S1"])
        self.assertEqual(spaces["Dinf"], first["classification"]["Dinf"])
        self.assertEqual(spaces["obstruction"], first["obstruction"])
        self.assertEqual(spaces["depth"]["kind"], "sufficient")
        W.check_report_v2(H, second)

    def test_committed_v2_receipt(self):
        import verify_sextic_core_v2 as W
        path = Path(__file__).with_name("SEXTIC_CORE_V2_REPLAY.json")
        receipt = json.loads(path.read_text())
        self.assertEqual(receipt["status"], "PASS")
        self.assertEqual(receipt["schema_1_derived_checks"], 27)
        self.assertEqual(len(receipt["quadratic_complement_checks"]), 23)
        self.assertEqual(receipt["corrupted_reports_rejected"], 8)
        self.assertEqual(receipt["source_sha256"],
                         Q.source_hashes(Path(W.__file__).resolve(),
                                         Path(__file__).resolve().parents[1] / "quadratic_sixfold.py"))


if __name__ == "__main__":
    unittest.main()
