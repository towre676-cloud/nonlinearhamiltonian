"""Independently replay selected existing PerfectJet constructions in its full star engine.

Python standard library only. The second q coordinate is a central spectator
parameter because no term uses its conjugate p coordinate. This makes lambda
an indeterminate, so the identities are symbolic parameter identities.
"""
from pathlib import Path
from fractions import Fraction as Q
import importlib.util,sys,json,hashlib
ROOT=Path(__file__).resolve().parent
source=ROOT/'source_snapshot/src/perfectjet/moyal.py'
spec=importlib.util.spec_from_file_location('recovered_moyal',source)
m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)
checks=[]
def check(name,value,scope):
 assert value,name
 checks.append({'name':name,'status':'passed','scope':scope})
q,p=m.PolyH.q(2,0),m.PolyH.p(2,0)
lam=m.PolyH.q(2,1);hb=m.PolyH.hbar(2)
f=q**6+lam*q**3*p**3+p**6
h=q*p*(q**3-p**3)
g8=q*p*(q**6+p**6-Q(7,20)*lam*q**3*p**3)
check('C3 sextic and degree8 partner for formal lambda',m.egorov_defect(f,g8).is_zero(),'Full star-product symbolic replay with central spectator parameter; correction gates vanish at every lambda')
check('Quintic obstruction factor',m.egorov_defect(f,h)==-3*hb**2*(7*lam-40)*(q**4*p+q*p**4),'Full star defect, exact rational polynomial identity')
fstar=q**6+Q(40,7)*q**3*p**3+p**6
check('Exceptional quintic partner active',m.egorov_defect(fstar,h).is_zero() and not m.poisson_bracket(fstar,h).is_zero(),'One exact instance at lambda=40/7; nonzero Poisson bracket checked separately')
cov=m.covariance_example()
check('Affine symplectic covariance finite calibration',cov['affine_covariance_exact'],'100 polynomial pairs degree<=3 under one affine symplectic transformation; general covariance is a theorem, not inferred from the census')
check('Nonlinear flat-star pullback defect',cov['nonlinear_poisson_covariance_exact'] and cov['nonlinear_star_defect']['terms']==[{'hbar_power':2,'exponents':[0,0],'real':'-1/2','imaginary':'0'}],'For Phi(q,p)=(q,p+q²), f=p²,g=p: pullback product defect is exactly -hbar²/2')
result={'status':'passed','check_count':len(checks),'checks':checks,'scope':'Existing source constructions, freshly replayed. Does not rerun global msolve or Singular classification receipts.','source_sha256':hashlib.sha256(source.read_bytes()).hexdigest()}
(ROOT/'checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':'passed','checks':len(checks)}))
