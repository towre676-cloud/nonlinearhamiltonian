import importlib.util
import unittest
from pathlib import Path

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location("sixfold_cubic_discovery",HERE/"sixfold_cubic_discovery.py")
M=importlib.util.module_from_spec(spec)
spec.loader.exec_module(M)


class SixfoldCubicDiscoveryTests(unittest.TestCase):
    def test_independent_engines(self):
        result=M.discover(max_degree=6,depth=2)
        self.assertEqual(len(result["results"]),3)
        self.assertTrue(all(row["kernel_dimensions"][-1]==2 for row in result["results"]))
        self.assertTrue(all(row["independent_star_expansion_agrees"] for row in result["results"]))


if __name__=="__main__":
    unittest.main()
