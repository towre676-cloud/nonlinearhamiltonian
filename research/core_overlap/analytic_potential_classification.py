#!/usr/bin/env python3
"""Exact coefficient checks for cubic-preserving analytic potentials.

Only the Python standard library is required. Coefficients are polynomials
in formal parameters over Fraction; q degrees and rational p exponents are
stored sparsely. No numerical special-function evaluations or sampled
parameter substitutions are used for the generic identities.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as F
import json
from math import comb
from pathlib import Path


PARAMETERS = ("a", "b", "c", "c0", "f_a", "f_b", "n")
ZERO_PARAMETERS = (0,) * len(PARAMETERS)


def clean(poly):
    return {key: value for key, value in poly.items() if value}


def monomial(q_degree=0, p_exponent=0, coefficient=1, parameters=None):
    """Construct a sparse monomial with named formal parameter powers."""
    if q_degree < 0 or int(q_degree) != q_degree:
        raise ValueError("q_degree must be a nonnegative integer")
    powers = list(ZERO_PARAMETERS)
    for name, exponent in (parameters or {}).items():
        if exponent < 0 or int(exponent) != exponent:
            raise ValueError("parameter exponents must be nonnegative integers")
        powers[PARAMETERS.index(name)] = exponent
    return clean({(int(q_degree), F(p_exponent), tuple(powers)): F(coefficient)})


def parameter(name):
    return monomial(parameters={name: 1})


def add(*polys):
    result = {}
    for poly in polys:
        for key, value in poly.items():
            result[key] = result.get(key, F(0)) + value
    return clean(result)


def scale(poly, coefficient):
    return clean({key: value * F(coefficient) for key, value in poly.items()})


def multiply(left, right):
    result = {}
    for (i, p, a), x in left.items():
        for (j, r, b), y in right.items():
            key = (i + j, p + r, tuple(u + v for u, v in zip(a, b)))
            result[key] = result.get(key, F(0)) + x * y
    return clean(result)


def power(poly, exponent):
    if exponent < 0 or int(exponent) != exponent:
        raise ValueError("power requires a nonnegative integer")
    result = monomial()
    for _ in range(exponent):
        result = multiply(result, poly)
    return result


def falling(value, count):
    result = F(1)
    for k in range(count):
        result *= value - k
    return result


def differentiate(poly, q_order=0, p_order=0):
    if min(q_order, p_order) < 0:
        raise ValueError("derivative orders must be nonnegative")
    result = {}
    for (q, p, params), coefficient in poly.items():
        multiplier = falling(q, q_order) * falling(p, p_order)
        if multiplier:
            result[(q - q_order, p - p_order, params)] = coefficient * multiplier
    return clean(result)


def transvectant(left, right, order):
    """Direct mixed derivative definition, with T1 equal to {left,right}."""
    return add(*(scale(multiply(differentiate(left, order - k, k),
                                differentiate(right, k, order - k)),
                       (-1) ** k * comb(order, k))
                 for k in range(order + 1)))


def q_degree(poly):
    return max((key[0] for key in poly), default=-1)


def potential_euler_operator(potential):
    """The left side of AP7, acting exactly on fractional polynomials."""
    return add(multiply(monomial(0, 4), differentiate(potential, p_order=4)),
               scale(multiply(monomial(0, 3), differentiate(potential, p_order=3)), 3),
               scale(multiply(monomial(0, 2), differentiate(potential, p_order=2)), F(-15, 16)),
               scale(multiply(monomial(0, 1), differentiate(potential, p_order=1)), F(-15, 32)))


def potential_offset_operator(potential):
    """The expression AP9; constant on every compatible potential."""
    return scale(add(multiply(monomial(0, 3), differentiate(potential, p_order=3)),
                     scale(multiply(monomial(0, 1), differentiate(potential, p_order=1)), F(-15, 16)),
                     scale(potential, F(15, 32))), F(32, 15))


def potential_compatibility_from_h(f, potential, g, h, eigenvalue):
    """Return denominator-cleared residuals of the two equations GC1."""
    f2 = differentiate(f, p_order=2)
    h1 = differentiate(h, p_order=1)
    first = add(multiply(f2, h1),
                scale(multiply(g, differentiate(potential, p_order=3)), -1))
    b = add(scale(differentiate(f, p_order=1), 2), eigenvalue)
    second = add(multiply(f, h1), scale(multiply(b, h), -1),
                 scale(multiply(g, differentiate(potential, p_order=1)), -3))
    return first, second


def cleared_potential_operator(f, potential, g, eigenvalue):
    """GC3; no divisions, including for a chart with F or B zeros."""
    f2 = differentiate(f, p_order=2)
    b = add(scale(differentiate(f, p_order=1), 2), eigenvalue)
    m = multiply(b, f2)
    v3 = differentiate(potential, p_order=3)
    z = multiply(g, add(multiply(f, v3),
                        scale(multiply(f2, differentiate(potential, p_order=1)), -3)))
    return add(multiply(m, differentiate(z, p_order=1)),
               scale(multiply(differentiate(m, p_order=1), z), -1),
               scale(multiply(multiply(multiply(power(b, 2), f2), g), v3), -1))


def run():
    checks = []

    def identity(name, left, right=None):
        right = right or {}
        delta = add(left, scale(right, -1))
        if delta:
            raise AssertionError(f"{name}: {delta!r}")
        checks.append({"name": name, "left_terms": len(left),
                       "right_terms": len(right), "all_coefficients_zero": True})

    q = monomial(1)
    f = monomial(0, F(-1, 4))
    g = monomial(0, F(-3, 4))
    v = add(parameter("c0"), multiply(parameter("a"), f),
            multiply(parameter("b"), monomial(0, F(3, 4))),
            multiply(parameter("c"), monomial(0, F(5, 2))))
    hamiltonian = add(multiply(q, f), v)
    shifted = add(hamiltonian, scale(parameter("c0"), -1))
    cube = power(shifted, 3)
    h = scale(add(multiply(parameter("a"), monomial(0, F(-3, 4))),
                  multiply(parameter("b"), monomial(0, F(1, 4))),
                  multiply(parameter("c"), monomial(0, 2))), 3)
    candidate = add(multiply(power(q, 3), g), multiply(power(q, 2), h))

    identity("generic_shifted_cube_stationary", transvectant(hamiltonian, cube, 1))
    for order in (3, 5, 7, 9):
        identity(f"generic_shifted_cube_T{order}", transvectant(hamiltonian, cube, order))
    identity("generic_cubic_candidate_T3", transvectant(hamiltonian, candidate, 3))
    dg = transvectant(hamiltonian, candidate, 1)
    assert q_degree(dg) <= 1
    assert q_degree(add(cube, scale(candidate, -1))) <= 1
    checks.append({"name": "generic_candidate_derivative_and_cube_difference_in_strip",
                   "derivative_q_degree": q_degree(dg), "all_coefficients_checked": True})
    for index, residual in enumerate(potential_compatibility_from_h(f, v, g, h, {})):
        identity(f"generic_compatibility_equation_{index + 1}", residual)
    identity("generic_potential_Euler_equation", potential_euler_operator(v))
    identity("generic_constant_offset_recovered", potential_offset_operator(v), parameter("c0"))
    identity("generic_h_reconstruction",
             h,
             add(scale(multiply(monomial(0, F(1, 2)), differentiate(v, p_order=1)), 6),
                 scale(multiply(monomial(0, F(5, 2)), differentiate(v, p_order=3)), F(-32, 5))))
    identity("generic_cleared_compatibility_operator", cleared_potential_operator(f, v, g, {}))

    # Formal indicial variable: the following proves the factorization for
    # every degree, rather than checking a list of exponents.
    n = parameter("n")

    def linear(constant, coefficient=1):
        return add(scale(n, coefficient), monomial(coefficient=constant))

    ff2 = multiply(n, linear(-1))
    ff3 = multiply(ff2, linear(-2))
    ff4 = multiply(ff3, linear(-3))
    indicial = add(ff4, scale(ff3, 3), scale(ff2, F(-15, 16)), scale(n, F(-15, 32)))
    factored = scale(multiply(multiply(multiply(n, linear(1, 4)), linear(-3, 4)), linear(-5, 2)), F(1, 32))
    identity("formal_indicial_factorization", indicial, factored)
    coefficients = {key[2][-1]: value for key, value in indicial.items()}
    assert coefficients == {4: F(1), 3: F(-3), 2: F(17, 16), 1: F(15, 32)}

    # Active F has two formal coefficients, and sector n remains formal.
    active_f = add(multiply(parameter("f_a"), f),
                   multiply(parameter("f_b"), monomial(0, 1)))
    active_f1 = differentiate(active_f, p_order=1)
    active_f2 = differentiate(active_f, p_order=2)
    active_f3 = differentiate(active_f, p_order=3)
    kn = add(scale(multiply(multiply(parameter("f_a"), linear(-3)),
                            monomial(0, F(-5, 4))), F(-1, 2)),
             scale(multiply(parameter("f_b"), linear(-6, 7)), F(-1, 4)))
    identity("all_sector_degrees_active_Kn_identity",
             scale(multiply(active_f2, kn), 3),
             add(multiply(linear(-2), multiply(active_f, active_f3)),
                 scale(multiply(n, multiply(active_f1, active_f2)), -3)))
    eigenvalue = scale(parameter("f_b"), F(-15, 4))
    identity("active_cubic_coefficient_eigenidentity",
             add(multiply(active_f, differentiate(g, p_order=1)),
                 scale(multiply(active_f1, g), -3)), multiply(eigenvalue, g))
    active_v = add(multiply(parameter("a"), active_f), parameter("c0"))
    active_h = scale(multiply(parameter("a"), g), 3)
    active_hamiltonian = add(multiply(q, active_f), active_v)
    active_cubic = multiply(power(add(q, parameter("a")), 3), g)
    identity("active_translated_cubic_eigenidentity",
             transvectant(active_hamiltonian, active_cubic, 1), multiply(eigenvalue, active_cubic))
    identity("active_translated_cubic_T3", transvectant(active_hamiltonian, active_cubic, 3))
    for index, residual in enumerate(potential_compatibility_from_h(active_f, active_v, g, active_h, eigenvalue)):
        identity(f"active_translated_compatibility_{index + 1}", residual)
    identity("active_translated_cleared_ODE",
             cleared_potential_operator(active_f, active_v, g, eigenvalue))

    # A rejected potential and the sharp depth-two example are checked by
    # direct mixed differentiation, independently of the Euler operator.
    rejected = monomial(0, F(7, 4))
    identity("rejected_potential_Euler_residual", potential_euler_operator(rejected),
             monomial(0, F(7, 4), F(-21, 8)))
    bad_hamiltonian = add(multiply(q, f), rejected)
    bad_candidate = add(monomial(3, F(-3, 4)), monomial(2, F(5, 4), F(-21, 25)))
    first_d = transvectant(bad_hamiltonian, bad_candidate, 1)
    second_d = transvectant(bad_hamiltonian, first_d, 1)
    identity("rejected_depth_two_initial_C3", transvectant(bad_hamiltonian, bad_candidate, 3))
    identity("rejected_depth_two_initial_C5", transvectant(bad_hamiltonian, bad_candidate, 5))
    identity("rejected_depth_two_first_C3", transvectant(bad_hamiltonian, first_d, 3))
    identity("rejected_depth_two_second_C3_nonzero",
             transvectant(bad_hamiltonian, second_d, 3), monomial(0, F(-9, 2), F(63, 8)))

    # Explicitly expose the constant-shift pitfall: generic unshifted H^3
    # is not silently accepted as a replacement for (H-c0)^3.
    unshifted_gate = transvectant(hamiltonian, power(hamiltonian, 3), 3)
    identity("unshifted_cube_constant_offset_gate_formula", unshifted_gate,
             scale(multiply(parameter("c0"), monomial(0, F(-15, 4))), F(-45, 16)))
    assert unshifted_gate
    checks.append({"name": "unshifted_cube_rejected_with_formal_constant_offset",
                   "nonzero_gate_terms": len(unshifted_gate), "passed": True})

    return {"format": "analytic-cubic-potential-classification-v1", "passed": True,
            "arithmetic": "rational coefficients; fractional p powers; formal coefficient parameters",
            "formal_parameters": list(PARAMETERS), "checks": checks,
            "check_count": len(checks),
            "compatible_potential_exponents": ["0", "-1/4", "3/4", "5/2"],
            "generic_shifted_cube_term_count": len(cube),
            "all_degree_proof": "analytic_potential_classification.md, Theorem AP",
            "active_extension_scope": "GC1 globally; four-dimensional potential space on regular charts only",
            "historical_priority": "unassessed"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="optional path for the exact JSON receipt")
    args = parser.parse_args()
    encoded = json.dumps(run(), indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(encoded, encoding="utf-8")
    print(encoded)


if __name__ == "__main__":
    main()
