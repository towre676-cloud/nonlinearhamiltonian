"""Adversarial tests of the supplied-report boundary and independent replay.

The producer supplies fixtures only.  Verification is tested with every producer
classification entry point disabled, and with coherent omissions that ordinary
spot checks can accept.
"""
import copy
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import verify_sextic_report as R

sys.path.insert(0, str(R.HERE.parent))
import partner_lab as P
import sextic_core as C


def valid_cases():
    cases = [(name, H, C.classify_sextic(H)) for name, _, H, _ in R.V.fixtures()]
    examples = [
        ("zero", "0", 1),
        ("infinite_affine", "q^6+q^3*p+q", 1),
        ("fivefold_affine", "q^5*p+q^3+p", 1),
        ("nonsplit_composition", "(q^2+p^2+q)^3+2*(q^2+p^2+q)", 1),
        ("fourfold_lift", "q^4*p^2+q^3", 1),
        ("no_fourfold_lift", "q^4*p^2+q^6+p^3", 1),
        ("schema2_adapter", "q^4*p^2+q^3", 2),
        ("constant_affine", "q^6+p^2", 2),
        ("constant_quadratic_b", "q^6+q^2*p+p^2", 2),
        ("constant_cubic_potential", "(p+q^3)^2+q^3", 2),
        ("constant_hidden_quadratic", "(p+q^3)^2+q^2", 2),
        ("variable_linear", "q^6+q*p^2", 2),
        ("variable_linear_high_b", "q^6+q*p^2+q^4*p", 2),
        ("variable_quadratic", "q^6+q^2*p^2", 2),
        ("variable_cubic", "q^6+(q^3+q+1)*p^2", 2),
        ("variable_square", "(q*p+q^3)^2", 2),
        ("unsupported_schema1", "q^6+p^2", 1),
        ("unsupported_schema2", "q^5*p+p^2", 2),
        ("unsupported_complement_five", "q^6+p^5", 2),
        ("zero_schema2", "0", 2),
        ("separable_cubic", "q^6+p^3", 2),
        ("separable_quartic", "q^6+p^4", 2),
        ("separable_transformed", "(2*q+p)^6+(q-3*p)^3+q-3*p", 2),
        ("weighted_cubic_four", "q^6+p^3+q*p", 2),
        ("weighted_cubic_three", "q^6+p^3+q*p^2", 2),
        ("weighted_cubic_two", "q^6+p^3+q^3*p", 2),
        ("weighted_quartic", "q^6+p^4+q^4*p+q^2*p^2", 2),
        ("weighted_transformed", "-2/3*((2*q+3*p+1)^6+(q-2*p-3)^3+(2*q+3*p+1)*(q-2*p-3)^2)", 2),
    ]
    for name, text, schema in examples:
        H = P.parse(text)
        cases.append((name, H, C.classify_sextic(H, schema=schema)))
    H = R.V.affine_substitute(P.parse("q^6+q^2*p^2"), ((2, 1), (-1, 2)), (1, -2), F(-2, 3))
    cases.append(("variable_affine_coordinates", H, C.classify_sextic(H, schema=2)))
    return cases


