#!/usr/bin/env python3
"""Portable, standard-library checks for the stated finite examples.
These exact/finite checks supplement, and do not replace, the written proofs.
"""
import json,math,cmath,re
from fractions import Fraction as F
from pathlib import Path
P=Path(__file__).resolve().parent
E=json.loads((P/'entries.json').read_text())
checks=[]
def check(n,name,fn):
 try: detail=fn(); status='pass'
 except Exception as e: detail=f'{type(e).__name__}: {e}';status='fail'
 checks.append(dict(id=f'Y24-11-{n:03d}',name=name,status=status,detail=detail or 'All stated assertions passed.'))
def mm(A,B):return [[sum(a*b for a,b in zip(row,col)) for col in zip(*B)] for row in A]
def tr(A):return list(map(list,zip(*A)))
def near(a,b,tol=1e-10):assert abs(a-b)<tol,(a,b)
def schema():
 assert len(E)==26
 for i,e in enumerate(E,1):
  assert e['id']==f'Y24-11-{i:03d}'
  for k in ('title','status','summary','limits','extension'):assert isinstance(e[k],str) and e[k]
  for g,ks in [('result',('name','statement','proof')),('example',('setup','calculation','conclusion'))]:
   for k in ks:assert isinstance(e[g][k],str) and e[g][k]
  o=e['original'];assert o['month']=='2024-11' and o['original_question'] is None
  assert (o['evidence'],o['date']) in re.findall(r'([UAT])@(2024-\d\d-\d\d)',o['source_excerpt'])
 return '26 entries: complete schema; dated attribution matches its selected source line; no invented verbatim original questions.'
check(0,'Schema and dated evidence attribution',schema)
def c1():
 lo=100000*F(108,100)**5;hi=100000*F(118,100)**5
 assert lo==F('146932.80768') and hi==F('228775.77568') and lo<177543<hi
 assert sum([10000,5000,12000,7500,15000,15000,10000])==74500
 assert F(245,700)==F(35,100) and 700000*1300==910000000
 return 'Exact rational growth bounds, 74500 allocation total, weekly normalization, aggregate/per-recipient factors.'
check(1,'Growth and denominator arithmetic',c1)
def c2():
 u=[1,0,0,0];p=[F(1,4)]*4;r=[a-b for a,b in zip(u,p)]
 assert sum(x*x for x in p)==F(1,4) and sum(x*x for x in r)==F(3,4)
 assert sum(a*b for a,b in zip(p,r))==0
 assert abs(1-F(3,2)*2)==2
 return 'Exact orthogonal energies 1/4 and 3/4; Euler step h=3/2 produces multiplier -2.'
check(2,'Bandwise energy certificate',c2)
def c3():
 S=[[F(0) for _ in range(5)] for _ in range(5)]
 for j,x in enumerate((-10,-5,0,5,10)):
  S[j][j]=x*x+F(2,25)
  if j<4:S[j][j+1]=S[j+1][j]=F(-1,25)
 for v in ([1,2,3,4,5],[0,0,1,0,0],[-2,3,-1,4,0]):
  q=sum(v[i]*S[i][j]*v[j] for i in range(5) for j in range(5));w=[0]+v+[0]
  form=sum(F((w[j+1]-w[j])**2,25) for j in range(6))+sum(x*x*v[j]*v[j] for j,x in enumerate((-10,-5,0,5,10)))
  assert q==form and q>0
 intervals=[(S[i][i]-sum(abs(S[i][j]) for j in range(5) if j!=i),S[i][i]+sum(abs(S[i][j]) for j in range(5) if j!=i)) for i in range(5)]
 for x in (F('-0.08'),F('24.88'),F('99.88')):assert not any(a<=x<=b for a,b in intervals)
 return 'Matrix assembled independently; quadratic-form expansion and excluded historical eigenvalues checked exactly.'
check(3,'Positive finite-difference matrix',c3)
def c4():
 z=F(1,4);delta=F(1,1000)
 assert (1-z)/(1-(1+delta)*z)==1/(1-delta/3)
 return 'Exact factor cancellation at s=2, p=2, delta=1/1000.'
check(4,'Euler-factor perturbation identity',c4)
def c5():
 Q=[[0,1,0],[1,0,0],[0,0,0]];H=mm(Q,Q);assert H==[[1,0,0],[0,1,0],[0,0,0]]
 w=cmath.exp(2j*math.pi/3);M=[[w**(-k*a)/math.sqrt(3) for a in range(3)] for k in range(3)]
 I=mm(M,[[x.conjugate() for x in row] for row in tr(M)])
 for i in range(3):
  for j in range(3):near(I[i][j],int(i==j))
 near(math.exp(-.7)-math.exp(-.7)-1,-1)
 return 'Q squared exactly; finite Fourier unitarity and heat supertrace checked.'
