"""Exact symbolic regression for the complete S0-S5 quadratic-momentum theorem."""
import sympy as s
q,p,c=s.symbols("q p c", nonzero=True)
a,b,k,u,v,w=s.symbols("a b k u v w")
h=s.Function("h")(q)
D=lambda x:s.expand(s.diff(h,q)*s.diff(x,p)-2*c*p*s.diff(x,q))
f=s.Function('f')(q);g=s.Function('g')(q);kk=s.Function('k')(q)
X=f+p*g+p*p*kk
assert s.expand(D(X)).coeff(p,3)==-2*c*s.diff(kk,q)
X2=f+p*g+p*p*k
assert s.expand(D(D(X2))).coeff(p,3)==4*c*c*s.diff(g,q,2)
X3=f+p*(a+b*q)+p*p*k
assert s.simplify(s.expand(D(D(D(X3)))).coeff(p,3)
    -(8*c*c*k*s.diff(h,q,3)-8*c**3*s.diff(f,q,3)))==0
G=k*h/c+u+v*q+w*q*q+p*(a+b*q)+k*p*p
for i in range(4):
    assert s.expand(G).coeff(p,3)==0
    G=D(G)
assert s.simplify(s.expand(G).coeff(p,3)
    +8*c**3*((a+b*q)*s.diff(h,q,4)+5*b*s.diff(h,q,3)))==0
G=k*h/c+u+v*q+w*q*q+k*p*p
for i in range(5):
    assert s.expand(G).coeff(p,3)==0
    G=D(G)
assert s.simplify(s.expand(G).coeff(p,3)
    -16*c**4*((v+2*w*q)*s.diff(h,q,4)+10*w*s.diff(h,q,3)))==0
H=h+c*p*p
assert D(H)==0 and D(s.Integer(1))==0
print("PASS: exact S0-S5 symbolic identities and persistent core")
