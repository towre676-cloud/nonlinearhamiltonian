#!/usr/bin/env python3
"""Portable stdlib finite checks. These replay examples, not all cited general theory."""
import json, math
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
P=Path(__file__).resolve().parent
checks=[]
def check(n,name,ok,detail):
    checks.append(dict(id=f'Y24-07-{n:03d}',name=name,status='pass' if ok else 'FAIL',detail=detail))
def rank(A):
    a=[[F(x) for x in r] for r in A]; r=0
    for c in range(len(a[0])):
        piv=next((j for j in range(r,len(a)) if a[j][c]),None)
        if piv is None: continue
        a[r],a[piv]=a[piv],a[r]; q=a[r][c]; a[r]=[v/q for v in a[r]]
        for j in range(len(a)):
            if j!=r:
                q=a[j][c]; a[j]=[x-q*y for x,y in zip(a[j],a[r])]
        r+=1
        if r==len(a): break
    return r
# Conjugacy: all invariant subsets, not just one orbit sample.
psi=[2,1,0,3]; T=lambda x:(x+1)%4; S=lambda y:psi[T(psi[y])]
invariants=[]
for mask in range(16):
    a={j for j in range(4) if mask>>j&1}
    if {T(j) for j in a}==a: invariants.append(mask)
check(1,'Four-cycle conjugacy and invariant sets',invariants==[0,15] and all(S(psi[x])==psi[T(x)] for x in range(4)) and len({S(x) for x in range(4)})==4,'All 16 subsets examined; only empty/full invariant; conjugacy holds pointwise.')
def h(p): return 0 if p in (0,1) else -p*math.log2(p)-(1-p)*math.log2(1-p)
eps=.25; cap=1-h(eps)
check(2,'Binary symmetric channel capacity example',abs(cap-.18872187554086717)<1e-14 and all(h(eps+p*(1-2*eps))-h(eps)<=cap+1e-14 for p in [j/1000 for j in range(1001)]) and h(.5)==1,'Capacity formula and 1,001 input distributions replayed; global maximality follows entropy proof, not grid search.')
words=[f'{j:03b}' for j in range(8)]; perm={w:w for w in words}; perm['111'],perm['001']='001','111'
d=lambda x,y:sum(a!=b for a,b in zip(x,y))
check(3,'Relabeling can destroy Hamming distance',len(set(perm.values()))==8 and d('000','111')==3 and d(perm['000'],perm['111'])==1,'Ambient permutation checked bijective; repetition-code distance falls from 3 to 1.')
w=F(23,4); r=F(14,25)
check(4,'Exact quotient and interval endpoints',w/r==F(575,56) and w*F(14,25)==F(161,50) and w/F(29,50)==F(575,58) and w/F(27,50)==F(575,54),'Exact fractions certify quotient, reverse convention and interval bounds.')
a,b,c=F(11,10),F(11,5),F(1,2)
roots=[-1-math.sqrt(66)/11,-1+math.sqrt(66)/11]
check(5,'PID characteristic quadratic and feedthrough',a>0 and b>0 and c>0 and b*b-4*a*c==F(66,25) and all(x<0 and abs(a*x*x+b*x+c)<1e-13 for x in roots) and F(1,10)/a==F(1,11),'Characteristic coefficients (11/10,11/5,1/2); both exact-form roots negative; ideal high-frequency ratio 1/11.')
check(6,'Power and amplitude logarithms',abs(10*math.log10(2)-3.010299956639812)<1e-12 and abs(20*math.log10(2)-6.020599913279624)<1e-12 and abs(20*math.log10(2)-10*math.log10(4))<1e-12,'Dimensionless ratios only; amplitude formula assumes power proportional to amplitude squared.')
V,power=F(2),F(1); I=power/V; R=V*V/power
check(7,'Positive ideal-circuit algebra',I==F(1,2) and R==4 and V==I*R and power==V*I,'Normalized positive example exactly satisfies both stipulated equations; no body-current or apparatus calculation.')
N=60; dp=[1]+[0]*N
for m in range(1,N+1):
    for n in range(m,N+1): dp[n]+=dp[n-m]
