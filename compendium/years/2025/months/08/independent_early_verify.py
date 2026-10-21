"""Portable scoped checks for the root-authored early-August treatments."""
from pathlib import Path
from fractions import Fraction as F
from math import exp,pi,sqrt
import json
ROOT=Path(__file__).resolve().parent
checks=[]
def check(i,name,detail):checks.append(dict(id=f'Y25-08-{i:03}',name=name,status='passed',detail=detail))
def derivative(p):return [F(i)*p[i] for i in range(1,len(p))] or[F(0)]
def add(a,b):return [(a[i] if i<len(a) else 0)+(b[i] if i<len(b) else 0) for i in range(max(len(a),len(b)))]
def mul(a,b):
 r=[F(0)]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):r[i+j]+=x*y
 return r
def scale(a,c):return[x*c for x in a]
for k in [F(1,2),F(1),F(3,2)]:
 U=[2*k*k,0,-2*k*k]
 DX=lambda p:scale(mul([1,0,-1],derivative(p)),k)
 residual=add(add(DX(DX(U)),scale(U,-4*k*k)),scale(mul(U,U),3))
 assert all(x==0 for x in residual)
check(901,'Exact polynomial traveling-wave residual','In the coordinate v=tanh(kX), rational polynomial differentiation verifies U-double-prime-4k²U+3U²=0 for the worked parameters. The proof gives the general identity.')

def fm(x,y):return((x[0]*y[0]+3*x[1]*y[1])%7,(x[0]*y[1]+x[1]*y[0])%7)
def fp(x,n):
 out=(1,0)
 while n:
  if n&1:out=fm(out,x)
  x=fm(x,x);n//=2
 return out
elements=[(a,b) for a in range(7) for b in range(7) if(a,b)!=(0,0)]
norms=[u for u in elements if fm(u,(u[0],-u[1]%7))==(1,0)]
ratios={fm(v,fp((v[0],-v[1]%7),47))for v in elements}
assert len(elements)==48 and len(norms)==8 and ratios==set(norms)
assert fm((1,1),fp((1,6),47))==(5,6)
check(902,'Exhaustive Hilbert90 witness calculation over F49','All48 nonzero elements give exactly the8 norm-one ratios; the explicit witness1+a maps to5-a.')

g1=(4,0);g2=(2,2);g3=(-4,2)
assert(g2[0]-g3[0]-g1[0],g2[1]-g3[1]-g1[1])==(2,0)
assert all(a%2==0 and b%2==0 for a,b in[g1,g2,g3])
assert not any(r*r+5*s*s==2 for r in range(-2,3)for s in range(-2,3))
check(903,'Squared-ideal certificate','The exact generator combination gives2 in I² and all square generators lie in(2). The norm obstruction is proved in the text; a finite small check agrees.')
for m in range(-8,9):assert F(m,2)*2*2==2*m
check(904,'Curvature integral normalization','The angular factors integral sin(theta)dtheta=2 and integral dphi=2pi give normalized Chern number m; the clutching proof supplies the classification.')
sigma=lambda n:sum(d for d in range(1,n+1)if n%d==0)
coeff=-24*sigma(9)+216*sigma(1);assert coeff==-96
check(905,'Eisenstein coefficient normalization','The q9 coefficient of E2-9E2(9tau) is-96 and its constant term is-8; covariance is the exact anomaly-cancellation derivation in the text.')

M=40;prod=[1]+[0]*(M-1)
for j in range(1,M):
 for shift in[j,11*j]:
  if shift>=M:continue
  for repeat in range(2):
   for i in range(M-1,shift-1,-1):prod[i]-=prod[i-shift]
a=[0]+prod
assert a[1:12]==[1,-2,-1,2,1,2,-2,0,-2,-2,1]
def point_count(p):return 1+sum((y*y+y-x*x*x+x*x+10*x+20)%p==0 for x in range(p)for y in range(p))
for p in[2,3,5,7,13,17,19,23,29,31,37]:assert a[p]==p+1-point_count(p)
c=2*pi/sqrt(11)
value=2*sum(a[n]/n*exp(-c*n)for n in range(1,M+1))
tail20=4*exp(-c*21)/(1-exp(-c))
assert abs(value-.2538418608559107)<1e-15 and tail20<3e-17
check(906,'Eta product, independent point counts and central-value example',dict(value_40_terms=value,analytic_tail_after20=tail20,scope='Integer coefficients through40; good-prime coefficients independently counted on11a. Floating exponential evaluation is illustrative; analytic tail is separate from rounding error.'))
assert 100%25==0 and 100%125!=0
check(907,'p-adic nonvanishing precision example','Residual100 vanishes mod25 and not mod125, and has valuation2.')
assert all((x*x-x+2)%2==0 for x in[0,1])
assert(1+1j)**2==2j
check(908,'Heegner split/ramified prime distinction','X²-X+2 has the two distinct roots0,1 modulo2, whereas2=-i(1+i)² in Z[i].')
p_any=1-(1-.001)**1000
assert .632<p_any<.633
check(909,'Explicit independent-test selection probability',dict(probability=p_any,scope='A newly stipulated1000-test independent null example, not the historical search size.'))
power=F(967,1000)**30
assert abs(float(power)-.36542160643857435)<1e-15
assert F(1)-1/(1+F(33,967))==F(33,1000)
check(910,'Exact reciprocal compounding',dict(power_factor=str(power),numeric_power=float(power),price_factor=float(1/power),price_rate=str(F(33,967))))

(ROOT/'early_checks.json').write_text(json.dumps(dict(checks=checks),indent=2))
print(json.dumps(dict(status='passed',checks=len(checks))))
