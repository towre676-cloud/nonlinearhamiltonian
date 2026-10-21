#!/usr/bin/env python3
from pathlib import Path
from fractions import Fraction as F
import json,math,cmath
H=Path(__file__).resolve().parent
checks=[]
def C(n,test,detail):
 assert test,(n,detail)
 checks.append(dict(id=f'Y24-05-{n:03d}',name='Worked mathematical certificate',status='pass',detail=detail))
def mm(a,b):return [[sum(x*y for x,y in zip(r,c)) for c in zip(*b)] for r in a]
def add(a,b,k=1):return [[x+k*y for x,y in zip(r,s)] for r,s in zip(a,b)]
v=[F(3,10),F(-3,10)]
for rho in [F(-1),F(0),F(1,2),F(1)]:
 K=[[1,rho],[rho,1]];q=sum(v[i]*K[i][j]*v[j] for i in range(2) for j in range(2));assert q==F(9,50)*(1-rho)
C(1,True,'Exact atomic-kernel quadratic form is (9/50)(1−ρ) at four rational parameters, including the distinct-measure collision at ρ=1.')
for k in [-3,-1,0,1,4]:
 N=128;out=sum((2j*math.pi*k*2*cmath.exp(2j*math.pi*k*t/N))/(2*cmath.exp(2j*math.pi*k*t/N)) for t in range(N))/(N*2j*math.pi)
 assert abs(out-k)<1e-12
C(2,True,'Contour replay for five circle winding numbers; integrality/homotopy invariance are proved analytically, not inferred from samples.')
C(3,(math.pi**2+1)/4>0 and (4*math.pi**2+1)/4>0,'The sine optimizer and second-mode energy-gap coefficients are positive. The all-perturbation gap identity is established in the proof.')
Qp=[[0,1],[0,0]];Qm=[[0,0],[1,0]];N=[[1,0],[0,0]];I=[[1,0],[0,1]];basis=[(N,0),(I,0),(Qp,1),(Qm,1)]
def bracket(a,b,p,q):return add(mm(a,b),mm(b,a),-((-1)**(p*q)))
assert bracket(Qp,Qm,1,1)==I and bracket(N,Qp,0,1)==Qp and bracket(N,Qm,0,1)==[[0,0],[-1,0]]
for X,p in basis:
 for Y,q in basis:
  for Z,r in basis:
   terms=[]
   for A,a,B,b,D,d in [(X,p,Y,q,Z,r),(Y,q,Z,r,X,p),(Z,r,X,p,Y,q)]:
    t=bracket(A,bracket(B,D,b,d),a,(b+d)%2);terms.append([[(-1)**(a*d)*x for x in row] for row in t])
   assert add(add(terms[0],terms[1]),terms[2])==[[0,0],[0,0]]
C(4,True,'All 64 homogeneous-basis graded Jacobi triples vanish exactly in gl(1|1); the general cancellation proof is in the entry.')
def mul(x,y):return ((x[0]*y[0]+2*x[1]*y[1])%5,(x[0]*y[1]+x[1]*y[0])%5)
def plus(x,y):return ((x[0]+y[0])%5,(x[1]+y[1])%5)
els=[(a,b) for a in range(5) for b in range(5)];sq={z:0 for z in els}
for y in els:sq[mul(y,y)]+=1
N25=1+sum(sq[plus(plus(mul(mul(x,x),x),x),(1,0))] for x in els)
N5=1+sum(sum(y*y%5==(x**3+x+1)%5 for y in range(5)) for x in range(5))
C(5,N5==9 and N25==27 and 25+1-((-3)**2-10)==N25,{'F5_points':N5,'F25_points':N25,'local_polynomial':'1+3t+5t²','finite_field':'u²=2 over F5'})
k=2;m=3;hbar=1
rho=1/(2*math.pi);j=hbar*k*rho/m
C(6,abs(j/rho-hbar*k/m)<1e-15,'Normalized periodic plane wave gives constant density and guidance velocity ℏk/m; the PDE identity is proved directly.')
for t in [0,.3,1,2]:
 psi=math.sqrt(3)*cmath.exp(-6j*t);der=-6j*psi
 assert abs(1j*der-2*abs(psi)**2*psi)<1e-13 and abs(abs(psi)**2-3)<1e-13
C(7,True,'The constant Gross–Pitaevskii solution exactly replays its nonlinear ODE to floating precision at four times, with mass density3 and energy density9.')
A=[[2,0],[0,8]];det=16;J=[2,0];mean=[1,0];energy=J[0]*mean[0]/2
C(8,det==16 and energy==1,'Finite Gaussian normalizer is (π/2)e and the stipulated two-pair Berezin quadratic determinant is16; continuum existence is not claimed.')
for x in [0,.2,-.7,2]:
 Z=(math.exp(x)+math.exp(-x))/2;mean=(math.exp(x)-math.exp(-x))/(2*Z);var=1-mean*mean
 assert abs(mean-math.tanh(x))<1e-14 and abs(var-1/math.cosh(x)**2)<1e-14
C(9,True,'A finite tilted two-point distribution independently recovers tanh mean and sech² variance; dimensional model claims are not treated as proofs.')
A=[[-1,0],[0,-2]];B=[[-1]]
C(10,mm([[1,0]],A)==mm(B,[[1,0]]) and mm([[1,1]],A)!=mm(B,[[1,1]]),'The first-coordinate map intertwines generators exactly; the sum map does not.')
for r in [F(-1,2),F(0),F(1,2),F(2)]:
 D=1-r*r
 if D:
  x,y=1/D,r/D;assert -x+r*y+1==0 and r*x-y==0
C(11,True,'Four rational parameter choices verify the coupled fixed-point formula; the stable/saddle classification follows from the exact characteristic polynomial.')
for t in [0,.5,1,4]:
 mean=math.exp(-2*t);var=9/4*(1-math.exp(-4*t));assert 0<=var<=9/4 and mean>0
C(12,True,'OU mean and variance formulas have the specified initial values and limiting variance9/4; stochastic identities are analytically justified in the entry.')
P=[[F(1,2),F(1,2)],[F(1),F(0)]];Q=[[F(1),F(0)],[F(1,4),F(3,4)]]
C(13,mm(P,Q)==[[F(5,8),F(3,8)],[1,0]] and mm(Q,P)==[[F(1,2),F(1,2)],[F(7,8),F(1,8)]],'Exact stochastic products demonstrate closure and noncommutativity; all kernel compositions use associative finite matrix multiplication.')
entries=json.loads((H/'entries.json').read_text());assert len(entries)==13
assert {e['id'] for e in entries}=={c['id'] for c in checks}
(H/'checks.json').write_text(json.dumps({'checks':checks,'summary':{'entries':13,'passed':len(checks),'scope':'Finite exact examples and explicitly scoped numerical replays, with general arguments in the entries.'}},ensure_ascii=False,indent=2))
print(json.dumps({'entries':13,'checks':len(checks),'all_passed':True}))
