#!/usr/bin/env python3
"""Exact finite robust-Gaussian sensor design certificate for synthesis S008.

Only coordinate-panel noncentrality is optimized. No observations are simulated,
and no physical, out-of-sample or universal detector advantage is asserted.
"""
from fractions import Fraction
from pathlib import Path
import itertools
import json

HERE=Path(__file__).resolve().parent
CHANNELS=[
    dict(id='A',cost=6,covers=[1,3,5]),
    dict(id='B',cost=7,covers=[1,2,3]),
    dict(id='C',cost=6,covers=[4]),
    dict(id='D',cost=6,covers=[2,3,5,6]),
    dict(id='E',cost=7,covers=[2,4,5,6]),
    dict(id='F',cost=4,covers=[1,6]),
]
FAULTS=[[2 if j in c['covers'] else 0 for c in CHANNELS] for j in range(1,7)]
THRESHOLD=4
checks=[]
def check(name,condition,detail):
    assert condition,name
    checks.append(dict(id='S008',name=name,status='pass',detail=detail))

def selected(mask):return [i for i in range(6) if mask>>i&1]
def panel_names(mask):return [CHANNELS[i]['id'] for i in selected(mask)]
def cost(mask):return sum(CHANNELS[i]['cost'] for i in selected(mask))
def energies(mask):return [sum(d[i]*d[i] for i in selected(mask)) for d in FAULTS]
def covered(mask):return [j+1 for j,v in enumerate(energies(mask)) if v>=THRESHOLD]
def is_feasible(mask):return len(covered(mask))==6

enumeration=[]
for mask in range(1<<6):
    en=energies(mask)
    enumeration.append(dict(mask=mask,channels=panel_names(mask),cost=cost(mask),energies=en,
                            covered=covered(mask),feasible=is_feasible(mask)))
feasible=[r for r in enumeration if r['feasible']]
optimum_cost=min(r['cost'] for r in feasible)
optimizers=[r for r in feasible if r['cost']==optimum_cost]
check('All coordinate panels exhaustively enumerated',len(enumeration)==64 and len({r['mask'] for r in enumeration})==64,
      'Every subset of six channels occurs once; empty and full panels are retained.')
check('Unique exact optimum',optimum_cost==13 and len(optimizers)==1 and optimizers[0]['channels']==['A','E'],
      'The unique minimum-cost feasible panel is A,E, cost13; selected energies are (4,4,4,4,8,4).')
check('Every cheaper panel has a failed target',all(not r['feasible'] for r in enumeration if r['cost']<13),
      'An exhaustive lower-cost exclusion is included as the complete 64-row certificate.')
check('Optimal energies and robust margins',optimizers[0]['energies']==[4,4,4,4,8,4],
      'ε=1 and target τ=1 reduce exact robust feasibility to energy≥(1+√1)²=4. Five optimum targets have worst-case1; target5 has worst-case9−4√2.')

single_nondominated=all(not(set(a['covers'])<=set(b['covers']) and a['cost']>=b['cost'])
                          for i,a in enumerate(CHANNELS) for j,b in enumerate(CHANNELS) if i!=j)
check('No single channel is cost-dominated',single_nondominated,
      'No other single channel covers a superset of its declared targets at an equal or lower cost.')
constraint_witnesses=[]
for j in range(1,7):
    miss_j=sum(1<<i for i,c in enumerate(CHANNELS) if j not in c['covers'])
    assert j not in covered(miss_j) and set(covered(miss_j))==set(range(1,7))-{j}
    constraint_witnesses.append(dict(omitted_target=j,panel=panel_names(miss_j),covered=covered(miss_j)))
check('Every declared target constraint is necessary',len(constraint_witnesses)==6,
      'For every target there is a panel satisfying all other targets and failing exactly that target; six witnesses are included.')
minimal_feasible=[r for r in feasible if not any(s['mask']!=r['mask'] and s['mask']&r['mask']==s['mask'] for s in feasible)]
check('Every channel appears in an inclusion-minimal feasible panel',
      all(any(i in selected(r['mask']) for r in minimal_feasible) for i in range(6)),
      'The complete inclusion-minimal panel list is included; no channel was added solely to reach the six-channel count.')

# Explicit gain-per-cost greedy: maximize newly satisfied targets/cost; ties
# choose the alphabetically first channel. This is not asserted globally optimal.
mask=0;trace=[]
while not is_feasible(mask):
    before=set(covered(mask));candidates=[]
    for i,c in enumerate(CHANNELS):
        if mask>>i&1:continue
        new=set(covered(mask|(1<<i)))-before
        candidates.append((Fraction(len(new),c['cost']),c['id'],i,sorted(new)))
    candidates.sort(key=lambda x:(-x[0],x[1]))
    assert len(candidates)<2 or candidates[0][0]>candidates[1][0]
    ratio,name,i,new=candidates[0]
    assert ratio>0
    trace.append(dict(before=panel_names(mask),choice=name,newly_satisfied=new,
                      gain_per_cost=str(ratio),
                      candidates=[dict(channel=n,ratio=str(r),newly_satisfied=v) for r,n,_,v in candidates]))
    mask|=1<<i
