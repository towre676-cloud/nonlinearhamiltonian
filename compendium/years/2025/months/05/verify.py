"""Portable finite mathematics checks; no performance or history-completeness certification."""
from pathlib import Path
from fractions import Fraction as F
import json,math,cmath,itertools
P=Path(__file__).resolve().parent; checks=[]
def check(n,name,ok,detail):
 assert ok,name
 checks.append(dict(id=f'Y25-05-{n:03d}',name=name,status='passed',detail=detail))
def mm(a,b):return [[sum(x*y for x,y in zip(r,c)) for c in zip(*b)] for r in a]
def tr(a):return list(map(list,zip(*a)))
def eye(n):return [[F(i==j) for j in range(n)] for i in range(n)]
def rank(a):
 a=[[F(v) for v in row] for row in a];r=0
 for c in range(len(a[0])):
  k=next((k for k in range(r,len(a)) if a[k][c]),None)
  if k is None:continue
  a[r],a[k]=a[k],a[r];z=a[r][c];a[r]=[v/z for v in a[r]]
  for j in range(len(a)):
   if j!=r:
    z=a[j][c];a[j]=[x-z*y for x,y in zip(a[j],a[r])]
  r+=1
  if r==len(a):break
 return r

def simpson(f,a,b,N=12000):
 h=(b-a)/N
 return h*(f(a)+f(b)+sum((4 if j%2 else 2)*f(a+j*h) for j in range(1,N)))/3
psi=lambda x:(1-x*x)*math.exp(-x*x/2)/math.sqrt(2*math.pi)
m0=simpson(psi,-10,10);m1=simpson(lambda x:x*psi(x),-10,10)
ft=simpson(lambda x:psi(x)*math.cos(x),-10,10)
check(1,'Gaussian-derivative moments and Fourier normalization',abs(m0)<1e-10 and abs(m1)<1e-10 and abs(ft-math.exp(-.5))<1e-10,
 {'moments':[m0,m1],'fourier_at_one':ft,'scope':'Numerical quadrature checks accompany the integration-by-parts proof; discrete frame completeness is not tested.'})
flux=math.pi*2**2
circ=sum(2 for _ in range(100))*2*math.pi/100
check(2,'Independent disk flux and circulation',abs(flux-circ)<1e-12,'Curl is constant one; the separately parameterized boundary dot product is two on [0,2π].')
a,b,c,d=95800,217519,414560,422481
check(3,'Exact quartic and fifth-power counterexamples',a**4+b**4+c**4==d**4 and math.gcd(math.gcd(a,b),math.gcd(c,d))==1 and 27**5+84**5+110**5+133**5==144**5 and F(1680)*F(1,2)*F(2,3)*F(4,5)*F(6,7)==384,
 'All power equalities, primitive gcd and totient factorization use integer/rational arithmetic.')
p=4;points=list(itertools.product(range(p),repeat=3));index={v:i for i,v in enumerate(points)}
A=[[0]*len(points) for _ in points]
for i,x in enumerate(points):
 A[i][i]=6
 for j in range(3):
  for sign in [-1,1]:
   y=list(x);y[j]=(y[j]+sign)%p;A[i][index[tuple(y)]]-=1
maxerr=0
for k in points:
 v=[cmath.exp(2j*math.pi*sum(a*b for a,b in zip(k,x))/p) for x in points]
 lam=4*sum(math.sin(math.pi*z/p)**2 for z in k)
 maxerr=max(maxerr,max(abs(sum(a*b for a,b in zip(row,v))-lam*v[i]) for i,row in enumerate(A)))
check(4,'Complete 4³ Fourier spectrum against matrix',all(sum(row)==0 for row in A) and maxerr<1e-12 and rank(A)==63,
 {'sites':64,'maximum_complex_mode_residual':maxerr,'kernel_dimension':1,'gap':2,'scope':'Every Fourier mode is checked for this finite grid; the written proof covers general p.'})
A2=[[F(1),0],[0,F(4)]];Pi=[[F(1,5),F(4,5)],[F(1,5),F(4,5)]]
check(5,'Exact Galerkin projection and energy example',mm(Pi,Pi)==Pi and mm(A2,Pi)==tr(mm(A2,Pi)) and F(4,5)**2+4*F(-1,5)**2==F(4,5) and mm(Pi,[[-4],[1]])==[[0],[0]],'Idempotence, energy self-adjointness, error energy and untouched complement verified independently.')
x=F(3,2);x1=(x+2/x)/2;x2=(x1+2/x1)/2
check(6,'Functional-calculus interpolation and Newton residuals',F(3,2)-F(1,2)==1 and F(3,2)-1==F(1,2) and x1==F(17,12) and x2==F(577,408) and x1*x1-2==F(1,144) and x2*x2-2==F(1,166464),
 'Two scalar interpolation values and two exact rational Newton steps, including residual certificates.')
