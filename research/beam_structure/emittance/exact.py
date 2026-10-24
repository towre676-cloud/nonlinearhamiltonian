"""Exact finite-measure residual-force identities; no floating-point guarantees.

Coordinates are centered internally; weights describe the same measure before
and after the fixed-position kick. Physical model/discretization premises are
external to this algebraic checker.
"""
from fractions import Fraction
from itertools import combinations
from math import isqrt


def rational(value):
    if isinstance(value, float):
        raise TypeError('Use integers, Fraction, or decimal strings for exact input')
    return Fraction(value)


def normalized_weights(n, weights=None):
    if n == 0:
        raise ValueError('empty measure')
    out = [Fraction(1, n)] * n if weights is None else list(map(rational, weights))
    if len(out) != n or any(v < 0 for v in out) or sum(out) != 1:
        raise ValueError('weights must be nonnegative and sum to one')
    return out


def center(values, weights):
    mean = sum(w * rational(v) for w, v in zip(weights, values))
    return [rational(v) - mean for v in values], mean


def inner(left, right, weights):
    return sum(w*x*y for w, x, y in zip(weights, left, right))


def determinant(matrix):
    a = [[rational(x) for x in row] for row in matrix]
    n = len(a)
    if any(len(row) != n for row in a):
        raise ValueError('square matrix required')
    result = Fraction(1)
    for j in range(n):
        pivot = next((k for k in range(j,n) if a[k][j]), None)
        if pivot is None:
            return Fraction(0)
        if pivot != j:
            a[j], a[pivot] = a[pivot], a[j]
            result = -result
        value = a[j][j]
        result *= value
        for k in range(j+1,n):
            scale = a[k][j] / value
            for ell in range(j+1,n):
                a[k][ell] -= scale*a[j][ell]
    return result


def is_psd(matrix):
    n=len(matrix)
    if any(len(row)!=n for row in matrix):
        return False
    if any(matrix[i][j] != matrix[j][i] for i in range(n) for j in range(n)):
        return False
    # All principal minors, not just the leading minors, are needed for PSD.
    return all(determinant([[matrix[i][j] for j in ids] for i in ids]) >= 0
               for size in range(1,n+1) for ids in combinations(range(n),size))


def sqrt_difference_leq(left_squared, right_squared, radius_squared):
    """Decide |sqrt(left)-sqrt(right)|<=sqrt(radius) using only rationals."""
    a,b,c=map(rational,(left_squared,right_squared,radius_squared))
    if min(a,b,c)<0:
        raise ValueError('nonnegative squared quantities required')
    t=a+b-c
    return t<=0 or t*t<=4*a*b


