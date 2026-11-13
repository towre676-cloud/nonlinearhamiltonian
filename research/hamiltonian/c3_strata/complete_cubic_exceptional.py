"""Complete all-degree cubic-perturbation exceptional-variety theorem.

This independently replays exact minor identities on the 15-dimensional
*global* polynomial static space, not a truncated degree search.

H = q^6 + u*q^3 + v*q^2*p + w*q*p^2 + x*p^3, x != 0.

S1 has dimension 4 exactly if 3*x*v-w^2=0, otherwise dimension 3.
S2 = D_infinity = span(1,H) for all parameters with x != 0.

The proof combines a canonical shear with three exact minors. Matrix row
indices are zero-based and fixed by cubic_static_recurrence._matrix_for_iterate.
"""
from __future__ import annotations

import json
from pathlib import Path
import sympy as S

from cubic_static_recurrence import (
    static_basis, hamiltonian, iterate_gate_matrix, stage_dimensions
)
from general_sixfold_discovery import Q, P, transvectant

FIRST_11_ROWS = [9,10,12,13,14,15,16,17,18,19,20]
FIRST_12_ROWS = [0,1,2,3,4,9,10,12,13,14,15,16]
SECOND_13_ROWS = [9,10,12,13,14,15,16,17,18,19,20,45,51]

FIRST_11_DET = S.Integer(-18886784506215213600737640604237824000000000000)
FIRST_12_DET = S.Integer(16899153589846893438848121333350400000000)
SECOND_13_DET = S.Integer(-25378036356152937765773242368902013596467200000000000000)


def _exact_minor(matrix, rows, columns, expected):
    result = S.factor(matrix.extract(rows, columns).det(method="domain-ge"))
    if S.cancel(result-expected) != 0:
        raise ArithmeticError(f"Exact determinant identity failed: {result}, expected {expected}")
    return {"matrix_shape": list(matrix.shape),
            "zero_based_rows": list(rows), "zero_based_columns": list(columns),
            "determinant": str(S.factor(result))}


def shear_identity():
    u,v,w,x = S.symbols("u v w x")
    H = hamiltonian(u,v,w,x)
    r = S.symbols("r")
    # r = p + (w/3x)q; p = r - (w/3x)q.
    transformed = S.expand(H.subs(P, r-w*Q/(3*x)))
    u0 = u-v*w/(3*x)+2*w**3/(27*x**2)
    v0 = v-w**2/(3*x)
    normalized = Q**6+u0*Q**3+v0*Q**2*r+x*r**3
    if S.cancel(transformed-normalized) != 0:
        raise ArithmeticError("Symplectic shear did not reconstruct the Hamiltonian")
    return {"canonical_shear": "r=p+w*q/(3*x)",
            "new_u": str(u0), "new_v": str(v0),
            "poisson_determinant": "1",
            "exceptional_condition": "3*v*x-w**2=0"}


def exact_rank_certificate():
    u,v,x = S.symbols("u v x")
    H = hamiltonian(u,v,0,x)
    basis = static_basis(u,v,0,x,check=True)
    if len(basis)!=15 or max(S.Poly(z,Q,P).total_degree() for z in basis)!=9:
        raise ArithmeticError("15-dimensional static basis or total degree bound failed")
    first = iterate_gate_matrix(H,basis,1)
    both = first.col_join(iterate_gate_matrix(H,basis,2))
    first11cols=[i for i in range(15) if i not in (3,12,13,14)]
    first12cols=[i for i in range(15) if i not in (3,12,13)]
    second13cols=[i for i in range(15) if i not in (3,12)]
    witnesses=[
      _exact_minor(first,FIRST_11_ROWS,first11cols,FIRST_11_DET*x**11),
      _exact_minor(first,FIRST_12_ROWS,first12cols,FIRST_12_DET*v**5*x**12),
      _exact_minor(both,SECOND_13_ROWS,second13cols,SECOND_13_DET*x**15),
    ]
    # Static space: the generator corresponding to p^3 carries the q^6
    # and u*q^3 corrections; H=x*B[3]+v*B[11].
    if S.expand(H-x*basis[3]-v*basis[11]) != 0:
        raise ArithmeticError("Hamiltonian coordinates in static basis failed")
    if (S.expand(basis[12]-1)!=0 or S.expand(basis[13]-Q)!=0 or
            S.expand(basis[14]-Q**2)!=0):
        raise ArithmeticError("Expected static coordinates missing")
    # All parameter values: 1, q, H lie in the first refinement.
    for f in (S.Integer(1),Q,H):
        if transvectant(H,f,3)!=0 or transvectant(H,f,5)!=0:
            raise ArithmeticError("Static universal survivor failed")
        d=transvectant(H,f,1)
        if transvectant(H,d,3)!=0 or transvectant(H,d,5)!=0:
            raise ArithmeticError("First universal survivor failed")
    # The only extra S1 direction on v=0 is q^2.
    q2defect=S.factor(transvectant(H,transvectant(H,Q**2,1),3))
    if S.cancel(q2defect-144*v*x)!=0:
        raise ArithmeticError("Exceptional q^2 obstruction is wrong")
    if transvectant(H,transvectant(H,Q**2,1),5)!=0:
        raise ArithmeticError("Unexpected fifth-order q^2 obstruction")
    # In all cases 1,H are invariant under D and survive forever.
    if transvectant(H,S.Integer(1),1)!=0 or transvectant(H,H,1)!=0:
        raise ArithmeticError("Claimed invariant core is not Poisson-invariant")
    return {
      "schema": "nonlinearhamiltonian/complete-cubic-exceptional-variety/1",
      "normalized_family": "q^6+u*q^3+v*q^2*p+x*p^3",
      "assumption": "x != 0 over characteristic zero",
      "static_dimension_all_degrees":15,
      "static_max_total_degree":9,
      "first_refinement_rank_minor_certificates":witnesses[:2],
      "second_refinement_rank_minor_certificate":witnesses[2],
      "q_squared_first_refinement_defect_T3":str(q2defect),
      "first_refinement_if_v_nonzero": ["1","q","H"],
      "first_refinement_if_v_zero": ["1","q","q**2","H"],
      "second_refinement_all_parameters": ["1","H"],
      "shear":shear_identity(),
      "full_family_exceptional_hypersurface": "3*x*v-w**2=0",
      "proof_boundary": "Global because the exact static PDE restricts all polynomial partners to 15 dimensions; determinant witnesses cover all coefficients x!=0; not Lean-formalized."
    }


def independent_point_replays():
    points=[(0,0,0,1),(0,1,0,1),(0,0,1,1),(0,1,1,1),(1,3,3,1),(2,-3,0,1)]
    rows=[]
    for u,v,w,x in points:
        dimensions=stage_dimensions(u,v,w,x,depth=2)
        exceptional=(3*x*v-w*w)==0
        expected=[15,4 if exceptional else 3,2]
        if dimensions!=expected:
            raise ArithmeticError(f"Pointwise rank disagreeing with theorem: {u,v,w,x}: {dimensions}")
        rows.append({"parameters":[u,v,w,x],"exceptional":exceptional,
                     "kernel_dimensions":dimensions})
    return rows


def receipt():
    report=exact_rank_certificate()
    report["independent_point_replays"]=independent_point_replays()
    return report


if __name__=="__main__":
    print(json.dumps(receipt(),sort_keys=True,indent=2))
