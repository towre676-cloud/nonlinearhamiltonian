from engine import *
from pathlib import Path
import json
q=monomial(1,0);p=monomial(0,1);one=monomial(0,0)
fixtures=[('three coordinate roots',[(q,1),(p,1),(add(q,p),1)]),('double and single',[(q,2),(p,1)]),('triple',[(q,3)]),('three oblique roots',[(add(q,scale(p,2)),1),(add(scale(q,2),scale(p,-1)),1),(add(scale(q,3),p),1)]),('oblique double',[(add(q,scale(p,2)),2),(add(scale(q,2),scale(p,-1)),1)])]
checks=0;rows=[]
for label,roots in fixtures:
 H=one
 for ell,m in roots:H=multiply(H,power(ell,m))
 H=add(H,power(q,2),scale(q,5),scale(p,7),one)
 for n in range(17):
  candidates=[]
  for ell,m in roots:
   a=ell.get((1,0),F(0));b=ell.get((0,1),F(0));t=scale(p,1/a) if a else scale(q,-1/b)
   for j in range(min(m-1,n)+1):
    G=multiply(power(t,j),power(ell,n-j));assert exact_partner(H,G);checks+=1;candidates.append(G)
  vectors=[[G.get((n-j,j),F(0)) for G in candidates] for j in range(n+1)]
  rank=len(candidates)-len(nullspace(vectors,len(candidates)));expected=min(n+1,3)
  assert rank==expected==len(homogeneous_kernel(H,n));checks+=2
 rows.append({'fixture':label,'degrees_checked':[0,16],'lower_terms_added':'q²+5q+7p+1'})
result={'status':'passed','exact_assertions':checks,'scope':'all-degree root-multiplicity theorem in cubic_appendix.md; independent finite direct-star and rank checks','fixtures':rows}
Path(__file__).with_name('cubic_checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'status':'passed','exact_assertions':checks}))
