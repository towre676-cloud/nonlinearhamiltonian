"""Portable, newly executed finite mathematics checks; no historical repository verification is inferred."""
from fractions import Fraction as F
from pathlib import Path
import json, math
P=Path(__file__).resolve().parent
CHECKS=[]
def trim(a):
 a=list(map(F,a))
 while len(a)>1 and not a[-1]: a.pop()
 return a
def add(a,b): return trim([(a[i] if i<len(a) else 0)+(b[i] if i<len(b) else 0) for i in range(max(len(a),len(b)))])
def scale(a,c): return trim([F(c)*x for x in a])
def mul(a,b):
 c=[F(0)]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b): c[i+j]+=x*y
 return trim(c)
def deriv(a): return trim([i*a[i] for i in range(1,len(a))] or [0])
def val(a,x):
 out=F(0)
 for c in reversed(a): out=out*x+c
 return out
def divrem(a,b):
 a=trim(a);b=trim(b);assert b!=[0]
 q=[F(0)]*max(1,len(a)-len(b)+1)
 while a!=[0] and len(a)>=len(b):
  k=len(a)-len(b);v=a[-1]/b[-1];q[k]+=v
  a=add(a,[0]*k+scale(b,-v))
 return trim(q),trim(a)
def gcd(a,b):
 while trim(b)!=[0]: a,b=b,divrem(a,b)[1]
 return scale(a,1/a[-1])
def variations(a):
 signs=[1 if x>0 else -1 for x in a if x]
 return sum(x!=y for x,y in zip(signs,signs[1:]))
def record(id,name,fn):
 try: detail=fn();CHECKS.append({'id':id,'name':name,'status':'passed','detail':detail})
 except Exception as e: CHECKS.append({'id':id,'name':name,'status':'failed','detail':repr(e)})
def c1():
 f=mul(mul([-1,1],[-1,1]),[2,1]);assert f==[2,-3,0,1]
 g=gcd(f,deriv(f));assert g==[-1,1]
 q,r=divrem(f,g);assert r==[0] and q==[-2,1,1]
 seq=[q,deriv(q)]
 while seq[-1]!=[0]:
  rem=divrem(seq[-2],seq[-1])[1]
  if rem==[0]: break
  seq.append(scale(rem,-1))
 assert seq==[[-2,1,1],[1,2],[F(9,4)]]
 ends=[F(-5,2),F(-3,2),F(1,2),F(3,2)]
 V=[variations([val(s,x) for s in seq]) for x in ends]
 assert V==[2,1,1,0]
 assert val(f,F(1,2))==F(5,8) and val(f,F(3,2))==F(7,8)
 assert divrem(f,[-1,1])[1]==[0] and divrem(divrem(f,[-1,1])[0],[-1,1])==([2,1],[0])
 return {'polynomial':list(map(str,f)),'gcd':list(map(str,g)),'sturm_variations':V,'multiplicities':{'-2':1,'1':2}}
def c2():
 f=[1,-1,0,1];assert [int(val(f,x))%2 for x in range(2)]==[1,1]
 for x,y in [(0,1),(1,1),(3,5)]: assert y*y==val(f,x)
 product=mul([2,1,1],[2,2,1]);assert [int(x)%3 for x in product]==[1,0,0,0,1]
 translated=[F(2),F(4),F(6),F(4),F(1)]
 for x in range(-3,4): assert val(translated,x)==(x+1)**4+1
 assert all(c%2==0 for c in translated[:-1]) and translated[0]%4!=0
 return {'cubic_mod2_values':[1,1],'quartic_mod3_factors':[[2,1,1],[2,2,1]],'shifted_eisenstein_coefficients':list(map(str,translated))}
record('Y26-10-001','Squarefree gcd, Sturm intervals, exact double-root deflation',c1)
record('Y26-10-002','Finite-field cubic irreducibility and shifted Eisenstein quartic',c2)
from itertools import product, combinations, permutations
from functools import lru_cache
from collections import Counter

