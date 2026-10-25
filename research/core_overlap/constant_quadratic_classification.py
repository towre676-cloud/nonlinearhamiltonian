#!/usr/bin/env python3
"""Complete exact-core classification for H=A p^2+B(q)p+C(q), A!=0.

The finite stopping bounds are theorem applications, not inferred from
finite-dimensional sampled kernels. Python standard library only.
"""
from __future__ import annotations

import argparse
import copy
from fractions import Fraction as F
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path[:0] = [str(HERE), str(ROOT/'extensions'/'hamiltonian')]
import pure_transverse as U
import quadratic_frontier as QF
import weyl_receipts as W

FORMAT = 'constant-quadratic-core-v1'


def exact_polynomial(H):
    """Validate before normalization; floats and nonpolynomial powers fail."""
    out = {}
    try:
        for (i, j), a in H.items():
            if any(not isinstance(v, (int, F, str)) for v in (i, j, a)):
                return None
            i, j, a = F(i), F(j), F(a)
            if i.denominator != 1 or j.denominator != 1 or i < 0 or j < 0:
                return None
            out[(int(i), int(j))] = a
    except (AttributeError, TypeError, ValueError, ZeroDivisionError):
        return None
    return U.tidy(out)


def classify(H, with_certificate=False):
    H = exact_polynomial(H)
    if not H or max(j for i, j in H) != 2:
        return None
    p2 = {(i, j): a for (i, j), a in H.items() if j == 2}
    if set(p2) != {(0, 2)}:
        return None
    A = p2[(0, 2)]
    u = {(i, 0): a/(2*A) for (i, j), a in H.items() if j == 1}
    Q = U.add({(0, 1): F(1)}, u)
    V = U.add(H, U.scale(U.power(Q, 2), -A))
    if any(j for i, j in V):
        raise AssertionError('completion of square failed')
    m = max((i for i, j in u), default=-1)
    n = max((i for i, j in V), default=-1)
    basis = None
    if m <= 1 and n <= 2:
        case, dimension, depth = 'quadratic Hamiltonian', 'infinite', 0
        core, proof, dependency = 'K[q,p]', 'constant_quadratic_classification.md', 'quadratic'
    elif m == 2 and n <= 1:
        case, dimension, depth = 'quadratic shear with affine residual', 'infinite', 2
        core, proof, dependency = 'K[Q] + span{q,qQ,q^2}', 'pure_quadratic_composition.md', 'QC'
    elif m >= 3 and n <= 2 or m == 2 and n == 2:
        case = 'six-dimensional oscillator sector'
        dimension, depth = 6, 2 if m >= 3 else 3
        core, proof, dependency = 'span{1,q,Q,q^2,qQ,Q^2}', 'shear_oscillator.md', 'SO'
        q = {(1, 0): F(1)}
        basis = [{(0, 0): F(1)}, q, Q, U.power(q, 2), U.mul(q, Q), U.power(Q, 2)]
    else:
        assert n >= 3
        case, dimension, core = 'nonlinear residual collapse', 2, 'span{1,H}'
        basis = [{(0, 0): F(1)}, H]
        if m >= 3:
            depth, proof, dependency = (6 if n == 3 else 4), 'quadratic_frontier.md', 'QF'
        elif m == 2:
            depth, proof, dependency = (6 if n == 3 else 4), 'quadratic_shear_residual.md', 'QR'
        else:
            depth, proof, dependency = (7 if n == 3 else 5), 'affine_shear_potentials.md', 'AFP'
    answer = {'format': FORMAT, 'route': 'CQ', 'proved': True, 'case': case,
              'dimension': dimension, 'core': core, 'H': U.terms(H),
              'A': str(A), 'u': U.terms(u), 'Q': U.terms(Q), 'V': U.terms(V),
              'degree_u': m, 'degree_V': n, 'n': n,
              'third_gate_depth': depth, 'proof': proof, 'dependency_route': dependency,
              'finite_stopping_equality': 'D_infinity(H) = intersection_{r=0}^'+str(depth)+' ker(C3 D^r)',
              'degree_convention': '-1 denotes the zero polynomial',
              'scope': 'one canonical pair; polynomial observables; fixed original flat Weyl convention; nonzero constant p^2 coefficient',
              'priority': 'historical priority unestablished; completion of square and quantization background are established machinery'}
    if basis is not None:
        answer['basis'] = [U.terms(f) for f in basis]
        closure = [QF.coordinates(U.bracket(H, f), basis) for f in basis]
        assert all(row is not None for row in closure)
        answer['closure'] = [[str(a) for a in row] for row in closure]
    if with_certificate:
        if dependency == 'QF':
            answer['supporting_certificate'] = QF.produce(H)
        elif dependency == 'QR':
            import quadratic_shear_residual as QR
            result = QR.classify(H)
            assert result and result['dimension'] == 2
            answer['supporting_classification'] = result
        elif dependency == 'SO':
            import shear_oscillator as SO
            result = SO.recognize(H)
            assert result and result['core_dimension'] == 6
            answer['supporting_recognizer'] = {'route': 'SO', 'third_gate_depth': result['third_gate_depth']}
        elif dependency == 'QC':
            import pure_quadratic_composition as QC
            result = QC.classify(H)
            assert result and result['degree_P'] == 2
            answer['supporting_classification'] = result
        elif dependency == 'AFP':
            import affine_shear_potentials as AP
            result = AP.classify(H)
            assert result and result['dimension'] == 2
            answer['supporting_recognizer'] = {'route': result['route'],
                    'dimension': result['dimension'], 'third_gate_depth': result['third_gate_depth'],
                    'proof': result['proof']}
    return answer


