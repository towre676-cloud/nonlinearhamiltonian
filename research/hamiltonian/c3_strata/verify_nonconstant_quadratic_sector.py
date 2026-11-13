"""Independent symbolic regression for nonconstant quadratic-momentum static sector."""
import sympy as s
q,p=s.symbols('q p')
h=s.Function('h')(q);A=s.Function('A')(q);B=s.Function('B')(q)
f=s.Function('f')(q);g=s.Function('g')(q);k=s.Function('k')(q)
H=h+A*p+B*p*p
G=f+g*p+k*p*p
def T(n,X):
    return s.expand(sum((-1)**i*s.binomial(n,i)
        *s.diff(H,q,n-i,p,i)*s.diff(X,q,i,p,n-i)
        for i in range(n+1)))
assert s.simplify(T(3,G)-6*(s.diff(B,q)*s.diff(g,q,2)-s.diff(A,q,2)*s.diff(k,q))
    -12*p*(s.diff(B,q)*s.diff(k,q,2)-s.diff(B,q,2)*s.diff(k,q)))==0
assert T(5,G)==0
lam,mu,a,d=s.symbols('lam mu a d')
X=f+p*(lam*A+a*q+d)+p*p*(lam*B+mu)
assert T(3,X)==0 and T(5,X)==0
D=s.expand(s.diff(H,q)*s.diff(X,p)-s.diff(H,p)*s.diff(X,q))
assert s.simplify(D.coeff(p,3)-2*mu*s.diff(B,q))==0
print("PASS: exact quadratic static sector and first-refinement obstruction")