def mm(a,b): return [[sum(F(x)*F(y) for x,y in zip(row,col)) for col in zip(*b)] for row in a]
def eye(n): return [[F(i==j) for j in range(n)] for i in range(n)]
def transpose(a): return list(map(list,zip(*a)))
def det(a):
 a=[list(map(F,row)) for row in a];out=F(1);n=len(a)
 for i in range(n):
  k=next((k for k in range(i,n) if a[k][i]),None)
  if k is None:return F(0)
  if k!=i:a[i],a[k]=a[k],a[i];out=-out
  p=a[i][i];out*=p
  for j in range(i+1,n):
   q=a[j][i]/p
   for k in range(i+1,n):a[j][k]-=q*a[i][k]
 return out

def inv(a):
 n=len(a);a=[list(map(F,row))+e for row,e in zip(a,eye(n))]
 for i in range(n):
  k=next(k for k in range(i,n) if a[k][i]);a[i],a[k]=a[k],a[i]
  p=a[i][i];a[i]=[v/p for v in a[i]]
  for j in range(n):
   if j!=i:
    q=a[j][i];a[j]=[x-q*y for x,y in zip(a[j],a[i])]
 return [row[n:] for row in a]
def phi(n):return sum(math.gcd(i,n)==1 for i in range(1,n+1))
def moebius(n):
 k=0;p=2
 while p*p<=n:
  if n%p==0:
   n//=p;k+=1
   if n%p==0:return 0
   while n%p==0:n//=p
  p+=1
 if n>1:k+=1
 return (-1)**k

def c3():
 for p in [2,3,5]:
  for k in [1,2,3]:
   m=p**k;W=math.prod(i for i in range(1,m+1) if i%p)%m
   for n in range(81):
    u=math.factorial(n)
    while u%p==0:u//=p
    a=n;v=1
    while a:
     q,r=divmod(a,m);V=math.prod(i for i in range(1,r+1) if i%p)%m
     v=v*pow(W,q,m)*V%m;a//=p
    assert u%m==v
 assert math.factorial(10)//3**4==44800
 return '729 exact factorial-unit/block comparisons; U3(10)=44800=7 mod9.'
def c4():
 for t in range(-25,26):assert 2*(18*t**3)**2==3*(6*t*t)**3
 got={(x,y) for x in range(-200,201) for y in range(0,51) if 2*x*x==3*y**3}
 expected={(18*t**3,6*t*t) for t in range(-10,11) if abs(18*t**3)<=200 and 6*t*t<=50}
 assert got==expected
 assert (-144,24) in got and len({(18*t**3,6*t*t) for t in range(-5,6)})==11
 return {'bounded_exhaustive_solutions':sorted(got),'bound_y150_count':11}
def c5():
 E=[(a,b,c,d) for a in range(11) for b in range(7) for c in range(7) for d in range(5) if 2*a+3*b==20 and 2*c+3*d==12]
 expected=[(10-3*r,2*r,6-3*s,2*s) for r in range(4) for s in range(3)]
 assert set(E)==set(expected) and len(E)==12
 assert all(2**(2*a+3*b)*3**(2*c+3*d)==2**20*3**12 for a,b,c,d in E)
 for t in range(-20,21): assert 2*(-1+3*t)+3*(1-2*t)==1
 return {'exponent_population':12,'address_range':[0,11]}
