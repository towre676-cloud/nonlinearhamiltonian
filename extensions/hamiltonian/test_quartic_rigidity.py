"""Quartic rigidity certificates: matrix family, covariance cross-checks, forgeries."""
import copy
import random
import sys
import unittest
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parent)]
import weyl_receipts as W            # noqa: E402
import quartic_rigidity as Q         # noqa: E402
import check_quartic_rigidity as C   # noqa: E402
import qlinalg as L                  # noqa: E402

_cert = {}


def cert(N=7):
    if N not in _cert:
        _cert[N] = Q.build(N)
    return copy.deepcopy(_cert[N])


def truncated_kernel_dim(H, n, depth):
    """Independent: dim of {G in V_n : C3 D^r G = 0, r <= depth} for an explicit H."""
    D, C3 = W.derivation(H), W.gates(H)[3]
    cols = []
    for a in range(n + 1):
        g, img = {(a, n - a): F(1)}, {}
        for r in range(depth + 1):
            img.update({(r, e): c for e, c in W.act(C3, g).items()})
            g = W.act(D, g)
        cols.append(img)
    keys = sorted({k for c in cols for k in c})
    M = [[c.get(k, F(0)) for c in cols] for k in keys]
    return n + 1 - (L.rank(M, n + 1) if M else 0)


class Family(unittest.TestCase):
    def test_parametric_matrix_matches_direct_evaluation(self):
        rng = random.Random(4)
        for _ in range(6):
            lam, n, depth = F(rng.randint(-9, 9), rng.randint(1, 5)), rng.randint(1, 7), rng.randint(0, 2)
            keys, mats = C.family_matrix_parts(n, depth)
            Mx = C.evaluate(mats, lam)
            H = W.tidy({(4, 0): F(1), (2, 2): lam, (0, 4): F(1)})
            self.assertEqual(n + 1 - L.rank(Mx, n + 1), truncated_kernel_dim(H, n, depth))

    def test_equianharmonic_exception_matches_rational_form(self):
        # l^2 = -12 is the j = 0 class; q^4 + q p^3 is a rational representative of it.
        H = W.tidy({(4, 0): F(1), (1, 3): F(1)})
        keys, mats = C.family_matrix_parts(1, 1)
        self.assertEqual(2 - C.nf_rank(mats, [F(12), F(0), F(1)]), truncated_kernel_dim(H, 1, 1))
        keys, mats = C.family_matrix_parts(3, 1)
        self.assertEqual(4 - C.nf_rank(mats, [F(12), F(0), F(1)]), truncated_kernel_dim(H, 3, 1))
        self.assertEqual(truncated_kernel_dim(H, 1, 3), 0)

    def test_square_stratum_exception_is_genuine(self):
        H = W.tidy({(4, 0): F(1), (2, 2): F(2), (0, 4): F(1)})     # (q^2 + p^2)^2
        for n in (2, 6, 8):
            self.assertGreater(truncated_kernel_dim(H, n, 3), 0)    # contains (q^2+p^2)^(n/2)


class Certificates(unittest.TestCase):
    def test_low_degrees(self):
        res = C.check(cert())
        by_n = {d['n']: d for d in res['degrees']}
        self.assertEqual(by_n[4]['generic_kernel_dimension'], 1)
        for n, d in by_n.items():
            if n != 4:
                self.assertEqual(d['generic_kernel_dimension'], 0)
            self.assertTrue(all(e['factor'] == ['-4', '0', '1'] for e in d['exceptions']), n)
        self.assertEqual((by_n[1]['depth'], by_n[3]['depth']), (3, 2))

    def test_forgeries(self):
        base = cert()
        muts = [lambda c: c['degrees'][4]['minors'][0].__setitem__(0, '1'),
                lambda c: c['degrees'][4]['gcd'].__setitem__(0, '5'),
                lambda c: c['degrees'][1]['factors'][0].update(rank=3),
                lambda c: c['degrees'][3].update(kernel_vectors=[]),
                lambda c: c['degrees'][3].update(kernel_vectors=[[['1'], ['0'], ['0', '2'], ['0'], ['1']]]),
                lambda c: c['degrees'][0].update(depth=1),
                lambda c: c.update(family='q^4 + p^4')]
        for m in muts:
            bad = copy.deepcopy(base)
            m(bad)
            with self.assertRaises((ValueError, KeyError, IndexError)):
                C.check(bad)


if __name__ == '__main__':
    unittest.main()
