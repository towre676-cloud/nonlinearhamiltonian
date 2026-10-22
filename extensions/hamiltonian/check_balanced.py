#!/usr/bin/env python3
"""Checker for the balanced-top theorem (balanced-top-v1).

Theorem B. Let H = H_d + P with deg P < d, d = 2 mu >= 4, and H_d = c Q^mu for a
nondegenerate quadratic form Q (over Qbar, H_d = c (qp)^mu). Then
    D_inf(H) = K[G]       if H lies in K[G] for some quadratic G with leading part Q,
    D_inf(H) = span{1, H} otherwise.

Proof (the checked identities are marked [B1]..[B4]).
 1. Work over Qbar with H_d = (qp)^mu. If D_inf(H) != span{1, H}, there is G in D_inf(H)
    with top (qp)^s, 1 <= s < mu (top-weight lemma with weight (1,1): tops lie in K[qp];
    subtract multiples of H). Translate H (affine covariance) so that the coefficients of
    q^mu p^(mu-1) and q^(mu-1) p^mu in H_(d-1) vanish: a translation adds
    mu (qp)^(mu-1) (x0 p + y0 q) to H_(d-1).
 2. Weights: H_(d-k) and G_(2s-k) have weight k. Call a monomial q^x p^y diagonal if x = y;
    the diagonal part of a form is its K[qp] part. Induction on k >= 1: the off-diagonal
    parts X of H_(d-k) and Y of G_(2s-k) vanish for smaller weights. Diagonal parts Poisson
    commute and have zero odd transvectants with each other ([B1]: psi_k(c, c) = 0 for
    H = (qp)^a), so at weight k only (H_d, Y) and (X, (qp)^s) contribute:
      D:   {H, G} has no component of weight < k; its weight-k component is its top, hence
           diagonal, but mu (qp)^(mu-1) L Y - s (qp)^(s-1) L X is off-diagonal (L = ad_qp is
           diagonal on monomials with eigenvalue y - x), so it vanishes: monomial-wise
           y_(x-mu+s, y-mu+s) = (s/mu) x_(x,y) (and x_(x,y) = 0 when an index is negative).
      T_3: T_3((qp)^mu, Y) + T_3(X, (qp)^s) = 0; with the D relation each off-diagonal
           monomial q^x p^y of X is multiplied by
             Omega = (s/mu) T3[(mu,mu) on (x-mu+s, y-mu+s)] + T3[(x,y) on (s,s)].
 3. [B2] Omega = s (s - mu)(x - y) R with, for u = x - y, k = 2 mu - (x + y),
             R = A (s + mu) - (3/2)(u^2 + k^2 + 2k - 4),   A = u^2 + 3k - 4.
    [B3] With a = |u| >= 1, k >= 1:
             2A(k + a) - 3(u^2 + k^2 + 2k - 4) = (a-1)(2a-1)(a+1) + (k-1)(2a^2 + 6a + 3k - 11),
    which is > 0 unless a = k = 1. The index conditions give s, mu >= (k + a)/2, so
    s + mu >= k + a, and R = 0 would need 2A(k+a) <= 3(u^2 + k^2 + 2k - 4): impossible
    unless a = k = 1, i.e. the two translation monomials of step 1, which were removed.
    Hence X = 0 and Y = 0 at every weight: H (translated) lies in K[qp].
 4. [B4] The T_3 coefficient formula used here agrees with weyl_receipts on a grid.

Usage: check_balanced.py [CERT.json]
"""
from __future__ import annotations
import json
import sys
from fractions import Fraction as F
from math import comb
from pathlib import Path

sys.path[:0] = [str(Path(__file__).resolve().parent), str(Path(__file__).resolve().parent.parent)]
import check_monomial_theorem as M   # noqa: E402  (polynomial arithmetic over symbols)

FORMAT = 'balanced-top-v1'


def ffn(z, k):
    out = 1
    for i in range(k):
        out *= (z - i)
    return out


