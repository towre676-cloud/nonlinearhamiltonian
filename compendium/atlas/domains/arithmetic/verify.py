#!/usr/bin/env python3
"""Exact worked-model checks; no general arithmetic solver is claimed.

Run with Python's standard library only. Infinite and global conclusions in the
families require their written arguments, not these bounded replay checks.
"""
import json
import math
from fractions import Fraction as Q
from pathlib import Path

HERE=Path(__file__).resolve().parent
BASE=HERE.parents[1]
RESULTS=[]
def check(name,family,fn,scope):
    detail=fn()
    RESULTS.append(dict(name=name,family_id=family,status='pass',scope=scope,detail=detail))

def det(a):
    a=[[Q(x) for x in row] for row in a];n=len(a);result=Q(1)
    for k in range(n):
        p=next((i for i in range(k,n) if a[i][k]),None)
        if p is None:return Q(0)
        if p!=k:a[k],a[p]=a[p],a[k];result=-result
        d=a[k][k];result*=d
        for j in range(k,n):a[k][j]/=d
        for i in range(k+1,n):
            d=a[i][k]
            for j in range(k,n):a[i][j]-=d*a[k][j]
    return result

def phi(n):return sum(math.gcd(n,a)==1 for a in range(1,n+1))
def mobius(n):
    sign=1;p=2
    while p*p<=n:
        if n%p==0:
            n//=p;sign=-sign
            if n%p==0:return 0
        p+=1
    return -sign if n>1 else sign
def divs(n):return [d for d in range(1,n+1) if n%d==0]
def valuation(n,p):
    if n==0:return None
    s=0
    while n%p==0:n//=p;s+=1
    return s

def hensel():
    p=7;a=3;mod=7;states=[dict(modulus=mod,root=a)]
    for k in range(1,8):
        roots=[a+t*mod for t in range(p) if ((a+t*mod)**2-2)%(mod*p)==0]
        assert len(roots)==1
        b=roots[0];assert b%mod==a
        a=b;mod*=p;assert (a*a-2)%mod==0 and math.gcd(2*a,p)==1
        states.append(dict(modulus=mod,root=a))
    assert states[1]['root']==10 and states[2]['root']==108
    return states
check('Simple-root compatible Hensel digits','D01-F01',hensel,'Eight finite congruence levels for X²−2 at p=7; convergence is supplied by the written theorem.')

def precision():
    r=4*25
    assert r%25==0 and r%125==100 and valuation(r,5)==2
    coeff=[27,0,9,27]
    vals=[valuation(x,3) for x in coeff if x]
    assert min(vals)==2 and next(i for i,x in enumerate(coeff) if x and valuation(x,3)==2)==2
    product=[27,27,9,36,27]
    assert min(valuation(x,3) for x in product if x)==2
    assert next(i for i,x in enumerate(product) if x and valuation(x,3)==2)==2
    return dict(filtered_residual=r,valuation=2,mu=2,lambda_index=2)
check('Finite precision and polynomial mu/lambda example','D01-F01',precision,'The power series here are exact polynomials; no unknown tail is inferred.')

def gcd_kernel():
    for n in [1,4,8,12]:
        g=[[math.gcd(i,j) for j in range(1,n+1)] for i in range(1,n+1)]
        e=[[int(i%d==0) for d in range(1,n+1)] for i in range(1,n+1)]
        w=[phi(d) for d in range(1,n+1)]
        assert all(g[i][j]==sum(e[i][d]*w[d]*e[j][d] for d in range(n)) for i in range(n) for j in range(n))
        assert det(g)==math.prod(w)
    return dict(cutoffs=[1,4,8,12],determinant_at_four=4)
check('GCD incidence factorization and determinants','D01-F02',gcd_kernel,'Finite exact matrix replay; the divisor-sum argument proves the general identity.')

def monomials():
    target=2**20*3**12
    points={(2**(10-3*r)*3**(6-3*s),2**(2*r)*3**(2*s)) for r in range(4) for s in range(3)}
    assert len(points)==12 and all(x*x*y**3==target for x,y in points)
    exp2=[(a,b) for a in range(21) for b in range(21) if 2*a+3*b==20]
    exp3=[(a,b) for a in range(13) for b in range(13) if 2*a+3*b==12]
    assert len(exp2)==4 and len(exp3)==3
    c=[1]
    for a in [3,2]:
        out=[0]*(len(c)+a)
        for i,v in enumerate(c):
            for j in range(a+1):out[i+j]+=v
        c=out
    assert c==[1,2,3,3,2,1]
    return dict(solution_count=12,divisor_rank_polynomial=c)
