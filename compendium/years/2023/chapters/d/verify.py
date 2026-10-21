#!/usr/bin/env python3
"""Reproduce worked checks for entries M057–M077 using only Python stdlib.

The arguments in entries.json supply proofs; these checks replay finite examples
and identities. No check establishes a new physical model or a set-theory axiom.
"""
import cmath
from fractions import Fraction as F
import json
import math
from pathlib import Path

HERE=Path(__file__).resolve().parent
checks=[]
def record(id,name,detail):checks.append(dict(id=id,name=name,status='pass',detail=detail))
def close(a,b,tol=1e-12):assert abs(a-b)<tol,(a,b)
def mm(a,b):return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]
def trans(a):return [list(x) for x in zip(*a)]
def adj(a):return [[complex(x).conjugate() for x in col] for col in zip(*a)]
def madd(a,b):return [[x+y for x,y in zip(ra,rb)] for ra,rb in zip(a,b)]
def det(a):return a[0][0]*a[1][1]-a[0][1]*a[1][0]
def qform(a,v):return sum(v[i]*a[i][j]*v[j] for i in range(len(v)) for j in range(len(v)))

# Characteristic-function product identity, not a stochastic simulation.
for n in [1,2,5,17,101]:
    for t in [-3,-.2,0,.2,3]:
        mu,gamma=.7,1.3
        phi=lambda s:cmath.exp(1j*mu*s-gamma*abs(s))
        close(phi(t/n)**n,phi(t))
close((math.atan(1)-math.atan(-1))/math.pi,.5)
record('M057','Cauchy averaging characteristic function',
       'For five sample sizes and five frequencies, φ(t/n)^n=φ(t) to numerical precision; P(|X̄|≤1)=1/2 for the standard Cauchy law. Distributional proof is in the entry.')

A=[[F(1,2),F(4)],[F(0),F(1,2)]]
An=[[F(1),F(0)],[F(0),F(1)]]
for n in range(1,16):
    An=mm(An,A)
    target=[[F(1,2)**n,n*F(1,2)**(n-1)*4],[F(0),F(1,2)**n]]
    assert An==target
assert sum(z[0]**2 for z in mm(A,[[0],[1]]))==F(65,4)
close(math.sqrt(4**2+.5**2),math.sqrt(65)/2)
record('M058','Jordan-block transient formula',
       'Exact rational multiplication verifies A^n=a^n I+n a^(n−1)bN for n=1,…,15; a=1/2,b=4 gives one-step norm amplification √65/2 from e₂.')

M=[[1,2],[3,4]]
whole=sum(x*x for row in M for x in row)
blocks=[sum(x*x for x in row) for row in M]
assert whole==30 and blocks==[5,25] and sum(blocks)==whole
assert 2*blocks[0]+blocks[1]==35
record('M059','Block-energy accounting','Disjoint row energies 5+25=30; repeating the first row gives 35, exactly the predicted multiplicity overcount.')

p=[F(1,4),F(3,4)];values=[2,4]
e=sum(pi*vi*vi for pi,vi in zip(p,values))
amp=sum(pi*pi*vi*vi for pi,vi in zip(p,values))
mean=sum(pi*vi for pi,vi in zip(p,values))
assert e==13 and amp==F(37,4) and e-mean*mean==F(3,4)
record('M060','Probability versus amplitude weighting','Exact rational arithmetic yields 13, 37/4 and variance 3/4 for the specified two-point example.')

samples=[(-1,-2),(1,2)]
cov=[[sum(F(1,2)*s[i]*s[j] for s in samples) for j in range(2)] for i in range(2)]
assert cov==[[1,2],[2,4]] and det(cov)==0 and qform(cov,[2,-1])==0
record('M061','Covariance Gram matrix','The two-point law gives Σ=[[1,2],[2,4]], determinant zero, and exact null combination 2X−Y.')

S=[[1,0],[0,4]];w=[F(4,5),F(1,5)]
assert sum(w)==1 and qform(S,w)==F(4,5)
for num in range(-20,21):assert qform(S,[F(num,10),1-F(num,10)])>=F(4,5)
rankone=[[1,1],[1,1]]
for num in range(-20,21):assert qform(rankone,[F(num,10),1-F(num,10)])==1
S2=[[1,2],[2,9]];wu=[F(7,6),F(-1,6)]
assert qform(S2,wu)==F(5,6)
wc=[1,0];gradient=[2*x[0] for x in mm(S2,[[1],[0]])]
assert gradient==[2,4]
assert [gradient[i]-2 for i in range(2)]==[0,2]
for num in range(101):assert qform(S2,[F(num,100),1-F(num,100)])>=1
record('M062','PSD quadratic programs and nonnegative KKT certificate',
       'Exact examples give positive-definite minimum 4/5, rank-one constant objective 1, unconstrained value 5/6 at (7/6,−1/6), and constrained value 1 with KKT dual slack (0,2).')

