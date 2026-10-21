"""Portable checks of the declared March catalog examples.

Exact algebra is used where available. Quadrature and elementary-function
evaluations are explicitly numerical checks, not proofs of theorems or of
historical coverage. No third-party package is required.
"""
from fractions import Fraction as F
from pathlib import Path
from math import factorial,exp,sqrt,pi,sin,cos,sinh,cosh,tan
import cmath,json

HERE=Path(__file__).resolve().parent
checks=[]
def check(n,name,condition,detail):
    assert condition,name
    checks.append(dict(id=f'Y24-03-{n:03d}' if isinstance(n,int) else n,
                       name=name,status='passed',detail=detail))

for s in [F(1),F(2),F(3),F(7,2)]:
    assert 1/(s*(s+2))==F(1,2)*(1/s-1/(s+2))
check(20,'Exact Laplace partial fractions',True,
      'The displayed transform agrees at rational s; the written identity follows by a common denominator.')
res=[]
for t in [0,.2,1,3]:
    y=(1-exp(-2*t))/2;dy=exp(-2*t)
    res.append(abs(dy+2*y-1))
check(20,'Time-domain initial value and residual',max(res)<1e-14,
      {'maximum_sampled_residual':max(res),'y_at_one':(1-exp(-2))/2,'scope':'Numerical samples accompany the analytic derivative proof.'})

def clean(p):return {k:v for k,v in p.items() if v}
def padd(*ps):
    out={}
    for p in ps:
        for k,v in p.items():out[k]=out.get(k,F(0))+v
    return clean(out)
def pscale(p,c):return clean({k:c*v for k,v in p.items()})
def pmul(p,q):
    out={}
    for j,a in p.items():
        for k,b in q.items():out[j+k]=out.get(j+k,F(0))+a*b
    return clean(out)
def pd(p):return {k-1:k*v for k,v in p.items() if k}
def int_pm1(p):return sum((2*v/F(k+1) for k,v in p.items() if k%2==0),F(0))
def peval(p,x):return sum((c*x**k for k,c in p.items()),F(0))
P=[]
for n in range(7):
    p={0:F(1)}
    for _ in range(n):p=pmul(p,{2:F(1),0:F(-1)})
    for _ in range(n):p=pd(p)
    p=pscale(p,F(1,2**n*factorial(n)));P.append(p)
    assert peval(p,F(1))==1
    for m,q in enumerate(P):
        assert int_pm1(pmul(p,q))==(F(2,2*n+1) if m==n else 0)
    # ((1-x²)P')'+n(n+1)P=0 as a coefficient identity.
    assert padd(pd(pmul({0:F(1),2:F(-1)},pd(p))),pscale(p,n*(n+1)))=={}
check(21,'Exact Rodrigues orthogonality, norms and ODE through degree six',True,
      'Polynomial differentiation and integration use rational coefficients; finite checks supplement the all-degree proof.')
check(21,'Exact x² projection',padd(pscale(P[0],F(1,3)),pscale(P[2],F(2,3)))=={2:F(1)} and F(2,9)+F(8,45)==F(2,5),
      'x²=P₀/3+2P₂/3 and the predicted squared norm is 2/5.')

for m in range(4):
    cs=[F((-1)**j,2**(2*j+m)*factorial(j)*factorial(j+m)) for j in range(12)]
    for j in range(1,len(cs)):assert 4*j*(m+j)*cs[j]+cs[j-1]==0
check(22,'Exact Bessel coefficient recurrence',True,
      'All retained coefficients for m=0,1,2,3 satisfy the ODE recurrence. No truncated polynomial is called an exact full solution.')
S=sum((F((-1)**j,4**j*factorial(j)**2) for j in range(11)),F(0))
next_term=F(1,4**11*factorial(11)**2)
lo,hi=S-next_term,S
check(22,'Certified alternating-series enclosure for J₀(1)',
      lo<hi and hi-lo==next_term and next_term<F(16,10**23),
      {'lower_rational':str(lo),'upper_rational':str(hi),'enclosure_width':str(next_term),'floating_midpoint':float((lo+hi)/2)})
