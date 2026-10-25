#!/usr/bin/env python3
"""Complete cores of H=A(p+u(q))^2+V(q), deg u>=3, arbitrary polynomial V.

The all-degree proof forces every core element into the six-dimensional
span of 1,H,q,Q,q^2,qQ. Full-output invariant-kernel
certificates independently replay the resulting six-versus-two classification.
Python standard library only; historical priority is not claimed.
"""
from __future__ import annotations

import argparse
import copy
import json
import sys
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path[:0] = [str(HERE), str(ROOT/'extensions')]
import pure_transverse as U
import qlinalg as L

FORMAT = 'quadratic-shear-core-v2'


def encode(f):
    return U.terms(f)


def decode(rows):
    if not isinstance(rows, list):
        raise ValueError('polynomial terms must be a list')
    f = {}
    for row in rows:
        if (not isinstance(row, list) or len(row) != 3
                or any(type(x) is not int or x < 0 for x in row[:2])
                or type(row[2]) not in (int, str)):
            raise ValueError('use nonnegative integer exponents and exact rational coefficients')
        k = tuple(row[:2])
        f[k] = f.get(k, F(0)) + F(row[2])
    return U.tidy(f)


def combine(basis, coefficients):
    return U.add(*(U.scale(f, c) for f, c in zip(basis, coefficients)))


def columns(polys):
    keys = sorted({k for f in polys for k in f})
    return [[f.get(k, F(0)) for f in polys] for k in keys]


def rank_independent(rows, ncols):
    """Independent fraction elimination, separate from compiler qlinalg."""
    work = [list(row) for row in rows]
    next_row = 0
    for col in range(ncols):
        pivot = next((r for r in range(next_row, len(work)) if work[r][col]), None)
        if pivot is None:
            continue
        work[next_row], work[pivot] = work[pivot], work[next_row]
        p = work[next_row][col]
        work[next_row] = [v/p for v in work[next_row]]
        for row in range(next_row+1, len(work)):
            if work[row][col]:
                factor = work[row][col]
                work[row] = [v-factor*w for v, w in zip(work[row], work[next_row])]
        next_row += 1
        if next_row == len(work):
            break
    return next_row


def coordinates(f, basis):
    keys = sorted(set(f).union(*(set(g) for g in basis)))
    rows = [[g.get(k, F(0)) for k in keys] for g in basis]
    return L.left_solve(rows, [f.get(k, F(0)) for k in keys], len(keys))


def recognize(H):
    H = U.tidy(H)
    if max((j for i, j in H), default=-1) != 2:
        return None
    quad = {(i, j): v for (i, j), v in H.items() if j == 2}
    if set(quad) != {(0, 2)}:
        return None
    A = quad[(0, 2)]
    u = {(i, 0): v/(2*A) for (i, j), v in H.items() if j == 1}
    m = max((i for i, j in u), default=-1)
    if m < 3:
        return None
    Q = U.add({(0, 1): F(1)}, u)
    V = U.add(H, U.scale(U.power(Q, 2), -A))
    assert all(j == 0 for i, j in V)
    return A, u, V, m


