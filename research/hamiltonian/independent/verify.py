#!/usr/bin/env python3
"""Independent exact derivative/exponential checks for partner research."""
from engine import *
from pathlib import Path
from math import comb
import json,random
ROOT=Path(__file__).resolve().parent
checks=[];assertions=0

def check(name,fn):
    global assertions
    before=assertions;details=fn();checks.append({'name':name,'status':'passed','assertions':assertions-before,'details':details})
def eq(a,b):
    global assertions
    assert a==b,(a,b);assertions+=1

def convention():
    eq(moyal(monomial(1,0),monomial(0,1)),{0:monomial(0,0)})
    eq(moyal(monomial(3,0),monomial(0,3)),{0:monomial(2,2,9),2:monomial(0,0,F(-3,2))})
    eq(moyal(monomial(1,5),monomial(5,3)),{0:monomial(5,7,-22),4:monomial(1,3,105)})
    return {'convention':'(f star g-g star f)/(i hbar), star=exp[(i hbar/2)Lambda]'}
check('Canonical convention and higher obstruction',convention)

def qp3_exactspace():
    H=monomial(1,3);rows=[]
    for c in range(15):
        for d in range(15):
            expected=c<=1 or c==3*d+2
            eq(exact_partner(H,monomial(c,d)),expected)
    for n in range(25):
        basis=homogeneous_kernel(H,n);expected=1 if n==0 else 2+int(n>=2 and n%4==2)
        eq(len(basis),expected);rows.append([n,len(basis)])
    return {'monomials_tested':225,'homogeneous_dimensions':rows}
check('Complete qp3 exponent rule on an independent finite grid',qp3_exactspace)

def closure():
    H=monomial(1,3);G=monomial(2,0);K=monomial(1,2)
    eq(exact_partner(H,G),True);eq(exact_partner(H,K),True)
    eq(exact_partner(H,multiply(G,G)),False)
    B=poisson(G,K);eq(B,monomial(2,1,4));eq(exact_partner(H,B),False)
    first=moyal(H,G);second=formal_action(H,first)
    eq(first,{0:monomial(2,2,-6)});eq(second,{0:monomial(2,4,24),2:monomial(0,2,18)})
    eq(poisson(H,poisson(H,G)),monomial(2,4,24))
    rng=random.Random(20261021)
    for _ in range(50):
        a=tidy({(q,p):rng.randint(-3,3) for q in [0,1] for p in range(6)})
        b=tidy({(q,p):rng.randint(-3,3) for q in [0,1] for p in range(6)})
        eq(exact_partner(a,b),True);eq(all(q<=1 for q,p in poisson(a,b)),True)
        eq(all(q<=1 for q,p in poisson(H,a)),True)
    return {'first_action':serialize_series(first),'second_action':serialize_series(second),'Poisson_Lie_counterexample':serialize(B),'random_strip_pairs':50}
check('Closure failures, dynamic discrepancy and exact strip Lie algebra',closure)

def qF_classification():
    p=monomial(0,1);one=monomial(0,0)
    samples=[('p2',power(p,2),2,None),('p2+p+1',add(power(p,2),p,one),2,None),('p3+p',add(power(p,3),p),3,None),('p3+p2+1',add(power(p,3),power(p,2),one),3,None),('p4',power(p,4),4,None),('p4+p2',add(power(p,4),power(p,2)),4,None),('p5+p',add(power(p,5),p),5,p),('p5+p3+p',add(power(p,5),power(p,3),p),5,None),('(p-1)5+3p+7',add(power(add(p,scale(one,-1)),5),scale(p,3),scale(one,7)),5,add(p,scale(one,-1))),('integral of (p2+1)3',add(scale(power(p,8),F(1,56)),scale(power(p,6),F(1,10)),scale(power(p,4),F(1,4)),scale(power(p,2),F(1,2))),8,add(power(p,2),one))]
    counts=[];D=8
    for label,Fpoly,M,R in samples:
        H=multiply(monomial(1,0),Fpoly);F2=derivative(Fpoly,p=2);total=0
        for c in range(11):
            basis=kernel_for_basis(H,[(c,d) for d in range(D+1)])
            if c<=1:expected=None;expected_count=D+1
            elif M==2:expected=monomial(c,0);expected_count=1
            elif M==3 and (c-2)%3==0:
                r=(c-2)//3;expected=multiply(monomial(c,0),power(F2,r));expected_count=1 if max(b for a,b in expected)<=D else 0
            elif M>=4 and c==2:expected=monomial(2,0);expected_count=1
            elif M>=4 and c==3 and R is not None:expected=multiply(monomial(3,0),R);expected_count=1
            else:expected=None;expected_count=0
            eq(len(basis),expected_count);total+=len(basis)
            if expected_count==1:
                eq(primitive(basis[0]),primitive(expected))
                eq(exact_partner(H,poisson(H,basis[0])),False)
            elif c<=1:
                for G in basis:eq(exact_partner(H,poisson(H,G)),True)
        counts.append({'F':label,'degree':M,'tested_q_degree_max':10,'tested_p_degree_max':D,'kernel_dimension':total})
    return counts
check('Arbitrary-F classification and dynamic escape in full q/p rectangles',qF_classification)

