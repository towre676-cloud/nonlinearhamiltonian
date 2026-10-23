#!/usr/bin/env python3
"""Exact finite linear target-observer seed; Python standard library only.

Commands: verify; compile MODEL.json [--output CERT.json]; check CERT.json [--input MODEL.json].
This implements algebraic closure/factorization, not general robust/adaptive optimization.
"""
from __future__ import annotations
import argparse
from copy import deepcopy
from fractions import Fraction as F
from functools import lru_cache
import hashlib
import json
from pathlib import Path


def rat(x):
    if isinstance(x, (float, bool)) or not isinstance(x, (str, int, F)):
        raise ValueError('Use exact integer or rational strings, not float/bool values')
    return F(x)


def matrix(rows, columns, row_count=None):
    if not isinstance(rows, list) or (row_count is not None and len(rows) != row_count):
        raise ValueError('Wrong matrix row count')
    if any(not isinstance(row, list) or len(row) != columns for row in rows):
        raise ValueError('Wrong matrix column count')
    return [[rat(x) for x in row] for row in rows]


def strings(rows):
    return [[str(x) for x in row] for row in rows]


def normalize(model):
    n = model['dimension']
    if isinstance(n, bool) or not isinstance(n, int) or n < 1:
        raise ValueError('dimension must be a positive integer')
    actions = model['actions']
    if not isinstance(actions, dict) or any(not isinstance(k, str) or not k for k in actions):
        raise ValueError('actions must have nonempty string names')
    result = dict(dimension=n, actions={k: strings(matrix(v, n, n)) for k, v in sorted(actions.items())},
                  target=strings(matrix(model['target'], n)))
    if 'observation' in model:
        result['observation'] = strings(matrix(model['observation'], n))
    return result


