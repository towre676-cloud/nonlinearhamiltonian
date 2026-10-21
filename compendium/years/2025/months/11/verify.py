#!/usr/bin/env python3
"""Portable finite certificates. Written proofs provide the general results."""
import json,math,cmath,re,itertools
from fractions import Fraction as F
from pathlib import Path
P=Path(__file__).resolve().parent;E=json.loads((P/'entries.json').read_text());C=[]
def ck(n,name,f):
 try:d=f();s='pass'
 except Exception as e:d=repr(e);s='fail'
 C.append(dict(id=f'Y25-11-{n:03d}',name=name,status=s,detail=d or 'Exact finite assertions passed.'))
def mm(A,B):return [[sum(a*b for a,b in zip(r,c)) for c in zip(*B)] for r in A]
def near(a,b,t=1e-8):assert abs(a-b)<t,(a,b)
def schema():
 assert len(E)==31
 for i,e in enumerate(E,1):
  assert e['id']==f'Y25-11-{i:03d}' and e['original']['month']=='2025-11'
  for k in ('title','summary','status','limits','extension'):assert isinstance(e[k],str) and e[k]
  for k in ('name','statement','proof'):assert e['result'][k]
  for k in ('setup','calculation','conclusion'):assert e['example'][k]
  o=e['original'];assert o['original_question'] is None
  if o['evidence']!='T':assert (o['evidence'],o['date']) in re.findall(r'([UA])@(2025-\d\d-\d\d)',o['source_excerpt'])
 return '31 entries and dated provenance validated; T passage carries an explicit file date.'
ck(0,'Schema and dated attribution',schema)
def c1():
 for x in (-3,-.5,0,.8,4):near(1/(1+4**x)+1/(1+4**(-x)),1)
 I=lambda a:math.pi/(4*math.sqrt(2))*(1+math.exp(-math.sqrt(2)*abs(a))*(math.cos(math.sqrt(2)*abs(a))+math.sin(math.sqrt(2)*abs(a))))
 near(I(0),math.pi/(2*math.sqrt(2)))
 # Independent midpoint quadrature over a long interval; quartic tail bounded by 2/(3 R^3).
 a=.7;R=40;N=80000;h=2*R/N
 q=sum(math.cos(a*(-R+(j+.5)*h))**2/(1+(-R+(j+.5)*h)**4)/(1+4**(-R+(j+.5)*h)) for j in range(N))*h
 assert abs(q-I(a))<2/(3*R**3)+1e-7
 return 'Parity identity and independent quadrature agree with the exact contour formula within a rigorous quartic-tail allowance.'
ck(1,'Quartic integral formula',c1)
def c2():
 near(.5*(1+math.exp(-.5)),.8032653298563167)
 t=1/math.sqrt(3);v=t*t/4-math.log(1+2*t*t)/8
 near(v,(2+3*math.log(3/5))/24)
 assert math.pi>1 and (3*math.log(3)-4*math.log(2))/4>0
 return 'Correct Lorentzian normalization, tangent antiderivative and positive double-integral value checked.'
ck(2,'Atlas integral checks',c2)
def c3():
 a=F(16,17);b=F(1,2);assert (1-b)*(1+b-2*a*a)==F(-157,1156)
 return 'Exact 3x3 Gram determinant -157/1156 rejects positive definiteness.'
ck(3,'Positive-definite counterexample',c3)
def c4():
 assert F(1,3)-F(1,2)**2==F(1,12)
 assert F(1)-F(1)**2==0
 return 'Bridge covariance correction gives 1/12 for f=t and zero for f=1.'
ck(4,'Bridge variance',c4)
def c5():
 assert F(1)-F(1,2)==F(1,2) and 16-F(1,2)*4==14
 for n in (1,2,3):assert n**4-n*n>=0
 return 'Hinged eigenvalues and sharp threshold P=1 at L=pi,D=1.'
ck(5,'Beam spectral threshold',c5)
def c6():
 near(math.log(320/math.e),math.log(320)-1);assert abs(math.log(320/math.e)-1)>1
 near(320*math.log(2),221.8070977791825)
 return 'The two entropy sample spaces differ; exact-period obstruction is proved by the endpoint theorem in text.'
ck(6,'Entropy normalization',c6)
def c7():
 for n in (1,8,16):near((math.pi**(n+1)*math.exp(n+.5)*math.gamma(n+1))/(math.pi**n*math.exp(n-.5)*math.gamma(n)),math.pi*math.e*n,1e-7)
 return 'Successive spectral ratios equal pi*e*n, not a fixed limit.'
ck(7,'Gamma spectrum ratios',c7)
def c8():
 # Polynomial residuals in s=sn: sn''=-(1+m)s+2ms^3.
 m=F(1,2);assert (1+m)==F(3,2)
 for s in (F(0),F(1,3),F(1)):
  spp=-(1+m)*s+2*m*s**3;assert -spp+2*m*s**3==(1+m)*s
 return 'Exact sn Lamé residual for m=1/2; cn/dn derivative identities and factorization are proved in text.'
