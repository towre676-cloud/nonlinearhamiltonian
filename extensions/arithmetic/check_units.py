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
    return {'status': 'passed', 'D': D, 'fundamental_unit': [a, b], 'norm': norm,
            'norm_one_unit': [a1, b1], 'negative_pell_solvable': norm == -1,
            'scope': 'unit group of the order Z[sqrt D] (not the maximal order when D = 1 mod 4)'}


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
