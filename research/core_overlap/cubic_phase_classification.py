#!/usr/bin/env python3
"""Full affine cubic-phase classification and exact rational chart recognition.

Written proof: cubic_phase_classification.md. No symbolic package is needed.
The recognizer checks its reconstructed chart exactly; a miss is unclassified.
"""
from __future__ import annotations
import argparse
from fractions import Fraction as F
import json
from math import isqrt
from pathlib import Path
import random
import sys

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parents[1]/'extensions/hamiltonian'),
               str(HERE.parents[1]/'extensions')]
import check_two_root as T
import check_triangular as CT
import weyl_receipts as W
import cubic_affine_completeness as AF
import cubic_phase_audit as AL

FORMAT = 'affine-cubic-phase-complete-v1'


def normalize(poly):
    out = {}
    try:
        for key, coefficient in poly.items():
            if len(key) != 2 or any(isinstance(x, float) for x in (*key, coefficient)):
                return None
            i, j, a = F(key[0]), F(key[1]), F(coefficient)
            if i < 0 or j < 0 or i.denominator != 1 or j.denominator != 1:
                return None
            if a:
                out[int(i), int(j)] = a
    except (TypeError, ValueError, ZeroDivisionError, AttributeError):
        return None
    return out


def _degree(u):
    return max(u, default=-1)


def _divmod(a, b):
    a, b = dict(a), dict(b)
    quotient = {}
    if not b:
        raise ZeroDivisionError('zero polynomial')
    while a and max(a) >= max(b):
        n, coefficient = max(a)-max(b), a[max(a)]/b[max(b)]
        quotient[n] = quotient.get(n, F(0))+coefficient
        for j, value in b.items():
            k = j+n
            a[k] = a.get(k, F(0))-coefficient*value
            if not a[k]:
                del a[k]
    return quotient, a


def _gcd(a, b):
    while b:
        _, remainder = _divmod(a, b)
        a, b = b, remainder
    return {j: coefficient/a[max(a)] for j, coefficient in a.items()} if a else {}


def _rational_roots(poly):
    degree = _degree(poly)
    if degree == 1:
        return [-poly.get(0, F(0))/poly[1]]
    if degree != 2:
        return []
    a, b, c = poly[2], poly.get(1, F(0)), poly.get(0, F(0))
    discriminant = b*b-4*a*c
    if discriminant < 0:
        return []
    n, d = isqrt(discriminant.numerator), isqrt(discriminant.denominator)
    if n*n != discriminant.numerator or d*d != discriminant.denominator:
        return []
    root = F(n, d)
    return sorted({(-b+root)/(2*a), (-b-root)/(2*a)})


def affine_directions(h):
    """Rational alpha with (partial_Q-alpha partial_P)^2 h=0."""
    a, b, c = W.pder(h, 2, 0), W.pder(h, 1, 1), W.pder(h, 0, 2)
    common = {}
    for monomial in sorted(set(a) | set(b) | set(c)):
        equation = {j: coefficient for j, coefficient in
                    ((0, a.get(monomial, F(0))),
                     (1, -2*b.get(monomial, F(0))),
                     (2, c.get(monomial, F(0)))) if coefficient}
        if not equation:
            continue
        common = _gcd(common, equation) if common else equation
        if _degree(common) == 0:
            return []
    return _rational_roots(common) if common else [F(0)]


def affine_chart(H):
    """Recover a rational quadratic shear making H affine in Q, when found.

    The linear shear term is recovered by a common polynomial gcd, rather
    than assuming the completed-power chart remains affine in Q.
    """
    H = normalize(H)
    if H is None or not H:
        return None
    s = max(j for _, j in H)
    if s < 1:
        return None
    column = lambda j: {i: coefficient for (i, k), coefficient in H.items() if k == j}
    leading = column(s)
    if _degree(leading) > 1:
        return None
    quotient, _ = _divmod(column(s-1), {i: s*a for i, a in leading.items()})
    if _degree(quotient) != 2:
        return None
    c = quotient[2]
    if _degree(leading) == 1:
        candidates = [quotient.get(1, F(0))]
    else:
        h0 = CT.untri(H, {2: c})
        candidates = affine_directions(h0)
        if all(i <= 1 for i, j in h0):
            candidates = [F(0)]+candidates
    for slope in dict.fromkeys(candidates):
        w = {2: c, **({1: slope} if slope else {})}
        h = CT.untri(H, w)
        if all(i <= 1 for i, j in h):
            assert CT.tri(h, w) == H
            return {'w': w, 'c': c, 'h': h}
    return None


