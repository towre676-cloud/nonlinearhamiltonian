from explore import *
import json
q,p=s.symbols('q p')
F=s.prod(q-i*p for i in range(1,7));H=dict(s.Poly(F,q,p).terms())
records=[]
for n in range(1,17):
 keys,M=mat(H,n);cols=[j for j in range(n+1) if not(n==6 and j==6)];M=M[:,cols]
 rows=list(M.T.rref()[1]);assert len(rows)==len(cols)
 val=M[rows,:].det(method='domain-ge');assert val!=0
 records.append({'n':n,'columns':cols,'rows':rows,'det':str(val)})
print('squarefree sample: 16 exact full-rank complements',flush=True)
open('squarefree_sample.json','w').write(json.dumps({'H':str(s.expand(F)),'factors':list(range(1,7)),'records':records},indent=2)+'\n')
