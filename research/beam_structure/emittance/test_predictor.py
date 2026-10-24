from fractions import Fraction as Q
import unittest
from exact import scalar_kick
from predictor import residual_radius_squared,round_profile_radius_squared,propagate


class PredictorTests(unittest.TestCase):
    def test_nonzero_correlation_tightens_radius(self):
        out=residual_radius_squared(Q(1,2),2,10,[4,4])
        self.assertEqual(out['radius_squared'],1)
        self.assertEqual(out['full_force_radius_squared'],5)
        out=residual_radius_squared(1,2,10,[-1,3])
        self.assertEqual(out['radius_squared'],20)

    def test_round_uniform_disk_residual_is_zero(self):
        self.assertEqual(round_profile_radius_squared(1,3,Q(1,2),Q(1,2)),0)
        self.assertEqual(round_profile_radius_squared(1,2,Q(1,2),Q(3,5)),Q(1,20))

    def test_word_contains_direct_empirical_evolution(self):
        x=[Q(-2),Q(-1),Q(0),Q(1),Q(2)];p=[Q(1),Q(-2),Q(0),Q(-2),Q(1)]
        initial=scalar_kick(x,p,[0]*5,0)
        sigma=[[initial['a'],initial['b']],[initial['b'],initial['p_variance']]]
        word=[]
        for index in range(5):
            h=Q(1,10);force=[-v**3 for v in x]
            kick=scalar_kick(x,p,force,h)
            word.append({'kind':'residual_force_kick','premise_id':f'exact finite-cloud step {index}',
                         'radius_squared_upper':kick['radius_squared']})
            p=[v+h*f for v,f in zip(p,force)]
            drift=Q(1,20);x=[v+drift*u for v,u in zip(x,p)]
            word.append({'kind':'uncoupled_symplectic','matrix':[[1,drift],[0,1]]})
        actual=scalar_kick(x,p,[0]*5,0)['eps2']
        out=propagate(sigma,word)
        self.assertLessEqual(out['lower']**2,actual)
        self.assertGreaterEqual(out['upper']**2,actual)
        self.assertFalse(out['force_premises_verified'])

    def test_refuses_unsupported_or_missing_premises(self):
        with self.assertRaises(ValueError):residual_radius_squared(1,1,1,[2,3])
        with self.assertRaises(ValueError):round_profile_radius_squared(1,1,1,0)
        with self.assertRaises(ValueError):propagate([[1,0],[0,1]],[{'kind':'coupled_linear'}])
        with self.assertRaises(ValueError):propagate([[1,0],[0,1]],[{'kind':'residual_force_kick','radius_squared_upper':0}])
        with self.assertRaises(ValueError):propagate([[1,0],[0,1]],[{'kind':'uncoupled_symplectic','matrix':[[2,0],[0,1]]}])


if __name__=='__main__':unittest.main()
