import importlib.util
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("perfectjet_bridge", HERE/"bridge.py")
B = importlib.util.module_from_spec(spec)
spec.loader.exec_module(B)


class PerfectJetBridgeTests(unittest.TestCase):
    def test_all_eleven_strata_through_degree_ten(self):
        rows = B.cross_check(10, 2)
        self.assertEqual(len(rows), 11*11)
        self.assertTrue(all(len(row["kernel_dimensions"]) == 3 for row in rows))

    def test_exceptional_family_rank_boundary(self):
        result = B.exceptional_family_report()
        self.assertEqual(
            [r["direct_kernel_dimension"] for r in result["boundary_delta_0"]["depths"]],
            [3, 1, 1])
        self.assertEqual(
            [r["direct_kernel_dimension"] for r in result["generic_delta_1"]["depths"]],
            [3, 1, 0])


if __name__ == "__main__":
    unittest.main(verbosity=2)
