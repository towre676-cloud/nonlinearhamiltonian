"""Independent exact certificates for the recovered December 22 oscillator.

Only Python's standard library is used.  Unit-disk counts use a polynomial
recursion proved by Rouche's theorem, not floating-point root finding.
For real P with leading a and constant b, P# is the reversed polynomial.
If |a|>|b|, (aP-bP#)/z has one fewer disk zero than P; if |b|>|a|,
bP-aP# has the same disk count and strictly lower degree.  A unit-circle zero
of P would survive in either reduced polynomial.  A nonzero terminal
constant therefore proves, inductively, that all boundary zeros are absent;
Rouche then supplies each disk-count step.  All comparisons here are strict.
"""
from pathlib import Path
from fractions import Fraction as F
from math import gcd, lcm
from functools import reduce
import json

ROOT=Path(__file__).resolve().parent

def primitive(coefficients):
    while len(coefficients)>1 and coefficients[-1]==0: coefficients.pop()
    g=reduce(gcd,coefficients)
    assert g
    return [v//g for v in coefficients]

def unit_disk_certificate(coefficients):
    p=primitive(list(coefficients)); steps=[]; count=0
    while len(p)>1:
        n=len(p)-1; a=p[-1]; b=p[0]
        assert a and abs(a)!=abs(b), 'Degenerate branch needs another method'
        if abs(a)>abs(b):
            q=[a*x-b*y for x,y in zip(p,p[::-1])]
            assert q[0]==0
            q=q[1:]; increment=1; branch='leading coefficient dominates'
        else:
            q=[b*x-a*y for x,y in zip(p,p[::-1])]
            assert q[-1]==0
            q=q[:-1]; increment=0; branch='constant coefficient dominates'
        q=primitive(q)
        assert len(q)<len(p)
        steps.append(dict(degree=n,polynomial=p,leading=a,constant=b,
                          branch=branch,disk_count_increment=increment,reduced=q))
        count+=increment;p=q
    assert p[0]
    return dict(inside=count,outside=len(coefficients)-1-count,boundary=0,
                terminal=p[0],steps=steps)

def determinant(m):
    m=[[F(x) for x in row] for row in m]; result=F(1); n=len(m)
    for k in range(n):
        pivot=next((j for j in range(k,n) if m[j][k]),None)
        if pivot is None:return F(0)
        if pivot!=k:m[k],m[pivot]=m[pivot],m[k];result=-result
        p=m[k][k];result*=p
        for i in range(k+1,n):
            factor=m[i][k]/p
            for j in range(k+1,n):m[i][j]-=factor*m[k][j]
    return result

def schur_inertia(a):
    """Independent rational congruence calculation; all pivots are nonzero."""
    n=len(a)-1
    A=[[F(a[n-(j-i)]) if j>=i else F(0) for j in range(n)] for i in range(n)]
    B=[[F(a[j-i]) if j>=i else F(0) for j in range(n)] for i in range(n)]
    H=[[sum(A[i][k]*A[j][k]-B[i][k]*B[j][k] for k in range(n))
        for j in range(n)] for i in range(n)]
    pivots=[]
    for k in range(n):
        p=H[k][k];assert p;pivots.append(p)
        for i in range(k+1,n):
            for j in range(i,n):
                H[j][i]=H[i][j]=H[i][j]-H[i][k]*H[k][j]/p
    return dict(positive=sum(p>0 for p in pivots),negative=sum(p<0 for p in pivots),
                zero=0,pivot_signs=''.join('+' if p>0 else '-' for p in pivots),
                pivots=[str(p) for p in pivots])

def poly_trim(a):
    while len(a)>1 and not a[-1]:a.pop()
    return a

def poly_add(a,b):
    return poly_trim([(a[i] if i<len(a) else F(0))+(b[i] if i<len(b) else F(0))
                      for i in range(max(len(a),len(b)))])

def poly_multiply(a,b):
    result=[F(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):result[i+j]+=x*y
    return poly_trim(result)

def poly_divmod(a,b):
    a=list(a);q=[F(0)]*max(1,len(a)-len(b)+1)
    while any(a) and len(a)>=len(b):
        degree=len(a)-len(b);c=a[-1]/b[-1];q[degree]=c
        for i,v in enumerate(b):a[i+degree]-=c*v
        poly_trim(a)
    return poly_trim(q),a

def bezout_bound(a):
    """UP+VP#=1 implies |P|>=1/(coefficient-one-norm(U)+norm(V))."""
    reverse=a[::-1]
    r0,r1=list(map(F,a)),list(map(F,reverse))
    u0,u1=[F(1)],[F(0)];v0,v1=[F(0)],[F(1)]
    while any(r1):
        quotient,remainder=poly_divmod(r0,r1);r0,r1=r1,remainder
        u0,u1=u1,poly_add(u0,[-x for x in poly_multiply(quotient,u1)])
        v0,v1=v1,poly_add(v0,[-x for x in poly_multiply(quotient,v1)])
    assert len(r0)==1 and r0[0]
    u=[x/r0[0] for x in u0];v=[x/r0[0] for x in v0]
    assert poly_add(poly_multiply(u,a),poly_multiply(v,reverse))==[F(1)]
    bound=1/(sum(abs(x) for x in u)+sum(abs(x) for x in v))
    return dict(U=[str(x) for x in u],V=[str(x) for x in v],
                lower_bound=str(bound)),bound

def main():
    # gamma=(sum a_k cos kt, sum b_k sin kt), from the recovered source.
    modes={1:(F(1),F(2)),2:(F(1,2),F(-1)),
           4:(F(1,2),F(1)),8:(F(3,8),F(-3,4))}
    z={}
    for k,(a,b) in modes.items():z[k]=(a+b)/2;z[-k]=(a-b)/2
    tangent={k:k*c for k,c in z.items()} # gamma'=i sum tangent_k u^k
    w={k:(1-k)*c for k,c in z.items()}  # z+i z'
    def polynomial(d):
        scale=lcm(*(c.denominator for c in d.values()))
        coeff=[int(d.get(j-8,F(0))*scale) for j in range(17)]
        return primitive(coeff)
    P=polynomial(tangent);Q=polynomial(w)
    assert P==[-9,0,0,0,2,0,-3,1,0,3,-1,0,6,0,0,0,-3]
    assert Q==[81,0,0,0,-20,0,36,-16,0,0,4,0,-36,0,0,0,21]
    cp=unit_disk_certificate(P);cq=unit_disk_certificate(Q)
    assert (cp['inside'],cq['inside'])==(6,2)
    assert (cp['inside']-8,cq['inside']-8)==(-2,-6)
    ip=schur_inertia(P);iq=schur_inertia(Q)
    assert (ip['positive'],ip['negative'])==(6,10)
    assert (iq['positive'],iq['negative'])==(2,14)
    bp,lp=bezout_bound(P);bq,lq=bezout_bound(Q)
    assert lp==F(6,35) and lq/F(16)>F(1,26)
    def moment(n):
        return sum(a*((-1)**(n//2))*k**n for k,(a,b) in modes.items()) if n%2==0 else F(0)
    h8=determinant([[moment(i+j) for j in range(8)] for i in range(8)])
    h9=determinant([[moment(i+j) for j in range(9)] for i in range(9)])
    assert h8 and h9==0
    annihilator=[4096,0,5440,0,1428,0,85,0,1]
    for n in range(20):assert sum(c*moment(n+j) for j,c in enumerate(annihilator))==0
    checks=[
      dict(id='DEC22-TANGENT',name='Exact source-curve regularity and tangent winding',status='passed',
           detail='Integer Rouche recursion gives6 disk zeros for P, no unit roots; tangent winding6-8=-2, and the convention2*wind gives Maslov-style integer-4.'),
      dict(id='DEC22-W',name='Exact winding of z+i z-prime',status='passed',
           detail='Integer Rouche recursion gives2 disk zeros for Q, no unit roots, hence winding2-8=-6.'),
      dict(id='DEC22-INERTIA',name='Independent rational Schur-Cohn matrix congruence',status='passed',
           detail='Pivot signs yield inertia(6,10) and(2,14), in agreement with the separate Rouche recursion.'),
      dict(id='DEC22-RANK',name='Exact derivative-Hankel rank and order-eight annihilator',status='passed',
           detail='The8x8 derivative-Hankel determinant is nonzero; the9x9 determinant vanishes. The order-eight constant-coefficient ODE supplies the upper bound, so minimal linear-realization dimension is8.'),
      dict(id='DEC22-ROBUST',name='Exact Bezout certificates for quantitative nonvanishing',status='passed',
           detail='UP+VP#=1 gives |P|>=6/35 on the unit circle, hence |gamma-prime|>=3/35. The independent Q certificate gives |w|>1/26. Uniform complex perturbations smaller than these margins preserve nonvanishing and winding.')]
    report=dict(checks=checks,curve={str(k):[str(a),str(b)] for k,(a,b) in modes.items()},
                tangent=dict(polynomial=P,certificate=cp,inertia=ip,bezout=bp),
                w=dict(polynomial=Q,certificate=cq,inertia=iq,bezout=bq),
                hankel8_determinant=str(h8),hankel9_determinant=str(h9),annihilator=annihilator,
                scope='Exact finite certificates for the recovered trigonometric curve. The Maslov-style integer uses the explicitly stated2*wind convention; no Catmull-Clark or motivic origin is inferred.')
    (ROOT/'independent_checks.json').write_text(json.dumps(report,indent=2))
    print(json.dumps(dict(status='passed',checks=len(checks),tangent_winding=-2,w_winding=-6,
                         minimal_realization_dimension=8,hankel8=str(h8))))

if __name__=='__main__':main()
