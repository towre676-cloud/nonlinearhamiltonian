"""Finite corroboration only. General mathematical claims are proved in entries."""
from pathlib import Path
from fractions import Fraction as F
import json,math,cmath,itertools
BASE=Path(__file__).resolve().parent
checks=[]
def check(n,name,test,detail):
 try:ok=bool(test());checks.append(dict(id=f'Y26-06-{n:03d}' if n else 'metadata',name=name,status='pass' if ok else 'fail',detail=detail))
 except Exception as e:checks.append(dict(id=f'Y26-06-{n:03d}',name=name,status='fail',detail=repr(e)))
def mm(A,B):return [[sum(a*b for a,b in zip(row,col)) for col in zip(*B)] for row in A]
def mt(A):return list(map(list,zip(*A)))
def err(A,B):return max(abs(x-y) for a,b in zip(A,B) for x,y in zip(a,b))
def eye(n):return [[int(i==j) for j in range(n)] for i in range(n)]
def det(A):
 A=[[F(x) for x in r] for r in A];v=F(1)
 for i in range(len(A)):
  j=next((j for j in range(i,len(A)) if A[j][i]),None)
  if j is None:return F(0)
  if i!=j:A[i],A[j]=A[j],A[i];v=-v
  d=A[i][i];v*=d
  for j in range(i+1,len(A)):
   q=A[j][i]/d;A[j]=[x-q*y for x,y in zip(A[j],A[i])]
 return v
q=cmath.exp(2j*math.pi/3);U=[[q**i if i==j else 0 for j in range(3)] for i in range(3)];V=[[int(i==(j+1)%3) for j in range(3)] for i in range(3)]
check(1,'Finite Weyl relation',lambda:err(mm(U,V),[[q*x for x in r] for r in mm(V,U)])<1e-14,'Three-dimensional clock/shift checked entrywise; determinant theorem proves obstruction.')
check(2,'Quadratic polarization',lambda:all(F(((x+y)%3)**2-x*x-y*y,3)%1==F(2*x*y,3)%1 for x,y in itertools.product(range(3),repeat=2)) and F(2,3)%1!=0,'All nine cyclic polarization values, including failure of alternation.')
S=[[cmath.exp(-2j*math.pi*2*x*y/3)/math.sqrt(3) for y in range(3)] for x in range(3)];T=[[q**(x*x) if x==y else 0 for y in range(3)] for x in range(3)];C=[[int(y==(-x)%3) for y in range(3)] for x in range(3)]
ST=mm(S,T)
check(3,'Finite Weil phase',lambda:err(mm(S,S),C)<1e-14 and err(mm(mm(ST,ST),ST),[[1j*x for x in r] for r in C])<1e-14,'Complete3×3 matrices, tolerance1e−14; finite-sum derivation is the proof.')
check(4,'CRT projectors and split idempotent',lambda:92*92%161==92 and 70*70%161==70 and 92*70%161==0 and (92+70)%161==1 and mm([[1,1],[0,0]],[[1,1],[0,0]])==[[1,1],[0,0]],'Exact residue and matrix identities.')
H=[[1,2],[2,-1]]
check(5,'LCU normalization',lambda:mm(H,H)==[[5,0],[0,5]] and F(5,9)<1,'Exact H²=5I gives input-independent success5/9.')
K=[[[1,0],[0,0]],[[0,1],[0,0]]]
check(6,'Composed instrument completeness',lambda:[[sum(mm(mt(k),k)[i][j] for k in K) for j in range(2)] for i in range(2)]==eye(2),'Both outcome branches included in exact Kraus sum.')
check(7,'Sector dependence and confidence',lambda:F(1,10)+F(1,10)-F(1,100)==F(19,100) and .0295<1-(1/20)**.01<.0296,'Exact union independence case and zero-failure100-trial bound.')
B=[[F(1,5),F(1,10)],[F(1,4),F(1,4)]]
check(8,'Weighted path majorant',lambda:max(map(sum,B))==F(1,2) and mm(mm([[1,0]],B),B)==[[F(13,200),F(9,200)]] and F(1,2)**4/(1-F(1,2))==F(1,8),'Exact two-step path weights and geometric tail; total11/100.')
check(9,'Cubic arithmetic',lambda:all(x**3-x+1!=0 for x in [-1,1]) and -4*(-1)**3-27==-23 and F(-4,3)**3-F(-4,3)+1==F(-1,27),'Rational-root exclusion, discriminant and real-root bracket.')
# Polynomial substitution identity: z³ f((z−1)/z) = z³−2z²+3z−1.
check(10,'Corner birational identity',lambda:all((z-1)**3-(z-1)*z*z+z**3==z**3-2*z*z+3*z-1 for z in range(-8,9)),'Degree-three identity checked at17 exact integer points; correct mapu=(z−1)/z.')
N=100000
cl=sum(math.sin(n*math.pi/3)/(n*n) for n in range(1,N+1))
check(11,'Regular-shape dilogarithm',lambda:abs(2*cl-2.029883212819307)<2/N,'100000-term absolutely convergent sum; certified truncation2/N.')
check(12,'Logarithmic period',lambda:abs(sum((1j*cmath.exp(2j*math.pi*k/64)/cmath.exp(2j*math.pi*k/64))*(2*math.pi/64) for k in range(64))-2j*math.pi)<1e-13,'Unit-circle integrand constanti; finite quadrature matches exact analytic period.')
t=F(1,4)
check(13,'Fold action difference',lambda:F(1,12)-F(-1,12)==F(1,6) and F(4,3)*F(1,8)==F(1,6),'Exact saddle values att=1/4.')
Bl=[[2,1],[0,1]];Un=[[1,1],[0,1]]
check(14,'Lattice covolume and minima',lambda:det(Bl)==2 and det(mm(Bl,Un))==2 and min(x*x+y*y for x,y in itertools.product(range(-3,4),repeat=2) if (x or y) and (x-y)%2==0)==2,'Exact covolume and exhaustive short-vector search in a containing box.')
poly=[(0,0),(1,0),(2,1),(2,2),(1,2),(0,1)]
area=F(abs(sum(poly[i][0]*poly[(i+1)%6][1]-poly[(i+1)%6][0]*poly[i][1] for i in range(6))),2)
check(15,'Zonotope area',lambda:area==3 and sum(abs(a*d-b*c) for (a,b),(c,d) in itertools.combinations([(1,0),(0,1),(1,1)],2))==3,'Independent polygon shoelace and determinant-sum calculations.')
f=[1,0,0,-1,-1];df=[4,0,0,-1]
Syl=[]
for i in range(3):Syl.append([0]*i+f+[0]*(2-i))
for i in range(4):Syl.append([0]*i+df+[0]*(3-i))
# polynomial arithmetic modulo2
pmod=lambda a:None
check(16,'Quartic Sylvester discriminant',lambda:det(Syl)==-283 and 256*(-1)**3-27*(-1)**4==-283,'Independent exact7×7 determinant and depressed-quartic formula.')
check(17,'Anharmonic units',lambda:abs(phi:=((1+math.sqrt(5))/2))>1 and abs(phi**2*(1-phi)**2-1)<1e-14,'Golden exceptional-unit relation; general positive-exponent proof uses coprime ideals.')
def fall(n,k):
 if k>n:return 0
 return math.factorial(n)//math.factorial(n-k)