def produce(H):
    """Return full exclusion/closure certificate, or None outside theorem scope."""
    H = U.tidy(H)
    shape = recognize(H)
    if shape is None:
        return None
    A, u, V, m = shape
    Q = U.add({(0, 1): F(1)}, u)
    q = {(1, 0): F(1)}
    ambient = [{(0, 0): F(1)}, H, q, Q, U.power(q, 2), U.mul(q, Q)]
    images = [U.transvectant(H, f, 3) for f in ambient]
    null = L.null_basis(columns(images), len(ambient))
    basis = [combine(ambient, v) for v in null]
    stages = [[encode(f) for f in basis]]
    # At each stage compute {f in K: Df belongs to K}. The ambient image is
    # never projected back into the weight box.
    for _ in range(len(ambient)+1):
        n = len(basis)
        dbasis = [U.bracket(H, f) for f in basis]
        augmented = dbasis + [U.scale(f, -1) for f in basis]
        null = L.null_basis(columns(augmented), 2*n)
        new = [combine(basis, v[:n]) for v in null]
        if len(new) == n:
            break
        basis = new
        stages.append([encode(f) for f in basis])
    else:
        raise AssertionError('finite invariant-kernel iteration did not stabilize')
    closure = [coordinates(U.bracket(H, f), basis) for f in basis]
    assert all(v is not None for v in closure)
    cert = {'format': FORMAT, 'H': encode(H), 'weight': [1, m],
            'weighted_degree_bound': max(2*m, max((i for i,j in V), default=-1)),
            'momentum_degree_bound': 2, 'initial_third_gate_depth': 2,
            'third_gate_depth': (2 if max((i for i,j in V), default=-1) <= 2 else
                                 6 if max(i for i,j in V) == 3 else 4),
            'ambient_dimension': len(ambient),
            'ambient': [encode(f) for f in ambient],
            'A': str(A), 'u': encode(u), 'V': encode(V),
            'stages': stages, 'basis': [encode(f) for f in basis],
            'closure': [[str(v) for v in row] for row in closure]}
    check_certificate(cert)
    return cert


def check_certificate(cert):
    """Replay upper-bound exclusion and lower-bound closure independently.

    The all-degree six-dimensional upper space follows from the
    proved momentum-degree and invariant-core argument, not a numerical inference. Rank equalities establish that each supplied stage
    is the complete kernel/preimage rather than a chosen subspace.
    """
    if cert.get('format') != FORMAT:
        raise ValueError('unknown certificate format')
    H = decode(cert['H'])
    # Independently recover the completion of the square and finite upper space.
    if not H or any(j > 2 for i, j in H):
        raise ValueError('Hamiltonian is not quadratic in p')
    A = H.get((0, 2), F(0))
    if not A or any(i for i, j in H if j == 2):
        raise ValueError('p^2 coefficient must be a nonzero constant')
    u = {(i, 0): v/(2*A) for (i, j), v in H.items() if j == 1}
    m = max((i for i, j in u), default=-1)
    if m < 3:
        raise ValueError('higher shear degree required')
    Q = U.add({(0, 1): F(1)}, u)
    V = U.add(H, U.scale(U.power(Q, 2), -A))
    if any(j for i, j in V):
        raise ValueError('completion of square has a momentum residual')
    n = max((i for i, j in V), default=-1)
    if (cert['weight'] != [1, m] or cert['weighted_degree_bound'] != max(2*m, n)
            or cert.get('momentum_degree_bound') != 2 or F(cert['A']) != A
            or decode(cert['u']) != u or decode(cert['V']) != V):
        raise ValueError('shape metadata mismatch')
    sys.path.insert(0, str(ROOT/'extensions'/'hamiltonian'))
    import weyl_receipts as W
    D, C3 = W.derivation(H), W.gate(H, 3)
    q = {(1, 0): F(1)}
    ambient = [{(0, 0): F(1)}, H, q, Q, U.power(q, 2), U.mul(q, Q)]
    if (cert['ambient_dimension'] != len(ambient)
            or [decode(f) for f in cert['ambient']] != ambient):
        raise ValueError('ambient upper space mismatch')
    stages = [[decode(f) for f in rows] for rows in cert['stages']]
    if not stages or len(stages) > len(ambient)+1:
        raise ValueError('invalid number of stages')
    if cert.get('initial_third_gate_depth') != 2:
        raise ValueError('initial finite reduction depth mismatch')
    expected_depth = 2 if n <= 2 else 6 if n == 3 else 4
    if cert.get('third_gate_depth') != expected_depth:
        raise ValueError('sharp depth metadata mismatch')
    for f in ambient:
        g = f
        for _ in range(3):
            if W.act(C3, g):
                raise ValueError('initial finite space does not pass depth two')
            g = W.act(D, g)
    image_rank = rank_independent(columns([W.act(C3, f) for f in ambient]), len(ambient))
    for s, basis in enumerate(stages):
        if any(any(i+m*j > max(2*m, n) for i, j in f) for f in basis):
            raise ValueError('basis leaves certified upper weight bound')
        if rank_independent(columns(basis), len(basis)) != len(basis):
            raise ValueError('dependent stage basis')
        if any(W.act(C3, f) for f in basis):
            raise ValueError('stage fails third gate')
        if s == 0:
            if (any(rank_independent(columns(ambient+[f]), len(ambient)+1) != len(ambient) for f in basis)
                    or len(basis) != len(ambient)-image_rank):
                raise ValueError('initial gate kernel is incomplete')
        else:
            prev = stages[s-1]
            prev_n = len(prev)
            aug = [W.act(D, f) for f in prev] + [U.scale(f, -1) for f in prev]
            expected = 2*prev_n-rank_independent(columns(aug), 2*prev_n)
            if len(basis) != expected or len(basis) >= prev_n:
                raise ValueError('preimage dimension/rank mismatch')
            for f in basis:
                # Membership is checked by an independent augmented-rank test.
                if rank_independent(columns(prev+[f]), prev_n+1) != prev_n:
                    raise ValueError('preimage basis not contained in preceding stage')
                if rank_independent(columns(prev+[W.act(D, f)]), prev_n+1) != prev_n:
                    raise ValueError('derivative not in preceding stage')
    basis = [decode(f) for f in cert['basis']]
    if basis != stages[-1] or len(basis) > 6:
        raise ValueError('final core metadata mismatch')
    closure = [[F(v) for v in row] for row in cert['closure']]
    if len(closure) != len(basis) or any(len(row) != len(basis) for row in closure):
        raise ValueError('closure matrix shape mismatch')
    for f, row in zip(basis, closure):
        if W.act(D, f) != combine(basis, row):
            raise ValueError('derivation closure identity failed')
        # Both H and f have p degree at most two, so every odd gate >=5
        # vanishes by total p derivatives. Check actual finite list as well.
        if any(W.act(gate, f) for gate in W.gates(H).values()):
            raise ValueError('higher gate failed')
    return {'status': 'passed', 'dimension': len(basis), 'stages': len(stages),
            'ambient_dimension': len(ambient), 'weighted_degree_bound': max(2*m, n)}


