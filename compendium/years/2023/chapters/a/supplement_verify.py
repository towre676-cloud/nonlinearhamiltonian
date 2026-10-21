"""Exact rational/Gaussian-rational replay of S007 triangular Koopman closure."""
from pathlib import Path
from fractions import Fraction as F
from dataclasses import dataclass
import json

@dataclass(frozen=True)
class QI:
    re:F=F(0)
    im:F=F(0)
    def __post_init__(self):
        object.__setattr__(self,'re',F(self.re));object.__setattr__(self,'im',F(self.im))
    @staticmethod
    def coerce(x):return x if isinstance(x,QI) else QI(x)
    def __add__(self,x):
        x=self.coerce(x);return QI(self.re+x.re,self.im+x.im)
    __radd__=__add__
    def __neg__(self):return QI(-self.re,-self.im)
    def __sub__(self,x):return self+-self.coerce(x)
    def __rsub__(self,x):return self.coerce(x)+-self
    def __mul__(self,x):
        x=self.coerce(x);return QI(self.re*x.re-self.im*x.im,self.re*x.im+self.im*x.re)
    __rmul__=__mul__
    def __truediv__(self,x):
        x=self.coerce(x);n=x.re*x.re+x.im*x.im
        if not n:raise ZeroDivisionError
        return QI((self.re*x.re+self.im*x.im)/n,(self.im*x.re-self.re*x.im)/n)
    def __pow__(self,n):
        assert isinstance(n,int) and n>=0
        result=QI(1);base=self
        while n:
            if n&1:result=result*base
            n//=2;base=base*base
        return result
    def __bool__(self):return bool(self.re or self.im)
    def __str__(self):
        if not self.im:return str(self.re)
        return f'({self.re}+({self.im})i)'

Z=QI();ONE=QI(1)
def clean(p):return {k:v for k,v in p.items() if v}
def add(p,q):
    r=p.copy()
    for k,v in q.items():r[k]=r.get(k,Z)+v
    return clean(r)
def scale(p,s):return clean({k:v*s for k,v in p.items()})
def mul(p,q):
    r={}
    for (i,j),v in p.items():
        for (k,l),w in q.items():r[(i+k,j+l)]=r.get((i+k,j+l),Z)+v*w
    return clean(r)
def power(p,n):
    r={(0,0):ONE}
    for _ in range(n):r=mul(r,p)
    return r
def compose(p,tx,ty):
    r={}
    for (i,j),c in p.items():r=add(r,scale(mul(power(tx,i),power(ty,j)),c))
    return r
I={(0,0):ONE};X={(1,0):ONE};Y={(0,1):ONE}
def rank(polynomials):
    mons=sorted(set().union(*(p.keys() for p in polynomials)))
    a=[[p.get(k,Z) for k in mons] for p in polynomials];i=0
    for j in range(len(mons)):
        pivot=next((k for k in range(i,len(a)) if a[k][j]),None)
        if pivot is None:continue
        a[i],a[pivot]=a[pivot],a[i];d=a[i][j];a[i]=[v/d for v in a[i]]
        for k in range(len(a)):
            if k!=i:
                c=a[k][j];a[k]=[u-c*v for u,v in zip(a[k],a[i])]
        i+=1
        if i==len(a):break
    return i
def op_polynomial(coeffs,p,U):
    result={};term=p
    for c in coeffs:result=add(result,scale(term,c));term=U(term)
    return result
def factor_polynomial(roots):
    c=[ONE]
    for root in roots:
        d=[Z]*(len(c)+1)
        for j,v in enumerate(c):d[j]=d[j]-root*v;d[j+1]=d[j+1]+v
        c=d
    return c
def convolution(b,mu,n):return sum((b**(n-1-j))*(mu**j) for j in range(n))

