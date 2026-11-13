"""Exact all-degree obstruction replay for affine quadratic momentum sextics."""
import sympy as s
q,p=s.symbols('q p')
a0,a1,b0,b1,u,v,a,d,l=s.symbols('a0 a1 b0 b1 u v a d l')
h=q**6+sum(s.Symbol('h'+str(i))*q**i for i in range(6))
A=a0+a1*q;B=b0+b1*q;H=h+A*p+B*p*p
D=lambda G:s.expand(s.diff(H,q)*s.diff(G,p)-s.diff(H,p)*s.diff(G,q))
T3=lambda G:s.expand(s.diff(h,q,3)*s.diff(G,p,3)+6*b1*s.diff(G,q,2,p))
T5=lambda G:s.expand(s.diff(h,q,5)*s.diff(G,p,5))
G=l*H+u+v*q+p*(a*q+d)
assert T3(G)==0 and T5(G)==0
assert T3(D(G))==0 and T5(D(G))==0
E=T3(D(D(G)))
assert s.Poly(E,q,p).coeff_monomial(q**4)==-15120*a*b1**2
assert s.Poly(E.subs(a,0),q,p).coeff_monomial(q**3)==-4320*d*b1**2
assert T3(D(D(l*H+u+v*q)))==0
Y=T3(D(D(D(l*H+u+v*q))))
assert s.Poly(Y,q,p).coeff_monomial(q**4)==30240*v*b1**3
assert T3(D(D(D(l*H+u))))==0
print('PASS affine quadratic all-degree S1=5 S2=3 S3=2 obstruction identities')
