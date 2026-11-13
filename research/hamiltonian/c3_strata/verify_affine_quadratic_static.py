"""Exact symbolic replay of the affine-quadratic static classification."""
import sympy as s
q,p=s.symbols("q p")
b=s.symbols("b", nonzero=True)
u,v,w,x=s.symbols("u v w x")
h=q**6+3*q**4+q
A=2+5*q
B=7+b*q
H=h+A*p+B*p*p
def T(k,G):
    return s.expand(sum((-1)**i*s.binomial(k,i)*s.diff(H,q,k-i,p,i)*s.diff(G,q,i,p,k-i) for i in range(k+1)))
g3=u+v*q
g4=w+x*q
g1=s.integrate(s.integrate(-s.diff(h,q,3)*g3/b,q),q)+3+4*q
g2=s.integrate(s.integrate(-2*s.diff(h,q,3)*g4/b,q),q)+5+6*q
G=q**9+q**2+p*g1+p*p*g2+p**3*g3+p**4*g4
assert T(3,G)==0 and T(5,G)==0
f0,f1,f2,f3,f4=[s.Function('g'+str(i))(q) for i in range(5)]
X=f0+p*f1+p*p*f2+p**3*f3+p**4*f4
expected=24*b*s.diff(f4,q,2)*p**3+18*b*s.diff(f3,q,2)*p**2
expected+=p*(24*s.diff(h,q,3)*f4+12*b*s.diff(f2,q,2))
expected+=6*s.diff(h,q,3)*f3+6*b*s.diff(f1,q,2)
assert s.simplify(T(3,X)-expected)==0
assert T(5,X)==0
print("PASS: affine quadratic full static family and exact coefficient equations")