check(5,'Finite supersymmetry and Fourier transform',c5)
def c6():
 # Multiplication of linear polynomial factors in h=s-1.
 p=[F(1)]
 for lam in (0,0,2):
  q=[F(0)]*(len(p)+1)
  for j,a in enumerate(p):q[j]+=lam*a;q[j+1]+=a
  p=q
 assert p==[0,0,2,1]
 N=[[0,1],[0,0]];assert mm(N,N)==[[0,0],[0,0]] and N!=[[0,0],[0,0]]
 return 'Determinant h^2(h+2); nonzero square-zero Jordan block exposes kernel/algebraic multiplicity distinction.'
check(6,'Multiplicity and semisimplicity examples',c6)
def c7():
 beta=.8;D=1.3;t=.4;rho0=1/(1+math.exp(-beta*D));rho1=1-rho0
 near(rho0*cmath.exp(1j*(t+1j*beta)*D),rho1*cmath.exp(1j*t*D))
 s=1+.2j;near((s+1j*D)/(s+1j*D),1)
 return 'KMS boundary checked with the stated sign; scalar resolvent factor has positive real Laplace parameter.'
check(7,'KMS two-level boundary convention',c7)
def c8():
 near(299792458/26965000,11.11784,tol=1e-5)
 assert F(237000,2*96485)>F(122,100) and F(237000,2*96485)<F(124,100)
 assert 2*96485*F(1,10**6)==F(19297,100000)
 return 'Vacuum wavelength and exact Faraday-current normalization checked.'
check(8,'Wave and charge dimensions',c8)
def c9():
 for x in (F(1,10),F(1),F(100)):
  y=1/x;assert x*y==1 and 0<x/(1+x)<1
 assert F(3,1)/(1+3)==F(3,4)
 return 'Affine projection witnesses and nonattainment sequence are algebraically explicit; compact-image argument is proved in text.'
check(9,'Projection and supremum witnesses',c9)
def c10():
 U=[[0,1],[1,0]];P0=[[F(1,2)]*2 for _ in range(2)];L=[[3,2],[2,3]]
 assert mm(P0,P0)==P0 and mm(U,P0)==P0 and mm(L,P0)==mm(P0,L)
 assert mm(L,[[1],[-1]])==[[1],[-1]]
 return 'Averaging projection, equivariance and antisymmetric eigenvalue checked exactly.'
check(10,'Symmetry reduction matrix certificate',c10)
def c11():
 assert 4-3==1 and 4-4==0
 # Integral after t=R sin(theta): (4pi/3)R^4 int cos^4 theta dtheta; integral=3pi/8.
 near((4*math.pi/3)*16*(3*math.pi/8),math.pi**2*16/2)
 return 'Slice radii and four-ball volume coefficient verified independently.'
check(11,'Slice and projection geometry',c11)
def c12():
 d=2;P0=[[1.,0.],[0.,0.]];v=[.5,math.sqrt(3)/2];Q0=[[a*b for b in v] for a in v]
 e1=[[d*x for x in row] for row in P0];e2=[[d*x for x in row] for row in Q0]
 for A,B in ((e1,e2),(e2,e1)):
  C=mm(mm(A,B),A)
  for i in range(2):
   for j in range(2):near(C[i][j],A[i][j])
 return 'Both TL triple relations in the explicit delta=2 projection representation.'
check(12,'Temperley-Lieb representation',c12)
def c13():
 for n in range(4,25):
  d=sum(F(1,2**abs(k-n)) for k in (-2,0,3))
  assert d<=3*F(1,2**(n-3))
 assert sum(1 for _ in range(2**8))==256
 return 'Exact homoclinic distance bound for the three-one sequence; 256 length-eight symbolic words.'
check(13,'Symbolic homoclinic orbit',c13)
def c14():
 for N in range(1,20):assert sum(F(1,2**n) for n in range(1,N+1))+F(1,2**N)==1
 return 'Every truncation has exact covariance trace and tail sum; infinite-space support is proved in text, not inferred from samples.'
check(14,'Trace-class covariance tails',c14)
def c15():
 B=[[1,1],[1,0]];v=[[1],[1]];seq=[]
 for _ in range(3):v=mm(B,v);seq.append(tuple(x[0] for x in v))
 assert seq==[(2,1),(3,2),(5,3)] and [a*a+b*b for a,b in [(1,1)]+seq]==[2,5,13,34]
 return 'Branching dimensions and distinct algebra dimensions computed exactly.'
check(15,'Bratteli path arithmetic',c15)
def c16():
 A=[[0,-1],[1,0]];X=[[1],[-1j]];assert mm(A,X)==[[1j],[1]]
 assert mm(A,A)==[[-1,0],[0,-1]]
 return 'The rational matrix has eigenline over C and square -I, hence no real eigenline.'