def corruptions(cases):
    by_name = {name: (H, report) for name, H, report in cases}

    def changed(name, case, path, value=None, *, delete=False):
        H, original = by_name[case]
        report = copy.deepcopy(original)
        obj = report
        for key in path[:-1]:
            obj = obj[key]
        if delete:
            del obj[path[-1]]
        else:
            obj[path[-1]] = value
        return name, H, report

    tests = [
        ("wrong_input", "fourfold_lift", ("input", 0, "coefficient"), "9"),
        ("wrong_degree", "fourfold_lift", ("degree",), 5),
        ("boolean_degree", "fourfold_lift", ("degree",), True),
        ("false_homogeneity", "fourfold_lift", ("homogeneous",), True),
        ("unknown_schema", "fourfold_lift", ("schema",), "hamiltonian-sextic-core/3"),
        ("suppressed_classification", "fourfold_lift", ("status",), "unsupported"),
        ("invented_support", "unsupported_schema2", ("status",), "classified"),
        ("false_method", "fourfold_lift", ("classification", "method"), "homogeneous"),
        ("false_family", "fourfold_lift", ("classification", "family"), "multiplicity_6"),
        ("formalization_overclaim", "fourfold_lift", ("proof_boundary", "formalized"), True),
        ("missing_theorem_dependencies", "fourfold_lift", ("proof_boundary", "dependencies"), []),
        ("changed_convention", "fourfold_lift", ("proof_boundary", "definitions"), "D=-T1"),
        ("path_injection", "fourfold_lift", ("proof_boundary", "dependencies"), [R.THEOREM, R.EXTENSION, "../../outside"]),
        ("infinity_convention", "fourfold_lift", ("leading", "infinity_point"), "[0:1]"),
        ("dehomogenization_convention", "fourfold_lift", ("leading", "dehomogenization"), "H6(1,t)"),
        ("boolean_infinity", "fourfold_lift", ("leading", "infinity_multiplicity"), False),
        ("factor_scalar", "fourfold_lift", ("leading", "factorization", "coefficient"), "7"),
        ("decimal_rational", "fourfold_lift", ("input", 0, "coefficient"), "1.0"),
        ("boolean_exponent", "fourfold_lift", ("input", 0, "q"), True),
        ("negative_exponent", "fourfold_lift", ("input", 0, "p"), -1),
        ("float_dimension", "fourfold_lift", ("classification", "S1", "dimension"), 3.0),
        ("missing_obstruction", "fourfold_lift", ("obstruction",), None),
        ("false_obstruction", "fourfold_lift", ("obstruction", "T3"), []),
        ("wrong_lift_column_names", "fourfold_lift", ("quadratic_lift", "system", "unknowns"), ["beta", "alpha"]),
        ("boolean_lift_rank", "fourfold_lift", ("quadratic_lift", "system", "rank"), True),
        ("false_lift_determinant", "fourfold_lift", ("quadratic_lift", "uniqueness_certificate", "determinant"), "0"),
        ("hidden_nonfinite", "fourfold_lift", ("proof_boundary", "sympy_version"), float("nan")),
        ("schema2_empty_stages", "constant_affine", ("classification", "stages"), []),
        ("schema2_stage_bool", "constant_affine", ("classification", "stages", 1, "index"), True),
        ("schema2_wrong_least_depth", "constant_affine", ("classification", "depth", "value"), 4),
        ("schema2_hide_first_stage", "constant_affine", ("classification", "stages", 1),
         {"index": 1, "status": "unknown", "space": None, "reason": "omitted"}),
        ("schema2_hide_static_stage", "constant_affine", ("classification", "stages", 0),
         {"index": 0, "status": "unknown", "space": None, "reason": "omitted"}),
        ("schema2_bad_chart", "constant_affine", ("classification", "coordinates", "M"), [{"q": 1, "p": 0, "coefficient": "1"}]),
        ("schema2_fake_regime", "constant_affine", ("classification", "regime"), "hidden_quadratic"),
        ("schema2_omit_square_integral", "variable_square", ("classification", "square_first_integral"), None),
        ("schema2_wrong_failure", "variable_quadratic", ("classification", "sharpness_witness", "first_failing_iterate"), 1),
        ("schema2_fake_static_status", "variable_quadratic", ("classification", "stages", 0),
         {"index": 0, "status": "classified", "space": {"kind": "finite_basis", "dimension": 0, "basis": []}}),
        ("adapter_unauthorized_S0", "schema2_adapter", ("classification", "stages", 0),
         {"index": 0, "status": "classified", "space": {"kind": "finite_basis", "dimension": 0, "basis": []}}),
        ("zero_false_degree", "zero", ("degree",), 0),
        ("zero_fake_factor_scalar", "zero", ("leading", "factorization", "coefficient"), "1"),
        ("separable_false_potential_degree", "separable_cubic", ("classification", "normal_form", "degree_f"), 5),
        ("separable_bad_determinant", "separable_cubic", ("classification", "coordinates", "determinant"), "2"),
        ("separable_missing_drops", "separable_cubic", ("classification", "drop_witnesses"), []),
        ("separable_legacy_certificate", "separable_cubic", ("classification", "quadratic_lift"), {}),
        ("separable_hide_static_vector", "separable_quartic", ("classification", "stages", 0, "space", "basis"), []),
        ("separable_false_old_dependencies", "separable_cubic", ("proof_boundary", "dependencies"), [R.THEOREM, R.EXTENSION, R.SEPARABLE]),
        ("weighted_false_weight", "weighted_cubic_three", ("classification", "weighted_model", "weights", "L"), 2),
        ("weighted_bool_weight", "weighted_cubic_three", ("classification", "weighted_model", "weights", "L"), True),
        ("weighted_shrunk_static_box", "weighted_cubic_three", ("classification", "weighted_model", "static_bound"), 9),
        ("weighted_missing_leading", "weighted_cubic_three", ("classification", "weighted_model", "leading"), []),
        ("weighted_missing_lower", "weighted_cubic_three", ("classification", "weighted_model", "lower"), []),
        ("weighted_missing_drop", "weighted_cubic_three", ("classification", "drop_witnesses"), []),
        ("weighted_missing_gates", "weighted_cubic_three", ("classification", "drop_witnesses", 0, "gates"), {}),
        ("weighted_wrong_gate_alias", "weighted_cubic_three", ("classification", "drop_witnesses", 0, "T3"), []),
        ("weighted_suppressed_support", "weighted_cubic_three", ("status",), "unsupported"),
        ("weighted_lost_transfer_dependency", "weighted_cubic_three", ("proof_boundary", "dependencies"), [R.SEPARABLE]),
    ]
    result = [changed(*row) for row in tests]
    for key in ("degree", "homogeneous", "proof_boundary", "leading", "status"):
        result.append(changed("missing_" + key, "fourfold_lift", (key,), delete=True))
    for key in ("stages", "depth", "sharpness_witness", "coordinates"):
        result.append(changed("schema2_missing_" + key, "constant_affine", ("classification", key), delete=True))
    # This generator has total degree ten.  A degree-six replay alone cannot
    # detect its removal, even though the all-degree static space is wrong.
    result.append(changed("degree_ten_static_omission", "constant_quadratic_b",
                          ("classification", "stages", 0, "space", "finite_span", -1), delete=True))
    for mutation in ("remove_module_direction", "proper_submodule", "truncate_coefficient_ring"):
        H, original = by_name["sixfold"]
        report = copy.deepcopy(original)
        for name in ("S1", "S2", "Dinf"):
            space = report["classification"][name]
            if mutation == "remove_module_direction":
                space["module_basis"] = space["module_basis"][:-1]
            elif mutation == "proper_submodule":
                space["module_basis"] = [R.E.serialize(R.E.multiply(R.X, R.polynomial(G))) for G in space["module_basis"]]
            else:
                space["coefficient_generators"] = [R.E.serialize(R.E.power(R.X, 2))]
        result.append((mutation, H, report))
    H, original = by_name["constant_affine"]
    report = copy.deepcopy(original)
    # The schema identifier is fixed: inserting legacy fields cannot make a
    # missing stage list fall back to a weaker format.
    del report["classification"]["stages"]
    report["classification"].update({"S1": report["classification"]["Dinf"], "S2": report["classification"]["Dinf"]})
    result.append(("ambiguous_schema2_layout", H, report))
    for case in ("separable_cubic", "weighted_cubic_three", "constant_affine"):
        H, original = by_name[case]
        report = copy.deepcopy(original)
        report["status"] = "unsupported"
        report["unsupported_reason"] = "An apparently well-formed suppressed result"
        report["classification"] = {"family": original["classification"]["family"], "method": "leading_form",
            "derived_from": R.SCHEMA1, "depth": None, "stages": None, "Dinf": None,
            "sharpness_witness": None, "obstruction": None, "quadratic_lift": None}
        result.append(("coherent_suppressed_" + case, H, report))
    return result


class SuppliedReportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases = valid_cases()

    def test_all_supported_shapes_and_scope_rejections(self):
        for name, H, report in self.cases:
            with self.subTest(name=name):
                receipt = R.verify_report(H, report)
                self.assertEqual(receipt["status"], "PASS")
                self.assertFalse(receipt["proof_boundary"]["classifier_called"])

    def test_adversarial_reports_are_rejected(self):
        for name, H, report in corruptions(self.cases):
            with self.subTest(name=name):
                with self.assertRaises(R.VerificationError):
                    R.verify_report(H, report)

    def test_verifier_never_calls_the_classifier(self):
        selected = {"fourfold_lift", "constant_affine", "variable_quadratic", "unsupported_schema2"}
        with patch.object(C, "classify_sextic", side_effect=AssertionError("producer called")), \
             patch.object(C, "classify_sextic_v2", side_effect=AssertionError("producer called")), \
             patch.object(R.V.C, "classify_sextic", side_effect=AssertionError("producer called")), \
             patch.object(R.V.C, "classify_sextic_v2", side_effect=AssertionError("producer called")):
            for name, H, report in self.cases:
                if name in selected:
                    with self.subTest(name=name):
                        self.assertEqual(R.verify_report(H, report)["status"], "PASS")

    def test_verifier_does_not_import_any_producer(self):
        program = r'''
import builtins, importlib.util, json, pathlib, sys
blocked = {"sextic_core", "quadratic_sixfold", "separable_sixfold", "weighted_separable"}
original_spec, original_import = importlib.util.spec_from_file_location, builtins.__import__
def guarded_spec(name, location, *args, **kwargs):
    if pathlib.Path(location).stem in blocked:
        raise AssertionError("producer source loaded: " + str(location))
    return original_spec(name, location, *args, **kwargs)
def guarded_import(name, *args, **kwargs):
    if name.split(".")[-1] in blocked:
        raise AssertionError("producer imported: " + name)
    return original_import(name, *args, **kwargs)
importlib.util.spec_from_file_location, builtins.__import__ = guarded_spec, guarded_import
sys.path.insert(0, sys.argv[1])
import verify_sextic_report as R
H = R.polynomial(R.load_json(sys.argv[2]))
print(json.dumps(R.verify_report(H, R.load_json(sys.argv[3]))))
'''
        chosen = {"constant_affine", "variable_quadratic", "separable_cubic", "weighted_cubic_three", "unsupported_schema2"}
        with tempfile.TemporaryDirectory() as directory:
            source, report_path = Path(directory) / "input.json", Path(directory) / "report.json"
            for name, H, report in self.cases:
                if name not in chosen:
                    continue
                with self.subTest(name=name):
                    source.write_text(json.dumps(R.E.serialize(H)), encoding="utf-8")
                    report_path.write_text(json.dumps(report), encoding="utf-8")
                    result = subprocess.run([sys.executable, "-c", program, str(R.HERE), str(source), str(report_path)],
                                            text=True, capture_output=True)
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertEqual(json.loads(result.stdout)["status"], "PASS")

    def test_missing_scope_checkers_cannot_silently_accept_unsupported(self):
        _, H, report = next(case for case in self.cases if case[0] == "unsupported_complement_five")
        for name in ("verify_separable_sixfold", "verify_weighted_separable"):
            with self.subTest(module=name), patch.dict(sys.modules, {name: None}):
                with self.assertRaisesRegex(R.VerificationError, "dependency unavailable"):
                    R.verify_report(H, report)

    def test_equivalent_finite_basis_and_unimodular_module_basis(self):
        H = P.parse("q^6+p^6")
        report = C.classify_sextic(H)
        basis = [R.E.serialize(R.E.add(H, R.ONE)), R.E.serialize(R.E.add(H, R.E.scale(R.ONE, -1)))]
        for name in ("S1", "S2", "Dinf"):
            report["classification"][name]["basis"] = copy.deepcopy(basis)
        R.verify_report(H, report)
        H = P.parse("q^6")
        report = C.classify_sextic(H)
        for name in ("S1", "S2", "Dinf"):
            report["classification"][name]["module_basis"][1] = R.E.serialize(R.E.add(R.Y, R.E.power(R.X, 7)))
        R.verify_report(H, report)

    def test_cli_duplicate_keys_nonfinite_and_input_binding(self):
        H = P.parse("q^6+p^6")
        report = C.classify_sextic(H)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "report.json"
            path.write_text(json.dumps(report), encoding="utf-8")
            command = [sys.executable, str(Path(R.__file__)), str(path)]
            accepted = subprocess.run(command + ["--H", "q^6+p^6"], text=True, capture_output=True)
            self.assertEqual(accepted.returncode, 0, accepted.stderr + accepted.stdout)
            rejected = subprocess.run(command + ["--H", "q^6-p^6"], text=True, capture_output=True)
            self.assertEqual(rejected.returncode, 2)
            for raw in ('{"schema":"x","schema":"y"}', '{"schema":NaN}', '{"schema":Infinity}'):
                path.write_text(raw, encoding="utf-8")
                result = subprocess.run(command + ["--H", "q^6+p^6"], text=True, capture_output=True)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(json.loads(result.stdout)["status"], "REJECTED")

    def test_checks_remain_active_under_python_optimization(self):
        _, H, report = next(case for case in corruptions(self.cases) if case[0] == "degree_ten_static_omission")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "report.json"
            path.write_text(json.dumps(report), encoding="utf-8")
            result = subprocess.run([sys.executable, "-O", str(Path(R.__file__)), str(path),
                                     "--H", "q^6+q^2*p+p^2"], text=True, capture_output=True)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(json.loads(result.stdout)["status"], "REJECTED")