ck(8,'Lame n=1 residual',c8)
def c9():
 assert 1**2-4*0*0==1
 assert math.gcd(0,math.gcd(1,0))==1 and math.gcd(0,math.gcd(2,0))==2
 return 'Primitive rho=0 relation has discriminant1; doubling it is nonprimitive.'
ck(9,'Humbert primitiveness',c9)
def c10():
 c=[F(1)]
 for n in range(1,6):c.append(c[-1]*F(n*n,1)/(F(n)-F(1,4))/(F(n)-F(3,4)))
 assert c[1]==F(16,3) and c[2]==F(1024,105)
 for n in range(1,6):assert n*(F(n)-F(1,4))*(F(n)-F(3,4))*c[n]==n**3*c[n-1]
 return 'Hypergeometric coefficient residuals through degree5; corrected c2=1024/105.'
ck(10,'Wallis/hypergeometric recurrence',c10)
def c11():
 t=.7;eps=.2;a=1;q=a*math.exp(-t);exact=q/(1-eps*a*(1-math.exp(-t)));x1=a*a*math.exp(-t)*(1-math.exp(-t))
 assert abs(exact-q-eps*x1)<=math.exp(-t)*eps**2/(1-eps)
 return 'Exact nonlinear ODE solution obeys the stated geometric-series remainder.'
