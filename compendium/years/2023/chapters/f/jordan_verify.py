#!/usr/bin/env python3
"""Exact Gaussian-rational certificates for the S014 Jordan classification."""
from fractions import Fraction as F
from pathlib import Path
import json
from math import comb
P=Path(__file__).resolve().parent
checks=[];cert={}
def check(name,detail):checks.append(dict(id='S014',name=name,status='passed',detail=detail))
class G:
 def __init__(self,a=0,b=0):
  if isinstance(a,G):self.a,self.b=a.a,a.b
  else:self.a,self.b=F(a),F(b)
 def __add__(self,o):o=G(o);return G(self.a+o.a,self.b+o.b)
 __radd__=__add__
 def __neg__(self):return G(-self.a,-self.b)
 def __sub__(self,o):return self+-G(o)
 def __rsub__(self,o):return G(o)+-self
 def __mul__(self,o):o=G(o);return G(self.a*o.a-self.b*o.b,self.a*o.b+self.b*o.a)
 __rmul__=__mul__
 def inv(self):
  d=self.a*self.a+self.b*self.b
  if not d:raise ZeroDivisionError
  return G(self.a/d,-self.b/d)
 def __truediv__(self,o):return self*G(o).inv()
 def __rtruediv__(self,o):return G(o)*self.inv()
 def __pow__(self,n):
  if n<0:return self.inv()**(-n)
  r=G(1)
  for k in range(n):r*=self
  return r
 def __eq__(self,o):o=G(o);return self.a==o.a and self.b==o.b
 def __ne__(self,o):return not self==o
 def __str__(self):return str(self.a)+' + ('+str(self.b)+')i'
def zero(n):return [[G(0) for _ in range(n)] for _ in range(n)]
def eye(n):return [[G(i==j) for j in range(n)] for i in range(n)]
def ma(a,b):return [[x+y for x,y in zip(r,s)] for r,s in zip(a,b)]
def ms(a,k):return [[x*k for x in row] for row in a]
def md(a,b):return ma(a,ms(b,-1))
def mm(a,b):return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]
def mv(a,v):return [sum(x*y for x,y in zip(row,v)) for row in a]
def outer(a,b):return [[x*y for y in b] for x in a]
def rank(a):
 a=[r[:] for r in a];i=0
 for j in range(len(a[0])):
  pivot=next((k for k in range(i,len(a)) if a[k][j]!=0),None)
  if pivot is None:continue
  a[i],a[pivot]=a[pivot],a[i];c=a[i][j];a[i]=[x/c for x in a[i]]
  for k in range(len(a)):
   if k!=i:
    c=a[k][j];a[k]=[x-c*y for x,y in zip(a[k],a[i])]
  i+=1
  if i==len(a):break
 return i
def Hs(sites):
 n=len(sites);out=[]
 for i in range(n):
  H=zero(n)
  for j in range(n):
   if i==j:continue
   O=ms(eye(n),F(1,2));O[i][i]=O[j][j]=G(F(-1,2));O[i][j]=O[j][i]=G(1)
   H=ma(H,ms(O,1/(sites[i]-sites[j])))
  out.append(H)
 E0=[sum(F(1,2)/(sites[i]-sites[j]) for j in range(n) if j!=i) for i in range(n)]
 return out,E0
def charpoly(A):
 n=len(A);power=eye(n);traces=[G(n)]
 for k in range(1,n+1):
  power=mm(power,A);traces.append(sum(power[i][i] for i in range(n)))
 descending=[G(1)]
 for k in range(1,n+1):descending.append(-sum(descending[k-j]*traces[j] for j in range(1,k+1))/k)
 return list(reversed(descending))
def pa(a,b):return [(a[i] if i<len(a) else G(0))+(b[i] if i<len(b) else G(0)) for i in range(max(len(a),len(b)))]
def ps(a,k):return [x*k for x in a]
def pm(a,b):
 c=[G(0)]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):c[i+j]+=x*y
 return c
def ppow(a,n):
 r=[G(1)]
 for k in range(n):r=pm(r,a)
 return r
def characteristic_formula(sites,base,E0):
 n=len(sites);p=[G(1)]
 for z in sites:p=pm(p,[-z,G(1)])
 derivative=[j*p[j] for j in range(1,len(p))]
 zi=sites[base];denom=sum(c*zi**k for k,c in enumerate(derivative))
 assert denom!=0
 ucoeff=[G(0)]*(n+1)
 for k,c in enumerate(derivative):
  for ell in range(k+1):ucoeff[n-ell]+=c*comb(k,ell)*zi**(k-ell)/denom
 out=[G(0)]
 for c in reversed(ucoeff):out=pa(pm(out,[-E0,G(1)]),[c])
 while len(out)>1 and out[-1]==0:out.pop()
 return out
def fractional_relations(sites,H,E0):
 n=len(sites);A0=md(H[0],ms(eye(n),E0[0]))
 for j in range(n):
  Aj=md(H[j],ms(eye(n),E0[j]));denom=ma(eye(n),ms(A0,sites[0]-sites[j]))
  assert rank(denom)==n and mm(Aj,denom)==A0 and mm(denom,Aj)==A0
