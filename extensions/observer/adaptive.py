#!/usr/bin/env python3
"""Exact Bellman solver for finite deterministic test tables (O3 producer, adaptive-tree-v1).

Memoized recursion over the subsets reachable by test fibres; emits the optimal tree
and the full table of Bellman values (which is exactly the lower-bound half of the
certificate). Replayed by check_adaptive.py before it is returned.

Usage: adaptive.py MODEL.json [--output CERT.json]
"""
from __future__ import annotations
import argparse
import json
import sys
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import check_adaptive as C  # noqa: E402


def solve(model):
    states, labels, tests = C.read(model)
    cert = {'format': C.FORMAT, 'model_sha256': C.digest(model)}
    INF = None

    @lru_cache(None)
    def V(T):
        if len({labels[s] for s in T}) == 1:
            return F(0), None
        best = None
        for e, (c, o) in enumerate(tests):
            fib = C.fibres(T, o)
            if not C.useful(T, fib):
                continue
            vals = [V(tuple(f))[0] for f in fib.values()]
            if any(v is INF for v in vals):
                continue
            val = c + max(vals)
            if best is None or val < best[0]:
                best = (val, e)
        return best if best else (INF, None)

    def witness(T):
        """A reachable set without admissible tests whose labels differ."""
        if V(T)[0] is not INF:
            return None
        for c, o in tests:
            fib = C.fibres(T, o)
            if C.useful(T, fib):
                for f in fib.values():
                    w = witness(tuple(f))
                    if w:
                        return w
        return list(T)
    root0 = tuple(sorted(states))
    if V(root0)[0] is INF:
        cert.update(status='unresolvable', witness_set=witness(root0))
        cert['result'] = C.check(cert, model)
        return cert

    def tree(T):
        val, e = V(T)
        if e is None:
            return {'states': list(T), 'kind': 'leaf', 'label': labels[T[0]]}
        fib = C.fibres(T, tests[e][1])
        return {'states': list(T), 'kind': 'test', 'test': e, 'name': model['tests'][e].get('name'),
                'children': {y: tree(tuple(f)) for y, f in fib.items()}}
    root = tuple(sorted(states))
    t = tree(root)
    table, witnesses = {}, {}
    stack = [root]
    while stack:                       # close the table under all splitting fibres
        T = stack.pop()
        k = C.key(T)
        if k in table:
            continue
        if V(T)[0] is INF:
            table[k] = 'inf'
            witnesses[k] = witness(T)
            continue
        table[k] = str(V(T)[0])
        if V(T)[1] is not None:
            for _, o in tests:
                fib = C.fibres(T, o)
                if C.useful(T, fib):
                    stack += [tuple(f) for f in fib.values()]
    cert.update(status='optimal', value=str(V(root)[0]), tree=t, lower_bounds=table, infinite_witnesses=witnesses)
    cert['result'] = C.check(cert, model)
    return cert


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('model', type=Path)
    ap.add_argument('--output', type=Path)
    a = ap.parse_args()
    try:
        cert = solve(json.loads(a.model.read_text()))
    except (ValueError, KeyError, TypeError) as e:
        print(json.dumps({'status': 'invalid_model', 'reason': str(e)}))
        sys.exit(2)
    if a.output:
        a.output.write_text(json.dumps(cert, indent=1) + '\n')
    print(json.dumps(cert['result'], indent=2))


if __name__ == '__main__':
    main()
