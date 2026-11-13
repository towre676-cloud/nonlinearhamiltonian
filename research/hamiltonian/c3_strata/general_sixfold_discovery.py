"""Exact filtered incidence discovery for H=q^6 + lower-degree perturbations.

The general leading-degree theorem is uniform in polynomial degree:
for H_6=q^6 and deg(H-H_6)<=5, the degree-N part of T3(H,G)
is 120 q^3 partial_p^3(G_N). Thus the leading homogeneous component
of every static partner has p-degree <=2.

The determinantal computations below are explicitly finite-window results.
"""
from __future__ import annotations
from itertools import combinations
from math import comb
import json
import sympy as S

Q, P = S.symbols("q p")


def transvectant(f, g, order):
    if type(order) is not int or order < 0:
        raise ValueError("order must be a nonnegative integer")
    return S.expand(sum((-1)**j * comb(order, j) *
        S.diff(f, Q, order-j, P, j) * S.diff(g, Q, j, P, order-j)
        for j in range(order+1)))


def sparse_family(terms):
    """Return q^6+sum(c_ij q^i p^j), with i+j<=5."""
    if not isinstance(terms, dict):
        raise ValueError("terms must be a coefficient dictionary")
    h=Q**6
    for exponent, coefficient in terms.items():
        if (not isinstance(exponent, tuple) or len(exponent)!=2
            or any(type(i) is not int for i in exponent)):
            raise ValueError("exponents must be integer pairs")
        i,j=exponent
        if min(i,j)<0 or i+j>5:
            raise ValueError("lower perturbation must have degree <=5")
        c=S.sympify(coefficient)
        if c.has(S.Float):
            raise ValueError("inexact floating point coefficients rejected")
        h+=c*Q**i*P**j
    return S.expand(h)


def input_basis(max_degree):
    if type(max_degree) is not int or max_degree<0:
        raise ValueError("max_degree must be nonnegative")
    return [Q**(d-j)*P**j for d in range(max_degree+1) for j in range(d+1)]


def observation_matrix(h, max_degree, depth):
    """Untruncated coefficient matrix [C;CD;...;CD^depth].

    C=(T3,T5) and D=T1; each output monomial and gate channel receives a
    separate row. Basis elements are all monomials of total degree <=max_degree.
    """
    if type(depth) is not int or depth<0:
        raise ValueError("depth must be nonnegative")
    basis=input_basis(max_degree)
    evolved=list(basis)
    rows,labels=[],[]
    for iterate in range(depth+1):
        for order in (3,5):
            images=[transvectant(h,f,order) for f in evolved]
            monomials=sorted(set().union(*(S.Poly(z,Q,P).monoms() for z in images)))
            for exponents in monomials:
                row=[S.Poly(z,Q,P).coeff_monomial(exponents) for z in images]
                if any(row):
                    rows.append(row)
                    labels.append((iterate,order,exponents))
        if iterate<depth:
            evolved=[transvectant(h,f,1) for f in evolved]
    return {"matrix":S.Matrix(rows) if rows else S.zeros(0,len(basis)),
            "basis":basis,"row_labels":labels,"input_degree":max_degree,"depth":depth}


def specialized_rank(report, parameters, values):
    if len(parameters)!=len(values):
        raise ValueError("parameter/value arity mismatch")
    subs=dict(zip(parameters,[S.Rational(x) for x in values]))
    mat=report["matrix"].subs(subs)
    rank=mat.rank()
    return {"parameter_values":[str(subs[t]) for t in parameters],
            "rank":rank,"kernel_dimension":mat.cols-rank,
            "kernel_basis":[[str(c) for c in v] for v in mat.nullspace()]}


def rank_drop_ideal(report, parameters, target_rank, max_minors=20000):
    """Full exact ideal for rank <= target_rank, never a partial-minor guess."""
    matrix=report["matrix"]
    params=tuple(parameters)
    if not params or any(not isinstance(t,S.Symbol) for t in params):
        raise ValueError("symbolic parameters required")
    if type(target_rank) is not int or target_rank<0:
        raise ValueError("target_rank must be nonnegative")
    if type(max_minors) is not int or max_minors<1:
        raise ValueError("max_minors must be positive")
    k=target_rank+1
    if k>min(matrix.rows,matrix.cols):
        return {"status":"whole_parameter_space","minors":0,
                "target_rank":target_rank,"groebner_basis":[]}
    required=comb(matrix.rows,k)*comb(matrix.cols,k)
    if required>max_minors:
        raise ValueError(f"exact locus requires {required} minors; budget {max_minors}; no partial result")
    generators=[]
    for rr in combinations(range(matrix.rows),k):
        for cc in combinations(range(matrix.cols),k):
            determinant=S.factor(matrix.extract(rr,cc).det(method="berkowitz"))
            if determinant:
                poly=S.Poly(determinant,*params,domain=S.QQ).clear_denoms(convert=True)[1]
                generators.append(poly.primitive()[1].as_expr())
    if not generators:
        return {"status":"whole_parameter_space","minors":required,
                "target_rank":target_rank,"groebner_basis":[]}
    gb=S.groebner(generators,*params,order="lex",domain=S.QQ)
    return {"status":"exact_determinantal_locus","target_rank":target_rank,
            "minors":required,"nonzero_minors":len(generators),
            "groebner_basis":[str(S.factor(v.as_expr())) for v in gb.polys],
            "scope":"Exact for the supplied finite input degree and refinement depth only."}


def uniform_leading_obstruction():
    return {"leading_form":"q^6",
            "degree_N_part_of_T3":"120*q^3*partial_p^3(G_N)",
            "result":"p_degree(G_N)<=2 for every nonzero static partner",
            "scope":"all finite degrees; any lower perturbation of total degree <=5"}


def discovery_example():
    a,b=S.symbols("a b")
    h=sparse_family({(0,3):a,(1,2):b})
    first=observation_matrix(h,2,1)
    second=observation_matrix(h,2,2)
    points=[(0,0),(1,0),(0,1),(1,1)]
    return {"schema":"nonlinearhamiltonian/general-sixfold-incidence/1",
            "family":str(h),"input_degree":2,
            "depth_1_rank_leq_3":rank_drop_ideal(first,(a,b),3,max_minors=1000),
            "specializations":[{"a":x,"b":y,
               "S1_dimension":specialized_rank(first,(a,b),(x,y))["kernel_dimension"],
               "S2_dimension":specialized_rank(second,(a,b),(x,y))["kernel_dimension"]}
               for x,y in points],
            "uniform_leading_obstruction":uniform_leading_obstruction(),
            "scope":"Bounded incidence only; not a complete classification of arbitrary lower perturbations."}


if __name__=="__main__":
    print(json.dumps(discovery_example(),indent=2,sort_keys=True))
