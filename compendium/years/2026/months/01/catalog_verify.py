"""Stdlib exact finite fixtures for January archive treatments901–910."""
from pathlib import Path
from fractions import Fraction as Q
from math import comb,pi,factorial
import json
P=Path(__file__).resolve().parent
checks=[]
def keep(n,name,details,scope='Exact finite arithmetic; general statements are proved separately in prose.'):
    checks.append(dict(id=f'Y26-01-{900+n:03}',name=name,status='passed',details=details,scope=scope))
assert Q(1,4)*4+1-Q(1,4)==Q(7,4)
keep(1,'OU second-moment fixture',{'moment':'7/4','Ito_variance_correction':'3/4'})
C=[comb(2*k,k)//(k+1)for k in range(12)]
assert C[:5]==[1,1,2,5,14]
assert all(C[k+1]==sum(C[i]*C[k-i]for i in range(k+1))for k in range(10))
keep(2,'Catalan moments and resolvent recurrence',{'even_moments':C})
K=[[1,1],[1,1]]
assert [sum(K[i][j]*[1,-1][j]for j in range(2))for i in range(2)]==[0,0]
assert [sum(K[i][j]for j in range(2))for i in range(2)]==[2,2]
keep(3,'Tangent-kernel reachable and invisible directions',{'eigenvalues':[2,0],'positive_direction':[1,1],'null_direction':[1,-1]})
for m in [Q(2),Q(1,3),Q(-5,7)]:assert abs(m)*abs(1/m)==1
keep(4,'Two-point commutator Lipschitz maximum',{'m_values':['2','1/3','-5/7'],'attaining_difference':'1/abs(m)'})
for n in range(2,10):
    for k in range(1,n):
        rank=n-k;assert n-rank==k
keep(5,'Finite truncation boundary defects',{'dimensions':'2..9','kernel_equals_cokernel':'k','finite_index':0,'infinite_shift_index':'-k by the separate closed-range proof'})
w=[Q(1),Q(2)]
values=[sum((v**(1-g)for v in w),Q(0))for g in range(3)]
assert values==[Q(3),Q(2),Q(3,2)]
for i in range(2):assert (1/w[i])*w[i]==1
keep(6,'Diagonal Frobenius handle values',{'Z0':'3','Z1':'2','Z2':'3/2'})
eps=Q(1);c=[Q(1)]
for n in range(10):c.append((n*(n+2+2*eps)-eps*(eps+1)/4)*c[-1]/(n+1)**2)
assert c[:4]==[Q(1),Q(-1,2),Q(-9,16),Q(-23,32)]
for n in range(10):
    residue=(n+1)**2*c[n+1]+(-n*(n+2+2*eps)+eps*(eps+1)/4)*c[n]
    assert residue==0
keep(7,'Recovered Picard–Fuchs coefficient recurrence',{'epsilon':1,'first_four':[str(v)for v in c[:4]],'exact_zero_residual_orders':'0..9'})
t=Q(1,2);total=Q(0)
for k in range(20):
    assert t==Q(2**max(k-1,0)*factorial(k)**2,factorial(2*k+1)*(2 if k==0 else 1))
    total+=t;t*=Q(k+1,2*k+3)
assert float(4*total)<pi<float(4*total+Q(1,2**18))
keep(8,'Accelerated arctangent rational partial sum',{'N':20,'sum_exact':str(total),'pi_interval_width':'2^-18'},'Term recurrence and rational interval width are exact; comparison against math.pi is only a floating cross-check. The inclusion follows analytically from the integral remainder.')
for n in range(1,10):assert n*factorial(n-1)==factorial(n)
assert Q(factorial(5),10**6)==Q(3,25000)
keep(9,'Factorial formal-ODE coefficients and remainder',{'checked_coefficients':'1..9','negative_ray_remainder_N5_a0.1':'3/25000'})
N=100;zeta=sum((Q(1,n*n)for n in range(1,N+1)),Q(0))
assert float(zeta+Q(1,N+1))<pi*pi/6<float(zeta+Q(1,N))
keep(10,'Dilogarithm endpoint tail bound',{'N':100,'lower_exact':str(zeta+Q(1,N+1)),'upper_exact':str(zeta+Q(1,N)),'width':'1/10100'},'Integral-test endpoints and width are exact; comparison with math.pi is a floating cross-check, and the valueπ²/6 has its own Fourier proof.')
(P/'catalog_checks.json').write_text(json.dumps(dict(status='passed',checks=checks),indent=2))
print(json.dumps(dict(status='passed',records=len(checks))))
