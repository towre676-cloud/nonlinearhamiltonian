"""Portable exact checks for the displayed July examples; not a proof of old datasets."""
import json, math
from fractions import Fraction as Q
from pathlib import Path
P=Path(__file__).resolve().parent
checks=[]
def check(n,name,condition,detail):
 if not condition: raise AssertionError((n,name,detail))
 checks.append(dict(id=f'Y26-07-{n:03d}',name=name,status='pass',detail=detail))
def mm(A,B):return [[sum(a*b for a,b in zip(r,c)) for c in zip(*B)] for r in A]
def tr(A):return list(map(list,zip(*A)))
def rank(A):
 A=[[Q(x) for x in r] for r in A];i=0
 if not A:return 0
 for j in range(len(A[0])):
  k=next((k for k in range(i,len(A)) if A[k][j]),None)
  if k is None:continue
  A[i],A[k]=A[k],A[i];a=A[i][j];A[i]=[x/a for x in A[i]]
  for k in range(len(A)):
   if k!=i:
    a=A[k][j];A[k]=[x-a*y for x,y in zip(A[k],A[i])]
  i+=1
  if i==len(A):break
 return i
def mul(a,b):
 c=[Q(0)]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):c[i+j]+=x*y
 return c
def val(a,x):
 y=Q(0)
 for c in reversed(a):y=y*x+c
 return y
S=[0,1,2,4,5,6,8];project=[]
for l in S:
 e=[Q(1)]
 for v in S:
  if v!=l:e=[x/Q(l-v) for x in mul(e,[-v,1])]
 project.append([val(e,v) for v in S])
check(1,'Rational Lagrange spectral projectors',project==[[int(i==j) for j in range(7)] for i in range(7)],'Evaluated every exact projector polynomial on every declared eigenvalue.')
mons=[(a,b) for a in range(6) for b in range(6) if not(a>=2 or(a>=1 and b>=1)or b>=3)]
check(2,'Cubic closure standard monomials',mons==[(0,0),(0,1),(0,2),(1,0)],'Exact monomial divisibility; without v³ all powers of v survive.')
# Sparse bivariate polynomial operations for the Hilbert–Burch columns.
def pm(a,b):
 c={}
 for (i,j),x in a.items():
  for (k,l),y in b.items():c[i+k,j+l]=c.get((i+k,j+l),0)+x*y
 return {m:c for m,c in c.items() if c}
def ps(*polys):
 c={}
 for p in polys:
  for m,x in p.items():c[m]=c.get(m,0)+x
 return {m:x for m,x in c.items() if x}
gens=[{(2,0):1},{(1,1):1},{(0,3):1}]
cols=[[{(0,1):1},{(1,0):-1},{}],[{},{(0,2):1},{(1,0):-1}]]
check(3,'Hilbert–Burch syzygies and socle',all(not ps(*(pm(g,h) for g,h in zip(gens,c))) for c in cols) and all((a+1,b)not in mons and(a,b+1)not in mons for a,b in [(1,0),(0,2)]),'Both displayed columns annihilate(x²,xy,y³); x and y² are killed by the maximal ideal.')
check(4,'Tensor resolution Betti convolution',mul([1,3,2],[1,1])==[1,4,5,2] and mul([1,2,1],[1,1])==[1,3,3,1],'Resolution ranks and quotient Hilbert series independently convolved.')
p,q=32003,40009;N=p*q
check(5,'Two-prime nonzero integer counterexample',N==1280408027 and N%p==N%q==0 and N!=0,'A nonzero rational matrix entry can vanish at both selected primes.')
def omega(v,w):return sum(v[i]*w[i+2]+v[i+2]*w[i] for i in range(2))%2
V=[tuple((j>>i)&1 for i in range(4)) for j in range(16)]
Z1=(0,0,1,0);Z2=(0,0,0,1);X1=(1,0,0,0);X2=(0,1,0,0)
cz=[v for v in V if all(omega(v,s)==0 for s in [Z1,Z2])]
czx=[v for v in V if all(omega(v,s)==0 for s in [Z1,Z2,X1,X2])]
check(6,'Exhaustive two-qubit Pauli centralizers',len(cz)==4 and len(czx)==1,'Enumerated all16 binary Pauli labels: centralizer dimensions2 and0.')
G=[(0,0,a,b) for a in range(2) for b in range(2)]
check(7,'Sector-kernel counterexample',all(omega(v,Z1)==0 for v in G) and len(G)==4,'G has dimension2 but its action on the Z1 character is trivial, contradicting the naive kernel G∩Q rule.')
check(8,'Schmidt block rank and one-sided failure',rank([[int(i==j) for j in range(5)] for i in range(5)])==5 and rank([[1,0],[1,0]])==1,'Two-sided orthogonal blocks3+2 have rank5; one-sided stacking of equal rows has rank1.')
a,b,c=-1,0,1;disc=a*a*b*b-4*b*b*b-4*a*a*a*c-27*c*c+18*a*b*c
check(9,'Cubic discriminant and modular factor patterns',disc==-23 and not any((t**3-t*t+1)%2==0 for t in range(2)) and [t for t in range(5) if(t*t+t+2)%5==0]==[],'Discriminant−23; irreducible mod2; the residual quadratic mod5 is irreducible.')
eta=[1]+[0]*30
for k in range(1,31):
 for j in range(30,k-1,-1):eta[j]-=eta[j-k]
