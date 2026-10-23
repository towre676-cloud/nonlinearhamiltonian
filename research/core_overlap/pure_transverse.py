#!/usr/bin/env python3
"""Exact pure-top / unequal perfect-power transverse classification.

All-degree statements use the proof in pure_perfect_power.md and the retained
unequal-monomial theorem. Finite matrices below are cross-checks, not proofs.
The classifier accepts H={(q_exponent,p_exponent): rational_coefficient} in
coordinates where the total top is c*q**d. Python standard library only.
"""
from __future__ import annotations

import json
import random
import sys
from fractions import Fraction as F
from math import comb, factorial
from pathlib import Path


def tidy(P):
    return {tuple(k): F(v) for k, v in P.items() if v}


def add(*polys):
    ans = {}
    for P in polys:
        for k, v in P.items():
            ans[k] = ans.get(k, F(0)) + v
    return tidy(ans)


def scale(P, c):
    return tidy({k: c*v for k, v in P.items()})


def mul(P, Q):
    ans = {}
    for (i, j), a in P.items():
        for (k, l), b in Q.items():
            z = (i+k, j+l)
            ans[z] = ans.get(z, F(0)) + a*b
    return tidy(ans)


def power(P, n):
    ans = {(0, 0): F(1)}
    for _ in range(n):
        ans = mul(ans, P)
    return ans