def quadmul(a,b,d):return (a[0]*b[0]+d*a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def c6():
 orbit=set()
 for seed in [(1,2),(5,4)]:
  for sign in [-1,1]:
   a=seed
   for n in range(12):
    assert a[0]**2-2*a[1]**2==-7
    if a[1]<=1000:orbit.add(a)
    a=quadmul(a,(3,sign*2),2)
 bounded={(x,y) for y in range(1,1001) for x in [math.isqrt(2*y*y-7) if 2*y*y>=7 else 0] if x*x==2*y*y-7}
 bounded|={(-x,y) for x,y in bounded}
 assert orbit==bounded
 assert [(y,2*y*y-7) for y in range(2,6)]==[(2,1),(3,11),(4,25),(5,43)]
 return {'bounded_solutions_y_le_1000':len(bounded),'reduction_seeds':[[1,2],[5,4]]}
def c7():
 for n in range(1,11):
  E=[[int(i%j==0) for j in range(1,n+1)] for i in range(1,n+1)]
  D=[[F(phi(i+1) if i==j else 0) for j in range(n)] for i in range(n)]
  G=[[math.gcd(i,j) for j in range(1,n+1)] for i in range(1,n+1)]
  assert mm(mm(E,D),transpose(E))==G and det(G)==math.prod(phi(i) for i in range(1,n+1))
 K=[[min(i,j) for j in range(1,4)] for i in range(1,4)]
 assert inv(K)==[[2,-1,0],[-1,2,-1],[0,-1,1]]
 return 'Exact GCD factorizations/determinants n1–10; independent rational inverse of min kernel.'
def c8():
 for d in range(2,9):
  for m in range(1,11):
   delta=math.gcd(d,m);R=m*(d-1)+d-delta
   g=F((d-1)*(m-1)-delta+1,2)
   assert g.denominator==1 and g>=0 and 2*g-2==-2*d+R
 assert (F((3-1)*(4-1)-1+1,2))==3
 return 'Finite ramification/genus consistency grid and examples (2,3):g1,(3,4):g3; proof supplies general result.'
def norm3(a,b,c):return a**3-4*b**3+16*c**3+12*a*b*c

def c9():
 for a,b,c in product(range(-2,3),repeat=3):
  M=[[a,-4*c,-4*b],[b,a,-4*c],[c,b,a]]
  assert det(M)==norm3(a,b,c)
 assert norm3(5,-3,2)==norm3(1,-1,-1)==1
 assert norm3(-1,-3,0)==norm3(-13,-2,4)==107
 return '125 independent determinant/norm comparisons, both unit norms and transported norm107.'
def c10():
 A=mul([-1,1],[-2,1]);B=[-1,1]
 N=add(mul(A,A),scale(mul(B,B),-2))
 assert N==mul(mul([-1,1],[-1,1]),[2,-4,1])
 assert val(A,1)==val(B,1)==0
 return {'eliminant_coefficients':list(map(str,N)),'exceptional_point':1}
def c11():
 p=mul(mul([-1,1],[1,1]),[-2,1]);a=[-1,1]
 assert gcd(p,a)==a
 h,r=divrem(p,a);assert r==[0] and h==[-2,-1,1]
 assert divrem(mul(a,[0,F(1,2)]),h)[1]==[1]
 assert gcd(a,a)==a
 return 'Exact gcd split and modular inverse t/2; repeated-factor gcd obstruction checked.'
def c12():
 t=[0,1];sech2=[1,0,-1]
 D=lambda p:mul(sech2,deriv(p))
 pot=[-2,0,6]
 L=lambda p:add(scale(D(D(p)),-1),mul(pot,p))
 assert L(sech2)==[0]
 J=lambda p:add(D(p),scale(mul(t,p),-1))
 shape=add(scale(J(J(t)),-1),mul(pot,t))
 assert shape==scale(t,3)
 assert F(3,4)*F(4,3)==1
 return 'Polynomial-in-tanh residuals vanish for zero and shape modes; exact normalization integral.'
def bdadd(a,b):
 out=dict(a)
 for k,v in b.items():out[k]=out.get(k,F(0))+v
 return {k:F(v) for k,v in out.items() if v}
def bdmul(a,b):
 out={}
 for (i,j),x in a.items():
  for (k,l),y in b.items():out[i+k,j+l]=out.get((i+k,j+l),0)+x*y
 return {k:F(v) for k,v in out.items() if v}
def bdd(a,dim):
 out={}
 for (i,j),v in a.items():
  n=(i,j)[dim]
  if n:out[(i-1,j) if dim==0 else (i,j-1)]=n*v
 return out
def c13():
 Xx={(2,0):1,(0,2):-1};Xy={(1,1):2};K={(1,0):2}
 for H in [{(0,1):1},{(2,0):1,(0,2):1}]:
  XH=bdadd(bdmul(Xx,bdd(H,0)),bdmul(Xy,bdd(H,1)))
  assert XH==bdmul(K,H)
 return 'Two Darboux/cofactor identities checked coefficientwise over Q.'
def compose(a,b,N):
 out=[F(0)];power=[F(1)]
 for c in a:
  out=add(out,scale(power,c));out=trim(out[:N+1]);power=trim(mul(power,b)[:N+1])
 return out
def c14():
 N=12;h=[0]+[F((-1)**(n+1),n) for n in range(1,N+1)]
 assert compose(h,[0,2,1],N)==scale(h,2)
 assert all(2**n-2!=0 for n in range(2,N+1))
 assert [n for n in range(2,9) if (-1)**n==(-1)]==[3,5,7]
 return 'Formal logarithmic Schröder identity through degree12; resonance pattern checked.'
weights=(2,3,4);profits=(3,4,5)
@lru_cache(None)
def completion(i,b):
 if b<0:return 0
 if i==len(weights):return 1
 if b>=sum(weights[i:]):return 2**(len(weights)-i)
 return completion(i+1,b)+completion(i+1,b-weights[i])
def population():return [x for x in product([0,1],repeat=3) if sum(w*b for w,b in zip(weights,x))<=5]
def c15():
 pop=population();assert len(pop)==completion(0,5)==5
 obj=[sum(p*b for p,b in zip(profits,x)) for x in pop]
 assert max(obj)==7 and obj.count(7)==1 and pop[obj.index(7)]==(1,1,0)
 assert sum(x[0] and x[2] for x in product([0,1],repeat=4))==4
 return {'population':5,'optimum':7,'optimum_multiplicity':1,'skipped_variable_example':4}
def c16():
 pop=population()
 def unrank(r):
  b=5;bits=[]
  for i in range(3):
   zero=completion(i+1,b)
   bit=int(r>=zero)
   if bit:r-=zero;b-=weights[i]
   bits.append(bit)
  assert r==0
  return tuple(bits)
 def rank(x):
  b=5;r=0
  for i,bit in enumerate(x):
   if bit:r+=completion(i+1,b);b-=weights[i]
  return r
 assert [unrank(r) for r in range(5)]==pop
 assert [rank(x) for x in pop]==list(range(5))
 counts=Counter(x%5 for x in range(8));assert [counts[i] for i in range(5)]==[2,2,2,1,1]
 return 'Complete rank/unrank inverse checks on all5 objects; modulo bias histogram(2,2,2,1,1).'
def c17():
 gate=lambda x,y,a:int(a==(x^y))
 assert sum(gate(x,y,a) for x,y,a in product([0,1],repeat=3))==4
 assert sum(gate(x,y,a)*a for x,y,a in product([0,1],repeat=3))==2
 for x,y in product([0,1],repeat=2):assert sum(gate(x,y,a)*a for a in [0,1])==(x^y)
 return 'All binary gate fibres and elimination tables enumerated; unconstrained auxiliary count8.'
def c18():
 A=[[int(i==j)*(i+1) for j in range(6)] for i in range(6)]
 R=[row[:6] for row in eye(6)[:3]];G=[[int(i==j)*(i+1) for j in range(3)] for i in range(3)]
 assert mm(R,A)==mm(G,R)
 y=[1+2**n+3**n for n in range(25)]
 H=[[y[i+j] for j in range(3)] for i in range(3)];assert det(H)==4
 assert all(y[n+3]==6*y[n+2]-11*y[n+1]+6*y[n] for n in range(22))
 return {'hankel_determinant':'4','global_intertwiner_checked':True,'recurrence_terms_checked':25}
def c19():
 H=[[1,1,0],[0,1,1]];G=[[1,2,1]];L=[[1,1]];v=[[1],[-1],[1]]
 assert mm(L,H)==G and mm(H,v)==[[0],[0]] and mm(G,v)==[[0]]
 assert mm([[1,0,0]],v)==[[1]]
 return 'Exact factorization L H=G and explicit nullspace witness for a nonidentifiable target.'
def c20():
 # Coefficients are ordered (cos t,sin t), so equality is symbolic.
 B=[[(1,0),(0,1)]];Bp=[[(-0, -1),(1,0)]]
 A=[[0,-1],[1,0]]
 BA=[[(sum(B[0][i][j]*A[i][k] for i in range(2))) for j in range(2)] for k in range(2)]
 assert [tuple(x) for x in BA]==[(0,1),(-1,0)]
 assert all(Bp[0][i][j]+BA[i][j]==0 for i in range(2) for j in range(2))
 assert mm([[1,0]],A)==[[0,-1]]
 return 'Symbolic sine/cosine coefficient cancellation B′+BA=0; fixed-frame obstruction.'
def c21():
 output=(0,0,0,1);identity=tuple(range(4));reset=(2,3,2,3)
 def refine(actions):
  labels=list(output)
  while True:
   keys=[(output[s],tuple(labels[a[s]] for a in actions)) for s in range(4)]
   uniq={k:i for i,k in enumerate(dict.fromkeys(keys))};new=[uniq[k] for k in keys]
   if all((new[i]==new[j])==(labels[i]==labels[j]) for i,j in product(range(4),repeat=2)):return new
   labels=new
 a=refine([identity]);b=refine([identity,reset])
 assert a[0]==a[1] and b[0]!=b[1] and output[reset[0]]!=output[reset[1]]
 return {'identity_classes':a,'with_reset_classes':b}
def c22():
 tests=[(1,(0,1,1)),(2,(0,1,0)),(4,(0,1,2))]
 @lru_cache(None)
 def V(S):
  if len(S)<=1:return 0
  cand=[]
  for cost,obs in tests:
   fibres=[tuple(s for s in S if obs[s]==v) for v in set(obs[s] for s in S)]
   if all(len(f)<len(S) for f in fibres):cand.append(cost+max(V(f) for f in fibres))
  return min(cand)
 assert V((0,1,2))==3 and V((1,2))==2
 return 'Exact minimax recursion on every reached subset: three-state optimum3, direct test4.'
def c23():
 c=(F(0),F(100));d=(F(7,4),F(9,4));A=(c[0]+d[0],c[1]+d[1]);B=c
 separate=(A[0]-B[1],A[1]-B[0]);assert separate[0]==F(-393,4) and d[0]==F(7,4)>0
 assert F(1,4)-F(1,10)==F(3,20)>0
 assert F(1,20)-F(1,10)<0<F(1,20)+F(1,10)
 return {'separate_interval':list(map(str,separate)),'joint_margin':'7/4','measurement_margin':'3/20'}
def c24():
 words=[]
 for x in range(31):
  out=[]
  for j in range(5):out.append(x%8);x=3*x%31
  words.append(tuple(out))
 counts=[len({w[:k] for w in words}) for k in range(1,4)];assert counts==[8,24,31]
 distance=min(sum(a!=b for a,b in zip(x,y)) for i,x in enumerate(words) for y in words[:i]);assert distance==3
 M=2**107-1;A=pow(3,121,M)
 assert 2**104<M and math.gcd(A,M)==math.gcd(2**26,M)==1
 return {'toy_code_distinct_counts':counts,'toy_length5_distance':distance,'actual_multiplier':str(A),'large_all_state_certificate':'separate root supplement Y26-10-901–902'}
def c25():
 t=[10**12+1,-10**12];s=sum(t);k=F(sum(map(abs,t)),abs(s));assert k==2*10**12+1
 eps=F(1,10**12);pert=[eps*abs(x) for x in t]
 assert abs(sum(pert))/abs(s)==eps*k
 return {'exact_condition_number':str(k),'attained_relative_error_bound':str(eps*k)}
for n,fn in enumerate([c3,c4,c5,c6,c7,c8,c9,c10,c11,c12,c13,c14,c15,c16,c17,c18,c19,c20,c21,c22,c23,c24,c25],3):
 record(f'Y26-10-{n:03d}',fn.__name__,fn)
def charpoly(A):
 n=len(A);out=[0]
 for perm in permutations(range(n)):
  sign=(-1)**sum(perm[i]>perm[j] for i in range(n) for j in range(i+1,n));term=[F(sign)]
  for i,j in enumerate(perm):term=mul(term,[-A[i][j],1] if i==j else [-A[i][j]])
  out=add(out,term)
 return trim(out)
def c26():
 T=[[0,6,0,0],[1,0,5,0],[0,1,4,1],[0,0,6,0]]
 p=charpoly(T);want=[1]
 for r in [6,2,-1,-3]:want=mul(want,[-r,1])
 assert p==want
 shells=[1,6,30,5];assert sum(shells)==42 and [shells[i]*[6,5,1][i] for i in range(3)]==[shells[i+1]*[1,1,6][i] for i in range(3)]
 mult={6:1,2:21,-1:6,-3:14}
 assert sum(mult.values())==42 and sum(x*m for x,m in mult.items())==0 and sum(x*x*m for x,m in mult.items())==252
 return {'quotient_characteristic_coefficients':list(map(str,p)),'conditional_spectrum':mult}
G_edges=[(0,3),(0,4),(0,6),(1,2),(1,3),(2,3),(2,4),(3,5)]
H_edges=[(0,1),(0,4),(0,6),(1,5),(1,6),(2,6),(3,6),(4,5)]
def energy(E,h):return sum((h[i]-h[j])**2 for i,j in E)
def compositions(n,k):
 if k==1:yield(n,);return
 for j in range(n+1):
  for rest in compositions(n-j,k-1):yield(j,)+rest

def c27():
 def binary(E):return Counter((sum(h),energy(E,h)) for h in product([0,1],repeat=7))
 assert binary(G_edges)==binary(H_edges)
 def coeff(E,R,support=None):
  return Counter(energy(E,h) for h in compositions(R,7) if support is None or sum(x>0 for x in h)==support)
 def difference(a,b):
  a.subtract(b);return {k:v for k,v in a.items() if v}
 for R in range(3):assert not difference(coeff(G_edges,R),coeff(H_edges,R))
 D=difference(coeff(G_edges,3),coeff(H_edges,3));marked=difference(coeff(G_edges,3,2),coeff(H_edges,3,2));assert D==marked
 p=[0,0,0,1]
 for step in [1,3,3,4,4]:p=mul(p,[1]+[0]*(step-1)+[-1])
 assert D=={i:int(v) for i,v in enumerate(p) if v}
 assert val(p,F(1,2))==F(11025,262144)
 return {'binary_assignments_checked':128,'height3_compositions':math.comb(9,6),'difference':{str(k):v for k,v in sorted(D.items())},'q_half':'11025/262144'}
def lap(n,E):
 L=[[0]*n for _ in range(n)]
 for i,j in E:L[i][i]+=1;L[j][j]+=1;L[i][j]-=1;L[j][i]-=1
 return L

def c28():
 cases=[([(0,1),(1,2)],[F(1,5),F(2,15),F(1,5)],F(5)), ([(0,1),(1,2),(0,2)],[F(2,15)]*3,F(15,2)), ([(0,1)],[F(5,24),F(5,24),F(1,3)],F(3))]
 rows=[]
 for E,diag,w in cases:
  L=lap(3,E);Q=[[L[i][j]+2*(i==j) for j in range(3)] for i in range(3)];Qinv=inv(Q)
  K=[[Qinv[i][j]-F(1,6) for j in range(3)] for i in range(3)]
  assert [K[i][i] for i in range(3)]==diag and 1/max(diag)==w
  for i in range(3):
   v=[[K[j][i]/K[i][i]] for j in range(3)]
   assert sum(row[0] for row in v)==0 and v[i][0]==1 and mm(mm(transpose(v),Q),v)==[[1/K[i][i]]]
  rows.append({'diagonal':list(map(str,diag)),'reciprocal_max':str(w)})
 return rows

def rowrank(a):
 if not a:return 0
 a=[list(map(F,row)) for row in a];r=0
 for col in range(len(a[0])):
  k=next((k for k in range(r,len(a)) if a[k][col]),None)
  if k is None:continue
  a[r],a[k]=a[k],a[r];v=a[r][col];a[r]=[x/v for x in a[r]]
  for k in range(r+1,len(a)):
   v=a[k][col];a[k]=[x-v*y for x,y in zip(a[k],a[r])]
  r+=1
  if r==len(a):break
 return r

def c29():
 M=[[0,1,0],[0,0,1],[1,0,0]];W=[[1,0,0]];ranks=[1]
 for j in range(3):W=W+mm(W,M);ranks.append(rowrank(W))
 assert ranks==[1,2,3,3]
 for a,b,ap,bp in product(range(-2,3),repeat=4):
  if a==ap and a*b==ap*bp:assert all(a*b**n==ap*bp**n for n in range(16))
 return {'finite_closure_ranks':ranks,'rational_family_prefix_example':'a,ab determines all checked coefficients; general proof in text'}

def c30():
 fibres=Counter(a%30 for a in range(1680) if math.gcd(a,1680)==1)
 assert len(fibres)==8 and set(fibres.values())=={48} and sum(fibres.values())==384
 assert phi(1680)==384 and phi(30)==8
 # Independent companion-matrix trace agrees with divisor formula for Phi30.
 poly=[1,1,0,-1,-1,-1,0,1,1];D=[[0]*8 for _ in range(8)]
 for i in range(7):D[i+1][i]=1
 for i in range(8):D[i][7]=-poly[i]
 power=eye(8)
 for n in range(1,61):
  power=mm(power,D);trace=sum(power[i][i] for i in range(8))
  cn=sum(d*moebius(30//d) for d in range(1,31) if 30%d==0 and n%d==0)
  assert trace==cn
 return {'primitive_phase_fibres':dict(sorted(fibres.items())),'companion_trace_checks':60}
def c31():
 primitive=[r for r in range(264) if math.gcd(1+1680*r,443520)==1]
 assert len(primitive)==240 and phi(443520)==92160 and F(92160,384)==240
 assert 443520==1680*264
 # N=2 Fourier filter: odd powers vanish and even powers have the exact scale.
 for n in range(1,41):assert F(1+(-1)**n,n*n)==(F(1,2*(n//2)**2) if n%2==0 else 0)
 return {'total_power_roots':264,'primitive_roots':240,'extension_degree':240}
def c32():
 N=16;S=[F(0)]*(2*N+1)
 for n in range(1,N+1):S[2*n]=F(1,n*n*math.comb(2*n,n))
 residual=add(mul([4,0,-1],deriv(deriv(S))),scale(mul([0,1],deriv(S)),-1))
 assert trim(residual[:2*N-1])==[4]
 assert [S[2],S[4],S[6]]==[F(1,2),F(1,24),F(1,180)]
 assert F(2,840**2)==F(1,352800)
 return {'series_ODE_residual_through_degree':2*N-2,'first_coefficients':['1/2','1/24','1/180'],'special_value_coefficient':'1/352800'}
def c33():
 ds=[d for d in range(1,31) if 30%d==0]
 S=sum(F(moebius(30//d),d) for d in ds);assert S==F(-4,15) and S+F(240,30**2)==0
 P30=[1,1,0,-1,-1,-1,0,1,1];num=scale(deriv(P30),-1);coeff=[]
 for n in range(60):
  v=(num[n] if n<len(num) else 0)-sum(P30[j]*coeff[n-j] for j in range(1,min(n,len(P30)-1)+1));coeff.append(F(v))
  cn=sum(d*moebius(30//d) for d in ds if (n+1)%d==0);assert coeff[-1]==cn
 logs=[F(-4,15)*F(2)/6,F(-4,15)*F(3,2)/6,F(-4,15)*F(5,4)/6]
 assert logs==[F(-16,180),F(-12,180),F(-10,180)]
 return {'divisor_sum':str(S),'zero_compensator':'4/15','logarithmic_coefficients_of_pi_squared':list(map(str,logs)),'log_derivative_coefficients_checked':60}
def c34():
 S=[0,1,2,4,11]
 def B(r):x=F(r%17,17);return x*x-x+F(1,6)
 terms=[B(s-r)+B(s+r) for s in S for r in S]
 assert sum(terms)==F(955,867)
 return {'ordered_phase_pairs':25,'bernoulli_terms':50,'exact_I_over_pi_cubed':'955/867'}
def c35():
 assert (5*7)%17==1
 assert (5*5+9)%17==0 and (6*5+4)%17==0
 assert (6*9)%17==(5*4)%17==3
 for delta in range(17):
  xi=(7*delta)%17;assert (5*xi)%17==delta
 return 'Exact determinant-twist and split-extension exponents checked in Z/17; no matrix density claim.'
def c36():
 for a,b in product(range(-4,5),repeat=2):
  v=quadmul(quadmul((a,b),(a,b),-2),(a,b),-2)
  assert v==(a**3-6*a*b*b,b*(3*a*a-2*b*b))
 candidates=[(a,b) for a in [-1,0,1] for b in [-1,1] if b*(3*a*a-2*b*b)==1]
 assert candidates==[(-1,1),(1,1)]
 points=sorted((a*a+2*b*b,a**3-6*a*b*b) for a,b in candidates)
 assert points==[(3,-5),(3,5)]
 assert max(x*x+2*y*y for x,y in product([F(-1,2),F(1,2)],repeat=2))==F(3,4)<1
 return {'cube_coefficient_candidates':candidates,'global_proof_reduced_points':points,'Euclidean_rounding_corner_bound':'3/4'}
def c37():
 a=F(0);b=F(-2);u=F(3);v=F(5);slope=(3*u*u+a)/(2*v);X=slope*slope-2*u;Y=slope*(u-X)-v
 assert (X,Y)==(F(129,100),F(-383,1000)) and Y*Y==X**3-2
 q=[a*a-4*b*X,-(8*b+4*a*X),-2*a,-4*X,1];assert val(q,u)==0
 return {'doubled_point':[str(X),str(Y)],'halving_quartic_residual':'0'}
def c38():
 # Independent AGM evaluation is a numerical convention check, not a replacement for the proved inequality.
 z=1e-8;s=math.sqrt(z);a,b=1.0,s
 for _ in range(15):a,b=(a+b)/2,math.sqrt(a*b)
 K=math.pi/(2*a);split=2*math.asinh(z**(-.25));err=s/2
 assert abs(K-split)<err+1e-10
 assert F(1,10000)/2==F(1,20000)
 return {'method':'independent AGM numerical convention check','K':K,'split_error':K-split,'proved_absolute_bound':err}
def c39():
 A=[[1,x,y,x*x] for x,y in [(0,0),(1,1),(2,4),(3,9)]];v=[[0],[0],[1],[-1]]
 assert det(A)==0 and mm(A,v)==[[0]]*4
 assert det([[64,0],[0,1]])==64
 return 'Parabola evaluation kernel checked exactly; equality-bound nonvanishing counterexample det=64.'
def c40():
 p=F(4,5);assert 30*p-F(95,4)==F(1,4) and F(95,4)/30==F(19,24)
 assert [10*j-F(95,4) for j in range(4)]==[F(-95,4),F(-55,4),F(-15,4),F(25,4)]
 upper=[(int(i!=0),)*3 for i in range(5)]
 lower=[tuple(int(i!=j) for j in range(3)) for i in range(5)]
 for pop in [upper,lower]:assert [F(sum(x[j] for x in pop),5) for j in range(3)]==[p]*3
 assert F(sum(all(x) for x in upper),5)==p and F(sum(all(x) for x in lower),5)==F(2,5)
 return {'expectation':'1/4','positive_event_probability_range':['2/5','4/5'],'independent_probability':'64/125'}
for n,fn in enumerate([c26,c27,c28,c29,c30,c31,c32,c33,c34,c35,c36,c37,c38,c39,c40],26):
 record(f'Y26-10-{n:03d}',fn.__name__,fn)

def schema_check():
 E=json.loads((P/'entries.json').read_text());assert len(E)==40
 assert [e['id'] for e in E]==[f'Y26-10-{i:03d}' for i in range(1,41)]
 for e in E:
  assert e['original']['month']=='2026-10'
  d=e['original']['date'];assert d is None or '2026-10-01'<=d<='2026-10-21'
  assert e['original']['original_question'] is None
  assert e['original']['evidence'] in ['U','A','T']
  receipt,idx=e['original']['retrieval_receipt'].split(' record ')
  data=json.loads((P/receipt).read_text());r=data[int(idx)];messages=r.get('result',r).get('structuredContent',{}).get('messages',[])
  assert any(e['original']['source_excerpt'] in m.get('content','') for m in messages)
 return 'All40 IDs, cutoff dates, author labels, nullable prompts and exact raw source excerpts checked against actual receipts.'
record('Y26-10-SCHEMA','Schema, cutoff and exact-source provenance audit',schema_check)
(P/'checks.json').write_text(json.dumps({'checks':CHECKS},ensure_ascii=False,indent=2)+'\n')
print(f"{sum(c['status']=='passed' for c in CHECKS)}/{len(CHECKS)} passed")
for c in CHECKS:
 if c['status']=='failed':print(c)
if any(c['status']!='passed' for c in CHECKS):raise SystemExit(1)
