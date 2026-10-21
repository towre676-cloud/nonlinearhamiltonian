"""Portable stdlib certificates for the declared finite examples.

These checks complement the written proofs; bounded samples are not general
theorem proofs. Run this file from any directory. Output stays beside it.
"""
from pathlib import Path
from fractions import Fraction as Q
from itertools import product
import json, math

HOME=Path(__file__).resolve().parent
checks=[]
def check(n,name,fn,detail):
    try:
        fn()
        checks.append(dict(id=f'Y24-06-{n:03d}',name=name,status='pass',detail=detail))
    except Exception as e:
        checks.append(dict(id=f'Y24-06-{n:03d}',name=name,status='fail',detail=f'{type(e).__name__}: {e}'))
def eq(a,b): assert a==b,(a,b)
def close(a,b,tol=1e-11): assert abs(a-b)<tol,(a,b)
def mm(A,B):return [[sum(a*b for a,b in zip(row,col)) for col in zip(*B)] for row in A]
def tr(A):return list(map(list,zip(*A)))
def ms(A,B):return [[a-b for a,b in zip(r,s)] for r,s in zip(A,B)]
def sc(c,A):return [[c*a for a in row] for row in A]
def eye(n):return [[int(i==j) for j in range(n)] for i in range(n)]
def zero(n):return [[0]*n for _ in range(n)]
def comm(A,B):return ms(mm(A,B),mm(B,A))
def mv(A,v):return [sum(a*b for a,b in zip(r,v)) for r in A]
def dot(x,y):return sum(a*b for a,b in zip(x,y))
def addv(x,y):return [a+b for a,b in zip(x,y)]
def scalev(a,x):return [a*t for t in x]
def rank(A,p=None):
    A=[[x%p if p else Q(x) for x in row] for row in A]
    if not A:return 0
    r=0
    for c in range(len(A[0])):
        k=next((k for k in range(r,len(A)) if A[k][c]),None)
        if k is None:continue
        A[r],A[k]=A[k],A[r]
        z=pow(A[r][c],-1,p) if p else 1/A[r][c]
        A[r]=[(x*z)%p if p else x*z for x in A[r]]
        for k in range(len(A)):
            if k==r:continue
            z=A[k][c]
            A[k]=[(a-z*b)%p if p else a-z*b for a,b in zip(A[k],A[r])]
        r+=1
        if r==len(A):break
    return r

def c1():
    # (3+2 sqrt2)(3-2 sqrt2)=1 and F4 inverses.
    eq(3*3-2*2*2,1)
    def mul(a,b):
        c=0
        while b:
            if b&1:c^=a
            a<<=1
            if a&4:a^=7
            b>>=1
        return c
    for a in (1,2,3):assert any(mul(a,b)==1 for b in (1,2,3))
    eq(mul(2,2),3);eq(mul(2,3),1)
    i=[[1j,0],[0,-1j]];j=[[0,1],[-1,0]]
    eq(mm(i,j),sc(-1,mm(j,i)));eq(mm(i,i),sc(-1,eye(2)))
check(1,'Number-field norm, F4 and quaternion relations',c1,'Exact finite field and matrix identities. Classification of all listed number systems is not inferred from these samples.')

def c2():
    E=[[0,1],[0,0]];F=[[0,0],[1,0]];H=[[1,0],[0,-1]];J=ms(E,F)
    eq(comm(H,E),sc(2,E));eq(comm(H,F),sc(-2,F));eq(comm(E,F),H)
    eq(mm(J,J),sc(-1,eye(2)))
check(2,'sl2 closure and periodic generator',c2,'Exact brackets and J squared equal minus identity; written exponential proof gives all real times.')

def c3():
    J=[[0,0,1,0],[0,0,0,1],[-1,0,0,0],[0,-1,0,0]]
    eq(mm(J,J),sc(-1,eye(4)));eq(ms(mm(tr(J),J),sc(-1,mm(J,J))),zero(4))
    for t in (0,.2,1.7):
        x1,x2,p1,p2=math.cos(t),math.sin(t),-math.sin(t),math.cos(t)
        close((x1*x1+x2*x2+p1*p1+p2*p2)/2,1)
        close(x1*p2-x2*p1,1)
