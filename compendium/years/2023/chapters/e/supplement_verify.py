#!/usr/bin/env python3
"""Exact rational certificates for S012; no external dependencies."""
from fractions import Fraction as F
from pathlib import Path
import json

HERE=Path(__file__).resolve().parent
checks=[]
def record(name,detail):checks.append(dict(id='S012',name=name,status='passed',detail=detail))
def mm(A,B):
 assert not A or not B or len(A[0])==len(B)
 return [[sum((a*b for a,b in zip(row,col)),F(0)) for col in zip(*B)] for row in A]
def tp(A):return list(map(list,zip(*A)))
def scale(A,c):return [[c*x for x in row] for row in A]
def plus(A,B):return [[a+b for a,b in zip(x,y)] for x,y in zip(A,B)]
def neg(A):return scale(A,-1)
def vector(x):return [[F(y)] for y in x]
def inner(x,y):return sum((a[0]*b[0] for a,b in zip(x,y)),F(0))
def diag(x):return [[F(a) if i==j else F(0) for j in range(len(x))] for i,a in enumerate(x)]
def penrose(A,G):
 assert mm(mm(A,G),A)==A and mm(mm(G,A),G)==G
 assert mm(A,G)==tp(mm(A,G)) and mm(G,A)==tp(mm(G,A))
def energy(Q,x):return inner(x,mm(Q,x))/2

Q=diag([2,0,3]);Qp=diag([F(1,2),0,F(1,3)])
B=[[F(1),F(1),F(0)],[F(0),F(1),F(1)]];z=vector([1,0])
P=scale([[F(1),F(-1)],[F(-1),F(1)]],F(1,2))
K=[[F(1),F(-1)],[F(-1),F(1)]]
raw=mm(mm(B,Qp),tp(B));H=mm(mm(P,raw),P);Hp=scale(K,F(6,5))
assert H==scale(K,F(5,24))
penrose(Q,Qp);penrose(H,Hp)
assert mm(P,P)==P and tp(P)==P
lam=mm(Hp,mm(P,z));r=mm(mm(mm(Qp,tp(B)),P),lam)
n=vector([0,F(2,5),0]);x=plus(r,n)
assert x==vector([F(3,5),F(2,5),F(-2,5)])
assert mm(B,x)==z and mm(Q,x)==mm(tp(B),lam)
primal=energy(Q,x)
dual=inner(lam,z)-inner(lam,mm(raw,lam))/2
assert primal==dual==F(3,5)
naive=energy(diag([2,3]),z)
assert naive==1 and naive!=primal
# Direct elimination is independent of the projector/pseudoinverse formula.
s=F(2,5);eliminated=1-2*s+F(5,2)*s*s
assert eliminated==primal
record('Nontrivial output-quotient counterexample','Q=diag(2,0,3), two-output B: Penrose equations, primal feasibility, stationarity and dual equality all exact. Correct energy 3/5; naive pseudoinverse value 1. Independent one-variable elimination agrees.')

# Conjugate and ridge error are exact rational calculations on rangeQ.
yR=vector([2,0,3]);finite=energy(Qp,yR)
assert finite==F(5,2)
epsilons=[F(1),F(1,2),F(1,10),F(1,100)]
ridge_values=[]
for eps in epsilons:
 inv=diag([1/(2+eps),1/eps,1/(3+eps)])
 fv=energy(inv,yR);gap=finite-fv
 assert 0<=gap<=eps*F(13,8)
 y=vector([2,1,3]);off=energy(inv,y)
 assert off-fv==1/(2*eps)
 ridge_values.append(dict(epsilon=str(eps),range_value=str(fv),nullspace_increment=str(off-fv)))
record('Ridge separation of range and nullspace',{'range_conjugate':str(finite),'exact_ridge_values':ridge_values,'range_error_bound':'epsilon*13/8','nullspace_divergence':'1/(2epsilon)'})

# A full-output infeasibility certificate, including a nontrivial nullspace.
Q0=diag([1,0]);B0=[[F(1),F(0)],[F(0),F(0)]];z0=vector([0,1]);w=vector([0,1])
assert mm(tp(B0),w)==vector([0,0]) and inner(w,z0)==1
record('Infeasibility by a dual separating direction','B=[[1,0],[0,0]], z=(0,1): B^T w=0 but w^T z=1 for w=(0,1). Thus no primal solution exists and the dual ray grows as t.')

# Parameter strata with nonnegative constraints; exact KKT checks prove sufficiency.
strata=[]
for t in [F(0),F(1,3),F(1),F(2),F(5)]:
 for a in [F(-3),F(-1),F(0),F(1,2),F(1),F(3)]:
  Qt=diag([1,t,0]);b=vector([1,1,a])
  if t==0:
   xx=vector([0,1,0]);ll=F(0);nu=vector([0,0,0]);value=F(0);label='rank_one'
  elif a>0:
   xx=vector([0,0,1/a]);ll=F(0);nu=vector([0,0,0]);value=F(0);label='positive_null_access'
  else:
   xx=vector([t/(1+t),1/(1+t),0]);ll=t/(1+t);nu=vector([0,0,-a*ll]);value=t/(2*(1+t));label='zero_coupling' if a==0 else 'negative_null_blocked'
  assert all(q[0]>=0 for q in xx) and inner(b,xx)==1
  assert all(q[0]>=0 for q in nu)
  assert mm(Qt,xx)==plus(scale(b,ll),nu)
  assert all(xx[i][0]*nu[i][0]==0 for i in range(3))
  assert energy(Qt,xx)==value
  # Dual vector entering the conjugate must belong to range(Qt).
  yy=plus(scale(b,ll),nu)
  if t:
   Qtp=diag([1,1/t,0]);assert yy[2][0]==0
  else:
   Qtp=diag([1,0,0]);assert yy[1][0]==yy[2][0]==0
  dual_value=ll-energy(Qtp,yy)
  assert dual_value==value
  # Equality-only comparison: nonnegative constraints block a<0 free solutions.
  if t>0 and a!=0:
   free=vector([0,0,1/a]);assert inner(b,free)==1 and energy(Qt,free)==0
  strata.append(dict(t=str(t),a=str(a),stratum=label,value=str(value),x=[str(q[0]) for q in xx],lambda_=str(ll),nu=[str(q[0]) for q in nu]))
record('Rank and active-constraint parameter strata',{'representative_points':len(strata),'certificates':strata,'scope':'Exact rational certificates at sample parameters; the text proves the formulas for all real parameters in each declared stratum.'})

# Test entire zero-cost sets at selected points, not only one optimizer.
for a in [F(-2),F(0),F(2)]:
 for s in ([F(0),F(1,4),F(1,2)] if a>0 else [F(0),F(1),F(10)]):
  xx=vector([0,1-a*s,s]);assert all(q[0]>=0 for q in xx)
  assert inner(vector([1,1,a]),xx)==1 and energy(diag([1,0,0]),xx)==0
for s in [F(0),F(1),F(7)]:
 xx=vector([F(2,3),F(1,3),s]);assert energy(diag([1,2,0]),xx)==F(1,3)
record('Degenerate optimizer sets','Sample points on the exact rank-one optimal segments/rays and the a=0 null-coordinate family remain feasible with the stated energy. Full optimizer-set formulas are proved in the text.')

out={'supplement':'S012','status':'passed','checks':checks,'count':len(checks),'method':'Python standard library exact fractions and polynomial identities; no numerical pseudoinverse or optimizer.'}
HERE.joinpath('supplement_checks.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
print(json.dumps({'supplement':'S012','status':'passed','checks':len(checks),'parameter_certificates':len(strata)}))
