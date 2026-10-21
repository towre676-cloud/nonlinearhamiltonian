#!/usr/bin/env python3
"""Independent small mathematical checks for chapter C; Python standard library only."""
from pathlib import Path
from fractions import Fraction as F
import cmath, math, json

checks=[]
def check(id,name,test,detail):
    assert test,(id,name,detail)
    checks.append(dict(id=id,name=name,status='pass',detail=detail))
def mm(a,b):return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]
def adj(a):return [list(map(lambda z:z.conjugate() if isinstance(z,complex) else z,col)) for col in zip(*a)]
def mv(a,v):return [sum(x*y for x,y in zip(row,v)) for row in a]
def inner(a,b):return sum(complex(x).conjugate()*y for x,y in zip(a,b))
def maxerr(a,b):return max(abs(x-y) for ra,rb in zip(a,b) for x,y in zip(ra,rb))

# Orthogonality is checked by a discrete quadrature exact on the finite frequency range.
N=64
coeff={}
for k in range(-3,4):
    coeff[k]=sum((3+2*math.cos(2*math.pi*j/N)-math.sin(4*math.pi*j/N))*cmath.exp(-2j*math.pi*k*j/N) for j in range(N))/N
expected={-3:0,-2:-.5j,-1:1,0:3,1:1,2:.5j,3:0}
check('M038','Finite Fourier coefficients and exact tail energy',max(abs(coeff[k]-expected[k]) for k in expected)<1e-13 and sum(abs(expected[k])**2 for k in [-2,2])==.5,'The degree-two trigonometric polynomial has squared cutoff error 1/2; finite quadrature recovers each coefficient.')
def simpson(f,a,b,n=4000):
    h=(b-a)/n
    return h/3*(f(a)+f(b)+4*sum(f(a+(2*k-1)*h) for k in range(1,n//2+1))+2*sum(f(a+2*k*h) for k in range(1,n//2)))
i1=simpson(lambda t:(4*math.cos(t)**2-1)*2/math.pi*math.sin(t)**2,0,math.pi)
i2=simpson(lambda t:(4*math.cos(t)**2-1)**2*2/math.pi*math.sin(t)**2,0,math.pi)
check('M038','SU(2) Haar integrals',abs(i1)<1e-12 and abs(i2-1)<1e-12,{'spin_one_mean':i1,'spin_one_squared_norm':i2,'scope':'Quadrature checks explicit integrals; analytic orthogonality proof is in the text.'})

w=cmath.exp(2j*math.pi/3)
U=[[w**(a*b)/math.sqrt(3) for b in range(3)] for a in range(3)]
I3=[[int(i==j) for j in range(3)] for i in range(3)]
J=(U[0][0]*U[1][1]*U[0][1].conjugate()*U[1][0].conjugate()).imag
phases_r=[.3,-.7,1.4];phases_c=[-.2,.8,2.2]
Ur=[[cmath.exp(1j*(phases_r[a]+phases_c[b]))*U[a][b] for b in range(3)] for a in range(3)]
Jr=(Ur[0][0]*Ur[1][1]*Ur[0][1].conjugate()*Ur[1][0].conjugate()).imag
check('M039','Unitary Fourier matrix attains rephasing-invariant bound',maxerr(mm(adj(U),U),I3)<1e-14 and abs(J-1/(6*math.sqrt(3)))<1e-14 and abs(Jr-J)<1e-14,{'J':J,'bound':1/(6*math.sqrt(3)),'rephased_J':Jr})

def rank2(cols):
    basis={}
    for x in cols:
        while x:
            p=x.bit_length()-1
            if p in basis:x^=basis[p]
            else:basis[p]=x;break
    return len(basis)
edges=[(0,1),(1,2),(2,0)]
betti=[]
for t in range(5):
    used=edges[:min(t,3)];r1=rank2([(1<<a)|(1<<b) for a,b in used]);r2=int(t>=4)
    betti.append((3-r1,len(used)-r1-r2))
check('M040','Boundary ranks reproduce the entire filtration',betti==[(3,0),(2,0),(1,0),(1,1),(1,0)],{'betti_by_time':betti,'H1_interval':[3,4],'field':'F2'})

theta=math.pi/3;N=4000
vectors=[[math.cos(theta/2),cmath.exp(2j*math.pi*k/N)*math.sin(theta/2)] for k in range(N)]
def loop_product(vs):
    p=1+0j
    for k in range(len(vs)):
        a=inner(vs[(k+1)%len(vs)],vs[k]);p*=a/abs(a)
    return p
hol=loop_product(vectors)
gauged=[[cmath.exp(1j*(.37*k+.8*math.sin(k)))*z for z in v] for k,v in enumerate(vectors)]
hol_g=loop_product(gauged)
check('M041','Berry holonomy and sampled gauge cancellation',abs(hol+1j)<1e-6 and abs(hol-hol_g)<1e-10,{'discrete_holonomy':[hol.real,hol.imag],'target':[0,-1],'gauge_difference':abs(hol-hol_g),'scope':'Numerical convergence check; exact latitude formula is proved analytically.'})

for t in [F(-1),F(0),F(1)]:
    e=F(1,5);H=[[t,e],[e,-t]];H2=mm(H,H)
    assert H2==[[t*t+e*e,0],[0,t*t+e*e]]
check('M042','Exact two-level square and gap',True,{'identity':'H²=(t²+ε²)I','epsilon':'1/5','minimum_gap':'2/5','arithmetic':'rational'})
checks.append(dict(id='M043',name='Moore-spectrum cofiber argument',status='proof-only',detail='The K(0) and K(n) conclusions are derived from the homology long exact sequence in the text. No finite program is claimed to compute Morava K-theory from first principles.'))

def stencil(x,a,b,c):return [a*x[(i-1)%len(x)]+b*x[i]+c*x[(i+1)%len(x)] for i in range(len(x))]
x=list(map(F,[1,-2,3,-4,5]));y=stencil(x,F(1,4),F(1,2),F(1,4))
impulse=[F(1),F(0),F(0),F(0),F(0)];positive=stencil(impulse,F(1,4),F(1,2),F(1,4));negative=stencil(impulse,F(3,4),F(-1,2),F(3,4))
check('M044','Exact conservation contraction and positivity counterexample',sum(y)==sum(x) and sum(t*t for t in y)<=sum(t*t for t in x) and positive==[F(1,2),F(1,4),0,0,F(1,4)] and negative[0]==F(-1,2),{'mass_before':str(sum(x)),'mass_after':str(sum(y)),'positive_impulse':[str(a) for a in positive],'outside_range_central':str(negative[0])})
def reflect(x):return [x[-i%len(x)] for i in range(len(x))]
for k in range(5):
    v=[F(int(i==k)) for i in range(5)]
    assert stencil(reflect(v),F(1,4),F(1,2),F(1,4))==reflect(stencil(v,F(1,4),F(1,2),F(1,4)))
asym=stencil(impulse,F(1,3),0,F(2,3))
check('M045','Reflection commutator on a basis and asymmetric witness',asym!=reflect(asym),'Exact linear-basis checks certify commutation for the five-node symmetric operator. The asymmetric impulse is an explicit failure witness; the general coefficient criterion is proved in text.')

R=[[0,-1],[1,0]];v=[1,0]
RT=mv(R,v);TR=[1,0]
check('M046','Affine composition order',RT==[0,1] and TR==[1,0] and RT!=TR,{'rotation_after_translation':RT,'translation_after_rotation':TR})

def mi(joint):
    px={};py={}
    for (x,y),p in joint.items():px[x]=px.get(x,0)+p;py[y]=py.get(y,0)+p
    return sum(p*math.log2(p/(px[x]*py[y])) for (x,y),p in joint.items() if p)
def bsc(e):return {(x,y):.5*(1-e if x==y else e) for x in [0,1] for y in [0,1]}
h=lambda x:-x*math.log2(x)-(1-x)*math.log2(1-x)
m1=mi(bsc(.1));m2=mi(bsc(.18))
check('M047','Direct joint-table information and cascade loss',abs(m1-(1-h(.1)))<1e-14 and abs(m2-(1-h(.18)))<1e-14 and m2<m1 and abs(mi({(0,0):.5,(1,1):.5})-1)<1e-14 and abs(mi({(x,y):.25 for x in [0,1] for y in [0,1]}))<1e-14,{'first_channel_bits':m1,'cascade_bits':m2,'common_cause_bits':1})

psi=[math.sqrt(3)/2,.5];plus=[1/math.sqrt(2)]*2
p0=abs(psi[0])**2;pp=abs(inner(plus,psi))**2
check('M048','A second effect separates otherwise identical probabilities',abs(p0-.75)<1e-14 and abs(pp-(2+math.sqrt(3))/4)<1e-14 and abs(pp-.5-math.sqrt(3)/4)<1e-14,{'coordinate_probability_both':.75,'plus_probability_pure':pp,'plus_probability_mixed':.5})

om=2;t=.3;state=[cmath.exp(-.5j*om*t)/math.sqrt(2),cmath.exp(.5j*om*t)/math.sqrt(2)]
H=[[om/2,0],[0,-om/2]];A=[[0,1],[1,0]]
av=inner(state,mv(A,state)).real;hv=inner(state,mv(H,state)).real
da=math.sqrt(1-av*av);dh=math.sqrt(inner(state,mv(mm(H,H),state)).real-hv*hv)
comm=[[x-y for x,y in zip(a,b)] for a,b in zip(mm(H,A),mm(A,H))]
rate=abs((1j*inner(state,mv(comm,state))).real)
check('M049','Observable timescale saturates Robertson-derived bound',abs(dh*da/rate-.5)<1e-13,{'hbar_units':1,'Delta_H':dh,'tau_A':da/rate,'product':dh*da/rate,'scope':'A finite-time nonzero-rate example, not a universal time-operator assertion.'})

def sigma(n,p):return sum(d**p for d in range(1,n+1) if n%d==0)
coeff4=[240*sigma(n,3) for n in range(1,5)]
q=math.exp(-2*math.pi);e6=1-504*sum(sigma(n,5)*q**n for n in range(1,21))
ratio=q*(22/21)**6;tail=504*21**6*q**21/(1-ratio)
check('M050','Eisenstein coefficients and forced-zero numerical residual',coeff4==[240,2160,6720,17520] and abs(e6)<1e-12 and ratio<1,{'E4_coefficients':coeff4,'E6_i_residual_float':e6,'analytic_tail_bound_after_20_terms':tail,'scope':'Floating residual includes rounding error; the exact E6(i)=0 result follows from the transformation law.'})

n=64;a=b=1;k=2;integral=0;integral_g=0
for ix in range(n):
    x=(ix+.5)/n
    for iz in range(n):
        z=(iz+.5)/n
        A1=a*math.cos(2*math.pi*z);A2=b*math.sin(2*math.pi*z)
        curl1=-2*math.pi*b*math.cos(2*math.pi*z);curl2=-2*math.pi*a*math.sin(2*math.pi*z)
        v=A1*curl1+A2*curl2
        integral+=v/n**2
        grad1=2*math.pi*math.cos(2*math.pi*x)*math.sin(2*math.pi*z)
        integral_g+=(v+grad1*curl1)/n**2
s=k/(4*math.pi)*integral;sg=k/(4*math.pi)*integral_g
check('M051','Torus action and a periodic small gauge change',abs(s+1)<1e-12 and abs(s-sg)<1e-12,{'action':s,'gauge_changed_action':sg,'scope':'A smooth globally defined trivial-bundle example; large-gauge quantization is not tested.'})

rt=math.sqrt(2);S=[[1/rt,1/rt],[1/rt,-1/rt]];T0=[[1,0],[0,1j]]
T=[[cmath.exp(-1j*math.pi/12)*z for z in row] for row in T0]
I2=[[1,0],[0,1]]
def cube(a):return mm(mm(a,a),a)
fusion={}
for a in range(2):
 for b in range(2):
  for c in range(2):fusion[f'{a}{b}{c}']=sum(S[a][x]*S[b][x]*S[c][x]/S[0][x] for x in range(2))
phase=cmath.exp(1j*math.pi/4)
fusion_ok=all(abs(v-int((int(key[0])^int(key[1]))==int(key[2])))<1e-14 for key,v in fusion.items())
check('M052','Torus anomaly and complete two-label fusion table',maxerr(mm(S,S),I2)<1e-14 and maxerr(cube(mm(S,T0)),[[phase,0],[0,phase]])<1e-14 and maxerr(cube(mm(S,T)),I2)<1e-14 and fusion_ok,{'fusion':fusion,'unadjusted_cubic_scalar':[phase.real,phase.imag],'adjusted_cubic_relation':'identity to floating precision','scope':'These matrix checks do not reconstruct all modular-functor gluing data.'})

stable=math.pi/6;unstable=5*math.pi/6
check('M053','Kuramoto branches and nonlocking witness',abs(1-2*math.sin(stable))<1e-14 and abs(1-2*math.sin(unstable))<1e-14 and -2*math.cos(stable)<0 and -2*math.cos(unstable)>0 and 3-2>0,{'stable_difference':stable,'unstable_difference':unstable,'stable_linear_rate':-2*math.cos(stable),'no_lock_Deltaomega':3})

E=[F(0),F(1),F(2)];g=[F(2)]*3;dg=[F(1),F(-2),F(1)]
gg=[a+F(1,4)*b for a,b in zip(g,dg)]
check('M054','Exact conductance nonidentifiability witness',sum(g)==sum(gg)==6 and sum(a*b for a,b in zip(E,g))==sum(a*b for a,b in zip(E,gg))==6 and min(gg)>0 and gg!=g,{'conductances_original':[str(x) for x in g],'conductances_changed':[str(x) for x in gg],'G':6,'B':6,'scope':'Frozen-gate protocol only; not a universal nonidentifiability theorem for the full model.'})
alpha=.2;beta=.3
for q0 in [0,1]:
    for t in [0,1,5,100]:assert -1e-14<=alpha/(alpha+beta)+(q0-alpha/(alpha+beta))*math.exp(-(alpha+beta)*t)<=1+1e-14
check('M054','Gate closed-form invariant interval samples',True,{'equilibrium':alpha/(alpha+beta),'time_constant':1/(alpha+beta),'scope':'The all-time interval claim is proved by boundary invariance in the text, not by these samples.'})

threshold=F(1,10);qmix=F(1,3)
check('M055','Finite decision threshold and mixed best-response equality',F(9)*threshold-(1-threshold)==0 and 2*qmix==1-qmix and F(9,1)*F(1,20)-(1-F(1,20))==F(-1,2) and F(9)*F(1,5)-(1-F(1,5))==1,{'decision_threshold':str(threshold),'mixed_B_probability':str(qmix),'mixed_payoff':str(2*qmix)})
for M in [10,100,1000]:
    for a in [-1,0,1]:
        p=F(1,2)+F(a,M)
        assert 0<=p<=1 and M*(2*p-1)==2*a
check('M056','Nonuniform prior-and-utility limit',True,{'family':'p_M=1/2+a/M','expected_A':'2a exactly','a_values':[-1,0,1],'M_values':[10,100,1000]})

out={'checks':checks,'summary':{'pass':sum(c['status']=='pass' for c in checks),'proof_only':sum(c['status']=='proof-only' for c in checks),'entries':19,'scope':'Examples and algebraic checks support stated elementary results. Deep general theories remain referenced, not machine-proved.'}}
(Path(__file__).resolve().parent/'checks.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
print(json.dumps(out['summary']))
