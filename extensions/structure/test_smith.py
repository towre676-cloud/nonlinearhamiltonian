"""Integer Smith backend: classical spaces, determinantal-divisor oracle, torsion witnesses, forgeries."""
import copy
import itertools
import random
import sys
import unittest
from math import gcd
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parent)]
import smith as S          # noqa: E402
import check_smith as C    # noqa: E402
import qlinalg as L        # noqa: E402


def model(n, d):
    return {'field': 'Z', 'dimensions': n, 'differentials': d}


def det(m):
    if not m:
        return 1
    return sum((-1) ** j * m[0][j] * det([r[:j] + r[j + 1:] for r in m[1:]]) for j in range(len(m)))


def invariant_factors(A):
    """Oracle: s_k = D_k / D_(k-1), D_k = gcd of all k x k minors."""
    if not A or not A[0]:
        return []
    m, n = len(A), len(A[0])
    Ds, out = [1], []
    for k in range(1, min(m, n) + 1):
        g = 0
        for rows in itertools.combinations(range(m), k):
            for cols in itertools.combinations(range(n), k):
                g = gcd(g, det([[A[i][j] for j in cols] for i in rows]))
        if g == 0:
            break
        out.append(g // Ds[-1])
        Ds.append(g)
    return out


class Classical(unittest.TestCase):
    def test_rp2_torus_klein(self):
        rp2 = S.build(model([1, 1, 1], [[[0]], [[2]]]))
        self.assertEqual([(g['rank'], g['torsion']) for g in rp2['cohomology']], [(1, []), (0, []), (0, [2])])
        torus = S.build(model([1, 2, 1], [[[0], [0]], [[0, 0]]]))
        self.assertEqual([g['rank'] for g in torus['cohomology']], [1, 2, 1])
        klein = S.build(model([1, 2, 1], [[[0], [0]], [[2, 0]]]))
        self.assertEqual([(g['rank'], g['torsion']) for g in klein['cohomology']], [(1, []), (1, []), (0, [2])])

    def test_rational_versus_integral(self):
        cert = S.build(model([1, 1], [[[2]]]), [(1, [1]), (1, [4])])
        self.assertEqual([a['status'] for a in cert['answers']], ['torsion', 'exact'])
        self.assertEqual(cert['answers'][0]['modulus'], 2)
        self.assertEqual(cert['answers'][1]['primitive'], [2])
        free = S.build(model([1, 2], [[[1], [1]]]), [(1, [1, 0])])
        self.assertEqual(free['answers'][0]['status'], 'rational')

    def test_rejections(self):
        for bad in (model([1, 1, 1], [[[1]], [[1]]]), model([1, 1], [[['1/2']]]), {'field': 'Q', 'dimensions': [1], 'differentials': []}):
            with self.assertRaises(ValueError):
                S.build(bad)
        self.assertEqual(S.build(model([200, 200], [[[0] * 200 for _ in range(200)]]))['status'], 'unknown')


class Oracle(unittest.TestCase):
    def test_random_matrices_match_determinantal_divisors(self):
        rng = random.Random(9)
        for trial in range(120):
            m, n = rng.randint(1, 4), rng.randint(1, 4)
            A = [[rng.choice([0, 0, 1, -1, 2, 3, -4, 6]) for _ in range(n)] for _ in range(m)]
            cert = S.build(model([n, m], [A]))
            self.assertEqual(cert['smith'][0]['invariants'], invariant_factors(A), (trial, A))

    def test_random_cocycle_answers(self):
        rng = random.Random(10)
        kinds = {'exact': 0, 'torsion': 0, 'rational': 0}
        for trial in range(120):
            m, n = rng.randint(1, 3), rng.randint(1, 3)
            A = [[rng.choice([0, 1, -1, 2, 3, -2, 4]) for _ in range(n)] for _ in range(m)]
            b = [rng.randint(-4, 4) for _ in range(m)]
            cert = S.build(model([n, m], [A]), [(1, b)])
            st = cert['answers'][0]['status']
            kinds[st] += 1
            # Rational solvability oracle: rank test with exact fractions.
            cols = L.transpose([[L.F(x) for x in r] for r in A], n)
            rat = L.rank(cols + [[L.F(x) for x in b]], m) == L.rank(cols, m)
            self.assertEqual(st == 'rational', not rat, trial)
        self.assertGreater(min(kinds.values()), 5)


class Forgeries(unittest.TestCase):
    def test_mutations(self):
        m = model([1, 2, 1], [[[0], [0]], [[2, 0]]])
        cert = S.build(m, [(2, [1]), (2, [2])])
        cert.pop('result')
        for mutate in (lambda c: c['cohomology'][2].update(torsion=[]),
                       lambda c: c['smith'][1]['invariants'].__setitem__(0, 4),
                       lambda c: c['smith'][1]['Pinv'][0].__setitem__(0, 2),
                       lambda c: c['answers'][0].update(modulus=3),
                       lambda c: c['answers'][0].update(status='exact', primitive=[0, 0]),
                       lambda c: c['answers'][1].update(primitive=[2, 0])):
            bad = copy.deepcopy(cert)
            mutate(bad)
            with self.assertRaises(ValueError):
                C.check(bad, m)


if __name__ == '__main__':
    unittest.main()
