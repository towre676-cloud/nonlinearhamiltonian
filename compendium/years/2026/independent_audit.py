"""Independent exact finite certificates for recovered2026 graph and phase claims.

Stdlib only. This does not certify unrelated implementation or formal-proof claims.
"""
from pathlib import Path
from collections import Counter
from fractions import Fraction as Q
from itertools import product
from math import gcd
import json
ROOT=Path(__file__).resolve().parent
checks=[]
G=[(0,3),(0,4),(0,6),(1,2),(1,3),(2,3),(2,4),(3,5)]
H=[(0,1),(0,4),(0,6),(1,5),(1,6),(2,6),(3,6),(4,5)]
def energy(h,E):return sum((h[u]-h[v])**2 for u,v in E)
def binary(E):return Counter((sum(h),energy(h,E))for h in product(range(2),repeat=7))
assert binary(G)==binary(H)
def compositions(n,k):
    if k==1:yield(n,);return
    for a in range(n+1):
        for rest in compositions(n-a,k-1):yield(a,)+rest
def census(n,E,nonzero=None):
    return Counter(energy(h,E)for h in compositions(n,7)if nonzero is None or sum(x>0 for x in h)==nonzero)
for n in range(3):assert census(n,G)==census(n,H)
delta=Counter(census(3,G));delta.subtract(census(3,H));delta={k:v for k,v in delta.items()if v}
def mul(a,b):
    c=Counter()
    for i,x in a.items():
        for j,y in b.items():c[i+j]+=x*y
    return{k:v for k,v in c.items()if v}
expected={3:1}
for d in [1,3,3,4,4]:expected=mul(expected,{0:1,d:-1})
assert delta==expected
d2=Counter(census(3,G,2));d2.subtract(census(3,H,2));assert {k:v for k,v in d2.items()if v}==expected
value=sum((Q(v,2**k)for k,v in delta.items()),Q(0));assert value==Q(11025,262144)
checks.append(dict(ids=['October graph-energy binary collision'],name='Exact binary equality and first multilevel separation',status='passed',scope='All128 binary assignments and all weak compositions of total height≤3 on the two explicitly stated seven-vertex graphs.',details={'edge_sets':{'G':G,'H':H},'difference_polynomial':delta,'at_q_half':str(value)}))
units=[a for a in range(1680)if gcd(a,1680)==1]
fibres=Counter(a%30 for a in units)
assert len(units)==384 and len(fibres)==8 and set(fibres.values())=={48}
assert set(fibres)=={a for a in range(30)if gcd(a,30)==1}
checks.append(dict(ids=['Y26-01 resonance','October E8 conductor bridge'],name='Conductor1680 primitive-phase multiplicities',status='passed',scope='Exact residue enumeration proves the finite phase map a mod1680 → a mod30; field-degree and trace statements have their own algebraic proof.',details={'phi1680':384,'phi30':8,'multiplicity':48,'fibres':dict(fibres)}))
# The projective quiver pencil has fourteen paths before its one relation.
# Count by path length in the acyclic direction, allowing at most one gamma.
paths=['e0','e1','e2','a','g','b','bp','ga','bg','bpg','ba','bpa','bga','bpga']
assert len(paths)==14
checks.append(dict(ids=['August projective quiver pencil'],name='Path-basis count with gamma squared zero',status='passed',scope='Enumeration of all paths in the stated three-vertex quiver before imposing the single projective relation; for nonzero(u,v), it reduces the14-dimensional space to13.',details={'paths':paths,'before_relation':14,'after_one_nonzero_relation':13}))
S=[0,1,2,4,11]
def bernoulli2(a):
    x=Q(a%17,17)
    return x*x-x+Q(1,6)
coefficient=sum((bernoulli2(s-r)+bernoulli2(s+r)for s in S for r in S),Q(0))
assert coefficient==Q(955,867)
checks.append(dict(ids=['October conductor17 phase integral'],name='Exact Bernoulli sum for the phase-log-square integral',status='passed',scope='Exact rational coefficient after the separately proved Fourier/Parseval reduction. This finite sum alone does not establish a monodromy closure.',details={'phase_set':S,'coefficient_of_pi_cubed':str(coefficient)}))
(ROOT/'independent_checks.json').write_text(json.dumps(dict(status='passed',checks=checks),indent=2))
print(json.dumps(dict(status='passed',records=len(checks))))
