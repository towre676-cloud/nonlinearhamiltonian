#!/usr/bin/env python3
"""Exact bounded discovery for H=q^6+lambda*p^3.

The family lies in the non-affine sixfold-leading stratum. We use two
independent engines: the maintained defining star-exponential implementation
and PerfectJet's odd transvectant kernel tower. The computations below are
bounded in polynomial degree and do not prove an all-degree theorem.
"""
from __future__ import annotations
import importlib.util
import json
from pathlib import Path

from perfectjet.kernel_tower import polynomial_kernel_tower
from perfectjet.polynomial import Poly
from perfectjet.transvectants import transvectant

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("independent_moyal",ROOT/"independent"/"engine.py")
E=importlib.util.module_from_spec(spec)
spec.loader.exec_module(E)


def polynomial_basis(max_degree):
    return [Poly({(d-j,j):1}) for d in range(max_degree+1) for j in range(d+1)]


def independent_dimensions(max_degree,depth,parameter):
    h={(6,0):1,(0,3):parameter}
    basis=[E.monomial(d-j,j) for d in range(max_degree+1) for j in range(d+1)]
    n=len(basis);rows=[];out=[]
    for _ in range(depth+1):
        images=[E.defects(h,g) for g in basis]
        keys=sorted({(k,a,b) for image in images for k,poly in image.items() for a,b in poly})
        rows.extend([[image.get(k,{}).get((a,b),0) for image in images] for k,a,b in keys])
        out.append(len(E.nullspace(rows,n)))
        basis=[E.poisson(h,g) for g in basis]
    return out


def discover(max_degree=9,depth=2):
    q,p=Poly.variable(0),Poly.variable(1)
    basis=polynomial_basis(max_degree)
    results=[]
    for lam in (1,2,-3):
        h=q**6+lam*p**3
        report=polynomial_kernel_tower(
            basis,lambda g:transvectant(h,g,1),
            [lambda g:transvectant(h,g,3),lambda g:transvectant(h,g,5)],
            max_depth=depth)
        dims=[x["kernel_dimension"] for x in report["history"]]
        if len(dims)<depth+1: dims += [0]*(depth+1-len(dims))
        independent=independent_dimensions(max_degree,depth,lam)
        if dims!=independent:
            raise AssertionError(("independent engine disagreement",lam,dims,independent))
        results.append({"lambda":lam,"kernel_dimensions":dims,
                        "independent_star_expansion_agrees":True})
    return {"schema":"nonlinearhamiltonian/sixfold-cubic-perturbation/1",
            "family":"q^6+lambda*p^3","degree_bound":max_degree,
            "depth_bound":depth,"results":results,
            "candidate_core_generators":["1","q^6+lambda*p^3"],
            "status":"bounded exact cross-check, all-degree classification not established",
            "proof_boundary":"No claim of stabilization beyond depth or degree bounds."}


if __name__=="__main__":
    print(json.dumps(discover(),indent=2,sort_keys=True))
