"""Quintic and sextic classification: static finiteness certificates, direct cross-checks, forgeries."""
import copy
import gzip
import json
import random
import sys
import unittest
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path[:0] = [str(HERE), str(HERE.parent)]
import weyl_receipts as W            # noqa: E402
import qlinalg as L                  # noqa: E402
import check_binary_static as C      # noqa: E402


def stored(d):
    path = ROOT / 'results' / 'hamiltonian' / f'binary_static_d{d}.json'
    raw = path.read_bytes() if path.exists() else gzip.decompress(path.with_suffix('.json.gz').read_bytes())
    return json.loads(raw)['payload']


def form(mult):
    """Product of linear factors: root r -> (q - r p), 'inf' -> p, with multiplicities."""
    G = {(0, 0): F(1)}
    for r, m in mult.items():
        lin = {(0, 1): F(1)} if r == 'inf' else W.tidy({(1, 0): F(1), (0, 1): F(-r)})
        for _ in range(m):
            G = W.pmul(G, lin)
    return G


def dims(H, N, R, static=False):
    """dim of {G in V_n : C_k D^r G = 0, r <= R} for n = 1..N (contains D_inf(H)_n)."""
    D, gates, out = W.derivation(H), W.gates(H), []
    for n in range(1, N + 1):
        cols = []
        for a in range(n + 1):
            g, img = {(a, n - a): F(1)}, {}
            for r in range((0 if static else R) + 1):
                for k, Ck in gates.items():
                    for e, c in W.act(Ck, g).items():
                        img[(r, k, e)] = c
                g = W.act(D, g)
            cols.append(img)
        keys = sorted({k for c in cols for k in c})
        M = [[c.get(k, F(0)) for c in cols] for k in keys]
        out.append(n + 1 - (L.rank(M, n + 1) if M else 0))
    return out


def predicted(kind, d, N):
    out = []
    for n in range(1, N + 1):
        out.append({'pure': min(3, n + 1), 'near': 2, 'square': int(n in (2, d)),
                    'cube': int(n % 2 == 0), 'generic': int(n == d)}[kind])
    return out


TYPES = {
    5: [({0: 5}, 'pure'), ({0: 4, 'inf': 1}, 'near'), ({0: 3, 'inf': 2}, 'square'), ({0: 3, 'inf': 1, 1: 1}, 'generic'),
        ({0: 2, 'inf': 2, 1: 1}, 'generic'), ({0: 2, 'inf': 1, 1: 1, -1: 1}, 'generic'),
        ({0: 1, 'inf': 1, 1: 1, -1: 1, 2: 1}, 'generic')],
    6: [({0: 6}, 'pure'), ({0: 5, 'inf': 1}, 'near'), ({0: 4, 'inf': 2}, 'square'), ({0: 3, 'inf': 3}, 'cube'),
        ({0: 4, 'inf': 1, 1: 1}, 'generic'), ({0: 3, 'inf': 2, 1: 1}, 'generic'), ({0: 3, 'inf': 1, 1: 1, -1: 1}, 'generic'),
        ({0: 2, 'inf': 2, 1: 2}, 'generic'), ({0: 2, 'inf': 2, 1: 1, -1: 1}, 'generic'),
        ({0: 2, 'inf': 1, 1: 1, -1: 1, 2: 1}, 'generic'), ({0: 1, 'inf': 1, 1: 1, -1: 1, 2: 1, 3: 1}, 'generic')],
}


class Certificates(unittest.TestCase):
    def test_stored_certificates_pass(self):
        for d in (5, 6):
            res = C.check(stored(d))
            self.assertEqual(res['status'], 'passed')
            self.assertGreater(res['contradictions'], 0)

    def test_forgeries(self):
        base = stored(5)
        def first(steps, op):
            for st in steps:
                if st['op'] == op:
                    return st
                if st['op'] == 'split':
                    for br in st['branches']:
                        r = first(br, op)
                        if r:
                            return r
        muts = [lambda c: c.update(N0=c['N0'] - 5),                               # below the validity bound
                lambda c: c['rows'][1]['A'][0].__setitem__(1, str(F(c['rows'][1]['A'][0][1]) + 1)),
                lambda c: c['systems'].pop(),                                      # a case left uncovered
                lambda c: c['systems'][0].update(chart=0),
                lambda c: first(c['systems'][0]['steps'], 'derive')['combo'][0][1][0].__setitem__(1, '7'),
                lambda c: first(c['systems'][0]['steps'], 'split')['factors'].pop(),
                lambda c: first(c['systems'][1]['steps'], 'contradiction').update(idx=0),
                lambda c: c.update(degree=4)]
        for m in muts:
            bad = copy.deepcopy(base)
            m(bad)
            with self.assertRaises((ValueError, KeyError, IndexError, TypeError)):
                C.check(bad)

    def test_rows_against_direct_static_spaces(self):
        """Evaluate the top-equation matrix at random local data: when it has rank 2 the
        static space of H in degree n must be zero, computed directly from the gates."""
        rng = random.Random(5)
        for d in (5, 6):
            cert = stored(d)
            nv = d - 1
            rows = [(C.parse(r['A'], nv), C.parse(r['B'], nv)) for r in cert['rows']]
            for trial in range(3):
                h = [F(rng.randint(-5, 5), rng.randint(1, 3)) for _ in range(d - 2)]
                n = cert['N0'] + trial
                vals = [n] + h
                M = [[sum((c * F(vals[0]) ** k[0] * eval_h(k, h) for k, c in p.items()), F(0)) for p in r] for r in rows]
                Hf = W.tidy({(d - 1, 1): F(1), **{(d - j, j): h[j - 3] for j in range(3, d + 1)}})
                static = dims(Hf, n, 0, static=True)[-1]
                if L.rank(M, 2) == 2:
                    self.assertEqual(static, 0, (d, h, n))


def eval_h(k, h):
    out = F(1)
    for x, e in zip(h, k[1:]):
        out *= x ** e
    return out


class Classification(unittest.TestCase):
    def test_representatives_of_every_root_type(self):
        """Direct dimensions of {G : C_k D^r G = 0, r <= 3} agree with the classified core in
        degrees 1..12 for one representative of every root type (the core is contained in this
        space, so equality there is a consistency check, not part of the proof)."""
        for d in (5, 6):
            for mult, kind in TYPES[d]:
                H = form(mult)
                self.assertEqual(dims(H, 12, 3), predicted(kind, d, 12), (d, mult))


if __name__ == '__main__':
    unittest.main()
