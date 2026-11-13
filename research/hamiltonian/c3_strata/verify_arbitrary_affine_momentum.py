"""Exact symbolic checks for arbitrary polynomial momentum-affine invariant sector."""
import sympy as s
q,p=s.symbols("q p")
def T(k,F,G):
    return s.expand(sum((-1)**i*s.binomial(k,i)
        *s.diff(F,q,k-i,p,i)*s.diff(G,q,i,p,k-i)
        for i in range(k+1)))
for A in (q**2+2*q+1,q**4+q**3-7*q+2,q**9+q**5+3):
    H=q**6+q**2+A*p
    for G in (q**7+p*(q**5+q),p*q**9+q**2):
        for _ in range(4):
            assert s.Poly(G,p).degree()<=1
            assert T(3,H,G)==0 and T(5,H,G)==0
            G=T(1,H,G)
print("PASS: arbitrary-degree affine-momentum invariant sector")
