#!/usr/bin/env python3
"""Independent checker for noise-aware sensor-panel certificates (noise-panel-v1)
and for all-time invariant-metric certificates (invariant-metric-v1).

Noise model. Readings y = H_P x + eta with eta^T R_P^{-1} eta <= delta^2, where R_P is
the principal block of one declared joint positive definite matrix R (correlated
noise is kept, never replaced by independent bars). A target T is recoverable with
worst-case amplification at most gamma, for every initial state, exactly when

    M(P,T) = gamma^2 H_P^T R_P^{-1} H_P - T^T T  is positive semidefinite.

Certificate tree. Every node fixes included sensors P and excluded sensors X; the
undecided rest is U. Leaves are
  feasible    M(P,T) = L diag(d) L^T with d >= 0 for every target T (checked exactly);
              costs are nonnegative, so no descendant is cheaper than P itself;
  infeasible  a vector v with v^T M(P u U, T) v < 0; since H_S^T R_S^{-1} H_S is monotone
              in S (Schur complement), the same v refutes every panel inside P u U;
  cost        cost(P) >= the claimed optimum, so no descendant improves on it (ties
              are not enumerated: tie policy one_optimum);
  open        only in an 'incomplete' certificate, which then claims a lower bound only.
Branch nodes split one undecided sensor into include/exclude children. The checker
verifies coverage, every leaf, and that the optimum is attained by a feasible leaf.

Usage: check_panel.py CERT.json --input MODEL.json
"""
from __future__ import annotations
import argparse
import hashlib
import itertools
import json
import sys
from fractions import Fraction as F
from pathlib import Path

FORMAT = 'noise-panel-v1'
METRIC_FORMAT = 'invariant-metric-v1'


def _rat(x):
    if type(x) not in (int, str) and not isinstance(x, F):
        raise ValueError('coefficients must be exact integers or rational strings')
    return F(x)


def _mat(rows, cols, nrows=None):
    if not isinstance(rows, list) or (nrows is not None and len(rows) != nrows):
        raise ValueError('wrong matrix row count')
    if any(not isinstance(r, list) or len(r) != cols for r in rows):
        raise ValueError('wrong matrix column count')
    return [[_rat(x) for x in r] for r in rows]


def _mul(a, b, cols):
    return [[sum((x * b[k][j] for k, x in enumerate(r)), F(0)) for j in range(cols)] for r in a]


def _t(a, cols):
    return [[a[i][j] for i in range(len(a))] for j in range(cols)]


def _eye(n):
    return [[F(int(i == j)) for j in range(n)] for i in range(n)]


def _quad(m, v):
    return sum((v[i] * m[i][j] * v[j] for i in range(len(v)) for j in range(len(v))), F(0))


def digest(model):
    raw = json.dumps(model, sort_keys=True, separators=(',', ':'), ensure_ascii=False)
    return hashlib.sha256(raw.encode()).hexdigest()


def read_model(model):
    n = model['dimension']
    if type(n) is not int or n < 1:
        raise ValueError('dimension must be a positive integer')
    sensors = model['sensors']
    rows = [_mat([s['row']], n)[0] for s in sensors]
    costs = [_rat(s['cost']) for s in sensors]
    if any(c < 0 for c in costs):
        raise ValueError('sensor costs must be nonnegative')
    k = len(sensors)
    R = _mat(model['noise'], k, k)
    if any(R[i][j] != R[j][i] for i in range(k) for j in range(k)):
        raise ValueError('noise matrix must be symmetric')
    for m in range(1, k + 1):            # Sylvester: leading principal minors > 0
        if _det([r[:m] for r in R[:m]]) <= 0:
            raise ValueError('noise matrix must be positive definite')
    g2 = _rat(model['gamma_squared'])
    if g2 < 0:
        raise ValueError('gamma_squared must be nonnegative')
    t = model['targets']
    if t['mode'] == 'explicit':
        targets = [_mat(m, n) for m in t['matrices']]
    elif t['mode'] == 'finite_horizon':
        acts = {a: _mat(v, n, n) for a, v in sorted(t['actions'].items())}
        g = _mat(t['target'], n)
        h = t['horizon']
        if type(h) is not int or h < 0:
            raise ValueError('horizon must be a nonnegative integer')
        targets = []
        for length in range(h + 1):
            for word in itertools.product(sorted(acts), repeat=length):
                m = g
                for a in reversed(word):      # chronological word: G A_ak ... A_a1
                    m = _mul(m, acts[a], n)
                targets.append(m)
    else:
        raise ValueError('unknown target mode')
    if model['contract'] == 'stacked':
        targets = [[r for m in targets for r in m]]
    elif model['contract'] != 'per_target':
        raise ValueError('contract must be per_target or stacked')
    tt = [_mul(_t(m, n), m, n) if m else [[F(0)] * n for _ in range(n)] for m in targets]
    return n, rows, costs, R, g2, tt


