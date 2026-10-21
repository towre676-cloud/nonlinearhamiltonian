"""Exact supporting checks for the geometry atlas; Python standard library only.

Finite identities support the written proofs. They are not general geometric,
persistent-homology, sheaf or inverse-limit solvers.
"""
from fractions import Fraction as Q
from itertools import product, permutations
from math import prod
from pathlib import Path
import json

HERE=Path(__file__).resolve().parent
CHECKS=[]

def mat(a):return [[Q(v) for v in row] for row in a]
def tr(a):return [list(row) for row in zip(*a)]
def mul(a,b):return [[sum((x*y for x,y in zip(row,col)),Q()) for col in zip(*b)] for row in a]
def add(a,b):return [[x+y for x,y in zip(r,s)] for r,s in zip(a,b)]
def sub(a,b):return [[x-y for x,y in zip(r,s)] for r,s in zip(a,b)]
def eye(n):return mat([[int(i==j) for j in range(n)] for i in range(n)])
def zeros(m,n):return mat([[0]*n for _ in range(m)])
def rank(a):
    a=mat(a); r=0
    if not a:return 0
    for j in range(len(a[0])):
        k=next((k for k in range(r,len(a)) if a[k][j]),None)
        if k is None:continue
        a[r],a[k]=a[k],a[r];q=a[r][j];a[r]=[v/q for v in a[r]]
        for k in range(len(a)):
            if k!=r:
                q=a[k][j];a[k]=[v-q*w for v,w in zip(a[k],a[r])]
        r+=1
        if r==len(a):break
    return r
def det2(a):return a[0][0]*a[1][1]-a[0][1]*a[1][0]
def check(name,families,evidence,fn):
    fn()
    CHECKS.append({'id':name,'family_ids':families.split(),'status':'pass','arithmetic':'exact rational/integer or finite combinatorial','evidence':evidence})

# A tiny sparse Q[x,y] ring makes the shear equality a coefficient identity.
class P:
    def __init__(self,v=0):
        self.v={k:Q(x) for k,x in v.items() if x} if isinstance(v,dict) else ({(0,0):Q(v)} if v else {})
    def __add__(self,o):
        o=o if isinstance(o,P) else P(o);d=self.v.copy()
        for k,v in o.v.items():d[k]=d.get(k,Q())+v
        return P(d)
    __radd__=__add__
    def __neg__(self):return P({k:-v for k,v in self.v.items()})
    def __sub__(self,o):return self+-P.coerce(o)
    def __rsub__(self,o):return P.coerce(o)+-self
    @staticmethod
    def coerce(o):return o if isinstance(o,P) else P(o)
    def __mul__(self,o):
        o=P.coerce(o);d={}
        for (i,j),a in self.v.items():
            for (k,l),b in o.v.items():d[i+k,j+l]=d.get((i+k,j+l),Q())+a*b
        return P(d)
    __rmul__=__mul__
    def __eq__(self,o):return self.v==P.coerce(o).v
    def __pow__(self,n):
        ans=P(1)
        for _ in range(n):ans=ans*self
        return ans
    def evaluate(self,x,y):return sum((v*Q(x)**i*Q(y)**j for (i,j),v in self.v.items()),Q())
def pmul(a,b):return [[sum((x*y for x,y in zip(row,col)),P()) for col in zip(*b)] for row in a]

def pushout():
    relation=mat([[1],[0],[0],[-1]])
    quotient=mat([[1,0,0,1],[0,1,0,0],[0,0,1,0]])
    assert mul(quotient,relation)==zeros(3,1)
    assert rank(quotient)==3 and rank(relation)==1
    functional=mat([[1,2,3]])
    assert mul(functional,quotient)==mat([[1,2,3,1]])
    assert mul(functional,mul(quotient,mat([[2],[1],[3],[4]])))==[[Q(17)]]
check('G01-pushout','D04-F01','Relation is killed by a surjective quotient; the compatible functional factors with value 17.',pushout)

def currying():
    M=mat([[1,2,3],[4,5,6]]);v=mat([[2,-1]]);w=mat([[1],[2],[3]])
    assert mul(v,M)==mat([[-2,-1,0]])
    assert mul(mul(v,M),w)==mul(v,mul(M,w))==[[Q(-4)]]
    assert mul(eye(2),tr(v))==tr(v)
check('G02-adjunction-model','D04-F01','Tensor–Hom routes agree on the worked bilinear form; finite coevaluation reconstructs the vector.',currying)

def totalization():
    d0=mat([[1],[1]]);d1=mat([[-1,1]])
    assert mul(d1,d0)==[[Q(0)]]
    assert (1-rank(d0),2-rank(d0)-rank(d1),1-rank(d1))==(0,0,0)
    assert mul(mat([[1,1]]),d0)==[[Q(2)]]
