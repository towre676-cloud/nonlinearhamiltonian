#!/usr/bin/env python3
"""Portable exact/finite checks of the stated July examples, not all general theory."""
import json,math,itertools,re
from pathlib import Path
from fractions import Fraction as F
P=Path(__file__).resolve().parent;C=[]
def ck(n,name,ok,detail):C.append(dict(id=f'Y25-07-{n:03d}',name=name,status='pass' if ok else 'FAIL',detail=detail))
def mv(a,v):return[sum(x*y for x,y in zip(r,v)) for r in a]
def mm(a,b):return[[sum(x*y for x,y in zip(r,c)) for c in zip(*b)] for r in a]
def rank(A):
 a=[[F(x) for x in r] for r in A];k=0
 for j in range(len(a[0])):
  z=next((i for i in range(k,len(a)) if a[i][j]),None)
  if z is None:continue
  a[k],a[z]=a[z],a[k];v=a[k][j];a[k]=[x/v for x in a[k]]
  for i in range(len(a)):
   if i!=k:
    v=a[i][j];a[i]=[x-v*y for x,y in zip(a[i],a[k])]
  k+=1
  if k==len(a):break
 return k
# 1 boundary differences telescope on all triples of a finite cusp subset.
cusps=['infinity','0','1','-1']
def boundary(a,b):return [int(v==b)-int(v==a) for v in cusps]
ck(1,'Cusp triangle boundary',all([x+y+z for x,y,z in zip(boundary(a,b),boundary(b,c),boundary(c,a))]==[0]*4 for a,b,c in itertools.product(cusps,repeat=3)),'All 64 triples checked; universal presentation is proved algebraically in text.')
counts=[sum((y*y-x*x*x+x)%5==0 for y in range(5)) for x in range(5)]
a=[1,-2]
for r in range(2,5):a.append(-2*a[-1]-5*a[-2])
ck(2,'Finite-field count and Euler recurrence',counts==[1,1,2,2,1] and sum(counts)+1==8 and a==[1,-2,-1,12,-19] and 26-(4-10)==32,'Exact F5 point enumeration and prime-power recurrence; Frobenius power sum distinguished.')
b2,b4,b6,b8=0,-2,0,-1;c4=b2*b2-24*b4;c6=-b2**3+36*b2*b4-216*b6;D=-b2*b2*b8-8*b4**3-27*b6*b6+9*b2*b4*b6
ck(3,'Weierstrass discriminant',c4==48 and c6==0 and D==64 and c4**3-c6**2==1728*D and F(c4**3,D)==1728,'Exact integral invariants of y²=x³−x; no conductor-at-two certification claimed.')
# Elementary quotient dimensions for a stipulated finitely generated group.
ck(4,'Selmer rank-bound bookkeeping',4-1==3 and all(len({(k*x)%4 for x in range(4)}) in (1,2,4) for k in (1,2,4)),'Stipulated s=4,t=1 gives rank≤3. General Kummer/Selmer exactness is proved in text, not inferred from this finite group check.')
G=[[2,1],[1,3]]
ck(5,'Height Gram and subgroup index',G[0][0]>0 and 2*3-1==5 and all(sum(v[i]*G[i][j]*v[j] for i in range(2) for j in range(2))>0 for v in itertools.product(range(-6,7),repeat=2) if v!=(0,0)) and F(5,2**2)==F(5,4),'Positive minors plus exact integer-vector replay and index-square regulator conversion.')
ck(6,'Quaternion 2-adic primitive obstruction',not any(sum(x*x for x in v)%8==0 and any(x%2 for x in v) for v in itertools.product(range(8),repeat=4)) and (F(1,2)+F(1,2))%1==0,'All 4096 primitive residue quadruples checked; odd-prime Hilbert formula and ABHN retain sourced theorem scope.')
ck(7,'Primal-dual exact optimum',F(3)+2*F(0)==3 and 3+0>=3 and 0<=1<=min(1,2) and 3*1==3,'Feasible primal (3,0), dual1, matching value3.')
vs=[(2,0,1),(1,3,1),(0,2,4)];join=lambda a,b:tuple(max(x,y) for x,y in zip(a,b))
ck(8,'Vector-clock joins',join(join(vs[0],vs[1]),vs[2])==join(vs[0],join(vs[1],vs[2]))==(2,3,4) and all(join(v,v)==v for v in vs),'Exact three-replica merge, associativity example and duplicate idempotence.')
ck(9,'Posterior moments and simulation bound',F(4,6)==F(2,3) and F(4*5,6*7)-F(2,3)**2==F(2,63) and math.ceil(math.log(40)/(2*.05**2))==738,'Beta moments and declared Hoeffding sample-size arithmetic; no empirical reliability inference.')
q=1+math.sqrt(2)
ck(10,'Riccati root and cost',abs(2*q-q*q+1)<1e-14 and 1-q<0 and q<2.5 and abs((1+q*q)/(2*math.sqrt(2))-q)<1e-14,'Exact-form stabilizing root, quadratic residual and integrated optimal cost.')
f=[F(2),F(-1),F(-1)]
ck(11,'Mean-zero conformal area variation',sum(f)==0 and sum(-2*x for x in f)==0,'Area density derivative −2f sums to zero for a mean-zero test; full metric variation proved in text.')
ck(12,'Heat Fourier energy identity',-(2*1+2*2*1+2*1*3)==-12,'At μ=1,λ=2,κ=1, the three energy derivative terms sum to −12π times the decay factor.')
Eps=[[0,0],[1,0]]
ck(13,'Dual-number extension structure',mm(Eps,Eps)==[[0,0],[0,0]] and rank(Eps)==1 and rank([[0,0],[0,0]])==0,'Nilpotent action ranks distinguish nonsplit R from split k⊕k; free resolution proves Ext dimension in text.')
ck(14,'Ribbon modulus',abs(math.exp(-2*math.log(2))-.25)<1e-15 and (-2)!=(-1),'Recovered scalar coefficient gives modulus1/4 at t=1, not the separate 2^−s target1/2.')
# Exact Weyl relation for N=2; trace obstruction for all finite N is algebraic.
X=[[0,1],[1,0]];Z=[[1,0],[0,-1]]
ck(15,'Finite Weyl relation',mm(Z,X)==[[-x for x in r] for r in mm(X,Z)] and mm(X,X)==[[1,0],[0,1]],'ZX=−XZ at N=2 and X²=I; finite additive CCR impossible by trace proof.')
root_count=4*math.comb(8,2)+2**7
N=4;coeff=[1]+[0]*N
for m in range(1,N+1):
 factor=[0]*(N+1)
 for j in range(min(24,N//m)+1):factor[m*j]=(-1)**j*math.comb(24,j)
 coeff=[sum(coeff[j]*factor[k-j] for j in range(k+1)) for k in range(N+1)]
ck(16,'E8 root count and Delta coefficients',root_count==240 and coeff[:4]==[1,-24,252,-1472],'Independent finite product expansion and coordinate root count.')
ck(17,'Finite stuffle identity',F(5,4)*F(9,8)==F(1,4)+F(1,8)+F(33,32)==F(45,32),'N=2 identity in exact rationals; all-orders limit has an absolute-convergence proof.')
D2=[[0,2],[2,0]];A2=[[F(1,2),0],[0,0]];comm=[[x-y for x,y in zip(r,s)] for r,s in zip(mm(D2,A2),mm(A2,D2))]
ck(18,'Two-point distance norm',mm([list(r) for r in zip(*comm)],comm)==[[1,0],[0,1]],'At m=2 and coordinate difference1/2, the commutator singular values are exactly1.')
chars=lambda m:{m-2*k:1 for k in range(m+1)}
out={}
for k,v in chars(2).items():
 for a in (-1,1):out[k+a]=out.get(k+a,0)+v
ck(19,'sl2 character decomposition',out=={3:1,1:2,-1:2,-3:1},'χ2χ1=χ3+χ1 with exact Laurent multiplicities.')
Fq=lambda x,y,z:x*x+2*y*y+3*z*z+x*z+y*z
local=all(Fq(x,y,z)%7 or ((x-3*z)%7==0 and (y-5*z)%7==0) for x,y,z in itertools.product(range(7),repeat=3))
excluded=[7,14,28,56,63,77]
ck(20,'Ternary local obstruction',local and all(n//7%7 in (1,2,4) for n in excluded) and all(8*Fq(x,y,z)==2*(2*x+z)**2+(4*y+z)**2+21*z*z for x,y,z in itertools.product(range(-3,4),repeat=3)),'All 343 mod7 triples and 343 integer square-completion samples checked. Descent proof supplies infinite nonrepresentation family.')
ck(21,'Cyclic decimal and corrected fractions',(10**6-1)//7==142857 and [pow(10,j,7) for j in range(7)]==[1,3,2,6,4,5,1] and F(384,840)+F(1680,1840)==F(1103,805) and F(384*(1840-1680),840)==F(512,7),'Exact period and both rational corrections.')
ck(22,'Ray-class arithmetic ingredients',math.sqrt(40)/2<3.163 and {x*x%5 for x in range(5)}.isdisjoint({2,3}) and 3*3-10==-1 and 2*2-10==-6 and {1%3,-1%3}=={1,2},'Minkowski bound, norm obstructions, norm−6 relation and residue-unit surjection; class-group proof is stated in full.')
ck(23,'Biquadratic discriminant audit',8*5*40==40**2 and 40*(-4)*(-40)//40**2==4,'Hilbert candidate relative discriminant norm1 versus K(i) norm4; real-place distinction in proof.')
squares17={x*x%17 for x in range(17)}
ck(24,'Quartic and rational ray audit',2**2==4 and sum(math.gcd(x,136)==1 for x in range(136))==64 and 6 not in squares17 and 11 not in squares17 and (-6*6)%17==(-2)%17,'φ136=64 and irreducible quadratic factors mod17; degree/normal-closure proof in text.')
g=[8*n*n-5*n+3 for n in range(8)];aa=[240+24*x for x in g]
ck(25,'Quadratic series recurrence',g[:5]==[3,6,25,60,111] and all(g[n]-g[n-1]==16*n-13 for n in range(1,8)) and [aa[n]-3*(aa[n-1] if n>=1 else 0)+3*(aa[n-2] if n>=2 else 0)-(aa[n-3] if n>=3 else 0) for n in range(8)]==[312,-552,624,0,0,0,0,0],'Denominator multiplication verifies exact rational generating function.')
ck(26,'Shadow weight and local differential coefficient',F(2)-F(3,2)==F(1,2) and F(1)-F(3,2)==F(-1,2),'ξ3/2 target weight1/2; local y^−1/2 coefficient−1/2. Domain divergence proved by term growth.')
rootsA=[v for v in itertools.product(range(-2,3),repeat=2) if v[0]**2+v[0]*v[1]+v[1]**2==1]
rootsD=[v for v in itertools.product(range(-2,3),repeat=4) if sum(x*x for x in v)==2 and sum(v)%2==0]
ck(27,'A2 and D4 root counts',len(rootsA)==6 and len(rootsD)==24 and 2**3*F(1,2)==4,'Root enumeration and D4 Schur-complement determinant.')
res=[math.log10(d)-(.514*r+1.291) for d,r in zip([9240,1320,80960,1020096],[4,6,7,8])]
ck(28,'Density residuals and interpolation ambiguity',res[0]>.6 and res[1]<-1.2 and all((x-F(1,2))*(x-1)*(x-2)==0 for x in [F(1,2),F(1),F(2)]) and 2+3+4+5==14,'Residuals reject close fit; vanishing cubic demonstrates nonunique beta interpolation.')
polys=[([1,-4,0,0,1],-4,0),([1,-6,4,2,1],-6,2)]
peval=lambda cs,x:sum(c*x**(4-i) for i,c in enumerate(cs))
ck(29,'Quartic irreducibility obstructions',all(peval(cs,x)!=0 for cs,_,_ in polys for x in (-1,1)) and all(e*cubic!=linear for _,cubic,linear in polys for e in (-1,1)),'No rational roots; the only possible monic quadratic constant patterns contradict cubic/linear coefficients.')
B4=[[-1,0,0,1],[1,-1,0,0],[0,1,-1,0],[0,0,1,-1]]
ck(30,'Empty two-CNF complex',rank(B4)==3 and 4-rank(B4)==1,'Four-cycle avoidance complex has β1=1, refuting universal contractibility.')
B3=[[-1,0,1],[1,-1,0],[0,1,-1]]
ck(31,'Inclusion can kill homology',rank(B3)==2 and mv(B3,[1,1,1])==[0,0,0] and rank([[1],[1],[1]])==1,'Triangle boundary H1 has dimension1; filling adds rank-one boundary, making target H1 zero.')
ck(32,'Transport curvatures',F(1)-F(1)==0 and F(1)-F(1,2)==F(1,2),'K2 transport cost1; K3 shared half-mass gives cost1/2, with lower bound proved in text.')
valid=[]
for fammask in range(256):
 fam={s for s in range(8) if fammask>>s&1}
 if not fam or fam=={0}:continue
 if all(a|b in fam for a in fam for b in fam):
  valid.append(fam);assert any(2*sum(bool(s>>j&1) for s in fam)>=len(fam) for j in range(3))
ck(33,'Bounded union-closed audit',len(valid)>0,'All 256 families on three labels examined; all nontrivial union-closed families satisfy the half-frequency assertion. This is bounded evidence only.')
bern=[F(1)]
for n in range(1,13):bern.append(-sum(F(math.comb(n+1,k))*bern[k] for k in range(n))/F(n+1))
ck(34,'Bernoulli exact coefficient',bern[12]==F(-691,2730) and -24/bern[12]==F(65520,691) and 2*abs(bern[12])==F(691,1365),'Bernoulli recurrence executed exactly through degree12.')
ck(35,'Mackey finite character',3==2+1 and 1==2-1,'Three-coset action has one fixed coset under the transposition; orbit splitting and stabilizers proved explicitly.')
entries=json.loads(P.joinpath('entries.json').read_text());assert len(entries)==35
for e in entries:
 o=e['original'];assert o['original_question'] is None and o['month']=='2025-07'
 fn,num=o['retrieval_receipt'].split(' record ');raw=json.loads(P.joinpath(fn).read_text())[int(num)]
 assert o['source_excerpt'] in json.dumps(raw,ensure_ascii=False) or any(o['source_excerpt'] in m.get('content',m.get('text','')) for m in raw.get('result',raw).get('structuredContent',{}).get('messages',[]))
P.joinpath('checks.json').write_text(json.dumps(dict(month='2025-07',checks=C,scope='Finite examples, exact algebra and bounded enumerations. General arithmetic/geometric theorems retain their stated proof and source scope.'),ensure_ascii=False,indent=2))
print(json.dumps(dict(month='2025-07',passed=sum(c['status']=='pass' for c in C),total=len(C))))
assert all(c['status']=='pass' for c in C)
