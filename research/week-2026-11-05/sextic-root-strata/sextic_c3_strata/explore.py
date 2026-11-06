"""Exact falling-factorial matrix producer; independent replay is verify.py."""
import sympy as s
from math import comb,prod
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
b,c,d,e=s.symbols('b c d e')
H={(2,4):1,(3,3):b,(4,2):c,(5,1):d,(6,0):e}
def mat(H,n):
 cols=[]
 for j in range(n+1):
  G={(j,n-j):1};DG=gate(H,G,1);col={}
  for depth,P in [(0,G),(1,DG)]:
   for k in [3,5]:
    for key,z in gate(H,P,k).items():col[(depth,k,*key)]=z
  cols.append(col)
 keys=sorted(set().union(*(set(C) for C in cols)))
 return keys,s.Matrix([[C.get(k,0) for C in cols] for k in keys])
if __name__=='__main__':
 keys,M=mat(H,2)
 for key,row in zip(keys,M.tolist()):print(key,[s.factor(z) for z in row])
