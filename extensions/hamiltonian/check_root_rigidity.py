#!/usr/bin/env python3
"""Root-rigidity certificates for polynomial Hamiltonians (root-rigidity-v1).

Given a rational polynomial H of degree d >= 3 whose top homogeneous part H_d has root type
lambda over Qbar, the checker verifies a declared square-free decomposition of H_d, derives
lambda, and applies the proved routes of DYNAMIC_CORE_RESULTS.md section 5:

  two distinct roots or fewer   monomial theorem (check_monomial_theorem.py) + GL2 transport
  >= 3 roots, some multiplicity mu with 2 <= mu <= d-2, mu != d/2      Theorem R1
  >= 3 roots, d odd >= 5 (then H_d is square-free)                      Theorem R2
  >= 3 roots, d = 3 (square-free cubic)                                  Theorem R3
  d = 4: (2,1,1) and (1^4)                                               W3 (section 3c)
  d = 6: (3,1,1,1) and (1^6)                                             W4 (section 3d)
  otherwise (d even >= 8, types (1^d) and (d/2, 1^(d/2)))               open

When H_d has at least three distinct roots and a route applies, D_inf(H_d) = span{1, H_d},
and the perturbation corollary gives D_inf(H) = span{1, H} for the full H = H_d + P,
deg P < d. A homogeneous H with at most two roots receives its monomial-class core.

Square-free decomposition. With f(x) = H_d(x, 1) and mu_inf = d - deg f (the multiplicity
of the root (1:0)), the certificate gives c and square-free polynomials S_1, ..., S_m with
f = c prod S_i^i; the checker verifies the product, that every S_i is monic and square-free
(gcd(S_i, S_i') = 1) and that the S_i are pairwise coprime. Then f has deg S_i roots of
multiplicity i over Qbar.

Usage: check_root_rigidity.py CERT.json
"""
from __future__ import annotations
import json
import sys
from fractions import Fraction as F

FORMAT = 'root-rigidity-v1'

# ---- univariate polynomials over Q: lists, lowest degree first --------------------------


def norm(p):
    p = [F(c) for c in p]
    while p and p[-1] == 0:
        p.pop()
    return p


