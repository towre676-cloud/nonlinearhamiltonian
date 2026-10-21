#!/usr/bin/env python3
"""Independent exact Gaussian-rational replay of p=x^4-1 one-magnon jets."""
from fractions import Fraction as F
from pathlib import Path
import json
class G:
 def __init__(self,a=0,b=0):
  if isinstance(a,G):self.a,self.b=a.a,a.b
  else:self.a,self.b=F(a),F(b)
 def __add__(self,x):x=G(x);return G(self.a+x.a,self.b+x.b)
 __radd__=__add__
 def __neg__(self):return G(-self.a,-self.b)
 def __sub__(self,x):return self+-G(x)
 def __rsub__(self,x):return G(x)+-self
 def __mul__(self,x):x=G(x);return G(self.a*x.a-self.b*x.b,self.a*x.b+self.b*x.a)
 __rmul__=__mul__
 def __truediv__(self,x):
  x=G(x);den=x.a*x.a+x.b*x.b
  assert den
  return self*G(x.a/den,-x.b/den)
 def __rtruediv__(self,x):return G(x)/self
 def __eq__(self,x):x=G(x);return self.a==x.a and self.b==x.b
 def __ne__(self,x):return not self==x
 def __str__(self):return str(self.a)+'+('+str(self.b)+')i'
def mm(a,b):return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]
def mv(a,v):return [sum(x*y for x,y in zip(row,v)) for row in a]
def plus(a,b):return [[x+y for x,y in zip(row,col)] for row,col in zip(a,b)]
def scale(a,c):return [[x*c for x in row] for row in a]
def zero():return [[G() for _ in range(4)] for _ in range(4)]
def eye():return [[G(i==j) for j in range(4)] for i in range(4)]
def rank(a):
 a=[r[:] for r in a];n=0
 for j in range(len(a[0])):
  k=next((k for k in range(n,len(a)) if a[k][j]!=0),None)
  if k is None:continue
  a[n],a[k]=a[k],a[n];p=a[n][j];a[n]=[v/p for v in a[n]]
  for k in range(len(a)):
   if k!=n:
    p=a[k][j];a[k]=[x-p*y for x,y in zip(a[k],a[n])]
  n+=1
  if n==len(a):break
 return n
sites=[G(1),G(-1),G(0,1),G(0,-1)];u=[G(1)]*4
V0=[-1/z for z in sites];V1=[1/(z*z) for z in sites];V2=[(z-1)/(z*z*z) for z in sites]
assert V0==[G(-1),G(1),G(0,1),G(0,-1)]
assert V1==[G(1),G(1),G(-1),G(-1)]
assert V2==[G(0),G(2),G(-1,-1),G(-1,1)]
assert all(sum(v)==0 for v in [V0,V1,V2]) and rank([u,V0,V1,V2])==4
Hs=[]
for i in range(4):
 H=zero()
 for j in range(4):
  if i==j:continue
  O=scale(eye(),F(1,2));O[i][i]=O[j][j]=G(F(-1,2));O[i][j]=O[j][i]=G(1)
  H=plus(H,scale(O,1/(sites[i]-sites[j])))
 Hs.append(H)
P0=[[G(F(1,4)) for _ in range(4)] for _ in range(4)];Q=plus(eye(),scale(P0,-1))
N=mm(plus(Hs[0],scale(eye(),F(1,4))),Q);N2=mm(N,N)
assert mv(N,V0)==[G()]*4 and mv(N,V1)==V0 and mv(N,V2)==V1
assert mm(N2,N)==zero() and N2!=zero() and rank(N)==2 and rank(N2)==1
for z,H in zip(sites,Hs):
 E0=3/(4*z);E=-1/(4*z);c1=1/(z*z);c2=(z-1)/(z*z*z)
 rebuilt=plus(plus(scale(P0,E0),scale(Q,E)),plus(scale(N,c1),scale(N2,c2)))
 assert rebuilt==H
 Nj=mm(plus(H,scale(eye(),-E)),Q)
 assert mm(mm(Nj,Nj),Nj)==zero() and rank(Nj)==2 and rank(mm(Nj,Nj))==1
 assert mv(H,u)==[E0*x for x in u]
record={'id':'S014','status':'passed','method':'Independent construction from pair-site action, exact Gaussian rational arithmetic','jet_basis':[[str(x) for x in v] for v in [u,V0,V1,V2]],'basis_rank':4,'base_nilpotent_ranks':[rank(N),rank(N2),0],'all_four_Hamiltonians':'Each reconstructed exactly as vacuum projector plus critical projector and c1*N+c2*N^2; c1 nonzero. All four have critical nilpotent ranks2,1,0.'}

# Independent eight-site characteristic check: direct determinants at nine
# rational points, rather than the producer's Newton/trace algorithm.
def determinant(A):
 A=[row[:] for row in A];answer=G(1);n=len(A)
 for j in range(n):
  pivot=next((k for k in range(j,n) if A[k][j]!=0),None)
  if pivot is None:return G()
  if pivot!=j:A[j],A[pivot]=A[pivot],A[j];answer=-answer
  pp=A[j][j];answer=answer*pp
  for k in range(j+1,n):
   ratio=A[k][j]/pp
   for ell in range(j+1,n):A[k][ell]=A[k][ell]-ratio*A[j][ell]
   A[k][j]=G()
 return answer
sites8=sites+[2*z for z in sites];H8=[[G() for _ in range(8)] for _ in range(8)]
for j in range(1,8):
 O=[[G(F(1,2)) if a==b else G() for b in range(8)] for a in range(8)]
 O[0][0]=O[j][j]=G(F(-1,2));O[0][j]=O[j][0]=G(1)
 H8=plus(H8,scale(O,1/(sites8[0]-sites8[j])))
assert sum(F(1,2)/(sites8[0]-sites8[j]) for j in range(1,8))==G(F(37,60))
det_values=[]
for ll in range(-4,5):
 A=[[G(ll*(a==b))-H8[a][b] for b in range(8)] for a in range(8)]
 actual=determinant(A)
 q=F(ll)-F(37,60)
 expected=(F(ll)-F(37,60))*(F(ll)+F(23,60))**3*(17*q**4-2*(q+1)**4)/15
 assert actual==G(expected)
 det_values.append({'lambda':ll,'determinant':str(actual)})
record['eight_site_independent_characteristic']={'method':'Exact Gaussian-rational elimination at nine distinct rational spectral values proves equality of degree-eight monic polynomials, independently of Newton identities.','values':det_values,'factorization':'(lambda−37/60)(lambda+23/60)^3 [17q^4−2(q+1)^4]/15, q=lambda−37/60'}
record['checks']=[
 {'id':'S014','name':'Independent quartic complete Jordan certificate','status':'passed','detail':'Exact Q(i) pair-site reconstruction of all four Hamiltonians, jet basis rank4, full operator reconstruction and common nilpotent ranks2,1,0.'},
 {'id':'S014','name':'Independent eight-site characteristic polynomial by determinants','status':'passed','detail':'Nine exact Gaussian-rational determinant evaluations prove the degree-eight factorization independently of the producer’s Newton/trace algorithm. Full values retained in this certificate.'}
]
Path(__file__).resolve().parent.joinpath('independent_s014_checks.json').write_text(json.dumps(record,ensure_ascii=False,indent=2))
print(json.dumps({'id':'S014','independent_quartic_check':'passed','field':'Q(i)','basis_rank':4,'nilpotent_ranks':[2,1,0],'eight_site_determinants_checked':9}))