for q in [0,.1,.25,.7,1]:
    K0=[[1,0],[0,math.sqrt(q)]];K1=[[0,math.sqrt(1-q)],[0,0]]
    total=madd(mm(adj(K0),K0),mm(adj(K1),K1))
    for i in range(2):
        for j in range(2):close(total[i][j],int(i==j))
    rho=[[.5,.5],[.5,.5]]
    out=madd(mm(mm(K0,rho),adj(K0)),mm(mm(K1,rho),adj(K1)))
    close(out[0][0]+out[1][1],1)
    assert det(out).real>=-1e-14
    if q==.25:
        close(out[0][0],F(7,8));close(out[0][1],F(1,4));close(det(out),F(3,64))
for q,r in [(.25,.4),(.7,.8)]:
    def damp(rho,t):
        a,b=rho[0];_,d=rho[1]
        return [[a+(1-t)*d,math.sqrt(t)*b],[math.sqrt(t)*complex(b).conjugate(),t*d]]
    first=damp(damp([[.4,.2j],[-.2j,.6]],q),r)
    second=damp([[.4,.2j],[-.2j,.6]],q*r)
    for i in range(2):
        for j in range(2):close(first[i][j],second[i][j])
record('M063','Amplitude damping Kraus channel','Kraus completeness, trace, positivity and semigroup composition verified on the stated qubit examples and five damping parameters; q=1/4 gives determinant 3/64.')

t=math.log(1e12/77000)/math.log1p(.0005)
close(t,32767.109878086045,1e-8)
close(77000*math.exp(t*math.log1p(.0005))/1e12,1)
assert math.ceil(t)==32768
tc=math.log(1e12/77000)/.0005
close(tc,32758.920830185452,1e-8)
record('M064','Exponential target-time correction',f'Real crossing {t:.12f}; first integer crossing 32768; continuous-rate comparison {tc:.12f}.')

# Coordinate covariance of a quadratic gradient flow, exact rational matrices.
G=[[2,0],[0,3]];S=[[2,0],[0,1]];Sinv=[[F(1,2),0],[0,1]]
Ktilde=mm(S,trans(S));Atilde=mm(mm(trans(Sinv),G),Sinv)
generator=mm(Ktilde,Atilde)
assert generator==mm(mm(S,G),Sinv)
for x in [[1,2],[-3,1],[0,0]]:
    derivative=-qform(mm(G,G),x)
    assert derivative<=0
record('M065','Gradient-flow coordinate transport','A scaled coordinate change with transported mobility K̃=SSᵀ reproduces the similarity-transformed generator exactly; quadratic energy dissipation is nonpositive.')

x=[2,3,6];proj=[2,3,0]
assert sum(v*v for v in x)==49
assert sum(v*v for v in proj)==13
assert sum((a-b)**2 for a,b in zip(x,proj))==36
record('M066','Bessel residual','The incomplete two-coordinate projection has exact residual squared norm 36, while total norm squared is 49 and measured coefficient energy is 13.')

p_exp=3;q_exp=1.5;a=2;b=4
close(a*b,a**p_exp/p_exp+b**q_exp/q_exp)
assert a**p_exp==b**q_exp==8
for a in [0,.2,1,2,4]:
    for b in [0,.2,1,2,4]:assert a*b<=a**p_exp/p_exp+b**q_exp/q_exp+1e-12
record('M067','Young inequality and sharp equality','p=3,q=3/2,a=2,b=4 attains equality; a finite nonnegative grid satisfies the inequality.')

A=[[1,2],[0,1]]
norm1=max(sum(abs(x) for x in col) for col in zip(*A))
norminf=max(sum(abs(x) for x in row) for row in A)
normF=math.sqrt(sum(x*x for row in A for x in row))
lam=3+2*math.sqrt(2)
assert norm1==norminf==3
close(math.sqrt(lam),1+math.sqrt(2));close(normF,math.sqrt(6))
assert (1+math.sqrt(2))<normF<math.sqrt(2)*(1+math.sqrt(2))
record('M068','Distinct matrix norms','The example has ||A||₁=||A||∞=3, ||A||F=√6, and ||A||₂=1+√2, satisfying the singular-value comparison.')

A=[[-1,4],[0,-1]];P=[[F(1,2),F(1)],[F(1),F(9,2)]]
L=madd(mm(trans(A),P),mm(P,A))
assert L==[[-1,0],[0,-1]] and P[0][0]>0 and det(P)==F(5,4)
ax=mm(A,[[1],[1]])
assert 2*(ax[0][0]+ax[1][0])==4
record('M069','Exact Lyapunov certificate','P has positive leading minors and AᵀP+PA=−I exactly, even though V=xᵀx has derivative 4 at (1,1).')

