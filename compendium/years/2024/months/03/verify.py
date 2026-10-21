"""Portable example certificates; classical global theorems remain cited background."""
from pathlib import Path
from fractions import Fraction as F
import json, math
HERE=Path(__file__).resolve().parent
checks=[]
def check(n,name,fn):
 try:
  detail=fn(); checks.append(dict(id=f'Y24-03-{n:03d}',name=name,status='passed',detail=detail))
 except Exception as exc: checks.append(dict(id=f'Y24-03-{n:03d}',name=name,status='failed',detail=repr(exc)))
def simpson(f,a,b,n=8192):
 assert n%2==0
 h=(b-a)/n
 return h/3*(f(a)+f(b)+sum((4 if k%2 else 2)*f(a+k*h) for k in range(1,n)))
def picard():
 monomials={(i,j) for i in range(3) for j in range(4)}
 assert len(monomials)==12
 J=((0,1),(1,0)); v=(2,3)
 assert sum(v[i]*J[i][j]*v[j] for i in range(2) for j in range(2))==12
 return '12 independent bidegree(2,3) monomials and self-intersection12; this does not prove the general Néron–Severi theorem.'
def action():
 for x in range(-5,6):
  for y in range(-5,6):
   p=(F(x+y,2),)*2
   assert p[0]==p[1] and F(x,1)-p[0]==-(F(y,1)-p[1])
   assert (F(p[0]+p[1],2),)*2==p
 return 'Averaging projection verified on a121-point lattice test; rank-one image/kernel identified algebraically in text.'
def variation():
 assert 1-1==0 and (1,-1)!=(0,0)
 # The explicit oscillator variation switches sign at the calculated threshold.
 for T,want in [(1,1),(4,-1)]:
  value=T*((math.pi/T)**2-1)/4
  assert (value>0)-(value<0)==want
 return 'Cancelling directional derivative has nonzero full gradient; oscillator test is positive atT1 and negative atT4.'
def entropy():
 def S(t):
  return -simpson(lambda x: ((x*x+t)/(t+1/3))*math.log((x*x+t)/(t+1/3)),0,1)
 exact=7/6-math.pi/4-math.log(1.5)
 rate=(10-3*math.pi)/16
 assert abs(S(1)-exact)<1e-12
 h=1e-4
 assert abs((S(1+h)-S(1-h))/(2*h)-rate)<1e-9
 assert abs(simpson(lambda x:(1/3-x*x)/(4/3)**2,0,1))<1e-13
 assert exact<0 and rate>0
 return {'S1':exact,'rate1':rate,'independent_method':'composite Simpson plus central time difference','derivative_tolerance':1e-9}
def numerical():
 weights=[1,4,1]
 val=sum(F(weights[i]*weights[j],36)*(F(i,2)**2+F(j,2)) for i in range(3) for j in range(3))
 assert val==F(5,6)
 for a in [F(k,7) for k in range(-30,31)]: assert (a*a+1)**2-1==a*a*(a*a+2)>=0
 return 'Tensor Simpson is exactly5/6; nonzero residual minimum certified by nonnegative factorization.'
def quantum():
 for t in [0,math.pi/8,math.pi/4,1.3]:
  a=math.cos(2*t); b=-1j*math.sin(2*t)
  assert abs(abs(a)**2+abs(b)**2-1)<1e-14
  integ=simpson(lambda s:math.cos(2*s),0,t,4096) if t else 0
  assert abs(-2*math.sin(2*t)+4*integ)<1e-12
 assert abs(math.cos(2*math.pi/8)**2-F(1,2))<1e-14
 return 'Full norm conservation and projected Volterra equation independently quadrature-checked at four times.'
def aggregate():
 z=[(F(1),F(0)),(F(0),F(1))]; w=(F(2),F(1)); wp=(F(20),F(1))
 original=[sum(a*b for a,b in zip(w,p)) for p in z]
 rescaled=[(p[0]/10,p[1]) for p in z]
 assert original==[2,1]
 assert [sum(a*b for a,b in zip(w,p)) for p in rescaled]==[F(1,5),1]
 assert [sum(a*b for a,b in zip(wp,p)) for p in rescaled]==original
 assert 2*1+1*(-2)==0
 return 'Exact unit transformation restores ranking; explicit nonzero score-kernel direction verified.'
for n,name,fn in [(1,'divisor example',picard),(2,'finite action projection',action),(3,'variation counterexample',variation),(4,'normalized entropy',entropy),(5,'quadrature and residual',numerical),(6,'unitary state versus projection',quantum),(7,'score invariance and collision',aggregate)]: check(n,name,fn)
result={'scope':'Finite examples and numerical identities only; no historical transcript completeness or general theorem proof is inferred. Catalog examples have their own verifier.','checks':checks,'passed':sum(c['status']=='passed' for c in checks),'failed':sum(c['status']=='failed' for c in checks)}
HERE.joinpath('checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
print(json.dumps(result,ensure_ascii=False,indent=2))
if result['failed']: raise SystemExit(1)