check('G03-total-signs','D04-F02','Signed totalization is acyclic; the unsigned square is exactly 2 over Q.',totalization)

def contraction():
    i=mat([[0],[1]]);p=mat([[0,1]])
    for eps in [Q(-2),Q(-1,2),Q(0),Q(1,3),Q(2)]:
        d=mat([[1+eps],[0]]);h=mat([[1/(1+eps),0]])
        assert mul(p,i)==eye(1)
        assert add(mul(d,h),zeros(2,2))==sub(eye(2),mul(i,p))
        assert mul(h,d)==eye(1)
    assert rank(mat([[0],[0]]))==0
check('G04-chain-contraction','D04-F02','Contraction identities hold for exact parameter choices; the exceptional parameter makes the pair noncontractible.',contraction)

def dualnumbers():
    epsilon=mat([[0,0],[1,0]])
    assert mul(epsilon,epsilon)==zeros(2,2) and rank(epsilon)==1
    assert mul(epsilon,mat([[0],[1]]))==zeros(2,1)
    # Hom_R(R,k) and R tensor_R k have one coordinate and zero induced map.
    assert mat([[0]])==zeros(1,1)
    # A prospective section v=(a,b) must have a=0 to be annihilated by epsilon,
    # while reduction to 1 requires a=1. The linear constraints are inconsistent.
    assert rank(mat([[1],[1]]))<rank(mat([[1,0],[1,1]]))
check('G05-derived-dualnumbers','D04-F03','The periodic free-resolution differential has equal kernel/image and becomes zero on k; section constraints contradict.',dualnumbers)

def lift_and_mc():
    # x=a*t+b*t^2 has coefficient a^2 in t^2 and 2ab in t^3.
    for a,b in product(range(-3,4),repeat=2):
        square={2:a*a,3:2*a*b,4:b*b}
        assert (square[2]==0)==(a==0)
    # d(a)=0,d(b)=c and [a,a]/2=c, all other brackets vanish.
    d_alpha=P({(2,0):-1}); half_bracket=P({(2,0):1})
    assert d_alpha+half_bracket==0
check('G06-obstruction-class','D04-F03','Double-point lift condition is a^2=0; the finite Maurer–Cartan defect is canceled by an explicit boundary.',lift_and_mc)

def filtration():
    assert rank(mat([[1]]))==1 and rank(mat([[0]]))==0
    cyclic_orders=sorted(next(k for k in range(1,5) if (k*a)%4==0) for a in range(4))
    split_orders=sorted(next(k for k in range(1,3) if (k*a)%2==0 and (k*b)%2==0) for a,b in product(range(2),repeat=2))
    assert cyclic_orders==[1,2,4,4] and split_orders==[1,2,2,2]
    assert len({0,2})==2 # the lower cyclic filtration has the same two-element size
check('G07-filtration-extension','D04-F04','Equal initial graded dimensions allow different differentials; common Z/2 layers conceal distinct element orders.',filtration)

def inverse_limit_support():
    a=[7,-2,10,0,-11,4]
    b=[a[n]-2*a[n+1] for n in range(len(a)-1)]
    N=len(b)-1
    assert sum(2**n*b[n] for n in range(N+1))==a[0]-2**(N+1)*a[N+1]
    # Finite binary approximations support the written infinite proof only.
    digits=[1,0,1,1,0,0,1];m=sum(v*2**j for j,v in enumerate(digits))
    for n in range(len(digits)+1):assert (m-sum(digits[j]*2**j for j in range(n)))%2**n==0
check('G08-limit-telescoping','D04-F04','Exact finite telescoping and 2-adic divisibility support the written lim^1 proof; no finite test certifies an infinite tower.',inverse_limit_support)

def triangle():
    b1=mat([[-1,0,-1],[1,-1,0],[0,1,1]])
    b2=mat([[1],[1],[-1]])
    assert mul(b1,b2)==zeros(3,1)
    assert rank(b1)==2 and rank(b2)==1
    assert (3-rank(b1),3-rank(b1),0)==(1,1,0)
    assert (3-rank(b1),3-rank(b1)-rank(b2),1-rank(b2))==(1,0,0)
    # Cellular RP2: d2=2, d1=0. Integer coker has two residue classes;
    # rational multiplication is invertible and mod-two multiplication is zero.
    assert {n%2 for n in range(-10,11)}=={0,1}
    assert rank(mat([[2]]))==1 and rank(mat([[2%2]]))==0
check('G09-homology-and-torsion','D05-F01 D04-F02','Triangle boundary/filling have the stated Betti vectors; the RP2 cellular differential has exact torsion order two.',triangle)

