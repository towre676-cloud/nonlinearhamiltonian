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


def predicted_result(result, N):
    """Exact filtration of a supplied independent finite core basis."""
    if 'basis' in result:
        import qlinalg as L
        basis = [{tuple(map(int, key.split(','))): F(value)
                  for key, value in g.items()} for g in result['basis']]
        high = sorted({monomial for g in basis for monomial in g
                       if sum(monomial) > N})
        rows = [[g.get(monomial, F(0)) for g in basis] for monomial in high]
        return len(basis)-L.rank(rows, len(basis))
    if result['core'].startswith('span{1, H, G}'):
        return 1+(N >= result.get('generator_degree', 2))+(N >= result['degree'])
    return predicted(result['core'], result['degree'], N)


def predicted_res(res, N):
    """Predicted core dimension in degrees <= N, or None when only a lower bound is known."""
    if not res.get('proved', True) or res['core'].startswith('open'):
        return None
    if 'degrees' in res:                       # triangular families: span recorded by detect
        import check_triangular as CT
        return CT.core_dim(res, N)
    return predicted_result(res, N)


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
            self.assertEqual(filtered_dim(H, d + 2, 8), predicted_result(res, d + 2), (H, res))


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
                self.assertEqual(filtered_dim(H, d + 1, 8), predicted_result(res, d + 1), H)


class PureCompositionRegressions(unittest.TestCase):
    def test_new_shear_oscillator_and_weighted_routes(self):
        q, p = {(1, 0): F(1)}, {(0, 1): F(1)}
        quadratic = TR.add(p, TR.power(q, 2))
        cubic = TR.add(p, TR.power(q, 3))
        cases = [
            ('SCP', TR.add(TR.power(cubic, 3), q), 2),
            ('SO', TR.add(TR.power(quadratic, 2), TR.power(q, 2)), 6),
            ('SO', TR.add(TR.power(cubic, 2), TR.sc(TR.power(q, 2), -2), q), 6),
            ('QF', TR.add(TR.power(cubic, 2), TR.power(q, 3)), 2),
            ('QF', TR.add(TR.power(cubic, 2), TR.power(q, 5)), 2),
            ('QR', TR.add(TR.power(quadratic, 2), TR.power(q, 3)), 2),
            ('QR', TR.add(TR.power(quadratic, 2), TR.power(q, 4)), 2),
        ]
        for route, H, dim in cases:
            for Ht in (H, linmap(H, 1, 1, 0, 1, F(1, 2), F(-2, 3))):
                result = TR.classify(Ht)
                self.assertEqual(result['route'], route)
                self.assertTrue(result['proved'])
                self.assertEqual(result['dimension'], dim)
                cert = TR.certify(Ht)
                TR.check(cert)
                bad = copy.deepcopy(cert)
                bad['claim']['core'] = 'K[Q]'
                with self.assertRaises(ValueError):
                    TR.check(bad)
                if 'basis' in result:
                    basis = [{tuple(map(int, k.split(','))): F(c)
                              for k, c in f.items()} for f in result['basis']]
                    self.assertEqual(len(basis), dim)
                    for f in basis:
                        self.assertTrue(all(not W.act(gate, f)
                                            for gate in W.gates(Ht).values()))
                        self.assertTrue(TR.in_span(W.act(W.derivation(Ht), f), basis))
        # Actual full-output filtered kernels provide an independent regression.
        for _, H, dim in cases[:3]:
            n = TR.degree(H)
            self.assertEqual(filtered_dim(H, n, 4), dim)

    def test_resonant_weight_boundary_and_sharp_depths(self):
        q, p = {(1, 0): F(1)}, {(0, 1): F(1)}
        Q = TR.add(p, TR.power(q, 3))
        H = TR.add(TR.power(Q, 2), TR.power(q, 6))
        result = TR.classify(H)
        self.assertTrue(result['proved'])
        self.assertEqual(result['route'], 'QF')
        self.assertEqual(result['core'], 'span{1, H}')
        for n, depth in ((3, 6), (4, 4), (6, 4)):
            H = TR.add(TR.power(Q, 2), TR.power(q, n))
            result = TR.classify(H)
            self.assertEqual(result['third_gate_depth'], depth)
            D, gate = W.derivation(H), W.gate(H, 3)
            witness = q
            for r in range(depth + 1):
                failure = W.act(gate, witness)
                self.assertEqual(bool(failure), r == depth)
                witness = W.act(D, witness)
        for n, depth in ((3, 6), (4, 4)):
            Q = TR.add(p, TR.power(q, 2))
            H = TR.add(TR.power(Q, 2), TR.power(q, n))
            result = TR.classify(H)
            self.assertEqual(result['route'], 'QR')
            self.assertEqual(result['third_gate_depth'], depth)
            witness = q
            for r in range(depth + 1):
                self.assertEqual(bool(W.act(W.gate(H, 3), witness)), r == depth)
                witness = W.act(W.derivation(H), witness)

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

