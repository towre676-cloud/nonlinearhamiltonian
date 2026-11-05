"""Generate exact Bezout certificates: first refinement, every a, degrees 0..16."""
import json, random, itertools
from pathlib import Path
from math import comb, prod
import sympy as s
a=s.Symbol('a')
HERE=Path(__file__).resolve().parent

def fall(x,k):return prod(x-i for i in range(k))
def gate(H,G,k):
 out={}
 for (u,v),h in H.items():
  for (c,e),g in G.items():
   if u+c<k or v+e<k:continue
   z=sum((-1)**j*comb(k,j)*fall(u,k-j)*fall(v,j)*fall(c,j)*fall(e,k-j) for j in range(k+1))
   key=(u+c-k,v+e-k)
   out[key]=s.expand(out.get(key,0)+h*g*z)
 return {key:z for key,z in out.items() if z!=0}
H={(6,0):1,(3,3):a,(0,6):1}

def block(n,r):
 # q^6 coefficient of H is 1, so deleting it gives a complement for ALL a.
 mons=[(c,n-c) for c in range(r,n+1,3) if not(n==6 and c==6) and n!=0]
 columns=[]
 for m in mons:
  G={m:1}; DG=gate(H,G,1)
  col={}
  for depth,P in [(0,G),(1,DG)]:
   for k in (3,5):
    for key,z in gate(H,P,k).items():col[(depth,k,*key)]=z
  columns.append(col)
 keys=sorted(set().union(*(set(c) for c in columns))) if columns else []
 rows=[[col.get(key,0) for col in columns] for key in keys]
 return mons,keys,s.Matrix(rows) if rows else s.zeros(0,len(mons))

def certify(n,r):
 mons,keys,M=block(n,r); k=len(mons)
 if not k:return None
 # Each recorded minor is exact; Bezout sum makes rank uniform over C.
 rng=random.Random(100*n+r); g=s.Integer(0); records=[]; weights=[]; seen=set()
 initial=list(M.subs(a,1).T.rref()[1])
 assert len(initial)==k,(n,r,'rank fails at 1')
 candidates=itertools.chain([initial],(sorted(rng.sample(range(M.rows),k)) for _ in range(2500)),itertools.combinations(range(M.rows),k))
 for idx in candidates:
  idx=tuple(idx)
  if idx in seen:continue
  seen.add(idx)
  det=s.Poly(M[list(idx),:].det(method='domain-ge'),a).as_expr()
  if det==0:continue
  u,v,ng=s.gcdex(g,det,a)
  if s.degree(ng,a)==s.degree(g,a) and g!=0:continue
  weights=[s.expand(u*w) for w in weights]+[s.expand(v)]
  records.append({'rows':list(idx),'det':str(s.factor(det))});g=s.expand(ng)
  if s.degree(g,a)==0:break
 assert g==1,(n,r,g)
 assert s.expand(sum(w*s.sympify(rec['det']) for w,rec in zip(weights,records)))==1
 return {'n':n,'residue':r,'columns':[list(m) for m in mons], 'row_keys':[list(key) for key in keys], 'minors':records,'bezout':[str(w) for w in weights]}

def main():
 out=[]
 for n in range(17):
  for r in range(3):
   rec=certify(n,r)
   if rec:out.append(rec)
  print('certified',n,flush=True)
 data={'format':'sextic-c3-bezout-v1','base_commit':'660cf921e2836191aa3233d94094a274e836baa7','sympy':s.__version__,'blocks':out}
 (HERE/'family_certificate.json').write_text(json.dumps(data,indent=2)+'\n')
if __name__=='__main__':main()
