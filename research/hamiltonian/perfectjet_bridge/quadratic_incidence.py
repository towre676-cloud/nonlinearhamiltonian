#!/usr/bin/env python3
"""Two-parameter quadratic dynamical rank-locus discovery.

H(a,b)=q^6+p^6+a*q^3*p^3+b*(q^4*p^2+q^2*p^4).

The optional --full-minors mode computes every maximal minor of the bounded
quadratic observation matrices and its rational Groebner basis using SymPy.
Default mode independently evaluates the proposed exceptional points with
PerfectJet's exact polynomial kernel tower. The full-minor computation is
optional because it is substantially more expensive than point replay.
"""
from __future__ import annotations
import argparse
import json
from perfectjet.kernel_tower import polynomial_kernel_tower
from perfectjet.polynomial import Poly
from perfectjet.transvectants import transvectant


def family(a,b):
    q,p=Poly.variable(0),Poly.variable(1)
    return q**6+p**6+a*q**3*p**3+b*(q**4*p**2+q**2*p**4)


def replay(a,b,depth=2):
    q,p=Poly.variable(0),Poly.variable(1)
    H=family(a,b)
    basis=[q**2,q*p,p**2]
    report=polynomial_kernel_tower(
        basis,lambda g:transvectant(H,g,1),
        [lambda g:transvectant(H,g,3),lambda g:transvectant(H,g,5)],
        max_depth=depth)
    dims=[row["kernel_dimension"] for row in report["history"]]
    return dims+[0]*(depth+1-len(dims))


def bounded_points():
    points=[(0,3),(16,-9),(-16,-9),(0,-9),(0,0),(1,0)]
    return [{"a":a,"b":b,"dimensions":replay(a,b)} for a,b in points]


def full_minor_ideals():
    import sympy as sp
    from itertools import combinations
    from math import comb
    q,p,a,b=sp.symbols("q p a b")
    H=q**6+p**6+a*q**3*p**3+b*(q**4*p**2+q**2*p**4)
    def T(F,G,r):
        return sp.expand(sum(
            (-1)**i*comb(r,i)*sp.diff(F,q,r-i,p,i)*sp.diff(G,q,i,p,r-i)
            for i in range(r+1)))
    basis=[q**2,q*p,p**2]
    evolved=basis[:]
    rows=[]
    ideals=[]
    for depth in range(3):
        for r in (3,5):
            images=[T(H,g,r) for g in evolved]
            monomials=set().union(*(set(sp.Poly(z,q,p).monoms()) for z in images))
            for exponents in sorted(monomials):
                row=[sp.Poly(z,q,p).coeff_monomial(exponents) for z in images]
                if any(row):
                    rows.append(row)
        if rows:
            M=sp.Matrix(rows)
            generators=[]
            for indices in combinations(range(M.rows),3):
                determinant=sp.expand(M[list(indices),:].det())
                if determinant:
                    generators.append(sp.Poly(determinant,a,b).primitive()[1].as_expr())
            gb=sp.groebner(generators,a,b,order="lex")
            ideals.append({"depth":depth,"rows":len(rows),
                           "nonzero_maximal_minors":len(generators),
                           "groebner_basis":[str(sp.factor(z.as_expr())) for z in gb.polys]})
        else:
            ideals.append({"depth":depth,"rows":0,"groebner_basis":[]})
        evolved=[T(H,g,1) for g in evolved]
    return ideals


def receipt(full=False):
    result={"schema":"nonlinearhamiltonian/quadratic-dynamical-incidence/1",
            "family":"q^6+p^6+a*q^3*p^3+b*(q^4*p^2+q^2*p^4)",
            "domain":"homogeneous quadratic partners",
            "points":bounded_points(),
            "candidate_first_refinement_locus":["(0,3)","(16,-9)","(-16,-9)"],
            "candidate_second_refinement_locus":["(0,3)"],
            "status":"exact point replay; full minor ideal is optional"}
    if full:
        result["maximal_minor_ideals"]=full_minor_ideals()
        result["status"]="full exact maximal-minor Groebner computation plus point replay"
    return result


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--full-minors",action="store_true")
    args=parser.parse_args()
    print(json.dumps(receipt(args.full_minors),indent=2,sort_keys=True))