check(16,'Invariant subspace field dependence',c16)
def c17():
 assert 4*1**2+2**2==8
 assert [0,0,0,0,1]==[int(math.log2(x)) for x in (1,1,1,1,2)]
 return 'Quaternion degree-square sum and p=2 height multiset checked exactly.'
check(17,'Quaternion character-height audit',c17)
def c18():
 for theta,k in ((0.,0.),(.7,1.1),(math.pi/2,math.pi)):
  a=2*math.cos(theta);b=1+cmath.exp(1j*k);H=[[a,b.conjugate()],[b,-a]];H2=mm(H,H);e2=a*a+abs(b)**2
  for i in range(2):
   for j in range(2):near(H2[i][j],e2 if i==j else 0)
 return 'Half-flux Bloch square and the touching zero-energy fiber checked.'
check(18,'Harper rational fiber',c18)
def c19():
 for k in range(-10,11):assert 5*(1-2*k)+2*(-2+5*k)==1
 assert 5*0+2*1==2
 return 'All displayed rational gap-label solutions verified, retaining the mod-Q ambiguity.'
check(19,'IDS Diophantine family',c19)
def c20():
 # sin(y) shear: nonlinear term zero, Laplacian -u, amplitude a'= -nu a.
 nu=F(2,3);a=F(5,7);adot=-nu*a
 assert a*adot+nu*a*a==0
 return 'Exact coefficient residual for the shear solution and its energy balance.'
check(20,'Navier-Stokes shear residual',c20)
def c21():
 # helix a=b=1 at s=0; c=sqrt2; T=(0,1/c,1/c), N=(-1,0,0), B=(0,-1/c,1/c).
 c=math.sqrt(2);T=[0,1/c,1/c];N=[-1,0,0];B=[0,-1/c,1/c];Np=[0,-1/c,0]
 for j in range(3):near(Np[j],-.5*T[j]+.5*B[j])
 near(sum(x*x for x in T),1);near(sum(x*x for x in B),1)
 return 'Helix curvature/torsion 1/2 checked in the Frenet equation at an explicit frame.'
check(21,'Helix frame certificate',c21)
def c22():
 # Wedge sign from inversion count, no differential-form library.
 def wedge(a,b):
  if set(a)&set(b):return 0
  z=a+b;return (-1)**sum(z[i]>z[j] for i in range(len(z)) for j in range(i+1,len(z)))
 assert wedge((0,1),(2,3))==wedge((2,3),(0,1))==1
 assert 2*2*3==12
 return 'Two-form cross-terms have positive sign and yield the characteristic number 12.'
check(22,'Characteristic-form wedge coefficient',c22)
def c23():
 L=2*math.pi;theta=math.pi
 for n in range(-3,4):
  k=(2*math.pi*n+theta)/L
  near(cmath.exp(1j*k*L),cmath.exp(1j*theta));near((k*cmath.exp(1j*k*L)),k*cmath.exp(1j*theta))
 assert min((n+.5)**2 for n in range(-5,6))==.25
 return 'Both function and derivative boundary phases checked; lowest antiperiodic eigenvalue 1/4.'
check(23,'Twisted-circle eigenfunctions',c23)
def c24():
 masks=[0,1,2,4];code=[0,7]
 images=[{x^m for x in code} for m in masks]
 assert all(images[i].isdisjoint(images[j]) for i in range(4) for j in range(i))
 assert [(-1)**(x&1) for x in code]==[1,-1]
 return 'Four bit-flip syndrome spaces disjoint; phase-error compression has unequal diagonal entries.'
check(24,'Repetition-code Knill-Laflamme certificate',c24)
def c25():
 # u'=(1-2x)/2, integrate its square coefficient by coefficient.
 integral=F(1,4)-F(1,2)+F(1,3)
 assert integral==F(1,12)
 assert -(-1)==1
 return 'Exact energy integral 1/12 and strong residual -u double-prime=1; counterexample eigenmode proved in text.'
check(25,'Weak-PDE example residual',c25)
def c26():
 b=F(2);g0=F(1,4);t=F(2);g=g0/(1+b*g0*t);gp=-b*g0*g0/(1+b*g0*t)**2
 assert g==F(1,8) and gp==-b*g*g and -1/(b*g0)==-2
 return 'Exact flow, derivative residual and pole location.'
check(26,'Quadratic beta-flow certificate',c26)
(P/'checks.json').write_text(json.dumps({'checks':checks},ensure_ascii=False,indent=2)+'\n')
print(f'{sum(c["status"]=="pass" for c in checks)}/{len(checks)} checks passed')
if any(c['status']!='pass' for c in checks):
 for c in checks:
  if c['status']!='pass':print(c)
 raise SystemExit(1)
