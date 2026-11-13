"""Exact independent weighted kernel and refinement replay for the two binomial strata.

Run: python verify_binomial_newton.py
Requires SymPy. The finite tail cutoffs are supplied by the separate human proof.
"""
from math import comb
from sympy import Matrix, Rational, symbols, expand

def fall(n, k):
    out = 1
    for i in range(k):
        out *= n - i
    return out if n >= k else 0

def diff(f, a, b):
    return {(i-a,j-b): c*fall(i,a)*fall(j,b)
            for (i,j),c in f.items() if i >= a and j >= b}

def mul(f, g):
    out = {}
    for (i,j),c in f.items():
        for (a,b),d in g.items():
            out[(i+a,j+b)] = out.get((i+a,j+b),0) + c*d
    return out

def trans(h, g, k):
    out = {}
    for t in range(k+1):
        left, right = diff(h,k-t,t),diff(g,t,k-t)
        for mon,c in mul(left,right).items():
            out[mon] = out.get(mon,0) + (-1)**t*comb(k,t)*c
    return {m:c for m,c in out.items() if c}

def basis(u,v,W):
    d = 6-u
    return [(a,(W-v*a)//d) for a in range(W//v+1)
            if (W-v*a)%d == 0]

def kernels(h,u,v,W):
    mons=basis(u,v,W)
    if not mons:
        return []
    cols=[]
    for mon in mons:
        g={mon:Rational(1)}
        vals={}
        for k in (3,5):
            vals.update({(k,)+m:c for m,c in trans(h,g,k).items()})
        cols.append(vals)
    rows=sorted(set().union(*(set(x) for x in cols)))
    mat=Matrix(len(rows),len(mons),lambda i,j:cols[j].get(rows[i],0))
    return [{m:vec[i] for i,m in enumerate(mons) if vec[i]}
            for vec in mat.nullspace()]

def run(u,v,cutoff,weights):
    h={(6,0):Rational(1),(u,v):Rational(1)}
    occupied=[]
    refined=[]
    twice=[]
    for W in range(cutoff+1):
        for g in kernels(h,u,v,W):
            occupied.append(W)
            dh=trans(h,g,1)
            if any(trans(h,dh,k) for k in (3,5)):
                continue
            refined.append(W)
            ddh=trans(h,dh,1)
            if not any(trans(h,ddh,k) for k in (3,5)):
                twice.append(W)
    assert occupied==weights,(u,v,occupied)
    assert refined==[0,6*v],(u,v,refined)
    assert twice==[0,6*v],(u,v,twice)
    print('PASS', (u,v),'static',len(occupied),'first',len(refined),
          'second',len(twice),'weights',occupied)

a,j=symbols('a j')
p4=5*a*a+6*a*j-19*a-9*j*j-21*j+18
p3=7*a*a+18*a*j-21*a-9*j+14-9*j*j
assert expand(p4-p4.subs({a:a-5,j:j+4},simultaneous=True))==2*(13*a+51*j+64)
assert expand(p3-p3.subs({a:a-4,j:j+3},simultaneous=True))==2*(a+63*j+64)
run(1,4,87,[0,4,5,8,9,10,14,20,24,44])
run(2,3,53,[0,3,4,6,7,8,12,16,18,28])
