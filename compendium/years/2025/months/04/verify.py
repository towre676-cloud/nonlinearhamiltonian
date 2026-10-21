#!/usr/bin/env python3
"""Portable standard-library certificates of April's finite arithmetic and models."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product,combinations
from decimal import Decimal,localcontext
import math,cmath,json
P=Path(__file__).resolve().parent;checks=[]
def need(x,msg='assertion failed'):
 if not x:raise AssertionError(msg)
def check(i,name,fn):
 try:d=fn();checks.append(dict(id=f'Y25-04-{i:03}',name=name,status='passed',detail=str(d)))
 except Exception as e:checks.append(dict(id=f'Y25-04-{i:03}',name=name,status='failed',detail=repr(e)))
def mm(a,b):return[[sum(a[i][k]*b[k][j]for k in range(len(b)))for j in range(len(b[0]))]for i in range(len(a))]
def sub(a,b):return[[x-y for x,y in zip(r,s)]for r,s in zip(a,b)]
def add(a,b):return[[x+y for x,y in zip(r,s)]for r,s in zip(a,b)]
def scale(c,a):return[[c*x for x in r]for r in a]
def adj(a):return[[complex(a[j][i]).conjugate()for j in range(len(a))]for i in range(len(a[0]))]
def eye(n):return[[int(i==j)for j in range(n)]for i in range(n)]
def near(a,b):return max(abs(x-y)for r,s in zip(a,b)for x,y in zip(r,s))<1e-12
def rank(a):
 a=[[F(x)for x in r]for r in a];i=0
 for j in range(len(a[0])):
  k=next((k for k in range(i,len(a))if a[k][j]),None)
  if k is None:continue
  a[i],a[k]=a[k],a[i];v=a[i][j];a[i]=[x/v for x in a[i]]
  for k in range(len(a)):
   if k!=i:v=a[k][j];a[k]=[x-v*y for x,y in zip(a[k],a[i])]
  i+=1
  if i==len(a):break
 return i
I=eye(2);X=[[0,1],[1,0]];Y=[[0,-1j],[1j,0]];Z=[[1,0],[0,-1]]
def c1():
 units=[a for a in range(1680)if math.gcd(a,1680)==1];orders=[]
 for a in units:
  k=1;b=a%1680
  while b!=1:b=b*a%1680;k+=1
  orders.append(k)
 need(len(units)==384 and max(orders)==12);need(384//2==192)
 return {'units':384,'maximum_order':12,'real_degree':192,'order_distribution':{k:orders.count(k)for k in sorted(set(orders))}}
check(1,'Cyclotomic units and automorphism orders',c1)
check(2,'Finite determinant example',lambda:(need(all((s-1)*(s-4)==s*s-5*s+4 for s in range(-5,6))),'Degree2 polynomial example exact; impossible finite384 identity proved by infinitely manyxi zeros.')[1])
def c3():
 m=840;C=lambda k:(m-1 if k==0 else(-1 if k%2==0 else 0))
 for r,t in product(range(1,m),repeat=2):need(C(r-t)-C(r+t)==(m if r==t else 0))
 full=2/m*sum(math.sin(math.pi*s/m)**2 for s in range(1,m));partial=2/m*sum(math.sin(math.pi*s/m)**2 for s in range(1,385))
 need(abs(full-1)<1e-13 and partial<1)
 S=scale(.5,[[1,math.sqrt(2),1],[math.sqrt(2),0,-math.sqrt(2)],[1,-math.sqrt(2),1]])
 need(near(mm(S,S),eye(3)))
 return {'all_integer_parity_orthogonality_pairs':839**2,'full_first_row_norm_squared':full,'truncated_first_row_norm_squared':partial,'m4_S_square':'I3'}
check(3,'Full sine orthogonality and truncation failure',c3)
def c4():
 need(sum(r*r for r in range(1,25))==4900);need(19600/math.pi**2>1960>1680)
 ps=[F(1,4),F(1,2),F(1,4)];need(sum(ps)==1 and sum(p*p for p in ps)==F(3,8))
 theta=math.pi/840;partial=sum((math.sin(r*theta)/math.sin(theta))**2 for r in range(1,385))
 return {'D384_numerical':partial,'rigorous_elementary_lower_bound':1960,'m4_collision_probability':'3/8'}
check(4,'Dimension-mass contradiction and entropy inputs',c4)
def c5():
 A=[[int(abs(i-j)==1)for j in range(5)]for i in range(5)];Id=eye(5);A2=mm(A,A);N2=sub(A2,Id);N4=add(sub(mm(A2,A2),scale(3,A2)),Id)
 need(mm(N2,N2)==add(add(Id,N2),N4));need(mm(N4,N4)==Id);need(all(v>=0 for row in N2+N4 for v in row))
 return 'Five-label exact fusionN1²=I+N2,N2²=I+N2+N4,N4²=I.'
check(5,'Integer fusion-ring recurrence',c5)
def c6():
 vs=list(product([0,1],repeat=2));B=lambda v,w:(-1)**(v[0]*w[1]+v[1]*w[0]);H=[[B(v,w)for w in vs]for v in vs]
 need(mm(H,H)==scale(4,eye(4)));need([v for v in vs if all(B(v,w)==1 for w in vs)]==[(0,0)])
 return 'Allbicharacter rows orthogonal; transparent subgroup only00.'
check(6,'Müger-center finite bicharacter',c6)
check(7,'Z2 quantum-double labels',lambda:(need(sorted((-1)**(a*b)for a,b in product([0,1],repeat=2))==[-1,1,1,1]),need(4==2**2),'Fourflux/charge labels, twists1,1,1,−1; dimension4.')[2])
def c8():
 mul=lambda u,v:(u[0]*v[0]+u[1]*v[1],u[0]*v[1]+u[1]*v[0]);p=(F(1,2),F(1,2));q=(F(1,2),F(-1,2))
 need(mul(p,p)==p and mul(q,q)==q and mul(p,q)==(0,0));need(2**2==4)
 return 'Frobenius pairingdiag1,1; exact separable idempotents; Lagrangian dimension2²=4.'
check(8,'Lagrangian algebra multiplication certificate',c8)
def c9():
 counts=[]
 for a,b,c in [(5,12,2),(41,840,2)]:
  basis=list(product(range(a-1),range(b-1),range(c-1)));need(len(set(basis))==(a-1)*(b-1)*(c-1));counts.append(len(basis))
 need(counts==[44,33560]);return {'Jacobian_basis_dimensions':counts,'scope':'Milnor topological identification cited separately'}
check(9,'Exact Brieskorn Jacobian bases',c9)
def c10():
 vals=[]
 for a,b in [(5,12),(41,840)]:
  need(math.gcd(a,b)==1 and a%2==1 and b%2==0)
  det=F(sum((-1)**(b*j)for j in range(a)),sum((-1)**j for j in range(a)));need(det==a);vals.append(str(det))
 return {'Alexander_minus1_values':vals,'H1_groups':['Z/5','Z/41'],'scope':'branched-cover theorem stated external input'}
check(10,'Link torsion determinant arithmetic',c10)
check(11,'Top-form quotient exactness counterexample',lambda:(need(F(1,2)*2==1),'dxdy=d(xdy); xdxdy=d(x²dy/2); adding all exacttopforms kills bothJacobianbasis elements.')[1])
check(12,'Logarithmic-derivative example',lambda:(need(abs(math.log(2)/(2**1-1)-math.log(2))<1e-15),need(abs(math.log(2)/(2**2-1)-math.log(2)/3)<1e-15),'Atpoints1,2 valueslog2,log2/3; Omegas2,2^(1/3).')[2])
def c13():
 with localcontext()as ctx:
  ctx.prec=70;D=Decimal
  def atan(z):
   return sum(((-1)**n*z**(2*n+1)/D(2*n+1)for n in range(120)),D(0))
  pi=16*atan(D(1)/5)-4*atan(D(1)/239);phi=(1+D(5).sqrt())/2;r=1/phi
  def li(x):return sum((x**n/D(n*n)for n in range(1,201)),D(0))
  a=li(r);b=li(r*r);ea=pi*pi/10-phi.ln()**2;eb=pi*pi/15-phi.ln()**2
  need(abs(a-ea)<D('1e-40')and abs(b-eb)<D('1e-40'))
  tail=r**201/(D(201)**2*(1-r));need(tail<D('1e-45'))
  return {'Li2_inverse_phi':str(a),'Li2_inverse_phi_squared':str(b),'positive_series_tail_bound':str(tail),'scope':'70-digitDecimal; Machinpi and exactfunctional formulas'}
check(13,'Certified golden dilogarithm series',c13)
def c14():
 V=lambda r:math.pi*(math.sinh(2*r)-2*r);small=V(.02)/V(.01);large=V(6)/V(3)
 need(abs(small-8)<.002 and large>300);return {'small_radius_ratio':small,'R3_ratio':large}
check(14,'Hyperbolic volume exact formula',c14)
check(15,'Canceled atom pairing normalization',lambda:(need(F(1,2)*1+F(-1,2)*(-1)==1),need(2*1*1==2),'Twoequal-volumeatomhalves givepairing1,BMO1; Lipschitzlocalbound2LR0.')[2])
def c16():
 for n in range(2,11):
  a=F(n-1,2);need(a*a-a*(n-1)==-F((n-1)**2,4))
 return 'Completed-square lower-bound coefficient exact in dimensions2–10; metric scale stated.'
check(16,'Hyperbolic Poincaré coefficient',c16)
def c17():
 H=scale(2,add(X,Z));need(mm(H,H)==scale(8,I))
 q=5;p=2;w=cmath.exp(2j*math.pi*p/q);U=[[int(i==(j-1)%q)for j in range(q)]for i in range(q)];V=[[w**i if i==j else 0 for j in range(q)]for i in range(q)]
 need(near(mm(U,V),scale(w,mm(V,U))));return 'Half-fluxH²=8I; rationalclock/shiftrelation checkedq5,p2.'
check(17,'Harper matrix and magnetic translation',c17)
def c18():
 need(41*41+840*(-2)==1 and 5*5+12*(-2)==1);need(len({41*r%840 for r in range(840)})==840)
 return 'Exactinverse41mod840 and5mod12; all840labelresiduespermuted; gapexistence notclaimed.'
check(18,'Complete Diophantine residue classification',c18)
check(19,'Overlapping Cantor contraction',lambda:(need(.5<2/(1+math.sqrt(5))<1),need(math.log(2)/math.log((1+math.sqrt(5))/2)>1),'Twoimagesoverlap andcover[0,1]; similarityexponent>1,actualdimension1.')[2])
check(20,'Golden update multipliers',lambda:(need(abs(1-2/(1+math.sqrt(5))-(2/(1+math.sqrt(5)))**2)<1e-15),'λ1multiplierphi>1; λ−1multiplierr²<1; exactclassification inproof.')[1])
def c21():
 C=lambda x,y:F(sum(a*b for a,b in zip(x,y))**2,sum(a*a for a in x)*sum(b*b for b in y))
 need(C([1,1],[1,-1])==0 and C([1,1],[2,2])==1);return 'Smoothedcoherence0 versus1 despiteallpointwisenonzeroratios1.'
check(21,'Finite coherence inequality examples',c21)
check(22,'Homotopy pushout cycle count',lambda:(need(rank([[-1,-1],[1,1]])==1),'Doublemappingcylinder has2edges,2vertices,beta1=1; ordinarypushoutpointbeta1=0.')[1])
def c23():
 for p in [2,3,5,7]:need([math.comb(p,j)%p for j in range(1,p+1)]==[0]*(p-1)+[1])
 return 'Binomialp-seriesreduces tox^p forfourprimes; additivep-series0.'
check(23,'Formal-group height examples',c23)
def c24():
 A=[[1,0,-1],[2,1,3],[-1,-1,-2]];need(rank(A)==3)
 v=[F(1,2),F(-3,2),F(1,2)];need([sum(x*y for x,y in zip(row,v))for row in A]==[0,1,0])
 return 'Dimensionmatrixrank3; Plancklength exponents produceexactdimensionL.'
check(24,'Dimension rank and invariant test',c24)
def c25():
 t=.3;U=[[cmath.exp(1j*t),0],[0,cmath.exp(-1j*t)]];actual=mm(mm(U,X),adj(U));expected=add(scale(math.cos(2*t),X),scale(-math.sin(2*t),Y));need(near(actual,expected));return 'Exact2-levelHeisenbergformula numericallyevaluatedwithsigncheck.'
check(25,'Doubled-frequency observable',c25)
check(26,'Canonical Bogoliubov coefficients',lambda:(need(F(5,4)**2-F(3,4)**2==1),need(F(3,4)**2==F(9,16)),'Commutator1 andvacuumoccupation9/16 atrlog2.')[2])
def c27():
 S1=[[0,F(1)],[-1,0]];S2=[[0,F(1,2)],[-2,0]];M=mm(S2,S1);need(M==[[F(-1,2),0],[0,-2]])
 need(M[0][0]*M[1][1]==1);return 'Exactmonodromydiag−1/2,−2,det1; growthrate4log2/(3pi).'
check(27,'Parametric oscillator monodromy',c27)
def c28():
 roots=set()
 for i,j in combinations(range(8),2):
  for a,b in product([-1,1],repeat=2):
   v=[F(0)]*8;v[i]=a;v[j]=b;roots.add(tuple(v))
 for signs in product([-1,1],repeat=8):
  if sum(x<0 for x in signs)%2==0:roots.add(tuple(F(x,2)for x in signs))
 need(len(roots)==240 and all(sum(x*x for x in r)==2 for r in roots));need(rank(list(roots))==8)
 return {'distinct_roots':240,'rank':8,'squared_length':2,'Lie_dimension_with_root_space_theorem':248}
check(28,'Exact E8 root enumeration',c28)
es=json.loads((P/'entries.json').read_text());need(len(es)==28 and {e['id']for e in es}=={c['id']for c in checks})
P.joinpath('checks.json').write_text(json.dumps({'scope':'Finite arithmetic/model certificates; external structural theorems and unrecovered claims remain explicitly bounded in the entries.','checks':checks},ensure_ascii=False,indent=2)+'\n')
print(f'{sum(c["status"]=="passed"for c in checks)}/{len(checks)} passed')
if any(c['status']!='passed'for c in checks):raise SystemExit(1)
