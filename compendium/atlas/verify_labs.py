#!/usr/bin/env python3
"""Independent algebraic fixtures for the ten finite atlas labs.

Python uses only its standard library. Node executes the actual browser engine.
Exact integer/fraction identities are used where applicable; transcendental
display values are compared with a declared floating-point tolerance.
"""
import collections
import hashlib
import itertools
import json
import math
import subprocess
from fractions import Fraction as Q
from pathlib import Path

BASE=Path(__file__).resolve().parent
ENGINE=BASE/'labs/engine.js'
CASES=[]
TOL=2e-12
def case(lab,params,expected,label,reject=False):
    CASES.append(dict(lab=lab,params=params,expected=expected,label=label,reject=reject))
def det(A):
    n=len(A)
    return sum((-1)**sum(p[i]>p[j] for i in range(n) for j in range(i+1,n))*math.prod(A[i][p[i]] for i in range(n)) for p in itertools.permutations(range(n)))
def gram_rank(rows):
    # Rank of a PSD Gram matrix is its largest nonsingular principal minor.
    G=[[sum(r[i]*r[j] for r in rows) for j in range(4)] for i in range(4)]
    for k in range(4,0,-1):
        if any(det([[G[i][j] for j in I] for i in I]) for I in itertools.combinations(range(4),k)):return k
    return 0

# L01: independent Gram-minor criterion, all 64 panels and both targets.
rows=[[1,0,0,0],[0,1,0,0],[1,1,0,0],[0,0,1,0],[0,0,0,1],[0,1,1,0]]
costs=[3,3,4,2,2,3]
for target,G in [('sum',[[1,1,0,0]]),('pair',[[1,0,0,0],[0,1,0,0]])]:
    fixture=[]
    for mask in range(64):
        H=[r for i,r in enumerate(rows) if mask&(1<<i)]
        r=gram_rank(H);s=gram_rank(H+G);cost=sum(c for i,c in enumerate(costs) if mask&(1<<i))
        fixture.append((r,s,cost))
    best=min(c for r,s,c in fixture if r==s)
    winners=[m for m,(r,s,c) in enumerate(fixture) if r==s and c==best]
    assert best==({'sum':4,'pair':6}[target])
    for mask,(r,s,c) in enumerate(fixture):
        case('L01',dict(mask=mask,target=target),dict(rank=r,joinedRank=s,identifies=r==s,cost=c,bestCost=best,bestMasks=winners),'Gram principal-minor row-space certificate')

# L02: generating-polynomial coefficients count feasible states independently;
# bit-address enumeration then checks every rank/unrank inverse.
weights=[2,3,4,5,6,7];values=[3,4,6,7,9,10]
poly={(0,0):1}
for w,v in zip(weights,values):
    new=collections.Counter(poly)
    for (a,b),n in poly.items():new[a+w,b+v]+=n
    poly=dict(new)
def knapsack_point(mask):
    return dict(mask=mask,weight=sum(w for i,w in enumerate(weights) if mask&(1<<i)),value=sum(v for i,v in enumerate(values) if mask&(1<<i)))
points=[knapsack_point(m) for m in range(64)]
for budget in range(28):
    feasible=[p for p in points if p['weight']<=budget]
    count=sum(n for (w,v),n in poly.items() if w<=budget)
    best=max(v for (w,v),n in poly.items() if w<=budget)
    assert count==len(feasible)
    winners=[p['mask'] for p in feasible if p['value']==best]
    for rank,p in enumerate(feasible):
        case('L02',dict(budget=budget,rank=rank,mask=p['mask']),dict(feasibleCount=count,optimalValue=best,optimalMasks=winners,rank=rank,selected=p,queryRank=rank,queryMask=p['mask']),'Generating polynomial plus rank-mask inversion')
    if budget in [0,12,27]:
        for mask,p in enumerate(points):
            position=next((i for i,a in enumerate(feasible) if a['mask']==mask),-1)
            case('L02',dict(budget=budget,mask=mask),dict(queryRank=position),'Feasible and infeasible address rank')

# L03: the exact mass-three polynomial is factored algebraically in the report.
def pmul(a,b):
    out=collections.Counter()
    for i,x in a.items():
        for j,y in b.items():out[i+j]+=x*y
    return {i:x for i,x in out.items() if x}
polynomial={3:1}
for factor in [{0:1,1:-1},{0:1,3:-1},{0:1,3:-1},{0:1,4:-1},{0:1,4:-1}]:polynomial=pmul(polynomial,factor)
for mass in range(7):
    expected=dict(configurations=math.comb(mass+6,6),binaryCensusEqual=True)
    case('L03',dict(total=mass,q=.5),expected,'Stars-and-bars configuration count and binary collision')
for q in [Q(0),Q(1,4),Q(1,2),Q(3,4),Q(1)]:
    exact=sum(Q(c)*q**e for e,c in polynomial.items())
    case('L03',dict(total=3,q=float(q)),dict(value=float(exact)),f'Exact factored difference at q={q}')

