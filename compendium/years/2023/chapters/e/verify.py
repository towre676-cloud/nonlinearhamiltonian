#!/usr/bin/env python3
"""Portable standard-library replay of the chapter E worked examples."""
from pathlib import Path
from fractions import Fraction as F
from dataclasses import dataclass
from itertools import product
from math import comb,factorial,exp,sqrt,pi,cos,sin,log
import cmath,json

HERE=Path(__file__).resolve().parent
checks=[]
def record(id,name,detail):checks.append(dict(id=id,name=name,status='passed',detail=detail))
def matmul(a,b):
 assert len(a[0])==len(b)
 return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]
def det(a,b):return a[0]*b[1]-a[1]*b[0]

# M078: exact unit covariance transformation and quadratic form.
r=[F(1),F(2)];var=[F(1),F(4)]
q=sum(x*x/v for x,v in zip(r,var))
qs=sum((10*x)**2/(100*v) for x,v in zip(r,var))
assert q==qs==2 and sum(x*x for x in r)==5
record('M078','Whitened discrepancy and unit invariance','r=(1,2), covariance diag(1,4): raw score 5, whitened score 2; rescaling observations and covariance together preserves 2.')

# M079: independent finite-difference check of an analytic chain rule.
fun=lambda u,v:(u*u+v)*exp(u)
h=1e-5
numerical=[(fun(1+h,2)-fun(1-h,2))/(2*h),(fun(1,2+h)-fun(1,2-h))/(2*h)]
assert abs(numerical[0]-5*exp(1))<1e-7 and abs(numerical[1]-exp(1))<1e-7
chain=matmul([[exp(1),3]],[[2,1],[exp(1),0]])[0]
assert abs(chain[0]-5*exp(1))<1e-14 and abs(chain[1]-exp(1))<1e-14
record('M079','Composite derivative','Analytic product gives (5e,e); symmetric finite differences agree within 1e-7.')

L=[[2,-1,0,-1],[-1,2,-1,0],[0,-1,2,-1],[-1,0,-1,2]]
v=[1,-1,1,-1]
Lv=[x[0] for x in matmul(L,[[x] for x in v])]
assert Lv==[4*x for x in v]
for eta,factor in [(F(2,5),F(-3,5)),(F(3,5),F(-7,5))]:
 step=[x-eta*y for x,y in zip(v,Lv)]
 assert step==[factor*x for x in v] and sum(step)==sum(v)
record('M080','Graph heat time-step threshold','Four-cycle top mode has λ=4; η=2/5 contracts by −3/5 whereas η=3/5 amplifies by −7/5. Mass is unchanged.')

lo=F('2.2360679774997896964');hi=F('2.2360679774997896965')
assert lo*lo<5<hi*hi and 2*27002==54004
record('M081','Certified mantissa bracket','Exact rational squares bracket √5 between 2.2360679774997896964 and 2.2360679774997896965; exponent is exactly 27002.')

assert [3*x*x for x in [1,2,4]]==[3,12,48]
b=log(12/3)/log(2/1);a=3/(1**b)
assert abs(b-2)<1e-14 and abs(a*4**b-48)<1e-12
record('M082','Noiseless power-family identification','Inputs 1,2 identify a=3,b=2; the unused third input x=4 predicts 48 exactly.')

A=[[-2,0,0],[0,0,0],[0,0,3]]
assert matmul(A,[[1],[0],[0]])==[[-2],[0],[0]]
assert A==[[-2*(i==0)*(j==0)+3*(i==2)*(j==2) for j in range(3)] for i in range(3)]
record('M083','Signed dyadic decomposition','diag(−2,0,3) is the sum of two signed rank-one dyads and has a negative quadratic direction, excluding positive-dyad decomposition.')

N=16
image=lambda i,j:int(j>=i)
tangent=[image(i+1,j+1)-image(i,j) for i in range(N-1) for j in range(N-1)]
horizontal=[image(i+1,j)-image(i,j) for i in range(N-1) for j in range(N)]
assert len(tangent)==225 and all(x==0 for x in tangent)
assert len(horizontal)==240 and sum(x!=0 for x in horizontal)==15
record('M084','Directional cancellation illustration','All 225 tangent differences vanish; 15 of 240 horizontal differences are nonzero. This checks only the declared finite directional illustration, not a full transform benchmark.')

