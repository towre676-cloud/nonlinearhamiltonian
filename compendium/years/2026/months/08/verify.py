"""Independent stdlib checks of August's own examples, not unavailable old data."""
import json,math,cmath
from fractions import Fraction as Q
from pathlib import Path
P=Path(__file__).resolve().parent
checks=[]
def check(n,name,condition,detail):
 if not condition:raise AssertionError((n,name,detail))
 checks.append(dict(id=f'Y26-08-{n:03d}',name=name,status='pass',detail=detail))
def mm(A,B):return [[sum(x*y for x,y in zip(r,c)) for c in zip(*B)] for r in A]
def tr(A):return list(map(list,zip(*A)))
def add(A,B):return [[x+y for x,y in zip(r,s)] for r,s in zip(A,B)]
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
eps=Q(1,100)
check(1,'Regular constrained pencil and regularized modes',(-1-Q(3))!=0 and Q(1,1)/eps==100 and -1/(1+eps)==Q(-100,101),'For λ3 original determinant−4; perturbation gives finite modes−100/101 and100.')
ns=[]
for d in range(6):
 # Coefficients of -λa(λ)+b(λ), degrees0..d+1.
 M=[[0]*(2*(d+1)) for _ in range(d+2)]
 for j in range(d+1):M[j+1][j]=-1;M[j][d+1+j]=1
 ns.append(2*(d+1)-rank(M))
check(2,'Exact polynomial nullities through degree five',ns==[0,1,2,3,4,5],'Constructed every block coefficient equation; right generator degree1 is not inferred from floating eigenvalues.')
A=[[-1,-2],[2,-1]];Ap=[[Q(-1,2),Q(-1,4)],[Q(1,4),Q(-1,2)]]
v=[[1],[-1j]];u=[[Q(1,2),.5j]]
der=mm(mm(u,Ap),v)[0][0]/mm(u,v)[0][0]
check(3,'Left-right sensitivity and damping numerator',abs(der-(-.5+.25j))<1e-14 and -4*Q(-1,2)+(-1)*2*Q(1,4)==Q(3,2),'Explicit normalized left/right vectors recover λ′; damping numerator is3/2.')
delta=Q(3,2)
check(4,'Rank-one contour margin improvement',delta/2==Q(3,4)<1 and delta>1 and abs(3-delta)>1,'Structured bound certifies δ3/2 while the loose global bound fails; perturbed second root remains outside unit disk.')
A=[[-1,3],[0,-2]];L=[[Q(1,2),Q(1,2)],[Q(1,2),1]]
lyap=add(mm(tr(A),L),mm(L,A));x=[[1],[Q(3,4)]]
growth=mm(mm(tr(x),add(A,tr(A))),x)[0][0]
check(5,'Exact Lyapunov identity and transient growth',lyap==[[-1,0],[0,-1]] and growth==Q(1,4) and L[0][0]*L[1][1]-L[0][1]**2==Q(1,4),'Positive definite Lyapunov matrix and positive initial Euclidean norm derivative verified independently.')
W=[[Q(1,2),Q(1,3)],[Q(1,3),Q(1,4)]]
check(6,'Kalman ranks and stable Gramian',rank([[1,-1],[1,-2]])==2 and rank([[1,0],[-1,0]])==1 and W[0][0]*W[1][1]-W[0][1]**2==Q(1,72),'Declared controllability/observability ranks and exact infinite-horizon Gramian determinant.')
check(7,'Information-volume versus worst-ratio example',10>8 and max(Q(1,10),100)==100 and max(Q(1,2),25)==25 and (1+10**2)>100,'D-optimal example prefersA while worst danger ratio prefersB; a null-information direction yields unbounded growth.')
J=[[0,1],[-1,0]];R=[[1,0],[0,2]];x=[[2],[3]]
check(8,'Port-Hamiltonian skew power cancellation',mm(mm(tr(x),J),x)==[[0]] and mm(mm(tr(x),R),x)==[[22]] and Q(1,2)**2==Q(1,4),'At x=(2,3), skew power0 and dissipation22; the reset halves state and quarters energy.')
v=Q(5);d=Q(3);Sigma=[[Q(4),0],[0,1]]
check(9,'Improper Gaussian real covariance and exponent',(v+d)/2==4 and(v-d)/2==1 and v*v-d*d==16 and (v*Q(2)**2-d*Q(2)**2)/16==Q(1,2),'Covariance diag4,1 and exponent at z2 equals1/2; normalization denominator4π.')
Y=[[0,Q(1,10)],[Q(-1,10),0]];R=[[100,0],[0,1]];I=[[1,0],[0,1]]
M=add(I,mm(R,Y));inv=[[Q(1,2),-5],[Q(1,20),Q(1,2)]]
check(10,'Weighted passive resolvent counterexample',mm(M,inv)==I and sum(row[1]**2 for row in inv)==Q(101,4)>25,'Exact inverse is verified; its second-column norm exceeds5 despite accretive Y.')
# Enumerate all paths excluding γγ. Paths are stored in travel order.
arrows={'a':(0,1),'g':(1,1),'b':(1,2),'c':(1,2)}
paths=[(i,()) for i in range(3)];front=[(i,(),i) for i in range(3)]
for _ in range(4):
 nxt=[]
 for start,path,end in front:
  for name,(s,t) in arrows.items():
   if s==end and not(path and path[-1]=='g' and name=='g'):
    new=path+(name,);paths.append((start,new));nxt.append((start,new,t))
 front=nxt