check(22,'Exact Helmholtz mode coefficient',-3**2-4**2+5**2==0,
      'sin(3x)sin(4y) has exact Helmholtz residual zero; endpoint sine values provide the rectangular Dirichlet boundary condition.')

errs=[]
for x in [F(1,2),F(1),F(3,2),F(2)]:
    f1=2*x;f2=2+4*x*x;f3=12*x+8*x**3
    direct=f3/f1-F(3,2)*(f2/f1)**2
    via_chain=-2*x*x-F(3,2)/x**2
    assert direct==via_chain
check(23,'Exact Schwarzian composition example',True,
      'After cancelling the common exponential, rational differentiation agrees with −2x²−3/(2x²); at x=1 the value is −7/2.')

a,b=240,46;remainders=[]
while b:a,b=b,a%b;remainders.append(b)
check(24,'Euclidean remainder and Bézout certificate',a==2 and -9*240+47*46==2 and remainders==[10,6,4,2,0],
      {'gcd':a,'remainders':remainders,'bezout_coefficients':[-9,47]})
x,y=1,0;pairs=[]
for _ in range(20):
    x,y=3*x+4*y,2*x+3*y
    assert x*x-2*y*y==1
    xp,yp=3*x-4*y,3*y-2*x
    assert xp>0 and 0<=yp<y and xp*xp-2*yp*yp==1
    pairs.append([x,y])
check(24,'Exact Pell recurrence, norm and descent examples',pairs[:4]==[[3,2],[17,12],[99,70],[577,408]],
      {'first_four_positive_pairs':pairs[:4],'checked_steps':20,'scope':'Completeness follows from the written descent proof, not this finite list.'})

fixed=(F(1,2),F(1,3))
check(25,'Exact square fixed point',
      (fixed[0]/2+F(1,4),fixed[1]/4+F(1,4))==fixed,
      'The affine square self-map has the declared fixed point. This is an example, not a numerical proof of Brouwer.')
points=[(F(0),F(0),F(1)),(F(0),F(0),F(-1)),(F(3,5),F(0),F(4,5)),(F(1),F(0),F(0))]
for x,y,z in points:
    v=(-z*x,-z*y,1-z*z)
    assert x*v[0]+y*v[1]+z*v[2]==0
    assert sum(q*q for q in v)==1-z*z
check(25,'Tangent-field examples',True,
      'The projected constant field is tangent and its norm identity identifies exactly the two poles as zeros. Degree theory, explicitly cited in the text, supplies the global obstruction.')

def contour_quad(fun,N=256):
    total=0j
    for j in range(N):
        t=2*pi*j/N;z=2*cmath.exp(1j*t)
        total+=fun(z)*(1j*z)
    return total*(2*pi/N)
v1=contour_quad(lambda z:(z**4+2*z)/(z-1)**3)
v2=contour_quad(lambda z:cmath.exp(z)/(z-1)**3)
check(26,'Cauchy coefficient and numerical contour checks',
      factorial(4)//factorial(2)//factorial(2)==6 and abs(v1-12j*pi)<1e-10 and abs(v2-1j*pi*exp(1))<1e-10,
      {'polynomial_integral_error':abs(v1-12j*pi),'exponential_integral_error':abs(v2-1j*pi*exp(1)),'points':256,'scope':'The residue coefficient six is exact; quadrature independently checks the finite examples.'})

def simpson(fun,a,b,N=20000):
    h=(b-a)/N
    return (fun(a)+fun(b)+sum((4 if j%2 else 2)*fun(a+j*h) for j in range(1,N)))*h/3