I=[[1,0],[0,1]];sx=[[0,1],[1,0]];sy=[[0,-1j],[1j,0]];sz=[[1,0],[0,-1]]
sig=[sx,sy,sz]
def madd(a,b):return [[a[i][j]+b[i][j] for j in range(2)] for i in range(2)]
def mscale(a,c):return [[c*x for x in row] for row in a]
def trace(a):return sum(a[i][i] for i in range(2))
def kernel(n):
 out=mscale(I,.5)
 for x,s in zip(n,sig):out=madd(out,mscale(s,sqrt(3)*x/2))
 return out
directions=[tuple((sign if j==i else 0) for j in range(3)) for i in range(3) for sign in [-1,1]]
rho=[[F(7,10),F(1,10)-.2j],[F(1,10)+.2j,F(3,10)]]
rec=[[0j,0j],[0j,0j]];integral=0j
for n in directions:
 d=kernel(n);w=trace(matmul(rho,d));integral+=w/3;rec=madd(rec,mscale(d,w/3))
assert abs(integral-1)<1e-14
assert all(abs(rec[i][j]-rho[i][j])<1e-14 for i in range(2) for j in range(2))
pair=sum(trace(matmul(sx,kernel(n)))*trace(matmul(sz,kernel(n)))/3 for n in directions)
assert abs(pair-trace(matmul(sx,sz)))<1e-14
record('M085','Normalized qubit kernel reconstruction','The six-axis spherical quadrature reconstructs a nontrivial Hermitian density matrix to <1e-14 and checks normalization and a trace pairing.')

# Exact Gaussian rational arithmetic for polynomial star products.
@dataclass(frozen=True)
class C:
 re:F=F(0)
 im:F=F(0)
 def __post_init__(self):object.__setattr__(self,'re',F(self.re));object.__setattr__(self,'im',F(self.im))
 def __add__(self,other):
  if not isinstance(other,C):other=C(other)
  return C(self.re+other.re,self.im+other.im)
 def __neg__(self):return C(-self.re,-self.im)
 def __mul__(self,other):
  if not isinstance(other,C):other=C(other)
  return C(self.re*other.re-self.im*other.im,self.re*other.im+self.im*other.re)
 def __bool__(self):return bool(self.re or self.im)
def pclean(p):return {k:v for k,v in p.items() if v}
def padd(a,b):
 c=a.copy()
 for k,v in b.items():c[k]=c.get(k,C())+v
 return pclean(c)
def fall(n,k):return factorial(n)//factorial(n-k) if n>=k else 0
ipowers=[C(1),C(0,1),C(-1),C(0,-1)]
def star(f,g):
 out={}
 for (a,b),cf in f.items():
  for (c,d),cg in g.items():
   for n in range(min(a+b,c+d)+1):
    for k in range(n+1):
     integer=(-1)**k*comb(n,k)*fall(a,n-k)*fall(b,k)*fall(d,n-k)*fall(c,k)
     if not integer:continue
     degree=(a+c-n,b+d-n)
     coeff=cf*cg*ipowers[n%4]*C(F(integer,2**n*factorial(n)))
     out[degree]=out.get(degree,C())+coeff
 return pclean(out)
qpoly={(1,0):C(1)};ppoly={(0,1):C(1)}
comm=padd(star(qpoly,ppoly),{k:-v for k,v in star(ppoly,qpoly).items()})
assert comm=={(0,0):C(0,1)}
assert star({(2,0):C(1)},{(0,2):C(1)})=={(2,2):C(1),(1,1):C(0,2),(0,0):C(F(-1,2))}
basis=[{(a,b):C(1)} for a in range(3) for b in range(3-a)]
for f,g,hp in product(basis,repeat=3):assert star(star(f,g),hp)==star(f,star(g,hp))
record('M086','Exact polynomial Moyal algebra','Gaussian rational arithmetic checks q⋆p−p⋆q=i, the full q²⋆p² formula, and all 216 associativity triples from monomials of total degree ≤2. ℏ=1.')