for k in range(23,31,23):
 for j in range(30,k-1,-1):eta[j]-=eta[j-k]
check(10,'Eta-product initial coefficients',[0]+eta[:8]==[0,1,-1,-1,0,0,1,0,1],'Exact truncated product, shifted by its initial q factor; no modularity claim tested numerically.')
A=[[int(i!=j and {i,j} not in [{0,1},{2,3}]) for j in range(5)] for i in range(5)]
A2=mm(A,A);A3=mm(A2,A)
check(11,'Graph edge and triangle counts',sum(A2[i][i] for i in range(5))==16 and sum(A3[i][i] for i in range(5))==24 and rank(A)==3,'Constructed K5 minus a matching; traces give8 edges and4 triangles, rank3 gives two zero eigenvalues.')
check(12,'Finite-cover degree example',Q(9,4)*4==9,'Only the displayed degree4/degree9 volume-ratio arithmetic is replayed; existence of a common cover is an explicit hypothesis.')
g=[Q((-1)**k,2*math.factorial(k)) for k in range(11)]
check(13,'Green-kernel local equation and derivative jump',all((k+2)*(k+1)*g[k+2]==g[k] for k in range(9)) and -Q(1,2)-Q(1,2)==-1,'The positive-half Taylor coefficients satisfy G″=G and the two one-sided derivatives jump by−1.')
check(14,'Half-spin and root counts',sum(math.comb(8,k) for k in range(0,9,2))==128 and math.comb(16,2)+128==248 and 2*8*7+128==240,'Exterior even-degree dimension, so16 dimension and D8+spin weight counts.')
check(15,'Variable-coefficient product-rule example',val([1,0],Q(2))==1 and val([1,-2],Q(2))==-3,'For x=l,y=3l+7, fixed q2 gives derivative1; q=2+l gives1−2l, checked at l2.')
z=1j;M=-1/z+2*z/(4-z*z)
check(16,'Finite Herglotz example',abs(M-1.4j)<1e-14 and Q(4,3)*3==4,'At z=i the imaginary part is7/5; the real zero equation is3x²−4=0. No old137-atom dataset tested.')
T=Q(551,4)
check(17,'Monotone-phase model counts',sum(0<k<=T for k in range(200))==137 and sum(0<Q(2*k+1,2)<=T for k in range(200))==138,'Exact positive integer and half-integer counts through137.75.')
r1,r2=Q(1,40),Q(1,4)
check(18,'Anisotropic box budget',10*r1+r2==Q(1,2) and 2*10*r1==Q(1,2) and 2*r2==Q(1,2),'Equalized coordinate error shares for the declared two-dimensional volume optimum.')
alpha=Q(1,10);mu=(1+alpha*alpha)/(2*alpha)
check(19,'Critical-point normal-form example',alpha*mu==Q(101,200),'For F=1−x², B=2αx and αμ=(1+α²)/2 exactly; limit1/2 follows algebraically.')
pad=mul([0,0,0,1],[-1,0,1]);eps=Q(1,10**8);pert=mul(mul([0,1],[-1,0,1]),[eps,0,1])
check(20,'Padded moment polynomial perturbation',pad==[0,0,0,-1,0,1] and pert==[0,-eps,0,eps-1,0,1] and Q(1,10**4)**2==eps,'Coefficient perturbation ε opens an imaginary pair at magnitude√ε.')
check(21,'Unimodular Smith witness',mm(mm([[1,0],[3,-1]],[[2,4],[6,8]]),[[1,-2],[0,1]])==[[2,0],[0,4]],'Exact integer matrix multiplication certifies the displayed Smith diagonal2,4.')
def sheaf(rs):
 m=len(rs);D=[[Q(0)]*m for _ in range(m)]
 for j,r in enumerate(rs):D[j][j]=-r;D[j][(j+1)%m]+=1
 return D
