"""Classifier regressions checked through the independent defining star product."""
import copy
from fractions import Fraction as F
import json
from pathlib import Path
import subprocess
import sys
import unittest

import verify_sextic_core as V


class SexticCoreTests(unittest.TestCase):
    def test_complete_independent_replay(self):
        receipt = V.verify()
        self.assertEqual(receipt["status"], "PASS")
        self.assertEqual(len(receipt["geometric_strata"]), 11)
        self.assertEqual(receipt["rational_GL2_and_scalar_checks"], 22)
        self.assertEqual(len(receipt["inhomogeneous_checks"]), 12)
        self.assertEqual(len(receipt["sixfold_affine_checks"]), 10)
        self.assertEqual(receipt["constant_shift_checks"], 11)
        self.assertEqual(len(receipt["unsupported_inhomogeneous_patterns"]), 3)
        self.assertGreaterEqual(receipt["second_iterate_obstruction_checks"], 6)
        # A receipt must serialize exactly, without float or SymPy objects.
        self.assertEqual(json.loads(json.dumps(receipt)), receipt)

    def test_strict_exact_input_validation(self):
        bad_inputs = [
            None,
            [(6, 0, 1)],
            {"q^6": F(1)},
            {(6,): F(1)},
            {(6, 0, 0): F(1)},
            {(6.0, 0): F(1)},
            {(True, 5): F(1)},
            {(-1, 7): F(1)},
            {(6, 0): 1.0},
            {(6, 0): True},
            {(6, 0): "1/3"},
            {(5, 0): F(1)},
            {(7, 0): F(1)},
            {(6, 0): F(1), (4, 3): F(1)},
        ]
        for bad in bad_inputs:
            with self.subTest(value=bad):
                with self.assertRaises((TypeError, ValueError)):
                    V.C.classify_sextic(bad)

    def test_exact_rational_scalar_and_zero_terms(self):
        H = {(6, 0): F(-11, 37), (0, 6): F(-11, 37), (0, 0): F(0)}
        report = V.C.classify_sextic(H)
        V.check_report(H, report)
        self.assertEqual(V.polynomial(report["input"]),
                         {(6, 0): F(-11, 37), (0, 6): F(-11, 37)})
        self.assertEqual(report["leading"]["geometric_root_pattern"], [1] * 6)
        self.assertEqual(report["leading"]["infinity_multiplicity"], 0)
        json.dumps(report, sort_keys=True)

    def test_factorization_corruption_rejected(self):
        H = {(6, 0): F(1), (0, 6): F(1)}
        report = V.C.classify_sextic(H)
        report["leading"]["factorization"]["coefficient"] = "2"
        with self.assertRaisesRegex(V.VerificationError, "Factorization"):
            V.check_report(H, report)

    def test_infinity_corruption_rejected(self):
        H = {(0, 6): F(1)}
        report = V.C.classify_sextic(H)
        report["leading"]["infinity_multiplicity"] = 0
        with self.assertRaisesRegex(V.VerificationError, "projective"):
            V.check_report(H, report)

    def test_missing_and_dependent_basis_rejected(self):
        H = {(6, 0): F(1), (0, 6): F(1)}
        original = V.C.classify_sextic(H)
        for replacement in ([], [original["classification"]["S1"]["basis"][0]] * 2):
            report = copy.deepcopy(original)
            report["classification"]["S1"]["basis"] = replacement
            with self.subTest(replacement=replacement):
                with self.assertRaisesRegex(V.VerificationError, "dimension|dependent"):
                    V.check_report(H, report)

    def test_consistent_core_basis_omission_rejected(self):
        H = {(6, 0): F(1), (0, 6): F(1)}
        original = V.C.classify_sextic(H)
        for retained_index in (0, 1):
            report = copy.deepcopy(original)
            for name in ("S1", "S2", "Dinf"):
                space = report["classification"][name]
                space["basis"] = [space["basis"][retained_index]]
                space["dimension"] = 1
            with self.subTest(retained_index=retained_index):
                with self.assertRaisesRegex(V.VerificationError, "contain both 1 and H"):
                    V.check_report(H, report)

    def test_root_pattern_and_family_corruption_rejected(self):
        H = {(6, 0): F(1), (0, 6): F(1)}
        original = V.C.classify_sextic(H)
        for change_pattern, change_family in ((True, False), (False, True), (True, True)):
            report = copy.deepcopy(original)
            if change_pattern:
                report["leading"]["geometric_root_pattern"] = [6]
            if change_family:
                report["classification"]["family"] = "multiplicity_6"
            with self.subTest(pattern=change_pattern, family=change_family):
                with self.assertRaisesRegex(V.VerificationError, "root pattern"):
                    V.check_report(H, report)

    def test_unreduced_geometric_factorization_rejected(self):
        H = {(6, 0): F(1)}
        original = V.C.classify_sextic(H)
        # Both corrupt descriptions reconstruct H exactly. Neither describes
        # distinct simple geometric roots with the asserted multiplicities.
        corrupt_factors = [
            [{"terms": [{"q": 6, "p": 0, "coefficient": "1"}],
              "geometric_degree": 6, "multiplicity": 1}],
            [{"terms": [{"q": 1, "p": 0, "coefficient": "1"}],
              "geometric_degree": 1, "multiplicity": 3}] * 2,
        ]
        for factors in corrupt_factors:
            report = copy.deepcopy(original)
            report["leading"]["factorization"]["factors"] = factors
            with self.subTest(factors=factors):
                with self.assertRaisesRegex(V.VerificationError, "squarefree|projective root"):
                    V.check_report(H, report)

    def test_spurious_quadratic_survivor_rejected(self):
        H = {(6, 0): F(1), (0, 6): F(1)}
        report = V.C.classify_sextic(H)
        report["classification"]["S1"]["basis"].append(
            [{"q": 1, "p": 1, "coefficient": "1"}])
        report["classification"]["S1"]["dimension"] = 3
        with self.assertRaisesRegex(V.VerificationError, "star defect"):
            V.check_report(H, report)

    def test_exceptional_obstruction_matches_star_exponential(self):
        H = {(4, 2): F(1), (6, 0): F(1)}
        report = V.C.classify_sextic(H)
        V.check_report(H, report)
        witness = report["obstruction"]
        self.assertEqual(V.polynomial(witness["G"]), {(1, 1): F(1)})
        self.assertEqual(V.polynomial(witness["D2G"]), {(9, 1): F(-48)})
        self.assertEqual(V.polynomial(witness["T3"]), {(10, 0): F(-82944)})
        self.assertEqual(V.polynomial(witness["T5"]), {})

    def test_corrupted_second_iterate_and_gate_rejected(self):
        H = {(4, 2): F(1), (6, 0): F(1)}
        original = V.C.classify_sextic(H)
        for field in ("D2G", "T3"):
            report = copy.deepcopy(original)
            report["obstruction"][field] = []
            with self.subTest(field=field):
                with self.assertRaises(V.VerificationError):
                    V.check_report(H, report)

    def test_missing_obstruction_rejected(self):
        H = {(4, 2): F(1), (6, 0): F(1)}
        report = V.C.classify_sextic(H)
        report["obstruction"] = None
        with self.assertRaisesRegex(V.VerificationError, "requires.*obstruction"):
            V.check_report(H, report)

    def test_refinement_depth_corruption_rejected(self):
        H = {(4, 2): F(1), (6, 0): F(1)}
        original = V.C.classify_sextic(H)
        for depth in (0, 1, True, None):
            report = copy.deepcopy(original)
            report["classification"]["sufficient_refinement_depth"] = depth
            with self.subTest(depth=depth):
                with self.assertRaisesRegex(V.VerificationError, "Refinement depth"):
                    V.check_report(H, report)

    def test_quadratic_lift_cannot_be_omitted_from_S1(self):
        H = {(4, 2): F(1), (6, 0): F(1)}
        report = V.C.classify_sextic(H)
        report["classification"]["S1"] = copy.deepcopy(report["classification"]["Dinf"])
        report["classification"]["sufficient_refinement_depth"] = 1
        report["obstruction"] = None
        # A consistent dimension/depth edit must not hide a returned lift.
        with self.assertRaisesRegex(V.VerificationError, "quadratic lift is missing"):
            V.check_report(H, report)

    def test_corrupted_affine_lift_determinant_rejected(self):
        H = V.affine_substitute({(4, 2): F(1), (6, 0): F(1)}, shift=(1, -2))
        report = V.C.classify_sextic(H)
        report["quadratic_lift"]["uniqueness_certificate"]["determinant"] = "0"
        with self.assertRaisesRegex(V.VerificationError, "affine-lift determinant"):
            V.check_report(H, report)

    def test_fourfold_report_requires_lift_and_correct_ranks(self):
        leading = {(4, 2): F(1), (6, 0): F(1)}
        hidden = V.C.classify_sextic(leading)
        hidden["classification"]["S1"] = copy.deepcopy(hidden["classification"]["Dinf"])
        hidden["classification"]["sufficient_refinement_depth"] = 1
        hidden["obstruction"] = hidden["quadratic_lift"] = None
        with self.assertRaisesRegex(V.VerificationError, "requires a quadratic lift"):
            V.check_report(leading, hidden)

        for lower in ({(2, 0): F(1)}, {(0, 3): F(1)}):
            H = V.sparse_add(leading, lower)
            original = V.C.classify_sextic(H)
            for field in ("rank", "augmented_rank"):
                report = copy.deepcopy(original)
                report["quadratic_lift"]["system"][field] = 0
                with self.subTest(lower=lower, field=field):
                    with self.assertRaisesRegex(V.VerificationError, field):
                        V.check_report(H, report)

    def test_nonsplit_fourfold_root_at_infinity_with_rational_affine_change(self):
        matrix = ((0, F(1, 2)), (F(3, 2), 1))
        shift, scalar = (F(1, 3), F(-2, 5)), F(-2, 3)
        H0 = {(4, 2): F(1), (6, 0): F(1), (2, 0): F(2)}
        H = V.affine_substitute(H0, matrix, shift, scalar)
        J = V.affine_substitute({(1, 1): F(1)}, matrix, shift)
        report = V.check_report(H, V.C.classify_sextic(H))
        self.assertEqual(report["leading"]["geometric_root_pattern"], [4, 1, 1])
        self.assertEqual(report["leading"]["infinity_multiplicity"], 4)
        self.assertTrue(report["quadratic_lift"]["linear_correction"])
        self.assertTrue(V.same_span(V.space_basis(report["classification"]["S1"]),
                                   [{(0, 0): F(1)}, H, J]))
        second = V.E.poisson(H, V.E.poisson(H, J))
        expected = V.affine_substitute({(10, 0): F(-82944)}, matrix, shift,
                                       scalar**3 * F(-3, 4)**5)
        self.assertEqual(V.E.scale(V.E.defects(H, second)[2], -24), expected)

    def test_nonsplit_triple_pair_declines_nonconstant_perturbation(self):
        Q = {(2, 0): F(2), (0, 2): F(3)}
        H = V.sparse_power(Q, 3)
        shifted = V.sparse_add(H, {(0, 0): F(1, 7)})
        report = V.check_report(shifted, V.C.classify_sextic(shifted))
        for name in ("S1", "S2", "Dinf"):
            space = report["classification"][name]
            self.assertTrue(V.same_span([Q], [V.polynomial(
                space["coefficient_generators"][0])]))
        perturbed = V.sparse_add(shifted, {(1, 0): F(1, 7)})
        unsupported = V.C.classify_sextic(perturbed)
        self.assertEqual(unsupported["status"], "unsupported")
        self.assertEqual(unsupported["leading"]["geometric_root_pattern"], [3, 3])
        for name in ("S1", "S2", "Dinf", "sufficient_refinement_depth"):
            self.assertIsNone(unsupported["classification"][name])

    def test_translated_exception_has_affine_lift(self):
        H0 = {(4, 2): F(1), (6, 0): F(1)}
        H = V.affine_substitute(H0, shift=(1, -2))
        report = V.C.classify_sextic(H)
        self.assertEqual(report["classification"]["method"], "leading_form")
        self.assertTrue(report["quadratic_lift"]["linear_correction"])
        J = V.affine_substitute({(1, 1): F(1)}, shift=(1, -2))
        V.gates_through(H, J, 1)
        self.assertTrue(V.E.defects(H, V.E.poisson(H, V.E.poisson(H, J))))
        self.assertTrue(V.same_span(V.space_basis(report["classification"]["S1"]),
                                   [{(0, 0): F(1)}, H, J]))

    def test_low_terms_can_remove_or_preserve_quadratic_lift(self):
        H0 = {(4, 2): F(1), (6, 0): F(1)}
        with_q3 = V.C.classify_sextic(V.sparse_add(H0, {(3, 0): F(1)}))
        with_p3 = V.C.classify_sextic(V.sparse_add(H0, {(0, 3): F(1)}))
        self.assertEqual(with_q3["classification"]["S1"]["dimension"], 3)
        self.assertEqual(with_p3["classification"]["S1"]["dimension"], 2)
        self.assertEqual(with_p3["quadratic_lift"]["status"], "absent")
        self.assertIsNone(with_p3["obstruction"])

    def test_four_two_inhomogeneous_core_may_remain_three_dimensional(self):
        H = {(4, 2): F(1), (1, 1): F(1)}
        report = V.C.classify_sextic(H)
        V.check_report(H, report)
        self.assertEqual(report["classification"]["S1"]["dimension"], 3)
        self.assertEqual(report["classification"]["Dinf"]["dimension"], 3)
        J = {(1, 1): F(1)}
        self.assertEqual(V.E.poisson(H, J), {(4, 2): F(2)})

    def test_sixfold_static_cubic_can_fail_first_refinement(self):
        H = {(6, 0): F(1), (2, 1): F(1)}
        G = {(0, 3): F(1), (4, 2): F(15)}
        V.gates_through(H, G, 0)
        self.assertTrue(V.E.defects(H, V.E.poisson(H, G)))

    def test_sixfold_univariate_perturbation_in_oblique_coordinates(self):
        L = {(1, 0): F(2), (0, 1): F(3)}
        H = V.sparse_add(V.sparse_power(L, 6), V.sparse_power(L, 4))
        report = V.check_report(H, V.C.classify_sextic(H))
        self.assertEqual(report["classification"]["method"], "sixfold_affine_complement")
        self.assertEqual(V.check_bounded_kernel(H, report, 4, 1)["dimension"], 12)

    def test_sixfold_cli_scope(self):
        cli = Path(__file__).resolve().parents[1] / "partner_lab.py"
        for expression, status, code in (
                ("p^6+p^3*q", "classified", 0), ("p^6+q^2", "unsupported", 2)):
            with self.subTest(expression=expression):
                result = subprocess.run([sys.executable, str(cli), "sextic-core",
                                         "--H", expression],
                                        capture_output=True, text=True, check=False)
                self.assertEqual(result.returncode, code, result.stderr)
                self.assertEqual(json.loads(result.stdout)["status"], status)

    def test_quadratic_sixfold_cli_is_opt_in(self):
        cli = Path(__file__).resolve().parents[1] / "partner_lab.py"
        for expression, dimension in (("(q*p+q^3)^2", 3), ("q^6+q^2*p^2", 2)):
            for schema, expected_code in ((1, 2), (2, 0)):
                with self.subTest(expression=expression, schema=schema):
                    result = subprocess.run([sys.executable, str(cli), "sextic-core",
                                             "--H", expression, "--schema", str(schema)],
                                            capture_output=True, text=True, check=False)
                    self.assertEqual(result.returncode, expected_code, result.stderr)
                    report = json.loads(result.stdout)
                    self.assertEqual(report["schema"], f"hamiltonian-sextic-core/{schema}")
                    if schema == 2:
                        self.assertEqual(report["classification"]["Dinf"]["dimension"], dimension)

    def test_triple_pair_perturbations_against_star_kernels(self):
        t = {(1, 1): F(1)}
        leading = {(3, 3): F(1)}
        nonsplit = {(2, 0): F(1), (0, 2): F(1)}
        examples = [
            (V.sparse_add(leading, {key: F(2)}), 3 if sum(key) <= 2 else 2)
            for key in ((1, 0), (0, 2), (3, 0), (1, 2), (3, 1), (4, 0), (4, 1), (0, 5))
        ]
        shifted_t = V.sparse_add(t, {(1, 0): F(2)})
        examples.extend([
            (V.affine_substitute(V.sparse_add(leading, {(2, 0): F(-2), (0, 1): F(3)}),
                                 ((2, 1), (1, 3)), (F(1, 2), F(-1, 3)), F(-2, 7)), 3),
            (V.affine_substitute(V.sparse_add(V.sparse_power(nonsplit, 3), {(1, 1): F(2)}),
                                 shift=(F(1, 2), F(-1, 3))), 3),
            (V.sparse_add(V.sparse_power(nonsplit, 3), {(1, 2): F(2)}), 2),
            (V.sparse_add(leading, {(3, 2): F(1), (4, 1): F(1), (0, 1): F(3)}), 2),
            (V.sparse_add(leading, {(3, 2): F(3)}), 2),
            (V.sparse_add(V.sparse_power(shifted_t, 3),
                          V.E.scale(V.sparse_power(shifted_t, 2), 3), {(0, 2): F(-1)}), 3),
        ])
        for H, first_dimension in examples:
            with self.subTest(H=H):
                report = V.C.classify_sextic(H, schema=2)
                self.assertEqual(V.C.classify_sextic(H)["status"], "unsupported")
                self.assertEqual(report["classification"]["method"], "triple_pair_perturbation")
                self.assertEqual(report["classification"]["S1"]["dimension"], first_dimension)
                self.assertEqual(report["classification"]["Dinf"]["dimension"], 2)
                V.check_report(H, report)
                for depth in (1, 2):
                    V.check_bounded_kernel(H, report, 8, depth)

    def test_triple_pair_symbolic_gate_coefficients(self):
        import sympy as s

        x, y, a, b, d = s.symbols("x y a b d")
        origin = {x: 0, y: 0}

        def gate(order, left, right):
            return s.expand(sum(
                (-1)**j * s.binomial(order, j)
                * left.diff(x, order-j, y, j).subs(origin)
                * right.diff(x, j, y, order-j).subs(origin)
                for j in range(order+1)
            ))

        # Derivatives at (1,1) of the original monomials via translation.
        radial = (1+x)**3 * (1+y)**3
        general = (1+x)**a * (1+y)**b
        third = gate(3, radial, general)
        fifth = gate(5, radial, general)
        self.assertEqual(s.expand(third + 6*(a-b)*(a*a-8*a*b-3*a+b*b-3*b+2)), 0)
        self.assertEqual(s.expand(fifth + 360*a*b*(a-1)*(a-b)*(b-1)), 0)
        for u in range(6):
            for v in range(6-u):
                if u == v:
                    continue
                with self.subTest(u=u, v=v):
                    actual = d*third.subs({a: d+u-3, b: d+v-3})/3 + gate(
                        3, (1+x)**u * (1+y)**v, (1+x)**d * (1+y)**d,
                    )
                    expected = d*(d-3)*(u-v)*(
                        d*((u-v)**2-3*(u+v)+14)-6*u*v+12*(u+v)-24
                    )
                    self.assertEqual(s.expand(actual - expected), 0)

    def test_triple_pair_static_and_refinement_counterexample(self):
        H = {(3, 3): F(1), (1, 0): F(1)}
        t = {(1, 1): F(1)}
        t_squared = {(2, 2): F(1)}
        V.gates_through(H, t, 1)
        V.gates_through(H, t_squared, 0)
        self.assertEqual(V.E.defects(H, V.E.poisson(H, t_squared))[2],
                         {(2, 1): F(-9)})
        report = V.C.classify_sextic(H, schema=2)
        self.assertEqual(V.polynomial(report["obstruction"]["T5"]), {(1, 0): F(12960)})
        corrupt = copy.deepcopy(report)
        corrupt["obstruction"]["T5"][0]["coefficient"] = "1"
        with self.assertRaisesRegex(V.VerificationError, "Incorrect T5 obstruction"):
            V.check_report(H, corrupt)

    def test_unsupported_results_do_not_assert_spaces(self):
        for H in ({(6, 0): F(1), (0, 2): F(1)},
                  {(5, 1): F(1), (0, 2): F(1)},
                  {(3, 3): F(1), (1, 0): F(1)}):
            report = V.C.classify_sextic(H)
            with self.subTest(H=H):
                self.assertEqual(report["status"], "unsupported")
                self.assertTrue(report["unsupported_reason"])
                for name in ("S1", "S2", "Dinf"):
                    self.assertIsNone(report["classification"][name])

    def test_constant_shift_preserves_infinite_family(self):
        H = {(6, 0): F(1), (0, 0): F(17, 19)}
        report = V.C.classify_sextic(H)
        self.assertFalse(report["homogeneous"])
        self.assertEqual(report["classification"]["method"], "constant_shift")
        self.assertEqual(report["classification"]["S1"]["kind"], "polynomial_family")
        V.check_report(H, report, sample_powers=(0, 2, 5, 9))

    def test_verifier_rejects_corruption_under_optimized_python(self):
        script = (
            "import sys; sys.path.insert(0, sys.argv[1]); "
            "import verify_sextic_core as V; "
            "H={(4,2):V.F(1),(6,0):V.F(1)}; "
            "r=V.C.classify_sextic(H); r['obstruction']['T3']=[]\n"
            "try:\n V.check_report(H,r)\n"
            "except V.VerificationError:\n sys.exit(0)\n"
            "sys.exit(1)\n"
        )
        result = subprocess.run([sys.executable, "-O", "-c", script,
                                 str(Path(__file__).resolve().parent)],
                                capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