# L04: rational fixtures arise by setting delta=1/16 and exp(power)=2.
for mode in ['mild','severe']:
    for r in [1,2,3]:
        for n in [1,3,8]:
            power=2 if mode=='mild' else math.log(2)
            bias=Q(1,(n+1)**r)
            noise=Q(n*n,16) if mode=='mild' else Q(2**n,16)
            case('L04',dict(mode=mode,r=r,power=power,L=math.log(16),N=n),dict(delta=1/16,selected=dict(n=n,bias=float(bias),noise=float(noise),total=float(bias+noise))),'Closed rational bias-plus-noise bound')

# L05: closed shear commutator, and exact cosine-squared special angles.
for a,b in itertools.product(range(-3,4),repeat=2):
    matrix=[[1+a*b+a*a*b*b,-a*a*b],[a*b*b,1-a*b]]
    assert det(matrix)==1
    case('L05',dict(a=a,b=b),dict(commutator=matrix,determinant=1),'Closed shear commutator polynomial')
for angle,q in [(30,Q(3,4)),(45,Q(1,2)),(60,Q(1,4))]:
    n=1
    while q**n>Q(1,100):n+=1
    comm=math.sqrt(float(q*(1-q)))
    case('L05',dict(mode='projection',angle=angle,epsilon=.01),dict(contraction=float(q),commutatorNorm=comm,iterations=n,residualBound=float(q**n)),'Exact principal-angle contraction and minimal iteration count')

# L06: two independently derived witnesses and a higher-order cancellation family.
case('L06',dict(a=3,b=0,c=0,d=3),dict(terms=[dict(order=1,hbar=0,q=2,p=2,S='9',coefficient='9'),dict(order=3,hbar=2,q=0,p=0,S='36',coefficient='-3/2')],exact=False,thirdOrderZero=False),'q³,p³: bracket 9q²p²−3hbar²/2')
case('L06',{},dict(terms=[dict(order=1,hbar=0,q=5,p=7,S='-22',coefficient='-22'),dict(order=5,hbar=4,q=1,p=3,S='201600',coefficient='105')],thirdOrderZero=True,exact=False),'Third order vanishes while fifth order survives')
for r in range(21):
    coefficient=-8*r-6
    case('L06',dict(a=1,b=3,c=3*r+2,d=r),dict(exact=True,thirdOrderZero=True,terms=[dict(order=1,hbar=0,q=3*r+2,p=r+2,S=str(coefficient),coefficient=str(coefficient))]),'Exact qp³ cancellation family')

# L07: compare every positive divisor with abstract group-order fibre counts.
def phi(n):
    ans=n;p=2;m=n
    while p*p<=m:
        if m%p==0:
            ans=ans//p*(p-1)
            while m%p==0:m//=p
        p+=1
    if m>1:ans=ans//m*(m-1)
    return ans