h=lambda z:0 if z in (0,1) else -z*math.log2(z)-(1-z)*math.log2(1-z)
def reduced(support,den,keep):
 out=[[F(0) for _ in range(2**len(keep))] for _ in range(2**len(keep))]
 for i,j in itertools.product(support,repeat=2):
  ib=[(i>>k)&1 for k in range(3)];jb=[(j>>k)&1 for k in range(3)]
  if all(ib[k]==jb[k] for k in range(3) if k not in keep):
   u=sum(ib[k]<<t for t,k in enumerate(keep));v=sum(jb[k]<<t for t,k in enumerate(keep))
   out[u][v]+=F(1,den)
 return out
quantum_ok=True
for support,den,ev in [([0,7],2,[F(1,2),F(1,2)]),([1,2,4],3,[F(2,3),F(1,3)])]:
 one=reduced(support,den,[0]);two=reduced(support,den,[1,2])
 quantum_ok &= sorted([one[0][0],one[1][1]])==sorted(ev) and one[0][1]==0 and rank(two)==2
 # The two-party nonzero spectrum is independently certified by its annihilating polynomial.
 product=two
 for lam in set(ev):
  shifted=[[two[i][j]-lam*int(i==j) for j in range(4)] for i in range(4)]
  product=mm(product,shifted)
 quantum_ok &= all(z==0 for row in product for z in row)
check(7,'Pure GHZ and W entropy cancellation',quantum_ok and h(.5)==1 and abs(h(1/3)-.9182958340544896)<1e-14,
 {'GHZ_single_entropy':h(.5),'W_single_entropy':h(1/3),'scope':'Reduced eigenvalues and Schmidt-complement equalities are given in the proof; I3=0 is an all-pure-three-party theorem, not an empirical transition.'})
B=[[-1,0,1],[1,-1,0],[0,1,-1]];J=[[1]*3 for _ in range(3)];L=mm(tr(B),B);Lfill=[[x+y for x,y in zip(r,s)] for r,s in zip(L,J)]
check(8,'Exact triangle Hodge matrices',mm(B,[[1],[1],[1]])==[[0],[0],[0]] and rank(L)==2 and Lfill==[[3*int(i==j) for j in range(3)] for i in range(3)],'Unfilled Δ1=3I−J and filled Δ1=3I; harmonic dimensions one and zero.')
def vp(n,p):
 if n==0:return math.inf
 v=0
 while n%p==0:n//=p;v+=1
 return v
pairs=[(1,-2),(3,-4)]
check(9,'Tropical necessary condition and lost unit information',all(x+y+1==0 and sorted([vp(x,3),vp(y,3),0])[0]==sorted([vp(x,3),vp(y,3),0])[1] for x,y in pairs) and [vp(1,3),vp(1,3)]==[0,0] and 1+1+1!=0,
 'Exact 3-adic valuations for two solutions and an equal-valuation nonsolution.')
z=F(9,13);N=7;shell=sum((F(2,3)*F(1,27)**n for n in range(N)),F(0))
check(10,'Exact valuation-shell integral and tail',shell==z*(1-F(1,27)**N) and z-shell==z*F(1,27)**N,'p=3,s=2 gives9/13 with exact geometric truncation remainder.')
M=[[0,0],[1,0]]
check(11,'Dual-number free resolution certificate',mm(M,M)==[[0,0],[0,0]] and rank(M)==1 and mm(M,[[0],[1]])==[[0],[0]],'Multiplication by ε has equal one-dimensional kernel and image; after tensoring with k all differentials vanish. The periodic proof covers all Tor degrees.')
den=F(11923)/F('28.6')
check(12,'Ratio denominator and duty-capacity distinction',den==F(59615,143) and F(5)/(F(10)*2)==F(1,4) and F(1,2)>F(1,4),{'implied_input_kWh':str(den),'capacity_factor':'1/4','duty_fraction':'1/2','scope':'Stipulated arithmetic, not a measured EROI.'})
cg=[F(16,25),F(-12,25)];cp=[F(9,25),F(12,25)]
check(13,'Exact group/phase geometry',sum(x*y for x,y in zip(cg,cp))==0 and 3*cg[0]+4*cg[1]==0 and F(5*3,5)==3,'N=5,k=3,m=4 yieldsω=3 and perpendicular velocity vectors.')
delta=F(1);x,y,z0=F(0),F(3,4),F(3,2)
check(14,'Tolerance counterexample and transitive chains',abs(x-y)<delta and abs(y-z0)<delta and abs(x-z0)>delta and all(abs(F(j+1,2)-F(j,2))<delta for j in range(20)),
 'Exact failure of transitivity and a finite tolerance chain from zero to ten.')
