#!/usr/bin/env python3
"""Independent exact all-degree certificate for H=q^6+lambda*p^3.

Uses SymPy solely for exact symbolic differentiation, coefficient matrices,
and determinant factorization. No polynomial degree cutoff is imposed.
"""
from __future__ import annotations
import json
from math import comb
from pathlib import Path
import sympy as s

q,p,l=s.symbols("q p lambda")
H=q**6+l*p**3
B=[
 s.Integer(1),q,q**2,p,q*p,q**2*p,p**2,q*p**2,q**2*p**2,
 p**3+q**6/l,
 q*p**3+s.Rational(4,7)*q**7/l,
 q**2*p**3+s.Rational(5,14)*q**8/l,
 p**4+4*q**6*p/l,
 q*p**4+s.Rational(16,7)*q**7*p/l,
 q**2*p**4+s.Rational(10,7)*q**8*p/l,
]

def T(F,G,k):
    return s.expand(sum((-1)**j*comb(k,j)*
        s.diff(F,q,k-j,p,j)*s.diff(G,q,j,p,k-j) for j in range(k+1)))

def D(G):
    return T(H,G,1)

def gate_matrix(basis,depth):
    images=[]
    for G in basis:
        for _ in range(depth):
            G=D(G)
        images.append((T(H,G,3),T(H,G,5)))
    keys=[]
    for gate in (3,5):
        mons=set().union(*(set(s.Poly(row[0 if gate==3 else 1],q,p).monoms()) for row in images))
        keys.extend((gate,mon) for mon in sorted(mons))
    M=s.Matrix([[s.Poly(images[j][0 if gate==3 else 1],q,p).coeff_monomial(mon)
                 for j in range(len(basis))] for gate,mon in keys])
    return keys,M

def verify():
    assert all(T(H,G,3)==0 and T(H,G,5)==0 for G in B)
    assert len(B)==15
    keys,M=gate_matrix(B,1)
    complement=[j for j in range(15) if j not in (0,1,2,9)]
    row_monomials=[(2,0),(2,1),(2,3),(3,0),(3,1),(3,2),(3,3),
                   (4,0),(4,1),(4,2),(4,3)]
    indices=[keys.index((3,mon)) for mon in row_monomials]
    determinant=s.factor(M[indices,complement].det())
    expected=2**54*3**38*5**12*11*17**2*l**11
    assert s.simplify(determinant-expected)==0
    assert all(M[:,j]==s.zeros(M.rows,1) for j in (0,1,2,9))
    first=[B[j] for j in (0,1,2,9)]
    keys2,M2=gate_matrix(first,2)
    nonzero=[(keys2[i],j,str(s.factor(M2[i,j])))
             for i in range(M2.rows) for j in range(M2.cols) if M2[i,j]!=0]
    assert nonzero==[
        ((3,(2,1)),1,"12960*lambda**2"),
        ((3,(3,1)),2,"103680*lambda**2")]
    return {
      "schema":"nonlinearhamiltonian/sixfold-cubic-all-degree/1",
      "static_basis_dimension":15,
      "static_basis":[str(s.factor(G)) for G in B],
      "first_refinement_dimension":4,
      "first_refinement_nonzero_minor":str(determinant),
      "first_refinement_minor_rows":[list(x) for x in row_monomials],
      "first_refinement_complement_columns":complement,
      "second_refinement_dimension":2,
      "second_refinement_nonzero_rows":[
          {"gate":gate,"monomial":list(mon),"column":j,"coefficient":value}
          for (gate,mon),j,value in nonzero],
      "invariant_core":["1","q**6+lambda*p**3"],
      "scope":"All polynomial degrees, nonzero rational lambda, exact identities and finite static reduction; not Lean formalized."
    }

if __name__=="__main__":
    print(json.dumps(verify(),indent=2,sort_keys=True))
