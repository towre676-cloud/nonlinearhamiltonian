#!/usr/bin/env python3
"""Independent cubic-phase identities and complete linear-coupling core.

The all-degree proof is cubic_phase_audit.md.  This checker uses the separate
direct mixed-derivative engine analytic_bridge_check, not the producer's
triangular/gauge checker.  Every matrix keeps the complete output.
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


def compose(f, x, y):
    return C.add(*(C.scale(C.mul(C.power(x, int(i)), C.power(y, int(j))), a)
                   for (i, j), a in f.items()))


def pull(f, w):
    """f(Q,P), with Q=q and P=p+w(q), in original coordinates."""
    return compose(f, C.mono(1, 0), C.add(C.mono(0, 1), w))


def affine_c3(a, b, g, c=1):
    """Original flat third gate expressed in (Q,P), h=a(P)+Qb(P)."""
    der = C.derivative
    return C.add(
        C.scale(C.mul(C.add(der(a, np=3),
                            C.mul(C.mono(1, 0), der(b, np=3))), der(g, nq=3)), -1),
        C.scale(C.mul(der(b, np=2), der(g, nq=2, np=1)), 3),
        C.scale(C.add(
            C.mul(der(b, np=1), der(g, np=3)),
            C.mul(der(b, np=2), der(g, np=2)),
            C.scale(C.mul(C.add(der(a, np=2),
                                C.mul(C.mono(1, 0), der(b, np=2))),
                          der(g, nq=1, np=2)), -1),
            C.scale(C.mul(C.add(der(a, np=3),
                                C.mul(C.mono(1, 0), der(b, np=3))),
                          der(g, nq=1, np=1)), -1)), 6 * c))


def linear_gate_terms(A, c=1):
    """Normally ordered (coefficient, P-derivatives, J-derivatives)."""
    p = C.mono(1, 0)
    a1, a2, a3 = [C.derivative(A, nq=k) for k in (1, 2, 3)]
    a_h3 = C.add(C.scale(a2, 3), C.mul(p, a3))
    return [
        (C.mono(0, 0, 6*c), 3, 0),
        (C.scale(C.add(a1, C.scale(C.mul(p, a2), -1)), 6*c), 2, 1),
        (C.scale(C.mul(a1, C.add(a1, C.scale(C.mul(p, a2), 2))), -6*c), 1, 2),
        (C.scale(C.add(C.scale(C.mul(C.power(a1, 2),
                                     C.add(a1, C.mul(p, a2))), 6*c), a_h3), -1), 0, 3),
        (C.scale(C.mul(p, a3), -6*c), 1, 1),
        (C.scale(C.add(C.scale(C.mul(a1, a2), 2), C.mul(p, C.power(a2, 2)),
                       C.mul(p, C.mul(a1, a3))), -6*c), 0, 2),
        (C.scale(a3, 6*c), 0, 1)]


def linear_diag_c3(A, g, c=1):
    """Third gate in independent (P,J), J=Q+A(P), h=PJ+constant.

    Here the first dictionary exponent is P and the second is J.
    """
    return C.add(*(C.mul(coefficient, C.derivative(g, nq=np, np=nj))
                   for coefficient, np, nj in linear_gate_terms(A, c)))


def stopping_shifts(A, c=1):
    """Exact D-weight support; |support|-1 is a proved stopping bound."""
    return sorted({int(i-j)-np+nj for coefficient, np, nj in linear_gate_terms(A, c)
                   for (i, j), value in coefficient.items() if value})


def classify(h, c=1):
    """Recognize h=a(P)+Qb(P), deg a>=3, deg b=1, in (Q,P).

    The returned basis is in (Q,P); apply the original quadratic shear after
    this function.  The quadratic shear coefficient must be nonzero.
    """
    try:
        if isinstance(c, float) or not F(c):
            return None
        c = F(c)
        normalized = {}
        for (i, j), value in h.items():
            if isinstance(i, float) or isinstance(j, float) or isinstance(value, float):
                return None
            i, j = F(i), F(j)
            if i < 0 or j < 0 or i.denominator != 1 or j.denominator != 1:
                return None
            if F(value):
                normalized[int(i), int(j)] = F(value)
        h = C.clean(normalized)
    except (TypeError, ValueError, ZeroDivisionError):
        return None
    if any(i > 1 or j < 0 or int(j) != j for i, j in h):
        return None
    a = {int(j): v for (i, j), v in h.items() if i == 0}
    b = {int(j): v for (i, j), v in h.items() if i == 1}
    if not a or max(a) < 3 or not b or max(b) != 1:
        return None
    mu = b[1]
    r = -b.get(0, F(0)) / mu
    degree = max(a)
    q, p = C.mono(1, 0), C.mono(0, 1)
    basis = [C.mono(0, 0), p, C.power(p, 2), h]
    if degree == 3:
        basis.append(q)
        a2_at_root = sum(F(i*(i-1))*v*r**(i-2) for i, v in a.items() if i >= 2)
        if not a2_at_root:
            basis.append(C.mul(C.add(p, C.mono(0, 0, -r)), h))
    root_centered_a = compose({(i, 0): v/mu for i, v in a.items()},
                             C.add(C.mono(1, 0), C.mono(0, 0, r)), C.mono(0, 1))
    A = {(i-1, 0): value for (i, _), value in root_centered_a.items() if i}
    shifts = stopping_shifts(A, c)
    return {'route': 'CPL', 'proved': True, 'dimension': len(basis),
            'degree_a': degree, 'root': str(r), 'mu': str(mu),
            'Q_degree_bound': 1, 'basis': basis,
            'third_gate_depth_bound': len(shifts)-1,
            'third_gate_weight_shifts': shifts, 'stopping_bound_sharp': False,
            'proof': 'cubic_phase_audit.md, Theorem CPL'}


def classify_linear(h, c=1):
    """Stable internal API; c is the nonzero quadratic shear coefficient."""
    return classify(h, c)


def check_original_gate(seed=281):
    rng = random.Random(seed)
    count = 0
    for _ in range(24):
        a = C.clean({(0, k): F(rng.randint(-2, 2)) for k in range(rng.randint(3, 6)+1)})
        b = C.clean({(0, k): F(rng.randint(-2, 2)) for k in range(rng.randint(1, 4)+1)})
        g = C.clean({(i, j): F(rng.randint(-2, 2)) for i in range(4)
                     for j in range(5) if i+j <= 5})
        c = F(rng.choice([-2, 1, 3]))
        w = C.add(C.mono(2, 0, c), C.mono(1, 0, rng.randint(-2, 2)),
                  C.mono(0, 0, rng.randint(-2, 2)))
        h = C.add(a, C.mul(C.mono(1, 0), b))
        direct = C.transvectant(pull(h, w), pull(g, w), 3)
        assert direct == pull(affine_c3(a, b, g, c), w)
        count += 1
    return count


def check_diagonal_operator(seed=283):
    rng = random.Random(seed)
    count = 0
    for m in range(2, 7):
        A = C.clean({(k, 0): F(rng.randint(-2, 2)) for k in range(m)})
        A = C.add(A, C.mono(m, 0, rng.choice([1, -2, 3])))
        c = F(rng.choice([1, 2, -1]))
        # Convert A(P) and g(P,J) to the independent (Q,P) coordinates.
        p, q = C.mono(0, 1), C.mono(1, 0)
        Ap = compose(A, p, q)
        J = C.add(q, Ap)
        a, b = C.mul(p, Ap), p
        for _ in range(5):
            g = C.clean({(i, j): F(rng.randint(-2, 2)) for i in range(4)
                         for j in range(4) if i+j <= 5})
            gqp = compose(g, p, J)
            assert compose(linear_diag_c3(A, g, c), p, J) == affine_c3(a, b, gqp, c)
            diagonal_D = C.add(C.mul(C.mono(1, 0), C.derivative(g, nq=1)),
                               C.scale(C.mul(C.mono(0, 1), C.derivative(g, np=1)), -1))
            assert compose(diagonal_D, p, J) == C.bracket(C.add(a, C.mul(q, p)), gqp)
            count += 1
    return count


def check_leading_obstructions():
    count = 0
    for m in range(2, 8):
        for c in (F(1), F(-2)):
            alpha = F(2, 3)
            A = C.add(C.mono(m, 0, alpha), C.mono(m-1, 0, 2), C.mono(0, 0, -3))
            for n in range(2, 9):
                for d in range(3):
                    g = C.mono(d, n)
                    for j in range(1, d+1):
                        g = C.add(g, C.mono(d-j, n-j, F(j+1, j+2)))
                    image = linear_diag_c3(A, g, c)
                    if n >= 3:
                        power = d+3*m-3
                        coefficient = -6*c*m**4*alpha**3*n*(n-1)*(n-2)
                        expected = {n-3: coefficient}
                    else:
                        power = d+2*m-3
                        coefficient = -12*c*m*m*(2*m-1)*(d+m-1)*alpha**2
                        expected = {0: coefficient}
                    assert image and max(i for i, _ in image) == power
                    assert {int(j): v for (i, j), v in image.items() if i == power} == expected
                    count += 1
    return count


def check_weight_kernels():
    rows = []
    for A in [C.add(C.mono(2, 0), C.mono(0, 0, 2)),
              C.add(C.mono(2, 0), C.mono(1, 0), C.mono(0, 0, -1)),
              C.add(C.mono(3, 0, 2), C.mono(1, 0)),
              C.add(C.mono(4, 0), C.mono(2, 0, -3))]:
        bound = 7
        groups = {}
        for i in range(bound+1):
            for j in range(bound+1-i):
                groups.setdefault(i-j, []).append(C.mono(i, j))
        dimensions = {}
        for weight, basis in groups.items():
            images = [linear_diag_c3(A, g) for g in basis]
            keys = sorted({key for image in images for key in image})
            matrix = [[image.get(key, F(0)) for image in images] for key in keys]
            dimensions[weight] = len(basis)-C.rank(matrix, len(basis))
        m = max(i for i, _ in A)
        expected = 4 + (m == 2) + (m == 2 and not A.get((1, F(0)), 0))
        assert sum(dimensions.values()) == expected
        rows.append({'degree_A': m, 'source_total_degree_bound_in_P_J': bound,
                     'maximal_invariant_kernel_dimension': expected,
                     'full_output_retained': True})
    return rows


def check_stopping_support():
    rows = []
    for m in range(2, 8):
        A = C.add(C.mono(m, 0, F(2, 3)), C.mono(m-1, 0, -1), C.mono(0, 0, 2))
        shifts = stopping_shifts(A)
        assert set(shifts) <= {-3, -1} | set(range(1, 3*m+1))
        assert len(shifts)-1 <= 3*m+1
        rows.append({'degree_A': m, 'weight_shifts': shifts,
                     'proved_depth_upper_bound': len(shifts)-1,
                     'sharpness_claimed': False})
    assert stopping_shifts(C.add(C.mono(2, 0, 2), C.mono(0, 0, -1))) == [-3, 3, 6]
    return rows


def check_classifier():
    count = 0
    q, p = C.mono(1, 0), C.mono(0, 1)
    for degree in (3, 4, 5):
        for r in (F(0), F(2, 3)):
            for quadratic in (F(0), F(2)):
                R = C.add(p, C.mono(0, 0, -r))
                a = C.add(C.power(R, degree), C.scale(C.power(R, 2), quadratic),
                          C.scale(R, -2), C.mono(0, 0, 7))
                b = C.scale(R, F(-3, 2))
                h = C.add(a, C.mul(q, b))
                result = classify_linear(h, F(2, 3))
                expected = 4 + (degree == 3) + (degree == 3 and not quadratic)
                assert result is not None and result['dimension'] == expected
                w = C.add(C.mono(2, 0, F(2, 3)), C.mono(1, 0, -1))
                H = pull(h, w)
                basis = [pull(g, w) for g in result['basis']]
                keys = sorted({key for g in basis for key in g})
                matrix = [[g.get(key, F(0)) for g in basis] for key in keys]
                assert C.rank(matrix, len(basis)) == len(basis)
                for g in basis:
                    Dg = C.bracket(H, g)
                    all_keys = sorted(set(keys) | set(Dg))
                    lhs = [[f.get(key, F(0)) for f in basis] for key in all_keys]
                    aug = [row+[Dg.get(key, F(0))] for row, key in zip(lhs, all_keys)]
                    assert C.rank(lhs, len(basis)) == C.rank(aug, len(basis)+1)
                    for gate in range(3, 2*degree+3, 2):
                        assert not C.transvectant(H, g, gate)
                count += 1
    assert classify(C.add(C.power(p, 2), C.mul(q, p))) is None
    assert classify(C.add(C.power(p, 3), C.mul(q, C.power(p, 2)))) is None
    assert classify(C.add(C.power(p, 3), C.power(q, 2))) is None
    assert classify_linear(C.add(C.power(p, 3), C.mul(q, p)), 0) is None
    assert classify({(F(1, 2), 3): 1, (1, 1): 1}) is None
    assert classify({(0, 3): 1.0, (1, 1): 1}) is None
    return count


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output', type=Path, default=HERE/'cubic_phase_audit_results.json')
    args = ap.parse_args()
    result = {'status': 'passed', 'format': 'cubic-phase-linear-completeness-v1',
              'checks': {'original_gate_identities': check_original_gate(),
                         'diagonal_operator_and_derivation_identities': check_diagonal_operator(),
                         'leading_coefficient_obstructions': check_leading_obstructions(),
                         'weight_kernel_cross_checks': check_weight_kernels(),
                         'finite_stopping_support': check_stopping_support(),
                         'classifier_and_all_odd_gate_instances': check_classifier()},
              'scope': 'Theorem CPL proves all polynomial degrees. Finite exact checks supplement the written semisimple and leading-degree argument; no degree cutoff supports the universal claim.',
              'naming_audit': 'The derivation defect Delta is a coboundary of partial_P^3. Its displayed vector-field component is a total derivative, not the nontrivial scalar Virasoro cocycle.'}
    args.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
