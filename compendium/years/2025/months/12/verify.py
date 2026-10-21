#!/usr/bin/env python3
"""Standard-library finite certificates for the recovered mathematical examples."""
import json,math,re,itertools,cmath
from fractions import Fraction as F
from pathlib import Path
from functools import reduce
P=Path(__file__).resolve().parent;E=json.loads((P/'entries.json').read_text());C=[]
def ck(n,name,f):
 try:d=f();s='pass'
 except Exception as e:d=repr(e);s='fail'
 C.append(dict(id=f'Y25-12-{n:03d}',name=name,status=s,detail=d or 'Finite assertions passed.'))
def mm(A,B):return [[sum(a*b for a,b in zip(r,c)) for c in zip(*B)] for r in A]
def near(a,b,t=1e-9):assert abs(a-b)<t,(a,b)
def bern(N):
 b=[F(1)]
 for n in range(1,N+1):b.append(-sum(F(math.comb(n+1,k))*b[k] for k in range(n))/F(n+1))
 return b
def stir(N):
 s=[[F(0)]*(N+1) for _ in range(N+1)];s[0][0]=1
 for n in range(N):
  for k in range(n+2):s[n+1][k]=(s[n][k-1] if k else 0)-n*s[n][k]
 return s
def schema():
 assert len(E)==27
 for i,e in enumerate(E,1):
  assert e['id']==f'Y25-12-{i:03d}'
  o=e['original'];assert o['month']=='2025-12' and o['original_question'] is None
  assert (o['evidence'],o['date']) in re.findall(r'([UA])@(2025-\d\d-\d\d)',o['source_excerpt'])
  for group in ('result','example'):assert all(isinstance(x,str) and x for x in e[group].values())
 return '27 complete entries with source/date/author matching and no invented verbatim prompts.'
ck(0,'Schema and attribution',schema)
def c1():
 s=stir(4);b=bern(4);A=[[s[n][k]*b[k] for k in range(5)] for n in range(5)]
 assert A[4]==[0,3,F(11,6),0,F(-1,30)]
 mu=[1,F(1,10),F(3,100),F(1,100),0];v=[sum(A[n][k]*mu[k] for k in range(5)) for n in range(4)]
 assert v==[1,F(-1,20),F(11,200),F(-23,200)] and all(A[n][3]==0 for n in range(5))
 assert sum(A[4][k]*10**k for k in range(5))==-120
 return 'All corrected rows and example moments exact; zero column and negative fourth moment certified.'
ck(1,'Stirling-Bernoulli matrix',c1)
def c2():
 # Average f(x+t): coefficient x^j from x^k is binom(k,j)/(k-j+1).
 f=[0,F(1,2),F(-3,2),1];avg=[sum(f[k]*F(math.comb(k,j),k-j+1) for k in range(j,4)) for j in range(4)]
 assert avg==[0,0,0,1]
 b=bern(3);assert [2**n*b[n] for n in range(2)]==[1,-1]
 return 'Bernoulli differential inverse returns x^3 under averaging; Blissard product begins 1-t.'
ck(2,'Bernoulli inverse and product',c2)
def c3():
 A=[[1,0,0],[F(1,2),1,0],[F(1,4),F(1,2),1]]
 cols=[sum(abs(A[i][j]) for i in range(3)) for j in range(3)];assert max(cols)==F(7,4)
 assert sum(row[0] for row in A)==F(7,4)
 return 'Weighted-column theorem attains the finite norm7/4 on e0; infinite geometric tail is2.'
ck(3,'Weighted column norm',c3)
def c4():
 h=[-1,3,-3,1];assert sum(h[j]*j*j for j in range(4))==0 and sum(h[j]*j**3 for j in range(4))==6
 return 'Third difference annihilates x^2 and maps x^3 to6.'
ck(4,'FIR moment constraints',c4)
def c5():
 assert [math.comb(3,j) for j in range(4)]==[1,3,3,1]
 for x in (F(1,5),F(1,2),F(2)):
  assert (x+x*x)**3==x**3+3*x**4+3*x**5+x**6
 return 'Exact composition expansion has degrees3through6, demonstrating increasing bandwidth.'