def check_certificate(certificate):
    """Replay the exact theorem-application data and finite-basis identities.

    This checks a scoped application of the linked all-degree proofs; it
    does not claim an independent formal verification of those proofs.
    """
    if certificate.get('format') != FORMAT:
        raise ValueError('unknown constant-quadratic certificate format')
    H = QF.decode(certificate['H'])
    expected = classify(H)
    if expected is None:
        raise ValueError('Hamiltonian outside constant-quadratic scope')
    for key, value in expected.items():
        if certificate.get(key) != value:
            raise ValueError('theorem application mismatch: '+key)
    if any(key.startswith('supporting_') for key in certificate):
        detailed = classify(H, with_certificate=True)
        for key in certificate:
            if key.startswith('supporting_') and certificate[key] != detailed.get(key):
                raise ValueError('supporting proof receipt mismatch: '+key)
    for rows in expected.get('basis', []):
        f = QF.decode(rows)
        if any(W.act(gate, f) for gate in W.gates(H).values()):
            raise ValueError('proposed finite generator fails a gate')
    return {'status': 'passed', 'dimension': expected['dimension'],
            'dependency_route': expected['dependency_route'],
            'third_gate_depth': expected['third_gate_depth'],
            'trust_boundary': 'exact normal-form application and basis checks; linked written all-degree theorem'}


def make(u, V, A=1):
    up = {(i, 0): F(a) for i, a in u.items() if a}
    Q = U.add({(0, 1): F(1)}, up)
    return U.add(U.scale(U.power(Q, 2), F(A)), {(i, 0): F(a) for i, a in V.items() if a}), Q


