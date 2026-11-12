import importlib.util
import unittest
from pathlib import Path
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location("quadratic_incidence",HERE/"quadratic_incidence.py")
M=importlib.util.module_from_spec(spec)
spec.loader.exec_module(M)

class QuadraticIncidenceTests(unittest.TestCase):
    def test_three_first_refinement_points(self):
        self.assertEqual(M.replay(0,3),[3,1,1])
        self.assertEqual(M.replay(16,-9),[3,1,0])
        self.assertEqual(M.replay(-16,-9),[3,1,0])
    def test_generic_points(self):
        self.assertEqual(M.replay(0,-9),[3,0,0])
        self.assertEqual(M.replay(1,0),[3,0,0])

if __name__=="__main__":
    unittest.main()