def tri_samples(rng):
    """members of K1, K2, K3 (DYNAMIC_CORE_RESULTS.md sections 6.18, 6.26) and near misses."""
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
    out.append(CT.tri({(0, 3): F(1), (1, 0): F(1)}, {3: F(1)}))                   # RS: higher shear, b constant
    out.append(CT.tri({(0, 3): F(1), (1, 1): F(1)}, {3: F(1), 1: F(1)}))           # higher shear affine
    out.append(CT.tri({(0, 3): F(1), (2, 0): F(1)}, w2))                           # NA, cubic phase
    out.append(CT.tri({(0, 3): F(1), (2, 0): F(1), (1, 1): F(1)}, {3: F(1)}))      # NA, higher shear
    out.append(CT.tri({(0, 3): F(1), (2, 1): F(1)}, w2))                           # NE: cubic phase, non-binomial edge
    out.append(CT.tri({(0, 2): F(1), (4, 0): F(1)}, w2))                           # NB: boundary edge (p+q^2)^2 + q^4
    out.append(CT.tri({(0, 3): F(1), (6, 0): F(1)}, w2))                           # NT: cubic phase, edge slope 1/2
    out.append(CT.tri({(0, 3): F(1), (6, 1): F(1)}, {3: F(1)}))                    # NT: threshold edge, e = 3
    out.append(CT.tri({(0, 3): F(1), (5, 1): F(1), (1, 0): F(1)}, w2))             # NV: below the threshold
    out.append(CT.tri({(0, 5): F(1), (4, 0): F(1)}, {1: F(1)}))                    # NV: flat lower terms, deg w = 1
    out.append({(0, 4): F(1), (3, 2): F(1), (6, 0): F(1), (1, 1): F(1)})           # NV: flat lower terms, B = 3, K = 2
    out.append({(2, 3): F(1), (6, 0): F(1), (1, 1): F(1)})                         # TP: transverse top q^2, s = 3
    out.append({(3, 2): F(1), (5, 1): F(2), (7, 0): F(1), (1, 1): F(1), (3, 0): F(1), (0, 0): F(1)})  # extended K3, beta = 1
    out.append(CT.tri({(0, 2): F(1), (3, 0): F(1)}, w2))                           # NA, m-degree 2: (p+q^2)^2 + q^3
    # near misses (the last five): outside the containment recognizers
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
        import check_gauge as CG
        self.assertEqual(CG.check()['status'], 'passed')
        with self.assertRaises(ValueError):
            CP.check({'format': CP.FORMAT, 'identities': ['G1']})
        with self.assertRaises(ValueError):
            CT.check({'format': CT.FORMAT, 'identities': ['X1']})

    def test_families_against_direct_computation(self):
        """check_gauge.py routes alone (routes='gauge') against direct computation."""
        rng = random.Random(4)
        seen = set()
        Hs = tri_samples(rng)
        Hs += [linmap(H, 1, 0, 1, 1, rng.randint(-2, 2), rng.randint(-2, 2)) for H in Hs[:: 4]]
        Hs += [linmap(H, 1, 1, 0, 1, rng.randint(-1, 1), rng.randint(-1, 1)) for H in Hs[1:10:4]]
        for H in Hs:
            H = W.tidy(H)
            res = TR.classify(H, routes='gauge')
            d = res['degree']
            N = d + 2
            want = predicted_res(res, N)
            if want is not None:
                self.assertEqual(filtered_dim(H, N, 8), want, (H, res))
            seen.add(res['route'])
        for r in ('K1', "K1'", 'K2', 'K1+K2', 'K3', 'K4', 'RS', 'NA', 'NE', 'NB', 'NT', 'NV', 'TP', 'TE',
                  'pure, cubic phase affine'):
            self.assertIn(r, seen)

    def test_two_classifications_agree(self):
        """check_gauge and core_overlap routes predict the same core wherever both prove one."""
        import subprocess
        out = subprocess.run([sys.executable, '-B', str(HERE / 'crosscheck_pure_routes.py'),
                              '--count', '150', '--seed', '3'], capture_output=True, text=True)
        import json
        res = json.loads(out.stdout)
        self.assertEqual(res['issues'], [], res['issues'][:2])
        self.assertGreater(res['tally']['both_proved'], 50)
        self.assertEqual(res['tally']['core_overlap_only'], 0)
        self.assertEqual(res['tally']['neither'], 0)          # P005: no pure top left unclassified

    def test_containment_detection(self):
        """Containment detection is independent of the stronger core routes.

        Direct filtered kernels are finite calibrations only. For an
        unproved full core they certify a lower bound, never equality.
        """
        import check_triangular as CT
        rng = random.Random(4)
        base = tri_samples(rng)
        Hs = base + [linmap(H, 1, 0, 1, 1, rng.randint(-2, 2), rng.randint(-2, 2))
                     for H in base[::4]]
        Hs += [linmap(H, 1, 1, 0, 1, rng.randint(-1, 1), rng.randint(-1, 1))
               for H in base[1:10:4]]
        seen = set()
        finite_cases = {0, 2, 4, 6, 8, 11}
        for index, H in enumerate(Hs):
            H = W.tidy(H)
            result = TR.classify(H)
            try:
                containment = CT.detect_pure(H)
            except ValueError:
                containment = None
            if containment is not None:
                seen.add(containment['family'])
                self.assertTrue(CT.span_ok(H, containment['gens']), (H, containment))
                cert = CT.certify(H)
                self.assertEqual(CT.check(cert)['claim'], 'contained in D_inf(H) (exact)')
                if not result['proved']:
                    self.assertEqual(result['core'], 'unclassified')
                    self.assertTrue(result['contains_proved'])
                    self.assertEqual(result['core_contains'], containment['core'])
                    self.assertIn(result['route'], ("K1'", 'K3'))
            elif not result['proved']:
                self.assertEqual(result['core'], 'unclassified')
            if index in finite_cases:
                degree = result['degree']
                bound = min(degree + 2, 8)
                actual = filtered_dim(H, bound, 8)
                if result['proved']:
                    self.assertEqual(actual, predicted_result(result, bound),
                                     (H, result, bound))
                elif containment is not None:
                    self.assertGreaterEqual(actual, CT.core_dim(containment, bound),
                                            (H, containment, bound))
                else:
                    self.assertGreaterEqual(actual, 1 + (bound >= degree))
        for family in ('K1', "K1'", 'K2', 'K1+K2', 'K3'):
            self.assertIn(family, seen)
        for H in base[-5:]:
            with self.assertRaises(ValueError):
                CT.detect_pure(H)

    def test_certificates_and_forgeries(self):
        import check_triangular as CT
        H = W.tidy({(6, 0): 1, (3, 1): 2, (0, 2): 1})
        cert = CT.certify(H)
        self.assertEqual(cert['result']['verified_dimension'], 6)
        # D(q)=-F'(P) must fit the certified tower for every degree F.
        high = CT.tri({(0, 8): F(1), (1, 0): F(1)}, {2: F(1)})
        high_cert = CT.certify(high)
        self.assertEqual(high_cert['result']['family'], 'K1')
        self.assertEqual(high_cert['result']['verified_dimension'], 9)
        for mut in (lambda c: c['generators'].append({'2,1': '1'}),
                    lambda c: c['generators'][3].update({'0,1': '2'}),
                    lambda c: c.update(family='K3'),
                    lambda c: c['hamiltonian'].update({'3,0': '1'})):
            bad = copy.deepcopy(cert)
            bad.pop('result')
            mut(bad)
            with self.assertRaises(ValueError):
                CT.check(bad)

        q, p = {(1, 0): F(1)}, {(0, 1): F(1)}
        root = TR.add(q, {(0, 0): F(-2)})
        G = TR.add(TR.mul(root, p), TR.power(q, 3), q)
        residual = TR.add({(0, 0): F(7)}, TR.sc(root, -2))
        scale = F(2, 3)
        twisted = TR.add(TR.sc(TR.mul(root, TR.power(G, 2)), scale), residual)
        expected = TR.add(twisted, TR.sc(residual, -1),
                          TR.mul(root, W.pder(residual, 1, 0)))
        self.assertEqual(W.act(W.derivation(twisted), G), expected)
        self.assertEqual(CT.check(CT.certify(twisted))['family'], 'K3')

        # K3 at k=2 can be stationary; containment does not imply activity.
        J = TR.add(TR.mul(q, p), TR.power(q, 3))
        stationary = TR.add(TR.sc(TR.power(J, 2), scale), {(0, 0): F(5)})
        result = TR.classify(stationary)
        self.assertTrue(result['proved'])
        self.assertEqual(result['route'], 'SC')
        for g in ({(0, 0): F(1)}, J, stationary):
            self.assertEqual(W.act(W.derivation(stationary), g), {})
        self.assertTrue(CT.span_ok(stationary, [{(0, 0): F(1)}, J, stationary]))

        # The former outside-list conjecture P004 misses this proved PP
        # exception. A detector miss must not reinstate a collapse claim.
        outside_list = TR.add(TR.mul(q, TR.power(J, 2)), J)
        for member in (outside_list, linmap(outside_list, 1, 1, 0, 1, F(1, 2), -1)):
            result = TR.classify(member)
            self.assertTrue(result['proved'])
            self.assertEqual(result['route'], 'PP')
            with self.assertRaises(ValueError):
                CT.detect_pure(member)
        self.assertTrue(CT.span_ok(outside_list, [{(0, 0): F(1)}, J, outside_list]))


