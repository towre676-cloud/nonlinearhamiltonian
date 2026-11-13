"""Exact regression for NONLINEAR_B_QUADRATIC_CUBIC.md.

The proof is in the manuscript. Finite matrices below are regression only.
Two implementations are used: symbolic differentiation and sparse monomial
contraction. Output degrees are never truncated.
"""
from __future__ import annotations

import argparse
import json
import math
import platform
from pathlib import Path

import sympy as s

q, p = s.symbols("q p")
checks = []


def equal(name, actual, expected=0):
    assert s.simplify(s.expand(actual - expected)) == 0, name
    checks.append(name)


def T(H, G, n):
    return s.expand(sum(
        (-1)**i * s.binomial(n, i)
        * s.diff(H, q, n-i, p, i) * s.diff(G, q, i, p, n-i)
        for i in range(n+1)
    ))


def symbolic_checks():
    h, A, B = (s.Function(name)(q) for name in ("h", "A", "B"))
    G = s.Function("G")(q, p)
    H = h + A*p + B*p**2
    equal("general_T3", T(H, G, 3),
          (s.diff(h,q,3)+s.diff(A,q,3)*p+s.diff(B,q,3)*p**2)*s.diff(G,p,3)
          -3*(s.diff(A,q,2)+2*s.diff(B,q,2)*p)*s.diff(G,q,p,2)
          +6*s.diff(B,q)*s.diff(G,q,2,p))
    equal("general_T5", T(H, G, 5),
          (s.diff(h,q,5)+s.diff(A,q,5)*p+s.diff(B,q,5)*p**2)*s.diff(G,p,5)
          -5*(s.diff(A,q,4)+2*s.diff(B,q,4)*p)*s.diff(G,q,p,4)
          +20*s.diff(B,q,3)*s.diff(G,q,2,p,3))
    f, g, k = (s.Function(name)(q) for name in ("f", "g", "k"))
    X = f+g*p+k*p**2
    equal("static_V2_T3", T(H,X,3),
          6*(s.diff(B,q)*s.diff(g,q,2)-s.diff(A,q,2)*s.diff(k,q))
          +12*p*(s.diff(B,q)*s.diff(k,q,2)-s.diff(B,q,2)*s.diff(k,q)))
    equal("static_V2_T5", T(H,X,5))
    lam, mu, a, e = s.symbols("lam mu a e")
    X = f+p*(lam*A+a*q+e)+p**2*(lam*B+mu)
    equal("static_sector_converse_T3", T(H,X,3))
    equal("static_sector_converse_T5", T(H,X,5))
    equal("nonlinear_mu_obstruction", T(H,T(H,X,1),3).coeff(p,2),
          24*mu*(2*s.diff(B,q)*s.diff(B,q,3)-3*s.diff(B,q,2)**2))

    b0,b1,b2,b3,u,v,n = s.symbols("b0 b1 b2 b3 u v n")
    B3 = b3*q**3+b2*q**2+b1*q+b0
    top = (n-1)*(n-2)*s.diff(B3,q,3)*(u*q+v)-6*(n-1)*s.diff(B3,q,2)*u
    equal("cubic_top_resonance", top,
          6*(n-1)*(b3*(n-8)*u*q+(n-2)*b3*v-2*b2*u))
    h6,b,c = s.symbols("h6 b c", nonzero=True)
    H = h6*q**6+b*q**3*p**2
    X = c*q*p**8-28*h6*c/b*q**4*p**6
    equal("cubic_resonance_fifth", T(H,X,5).coeff(p,3))
    equal("cubic_resonance_third", T(H,X,3).coeff(p,5).coeff(q,4),104832*h6*c)

    B2 = b2*q**2+b1*q+b0
    t=s.diff(B2,q); delta=s.expand(t**2-2*s.diff(B2,q,2)*B2)
    equal("quadratic_g4_square_obstruction",
          t*s.diff(B2**2,q,2)-3*s.diff(B2,q,2)*s.diff(B2**2,q),2*t*delta)
    X=u+v*t**3
    equal("quadratic_g3_to_Dg4",3*t*X-2*B2*s.diff(X,q),3*u*t+3*v*delta*t**2)
    H=h6*q**6+b*q**2*p**2
    X=c*q**4*p**4-s.Rational(5,2)*h6*c/b*q**8*p**2
    equal("quadratic_g4_static_forcing",T(H,X,3))
    equal("quadratic_g4_dynamic_obstruction",T(H,X,1).coeff(p,3).coeff(q,9),54*h6*c)
    X=c*q**3*p**3-s.Rational(10,7)*h6*c/b*q**7*p
    equal("quadratic_g3_static_forcing",T(H,X,3))
    equal("quadratic_g3_dynamic_obstruction",T(H,X,1).coeff(p,2).coeff(q,8),s.Rational(246,7)*h6*c)

    h=sum(s.Symbol(f"h{i}")*q**i for i in range(7))
    A=s.Symbol("a0")+s.Symbol("a1")*q
    r,c0=s.symbols("r c0"); x=q-r
    for d in (2,3):
        B=b*x**d+c0; H=h+A*p+B*p**2; X=x*p
        equal(f"degree_{d}_extra_static_T3",T(H,X,3))
        equal(f"degree_{d}_extra_static_T5",T(H,X,5))
        equal(f"degree_{d}_extra_first_T3",T(H,T(H,X,1),3))
        equal(f"degree_{d}_extra_first_T5",T(H,T(H,X,1),5))
        equal(f"degree_{d}_extra_D",T(H,X,1),x*s.diff(h,q)+(x*s.diff(A,q)-A)*p+((d-2)*b*x**d-2*c0)*p**2)
        equal(f"degree_{d}_second_refinement_leading",s.expand(x*s.diff(h,q)-(d-2)*h).coeff(q,6),(8-d)*s.Symbol("h6"))
        equal(f"degree_{d}_mu_nonzero_leading",
              s.Poly(2*s.diff(B,q)*s.diff(B,q,3)-3*s.diff(B,q,2)**2,q).LC(),-d**2*(d-1)*(d+1)*b**2)
    H=q**6+q*p**2; X=p**2+s.Rational(12,5)*q**5
    equal("affine_counterexample_static_T3",T(H,X,3))
    equal("affine_counterexample_static_T5",T(H,X,5))
    equal("affine_counterexample_D",T(H,X,1),2*p**3-12*q**5*p)
    equal("affine_counterexample_first_T3",T(H,T(H,X,1),3))
    equal("affine_counterexample_first_T5",T(H,T(H,X,1),5))
    equal("affine_counterexample_second_failure",T(H,T(H,T(H,X,1),1),3),51840*p*q**3)


