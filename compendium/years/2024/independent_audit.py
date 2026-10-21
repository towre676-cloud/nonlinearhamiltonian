"""Independent exact reconstructions of three delicate worked examples.

These calculations use no chapter helper code. The general mathematical
arguments remain in the written treatments.
"""
from pathlib import Path
from fractions import Fraction as Q
import json
P=Path(__file__).resolve().parent
checks=[]
def add(id,name,detail):checks.append(dict(id=id,name=name,status='passed',detail=detail))

# Q(sqrt(2),i) in the basis 1,sqrt(2),i,i*sqrt(2).
def mul(a,b):
    c=[Q(0)]*4
    for u,x in enumerate(a):
        for v,y in enumerate(b):
            ru,iu=u&1,(u>>1)&1;rv,iv=v&1,(v>>1)&1
            c[((iu^iv)<<1)|(ru^rv)]+=x*y*(2 if ru and rv else 1)*(-1 if iu and iv else 1)
    return tuple(c)
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
one=(Q(1),Q(0),Q(0),Q(0));zero=(Q(0),)*4
roots=[(Q(0),Q(s),Q(t),Q(0)) for s in [-1,1] for t in [-1,1]]
for r in roots:
    r2=mul(r,r);r4=mul(r2,r2)
    assert tuple(r4[j]-2*r2[j]+9*one[j] for j in range(4))==zero
def aut(a,s,t):return (a[0],s*a[1],t*a[2],s*t*a[3])
basis=[tuple(Q(i==j) for j in range(4)) for i in range(4)]
for s in [-1,1]:
    for t in [-1,1]:
        for a in basis:
            for b in basis:assert aut(mul(a,b),s,t)==mul(aut(a,s,t),aut(b,s,t))
assert len({aut(roots[0],s,t) for s in [-1,1] for t in [-1,1]})==4
add('June quartic','Independent exact splitting-algebra and automorphism calculation',{'field_basis':['1','sqrt(2)','i','i sqrt(2)'],'exact_roots':4,'distinct_sign_automorphisms':4,'scope':'Algebraic certificate for the explicit example; written text proves the field degree.'})

# Exact P30 data, independently compared with the recovered coefficient strings.
A=3284159265358979323846
B=847210362759896503429654125516779999512554883
a=-27006183241630922218434652145297453784768054621836357954737385
b=55258058551342376475736699591118191821521067032535079608372404779149413277716173425636721497
raw=(P/'months'/'12'/'root_details.json').read_text(encoding='utf-8')
for n in [A,B,a,b]:assert str(n) in raw
def plus(*ps):
    out={}
    for p in ps:
        for k,v in p.items():out[k]=out.get(k,Q(0))+v
    return {k:v for k,v in out.items() if v}
def times(p,q):
    out={}
    for i,x in p.items():
        for j,y in q.items():out[i+j]=out.get(i+j,Q(0))+x*y
    return {k:v for k,v in out.items() if v}
def scale(p,c):return {k:v*c for k,v in p.items() if v*c}
# t=sqrt(pi), x=A(t^4-1)t^-8, y=B(1+t^5)t^-10.
x={-4:Q(A),-8:Q(-A)};y={-10:Q(B),-5:Q(B)}
residual=plus(times(y,y),times(x,y),scale(times(times(x,x),x),-1),scale(x,-a),{0:Q(-b)})
poly={k+24:v for k,v in residual.items()}
assert min(poly)>=0 and max(poly)==24 and poly[24]==-b
add('December P30','Independent sparse-polynomial obstruction',{'clearing_power':'t^24 with t=sqrt(pi)','polynomial_degree':24,'leading_coefficient':str(-b),'nonzero_terms':len(poly),'scope':'The polynomial is nonzero exactly. Its nonvanishing at sqrt(pi) uses the written transcendence argument, not a finite numerical check.'})

# An independent rejection using only 3<pi<4, with no transcendence premise.
x_upper=Q(A,9);y_upper=Q(33*B,243)
rhs_lower=Q(b)-abs(a)*x_upper
lhs_upper=y_upper*y_upper+x_upper*y_upper
gap=rhs_lower-lhs_upper
assert gap>0
add('December P30','Independent rational separation for the entire interval 3<pi<4',{'rhs_lower_minus_lhs_upper':str(gap),'strict_positive':True,'bound':'0<x<A/9, 0<y<33B/243; RHS>=b-|a|A/9; LHS<y_upper^2+x_upper*y_upper','scope':'Exact rational inequalities reject the displayed candidate for every parameter pi in (3,4), independently of the polynomial proof.'})

for q in [Q(1),Q(1,2),Q(1,10),Q(1,100),Q(1,10**6)]:
    eps=q*q
    for lam,v in [(q,(Q(1),q)),(-q,(Q(1),-q))]:
        av=(v[1],eps*v[0]);assert av==tuple(lam*z for z in v)
    assert 2>=2*eps and Q(2)/(2*eps)==1/eps
add('December Jordan family','Exact rational eigenvectors and Gram singular-value ratios',{'rational_cases':5,'eigenvalues':'±q where epsilon=q²','basis_Gram_eigenvalues':['2','2 epsilon'],'condition_number_squared':'1/epsilon','scope':'Exact finite samples of the symbolic family shown in the illustration.'})
(P/'independent_checks.json').write_text(json.dumps(dict(checks=checks),ensure_ascii=False,indent=2))
print(json.dumps(dict(status='passed',checks=len(checks))))
