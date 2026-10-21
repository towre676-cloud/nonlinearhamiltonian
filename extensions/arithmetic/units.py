#!/usr/bin/env python3
"""Fundamental unit of Z[sqrt D] from the continued fraction of sqrt D (producer).

Usage: units.py D [--output CERT.json]
"""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import check_units as C  # noqa: E402


def fundamental(D, max_steps=10 ** 6):
    model = {'D': D}
    if type(D) is not int or D < 2 or C.isqrt(D) ** 2 == D:
        raise ValueError('D must be a nonsquare integer >= 2')
    first = None
    for steps, (p, q) in enumerate(C.convergents(D)):
        if steps > max_steps:
            return None, model
        nrm = p * p - D * q * q
        if nrm in (1, -1) and first is None:
            first = [p, q]
        if nrm == 1:
            cert = {'format': C.FORMAT, 'model_sha256': C.digest(model), 'unit': first, 'norm_one_unit': [p, q]}
            cert['result'] = C.check(cert, model, max_steps)
            return cert, model


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('D', type=int)
    ap.add_argument('--output', type=Path)
    a = ap.parse_args()
    try:
        cert, _ = fundamental(a.D)
    except ValueError as e:
        print(json.dumps({'status': 'invalid_model', 'reason': str(e)}))
        sys.exit(2)
    if cert is None:
        print(json.dumps({'status': 'unknown', 'reason': 'step budget exhausted'}))
        sys.exit(3)
    if a.output:
        a.output.write_text(json.dumps(cert, indent=1) + '\n')
    print(json.dumps(cert['result'], indent=2))


if __name__ == '__main__':
    main()
