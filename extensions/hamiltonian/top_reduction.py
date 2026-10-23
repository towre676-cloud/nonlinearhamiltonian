#!/usr/bin/env python3
"""Produce a weyl-top-reduction-v1 certificate: certify D_inf(H_w) for the weighted top part
H_w of H with the Groebner backend and the kernel classifier, then let check_top_reduction.py
transfer it to H (see the lemma there).

Usage: top_reduction.py "q*p^3 + 3*q^2 - 2*q*p + p^2/1 + 5*q - p" --weight 3 1 [--output CERT.json]
"""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import weyl_receipts as W            # noqa: E402
import weyl_groebner as G            # noqa: E402
import weyl_kernel as KP             # noqa: E402
import check_top_reduction as C      # noqa: E402

_top_cache = {}


def reduce(H, weight, **budget):
    h = max(C.wt(e, weight) for e in H)
    Hw = {e: c for e, c in H.items() if C.wt(e, weight) == h}
    key = (tuple(sorted(Hw.items())), tuple(budget.items()))
    if key not in _top_cache:
        meta, receipt = G.discover(Hw, **budget)
        if receipt is None:
            return {'status': 'unknown', 'reason': 'top part: ' + meta['reason']}, None
        kmeta, kobj = KP.classify(receipt)
        if kobj is None:
            return {'status': 'unclassified', 'reason': 'top part: ' + kmeta['reason']}, None
        _top_cache[key] = kobj
    kobj = _top_cache[key]
    kind = kobj['claim']['kind']
    cert = {'format': C.FORMAT, 'coefficient_domain': 'Q', 'weight': list(weight),
            'hamiltonian': [[a, b, str(c)] for (a, b), c in sorted(H.items())],
            'top_certificate': kobj, 'claim': 'lines' if kind == 'monomial_span' else 'finite'}
    try:
        return {**C.check(cert), 'status': 'certified'}, cert
    except ValueError as e:
        return {'status': 'not_transferable', 'reason': str(e)}, None


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('hamiltonian')
    ap.add_argument('--weight', type=int, nargs=2, required=True)
    ap.add_argument('--output', type=Path)
    a = ap.parse_args()
    meta, cert = reduce(G.parse_poly(a.hamiltonian), a.weight)
    if cert and a.output:
        a.output.write_text(json.dumps(cert, indent=1) + '\n')
    print(json.dumps(meta, indent=2))
    sys.exit(0 if cert else 3)


if __name__ == '__main__':
    main()