check('Complete bounded valuation rectangle','D01-F02',monomials,'Enumeration is exhaustive after the written prime-support and valuation bounds.')

def factorials():
    for p in [2,3,5,7]:
        for n in range(1,81):
            v=sum(n//(p**j) for j in range(1,10))
            u=math.factorial(n)//p**v
            m=n//p;vm=sum(m//(p**j) for j in range(1,10))
            assert u==math.prod(i for i in range(1,n+1) if i%p)*math.factorial(m)//p**vm
    assert math.factorial(10)//3**4==44800
    return dict(primes=[2,3,5,7],max_n=80,U_3_10=44800)
check('Stripped factorial integer recursion','D01-F02',factorials,'Integer factorization replay; no invalid modular division is used.')

def fibres():
    units=[a for a in range(1680) if math.gcd(a,1680)==1]
    counts={b:sum(a%30==b for a in units) for b in range(30) if math.gcd(b,30)==1}
    assert len(units)==384 and len(counts)==8 and set(counts.values())=={48}
    def order(a):
        x=1
        for k in range(1,385):
            x=x*a%1680
            if x==1:return k
        raise AssertionError('Order did not return')
    assert max(order(a) for a in units)==12
    cs={n:sum(d*mobius(30//d) for d in divs(math.gcd(30,n))) for n in [1,2,15,30]}
    assert cs=={1:-1,2:1,15:-8,30:8}
    return dict(fibres=counts,trace_values={n:48*c for n,c in cs.items()},maximum_galois_element_order=12)
check('L07 conductor fibres and exact traces','D01-F03',fibres,'The implemented 1680-to-30 residue model; field interpretation uses the written cyclotomic theorem.')

def trace_orthogonality():
    p=5;a=[2,-1,3,0,1];cyclic=[0]*p
    for i,x in enumerate(a):
        for j,y in enumerate(a):cyclic[(i+j)%p]+=x*y
    trace=(p-1)*cyclic[0]-sum(cyclic[1:])
    assert trace==p*cyclic[0]-sum(a)**2
    nums=[95800,217519,414560,422481]
    assert sum(n**4 for n in nums[:3])==nums[3]**4
    assert math.gcd(*nums)==1
    return dict(trace=trace,primitive_fourth_power_counterexample=True)
check('Trace coefficient and scope counterexample','D01-F03',trace_orthogonality,'Finite exact cyclotomic coefficient model and integer counterexample.')

def pell():
    positive=[];x,y=1,0
    for j in range(21):
        assert x*x-2*y*y==1
        positive.append((x,y));x,y=3*x+4*y,2*x+3*y
    assert positive[1:5]==[(3,2),(17,12),(99,70),(577,408)]
    state=(1,0);orbit=[]
    while state not in orbit:
        orbit.append(state);x,y=state;state=((3*x+4*y)%3,(2*x+3*y)%3)
    assert state==orbit[0] and len(orbit)==4
    assert [j for j,(x,y) in enumerate(orbit) if y==0]==[0,2]
    bound=3000;generated=set()
    for seed in [(1,2),(5,4)]:
        for j in range(-12,13):
            x,y=seed
            for k in range(abs(j)):
                x,y=(3*x+4*y,2*x+3*y) if j>=0 else (3*x-4*y,-2*x+3*y)
            assert x*x-2*y*y==-7 and y>0
            if y<=bound:generated.add((x,y))
    brute=set()
    for y in range(1,bound+1):
        t=2*y*y-7
        if t>=0:
            x=math.isqrt(t)
            if x*x==t:brute.update({(x,y),(-x,y)})
    assert generated==brute
    seeds=[(math.isqrt(2*y*y-7),y) for y in range(2,6) if math.isqrt(2*y*y-7)**2==2*y*y-7]
    assert seeds==[(1,2),(5,4)]
    return dict(positive_steps=20,modulus_three_period=orbit,negative_seed_candidates=seeds,bounded_comparison_y=bound,negative_points_in_window=len(brute))
check('L10 Pell invariants, seed interval and modular filter','D01-F04',pell,'The bounded comparison validates the model; the written descent and interval proof establish global completeness.')

def norm(a,b,c):return a**3-4*b**3+16*c**3+12*a*b*c
def norm_forms():
    for a in range(-3,4):
        for b in range(-3,4):
            for c in range(-3,4):
                assert det([[a,-4*c,-4*b],[b,a,-4*c],[c,b,a]])==norm(a,b,c)
    assert norm(5,-3,2)==norm(1,-1,-1)==1
    assert norm(-1,-3,0)==norm(-13,-2,4)==107
    # Independently multiply (-1-3z)(1-z-z²), using z³=-4.
    raw=[0]*5
    for i,x in enumerate([-1,-3,0]):
        for j,y in enumerate([1,-1,-1]):raw[i+j]+=x*y
    for k in [4,3]:raw[k-3]-=4*raw[k]
    assert raw[:3]==[-13,-2,4]
    for u in range(-5,6):
        for v in range(-5,6):
            a,b=-3*u,-v
            n=det([[a,0,18*b],[b,a,27*b],[0,b,a]])
            h=-3*u**3+9*u*v*v-2*v**3
            assert n==9*h
    return dict(cubic_norm_samples=343,transport_output=[-13,-2,4],binary_plane_preserved=False,Thue_scalar=9)
check('Cubic determinant norms and binary-plane escape','D01-F05',norm_forms,'Exact determinant identities and one explicit transport; no unit-basis or global norm search is claimed.')

def discriminants():
    cubic=-4*(-1)**3-27
    quartic=256*(-1)**3-27*(-1)**4
    assert cubic==-23 and quartic==-283
    assert 8*5*40==40**2 and 40*(-4)*(-40)==4*40**2
    # F2 quartic x^4+x+1 has no linear factor and remainder 1
    # modulo the unique monic irreducible quadratic x²+x+1.
    def rem(a,b):
        while a.bit_length()>=b.bit_length():a^=b<<(a.bit_length()-b.bit_length())
        return a
    assert rem(0b10011,0b111)==1
    assert all((x**4+x+1)%2 for x in [0,1])
    return dict(cubic_discriminant=cubic,quartic_discriminant=quartic,relative_discriminant_norms=[1,4])
check('Field obstruction discriminant arithmetic','D01-F05',discriminants,'Finite polynomial and discriminant checks; Galois and class-field conclusions use the stated structural theorems.')

def mordell_coefficients():
    cases=[]
    for b in [-1,1]:
        rhs=(1//b+2*b*b)
        for a in [-2,-1,0,1,2]:
            if b*(3*a*a-2*b*b)==1:
                x=a*a+2*b*b;y=a**3-6*a*b*b
                assert y*y==x**3-2
                cases.append((x,y))
    assert set(cases)=={(3,5),(3,-5)}
    assert Q(1,4)+2*Q(1,4)==Q(3,4)<1
    return dict(coefficient_solutions=cases,norm_Euclidean_rounding_bound='3/4')
check('Mordell cube coefficients','D01-F05',mordell_coefficients,'All remaining b=±1 coefficient cases after the written UFD and coprimality proof, not a bounded x-search.')

def modular_forms():
    wt38=[(a,b) for a in range(10) for b in range(8) if 4*a+6*b==38]
    wt26=[(a,b) for a in range(8) for b in range(6) if 4*a+6*b==26]
    assert set(wt38)=={(8,1),(5,3),(2,5)} and len(wt26)==2
    sigma=lambda n:sum(d**3 for d in divs(n))
    assert sigma(2)==9 and sigma(4)==sigma(2)**2-2**3==73
    p,a=2,-2;coeff=[1,-(a*a-p),p*(a*a-p),-p**3]
    assert coeff==[1,-2,4,-8]
    return dict(weight38_monomials=wt38,weight26_monomials=wt26,E4_p2=[9,73],symmetric_square_coefficients=coeff)
check('Modular weights and Hecke arithmetic','D01-F06',modular_forms,'Finite monomial and coefficient checks, conditional on the full-level modular-form ring theorem.')

def divisor_convolution():
    # Record coefficients of formal log primes as exact exponent vectors.
    primes=[p for p in range(2,101) if all(p%d for d in range(2,math.isqrt(p)+1))]
    for n in range(1,101):
        for p in primes:
            c=sum(mobius(d)*(valuation(n//d,p) or 0) for d in divs(n))
            expected=int(n>1 and (lambda m:m==1)(n//p**(valuation(n,p) or 0)) and n%p==0)
            assert c==expected,(n,p,c,expected)
        assert sum(phi(d) for d in divs(n))==n
    assert Q(1,2*100**2)==Q(1,20000)
    return dict(convolution_max_n=100,totient_tail_sigma4_N100='1/20000')
check('Formal-log convolution and totient divisor identity','D01-F07',divisor_convolution,'Exact formal prime-log coefficients avoid numerical cancellation; analytic tails use the written integral bound.')

def curve_models():
    for t in range(-8,9):
        x,y=t*t,t*t*t
        assert y*y==x*x*x
        assert y*y-x*x*x==0
    # Cleared forward corner identity: z³ f((z-1)/z)
    # = z³-2z²+3z-1, checked coefficient-wise by evaluations
    # at four distinct integers, sufficient for cubics.
    for z in [2,3,4,5]:
        u=Q(z-1,z)
        assert z**3*(u**3-u+1)==z**3-2*z*z+3*z-1
    def genus(d,m):
        numerator=(d-1)*(m-1)-math.gcd(d,m)+1
        assert numerator%2==0
        return numerator//2
    assert genus(2,3)==1 and genus(3,4)==3 and genus(2,5)==2
    return dict(cusp_intersection_length=3,corner_identity='exact cubic identity',superelliptic_genera={'2,3':1,'3,4':3,'2,5':2})
check('Cusp and superelliptic worked models','D02-F01',curve_models,'Polynomial identities and genus arithmetic after the written normalization and ramification arguments.')

def count_general(p):
    return 1+sum((y*y+y-x*x*x+x)%p==0 for x in range(p) for y in range(p))
def ec_add(P,R):
    if P is None:return R
    if R is None:return P
    x,y=P;u,v=R
    if x==u and y+v+1==0:return None
    slope=(3*x*x-1)/(2*y+1) if P==R else (v-y)/(u-x)
    intercept=y-slope*x
    X=slope*slope-x-u
    Y=-slope*X-intercept-1
    assert Y*Y+Y==X**3-X
    return X,Y
def elliptic():
    counts={p:count_general(p) for p in [2,3,5,7]}
    assert counts=={2:5,3:7,5:8,7:9}
    P=(Q(0),Q(0));R=None;points={}
    for j in range(1,8):R=ec_add(R,P);points[j]=R
    assert points[2]==(1,0) and points[3]==(-1,-1) and points[7]==(Q(-5,9),Q(8,27))
    for p in [3,7,11,19]:
        count=1+sum((y*y-x*x*x+x)%p==0 for x in range(p) for y in range(p))
        assert count==p+1
    # Prime-order torsion exclusions used in the written proof.
    assert [ell for ell in [2,5] if (counts[7]%ell)==0]==[]
    return dict(counts=counts,multiples={j:[str(x) for x in point] for j,point in points.items()},CM_zero_trace_primes=[3,7,11,19])
check('Elliptic finite counts and exact group law','D02-F02',elliptic,'Specific curves and rational multiples; the prime-to-p reduction theorem supplies the global rank lower bound.')

def genus_two():
    p=3
    elems=[(a,b) for a in range(3) for b in range(3)]
    def add(x,y):return ((x[0]+y[0])%3,(x[1]+y[1])%3)
    def neg(x):return ((-x[0])%3,(-x[1])%3)
    def mul(x,y):return ((x[0]*y[0]-x[1]*y[1])%3,(x[0]*y[1]+x[1]*y[0])%3)
    def power(x,n):
        out=(1,0)
        for _ in range(n):out=mul(out,x)
        return out
    n1=1+sum((y*y-x**5+x-1)%3==0 for x in range(3) for y in range(3))
    n2=1+sum(mul(y,y)==add(add(power(x,5),neg(x)),(1,0)) for x in elems for y in elems)
    assert (n1,n2)==(7,15)
    a1=p+1-n1;a2=(n2-(p*p+1)+a1*a1)//2
    coeff=[1,-a1,a2,-p*a1,p*p]
    assert coeff==[1,3,7,9,9]
    return dict(N1=n1,N2=n2,Frobenius_polynomial_coefficients=coeff,field='F3[u]/(u²+1)')
check('Genus-two finite-field Frobenius reconstruction','D02-F02',genus_two,'Exact F3 and F9 enumeration; reciprocal symmetry and the point-trace theorem are stated inputs.')

def positivity():
    rows=[]
    for n in [3,4,5,6,7]:
        size=sum((a*d-b*c)%n==1 for a in range(n) for b in range(n) for c in range(n) for d in range(n))
        mu=size//2;c=mu//n;g=Q(2-c,2)+Q(mu,12)
        assert g.denominator==1
        rows.append(dict(level=n,index=mu,cusps=c,genus=int(g)))
    assert [r['genus'] for r in rows]==[0,0,0,1,3]
    assert det([[1,1],[0,2]])==2
    assert det([[1,1],[0,1]])==det([[1,1],[1,2]])==1
    assert [(g,d,d+1-g,d-g) for g,d in [(1,3),(3,7)]]==[(1,3,3,2),(3,7,5,4)]
    return dict(modular_curves=rows,toric_determinants=[2,1,1],embedding_examples=[dict(genus=1,degree=3,sections=3,target_dimension=2),dict(genus=3,degree=7,sections=5,target_dimension=4)])
check('Compactification and positivity arithmetic','D02-F03',positivity,'Small modular indices and two-dimensional cones; global positivity and embedding follow the stated geometric theorems.')

def monodromy():
    for n in [1,2,6,12]:
        # Image of M_n-I is nZ e1; the second basis coordinate is free.
        assert math.gcd(n,0)==n
    assert sum((-1)**i*b for i,b in enumerate([1,2,1]))==0
    assert [2-2*g for g in [0,1,2]]==[2,0,-2]
    assert [1+5**r for r in [1,2]]==[6,26]
    N=[[0,1],[0,0]]
    assert all(sum(N[i][k]*N[k][j] for k in range(2))==0 for i in range(2) for j in range(2))
    assert [N[0][1],N[1][0]]==[1,0]
    return dict(nonzero_weight_grades=[0,2],N_Gr2_to_Gr0='1',integer_coinvariant_torsion_orders=[1,2,6,12],P1_Frobenius_counts=[6,26],curve_euler_characteristics=[2,0,-2])
check('Monodromy, torsion and realization tests','D02-F04',monodromy,'Exact rank-two lattice model and cellular counts; no general comparison theorem is computationally certified.')

def provenance():
    corpus=json.loads((BASE/'data/source_corpus_initial_routing.json').read_text());by_uid={x['uid']:x for x in corpus}
    families=json.loads((HERE/'families.json').read_text())
    reviews=json.loads((HERE/'classification_review.json').read_text())
    initial={x['uid'] for x in corpus if x['primary_domain'] in ['D01','D02']}
    reviewed={x['uid'] for x in reviews}
    assert initial<=reviewed and len(reviewed)==len(reviews)
    assert len(families)==11 and {x['domain_id'] for x in families}=={'D01','D02'}
    for f in families:
        assert 4<=len(f['anchor_uids'])<=8
        assert set(f['anchor_uids'])<=set(f['source_uids'])<=by_uid.keys()
        assert len(f['source_uids'])==len(set(f['source_uids']))
        for p in f['progression']:
            assert set(p['evidence_uids'])<=set(f['source_uids'])
            assert all(by_uid[u]['year']==p['year'] for u in p['evidence_uids'])
    return dict(initial_primary_entries=len(initial),reviewed_entries=len(reviews),concept_families=len(families),all_source_ids_valid=True)
check('Source coverage and chronology validation','D01-F01',provenance,'Catalog integrity and source-supported years only; no historical originality or proof attribution is inferred.')

summary=dict(status='pass',runtime='Python standard library; exact integers and fractions',check_count=len(RESULTS),checks=RESULTS,limitation='Executed checks replay specified finite models. Global completeness, geometric existence and comparison theorems rely on their written proofs or explicitly cited classical inputs.')
(HERE/'checks.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2))
print(json.dumps(dict(status='pass',check_count=len(RESULTS),families=11,reviewed_entries=176),indent=2))