# Separate implementation using exponent dictionaries and falling factorials.
def sparse(expr):
    return {m:c for m,c in s.Poly(s.expand(expr),q,p).terms() if c}


def falling(a,b):
    return math.prod(range(a-b+1,a+1)) if 0<=b<=a else 0


def contract(H,G,n):
    out={}
    for (a,b),h in H.items():
        for (c,d),g in G.items():
            for i in range(n+1):
                factor=((-1)**i*math.comb(n,i)*falling(a,n-i)*falling(b,i)
                        *falling(c,i)*falling(d,n-i))
                if factor:
                    mon=(a+c-n,b+d-n)
                    out[mon]=out.get(mon,0)+h*g*factor
    return {m:c for m,c in out.items() if c}


def bounded_case(name,H,expected1,expected2,qmax=10,pmax=8):
    mons=[(i,j) for j in range(pmax+1) for i in range(qmax+1)]
    inputs=[{m:s.Integer(1)} for m in mons]
    h=sparse(H); current=inputs; C=s.eye(len(mons)); dims=[]; saved={}
    for r in range(3):
        rows={}
        for col,g in enumerate(current):
            for n in (3,5):
                for m,c in contract(h,g,n).items():
                    rows.setdefault((n,*m),{})[col]=c
        entries={(i,j):c for i,row in enumerate(rows.values()) for j,c in row.items()}
        M=s.MutableSparseMatrix(len(rows),len(mons),entries)
        ns=(M*C).nullspace()
        C=C*s.Matrix.hstack(*ns) if ns else s.zeros(len(mons),0)
        dims.append(C.cols)
        if r in (1,2):
            expected=expected1 if r==1 else expected2
            E=s.Matrix([[sparse(x).get(m,0) for x in expected] for m in mons])
            assert C.cols==len(expected),(name,r,C.cols)
            assert C.row_join(E).rank()==C.cols,(name,r,"basis mismatch")
            saved[str(r)]=[str(s.expand(x)) for x in expected]
        current=[contract(h,g,1) for g in current]
    if s.degree(H,p)==2 and s.degree(s.expand(H).coeff(p,2),q)==3:
        assert dims[0]==qmax+5,(name,"cubic static dimension",dims[0])
    return {"case":name,"H":str(s.expand(H)),"input_box":{"q_max":qmax,"p_max":pmax},
            "dimensions":dims,"expected_bases":saved,"output_truncated":False}


