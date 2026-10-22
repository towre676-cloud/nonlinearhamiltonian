#!/usr/bin/env python3
"""Exact recognition and checks for the oscillator shear-sector theorem."""
from __future__ import annotations

import argparse
from fractions import Fraction as F
import importlib.util
from math import factorial
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import analytic_bridge_check as C


def recognize(H):
    """Recognize the SO family in original rational (q,p) coefficients.

    u(0)=0; degree u>=3 allows any kappa. Degree u=2 requires kappa!=0.
    A quadratic shear with kappa=0 returns None and is deferred to QC.
    """
    # Validate before C.clean: that low-level helper intentionally converts
    # q exponents to int and accepts floats for unrelated arithmetic uses.
    normalized = {}
    try:
        for (i, j), a in H.items():
            if any(not isinstance(x, (int, F, str)) for x in (i, j, a)):
                return None
            i, j, a = F(i), F(j), F(a)
            if i < 0 or j < 0 or i.denominator != 1 or j.denominator != 1:
                return None
            normalized[(int(i), j)] = a
    except (TypeError, ValueError, ZeroDivisionError, AttributeError):
        return None
    H = C.clean(normalized)
    if not H:
        return None
    if max(j for _, j in H) != 2:
        return None
    A = H.get((0, F(2)), F(0))
    if not A or any(i and j == 2 for i, j in H):
        return None
    B = H.get((0, F(1)), F(0))
    u = C.clean({(i, 0): a / (2*A) for (i, j), a in H.items() if j == 1 and i})
    degree = max((i for i, _ in u), default=0)
    if degree < 2:
        return None
    Q = C.add(C.mono(0, 1), u)
    residual = C.add(H, C.scale(C.power(Q, 2), -A), C.scale(Q, -B))
    if any(j or i > 2 for i, j in residual):
        return None
    kappa = 2*residual.get((2, F(0)), F(0))
    if degree == 2 and not kappa:
        return None
    q = C.mono(1, 0)
    return {'route': 'SO', 'proved': True, 'core_dimension': 6,
            'third_gate_depth': 2 if degree >= 3 else 3,
            'A': A, 'B': B, 'kappa': kappa,
            'epsilon': residual.get((1, F(0)), F(0)),
            'constant': residual.get((0, F(0)), F(0)),
            'u': u, 'Q': Q,
            'basis': [C.mono(0, 0), q, Q, C.power(q, 2), C.mul(q, Q), C.power(Q, 2)]}


def compose(f, Q):
    out = {}
    for (i, j), a in f.items():
        assert j.denominator == 1 and j >= 0
        out = C.add(out, C.scale(C.mul(C.mono(i, 0), C.power(Q, int(j))), a))
    return out


def d_new(f, A, B, kappa, epsilon):
    return C.add(C.mul(C.add(C.mono(1, 0, kappa), C.mono(0, 0, epsilon)),
                       C.derivative(f, np=1)),
                 C.scale(C.mul(C.add(C.mono(0, 1, 2*A), C.mono(0, 0, B)),
                               C.derivative(f, nq=1)), -1))


def c3_new(f, u, A, B):
    return C.add(C.mul(C.add(C.mono(0, 1, 2*A), C.mono(0, 0, B)),
                       C.mul(C.derivative(u, nq=3), C.derivative(f, np=3))),
                 C.scale(C.mul(C.derivative(u, nq=2),
                               C.derivative(f, nq=1, np=2)), -6*A))


def matrix(A, B, kappa, epsilon):
    return [[F(v) for v in row] for row in
            [[0, -B, epsilon, 0, 0, 0],
             [0, 0, kappa, -2*B, epsilon, 0],
             [0, -2*A, 0, 0, -B, 2*epsilon],
             [0, 0, 0, 0, kappa, 0],
             [0, 0, 0, -4*A, 0, 2*kappa],
             [0, 0, 0, 0, -2*A, 0]]]


def matrix_product(a, b):
    return [[sum(a[i][k]*b[k][j] for k in range(6)) for j in range(6)] for i in range(6)]


