"""Two-root tops: decision procedure versus direct computation, forgeries."""
import copy
import random
import sys
import unittest
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parent)]
import weyl_receipts as W            # noqa: E402
import check_two_root as TR          # noqa: E402
from test_root_rigidity import filtered_dim  # noqa: E402


def predicted(core, d, N):
    """dim of the classified core in degrees <= N."""
    if core.startswith('span{1, H, G}'):
        return 1 + (N >= 2) + (N >= d)
    if core.startswith('span{1, H}'):
        return 1 + (N >= d)
    if core == 'K[G]':
        return N // 2 + 1
    if core == 'K[Q] + span{l, lQ, l^2}':
        return N // 2 + 1 + (N >= 1) + (N >= 2) + (N >= 3)
    if core == 'K[Q] + K*l':
        return N // 2 + 1 + (N >= 1)
    if core == 'span{1, l, Q, l^2, lQ, Q^2}':
        n = d // 2
        return 1 + (N >= 1) + (N >= n) + (N >= 2) + (N >= n+1) + (N >= 2*n)
    if core.startswith('K[l] + m K[l]'):
        return sum(min(2, n + 1) for n in range(N + 1))
    if core.startswith('(+)_{j<=2}'):
        return sum(min(3, n + 1) for n in range(N + 1))
    raise ValueError(core)


def linmap(H, a, b, c, e, x0, y0):
    """H(a q + b p + x0, c q + e p + y0)."""
    return TR.comp(TR.tidy(H), {(1, 0): F(a), (0, 1): F(b), (0, 0): F(x0)},
                   {(1, 0): F(c), (0, 1): F(e), (0, 0): F(y0)})


def samples(rng):
    out = []
    for d in (3, 4, 5):
        lower = lambda allow: {(i, s - i): F(rng.randint(-2, 2)) for s in range(d) for i in range(s + 1)
                               if allow(i, s - i) and rng.random() < 0.5}
        # pure top q^d: W, V, Q', generic
        out.append({(d, 0): F(1), **lower(lambda i, j: j == 0), (1, 1): F(rng.randint(-2, 2)), (0, 1): F(1)})
        out.append({(d, 0): F(1), **lower(lambda i, j: j <= 1), (d - 2, 1): F(1)})
        out.append({(d, 0): F(1), **lower(lambda i, j: j == 0 or (j == 1 and 2 * i < d)), (0, 2): F(2)})
        out.append({(d, 0): F(1), **lower(lambda i, j: True)})
        # near top q p^(d-1): V, Q, generic
        out.append({(1, d - 1): F(1), **lower(lambda i, j: i <= 1)})
        out.append({(1, d - 1): F(1), **lower(lambda i, j: i <= 1), (2, 0): F(-1)})
        out.append({(1, d - 1): F(1), **lower(lambda i, j: True)})
        if d == 4:
            mu = d // 2
            G = {(1, 1): F(1), (1, 0): F(rng.randint(-2, 2)), (0, 1): F(rng.randint(-2, 2))}
            out.append(TR.add(TR.power(G, mu), TR.sc(G, 3)))            # in K[G]
            out.append({(mu, mu): F(1), **lower(lambda i, j: True)})
        if d == 5:
            a, b = d - 2, 2
            out.append({(a, b): F(1), (a - b, 0): F(2), (a - b + 1, 1): F(-1), (1, 1): F(3)})   # normal form
            out.append({(a, b): F(1), **lower(lambda i, j: True)})
    # random linear changes and translations of a few
    more = []
    for H in out[:: 3]:
        more.append(linmap(H, 1, 1, 0, 1, rng.randint(-2, 2), rng.randint(-2, 2)))
    return out + more


class NearEdges(unittest.TestCase):
    def test_identities(self):
        import check_near_edges as NE
        self.assertEqual(NE.check()['status'], 'passed')
        with self.assertRaises(ValueError):
            NE.check({'format': NE.FORMAT, 'identities': ['E1']})


class Balanced(unittest.TestCase):
    def test_identities(self):
        import check_balanced as CB
        self.assertEqual(CB.check()['status'], 'passed')
        with self.assertRaises(ValueError):
            CB.check({'format': CB.FORMAT, 'identities': ['B1']})

    def test_box_and_edge_perturbations(self):
        """Balanced tops with perturbations inside the box i, j <= mu (no Newton-polygon edge),
        on an edge, and translated K[G] members, against direct computation."""
        rng = random.Random(12)
        cases = [{(2, 2): F(1), (1, 0): F(1)}, {(2, 2): F(1), (2, 0): F(1)}, {(2, 2): F(1), (2, 1): F(1), (1, 1): F(1)},
                 {(3, 3): F(1), (2, 1): F(1)}, {(3, 3): F(1), (2, 2): F(1), (1, 1): F(-2), (1, 0): F(1)},
                 {(2, 2): F(1), (3, 0): F(1)}, TR.shift({(2, 2): F(1), (1, 1): F(3)}, 1, -2),
                 TR.add(TR.shift({(2, 2): F(1), (1, 1): F(3)}, 1, -2), {(0, 1): F(1)})]
        for H in cases:
            H = W.tidy(H)
            res = TR.classify(H)
            d = res['degree']
            self.assertTrue(res['proved'])
            self.assertEqual(filtered_dim(H, d + 2, 8), predicted(res['core'], d, d + 2), (H, res))