def T3n(A, B, a, b):
    return sum((-1) ** l * comb(3, l) * ffn(A, 3 - l) * ffn(B, l) * ffn(a, l) * ffn(b, 3 - l) for l in range(4))


def identities():
    # use the symbol slots of check_monomial_theorem: a -> mu, b -> s, c -> x, e -> y, r -> k, l -> u
    V, cst, padd, pmul = M.V, M.cst, M.padd, M.pmul
    mu, s, x, y = V('a'), V('b'), V('c'), V('e')
    neg = lambda p: pmul(cst(-1), p)
    shift = padd(s, neg(mu))
    om = padd(pmul(s, M.psi(3, padd(x, shift), padd(y, shift), A=mu, B=mu)),
              pmul(mu, M.psi(3, s, s, A=x, B=y)))                    # mu * Omega
    u = padd(x, neg(y))
    k = padd(pmul(cst(2), mu), neg(x), neg(y))
    A = padd(pmul(u, u), pmul(cst(3), k), cst(-4))
    R = padd(pmul(A, padd(s, mu)), pmul(cst(F(-3, 2)), padd(pmul(u, u), pmul(k, k), pmul(cst(2), k), cst(-4))))
    res = {'B1': all(M.psi(kk, x, x, B=V('a')) == {} for kk in (3, 5, 7)),
           'B2': om == pmul(mu, s, shift, u, R)}
    # B3 in symbols a (slot 'a'), k (slot 'r')
    a, kk = V('a'), V('r')
    A2 = padd(pmul(a, a), pmul(cst(3), kk), cst(-4))
    lhs = padd(pmul(cst(2), A2, padd(kk, a)), pmul(cst(-3), padd(pmul(a, a), pmul(kk, kk), pmul(cst(2), kk), cst(-4))))
    rhs = padd(pmul(padd(a, cst(-1)), padd(pmul(cst(2), a), cst(-1)), padd(a, cst(1))),
               pmul(padd(kk, cst(-1)), padd(pmul(cst(2), a, a), pmul(cst(6), a), pmul(cst(3), kk), cst(-11))))
    res['B3'] = lhs == rhs
    return res


def grid():
    import weyl_receipts as W
    n = 0
    for (A, B) in ((3, 3), (2, 4), (5, 1)):
        Hm = {(A, B): F(1)}
        C3 = W.gate(Hm, 3)
        for a in range(0, 6):
            for b in range(0, 6):
                img = W.act(C3, {(a, b): F(1)})
                want = T3n(A, B, a, b)
                got = img.get((A + a - 3, B + b - 3), F(0))
                if got != want:
                    return False, n
                n += 1
    return True, n


def check(cert=None):
    if cert is not None and cert.get('format') != FORMAT:
        raise ValueError('not a balanced-top-v1 certificate')
    res = identities()
    ok, n = grid()
    res['B4'] = ok
    bad = [k for k, v in res.items() if not v]
    if bad:
        raise ValueError(f'identities fail: {bad}')
    if cert is not None and cert.get('identities') != sorted(res):
        raise ValueError('certificate lists other identities')
    # spot-check of the positivity claim used in step 3
    for a in range(1, 40):
        for k in range(1, 40):
            f = (a - 1) * (2 * a - 1) * (a + 1) + (k - 1) * (2 * a * a + 6 * a + 3 * k - 11)
            if (f <= 0) != (a == 1 and k == 1):
                raise ValueError('positivity fails')
    return {'status': 'passed', 'identities': sorted(res), 'grid_points': n,
            'theorem': 'balanced top c Q^mu with lower-order terms: D_inf = K[G] if H in K[G] for a quadratic G, '
                       'else span{1, H}'}


def main():
    try:
        cert = json.loads(open(sys.argv[1]).read()) if len(sys.argv) > 1 else None
        print(json.dumps(check(cert), indent=1))
    except (ValueError, KeyError) as e:
        print(json.dumps({'status': 'rejected', 'reason': str(e)}))
        sys.exit(2)


if __name__ == '__main__':
    main()