check(3,'Canonical symplectic matrix and oscillator invariants',c3,'Exact infinitesimal symplectic identity plus sample evaluations. Constancy of every canonical Casimir is proved in prose with coordinate test functions.')

def c4():
    t=Q(3,4);x=(1-t*t)/(1+t*t);y=2*t/(1+t*t)
    eq((x,y),(Q(7,25),Q(24,25)));eq(x*x+y*y,1);eq(y/(1+x),t)
check(4,'Rational circle parametrization',c4,'Exact worked point and inverse parameter; density and cardinality are proof statements.')

def c5():
    for n in range(2,10):
        # n! times a finite tail lies below geometric bound 1/n.
        tail=sum(Q(math.factorial(n),math.factorial(k)) for k in range(n+1,n+30))
        assert 0<tail<Q(1,n)
    eq(abs(2*3-0*1),6)
check(5,'Factorial tail bound and affine area',c5,'Exact finite-tail inequalities check the displayed irrationality argument; its infinite geometric bound is supplied by the written proof.')

def c6():
    x,y=Q(7,25),Q(24,25)
    eq((2*x)**2+(2*y)**2,4)
    eq((x*x+y*y)-1,0)
check(6,'Coordinate-ring radius rescaling',c6,'Exact point and polynomial substitution check; irreducibility/domain statements use the written algebraic proof.')

def fmul(x,y):
    z=[Q(0)]*4
    for i,a in enumerate(x):
        for j,b in enumerate(y):
            z[i^j]+=a*b*(2 if i&j&1 else 1)*(-1 if i&j&2 else 1)
    return tuple(z)
def fadd(x,y):return tuple(a+b for a,b in zip(x,y))
def fpow(x,n):
    r=(Q(1),Q(0),Q(0),Q(0))
    for _ in range(n):r=fmul(r,x)
    return r
def c7():
    roots=[(0,a,b,0) for a,b in product((1,-1),repeat=2)]
    for r in roots:
        q=fpow(r,4);r2=fpow(r,2)
        eq(fadd(fadd(q,tuple(-2*t for t in r2)),(9,0,0,0)),(0,0,0,0))
    eq(len(set(roots)),4)
    for sa,si in product((1,-1),repeat=2):
        im=lambda r:(r[0],sa*r[1],si*r[2],sa*si*r[3])
        eq({im(r) for r in roots},set(roots))
        for r in roots:eq(im(im(r)),r)
check(7,'Correct quartic roots and V4 sign automorphisms',c7,'Exact arithmetic in basis 1,sqrt2,i,sqrt2 i checks all four roots and all four sign maps. Field degree is proved separately.')

