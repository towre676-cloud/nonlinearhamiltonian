import unittest
import sympy as S
from general_sixfold_discovery import Q,P,transvectant
from complete_cubic_exceptional import exact_rank_certificate, shear_identity, independent_point_replays

class CompleteCubicExceptionalTests(unittest.TestCase):
    def test_three_exact_symbolic_minors(self):
        report=exact_rank_certificate()
        self.assertEqual(len(report["first_refinement_rank_minor_certificates"]),2)
        self.assertEqual(report["static_dimension_all_degrees"],15)
        self.assertEqual(report["second_refinement_all_parameters"],["1","H"])

    def test_symplectic_shear(self):
        self.assertEqual(shear_identity()["exceptional_condition"],"3*v*x-w**2=0")

    def test_unreduced_q2_defect(self):
        u,v,w,x=S.symbols("u v w x")
        H=Q**6+u*Q**3+v*Q**2*P+w*Q*P**2+x*P**3
        D=lambda G:transvectant(H,G,1)
        self.assertEqual(S.factor(transvectant(H,D(Q**2),3)),48*(3*v*x-w*w))
        self.assertEqual(transvectant(H,D(Q**2),5),0)

    def test_all_degree_point_ranks(self):
        self.assertEqual(len(independent_point_replays()),6)

if __name__=="__main__":
    unittest.main()