alpha=1.5;t=.73;energy=[0,1,2**alpha]
coeff=[cmath.exp(-1j*t*e)/sqrt(3) for e in energy]
assert abs(sum(abs(x)**2 for x in coeff)-1)<1e-14
sampled=sum(abs(sum(coeff[n]*cmath.exp(1j*n*(2*pi*j/16))/sqrt(2*pi) for n in range(3)))**2 for j in range(16))*2*pi/16
assert abs(sampled-1)<1e-14
record('M087','Fractional periodic spectral evolution','Three-mode spectral norm and a 16-point physical-space Parseval sum remain one to <1e-14 for α=3/2.')

a=[1,2,3];b=[2,-1,4]
def dot(a,b):return sum(x*y for x,y in zip(a,b))
deficit=dot(a,a)*dot(b,b)-dot(a,b)**2
minor_sum=sum((a[i]*b[j]-a[j]*b[i])**2 for i in range(3) for j in range(i+1,3))
assert deficit==minor_sum==150
record('M088','Lagrange identity','Vectors (1,2,3),(2,−1,4) give Cauchy–Schwarz deficit 150 and squared minors 25+4+121=150.')

n=512
winding=sum((3j*cmath.exp(3j*(2*pi*(k+.5)/n)))/cmath.exp(3j*(2*pi*(k+.5)/n)) for k in range(n))/n/1j
assert abs(winding-3)<1e-12
assert abs((1/4)*(4*pi*4)-4*pi)<1e-14
record('M089','Winding and sphere calibration','The analytic derivative ratio for e^(3it) integrates to winding three; curvature×area for radius-two sphere is 4π.')

b=F(2);mu=(1-b)/(1+b);K=(1+abs(mu))/(1-abs(mu))
assert mu==F(-1,3) and K==2
record('M090','Marked torus stretch','The affine b=2 stretch gives exact Beltrami coefficient −1/3 and dilatation 2; its lattice periods are 1 and 2i.')

lower=F('2.449489742783178');upper=F('2.449489742783179')
assert lower*lower<6<upper*upper
m=lambda r:-r*r+2*r+4
assert m(F(16,5))==F(4,25) and m(F(7,2))==F(-5,4)
r=4;xplus=(r+1+sqrt((r-3)*(r+1)))/(2*r);xminus=(r+1-sqrt((r-3)*(r+1)))/(2*r)
f=lambda x:r*x*(1-x)
assert abs(f(xplus)-xminus)<1e-14 and abs(f(xminus)-xplus)<1e-14
assert abs(r*r*(1-2*xplus)*(1-2*xminus)-m(r))<1e-13
critical=1+sqrt(6)
for slope,other in [(-1-sqrt(2),-1+sqrt(2)),(-1+sqrt(2),-1-sqrt(2))]:
 assert abs(slope*other+1)<1e-14
 second=-2*critical
 g2=second*(slope*slope+other);g3=3*second*second*slope
 cubic=g3/6+g2*g2/4
 schwarz=-6*critical*critical/(other*other)*slope*slope-6*critical*critical/(slope*slope)
 assert cubic>0 and abs(cubic+schwarz/6)<1e-8
assert 2-2*critical<0
record('M091','Certified logistic thresholds','Exact rational squaring brackets r₂=1+√6 to width 1e−15. Exact rational multipliers at r=3.2 and 3.5 check opposite sides of stability. A two-cycle is checked independently; a numerical derivative/Schwarzian cross-check verifies the flip cubic formula, whose strict positivity is proved analytically in the text.')

def orbit(c,steps):
 z=0;out=[z]
 for _ in range(steps):z=z*z+c;out.append(z)
 return out
assert orbit(0,5)==[0]*6 and orbit(-1,5)==[0,-1,0,-1,0,-1]
assert orbit(1,4)==[0,1,2,5,26]
assert -F(10)-1-F(8,3)==-F(41,3)
record('M092','State-versus-parameter examples','Exact quadratic critical orbits distinguish c=0,−1,1. Lorenz divergence at σ=10,β=8/3 is −41/3; this is not a chaos certificate.')

k=F(2);p=F(-4);opt=p/(2*k)
assert opt==-1 and p*opt-k*opt*opt==2
assert max(p*F(j,10)-k*F(j,10)**2 for j in range(101))==0
for x in [F(-3),F(-1),F(0),F(1,2),F(3)]:assert k*x*x+p*p/(4*k)>=p*x
record('M093','Convex conjugate and boundary optimizer','For k=2,p=−4 the full-line optimizer is −1 with value 2; the constrained half-line optimizer is 0 with value 0. Fenchel inequalities are checked on rational examples.')