def deriv(P, a=0, b=0):
    return {(i-a, j-b): v*(factorial(i)//factorial(i-a))*(factorial(j)//factorial(j-b))
            for (i, j), v in P.items() if i >= a and j >= b}


def bracket(H, G):
    return add(mul(deriv(H, 1), deriv(G, 0, 1)),
               scale(mul(deriv(H, 0, 1), deriv(G, 1)), -1))


def transvectant(H, G, k):
    return add(*(scale(mul(deriv(H, k-j, j), deriv(G, j, k-j)),
                       (-1)**j*comb(k, j)) for j in range(k+1)))


def shift_q(H, c):
    """H(q+c,p)."""
    ans = {}
    for (i, j), v in H.items():
        for k in range(i+1):
            z = (k, j)
            ans[z] = ans.get(z, F(0)) + v*comb(i, k)*c**(i-k)
    return tidy(ans)


def uder(P):
    return {i-1: F(i)*v for i, v in P.items() if i}


def uadd(*polys):
    ans = {}
    for P in polys:
        for i, v in P.items():
            ans[i] = ans.get(i, F(0)) + v
    return {i: v for i, v in ans.items() if v}


def umul(P, Q):
    ans = {}
    for i, a in P.items():
        for j, b in Q.items():
            ans[i+j] = ans.get(i+j, F(0)) + a*b
    return {i: v for i, v in ans.items() if v}


def uscale(P, c):
    return {i: c*v for i, v in P.items() if c*v}


def terms(P):
    return [[*k, str(v)] for k, v in sorted(P.items())]


def classify(H):
    """Return None outside scope; otherwise a proved 2- or 3-dimensional core.

    No bounded-degree search is involved. Any coefficient field supporting
    exact Fraction coercion is accepted; output coefficients are rational.
    """
    H = tidy(H)
    if not H:
        return None
    d = max(sum(k) for k in H)
    if d < 3 or {(i, j) for i, j in H if i+j == d} != {(d, 0)}:
        return None
    s = max(j for i, j in H)
    if s < 2:
        return None
    phi = {i: v for (i, j), v in H.items() if j == s}
    r = max(phi)
    if r < 2 or r == s:
        return None
    alpha = phi[r]
    gamma = phi.get(r-1, F(0))/(r*alpha)
    if phi != {i: alpha*comb(r, i)*gamma**(r-i)
               for i in range(r+1) if alpha*comb(r, i)*gamma**(r-i)}:
        return None
    ans = {'scope': 'pure total top; unequal perfect-power transverse top',
           'proved': True, 'route': 'PP', 'degree': d, 'r': r, 's': s,
           'gamma': str(gamma), 'dimension': 2, 'core': 'span{1, H}',
           'active_part': '0', 'proof': 'pure_perfect_power.md'}
    if s >= 3:
        ans['reason'] = 'T3 forbids a nonquadratic third element when p-degree >= 3'
        return ans
    # Work in t=q+gamma, i.e. substitute q=t-gamma into the original H.
    Ht = shift_q(H, -gamma)
    B = {i: v for (i, j), v in Ht.items() if j == 1}
    C = {i: v for (i, j), v in Ht.items() if j == 0}
    a = F(r-2)
    b = -a*B.get(1, F(0))
    numerator = {i: F(i-r+1)*v for i, v in B.items() if (i-r+1)*v}
    numerator = uadd(numerator, {1: -b} if b else {})
    if any(i < r for i in numerator):
        ans['reason'] = 'closure p coefficient has no polynomial antiderivative'
        return ans
    up = {i-r: v/(2*alpha) for i, v in numerator.items()}
    u = {i+1: v/(i+1) for i, v in up.items()}
    residual = uadd({i: i*v for i, v in C.items() if i},
                    uscale(umul(B, up), -1), uscale(C, -a), uscale(u, -b))
    if any(i != 0 for i in residual):
        ans['reason'] = 'closure constant coefficient is not constant'
        return ans
    c = residual.get(0, F(0))
    Jt = add({(1, 1): F(1)}, {(i, 0): v for i, v in u.items()})
    J = shift_q(Jt, gamma)
    # Replay the defining identities in the original canonical coordinates.
    assert bracket(H, J) == add(scale(H, a), scale(J, b), {(0, 0): c})
    assert max((i for i in u), default=-1) >= 3
    for k in range(3, d+1, 2):
        assert not transvectant(H, J, k)
    ans.update(dimension=3, core='span{1, H, J}', J=terms(J),
               active_part='K*J modulo stationary span{1,H}',
               closure={'a': str(a), 'b': str(b), 'c': str(c)},
               reason='exact polynomial closure and every odd gate verified')
    return ans


def family(a=1, u=None, coeffs=(1, 0, 0), beta=0, delta=0, gamma=0):
    """Generate the complete exceptional family in the theorem's coordinates."""
    if u is None:
        u = {3: F(1)}
    J = add({(1, 1): F(1)}, {(i, 0): F(v) for i, v in u.items()})
    P = add(scale(power(J, 2), F(coeffs[0])), scale(J, F(coeffs[1])),
            {(0, 0): F(coeffs[2])})
    H = add(mul({(a, 0): F(1)}, P), scale(J, F(beta)), {(0, 0): F(delta)})
    return shift_q(H, F(gamma)), shift_q(J, F(gamma))


def self_test():
    """Exact structural tests plus independent PBW convention checks."""
    root = Path(__file__).resolve().parents[2]
    sys.path.insert(0, str(root/'extensions'/'hamiltonian'))
    import weyl_receipts as W
    rng = random.Random(20261022)
    fixtures = []
    checks = {'family_instances': 0, 'direct_gate_identities': 0,
              'closure_iterates': 0, 'rejected_perturbations': 0,
              's_ge_3_instances': 0, 'independent_operator_checks': 0}
    for n in (3, 4, 5):
        for a in (1, 2, 4):
            for gamma in (F(0), F(2, 3)):
                u = {n: F(rng.choice((-2, 1, 3))), 1: F(rng.randint(-2, 2)),
                     2: F(rng.randint(-2, 2))}
                coeffs = (F(rng.choice((-2, 1, 3))), F(rng.randint(-2, 2)),
                          F(rng.randint(-2, 2)))
                beta, delta = F(rng.randint(-2, 2)), F(rng.randint(-2, 2))
                H, J = family(a, u, coeffs, beta, delta, gamma)
                res = classify(H)
                assert res['dimension'] == 3, (H, res)
                Jr = W.read_terms(res['J'], 2)
                # Normalization may subtract the harmless constant u(gamma).
                assert not deriv(add(Jr, scale(J, -1)), 1)
                assert not deriv(add(Jr, scale(J, -1)), 0, 1)
                d = max(sum(k) for k in H)
                Q = Jr
                for depth in range(6):
                    for k in range(3, d+1, 2):
                        gate_value = transvectant(H, Q, k)
                        assert gate_value == W.act(W.gate(H, k), Q) == {}
                        checks['direct_gate_identities'] += 1
                        checks['independent_operator_checks'] += 1
                    direct_next = bracket(H, Q)
                    assert direct_next == W.act(W.derivation(H), Q)
                    Q = direct_next
                    checks['closure_iterates'] += 1
                # A low-order perturbation can preserve the top hypotheses
                # while breaking the exact third-element closure.
                bad = add(H, {(0, 1): F(1)})
                bad_res = classify(bad)
                assert bad_res['dimension'] == 2, (bad, bad_res)
                checks['rejected_perturbations'] += 1
                checks['family_instances'] += 1
                if n == 3 and a == 1:
                    fixtures.append({'H': terms(H), 'result': res})
    # Unequal transverse powers of p-degree >=3: the classification collapses
    # even with an arbitrarily high pure term or a translated root form.
    for r, s in ((2, 3), (3, 4), (4, 3), (2, 5), (5, 2)):
        for gamma in (F(0), F(-3, 2)):
            d = r+s+2
            H = shift_q({(r, s): F(1), (d, 0): F(1)}, gamma)
            res = classify(H)
            assert res and res['dimension'] == 2
            checks['s_ge_3_instances' if s >= 3 else 'rejected_perturbations'] += 1
    H, J = family()
    assert H == {(3, 2): F(1), (5, 1): F(2), (7, 0): F(1)}
    assert bracket(H, J) == H
    assert classify(H)['dimension'] == 3
    # Scope refuses balanced transverse powers and non-pure total tops.
    assert classify({(6, 0): 1, (2, 2): 1}) is None
    Hq, Jq = family(u={2: 1})
    assert classify(Hq) is None
    assert classify({(7, 0): 1, (3, 2): 1, (1, 2): 1}) is None
    return {'status': 'passed', 'checks': checks, 'minimal_counterexample': {
                'H': terms(H), 'J': terms(J), 'result': classify(H)},
            'fixtures': fixtures,
            'limits': 'The proof uses the retained all-degree unequal-monomial theorem; no literature-priority claim.'}


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', nargs='?', help='optional result JSON path')
    parser.add_argument('--classify', metavar='JSON',
                        help='read a list of [q exponent,p exponent,rational] terms')
    args = parser.parse_args()
    if args.classify:
        rows = json.loads(Path(args.classify).read_text())
        if isinstance(rows, dict):
            rows = rows['hamiltonian']
        H = {}
        for row in rows:
            if (len(row) != 3 or any(type(x) is not int or x < 0 for x in row[:2])
                    or type(row[2]) not in (int, str)):
                raise ValueError('terms must be [nonnegative integer, nonnegative integer, exact rational]')
            k = tuple(row[:2])
            H[k] = H.get(k, F(0)) + F(row[2])
        result = classify(H)
        if result is None:
            result = {'status': 'outside scope', 'proved': False}
    else:
        result = self_test()
    if args.output:
        Path(args.output).write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))
