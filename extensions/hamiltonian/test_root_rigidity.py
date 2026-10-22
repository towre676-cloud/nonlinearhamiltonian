"""Arbitrary-degree results: monomial theorem, root-type routing, perturbation corollary, odd squarefree."""
import copy
import random
import sys
import unittest
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parent)]
import weyl_receipts as W            # noqa: E402
import qlinalg as L                  # noqa: E402
import check_monomial_theorem as M   # noqa: E402
import check_root_rigidity as RR     # noqa: E402
import test_binary_static as T       # noqa: E402


def monomial_prediction(a, b, n):
    """dim of the monomial-theorem core in degree n for H = q^a p^b, a >= b."""
    if b == 0:
        return min(3, n + 1)
    if b == 1:
        return 2 if n >= 1 else 1
    if a == b:
        return int(n % 2 == 0)
    return int(n in (0, 2, a + b))


def filtered_dim(H, N, R):
    """dim of {G : deg G <= N, C_k D^r G = 0 for r <= R} for an inhomogeneous H."""
    D, gates = W.derivation(H), W.gates(H)
    mons = [(i, j) for s in range(N + 1) for i in range(s + 1) for j in [s - i]]
    cols = []
    for m in mons:
        g, img = {m: F(1)}, {}
        for r in range(R + 1):
            for k, Ck in gates.items():
                for e, c in W.act(Ck, g).items():
                    img[(r, k, e)] = c
            g = W.act(D, g)
        cols.append(img)
    keys = sorted({k for c in cols for k in c})
    Mx = [[c.get(k, F(0)) for c in cols] for k in keys]
    return len(mons) - L.rank(Mx, len(mons))


class Monomial(unittest.TestCase):
    def test_identities(self):
        self.assertEqual(M.check({'format': M.FORMAT, 'identities': sorted(M.identities())})['status'], 'passed')
        with self.assertRaises(ValueError):
            M.check({'format': M.FORMAT, 'identities': ['I1']})

    def test_direct_dimensions(self):
        for d in range(3, 10):
            for b in range(0, d // 2 + 1):
                a = d - b
                H = {(a, b): F(1)}
                got = T.dims(H, 12, 3)
                self.assertEqual(got, [monomial_prediction(a, b, n) for n in range(1, 13)], (a, b))


def c3_depth3_dims(H, N):
    """dims of {G in V_n : C_3 D^r G = 0, r = 0..3} (the stopping rule of Theorem M)."""
    D, C3 = W.derivation(H), W.gate(H, 3)
    out = []
    for n in range(1, N + 1):
        cols = []
        for a in range(n + 1):
            g, img = {(a, n - a): F(1)}, {}
            for r in range(4):
                for e, c in W.act(C3, g).items():
                    img[(r, e)] = c
                g = W.act(D, g)
            cols.append(img)
        keys = sorted({k for c in cols for k in c})
        Mx = [[c.get(k, F(0)) for c in cols] for k in keys]
        out.append(n + 1 - (L.rank(Mx, n + 1) if Mx else 0))
    return out


class StoppingRule(unittest.TestCase):
    def test_c3_with_depth_three_suffices_for_monomials(self):
        for d in range(3, 9):
            for b in range(0, d // 2 + 1):
                a = d - b
                self.assertEqual(c3_depth3_dims({(a, b): F(1)}, 12),
                                 [monomial_prediction(a, b, n) for n in range(1, 13)], (a, b))


def random_form(rng, lam):
    pts = rng.sample([F(x, y) for x in range(-6, 7) for y in (1, 2, 3)], len(lam))
    mult = {}
    for i, (r, m) in enumerate(zip(pts, lam)):
        mult['inf' if i == 0 and rng.random() < 0.5 else r] = m
    H = T.form(mult)
    c = F(rng.choice([1, -2, 3, F(1, 2)]))
    return {k: v * c for k, v in H.items()}


class Routing(unittest.TestCase):
    def test_root_types_are_recovered(self):
        rng = random.Random(3)
        for lam in ([3], [2, 1], [1, 1, 1], [4, 2, 1], [3, 3, 1], [2, 2, 2, 1], [1] * 7, [4, 1, 1, 1, 1], [1] * 8,
                    [5, 3], [4, 4], [6, 1, 1], [3, 1, 1, 1]):
            H = random_form(rng, lam)
            res = RR.certify(H)['result']
            self.assertEqual(res['root_type'], sorted(lam, reverse=True))

    def test_routes(self):
        self.assertEqual(RR.route([1] * 7, 7), 'R2')
        self.assertEqual(RR.route([4, 1, 1, 1, 1], 8), 'open')
        self.assertEqual(RR.route([1] * 8, 8), 'open')
        self.assertEqual(RR.route([4, 2, 1, 1], 8), 'R1')
        self.assertEqual(RR.route([3, 1, 1, 1], 6), 'W4')
        self.assertEqual(RR.route([2, 1, 1], 4), 'W3')
        self.assertEqual(RR.route([1, 1, 1], 3), 'R3')

    def test_forgeries(self):
        H = random_form(random.Random(1), [2, 1, 1, 1])
        base = RR.certify(H)
        for mut in (lambda c: c['squarefree'].__setitem__(0, c['squarefree'][1] if len(c['squarefree']) > 1 else ['0', '1']),
                    lambda c: c.update(leading=str(F(c['leading']) * 2)),
                    lambda c: c['squarefree'].append(['1', '1'])):
            bad = copy.deepcopy(base)
            bad.pop('result')
            mut(bad)
            with self.assertRaises(ValueError):
                RR.check(bad)


class Perturbation(unittest.TestCase):
    def test_lower_order_perturbations_keep_span_1_H(self):
        """Top parts from routes R1, R2, W3, W4 plus random lower-degree terms: the direct
        space {deg G <= N, C_k D^r G = 0, r <= 2} is span{1, H} (consistency check)."""
        rng = random.Random(9)
        for lam in ([2, 1, 1], [1, 1, 1, 1], [1] * 5, [3, 1, 1], [2, 2, 1], [3, 1, 1, 1]):
            top = random_form(rng, lam)
            d = sum(lam)
            P = {(i, j): F(rng.randint(-3, 3)) for s in range(0, d) for i in range(s + 1) for j in [s - i]
                 if rng.random() < 0.4}
            H = W.tidy({**P, **{k: top.get(k, F(0)) + P.get(k, F(0)) for k in top}})
            res = RR.certify(H)['result']
            self.assertEqual(res['core'], 'span{1, H}')
            self.assertEqual(filtered_dim(H, d + 2, 2), 2, lam)


class OddSquarefree(unittest.TestCase):
    def test_static_space_vanishes_beyond_the_apolar_bound(self):
        """Theorem R2 bound for d = 7: E_n(H) = 0 for n >= (d-1)(d-2) + 3 = 33."""
        H = T.form({0: 1, 'inf': 1, 1: 1, -1: 1, 2: 1, F(-1, 2): 1, 3: 1})
        self.assertEqual(T.dims(H, 33, 0, static=True)[-1], 0)

    def test_squarefree_cubic(self):
        H = T.form({0: 1, 'inf': 1, 1: 1})
        self.assertEqual(T.dims(H, 10, 3), [int(n == 3) for n in range(1, 11)])


if __name__ == '__main__':
    unittest.main()