def classify_in_chart(h, c=1):
    """Classify EVERY h=a(P)+Qb(P), in a supplied nonzero quadratic shear."""
    h = normalize(h)
    try:
        if isinstance(c, float) or not F(c):
            return None
        c = F(c)
    except (TypeError, ValueError, ZeroDivisionError):
        return None
    if h is None or any(i > 1 for i, j in h):
        return None
    a = {j: x for (i, j), x in h.items() if i == 0}
    b = {j: x for (i, j), x in h.items() if i == 1}
    f, d = _degree(a), _degree(b)
    one, q, p = {(0, 0): F(1)}, {(1, 0): F(1)}, {(0, 1): F(1)}
    if d >= 2:
        result = AF.classify_affine(h)
    elif d == 1 and f >= 3:
        result = AL.classify_linear(h, c)
    elif d == 1 and f == 2:
        result = {'case': 'quadratic affine chart', 'dimension': 6,
                  'basis': [one, q, p, T.power(q, 2), T.mul(q, p), T.power(p, 2)],
                  'core': 'span{1,Q,P,Q^2,QP,P^2}', 'proof': 'SO/CQ',
                  'third_gate_depth': 3}
    elif d == 1:
        result = {'case': 'positive three-strip', 'dimension': 'infinite',
                  'core': 'K[Q]+P*K[Q]+P^2*K[Q]', 'proof': 'positive strip W',
                  'algebra_generators': [q], 'module_generators': [one, p, T.power(p, 2)]}
    elif f >= 3:
        result = {'case': 'QC nonlinear composition', 'dimension': 'infinite',
                  'core': 'K[P]+K*Q', 'proof': 'QC', 'third_gate_depth': 1,
                  'tower_generator': p, 'extra_generators': [q]}
    elif f == 2:
        result = {'case': 'QC quadratic composition', 'dimension': 'infinite',
                  'core': 'K[P]+span{Q,QP,Q^2}', 'proof': 'QC',
                  'third_gate_depth': 2, 'tower_generator': p,
                  'extra_generators': [q, T.mul(q, p), T.power(q, 2)]}
    else:
        result = {'case': 'quadratic original Hamiltonian', 'dimension': 'infinite',
                  'core': 'K[Q,P]', 'proof': 'quadratic Hamiltonian',
                  'third_gate_depth': 0, 'algebra_generators': [q, p]}
    if result is None:
        raise AssertionError('affine classification branch missing')
    result.setdefault('case', 'K1-prime full core')
    if 'core' not in result:
        result['core'] = ('span{1,H}' if result['dimension'] == 2 else
                          'span{declared basis}')
    if 'basis' in result:
        result['basis'] = [normalize(g) for g in result['basis']]
    return {**result, 'proved': True, 'degree_a': f, 'degree_b': d}


def recognize(H):
    chart = affine_chart(H)
    if chart is None:
        return None
    result = classify_in_chart(chart['h'], chart['c'])
    out = {**result, 'route': 'CP', 'w': chart['w'], 'h': chart['h'],
           'c': chart['c'], 'chart_proof': 'cubic_phase_classification.md'}
    if 'basis' in result:
        out['basis'] = [CT.tri(g, chart['w']) for g in result['basis']]
    for key in ('algebra_generators', 'module_generators', 'extra_generators'):
        if key in result:
            out[key] = [CT.tri(g, chart['w']) for g in result[key]]
    if 'tower_generator' in result:
        out['tower_generator'] = CT.tri(result['tower_generator'], chart['w'])
    return out


def serial(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, list):
        return [serial(x) for x in value]
    if isinstance(value, dict):
        if value and all(isinstance(k, tuple) for k in value):
            return T.ser(value)
        return {str(k): serial(x) for k, x in value.items()}
    return value


def certify(H):
    result = recognize(H)
    if result is None:
        raise ValueError('no recognized rational affine cubic-phase chart')
    return {'format': FORMAT, 'hamiltonian': T.ser(normalize(H)),
            'claim': serial(result)}


