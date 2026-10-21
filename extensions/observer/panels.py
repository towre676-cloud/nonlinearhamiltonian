#!/usr/bin/env python3
"""Certified cheapest noise-aware static sensor panel (noise-panel-v1 producer).

Branch and bound over a finite sensor menu. At each node (included P, excluded X):
  * if P itself meets every target's amplification cap -> feasible leaf (PSD receipts);
  * else if even P u U fails some target -> infeasible leaf with a negative quadratic
    witness, valid for every descendant by monotonicity of the information matrix;
  * else if cost(P) >= incumbent -> cost leaf;
  * else branch on the next undecided sensor (include first).
A node budget turns the remaining nodes into 'open' leaves and the claim into
'incomplete' with an exact lower bound. The certificate is replayed by the
independent check_panel.py before it is returned.

Also: `exhaustive` (independent small-menu oracle, no pruning) and `metric`
(builds an invariant-metric-v1 receipt for a user-supplied S; sufficient only).

Usage:
  panels.py solve MODEL.json [--output CERT.json] [--max-nodes N]
  panels.py exhaustive MODEL.json
"""
from __future__ import annotations
import argparse
import itertools
import json
import sys
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parent)]
import qlinalg as L          # noqa: E402
import check_panel as C      # noqa: E402  (model reading/hash only; verification is replayed at the end)


class Problem:
    def __init__(self, model):
        self.model = model
        self.n, self.rows, self.costs, self.R, self.g2, self.tt = C.read_model(model)
        self.k = len(self.rows)
        self._cache = {}

    def rinv(self, S):
        S = tuple(sorted(S))
        return L.inverse([[self.R[i][j] for j in S] for i in S]) if S else []

    def matrices(self, S):
        S = tuple(sorted(S))
        if S not in self._cache:
            ri = self.rinv(S)
            n = self.n
            if S:
                HS = [self.rows[i] for i in S]
                J = L.mul(L.mul(L.transpose(HS, n), ri), HS, n)
            else:
                J = L.zeros(n, n)
            Ms = [[[self.g2 * J[i][j] - T[i][j] for j in range(n)] for i in range(n)] for T in self.tt]
            self._cache[S] = (ri, Ms)
        return self._cache[S]

    def feasible(self, S):
        ri, Ms = self.matrices(S)
        out = []
        for t, M in enumerate(Ms):
            r = L.ldl_psd(M)
            if r[0] == 'not_psd':
                return False, (t, r[1], ri)
            out.append({'L': L.strs(r[1]), 'd': L.vstr(r[2])})
        return True, (out, ri)

    def cost(self, S):
        return sum((self.costs[i] for i in S), F(0))


def solve(model, max_nodes=100000):
    pb = Problem(model)
    best = [None, None]                  # cost, sensors
    budget = [max_nodes]

    def node(P, X):
        base = {'include': sorted(P), 'exclude': sorted(X)}
        if budget[0] <= 0:
            return {**base, 'kind': 'open'}
        budget[0] -= 1
        c = pb.cost(P)
        if best[0] is not None and c >= best[0]:
            return {**base, 'kind': 'cost'}
        ok, data = pb.feasible(P)
        if ok:
            best[0], best[1] = c, sorted(P)
            return {**base, 'kind': 'feasible', 'ldl': data[0], 'rinv': L.strs(data[1])}
        allowed = set(range(pb.k)) - X
        ok, data = pb.feasible(allowed)
        if not ok:
            t, v, ri = data
            return {**base, 'kind': 'infeasible', 'target': t, 'vector': L.vstr(v), 'rinv': L.strs(ri)}
        j = min(allowed - P)             # P infeasible but P u U feasible, so U is nonempty
        inc = node(P | {j}, X)
        exc = node(P, X | {j})
        return {**base, 'kind': 'branch', 'sensor': j, 'children': [inc, exc]}

    tree = node(frozenset(), frozenset())
    cert = {'format': C.FORMAT, 'coefficient_domain': 'Q', 'model_sha256': C.digest(model),
            'tie_policy': 'one_optimum', 'tree': tree}
    opens = []
    stack = [tree]
    while stack:
        t = stack.pop()
        if t['kind'] == 'branch':
            stack += t['children']
        elif t['kind'] == 'open':
            opens.append(pb.cost(t['include']))
    if best[0] is not None:
        cert['optimum'] = {'sensors': best[1], 'cost': str(best[0]),
                           'names': [model['sensors'][i]['name'] for i in best[1]]}
    if opens:
        cert['status'] = 'incomplete'
        cert['lower_bound'] = str(min(opens + ([best[0]] if best[0] is not None else [])))
    else:
        cert['status'] = 'optimal' if best[0] is not None else 'infeasible'
    result = C.check(cert, model)
    return cert, result


def exhaustive(model):
    """Independent oracle: every subset, exact PSD test, no pruning or tree."""
    pb = Problem(model)
    best = None
    for size in range(pb.k + 1):
        for S in itertools.combinations(range(pb.k), size):
            if pb.feasible(set(S))[0]:
                c = pb.cost(S)
                if best is None or c < best[0]:
                    best = (c, list(S))
    return best


def metric(model, observer_cert, S, panel):
    """invariant-metric-v1 receipt for a supplied S (None if some condition fails)."""
    pb = Problem(model)
    r, n = observer_cert['rank'], pb.n
    Q = L.mat(observer_cert['basis'], n, r)
    Cm = L.mat(observer_cert['target_factor'], r)
    S = L.mat(S, r, r)
    conds = []
    for a, B in sorted(observer_cert['quotient_actions'].items()):
        B = L.mat(B, r, r)
        conds.append(L.add(S, L.mul(L.mul(L.transpose(B, r), S), B, r), -1))
    conds.append(L.add(S, L.mul(L.transpose(Cm, r), Cm, r), -1))
    ri = pb.rinv(panel)
    if panel:
        HS = [pb.rows[i] for i in sorted(panel)]
        J = L.mul(L.mul(L.transpose(HS, n), ri), HS, n)
    else:
        J = L.zeros(n, n)
    conds.append(L.add(L.scale(J, pb.g2), L.mul(L.mul(L.transpose(Q, n), S), Q, n), -1))
    ldls = []
    for M in conds:
        res = L.ldl_psd(M)
        if res[0] != 'psd':
            return None
        ldls.append({'L': L.strs(res[1]), 'd': L.vstr(res[2])})
    cert = {'format': C.METRIC_FORMAT, 'model_sha256': C.digest(model), 'observer': observer_cert,
            'S': L.strs(S), 'panel': sorted(panel), 'rinv': L.strs(ri), 'ldl': ldls}
    C.check_metric(cert, model)
    return cert


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)
    s = sub.add_parser('solve')
    s.add_argument('model', type=Path)
    s.add_argument('--output', type=Path)
    s.add_argument('--max-nodes', type=int, default=100000)
    e = sub.add_parser('exhaustive')
    e.add_argument('model', type=Path)
    a = ap.parse_args()
    model = json.loads(a.model.read_text())
    try:
        if a.cmd == 'exhaustive':
            best = exhaustive(model)
            print(json.dumps({'status': 'oracle', 'optimum': best and {'cost': str(best[0]), 'sensors': best[1]}}))
            return
        cert, result = solve(model, a.max_nodes)
    except (ValueError, KeyError, TypeError) as err:
        print(json.dumps({'status': 'invalid_model', 'reason': str(err)}))
        sys.exit(2)
    if a.output:
        a.output.write_text(json.dumps(cert, indent=1) + '\n')
        result['written'] = str(a.output)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