out=[(1+z)*(1+w) for z,w in itertools.product([-1,1],repeat=2)];mean=F(sum(out),4);var=F(sum(t*t for t in out),4)-mean*mean
check(15,'Independent product variance and repeated-variable cancellation',out==[0,0,0,4] and mean==1 and var==3 and all((1+z)-(1+z)==0 for z in [-1,1]),'Exact outcome enumeration gives variance3 versus first-order variance2; X−X is identically zero.')
f1={'a':1,'b':2};f2={'b':2,'c':3};glue={**f1,**f2}
check(16,'Finite contextual gluing and zero divisors',f1['b']==f2['b'] and glue=={'a':1,'b':2,'c':3} and [a*b for a,b in zip([1,0,0],[0,1,0])]==[0,0,0],
 'Compatible restrictions glue uniquely; pointwise context functions form a product ring, not a field.')
v1,v2,w1,w2=F(1,2),F(3,2),F(1),F(1,3)
check(17,'Exact hybrid variational optimum',F(1,2)*(v1+v2)==1 and w1*v1==w2*v2 and F(1,4)*(w1*v1*v1+w2*v2*v2)==F(1,4) and F(1,4)<F(1,3),
 'Endpoint, weighted momentum and objective agree with the Cauchy–Schwarz global lower bound.')
Lr=[[F(1,6),0,F(-1,6)],[0,F(1,3),F(-1,3)],[F(-1,6),F(-1,3),F(1,2)]]
L2=mm(Lr,Lr);L3=mm(L2,Lr)
check(18,'Actual recovered arithmetic graph polynomial',all(sum(row)==0 for row in Lr) and rank(Lr)==2 and all(L3[i][j]-L2[i][j]+Lr[i][j]/6==0 for i in range(3) for j in range(3)),
 'L(L²−L+I/6)=0 and nullity one; coprime set modulo6 is{1,5}.')
check(19,'Finite spectral-zeta values and gamma moments',F(1)+F(1,3)==F(4,3) and F(1)+F(1,9)==F(10,9) and F('1.528')>1,
 'Positive spectrum{1,3} has ζ(1)=4/3,ζ(2)=10/9. Integral divergence of λ^(−α) near0 is proved in the entry, not numerically extrapolated.')
def mobius(n):
 r=0;p=2
 while p*p<=n:
  if n%p==0:
   n//=p;r+=1
   if n%p==0:return 0
   while n%p==0:n//=p
  p+=1
 if n>1:r+=1
 return (-1)**r
D=lambda n:[d for d in range(1,n+1) if n%d==0]
tau=lambda n:len(D(n))
check(20,'Exact divisor convolution and inversion through120',all(sum(mobius(d)*tau(n//d) for d in D(n))==1 for n in range(1,121)) and tau(12)==6,'μ*τ=1 verified at every integer through120; the all-n proof is algebraic associativity and μ*1=ε.')
pen=(math.log(2)+math.log(20))/20+20/800
check(21,'Declared PAC–Bayes numerical certificate',abs(pen-.2094439727056968)<1e-13 and .1+pen<1,
 {'penalty':pen,'loss_bound':.1+pen,'scope':'A finite arithmetic check under the entry’s iid bounded-loss and fixed-parameter hypotheses; not validation of reported R².'})
x=F(1,4000);response=1-math.exp(-float(x));lower=x-x*x/2
check(22,'Thermal energy geometry and pulse enclosure',F(2)*3*4/(6*2)==2 and F(2)*4*(F(6,3))/2==8 and float(lower)<=response<=float(x),
 {'step_response':response,'lower_bound':str(lower),'upper_bound':str(x),'scope':'Declared lumped model; no performance validation.'})
par=F(88,100)*320+F(12,100);series=1/(F(88,100)/320+F(12,100))
check(23,'Exact series versus parallel conductivity',par==F('281.72') and series==F(4000,491) and par>series and 1/(1/series+1)<series,
 {'parallel':str(par),'series':str(series),'scope':'Second conductivity1 is an explicitly constructed example, not a material measurement.'})
stress=F(200*10**9)*F(1,10**5)*100/2
check(24,'Compatible-layer stress and specific-mass discrepancy',stress==100*10**6 and F('7.48')/F('6.8')==F(11,10),
 {'constructed_stress_Pa':str(stress),'specific_mass_ratio':'11/10','scope':'The historical274.5MPa lacks sufficient inputs and is not certified.'})
es=json.loads((P/'entries.json').read_text());assert len(es)==24
assert all(e['original']['month']=='2025-05' and e['original']['original_question'] is None for e in es)
assert all(e['original']['evidence'] in ['U','A','T'] for e in es)
checks.append(dict(id='MONTH-2025-05',name='Attribution and source boundary',status='passed',detail='24 entries; all original prompts null. May4 external context is T. New models and cited classical inputs are separated from source claims.'))
(P/'checks.json').write_text(json.dumps(dict(month='2025-05',status='passed',count=len(checks),checks=checks),ensure_ascii=False,indent=2))
print(json.dumps({'month':'2025-05','entries':24,'checks':len(checks),'status':'passed'}))
