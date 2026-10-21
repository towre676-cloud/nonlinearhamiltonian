#!/usr/bin/env python3
"""Exact independent fixtures for structural Moyal-partner theorems (stdlib)."""
from fractions import Fraction as Q
from math import comb, factorial
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent
CHECKS=[]
def record(name,**details):CHECKS.append(dict(name=name,status='passed',details=details))
def trim(P):return {e:Q(a) for e,a in P.items() if a}
def add(*polys):
 out={}
 for P in polys:
  for e,a in P.items():out[e]=out.get(e,0)+a
 return trim(out)
def scale(P,a):return trim({e:a*v for e,v in P.items()})
def mul(P,R):
 out={}
 for (a,b),v in P.items():
  for (c,d),w in R.items():out[a+c,b+d]=out.get((a+c,b+d),0)+v*w
 return trim(out)
def power(P,n):
 out={(0,0):Q(1)}
 for _ in range(n):out=mul(out,P)
 return out
def fall(n,k):return factorial(n)//factorial(n-k) if n>=k else 0
def deriv(P,a,b):return trim({(c-a,d-b):v*fall(c,a)*fall(d,b) for (c,d),v in P.items() if c>=a and d>=b})
def lam(H,G,k):return add(*(scale(mul(deriv(H,k-j,j),deriv(G,j,k-j)),(-1)**j*comb(k,j)) for j in range(k+1)))
def exact(H,G):
 m=min(max((sum(e) for e in H),default=0),max((sum(e) for e in G),default=0))
 return all(not lam(H,G,k) for k in range(3,m+1,2))
def rank(A):
 if not A:return 0
 A=[[Q(x) for x in row] for row in A];m=len(A);n=len(A[0]);r=0
 for c in range(n):
  pivot=next((i for i in range(r,m) if A[i][c]),None)
  if pivot is None:continue
  A[pivot],A[r]=A[r],A[pivot];v=A[r][c];A[r]=[x/v for x in A[r]]
  for i in range(m):
   if i!=r and A[i][c]:
    v=A[i][c];A[i]=[x-v*y for x,y in zip(A[i],A[r])]
  r+=1
  if r==m:break
 return r
def kernel_dimension(images,n):
 keys=sorted(set(k for P in images for k in P));return n-rank([[P.get(k,0) for P in images] for k in keys])
q={(1,0):Q(1)};p={(0,1):Q(1)};one={(0,0):Q(1)}
def ppoly(coeffs):return trim({(0,d):Q(v) for d,v in enumerate(coeffs)})
def shiftq(P,c):return {(a+c,b):v for (a,b),v in P.items()}
# General qF classification, including an irreducible quadratic cube F''.
fixtures=[
 ('quadratic',ppoly([3,2,1]),None),
 ('cubic',ppoly([1,3,2,1]),None),
 ('quartic',ppoly([1,0,1,0,1]),None),
 ('quintic-cube',ppoly([0,1,0,0,0,1]),p),
 ('quintic-generic',ppoly([0,1,0,1,0,1]),None),
 ('degree-eight-cube',ppoly([0,0,140,0,70,0,28,0,5]),add(power(p,2),one)),
]
D=8;classified=0;dynamic=0
for label,F,R in fixtures:
 M=max(b for a,b in F);H=mul(q,F);y=deriv(F,0,2)
 if R is not None:
  cube=power(R,3);e=next(iter(cube));gamma=y[e]/cube[e];assert y==scale(cube,gamma)
 for c in range(15):
  images=[]
  for d in range(D+1):
   G={(c,d):Q(1)};im={}
   for k in range(3,M+2,2):
    for exp,a in lam(H,G,k).items():im[(k,)+exp]=a
   images.append(im)
  dim=kernel_dimension(images,D+1)
  if c<=1:expected=D+1;A=None
  elif M==2:expected=1;A=one
  elif M==3 and c%3==2:
   r=(c-2)//3;A=power(y,r);expected=int(r<=D)
  elif M>=4 and c==2:expected=1;A=one
  elif M>=4 and c==3 and R is not None:expected=1;A=R
  else:expected=0;A=None
  assert dim==expected,(label,c,dim,expected)
  if A is not None and expected:
   G=shiftq(A,c);assert exact(H,G)
   # Every exceptional q-degree>=2 partner exits E after one Poisson action.
   DG=lam(H,G,1);assert not exact(H,DG),(label,c)
   dynamic+=1
  classified+=1
 # The infinite low transverse-degree strip is invariant and pairwise exact.
 for i in range(5):
  for j in range(5):
   G={(i%2,i):Q(1)};K={(j%2,j):Q(1)}
   assert exact(H,G) and exact(G,K) and exact(H,lam(H,G,1))