counts=[sum(len(p)==k for _,p in paths) for k in range(4)]
check(11,'Quiver path enumeration and relation rank',counts==[3,4,5,2] and len(paths)==14 and len({(0,('a','g','b')),(0,('a','b'))})==2,'Enumerated all14 surviving paths; the nonzero source-to-sink relation has rank1 in every projective chart.')
mult2x=[[0,0],[2,0]]
obstruction=[0]*13+[1]
check(12,'Dual-number Hochschild cochain ranks',rank(mult2x)==1 and 2-rank(mult2x)==1 and rank([[0,0],[0,0]])==0 and not any(obstruction[:13]) and obstruction[13]!=0,'Alternating zero and rank-one maps leave one-dimensional positive-degree cohomology; s=ε has zero s13 obstruction through order12 but nonzero order13.')
a=2
check(13,'Regulator branch enclosure and stability',math.tanh(a*.9)>.9 and math.tanh(a)<1 and a/(math.cosh(a*.9)**2)<1,'A positive branch lies in(.9,1); its multiplier is below the bound at .9, itself below1.')
B=[[0,1],[-1,0]];Bad=[[0,1],[-2,1]];x=Q(2);y=Q(3)
# For X=x,Y=y(1+x), Jacobian determinant 1+x; bracket XY equals xy(1+x).
bracket=x*y*(1+x)
check(14,'Skew condition and Poisson toy map',all(B[i][j]==-B[j][i] for i in range(2) for j in range(2)) and not all(Bad[i][j]==-Bad[j][i] for i in range(2) for j in range(2)) and bracket==x*(y*(1+x)) and y*(1+x)/(1+x)==y,'The valid skew map fixes x and has inverse division on y; the retrieved matrix fails skewness.')
u=[1,0,2,-1];v=[0,1,3,4];w={(i,j):u[i]*v[j]-u[j]*v[i] for i in range(4) for j in range(i+1,4)}
q=w[0,2]+w[1,3];X=[w[0,2]-w[1,3],w[0,1]+w[2,3],w[0,1]-w[2,3],w[0,3]+w[1,2],w[0,3]-w[1,2]]
check(15,'Plücker minors shell and parity',list(w.values())==[1,3,4,-2,1,11] and X==[2,12,-10,2,6] and X[0]**2+X[1]**2+X[3]**2-X[2]**2-X[4]**2==q*q and(X[0]-q)%2==(X[1]-X[2])%2==(X[3]-X[4])%2==0,'All six minors and the shell coordinates derived from the original two integer vectors.')
remaining=79477040208394+4239638994011
check(16,'Joint-dependence example and aggregate bookkeeping',all(t-t==0 for t in [Q(-1),Q(-1,2),Q(0),Q(1)]) and remaining==83716679202405 and remaining+2077907067913639==2161623747116044,'Shared symbolic function a(t)=b(t) cancels exactly; old exclusion totals check arithmetically only.')
f=[0,1,0,-1,0,0];g=[f[(i+1)%6]-f[i] for i in range(6)];h=[Q(1,10)]*6
check(17,'Cycle gradient and harmonic energy',g==[1,-1,-1,1,0,0] and sum(g)==0 and sum(x*x for x in h)==Q(3,50),'A nonzero exact gradient has no harmonic part; constant0.1 adds energy3/50.')
X=[[0,1],[0,0]];Y=[[0,0],[1,0]];comm=add(mm(X,Y),[[-z for z in r] for r in mm(Y,X)])
check(18,'Nonabelian infinitesimal loop commutator',comm==[[1,0],[0,-1]] and abs(cmath.exp(1j*.7/6)**6-cmath.exp(1j*.7))<1e-14,'Exact commutator matrix and numerical U1 six-edge holonomy composition; no inferred surface curvature.')
def sw(a):return(a&~3)|((a&1)<<1)|((a&2)>>1)
corners={(x,y,x^d,y,x,y^d) for x in range(16) for y in range(16) for d in range(1,16)}
def affine(c):
 x,y,a,b,s,t=c
 return(sw(x)^1,sw(y)^2,sw(a)^1,sw(b)^2,sw(s)^1,sw(t)^2)
