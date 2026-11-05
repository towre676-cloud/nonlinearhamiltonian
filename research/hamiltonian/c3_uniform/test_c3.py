import copy,contextlib,io,json,random,subprocess,sys,unittest
from pathlib import Path
import sympy as s
import family_certificate as F
import verify_certificate as V
import monomial_proof as MP
HERE=Path(__file__).resolve().parent
class C3Tests(unittest.TestCase):
 def test_all_parameter_certificate(self):
  result=V.verify(json.loads((HERE/'family_certificate.json').read_text()))
  self.assertEqual(result['independently_verified_minors'],101)
 def test_corrupted_bezout_rejected(self):
  data=json.loads((HERE/'family_certificate.json').read_text());data['blocks'][0]['bezout'][0]='0'
  with self.assertRaises(AssertionError):V.verify(data)
 def test_missing_block_rejected(self):
  data=json.loads((HERE/'family_certificate.json').read_text());data['blocks'].pop()
  with self.assertRaises(AssertionError):V.verify(data)
 def test_monomial_symbolic_and_counterexample_search(self):
  with contextlib.redirect_stdout(io.StringIO()):MP.run()
 def test_independent_random_operator_comparison(self):
  rng=random.Random(20261104);q,p=V.q,V.p
  for _ in range(32):
   n=rng.randrange(21);a0=s.Rational(rng.randrange(-21,22),rng.randrange(1,8))
   G={(c,n-c):s.Rational(rng.randrange(-4,5),rng.randrange(1,6)) for c in range(n+1)}
   expr=sum(z*q**c*p**e for (c,e),z in G.items());H={m:z.subs(F.a,a0) if hasattr(z,'subs') else z for m,z in F.H.items()}
   Hexpr=V.H.subs(V.a,a0)
   for k in (1,3,5):
    got=F.gate(H,G,k)
    want={m:v for m,v in V.T(Hexpr,expr,k).terms() if v}
    self.assertEqual(got,want)
 def test_exceptional_partners(self):
  q,p,a=V.q,V.p,V.a;R=s.Rational
  cases=[(0,q*q*p),(0,q*p*p),(20,q**3+p**3),(-20,q**3-p**3),
   (R(40,7),q*p**4-q**4*p),(-R(40,7),q*p**4+q**4*p),
   (0,q**8*p**2+q**2*p**8)]
  quadratic=[(a*a+50,q**3*p-a*p**4/10),(a*a+50,q**4+a*q*p**3/5),
   (a*a+50,q**13*p+q*p**13+13*a*(q**4*p**10+q**10*p**4)/20+R(39,2)*(q*p)**7),
   (a*a+5,q**12+p**12+11*a*(q**3*p**9+q**9*p**3)+33*q**6*p**6)]
  for a0,G in cases:
   H=V.H.subs(a,a0)
   self.assertTrue(all(V.T(H,G,k).is_zero for k in (3,5)))
   self.assertFalse(V.T(H,V.T(H,G,1).as_expr(),3).is_zero)
  for modulus,G in quadratic:
   for k in (3,5):self.assertTrue(all(s.rem(z,modulus,a)==0 for _,z in V.T(V.H,G,k).terms()))
   self.assertTrue(any(s.rem(z,modulus,a)!=0 for _,z in V.T(V.H,V.T(V.H,G,1).as_expr(),3).terms()))
 def test_retained_static_tail_certificate(self):
  result=subprocess.run([sys.executable,str(HERE/'inputs/check_binary_static.py'),str(HERE/'inputs/binary_static_d6.json')],capture_output=True,text=True,check=True)
  self.assertEqual(json.loads(result.stdout)['status'],'passed')
if __name__=='__main__':unittest.main(verbosity=2)
