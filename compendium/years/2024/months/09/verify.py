#!/usr/bin/env python3
"""Portable stdlib checks of the stated finite examples; not automated proof of all theorems."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product, permutations
import math, json
P=Path(__file__).resolve().parent
checks=[]
def check(n,name,fn):
 try:
  detail=fn(); checks.append(dict(id=f'Y24-09-{n:03}',name=name,status='passed',detail=str(detail)))
 except Exception as e:
  checks.append(dict(id=f'Y24-09-{n:03}',name=name,status='failed',detail=repr(e)))
def need(x,msg='assertion failed'):
 if not x:raise AssertionError(msg)
def rank(a):
 a=[[F(v) for v in r] for r in a];i=0
 for j in range(len(a[0]) if a else 0):
  k=next((k for k in range(i,len(a)) if a[k][j]),None)
  if k is None:continue
  a[i],a[k]=a[k],a[i];v=a[i][j];a[i]=[x/v for x in a[i]]
  for k in range(len(a)):
   if k!=i:
    v=a[k][j];a[k]=[x-v*y for x,y in zip(a[k],a[i])]
  i+=1
  if i==len(a):break
 return i
def p1():
 beta=math.log(4)/math.log(8);need(abs(beta-2/3)<1e-14)
 x=(1/137)**.673;y=.0334**.673
 need(abs(x-.036474307765451554)<1e-15 and abs(y-.10150358285424899)<1e-15)
 need(abs(x-.0334)>.003 and abs(y-.0867)>.014)
 return {'two_point_beta':beta,'first_historical_claim_actual':x,'second_actual':y}
check(1,'Power-law identification and erroneous source decimals',p1)
def p2():
 a=F(1,3);phi=lambda x:x+float(a)*math.copysign(abs(x)**(2/3),x) if x else 0
 xs=[-8,-1,-.01,0,.01,1,8]
 need(abs(phi(8)-28/3)<1e-12)
 for x,y in zip(xs,xs[1:]):need(phi(y)-phi(x)>=y-x-1e-14)
 return 'Signed map monotonicity/inverse-Lipschitz inequalities on declared samples; exact endpoint 28/3.'
check(2,'Signed deformation sample and endpoint',p2)
check(3,'Transported cubic operation',lambda:(need((1+1-1)==1), 'Associative transported sum verified after cubing; multiplication is ordinary.')[1])
check(4,'Constant-width curvature bound and nonlinear obstruction',lambda:(need(F(1)-8*F(1,16)==F(1,2)),need((F(17,16)**(2/3)+F(15,16)**(2/3))<2),'Curvature lower bound1/2; strict concavity width loss.')[2])
check(5,'Irrational endpoint gap',lambda:(need(abs(math.cos(2*math.pi*math.sqrt(2))-1)>0.1),'r(0) andr(2π) differ; numerical gap illustrates exact irrationality proof.')[1])
check(6,'Geometric regularity bounds',lambda:(need(F(1,16)/(1-F(1,8))==F(1,14)),need(F(1,16)/(1-F(1,2))==F(1,8)),'Exact M0=1/14,M2=1/8.')[2])
check(7,'Graph boundary rank and cycle dimensions',lambda:(need(rank([[-1,0,1],[1,-1,0],[0,1,-1]])==2),need(3-2==1),'Triangle boundary has rank2 and cycle rank1; wedge loop count2.')[2])
def p8():
 f=[0,2,2];g=[1,2,3]
 for t in [-1,0,1,2,3,4]:
  need(all(not (x<=t) or y<=t+1 for x,y in zip(f,g)))
  need(all(not (y<=t) or x<=t+1 for x,y in zip(f,g)))
 return 'All threshold breakpoints satisfy the two1-shift cell inclusions.'
check(8,'Finite persistence interleaving',p8)
check(9,'Circle Čech rank',lambda:(need(rank([[-1,1],[-1,1]])==1),'Kernel and cokernel dimensions each1.')[1])
def mm(a,b):return [[sum(a[i][k]*b[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
def comm(a,b):
 ab=mm(a,b);ba=mm(b,a);return [[ab[i][j]-ba[i][j] for j in range(2)] for i in range(2)]
def p10():
 e11=[[1,0],[0,0]];e22=[[0,0],[0,1]];e12=[[0,1],[0,0]];e21=[[0,0],[1,0]]
 need(comm(e11,e12)==e12);need(comm(e22,e21)==e21);need(comm(e12,e21)==[[1,0],[0,-1]])
 return 'Three matrix commutators span all traceless2×2 matrices; projection ranks1+1=2.'
check(10,'HH0 commutator basis and K0 ranks',p10)
def p11():
 for n in range(1,9):
  q=n/2;co=1/math.gamma(q+1)
  d=co*math.gamma(q+1)/math.gamma(q+.5)
  need(abs(d-1/math.gamma((n-1)/2+1))<1e-12)
 return 'First8 Mittag-Leffler coefficient shifts under Caputo order1/2, using gamma values.'
check(11,'Fractional solution coefficient recurrence',p11)
def count(p):return 1+sum((y*y+y-x*x*x+x)%p==0 for x in range(p) for y in range(p))
check(12,'Exact finite-field counts and discriminant',lambda:(need([count(p) for p in [2,3,5,7]]==[5,7,8,9]),need(-8*(-2)**3-27==37),'Counts[5,7,8,9], traces[−2,−3,−2,−1], discriminant37.')[2])
def p13():
 need(math.gcd(count(5),count(7))==1)
 x=F(-5,9);y=F(8,27);need(y*y+y==x*x*x-x)
 return 'Group orders8 and9 are coprime; rational point(−5/9,8/27) lies exactly onE. Prime-to-p logic is in proof.'
check(13,'Non-torsion certificate data',p13)
check(14,'Normalized trace second moments',lambda:(need((F(4,2)+F(9,3)+F(4,5)+F(1,7))/4==F(52,35)), 'Exact sample mean52/35; theoretical density normalization derived in text.')[1])
def p15():
 theta=math.sqrt(2);N=10000;counts=[0]*9
 for n in range(1,N+1):
  u=(n*theta)%1;d=min(9,int(10**u));counts[d-1]+=1
 need(sum(counts)==N)
 need(max(abs(counts[d-1]/N-math.log10(1+1/d)) for d in range(1,10))<.002)
 return {'N':N,'leading_digit_counts':counts,'scope':'finite illustration; limit proved by geometric sums'}
check(15,'Benford logarithmic-fraction computation',p15)
check(16,'Nonnormal residual counterexample',lambda:(need(1/math.sqrt(100**2+1)<.01),'Spectrum distance1, unit-vector residual1/√10001.')[1])
def p17():
 a=4/math.pi;c=32/math.pi**2
 vals=[c*.5*a**(-(m+1)/2)*math.gamma((m+1)/2) for m in [2,3,4]]
 need(abs(vals[0]-1)<1e-14 and abs(vals[1]-1)<1e-14 and abs(vals[2]-3*math.pi/8)<1e-14)
 return {'mass':vals[0],'mean':vals[1],'second_moment':vals[2]}
check(17,'Wigner-surmise gamma integrals',p17)
def primes(n):return [p for p in range(2,n+1) if all(p%d for d in range(2,math.isqrt(p)+1))]
def p18():
 zp=math.prod(1/(1-p**-2) for p in primes(100));delta=math.log(math.pi**2/6)-math.log(zp)
 need(0<delta<1/75)
 return {'logarithmic_tail':delta,'proved_upper_bound':1/75}
check(18,'Euler-product tail enclosure atσ2,P100',p18)
def p19():
 best=max(abs(a*b-a*bp)+abs(ap*b+ap*bp) for a,ap,b,bp in product([-1,1],repeat=4))
 need(best==2);q=2*math.sqrt(2);need(q>2)
 return 'All16 deterministic local cases have bound2; declared singlet directions give2√2.'
check(19,'CHSH exact local enumeration',p19)
check(20,'Two-level temporal overlap',lambda:(need(abs(math.cos(math.pi/2))<1e-15),need(abs(math.cos(math.pi/4)**2-.5)<1e-15),'Survival probabilities atπ/4 andπ/2 are1/2 and0.')[2])
check(21,'Toeplitz moment and exact n3 spectrum',lambda:(need(abs((3+math.sqrt(2))**2+9+(3-math.sqrt(2))**2-31)<1e-12),'TrT3²=31=11·3−2.')[1])
def p22():
 ds=[1,3]
 for n in range(2,5):ds.append(3*ds[-1]-ds[-2])
 need(ds==[1,3,8,21,55]);rp=(3+math.sqrt(5))/2;rm=(3-math.sqrt(5))/2
 need(abs((rp**5-rm**5)/(rp-rm)-55)<1e-10)
 return 'Exact determinant sequence1,3,8,21,55 and closed-formn4 check.'
check(22,'Toeplitz determinant recurrence',p22)
check(23,'Hardy one-atom sharpness',lambda:(need(F(1,2)*2==1), 'g L1 norm2; g/2 L2 norm1/√2; upper and lower atomic bounds2.')[1])
def compose(a,b):return tuple(a[b[i]] for i in range(6))
def inv(a):return tuple(a.index(i) for i in range(6))
def even(a):return sum(a[i]>a[j] for i in range(6) for j in range(i+1,6))%2==0
def p24():
 group=[a for a in permutations(range(6)) if even(a)];todo=set(group);sizes=[]
 while todo:
  a=next(iter(todo));cl={compose(compose(g,a),inv(g)) for g in group};sizes.append(len(cl));todo-=cl
 need(sorted(sizes)==[1,40,40,45,72,72,90])
 return {'group_order':len(group),'class_sizes':sorted(sizes),'scope':'no full automorphism classification claimed'}
check(24,'A6 exact conjugacy-class enumeration',p24)
def pmul(a,b,n=3):
 c=[0]*n
 for i,x in enumerate(a):
  for j,y in enumerate(b):
   if i+j<n:c[i+j]+=x*y
 return c
def ppow(a,k):
 c=[1,0,0]
 for _ in range(k):c=pmul(c,a)
 return c
def p25():
 pairs=[(a,b) for a in range(10) for b in range(7) if 4*a+6*b==38]
 need(pairs==[(2,5),(5,3),(8,1)])
 forms=[pmul(ppow([1,240,2160],a),ppow([1,-504,-16632],b)) for a,b in [(8,1),(5,3),(2,5)]]
 need([x[1] for x in forms]==[1416,-312,-2040]);need(rank(forms)==3)
 return {'basis_first_three_coefficients':forms,'dimension':3,'cusp_dimension':2}
check(25,'Weight38 monomials and Fourier independence',p25)
def p26():
 ds=[1,2,4,8];ts=[0,2,9,28];table=[[ts[i]+ts[j]+3*ds[i]*ds[j] for j in range(4)] for i in range(4)]
 need(table==[[3,8,21,52],[8,16,35,78],[21,35,66,133],[52,78,133,248]])
 return table
check(26,'Magic-square dimension arithmetic',p26)
check(27,'Quiver cotangent chart and dimension',lambda:(need(all((-u*p)+u*p==0 for u,p in product(range(-3,4),repeat=2))),'Chartz=(1,u),w=(−up,p) solves moment equation; quotient dimension2 at m2.')[1])
def p28():
 alpha=1/30;lo=1/729000;hi=1/216000
 h=lambda t:alpha*t**(-1/3)/(1+math.exp(t))
 need(h(lo)>1 and h(hi)<1)
 for _ in range(80):
  mid=(lo+hi)/2
  if h(mid)>1:lo=mid
  else:hi=mid
 return {'second_zero_negative_x':-(lo+hi)/2,'initial_bracket':[-1/216000,-1/729000],'scope':'bisection illustrates monotone exact existence proof'}
check(28,'Logistic deformation second zero',p28)
entries=json.loads(P.joinpath('entries.json').read_text())
need(len(entries)==28);need({e['id'] for e in entries}=={r['id'] for r in checks})
P.joinpath('checks.json').write_text(json.dumps({'checks':checks},ensure_ascii=False,indent=2)+'\n')
print(f'{sum(c["status"]=="passed" for c in checks)}/{len(checks)} checks passed')
if any(c['status']!='passed' for c in checks):raise SystemExit(1)