record('Complete qF bounded kernel dimensions agree with theorem',Hamiltonians=len(fixtures),q_degrees=15,p_degree_bound=D,cases=classified)
record('Every exceptional qF basis partner exits after one classical action',partners=dynamic)
record('Coordinate algebra pairwise exactness and invariant-strip checks',pairs=150)
# Cubic homogeneous degreewise kernel dimensions: all factor-multiplicity types.
cubics=[power(q,3),mul(power(q,2),p),add(power(q,3),power(p,3)),mul(mul(q,p),add(q,p)),add(power(q,3),scale(mul(q,power(p,2)),-3))]
cubiccases=0
for H in cubics:
 for n in range(16):
  basis=[{(i,n-i):Q(1)} for i in range(n+1)]
  dim=kernel_dimension([lam(H,G,3) for G in basis],n+1)
  assert dim==min(n+1,3),(H,n,dim);cubiccases+=1
record('Every nonzero binary cubic has Hilbert function min(n+1,3)',Hamiltonians=len(cubics),degrees=16,cases=cubiccases)
# Arbitrary one-coordinate Hamiltonians: exactness iff transverse degree<=2.
for F in [ppoly([0,0,0,1]),ppoly([1,3,0,2,0,1]),ppoly([0,0,1,0,0,0,1])]:
 for c in range(7):
  for d in range(7):assert exact(F,{(c,d):Q(1)})==(c<=2)
record('Univariate Hamiltonian full transverse-strip classification',monomial_cases=147)
# Explicit closure/dynamics counterexamples.
H=mul(q,power(p,3));G=power(q,2);K=mul(power(q,2),p)
assert exact(power(p,3),G) and exact(power(p,3),K)
assert not exact(power(p,3),mul(G,q))
assert not exact(power(p,3),lam(G,K,1))
DG=lam(H,G,1);assert DG==scale(mul(power(q,2),power(p,2)),-6)
assert lam(H,DG,3)==scale(power(p,2),-432)
record('Exact partner spaces need not be multiplicative, Lie closed or dynamically invariant',second_action_correction='18 hbar^2 p^2')
# Affine symplectic substitution and nonlinear canonical failure.
P=add(p,power(q,2));Hs=power(P,3);Gs=mul(power(q,2),P)
assert lam(Hs,Gs,3)==scale(q,-72)
assert all(not lam(Hs,Gs,k) for k in [5,7,9])
record('Nonlinear canonical shear does not preserve naive Weyl symbols',Lambda3='-72q',normalized_correction='3 hbar^2 q')
# Separable Hamiltonians always have the finite biquadratic exact sector.
Hs=add(power(q,7),scale(power(p,6),3))
for a in range(3):
 for b in range(3):assert exact(Hs,{(a,b):Q(1)})
record('Separable potentials have a biquadratic exact sector',basis_dimension=9)
result=dict(status='passed',check_count=len(CHECKS),scope='Exact rational polynomial fixtures; proofs supply unrestricted classification.',checks=CHECKS)
(ROOT/'checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(status=result['status'],checks=len(CHECKS),classified_kernel_cases=classified,cubic_kernel_cases=cubiccases)))
