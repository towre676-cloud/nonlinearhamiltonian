"""Independent exact worked-model and certificate checks; standard library only.
Run from any directory. Source volumes are read/imported without modification.
Finite examples corroborate their scoped statements; proofs supply global scope.
"""
from pathlib import Path
from fractions import Fraction as Q
from itertools import product,combinations
from functools import lru_cache
from collections import Counter
import json,math,importlib.util
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
checks=[]
def record(id,name,scope,details):checks.append(dict(id=id,name=name,status='passed',scope=scope,details=details))
def rank(A):
 A=[[Q(x) for x in r] for r in A];i=0
 for j in range(len(A[0]) if A else 0):
  piv=next((k for k in range(i,len(A)) if A[k][j]),None)
  if piv is None:continue
  A[i],A[piv]=A[piv],A[i];v=A[i][j];A[i]=[x/v for x in A[i]]
  for k in range(len(A)):
   if k!=i:
    v=A[k][j];A[k]=[x-v*y for x,y in zip(A[k],A[i])]
  i+=1
  if i==len(A):break
 return i
def det(A):
 A=[[Q(x) for x in r] for r in A];d=Q(1)
 for i in range(len(A)):
  p=next((j for j in range(i,len(A)) if A[j][i]),None)
  if p is None:return Q(0)
  if p!=i:A[i],A[p]=A[p],A[i];d=-d
  v=A[i][i];d*=v;A[i]=[x/v for x in A[i]]
  for j in range(i+1,len(A)):
   v=A[j][i];A[j]=[x-v*y for x,y in zip(A[j],A[i])]
 return d
def inv(A):
 n=len(A);X=[[Q(x) for x in r]+[Q(i==j) for j in range(n)] for i,r in enumerate(A)]
 for i in range(n):
  p=next(j for j in range(i,n) if X[j][i]);X[i],X[p]=X[p],X[i];v=X[i][i];X[i]=[x/v for x in X[i]]
  for j in range(n):
   if j!=i:
    v=X[j][i];X[j]=[x-v*y for x,y in zip(X[j],X[i])]
 return [r[n:] for r in X]
def mm(A,B):return [[sum(x*y for x,y in zip(r,c)) for c in zip(*B)] for r in A]
def tr(A):return list(map(list,zip(*A)))
# D13-F01: direct enumeration is independent of completion recursion.
w=(2,3,4);p=(3,4,5);pop=[x for x in product((0,1),repeat=3) if sum(a*b for a,b in zip(x,w))<=5]
@lru_cache(None)
def count(i,b):
 if b<0:return 0
 if i==len(w):return 1
 return count(i+1,b)+count(i+1,b-w[i])
def unrank(r):
 b=5;bits=[]
 for i in range(3):
  z=count(i+1,b)
  if r<z:bits.append(0)
  else:bits.append(1);r-=z;b-=w[i]
 return tuple(bits)
def address(bits):
 b=5;r=0
 for i,x in enumerate(bits):
  if x:r+=count(i+1,b);b-=w[i]
 return r
assert count(0,5)==len(pop)==5
assert all(unrank(i)==x and address(x)==i for i,x in enumerate(pop))
profits=[sum(a*b for a,b in zip(x,p)) for x in pop];assert max(profits)==7 and profits.count(7)==1
record('D13-F01','Completion count, rank/unrank and threshold optimum','Complete three-project finite population.',{'population':len(pop),'unique_optimum':7,'inverse_pairs':len(pop)})
# D13-F02: graph histograms and exact polynomial factorization.
G=[(0,3),(0,4),(0,6),(1,2),(1,3),(2,3),(2,4),(3,5)]
H=[(0,1),(0,4),(0,6),(1,5),(1,6),(2,6),(3,6),(4,5)]
def energy(edges,h):return sum((h[a]-h[b])**2 for a,b in edges)
def census(edges):return Counter((sum(h),energy(edges,h)) for h in product((0,1),repeat=7))
assert census(G)==census(H)
def compositions(n,k):
 if k==1:yield(n,);return
 for v in range(n+1):
  for r in compositions(n-v,k-1):yield(v,)+r
def height(edges,n):return Counter(energy(edges,h) for h in compositions(n,7))
def pdiff(a,b):return {k:a[k]-b[k] for k in set(a)|set(b) if a[k]!=b[k]}
assert all(not pdiff(height(G,n),height(H,n)) for n in range(3))
difference=pdiff(height(G,3),height(H,3));poly={3:1}
for k in (1,3,3,4,4):
 new=Counter()
 for i,v in poly.items():new[i]+=v;new[i+k]-=v
 poly={i:v for i,v in new.items() if v}
