import unittest
from fractions import Fraction as Fr

import sixfold_global_depth as G


class Classifier(unittest.TestCase):
    def check(self, text, branch, depth, core=2):
        info = G.classify(G.parse(text))
        self.assertEqual((info["depth"], info["core_dimension"]), (depth, core), text)
        self.assertIn(branch, info["branch"])
        self.assertLessEqual(info["depth"], info["depth_bound"])
        self.assertLessEqual(info["depth_bound"], 6)

    def test_depth_six_locus(self):
        self.check("(p+q^3)^2+q^3", "N=3", 6)
        self.check("3*(p+q^3-q)^2+2*q^3+q", "N=3", 6)
        self.assertTrue(G.depth_six_conditions(G.parse("(p+q^3)^2+q^3")))
        for other in ("(p+q^3)^2+q^2", "(p+q^3)^2+q^4", "q^6+p^2", "(p+q^3)^2+q^3+q*p^2", "(p+q^3)^2+q^3+p^3"):
            self.assertFalse(G.depth_six_conditions(G.parse(other)))
            self.assertNotEqual(G.classify(G.parse(other))["depth"], 6)

    def test_every_row(self):
        self.check("q^6+p^2", "b''=0", 5)
        self.check("(p+q^3)^2+q^5", "N>=4", 4)
        self.check("p^2+q^4*p+q^6", "N>=4", 4)
        self.check("q^6+q*p^2", "linear", 3)
        self.check("(p+q^2)^3+q*(p+q^2)+q^2", "cube", 3)
        self.check("(p+q^3)^2+q^2", "N<=2", 2, 6)
        self.check("q^6+q^2*p^2", "quadratic quadratic", 2)
        self.check("(q*p+q^3)^2", "quadratic quadratic", 1, 3)
        self.check("q^6+20*q^3*p^2-10*p^4", "c04", 2)
        self.check("q^6+p^4", "c04", 1)
        self.check("q^6+q^3*p^2", "c32", 2)
        self.check("q^6+(q^3+q)*p^2", "c32", 1)
        self.check("q^6+q*p^3", "c13", 2)
        self.check("q^6+p^3", "off the cube", 2)
        self.check("q^6+q^4*p+p^3", "off the cube", 1)
        self.check("(p+q^2)^3+q*(p+q^2)", "cube", 1, 6)
        self.check("(p+q^2)^3+q*(p+q^2)+q", "cube", 1, 5)
        self.check("(p+q^2)^3+q", "cube", 1, G.INF)
        self.check("q^6+q^2*p", "affine in p", 1, G.INF)
        self.check("q^6+q*p", "affine in p", 0, G.INF)
        for text in ("q^6+p^5+q*p", "q^6+q*p^4+p^3", "q^6+q^2*p^3+q"):
            self.check(text, "c", 1)

    def test_rejects_other_leading_forms(self):
        for text in ("q^6+p^6", "q^5+p", "q^6+q^5*p"):
            with self.assertRaises(ValueError):
                G.classify(G.parse(text))


class Engine(unittest.TestCase):
    def test_regression_anchor(self):
        h = G.parse("q^6+q*p^2")
        g = G.parse("p^2+12/5*q^5")
        self.assertFalse(G.transvectant(h, g, 3) or G.transvectant(h, g, 5))
        dg = G.transvectant(h, g, 1)
        self.assertEqual(dg, {(0, 3): Fr(2), (5, 1): Fr(-12)})
        self.assertFalse(G.transvectant(h, dg, 3) or G.transvectant(h, dg, 5))
        self.assertEqual(G.transvectant(h, G.transvectant(h, dg, 1), 3), {(3, 1): Fr(51840)})

    def test_window_chains(self):
        w = G.degree_window(10)
        self.assertEqual(G.chain(G.parse("(p+q^3)^2+q^3"), w, 8), [22, 14, 6, 5, 4, 3, 2, 2, 2])
        self.assertEqual(G.chain(G.parse("q^6+p^2"), w, 7), [30, 22, 14, 6, 4, 2, 2, 2])
        self.assertEqual(G.chain(G.parse("q^6+q*p^2"), w, 5), [19, 6, 3, 2, 2, 2])

    def test_stage_dimensions_for_nonconstant_coefficient(self):
        box = G.weight_window(2, 5, 22)
        self.assertEqual(G.chain(G.parse("q^6+q^5+(q+3)*p^2+(q^2+2*q+5)*p"), box, 3)[1:], [6, 3, 2])
        self.assertEqual(G.chain(G.parse("q^6+q*p^2+q^3*p"), box, 3)[1:], [5, 3, 2])
        self.assertEqual(G.chain(G.parse("q^6+q*p^2+q^4*p"), G.weight_window(1, 3, 13), 3)[1:], [5, 3, 2])
        cubic = G.weight_window(2, 3, 26)
        self.assertEqual(G.chain(G.parse("q^6+(q^3+1)*p^2+q^4*p"), cubic, 2)[1:], [3, 2])
        self.assertEqual(G.chain(G.parse("q^6+(q^3+q)*p^2+q^4*p"), cubic, 2)[1:], [2, 2])


if __name__ == "__main__":
    unittest.main()