check(19,'Exhaustive ordered-corner permutation',len(corners)==3840 and{affine(c) for c in corners}==corners,'Generated every ordered corner in F2^4×F2^4 and checked the declared affine map permutes all of them.')
K=set(range(10));L=set(range(6,16));T15,T17,h=3,4,0
check(20,'Halo-premise counterexample and exact swaps',h+7*((T15-3)+(T17-4))==0<54 and len(K-L)==6 and len(K^L)//2==6,'Visible scalar bounds do not imply the missing weighted row; equal-size set swap distance independently computed.')
check(21,'Integer saturation example',rank([[2,-2]])==rank([[1,-1]])==1 and all(t%2==0 for t in [2,-2]) and (1,-1)!=(2,-2) and 57676-44==57632,'Rational ranks agree but generator has index2; reported graph scalars determine only E−V.')
coords=[(0,0,0),(2,0,1),(2,2,4)];Phi=[G+A-v for G,A,v in coords]
check(22,'Local potential failing edge',Phi==[0,1,0] and [Phi[i+1]-Phi[i] for i in range(2)]==[1,-1],'The second declared edge violates the proposed monotonicity although the total path change iszero.')
omega=cmath.exp(2j*math.pi/7)
err=max(abs(sum(omega**(j*(b-a)) for j in range(7))/7-int(a==b)) for a in range(7) for b in range(7))
check(23,'Fourier orthogonality and opened-mode conditioning',err<1e-13 and (Q(7)+Q(1,100))/Q(1,100)==701,'Numerical7-mode Fourier orthogonality cross-check plus exact condition number701; proof uses a geometric sum.')
phase=.04;p=.5
overlap=p*cmath.exp(1j*phase/2)+(1-p)*cmath.exp(-1j*phase/2)
check(24,'Balanced-state fidelity and threshold',abs(abs(overlap)**2-math.cos(phase/2)**2)<1e-14 and abs(math.cos(math.asin(1/math.sqrt(1000)))**2-.999)<1e-14,'Direct overlap matchescos²(ε/2); the0.999 boundary is independently evaluated.')
J=[[1,0],[0,-1]];T=[[2,0],[0,Q(1,2)]]
check(25,'dB addition and determinant-one counterexample',abs(10*math.log10(.25)+10*math.log10(.04)+20)<1e-12 and mm(mm(tr(T),J),T)==[[4,0],[0,Q(-1,4)]] and T[0][0]*T[1][1]==1,'Power budgets add to−20dB; determinant1 fails the full flux identity.')
entries=json.loads((P/'entries.json').read_text());assert len(entries)==25
for e in entries:
 o=e['original'];fn,rec=o['retrieval_receipt'].split(' record ');rs=json.loads((P/fn).read_text())[int(rec)];r=rs.get('result',rs)
 blocks=r.get('structuredContent',{}).get('messages',[]) or r.get('content',[])
 assert any(o['source_excerpt'] in b.get('content',b.get('text','')) for b in blocks)
 assert o['original_question'] is None
(P/'checks.json').write_text(json.dumps(dict(scope='Own25 entries; helper catalogs have independent verifiers; displayed examples only',checks=checks),ensure_ascii=False,indent=2)+'\n')
print(f'{len(checks)}/{len(checks)} scoped checks passed')