def spectral_check(A, B, kappa, epsilon):
    """Exact characteristic/minimal-polynomial verification, kappa!=0."""
    assert kappa
    M = matrix(A, B, kappa, epsilon)
    identity = [[F(i == j) for j in range(6)] for i in range(6)]
    powers = [identity]
    for _ in range(6):
        powers.append(matrix_product(M, powers[-1]))
    omega2 = 2*A*kappa
    assert all(powers[5][i][j]+5*omega2*powers[3][i][j]+4*omega2**2*M[i][j] == 0
               for i in range(6) for j in range(6))
    assert C.rank([[p[i][j] for i in range(6) for j in range(6)] for p in powers[:5]], 36) == 5
    assert C.rank(M, 6) == 4
    # Faddeev-LeVerrier computes characteristic coefficients from exact
    # rational matrix products; it is independent of the spectral proof.
    Bk = identity
    characteristic = [F(1)]
    for degree in range(1, 7):
        MB = matrix_product(M, Bk)
        coefficient = -sum(MB[i][i] for i in range(6))/degree
        characteristic.append(coefficient)
        Bk = [[MB[i][j]+coefficient*identity[i][j] for j in range(6)] for i in range(6)]
    assert characteristic == [F(1), F(0), 5*omega2, F(0), 4*omega2**2, F(0), F(0)]
    return {'omega_squared': str(omega2),
            'characteristic_polynomial_coefficients_descending': list(map(str, characteristic)),
            'minimal_polynomial_coefficients_descending': list(map(str, [1, 0, 5*omega2, 0, 4*omega2**2, 0])),
            'minimal_polynomial_matrix_identity': True,
            'matrix_powers_I_through_M4_rank': 5,
            'zero_eigenspace_dimension': 2, 'semisimple_over_algebraic_closure': True}


def observer_check(A, B, kappa, epsilon):
    """Replay the retained observer checker on the stated original targets."""
    filename = Path(__file__).resolve().parents[2]/'extensions'/'observer'/'observation_closure_reference.py'
    spec = importlib.util.spec_from_file_location('_oscillator_observer', filename)
    O = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(O)
    M = matrix(A, B, kappa, epsilon)
    action = list(map(list, zip(*M)))
    dimensions = []
    for indices in [(1,), (3,), (1, 3)]:
        model = {'dimension': 6, 'actions': {'D': O.strings(action)},
                 'target': [[int(j == i) for j in range(6)] for i in indices]}
        certificate = O.compile_model(model)
        O.check_certificate(certificate, model)
        dimensions.append(len(certificate['basis']))
    expected = [2, 3, 5] if not epsilon else [3, 5, 6]
    assert dimensions == expected
    return {'target_contract': 'original q; original q^2; joint original (q,q^2), coefficient-linear derivative closure',
            'target_dimensions': dimensions, 'observer_certificates_replayed': 3}


def finite_kernel(u, A, B, kappa, epsilon, bound=6):
    depth = 2 if max(i for i, _ in u) >= 3 else 3
    basis = [C.mono(i, j) for i in range(bound+1) for j in range(bound+1-i)]
    images = []
    for f in basis:
        image = []
        for _ in range(depth+1):
            image.append(c3_new(f, u, A, B))
            f = d_new(f, A, B, kappa, epsilon)
        images.append(image)
    keys = sorted({(r, i, j) for image in images for r, f in enumerate(image) for i, j in f})
    rows = [[image[r].get((i, j), F(0)) for image in images] for r, i, j in keys]
    dimension = len(basis)-C.rank(rows, len(basis))
    assert dimension == 6
    return {'input_monomials': len(basis), 'degree_bound_in_q_Q': bound,
            'third_gate_depth': depth, 'kernel_dimension': dimension,
            'full_output_coordinates': len(keys), 'output_projection': False}


