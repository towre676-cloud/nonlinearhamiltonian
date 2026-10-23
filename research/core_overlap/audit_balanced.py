#!/usr/bin/env python3
"""Independent boundary audit for the balanced-top induction.

The symbolic factorization is checked by Claude's existing checker.  This
separate checker uses only falling factorials and rational arithmetic, covers
top exponents s on BOTH sides of mu, and checks the polynomial-support boundary
where the partner monomial or the T3 output does not exist.
"""
from fractions import Fraction
from math import comb, prod
import json


def fall(n, r):
    return prod(n-j for j in range(r))


def transvectant3(a, b, c, d):
    return sum((-1)**j*comb(3,j)*fall(a,3-j)*fall(b,j)
               *fall(c,j)*fall(d,3-j) for j in range(4))


def audit(mu_max=12, s_max=20):
    matched = unmatched_x = unmatched_y = higher_s = negative_output = 0
    translations = 0
    for mu in range(2, mu_max+1):
        for s in range(1, s_max+1):
            if s == mu:
                continue
            for x in range(2*mu):
                for y in range(2*mu-x):
                    if x == y:
                        continue
                    k, u = 2*mu-x-y, x-y
                    aa, bb = x-mu+s, y-mu+s
                    # If X has no partner Y, the bracket already kills X.
                    if min(aa,bb) < 0:
                        assert s*(x-y) != 0
                        unmatched_x += 1
                        continue
                    matched += 1
                    higher_s += s > mu
                    omega = (Fraction(s,mu)*transvectant3(mu,mu,aa,bb)
                             + transvectant3(x,y,s,s))
                    A = u*u+3*k-4
                    R = A*(s+mu)-Fraction(3,2)*(u*u+k*k+2*k-4)
                    assert omega == s*(s-mu)*u*R
                    assert min(s,mu)*2 >= k+abs(u)
                    is_translation = k == 1 and abs(u) == 1
                    assert (R == 0) == is_translation
                    assert R > 0 or is_translation
                    assert (omega == 0) == is_translation
                    translations += is_translation
                    if min(x+s-3,y+s-3) < 0:
                        negative_output += 1
                        assert omega == 0 and is_translation
            # If Y has no partner X, its nonzero bracket coefficient kills Y.
            for aa in range(2*s):
                for bb in range(2*s-aa):
                    if aa == bb:
                        continue
                    x,y = aa+mu-s, bb+mu-s
                    if min(x,y) < 0:
                        assert mu*(aa-bb) != 0
                        unmatched_y += 1
    return {'status':'passed', 'mu_range':[2,mu_max], 's_range':[1,s_max],
            'matched_monomials':matched,'matched_with_s_greater_than_mu':higher_s,
            'unmatched_X_killed_by_bracket':unmatched_x,
            'unmatched_Y_killed_by_bracket':unmatched_y,
            'translation_zeros':translations,
            'negative_T3_outputs_all_translation_zeros':negative_output}


if __name__ == '__main__':
    print(json.dumps(audit(), indent=2))
