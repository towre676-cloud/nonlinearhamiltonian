"""Symbolic all-exponent identities and exhaustive exact bounded regression."""
import json
from pathlib import Path
from math import comb,prod
import sympy as s
c,e=s.symbols('c e',integer=True)
HERE=Path(__file__).resolve().parent
def ff(x,k):return s.prod(x-i for i in range(k))
def psi(A,B,k,x=c,y=e):return s.expand(sum((-1)**j*comb(k,j)*ff(A,k-j)*ff(B,j)*ff(x,j)*ff(y,k-j) for j in range(k+1)))

def static(A,B,x,y):
 if B==0:return y<=2
 if B==1:return y<=1 or (x,y) in [(0,2),(1,3)]
 if B==2:return y==0 or (x,y) in [(0,1),(0,2),(1,1),(4,2)]
 return x==y or (x,y) in [(0,1),(0,2),(1,0),(2,0),(1,11),(11,1)]
def core(A,B,x,y):
 if B==0:return y<=2
 if B==1:return y<=1
 if B==2:return (x,y) in [(0,0),(1,1),(4,2)]
 return x==y

def run():
 expected={
 (6,0):(120*e*(e-1)*(e-2),720*ff(e,5)),
 (5,1):(-60*e*(e-1)*(c-e+2),-120*ff(e,4)*(5*c-e+4)),
 (4,2):(24*e*(c*c-3*c*e+2*c+e*e-3*e+2),240*c*e*(e-1)*(e-2)*(2*c-e+1)),
 (3,3):(-6*(c-e)*(c*c-8*c*e-3*c+e*e-3*e+2),-360*c*e*(c-1)*(c-e)*(e-1))}
 report={'format':'monomial-c3-symbolic-v1','identities':[],'noncore_gate_values':[]}
 for (A,B),(p3,p5) in expected.items():
  assert s.expand(psi(A,B,3)-p3)==0 and s.expand(psi(A,B,5)-p5)==0
  report['identities'].append({'A':A,'B':B,'psi3':str(s.factor(p3)),'psi5':str(s.factor(p5))})
 # Algebraic substitutions used to exhaust the zero loci of the factored psi5.
 Q=expected[4,2][0]/(24*e)
 assert s.expand(Q.subs(e,2*c+1)+c*(c+3))==0
 assert s.expand(Q.subs(c,0)-(e-1)*(e-2))==0
 assert s.expand(Q.subs(e,1)-c*(c-1))==0
 assert s.expand(Q.subs(e,2)-c*(c-4))==0
 # Infinite noncore ray q^c for H=q^4 p^2: exact all-c first gate.
 value=s.expand(-2*c*psi(4,2,3,c+3,1))
 assert s.expand(value+48*c*(c+2)*(c+3))==0
 report['q4p2_qc_first_gate']=str(s.factor(value))
 for A,B,extras in [(5,1,[(0,2),(1,3)]),(4,2,[(0,1),(0,2)]),(3,3,[(0,1),(0,2),(1,0),(2,0),(1,11),(11,1)])]:
  for x,y in extras:
   v=(A*y-B*x)*psi(A,B,3,x+A-1,y+B-1)
   assert v!=0
   report['noncore_gate_values'].append({'A':A,'B':B,'c':x,'e':y,'T3D_coefficient':str(v)})
 # Full monomial grid uses direct integer sums, including reflections.
 tests=0
 for A in range(7):
  B=6-A
  for x in range(81):
   for y in range(81-x):
    def coeff(k,u,v):return sum((-1)**j*comb(k,j)*prod(A-i for i in range(k-j))*prod(B-i for i in range(j))*prod(u-i for i in range(j))*prod(v-i for i in range(k-j)) for j in range(k+1))
    st=all(coeff(k,x,y)==0 for k in [3,5])
    delta=A*y-B*x
    refined=st and (delta==0 or all(coeff(k,x+A-1,y+B-1)==0 for k in [3,5]))
    AA,BB,xx,yy=(A,B,x,y) if A>=B else (B,A,y,x)
    assert st==static(AA,BB,xx,yy),(A,B,x,y,'static')
    assert refined==core(AA,BB,xx,yy),(A,B,x,y,'refined')
    tests+=1
 report.update(status='passed',regression_monomials=tests,max_total_degree=80)
 (HERE/'monomial_certificate.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps(report))
if __name__=='__main__':run()