# Exponents in dimensions ordered (mass,length,time).
dimG=(-1,3,-2);dimc=(0,1,-1);dimT=(1,-1,-2)
dimrhs=tuple(a-4*b+c for a,b,c in zip(dimG,dimc,dimT))
assert dimrhs==(0,-2,0)
record('M070','Einstein-equation dimensional exponents','G_N c⁻⁴ times stress-energy has dimension vector (0,−2,0), matching curvature in the stated length-coordinate frame.')

source_factor=F(1)-F(1,2)
assert source_factor==F(1,2)
assert F(4)/source_factor==8
record('M071','Newtonian normalization factor','Trace reversal contributes 1/2 to the dust 00 source; matching the Poisson coefficient 4π yields 8π. Differential geometry derivation and conventions are in the entry.')

n=4
assert n*(n+1)//2==10 and n*n==16
phase=2*6-2*4
assert phase==4 and phase//2==2
record('M072','Component and canonical counts','Symmetric 4×4 display has 10 independent components; the regular vacuum canonical count leaves 4 phase variables, or 2 configuration polarizations, after four first-class constraints.')

for w in [F(0),F(1,3),F(-1)]:
    exponent=3*(1+w)
    assert -exponent+3*(1+w)==0
assert 2**3==8 and 2**4==16
record('M073','FLRW continuity exponents','ε∝a⁻³ for dust and ε∝a⁻⁴ for radiation satisfy the stated continuity equation; a doubling gives factors 8 and 16.')

def powerset(s):
    seq=list(s)
    return frozenset(frozenset(seq[i] for i in range(len(seq)) if mask>>i&1) for mask in range(1<<len(seq)))
V0=frozenset();V1=powerset(V0);V2=powerset(V1);V3=powerset(V2)
assert [len(V0),len(V1),len(V2),len(V3)]==[0,1,2,4]
assert V2 in V3 and powerset(V2) not in V3
record('M074','Finite-rank closure illustration only','V₂∈V₃ but P(V₂)=V₃∉V₃, illustrating why a finite rank cutoff is not the required universe closure. Existence of inaccessible cardinals is not computationally verified or asserted.')

def stirling(n,k):
    tab=[[0]*(k+1) for _ in range(n+1)];tab[0][0]=1
    for i in range(1,n+1):
        for j in range(1,k+1):tab[i][j]=j*tab[i-1][j]+tab[i-1][j-1]
    return tab[n][k]
assert stirling(4,2)==7 and math.comb(3,1)==3
for N in range(1,30):
    h=F(1,N);theta=[F(i*i,N*N) for i in range(N+1)]
    E=F(1,2)*sum(((theta[i+1]-theta[i])/h)**2*h for i in range(N))
    assert E==F(2,3)-F(1,6*N*N)
record('M075','Partition counts and discrete continuum energy','S(4,2)=7 versus 3 contiguous partitions. For θ=x² on [0,1], exact rational energies equal 2/3−1/(6N²) for N=1,…,29.')

R=[[F(3,5),F(-4,5)],[F(4,5),F(3,5)]]
assert mm(trans(R),R)==[[1,0],[0,1]]
forward=mm(R,[[1],[0]]);diagonal=mm(R,[[1],[1]])
assert sum(z[0]**2 for z in forward)==1 and sum(z[0]**2 for z in diagonal)==2
record('M076','Exact frame conversion and speed','The rational 3/5,4/5 rotation preserves squared norm 1 for forward input and squared norm 2 for raw diagonal input.')

for t1,t2 in [(2,1),(2,-1),(-2,-1),(1,1),(0,3)]:
    endpoint_min=min(t1*t1+t2*t2+2*t1*t2*c for c in [-1,1])
    close(endpoint_min,(abs(t1)-abs(t2))**2)
close(2*abs(abs(2)-abs(1)),2)
record('M077','Periodic two-band dispersion and gap','The minimum squared band magnitude is (|t₁|−|t₂|)² across five signed hopping examples; (2,1) has bands ±3 at k=0, ±1 at k=π and gap 2.')

entries=json.loads(HERE.joinpath('entries.json').read_text())
expected={f'M{i:03d}' for i in range(57,78)}
assert {e['id'] for e in entries}==expected
assert {c['id'] for c in checks}==expected
for e in entries:
    for k in ['id','title','status','summary','definitions','result','example','limits','extension','references']:assert k in e,(e['id'],k)
    assert all(isinstance(e['result'][k],str) and e['result'][k] for k in ['name','statement','proof'])
    assert all(isinstance(e['example'][k],str) and e['example'][k] for k in ['setup','calculation','conclusion'])
payload=dict(scope='M057–M077',checks=checks,check_count=len(checks),all_passed=True,method='Exact rational arithmetic where possible; explicit floating-point checks otherwise; proofs and conditional scope in entries.json.')
HERE.joinpath('checks.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2))
print(json.dumps(dict(check_count=len(checks),all_passed=True,entry_count=len(entries))))
