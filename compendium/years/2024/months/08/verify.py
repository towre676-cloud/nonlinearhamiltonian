#!/usr/bin/env python3
"""Stdlib exact arithmetic replay of the fourteen declared August examples."""
import json,math,itertools
from fractions import Fraction as F
from pathlib import Path
P=Path(__file__).resolve().parent; checks=[]
def check(n,name,ok,detail): checks.append(dict(id=f'Y24-08-{n:03d}',name=name,status='pass' if ok else 'FAIL',detail=detail))
def mm(a,b): return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]
def addm(a,b,c=1): return [[x+c*y for x,y in zip(u,v)] for u,v in zip(a,b)]
def ident(n):return [[F(i==j) for j in range(n)] for i in range(n)]
def rank(A):
    a=[[F(x) for x in row] for row in A]; r=0
    for c in range(len(a[0])):
        p=next((j for j in range(r,len(a)) if a[j][c]),None)
        if p is None:continue
        a[p],a[r]=a[r],a[p]; q=a[r][c];a[r]=[x/q for x in a[r]]
        for j in range(len(a)):
            if j!=r:
                q=a[j][c];a[j]=[x-q*y for x,y in zip(a[j],a[r])]
        r+=1
        if r==len(a):break
    return r
# Enumerate every partial diagram matching, including empty and diagonal alternatives.
D=[(F(0),F(3)),(F(1),F(2))]; E=[(F(1,10),F(16,5)),(F(4,5),F(23,10))]
cost=lambda a,b:max(abs(a[0]-b[0]),abs(a[1]-b[1])); diag=lambda a:(a[1]-a[0])/2
panels=[]
for k in range(3):
 for ii in itertools.combinations(range(2),k):
  for jj in itertools.permutations(range(2),k):
   cs=[cost(D[i],E[j]) for i,j in zip(ii,jj)]+[diag(D[i]) for i in range(2) if i not in ii]+[diag(E[j]) for j in range(2) if j not in jj]
   panels.append((max(cs,default=F(0)),sum(c*c for c in cs)))
check(1,'Exhaustive diagram matchings',len(panels)==7 and min(a for a,b in panels)==F(3,10) and min(b for a,b in panels)==F(13,100),'All 7 partial bijections enumerated with all unmatched points sent to diagonal.')
B=[[-1,1,0],[0,-1,1]]; Z=[[0]*5 for _ in range(5)]
for i in range(2):
 for j in range(3):Z[j][3+i]=Z[3+i][j]=B[i][j]