def classify(H):
    cert = produce(H)
    if cert is None:
        return None
    dimension = len(cert['basis'])
    n = max((row[0] for row in cert['V']), default=-1)
    expected = 6 if n <= 2 else 2
    assert dimension == expected, ('closed classification disagrees with certificate', n, dimension)
    return {'proved': True, 'route': 'QF', 'scope': 'constant quadratic momentum coefficient; deg u>=3; arbitrary polynomial residual V',
            'dimension': dimension, 'core': ('span{1,q,Q,q^2,qQ,Q^2}' if n <= 2 else 'span{1,H}'),
            'basis': cert['basis'], 'closure': cert['closure'],
            'weight': cert['weight'], 'weighted_degree_bound': cert['weighted_degree_bound'],
            'ambient_dimension': cert['ambient_dimension'], 'momentum_degree_bound': 2,
            'third_gate_depth': cert['third_gate_depth'],
            'active_part': 'given by the certified Hamiltonian derivation matrix',
            'proof': 'quadratic_frontier.md', 'certificate': cert}


def make(u, V=None, A=1):
    u = {(i, 0): F(v) for i, v in u.items() if v}
    V = {(i, 0): F(v) for i, v in (V or {}).items() if v}
    Q = U.add({(0, 1): F(1)}, u)
    return U.add(U.scale(U.power(Q, 2), F(A)), V), Q


