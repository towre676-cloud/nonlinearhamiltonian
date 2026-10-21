"""Portable finite certificates; general proof scopes remain in entries.json."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import json,math,cmath
HERE=Path(__file__).resolve().parent
checks=[]
def eq(a,b):assert a==b,(a,b)
def near(a,b,t=1e-10):assert abs(a-b)<t,(a,b)
def check(n,name,fn,scope):
    try:fn();status='pass';detail=scope
    except Exception as e:status='fail';detail=repr(e)
    checks.append(dict(id=f'Y25-09-{n:03d}',name=name,status=status,detail=detail))
def dot(x,y):return sum(a*b for a,b in zip(x,y))
def mv(A,v):return [dot(r,v) for r in A]
def mm(A,B):return [[dot(r,c) for c in zip(*B)] for r in A]
def rank(A,p=None):
    A=[[x%p if p else F(x) for x in row] for row in A];r=0
    for c in range(len(A[0])):
        k=next((k for k in range(r,len(A)) if A[k][c]),None)
        if k is None:continue
        A[r],A[k]=A[k],A[r];z=pow(A[r][c],-1,p) if p else 1/A[r][c]
        A[r]=[(z*x)%p if p else z*x for x in A[r]]
        for k in range(len(A)):
            if k==r:continue
            z=A[k][c];A[k]=[(a-z*b)%p if p else a-z*b for a,b in zip(A[k],A[r])]
        r+=1
        if r==len(A):break
    return r
def c1():
    M=[[F(5,16),F(1,16)],[F(1,16),F(5,16)]];x=[F(22,15),F(2,15)]
    eq([x[0]-mv(M,x)[0],x[1]-mv(M,x)[1]],[1,0]);eq(F(5,16)+F(1,16),F(3,8))
check(1,'Exact affine fixed point and norm',c1,'Rational matrix equation and symmetric eigenvalue bound; the general Banach theorem is proved in the entry.')
def c2():
    assert math.cos(.739)>.739 and math.cos(.740)<.740
    x=0.;inc=[]
    for _ in range(40):y=math.cos(x);inc.append(abs(y-x));x=y
    for a,b in zip(inc[1:],inc[2:]):assert b<=math.sin(1)*a+1e-15
    assert 0**2<math.cos(0)**2
check(2,'Cosine bracket and finite increment check',c2,'The displayed bracket is checked numerically; uniform interval contraction and infinite-tail bound are analytic proofs, not inferred from40 samples.')
def c3():
    A=[[1,1],[0,1]];a=[1,2];b=[4,1];d=[v-u for v,u in zip(b,mv(A,a))];eq(d,[1,-1])
    eq(dot([2,-1],b)-dot([2,1],a),3);eq(dot([1,1],d),0);assert 3<=2*sum(map(abs,d))
    G=[[2,-1]];c=[7];dg=[c[0]-mv(G,b)[0]]
    eq([c[0]-mv(mm(G,A),a)[0]],[mv(G,d)[0]+dg[0]])
check(3,'Cocycle and exact Lipschitz example',c3,'All transport defects and weighted scalars are exact integers; the general inequality is proved in prose.')
def c4():
    eq({(k%2,k%3) for k in range(6)},set(product(range(2),range(3))))
    eq(next(k for k in range(1,7) if k%2==0 and k%3==0),6)
    eq([2*F(1,2),3*F(1,3)],[1,1])
check(4,'Cokernel of diag2,3',c4,'All six CRT classes and rational zero-residual solution checked; integral obstruction remains nonzero.')
def c5():
    r=[1,-2,1]
    for w in ([1,1,1],[1,2,3],[2,1,0],[-1,0,1]):eq(dot(w,r),0)
    for k in range(3):x=[k,4-2*k,k];eq(dot([1,1,1],x),4);eq(dot([1,2,3],x),8)
check(5,'Rewrite invariants',c5,'Exact local annihilation and finite trace values; the written induction certifies arbitrary trace length.')
def c6():
    counts={p:1+sum((y*y+y-x*x*x+x*x+10*x+20)%p==0 for x in range(p) for y in range(p)) for p in (2,3,5,7)}
    eq(counts,{2:5,3:5,5:5,7:10})
    seq=[1,-2]
    for _ in range(3):seq.append(-2*seq[-1]-2*seq[-2])
    eq(seq,[1,-2,2,0,-4])
check(6,'11a1 point counts and Hecke recurrence',c6,'Exact finite-field enumeration at all four stated primes and integral prime-power coefficients; no rank or BSD claim checked.')
def c7():
    p=2;a=-2;den=[1,-(a*a-p),p*(a*a-p),-p**3];eq(den,[1,-2,4,-8])
    coeff=[1]
    for n in range(1,5):coeff.append(-sum(den[j]*coeff[n-j] for j in range(1,min(n,3)+1)))
    eq(coeff,[1,2,0,0,16])
check(7,'Symmetric-square local factor',c7,'Exact cubic coefficient and reciprocal-series certificate for p2,a−2; global functoriality is outside scope.')
def c8():
    N=8;f=lambda x:math.sin(x)+2*math.cos(2*x)
    for j in range(N):near(f(2*math.pi*j/N)+3*(math.cos(N*2*math.pi*j/N)-1),f(2*math.pi*j/N))
    eq(-3*N*N,-192)
check(8,'Fourier aliasing counterexample',c8,'Finite grid equality and exact second-derivative discrepancy; general nonidentifiability follows from the explicit family.')
def c9():
    eps=F(1,100);r=F(1,2);eq(r*r-eps,F(6,25))
    for z in (1+.1j,1-.1j):near((z-1)**2+.01,0);assert abs(2*(z-1))>0
check(9,'Two simple roots within a certified contour',c9,'Exact Rouche margin and numerical root substitution; the written complex-analysis theorem certifies total multiplicity.')
def val(n,p):
    if not n:return math.inf
    k=0
    while n%p==0:n//=p;k+=1
    return k
def c10():
    f=[27,0,9,27];g=[27,27,9,36,27]
    for v in (f,g):mu=min(val(a,3) for a in v);eq(mu,2);eq(next(i for i,a in enumerate(v) if val(a,3)==mu),2)
check(10,'Exact mu and lambda of primitive products',c10,'Integer coefficient valuations before and after multiplying by1+T; infinite-series invariance proved separately.')
def c11():
    j=lambda l:256*(1-l+l*l)**3/(l*l*(1-l)**2)
    vals=[F(3),F(-2),F(1,3),F(-1,2),F(3,2),F(2,3)]
    eq({j(l) for l in vals},{F(21952,9)})
check(11,'Six cross-ratio parameters and one j value',c11,'Exact rational six-point collision and pushforward example; no isogeny or physical classification claimed.')
def c12():
    roots=[x for x in range(163) if x*x%163==6];eq(len(roots),2);eq(pow(6,81,163),1)
    assert all(163%d for d in range(2,13))
check(12,'Quadratic residue at163',c12,'Two exact roots, Euler exponent and elementary primality check; semantic labels such as Tamagawa are not certified.')
def c13():
    shares=[F(1,3)]*3;eq(sum(shares),1);assert sum(shares+[F(1,3)])>1;eq(F(1,3)+F(2,3),1)
check(13,'Fractional ownership budget',c13,'Exact rational compatibility and incompatibility examples; no program race-freedom claim.')
def c14():
    transitions={0:[('a',1)],1:[('a',0)],2:[('a',2)]};R={(0,2),(1,2)}
    for x,y in R:
        for a,z in transitions[x]:assert any(a==b and (z,w) in R for b,w in transitions[y])
        for b,w in transitions[y]:assert any(a==b and (z,w) in R for a,z in transitions[x])
check(14,'Finite bisimulation certificate',c14,'Every forth/back transition checked; general trace preservation is the written induction theorem.')
def c15():
    h=lambda u:(u+math.sqrt(u))/2
    eq(h(.25),.375);near(h(.2)-.2,(math.sqrt(.2)-.2)/2);assert h(.2)>.2
    for u in (.001,.1,.7):assert u<h(u)<1
check(15,'Square-root smoothing and endpoint defect',c15,'Explicit finite counterexample to commutation and linearity; limit dynamics proved analytically.')
def c16():
    M=10**6;h=lambda x:(x+math.isqrt(x*M))//2
    eq(h(0),0);eq(h(1),500)
    for x in (0,1,2,30,12345,500000,M):
        err=(x+math.sqrt(x*M))/2-h(x);assert 0<=err<1
check(16,'Micro quantizer exact envelope',c16,'Exact integer samples and the500-fold input amplification; the all-input rounding bound is proved in the entry.')
def c17():
    seq=[1,-2]
    for _ in range(4):seq.append(-2*seq[-1]-2*seq[-2])
    eq(seq[:5],[1,-2,2,0,-4])
    for r,c in enumerate(seq):assert abs(c)<=(r+1)*2**(r/2)+1e-12
check(17,'Normalized Chebyshev local coefficients',c17,'Exact integral recurrence and finite sample bound; the trigonometric sum proves the general bound.')
def c18():
    times=[1,2,4,8,16];eq(len(times),5)
    logs=[math.log(3)-t/2 for t in times]
    for k in range(1,5):near(-(logs[k]-logs[k-1])/(times[k]-times[k-1]),.5)
    eq(F(2,100)/(16-8),F(1,400))
check(18,'Geometric sample count and decay estimate',c18,'Finite exact schedule and slope/noise calculations; no PDE or performance interpretation.')
def c19():
    A=[[1,2,3],[2,4,6],[0,1,1]];eq(rank(A),2)
    for p in (2,3,5,7):eq(rank(A,p),2)
    eq(mv(A,[-1,-1,1]),[0,0,0]);eq(rank([[7]]),1);eq(rank([[7]],7),0)
check(19,'Rational and modular ranks',c19,'Exact ranks, unit minor, null vector and rank-drop counterexample; prime moduli explicitly stated.')
def c20():
    times=[F(3*k,50) for k in range(6)]
    for i,j in product(range(6),repeat=2):
        if i<j:eq(times[j]-times[i],F(3*(j-i),50));assert times[j]>times[i]
    eq(times[-1]-times[0],F(3,10))
check(20,'Exact finite monotonicity certificate',c20,'All15 ordered pairs and telescoping gaps checked with rational timestamps.')
def c21():
    for z in (-2,-.3,0,.8,2):
        k=1.3;u=2*k*k/math.cosh(k*z)**2;tanh=math.tanh(k*z)
        # F''=4 k²F−3F², derived independently through tanh differentiation.
        second=4*k*k*u*tanh*tanh-2*k*k*u/(math.cosh(k*z)**2)
        near(second,4*k*k*u-3*u*u)
check(21,'KdV traveling-wave profile identity',c21,'Finite evaluations check the exact differentiated formula; cancellation and mass integral are proved analytically.')

(HERE/'checks.json').write_text(json.dumps({'checks':checks,'scope':'Exact finite certificates and labeled numerical examples accompany, but do not replace, the written general proofs.'},ensure_ascii=False,indent=2)+'\n')
print(sum(c['status']=='pass' for c in checks),'/',len(checks),'pass')
for c in checks:
    if c['status']!='pass':print(c)
assert all(c['status']=='pass' for c in checks)