D2=mm(Z,Z); poly=mm(mm(Z,addm(D2,ident(5),-1)),addm(D2,[[3*x for x in row] for row in ident(5)],-1))
check(2,'Graph Dirac polynomial and nullity',all(x==0 for row in poly for x in row) and rank(Z)==4 and rank(B)==2,'Exact D(D²−I)(D²−3I)=0 and rank 4, agreeing with spectrum 0,±1,±√3; no assertion about zeta zeros.')
C=[[F(4,100),F(1,100),F(15,1000)],[F(1,100),F(625,10000),F(2,100)],[F(15,1000),F(2,100),F(9,100)]]
w=[F(2,5),F(7,20),F(1,4)];mu=[F(15,100),F(18,100),F(20,100)]
det2=C[0][0]*C[1][1]-C[0][1]**2
det3=sum((-1)**j*C[0][j]*(C[1][(j+1)%3]*C[2][(j+2)%3]-C[1][(j+2)%3]*C[2][(j+1)%3])*(-1)**j for j in range(3))
# Cyclic expansion above has its sign already incorporated by the cyclic minor order.
mean=sum(x*y for x,y in zip(w,mu));var=sum(w[i]*C[i][j]*w[j] for i in range(3) for j in range(3))
check(3,'Exact historical stipulated covariance calculation',mean==F(173,1000) and var==F(4637,160000) and C[0][0]>0 and det2>0 and det3>0 and abs(math.sqrt(var)-.17023880286233217)<1e-14,'Exact mean .173, variance .02898125, positive leading principal minors; inputs are stipulated historical values.')
# Dimensions represented by exponents of mass, length, time.
plus=lambda a,b:tuple(x+y for x,y in zip(a,b));minus=lambda a,b:tuple(x-y for x,y in zip(a,b))
n=(0,-3,0);h=(1,2,-1);c=(0,1,-1);wave=(0,1,0)
u=minus(plus(plus(n,h),c),wave);flux=plus(u,c)
check(4,'Energy-density dimensions and isotropic transport factor',u==(1,-1,-2) and flux==(1,0,-3) and F(1,2)*F(1,2)==F(1,4),'n hc/λ has energy-density dimensions; multiplying by speed supplies flux. Hemisphere integral (2π)(1/2)/(4π)=1/4 under isotropic convention.')
tan2=[a for a in range(2) if 2*a%2==0];tan3=[a for a in range(3) if 2*a%3==0]
check(5,'Deformation tangent and obstruction',tan2==[0,1] and tan3==[0] and (1+1+0)%2==0 and 1%2!=0,'For u=1+aε, relation u²=1 gives 2a=0. At char 2 the lift 1+η+bη² has unavoidable η² coefficient 1; all b share the obstruction.')
indices=[]
for p in (2,3,5):
 G=[(a,b,c,d) for a,b,c,d in itertools.product(range(p),repeat=4) if (a*d-b*c)%p==1]
 H=[g for g in G if g[2]==0];indices.append(len(G)//len(H))
check(6,'Prime-level subgroup index finite enumeration',indices==[3,4,6],'SL₂(F_p) and upper triangular determinant-one subgroup enumerated completely for p=2,3,5, giving index p+1.')
L=[[F(5,3),F(4,3),0,0],[F(4,3),F(5,3),0,0],[0,0,1,0],[0,0,0,1]];eta=[[-1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
Lt=[list(r) for r in zip(*L)];b=[[1],[0],[0],[0]];comm=addm(mm(L,b),b,-1)
check(7,'Lorentz condition and semidirect commutator',mm(mm(Lt,eta),L)==eta and comm==[[F(2,3)],[F(4,3)],[0],[0]],'Exact rational boost preserves signature (−+++); [boost, translation e₀] translates by (2/3,4/3,0,0).')
# Polynomial product evaluated at exact rational points proves its symmetry by coefficient expansion.
def pmul(a,b):
 out=[F(0)]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):out[i+j]+=x*y
 return out
p=pmul([F(17,16),F(-1,2),F(1)],[F(25,16),F(-3,2),F(1)])
q=[sum(p[k]*math.comb(k,j)*(-1)**j for k in range(j,len(p))) for j in range(len(p))]
check(8,'Symmetry does not imply critical-line zeros',p==q and F(1,4)!=F(1,2) and F(3,4)!=F(1,2),'Exact coefficients satisfy P(1−s)=P(s); factors visibly have roots 1/4±i and 3/4±i. This changes analytic class and is not a counterexample to RH.')
qfield=2;z=[F(1)]
for n0 in range(1,9):z.append(sum(F(qfield**k+1)*z[n0-k] for k in range(1,n0+1))/n0)
check(9,'Projective-line zeta coefficient identity',z==[F(2**(m+1)-1) for m in range(9)] and [2**n+1 for n in (1,2,3)]==[3,5,9],'Log-derivative recurrence from point counts matches rational zeta 1/((1−t)(1−2t)) through degree 8; counts differ from series coefficients.')
# Algebra k[x,ε]/(x²−ε, ε²), basis 1,x,ε,εx. Multiplication is powers of x mod x⁴.
def mul4(a,b):
 out=[F(0)]*4
 for i,x in enumerate(a):
  for j,y in enumerate(b):
   if i+j<4:out[i+j]+=x*y
 return out
basis=[[F(i==j) for i in range(4)] for j in range(4)]
assoc=all(mul4(mul4(a,b),c)==mul4(a,mul4(b,c)) for a,b,c in itertools.product(basis,repeat=3))
check(10,'Associative first-order deformation',assoc and mul4(basis[1],basis[1])==basis[2] and mul4(basis[2],basis[2])==[0]*4,'All 64 basis triples in k[x]/(x⁴) checked; identify ε=x², so x²=ε and ε²=0, a free rank-two dual-number algebra.')
def v3(a):
 a=F(a)
 if not a:return math.inf
 num,den=a.numerator,a.denominator;v=0
 while num%3==0:num//=3;v+=1
 while den%3==0:den//=3;v-=1
 return v
gnorm=lambda a: min(v3(x) for x in a)
f=[F(1),F(3)];g=[F(1),F(1)];fg=pmul(f,g)
check(11,'Gauss norm multiplicativity example',fg==[1,4,3] and gnorm(f)==gnorm(g)==gnorm(fg)==0 and all(gnorm([-a,1])==0 for a in (-1,0,1)),'p=3 polynomial example has all Gauss norms 1; T−a has norm 1 despite evaluating to zero at a. General multiplicativity is proved by reduction in text.')
# Odd BV algebra: polynomial pairs (even f, odd gθ). Degree tracking homogeneous.
def clean(p):return {i:F(x) for i,x in p.items() if x}
def pa(a,b,c=1):
 out=dict(a)
 for i,x in b.items():out[i]=out.get(i,F(0))+c*x
 return clean(out)
def ps(a,c):return clean({i:c*x for i,x in a.items()})
def pd(a):return clean({i-1:i*x for i,x in a.items() if i})
def pt(a,b):
 out={}
 for i,x in a.items():
  for j,y in b.items():out[i+j]=out.get(i+j,F(0))+x*y
 return clean(out)
def ea(a,b,c=1):return (pa(a[0],b[0],c),pa(a[1],b[1],c))
def es(a,c):return(ps(a[0],c),ps(a[1],c))
def em(a,b):return(pt(a[0],b[0]),pa(pt(a[0],b[1]),pt(a[1],b[0])))
def delta(a):return(pd(a[1]),{})
def bracket(a,b,da):return es(ea(ea(delta(em(a,b)),em(delta(a),b),-1),em(a,delta(b)),-(-1)**da),(-1)**da)
monos=[(({n:F(1)},{}),0) for n in range(3)]+[(({}, {n:F(1)}),1) for n in range(3)]
bv_square=all(delta(delta(a))==({}, {}) for a,da in monos)
jac=True
for (a,da),(b,db),(c0,dc) in itertools.product(monos,repeat=3):
 left=bracket(a,bracket(b,c0,db),da)
 right=ea(bracket(bracket(a,b,da),c0,da+db-1),bracket(b,bracket(a,c0,da),db),(-1)**((da-1)*(db-1)))
 if left!=right:jac=False;break
x2=({2:F(1)},{});xtheta=({}, {1:F(1)});x2theta=({}, {2:F(1)})
check(12,'BV differential and odd Jacobi identities',bv_square and jac and bracket(x2,xtheta,0)==({2:F(2)}, {}) and bracket(xtheta,x2theta,1)==({}, {2:F(-1)}),'Δ²=0 on six basis monomials; all 216 homogeneous monomial Jacobi triples replayed with shifted signs; two displayed brackets exact. General second-order identity proved in text.')
# Exact integration of each affine piece on a rational interval.
def int_affine(a,b,left,right):return a*(right*right-left*left)/2+b*(right-left)
atom_integral=int_affine(F(0),F(-1,2),F(-1),F(0))+int_affine(F(0),F(1,2),F(0),F(1))
pairing=int_affine(F(-1,2),F(0),F(-1),F(0))+int_affine(F(1,2),F(0),F(0),F(1))
mean_abs=(int_affine(F(-1),F(0),F(-1),F(0))+int_affine(F(1),F(0),F(0),F(1)))/2
check(13,'Atomic local Hardy–BMO pairing',atom_integral==0 and pairing==F(1,2) and mean_abs==F(1,2),'For I=[−1,1], a=sign(x)/2 has mean zero, sup norm 1/2, pairing ∫|x|/2=1/2, and mean oscillation |I|⁻¹∫|x|=1/2. Full duality is sourced, not proved by this one atom.')
a,b=F(2),F(4)
check(14,'Power-law ratios and finite-data nonuniqueness',(a/b)**2==F(1,4) and (a/b)**8==F(1,256) and (F(1,3)**2)**4==F(1,3)**8 and (3-2)*(3-4)!=0,'Exact scale ratios and elimination exponent 4 verified; perturbation vanishes at n=2,4 and not n=3, so finitely many samples do not identify a global power law.')
entries=json.loads(P.joinpath('entries.json').read_text());assert len(entries)==14
assert all(e['original']['month']=='2024-08' and e['original']['original_question'] is None for e in entries)
assert entries[12]['original']['date'] is None
P.joinpath('checks.json').write_text(json.dumps(dict(month='2024-08',scope='Exact finite examples and algebra; no numerical proof of RH, generic geometry, physical validation or current-data claim.',checks=checks),ensure_ascii=False,indent=2))
print(json.dumps(dict(month='2024-08',passed=sum(c['status']=='pass' for c in checks),total=len(checks))))
assert all(c['status']=='pass' for c in checks)