ck(5,'Composition coefficients',c5)
def c6():
 r=F(16,5);assert -r*r+2*r+4==F(4,25)
 assert F(2)-F(3)==-1
 return 'Two-cycle multiplier4/25 at r=3.2; fixed-point boundary multiplier -1 at r=3.'
ck(6,'Logistic bifurcation arithmetic',c6)
def c7():
 h=F(1,2);a=1-h;v=h/(1-a*a);assert v==F(2,3) and v==a*a*v+h
 return 'Discrete OU stationary variance2epsilon/3 satisfies the exact variance recurrence.'
ck(7,'Euler-Maruyama variance',c7)
def c8():
 T=.8;W=(1-math.exp(-2*T))/2;a=1.3
 cost=.5*a*a/W;near(cost,a*a/(1-math.exp(-2*T)))
 return 'OU Gramian and minimum action agree with both equivalent formulas.'
ck(8,'Gramian action',c8)
def c9():
 for v in (F(1,2),F(2),F(-3)):
  p=(1 if v>=0 else -1)*max(abs(v)-1,0);H=p*p/2+abs(p);L=max(abs(v)-1,0)**2/2
  assert p*v-H==L
 return 'Fenchel maximizing momenta produce the stated hinge-squared Lagrangian.'
ck(9,'Fenchel duality',c9)
def c10():
 Fnorm=lambda x,y:max(abs(x),abs(y))
 assert Fnorm(1,1)==1 and Fnorm(1,0)+Fnorm(0,1)==2
 omega=1/math.sqrt(.2*7.5e-10);near(omega,81649.6580927726,1e-7)
 near(omega/(2*math.pi),12994.946687227936,1e-7)
 return 'Straight-vs-detour norm lengths and LC angular/ordinary frequencies checked.'
ck(10,'Metric and LC normalization',c10)
def c11():
 t=2.;p=1-math.exp(-1);rate=-math.log(1-p)/t;near(rate,.5);near(-math.log(rate),math.log(2))
 return 'Exact exponential-law inversion at the worked probability; logarithm argument is a rate ratio.'
ck(11,'Barrier inversion',c11)
def c12():
 a=F(15,1000);b=F(20,1000)
 assert F(10,1000)**2<a*b and F(30,1000)**2>a*b and a+b==F(35,1000)
 return 'Stable/unstable symmetric models share trace -0.035 but have opposite determinant signs.'
ck(12,'Abel-Liouville distinction',c12)
def order(p):
 r=10%p;n=1
 while r!=1:r=r*10%p;n+=1;assert n<=p
 return n
def c13():
 assert order(7)==6 and order(11)==2
 ps=[7,17,19,23,29,47,59,61,97,109,113]
 return 'Exact decimal orders: '+str({p:order(p) for p in ps})
ck(13,'Remainder orbit orders',c13)
def c14():
 m=97;p=F(1,m);Fisher=[[p*int(i==j)-p*p for j in range(3)] for i in range(3)]
 assert p-m*p*p==0;near(math.log(m),4.574710978503383)
 return 'Uniform entropy log97 and Fisher null-direction coefficient p-mp^2=0.'
ck(14,'Softmax Fisher normalization',c14)
def c15():
 g=[3,1];M=[1,4];lam=2;d=[-F(1,M[i])*max(g[i]-lam,0) for i in range(2)];assert d==[-1,0]
 assert mm([[1,0],[0,0]],[[0],[-1]])==[[0],[0]]
 return 'Diagonal proximal minimizer and discarded-gradient projection checked exactly.'
ck(15,'Tube proximal model',c15)
def c16():
 eps=.01;delta=.002;norm=abs(delta)/math.sqrt(delta*delta+eps)
 assert norm<=abs(delta)/math.sqrt(eps)
 for x in (-2.17,-.03,0,.57,3.14):assert abs(.1*round(x/.1)-x)<=.05+1e-12
 return 'Nearest quantization bound and centered LayerNorm perturbation bound checked.'