def associative():
    H=monomial(1,3);rng=random.Random(181)
    for _ in range(40):
        G=tidy({(q,p):rng.randint(-2,2) for q,p in [(0,0),(0,1),(0,3),(1,0),(1,2),(2,0),(5,1),(8,2)]})
        eq(exact_partner(H,G),True)
        if any(q>0 for q,p in G):eq(exact_partner(H,power(G,3)),False)
    return {'polynomial_cube_counterexamples':40,'theorem':'G cubed in E(qp3) implies G is in k[p]'}
check('Associative-subalgebra rigidity for the favorite Hamiltonian',associative)

def apolar(A,B,n):
    return sum(F((-1)**j,comb(n,j))*A.get((n-j,j),F(0))*B.get((j,n-j),F(0)) for j in range(n+1))
def quartic_review():
    q=monomial(1,0);p=monomial(0,1);rng=random.Random(411)
    quartics=[('q4',power(q,4),1),('q2p2',multiply(power(q,2),power(p,2)),2),('(q2+p2)2',power(add(power(q,2),power(p,2)),2),2),('qp3',multiply(q,power(p,3)),4),('q4+p4',add(power(q,4),power(p,4)),4),('q4+q2p2+p4',add(power(q,4),multiply(power(q,2),power(p,2)),power(p,4)),4),('q4+qp3+p4',add(power(q,4),multiply(q,power(p,3)),power(p,4)),4)]
    dimensions=[]
    for label,H,e in quartics:
        row=[]
        for n in range(2,17):
            eq(len(homogeneous_kernel(H,n)),2+int((n-2)%e==0));row.append([n,2+int((n-2)%e==0)])
            G=tidy({(n-j,j):rng.randint(-3,3) for j in range(n+1)})
            Fpoly=tidy({(n-2-j,j):rng.randint(-3,3) for j in range(n-1)})
            T3=scale(defects(H,G).get(2,{}),-24)
            eq(apolar(T3,Fpoly,n-2),-6*n*(n-1)*apolar(G,poisson(H,Fpoly),n))
        delta=add(multiply(derivative(H,q=2),derivative(H,p=2)),scale(power(derivative(H,q=1,p=1),2),-1))
        eq(exact_partner(H,delta),True)
        dimensions.append({'H':label,'primitive_root_degree':e,'dimensions':row})
    return dimensions
check('Independent quartic apolar adjoint, full degree dimensions and Hessian partners',quartic_review)

def star_power(H,n):
    series={0:monomial(0,0)}
    for _ in range(n):
        terms={}
        for j,A in series.items():
            for (a,b,k),(real,imag) in star(A,H).items():
                old=terms.get((a,b,j+k),(F(0),F(0)));terms[(a,b,j+k)]=(old[0]+real,old[1]+imag)
        assert all(not imag for real,imag in terms.values())
        series={}
        for (a,b,k),(real,imag) in terms.items():
            if real:series.setdefault(k,{})[(a,b)]=real
    return series

def ladders():
    records=[]
    for m,c,d in [(3,3*r+2,r) for r in range(7)]+[(2,c,0) for c in range(1,6)]+[(5,4,0),(11,3,3)]:
        H=monomial(1,m);s=(c-d)//(m-1);assert c-d==s*(m-1) and s>=0;N=s+c
        series={0:monomial(c,d)}
        for _ in range(N):series=formal_action(H,series)
        expected={k:scale(P,(-(m-1))**N*factorial(N)) for k,P in star_power(H,c).items()}
        eq(series,expected);eq(bool(series),True);eq(formal_action(H,series),{})
        classical=monomial(c,d)
        for _ in range(N):classical=poisson(H,classical)
        eq(classical,scale(power(H,c),(-(m-1))**N*factorial(N)));eq(poisson(H,classical),{})
        records.append(dict(m=m,c=c,d=d,top_order=N,nilpotence_index=N+1))
    H=monomial(1,3);G=monomial(2,0);series={0:G};derivatives=[]
    for n in range(4):
        derivatives.append(serialize_series(series));series=formal_action(H,series)
    for r in range(8):
        c=3*r+2;G=monomial(c,r);second=formal_action(H,moyal(H,G))
        eq(second,{0:monomial(c,r+4,(8*r+6)*(8*r+4)),2:monomial(3*r,r+2,(12*r+9)*(3*r+2)*(3*r+1))})
    H=add(monomial(4,0),monomial(0,4));G=monomial(2,2);K=poisson(H,G)
    eq(K,add(monomial(5,1,8),monomial(1,5,-8)));eq(defects(H,K),{2:monomial(2,2,960)})
    return {'finite_quantum_ladders':records,'q2_first_four_derivatives':derivatives,'all_r_second_action_formula_checked_r_max':7,'generic_quartic_dynamic_failure':'H=q4+p4,G=q2p2; correction in second action is960 hbar2 q2p2'}
check('Finite quantum ladders and all-r dynamic obstruction',ladders)

result={'status':'passed','implementation':'direct derivative expansion with Gaussian rational coefficients','check_groups':len(checks),'exact_assertions':assertions,'checks':checks,'scope':'Finite checks corroborate the accompanying all-degree proofs; they do not replace those proofs or assert a global classification for arbitrary Hamiltonians.'}
(ROOT/'checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:result[k] for k in ['status','check_groups','exact_assertions']}))