def umul(a, b):
    if not a or not b:
        return []
    out = [F(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return norm(out)


def udivmod(a, b):
    a, b = norm(a), norm(b)
    q = [F(0)] * max(len(a) - len(b) + 1, 0)
    while len(a) >= len(b) and a:
        c = a[-1] / b[-1]
        k = len(a) - len(b)
        q[k] = c
        for i, y in enumerate(b):
            a[i + k] -= c * y
        a = norm(a)
    return norm(q), a


def ugcd(a, b):
    a, b = norm(a), norm(b)
    while b:
        a, b = b, udivmod(a, b)[1]
    return [c / a[-1] for c in a] if a else []


def deriv(a):
    return norm([i * c for i, c in enumerate(a)][1:])


def yun(f):
    """Square-free decomposition f = c prod S_i^i (Yun)."""
    f = norm(f)
    c = f[-1]
    f = [x / c for x in f]
    out = []
    a0 = ugcd(f, deriv(f))
    b = udivmod(f, a0)[0]
    cc = udivmod(deriv(f), a0)[0]
    dd = norm([x - y for x, y in zip(cc + [F(0)] * len(b), deriv(b) + [F(0)] * len(cc))])
    while len(b) > 1:
        a = ugcd(b, dd)
        out.append(a)
        b = udivmod(b, a)[0]
        cc = udivmod(dd, a)[0]
        dd = norm([x - y for x, y in zip(cc + [F(0)] * len(b), deriv(b) + [F(0)] * len(cc))])
    while out and len(out[-1]) == 1:
        out.pop()
    return c, out


# ---- Hamiltonians: {(i, j): coefficient} for q^i p^j -------------------------------------


def parse_h(h):
    return {tuple(map(int, k.split(','))): F(v) for k, v in h.items() if F(v)}


def top_part(H):
    d = max(i + j for i, j in H)
    return d, {k: v for k, v in H.items() if sum(k) == d}


def dehom(Hd, d):
    f = [F(0)] * (d + 1)
    for (i, j), v in Hd.items():
        f[i] += v                      # H_d(x, 1): q^i p^j -> x^i
    return norm(f)


def route(lam, d):
    roots = len(lam)
    if roots <= 2:
        return 'monomial'
    if any(2 <= m <= d - 2 and 2 * m != d for m in lam):
        return 'R1'
    if d % 2 == 1:
        return 'R2' if d >= 5 else 'R3'
    if d == 4:
        return 'W3'
    if d == 6:
        return 'W4'
    return 'open'


def monomial_core(lam, d):
    if len(lam) == 1:
        return 'sum_{j<=2} M^j Q[L]  (H = c L^d)'
    a, b = max(lam), min(lam)
    if b == 1:
        return 'Q[L] + M Q[L]  (H = c L^(d-1) M)'
    if a == b:
        return 'Q[Q2]  (H = c Q2^(d/2))'
    return 'span{1, LM, H}  (H = c L^a M^b)'


def check(cert):
    if cert.get('format') != FORMAT:
        raise ValueError('not a root-rigidity-v1 certificate')
    H = parse_h(cert['hamiltonian'])
    d, Hd = top_part(H)
    if d < 3:
        raise ValueError('degree must be at least 3')
    f = dehom(Hd, d)
    mu_inf = d - (len(f) - 1)
    c = F(cert['leading'])
    S = [norm(s) for s in cert['squarefree']]
    prod = [c]
    for i, s in enumerate(S, start=1):
        if s and s[-1] != 1:
            raise ValueError('square-free factors must be monic')
        if len(s) > 1 and len(ugcd(s, deriv(s))) > 1:
            raise ValueError('a declared factor is not square-free')
        for _ in range(i):
            prod = umul(prod, s)
    if prod != f:
        raise ValueError('declared decomposition does not multiply to H_d(x, 1)')
    for i in range(len(S)):
        for j in range(i + 1, len(S)):
            if len(S[i]) > 1 and len(S[j]) > 1 and len(ugcd(S[i], S[j])) > 1:
                raise ValueError('declared factors are not coprime')
    lam = []
    for i, s in enumerate(S, start=1):
        lam += [i] * (len(s) - 1)
    if mu_inf:
        lam.append(mu_inf)
    lam = sorted(lam, reverse=True)
    rt = route(lam, d)
    homogeneous = all(sum(k) == d for k in H)
    out = {'status': 'passed', 'degree': d, 'root_type': lam, 'route': rt, 'homogeneous': homogeneous}
    if rt == 'open':
        out['core'] = 'not determined (open stratum: even degree >= 8, type (1^d) or (d/2, 1^(d/2)))'
        out['active_part'] = 'unknown'
    elif rt == 'monomial':
        if homogeneous:
            out['core'] = monomial_core(lam, d)
            out['active_part'] = ('nonzero' if not (len(lam) == 2 and lam[0] == lam[1]) else '0 (all stationary)')
        else:
            out['core'] = 'not determined by the perturbation corollary (top part has at most two roots)'
            out['active_part'] = 'unknown'
    else:
        out['core'] = 'span{1, H}'
        out['active_part'] = '0: no nonstationary observable is exact under repeated evolution'
        if not homogeneous:
            out['via'] = 'perturbation corollary: D_inf(H_d) = span{1, H_d} and deg(H - H_d) < d'
    return out


def certify(H):
    """Producer: H as {(i, j): Fraction}."""
    d, Hd = top_part(H)
    c, S = yun(dehom(Hd, d))
    cert = {'format': FORMAT, 'hamiltonian': {f'{i},{j}': str(v) for (i, j), v in sorted(H.items())},
            'leading': str(c), 'squarefree': [[str(x) for x in s] for s in S]}
    cert['result'] = check(cert)
    return cert


def main():
    try:
        print(json.dumps(check(json.loads(open(sys.argv[1]).read())), indent=1))
    except (ValueError, KeyError) as e:
        print(json.dumps({'status': 'rejected', 'reason': str(e)}))
        sys.exit(2)


if __name__ == '__main__':
    main()