def flow_check(A, B, kappa, epsilon, order=12):
    q, Q, one = C.mono(1, 0), C.mono(0, 1), C.mono(0, 0)
    basis = [one, q, Q, C.power(q, 2), C.mul(q, Q), C.power(Q, 2)]
    keys = [(0, F(0)), (1, F(0)), (0, F(1)), (2, F(0)), (1, F(1)), (0, F(2))]
    M = matrix(A, B, kappa, epsilon)
    for j, f in enumerate(basis):
        assert d_new(f, A, B, kappa, epsilon) == C.clean({key: M[i][j] for i, key in enumerate(keys)})
    omega2 = 2*A*kappa
    cs, ss, ts = [F(0)]*(order+1), [F(0)]*(order+1), [F(0)]*(order+1)
    for j in range(order//2+1):
        if 2*j <= order: cs[2*j] = (-omega2)**j/F(factorial(2*j))
        if 2*j+1 <= order: ss[2*j+1] = (-omega2)**j/F(factorial(2*j+1))
        if 2*j+2 <= order: ts[2*j+2] = (-omega2)**j/F(factorial(2*j+2))
    qt = [C.add(C.scale(q, cs[r]), C.scale(Q, -2*A*ss[r]),
                C.scale(one, -B*ss[r]-2*A*epsilon*ts[r])) for r in range(order+1)]
    Qt = [C.add(C.scale(Q, cs[r]), C.scale(q, kappa*ss[r]),
                C.scale(one, epsilon*ss[r]-kappa*B*ts[r])) for r in range(order+1)]
    for r in range(order):
        assert C.scale(qt[r+1], r+1) == C.add(C.scale(Qt[r], -2*A), C.scale(one, -B if r == 0 else 0))
        assert C.scale(Qt[r+1], r+1) == C.add(C.scale(qt[r], kappa), C.scale(one, epsilon if r == 0 else 0))
    def convolution(a, b):
        return [C.add(*(C.mul(a[j], b[r-j]) for j in range(r+1))) for r in range(order+1)]
    flows = [[one]+[{} for _ in range(order)], qt, Qt,
             convolution(qt, qt), convolution(qt, Qt), convolution(Qt, Qt)]
    for j, f in enumerate(basis):
        for r in range(order+1):
            assert C.scale(f, F(1, factorial(r))) == flows[j][r]
            f = d_new(f, A, B, kappa, epsilon)
    return {'matrix_columns_checked': 6, 'formal_flow_order': order,
            'closed_flow_basis_coefficients_checked': 6*(order+1)}


def check():
    us = [C.mono(2, 0), C.add(C.mono(2, 0, F(-3, 2)), C.mono(1, 0, 2)),
          C.mono(3, 0), C.add(C.mono(4, 0, -2), C.mono(2, 0, 3)),
          C.add(C.mono(5, 0, F(2, 3)), C.mono(3, 0, -1), C.mono(1, 0, 4))]
    parameters = [(F(1), F(0), F(1), F(0)), (F(2), F(3), F(-2), F(5)),
                  (F(-1), F(-2), F(3, 2), F(-3)),
                  (F(3, 2), F(-5, 2), F(0), F(7, 3))]
    counters = {'recognizer_checks': 0, 'transformed_third_gate_checks': 0,
                'transformed_derivation_checks': 0, 'protected_basis_checks': 0,
                'sharp_depth_checks': 0, 'commutator_span_checks': 0}
    fixtures = []
    for ui, u in enumerate(us):
        degree = max(i for i, _ in u)
        Q = C.add(C.mono(0, 1), u)
        for A, B, kappa, epsilon in parameters:
            H = C.add(C.scale(C.power(Q, 2), A), C.scale(Q, B),
                      C.mono(2, 0, kappa/2), C.mono(1, 0, epsilon), C.mono(0, 0, 7))
            rec = recognize(H)
            counters['recognizer_checks'] += 1
            if degree == 2 and not kappa:
                assert rec is None
                continue
            assert rec and rec['u'] == u
            assert (rec['A'], rec['B'], rec['kappa'], rec['epsilon'], rec['constant']) == (A, B, kappa, epsilon, F(7))
            for i in range(5):
                for j in range(5):
                    f = C.mono(i, j)
                    original = compose(f, Q)
                    assert C.transvectant(H, original, 3) == compose(c3_new(f, u, A, B), Q)
                    counters['transformed_third_gate_checks'] += 1
                    assert C.bracket(H, original) == compose(d_new(f, A, B, kappa, epsilon), Q)
                    counters['transformed_derivation_checks'] += 1
            for f in rec['basis']:
                assert all(k == 0 for k in C.moyal(H, f))
                counters['protected_basis_checks'] += 1
            if degree >= 3:
                g = C.mono(3, 0)
                for r in range(3):
                    actual = C.transvectant(H, compose(g, Q), 3)
                    expected = compose(C.scale(C.derivative(u, nq=2), -288*A**3), Q) if r == 2 else {}
                    assert actual == expected
                    counters['sharp_depth_checks'] += 1
                    g = d_new(g, A, B, kappa, epsilon)
            else:
                x, y = C.add(C.mono(1, 0), C.mono(0, 0, epsilon/kappa)), C.add(C.mono(0, 1), C.mono(0, 0, B/(2*A)))
                g = C.add(C.scale(C.mul(C.power(x, 2), y), 3*kappa), C.scale(C.power(y, 3), 4*A))
                b = u[(2, F(0))]
                for r in range(4):
                    actual = C.transvectant(H, compose(g, Q), 3)
                    assert actual == (C.mono(0, 0, -1728*A**3*b*kappa**2) if r == 3 else {})
                    counters['sharp_depth_checks'] += 1
                    g = d_new(g, A, B, kappa, epsilon)
                E = [C.mono(1, 2)]
                for _ in range(3):
                    E.append(C.add(C.scale(C.mul(C.mono(0, 1), C.derivative(E[-1], nq=1)), kappa),
                                   C.scale(C.mul(C.mono(1, 0), C.derivative(E[-1], np=1)), -2*A)))
                operator_basis = [(3, F(0)), (2, F(1)), (1, F(2)), (0, F(3))]
                rows = [[f.get(key, F(0)) for key in operator_basis] for f in E]
                assert C.rank(rows, 4) == 4
                assert E[1] == C.add(C.mono(0, 3, kappa), C.mono(2, 1, -4*A))
                assert E[2] == C.add(C.mono(3, 0, 8*A*A), C.mono(1, 2, -14*A*kappa))
                assert E[3] == C.add(C.mono(2, 1, 80*A*A*kappa), C.mono(0, 3, -14*A*kappa*kappa))
                counters['commutator_span_checks'] += 1
            for broken in [C.add(H, C.mono(3, 0)), C.add(H, C.mono(1, 2)), C.add(H, C.mono(0, 3)),
                           {**H, (F(1, 2), F(0)): F(1)},
                           {**H, (-1, F(0)): F(1)},
                           {**H, (0, F(-1)): F(1)},
                           {**H, (0, F(1, 2)): F(1)},
                           {**H, (0, F(2)): 1.0},
                           {(float(i), j): a for (i, j), a in H.items()}]:
                assert recognize(broken) is None
                counters['recognizer_checks'] += 1
            fixture = {'u_index': ui, 'degree_u': degree, 'A': str(A), 'B': str(B),
                             'kappa': str(kappa), 'epsilon': str(epsilon),
                             **finite_kernel(u, A, B, kappa, epsilon),
                             **flow_check(A, B, kappa, epsilon),
                             **observer_check(A, B, kappa, epsilon)}
            if kappa:
                fixture['spectral_certificate'] = spectral_check(A, B, kappa, epsilon)
            fixtures.append(fixture)
    return {'format': 'shear-oscillator-core-v1', 'passed': True,
            **counters, 'fixtures': fixtures,
            'spectral_certificates_checked': sum('spectral_certificate' in f for f in fixtures),
            'observer_certificates_replayed': sum(f['observer_certificates_replayed'] for f in fixtures),
            'closed_flow_basis_coefficients_checked': sum(f['closed_flow_basis_coefficients_checked'] for f in fixtures),
            'all_degree_proof': 'shear_oscillator.md, Theorem SO',
            'quadratic_shear_kappa_zero': 'deferred to retained QC infinite family'}


run = check


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    encoded = json.dumps(check(), indent=2, sort_keys=True)+'\n'
    if args.output:
        args.output.write_text(encoded, encoding='utf-8')
    print(encoded)


if __name__ == '__main__':
    main()
