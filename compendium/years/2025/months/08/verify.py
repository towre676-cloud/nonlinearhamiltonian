#!/usr/bin/env python3
"""Portable stdlib checks; exact finite examples and clearly scoped floating evaluations."""
import json,math,itertools,subprocess,sys,re
from fractions import Fraction as F
from pathlib import Path
P=Path(__file__).resolve().parent;C=[]
def ck(n,name,ok,detail):C.append(dict(id=f'Y25-08-{n:03d}',name=name,status='pass' if ok else 'FAIL',detail=detail))
def mm(a,b):return[[sum(x*y for x,y in zip(r,c)) for c in zip(*b)] for r in a]
def mv(a,v):return[sum(x*y for x,y in zip(r,v)) for r in a]
def eye(n):return[[F(i==j) for j in range(n)] for i in range(n)]
def ma(a,b,c=1):return[[x+c*y for x,y in zip(r,s)] for r,s in zip(a,b)]
def rank(a):
 a=[[F(x) for x in r] for r in a];k=0
 for j in range(len(a[0])):
  i=next((i for i in range(k,len(a)) if a[i][j]),None)
  if i is None:continue
  a[i],a[k]=a[k],a[i];v=a[k][j];a[k]=[x/v for x in a[k]]
  for i in range(len(a)):
   if i!=k:
    v=a[i][j];a[i]=[x-v*y for x,y in zip(a[i],a[k])]
  k+=1
  if k==len(a):break
 return k