def sk(a,b,c,d,k):return sum((-1)**r*math.comb(k,r)*fall(a,k-r)*fall(b,r)*fall(c,r)*fall(d,k-r) for r in range(k+1))
check(18,'Moyal defect coefficients',lambda:sk(3,0,0,3,3)==36 and F(-sk(5,0,0,5,3),24)==-150 and F(sk(5,0,0,5,5),1920)==F(15,2),'Exact falling-factorial coefficients under declared ℏ convention.')
check(19,'Corrected infinite-family samples',lambda:all(sk(1,3,3*r+2,r,3)==0 and sk(1,3,3*r+2,r,5)==0 for r in range(1,51)),'50exact samples; uniform proof comes from degree≤4and factorization.')
check(20,'Genuine fifth-order obstruction',lambda:sk(1,5,5,3,3)==0 and sk(1,5,5,3,5)==201600 and F(201600,1920)==105,'Corrected new replacement example; Moyal value83 atq=p=ℏ=1.')
check(21,'Gas-stream mass and covariance',lambda:F(150)*F(3,1000)*F(3,5)*F(9,5)*24==F(1458,125) and F(120)*F(6,1000)*F(3,5)*F(9,5)*2==F(972,625) and F(150)*F(5,1000)*F(9,5)*2==F(27,10),'Exact unit-converted throughput and separate-average counterexample.')
check(22,'Sine transform and dimension',lambda:all(err(mm([[math.sqrt(2/L)*math.sin(math.pi*r*s/L) for s in range(1,L)] for r in range(1,L)],[[math.sqrt(2/L)*math.sin(math.pi*r*s/L) for s in range(1,L)] for r in range(1,L)]),eye(L-1))<2e-14 for L in [3,5,7,11]),'Full matrices at four conductors; sine-sum argument proves allL.')
check(23,'Sign-action cohomology',lambda:{(-2*m)%2 for m in range(-10,11)}=={0} and {x%2 for x in range(-10,11)}=={0,1},'Exact cocycle/coboundary parity classes; infinite quotient computed in proof.')
def phi(n):return sum(math.gcd(n,k)==1 for k in range(1,n+1))
check(24,'Totient convolution',lambda:all(sum(phi(d) for d in range(1,n+1) if n%d==0)==n for n in range(1,101)),'All divisor-sum identities through100; analytic series argument proves full half-plane.')
A=[[2,1,1],[1,1,0],[1,0,1]]
check(25,'Habiro free-direction spectrum',lambda:mm(A,[[-1],[1],[1]])==[[0],[0],[0]] and mm(A,[[0],[1],[-1]])==[[0],[1],[-1]] and mm(A,[[2],[1],[1]])==[[6],[3],[3]] and det(A)==0,'Three exact orthogonal eigenvectors, eigenvalues0,1,3.')
check(26,'Projection cycle count',lambda:F(1,4)**3>F(1,100) and F(1,4)**4<F(1,100) and F(3,4)**16>F(1,100) and F(3,4)**17<F(1,100),'Exact iteration counts:θπ/3 needs4;θπ/6 needs17,not20.')
def c(S):return S|({'b'} if 'a'in S else set())
def d(S):return S|({'c'} if 'b'in S else set())
check(27,'Ordered closure iteration',lambda:c(d({'a'}))=={'a','b'} and c(d(c(d({'a'}))))=={'a','b','c'} and d(c({'a'}))=={'a','b','c'},'Exact finite noncommuting closures.')
check(28,'Compression arithmetic',lambda:191821-187496==4325 and 187496-183184==4312 and 183184-150517==32667 and 2**2<5<=2**3,'Exact source byte gaps and five-symbol lower bound.')
def actA(s):r=s.copy();r['x']=r['y']+1;return r
def actB(s):r=s.copy();r['z']=2*r['w'];return r
def badB(s):r=s.copy();r['y']=0;return r
states=[dict(zip('xyzw',a)) for a in itertools.product(range(3),repeat=4)]
check(29,'Footprint commutation',lambda:all(actA(actB(s))==actB(actA(s)) for s in states) and any(actA(badB(s))!=badB(actA(s)) for s in states),'All81states for sufficient condition and read-write counterexample.')
check(30,'Tangram area and orientation',lambda:2*F(1,4)+F(1,8)+2*F(1,16)+2*F(1,8)==1 and det([[1,1],[0,1]])==1 and det([[1,1],[0,-1]])==-1,'Exact area conservation and labeled orientation reversal.')
check(31,'Projective symplectic group order',lambda:5**4*(5**2-1)*(5**4-1)//2==4680000,'Exact symplectic-basis counting formula; braid-image identification not verified.')

def fmul(a,b):
 c=[0]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):c[i+j]+=x*y
 f=[-1,-2,2,3,-2]
 for k in range(len(c)-1,4,-1):
  z=c[k]
  for j in range(5):c[k-5+j]-=z*f[j]
 return c[:5]
h=[5,68,49,-29,21];iv=[-1379,1939,-2235,2484,464]
cols=[fmul(h,[0]*i+[1]) for i in range(5)]
check(32,'Quintic Hessian inverse',lambda:fmul(h,iv)==[39681,0,0,0,0] and det([[cols[j][i] for j in range(5)] for i in range(5)])==39681,'Independent exact reduced multiplication and5×5 norm determinant.')

a=json.loads((BASE/'entries.json').read_text())
check(0,'Attribution and IDs',lambda:len(a)==32 and all(x['original']['original_question'] is None and x['original']['question'].startswith('Reconstruction:') for x in a),'No invented literal historical prompt; Tfile evidence may have null dates.')
(BASE/'checks.json').write_text(json.dumps(dict(checks=checks),ensure_ascii=False,indent=2)+'\n')
print(sum(x['status']=='pass' for x in checks),'/',len(checks),'pass')
if any(x['status']!='pass' for x in checks):print([x for x in checks if x['status']!='pass']);raise SystemExit(1)
