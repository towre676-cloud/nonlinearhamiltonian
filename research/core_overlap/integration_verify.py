#!/usr/bin/env python3
"""Exact coefficient-box census and decision-procedure transport checks.

Finite checks complement the all-degree proofs. They never upgrade an
unclassified Hamiltonian to a theorem. No output is projected by degree.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import importlib.util
import json
import random
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path[:0] = [str(HERE), str(ROOT / 'extensions/hamiltonian')]
import pure_transverse as PP
import check_two_root as TR
import weyl_receipts as W


def run():
    counts = {'coefficient_box_families': 0, 'broken_closure_perturbations': 0,
              'affine_transports': 0, 'direct_gate_replays': 0,
              'direct_closure_replays': 0}
    rng = random.Random(20261022)
    fixtures = []
    # This is the full declared box, rather than a random sample.
    for a, u3, u2, u1, A, B, C, beta in product(
            range(1, 5), (-1, 1), (-1, 0, 1), (-1, 0, 1),
            (-1, 1), (-1, 0, 1), (-1, 0, 1), (-1, 0, 1)):
        H, J = PP.family(a=a, u={3: u3, 2: u2, 1: u1},
                         coeffs=(A, B, C), beta=beta)
        result = PP.classify(H)
        assert result['dimension'] == 3
        bad = PP.add(H, {(0, 1): F(1)})
        assert PP.classify(bad)['dimension'] == 2
        counts['coefficient_box_families'] += 1
        counts['broken_closure_perturbations'] += 1
        if counts['coefficient_box_families'] % 91 == 0:
            fixtures.append((H, J))
    # Actual public decision route after rational affine coordinate changes.
    for H, J in fixtures:
        while True:
            a, b, c, d = [F(rng.randint(-2, 2)) for _ in range(4)]
            if a*d-b*c:
                break
        x0, y0 = F(rng.randint(-3, 3), 2), F(rng.randint(-3, 3), 3)
        X = {(1, 0): a, (0, 1): b, (0, 0): x0}
        Y = {(1, 0): c, (0, 1): d, (0, 0): y0}
        Ht = TR.comp(H, X, Y)
        res = TR.classify(Ht)
        assert res['route'] == 'PP' and res['proved']
        assert res['core'] == 'span{1, H, G}'
        Gt = {tuple(map(int, k.split(','))): F(v) for k, v in res['G'].items()}
        assert TR.in_span(W.act(W.derivation(Ht), Gt),
                          [{(0, 0): F(1)}, Ht, Gt])
        counts['direct_closure_replays'] += 1
        for k in range(3, res['degree']+1, 2):
            assert W.act(W.gate(Ht, k), Gt) == {}
            counts['direct_gate_replays'] += 1
        counts['affine_transports'] += 1
    basic, generator = PP.family()
    decision = TR.classify(basic)
    assert decision['generator_degree'] == 3
    assert PP.bracket(basic, generator) == basic
    # The original conjectural pure-top result is no longer emitted here.
    assert TR.classify({(6, 0): F(1), (2, 2): F(1)})['proved'] is False
    return {'status': 'passed', 'counts': counts,
            'basic_counterexample': {'H': PP.terms(basic), 'G': PP.terms(generator),
                                    'decision': decision},
            'scope': 'Exact declared coefficient box and rational affine transports; all-degree classification rests on the written proof.'}


if __name__ == '__main__':
    result = run()
    if len(sys.argv) == 2:
        Path(sys.argv[1]).write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))
