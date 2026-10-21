"""Offline checks of the finite data used in the three calculated illustrations."""
from pathlib import Path
import math,json
P=Path(__file__).resolve().parent
d=json.loads((P/'figures'/'figure_data.json').read_text());checks=[]
def add(name,detail):
    checks.append(dict(id='Illustrations',name=name,status='passed',detail=detail))
for pair in d['roots']:
    z=complex(*pair);assert abs(z**4-2*z*z+9)<1e-12
add('Quartic plotted roots satisfy the polynomial',{'roots':len(d['roots']),'tolerance':1e-12})
for r in d['traces']:
    p=r['p'];n=1+sum((y*y+y-x*x*x+x)%p==0 for x in range(p) for y in range(p))
    assert n==r['points'] and p+1-n==r['trace']
    assert r['trace']**2<=4*p
assert d['traces'][0]['trace']==-2
add('Independent exact finite-field point counts and Hasse bounds',{'good_primes':len(d['traces']),'equation':'y²+y=x³−x'})
for r in d['jordan']:
    e=r['epsilon'];s=r['eigenvalue_magnitude']
    assert abs(s*s-e)<=1e-14*e
    assert abs(s*r['eigenvector_condition']-1)<1e-14
    assert r['operator_perturbation']==e
add('Jordan-family plotted quantities satisfy the exact identities',{'samples':len(d['jordan']),'scope':'Numerical evaluation of explicitly proved formulas'})
(P/'figure_checks.json').write_text(json.dumps(dict(checks=checks),indent=2))
print(json.dumps(dict(status='passed',checks=len(checks))))
