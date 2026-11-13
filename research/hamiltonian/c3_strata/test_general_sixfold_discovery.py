"""Exact gate-incidence and independent defining-star replay tests."""
import importlib.util
from fractions import Fraction
from pathlib import Path
import unittest
import sympy as S
import general_sixfold_discovery as G

HERE=Path(__file__).resolve().parent


class GeneralSixfoldTests(unittest.TestCase):
    def test_exact_rank_drop_locus(self):
        r=G.discovery_example()
        self.assertEqual(r["depth_1_rank_leq_3"]["groebner_basis"],["a**3*b**2"])
        self.assertEqual([(x["S1_dimension"],x["S2_dimension"])
                          for x in r["specializations"]],[(6,6),(3,1),(4,2),(2,1)])

    def test_uniform_leading_gate(self):
        q,p=G.Q,G.P
        c=S.symbols("c0:7")
        top=sum(c[j]*q**(6-j)*p**j for j in range(7))
        a,b=S.symbols("a b")
        h=G.sparse_family({(0,3):a,(1,2):b,(2,1):3})
        expr=G.transvectant(h,top,3)
        highest=sum(v*q**i*p**j for (i,j),v in S.Poly(expr,q,p).terms()
                    if i+j==6)
        self.assertEqual(S.expand(highest-120*q**3*S.diff(top,p,3)),0)

    def test_no_partial_locus(self):
        a,b=S.symbols("a b")
        r=G.observation_matrix(G.sparse_family({(0,3):a,(1,2):b}),2,1)
        with self.assertRaisesRegex(ValueError,"no partial result"):
            G.rank_drop_ideal(r,(a,b),3,max_minors=1)
        with self.assertRaises(ValueError):
            G.sparse_family({(1,5):1})

    def test_independent_defining_star(self):
        engine=HERE.parent/"independent"/"engine.py"
        spec=importlib.util.spec_from_file_location("general_sixfold_moyal",engine)
        E=importlib.util.module_from_spec(spec)
        spec.loader.exec_module(E)
        a,b=S.symbols("a b")
        symbolic=G.sparse_family({(0,3):a,(1,2):b})
        for x,y in ((0,0),(1,0),(0,1),(1,1),(2,-3)):
            H={(6,0):1}
            if x:H[(0,3)]=x
            if y:H[(1,2)]=y
            basis=[E.monomial(d-j,j) for d in range(3) for j in range(d+1)]
            rows=[]
            for depth in range(3):
                images=[E.defects(H,g) for g in basis]
                keys=sorted({(power,exps) for image in images for power,terms in image.items()
                             for exps in terms})
                rows.extend([[image.get(power,{}).get(exps,Fraction(0))
                              for image in images] for power,exps in keys])
                actual=len(E.nullspace(rows,len(basis)))
                predicted=G.specialized_rank(
                    G.observation_matrix(symbolic,2,depth),(a,b),(x,y))["kernel_dimension"]
                self.assertEqual(actual,predicted)
                basis=[E.poisson(H,g) for g in basis]


if __name__=="__main__":
    unittest.main()
