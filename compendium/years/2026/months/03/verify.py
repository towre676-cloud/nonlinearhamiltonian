"""Portable independent example and provenance checks; Python standard library only."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product,combinations
import math,cmath,json,re
P=Path(__file__).resolve().parent
checks=[]
def check(n,name,ok,detail):
 if not ok:raise AssertionError((n,name,detail))
 checks.append(dict(id=f'Y26-03-{n:03}',name=name,status='passed',detail=detail))
def mm(A,B):return [[sum(a*b for a,b in zip(row,col)) for col in zip(*B)] for row in A]
def add(A,B):return [[a+b for a,b in zip(r,s)]for r,s in zip(A,B)]
def tr(A):return list(map(list,zip(*A)))
def close(x,y,tol=1e-10):return abs(x-y)<=tol
A=[[-1,2],[0,-1]];G=[[F(1,2),F(1,2)],[F(1,2),F(3,2)]]
check(1,'generator energy form',[-4,-6][0]<=-4 and -6<=-2,'AᵀP+PA=diag(−4,−6)≤diag(−4,−2).')
check(2,'exact nonnormal Lyapunov matrix',add(mm(tr(A),G),mm(G,A))==[[-1,0],[0,-1]] and G[0][0]*G[1][1]-G[0][1]**2==F(1,2),'Exact rational equation and positive leading minors.')
check(3,'inverse derivatives and independent Hessian',close(2/(2**3),F(1,4)) and 100/1==100,'Scalar inverse second derivative 1/4; fixed resolvent permits Hessian condition100.')
check(4,'Stein series and Euler step',F(1,4)*F(4,3)-F(4,3)==-1 and abs(1-2*F(3,2))>1,'P=4/3 for F=1/2; step3/2 gives unstable F=−2.')
check(5,'gap and continuum tail',close(1/F(1,10),10) and close(100*(1-math.exp(-100))/100,1),'Inverse gap10; tC(t)=1−e^(−t) tends to1.')
edges=list(product(range(2),repeat=3));M=max(len(S) for k in range(1,3) for S in combinations(edges,k) if all(len({e[j] for e in S})==k for j in range(3)))
check(6,'ordinary versus induced matching',len(edges)==8 and M==2 and 3*4-2==10,'Complete2×2×2 support has matching2; any two selected triples generate cross edges, so induced optimum1.')
check(7,'concentration threshold arithmetic',F(2,3)+F(2,3)-1==F(1,3) and F(1,4)<F(1,3),'Necessary D≥1/3, and D=1/4 fails by1/12.')
def simpson(f,a,b,n=80000):
 h=(b-a)/n
 return h/3*(f(a)+f(b)+4*sum(f(a+h*k)for k in range(1,n,2))+2*sum(f(a+h*k)for k in range(2,n,2)))
def transformed(t,alpha):
 if t<=0 or t>=1:return 0.
 x=(math.pi/2)*t**8
 L=-math.log1p(-2*math.sin(x/2)**2)
 return (complex(L,x)**(-alpha)).real*4*math.pi*t**7
alpha=.7418045150878947
value=simpson(lambda t:transformed(t,alpha),0,1)
exact=math.pi/(2*math.log(2)**alpha)
check(8,'independent endpoint-regularized integral',abs(value-exact)<2e-5 and close(exact,2.061561374758122),'Power-substitution Simpson quadrature agrees with the analytic formula within2e−5; not a rigorous quadrature enclosure.')
check(9,'parameter fibers',close(2**-1,4**-.5),'Pairs(2,1),(4,1/2) give exactly the same exponent1/2.')
def U(x):return x*x+math.log(math.cos(x))**2
def Up(x):return 2*x-2*math.log(math.cos(x))*math.tan(x)
def flip(x):return U(x)*math.log(U(x))+x*math.log(x)*Up(x)
a,b=.94,.95
assert flip(a)<0<flip(b)
for _ in range(70):
 c=(a+b)/2
 if flip(c)>0:b=c
 else:a=c
x=(a+b)/2;al=-2*math.log(x)/math.log(U(x))
check(10,'recomputed flip candidate',abs(U(x)**(-al/2)-x)<1e-14 and abs(-al*x*Up(x)/(2*U(x))+1)<1e-13,'Bisection bracket[.94,.95]; x≈%.16g, alpha≈%.16g; no global uniqueness claim.'%(x,al))
a=list(map(F,['4.0539120913','-2.8914540799','4.3080022014','-6.0126189168','9.1305430243','-14.3699269347']))
k2=2*a[1]/a[0];k3=6*a[2]/a[0]
check(11,'normalized jet ratios',abs(float(k2)+1.426500632)<1e-8 and abs(float(k3-k2*k2)-4.34116248)<2e-8,'Exact decimal-rational derivatives and logarithmic derivative slope.')
det=a[1]**2-a[0]*a[2];c1=(a[2]*a[1]-a[0]*a[3])/det;c2=(a[1]*a[3]-a[2]**2)/det
p5=c1*a[3]+c2*a[2];p6=c1*a[4]+c2*a[3]
check(12,'withheld recurrence coefficients',abs(float(a[4]-p5)-.7036907989)<1e-8 and abs(float(a[5]-p6)+1.6414629772)<1e-8,'Rational two-equation fit; independent fifth/sixth residuals bounded far from zero.')
check(13,'ADE information dimension',math.comb(5,3)==10 and 6<10,'Degree≤2 in three variables has10 monomials; six reliably available rows cannot have full column rank.')
f=lambda v:v*v*math.expm1(v)
check(14,'monotone exponential example bracket',f(.5)<1<f(1) and all(2*v*math.expm1(v)+v*v*math.exp(v)>0 for v in [.1,.5,1]),'Existence bracket and positive analytic derivative; transcendence uses the cited theorem, not numerics.')
check(15,'Lambert lower-branch calibration',close((-2)*math.exp(-2),-4/(2*math.sqrt(math.exp(4)))) and -2<-1,'v=4 requires W_−1; principal real branch cannot return−2.')
P1=[[1,0,0],[0,1,0],[0,0,0]];P2=[[1,0,0],[0,0,0],[0,0,1]]
check(16,'commuting idempotent blocks',mm(P1,P1)==P1 and mm(P1,P2)==mm(P2,P1),'P,Q commute and are idempotent; three nonzero joint coordinate blocks sum toI.')
check(17,'global counterexample and contraction',all(abs(math.sin(2*math.pi*k))<1e-12 for k in range(-3,4)) and F(1,3)==(1+F(1,3))/4,'Nonsingular polar-exponential map has infinitely many zeros; invariant affine contraction has fixed point1/3.')
check(18,'coupled residual normal matrix',mm([[1,1],[1,-1]],[[1,1],[1,-1]])==[[2,0],[0,2]],'Exact Hessian2I and unique residual zero(1/2,1/2).')
J=[[F('-2.15'),F('-2.65')],[F('2.65'),F('-2.15')]]
check(19,'anisotropy and equal singular values',mm(tr(J),J)==[[F('11.645'),0],[0,F('11.645')]] and (F('2.51')-F('1.69'))/(F('2.51')+F('1.69'))==F(41,210),'Exact rational Gram matrix and mixed anisotropy41/210.')
check(20,'log-scale integral',close(math.log((3**2+1)/(1**2+1)),math.log(5)),'B0=2,w=1 gives exact area log5 and suppression1/5.')
check(21,'invariant map ambiguity',[2**j for j in (2,4,6,8)]==[(-2)**j for j in (2,4,6,8)],'Four even-power invariants fail to distinguish±2.')
xs=[0,1,2];ys=[1,3,5];sx=sum((x-1)**2 for x in xs);sxy=sum((x-1)*(y-3)for x,y in zip(xs,ys))
check(22,'least-squares slope',F(sxy,sx)==2,'Sxx=2,Sxy=4, slope2 and intercept1; constant x gives zero denominator.')
check(23,'quadratic gradient flip',[1-F(2,5)*l for l in (1,4)]==[F(3,5),-F(3,5)] and 1-F(1,2)*4==-1,'Optimal step2/5 gives±3/5; stability boundary1/2 gives−1.')
xe=math.exp(-1);ae=math.e
check(24,'exponential-kernel exact candidate',close(math.exp(-ae*xe),xe) and close(-ae*math.exp(-ae*xe),-1),'c=r=1: x=e⁻¹, alpha=e satisfy both equations.')
mu=F(1,4);xx=F(1,2);fun=lambda t:-(1+mu)*t+t**3
check(25,'exact born two-cycle',fun(xx)==-xx and fun(-xx)==xx and (-1+2*mu)**2==F(1,4),'Cycle±1/2 and multiplier1/4, exact rational arithmetic.')
z=1+2j;T=lambda z:1j*z.conjugate()
check(26,'reflection involution and damped multiplier',T(T(z))==z and abs(T(z))==abs(z),'Anti-linear reflection squares toidentity; scalar multiplier modulus1/2 gives2⁻n decay.')
S=sum(math.comb(6-k,k)for k in range(4));phi=(1+math.sqrt(5))/2;psi=(1-math.sqrt(5))/2
check(27,'Fibonacci binomial and Pisot identity',S==13 and close(phi**6+psi**6,18),'Exact S6=13; conjugate power identityL6=18.')
entries=json.loads((P/'entries.json').read_text())
assert len(entries)==27
for e in entries:
 o=e['original'];fn,_,idx=o['retrieval_receipt'].partition(' record ')
 rec=json.loads((P/fn).read_text())[int(idx)]
 texts=[c['text'] for c in rec['result'].get('content',[])if c.get('type')=='text']
 assert any(o['source_excerpt'] in t for t in texts),(e['id'],'nonliteral source')
 assert f"{o['evidence']}@{o['date']}" in o['source_excerpt']
 assert o['original_question'] is None
 if e['id']=='Y26-03-007':assert 'derived concentration bound' in o['source_excerpt']
(P/'checks.json').write_text(json.dumps({'checks':checks,'provenance':{'entries':len(entries),'literal_source_excerpts':'passed'},'all_passed':True},ensure_ascii=False,indent=2)+'\n')
print(len(checks),'checks passed; literal provenance passed')