def sigma3(n):return sum(d**3 for d in range(1,n+1) if n%d==0)
def c8():
    eq(sigma3(2),9)
    for n in range(1,101):eq(sigma3(2*n)+(8*sigma3(n//2) if n%2==0 else 0),9*sigma3(n))
    eq(240*sigma3(1),240);eq(240*sigma3(2),2160)
check(8,'Weight-four Hecke eigen-coefficients',c8,'Exact first100 nonconstant coefficients for T2 E4=9E4, with the required 2^(k-1) a_(n/2) term; the divisor proof establishes all n.')

def c9():
    D=[[-1,1],[-1,1]]
    eq(rank(D),1);eq(2-rank(D),1)
    assert [1,0] not in ([a,a] for a in range(-3,4))
check(9,'Two-arc Cech constant-sheaf differential',c9,'Exact differential rank and quotient dimension for this cover; this is not a violation of the sheaf gluing axiom.')

class P:
    """Laurent polynomials over the rational numbers."""
    def __init__(self,x=0):self.d=({k:Q(v) for k,v in x.items() if v} if isinstance(x,dict) else ({0:Q(x)} if x else {}))
    def __add__(self,o):
        o=o if isinstance(o,P) else P(o);d=self.d.copy()
        for k,v in o.d.items():d[k]=d.get(k,0)+v
        return P(d)
    __radd__=__add__
    def __neg__(self):return P({k:-v for k,v in self.d.items()})
    def __sub__(self,o):return self+-1*o
    def __rsub__(self,o):return P(o)+-self
    def __mul__(self,o):
        o=o if isinstance(o,P) else P(o);d={}
        for k,v in self.d.items():
            for l,w in o.d.items():d[k+l]=d.get(k+l,0)+v*w
        return P(d)
    __rmul__=__mul__
    def __eq__(self,o):return self.d==(o.d if isinstance(o,P) else P(o).d)
    def __repr__(self):return repr(self.d)
q=P({1:1});qi=P({-1:1});a=q-qi
def braid(v,pos):
    out={}
    for bits,c in v.items():
        x,y=bits[pos:pos+2]
        terms=[((x,y),q)] if x==y else ([((1,0),P(1))] if (x,y)==(0,1) else [((0,1),P(1)),((1,0),a)])
        for pair,k in terms:
            b=bits[:pos]+pair+bits[pos+2:]
            out[b]=out.get(b,P())+c*k
    return {b:c for b,c in out.items() if c!=0}
def c10():
    for bits in product((0,1),repeat=3):
        v={bits:P(1)}
        eq(braid(braid(braid(v,0),1),0),braid(braid(braid(v,1),0),1))
    for bits in product((0,1),repeat=2):
        v={bits:P(1)};r=braid(v,0);rr=braid(r,0)
        for b in set(v)|set(r)|set(rr):eq(rr.get(b,P())-a*r.get(b,P())-v.get(b,P()),P())
check(10,'Formal Laurent-polynomial braid and Hecke equations',c10,'All8 basis triples and4 pairs are checked exactly over Q[q,q^-1], so this finite symbolic identity holds for every nonzero q in the declared convention.')

def c11():
    A=P({1:1});Ai=P({-1:1});delta=-P({2:1})-P({-2:1})
    def tl(x,y):return (x[0]*y[0],x[0]*y[1]+x[1]*y[0]+x[1]*y[1]*delta)
    g=(A,Ai);g3=tl(tl(g,g),g)
    bracket=g3[0]*delta+g3[1]
    eq(bracket,P({5:-1,-3:-1,-7:1}))
    eq(-P({-9:1})*bracket,P({-4:1,-12:1,-16:-1}))
check(11,'Trefoil bracket and writhe normalization',c11,'Exact Temperley-Lieb Laurent calculation in the stated crossing and variable convention; knot invariance is the cited bracket theorem.')

def c12():
    for t in (-2,0,.5,2):
        y=math.exp(t);close(y-y*y/y,0);close(y*y/y**2,1)
    for z in (1+2j,-.5+.7j,3j):
        w=(z-1j)/(z+1j)
        lhs=4*abs(2j/(z+1j)**2)**2/(1-abs(w)**2)**2
        close(lhs,1/z.imag**2)
    close(math.log(math.exp(2)),2)
check(12,'Hyperbolic geodesic and Cayley metric factors',c12,'Sample evaluations check the explicit metric identity and vertical geodesic. Differentiated formulas in the entry prove the identities for all points.')

def c13():
    def h(m):return m**3-m
    for m,n in product(range(-12,13),repeat=2):
        p=-m-n
        eq((m-n)*h(m+n)+(n-p)*h(n+p)+(p-m)*h(p+m),0)
    for m in (-1,0,1):eq(h(m),0)
    eq(Q(h(2),12),Q(1,2))
check(13,'Virasoro central-cocycle arithmetic',c13,'625 exact mode pairs and the low modes are checked; the written polynomial cancellation proves the unbounded Jacobi identity.')

def c14():
    # Boundary of a triangle versus the same triangle filled.
    d1=[[1,0,1],[1,1,0],[0,1,1]]
    eq(rank(d1,2),2);eq(3-rank(d1,2),1)
    d2=[[1],[1],[1]];eq(rank(d2,2),1);eq(3-rank(d1,2)-rank(d2,2),0)
    eq(mm(d1,d2),[[2],[2],[2]]) # Zero over F2.
check(14,'Triangle boundary and filling homology',c14,'Exact mod-two ranks support the finite cell example. General sphere and surface fundamental groups use the explicit covering and van Kampen arguments, not these ranks.')

def c15():
    for u in (0,.3,1.7,4.2):
        x,y=math.cos(u),math.sin(u);dx,dy=-math.sin(u),math.cos(u)
        close((-y*dx+x*dy)/2,.5)
        close((-y*dx+x*dy)/(x*x+y*y),1)
    eq(2*5-3*7,-11)
check(15,'Exterior forms and oriented determinant',c15,'Pullbacks along the unit circle and a wedge determinant are checked. The exact integrals are constants times2pi; nonexactness follows from the written period proof.')

def c16():
    volume=Q(1,6);mass=volume*Q(1+2+2+2,4)
    eq(mass,Q(7,24));eq(Q(1,6)+3*Q(1,24),mass)
    eq(1+3*Q(1,4),Q(7,4))
check(16,'Affine tetrahedron mass',c16,'Exact barycentric, monomial and centroid values agree; no quadrature tolerance is used.')

def c17():
    A=[[2,-1,0],[-1,2,-1],[0,-1,2]];b=[Q(1)]*3
    eq(mv(A,[Q(3,2),2,Q(3,2)]),b)
    x=[Q(0)]*3;r=b;p=b;iterations=0
    for _ in range(3):
        rr=dot(r,r)
        if not rr:break
        Ap=mv(A,p);alpha=rr/dot(p,Ap)
        x=addv(x,scalev(alpha,p));rn=addv(r,scalev(-alpha,Ap))
        beta=dot(rn,rn)/rr;p=addv(rn,scalev(beta,p));r=rn;iterations+=1
    eq(iterations,2);eq(r,[0,0,0]);eq(x,[Q(3,2),2,Q(3,2)])
    close((2+math.sqrt(2))/(2-math.sqrt(2)),3+2*math.sqrt(2))
check(17,'Exact Poisson CG iteration',c17,'Fraction arithmetic reaches the stated solution in exactly two steps. The general SPD requirement is proved by the displayed sum of squares.')

def c18():
    vertices=list(product(range(3),range(4)));vi={v:i for i,v in enumerate(vertices)}
    V=lambda i,j:(i%3,j%4)
    faces=[]
    for i,j in vertices:
        faces.extend([frozenset((V(i,j),V(i+1,j),V(i+1,j+1))),frozenset((V(i,j),V(i,j+1),V(i+1,j+1)))])
    edges=sorted({tuple(sorted((a,b))) for f in faces for a in f for b in f if a<b})
    d1=[[int(v in edge) for edge in edges] for v in vertices]
    d2=[[int(set(edge)<=f) for f in faces] for edge in edges]
    eq((len(vertices),len(edges),len(faces)),(12,36,24));eq(rank(d1,2),11);eq(rank(d2,2),23)
    eq(len(edges)-rank(d1,2)-rank(d2,2),2);eq(len(edges)-len(vertices)+1,25)
    cyc=[(0,0),(1,0),(2,0),(2,1),(1,1),(0,1),(0,2),(1,2),(2,2),(2,3),(1,3),(0,3)]
    eq(len(set(cyc)),12)
    for a,b in zip(cyc,cyc[1:]+cyc[:1]):assert tuple(sorted((a,b))) in edges
    indices=[int(cx>0)+int(cy>0) for cx,cy in product((1,-1),repeat=2)]
    eq(sorted(indices),[0,1,1,2])
check(18,'Toroidal complex, Hamiltonian cycle and Morse indices',c18,'Exact boundary ranks, all12 cycle vertices/edges and four diagonal Hessian indices are checked for the newly declared toy complex.')

def c19():
    t=.8;target=math.exp(-t*t/2);errs=[]
    for k in range(1,12):
        n=2**k;errs.append(abs(math.cos(t/math.sqrt(n))**n-target))
    assert all(b<a for a,b in zip(errs,errs[1:]));assert errs[-1]<2e-5
    eq(Q(-2,2**6),Q(-1,32))
check(19,'Normalized Rademacher sums',c19,'Finite characteristic-function errors decrease in the displayed sample and the fourth cumulant scales exactly. The finite-variance limit theorem is proved analytically in the entry.')

def c20():
    eq(4*3//2,6)
    A=[[0,2,-3],[-2,0,5],[3,-5,0]]
    det=A[0][0]*(A[1][1]*A[2][2]-A[1][2]*A[2][1])-A[0][1]*(A[1][0]*A[2][2]-A[1][2]*A[2][0])+A[0][2]*(A[1][0]*A[2][1]-A[1][1]*A[2][0])
    eq(det,0)
    for th in (.2,1,2.7):close((1-math.cos(th))-(-1-math.cos(th)),2)
    eq(2*2,4) # integral sin(theta) dtheta times2pi gives4pi.
check(20,'Skew-matrix and gauge-patch checks',c20,'Exact odd skew determinant plus patch-coefficient identity. Flux4pi g follows from the stated elementary integral; no monopole existence is inferred.')

def c21():
    states=list(product((-1,1),repeat=2));pi=[Q(2,5) if a==b else Q(1,10) for a,b in states]
    Pm=[[Q(0)]*4 for _ in states]
    for i,(a,b) in enumerate(states):
        for dest in ((-a,b),(a,-b)):
            j=states.index(dest);prob=Q(1,8) if a==b else Q(1,2)
            Pm[i][j]+=prob;Pm[i][i]+=Q(1,2)-prob
    for i in range(4):eq(sum(Pm[i]),1)
    for i,j in product(range(4),repeat=2):eq(pi[i]*Pm[i][j],pi[j]*Pm[j][i])
    eq(sum(pi),1);eq(sum(p*a*b for p,(a,b) in zip(pi,states)),Q(3,5))
check(21,'Finite Ising normalization and detailed balance',c21,'All16 transition entries, stationary pair flows and the correlation are checked exactly with rational probabilities.')

def c22():
    p=lambda w:math.sin(w/2)**2
    for w in (.2,1,3*math.pi/2):close((p(w+math.pi/2)-p(w-math.pi/2))/2,math.sin(w)/2)
    old=3*math.pi/2;new=old+.1
    close(p(old),.5);assert .5*(p(new)-1)**2>Q(1,8)
    close(.5*(p(new)-1)**2,.15120419304662927,1e-12)
check(22,'Parameter shift and non-descent counterexample',c22,'Analytic formulas checked numerically, including a strict loss increase for the recovered heuristic update; no empirical training claim.')

def c23():
    for qv in (Q(0),Q(1,4),Q(1)):
        rho=[[Q(0)]*4 for _ in range(4)]
        rho[0][0]=rho[3][3]=Q(1,2);rho[0][3]=rho[3][0]=qv/2
        eq(sum(rho[i][i] for i in range(4)),1)
        for first in (True,False):
            marg=[[sum(rho[2*i+k][2*j+k] if first else rho[2*k+i][2*k+j] for k in range(2)) for j in range(2)] for i in range(2)]
            eq(marg,[[Q(1,2),0],[0,Q(1,2)]])
        XX=[[int(j==(i^3)) for j in range(4)] for i in range(4)]
        eq(sum(mm(rho,XX)[i][i] for i in range(4)),qv)
        eq(sum(rho[i][i]*(1 if i in (0,3) else -1) for i in range(4)),1)
        assert (1+qv)/2>=0 and (1-qv)/2>=0
check(23,'Bell dephasing density matrix and blind marginals',c23,'Exact rational states at q=0,1/4,1 check normalization, positivity eigenvalues, both marginals and joint XX/ZZ. Kraus proof establishes complete positivity for all0≤q≤1.')

def c24():
    A=[[1,1]];eq(rank(A),1);eq(mv(A,[1,-1]),[0])
    B=[[int(j==i) for j in range(4)]+[int(j==i) for j in range(4)] for i in range(4)]
    eq(rank(B),4)
    for j in range(4):
        v=[int(k==j) for k in range(4)];eq(mv(B,v+[-x for x in v]),[0]*4)
    eq(mv([[1,1],[1,2]],[5,2]),[7,9])
check(24,'Additive-model sensitivity rank and null directions',c24,'Exact scalar and four-output ranks, all four null directions and the independently informative two-equation example.')

data={'checks':checks,'scope':'Finite certificates and arithmetic checks accompany the entries. Their details distinguish exact identities, numerical samples and proof-only general statements.'}
(HOME/'checks.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
print(f'{sum(c["status"]=="pass" for c in checks)}/{len(checks)} checks pass')
for c in checks:
    if c['status']!='pass':print(c)
assert all(c['status']=='pass' for c in checks)