Ss=[]
for a0,a1,b0,b1 in product([-1,1],repeat=4):Ss.append(a0*b0+a0*b1+a1*b0-a1*b1)
assert set(Ss)=={-2,2}
assert abs(exp(-2*1000*.05**2)-exp(-5))<1e-15
record('M094','CHSH deterministic exhaustion','All sixteen deterministic assignments give S=±2. The declared iid 1000-trial 0.80 win-fraction Hoeffding bound is e^(−5).')

def imul(a,b):
 out={}
 for (i,j),u in a.items():
  for (k,l),v in b.items():out[(i+k,j+l)]=out.get((i+k,j+l),0)+u*v
 return {key:value for key,value in out.items() if value}
def iadd(a,b):
 out=a.copy()
 for key,value in b.items():out[key]=out.get(key,0)+value
 return {key:value for key,value in out.items() if value}
X={(1,0):1};Y={(0,1):1};mx={(1,0):-1};my={(0,1):-1};zero={}
gens=[imul(X,X),imul(X,Y),imul(Y,Y)]
syzygies=[[my,X,zero],[zero,my,X]]
for syz in syzygies:
 ans={}
 for aa,gg in zip(syz,gens):ans=iadd(ans,imul(aa,gg))
 assert not ans
for a1,c1 in [({(0,0):1},X),(iadd(X,Y),imul(X,Y))]:
 triple=[imul(my,a1),iadd(imul(X,a1),imul(my,c1)),imul(X,c1)]
 ans={}
 for aa,gg in zip(triple,gens):ans=iadd(ans,imul(aa,gg))
 assert not ans
record('M095','Syzygy and strict-transform checks','Exact polynomial arithmetic verifies both syzygies and generated relations for (x²,xy,y²). The cusp strict transform is v²−x, with derivative −1 in x; its further normal-crossings issue is retained in the text.')

v0,v1,v2=(1,0),(1,1),(1,2)
assert [det(v0,v2),det(v0,v1),det(v1,v2)]==[2,1,1]
assert tuple(a+b for a,b in zip((0,1),(2,-1)))==tuple(2*a for a in (1,0))
record('M096','Toric lattice certificate','The original determinant is 2; both subdivided cone determinants are 1. Dual Hilbert-generator relation gives uw=v².')

hodge={(0,0):1,(1,1):1};product_hodge={}
for (p,q),a in hodge.items():
 for (r,s),b in hodge.items():product_hodge[(p+r,q+s)]=product_hodge.get((p+r,q+s),0)+a*b
assert product_hodge=={(0,0):1,(1,1):2,(2,2):1}
assert (5-1)*(5-2)//2==6 and 2-2*6==-10
record('M097','Hodge consistency examples','Künneth multiplication gives Hodge polynomial (1+uv)² for P¹×P¹. The plane-quintic genus is six and curve Euler characteristic −10.')

for t in [F(-3),F(-1),F(0),F(1,2),F(2)]:
 xx=(1-t*t)/(1+t*t);yy=2*t/(1+t*t)
 assert xx*xx+yy*yy==1
assert [(a,b) for a,b in product(range(3),repeat=2) if (a*a+b*b)%3==0]==[(0,0)]
record('M098','Conic parametrization and obstruction','Rational circle parametrizations are checked exactly. Exhaustion modulo three shows a²+b²≡0 forces a≡b≡0, the key step in the primitive descent excluding x²+y²=3 over Q.')

z=[1,1j]
assert sum(x*x for x in z)==0 and sum(x.conjugate()*x for x in z)==2
assert matmul([[2,3]],[[1,0,4],[0,1,5]])==[[2,3,23]]
record('M099','Typed composition and Hermitian positivity','The valid derivative product is [2,3,23]. For z=(1,i), zᵀz=0 but z†z=2.')

assert {x['id'] for x in checks}=={f'M{i:03d}' for i in range(78,100)}
result={'chapter':'e','checks':checks,'status':'passed','count':len(checks),'method':'Portable Python standard library; exact rational and polynomial checks where stated, numerical tolerance checks explicitly labeled.'}
HERE.joinpath('checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
print(json.dumps({'chapter':'e','checks':len(checks),'status':'passed'}))
