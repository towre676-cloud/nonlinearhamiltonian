#!/usr/bin/env python3
"""Stdlib proof-certificate and regression replay for monomial classification."""
from pathlib import Path
from math import comb,factorial
import json
from classification import S,exact,poisson,balanced_member,classify_unequal,correction_polynomial,peval
ROOT=Path(__file__).resolve().parent
CHECKS=[]
def check(name,condition,details=None):
 assert condition,name
 CHECKS.append({'name':name,'status':'passed','details':details})
# Sparse formal polynomials in three indeterminates. These coefficient checks
# establish identities for indeterminates, rather than testing sample values.
N=3
class P(dict):
 def __add__(self,o):
  o=coerce(o);r=P(self)
  for e,c in o.items():r[e]=r.get(e,0)+c
  return P({e:c for e,c in r.items() if c})
 __radd__=__add__
 def __neg__(self):return P({e:-c for e,c in self.items()})
 def __sub__(self,o):return self+-coerce(o)
 def __rsub__(self,o):return coerce(o)+-self
 def __mul__(self,o):
  o=coerce(o);r={}
  for e,c in self.items():
   for f,d in o.items():
    ef=tuple(ei+fi for ei,fi in zip(e,f));r[ef]=r.get(ef,0)+c*d
  return P({e:c for e,c in r.items() if c})
 __rmul__=__mul__
 def __pow__(self,n):
  r=coerce(1)
  for _ in range(n):r=r*self
  return r

def coerce(x):return x if isinstance(x,P) else P({(0,0,0):x}) if x else P()
def var(i):return P({tuple(int(j==i) for j in range(N)):1})
def ff(x,k):
 r=coerce(1)
 for j in range(k):r=r*(coerce(x)-j)
 return r

def SP(a,b,c,d,k):return sum(((-1)**j*comb(k,j))*ff(a,k-j)*ff(b,j)*ff(c,j)*ff(d,k-j) for j in range(k+1))
m,c,d=[var(i) for i in range(3)];n=c+d;t=c*d
Q=(m-2)*(n-1)*(n-2)-2*(2*m-1)*t
P5=(m-3)*(m-4)*(n-1)*(n-2)*(n-3)*(n-4)-4*(2*m-3)*((m-3)*n*n-5*(m-4)*n+5*(2*m-7))*t+4*(2*m-1)*(2*m-3)*t*t
check('Formal balanced S3 factorization',SP(m,m,c,d,3)==m*(m-1)*(d-c)*Q)
check('Formal balanced S5 factorization',SP(m,m,c,d,5)==m*(m-1)*(m-2)*(d-c)*P5)
m,n,t=[var(i) for i in range(3)]
Q=(m-2)*(n-1)*(n-2)-2*(2*m-1)*t
P5=(m-3)*(m-4)*(n-1)*(n-2)*(n-3)*(n-4)-4*(2*m-3)*((m-3)*n*n-5*(m-4)*n+5*(2*m-7))*t+4*(2*m-1)*(2*m-3)*t*t
R=(2*m-3)*(m*n*n-7*m*n-4*m*t+18*m-4*n*n+34*n+2*t-66)
check('Formal balanced elimination certificate',(2*m-1)*P5+3*(n-1)*(n-2)*(2*m+n-7)*(2*m*m+m*n-6*m-4*n+12)==Q*R)
a,b,r=[var(i) for i in range(3)]
check('Formal ordinary-power obstruction',SP(a,b,a*r,b*r,3)==-2*a*b*r*(a-b)*(r-1)*((a+b)*(r+1)-3))
check('Correct even-line nonzero constant certificate',SP(a,b,-1,-1,3)==-6*(a-b)*(a*a+b*b-3*(a+b)+2))
# Highest corrections: exact polynomial identity in partner exponents for each
# Hamiltonian in the complete table, including swapped exponents.
c,d=var(0),var(1)
for a in range(2,13):
 for b in range(2,13):
  D=a+b
  lhs=SP(a,b,c,d,D if D%2 else D-1)
  if D%2:rhs=(-1)**b*factorial(D)*ff(c,b)*ff(d,a)
  else:rhs=(-1)**(b-1)*factorial(D-1)*ff(c,b-1)*ff(d,a-1)*(b*(d-a+1)-a*(c-b+1))
  check(f'Highest correction formal identity {a},{b}',lhs==rhs)
# Closed balanced theorem versus the independently evaluated defining sums.
count=0
for m in range(2,17):
 for c in range(71):
  for d in range(71):
   assert balanced_member(m,c,d)==exact(m,m,c,d),(m,c,d)
   count+=1
check('Balanced theorem defining-sum grid',True,{'cases':count,'m':[2,16],'partner_exponents':[0,70],'scope':'regression; universal proof in proofs.md'})
# Complete unequal table rebuilt and compared exactly; bounded defining-sum
# grid is an independent implementation cross-check, not the completeness proof.
table=json.loads((ROOT/'complete_table_2_to_12.json').read_text())['records'];count=0
for expected in table:
 a,b=expected['hamiltonian'];record=classify_unequal(a,b)
 assert record==expected
 finite={tuple(x) for x in record['finite_basis_exponents']}
 mirrored={tuple(x) for x in classify_unequal(b,a)['finite_basis_exponents']}
 assert mirrored=={(d,c) for c,d in finite}
 for c in range(61):
  for d in range(61):
   predicted=(c,d) in finite or ('p' in record['infinite_coordinate_algebras'] and c==0) or ('q' in record['infinite_coordinate_algebras'] and d==0)
   assert predicted==exact(a,b,c,d),(a,b,c,d,predicted)
   count+=1
check('All 55 complete unequal classifications and swapped symmetry',True,{'hamiltonians':55,'defining_sum_grid_cases':count,'partner_exponents':[0,60],'classification_scope':'all partner degrees via top-order/cubic theorem'})
check('Sextic exceptional degree twelve partners',exact(3,3,1,11) and exact(3,3,11,1) and poisson(3,3,1,11)==30 and poisson(3,3,11,1)==-30)
check('Quintic exceptional partner',classify_unequal(2,3)['finite_basis_exponents']==[[1,0],[1,1],[2,0],[2,3],[8,1]])
check('Degree ten exceptional partner',classify_unequal(2,8)['finite_basis_exponents']==[[1,0],[1,1],[2,0],[2,8],[3,1]])
check('Unequal noncommuting-power example',S(3,4,6,8,3)==864 and not exact(3,4,6,8))
result={'status':'passed','stdlib_only':True,'checks':CHECKS,'check_count':len(CHECKS),'scope':'formal polynomial certificates; complete cubic-root tables for 55 fixed Hamiltonians; bounded independent defining-sum regression grids; universal proofs in proofs.md'}
(ROOT/'checks.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':'passed','checks':len(CHECKS),'balanced_grid_cases':15*71*71,'unequal_grid_cases':55*61*61}))
