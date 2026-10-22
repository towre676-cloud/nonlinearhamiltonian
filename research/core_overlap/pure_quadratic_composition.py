#!/usr/bin/env python3
"""All-degree cores for H=P(p+b*q^2+c*q)+epsilon*q, b nonzero.

Proof: pure_quadratic_composition.md. Exact recognition and independent PBW
cross-checks; standard library only. Historical priority is not claimed.
"""
from __future__ import annotations

import argparse
import json
import random
import sys
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import pure_transverse as U


def comp(f, Q):
    """f(q,Q(q,p)) with the first variable unchanged."""
    return U.add(*(U.scale(U.mul({(i, 0): F(1)}, U.power(Q, j)), v)
                   for (i, j), v in f.items()))


def make(P, b=1, c=0, epsilon=0, d=0):
    Q = U.tidy({(0, 1): F(1), (2, 0): F(b), (1, 0): F(c), (0, 0): F(d)})
    H = U.add(*(U.scale(U.power(Q, j), F(v)) for j, v in P.items()),
              {(1, 0): F(epsilon)})
    return H, Q


def classify(H):
    """Recognize the composition family exactly; return None outside scope."""
    H = U.tidy(H)
    if not H:
        return None
    mu = max(j for i, j in H)
    if mu < 2:
        return None
    top = {(i, j): v for (i, j), v in H.items() if j == mu}
    if set(top) != {(0, mu)}:
        return None
    alpha = top[(0, mu)]
    B = {i: v for (i, j), v in H.items() if j == mu-1}
    V = {(i, 0): v/(mu*alpha) for i, v in B.items() if i}
    if max((i for i, j in V), default=-1) != 2 or not V.get((2, 0)):
        return None
    # In (q,z) coordinates p=z-V(q).
    inverse_Q = U.add({(0, 1): F(1)}, U.scale(V, -1))
    transformed = comp(H, inverse_Q)
    if any(i and (i, j) != (1, 0) for i, j in transformed):
        return None
    P = {j: v for (i, j), v in transformed.items() if i == 0}
    epsilon = transformed.get((1, 0), F(0))
    Q = U.add({(0, 1): F(1)}, V)
    assert make(P, V[(2, 0)], V.get((1, 0), F(0)), epsilon)[0] == H
    core = 'K[Q] + span{q, qQ, q^2}' if mu == 2 else 'K[Q] + K*q'
    return {'proved': True, 'route': 'QC', 'scope': 'parabolic quadratic composition with linear forcing',
            'degree': max(sum(k) for k in H), 'degree_P': mu, 'core': core,
            'Q': U.terms(Q), 'P': [[j, str(v)] for j, v in sorted(P.items())],
            'epsilon': str(epsilon), 'dimension': 'infinite',
            'active_part': ('infinite (epsilon != 0)' if epsilon else
                            ('three-dimensional modulo K[Q]' if mu == 2 else 'K*q modulo K[Q]')),
            'proof': 'pure_quadratic_composition.md'}


def c3_transformed(P, f, b):
    """Apply the proved operator in independent variables (t,z)."""
    Pz = {(0, j): F(v) for j, v in P.items()}
    P2, P3 = U.deriv(Pz, 0, 2), U.deriv(Pz, 0, 3)
    return U.add(U.scale(U.mul(P3, U.add(U.deriv(f, 3),
                                        U.scale(U.deriv(f, 1, 1), 6*b))), -1),
                 U.scale(U.mul(P2, U.deriv(f, 1, 2)), -6*b))


def self_test(matrix_checks=True):
    root = HERE.parents[1]
    sys.path[:0] = [str(root/'extensions'/'hamiltonian'), str(root/'extensions')]
    import weyl_receipts as W
    rng = random.Random(43120261022)
    counts = {'composition_instances': 0, 'chain_rule_gate_checks': 0,
              'stationary_tower_gate_checks': 0, 'invariant_sector_iterate_checks': 0,
              'recognition_rejections': 0, 'independent_filtered_dimensions': 0}
    for mu in (2, 3, 4, 5):
        for b, c, epsilon in ((F(1), F(0), F(0)),
                              (F(-2, 3), F(1, 2), F(2)),
                              (F(3, 2), F(-2), F(-1, 3))):
            P = {j: F(rng.randint(-2, 2)) for j in range(mu)}
            P[mu] = F(rng.choice((-2, 1, 3)))
            H, Q = make(P, b, c, epsilon)
            result = classify(H)
            assert result and result['degree_P'] == mu
            counts['composition_instances'] += 1
            for _ in range(8):
                f = U.tidy({(rng.randrange(6), rng.randrange(6)): F(rng.randint(-3, 3),
                                                                       rng.randint(1, 4))
                            for _ in range(7)})
                direct = W.act(W.gate(H, 3), comp(f, Q))
                expected = comp(c3_transformed(P, f, b), Q)
                assert direct == expected
                counts['chain_rule_gate_checks'] += 1
            for n in range(9):
                f = U.power(Q, n)
                for k, gate in W.gates(H).items():
                    assert not W.act(gate, f)
                    counts['stationary_tower_gate_checks'] += 1
            sector = [{(1, 0): F(1)}]
            if mu == 2:
                sector += [U.mul({(1, 0): F(1)}, Q), {(2, 0): F(1)}]
            for f in sector:
                for _ in range(6):
                    assert all(not W.act(gate, f) for gate in W.gates(H).values())
                    f = W.act(W.derivation(H), f)
                    counts['invariant_sector_iterate_checks'] += 1
            assert classify(U.add(H, {(1, 1): F(1)})) is None
            counts['recognition_rejections'] += 1
    # Exact finite-degree dimensions are independent sanity checks, not the
    # source of the theorem. Use the retained PBW + rational rank engine.
    if matrix_checks:
        from test_root_rigidity import filtered_dim
        for mu, epsilon in ((2, 0), (2, 1), (3, 0), (3, 2), (4, -1)):
            H, Q = make({mu: 1, 1: -2, 0: 1}, epsilon=epsilon)
            N = 2*mu+1
            expected = N//2+1+(3 if mu == 2 else 1)
            got = filtered_dim(H, N, 4)
            assert got == expected, (mu, epsilon, got, expected)
            counts['independent_filtered_dimensions'] += 1
    H, Q = make({2: 1})
    return {'status': 'passed', 'checks': counts,
            'quartic_counterexample': {'H': U.terms(H), 'Q': U.terms(Q), 'result': classify(H)},
            'limits': 'All-degree proof supplied separately; no nonlinear Moyal covariance or literature-priority claim.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', nargs='?')
    parser.add_argument('--classify', metavar='JSON')
    parser.add_argument('--skip-matrix-checks', action='store_true')
    args = parser.parse_args()
    if args.classify:
        rows = json.loads(Path(args.classify).read_text())
        if isinstance(rows, dict):
            rows = rows['hamiltonian']
        H = {}
        for row in rows:
            if (len(row) != 3 or any(type(x) is not int or x < 0 for x in row[:2])
                    or type(row[2]) not in (int, str)):
                raise ValueError('terms require exact rational coefficients')
            k = tuple(row[:2])
            H[k] = H.get(k, F(0)) + F(row[2])
        result = classify(H) or {'status': 'outside scope', 'proved': False}
    else:
        result = self_test(not args.skip_matrix_checks)
    if args.output:
        Path(args.output).write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))
