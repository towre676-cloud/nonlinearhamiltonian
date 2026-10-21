#!/usr/bin/env python3
"""Independent checker for top-weight reduction certificates (weyl-top-reduction-v1).

Lemma (top-weight reduction). Let w be a positive integer weight on (q,p) and write
H = H_w + H_<, where H_w collects the terms of maximal weight h and H_< has strictly
smaller weight. For G in D_inf(H) with top weighted component G_top,
    G_top lies in D_inf(H_w).
Proof: the gates and D are linear in H, and the top weighted parts of C_k(H) and D_H are
C_k(H_w) and D_(H_w). The weight-(m + shifts) component of C_k(H) D_H^r G is therefore
C_k(H_w) D_(H_w)^r G_top, and it vanishes because the whole expression vanishes. The
gates of H_w are among the odd orders considered for H. Hence gr D_inf(H) embeds in
D_inf(H_w).

Two conclusions are certified:
  finite  D_inf(H_w) = span{1, H_w} with h > 0 (an embedded weyl-kernel-v1 certificate of
          dimension 2). Then dim D_inf(H) <= 2. Since 1 and H always lie in D_inf(H)
          (D H = 0, T_k(H,H) = 0 for odd k), D_inf(H) = span{1, H}.
  lines   D_inf(H_w) = V, the sum of q^i Q[p] for i in I (an embedded monomial_span
          certificate whose zero set is exactly these vertical lines). The checker proves
          V <= D_inf(H) symbolically in the p-exponent j: every gate C_k(H) kills q^i p^j
          for all j, and D_H maps q^i p^j into V for all j. Because V is spanned by
          w-homogeneous monomials, subtracting top components inside V descends to
          D_inf(H) = V.
Usage: check_top_reduction.py CERT.json
"""
from __future__ import annotations
import json
import sys
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import weyl_receipts as W        # noqa: E402  (gate/derivation definitions, receipt replay)
import check_weyl_kernel as K    # noqa: E402  (all-degree kernel checker)

FORMAT = 'weyl-top-reduction-v1'


def wt(e, w):
    return w[0] * e[0] + w[1] * e[1]


def _jfall(i, d):
    """(j - i0)... as a univariate polynomial: (j)_d."""
    out = {0: F(1)}
    for t in range(d):
        nxt = {}
        for e, c in out.items():
            nxt[e + 1] = nxt.get(e + 1, F(0)) + c
            nxt[e] = nxt.get(e, F(0)) - t * c
        out = {e: c for e, c in nxt.items() if c}
    return out


def line_images(op, i):
    """op applied to q^i p^j, grouped by output (q-exponent, p-shift): polynomials in j."""
    groups = {}
    for (x, y, c, d), v in op.items():
        if c > i:
            continue
        coef = v
        for t in range(c):
            coef *= (i - t)
        key = (i + x - c, y - d)
        poly = groups.setdefault(key, {})
        for e, u in _jfall(i, d).items():
            poly[e] = poly.get(e, F(0)) + coef * u
    return {k: {e: c for e, c in p.items() if c} for k, p in groups.items()}


def check(cert):
    if cert.get('format') != FORMAT or cert.get('coefficient_domain') != 'Q':
        raise ValueError('not a weyl-top-reduction-v1 certificate over Q')
    H = W.read_terms(cert['hamiltonian'], 2)
    w = cert['weight']
    if len(w) != 2 or any(type(x) is not int or x < 1 for x in w):
        raise ValueError('weight must be two positive integers')
    if not H:
        raise ValueError('H must be nonzero')
    h = max(wt(e, w) for e in H)
    Hw = {e: c for e, c in H.items() if wt(e, w) == h}
    top = cert['top_certificate']
    if W.read_terms(top['receipt']['hamiltonian'], 2) != Hw:
        raise ValueError('embedded certificate is not for the weighted top part of H')
    res = K.check(top)
    claim = cert['claim']
    if claim == 'finite':
        if h == 0 or res['kind'] not in ('finite_support', 'degree_bound') or res['dimension'] != 2:
            raise ValueError('finite reduction needs D_inf(H_w) of dimension 2 and positive weight')
        basis = [W.read_terms(g, 2) for g in top['claim']['basis']]
        anchor = next(iter(Hw))
        # Both basis elements lie in span{1, H_w}; with dimension 2 the spans coincide.
        for g in basis:
            rest = {e: c for e, c in g.items() if e != (0, 0)}
            lam = rest.get(anchor, F(0)) / Hw[anchor]
            if rest != {e: lam * c for e, c in Hw.items() if lam * c}:
                raise ValueError('top kernel is not span{1, H_w}')
        return {'status': 'passed', 'claim': 'finite', 'core': 'span{1, H}', 'weight': w,
                'top_part': [[a, b, str(c)] for (a, b), c in sorted(Hw.items())],
                'scope': 'full dynamic core of H in all degrees, over Q'}
    if claim != 'lines':
        raise ValueError('unknown claim')
    tc = top['claim']
    if res['kind'] != 'monomial_span' or tc['horizontal_lines'] or tc['progressions'] or \
            any(a not in tc['vertical_lines'] for a, _ in tc['points']):
        raise ValueError('lines reduction needs a top core made only of vertical lines')
    I = set(tc['vertical_lines'])
    D = W.derivation(H)
    gates = W.gates(H)
    for i in I:
        for k, Ck in gates.items():
            if any(line_images(Ck, i).values()):
                raise ValueError(f'gate {k} does not kill q^{i} Q[p]')
        for (qe, _), poly in line_images(D, i).items():
            if poly and qe not in I:
                raise ValueError(f'D maps q^{i} Q[p] outside the declared lines')
    return {'status': 'passed', 'claim': 'lines', 'core': [f'q^{i}*Q[p]' for i in sorted(I)], 'weight': w,
            'scope': 'full dynamic core of H in all degrees, over Q'}


if __name__ == '__main__':
    try:
        print(json.dumps(check(json.loads(Path(sys.argv[1]).read_text())), indent=2))
    except (ValueError, KeyError, TypeError, IndexError, ZeroDivisionError) as e:
        print(json.dumps({'status': 'rejected', 'reason': str(e)}))
        sys.exit(2)
