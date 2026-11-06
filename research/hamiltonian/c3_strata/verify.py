"""Independent literal-differentiation replay. Run with Python 3 + SymPy."""
import json
from pathlib import Path
import sympy as s
q,p,t=s.symbols('q p t')
def T(H,G,k):
 return s.expand(sum((-1)**j*s.binomial(k,j)*s.diff(H,q,k-j,p,j)*s.diff(G,q,j,p,k-j) for j in range(k+1)))
def D(H,G):return T(H,G,1)
def matrix(H,n):
 cols=[]
 for j in range(n+1):
  G=q**j*p**(n-j);col={}
  for depth,F in [(0,G),(1,D(H,G))]:
   for k in [3,5]:
    for (u,v),a in s.Poly(T(H,F,k),q,p).terms():
     if a:col[(depth,k,u,v)]=a
  cols.append(col)
 keys=sorted(set().union(*(set(c) for c in cols)))
 return keys,s.Matrix([[c.get(k,0) for c in cols] for k in keys])
HERE=Path(__file__).resolve().parent
def verify(recs=None, sample=None):
 if recs is None:recs=json.loads((HERE/'triple_certificate.json').read_text())
 count=0
 assert [r['n'] for r in recs]==list(range(1,17))
 H=q**3*p*(p-q)*(p-t*q)
 for rec in recs:
  keys,M=matrix(H,rec['n']);assert [list(k) for k in keys]==rec['row_keys']
  assert len(rec['minors'])==len(rec['bezout'])>0
  cols=[j for j in range(rec['n']+1) if not(rec['n']==6 and j==3)]
  assert cols==rec['columns'];M=M[:,cols];total=0
  for minor,w in zip(rec['minors'],rec['bezout']):
   val=M[minor['rows'],:].det(method='bareiss');assert s.expand(val-s.sympify(minor['det']))==0
   total+=s.sympify(w)*val;count+=1
  assert s.expand(total-1)==0
 print('triple-root certificates:',len(recs),'blocks,',count,'minors',flush=True)
 z=s.symbols('z');H=q**4*p**2+z*q**6;G=q*p
 assert T(H,G,3)==T(H,G,5)==T(H,D(H,G),3)==T(H,D(H,G),5)==0
 assert s.expand(D(H,G)-2*H-4*z*q**6)==0
 assert D(H,D(H,G))==-48*z*q**9*p
 assert T(H,D(H,D(H,G)),3)==-82944*z*q**10
 keys,M=matrix(H,2)
 assert M[:,1]==s.zeros(M.rows,1)
 assert M[[keys.index((1,3,4,2)),keys.index((1,3,6,0))],[0,2]].det()==11059200
 b,c,d,e=s.symbols('b c d e');H=q**2*(p**4+b*q*p**3+c*q**2*p**2+d*q**3*p+e*q**4)
 keys,M=matrix(H,2);v=s.Matrix([0,1,b/4]);R=dict(zip(keys,M*v))
 assert R[(1,3,0,6)]==0
 # The first row forces g0=0; the q2p4 row then forces g2=b*g1/4.
 assert M[keys.index((1,3,0,6)),0]==-1920
 assert list(M[keys.index((1,3,2,4)),1:])==[1440*b,-5760]
 sub={c:3*b**2/8,d:b**3/16,e:b**4/256}
 assert all(s.expand(x.subs(sub,simultaneous=True))==0 for x in M*v)
 assert s.expand(R[(1,3,3,3)]+480*(3*b*b-8*c))==0
 assert s.expand(R[(1,5,2,0)]-2880*(9*b**3-34*b*c+60*d))==0
 assert s.expand(R[(1,3,5,1)]+720*(b*b*c-8*b*d+32*e))==0
 print('symbolic double-root reduction and all-parameter counterexample: PASS',flush=True)
 if sample is None:sample=json.loads((HERE/'squarefree_sample.json').read_text())
 assert sample['factors']==list(range(1,7))
 assert s.discriminant(s.Poly(s.prod(q-i for i in sample['factors']),q).as_expr(),q)!=0
 assert [r['n'] for r in sample['records']]==list(range(1,17))
 F=s.prod(q-i*p for i in sample['factors'])
 assert s.expand(F-s.sympify(sample['H']))==0
 for rec in sample['records']:
  keys,M=matrix(F,rec['n'])
  cols=[j for j in range(rec['n']+1) if not(rec['n']==6 and j==6)]
  assert cols==rec['columns'] and len(rec['rows'])==len(cols)
  val=M[rec['rows'],cols].det(method='bareiss')
  assert val==int(rec['det']) and val!=0
 print('squarefree sample: 16 independent exact determinant replays PASS',flush=True)
 result={'status' :'PASS','triple_blocks':len(recs),'triple_minors':count,'counterexample':'H=q^4 p^2+q^6, G=qp','second_iterate_gate':'-82944 q^10'}
 return result
if __name__=='__main__':print(json.dumps(verify(),indent=2))
