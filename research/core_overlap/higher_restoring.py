#!/usr/bin/env python3
"""All-degree nonlinear quadratic-shear compositions with quadratic restoring force.

Proof: higher_restoring.md, Theorem HR. Standard-library exact arithmetic.
Finite matrices retain all output monomials and supplement the written proof.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as F
import json
from pathlib import Path
import random
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import analytic_bridge_check as C


def compose(f, P):
    """Substitute P(q,p) for the second variable of f(q,P)."""
    return C.add(*(C.scale(C.mul(C.mono(i, 0), C.power(P, int(j))), a)
                   for (i, j), a in f.items()))


def make(coefficients, w, lam, epsilon=0, constant=0):
    P = C.add(C.mono(0, 1), w)
    f = C.clean({(0, j): a for j, a in coefficients.items()})
    H = C.add(compose(f, P), C.mono(2, 0, lam),
              C.mono(1, 0, epsilon), C.mono(0, 0, constant))
    return H, P, f


def recognize(H):
    """Recognize HR; return None outside its exact rational input scope."""
    normalized = {}
    try:
        for (i, j), value in H.items():
            if any(isinstance(x, float) for x in (i, j, value)):
                return None
            i, j, value = F(i), F(j), F(value)
            if i < 0 or j < 0 or i.denominator != 1 or j.denominator != 1:
                return None
            if value:
                normalized[int(i), int(j)] = value
    except (TypeError, ValueError, ZeroDivisionError, AttributeError):
        return None
    H = C.clean(normalized)
    m = int(max((j for _, j in H), default=0))
    if m < 3:
        return None
    top = {key: a for key, a in H.items() if key[1] == m}
    if set(top) != {(0, F(m))}:
        return None
    rho = top[0, F(m)]
    w = C.clean({(i, 0): a / (m*rho) for (i, j), a in H.items()
                 if j == m-1 and i})
    if max((i for i, _ in w), default=0) != 2:
        return None
    transformed = compose(H, C.add(C.mono(0, 1), C.scale(w, -1)))
    if any(i and (i, j) not in ((1, 0), (2, 0)) for i, j in transformed):
        return None
    lam = transformed.get((2, F(0)), F(0))
    if not lam:
        return None
    f = C.clean({(0, j): a for (i, j), a in transformed.items() if not i})
    epsilon = transformed.get((1, F(0)), F(0))
    P = C.add(C.mono(0, 1), w)
    assert C.add(compose(f, P), C.mono(2, 0, lam), C.mono(1, 0, epsilon)) == H
    return {'route': 'HR', 'proved': True, 'core': 'span{1,H}',
            'dimension': 2, 'core_dimension': 2, 'active_part': '0',
            'third_gate_depth': 3, 'degree_composition': m,
            'degree_shear': 2, 'c': w[2, F(0)], 'lambda': lam,
            'epsilon': epsilon, 'w': w, 'P': P, 'F': f,
            'basis': [C.mono(0, 0), H],
            'depth_dimensions': {'1': 4, '2': 3, '3': 2},
            'proof': 'higher_restoring.md, Theorem HR'}


classify = recognize


def d_new(g, f, lam, epsilon=0):
    return C.add(C.scale(C.mul(C.derivative(f, np=1), C.derivative(g, nq=1)), -1),
                 C.mul(C.add(C.mono(1, 0, 2*lam), C.mono(0, 0, epsilon)),
                       C.derivative(g, np=1)))


def c3_new(g, f, c=1):
    f2, f3 = C.derivative(f, np=2), C.derivative(f, np=3)
    return C.add(C.scale(C.mul(f3, C.derivative(g, nq=3)), -1),
                 C.scale(C.mul(f2, C.derivative(g, nq=1, np=2)), -6*c),
                 C.scale(C.mul(f3, C.derivative(g, nq=1, np=1)), -6*c))


def finite_kernel(f, c, lam, epsilon, bound, depth):
    basis = [C.mono(i, j) for i in range(bound+1)
             for j in range(bound+1-i)]
    columns = []
    for g in basis:
        values = []
        for _ in range(depth+1):
            values.append(c3_new(g, f, c))
            g = d_new(g, f, lam, epsilon)
        columns.append(values)
    keys = sorted({(step, i, j) for values in columns
                   for step, value in enumerate(values) for i, j in value})
    rows = [[values[step].get((i, j), F(0)) for values in columns]
            for step, i, j in keys]
    dimension = len(basis)-C.rank(rows, len(basis))
    expected = {1: 4, 2: 3, 3: 2}[depth]
    assert dimension == expected, (dimension, expected, bound, depth)
    return {'degree_bound_q_P': bound, 'input_monomials': len(basis),
            'full_output_coordinates': len(keys), 'output_projection': False,
            'third_gate_depth': depth, 'kernel_dimension': dimension}


def run():
    rng = random.Random(20261023)
    counts = {'recognition_acceptances': 0, 'recognition_rejections': 0,
              'direct_original_gate_checks': 0, 'direct_original_derivation_checks': 0,
              'highest_q_coefficient_checks': 0, 'scalar_ode_checks': 0,
              'sharp_depth_checks': 0, 'leading_nonvanishing_checks': 0,
              'independent_pbw_checks': 0}
    finite = []
    for m in range(3, 8):
        for c, lam, epsilon in ((F(1), F(1), F(0)),
                                 (F(-2, 3), F(-3, 2), F(5, 7))):
            coefficients = {m: F(rng.choice([1, -2, 3])),
                            **{j: F(rng.randint(-2, 2)) for j in range(m)}}
            w = C.add(C.mono(2, 0, c), C.mono(1, 0, F(2, 5)),
                      C.mono(0, 0, F(-3, 7)))
            H, P, f = make(coefficients, w, lam, epsilon, F(4, 3))
            result = recognize(H)
            assert result and result['third_gate_depth'] == 3
            assert result['lambda'] == lam
            counts['recognition_acceptances'] += 1
            for _ in range(12):
                g = C.mono(rng.randrange(6), rng.randrange(7), F(rng.choice([1, -2])))
                pulled = compose(g, P)
                assert C.transvectant(H, pulled, 3) == compose(c3_new(g, f, c), P)
                assert C.bracket(H, pulled) == compose(d_new(g, f, lam, epsilon), P)
                counts['direct_original_gate_checks'] += 1
                counts['direct_original_derivation_checks'] += 1
            f2, f3 = C.derivative(f, np=2), C.derivative(f, np=3)
            R = C.derivative(C.mul(f2, f3), np=1)
            assert R
            expected_lead = coefficients[m]**2*m*m*(m-1)**2*(m-2)*(2*m-5)
            assert R.get((0, F(2*m-6))) == expected_lead
            counts['leading_nonvanishing_checks'] += 1
            for N in range(3, 10):
                lead = F(-2, 3)
                g = C.add(C.mono(N, 0, lead), C.mono(N-1, 0, F(4, 5)),
                          C.mono(N-2, 1, -N*(N-1)*lead/(6*c)))
                if N > 3:
                    g = C.add(g, C.mono(N-3, 4, F(3, 2)))
                image = c3_new(d_new(g, f, lam, epsilon), f, c)
                top = C.clean({(0, j): a for (i, j), a in image.items() if i == N-2})
                expected = C.scale(C.mul(f2, f3), 12*c*N*(N-1)*lead)
                assert top == expected, (m, N, top, expected)
                counts['highest_q_coefficient_checks'] += 1
            arbitrary = C.add(C.mono(0, m+2, F(2, 3)), C.mono(0, 2, F(-1)),
                              C.mono(0, 0, F(4)))
            b = F(-3, 5)
            g = C.add(arbitrary, C.mono(1, 0, F(7)), C.mono(2, 0, b))
            expected = C.scale(C.derivative(C.mul(f2, C.add(C.scale(f2, b),
                                              C.scale(C.derivative(arbitrary, np=2), -lam))), np=1), 12*c)
            assert c3_new(d_new(g, f, lam, epsilon), f, c) == expected
            counts['scalar_ode_checks'] += 1
            for witness, faildepth, factor in ((C.mono(1, 0), 2, 12*c*lam),
                                                (C.mono(0, 1), 3, 24*c*lam*lam)):
                current = witness
                for depth in range(faildepth+1):
                    value = c3_new(current, f, c)
                    assert value == (C.scale(R, factor) if depth == faildepth else {})
                    current = d_new(current, f, lam, epsilon)
                    counts['sharp_depth_checks'] += 1
            for perturbation in (C.mono(1, 1), C.mono(2, 1), C.mono(3, 0)):
                assert recognize(C.add(H, perturbation)) is None
                counts['recognition_rejections'] += 1
            if m in (3, 4, 6) and c == 1:
                finite.extend(finite_kernel(f, c, lam, epsilon, m, depth)
                              for depth in (1, 2, 3))
    for w, coefficients, lam in ((C.mono(2, 0), {3: 1}, 0),
                                  (C.mono(2, 0), {2: 1}, 1),
                                  (C.mono(1, 0), {3: 1}, 1),
                                  (C.mono(3, 0), {3: 1}, 1)):
        assert recognize(make(coefficients, w, lam)[0]) is None
        counts['recognition_rejections'] += 1
    for malformed in ({(0, F(3, 2)): 1}, {(0, -1): 1}, {(0, 3): 1.5},
                      {(F(1, 2), 3): 1}, {(0, 3): F(1), (0, 2): 0.5}):
        assert recognize(malformed) is None
        counts['recognition_rejections'] += 1
    # A second engine forms the original-coordinate PBW operator directly.
    sys.path[:0] = [str(HERE.parents[1]/'extensions/hamiltonian'),
                    str(HERE.parents[1]/'extensions')]
    import weyl_receipts as W
    H, P, f = make({4: F(2), 3: F(-1), 1: F(3)}, C.mono(2, 0, F(-2, 3)),
                    F(3, 5), F(-4, 7))
    integer_H = {(i, int(j)): a for (i, j), a in H.items()}
    gate, derivation = W.gate(integer_H, 3), W.derivation(integer_H)
    for i, j in ((0, 1), (1, 2), (2, 0), (3, 3), (5, 1)):
        g = C.mono(i, j)
        pulled = {(i, int(j)): a for (i, j), a in compose(g, P).items()}
        assert W.act(gate, pulled) == compose(c3_new(g, f, F(-2, 3)), P)
        assert W.act(derivation, pulled) == compose(d_new(g, f, F(3, 5), F(-4, 7)), P)
        counts['independent_pbw_checks'] += 2
    return {'format': 'higher-restoring-v1', 'passed': True,
            'checks': counts, 'finite_full_output_kernels': finite,
            'all_degree_proof': 'higher_restoring.md, Theorem HR',
            'scope': 'Quadratic w with nonzero leading coefficient; H=F(p+w(q))+lambda*q^2+epsilon*q+C, deg F>=3, lambda!=0',
            'complete_core': 'span{1,H}', 'sharp_third_gate_depth': 3,
            'intermediate_kernel_dimensions': {'1': 4, '2': 3, '3': 2},
            'limits': 'Other shear degrees, lambda=0 and quadratic compositions follow separate theorems. Finite boxes supplement the all-degree highest-q proof; historical priority unestablished.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    encoded = json.dumps(run(), indent=2, sort_keys=True)+'\n'
    if args.output:
        args.output.write_text(encoded)
    print(encoded)


if __name__ == '__main__':
    main()
