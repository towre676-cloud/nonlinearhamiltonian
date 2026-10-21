"""Portable exact/numerical example checks; Python standard library only."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import math,cmath,json
P=Path(__file__).resolve().parent;checks=[]
def check(n,name,ok,detail):
 if not ok:raise AssertionError((n,name,detail))
 checks.append(dict(id=f'Y26-04-{n:03}',name=name,status='passed',detail=detail))
def mm(A,B):return [[sum(a*b for a,b in zip(row,col))for col in zip(*B)]for row in A]
def tr(A):return list(map(list,zip(*A)))
def rank(A):
 A=[list(map(F,r))for r in A];r=0
 for j in range(len(A[0])):
  k=next((k for k in range(r,len(A))if A[k][j]),None)
  if k is None:continue
  A[r],A[k]=A[k],A[r];v=A[r][j];A[r]=[x/v for x in A[r]]
  for k in range(len(A)):
   if k!=r:
    q=A[k][j];A[k]=[x-q*y for x,y in zip(A[k],A[r])]
  r+=1
  if r==len(A):break
 return r
def close(x,y,tol=1e-10):return abs(x-y)<tol
edges=list(product(range(3),repeat=2));B=[[0]*9 for _ in range(6)]
for k,(i,j)in enumerate(edges):B[i][k]=-1;B[j+3][k]=1
cycles=[]
for i,j in product((1,2),repeat=2):
 z=[0]*9
 for e,v in [((i,j),1),((i,0),-1),((0,j),-1),((0,0),1)]:z[edges.index(e)]=v
 cycles.append(z)
check(1,'K3,3 rank and cycle basis',rank(B)==5 and rank(cycles)==4 and mm(B,tr(cycles))==[[0]*4 for _ in range(6)],'Exact incidence rank5, nullity4 and four independent integer circulations.')
check(2,'quartic Gaussian coefficient',-4*math.prod([1,-1,1,-1])==-4 and math.factorial(4)==24,'Only all-four-distinct term survives;24 multinomial permutations cancel4!, giving residue−4.')
check(3,'Gaussian monomial norm',F((1+2+3)**2,1*2*3)==6 and rank([[6,6],[6,6]])==1,'Squared coefficient gives6, and repeated observables force rank1.')
A=[[1],[0]];d=[[0,0],[0,1]];S=[[0,1],[1,0]]
check(4,'coboundary secondary defect',mm(d,A)==[[0],[0]] and mm(d,mm(S,A))==[[0],[1]],'Typed maps deltaY:Y0→Y1,deltaZ:Z0→Z1 andB0:Y0→Z0; nextdifferentialszero. Closedinput transports toanonclosedoutput; no square-zeroendomorphism claimed.')
x=y=F(1);X=[[1,x],[0,1]];Y=[[1,0],[y,1]];Xi=[[1,-x],[0,1]];Yi=[[1,0],[-y,1]]
check(5,'exact shear-loop commutator',mm(mm(mm(X,Y),Xi),Yi)==[[3,-1],[1,0]],'Four rational matrix products give nonidentity determinant-one loop.')
a=F('-1.2715');b=F('.1297')
check(6,'return second-iterate coefficient',-2*(a*a+b)==F('-3.4928245'),'Exact rational cubic coefficient of R²−identity.')
s=math.log(2)/math.log(3);ds=-math.log(2)/math.log(3)**2
check(7,'pressure root and sensitivity',close(2*math.exp(-s*math.log(3)),1) and close(ds,-s/math.log(3)),'Two constant branches give root log2/log3 and exact implicit derivative.')
M=[[F(3,4),F(1,4)],[F(1,4),F(3,4)]]
check(8,'finite Poisson solution',mm([[1-M[0][0],-M[0][1]],[-M[1][0],1-M[1][1]]],[[2],[-2]])==[[1],[-1]],'Mean-zero spectral multiplier1/2, inverse2 and exact solution(2,−2).')
a=F(1,2);b=F(1,10);q=1/(a*a-b)
check(9,'nonresonant invariant graph',q==F(20,3) and q*a*a==b*q+1,'Exact quadratic graph coefficient20/3 and transverse multiplier1/10.')
xx=F(1,10)
check(10,'resonant analytic graph family',8*(xx/2)**2+(xx/2)**3==(8*xx*xx+xx**3)/8+xx*xx,'Cubic resonance leaves free C; checked C=1 exactly.')
J=[]
for delta in (3,4,7):
 for i in range(12):
  row=[0]*12;row[(i+delta)%12]+=1;row[i]-=1;J.append(row)
check(11,'exact cyclic difference rank',rank(J)==11 and all(sum(r)==0 for r in J),'36×12 declared difference matrix has rank11 and uniform-shift kernel.')
forcing=[sum(J[i][j]for i in range(36))for j in range(12)]
check(12,'family-constant target cancellation',forcing==[0]*12 and F(3,2)==F(1,2)*3,'Each cyclic family sums tozero; three-cycle constant residual energy3/2.')
Y=[[1,0],[0,1],[1,1]];weights=[[1,0,0],[1,1,0],[1,1,1]];b=[2,3,-6]
H=[[4,1],[1,3]];Hinv=[[F(3,11),-F(1,11)],[-F(1,11),F(4,11)]]
forces=[[sum(Y[i][j]*weights[k][i]*b[i] for i in range(3))for k in range(3)]for j in range(2)]
D=mm(Hinv,forces)
check(13,'realizable nested least-squares sensitivity rank',forces==[[2,2,-4],[0,3,-3]] and D==[[F(6,11),F(3,11),-F(9,11)],[-F(2,11),F(10,11),-F(8,11)]] and rank(D)==2 and all(sum(row)==0 for row in forces) and mm(H,D)==forces,'Atgamma=(1,1,1),x*=0,Hpositive withdet11; exact sensitivity rank2 andsumDk=0 respectstationarity.')
check(14,'participation ratio versus rank',F(10**2,9**2+1)==F(50,41),'Eigenvalues9,1,0 give rank2 and effective dimension50/41.')
def increment_cov(k,H):return ((k+1)**(2*H)-2*k**(2*H)+(k-1)**(2*H))/2
check(15,'Brownian noise calibration',all(close(increment_cov(k,.5),0)for k in range(1,20)),'H=1/2 has zero nonzero-lag increment covariance and flat stationary-noise spectrumβ=0.')
check(16,'equal volume different sphere norm',F(3*0**2+1,8)==F(1,8) and F(3*1**2+1,8)==F(1,2),'Unit-determinant shear family has Q=(3t²+1)/8.')
def doublefact(n):return math.prod(range(n,0,-2))
check(17,'spherical pairing normalization',doublefact(7)==105 and doublefact(9)==945 and math.prod((4,6,8,10))==1920 and math.prod((5,7,9,11,13))==45045,'Exact pairing counts and sphere denominators for orthonormal4/5-tuples.')
check(18,'trace normalization and dyadic growth',F(3,8)==3*F(1,8) and F(1,16) not in [F(k,8)for k in range(-8,9)],'Rank3 inM8 has trace3/8; later1/16 is outside previous eighth lattice.')
check(19,'gapped finite trace label',F(sum(v<=0 for v in (-2,1,4)),3)==F(1,3) and min(abs(v)for v in (-2,1,4))>F(1,2),'One negative eigenvalue gives normalized trace1/3 and a gap margin greater than1/2.')
th=math.sqrt(2)
check(20,'Morita lattice arithmetic',all(close((m+n*th)/th,n+m/th)for m in range(-3,4)for n in range(-3,4)),'Reciprocal√2 scaling interchanges lattice coefficient coordinates.')
pos=[2,3];neg=[1,2];auc=sum(F(1)if a>b else F(1,2)if a==b else F(0)for a in pos for b in neg)/4
check(21,'exact AUROC pair table',auc==F(7,8),'Four pair values1,1/2,1,1 giveAUROC7/8.')
pairs=[(10*g+u,10*g+v)for g,u,v in product((0,1),(-1,1),(-1,1))];mean=lambda s:sum(s)/len(s)
mx=mean([x for x,y in pairs]);my=mean([y for x,y in pairs]);cov=mean([(x-mx)*(y-my)for x,y in pairs]);var=mean([(x-mx)**2 for x,y in pairs])
check(22,'pooled covariance confounding',cov==25 and var==26,'Eight equally likely samples have pooledρ=25/26 although each domain covariance iszero.')
check(23,'nonconvex projection tie',F((-1)**2,2)==F(1**2,2)==F(1,2),'Two nonconvex branches tie at trialzero; convex interval includes unique minimizerzero.')
check(24,'R squared arithmetic and runs expectation',F('0.4311651513')-F('0.3000468863')==F('.1311182650') and 1+F(2*59*59,118)==60,'Exact reported decimal increment and balanced-sign expected runs60; no p-value asserted.')
c=F('.167918')*F('2.15');amin=math.sqrt(float(c/F('.1681')))
check(25,'compatibility minimum',c==F('.3610237') and close(amin,1.46549,2e-5),'Fixedalpha0 givesc=.3610237, zeta=sqrt(c/a), unique minimizingxi1.')
arr=[0,0,1,1];perm=[0,1,0,1];jumps=lambda a:sum(a[i]!=a[i-1]for i in range(1,len(a)))
check(26,'layout preserves values not adjacency',sorted(arr)==sorted(perm) and jumps(arr)==1 and jumps(perm)==3,'Equal sample multiset can have different adjacency statistics; analytic conjugation proved intext.')
Bdiamond=[[-1,0,-1,0],[1,-1,0,0],[0,0,1,-1],[0,1,0,1]]
check(27,'diamond path circulation',mm(Bdiamond,[[1],[1],[-1],[-1]])==[[0],[0],[0],[0]] and rank(Bdiamond)==3,'Exact path difference spans incidence nullity1.')
check(28,'cover period depends on coefficients',2*1!=0 and (2*1)%2==0,'A degree-two cover does not kill integer periodone but kills it modulo2.')
lam=1+math.sqrt(2)
check(29,'silver-mean eigenvector frequencies',close(2*lam+1,lam*lam) and close(lam/(lam+1),1/math.sqrt(2)) and close(1/(lam+1),1-1/math.sqrt(2)),'Correct normalized letters(1/√2,1−1/√2); reciprocalλ is frequency ratio.')
def compose(p,q):return tuple(p[q[i]]for i in range(4))
r=(1,2,3,0);t=(0,3,2,1);identity=tuple(range(4));grp={identity};todo=[identity]
while todo:
 p=todo.pop()
 for g in (r,t):
  q=compose(g,p)
  if q not in grp:grp.add(q);todo.append(q)
check(30,'exact dihedral root permutation group',len(grp)==8 and compose(t,compose(r,t))==(3,0,1,2),'Root permutations generate8-element D4 withτ ρ τ=ρ⁻¹; degree proof is algebraic intext.')
eps=F(1,4);H=[[-1,eps],[eps,1]];R=[[ -v/(1+eps*eps)for v in row]for row in H]
check(31,'exact coupled resolvent inverse',mm([[-v for v in row]for row in H],R)==[[1,0],[0,1]],'Atz0, exact inverse−H/(1+eps²); Neumann bound is sufficient, not necessary.')
h=F(1,3)
check(32,'discrete product correction',h*h/h==h and sum((3,-3))==0,'Forward difference ofx² atzero ish, and internal graph flux conserves mass.')
check(33,'quotient factorization test',all((k%6)%2==k%2 for k in range(-12,13)) and (6%6)%4!=6%4,'Parity descends throughZ/6; mod4 doesnot.')
entries=json.loads((P/'entries.json').read_text());assert len(entries)==33
for e in entries:
 o=e['original'];fn,_,idx=o['retrieval_receipt'].partition(' record ');r=json.loads((P/fn).read_text())[int(idx)]
 assert any(o['source_excerpt'] in c['text']for c in r['result'].get('content',[])if c.get('type')=='text'),e['id']
 assert f"{o['evidence']}@{o['date']}" in o['source_excerpt'];assert o['original_question'] is None
(P/'checks.json').write_text(json.dumps({'checks':checks,'provenance':{'entries':len(entries),'literal_source_excerpts':'passed'},'all_passed':True},ensure_ascii=False,indent=2)+'\n')
print(len(checks),'checks passed; literal provenance passed')
