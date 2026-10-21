"""Exact sparse Weyl--Moyal calculus in one canonical pair (stdlib only).

Polynomials map (q_degree,p_degree) to Fraction. Star coefficients map
(q_degree,p_degree,hbar_degree) to a Gaussian rational (real,imaginary).
The implementation expands the defining bidifferential exponential directly.
It does not use the closed monomial S_k formula employed by other verifiers.
"""
from fractions import Fraction as F
from math import factorial,gcd,lcm
from functools import reduce

def tidy(poly):return {tuple(k):F(v) for k,v in poly.items() if v}
def monomial(q,p,c=1):
    assert isinstance(q,int) and isinstance(p,int) and min(q,p)>=0
    return {} if not c else {(q,p):F(c)}
def add(*polys):
    out={}
    for poly in polys:
        for k,v in poly.items():out[k]=out.get(k,F(0))+v
    return tidy(out)
def scale(poly,c):return tidy({k:v*c for k,v in poly.items()})
def multiply(f,g):
    out={}
    for (a,b),x in f.items():
        for (c,d),y in g.items():
            key=(a+c,b+d);out[key]=out.get(key,F(0))+x*y
    return tidy(out)
def power(f,n):
    out=monomial(0,0)
    for _ in range(n):out=multiply(out,f)
    return out

def derivative(poly,q=0,p=0):
    out=tidy(poly)
    for axis,count in [(0,q),(1,p)]:
        for _ in range(count):
            nxt={}
            for k,v in out.items():
                if k[axis]:
                    degree=list(k);degree[axis]-=1;nxt[tuple(degree)]=v*k[axis]
            out=nxt
    return out

def poisson(f,g):return add(multiply(derivative(f,q=1),derivative(g,p=1)),scale(multiply(derivative(f,p=1),derivative(g,q=1)),-1))

def star(f,g):
    """Defining exponential, expanded in q/p derivatives with exact Gaussian coefficients."""
    if not f or not g:return {}
    rmax=min(max(a for a,b in f),max(b for a,b in g))
    smax=min(max(b for a,b in f),max(a for a,b in g))
    out={}
    for r in range(rmax+1):
        for s in range(smax+1):
            fg=multiply(derivative(f,q=r,p=s),derivative(g,q=s,p=r))
            if not fg:continue
            k=r+s;factor=F((-1)**s,2**k*factorial(r)*factorial(s));real,imag=[(1,0),(0,1),(-1,0),(0,-1)][k%4]
            for (a,b),v in fg.items():
                key=(a,b,k);old=out.get(key,(F(0),F(0)));out[key]=(old[0]+factor*v*real,old[1]+factor*v*imag)
    return {k:v for k,v in out.items() if v!=(0,0)}

def moyal(f,g):
    """Normalized commutator divided by i*hbar; returns {hbar degree: polynomial}."""
    fg=star(f,g);gf=star(g,f);out={}
    for key in fg.keys()|gf.keys():
        a,b,k=key;x=fg.get(key,(F(0),F(0)));y=gf.get(key,(F(0),F(0)));real,imag=x[0]-y[0],x[1]-y[1]
        assert real==0,('Commutator unexpectedly has real coefficient',key,real)
        if not imag:continue
        assert k>=1 and k%2==1
        poly=out.setdefault(k-1,{});poly[(a,b)]=poly.get((a,b),F(0))+imag
    out={k:tidy(v) for k,v in out.items() if tidy(v)}
    assert out.get(0,{})==poisson(f,g)
    return out

def defects(f,g):return {k:v for k,v in moyal(f,g).items() if k>0}
def exact_partner(f,g):return not defects(f,g)

def formal_add(*series):
    out={}
    for series in series:
        for k,p in series.items():out[k]=add(out.get(k,{}),p)
    return {k:p for k,p in out.items() if p}
def formal_action(H,series):
    out={}
    for j,p in series.items():
        for k,q in moyal(H,p).items():out[j+k]=add(out.get(j+k,{}),q)
    return {k:p for k,p in out.items() if p}

def nullspace(matrix,ncols):
    A=[[F(x) for x in r] for r in matrix];pivots=[];i=0
    for j in range(ncols):
        pivot=next((k for k in range(i,len(A)) if A[k][j]),None)
        if pivot is None:continue
        A[i],A[pivot]=A[pivot],A[i];v=A[i][j];A[i]=[x/v for x in A[i]]
        for k in range(len(A)):
            if k!=i and A[k][j]:
                v=A[k][j];A[k]=[x-v*y for x,y in zip(A[k],A[i])]
        pivots.append(j);i+=1
        if i==len(A):break
    vectors=[]
    for free in [j for j in range(ncols) if j not in pivots]:
        v=[F(0)]*ncols;v[free]=F(1)
        for i,j in enumerate(pivots):v[j]=-A[i][free]
        vectors.append(v)
    return vectors

def homogeneous_kernel(H,n):
    """All homogeneous degree-n hbar-independent partners, by exact rational nullspace."""
    exponents=[(a,n-a) for a in range(n+1)]
    images=[defects(H,monomial(*e)) for e in exponents]
    keys=sorted({(k,a,b) for image in images for k,p in image.items() for a,b in p})
    matrix=[[image.get(k,{}).get((a,b),F(0)) for image in images] for k,a,b in keys]
    vectors=nullspace(matrix,n+1)
    polys=[tidy(dict(zip(exponents,v))) for v in vectors]
    assert all(exact_partner(H,G) for G in polys)
    return polys

def primitive(poly):
    if not poly:return {}
    den=reduce(lcm,(v.denominator for v in poly.values()),1);ints={k:int(v*den) for k,v in poly.items()};g=reduce(gcd,(abs(v) for v in ints.values()));sign=1 if ints[sorted(ints)[0]]>0 else -1
    return {k:F(v*sign,g) for k,v in ints.items()}

def serialize(poly):return [{'q':a,'p':b,'coefficient':str(v)} for (a,b),v in sorted(poly.items())]
def serialize_series(series):return [{'hbar':k,'terms':serialize(p)} for k,p in sorted(series.items())]

def kernel_for_basis(H,exponents):
    """Exact partner kernel in an arbitrary finite monomial span."""
    exponents=list(exponents);images=[defects(H,monomial(*e)) for e in exponents]
    keys=sorted({(k,a,b) for image in images for k,p in image.items() for a,b in p})
    matrix=[[image.get(k,{}).get((a,b),F(0)) for image in images] for k,a,b in keys]
    polys=[tidy(dict(zip(exponents,v))) for v in nullspace(matrix,len(exponents))]
    assert all(exact_partner(H,G) for G in polys)
    return polys