def finite_checks():
    h=2*q**6-3*q**5+7*q**3-q+11; A=3*q-2
    cases=[]
    for name,h0,A0,B0,x in [
        ("quadratic_square",q**6,0,q**2,q),
        ("quadratic_distinct_roots",h,A,q**2+1,q),
        ("quadratic_shifted_square",h,A,(2*q+1)**2,q+s.Rational(1,2)),
        ("quadratic_shifted_distinct",h,A,3*q**2-2*q+5,q-s.Rational(1,3)),
        ("cubic_regular",q**6,0,q**3+q,None),
        ("cubic_regular_shifted",h,A,2*q**3+q**2-3*q+7,None),
        ("cubic_exceptional",q**6,0,q**3,q),
        ("cubic_exceptional_nonzero_constant",h,A,2*(q-2)**3+5,q-2),
    ]:
        H=s.expand(h0+A0*p+B0*p**2)
        expected=[s.Integer(1),H]+([] if x is None else [x*p])
        case=bounded_case(name,H,expected,[s.Integer(1),H])
        cases.append(case)
        print(f"PASS {name}: {case['dimensions']}",flush=True)
    H=q**6+q*p**2
    case=bounded_case("affine_counterexample_baseline",H,
                      [s.Integer(1),q,p,q*p,H,p**2+s.Rational(12,5)*q**5],
                      [s.Integer(1),q,H])
    cases.append(case)
    print(f"PASS affine_counterexample_baseline: {case['dimensions']}",flush=True)
    # Cross-check the separate implementation on mixed, dense polynomials.
    H=h+A*p+(2*q**3+q**2-3*q+7)*p**2
    G=(q+2*p+1)**9+q**2*p**7
    for n in (1,3,5):
        assert contract(sparse(H),sparse(G),n)==sparse(T(H,G,n))
        checks.append(f"independent_contraction_T{n}")
    return cases


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",type=Path)
    args=parser.parse_args()
    symbolic_checks()
    print(f"PASS {len(checks)} symbolic identities",flush=True)
    cases=finite_checks()
    result={"status":"passed","python":platform.python_version(),"sympy":s.__version__,
            "symbolic_checks":checks,"finite_cases":cases,
            "all_degree_proof":"NONLINEAR_B_QUADRATIC_CUBIC.md Sections 2-5",
            "finite_results_are_proof":False,
            "lean_formalization":"formal/SexticC3/NonlinearBClassification.lean",
            "lean_build_checked_by_this_script":False}
    if args.output:
        args.output.write_text(json.dumps(result,indent=2)+"\n")
    print(f"PASS: {len(checks)} identities and {len(cases)} exact finite regressions",flush=True)


if __name__=="__main__":
    main()
