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
    if core.startswith('K[l] + m K[l]'):
        return sum(min(2, n + 1) for n in range(N + 1))
    if core.startswith('(+)_{j<=2}'):
        return sum(min(3, n + 1) for n in range(N + 1))
    raise ValueError(core)


def predicted_res(res, N):
    if res['core'].startswith('open'):         # cubic phase: only the lower bound is known
        return None
    if 'degrees' in res:                       # triangular families: span recorded by detect
        import check_triangular as CT
        return CT.core_dim(res, N)
    return predicted(res['core'], res['degree'], N)


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


def tri_samples(rng):
    """members of K1, K2, K3 (DYNAMIC_CORE_RESULTS.md section 6.8) and near misses."""
    import check_triangular as CT
    out = []
    w2 = {2: F(1), 1: F(rng.randint(-1, 1))}
    out.append(CT.tri({(0, 3): F(1), (0, 1): F(-2), (1, 0): F(1)}, w2))            # K1, active tower
    out.append(CT.tri({(0, 3): F(1), (0, 0): F(1)}, w2))                           # K1, stationary tower
    out.append(CT.tri({(0, 2): F(1), (1, 0): F(rng.randint(-2, 2))}, w2))           # K1 + K2
    out.append(CT.tri({(0, 2): F(1), (2, 0): F(1)}, w2))                           # K2, e = 2
    out.append(CT.tri({(0, 2): F(2), (1, 1): F(1), (1, 0): F(-1)}, {3: F(1)}))     # K2, e = 3
    out.append(CT.tri({(0, 2): F(1), (2, 0): F(1)}, {4: F(1), 1: F(1)}))           # K2, e = 4
    out.append({(1, 2): F(1), (3, 1): F(2), (5, 0): F(1), (1, 0): F(1)})           # K3, k = 1
    out.append({(1, 2): F(1), (0, 2): F(1), (3, 1): F(2), (2, 1): F(2), (5, 0): F(1), (4, 0): F(1)})
    out.append({(3, 2): F(1), (5, 1): F(2), (7, 0): F(1), (1, 0): F(1)})           # K3, k = 3, r = Q
    out.append({(2, 2): F(1), (3, 1): F(4), (4, 1): F(2), (4, 0): F(4), (5, 0): F(4), (6, 0): F(1)})
    out.append(CT.tri({(0, 4): F(1), (1, 1): F(-1), (1, 0): F(1)}, w2))            # K1'
    out.append(CT.tri({(0, 3): F(1), (1, 1): F(1)}, w2))                           # K1', P H in the core
    out.append(CT.tri({(0, 4): F(1), (1, 2): F(1)}, w2))                           # K4, double root
    out.append(CT.tri({(0, 4): F(1), (0, 1): F(-1), (1, 2): F(1), (1, 1): F(2), (1, 0): F(-3)}, w2))  # K4, r' = -3r
    out.append(CT.tri({(0, 4): F(1), (1, 2): F(1), (1, 0): F(-1)}, w2))            # affine cubic phase, not K4
    # near misses: conjectured span{1, H}, or open (cubic phase)
    out.append(CT.tri({(0, 3): F(1)}, {3: F(1)}))                                  # cubic in P, e = 3
    out.append(CT.tri({(0, 3): F(1), (2, 0): F(1)}, w2))                           # Q^2 breaks K1
    out.append(CT.tri({(0, 2): F(1), (3, 0): F(1)}, {3: F(1)}))                    # cubic r breaks K2
    out.append({(1, 2): F(1), (3, 1): F(2), (5, 0): F(1), (2, 0): F(1)})           # r = Q^2 breaks K3
    out.append({(2, 2): F(1), (4, 1): F(2), (6, 0): F(1), (1, 0): F(1)})           # k = 2 needs r const
    return out


class Triangular(unittest.TestCase):
    def test_identities(self):
        import check_triangular as CT
        import check_cubic_phase as CP
        self.assertEqual(CT.check()['status'], 'passed')
        self.assertEqual(CP.check()['status'], 'passed')
        with self.assertRaises(ValueError):
            CP.check({'format': CP.FORMAT, 'identities': ['G1']})
        with self.assertRaises(ValueError):
            CT.check({'format': CT.FORMAT, 'identities': ['X1']})

    def test_families_against_direct_computation(self):
        rng = random.Random(4)
        seen = set()
        Hs = tri_samples(rng)
        Hs += [linmap(H, 1, 0, 1, 1, rng.randint(-2, 2), rng.randint(-2, 2)) for H in Hs[:: 4]]
        Hs += [linmap(H, 1, 1, 0, 1, rng.randint(-1, 1), rng.randint(-1, 1)) for H in Hs[1:10:4]]
        for H in Hs:
            H = W.tidy(H)
            res = TR.classify(H)
            d = res['degree']
            N = d + 2
            want = predicted_res(res, N)
            if want is not None:
                self.assertEqual(filtered_dim(H, N, 8), want, (H, res))
            seen.add(res['route'])
        for r in ('K1', "K1'", 'K2', 'K1+K2', 'K3', 'K4', 'pure, conjectural', 'pure, cubic phase',
                  'pure, cubic phase affine'):
            self.assertIn(r, seen)

    def test_certificates_and_forgeries(self):
        import check_triangular as CT
        H = W.tidy({(6, 0): 1, (3, 1): 2, (0, 2): 1})                  # (q^3 + p)^2
        cert = CT.certify(H)
        self.assertEqual(cert['result']['verified_dimension'], 6)
        for mut in (lambda c: c['generators'].append({'2,1': '1'}),
                    lambda c: c['generators'][3].update({'0,1': '2'}),
                    lambda c: c.update(family='K3'),
                    lambda c: c['hamiltonian'].update({'3,0': '1'})):
            bad = copy.deepcopy(cert)
            bad.pop('result')
            mut(bad)
            with self.assertRaises(ValueError):
                CT.check(bad)


class Decision(unittest.TestCase):
    def test_against_direct_computation(self):
        rng = random.Random(7)
        seen = set()
        for H in samples(rng):
            H = W.tidy(H)
            res = TR.classify(H)
            d = res['degree']
            N = d + 1
            got, want = filtered_dim(H, N, 8), predicted_res(res, N)
            if want is None:
                self.assertGreaterEqual(got, 1 + (N >= d), (H, res))
            else:
                self.assertEqual(got, want, (H, res))
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