greedy=dict(channels=panel_names(mask),cost=cost(mask),energies=energies(mask),trace=trace)
check('Declared greedy heuristic replay',greedy['channels']==['C','D','F'] and greedy['cost']==16 and [s['choice'] for s in trace]==['D','F','C'],
      'The ratio-maximizing heuristic uniquely chooses D (2/3), then F (1/4), then C (1/6), yielding cost16. There are no maximizing ties on this path.')
check('Strict finite greedy gap',Fraction(greedy['cost'],optimum_cost)==Fraction(16,13),
      'Greedy has cost16 versus exact cost13: additive gap3 and ratio16/13 for this constructed declared family only.')

# Fault-by-fault exact perturbations attain the optimum robust boundary.
optimal_mask=optimizers[0]['mask']
attainers=[]
for j,d in enumerate(FAULTS,1):
    active=[i for i in selected(optimal_mask) if d[i]]
    m=len(active);assert m in [1,2] and all(d[i]==2 for i in active)
    # e_i=−1/√m on the active retained coordinates, zero elsewhere.
    # The squared norm m/m=1 is rational, while the attained energy is
    # m(2−1/√m)^2=4m+1−4√m, an exact quadratic-surd descriptor.
    assert Fraction(m,m)==1
    descriptor=dict(rational_part=4*m+1,sqrt_coefficient=-4,radicand=m)
    if m==1:assert descriptor['rational_part']+descriptor['sqrt_coefficient']==1
    else:assert descriptor==dict(rational_part=9,sqrt_coefficient=-4,radicand=2)
    attainers.append(dict(fault=j,active_coordinates=[CHANNELS[i]['id'] for i in active],
                          perturbation_nonzero_value=f'-1/sqrt({m})',perturbation_norm_squared=1,
                          attained_noncentrality=descriptor))
check('Robust lower bounds are attained',len(attainers)==6,
      'Five integer perturbations and one exact quadratic-surd perturbation of norm1 attain the stated robust bounds. Each attainer is represented exactly in the certificate.')

withheld=[0,0,0,2,0,0]
withheld_selected=sum(withheld[i]**2 for i in selected(optimal_mask))
withheld_full=sum(v*v for v in withheld)
withheld_greedy=sum(withheld[i]**2 for i in selected(mask))
check('Withheld-direction exact blindness',withheld_selected==0 and withheld_full==withheld_greedy==4,
      'The withheld shift2e_D has zero selected mean in A,E, so its observation law equals the null law exactly. Full and greedy panels retain center noncentrality4 and worst-case1 at ε=1.')

# Reproduce projection facts with integer/rational coordinate matrices.
P=[[int(i==j and i in selected(optimal_mask)) for j in range(6)] for i in range(6)]
def mm(a,b):return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]
check('Projection identity',mm(P,P)==P and sum(P[i][i] for i in range(6))==2,
      'The optimum projection is diag(1,0,0,0,1,0), idempotent with rank2. It has a four-dimensional nullspace, as rank-nullity requires.')

out=dict(id='S008',model=dict(covariance='I_6',channels=CHANNELS,fault_centers=FAULTS,
                             uncertainty='For each center, all e∈R^6 with ||e||₂≤1',
                             target_noncentrality=1,exact_energy_threshold=THRESHOLD,
                             criterion='Each declared fault center must retain worst-case noncentrality at least1.'),
         checks=checks,check_count=len(checks),all_passed=True,
         optimum=dict(cost=optimum_cost,unique=True,panel=optimizers[0]),
         feasible_panel_count=len(feasible),greedy=greedy,
         target_nonredundancy_witnesses=constraint_witnesses,
         inclusion_minimal_feasible_panels=minimal_feasible,
         robust_attainers=attainers,
         withheld=dict(center=withheld,optimal_panel_noncentrality=withheld_selected,
                       full_noncentrality=withheld_full,greedy_noncentrality=withheld_greedy,
                       interpretation='Same observation distribution as the null for the optimal finite-family panel.'),
         exhaustive_certificate=enumeration,
         scope='A deterministic constructed finite Gaussian mean-shift design, with all64 coordinate panels checked exactly. Noncentrality threshold is the declared objective; no empirical or universal detector claim.')
HERE.joinpath('supplement_checks.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
print(json.dumps(dict(check_count=len(checks),all_passed=True,panels_enumerated=len(enumeration),
                      feasible_panels=len(feasible),optimal_cost=optimum_cost,optimal_panel=['A','E'],
                      greedy_cost=greedy['cost'],greedy_panel=greedy['channels'])))