check(22,'Twisted-cycle cohomology ranks',rank(sheaf([Q(2),Q(3),Q(1,6)]))==2 and rank(sheaf([2,3,1]))==3,'Holonomy1 gives kernel/cokernel dimension1; holonomy6 gives both zero.')
check(23,'Signed total-complex matrix product',mm([[-1,1]],[[1],[1]])==[[0]] and rank([[1],[1]])==rank([[-1,1]])==1,'The1→2→1 total complex squares tozero and is acyclic; unsigned product would be2.')
v=[2,-1];M=[[1,2,3],[4,5,6]];w=[[1],[2],[3]]
check(24,'Currying example by both contractions',mm(mm([v],M),w)==[[-4]] and mm([v],M)==[[-2,-1,0]],'The tensor bilinear map and curried functional give the same exact value.')
def plus(Pt,Qt):
 if Pt is None:return Qt
 if Qt is None:return Pt
 x,y=Pt;u,v=Qt
 if x==u and y+v==-1:return None
 l=(3*x*x-1)/(2*y+1) if Pt==Qt else(v-y)/(u-x)
 X=l*l-x-u;Y=-y-1+l*(x-X)
 return X,Y
Pt=(Q(0),Q(0));Qp=None;got=[]
for j in range(6):Qp=plus(Qp,Pt);got.append(Qp)
want=[(0,0),(1,0),(-1,-1),(2,-3),(Q(1,4),Q(-5,8)),(6,14)]
orders=[1+sum((y*y+y-x*x*x+x)%p==0 for x in range(p) for y in range(p)) for p in [3,5]]
check(25,'Elliptic multiples and reduction counts',got==want and orders==[7,8] and all(y*y+y==x*x*x-x for x,y in got),'Exact rational group law through6P and full enumeration over F3,F5.')
check(26,'Conditional code parameters and field model',39+1-3==37 and 91-39==52 and(52-1)//2==25 and all((a*a+1)%7 for a in range(7)),'Riemann–Roch example arithmetic and irreducibility of u²+1 overF7; no original curve certified.')
check(27,'Base-twelve rational identities',12**3+2*12**2+10==2026 and Q(1,12)+Q(6,144)==Q(1,8) and Q(2*12**3+4*12**2+9*12+7,12**4-1)==Q(1,5),'Integer place values and both finite/repeating fractional representations checked exactly.')
check(28,'Rouché margins and Graeffe coefficients',4>2 and 27>13 and mul([2,1],[2,1])==[4,4,1] and [4,4-9,1]==[4,-5,1],'Dominant coefficient inequalities and root-squared polynomial y²−5y+4.')
c,C,r=Q(7,5),Q(5,14),Q(1,50);q=Q(1,70)
check(29,'Exact contraction box for sqrt2',max(abs(1-C*2*x) for x in[c-r,c+r])==q and abs(C*(c*c-2))+q*r==Q(51,3500)<r,'Both derivative and self-mapping bounds verified with rational arithmetic.')
entries=json.loads((P/'entries.json').read_text())
check(30,'Tetrahedral angular-defect count',3*4==2*6 and 4*Q(1)==2*(4-6+4),'Angles are measured in π units; four defectsπ sum to2πχ withχ2.')
residues=[1,16,16,516]
check(31,'Exact Hensel lifts of sqrt6 at5',all((r*r-6)%(5**n)==0 for n,r in enumerate(residues,1)) and all(residues[n]%5**n==residues[n-1] for n in range(1,4)),'Residues checked modulo5,25,125,625 and compatibility checked at every lift.')
assert len(entries)==31 and len({e['id'] for e in entries})==31
for e in entries:
 o=e['original'];fn,rec=o['retrieval_receipt'].split(' record ');rs=json.loads((P/fn).read_text())[int(rec)];assert o['source_excerpt'] in json.dumps(rs,ensure_ascii=False).replace('\\n','\n') or any(o['source_excerpt'] in m.get('content',m.get('text','')) for m in rs.get('result',rs).get('structuredContent',{}).get('messages',[]) or rs.get('result',rs).get('content',[]))
(P/'checks.json').write_text(json.dumps(dict(scope='Exact displayed examples and provenance only; not unavailable historical computations',checks=checks),ensure_ascii=False,indent=2)+'\n')
print(f'{len(checks)}/{len(checks)} scoped checks passed')