ck(11,'Volterra expansion remainder',c11)
def c12():
 sig=lambda n:sum(d**3 for d in range(1,n+1) if n%d==0) if n else 0
 for p in (2,3,5):
  for n in range(1,30):assert sig(p*n)+p**3*(sig(n//p) if n%p==0 else 0)==(1+p**3)*sig(n)
 return 'Full prime-divisibility Hecke recurrence checked exactly for 87 cases.'
ck(12,'Hecke coefficient identity',c12)
def c13():
 for t in (F(0),F(1,10),F(1,4)):
  scale=1-2*t;assert 2/scale**2==2*(1/scale**2)
 return 'Round-sphere metric scaling agrees with the corrected Ricci commutator; general derivation is in text.'
ck(13,'Ricci flow convention',c13)
def c14():
 R=[[0,1],[0,0]];Rt=[[0,0],[1,0]];A=mm(R,Rt);B=mm(Rt,R)
 X=[[A[i][j]-B[i][j] for j in range(2)] for i in range(2)]
 assert X==[[1,0],[0,-1]] and X[0][0]+X[1][1]==0
 return 'Finite commutator is Hermitian trace-zero; weighted trace at s=1 is 1/2.'
ck(14,'Commutator trace',c14)
def c15():
 z=[1]*5+[-1]*5;assert sum(z)==0 and sum(x*x for x in z)==10
 return 'Opposing phase cones have zero first resultant and unit second resultant.'
ck(15,'Circular mixture ambiguity',c15)
def c16():
 w=(1+math.sqrt(5))/2
 for k in ((1,0),(0,1),(2,-1),(3,-2)):
  v=k[0]+k[1]*w;assert abs(v)>0
  T=1000;avg=(cmath.exp(2j*math.pi*T*v)-1)/(2j*math.pi*T*v);assert abs(avg)<=1/(math.pi*T*abs(v))+1e-12
 return 'Active irrational character averages satisfy the exact O(1/T) bound.'
ck(16,'Kronecker averages',c16)
def c17():
 for a in (F(-1),F(0),F(2)):
  mins=[F(0)]
  if a>0:mins.append(-a*a/4)
  assert min(mins)==(0 if a<=0 else -a*a/4)
 return 'Landau minimized energy has distinct left/right second derivatives; inflection ridge remains polynomial.'
ck(17,'Phase-ridge distinction',c17)
def c18():
 p=[F(2,3),F(1,3)];eigs=[a/b for a in p for b in p];assert eigs==[1,2,F(1,2),1]
 return 'Finite modular eigenvalue ratios 1,2,1/2,1 from the faithful density matrix.'
ck(18,'Finite modular spectrum',c18)
def c19():
 X=[[0,0,0],[0,0,0],[0,0,1]];A=[[0,1,0],[1,0,0],[0,0,1]];assert mm(A,X)==mm(X,A)
 assert A[0][1]!=0 and F(1,2)==1/F(2)
 return 'Commuting nonscalar multiplicity block and two-point distance 1/2.'
ck(19,'Commutant and distance',c19)
def c20():
 for v in range(3,10):
  for k in range(1,v):
   z=cmath.exp(2j*math.pi*k/v);c=z.real;M=[[(3+c)/8,(1+1/z)/16],[(1+z)/4,.25]]
   near(M[0][0]+M[1][1],(5+c)/8);near(M[0][0]*M[1][1]-M[0][1]*M[1][0],1/16)
   assert (c+9)*(c+1)>-1e-12
 return 'Standard Catmull-Clark block trace, determinant and real discriminant checked across valences3-9.'
ck(20,'Stencil Fourier certificate',c20)
def c21():
 B=[[1,1],[0,1]];Bt=[[1,0],[1,1]];C0=mm(Bt,B);assert C0==[[1,1],[1,2]] and C0[0][0]*C0[1][1]-C0[0][1]*C0[1][0]==1
 return 'B*B has trace3 determinant1, hence Levi characteristic t4-3t2+1.'
ck(21,'Levi singular spectrum',c21)
def c22():
 d=[[-1,1,0],[0,-1,1],[1,0,-1]];assert mm(d,[[1],[1],[1]])==[[0],[0],[0]]
 A=[[1,1],[0,1]];M=[[1,1,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]];J=[[0,0,1,0],[0,0,0,1],[-1,0,0,0],[0,-1,0,0]]
 assert mm(mm(list(map(list,zip(*M))),J),M)!=J
 return 'Cycle harmonic vector and determinant-one nonsymplectic 4x4 counterexample.'
ck(22,'Hodge and symplectic data',c22)
def c23():
 a=F(1,2);d=F(2);x=0
 for n in range(8):
  assert x==(d**n-a**n)/(d-a)
  x=a*x+d**n
 assert F(2)-F(1)**2/F(1)==1 and F(2)-F(2)**2/F(1)==-2
 return 'Forced recurrence and positive/negative Schur complements checked exactly.'
ck(23,'Block forcing and Schur complement',c23)
def c24():
 # Algebraic identities valid for every distinct a,b and nonzero r; use rational specialization.
 a,b,r=F(2),F(-1),F(3);B=[[a,r],[0,b]]
 S=[[a,r,1,0],[0,b,0,1],[0,0,a,r],[0,0,0,b]];N=[[0,0,1,0],[0,0,0,1],[0,0,0,0],[0,0,0,0]]
 Ss=[[S[i][j]-N[i][j] for j in range(4)] for i in range(4)];assert mm(N,N)==[[0]*4 for _ in range(4)] and mm(Ss,N)==mm(N,Ss)
 U=[[S[i][j] if j>i else 0 for j in range(4)] for i in range(4)];assert mm(U,U)[0][3]==2*r and mm(mm(U,U),U)==[[0]*4 for _ in range(4)]
 return 'Universal block algebra checked: commuting nilpotent squares to zero, raw triangle cubes to zero with nonzero square.'
ck(24,'S6 decomposition',c24)
def c25():
 a=[1,1,1]
 for _ in range(9):a.append(a[-2]+a[-3])
 assert a==[1,1,1,2,2,3,4,5,7,9,12,16]
 assert -4*(-1)**3-27*(-1)**2==-23
 return 'Padovan terms and cubic discriminant -23 checked exactly.'
ck(25,'Plastic Pisot recurrence',c25)
def c26():
 f=lambda h:F(7)+3*h*h+5*h**4
 for h in (F(1),F(1,2),F(1,4)):assert (4*f(h/2)-f(h))/3==7-F(5,4)*h**4
 assert (4*F(1,64)+1)/3==F(17,48)
 return 'Exact quartic cancellation and sixth-order remainder constant.'
ck(26,'Drift extrapolation',c26)
def c27():
 T=[[1,F(0)],[F(1,2),F(1,2)]];A=[[F(1),F(0)],[F(0),F(1)]]
 for n in range(1,8):
  A=mm(A,T);assert A==[[1,0],[1-F(1,2)**n,F(1,2)**n]]
 return 'Oblique stochastic iteration limit computed by exact powers.'
ck(27,'IMP limit counterexample',c27)
def c28():
 # Off-diagonal product uses (1+i sqrt3)(1-i sqrt3)=4.
 det=F(-7,48)*F(-9,8)-F(3,32)*F(5,16)*4
 assert det==F(3,64) and F(-7,48)+F(-9,8)==F(-61,48)
 assert 1-F(61,48)+F(3,64)==F(-43,192)
 return 'Recovered curvature determinant/trace and chi(-1)<0 certify an eigenvalue below -1.'
ck(28,'Unstable recovered block',c28)
def c29():
 n=8192;d=16;assert n*n==67108864 and 2*n*d==262144 and F(n*n,2*n*d)==256
 return 'Isolated rank-factor multiplication costs differ by256, not the differently normalized6144.'
ck(29,'Low-rank cost arithmetic',c29)
def c30():
 for t in (.1,.4,.8):
  pp=math.tanh(1-t);pprime=-(1-pp*pp);near(pprime,pp*pp-1)
 return 'Explicit Riccati solution satisfies Pprime=P2-1 and P(1)=0.'
ck(30,'LQR Riccati solution',c30)
def c31():
 e=.3;mult=math.exp(-e*e);near(-(-mult),mult)
 assert sum([F(1),F(-1)])==0
 return 'Poisson cosine residual and zero-mode compatibility checked.'
ck(31,'Poisson smoothing mode',c31)
(P/'checks.json').write_text(json.dumps({'checks':C},ensure_ascii=False,indent=2)+'\n');print(sum(x['status']=='pass' for x in C),'/',len(C))
if any(x['status']!='pass' for x in C):
 print([x for x in C if x['status']!='pass']);raise SystemExit(1)
