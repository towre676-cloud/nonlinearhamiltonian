#!/usr/bin/env python3
"""Independent checker for finite adaptive experiment certificates (adaptive-tree-v1).

Model (test-table-v1): finitely many states with target labels and deterministic tests
with positive exact costs. V(S) = 0 if the label is constant on S; otherwise
V(S) = min over tests e that strictly split S of  c_e + max_y V(S_(e,y)).

An 'optimal' certificate holds two independent halves:
  upper   a decision tree; every test node strictly splits its states into the exact
          outcome fibres, every leaf has a constant label; its worst-case cost is computed;
  lower   a table v over subsets with v(T) <= 0 for constant-label T and, for nonconstant T,
          v(T) <= c_e + max_y v(T_(e,y)) for EVERY test e splitting T (fibres in the table);
          by induction v <= V on the table.
Optimality: v(root) equals the tree's worst-case cost. With "noise": "set_valued" each
test returns, at a state, any element of a declared finite set (adversarial noise); the
feasible set after observing y is S_y = {s : y possible at s}, and a test is admissible only
if every possible observation strictly shrinks the feasible set. An 'unresolvable'
certificate is a set W with two labels on which every test has a common observation.
Probabilistic or continuous noise needs different semantics and is not covered.

Usage: check_adaptive.py CERT.json --input MODEL.json
"""
from __future__ import annotations
import argparse
import hashlib
import json
import sys
from fractions import Fraction as F
from pathlib import Path

FORMAT = 'adaptive-tree-v1'


def digest(model):
    return hashlib.sha256(json.dumps(model, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def read(model):
    states = model['states']
    if not states or len(set(states)) != len(states) or len(states) > 12:
        raise ValueError('need 1..12 distinct states')
    labels = model['labels']
    if set(labels) != set(states):
        raise ValueError('every state needs a label')
    tests = []
    for t in model['tests']:
        c = t['cost']
        if type(c) not in (int, str) or F(c) <= 0:
            raise ValueError('test costs must be positive exact numbers')
        if set(t['outcomes']) != set(states):
            raise ValueError('each test must give an outcome for every state')
        outc = {}
        for st, v in t['outcomes'].items():
            if model.get('noise') == 'set_valued':
                # adversarial noise: the observation is any element of the declared set
                if not isinstance(v, list) or not v:
                    raise ValueError('set-valued outcomes must be nonempty lists')
                outc[st] = sorted({str(x) for x in v})
            else:
                outc[st] = [str(v)]
        tests.append((F(c), outc))
    return states, labels, tests


def fibres(T, outcomes):
    """y -> {s in T : y is a possible observation at s}; overlapping under set-valued noise."""
    out = {}
    for s in sorted(T):
        for y in outcomes[s]:
            out.setdefault(y, []).append(s)
    return out


def useful(T, fib):
    """Every possible observation must strictly shrink the feasible set."""
    return all(len(f) < len(T) for f in fib.values())


def key(T):
    return '|'.join(sorted(T))


def check(cert, model):
    if cert.get('format') != FORMAT or cert.get('model_sha256') != digest(model):
        raise ValueError('not an adaptive-tree-v1 certificate for this model')
    states, labels, tests = read(model)
    def unresolvable(Wset, within):
        # A set W with two labels on which every test has an observation common to all of W:
        # answering it forever keeps W feasible under every policy, so V(U) is infinite for U >= W.
        if not set(Wset) <= set(within) or len({labels[s] for s in Wset}) < 2:
            raise ValueError('witness set must contain two different labels inside its set')
        for _, o in tests:
            if not set.intersection(*(set(o[s]) for s in Wset)):
                raise ValueError('some test has no observation common to the witness set')
    if cert['status'] == 'unresolvable':
        unresolvable(cert['witness_set'], states)
        return {'status': 'passed', 'claim': 'unresolvable', 'witness_set': sorted(cert['witness_set'])}
    if cert['status'] != 'optimal':
        raise ValueError('unknown status')

    def walk(node, T):
        if sorted(node['states']) != sorted(T):
            raise ValueError('tree node states are wrong')
        if node['kind'] == 'leaf':
            if {labels[s] for s in T} != {node['label']}:
                raise ValueError('leaf label is not constant on its states')
            return F(0)
        c, outc = tests[node['test']]
        fib = fibres(T, outc)
        if not useful(T, fib) or set(fib) != set(node['children']):
            raise ValueError('test node must strictly shrink the feasible set for every observation')
        return c + max(walk(node['children'][y], fib[y]) for y in fib)
    upper = walk(cert['tree'], states)
    INF = float('inf')
    table = {k: (INF if v == 'inf' else F(v)) for k, v in cert['lower_bounds'].items()}
    for k, v in table.items():
        T = k.split('|')
        if not set(T) <= set(states):
            raise ValueError('unknown state in table')
        if v == INF:
            unresolvable(cert['infinite_witnesses'][k], T)
            continue
        if len({labels[s] for s in T}) == 1:
            if v > 0:
                raise ValueError('constant-label set must have bound <= 0')
            continue
        split = False
        for c, outc in tests:
            fib = fibres(T, outc)
            if not useful(T, fib):
                continue
            split = True
            vals = []
            for f in fib.values():
                if key(f) not in table:
                    raise ValueError('table is not closed under splitting fibres')
                vals.append(table[key(f)])
            if v > c + max(vals):
                raise ValueError('Bellman lower-bound inequality fails')
        if not split:
            raise ValueError('nonconstant set with no splitting test cannot carry a finite bound')
    if table.get(key(states)) != upper or F(cert['value']) != upper:
        raise ValueError('lower bound at the root does not meet the tree cost')
    return {'status': 'passed', 'claim': 'optimal', 'worst_case_cost': str(upper), 'table_entries': len(table),
            'scope': 'exact minimum worst-case cost over all adaptive test policies; outcomes are deterministic '
                     'or adversarially set-valued as declared; no probabilistic noise model'}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('certificate', type=Path)
    ap.add_argument('--input', type=Path, required=True)
    a = ap.parse_args()
    try:
        print(json.dumps(check(json.loads(a.certificate.read_text()), json.loads(a.input.read_text())), indent=2))
    except (ValueError, KeyError, TypeError, IndexError) as e:
        print(json.dumps({'status': 'rejected', 'reason': str(e)}))
        sys.exit(2)


if __name__ == '__main__':
    main()