def digest(model):
    raw = json.dumps(model, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()
    return hashlib.sha256(raw).hexdigest()


def rref(rows, columns):
    a = deepcopy(rows)
    pivots = []
    for col in range(columns):
        pivot = next((i for i in range(len(pivots), len(a)) if a[i][col]), None)
        if pivot is None:
            continue
        k = len(pivots)
        a[k], a[pivot] = a[pivot], a[k]
        value = a[k][col]
        a[k] = [x / value for x in a[k]]
        for i in range(len(a)):
            if i != k and a[i][col]:
                value = a[i][col]
                a[i] = [x - value * y for x, y in zip(a[i], a[k])]
        pivots.append(col)
        if len(pivots) == len(a):
            break
    return a, pivots


def rank(rows, columns):
    return len(rref(rows, columns)[1])


def row_times(row, a):
    return [sum((row[i] * a[i][j] for i in range(len(row))), F(0)) for j in range(len(a[0]))]


def product(a, b, output_columns=None):
    columns = len(b[0]) if b else (output_columns or 0)
    return [[sum((x * b[k][j] for k, x in enumerate(row)), F(0)) for j in range(columns)] for row in a]


def coefficients(rows, target, n):
    """Find c with c*rows=target; free coefficients set to zero; None if impossible."""
    m = len(rows)
    augmented = [[rows[j][i] for j in range(m)] + [target[i]] for i in range(n)]
    reduced, pivots = rref(augmented, m)
    if any(not any(row[:m]) and row[-1] for row in reduced):
        return None
    c = [F(0)] * m
    for i, pivot in enumerate(pivots):
        c[pivot] = reduced[i][-1]
    if product([c], rows, n)[0] != target:
        raise AssertionError('Internal solve identity failed')
    return c


def null_basis(rows, n):
    reduced, pivots = rref(rows, n)
    answer = []
    for free in range(n):
        if free not in pivots:
            v = [F(0)] * n
            v[free] = F(1)
            for i, pivot in enumerate(pivots):
                v[pivot] = -reduced[i][free]
            answer.append(v)
    return answer


def dot(row, v):
    return sum((a * b for a, b in zip(row, v)), F(0))


def word_row(target_row, word, actions):
    """Chronological word a,b means state A_b A_a x, hence row G A_b A_a."""
    row = target_row[:]
    for action in reversed(word):
        row = row_times(row, actions[action])
    return row


def compile_model(model):
    model = normalize(model)
    n = model['dimension']
    actions = {k: matrix(v, n, n) for k, v in model['actions'].items()}
    g = matrix(model['target'], n)
    q, provenance = [], []
    for i, row in enumerate(g):
        if rank(q + [row], n) > len(q):
            q.append(row)
            provenance.append(dict(target_row=i, word=[]))
    history = [len(q)]
    while True:
        old = len(q)
        for i in range(old):
            for name, a in actions.items():
                candidate = row_times(q[i], a)
                if rank(q + [candidate], n) > len(q):
                    q.append(candidate)
                    # Right multiplication prepends an action to the chronological word.
                    provenance.append(dict(target_row=provenance[i]['target_row'],
                                           word=[name] + provenance[i]['word']))
        if len(q) == old:
            break
        history.append(len(q))
    quotient = {name: [coefficients(q, row_times(row, a), n) for row in q] for name, a in actions.items()}
    c = [coefficients(q, row, n) for row in g]
    cert = dict(format='observer-closure-v1', model=model, model_sha256=digest(model),
                basis=strings(q), basis_words=provenance, quotient_actions={k: strings(v) for k, v in quotient.items()},
                target_factor=strings(c), diagnostics={'basis_dimensions': history, 'proof_source': 'exact identities and word provenance; not sampled trajectories'})
    if 'observation' in model:
        h = matrix(model['observation'], n)
        recovery = [coefficients(h, row, n) for row in q]
        if all(row is not None for row in recovery):
            cert['panel'] = dict(status='recoverable', recovery=strings(recovery))
        else:
            witness = next(v for v in null_basis(h, n) if any(dot(row, v) for row in q))
            lost = next(i for i, row in enumerate(q) if dot(row, witness))
            cert['panel'] = dict(status='impossible', invisible_state=[str(x) for x in witness], lost_basis_row=lost,
                                 lost_target_word=provenance[lost])
    check_certificate(cert, model)
    return cert


def check_certificate(cert, expected_model=None):
    """Check supplied identities/provenance; does not call or trust compile_model."""
    if cert.get('format') != 'observer-closure-v1':
        raise ValueError('Unknown certificate format')
    model = normalize(cert['model'])
    if model != cert['model'] or digest(model) != cert['model_sha256']:
        raise ValueError('Model normalization/hash mismatch')
    if expected_model is not None and model != normalize(expected_model):
        raise ValueError('Certificate belongs to a different input model')
    n = model['dimension']
    actions = {k: matrix(v, n, n) for k, v in model['actions'].items()}
    g = matrix(model['target'], n)
    q = matrix(cert['basis'], n)
    r = len(q)
    if rank(q, n) != r or len(cert['basis_words']) != r:
        raise ValueError('Dependent basis or wrong provenance count')
    for row, witness in zip(q, cert['basis_words']):
        i, word = witness['target_row'], witness['word']
        if isinstance(i, bool) or not isinstance(i, int) or not 0 <= i < len(g):
            raise ValueError('Invalid target-row provenance')
        if not isinstance(word, list) or any(a not in actions for a in word):
            raise ValueError('Invalid word provenance')
        if row != word_row(g[i], word, actions):
            raise ValueError('Basis row is not its declared target word')
    c = matrix(cert['target_factor'], r, len(g))
    if product(c, q, n) != g:
        raise ValueError('Target factorization failed')
    if set(cert['quotient_actions']) != set(actions):
        raise ValueError('Action alphabet mismatch')
    for name, a in actions.items():
        b = matrix(cert['quotient_actions'][name], r, r)
        if product(q, a, n) != product(b, q, n):
            raise ValueError('Action intertwining failed')
    if 'observation' in model:
        h = matrix(model['observation'], n)
        panel = cert['panel']
        if panel['status'] == 'recoverable':
            k = matrix(panel['recovery'], len(h), r)
            if product(k, h, n) != q:
                raise ValueError('Sensor recovery identity failed')
        elif panel['status'] == 'impossible':
            v = [rat(x) for x in panel['invisible_state']]
            i = panel['lost_basis_row']
            if len(v) != n or not isinstance(i, int) or not 0 <= i < r:
                raise ValueError('Malformed invisible-state witness')
            if any(dot(row, v) for row in h) or not dot(q[i], v):
                raise ValueError('Invisible-state witness failed')
            if panel['lost_target_word'] != cert['basis_words'][i]:
                raise ValueError('Lost output word mismatch')
        else:
            raise ValueError('Unknown panel claim')
    return dict(status='passed', minimal_linear_state_dimension=r,
                scope='all allowed finite words and all initial states of the encoded finite rational model',
                input_bound=expected_model is not None)


def verify():
    checks = []
    def record(name, condition):
        if not condition:
            raise AssertionError(name)
        checks.append(name)
    def rejected(cert, expected, name):
        try:
            check_certificate(cert, expected)
        except (ValueError, KeyError, IndexError, TypeError):
            record(name, True)
        else:
            record(name, False)
    examples = [
        ('present_is_not_future', dict(dimension=2, actions={'step': [[1, 1], [0, 1]]}, target=[[1, 0]], observation=[[1, 0]]), 2, 'impossible'),
        ('shared_nuisance_stays_hidden', dict(dimension=2, actions={'step': [[1, 0], [0, 1]]}, target=[[0, 1]], observation=[[0, 1]]), 1, 'recoverable'),
        ('shared_nuisance_feeds_target', dict(dimension=2, actions={'step': [[1, 0], [1, 1]]}, target=[[0, 1]], observation=[[0, 1]]), 2, 'impossible'),
        ('multioutput_dimension_not_recurrence_degree', dict(dimension=2, actions={'step': [[1, 0], [0, 1]]}, target=[[1, 0], [0, 1]], observation=[[1, 0], [0, 1]]), 2, 'recoverable'),
        ('ill_conditioned_but_exact', dict(dimension=2, actions={'step': [[1, 0], [0, 1]]}, target=[[0, 1]], observation=[[1, 0], [0, '1/1000000']]), 1, 'recoverable'),
        ('zero_target_no_sensors', dict(dimension=2, actions={'step': [[1, 1], [0, 1]]}, target=[[0, 0]], observation=[]), 0, 'recoverable'),
        ('empty_alphabet_only_current_target', dict(dimension=2, actions={}, target=[[1, 1]], observation=[[1, 1], [2, 2]]), 1, 'recoverable'),
    ]
    certs = {}
    for name, model, expected_rank, status in examples:
        cert = compile_model(model)
        result = check_certificate(cert, model)
        certs[name] = cert
        record(name + ':minimal_dimension', result['minimal_linear_state_dimension'] == expected_rank)
        record(name + ':panel_claim', cert['panel']['status'] == status)
    ill = certs['ill_conditioned_but_exact']
    record('exact_recovery_amplification_is_one_million', ill['panel']['recovery'] == [['0', '1000000']])
    record('smaller_noise_cap_has_exact_negative_witness', F(999999)**2/F(1000000)**2 - 1 < 0)
    order = dict(dimension=2, actions={'a': [[0, 1], [0, 0]], 'b': [[0, 0], [1, 0]]}, target=[[1, 0]], observation=[[1, 0], [0, 1]])
    cert = compile_model(order)
    acts = {k: matrix(v, 2, 2) for k, v in order['actions'].items()}
    record('chronological_action_order_is_not_commutative', word_row([F(1), F(0)], ['a', 'b'], acts) != word_row([F(1), F(0)], ['b', 'a'], acts))
    bad = deepcopy(cert); bad['basis_words'][1]['word'] = ['b']
    rejected(bad, order, 'wrong_word_provenance_rejected')
    bad = deepcopy(cert); bad['target_factor'][0][0] = '2'
    rejected(bad, order, 'corrupted_target_factor_rejected')
    bad = deepcopy(cert); bad['quotient_actions']['a'][0][0] = '1'
    rejected(bad, order, 'false_closed_projection_rejected')
    changed = deepcopy(order); changed['target'] = [[0, 1]]
    rejected(cert, changed, 'different_input_model_rejected')
    # Each triangular action has eigenvalues 1/2. Their symmetric product has p(1)<0,
    # hence a real eigenvalue greater than one: individual stability is insufficient.
    record('individually_stable_actions_can_have_unstable_product', F(1) - F(3, 2) + F(1, 16) < 0)
    record('shared_noise_difference_variance', F(101) + F(101) - 2*F(100) == 2)
    record('independent_noise_bars_change_model', F(101) + F(101) == 202)
    # Tiny independent Bellman fixture: general adaptive implementation remains future work.
    tests = [(1, {'a': 0, 'b': 1, 'c': 1}), (2, {'a': 1, 'b': 0, 'c': 1}), (4, {'a': 0, 'b': 1, 'c': 2})]
    def cost(labels):
        @lru_cache(None)
        def value(state):
            if len({labels[x] for x in state}) <= 1:
                return 0
            best = float('inf')
            for price, outcomes in tests:
                fibres = [tuple(x for x in state if outcomes[x] == y) for y in sorted({outcomes[x] for x in state})]
                if len(fibres) > 1:
                    best = min(best, price + max(value(fibre) for fibre in fibres))
            return best
        return value(('a', 'b', 'c'))
    record('full_identification_cost_three', cost({'a': 0, 'b': 1, 'c': 2}) == 3)
    record('target_only_identification_cost_one', cost({'a': 0, 'b': 1, 'c': 1}) == 1)
    return dict(status='passed', checks=len(checks), names=checks,
                scope='exact finite reference fixtures and certificate identities; general theorem proof is in observation_plan.md')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command')
    sub.add_parser('verify')
    build = sub.add_parser('compile'); build.add_argument('model', type=Path); build.add_argument('--output', type=Path)
    check = sub.add_parser('check'); check.add_argument('certificate', type=Path); check.add_argument('--input', type=Path)
    args = parser.parse_args()
    if args.command in (None, 'verify'):
        result = verify()
    elif args.command == 'compile':
        result = compile_model(json.loads(args.model.read_text()))
        if args.output:
            args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
            print(json.dumps({'status': 'written', 'path': str(args.output)})); return
    else:
        original = json.loads(args.input.read_text()) if args.input else None
        result = check_certificate(json.loads(args.certificate.read_text()), original)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
