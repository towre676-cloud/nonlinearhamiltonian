import unittest
import sympy as S
import cubic_static_recurrence as C
from general_sixfold_discovery import Q,P


class CubicStaticTheoremTests(unittest.TestCase):
    def test_symbolic_all_degree_static_basis(self):
        u,v,w,x=S.symbols("u v w x",nonzero=True)
        basis=C.static_basis(u,v,w,x)
        self.assertEqual(len(basis),15)
        self.assertEqual(max(S.Poly(z,Q,P).total_degree() for z in basis),9)

    def test_exact_pointwise_all_degree_refinements(self):
        for args,expected in [
            ((0,0,0,1),[15,4,2]),
            ((0,0,1,1),[15,3,2]),
            ((1,2,3,1),[15,3,2]),
            ((0,1,0,1),[15,3,2])
        ]:
            self.assertEqual(C.stage_dimensions(*args),expected)

    def test_generic_nonzero_minors(self):
        receipt=C.generic_minor_certificate()
        self.assertEqual(receipt["generic_dimensions"],[15,3,2])
        self.assertEqual([x["rank"] for x in receipt["rank_witnesses"]],[12,13])

    def test_zero_transverse_cubic_is_out_of_scope(self):
        with self.assertRaises(ValueError):
            C.static_basis(0,0,0,0)


if __name__=="__main__":
    unittest.main()