cases=[
 ('distinct nonresonant',QI(2),QI(3),{0:1,1:2,2:1,3:1},5,False),
 ('quadratic resonance',QI(2),QI(4),{2:1,3:1},5,True),
 ('real parity collision',QI(-1),QI(1),{2:1,3:2,4:3},5,True),
 ('a one nonresonant',QI(1),QI(2),{2:1,5:1},4,False),
 ('a one resonant',QI(1),QI(1),{2:1,5:1},4,True),
 ('a zero nilpotent resonance',QI(0),QI(0),{0:3,1:2,2:1,5:2},4,True),
 ('a zero constant resonance',QI(0),QI(1),{0:3,1:2,2:1,5:2},4,True),
 ('a zero nonresonant',QI(0),QI(2),{2:1,5:1},4,False),
 ('fourth-root collision resonant',QI(0,1),QI(-1),{2:1,6:1,3:2,7:3,4:1,8:1},6,True),
 ('fourth-root collision nonresonant',QI(0,1),QI(2),{2:1,6:1,3:2,7:3,4:1,8:1},6,False),
 ('affine resonance',QI(2),QI(2),{0:3,1:1},3,True),
 ('zero polynomial repeated diagonal eigenvalue',QI(2),QI(2),{},3,False),
]
records=[]
for label,a,b,pc,expected_dimension,expected_resonance in cases:
    p={(k,0):QI(c) for k,c in pc.items() if c}
    tx=scale(X,a);ty=add(scale(Y,b),p)
    U=lambda f:compose(f,tx,ty)
    groups={}
    for k,c in pc.items():
        if k>=2 and c:
            mu=a**k;groups[mu]=add(groups.get(mu,{}),{(k,0):QI(c)})
    basis=[I,X,Y]+list(groups.values())
    assert len(basis)==rank(basis)==expected_dimension
    assert all(rank(basis+[U(v)])==len(basis) for v in basis)
    generated=[I,X,Y];term=Y
    for _ in range(expected_dimension+2):term=U(term);generated.append(term)
    assert rank(generated)==len(basis)
    p_groups={}
    for k,c in pc.items():
        if c:
            mu=a**k;p_groups[mu]=add(p_groups.get(mu,{}),{(k,0):QI(c)})
    pb=p_groups.get(b,{})
    assert bool(pb)==expected_resonance
    tilted=Y.copy()
    for mu,v in p_groups.items():
        if mu!=b:tilted=add(tilted,scale(v,ONE/(b-mu)))
    assert add(U(tilted),scale(tilted,-b))==pb
    assert not add(U(pb),scale(pb,-b))
    eigenvalues=set([QI(1),a,b]+list(groups))
    roots=list(eigenvalues)+([b] if pb else [])
    minpoly=factor_polynomial(roots)
    assert all(not op_polynomial(minpoly,v,U) for v in basis)
    # Removing any one root factor destroys the annihilator on at least one basis vector.
    for j in range(len(roots)):
        shorter=factor_polynomial(roots[:j]+roots[j+1:])
        assert any(op_polynomial(shorter,v,U) for v in basis)
    term=Y
    for n in range(8):
        closed=scale(Y,b**n)
        for mu,v in p_groups.items():closed=add(closed,scale(v,convolution(b,mu,n)))
        assert term==closed
        term=U(term)
    records.append(dict(label=label,a=str(a),b=str(b),dimension=len(basis),nonlinear_groups=[str(v) for v in groups],resonance=bool(pb),minimal_polynomial_degree=len(minpoly)-1))

# A coupled invertible map has degree growth, so no finite polynomial closure containing y.
tx=Y;ty=add(mul(Y,Y),scale(X,QI(-1)))
term=Y;degrees=[]
for n in range(6):
    degrees.append(max(i+j for i,j in term));term=compose(term,tx,ty)
assert degrees==[1,2,4,8,16,32]
inverse_x=add(mul(X,X),scale(Y,QI(-1)))
inverse_y=X
assert compose(tx,inverse_x,inverse_y)==X and compose(ty,inverse_x,inverse_y)==Y
assert compose(inverse_x,tx,ty)==X and compose(inverse_y,tx,ty)==Y

checks=[
 dict(id='S007',name='Minimal invariant triangular feature spaces',status='passed',detail={'exact_cases':records,'method':'Exact Gaussian-rational polynomial composition, rank, closure and independent iterated-observable span.'}),
 dict(id='S007',name='Resonance Jordan chains and minimal polynomials',status='passed',detail='In every case the shifted y coordinate has the stated length-one or length-two chain. The asserted polynomial annihilates every basis vector, and deleting any one root factor fails.'),
 dict(id='S007',name='Closed iterate formula including zero resonance',status='passed',detail='Direct composition equals the convolution-sum formula for n=0,...,7 in all twelve cases; no division at resonance or 0^0 convention is needed.'),
 dict(id='S007',name='Invertible coupled degree-growth counterexample',status='passed',detail={'map':'(x,y)→(y,y²−x)','inverse':'(x,y)→(x²−y,x)','degrees_of_iterated_y':degrees,'scope':'Exact finite examples accompany the general degree-growth proof.'}),
]
Path(__file__).resolve().with_name('supplement_checks.json').write_text(json.dumps({'checks':checks,'status':'passed','count':len(checks)},ensure_ascii=False,indent=2))
print(json.dumps({'cases':len(cases),'checks':len(checks),'status':'passed','coupled_degrees':degrees}))
