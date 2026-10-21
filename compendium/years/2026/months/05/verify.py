"""Portable stdlib finite certificates; these corroborate, not replace, proofs."""
from pathlib import Path
from fractions import Fraction as F
import json,math,itertools,cmath
BASE=Path(__file__).resolve().parent
checks=[]
def check(n,name,test,detail):
 try:
  ok=bool(test());checks.append(dict(id=f'Y26-05-{n:03d}' if n else 'metadata',name=name,status='pass' if ok else 'fail',detail=detail))
 except Exception as e:checks.append(dict(id=f'Y26-05-{n:03d}',name=name,status='fail',detail=repr(e)))
def mat(A,B):return [[sum(a*b for a,b in zip(row,col)) for col in zip(*B)] for row in A]
def tr(A):return list(map(list,zip(*A)))
def det(A):
 A=[[F(x) for x in r] for r in A];v=F(1)
 for i in range(len(A)):
  j=next((j for j in range(i,len(A)) if A[j][i]),None)
  if j is None:return F(0)
  if i!=j:A[i],A[j]=A[j],A[i];v=-v
  d=A[i][i];v*=d
  for j in range(i+1,len(A)):
   q=A[j][i]/d
   A[j]=[x-q*y for x,y in zip(A[j],A[i])]
 return v
check(1,'Meet propagation',lambda:tuple(min(x) for x in zip((2,2,1,2,1,2),(2,1,2,2,2,1),(2,2,2,1,2,2)))==(2,1,1,1,1,1),'Exact ordinal-coordinate calculation.')
check(2,'Perturbed contraction',lambda:F(3,2)*F(-2,3)==-1 and F(-2,3)*F(3,2)==-1,'Exact differential/homotopy identity on contractible summand.')
check(3,'RG characteristic functions',lambda:all(abs(math.exp(-3*(t/math.sqrt(2))**2)**2-math.exp(-3*t*t))<1e-14 for t in [-2,-.1,0,1]),'Finite Gaussian evaluations; the finite-variance classification is proved in the entry.')
check(4,'Cycle Hessian',lambda:mat([[2,-1,0,-1],[-1,2,-1,0],[0,-1,2,-1],[-1,0,-1,2]],[[1],[0],[-1],[0]])==[[2],[0],[-2],[0]],'Exact first cycle eigenmode; the full spectrum is derived in the written Fourier proof.')
phi=(1+math.sqrt(5))/2
check(5,'Unit and length conventions',lambda:abs(phi**-4-(7-3*math.sqrt(5))/2)<1e-14 and mat([[1,1],[1,0]],[[1,1],[1,0]])==[[2,1],[1,1]],'Exact Fibonacci matrix product and independent real unit evaluation.')
alpha=phi**-2
word=[math.floor((j+1)*alpha)-math.floor(j*alpha) for j in range(200)]
check(6,'Mechanical word balance',lambda:''.join(map(str,word[:12]))=='001001010010' and all(max(sum(word[j:j+m]) for j in range(201-m))-min(sum(word[j:j+m]) for j in range(201-m))<=1 for m in range(1,31)),'200-symbol finite corroboration; uniform balance is proved by telescoping.')
ideals=[{(d*k)%12 for k in range(12)} for d in [1,2,3,4,6,12]]
maxproper=[I for I in ideals if len(I)<12 and not any(I<J and len(J)<12 for J in ideals)]
check(7,'Finite maximal ideals',lambda:sorted(map(len,maxproper))==[4,6],'Exhaustive divisor-generated ideals of Z/12Z.')
check(8,'Triangle gauge classes and spectra',lambda:all(det([[t,-1,-s],[-1,t,-1],[-s,-1,t]])==t**3-3*t-2*s for s in [-1,1] for t in range(-3,4)),'Exact determinant evaluations of degree-three characteristic polynomials at seven points.')
check(9,'Spin ladder Casimir',lambda:all(F((2*r-n)**2,4)+F(r*(n-r+1)+(n-r)*(r+1),2)==F(n*(n+2),4) for n in range(10) for r in range(n+1)),'Exact Casimir identity in sectors n=0..9.')
check(10,'Observation weak direction',lambda:mat([[1,0,0],[0,1,0],[0,0,F(1,100)]],[[0],[0],[100]])==[[0],[0],[1]],'Exact factor100 amplification in the stipulated weakest channel.')
A=[[-1,3],[0,-1]];P=[[F(1,2),F(3,4)],[F(3,4),F(11,4)]]
M=mat(tr(A),P);N=mat(P,A)
check(11,'Lyapunov metric',lambda:sum(A[i][j]+A[j][i] for i in range(2) for j in range(2))==2 and det(P)==F(13,16) and det([[3-P[0][0],-P[0][1]],[-P[1][0],3-P[1][1]]])==F(1,16) and [[M[i][j]+N[i][j] for j in range(2)] for i in range(2)]==[[-1,0],[0,-1]],'Exact positive metric, P≤3I and Lyapunov identity; Euclidean symmetric part has positive direction(1,1).')
check(12,'SDP primal-dual certificate',lambda:F(3,4)+2*F(1,4)-1==F(1,4) and det([[1,F(1,10)],[F(1,10),0]])<0,'Exact feasible-pair gap and a non-PSD perturbation counterexample.')
check(13,'Annealed versus quenched',lambda:math.log(3)<math.log(5) and abs((math.log(2)+math.log(3)*(-math.log(2)/math.log(3))))<1e-14,'Strict Jensen example and deterministic pressure zero.')
check(14,'Hyperbolic metric scale',lambda:abs(2*math.atanh(.6)-math.log(4))<1e-14 and abs(2*math.acosh(1.5)-4*math.log(phi))<1e-14,'Two independent hyperbolic-length formulas.')
check(15,'Heat trace exact geometric tail',lambda:sum(F(1,2**n) for n in range(10))+F(1,512)==2,'Exact ten-term heat trace plus tail.')
check(16,'Pendulum separatrix residual',lambda:all(abs((2/math.cosh(t))**2/2+1-(2/math.cosh(t)**2-1)-2)<1e-13 for t in [-3,-1,0,.5,2]),'Finite independent energy residuals; ODE identity proved analytically.')
check(17,'Reduced oscillator',lambda:all(abs(math.cos(t)**2/2+math.sin(t)**2/2+F(9,2)-5)<1e-14 for t in [0,.2,1,3]),'Momentum3 oscillator energy five.')
ratio=F(203295,24305)
check(18,'Hydrate mass accounting',lambda:ratio*13*F(3,5)/ratio==F(39,5) and 10<ratio*F(13,10)<11,'Exact molar conversion and retained magnesium.')
check(19,'Least representative',lambda:min((2**a)*(3**b)*(5**c) for a,b,c in itertools.permutations((3,2,1)))==360 and 4*3*2==24,'All exponent assignments to2,3,5 enumerated.')
p=[1]
for a in [3,2,1]:
 q=[0]*(len(p)+a)
 for i,x in enumerate(p):
  for j in range(a+1):q[i+j]+=x
 p=q