for m in [d for d in range(1,1681) if 1680%d==0]:
    target=[a for a in range(m) if math.gcd(a,m)==1]
    assert len(target)==phi(m) and 384%phi(m)==0
    fibres={str(a):384//phi(m) for a in target}
    case('L07',dict(modulus=m),dict(conductor=1680,targetModulus=m,sourceUnits=384,targetUnits=phi(m),fibreSize=384//phi(m),uniform=True,fibres=fibres),'CRT quotient-group uniform fibres for every divisor')

# L08: enumerate compatible joint corners before taking separate ranges.
for C in [0,1,10,100]:
    for lo,hi in [(Q(7,4),Q(9,4)),(Q(-2),Q(-1)),(Q(-1),Q(2)),(Q(2),Q(1))]:
        lo,hi=sorted((lo,hi));corners=[(c+d,c) for c in [-C,C] for d in [lo,hi]]
        A=[min(a for a,b in corners),max(a for a,b in corners)];B=[min(b for a,b in corners),max(b for a,b in corners)]
        differences=[a-b for a,b in corners]
        expected=dict(difference=[float(min(differences)),float(max(differences))],A=list(map(float,A)),B=list(map(float,B)),AAlwaysLarger=min(differences)>0,BAlwaysLarger=max(differences)<0,intervalsOverlap=max(A[0],B[0])<=min(A[1],B[1]))
        case('L08',dict(common=C,lo=float(lo),hi=float(hi)),expected,'Joint-state cancellation and exact corner extrema')
case('L08',dict(common=3,lo=2,hi=1),dict(difference=[1,2]),'Reversed interval endpoints normalized')

# L09: connected graph cycle rank E−V+1; the filled triangle is a disk.
for mode,filled,V,E,F,betti in [('triangle',False,3,3,0,[1,1,0]),('triangle',True,3,3,1,[1,0,0]),('square',False,4,4,0,[1,1,0]),('k33',False,6,9,0,[1,4,0])]:
    case('L09',dict(mode=mode,filled=filled),dict(vertices=V,edges=E,faces=F,beta0=betti[0],beta1=betti[1],beta2=betti[2],boundaryRanks=[V-1,F],boundarySquaredZero=True),'Topological cycle rank and disk homology')

# L10: use the binomial expansion of (3±2sqrt(2))^n, not iteration.
def unit_power(n):
    k=abs(n)
    x=sum(math.comb(k,j)*3**(k-j)*2**j*2**(j//2) for j in range(0,k+1,2))
    y=sum(math.comb(k,j)*3**(k-j)*2**j*2**((j-1)//2) for j in range(1,k+1,2))
    return x,(-y if n<0 else y)
for seed in [(1,2),(5,4)]:
    for n in list(range(-20,21))+[-100,100]:
        a,b=unit_power(n);x=seed[0]*a+2*seed[1]*b;y=seed[0]*b+seed[1]*a
        assert x*x-2*y*y==-7
        case('L10',dict(seed=','.join(map(str,seed)),n=n),dict(x=str(x),y=str(y),norm='-7',step=n),'Independent binomial unit-power coordinates')

# Guards are tested only where the current engine explicitly supplies them.
for lab,params in [('L06',{'a':-1}),('L06',{'a':1.5}),('L06',{'a':65}),('L06',{'d':'not-a-number'}),('L07',{'modulus':0}),('L07',{'modulus':-30}),('L07',{'modulus':1.5}),('L07',{'modulus':11}),('L08',{'common':-1}),('L08',{'lo':'not-a-number'}),('L10',{'seed':'3,2'}),('L10',{'n':.5}),('L10',{'n':1001})]:
    case(lab,params,None,'Explicit input guard rejection',reject=True)

JS="""const fs=require('fs');const A=require(process.argv[1]);const qs=JSON.parse(fs.readFileSync(0,'utf8'));process.stdout.write(JSON.stringify(qs.map(q=>{try{return {ok:true,result:A[q.lab](q.params)}}catch(e){return {ok:false,error:String(e.message)}}})));"""
proc=subprocess.run(['node','-e',JS,str(ENGINE)],input=json.dumps([dict(lab=c['lab'],params=c['params']) for c in CASES]),text=True,capture_output=True,check=True,timeout=120)
actual=json.loads(proc.stdout)
assert len(actual)==len(CASES)

def compare(expected,got,path):
    if isinstance(expected,dict):
        assert isinstance(got,dict),(path,'expected object')
        for k,v in expected.items():
            assert k in got,(path,'missing',k)
            compare(v,got[k],path+'.'+str(k))
    elif isinstance(expected,list):
        assert isinstance(got,list) and len(got)==len(expected),(path,'length',len(expected),len(got))
        for i,(a,b) in enumerate(zip(expected,got)):compare(a,b,path+f'[{i}]')
    elif isinstance(expected,float):
        assert isinstance(got,(int,float)) and math.isclose(expected,got,rel_tol=TOL,abs_tol=TOL),(path,expected,got)
    else:assert expected==got,(path,expected,got)

passed=collections.Counter();rejections=collections.Counter();failures=[]
for c,a in zip(CASES,actual):
    try:
        if c['reject']:
            assert not a['ok'],('Expected rejected input',c['params'])
            rejections[c['lab']]+=1
        else:
            assert a['ok'],a.get('error')
            compare(c['expected'],a['result'],c['lab'])
            if c['lab']=='L03' and c['params'].get('total')==3:
                got={row['energy']:row['difference'] for row in a['result']['difference'] if row['difference']}
                assert got==polynomial,('Exact graph difference coefficients',polynomial,got)
        passed[c['lab']]+=1
    except (AssertionError,TypeError,KeyError) as e:
        failures.append(dict(lab=c['lab'],params=c['params'],label=c['label'],error=str(e)))

examples={}
for c in CASES:
    if c['reject']:continue
    if c['lab'] not in examples or (c['lab']=='L03' and c['params'].get('total')==3):
        examples[c['lab']]=dict(inputs=c['params'],expected=c['expected'],basis=c['label'])
report=dict(status='pass' if not failures else 'fail',engine_sha256=hashlib.sha256(ENGINE.read_bytes()).hexdigest(),case_count=len(CASES),passed_count=sum(passed.values()),cases_by_lab=dict(passed),rejections_by_lab=dict(rejections),floating_tolerance=TOL,exact_arithmetic='Python integers and fractions; polynomial and finite counting identities',independent_methods=['Gram principal minors rather than engine row elimination','Bivariate generating polynomial and address inversion','Factored graph-energy difference and stars-and-bars','Rational inverse-problem bounds at selected exponential inputs','Closed shear commutator and exact special-angle factors','Two known Moyal witnesses and an exact cancellation family','CRT quotient-group fibre cardinalities for all 40 divisors','Joint-corner evaluation before marginal extrema','Connected graph cycle rank and disk topology','Binomial unit powers rather than Pell recurrence'],representative_expected_fixtures=examples,graph_mass_three_exact_coefficients=polynomial,failures=failures,scope='These tests certify finite worked-model outputs. They do not prove the global source theorems or implement general solvers.')
(BASE/'data/lab_independent_checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps({k:report[k] for k in ['status','case_count','passed_count','cases_by_lab','rejections_by_lab','failures']},indent=2))
if failures:raise SystemExit(1)