def encode(v):return [str(x) for x in v]
def chain(sites,w,m,base=0):
 a=1/(w-sites[base]);vectors=[];coeffs=[]
 for k in range(m):
  vec=[]
  for z in sites:
   d=sites[base]-z;A=1+d*a
   vec.append(a/A if k==0 else (-d)**(k-1)/A**(k+1))
  vectors.append(vec)
 for j,z in enumerate(sites):
  d=sites[base]-z;A=1+d*a
  coeffs.append([(-d)**(k-1)/A**(k+1) for k in range(1,m)])
 return vectors,coeffs

i=G(0,1)
sites=[G(1),G(-1),i,-i];H,E0=Hs(sites);V,c=chain(sites,G(0),3)
expected=[[-1,1,i,-i],[1,1,-1,-1],[0,2,-1-i,-1+i]]
assert V==[[G(x) for x in row] for row in expected]
u=[G(1)]*4;E=[E0[j]+1/(-sites[j]) for j in range(4)]
assert E0==[G(3)/(4*z) for z in sites]
assert E==[-G(1)/(4*z) for z in sites]
for j,A in enumerate(H):
 for k in range(3):
  left=[x-E[j]*y for x,y in zip(mv(A,V[k]),V[k])]
  right=[sum(c[j][ell-1]*V[k-ell][a] for ell in range(1,k+1)) for a in range(4)]
  assert left==right
assert rank([u]+V)==4
Q=md(eye(4),ms(outer(u,u),F(1,4)))
N=mm(md(H[0],ms(eye(4),E[0])),Q)
assert mm(N,N)!=zero(4) and mm(mm(N,N),N)==zero(4)
expected_char=pm([G(F(-3,4)),G(1)],ppow([G(F(1,4)),G(1)],3))
assert charpoly(H[0])==expected_char
assert characteristic_formula(sites,0,E0[0])==expected_char
fractional_relations(sites,H,E0)
check('Multiplicity-three critical point and complete length-three chain','For sites (1,−1,i,−i), all four Hamiltonians satisfy the exact Taylor-chain polynomial relations. The uniform vector plus V₀,V₁,V₂ has rank4. On the highest-weight plane N²≠0 and N³=0; the full characteristic polynomial is (λ−3/4)(λ+1/4)³.')
check('Closed characteristic formula and fractional-linear Hamiltonian identities for four sites','Exact Gaussian-rational evaluation verifies χ_Hi(λ)=u^n p′(z_i+1/u)/p′(z_i) at the base site. All A_j[I+(z_i−z_j)A_i]=A_i identities hold with invertible denominators.')
cert['four_site']={'sites':encode(sites),'chain':[encode(v) for v in V],'vacuum_eigenvalues':encode(E0),'critical_eigenvalues':encode(E),'characteristic_polynomial_ascending':encode(expected_char),'N_squared':[[str(x) for x in r] for r in mm(N,N)],'N_cubed':'zero'}

# A mixed critical multiplicity pattern with all physical sites in Q(i).
sites=[G(1),G(-1),i,-i,G(2),G(-2),2*i,-2*i];H,E0=Hs(sites)
V,c=chain(sites,G(0),3);u=[G(1)]*8
E=[E0[j]+1/(-sites[j]) for j in range(8)]
assert E0[0]==G(F(37,60)) and E[0]==G(F(-23,60))
for j,A in enumerate(H):
 for k in range(3):
  left=[x-E[j]*y for x,y in zip(mv(A,V[k]),V[k])]
  right=[sum(c[j][ell-1]*V[k-ell][a] for ell in range(1,k+1)) for a in range(8)]
  assert left==right
assert rank([u]+V)==4
q=[G(F(-37,60)),G(1)];qplus=pa(q,[G(1)])
quartic=ps(pa(ps(ppow(q,4),17),ps(ppow(qplus,4),-2)),F(1,15))
expected_char=pm(pm([G(F(-37,60)),G(1)],ppow([G(F(23,60)),G(1)],3)),quartic)
actual=charpoly(H[0]);assert actual==expected_char
assert characteristic_formula(sites,0,E0[0])==actual
fractional_relations(sites,H,E0)
assert all(x.b==0 for x in actual)
for j,A in enumerate(H):
 assert mv(A,u)==[E0[j]*x for x in u]
for A in H:
 for B in H:assert mm(A,B)==mm(B,A)
check('Mixed multiplicity example with exact characteristic factorization','For eight sites ±1,±i,±2,±2i, the multiplicity-three chain is checked for every Hamiltonian. An independent Newton/trace computation of the full H₁ characteristic polynomial exactly matches the stated cubic factor times four distinct regular-root factors and the uniform factor. All Hamiltonians commute.')
check('Closed characteristic formula and fractional-linear identities in the mixed case','The general characteristic-polynomial formula independently reproduces the full degree-eight polynomial, and all eight Hamiltonian fractional-linear relations have exactly invertible denominators and zero residual matrices.')
cert['eight_site']={'sites':encode(sites),'chain':[encode(v) for v in V],'base_vacuum_eigenvalue':str(E0[0]),'base_triple_eigenvalue':str(E[0]),'characteristic_polynomial_ascending':encode(actual),'quartic_regular_factor_ascending':encode(quartic),'critical_factorization':'p′=4x³(2x⁴−17)','Jordan_block_sizes':[3,1,1,1,1,1]}

out={'checks':checks,'certificates':cert,'scope':'Every calculation here is exact in Q(i). The arbitrary-n classification and the squarefreeness criterion are proved in S014; they are not inferred from these examples.'}
P.joinpath('jordan_checks.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
print(json.dumps({'id':'S014','checks':len(checks),'arithmetic':'exact Q(i)','status':'passed'}))