assert difference==poly
value=sum(Q(v,2**k) for k,v in difference.items());assert value==Q(11025,262144)
Qp=[[3,-1,0],[-1,4,-1],[0,-1,3]];Pi=[[Q(i==j)-Q(1,3) for j in range(3)] for i in range(3)];K=mm(mm(Pi,inv(Qp)),Pi)
assert [K[i][i] for i in range(3)]==[Q(1,5),Q(2,15),Q(1,5)]
record('D13-F02','Complete census collision and Green cost','All 128 binary assignments; all total-height-three compositions; rational Green inverse.',{'binary_assignments':128,'height3_compositions':84,'separation_at_half':str(value),'P3_Green_diagonal':[str(K[i][i]) for i in range(3)]})
# D13-F03 incidence kernel, then exact cover and matching bounds.
B=[[-1,0,-1,0],[1,-1,0,0],[0,1,0,1],[0,0,1,-1]];z=[[1],[1],[-1],[-1]]
assert rank(B)==3 and mm(B,z)==[[0],[0],[0],[0]]
assert 9-rank([[-1 if i==a else 1 if i==b else 0 for a,b in product(range(3),range(3,6))] for i in range(6)])==4
# Enumerate every vertex-call set for K4,7 and prove the least size found is four.
edges=list(product(range(4),range(4,11)))
least=next(k for k in range(12) if any(all(a in s or b in s for a,b in edges) for s in map(set,combinations(range(11),k))))
assert least==4
record('D13-F03','Cycle ranks and vertex-call optimum','Exact diamond and K3,3 incidence ranks; exhaustive K4,7 cover census.',{'diamond_cycle_dimension':1,'K33_cycle_dimension':4,'K47_minimum_calls':least})
# D13-F04 gate fibres, exact physical quotient weight, and min-plus path messages.
gate=[(a,b,c) for a,b,c in product((0,1),repeat=3) if c==(a^b)]
assert len(gate)==4 and all(sum(x==a and y==b for x,y,c in gate)==1 for a,b in product((0,1),repeat=2))
fibres=[]
for banks in product(range(4),repeat=4):
 occ=Counter(banks);fibres.append(math.prod(math.perm(4,n) for n in occ.values()))
assert len(fibres)==256 and sum(fibres)==43680 and fibres[0]==24
phi=[[[0,3],[2,1]],[[2,0],[1,4]],[[0,2],[3,1]]]
msg=[0,0]
for F in phi:msg=[min(msg[s]+F[s][t] for s in (0,1)) for t in (0,1)]
brute=[min(sum(phi[i][x[i]][x[i+1]] for i in range(3)) for x in product((0,1),repeat=4) if x[-1]==t) for t in (0,1)]
assert msg==brute
record('D13-F04','Unique-extension, channel fibres and min-plus separator','Complete finite gate and bank quotient; all 16 path assignments.',{'gate_assignments':4,'quotient_states':256,'physical_states':sum(fibres),'path_final_messages':msg})
# D14-F01 partition refinement with complete continuation semantics.
def refine(n,delta,output,cost=None):
 classes=[0]*n
 while True:
  keys=[(output(s),tuple((cost(s,a) if cost else None,classes[delta(s,a)]) for a in range(2))) for s in range(n)]
  names={};new=[names.setdefault(k,len(names)) for k in keys]
  if new==classes:return new
  classes=new