g=lambda r:sqrt(2/pi)*r*r*exp(-r*r/2)
vals=[simpson(lambda r,p=p:r**p*g(r),0,10) for p in range(3)]
expected=[1,sqrt(8/pi),3]
errors=[abs(v-e) for v,e in zip(vals,expected)]
tail2=sqrt(2/pi)*(10**3+3*10+F(3,10))*exp(-50)
check(27,'Numerical speed-density moments',max(errors)<1e-10 and tail2<1e-18,
      {'simpson_values':vals,'absolute_errors':errors,'panels':20000,'second_moment_tail_bound':float(tail2),'scope':'Moment proof uses the gamma integral. The stated tail bound follows by integration by parts and the Gaussian tail bound.'})
check(27,'Characteristic speed ordering',sqrt(2)<sqrt(8/pi)<sqrt(3) and 3-8/pi>0,
      {'mode':sqrt(2),'mean':sqrt(8/pi),'rms':sqrt(3),'variance':3-8/pi})

cat_res=[]
for x in [-2,-1,0,1,2]:cat_res.append(abs(cosh(x/2)/2-sqrt(1+sinh(x/2)**2)/2))
target=4*sinh(1)
length=lambda a:2*a*sinh(2/a)
check(28,'Catenary ODE, length and inverse bracket',max(cat_res)<1e-14 and length(1.999)>target>length(2.001),
      {'length':target,'sag':2*(cosh(1)-1),'maximum_sampled_residual':max(cat_res),'unique_a_bracket':[1.999,2.001],'scope':'Uniqueness follows from the written monotonicity proof.'})

check(29,'Exact Navier plate coefficients',3*2**2==12 and F(3*2**2,2)==6,
      'On the π-square the (1,1) mode has Laplacian eigenvalue two, static stiffness twelve and squared frequency six.')
v=[F(1),F(2)];Av=[F(4),F(5)];q=sum(a*b for a,b in zip(v,Av))/sum(a*a for a in v)
r=[a-q*b for a,b in zip(Av,v)];norm2=sum(a*a for a in r)/sum(a*a for a in v)
check(29,'Exact Rayleigh quotient and residual',q==F(14,5) and r==[F(6,5),F(-3,5)] and norm2==F(9,25) and F(1,25)<=norm2,
      {'quotient':str(q),'normalized_residual_squared':str(norm2),'distance_to_spectrum_squared':'1/25'})

H,g0,f,k,A,w=F(1),F(16),F(3),F(1),F(1,10),F(5)
U=w*A/(H*k);V=f*A/(H*k)
check(30,'Exact rotating-wave residual and dispersion',
      w*w==f*f+g0*H*k*k and w*U-f*V==g0*k*A and -w*V+f*U==0 and w*A-H*k*U==0,
      {'surface_amplitude':str(A),'east_velocity_amplitude':str(U),'north_quadrature_amplitude':str(V),'frequency':str(w),'scope':'The check is for the explicitly local f-plane system, not global ocean geometry.'})

hmerr=[]
for t in [0,.2,pi/4,1]:
    q0=2;p0=0;q=q0*cos(t)+p0*sin(t);p1=p0*cos(t)-q0*sin(t)
    At=-tan(t);Ad=-1/(cos(t)**2)
    hmerr.extend([abs((q*q+p1*p1)/2-2),abs(p1-At*q),abs(Ad+At*At+1)])
check(31,'Hamilton flow and Hamilton–Jacobi/Riccati residuals',max(hmerr)<1e-13 and F(-2)+F(-1)**2+1==0,
      {'maximum_numerical_residual':max(hmerr),'exact_A_at_pi_over_four':'-1','exact_A_derivative_at_pi_over_four':'-2','scope':'The graph is used before its first caustic; the written derivation proves the identities.'})

