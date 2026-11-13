"""Exact symbolic regression for the first three quadratic-momentum refinements."""
import sympy as s
q,p,c=s.symbols("q p c", nonzero=True)
a,b,k,u,v,w=s.symbols("a b k u v w")
h=q**6+2*q**3+q
D=lambda x:s.expand(s.diff(h,q)*s.diff(x,p)-2*c*p*s.diff(x,q))
G=k*h/c+u+v*q+w*q*q+p*(a+b*q)+k*p*p
for i in range(4):
    assert s.Poly(G,p).degree()<=2
    G=D(G)
f=s.Function('f')(q);g=s.Function('g')(q);kk=s.Function('k')(q)
X=f+p*g+p*p*kk
assert s.expand(D(X)).coeff(p,3)==-2*c*s.diff(kk,q)
X2=f+p*g+p*p*k
assert s.expand(D(D(X2))).coeff(p,3)==4*c*c*s.diff(g,q,2)
X3=f+p*(a+b*q)+p*p*k
assert s.simplify(s.expand(D(D(D(X3)))).coeff(p,3)
    -(8*c*c*k*s.diff(h,q,3)-8*c**3*s.diff(f,q,3)))==0
print("PASS: S0-S3 exact symbolic coefficient identities")
