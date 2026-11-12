#!/usr/bin/env python3
"""Cross-check nonlinearhamiltonian refinement kernels with PerfectJet.

This bridge is intentionally read-only with respect to the maintained
classifier. nonlinearhamiltonian's stdlib sparse Weyl--Moyal engine remains
one implementation; PerfectJet supplies a second transvectant/kernel-tower
implementation and the parametric constructible-rank machinery.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
HAM = HERE.parent
ENGINE = HAM / "independent" / "engine.py"

_spec = importlib.util.spec_from_file_location("_nh_independent_engine", ENGINE)
E = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(E)

from perfectjet.kernel_tower import polynomial_kernel_tower
from perfectjet.parametric_kernel_tower import parametric_kernel_tower, replay_point
from perfectjet.polynomial import Poly
from perfectjet.transvectants import transvectant


def to_poly(poly):
    return Poly({tuple(k): F(v) for k, v in poly.items()})


def monomial_basis(degree):
    return [E.monomial(degree-j, j) for j in range(degree+1)]


def _independent_defect_rows(H, evolved):
    images = [E.defects(H, g) for g in evolved]
    keys = sorted({(hbar, a, b) for image in images
                   for hbar, polynomial in image.items()
                   for a, b in polynomial})
    return [[image.get(hbar, {}).get((a, b), F(0)) for image in images]
            for hbar, a, b in keys]


def independent_kernel_dimensions(H, degree, max_depth):
    evolved = monomial_basis(degree)
    cumulative = []
    dims = []
    for _ in range(max_depth+1):
        cumulative += _independent_defect_rows(H, evolved)
        dims.append(len(E.nullspace(cumulative, degree+1)))
        evolved = [E.poisson(H, g) for g in evolved]
    return dims


def perfectjet_kernel_dimensions(H, degree, max_depth):
    hp = to_poly(H)
    basis = [Poly({(degree-j, j): 1}) for j in range(degree+1)]
    report = polynomial_kernel_tower(
        basis,
        evolution=lambda g: transvectant(hp, g, 1),
        constraints=[lambda g: transvectant(hp, g, 3),
                     lambda g: transvectant(hp, g, 5)],
        max_depth=max_depth)
    return [row["kernel_dimension"] for row in report["history"]]


def product(*polys):
    out = E.monomial(0, 0)
    for poly in polys:
        out = E.multiply(out, poly)
    return out


def representatives():
    q, p = E.monomial(1, 0), E.monomial(0, 1)
    return {
        "6": E.power(q, 6),
        "5,1": E.multiply(E.power(q, 5), p),
        "4,2": E.multiply(E.power(q, 4), E.power(p, 2)),
        "4,1,1": E.add(E.multiply(E.power(q, 4), E.power(p, 2)), E.power(q, 6)),
        "3,3": E.multiply(E.power(q, 3), E.power(p, 3)),
        "3,2,1": product(E.power(q, 3), E.power(p, 2), E.add(p, E.scale(q, -1))),
        "3,1,1,1": product(E.power(q, 3), p, E.add(p, E.scale(q, -1)), E.add(p, E.scale(q, -2))),
        "2,2,2": product(E.power(q, 2), E.power(p, 2), E.power(E.add(p, E.scale(q, -1)), 2)),
        "2,2,1,1": product(E.power(q, 2), E.power(p, 2),
                           E.add(p, E.scale(q, -1)), E.add(p, E.scale(q, -2))),
        "2,1,1,1,1": product(E.power(q, 2), p,
                             E.add(p, E.scale(q, -1)), E.add(p, E.scale(q, -2)),
                             E.add(p, E.scale(q, -3))),
        "1,1,1,1,1,1": product(q, p,
                               E.add(p, E.scale(q, -1)), E.add(p, E.scale(q, -2)),
                               E.add(p, E.scale(q, -3)), E.add(p, E.scale(q, -4))),
    }


def cross_check(max_degree=10, max_depth=2):
    rows = []
    for stratum, H in representatives().items():
        for degree in range(max_degree+1):
            left = independent_kernel_dimensions(H, degree, max_depth)
            right = perfectjet_kernel_dimensions(H, degree, max_depth)
            if left != right:
                raise AssertionError((stratum, degree, left, right))
            rows.append({"stratum": stratum, "degree": degree,
                         "kernel_dimensions": left})
    return rows


def exceptional_family_report():
    q, p = Poly.variable(0), Poly.variable(1)
    basis = [q**2, q*p, p**2]

    def family(delta):
        return q**4*p**2 + delta*q**6

    def evolution(h):
        return lambda g: transvectant(h, g, 1)

    def constraints(h):
        return [lambda g: transvectant(h, g, 3),
                lambda g: transvectant(h, g, 5)]

    report = parametric_kernel_tower(
        family, basis, evolution, constraints,
        nvars=1, parameter_degree=3, max_depth=2, names=["delta"])
    boundary = replay_point(report, [0], family, basis, evolution, constraints)
    generic = replay_point(report, [1], family, basis, evolution, constraints)
    if [r["direct_kernel_dimension"] for r in boundary["depths"]] != [3, 1, 1]:
        raise AssertionError("delta=0 boundary replay changed")
    if [r["direct_kernel_dimension"] for r in generic["depths"]] != [3, 1, 0]:
        raise AssertionError("delta=1 exceptional replay changed")
    return {"rank_cells": report, "boundary_delta_0": boundary, "generic_delta_1": generic}


def receipt(max_degree=10, max_depth=2):
    rows = cross_check(max_degree, max_depth)
    return {
        "schema": "nonlinearhamiltonian/perfectjet-kernel-bridge/1",
        "perfectjet_role": "independent exact transvectant/kernel and parametric rank-cell engine",
        "nonlinearhamiltonian_role": "maintained stdlib Weyl--Moyal implementation and classification theorems",
        "cross_checks": {
            "strata": 11,
            "degrees": [0, max_degree],
            "depths": [0, max_depth],
            "cases": len(rows),
            "all_equal": True,
            "rows": rows,
        },
        "exceptional_family": exceptional_family_report(),
        "proof_boundary": [
            "The cross-check is finite in degree/depth and does not replace the all-degree stratum proofs.",
            "PerfectJet interpolation uses the explicitly justified degree-3 bound for depth two in the affine delta family.",
            "No Lean formalization is claimed by this bridge.",
        ],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-degree", type=int, default=10)
    parser.add_argument("--max-depth", type=int, default=2)
    parser.add_argument("--output")
    args = parser.parse_args()
    data = receipt(args.max_degree, args.max_depth)
    text = json.dumps(data, indent=2, sort_keys=True)
    if args.output:
        Path(args.output).write_text(text + "\n")
    else:
        print(text)


if __name__ == "__main__":
    main()
