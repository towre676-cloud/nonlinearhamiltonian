"""All-degree quartic theorem: symbolic top equations versus direct computation, forgeries."""
import copy
import json
import random
import sys
import unittest
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parent)]
import weyl_receipts as W            # noqa: E402
import check_quartic_uniform as C    # noqa: E402
import quartic_uniform as QU         # noqa: E402

_cert = {}


def cert():
    if 'c' not in _cert:
        _cert['c'] = QU.build(small=8)
    return copy.deepcopy(_cert['c'])


def ev(p, nv, lam):
    return sum((v * F(nv) ** a * F(lam) ** b for (a, b), v in p.items()), F(0))


def direct_top(nv, lam, free, param, ts):
    """Exact top coefficients of T3(H, D G) for G in E_n built top-down from one free parameter."""
    H = W.tidy({(4, 0): F(1), (2, 2): F(lam), (0, 4): F(1)})
    h = {t: F(int(t == param)) for t in free}
    for t in range(0, nv - 1):
        if t + 3 in h or t + 3 > nv:
            continue
        A = 24 * (t + 3) * (t + 2) * (t + 1)
        B = 12 * F(lam) * (nv - 1 - t) * (t + 1) * (nv - 2 - 2 * t)
        Cc = -24 * (nv + 1 - t) * (nv - t) * (nv - 1 - t)
        h[t + 3] = -(B * h.get(t + 1, F(0)) + Cc * h.get(t - 1, F(0))) / A
    G = W.tidy({(nv - t, t): v for t, v in h.items() if t <= nv})
    # G must really satisfy the static condition except possibly at the bottom boundary
    img = W.act(W.gate(H, 3), W.act(W.derivation(H), G))
    return [img.get((nv - t, t), F(0)) for t in ts]


class Symbolic(unittest.TestCase):
    def test_top_equations_agree_with_direct_computation_from_threshold_on(self):
        rng = random.Random(11)
        odd = C.top_equations([1])
        even = C.top_equations([0, 2])
        for nv in range(8, 21):
            lam = F(rng.randint(-9, 9), rng.randint(1, 4))
            got = direct_top(nv, lam, [1], 1, [1, 3])
            self.assertEqual(got, [ev(odd[t].coef.get(1, {}), nv, lam) / odd[t].den for t in (1, 3)], nv)
            for p in (0, 2):
                got = direct_top(nv, lam, [0, 2], p, [0, 2, 4])
                self.assertEqual(got, [ev(even[t].coef.get(p, {}), nv, lam) / even[t].den for t in (0, 2, 4)], nv)

    def test_square_stratum_is_the_only_common_factor(self):
        even = C.top_equations([0, 2])
        rows = [(even[t].coef.get(0, {}), even[t].coef.get(2, {})) for t in (0, 2, 4)]
        m01 = C.padd(C.pmul(rows[0][0], rows[1][1]), C.psc(C.pmul(rows[1][0], rows[0][1]), -1))
        # at l = 2 every minor vanishes identically in n (genuine extra core for (q^2+p^2)^2)
        self.assertTrue(all(v == 0 for v in {a: sum(c * 2 ** b for (aa, b), c in m01.items() if aa == a)
                                             for (a, _) in m01}.values()))

    def test_certificate_and_forgeries(self):
        base = cert()
        self.assertEqual(C.check(base)['status'], 'passed')
        muts = [lambda c: c['R1'].__setitem__(0, '1'),
                lambda c: c.update(threshold=3),
                lambda c: c.update(threshold=5),                     # below the validity bound
                lambda c: c.update(threshold=20),                    # small certificate covers only 1..8
                lambda c: c['odd_coefficients'][0].pop(),
                lambda c: c['small_degree_certificate']['degrees'][1]['factors'][0].update(rank=0),
                lambda c: c.update(family='q^4 + p^4')]
        for m in muts:
            bad = copy.deepcopy(base)
            m(bad)
            with self.assertRaises((ValueError, KeyError, IndexError)):
                C.check(bad)


if __name__ == '__main__':
    unittest.main()