def self_test():
    records = []
    for m in (3, 4, 5):
        for V in ({}, {1: 2}, {2: 3}, {3: 1}, {2*m-1: -2},
                  {0: 2, 1: -1, 3: F(2, 3)}, {2*m: 1}, {2*m+3: -1},
                  {2*m: F(-2, 3)}):
            H, Q = make({m: F(2, 3), 2: -1, 1: 2, 0: F(1, 2)}, V, A=F(-3, 2))
            cert = produce(H)
            result = check_certificate(cert)
            assert result['dimension'] <= 6
            if max(V, default=-1) <= 2:
                assert result['dimension'] == 6
            else:
                assert result['dimension'] == 2
            expected_depth = 2 if max(V, default=-1) <= 2 else 6 if max(V) == 3 else 4
            assert cert['third_gate_depth'] == expected_depth
            witness = {(3, 0): F(1)} if expected_depth == 2 else {(1, 0): F(1)}
            g = witness
            for r in range(expected_depth):
                assert not U.transvectant(H, g, 3), (m, V, r)
                g = U.bracket(H, g)
            obstruction = U.transvectant(H, g, 3)
            assert obstruction
            u = {(i, 0): v for (i, j), v in Q.items() if j == 0}
            if expected_depth == 2:
                predicted = U.scale(U.deriv(u, 2), -288*F(-3, 2)**3)
            elif expected_depth == 4:
                predicted = U.scale(U.mul(U.deriv(u, 2), U.deriv({(i, 0): F(v) for i,v in V.items()}, 4)), 96*F(-3, 2)**4)
            else:
                v3 = U.deriv({(i, 0): F(v) for i,v in V.items()}, 3)
                predicted = U.scale(U.mul(U.deriv(u, 2), U.power(v3, 2)), -960*F(-3, 2)**5)
            assert obstruction == predicted, (m, V, obstruction, predicted)
            records.append({'m': m, 'sharp_third_gate_depth': expected_depth, 'potential': [[i, str(v)] for i, v in sorted(V.items())],
                            **result, 'stage_dimensions': [len(s) for s in cert['stages']]})
    H, Q = make({3: 1}, {3: 1})
    cert = produce(H)
    assert len(cert['basis']) == 2
    # Keep a complete modest example in the result receipt for external replay.
    sample = cert
    for mutate in (lambda c: c.update(weighted_degree_bound=7),
                   lambda c: c['closure'][0].__setitem__(0, '1'),
                   lambda c: c['basis'].pop(),
                   lambda c: c['stages'][0].pop()):
        bad = copy.deepcopy(cert)
        mutate(bad)
        try:
            check_certificate(bad)
        except (ValueError, IndexError):
            pass
        else:
            raise AssertionError('forged certificate accepted')
    for u in ({2: 1}, {1: 2}, {}):
        H, Q = make(u, {3: 1})
        assert produce(H) is None
    assert produce({(1,2): F(1), (7,0): F(1)}) is None
    return {'status': 'passed', 'format': FORMAT, 'instances': records,
            'forgery_rejections': 4, 'scope_rejections': 4, 'sharp_depth_checks': len(records), 'sample_certificate': sample,
            'scope': 'Complete higher-shear constant-quadratic classification for arbitrary polynomial V. Quadratic shears and variable leading p^2 coefficient remain outside scope.'}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('output', nargs='?')
    ap.add_argument('--classify', type=Path)
    ap.add_argument('--check-certificate', type=Path)
    args = ap.parse_args()
    if args.classify:
        rows = json.loads(args.classify.read_text())
        H = decode(rows['hamiltonian'] if isinstance(rows, dict) else rows)
        result = classify(H) or {'proved': False, 'status': 'outside scope'}
    elif args.check_certificate:
        result = check_certificate(json.loads(args.check_certificate.read_text()))
    else:
        result = self_test()
    if args.output:
        Path(args.output).write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
