"""Exact symbolic proof-obligation replay for H=q^6+qp^2."""
import sympy as s
q,p=s.symbols("q p")
a,b,c,d,e,t,g,h,u,v=s.symbols("a b c d e t g h u v")
F=s.Function("F")(q)
H=q**6+q*p**2
D=lambda x:s.expand(s.diff(H,q)*s.diff(x,p)-s.diff(H,p)*s.diff(x,q))
T3=lambda x:s.expand(120*q**3*s.diff(x,p,3)+6*s.diff(x,q,2,p))
T5=lambda x:s.expand(720*q*s.diff(x,p,5))
G=F+(e+t*q-6*a*q**5-4*b*q**6)*p+(g+h*q-12*c*q**5-8*d*q**6)*p**2+(a+b*q)*p**3+(c+d*q)*p**4
assert T3(G)==0 and T5(G)==0
X=D(G)
assert s.expand(X).coeff(p,5)==4*c+2*d*q
assert s.expand(s.expand(T3(X)).coeff(p,1)-720*q**3*(36*a+35*b*q))==0
assert s.expand(s.expand(T3(X)).coeff(p,2)-1440*q**3*(50*c+49*d*q))==0
G1=u+v*q+s.Rational(12,5)*g*q**5+h*q**6+(e+t*q)*p+(g+h*q)*p**2
assert T3(G1)==0 and T5(G1)==0 and T3(D(G1))==0 and T5(D(G1))==0
assert s.factor(T3(D(D(G1))))==2160*q**3*(-2*e-7*t*q+24*g*p)
G2=u+v*q+h*H
assert T3(D(D(G2)))==0 and T5(D(D(G2)))==0
assert s.factor(T3(D(D(D(G2)))))==30240*q**4*v
print("PASS: exact all-degree qp2 coefficient identities")
