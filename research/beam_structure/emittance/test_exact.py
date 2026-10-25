"""Independent exact finite-cloud tests of cancellation, sign and coupling."""
from fractions import Fraction as Q
from itertools import product
import random
import unittest
from exact import (scalar_kick,vector_kick,determinant,is_psd,
                   sqrt_difference_leq,conditional_emittance_interval,sqrt_upper)


class ScalarTests(unittest.TestCase):
    def test_random_weighted_clouds(self):
        rng=random.Random(20261024)
        for case in range(240):
            n=rng.randrange(3,12)
            x=[rng.randrange(-7,8) for _ in range(n)]
            if len(set(x))==1:x[-1]+=1
            p=[rng.randrange(-8,9) for _ in range(n)]
            f=[rng.randrange(-9,10) for _ in range(n)]
            masses=[rng.randrange(1,7) for _ in range(n)];total=sum(masses)
            w=[Q(v,total) for v in masses];h=Q(rng.randrange(-4,5),7)
            out=scalar_kick(x,p,f,h,w)
            self.assertEqual(out['identity_rhs'],out['epsnew2'])
            self.assertEqual(out['orthogonality_residuals'],(0,0))
            self.assertTrue(out['gram_psd'])
            box=conditional_emittance_interval(out['eps2'],out['a'],h,out['g_variance'])
            self.assertLessEqual(box['lower']**2,out['epsnew2'])
            self.assertGreaterEqual(box['upper']**2,out['epsnew2'])

    def test_affine_force_removal_and_offsets(self):
        x=[-3,-1,0,2,5];p=[4,2,-5,1,7];force=[2*t+7 for t in x]
        out=scalar_kick(x,p,force,Q(3,5))
        self.assertEqual(out['g_variance'],0)
        self.assertEqual(out['ug'],0)
        self.assertEqual(out['eps2'],out['epsnew2'])
        shifted=scalar_kick([t+13 for t in x],[t-21 for t in p],[t+17 for t in force],Q(3,5))
        for key in ['a','eps2','epsnew2','g_variance','ug']:self.assertEqual(out[key],shifted[key])

    def test_bound_sharp_for_position_dependent_force(self):
        x=[-1,0,1];p=[t*t for t in x];f=[2*t*t for t in x]
        out=scalar_kick(x,p,f,Q(1,2))
        self.assertEqual(out['epsnew2'],4*out['eps2'])
        self.assertEqual(out['radius_squared'],out['eps2'])
        # sqrt(epsnew2)-sqrt(eps2) exactly equals the bound.

    def test_signed_correlation_can_reduce_emittance(self):
        out=scalar_kick([-1,0,1],[1,0,1],[-1,0,-1],Q(1,2))
        self.assertLess(out['ug'],0);self.assertLess(out['epsnew2'],out['eps2'])

    def test_invalid_inputs(self):
        with self.assertRaises(ValueError):scalar_kick([1,1],[2,3],[4,5],1)
        with self.assertRaises(ValueError):scalar_kick([1,2],[2,3],[4,5],1,[Q(-1),Q(2)])
        with self.assertRaises(TypeError):scalar_kick([1.,2.],[2,3],[4,5],1)
        with self.assertRaises(ValueError):conditional_emittance_interval(1,1,1,-1)
        with self.assertRaises(ValueError):sqrt_difference_leq(-1,1,1)

    def test_sqrt_rounding(self):
        for v in [Q(0),Q(1),Q(2),Q(1,9),Q(100,17)]:
            bound=sqrt_upper(v,20)
            self.assertGreaterEqual(bound*bound,v)
            if bound:self.assertLessEqual((bound-Q(1,1<<20))**2,v)


class VectorTests(unittest.TestCase):
    def test_random_vector_clouds(self):
        rng=random.Random(1210)
        for case in range(90):
            q=[[rng.randrange(-4,5),rng.randrange(-4,5)]for _ in range(10)]
            # Add a fixed noncollinear triple to avoid singular q covariance.
            q[:3]=[[0,0],[1,0],[0,1]]
            p=[[rng.randrange(-5,6),rng.randrange(-5,6)]for _ in q]
            f=[[rng.randrange(-6,7),rng.randrange(-6,7)]for _ in q]
            out=vector_kick(q,p,f,Q(case%7-3,11))
            self.assertEqual(out['Unew'],out['identity_rhs'])
            self.assertTrue(out['joint_gram_psd'])

    def test_cross_plane_linear_force_changes_projected_not_full(self):
        cloud=list(product([-1,1],repeat=4))
        q=[[x,y]for x,p,y,v in cloud];p=[[u,v]for x,u,y,v in cloud]
        # Symmetric cross-plane kick is canonical, not merely volume preserving.
        force=[[y,x]for x,u,y,v in cloud]
        out=vector_kick(q,p,force,1)
        self.assertEqual(out['G'],[[0,0],[0,0]])
        self.assertEqual(out['C'],[[0,0],[0,0]])
        self.assertEqual(out['Unew'],out['U'])
        scalar=scalar_kick([row[0]for row in q],[row[0]for row in p],[row[0]for row in force],1)
        self.assertEqual(scalar['eps2'],1);self.assertEqual(scalar['epsnew2'],2)
        self.assertEqual(out['det_covariance'],1)

    def test_all_principal_minors_not_just_diagonals(self):
        self.assertFalse(is_psd([[1,2],[2,1]]))
        self.assertTrue(is_psd([[1,1],[1,1]]))

    def test_singular_position_chart_rejected(self):
        with self.assertRaises(ValueError):vector_kick([[0,0],[1,1]],[[0,1],[1,0]],[[0,0],[0,0]],1)


if __name__=='__main__':unittest.main()
