#!/usr/bin/env python3
"""Independent checker for fundamental-unit certificates of Z[sqrt D] (fundamental-unit-v1).

Claim: for nonsquare D >= 2, eps0 = a + b sqrt D is the smallest unit > 1 of Z[sqrt D]
(norm +1 or -1), and eps1 = a1 + b1 sqrt D is the smallest unit > 1 of norm +1.

Proof route. A unit x + y sqrt D > 1 with norm +-1 has x, y > 0 and
|x/y - sqrt D| = 1 / (y^2 (x/y + sqrt D)) < 1/(2 y^2), since x/y + sqrt D >= 1 + sqrt 2 > 2.
By Legendre's criterion x/y is then a convergent of the continued fraction of sqrt D, and
units are increasing in y. The checker therefore recomputes the convergents p_k/q_k of
sqrt D with exact integer arithmetic (the standard (m, d, a) recurrence) and verifies that
(a, b) is the first convergent of norm +-1 and (a1, b1) the first of norm +1. Every unit
of norm +1 is then +-eps1^j and every unit is +-eps0^j.

Usage: check_units.py CERT.json --input MODEL.json     (MODEL = {"D": D})
"""
from __future__ import annotations
import argparse
import hashlib
import json
import sys
from math import isqrt
from pathlib import Path

FORMAT = 'fundamental-unit-v1'


def digest(model):
    return hashlib.sha256(json.dumps(model, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def convergents(D):
    """Yield (p_k, q_k) for sqrt D, exact."""
    a0 = isqrt(D)
    m, d, a = 0, 1, a0
    p_prev, p = 1, a0
    q_prev, q = 0, 1
    yield p, q
    while True:
        m = d * a - m
        d = (D - m * m) // d
        a = (a0 + m) // d
        p_prev, p = p, a * p + p_prev
        q_prev, q = q, a * q + q_prev
        yield p, q


def icbrt(n):
    """Floor of the real cube root of an integer, exactly."""
    if n < 0:
        return -icbrt(-n) - (0 if icbrt(-n) ** 3 == -n else 1)
    x = int(round(n ** (1 / 3))) if n < 2 ** 1000 else 1 << (n.bit_length() // 3 + 1)
    while x ** 3 > n:
        x -= 1
    while (x + 1) ** 3 <= n:
        x += 1
    return x


def maximal(cert, D, eps, nrm):
    """Order O = Z[(1+sqrt D)/2], D = 1 mod 4 (the maximal order when D is squarefree): every unit cubed lies in Z[sqrt D] (the unit
    group of (O/2O) has order 1 or 3), so the fundamental unit eta satisfies eta = eps or
    eta^3 = eps. A cube root (u + v sqrt D)/2 has trace u, a root of t^3 - 3 nu t - 2a = 0 with
    nu = N(eps); the checker either verifies eta^3 = eps exactly or shows that this cubic has
    no integer root (it has a single real root, located strictly between consecutive integers)."""
    a, b = eps
    m = cert['maximal_order']
    if m['cube_root'] is None:
        nu = nrm
        f = lambda t: t ** 3 - 3 * nu * t - 2 * a
        t0 = icbrt(2 * a)
        # With nu = -1 the cubic is increasing; with nu = +1 and a >= 2 its local maximum
        # (at t = -1) is 2 - 2a < 0. Either way it has exactly one real root.
        if nu == 1 and a < 2:
            raise ValueError('cannot certify the absence of a cube root')
        root = next((t for t in range(t0 - 2, t0 + 3) if f(t) == 0), None)
        if root is None:
            if next((t for t in range(t0 - 2, t0 + 3) if f(t) < 0 < f(t + 1)), None) is None:
                raise ValueError('cannot locate the real root of the trace cubic')
        else:
            # integral trace u: a cube root would need v^2 = (u^2 - 4 nu)/D integral, square, u = v mod 2
            v2, r = divmod(root * root - 4 * nu, D)
            if not r and v2 >= 0 and isqrt(v2) ** 2 == v2 and (root - isqrt(v2)) % 2 == 0:
                raise ValueError('a cube root exists but was not declared')
        return {'maximal_unit': [2 * a, 2 * b], 'maximal_unit_is_integral': True}
    u, v = m['cube_root']
    if (u - v) % 2 or u * u - D * v * v != 4 * nrm or u < 1 or v < 1:
        raise ValueError('declared cube root is not a unit of the maximal order with the right norm')
    x, y = u, v                         # (x + y sqrt D)/2 = eta^k, start k = 1
    for _ in range(2):
        x, y = (x * u + D * y * v) // 2, (x * v + y * u) // 2
    if [x, y] != [2 * a, 2 * b]:
        raise ValueError('declared cube root does not cube to eps')
    return {'maximal_unit': [u, v], 'maximal_unit_is_integral': False}


def check(cert, model, max_steps=10 ** 6):
    if cert.get('format') != FORMAT or cert.get('model_sha256') != digest(model):
        raise ValueError('not a fundamental-unit-v1 certificate for this model')
    D = model['D']
    if type(D) is not int or D < 2 or isqrt(D) ** 2 == D:
        raise ValueError('D must be a nonsquare integer >= 2')
    a, b = cert['unit']
    a1, b1 = cert['norm_one_unit']
    if a * a - D * b * b not in (1, -1) or a1 * a1 - D * b1 * b1 != 1 or min(a, b, a1, b1) < 1:
        raise ValueError('declared units have the wrong norms')
    first = first_plus = None
    for steps, (p, q) in enumerate(convergents(D)):
        if steps > max_steps or q > b1:
            break
        nrm = p * p - D * q * q
        if nrm in (1, -1) and first is None:
            first = [p, q]
        if nrm == 1:
            first_plus = [p, q]
            break
    if first != [a, b] or first_plus != [a1, b1]:
        raise ValueError('declared units are not the first convergents of norm +-1 / +1')
    norm = a * a - D * b * b
    out = {'status': 'passed', 'D': D, 'fundamental_unit': [a, b], 'norm': norm,
           'norm_one_unit': [a1, b1], 'negative_pell_solvable': norm == -1,
           'scope': 'unit group of the order Z[sqrt D]'}
    if 'maximal_order' in cert:
        if D % 4 != 1:
            raise ValueError('maximal-order data only for D = 1 mod 4')
        mx = maximal(cert, D, [a, b], norm)
        u, v = mx['maximal_unit']
        nm = (u * u - D * v * v) // 4
        # smallest norm-one unit of the maximal order, in half-coordinates
        one = [u, v] if nm == 1 else [(u * u + D * v * v) // 2, u * v]
        out.update(maximal_order_unit_half_coordinates=[u, v], maximal_order_norm=nm,
                   maximal_order_norm_one_unit=one,
                   scope='unit groups of Z[sqrt D] and of Z[(1+sqrt D)/2] (the maximal order when D is '
                         'squarefree)')
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('certificate', type=Path)
    ap.add_argument('--input', type=Path, required=True)
    a = ap.parse_args()
    try:
        print(json.dumps(check(json.loads(a.certificate.read_text()), json.loads(a.input.read_text())), indent=2))
    except (ValueError, KeyError, TypeError) as e:
        print(json.dumps({'status': 'rejected', 'reason': str(e)}))
        sys.exit(2)


if __name__ == '__main__':
    main()