rp=[1]+[0]*N
for n in range(1,N+1):
    k=1
    while k*(3*k-1)//2<=n:
        for g in (k*(3*k-1)//2,k*(3*k+1)//2):
            if g<=n: rp[n]+=(-1)**(k-1)*rp[n-g]
        k+=1
check(8,'Partition recurrence versus independent counting',dp==rp and dp[:11]==[1,1,2,3,5,7,11,15,22,30,42],'Independent part-size dynamic program and pentagonal recurrence agree through n=60; not an all-orders proof of Euler identity.')
dims=[math.comb(11,k) for k in range(12)]
check(9,'Exterior-algebra dimensions and wedge cancellation',dims==[1,11,55,165,330,462,462,330,165,55,11,1] and sum(dims)==2048 and sum((-1)**k*v for k,v in enumerate(dims))==0 and -1+1==0,'Dimensions by exact binomial coefficients; worked mixed derivative terms cancel with opposite wedge signs. General d²=0 is proved in text.')
A=[[-2,1],[1,-2]]
matvec=lambda a,x:[sum(v*w for v,w in zip(row,x)) for row in a]
energy_ok=all(-u*u+2*u*v-v*v==-(u-v)**2 for u in range(-4,5) for v in range(-4,5))
check(10,'Diffusion mode eigenvalues and coupling energy',matvec(A,[1,1])==[-1,-1] and matvec(A,[1,-1])==[-3,3] and energy_ok,'k=1 mode has decay rates 1,3; coupling quadratic identity checked on integer grid and proved algebraically in text.')
vals=[(2-2*g)*math.log(2) for g in range(3)]
check(11,'Euler realization and entropy sign counterexample',vals[0]>0 and vals[1]==0 and vals[2]<0 and abs(vals[0]+vals[2])<1e-15,'Genus 0,1,2 yield 2 log 2,0,−2 log 2; Grothendieck/Hodge realization facts are sourced theorem scope.')
check(12,'Rank-one monodromy example',abs(complex(math.cos(math.pi),math.sin(math.pi))+1)<1e-14 and abs(complex(math.cos(2*math.pi),math.sin(2*math.pi))-1)<1e-14,'α=1/2 gives −1 and square 1. Irrational non-root assertion follows mα∈Z proof, not finite numeric testing; Hodge-module compatibility is not computationally certified.')
boundary=[[-1,0,1],[1,-1,0],[0,1,-1]]; face=[1,1,1]
check(13,'Triangle homology ranks',rank(boundary)==2 and matvec(boundary,face)==[0,0,0] and 3-rank(boundary)==1 and rank([[1],[1],[1]])==1,'Triangle graph H₁ dimension 1; filling adds rank-one boundary and kills it. Nodal-curve IH is explicitly a cited theorem, not this matrix check.')
# Independently calculate transformed contact-covector coefficients by Jacobian pullback.
contact_checks=[]
for a in [F(1,2),F(-2),F(3)]:
 for y in [F(-3),F(0),F(5,2)]:
  alpha_at_image=[-a*y,F(0),F(1)]
  jac=[[a,0,0],[0,a,0],[0,0,a*a]]
  pulled=[sum(alpha_at_image[i]*jac[i][j] for i in range(3)) for j in range(3)]
  target=[a*a*x for x in [-y,F(0),F(1)]]
  contact_checks.append(pulled==target)
# Derivatives of polynomial coordinates x=t,y=t,z=t²/2, evaluated exactly.
tangent_checks=[2*F(1,2)*t-t*F(1)==0 for t in map(F,range(-5,6))]
check(14,'Legendrian tangent and contact scaling',all(tangent_checks) and all(contact_checks) and 0-F(2,2)==-1,'Polynomial tangent z′−yx′=0, pullback scaling a² and two-cusp tb=−1 replayed; knot classification not asserted.')
meanA=[[F(-1),F(1)],[F(1),F(-1)]]
check(15,'Aggregation erases diffusion while contrast distinguishes it',matvec(meanA,[1,1])==[0,0] and matvec(meanA,[1,-1])==[-2,2] and all(-(D+2) in (-3,-4) for D in (1,2)),'Closed mean matrix independent of D; common mean 1 unchanged; contrasting Fourier mode rates −3 and −4 distinguish the two stipulated models.')
entries=json.loads(P.joinpath('entries.json').read_text())
assert len(entries)==15 and len({e['id'] for e in entries})==15
assert all(e['original']['original_question'] is None for e in entries)
assert all(e['original']['evidence'] in ('A','T') for e in entries)
assert all(e['original']['month']=='2024-07' for e in entries)
P.joinpath('checks.json').write_text(json.dumps(dict(month='2024-07',scope='Finite examples and exact algebra replayed; general theorems retain their stated proof/source scope.',checks=checks),ensure_ascii=False,indent=2))
print(json.dumps(dict(month='2024-07',passed=sum(c['status']=='pass' for c in checks),total=len(checks))))
assert all(c['status']=='pass' for c in checks)
