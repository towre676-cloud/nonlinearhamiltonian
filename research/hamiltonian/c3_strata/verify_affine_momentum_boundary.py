"""Regression checks for the affine-momentum infinite-core theorem."""
import sympy as s

q,p=s.symbols("q p")
a,b=s.symbols("a b")
h=q**6+2*q**3+q
H=h+(a+b*q)*p

def trans(k,F,G):
    return s.expand(sum((-1)**i*s.binomial(k,i)
        *s.diff(F,q,k-i,p,i)*s.diff(G,q,i,p,k-i)
        for i in range(k+1)))

for G in (q**7+p*q**4+p**2*(q**3+q),p**2*q**9+q**2):
    assert s.expand(trans(3,H,G)-s.diff(h,q,3)*s.diff(G,p,3))==0
    assert trans(3,H,G)==0
    assert trans(5,H,G)==0
    DG=trans(1,H,G)
    assert trans(3,H,DG)==0 and trans(5,H,DG)==0
    DDG=trans(1,H,DG)
    assert trans(3,H,DDG)==0 and trans(5,H,DDG)==0
print("PASS: symbolic affine-momentum regression")