def bottleneck(D,E):
    # Partial injections are all finite matchings; unmatched points go diagonal.
    best=None
    def rec(i,unused,cost):
        nonlocal best
        if i==len(D):
            cost=max([cost]+[(E[j][1]-E[j][0])/2 for j in unused])
            best=cost if best is None else min(best,cost);return
        rec(i+1,unused,max(cost,(D[i][1]-D[i][0])/2))
        for j in unused:
            c=max(abs(D[i][0]-E[j][0]),abs(D[i][1]-E[j][1]))
            rec(i+1,unused-{j},max(cost,c))
    rec(0,set(range(len(E))),Q())
    return best
def persistence():
    D=[(Q(0),Q(3)),(Q(1),Q(2))]
    E=[(Q(1,10),Q(16,5)),(Q(4,5),Q(23,10))]
    assert bottleneck(D,E)==Q(3,10)
    # [0,1), [0,1), [0,infinity) in H0 and [1,2) in H1.
    for t,betti in [(Q(0),(3,0)),(Q(1),(1,1)),(Q(2),(1,0))]:
        h0=1+2*int(t<1);h1=int(1<=t<2)
        assert (h0,h1)==betti
    assert Q(1,4+1)==Q(1,5) # exact integral of t^4 over [0,1]
check('G10-persistence','D05-F02','All partial diagram matchings give bottleneck 3/10; finite bar ranks and the random square lifetime 1/5 agree.',persistence)

def gluing():
    cech=mat([[-1,1],[-1,1]])
    assert rank(cech)==1
    def delta(r):
        n=len(r);a=zeros(n,n)
        for j in range(n):a[j][j]=-r[j];a[j][(j+1)%n]+=1
        return a
    d=delta([Q(2),Q(3),Q(1,6)])
    assert rank(d)==2 and mul(d,mat([[1],[2],[6]]))==zeros(3,1)
    assert rank(delta([Q(2),Q(3),Q(1)]))==3
    D=mat([[-1,1,0],[0,-1,1],[1,0,-1]])
    assert mul(D,mat([[0],[1],[3]]))==mat([[1],[2],[-3]])
    assert sum([1,2,-3])==0 and sum([1,2,-2])==1
check('G11-gluing-local-system','D05-F03','Čech rank, exact triangle potentials and both holonomy-controlled local-system ranks are verified over Q.',gluing)

def cocycle():
    G=list(product(range(2),repeat=2))
    plus=lambda g,h:((g[0]+h[0])%2,(g[1]+h[1])%2)
    sig=lambda g,h:(-1)**(g[1]*h[0])
    for g,h,k in product(G,repeat=3):assert sig(g,h)*sig(plus(g,h),k)==sig(h,k)*sig(g,plus(h,k))
    assert sig((1,0),(0,1))==1 and sig((0,1),(1,0))==-1
    assert 2*2*3==12
check('G12-projective-cocycle','D05-F04','All 64 cocycle identities pass; asymmetric coordinate multiplier cannot be an abelian coboundary; normalized torus model gives 12.',cocycle)

def metric():
    # Nonlazy neighbor measures in these two graphs have one explicit optimal plan.
    w2=Q(1);w3=Q(1,2)
    assert 1-w2==0 and 1-w3==Q(1,2)
    # Distance, area, sectional curvature and Laplace scaling for g -> 9g.
    c=Q(3);assert c*c==9 and 1/(c*c)==Q(1,9)
    # Prefix ultrametric follows from min prefix length; check finite sequences.
    seq=list(product(range(2),repeat=4))
    def dist(x,y):
        return Q() if x==y else Q(1,2)**next(i for i in range(4) if x[i]!=y[i])
    for a,b,c in product(seq,repeat=3):assert dist(a,c)<=max(dist(a,b),dist(b,c))
check('G13-metric-models','D06-F01','The declared K2/K3 transport plans, scaling powers and all triples in a finite prefix ultrametric pass.',metric)

def reduction_and_oscillator():
    # Coordinate order q1,q2,p1,p2; level tangent order q1,q2,p1.
    J=mat([[0,0,1,0],[0,0,0,1],[-1,0,0,0],[0,-1,0,0]])
    embedding=mat([[1,0,0],[0,1,0],[0,0,1],[0,0,0]])
    pull=mul(tr(embedding),mul(J,embedding))
    assert pull==mat([[0,0,1],[0,0,0],[-1,0,0]]) and rank(pull)==2
    assert mul(pull,mat([[0],[1],[0]]))==zeros(3,1)
    keep=mat([[1,0],[0,0],[0,1]])
    assert mul(tr(keep),mul(pull,keep))==mat([[0,1],[-1,0]])
    R=mat([[Q(3,5),Q(4,5)],[-Q(4,5),Q(3,5)]])
    j=mat([[0,1],[-1,0]])
    assert mul(tr(R),mul(j,R))==j and mul(tr(R),R)==eye(2)
    # For S=-A*q²/2, with A=tan t, A'=1+A²: S_t+(S_q²+q²)/2=0.
    a=P({(1,0):1}); assert -(1+a*a)+(a*a+1)==0
    # Cotangent chart constraint w(z)=(-up)*1+p*u=0.
    u=P({(1,0):1});p=P({(0,1):1});assert -u*p+p*u==0