def _det(a):
    a = [r[:] for r in a]
    n, det = len(a), F(1)
    for c in range(n):
        p = next((i for i in range(c, n) if a[i][c]), None)
        if p is None:
            return F(0)
        if p != c:
            a[c], a[p] = a[p], a[c]
            det = -det
        det *= a[c][c]
        for i in range(c + 1, n):
            f = a[i][c] / a[c][c]
            a[i] = [x - f * y for x, y in zip(a[i], a[c])]
    return det


def info(rows, R, S, rinv, n):
    """H_S^T R_S^{-1} H_S, after verifying the supplied inverse of the principal block."""
    S = sorted(S)
    if not S:
        return [[F(0)] * n for _ in range(n)]
    RS = [[R[i][j] for j in S] for i in S]
    Ri = _mat(rinv, len(S), len(S))
    if _mul(RS, Ri, len(S)) != _eye(len(S)):
        raise ValueError('supplied inverse of the noise block is wrong')
    HS = [rows[i] for i in S]
    return _mul(_mul(_t(HS, n), Ri, len(S)), HS, n)


def _check_ldl(M, ldl):
    n = len(M)
    Lm = _mat(ldl['L'], n, n)
    d = [_rat(x) for x in ldl['d']]
    if len(d) != n or any(x < 0 for x in d):
        raise ValueError('LDL certificate needs nonnegative diagonal')
    D = [[d[i] if i == j else F(0) for j in range(n)] for i in range(n)]
    if _mul(_mul(Lm, D, n), _t(Lm, n), n) != M:
        raise ValueError('LDL certificate does not reproduce the matrix')


def check(cert, model):
    if cert.get('format') != FORMAT or cert.get('coefficient_domain') != 'Q':
        raise ValueError('not a noise-panel-v1 certificate over Q')
    if cert.get('model_sha256') != digest(model):
        raise ValueError('certificate belongs to another model')
    if cert.get('tie_policy') != 'one_optimum':
        raise ValueError('only tie policy one_optimum is supported')
    n, rows, costs, R, g2, tt = read_model(model)
    k = len(rows)
    status = cert['status']
    opt_cost = F(cert['optimum']['cost']) if cert.get('optimum') else None
    feasible_costs, open_bounds = [], []
    counts = {'branch': 0, 'feasible': 0, 'infeasible': 0, 'cost': 0, 'open': 0}

    def M_of(S, rinv):
        J = info(rows, R, S, rinv, n)
        return [[[g2 * J[i][j] - T[i][j] for j in range(n)] for i in range(n)] for T in tt]

    stack = [(cert['tree'], frozenset(), frozenset())]
    while stack:
        node, P, X = stack.pop()
        if sorted(node['include']) != sorted(P) or sorted(node['exclude']) != sorted(X):
            raise ValueError('node sensor sets are inconsistent with the tree')
        kind = node['kind']
        counts[kind] = counts.get(kind, 0) + 1
        cost = sum((costs[i] for i in P), F(0))
        if kind == 'branch':
            j = node['sensor']
            if type(j) is not int or not 0 <= j < k or j in P or j in X:
                raise ValueError('branch sensor must be undecided')
            inc, exc = node['children']
            stack += [(inc, P | {j}, X), (exc, P, X | {j})]
        elif kind == 'feasible':
            Ms = M_of(P, node['rinv'])
            if len(node['ldl']) != len(Ms):
                raise ValueError('one PSD certificate per target required')
            for M, ldl in zip(Ms, node['ldl']):
                _check_ldl(M, ldl)
            feasible_costs.append((cost, sorted(P)))
        elif kind == 'infeasible':
            allowed = frozenset(range(k)) - X
            Ms = M_of(allowed, node['rinv'])
            t = node['target']
            v = [_rat(x) for x in node['vector']]
            if type(t) is not int or not 0 <= t < len(Ms) or len(v) != n or not _quad(Ms[t], v) < 0:
                raise ValueError('negative quadratic witness fails')
        elif kind == 'cost':
            if opt_cost is None or cost < opt_cost:
                raise ValueError('cost pruning without a cheaper or equal incumbent')
        elif kind == 'open':
            if status != 'incomplete':
                raise ValueError('open node in a certificate claiming completeness')
            open_bounds.append(cost)
        else:
            raise ValueError('unknown node kind')
    if status == 'optimal':
        if not feasible_costs or min(c for c, _ in feasible_costs) != opt_cost:
            raise ValueError('claimed optimum is not the cheapest feasible leaf')
        if (opt_cost, sorted(cert['optimum']['sensors'])) not in feasible_costs:
            raise ValueError('claimed optimal panel is not a certified feasible leaf')
        return {'status': 'passed', 'claim': 'optimal', 'cost': str(opt_cost), 'sensors': cert['optimum']['sensors'],
                'nodes': counts, 'scope': 'exact minimum over all subsets of the finite menu; initial static '
                'panel, deterministic ellipsoidal noise, worst case over all initial states'}
    if status == 'infeasible':
        if feasible_costs or opt_cost is not None:
            raise ValueError('infeasibility claim with a feasible leaf')
        return {'status': 'passed', 'claim': 'infeasible', 'nodes': counts,
                'scope': 'no subset of the finite menu meets the declared amplification cap'}
    if status == 'incomplete':
        lb = min(open_bounds + [c for c, _ in feasible_costs]) if open_bounds or feasible_costs else None
        if str(lb) != cert['lower_bound']:
            raise ValueError('declared lower bound is wrong')
        return {'status': 'passed', 'claim': 'incomplete', 'lower_bound': str(lb),
                'incumbent': cert.get('optimum'), 'nodes': counts,
                'scope': 'bounds only; no optimality claim'}
    raise ValueError('unknown status')