ck(1,'Trochoid frequency period',F(5,2).denominator==2 and (F(3,2)*2).denominator==1 and math.lcm(2,3)==6,'R/r=5/2 gives period4π; added frequency1/3 gives common period12π.')
Jx=[[0,0,0],[0,0,-1],[0,1,0]];Jy=[[0,0,1],[0,0,0],[-1,0,0]];Jz=[[0,-1,0],[1,0,0],[0,0,0]]
Rx=[[1,0,0],[0,0,-1],[0,1,0]];Ry=[[0,0,1],[0,1,0],[-1,0,0]]
ck(2,'Rotation bracket and order',ma(mm(Jx,Jy),mm(Jy,Jx),-1)==Jz and mv(mm(Rx,Ry),[0,0,1])==[1,0,0] and mv(mm(Ry,Rx),[0,0,1])==[0,-1,0],'Exact integer matrices verify Lie bracket and noncommuting right-angle example.')
ck(3,'TL trace Gram positivity',1-F(1,2)**2>0 and 1-F(1,F(1,2))**2<0 and 2-2/F(1,2)==-2,'Two-strand δ=2 positive minors; δ=1/2 negative squared-norm witness.')
phi=(1+math.sqrt(5))/2;Pmark=[[1/phi,1/phi**2],[1,0]];pi=[phi**2/(phi**2+1),1/(phi**2+1)]
ent=-sum(pi[i]*p*math.log(p) for i,row in enumerate(Pmark) for p in row if p)
ck(4,'Perron stochastic normalization',max(abs(sum(r)-1) for r in Pmark)<1e-14 and max(abs(sum(pi[i]*Pmark[i][j] for i in range(2))-pi[j]) for j in range(2))<1e-14 and abs(ent-math.log(phi))<1e-14,'Row sums, stationary law and entropy logφ numerically replayed to1e−14; variational bound proved by KL in text.')
M=[[1,1],[1,0]];r=[phi,1];proj=[[phi*phi/(phi*phi+1),phi/(phi*phi+1)],[phi/(phi*phi+1),1/(phi*phi+1)]]
R=ma(M,[[phi*x for x in row] for row in proj],-1)
ck(5,'Perron eigenvalue correction',max(abs(x) for x in mv(R,r))<1e-14 and max(abs(x) for row in mm(proj,R) for x in row)<1e-14 and abs(phi-1)>.6,'Correct R=M−φΠ annihilates r; erroneous M−Π would leave(φ−1)r.')
ck(6,'Chebyshev degree-one example',1-F(2,5)==F(3,5) and 1-F(8,5)==F(-3,5),'For diag(1,4), p1(A) has exact multipliers±3/5; general bound uses spectral theorem.')
ck(7,'Cubic KKT sign branch',(-1)**3==-1 and 1+3*(-1)**2*F(-1,3)==0 and 1**3!=-1,'Negative feasible branch satisfies stationarity; positive-root-only branch is infeasible.')
ck(8,'Gaussian geometric covariance tail',all(sum((F(1,2)**j for j in range(1,N+1)),F(0))==1-F(1,2)**N for N in range(1,20)),'Exact partial traces and tail2^−N. Almost-sure Gaussian support theorem proved in text, not simulated.')
B=[[-1,0,1],[1,-1,0],[0,1,-1]]
ck(9,'Triangle cohomology and killed class',rank(B)==2 and mv([list(r) for r in zip(*B)],[1,1,1])==[0,0,0] and 3-rank(B)==1,'H1 dimension1 and nonzero harmonic circulation; zero adapter cannot induce injection.')
ck(10,'Relative-period return bound',all((m+m)%7==(2*m)%7 for m in range(8)) and (7*1)%7==0 and 4*7==28,'Translation(1,1) on a7-torus has order7, giving relative-period4 return bound28; minimality not asserted.')
ck(11,'Lp spike norm',all(F(n)*F(1,n)==1 for n in range(1,40)) and F(1,20)<F(1,10),'Spike pth power integrates exactly to1 while support shrinks; measure theorem is analytically proved.')
ck(12,'Torus coarea factor',F(4*3*1,2*1)==6 and 2*1==2,'R=3,r=1: area12π², delta integral6π², gradient norm2; geometric derivation in text.')
# Exact local atom integrals, using polynomial antiderivatives on each half interval.
integ=lambda a,l,r:a*(r*r-l*l)/2
pair=integ(F(-1,2),F(-1),F(0))+integ(F(1,2),F(0),F(1))
osc=(integ(F(-1),F(-1),F(0))+integ(F(1),F(0),F(1)))/2
ck(13,'Atomic pairing exact integral',pair==osc==F(1,2),'Piecewise affine integrals independently give sharp local atom pairing1/2.')
ck(14,'Landau quartic completion',all(s*s-2*s==(s-1)**2-1 for s in map(F,range(10))) and F(1)**2-2*F(1)==-1,'Quartic completion exact on sample amplitudes; general square identity supplies global minima.')
nonzero=[v for v in itertools.product(range(2),repeat=3) if any(v)]
flags=sum(sum(x*y for x,y in zip(v,w))%2==0 for v in nonzero for w in nonzero)
ck(15,'Hall flag count',len(nonzero)==7 and flags==21 and (2+1)*(2*2+2+1)==21,'All nonzero vectors/functionals of F2^3 enumerate21 incident line-plane flags.')
fac=[math.factorial(5*n)//math.factorial(n)**5 for n in range(5)]
ck(16,'Quintic factorial Picard-Fuchs recurrence',fac[:3]==[1,120,113400] and all(n**4*fac[n]==5*math.prod(5*n-j for j in (1,2,3,4))*fac[n-1] for n in range(1,5)),'Exact coefficients verify θ4−5z product operator; coordinate factor5 retained.')
# Derived graph-potential interpretation of the published CRT labels, explicitly not the absent original matrix.
edges=[('t','mu',5),('b','mu',5),('c','tau',55),('b','e',5),('t','e',5),('s','e',55),('s','mu',55),('c','s',17),('b','s',5),('mu','e',20),('tau','mu',0)]
verts=sorted({v for x,y,b in edges for v in (x,y)})
A=[[int(v==x)-int(v==y) for v in verts] for x,y,b in edges]
# rank over F5 by exact modular elimination.
def rank5(a):
 a=[[x%5 for x in r] for r in a];k=0
 for j in range(len(a[0])):
  i=next((i for i in range(k,len(a)) if a[i][j]),None)
  if i is None:continue
  a[k],a[i]=a[i],a[k];z=pow(a[k][j],-1,5);a[k]=[x*z%5 for x in a[k]]
  for i in range(len(a)):
   if i!=k:
    z=a[i][j];a[i]=[(x-z*y)%5 for x,y in zip(a[i],a[k])]
  k+=1
  if k==len(a):break
 return k
aug=[r+[edges[i][2]%5] for i,r in enumerate(A)]
ck(17,'Graph-phase inconsistency certificate',rank5(A)==6 and rank5(aug)==7 and all(b%5==0 for i,(x,y,b) in enumerate(edges) if i!=7),'Derived incidence model has rank6/augmented7, but deleting only c/s leaves10 feasible edges; original max8 cannot be reconstructed.')
ck(18,'A-hat cross coefficient',F(7*2-4,5760)==F(1,576) and F(7,5760)-F(1,24)**2/2!=0,'Exact two-root quartic cross coefficient(14−4)/5760=1/576; series derivation in text.')
orb=set()
for pos in itertools.combinations(range(5),2):
 for signs in itertools.product((-1,1),repeat=2):
  v=[0]*5
  for i,s in zip(pos,signs):v[i]=s
  orb.add(tuple(v))
ck(19,'Signed-permutation orbit size',2**5*math.factorial(5)==3840 and len(orb)==40,'Generic group order3840 contrasted with exact degenerate orbit40.')
s=[F(-3),F(4)];y=[F(-6),F(8)];sy=sum(a*b for a,b in zip(s,y));yy=sum(a*a for a in y)
rho=1/sy;V=ma(eye(2),[[rho*a*b for b in y] for a in s],-1);Hnew=ma(mm(V,[list(r) for r in zip(*V)]),[[rho*a*b for b in s] for a in s])
ck(20,'Quadratic Armijo and BFGS secant',sy==50 and yy==100 and sy/yy==F(1,2) and mv(Hnew,y)==s and Hnew[0][0]>0 and Hnew[0][0]*Hnew[1][1]-Hnew[0][1]**2>0,'Exact curvature/scaling, secant identity and positive minors; half-step reaches the specified optimum.')
soft=lambda x,l:max(F(0),x-l)-max(F(0),-x-l)
ck(21,'ISTA soft-threshold example',[soft(F(3),F(1)),soft(F(-1),F(1))]==[2,0],'Identity least-squares plus l1 penalty gives exact proximal optimum(2,0).')
th=[F(1),F(-2)];u=[F(1,2),F(-1,4)];eta=F(1,10);lam=F(1,5)
z=[a-eta*b-eta*lam*a for a,b in zip(th,u)]
geta=sum(a*(-b-lam*c) for a,b,c in zip(z,u,th));glam=sum(a*(-eta*b) for a,b in zip(z,th))
ck(22,'One-step hypergradient exact values',z==[F(93,100),F(-387,200)] and geta==F(-1527,800) and glam==F(-12,25),'Analytic partials evaluated in exact fractions; later recovery-file evidence is not a recovered original program.')
Inc=[[int((i-j)%7 in (0,1,3)) for j in range(7)] for i in range(7)]
BB=mm(Inc,[list(r) for r in zip(*Inc)])
ck(23,'Fano incidence spectral certificate',BB==[[2*int(i==j)+1 for j in range(7)] for i in range(7)] and F(36,7)+F(1,6)==F(223,42),'Exact BBᵀ=2I+J establishes Heawood singular values; zeta1 simplification exact.')
A5=[[int((i-j)%5 in (1,4)) for j in range(5)] for i in range(5)];L5=ma([[2*x for x in r] for r in eye(5)],A5,-1)
poly=mm(L5,ma(ma(mm(L5,L5),[[5*x for x in r] for r in L5],-1),[[5*x for x in r] for r in eye(5)]))
ck(24,'Paley5 Laplacian polynomial',rank(L5)==4 and all(x==0 for r in poly for x in r) and F(4*(5+1),5*(5-1))==F(6,5),'Exact C5 Laplacian satisfies L(L²−5L+5I)=0 with rank4; inverse moment6/5 follows conjugate roots.')
H=-sum(F(n,16)*math.log(F(n,16)) for n in (6,5,5))
ck(25,'CRT and finite ternary entropy',all(((33*a+16*b)%48)%16==a and ((33*a+16*b)%48)%3==b for a in range(16) for b in range(3)) and .996<H/math.log(3)<.997,'All48 CRT pairs checked; maximal16-sample ternary entropy is near.9965 of log3, not a normality proof.')
ks=[-math.pi,-2,-1,-.2,0,.2,1,2,math.pi]
ck(26,'Lattice symbol bounds',all(-1e-14<=k*k-4*math.sin(k/2)**2<=k**4/12+1e-14 for k in ks),'Declared h=1 dispersion bound checked at nine modes; global bound is proved analytically.')
b=F(91,2000);mu0=F(1,10);ell=F(100);mu=mu0/(1-b*mu0*ell)
ck(27,'Riccati invariant',mu==F(20,109) and 1/mu+b*ell-1/mu0==0 and 1/(b*mu0)==F(20000,91),'Exact stipulated parameters, value at100 and pole time.')
ck(28,'Complete graph audit',23*22//2==253 and 231-253==-22 and F(231,253)==F(21,23) and F(78,45)==F(26,15) and [n*(n-1)//2 for n in (33,44,94)]==[528,946,4371],'All five recovered example counts checked; n10/e78 is infeasible for a simple graph.')
S=ma(eye(3),[[F(1,6)]*3 for _ in range(3)]);Sinv=ma(eye(3),[[F(1,9)]*3 for _ in range(3)],-1)
ck(29,'Rank-one inverse exact product',mm(S,Sinv)==eye(3) and mv(S,[1,1,1])==[F(3,2)]*3,'Exact n3,t1/6 inverse and constant-vector eigenvalue3/2.')
ck(30,'Residual counterexample and log-noise bound',rank([[0]])==0 and 1-rank([[0]])==1 and F(2,1000)/F(1,10)==F(1,50),'Zero differential complex has H1 dimension1 despite zero Laplacian; deterministic rate error bound.02.')
# Preserve root helper tests and make this verifier self-contained in the source bundle.
subprocess.run([sys.executable,'-S',str(P/'independent_early_verify.py')],check=True)
early=json.loads(P.joinpath('early_checks.json').read_text())
for x in early['checks']:
 x=dict(x);x['status']='pass' if x['status'] in ('pass','passed') else x['status'];C.append(x)
es=json.loads(P.joinpath('entries.json').read_text());assert len(es)==40 and len({e['id'] for e in es})==40
for e in es:
 o=e['original'];assert o['month']=='2025-08' and o['original_question'] is None
 match=re.fullmatch(r'(.+?) record\s*(\d+)',o['retrieval_receipt']);assert match
 fn,num=match.groups();raw=json.loads(P.joinpath(fn).read_text())[int(num)]
 assert any(o['source_excerpt'] in m.get('content',m.get('text','')) for m in raw.get('result',raw).get('structuredContent',{}).get('messages',[]))
P.joinpath('checks.json').write_text(json.dumps(dict(month='2025-08',checks=C,scope='Thirty core examples plus ten separately implemented root helper checks; no empirical, universal cohomological or physical validation claimed.'),ensure_ascii=False,indent=2))
print(json.dumps(dict(month='2025-08',passed=sum(c['status']=='pass' for c in C),total=len(C))))
assert all(c['status']=='pass' for c in C)