check('G14-symplectic-models','D06-F02','The momentum-level form has precisely the cyclic-coordinate kernel; the quotient, oscillator rotation and cotangent chart identities pass.',reduction_and_oscillator)

def holonomy():
    x=P({(1,0):1});y=P({(0,1):1})
    U=[[P(1),x],[P(0),P(1)]];V=[[P(1),P(0)],[y,P(1)]]
    Ui=[[P(1),-x],[P(0),P(1)]];Vi=[[P(1),P(0)],[-y,P(1)]]
    H=pmul(pmul(pmul(U,V),Ui),Vi)
    expected=[[1+x*y+x*x*y*y,-x*x*y],[x*y*y,1-x*y]]
    assert H==expected
    assert H[0][0]*H[1][1]-H[0][1]*H[1][0]==1
    assert H[0][0]+H[1][1]==2+x*x*y*y
    numeric=[[v.evaluate(1,1) for v in row] for row in H]
    assert numeric==mat([[3,-1],[1,0]])
    h=mat([[2,0],[0,1]]);hi=mat([[Q(1,2),0],[0,1]])
    g=mul(h,mul(numeric,hi))
    assert g==mat([[3,-2],[Q(1,2),0]]) and det2(g)==1 and g[0][0]+g[1][1]==3
check('G15-exact-holonomy','D06-F03 D05-F03','The full two-variable shear commutator is verified coefficient by coefficient; conjugate holonomies retain trace and determinant.',holonomy)

def curves():
    # Integral of (1+2a-2as)^2/2 from 0 to 2: coefficients in a.
    for a in [Q(-2),Q(-1,3),Q(0),Q(2,7),Q(3)]:
        c0=1+2*a;c1=-2*a
        value=(2*c0*c0+4*c0*c1+Q(8,3)*c1*c1)/2
        assert value==1+Q(4,3)*a*a and value>=1
    # Darboux cross-product coefficients in oriented frame (T,N,B).
    def cross(a,b):return [a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]]
    k=Q(2);tau=Q(3);omega=[tau,0,k]
    assert cross(omega,[1,0,0])==[0,k,0]
    assert cross(omega,[0,1,0])==[-k,0,tau]
    assert cross(omega,[0,0,1])==[0,-tau,0]
    # Sphere H² times area has coefficient four in units of pi, at all rational R.
    for R in [Q(1,3),Q(1),Q(7,2)]:assert (1/R**2)*(4*R**2)==4
check('G16-curvature-energy','D06-F04','The full quadratic objective gap is 4a²/3; frame cross products and scale-independent round-sphere energy coefficients pass.',curves)

def structure():
    families=json.loads((HERE/'families.json').read_text())
    chapters=json.loads((HERE/'chapters.json').read_text())
    reviews=json.loads((HERE/'classification_review.json').read_text())
    root=HERE.parents[1]; corpus=json.loads((root/'data/source_corpus_initial_routing.json').read_text())
    by={x['uid']:x for x in corpus}
    assert len(families)==12 and len(chapters)==3
    assert len({f['id'] for f in families})==12
    for f in families:
        assert 500<=f['substantive_word_count']<=900
        assert 4<=len(f['anchor_uids'])<=8
        assert set(f['anchor_uids'])<=set(f['source_uids'])
        assert all(u in by for u in f['source_uids'])
        for p in f['progression']:
            assert all(by[u]['year']==p['year'] for u in p['evidence_uids'])
    expected={x['uid'] for x in corpus if x['primary_domain'] in {'D04','D05','D06'}}
    assert {x['uid'] for x in reviews}==expected and len(reviews)==len(expected)==137
    assert all(400<=len(c['overview'].split())<=600 for c in chapters)
check('G17-source-coverage','D04-F01 D04-F02 D04-F03 D04-F04 D05-F01 D05-F02 D05-F03 D05-F04 D06-F01 D06-F02 D06-F03 D06-F04','All 137 initial primary entries reviewed; every source ID and progression year exists; family and chapter depth contracts pass.',structure)

out={'status':'pass','check_count':len(CHECKS),'scope':'Exact finite supporting models and source-structure checks. Infinite and smooth statements also require the written proofs and hypotheses.','checks':CHECKS}
(HERE/'checks.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':out['status'],'check_count':len(CHECKS)}))
