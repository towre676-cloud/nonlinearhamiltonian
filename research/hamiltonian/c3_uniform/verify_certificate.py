"""Independent verifier. Uses literal derivatives and Leibniz determinants.
Does not import the producer, its gate formula, or a matrix determinant routine.
"""
import itertools,json
from pathlib import Path
import sympy as s
q,p,a=s.symbols('q p a'); H=q**6+a*q**3*p**3+p**6
HERE=Path(__file__).resolve().parent

def T(F,G,k):
 return s.Poly(s.expand(sum((-1)**j*s.binomial(k,j)*s.diff(F,q,k-j,p,j)*s.diff(G,q,j,p,k-j) for j in range(k+1))),q,p)

def leibniz(M):
 k=len(M);answer=0
 for perm in itertools.permutations(range(k)):
  if any(M[i][perm[i]]==0 for i in range(k)):continue
  sign=(-1)**sum(perm[i]>perm[j] for i in range(k) for j in range(i+1,k))
  answer+=sign*s.prod(M[i][perm[i]] for i in range(k))
 return s.expand(answer)

def verify(data):
 assert data['format']=='sextic-c3-bezout-v1'
 expected={(n,r) for n in range(1,17) for r in range(3) if any(c!=6 or n!=6 for c in range(r,n+1,3))}
 assert {(b['n'],b['residue']) for b in data['blocks']}==expected
 assert len(data['blocks'])==len(expected)
 nminors=0
 for b in data['blocks']:
  n,r=b['n'],b['residue']
  mons=[(c,n-c) for c in range(r,n+1,3) if not(n==6 and c==6)]
  assert b['columns']==[list(m) for m in mons]
  cols=[]
  for c,e in mons:
   G=q**c*p**e; DG=s.diff(H,q)*s.diff(G,p)-s.diff(H,p)*s.diff(G,q)
   col={}
   for depth,F in ((0,G),(1,DG)):
    for k in (3,5):
     col.update({(depth,k,*ex):v for ex,v in T(H,F,k).terms() if v})
   cols.append(col)
  keys=sorted(set().union(*(set(col) for col in cols)))
  assert b['row_keys']==[list(key) for key in keys]
  M=[[col.get(key,0) for col in cols] for key in keys]
  total=0
  assert len(b['minors'])==len(b['bezout'])
  for record,weight in zip(b['minors'],b['bezout']):
   idx=record['rows'];assert len(idx)==len(mons) and len(set(idx))==len(idx)
   d=leibniz([M[i] for i in idx]);assert s.expand(d-s.sympify(record['det']))==0,(n,r,idx)
   total+=s.sympify(weight)*d;nminors+=1
  assert s.expand(total-1)==0,(n,r,'Bezout')
 # Lower bounds: these elements are killed by D itself.
 assert T(H,1,3).is_zero and T(H,H,3).is_zero and T(H,H,5).is_zero
 assert s.expand(s.diff(H,q)*s.diff(H,p)-s.diff(H,p)*s.diff(H,q))==0
 return {'status':'passed','blocks':len(expected),'independently_verified_minors':nminors,'parameter_scope':'all complex a','degrees':'0..16','first_refined_kernel':'span{1,H_a}'}
if __name__=='__main__':
 result=verify(json.loads((HERE/'family_certificate.json').read_text()))
 (HERE/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
