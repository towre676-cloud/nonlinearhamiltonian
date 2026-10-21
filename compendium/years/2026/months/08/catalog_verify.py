"""Offline finite exact examples for approximation entries901–906.

The floating rectangle calculation is explicitly numerical, not interval-certified.
All other calculations below use integers or Fraction.
"""
from pathlib import Path
from fractions import Fraction as Q
from math import comb,factorial,exp,sqrt,log,ceil,floor
import json
P=Path(__file__).resolve().parent
checks=[]
def keep(n,name,details,scope='Exact finite arithmetic; the general theorem has a separate written proof.'):
    checks.append(dict(id=f'Y26-08-{900+n:03}',name=name,status='passed',details=details,scope=scope))
assert Q(1,11)+Q(1,10)==Q(21,110)
keep(1,'Cutoff bound at delta=1/100',{'N':10,'bias':'1/11','noise':'1/10','sum':'21/110'})
for j in range(1,8):
    delta=Q(1,100**j);N=10**j
    assert Q(1,N+1)+delta*N<2*Q(1,N)
    assert Q(1,N)**2==delta
keep(2,'Matching polynomial-rate sequence',{'deltas':'100^(-j), j=1..7','upper':'<2sqrt(delta)','two_point_lower':'sqrt(delta)'})
for j in [20,50,100,200]:
    N=floor(j-log(j));assert N>0
    assert exp(N-j)<=1/j*(1+1e-12)
    assert abs(exp(-j)*exp(j)-1)<1e-14
keep(3,'Log-log cutoff and naive instability',{'L_values':[20,50,100,200],'safe_N_at100':floor(100-log(100)),'naive_noise':1},'Floating examples of an analytically proved estimate; not a floating interval certificate.')
alpha=Q(1,4);sigma=Q(1,2)
g=sigma/(sigma*sigma+alpha);residual=alpha/(sigma*sigma+alpha)
assert g==1 and residual==Q(1,2)
assert residual*Q(1,2)==Q(1,4)
keep(4,'Sharp two-coordinate Tikhonov fixture',{'filter':['4/5','1'],'bias':'1/4','noise_norm':'1'})
x=Q(0);s=Q(1,2);y=s
for m in range(1,5):
    x=x+s*(y-s*x)
    closed=1-(1-s*s)**m
    assert x==closed
assert 1-x==Q(81,256)
assert (1-(1-s*s)**4)/s==Q(175,128)
keep(5,'Landweber recurrence equals spectral filter',{'iterations':4,'residual':'81/256','filter':'175/128'})
a=Q(1,2);S=Q(0);coeff=Q(0);K=64
for k in range(1,K+1):
    if k>1:a*=Q(2*k-3,2*k)
    assert a==Q(comb(2*k,k),4**k*(2*k-1))
    integral=sum((Q(comb(k,j)*factorial(j),k**(j+1))for j in range(k+1)),Q(0))
    S+=a*integral;coeff+=a
upper=S+2*(1-coeff)
assert Q(13,10)<S<upper<Q(3,2)
keep(6,'Positive rational-series enclosure for C0',{'K':K,'strict_lower_decimal_for_reading':float(S),'strict_upper_decimal_for_reading':float(upper),'exact_lower':str(S),'exact_upper':str(upper)},'Exact rational-series enclosure; displayed decimals are approximations of its exact endpoints.')
L=24;step=0.0001;count=round(L/step)
def h(t):
    s=(1+t)*exp(-t)
    return s/(1+sqrt(max(0.,1-s)))
right=step*sum(h(i*step)for i in range(1,count+1))
left=right+step*(h(0)-h(L));tail=(L+2)*exp(-L)
assert right<1.344045683<left+tail
keep(6,'Independent monotone-quadrature numerical cross-check',{'right_sum':right,'left_plus_tail':left+tail,'mesh':step,'tail_upper_formula':'(L+2)exp(-L)'},'Floating implementation only. Monotonicity and tail bounds are proved in prose; rounding is not interval-certified.')
(P/'catalog_checks.json').write_text(json.dumps(dict(status='passed',checks=checks),indent=2))
print(json.dumps(dict(status='passed',records=len(checks))))