def self_test():
    records = []
    counters = {'instances': 0, 'original_gate_checks': 0, 'derivation_closure_checks': 0,
                'sharp_depth_checks': 0, 'invalid_input_rejections': 0,
                'forged_application_rejections': 0, 'supporting_branch_checks': 0}
    for m in (-1, 0, 1, 2, 3, 4):
        u = ({} if m < 0 else {0: F(2, 3)} if m == 0 else
             {0: F(2, 3), 1: F(-3, 2)} if m == 1 else
             {0: F(2, 3), 1: F(-3, 2), m: F(5, 4)})
        for n in (-1, 0, 1, 2, 3, 4, 6):
            V = {} if n < 0 else ({0: F(7, 3)} if n == 0 else
                                 {0: F(7, 3), n: F(-2, 3)})
            if n >= 2:
                V[1] = F(3, 2)
            A = F(-3, 2) if (m+n) % 2 else F(2, 3)
            H, Q = make(u, V, A)
            answer = classify(H)
            assert answer and answer['degree_u'] == m and answer['degree_V'] == n
            check_certificate(answer)
            counters['instances'] += 1
            gates = W.gates(H)
            D = W.derivation(H)
            basis = [QF.decode(rows) for rows in answer.get('basis', [])]
            if basis:
                for f, row in zip(basis, answer['closure']):
                    assert W.act(D, f) == QF.combine(basis, list(map(F, row)))
                    counters['derivation_closure_checks'] += 1
            elif answer['dependency_route'] == 'QC':
                basis = [U.power(Q, j) for j in range(7)] + [{(1, 0): F(1)}, U.mul({(1, 0): F(1)}, Q), {(2, 0): F(1)}]
            else:
                basis = [{(i, j): F(1)} for i in range(5) for j in range(5-i)]
            for f in basis:
                for _ in range(3):
                    assert all(not W.act(gate, f) for gate in gates.values())
                    counters['original_gate_checks'] += len(gates)
                    f = W.act(D, f)
            depth = answer['third_gate_depth']
            if depth:
                if answer['dimension'] == 6 and m == 2:
                    kappa = 2*F(V[2]); epsilon = F(V.get(1, 0))
                    x = U.add({(1, 0): F(1)}, {(0, 0): epsilon/kappa})
                    witness = U.add(U.scale(U.mul(U.power(x, 2), Q), 3*kappa), U.scale(U.power(Q, 3), 4*A))
                else:
                    witness = {(3 if depth == 2 else 1, 0): F(1)}
                g = witness
                C3 = W.gate(H, 3)
                for _ in range(depth):
                    assert not W.act(C3, g), (m, n, depth)
                    g = W.act(D, g)
                assert W.act(C3, g), (m, n, depth)
                counters['sharp_depth_checks'] += 1
            records.append({'degree_u': m, 'degree_V': n, 'dimension': answer['dimension'],
                            'case': answer['case'], 'dependency_route': answer['dependency_route'],
                            'third_gate_depth': depth})
    H, Q = make({3: 1, 1: 2}, {3: 1}, A=F(3, 2))
    for bad in [{**H, (1, 2): F(1)}, {**H, (0, 3): F(1)},
                {**H, (F(1, 2), 0): F(1)}, {**H, (-1, 0): F(1)},
                {**H, (0, F(1, 2)): F(1)}, {**H, (0, -1): F(1)},
                {**H, (0, 2): 1.0}, {(float(i), j): a for (i, j), a in H.items()},
                {(0, 1): F(1)}]:
        assert classify(bad) is None
        counters['invalid_input_rejections'] += 1
    sample = classify(H)
    for key, value in [('dimension', 6), ('third_gate_depth', 2), ('proved', False), ('degree_u', 4)]:
        bad = copy.deepcopy(sample); bad[key] = value
        try:
            check_certificate(bad)
        except ValueError:
            counters['forged_application_rejections'] += 1
        else:
            raise AssertionError('forged theorem application accepted')
    for u, V in [({1: 2}, {3: 1}), ({2: 1}, {1: 2}),
                 ({2: 1}, {2: 2}), ({2: 1}, {3: 1, 1: 2}),
                 ({3: 1}, {2: 2}), ({3: 1}, {3: 1})]:
        detailed = classify(make(u, V)[0], with_certificate=True)
        json.dumps(detailed)  # The complete optional result must be serializable.
        check_certificate(detailed)
        counters['supporting_branch_checks'] += 1
    return {'format': FORMAT, 'status': 'passed', 'checks': counters,
            'instances': records, 'sample_application': sample,
            'scope': 'all rational constant-leading-coefficient quadratic momentum Hamiltonians',
            'priority': 'historical priority unestablished'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', nargs='?', type=Path)
    parser.add_argument('--classify', type=Path, help='JSON list [q_exponent,p_exponent,rational] or object with hamiltonian')
    parser.add_argument('--check-certificate', type=Path)
    parser.add_argument('--with-certificate', action='store_true')
    args = parser.parse_args()
    if args.classify:
        data = json.loads(args.classify.read_text())
        H = QF.decode(data['hamiltonian'] if isinstance(data, dict) else data)
        result = classify(H, args.with_certificate) or {'proved': False, 'status': 'outside constant-quadratic scope'}
    elif args.check_certificate:
        result = check_certificate(json.loads(args.check_certificate.read_text()))
    else:
        result = self_test()
    encoded = json.dumps(result, indent=2, sort_keys=True)+'\n'
    if args.output:
        args.output.write_text(encoded, encoding='utf-8')
    print(encoded)


if __name__ == '__main__':
    main()