def replay():
    cases = valid_cases()
    accepted = []
    fingerprints = {}
    for name, H, report in cases:
        receipt = R.verify_report(H, report)
        fingerprints.update(receipt["source_sha256"])
        accepted.append({"case": name, "schema": report["schema"], "classification_status": report["status"],
                         "report_sha256": receipt["report_sha256"], "checks": receipt["checks"]})
    rejected = []
    for name, H, report in corruptions(cases):
        try:
            R.verify_report(H, report)
        except R.VerificationError as exc:
            rejected.append({"case": name, "reason": str(exc)})
        else:
            raise R.VerificationError("Corruption was accepted: " + name)
    fixture_paths = [Path(__file__).resolve()] + [R.HERE.parent / name for name in
        ("sextic_core.py", "quadratic_sixfold.py", "separable_sixfold.py", "weighted_separable.py", "partner_lab.py")]
    return {"schema": "hamiltonian-sextic-report-adversarial-replay/1", "status": "PASS",
            "accepted_report_count": len(accepted), "rejected_corruption_count": len(rejected),
            "accepted": accepted, "rejected": rejected, "source_sha256": fingerprints,
            "fixture_source_sha256": {str(path.relative_to(R.HERE.parents[2])): hashlib.sha256(path.read_bytes()).hexdigest()
                                       for path in sorted(fixture_paths)},
            "boundary": "Producer used only to create fixtures; supplied-report verification calls no classifier. All-degree completeness remains conditional on written theorems."}


if __name__ == "__main__":
    if sys.argv[1:] == ["--receipt"]:
        print(json.dumps(replay(), indent=2, sort_keys=True))
    else:
        unittest.main()