def sqrt_upper(value, bits=80):
    """Rational upper enclosure; exact comparison is performed after rounding."""
    value=rational(value)
    if value<0 or bits<1:
        raise ValueError('nonnegative radicand and positive precision required')
    scale=1<<bits
    lower=isqrt((value.numerator*scale*scale)//value.denominator)
    if Fraction(lower,scale)**2==value:
        return Fraction(lower,scale)
    return Fraction(lower+1,scale)


def scalar_kick(x,p,force,h,weights=None):
    n=len(x)
    if len(p)!=n or len(force)!=n:
        raise ValueError('paired clouds must have equal lengths')
    w=normalized_weights(n,weights)
    xc,mx=center(x,w);pc,mp=center(p,w);fc,mf=center(force,w)
    h=rational(h)
    a=inner(xc,xc,w);b=inner(xc,pc,w);c=inner(pc,pc,w)
    if a<=0:
        raise ValueError('positive position variance required for this chart')
    m=inner(xc,fc,w);nn=inner(pc,fc,w);ell=inner(fc,fc,w)
    u=[v-b/a*t for t,v in zip(xc,pc)]
    g=[v-m/a*t for t,v in zip(xc,fc)]
    U=inner(u,u,w);G=inner(g,g,w);C=inner(u,g,w)
    eps2=a*c-b*b
    pp=[v+h*f for v,f in zip(pc,fc)]
    epsnew2=a*inner(pp,pp,w)-inner(xc,pp,w)**2
    predicted=eps2+2*h*a*C+h*h*a*G
    if epsnew2 != predicted or eps2 != a*U:
        raise ArithmeticError('exact emittance identity failed')
    if C*C>U*G or not sqrt_difference_leq(eps2,epsnew2,h*h*a*G):
        raise ArithmeticError('exact Cauchy/norm bound failed')
    return {'a':a,'b':b,'p_variance':c,'qF':m,'pF':nn,'FF':ell,
            'u_variance':U,'g_variance':G,'ug':C,'eps2':eps2,
            'epsnew2':epsnew2,'identity_rhs':predicted,
            'radius_squared':h*h*a*G,'centroids':(mx,mp,mf),
            'orthogonality_residuals':(inner(xc,u,w),inner(xc,g,w)),
            'gram_psd':is_psd([[U,C],[C,G]])}


def conditional_emittance_interval(eps2,a,h,g_upper,bits=80):
    """Outward rational interval, conditional on a true upper bound for E[g²].

    Supplying g_upper does not prove it covers an unknown physical beam. This
    function validates arithmetic and returns the resulting conditional interval.
    """
    eps2,a,h,g_upper=map(rational,(eps2,a,h,g_upper))
    if eps2<0 or a<=0 or g_upper<0:
        raise ValueError('invalid conditional premises')
    eps_hi=sqrt_upper(eps2,bits)
    step=Fraction(1,1<<bits)
    eps_lo=eps_hi if eps_hi*eps_hi==eps2 else max(Fraction(0),eps_hi-step)
    radius=sqrt_upper(h*h*a*g_upper,bits)
    return {'lower':max(Fraction(0),eps_lo-radius),'upper':eps_hi+radius,
            'radius_upper':radius,'required_g_upper':g_upper,
            'scope':'conditional algebra only; force-bound premise not established'}


def transpose(a):
    return [list(row) for row in zip(*a)]


def multiply(a,b):
    return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]


def subtract(a,b):
    return [[x-y for x,y in zip(row,col)] for row,col in zip(a,b)]


def inverse2(a):
    det=determinant(a)
    if det<=0 or a[0][0]<=0:
        raise ValueError('positive definite position covariance required')
    return [[a[1][1]/det,-a[0][1]/det],[-a[1][0]/det,a[0][0]/det]]


def vector_kick(q,p,force,h,weights=None):
    n=len(q)
    if len(p)!=n or len(force)!=n or any(len(row)!=2 for arr in (q,p,force) for row in arr):
        raise ValueError('paired N by 2 clouds required')
    w=normalized_weights(n,weights);h=rational(h)
    qc=[center(v,w)[0] for v in zip(*q)]
    pc=[center(v,w)[0] for v in zip(*p)]
    fc=[center(v,w)[0] for v in zip(*force)]
    def cov(a,b):
        return [[inner(x,y,w) for y in b] for x in a]
    A=cov(qc,qc);S=cov(qc,pc);P=cov(pc,pc)
    M=cov(qc,fc);N=cov(pc,fc);L=cov(fc,fc)
    inv=inverse2(A)
    U=subtract(P,multiply(multiply(transpose(S),inv),S))
    G=subtract(L,multiply(multiply(transpose(M),inv),M))
    C=subtract(N,multiply(multiply(transpose(S),inv),M))
    newpc=[[v+h*f for v,f in zip(row,frow)] for row,frow in zip(pc,fc)]
    Snew=cov(qc,newpc);Pnew=cov(newpc,newpc)
    Unew=subtract(Pnew,multiply(multiply(transpose(Snew),inv),Snew))
    rhs=[[U[i][j]+h*(C[i][j]+C[j][i])+h*h*G[i][j] for j in range(2)] for i in range(2)]
    gram=[U[i]+C[i] for i in range(2)]+[transpose(C)[i]+G[i] for i in range(2)]
    sigma=[A[i]+S[i] for i in range(2)]+[transpose(S)[i]+P[i] for i in range(2)]
    if Unew!=rhs or not is_psd(gram) or determinant(sigma)!=determinant(A)*determinant(U):
        raise ArithmeticError('exact Schur update/PSD/determinant identity failed')
    return {'A':A,'S':S,'P':P,'M':M,'N':N,'L':L,'U':U,'G':G,'C':C,
            'Unew':Unew,'identity_rhs':rhs,'joint_gram_psd':True,
            'det_covariance':determinant(sigma),'det_schur_product':determinant(A)*determinant(U)}
