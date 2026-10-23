"""W1 acceptance tests: Groebner discovery receipts, all-degree kernel certificates,
independent star-engine cross-checks, budget behaviour and forged certificates."""
import copy
import importlib.util
import sys
import unittest
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path[:0] = [str(HERE), str(HERE.parent)]
import weyl_receipts as W        # noqa: E402
import weyl_groebner as G        # noqa: E402
import weyl_kernel as KP         # noqa: E402
import check_weyl_kernel as KC   # noqa: E402

spec = importlib.util.spec_from_file_location('baseline_engine', ROOT / 'research/hamiltonian/independent/engine.py')
E = importlib.util.module_from_spec(spec)
spec.loader.exec_module(E)

# Hamiltonian -> expected all-degree dynamic core, as (families, finite basis display).
CASES = {
    'q^3': ('monomial_span', ['p^0*Q[q]', 'p^1*Q[q]', 'p^2*Q[q]']),
    'q*p^3': ('monomial_span', ['q^0*Q[p]', 'q^1*Q[p]']),
    'q*p^3+q^2': ('finite_support', ['1', 'q*p^3 + q^2']),
    'q*p^3+2*q^2': ('finite_support', ['1', '1/2*q*p^3 + q^2']),
    'q*p^3+p^2': ('monomial_span', ['q^0*Q[p]', 'q^1*Q[p]']),
    'q^3*p^3': ('monomial_span', ['q^0*p^0*Q[q^1*p^1]']),
    'q^2*p^2': ('monomial_span', ['q^0*p^0*Q[q^1*p^1]']),
    'q^2*p^3': ('monomial_span', ['q^0*p^0', 'q^1*p^1', 'q^2*p^3']),
    'p^3+q^2': ('finite_support', ['1', 'p^3 + q^2']),
}

_cache = {}


def run(h):
    if h not in _cache:
        meta, cert = G.discover(G.parse_poly(h))
        kmeta, kobj = KP.classify(cert)
        _cache[h] = (meta, cert, kmeta, kobj)
    return _cache[h]


def exact_through(H, Gp, depth):
    """Independent check with the baseline star engine: D^r G is exact for r <= depth."""
    for _ in range(depth + 1):
        if E.defects(H, Gp):
            return False
        Gp = E.poisson(H, Gp)
    return True


class Discovery(unittest.TestCase):
    def test_q_cubed_matches_handoff_receipt(self):
        meta, cert, _, _ = run('q^3')
        self.assertEqual(cert['generators'], [[[0, 0, 0, 3, '1']]])

    def test_every_case_replays_and_classifies(self):
        for h, (kind, kernel) in CASES.items():
            meta, cert, kmeta, kobj = run(h)
            self.assertEqual(meta['status'], 'certified', h)
            self.assertEqual(W.verify_certificate(cert)['status'], 'passed', h)
            self.assertEqual((kmeta['status'], kmeta['kind'], kmeta['kernel']), ('classified', kind, kernel), h)
            self.assertEqual(KC.check(kobj)['status'], 'passed', h)

    def test_all_higher_odd_gates_present(self):
        meta, cert, _, _ = run('q^3*p^3')
        self.assertEqual(sorted(cert['correction_containment']), ['3', '5'])

    def test_qp3_ideal_is_strictly_inside_W2_dq2(self):
        # The generators lie in W2*dq^2, yet dq^2 itself is not in the ideal: equal polynomial
        # kernels do not identify the Weyl ideals.
        _, cert, _, _ = run('q*p^3')
        P = [W.read_terms(g, 4) for g in cert['generators']]
        eng = G.Engine(G.parse_poly('q*p^3'))
        eng.basis = [(p, {}) for p in P]
        rem, _ = eng.reduce({(0, 0, 2, 0): F(1)}, eng.basis, track=False)
        self.assertTrue(rem)
        for p in P:
            self.assertTrue(all(c >= 2 for (_, _, c, _) in p))