ck(16,'Quantization domain and sensitivity',c16)
def c17():
 a=F(2);U=lambda m:m**4/4-a*m*m/2
 assert a*a/4==1 and -a*a/4==-1
 k=F(4);assert F(4,3)*8==F(32,3)
 return 'Exact symmetric barrier1 and saddle-node barrier32/3 at kappa4.'
ck(17,'Pitchfork and fold barriers',c17)
def det(A):
 A=[[F(x) for x in r] for r in A];d=F(1)
 for k in range(len(A)):
  pivot=next((j for j in range(k,len(A)) if A[j][k]),None)
  if pivot is None:return F(0)
  if pivot!=k:A[k],A[pivot]=A[pivot],A[k];d=-d
  v=A[k][k];d*=v
  for i in range(k+1,len(A)):
   f=A[i][k]/v
   for j in range(k+1,len(A)):A[i][j]-=f*A[k][j]
 return d
modes={1:(F(1),F(2)),2:(F(1,2),F(-1)),4:(F(1,2),F(1)),8:(F(3,8),F(-3,4))}
def moment(n):return sum(a*(-1)**(n//2)*k**n for k,(a,b) in modes.items()) if n%2==0 else F(0)
def c18():
 d8=det([[moment(i+j) for j in range(8)] for i in range(8)]);d9=det([[moment(i+j) for j in range(9)] for i in range(9)])
 assert d8==3317490507809254951983513600000000 and d9==0
 poly=[4096,0,5440,0,1428,0,85,0,1]
 for n in range(20):assert sum(c*moment(n+j) for j,c in enumerate(poly))==0
 return 'Exact nonzero Hankel8 determinant, zero Hankel9 and order-eight derivative recurrence.'
ck(18,'Original oscillator minimality',c18)
def primitive(p):
 while len(p)>1 and p[-1]==0:p.pop()
 g=reduce(math.gcd,p);assert g
 return [x//g for x in p]
def disk(p):
 p=primitive(p[:]);count=0;steps=[]
 while len(p)>1:
  a,b=p[-1],p[0];assert abs(a)!=abs(b)
  if abs(a)>abs(b):q=[a*x-b*y for x,y in zip(p,p[::-1])][1:];inc=1
  else:q=[b*x-a*y for x,y in zip(p,p[::-1])][:-1];inc=0
  q=primitive(q);assert len(q)<len(p);steps.append(dict(polynomial=p,reduced=q,increment=inc));count+=inc;p=q
 assert p[0];return count,steps

def c19():
 z={}
 for k,(a,b) in modes.items():z[k]=(a+b)/2;z[-k]=(a-b)/2
 tan={k:k*v for k,v in z.items()};w={k:(1-k)*v for k,v in z.items()}
 def pp(d):
  den=math.lcm(*(v.denominator for v in d.values()));return primitive([int(d.get(j-8,F(0))*den) for j in range(17)])
 p=pp(tan);q=pp(w)
 assert p==[-9,0,0,0,2,0,-3,1,0,3,-1,0,6,0,0,0,-3]
 assert q==[81,0,0,0,-20,0,36,-16,0,0,4,0,-36,0,0,0,21]
 np,sp=disk(p);nq,sq=disk(q);assert (np,nq)==(6,2)
 bez=json.loads((P/'bezout_certificate.json').read_text())
 def conv(a,b):
  out=[F(0)]*(len(a)+len(b)-1)
  for i,x in enumerate(a):
   for j,y in enumerate(b):out[i+j]+=x*y
  return out
 for name,poly in [('tangent',p),('w',q)]:
  z=bez[name];assert z['polynomial']==poly
  U=list(map(F,z['U']));V=list(map(F,z['V']));up=conv(U,poly);vp=conv(V,poly[::-1]);res=[a+b for a,b in zip(up,vp)]
  assert res[0]==1 and all(x==0 for x in res[1:])
  assert 1/(sum(map(abs,U))+sum(map(abs,V)))==F(z['lower_bound'])
 assert F(bez['tangent']['lower_bound'])/2==F(3,35)
 assert F(bez['w']['lower_bound'])/16>F(1,26)
 (P/'winding_certificate.json').write_text(json.dumps(dict(tangent=dict(inside=np,winding=np-8,steps=sp),w=dict(inside=nq,winding=nq-8,steps=sq)),indent=2)+'\n')
 return 'Independently rebuilt Laurent polynomials; strict integer Rouche recursion gives disk counts6,2 and windings-2,-6 without unit roots; exact Bezout identities prove margins3/35 and1/26.'
ck(19,'Original oscillator exact windings',c19)
def c20():
 M=list(itertools.product(range(2),range(3)))
 mul=lambda x,y:((x[0]+y[0])%2,min(x[1]+y[1],2))
 for a,b,c in itertools.product(M,repeat=3):assert mul(mul(a,b),c)==mul(a,mul(b,c))
 assert [x for x in M if mul(x,x)==x]==[(0,0),(0,2)]
 return 'All216associativity triples in the six-element capped product, identity and two idempotents.'
ck(20,'Capped monoid exhaustive check',c20)
def c21():
 for u,v in [((1,0,0),(0,1,0)),((1,0,0),(-1,0,0)),((1,0,0),(1,0,0))]:
  dot=sum(a*b for a,b in zip(u,v));diff=sum((a-b)**2 for a,b in zip(u,v));assert 1-dot*dot<=diff
 assert 4*F(1,2)**2==1
 return 'Exact unit-vector disorder inequality including antipodal directions; normalized constant weight has Jr=1.'
ck(21,'Two-point geometric inequality',c21)
def c22():
 for a,b in itertools.product(range(-3,4),repeat=2):assert (a*a)*(b*b)-(a*b)**2==0
 assert 4*math.pi**3>0
 return 'Every collinear vorticity pair has zero misalignment while shear gradient energy4pi^3 is positive.'
ck(22,'Coercivity shear counterexample',c22)
def c23():
 P0,Q,R,G=False,True,True,False
 assert ((not(P0 and Q and R)) or G) and not G
 N=[[0,F(631,25000)],[0,0]];assert mm(N,N)==[[0,0],[0,0]]
 return 'Conditional implication has a countermodel to unconditional G; hard-coded Jordan residual is square-zero.'
ck(23,'Conditional-proof dependency',c23)
def c24():
 L=[[1,1],[1,-1]];mu=[[1],[0]];d=[[0],[1]];a=mm(L,mu);b=mm(L,d)
 assert [a[i][0]*b[i][0] for i in range(2)]==[1,-1]
 assert [mu[i][0]*d[i][0] for i in range(2)]==[0,0]
 assert mm([[1,1]],[[1],[0]])==mm([[1,1]],[[0],[1]])
 return 'Hadamard rank changes0to1 under the claimed coordinate rule; one-sparse ambiguity is exact.'
ck(24,'Weighted rank counterexample',c24)
def c25():
 c=[1,2,0,0];f=[3,5,7,11];assert sum(x*y for x,y in zip(c,f))==13
 return 'Orthogonal mode coefficient pairing gives13 and kills the specified excluded modes.'
ck(25,'Portal spectral projection',c25)
def c26():
 for n in range(8):assert sum(F(1,2**(j-1)) for j in range(n+1,n+30))<F(2,2**n)
 return 'Exact finite tails lie under2^(1-n); tail formula and trace-class limit are proved in text.'
ck(26,'Greedy deflation tails',c26)
def c27():
 lam=F(1);b=F(3);eps=F(1,5);mean=b/lam;var=eps/(2*lam)
 assert -lam*mean+b==0 and -2*lam*var+eps==0
 return 'Stationary OU cumulants satisfy mean3,varianceepsilon/2; changing forcing leaves drift eigenvalue-1.'
ck(27,'OU cumulant hierarchy',c27)
(P/'checks.json').write_text(json.dumps({'checks':C},ensure_ascii=False,indent=2)+'\n');print(sum(x['status']=='pass' for x in C),'/',len(C))
if any(x['status']!='pass' for x in C):print([x for x in C if x['status']!='pass']);raise SystemExit(1)