def routh(a,b,c):return [F(1),a,(a*b-c)/a,c]
check(32,'Exact cubic stability parameter certificates',
      routh(F(2),F(2),F(2))==[F(1),F(2),F(1),F(2)] and routh(F(2),F(2),F(4))[2]==0 and routh(F(2),F(2),F(5))[2]==F(-1,2),
      'The certified strict interval is 0<K<4; K=4 has exact factorization (s+2)(s²+2).')
check(32,'Exact boundary polynomial multiplication',pmul({1:F(1),0:F(2)},{2:F(1),0:F(2)})=={3:F(1),2:F(2),1:F(2),0:F(4)},
      'The boundary has roots −2 and ±i√2, and is not strictly Hurwitz.')

f0,kappa,T,Fs=F(100),F(50),F(2),F(1000)
cycles=f0*T+kappa*T*T/2
increments=[(f0+kappa*(F(n)+F(1,2))/Fs)/Fs for n in range(2000)]
check(33,'Exact linear-chirp cycles and phase increments',
      cycles==300 and f0+kappa*T==200 and min(increments)==F('0.100025') and max(increments)==F('0.199975'),
      {'cycles':str(cycles),'first_increment_cycles':str(min(increments)),'last_increment_cycles':str(max(increments)),'scope':'A phase-increment statement, not a band-limiting theorem.'})
alias_errors=[]
for n in [0,1,17,123,1000,2000]:
    t=n/1000
    z1=cmath.exp(1j*(2*pi*100*t+pi*50*t*t))
    z2=cmath.exp(1j*(2*pi*1100*t+pi*50*t*t))
    alias_errors.append(abs(z1-z2))
check(33,'Sample aliasing identity',max(alias_errors)<1e-10,
      {'maximum_numerical_sample_difference':max(alias_errors),'proof':'The added phase is exactly 2πn at the sample times.'})

# Surface integration after setting z=cos(theta), and factoring pi*mu*a*U.
pressure=3*F(2,3);shear=3*(F(2)-F(2,3))
check(34,'Exact pressure and shear drag contributions',pressure==2 and shear==4 and pressure+shear==6,
      'The angular pressure and shear integrals give 2πμaU and 4πμaU. Their sum fixes the coefficient 6π.')
radius=F(1,10**5);mu=F(1,1000);density=F(1000);delta_rho=F(1000);gravity=F('9.81')
terminal=2*radius**2*delta_rho*gravity/(9*mu);Re=2*radius*density*terminal/mu
check(34,'Exact terminal speed and Reynolds check',terminal==F('0.000218') and Re==F('0.00436') and Re<F(1,100),
      {'terminal_metres_per_second':str(terminal),'Reynolds_number':str(Re),'scope':'Constructed model inputs, not retrieved measurements; low Re is an internal approximation check.'})

entries=json.loads((HERE/'catalog_entries.json').read_text())
assert [e['id'] for e in entries]==[f'Y24-03-{n:03d}' for n in range(20,35)]
numbers=sorted(n for e in entries for n in e['original']['source_numbers'])
assert numbers==list(range(81,101))
assert sum(len(e['catalog_concepts']) for e in entries)==21
for e in entries:
    o=e['original']
    assert o['date']=='2024-03-31T02:28:25Z' and o['month']=='2024-03'
    assert o['evidence']=='A' and o['original_question'] is None
    assert o['question'].startswith('Reconstruction:') and 'A@'+o['date'] in o['source_excerpt']
    assert o['retrieval_receipt'] in ['root_specifics.json record 3','root_details.json record 0']
check('CATALOG-2024-03','Complete recovered-name coverage with attribution boundary',True,
      'All 20 names numbered 81–100 plus the unnumbered Laplace transform are developed. No missing 1–80 entries and no query-echo U attribution are imported.')
out=dict(month='2024-03',scope='catalog supplement only; examples and attribution, not exhaustive historical retrieval',status='passed',checks=checks,count=len(checks))
(HERE/'catalog_checks.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
print(json.dumps({'month':'2024-03','catalog_entries':len(entries),'checks':len(checks),'status':'passed'}))