class TransverseAndVertex(unittest.TestCase):
    def test_routes_T_and_N_against_direct_computation(self):
        cases = {'T': [{(0, 6): F(1), (2, 3): F(1), (2, 1): F(1), (1, 1): F(1)}],
                 'NE': [{(1, 4): F(1), (2, 2): F(1), (2, 1): F(1)}, {(1, 5): F(1), (3, 2): F(1), (4, 0): F(1)},
                        {(1, 4): F(1), (2, 2): F(1), (3, 0): F(1)}, {(1, 6): F(1), (2, 3): F(1), (3, 0): F(1)},
                        {(1, 4): F(1), (2, 2): F(-2), (3, 0): F(1), (0, 2): F(1)}]}
        for route, Hs in cases.items():
            for H in Hs:
                H = W.tidy(H)
                res = TR.classify(H)
                self.assertEqual(res['route'], route, H)
                d = res['degree']
                self.assertEqual(filtered_dim(H, d + 1, 8), predicted(res['core'], d, d + 1), H)


class PureCompositionRegressions(unittest.TestCase):
    def test_counterexamples_and_distinct_composition_routes(self):
        q, p = {(1, 0): F(1)}, {(0, 1): F(1)}
        Q = TR.add(p, TR.power(q, 2))
        J = TR.add(TR.mul(q, p), TR.power(q, 3))
        R = TR.add(p, TR.power(q, 3))
        cases = [('QC', TR.power(Q, 2)),
                 ('QC', TR.add(TR.power(Q, 3), q)),
                 ('PP', TR.mul(q, TR.power(J, 2))),
                 ('SC', TR.power(J, 2)), ('SC', TR.power(J, 3)),
                 ('SS', TR.add(TR.power(R, 2), q))]
        for route, H in cases:
            for Ht in (H, linmap(H, 1, 1, 0, 1, F(1, 2), F(-2, 3))):
                result = TR.classify(Ht)
                self.assertEqual(result['route'], route)
                self.assertTrue(result['proved'])
                TR.check(TR.certify(Ht))
                if 'G' in result:
                    G = {tuple(map(int, k.split(','))): F(v) for k, v in result['G'].items()}
                    for gate in W.gates(Ht).values():
                        self.assertEqual(W.act(gate, G), {})
                    self.assertTrue(TR.in_span(W.act(W.derivation(Ht), G),
                                              [{(0, 0): F(1)}, Ht, G]))
                if result.get('composition_generator_is_core') is False:
                    G = {tuple(map(int, k.split(','))): F(v)
                         for k, v in result['composition_generator'].items()}
                    self.assertNotEqual(W.act(W.gate(Ht, 3), G), {})
        self.assertEqual(filtered_dim(TR.power(Q, 2), 5, 4), 6)
        self.assertEqual(filtered_dim(TR.mul(q, TR.power(J, 2)), 8, 4), 3)

    def test_unknown_and_forged_claims(self):
        result = TR.classify({(6, 0): F(1), (2, 2): F(1)})
        self.assertFalse(result['proved'])
        self.assertEqual(result['core'], 'unclassified')
        H = {(4, 0): F(1), (2, 1): F(2), (0, 2): F(1)}
        cert = TR.certify(H)
        cert['claim']['core'] = 'span{1, H}'
        with self.assertRaises(ValueError):
            TR.check(cert)


class Decision(unittest.TestCase):
    def test_against_direct_computation(self):
        rng = random.Random(7)
        seen = set()
        for H in samples(rng):
            H = W.tidy(H)
            res = TR.classify(H)
            d = res['degree']
            N = d + 1
            got = filtered_dim(H, N, 8)
            if res['proved']:
                self.assertEqual(got, predicted(res['core'], d, N), (H, res))
            else:
                # A sampled dimension cannot classify an unresolved all-degree
                # core. The old blanket pure-top conjecture has counterexamples.
                self.assertGreaterEqual(got, 1 + (N >= d), (H, res))
            seen.add(res['route'])
        for r in ('U', 'NE', "Q'", 'B', 'P+ near', 'P+ pure W', 'P+ pure V', 'P+ balanced'):
            self.assertIn(r, seen)

    def test_forgeries(self):
        H = {(3, 2): F(1), (2, 1): F(1)}
        cert = TR.certify(H)
        for mut in (lambda c: c['claim'].update(core='span{1, H}'),
                    lambda c: c['claim'].update(proved=False),
                    lambda c: c['hamiltonian'].update({'0,1': '1'})):
            bad = copy.deepcopy(cert)
            bad.pop('result')
            mut(bad)
            with self.assertRaises(ValueError):
                TR.check(bad)
        with self.assertRaises(ValueError):
            TR.classify({(1, 2): F(1), (2, 1): F(1)})        # three roots: not a two-root top


if __name__ == '__main__':
    unittest.main()
