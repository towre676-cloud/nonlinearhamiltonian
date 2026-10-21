"""Independent portable checks for six August handoff developments."""
from pathlib import Path
from fractions import Fraction as F
from itertools import permutations,product
from collections import Counter
import math,json
P=Path(__file__).resolve().parent;checks=[]
def check(i,name,ok,detail):
 if not ok:raise AssertionError((i,name,detail))
 checks.append(dict(id=f'Y26-08-{i}',name=name,status='passed',detail=detail))
def mm(A,B):return [[sum(a*b for a,b in zip(row,col))for col in zip(*B)]for row in A]
def dot(a,b):return sum(x*y for x,y in zip(a,b))
check(801,'feasible optimum monotonicity',min([12,9,10])==9 and min([12])==12 and 10-9==1,'Exact finite cost set gives improved optimum9 and search regret1.')
check(801,'separated observation error',abs(F('10.4')-9)<=1+F('.5'),'Triangle error bound1.4≤1.5; distinct from certifying physical calibration.')
R=[[F(3,5),-F(4,5)],[F(4,5),F(3,5)]];A=[[2,-3],[3,2]]
check(802,'rotation commutant',mm(A,R)==mm(R,A),'Exact rational rotation and nontrivial aI+bJ commutant.')
q=[F(2),F(-1)];k=[F(3),F(4)];Q=[2*x for x in q];K=[x/2 for x in k]
check(802,'exact QK score gauge',dot(Q,K)==dot(q,k) and dot(Q,[sum(R[i][j]*K[j]for j in range(2))for i in range(2)])==dot(q,[sum(R[i][j]*k[j]for j in range(2))for i in range(2)]),'A=2I preserves both plain and RoPE scores exactly.')
B=[[F(2),0],[0,F(3)]];Bi=[[F(1,2),0],[0,F(1,3)]];O=[[1,2],[3,4]];v=[[5],[7]]
check(802,'exact VO gauge',mm(mm(O,Bi),mm(B,v))==mm(O,v),'Output matrix and value basis changes cancel by rational multiplication.')
silu=lambda x:x/(1+math.exp(-x))
g=[.2,-.7];u=[.8,1.2];D=[[1.,2.],[-1.,3.]];lam=[2.,-1.]
z=[silu(g[i])*u[i]for i in range(2)];z2=[silu(g[i])*lam[i]*u[i]for i in range(2)]
out=mm(D,[[z[0]],[z[1]]]);out2=mm([[D[i][j]/lam[j]for j in range(2)]for i in range(2)],[[z2[0]],[z2[1]]])
check(802,'SwiGLU linear-branch scaling',all(abs(out[i][0]-out2[i][0])<1e-14 for i in range(2)),'Nonzero diagonal scaling oflinear branch cancels inoutput; gate scaling is not assumed.')
blocks={frozenset((0,1)),frozenset((2,3))};pres=[p for p in permutations(range(4))if {frozenset((p[0],p[1])),frozenset((p[2],p[3]))}==blocks]
check(802,'GQA wreath count',len(pres)==8,'All24 permutations enumerated; exactly8 preserve two sharing groups ofsize2.')
costs={'a':(0,10),'b':(10,0),'c':(0,10)}
check(803,'future equivalence versus scalar minimum',costs['a']==costs['c'] and min(costs['a'])==min(costs['b']) and costs['a'][0]!=costs['b'][0],'a,c merge; b has same minimum but differs under actionL restriction.')
coarse=[{'a','b','c'}];fine=[{'a','c'},{'b'}]
check(803,'partition direction',len(fine)>=len(coarse) and all(any(s<=t for t in coarse)for s in fine),'A refinement has at least asmany blocks onthe same state set.')
physical=Counter(tuple(c//4 for c in channels)for channels in permutations(range(16),4))
def falling(n,k):return math.prod(range(n-k+1,n+1))
def fiber(t):return math.prod(falling(4,t.count(b))for b in range(4))
check(804,'complete physical-to-bank fiber enumeration',len(physical)==256 and sum(physical.values())==43680 and all(n==fiber(t)for t,n in physical.items()),'All43,680 injections enumerated; every one of256 banktuples appears withthe exact fiber formula.')
check(804,'unequal fibers and route tree bound',physical[(0,0,0,0)]==24 and physical[(0,1,2,3)]==256 and sum(4**k for k in range(5))==341,'Fiber sizes24 and256; full four-ary depth-four tree341.')
inf=math.inf;M=[[inf,2],[3,inf]];I=[[0,inf],[inf,0]]
def trop(A,B):return [[min(A[i][k]+B[k][j]for k in range(len(B)))for j in range(len(B[0]))]for i in range(len(A))]
powers=[I]
for _ in range(14):powers.append(trop(powers[-1],M))
check(805,'exact repeated-layer min-plus identity',all(powers[L+2]==[[x+5 for x in row]for row in powers[L]]for L in range(12)),'M²=5+I and M^(L+2)=5+M^L verified onexact integer/infinity matrices throughL13.')
# Nontrivial chain separator test: binary variables, alternating unary preferences, edge disagreement cost2.
unary=lambda i,x:0 if x==i%2 else 3
brute=min(sum(unary(i,x[i])for i in range(6))+2*sum(x[i]!=x[i-1]for i in range(1,6))for x in product(range(2),repeat=6))
v={x:unary(0,x)for x in range(2)}
for i in range(1,6):v={x:unary(i,x)+min(v[y]+2*(x!=y)for y in range(2))for x in range(2)}
check(805,'frontier versus exhaustive chain optimum',min(v.values())==brute,'Boundary sizeone dynamic program matches all64 binary assignments, optimum%d.'%brute)
def partitions(k):
 def rec(a,maxval):
  if len(a)==k:yield tuple(a);return
  for x in range(maxval+2):yield from rec(a+[x],max(maxval,x))
 yield from rec([0],0)
def crow(p):
 bits=0
 for tail in product(range(2),repeat=len(p)-1):
  cut=(0,)+tail
  if all(cut[i]==cut[j]for i in range(len(p))for j in range(i)if p[i]==p[j]):
   idx=sum(cut[i]<< (i-1)for i in range(1,len(p)));bits|=1<<idx
 return bits
def connected(p,q):
 parent=list(range(len(p)))
 def find(a):
  while parent[a]!=a:parent[a]=parent[parent[a]];a=parent[a]
  return a
 for i in range(len(p)):
  for j in range(i):
   if p[i]==p[j] or q[i]==q[j]:parent[find(i)]=find(j)
 return len({find(i)for i in range(len(p))})==1
def basis(rows):
 piv={};ret=[]
 for i,row in enumerate(rows):
  x=row
  while x:
   j=x.bit_length()-1
   if j in piv:x^=piv[j]
   else:piv[j]=x;ret.append(i);break
 return ret
small=list(partitions(3));rows=[crow(p)for p in small]
check(806,'connectivity matrix factorization small exhaustive',len(small)==5 and all(((rows[i]&rows[j]).bit_count()%2)==connected(small[i],small[j])for i in range(5)for j in range(5)),'All25 join tests equalthe F2cut-row dotproducts.')
weights=[7,2,5,1,6];order=sorted(range(5),key=lambda i:weights[i]);kept=[order[j]for j in basis([rows[i]for i in order])]
opt=lambda inds,q:min((weights[i]for i in inds if connected(small[i],q)),default=inf)
check(806,'weighted representatives all small completions',len(kept)==4 and all(opt(range(5),q)==opt(kept,q)for q in small),'Cost-ordered rowbasis preservesminimum for allfive completionpartitions.')
large=list(partitions(8));large_rows=[crow(p)for p in large]
check(806,'Bell-eight count and full cut rank',len(large)==4140 and len(basis(large_rows))==128,'All4,140 partitions generated; exact F2rowelimination givesrank128 over128cutcolumns.')
entries=json.loads((P/'catalog2_entries.json').read_text());assert len(entries)==6
for e in entries:
 o=e['original'];fn,_,i=o['retrieval_receipt'].partition(' record ');r=json.loads((P/fn).read_text())[int(i)]
 assert any(o['source_excerpt'] in c['text']for c in r['result'].get('content',[])if c.get('type')=='text')
 assert f"{o['evidence']}@{o['date']}" in o['source_excerpt'];assert o['original_question'] is None
(P/'catalog2_checks.json').write_text(json.dumps({'checks':checks,'all_passed':True,'provenance':{'entries':6,'literal_excerpts':'passed'}},ensure_ascii=False,indent=2)+'\n')
print(len(checks),'catalog2checks passed; all6literal source excerpts passed')
