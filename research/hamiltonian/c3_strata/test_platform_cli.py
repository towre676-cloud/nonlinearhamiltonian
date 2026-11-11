"""Exercise the public classifier/checker handoff and its input binding."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

CLI = Path(__file__).resolve().parents[1] / "partner_lab.py"


class PlatformCLITests(unittest.TestCase):
    def run_cli(self, *args):
        return subprocess.run([sys.executable, str(CLI), *args], capture_output=True, text=True)

    def test_general_potential_degree_and_scope_exit(self):
        result = self.run_cli("separable-core", "--H", "q^7+p^3+q")
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["schema"], "hamiltonian-separable-core/1")
        self.assertEqual(report["classification"]["depth"], {"kind": "least", "value": 2})
        self.assertEqual(report["classification"]["Dinf"]["dimension"], 2)
        refused = self.run_cli("separable-core", "--H", "q^6+p^5")
        self.assertEqual(refused.returncode, 2)
        self.assertEqual(json.loads(refused.stdout)["status"], "out_of_scope")

    def test_report_handoff_binds_independent_input(self):
        result = self.run_cli("sextic-core", "--schema", "2", "--H", "q^6+p^4")
        self.assertEqual(result.returncode, 0, result.stderr)
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "report.json"
            path.write_text(result.stdout)
            accepted = self.run_cli("verify-report", str(path), "--H", "q^6+p^4")
            self.assertEqual(accepted.returncode, 0, accepted.stderr + accepted.stdout)
            self.assertEqual(json.loads(accepted.stdout)["status"], "PASS")
            rejected = self.run_cli("verify-report", str(path), "--H", "q^6+p^3")
            self.assertEqual(rejected.returncode, 2)
            self.assertEqual(json.loads(rejected.stdout)["status"], "REJECTED")

    def test_weighted_mixed_input_and_sextic_stage_adapter(self):
        for expression, dimension, depth in (("q^6+p^3+q*p^2", 3, 2),
                                              ("q^6+p^3+q^3*p", 2, 1)):
            result = self.run_cli("sextic-core", "--schema", "2", "--H", expression)
            self.assertEqual(result.returncode, 0, result.stderr)
            spaces = json.loads(result.stdout)["classification"]
            self.assertEqual(spaces["method"], "sixfold_weighted_separable")
            self.assertEqual(spaces["stages"][1]["space"]["dimension"], dimension)
            self.assertEqual(spaces["depth"], {"kind": "least", "value": depth})
        result = self.run_cli("weighted-core", "--H", "q^8+p^3+q*p")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["classification"]["Dinf"]["dimension"], 2)


if __name__ == "__main__":
    unittest.main()
