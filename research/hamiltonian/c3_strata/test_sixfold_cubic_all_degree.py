import importlib.util
import unittest
from fractions import Fraction as F
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
spec=importlib.util.spec_from_file_location("sixfold_cubic_all_degree",
    HERE/"verify_sixfold_cubic_all_degree.py")
M=importlib.util.module_from_spec(spec)
spec.loader.exec_module(M)

import sys
sys.path.insert(0,str(ROOT))
import sextic_core as C
from independent import engine as E


class SixfoldCubicAllDegreeTests(unittest.TestCase):
    def test_exact_all_degree_certificate(self):
        receipt=M.verify()
        self.assertEqual(receipt["static_basis_dimension"],15)
        self.assertEqual(receipt["first_refinement_dimension"],4)
        self.assertEqual(receipt["second_refinement_dimension"],2)

    def test_classifier_normalized_and_scaled(self):
        for lam in (F(1),F(2),F(-3)):
            H={(6,0):F(1),(0,3):lam}
            report=C.classify_sextic(H)
            self.assertEqual(report["classification"]["method"],"sixfold_cubic_complement")
            self.assertEqual(report["classification"]["S1"]["dimension"],4)
            self.assertEqual(report["classification"]["S2"]["dimension"],2)
            self.assertEqual(report["classification"]["Dinf"]["dimension"],2)

    def test_rational_gl2_and_constant_shift(self):
        q={(1,0):F(1)}
        p={(0,1):F(1)}
        L=E.add(q,E.scale(p,F(2)))
        N=E.add(E.scale(q,F(3)),p)
        H=E.add(E.scale(E.power(L,6),F(5,7)),
                E.scale(E.power(N,3),F(-2,3)),
                {(0,0):F(11,5)})
        report=C.classify_sextic(H)
        self.assertEqual(report["classification"]["method"],"sixfold_cubic_complement")
        self.assertEqual(report["classification"]["S1"]["dimension"],4)
        self.assertEqual(report["classification"]["Dinf"]["dimension"],2)

    def test_parallel_sixfold_not_misclassified(self):
        H={(6,0):F(1),(3,0):F(2)}
        self.assertNotEqual(C.classify_sextic(H)["classification"]["method"],
                            "sixfold_cubic_complement")

if __name__=="__main__":
    unittest.main()