class IndependentStarEngine(unittest.TestCase):
    def test_kernel_elements_are_exact_under_repeated_dynamics(self):
        for h in CASES:
            meta, cert, kmeta, kobj = run(h)
            H = W.read_terms(cert['hamiltonian'], 2)
            claim = kobj['claim']
            samples = [W.read_terms(g, 2) for g in claim.get('basis', [])]
            samples += [{(a, b): F(1)} for a in claim['vertical_lines'] for b in range(4)]
            samples += [{(a, b): F(1)} for b in claim['horizontal_lines'] for a in range(4)]
            samples += [{(a0 + t * da, b0 + t * db): F(1)} for (a0, b0), (da, db) in claim['progressions'] for t in range(4)]
            samples += [{tuple(x): F(1)} for x in claim['points'] if kmeta['kind'] == 'monomial_span']
            self.assertTrue(samples, h)
            for g in samples:
                self.assertTrue(exact_through(H, g, 3), (h, g))

    def test_outside_elements_fail_somewhere(self):
        # Monomials of low degree outside the certified kernel leave the dynamic core.
        for h in ('q*p^3+q^2', 'q^2*p^3', 'q^3*p^3'):
            meta, cert, kmeta, kobj = run(h)
            H = W.read_terms(cert['hamiltonian'], 2)
            gens = [W.read_terms(g, 4) for g in cert['generators']]
            for a in range(4):
                for b in range(4):
                    m = {(a, b): F(1)}
                    if any(W.act(P, m) for P in gens):
                        self.assertFalse(exact_through(H, m, 6), (h, a, b))

    def test_mandatory_counterexample_qp3_q2(self):
        # qp^3 with G = q^2: one bracket exact, the next iterate is not.
        H = E.monomial(1, 3)
        self.assertEqual(E.defects(H, E.monomial(2, 0)), {})
        self.assertEqual(E.defects(H, E.poisson(H, E.monomial(2, 0))), {2: {(0, 2): F(18)}})


class Budgets(unittest.TestCase):
    def test_budget_exhaustion_is_unknown(self):
        meta, cert = G.discover(G.parse_poly('q^4+p^4'), max_generators=5)
        self.assertEqual((meta['status'], cert), ('unknown', None))
        meta, cert = G.discover(G.parse_poly('q*p^3+q^2'), max_steps=50)
        self.assertEqual((meta['status'], cert), ('unknown', None))

    def test_parser_rejects_floats_and_code(self):
        for bad in ('0.5*q', "__import__('os')", 'q/p', 'q**2', ''):
            with self.assertRaises(ValueError):
                G.parse_poly(bad)


class Forgeries(unittest.TestCase):
    def rejects(self, obj):
        with self.assertRaises((ValueError, KeyError, TypeError, IndexError)):
            KC.check(obj)

    def test_kernel_certificate_mutations(self):
        _, _, _, fin = run('q*p^3+q^2')
        _, _, _, span = run('q*p^3')
        _, _, _, prog = run('q^3*p^3')
        b = copy.deepcopy(fin); b['claim']['basis'] = b['claim']['basis'][:1]; self.rejects(b)
        b = copy.deepcopy(fin); b['claim']['points'] = b['claim']['points'][:-1]; self.rejects(b)
        b = copy.deepcopy(fin); b['support']['U'] = [[0, '0']]; self.rejects(b)
        b = copy.deepcopy(fin); b['support']['multipliers'][0] = [[0, 0, '7']]; self.rejects(b)
        b = copy.deepcopy(fin); b['claim']['kind'] = 'monomial_span'; self.rejects(b)
        b = copy.deepcopy(span); b['claim']['vertical_lines'] = [0, 1, 2]; self.rejects(b)
        b = copy.deepcopy(span); b['receipt']['closure'][0][0]['left_multiplier'][0][-1] = '99'; self.rejects(b)
        b = copy.deepcopy(prog); b['support']['common_factor']['linear_factors'] = [['1', '-2', '0']]; self.rejects(b)
        b = copy.deepcopy(prog); b['claim']['progressions'] = [[[0, 0], [2, 2]]]; self.rejects(b)
        b = copy.deepcopy(span); b['support']['monomial_generators'] = [0]; self.rejects(b)


if __name__ == '__main__':
    unittest.main()
