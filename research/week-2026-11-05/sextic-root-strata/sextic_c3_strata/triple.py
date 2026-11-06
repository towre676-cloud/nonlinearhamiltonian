from explore import *
import json,random,itertools,time
t=s.symbols('t')
H={(3,3):1,(4,2):-(1+t),(5,1):t}
records=[]
for n in range(1,17):
 keys,M=mat(H,n)
 cs=[j for j in range(n+1) if not(n==6 and j==3)]
 M=M[:,cs];k=M.cols
 rng=random.Random(n);g=s.Integer(0);weights=[];ds=[]
 candidates=[]
 for v in [0,1,-1,2,3]:
  piv=list(M.subs(t,v).T.rref()[1]);candidates.append(piv)
 for it in range(100):
  idx=candidates[it] if it<len(candidates) else sorted(rng.sample(range(M.rows),k))
  if len(idx)!=k:continue
  det=s.Poly(M[idx,:].det(method='domain-ge'),t).as_expr()
  if det==0:continue
  u,v,ng=s.gcdex(g,det,t)
  if g!=0 and s.degree(ng,t)==s.degree(g,t):continue
  weights=[s.expand(u*w) for w in weights]+[v];ds.append({'rows':idx,'det':str(s.factor(det))});g=ng
  if g==1:break
 print(n,'gcd',s.factor(g),'minors',len(ds),flush=True)
 assert g==1
 records.append({'n':n,'columns':cs,'row_keys':keys,'minors':ds,'bezout':[str(w) for w in weights]})
open('triple_certificate.json','w').write(json.dumps(records,indent=2)+'\n')
