#!/usr/bin/env python3
"""Exact six-dimensional dynamics and existing observer-closure replay."""
from fractions import Fraction as F
from math import factorial
from pathlib import Path
import importlib.util
import json


def matrix(A,B,e):
    return [[F(x) for x in row] for row in
            [[0,-B,e,0,0,0],[0,0,0,-2*B,e,0],
             [0,-2*A,0,0,-B,2*e],[0,0,0,0,0,0],
             [0,0,0,-4*A,0,0],[0,0,0,0,-2*A,0]]]


def eye(): return [[F(i==j) for j in range(6)] for i in range(6)]
def transpose(M): return list(map(list,zip(*M)))


def product(A,B):
    return [[sum(A[i][k]*B[k][j] for k in range(6)) for j in range(6)]
            for i in range(6)]


def p_add(*ps):
    out={}
    for p in ps:
        for k,v in p.items(): out[k]=out.get(k,F(0))+v
    return {k:v for k,v in out.items() if v}


def p_scale(p,c): return {k:v*c for k,v in p.items() if v*c}


def p_mul(a,b):
    out={}
    for e,c in a.items():
        for f,d in b.items():
            k=tuple(x+y for x,y in zip(e,f))
            out[k]=out.get(k,F(0))+c*d
    return {k:v for k,v in out.items() if v}


def check():
    root=Path(__file__).resolve().parents[2]
    filename=root/'extensions'/'observer'/'observation_closure_reference.py'
    spec=importlib.util.spec_from_file_location('_sector_observer',filename)
    O=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(O)
    basis=[{(0,0,0):F(1)},{(1,0,0):F(1)},{(0,1,0):F(1)},
           {(2,0,0):F(1)},{(1,1,0):F(1)},{(0,2,0):F(1)}]
    fixtures=[]
    for A,B in ((F(1),F(0)),(F(-2),F(3)),(F(2,3),F(-5,2))):
        for e in (F(0),F(1),F(-2,3)):
            M=matrix(A,B,e)
            powers=[eye()]
            for _ in range(5): powers.append(product(M,powers[-1]))
            ranks=[O.rank(x,6) for x in powers[1:]]
            assert ranks==([3,1,0,0,0] if not e else [4,3,2,1,0])
            q_t={(1,0,0):F(1),(0,1,1):-2*A,(0,0,1):-B,(0,0,2):-A*e}
            Q_t={(0,1,0):F(1),(0,0,1):e}
            q_t=p_add(q_t); Q_t=p_add(Q_t)
            flows=[basis[0],q_t,Q_t,p_mul(q_t,q_t),p_mul(q_t,Q_t),p_mul(Q_t,Q_t)]
            for j in range(6):
                exponential={}
                for r in range(5):
                    for i in range(6):
                        for (a,b,_),c in basis[i].items():
                            exponential=p_add(exponential,
                                {(a,b,r):powers[r][i][j]*c/F(factorial(r))})
                assert exponential==flows[j],(A,B,e,j)
            target_dimensions=[]
            for indices in ((1,),(3,),(1,3)):
                target=[[int(j==i) for j in range(6)] for i in indices]
                model={'dimension':6,'actions':{'D':O.strings(transpose(M))},
                       'target':target}
                cert=O.compile_model(model)
                O.check_certificate(cert,model)
                target_dimensions.append(len(cert['basis']))
            assert target_dimensions==([2,3,5] if not e else [3,5,6])
            fixtures.append({'A':str(A),'B':str(B),'epsilon':str(e),
                             'ranks':ranks,'target_dimensions':target_dimensions})
    return {'status':'passed','parameter_fixtures':len(fixtures),
            'closed_flow_basis_checks':6*len(fixtures),
            'observer_certificates_replayed':3*len(fixtures),'fixtures':fixtures}


if __name__=='__main__': print(json.dumps(check(),indent=2))