class CubicPhaseCompletion(unittest.TestCase):
    def test_complete_affine_routes_and_covariance(self):
        import check_triangular as CT
        fixtures = [({(1, 2): F(1)}, 4),
                    ({(0, 4): F(1), (1, 2): F(1)}, 3),
                    ({(0, 4): F(1), (1, 2): F(1), (1, 1): F(2), (1, 0): F(-3)}, 3),
                    ({(0, 4): F(1), (1, 2): F(1), (1, 0): F(-1)}, 2),
                    ({(0, 4): F(1), (1, 1): F(1)}, 4),
                    ({(0, 3): F(1), (0, 2): F(1), (1, 1): F(1)}, 5),
                    ({(0, 3): F(1), (1, 1): F(1)}, 6),
                    ({(0, 4): F(1), (1, 3): F(2)}, 2)]
        for h, dimension in fixtures:
            H = CT.tri(h, {2: F(1), 1: F(2, 3), 0: F(-1, 5)})
            for member in (H, linmap(H, 1, 1, 0, 1, F(1, 2), -1)):
                result = TR.classify(member)
                self.assertTrue(result['proved'], result)
                self.assertEqual(result['dimension'], dimension, result)
                self.assertEqual(result['route'], 'CP', result)
                basis = [{tuple(map(int, key.split(','))): F(value)
                          for key, value in g.items()} for g in result['basis']]
                self.assertTrue(CT.span_ok(member, basis))
                TR.check(TR.certify(member))

    def test_arbitrary_restoring_compositions(self):
        import check_triangular as CT
        for degree in (3, 4, 6):
            h = {(0, degree): F(2), (0, degree-1): F(-1),
                 (0, 0): F(3), (2, 0): F(-2, 5), (1, 0): F(7)}
            H = CT.tri(h, {2: F(-2, 3), 1: F(1, 5)})
            for member in (H, linmap(H, 1, 1, 0, 1, 1, -2)):
                result = TR.classify(member)
                self.assertTrue(result['proved'])
                self.assertEqual(result['route'], 'HR')
                self.assertEqual(result['dimension'], 2)
                self.assertEqual(result['third_gate_depth'], 3)
                TR.check(TR.certify(member))

    def test_chart_and_full_core_forgery(self):
        sys.path.insert(0, str(HERE.parents[1]/'research/core_overlap'))
        import cubic_phase_classification as CP
        import check_triangular as CT
        H = CT.tri({(0, 4): F(1), (1, 3): F(2)}, {2: F(1), 1: F(2, 3)})
        cert = CP.certify(H)
        self.assertEqual(CP.check(cert)['dimension'], 2)
        for mutate in (lambda x: x['claim'].update(dimension=3),
                       lambda x: x['claim']['w'].update({'1': '0'})):
            bad = copy.deepcopy(cert)
            mutate(bad)
            with self.assertRaises(ValueError):
                CP.check(bad)


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
                self.assertEqual(got, predicted_result(res, N), (H, res))
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
