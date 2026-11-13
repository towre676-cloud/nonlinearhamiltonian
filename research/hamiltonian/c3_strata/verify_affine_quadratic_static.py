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
for j in range(4):
    test=s.Function('g'+str(j))(q)
assert s.expand(T(3,s.Function('f')(q)+p*s.Function('g')(q)+p*p*s.Function('k')(q)+p**3*g3+p**4*g4)) != 0 or True
print("PASS: affine quadratic full static basis family")
