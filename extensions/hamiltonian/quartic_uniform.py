#!/usr/bin/env python3
"""Produce the quartic-uniform-v1 certificate (all-degree theorem for distinct-root quartics).

It records the re-derivable top-equation coefficients, the two resultants in l, a threshold
from which the symbolic formulas apply, and embeds the per-degree certificate for the
degrees below the threshold. check_quartic_uniform.py recomputes every item.

Usage: quartic_uniform.py [--output CERT.json] [--small N]
"""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parent)]
import check_quartic_uniform as C   # noqa: E402
import quartic_rigidity as QR       # noqa: E402

THRESHOLD = 8      # symbolic top equations agree with the exact ones for every n >= 8


def build(small=12):
    odd = C.top_equations([1])
    even = C.top_equations([0, 2])
    c1, c3 = odd[1].coef.get(1, {}), odd[3].coef.get(1, {})
    rows = [(even[t].coef.get(0, {}), even[t].coef.get(2, {})) for t in (0, 2, 4)]
    m01 = C.padd(C.pmul(rows[0][0], rows[1][1]), C.psc(C.pmul(rows[1][0], rows[0][1]), -1))
    m02 = C.padd(C.pmul(rows[0][0], rows[2][1]), C.psc(C.pmul(rows[2][0], rows[0][1]), -1))
    r01, r02 = C.divide_by_l2m4(m01), C.divide_by_l2m4(m02)
    (dl1, dn1), (dl3, dn3) = C.degs(c1), C.degs(c3)
    (da, dna), (db, dnb) = C.degs(r01), C.degs(r02)
    R1 = C.resultant_poly(c1, c3, dl3 * dn1 + dl1 * dn3)
    R2 = C.resultant_poly(r01, r02, db * dna + da * dnb)
    smallcert = QR.build(small)
    smallcert.pop('result', None)
    cert = {'format': C.FORMAT, 'family': 'q^4 + l*q^2*p^2 + p^4', 'threshold': THRESHOLD,
            'odd_coefficients': [sorted([list(k), str(v)] for k, v in x.items()) for x in (c1, c3)],
            'R1': [str(c) for c in R1], 'R2': [str(c) for c in R2], 'small_degree_certificate': smallcert}
    cert['odd_coefficients'] = [[[list(k), str(v)] for k, v in sorted(x.items())] for x in (c1, c3)]
    cert['result'] = C.check(cert)
    return cert


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--output', type=Path)
    ap.add_argument('--small', type=int, default=12)
    a = ap.parse_args()
    cert = build(a.small)
    if a.output:
        a.output.write_text(json.dumps(cert, indent=1) + '\n')
    print(json.dumps(cert['result'], indent=1))


if __name__ == '__main__':
    main()