def check(cert):
    if cert.get('format') != FORMAT:
        raise ValueError('wrong affine cubic-phase certificate format')
    H = {tuple(map(int, k.split(','))): F(x) for k, x in cert['hamiltonian'].items()}
    actual = certify(H)
    if actual != cert:
        raise ValueError('declared full-core classification differs from exact recomputation')
    return {'status': 'passed', 'dimension': actual['claim']['dimension'],
            'case': actual['claim']['case'], 'claim': 'full polynomial dynamic core'}


def run():
    import copy
    rng = random.Random(20261022)
    counts = {'classified_instances': 0, 'finite_basis_gate_and_closure_checks': 0,
              'ambiguous_completion_charts': 0, 'forgery_rejections': 0,
              'invalid_input_rejections': 0}
    cases = [
        {(0, 4): F(1), (1, 3): F(2), (1, 0): F(-1)},
        {(0, 4): F(1), (1, 2): F(1)},
        {(0, 4): F(1), (1, 2): F(1), (1, 1): F(2), (1, 0): F(-3)},
        {(0, 3): F(1), (1, 1): F(1)},
        {(0, 3): F(1), (0, 2): F(2), (1, 1): F(1)},
        {(0, 5): F(1), (1, 1): F(1)},
        {(1, 2): F(1), (0, 1): F(2)},
        {(0, 2): F(1), (1, 1): F(1)},
        {(0, 1): F(2), (1, 1): F(1)},
        {(0, 4): F(1), (1, 0): F(1)},
        {(0, 2): F(1), (1, 0): F(1)},
        {(0, 1): F(1), (1, 0): F(1)},
        {(1, 3): F(1), (0, 1): F(-2)},
    ]
    seen = set()
    for h in cases:
        for w in ({2: F(1)}, {2: F(-2, 3), 1: F(3, 5), 0: F(-7, 11)}):
            H = CT.tri(h, w)
            chart, result = affine_chart(H), recognize(H)
            assert chart is not None and result is not None, (h, w)
            expected = classify_in_chart(h, w[2])
            assert result['dimension'] == expected['dimension'], (result, expected)
            seen.add(result['case'])
            counts['classified_instances'] += 1
            if result.get('basis'):
                assert CT.span_ok(H, result['basis']), (h, w, result)
                counts['finite_basis_gate_and_closure_checks'] += len(result['basis'])
            check(certify(H))
    # A completed-power shift can destroy affinity in Q. Recover the chart
    # through the common directional-Hessian equations instead.
    for degree in range(3, 7):
        for slope in (F(0), F(2, 3)):
            h = {(0, degree): F(1), (1, degree-1): F(2), (0, 0): F(1)}
            H = CT.tri(h, {2: F(1), 1: slope})
            chart = affine_chart(H)
            assert chart and chart['w'].get(1, F(0)) == slope
            assert CT.span_ok(H, recognize(H)['basis'])
            counts['ambiguous_completion_charts'] += 1
    cert = certify(CT.tri(cases[1], {2: F(1)}))
    for mutate in (lambda x: x['claim'].update(dimension=2),
                   lambda x: x['claim']['basis'].append({'0,1': '1'}),
                   lambda x: x['hamiltonian'].update({'0,0': '3'})):
        forged = copy.deepcopy(cert)
        mutate(forged)
        try:
            check(forged)
        except ValueError:
            counts['forgery_rejections'] += 1
        else:
            raise AssertionError('forged certificate accepted')
    for malformed in ({(0, -1): 1}, {(0, F(3, 2)): 1}, {(0, 3): 0.5},
                      {(0, 2): 1}, {(2, 2): 1, (0, 3): 1}):
        assert recognize(malformed) is None, malformed
        counts['invalid_input_rejections'] += 1
    return {'format': FORMAT, 'status': 'passed', 'checks': counts,
            'cases': sorted(seen), 'scope': 'Full affine-Q cubic-phase classification; exact rational chart recognition; all-degree proofs in the three cited notes.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    encoded = json.dumps(run(), indent=2)+'\n'
    if args.output:
        args.output.write_text(encoded)
    print(encoded)


if __name__ == '__main__':
    main()