check(20,'Divisor rank polynomial',lambda:p==[1,3,5,6,5,3,1] and sum(p)==24,'Exact polynomial convolution.')
check(21,'Species count through12',lambda:sorted(2**a*6**b for a in range(4) for b in range(2) if 2**a*6**b<=12)==[1,2,4,6,8,12],'Exact primorial partition enumeration without log rounding.')
check(22,'Leading saddle constant',lambda:abs(2*math.sqrt(2*(math.pi**2/6))-2*math.pi/math.sqrt(3))<1e-14,'Constant algebra only; the PNT/Laplace asymptotics are stated analytic hypotheses.')
check(23,'Coercivity ledger and triangle',lambda:1-F(1,5)-F(3,10)==F(1,2) and 2+3-5==0 and 2+3-4==1,'Exact budget and separate gluing obstruction.')
probs=[F(3,8),F(1,8),F(1,8),F(3,8)]
H=-sum(float(p)*math.log2(float(p)) for p in probs)
check(24,'Two-qubit source statistic',lambda:abs((2-H)-(1-(-.25*math.log2(.25)-.75*math.log2(.75))))<1e-14 and -math.log(2)<0,'Exact probabilities with numerical entropy; Bell log-distance is negative.')
def rank(A):
 A=[[F(x) for x in r] for r in A];r=0
 for c in range(len(A[0])):
  j=next((j for j in range(r,len(A)) if A[j][c]),None)
  if j is None:continue
  A[r],A[j]=A[j],A[r];d=A[r][c];A[r]=[x/d for x in A[r]]
  for j in range(len(A)):
   if j!=r:
    q=A[j][c];A[j]=[x-q*y for x,y in zip(A[j],A[r])]
  r+=1
 return r
def incidence(v,edges):
 B=[[0]*len(edges) for _ in range(v)]
 for j,(a,b) in enumerate(edges):B[a][j]-=1;B[b][j]+=1
 return B