def check_metric(cert, model):
    """invariant-metric-v1: S with B_a^T S B_a <= S, C^T C <= S, Q^T S Q <= gamma^2 J(P).

    Then every future output error is at most gamma*delta for the reconstruction of Q x;
    the certificate is sufficient, not necessary.
    """
    if cert.get('format') != METRIC_FORMAT or cert.get('model_sha256') != digest(model):
        raise ValueError('not an invariant-metric-v1 certificate for this model')
    n, rows, costs, R, g2, _ = read_model(model)
    obs = cert['observer']             # a checked observer-closure-v2 certificate is replayed separately
    r = obs['rank']
    Q = _mat(obs['basis'], n, r)
    C = _mat(obs['target_factor'], r)
    S = _mat(cert['S'], r, r)
    P = cert['panel']
    if S != _t(S, r):
        raise ValueError('S must be symmetric')
    conds = []
    for a, B in sorted(obs['quotient_actions'].items()):
        B = _mat(B, r, r)
        conds.append(('contract_' + a, [[S[i][j] - x for j, x in enumerate(row)]
                                        for i, row in enumerate(_mul(_mul(_t(B, r), S, r), B, r))]))
    CtC = _mul(_t(C, r), C, r)
    conds.append(('target', [[S[i][j] - CtC[i][j] for j in range(r)] for i in range(r)]))
    J = info(rows, R, P, cert['rinv'], n)
    QSQ = _mul(_mul(_t(Q, n), S, r), Q, n)
    conds.append(('panel', [[g2 * J[i][j] - QSQ[i][j] for j in range(n)] for i in range(n)]))
    if len(cert['ldl']) != len(conds):
        raise ValueError('one PSD certificate per condition required')
    for (_, M), ldl in zip(conds, cert['ldl']):
        _check_ldl(M, ldl)
    return {'status': 'passed', 'claim': 'all_time_bound_sufficient', 'conditions': [c for c, _ in conds],
            'scope': 'sufficient certificate: every future target output is recovered with amplification '
                     '<= gamma for all words; absence of such S is not evidence of instability'}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('certificate', type=Path)
    ap.add_argument('--input', type=Path, required=True)
    a = ap.parse_args()
    try:
        cert, model = json.loads(a.certificate.read_text()), json.loads(a.input.read_text())
        fn = check_metric if cert.get('format') == METRIC_FORMAT else check
        print(json.dumps(fn(cert, model), indent=2))
    except (ValueError, KeyError, TypeError, IndexError, ZeroDivisionError) as e:
        print(json.dumps({'status': 'rejected', 'reason': str(e)}))
        sys.exit(2)


if __name__ == '__main__':
    main()