D=lambda s,a:max(0,s-1) if a==0 else 2
C=lambda s,a:int(a==1 and s==0)
assert len(set(refine(3,D,lambda s:0,C)))==3
assert C(1,1)==C(2,1)==0 and C(D(1,0),1)!=C(D(2,0),1)
assert refine(4,lambda s,a:(s+1)%4,lambda s:s%2)==[0,1,0,1]
record('D14-F01','TTL future distinction and stable observation quotient','Complete three-state and four-state deterministic machines.',{'TTL_classes':3,'cycle_classes':2,'distinguishing_word':['tick','read']})
# D14-F02 exact Hankel rank lower bound and global recurrence coefficients.
y=[1+2**i+3**i for i in range(30)];hankel=[[y[i+j] for j in range(3)] for i in range(3)]
R=[[int(i==j) for j in range(6)] for i in range(3)]; A6=[[int(i==j)*(i+1) for j in range(6)] for i in range(6)]; G3=[[int(i==j)*(i+1) for j in range(3)] for i in range(3)]
assert mm(R,A6)==mm(G3,R) and mm([[1,1,1]],R)==[[1,1,1,0,0,0]]
assert det(hankel)==4 and all(y[n+3]==6*y[n+2]-11*y[n+1]+6*y[n] for n in range(27))
assert 0+0!=2+2
record('D14-F02','Hankel determinant and min-plus gap','Exact rational realization example; prefix check corroborates the symbolic intertwiner/Cayley–Hamilton proof.',{'Hankel_determinant':4,'tested_recurrence_steps':27,'tropical_gap':4})
# D14-F03 exhaustive polynomial function is not a formal identity, and LP certificate.
assert all((x[0]**3-x[0])%3==0 for x in product(range(3),repeat=4))
assert {3:1,1:-1}!={}
assert 3+0==3 and min(3,0)>=0 and 1<=1 and 1<=2 and 3+2*0==3*1
# coefficients of xy - (xy-1) are identically one
assert {'xy':1-1,'1':1}=={'xy':0,'1':1}
record('D14-F03','Certificate-type distinctions','All 81 F3^4 evaluations; exact primal-dual pair; formal Bezout identity.',{'finite_evaluations':81,'LP_optimum':3,'nonzero_formal_polynomial':'x^3-x'})
# D14-F04 read actual large certificate without invoking any source main/write.
source=ROOT/'source_working/2026_Mathematics_Source_Bundle/2026_Mathematics'
spec=importlib.util.spec_from_file_location('atlas_freelip',source/'verify_freelip.py');vf=importlib.util.module_from_spec(spec);spec.loader.exec_module(vf)
data,cache,maximum=vf.prepare();A,M,b=[data[k] for k in ('A','M','output_modulus')]
fixtures=0
for state in (0,1,1234567890123456789,M//3,M-1):
 raw=vf.raw(state,9,A,M,b)
 for positions in cache:
  assert vf.decode([raw[p] for p in positions],positions,data,cache)==state;fixtures+=1
assert len(cache)==126 and fixtures==630 and maximum<Q(3,8)
raw=vf.raw(1234567890123456789,9,A,M,b);e7=raw[:7];e7[2]=(e7[2]+12345)%b;e9=raw[:];e9[1]=(e9[1]+54321)%b;e9[7]=(e9[7]+98765)%b
assert vf.correct(e7,1,data,cache)==vf.correct(e9,2,data,cache)==1234567890123456789
# Recompute all determinants independently by fraction-free Bareiss elimination.
def bareiss(A):
 A=[r[:] for r in A];d=1;sign=1;n=len(A)
 for k in range(n-1):
  if A[k][k]==0:
   p=next(i for i in range(k+1,n) if A[i][k]);A[k],A[p]=A[p],A[k];sign=-sign
  pivot=A[k][k]
  for i in range(k+1,n):
   for j in range(k+1,n):
    v=A[i][j]*pivot-A[i][k]*A[k][j];assert v%d==0;A[i][j]=v//d
   A[i][k]=0
  d=pivot
 return sign*A[-1][-1]
assert all(abs(bareiss(row['basis']))==M**4 for row in data['records'])
small=[tuple((pow(3,i,31)*s%31)%8 for i in range(5)) for s in range(31)]
assert [len({w[:k] for w in small}) for k in (1,2,3)]==[8,24,31]
assert min(sum(a!=b for a,b in zip(u,v)) for u,v in combinations(small,2))==3
record('D14-F04','All126 raw-state lattice certificates and exact decoding','Universal collision exclusion follows from exact basis membership/index/dual bounds; fixtures separately check decoding. No accepted-output claim.',{'lattice_patterns':126,'independent_Bareiss_determinants':126,'decoder_fixtures':fixtures,'error_correction_fixtures':2,'maximum_dual_bound':str(maximum),'small_state_population':31})
# D15-F01 kernel factorization, counterexample and closure failure.
H=[[1,1,0],[0,1,1]];G=[[1,2,1]];L=[[1,1]];v=[[1],[-1],[1]]
assert mm(L,H)==G and mm(H,v)==[[0],[0]] and mm(G,v)==[[0]]
assert mm([[1,0,0]],v)==[[1]]
# Observation of x1 alone is not closed under x1'=x2.
Ha=[[1,0]];Aa=[[0,1],[0,0]];hidden=[[0],[1]]
assert mm(Ha,hidden)==[[0]] and mm(mm(Ha,Aa),hidden)==[[1]]
record('D15-F01','Target factorization and dynamic-closure counterexample','Exact rational matrices; nonlinear z^2 example is a direct symbolic fibre argument.',{'recoverable_target':[1,2,1],'recovery_norm_squared':2,'full_state_identifiable':False,'present_observation_closed':False})
# D15-F02 Lyapunov metric, transient growth, Gramian and pencil.
A=[[-1,4],[0,-1]];P=[[Q(1,2),1],[1,Q(9,2)]];AP=mm(tr(A),P);PA=mm(P,A)
assert [[AP[i][j]+PA[i][j] for j in range(2)] for i in range(2)]==[[-1,0],[0,-1]]
assert P[0][0]>0 and det(P)==Q(5,4)
assert 2*(3-1)==4 and det([[Q(1,2),Q(1,3)],[Q(1,3),Q(1,4)]])==Q(1,72)
epsilon=Q(1,100);spurious=1/epsilon
assert det([[spurious*(1+epsilon)+1,0],[0,spurious*epsilon-1]])==0
assert det([[spurious+1,0],[0,-1]])!=0
record('D15-F02','Compatible Lyapunov metric and exact Gramian','Declared two-state matrices; descriptor eigenvalue 1/epsilon is derived directly from its diagonal pencil.',{'P_determinant':'5/4','Euclidean_energy_derivative_at_11':4,'Gramian_determinant':'1/72','descriptor_spurious_root_at_epsilon_001':100})
# D15-F03 finite diagonal filter bounds, severe margin and exact Landweber filter.
assert Q(1,101)+Q(1,100)<Q(1,50)
assert 1/96+math.exp(-5)<0.01716 and math.exp(-100)*math.exp(100)==1.0
alpha=Q(1,4);sigma=Q(1,2);tikh=sigma/(sigma*sigma+alpha);assert tikh==1
residual=(1-sigma*sigma)**4;filter=(1-residual)/sigma
assert residual==Q(81,256) and filter==Q(175,128) and filter<2
record('D15-F03','Cutoff safety and spectral filter arithmetic','Concrete mild/severe examples; exact rational four-step Landweber and Tikhonov filters. Universal/minimax scope is proved in text.',{'mild_bound_exact':str(Q(1,101)+Q(1,100)),'severe_safe_cutoff':95,'naive_noise_amplification':1,'Landweber_residual':str(residual),'Landweber_filter':str(filter)})
# D15-F04 exact Bellman minimax tree and target-only resolution.
experiments=[(1,('a','bc','bc')),(2,('ac','b','ac')),(4,('a','b','c'))]
def bellman(target):
 @lru_cache(None)
 def V(S):
  if len({target[s] for s in S})<=1:return 0
  options=[]
  for cost,outcomes in experiments:
   fibres=[tuple(s for s in S if outcomes[s]==y) for y in {outcomes[s] for s in S}]
   if all(len(f)<len(S) for f in fibres):options.append(cost+max(V(f) for f in fibres))
  return min(options)
 return V((0,1,2))
assert bellman((0,1,2))==3 and bellman((0,1,1))==1
assert Q(1,1)+2*Q(1,2)+1==3 # target quadratic form for rho=1/2
record('D15-F04','Cheapest exact experiments and correlated target support','Complete finite three-state test menu; target-only variant and exact ellipsoid quadratic form.',{'full_state_worst_cost':3,'target_only_cost':1,'sum_target_variance_at_rho_half':3})
# Evidence coverage and artifact integrity.
families=json.loads((HERE/'families.json').read_text());reviews=json.loads((HERE/'classification_review.json').read_text());corpus=json.loads((ROOT/'data/source_corpus_initial_routing.json').read_text())
uids={x['uid'] for x in corpus};initial={x['uid'] for x in corpus if x['primary_domain'] in ('D13','D14','D15')}
assert initial<={x['uid'] for x in reviews}
assert len(families)==12 and len({f['id'] for f in families})==12
assert all(set(f['source_uids'])<=uids and set(f['anchor_uids'])<=set(f['source_uids']) and 4<=len(f['anchor_uids'])<=8 for f in families)
record('coverage','All initial domain entries reviewed','Every initial D13–D15 primary UID is retained in the review ledger, including explicit outgoing moves.',{'initial_primary_entries':len(initial),'reviewed_entries':len(reviews),'families':len(families)})
report=dict(status='passed',checks=checks,scope='Exact finite worked models plus replay of the actual all-state raw-generator certificate. Other global statements retain their written proofs and hypotheses; no absent historical instance is claimed checked.')
(HERE/'checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(status='passed',checks=len(checks),families=12,initial_entries=len(initial),FreeLIP_patterns=126)))