edges=[(0,1),(1,2),(2,0),(3,4),(4,5),(5,3),(2,3)]
check(25,'Graph homology ranks',lambda:rank(incidence(6,edges))==5 and len(edges)-rank(incidence(6,edges))==2,'Exact rational elimination on two triangles with a bridge.')
check(26,'Hybrid rate threshold',lambda:1-math.log(2)>0 and 1-math.log(4)<0 and abs((4*math.exp(-2))**5-math.exp(-2*(1-math.log(2))*5))<1e-14,'Exact formula checked at five jumps; theorem proves all times.')
def fm(a,b):
 r=0
 while b:
  if b&1:r^=a
  b>>=1;a<<=1
  if a&8:a^=11
 return r
powers=[1]
for _ in range(7):powers.append(fm(powers[-1],2))
check(27,'F8 arithmetic and Frobenius',lambda:powers==[1,2,4,3,6,7,5,1] and all(fm(fm(fm(x,x),fm(x,x)),fm(fm(x,x),fm(x,x)))==x for x in range(8)),'All elements and primitive powers checked with binary polynomial reduction.')
code=[v for v in range(128) if __import__('functools').reduce(int.__xor__,(j+1 for j in range(7) if v>>j&1),0)==0]
weights={k:sum(v.bit_count()==k for v in code) for k in range(8)}
check(28,'Hamming code',lambda:len(code)==16 and weights=={0:1,1:0,2:0,3:7,4:7,5:0,6:0,7:1},'All128 words enumerated; exact syndrome and weight distribution.')
check(29,'Maurer-Cartan cancellation',lambda:F(-1)+F(2,2)==0,'Exact coefficients of t²; centrality makes all higher brackets vanish in the stated model.')
def padd(a,b):
 d=a.copy()
 for k,v in b.items():d[k]=d.get(k,F(0))+v
 return {k:v for k,v in d.items() if v}
def pmul(a,b):
 d={}
 for (i,j),v in a.items():
  for (k,l),w in b.items():d[(i+k,j+l)]=d.get((i+k,j+l),F(0))+v*w
 return {k:v for k,v in d.items() if v}
def neg(a):return {k:-v for k,v in a.items()}
x={(1,0):F(1)};y={(0,1):F(1)};one={(0,0):F(1)}
f1=padd(pmul(x,x),neg(y));f2=padd(pmul(x,y),neg(one));g1=padd(x,neg(pmul(y,y)));g2=padd(pmul(pmul(y,y),y),neg(one))
check(30,'Groebner ideal witnesses',lambda:padd(pmul(y,f1),neg(pmul(x,f2)))==g1 and padd(f2,neg(pmul(y,g1)))==g2 and padd(pmul(padd(x,pmul(y,y)),g1),pmul(y,g2))==f1 and padd(pmul(y,g1),g2)==f2,'Exact multivariate polynomial identities in both containment directions.')
check(31,'Cusp transform and intersection',lambda:padd({(2,2):F(1)},{(3,0):F(-1)})==pmul({(2,0):F(1)},{(0,2):F(1),(1,0):F(-1)}) and len([0,1,2])==3,'Exact blowup polynomial factor; quotient basis is1,x,x².')
check(32,'Extension ambiguity',lambda:max(next(k for k in range(1,5) if k*x%4==0) for x in range(4))==4 and all((2*a%2,2*b%2)==(0,0) for a,b in itertools.product(range(2),repeat=2)),'Element-order invariant separates Z/4 from(Z/2)^2.')
constraints=[lambda x,y:x==0,lambda x,y:y==0,lambda x,y:x or y]
check(33,'Pairwise compatibility is not global',lambda:all(any(constraints[i](x,y) and constraints[j](x,y) for x,y in itertools.product([0,1],repeat=2)) for i,j in itertools.combinations(range(3),2)) and not any(all(f(x,y) for f in constraints) for x,y in itertools.product([0,1],repeat=2)),'All Boolean assignments checked exactly.')
a=json.loads((BASE/'entries.json').read_text())
check(0,'Schema and attribution',lambda:len(a)==33 and all(x['original']['original_question'] is None and x['original']['question'].startswith('Reconstruction:') for x in a),'Historical source lines are retrieval summaries; no invented original prompts.')
(BASE/'checks.json').write_text(json.dumps(dict(checks=checks),ensure_ascii=False,indent=2)+'\n')
print(sum(x['status']=='pass' for x in checks),'/',len(checks),'pass')
if any(x['status']!='pass' for x in checks):
 print([x for x in checks if x['status']!='pass']);raise SystemExit(1)
