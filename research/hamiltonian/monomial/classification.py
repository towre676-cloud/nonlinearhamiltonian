"""Exact monomial Hamiltonian partner classification; Python standard library.

E(H) means hbar-independent polynomial G such that every odd Moyal correction
S_k(H,G), k>=3, vanishes. For unequal a,b>=2 this algorithm is complete,
not a search with a partner-degree cutoff. The a=2 or b=2 axis is symbolic.
Balanced exponents use proved closed formulae.
"""
from math import comb,factorial,gcd,isqrt,prod

def falling(n,k):return prod(range(n-k+1,n+1)) if 0<=k<=n else 0

def S(a,b,c,d,k):return sum((-1)**j*comb(k,j)*falling(a,k-j)*falling(b,j)*falling(c,j)*falling(d,k-j) for j in range(k+1))
def exact(a,b,c,d):return all(S(a,b,c,d,k)==0 for k in range(3,min(a+b,c+d)+1,2))
def poisson(a,b,c,d):return a*d-b*c

def padd(a,b):
 r=[0]*max(len(a),len(b))
 for i,x in enumerate(a):r[i]+=x
 for i,x in enumerate(b):r[i]+=x
 while len(r)>1 and r[-1]==0:r.pop()
 return r

def pmul(a,b):
 r=[0]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):r[i+j]+=x*y
 while len(r)>1 and r[-1]==0:r.pop()
 return r

def pfall(line,k):
 r=[1]
 for j in range(k):r=pmul(r,[line[0]-j,line[1]])
 return r

def correction_polynomial(a,b,c_line,d_line,k=3):
 out=[0]
 for j in range(k+1):
  coefficient=(-1)**j*comb(k,j)*falling(a,k-j)*falling(b,j)
  if coefficient:
   p=pmul(pfall(c_line,j),pfall(d_line,k-j));out=padd(out,[coefficient*x for x in p])
 return out

def peval(p,n):
 out=0
 for x in reversed(p):out=out*n+x
 return out

def divisors(n):
 assert n>0
 factors=[];p=2
 while p*p<=n:
  if n%p==0:
   power=0
   while n%p==0:n//=p;power+=1
   factors.append((p,power))
  p=3 if p==2 else p+2
 if n>1:factors.append((n,1))
 out=[1]
 for p,e in factors:out=[d*p**j for d in out for j in range(e+1)]
 return out

def nonnegative_integer_roots(p):
 p=list(p)
 while len(p)>1 and p[-1]==0:p.pop()
 if p==[0]:raise ValueError('Identically zero polynomial: symbolic family required')
 roots=[]
 while len(p)>1 and p[0]==0:
  if not roots:roots=[0]
  p=p[1:]
 if p[0]==0:return roots
 if len(p)>1:
  roots.extend(n for n in divisors(abs(p[0])) if peval(p,n)==0)
 return sorted(set(roots))

def classify_unequal(a,b):
 if not (isinstance(a,int) and isinstance(b,int) and min(a,b)>=2 and a!=b):raise ValueError('Require unequal integer exponents at least 2')
 candidates=set();axes=[]
 if a==2:axes.append('p')
 if b==2:axes.append('q')
 D=a+b;cwidth=b if D%2 else b-1;dwidth=a if D%2 else a-1
 for c in range(cwidth):
  if a==2 and c==0:continue
  p=correction_polynomial(a,b,(c,0),(0,1))
  for d in nonnegative_integer_roots(p):candidates.add((c,d))
 for d in range(dwidth):
  if b==2 and d==0:continue
  p=correction_polynomial(a,b,(0,1),(d,0))
  for c in nonnegative_integer_roots(p):candidates.add((c,d))
 if D%2==0:
  g=gcd(a,b);A=a//g;B=b//g
  p=correction_polynomial(a,b,(-1,B),(-1,A))
  for n in nonnegative_integer_roots(p):
   if n>=1:candidates.add((B*n-1,A*n-1))
 result=sorted((c,d) for c,d in candidates if not ((a==2 and c==0) or (b==2 and d==0)) and exact(a,b,c,d))
 return {'hamiltonian':[a,b],'scope':'complete over all nonnegative partner exponents','infinite_coordinate_algebras':axes,'finite_basis_exponents':[list(x) for x in result],'candidate_count_before_full_check':len(candidates),'method':'top correction strips/affine line, exact cubic integer roots, all odd corrections'}

def balanced_member(m,c,d):
 if m<=1:return True
 if m==2:return c==0 or d==0 or c==d
 if m==3:return c==d or c+d<=2 or (c,d) in [(1,11),(11,1)]
 return c==d or c+d<=2
