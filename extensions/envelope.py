#!/usr/bin/env python3
"""Typed claim envelopes (machinery-envelope-v1) and dispatch to independent checkers.

An envelope binds one certificate to: its witness kind, coefficient domain, the
hashes of the exact model and payload, declared hypotheses and scope, and source
identifiers in the retained atlas. The checker refuses an envelope whose witness
kind and payload schema disagree, so witness types cannot be exchanged merely
because each consists of matrices or kernels.

Commands:
  envelope.py check ENVELOPE.json        replay one envelope with its checker
  envelope.py kinds                      list registered witness kinds
"""
from __future__ import annotations
import argparse
import gzip
import hashlib
import importlib.util
import json
import sys
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SCHEMA = 'machinery-envelope-v1'


def sha(obj):
    raw = json.dumps(obj, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()
    return hashlib.sha256(raw).hexdigest()


def _load(rel, name):
    spec = importlib.util.spec_from_file_location(name, HERE / rel)
    mod = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str((HERE / rel).parent))
    try:
        spec.loader.exec_module(mod)
    finally:
        sys.path.pop(0)
    return mod


def _observer(model, payload):
    return _load('observer/check_observer.py', 'mx_check_observer').check(payload, model)


def _weyl(model, payload):
    m = _load('hamiltonian/weyl_receipts.py', 'mx_weyl_receipts')
    if model is not None and model != payload.get('hamiltonian'):
        raise ValueError('envelope model is not the receipt Hamiltonian')
    return m.verify_certificate(payload)


def _contraction(model, payload):
    return _load('structure/check_contraction.py', 'mx_check_contraction').verify(model, payload)


def _weyl_kernel(model, payload):
    if model is not None and model != payload['receipt'].get('hamiltonian'):
        raise ValueError('envelope model is not the receipt Hamiltonian')
    return _load('hamiltonian/check_weyl_kernel.py', 'mx_check_weyl_kernel').check(payload)


def _noise_panel(model, payload):
    return _load('observer/check_panel.py', 'mx_check_panel').check(payload, model)


def _pell(model, payload):
    return _load('arithmetic/check_pell.py', 'mx_check_pell').check(payload, model)


def _adaptive(model, payload):
    return _load('observer/check_adaptive.py', 'mx_check_adaptive').check(payload, model)


def _obstruction_answer(model, payload):
    return _load('structure/obstruction.py', 'mx_obstruction').check_answer(model, payload)


def _dgla(model, payload):
    return _load('structure/check_dgla.py', 'mx_check_dgla').check(payload, model)


# witness kind -> (payload schema field, required value, checker)
KINDS = {
    'observer-closure': ('format', 'observer-closure-v2', _observer),
    'weyl-invariant-kernel': ('schema', 'weyl-invariant-kernel-v1', _weyl),
    'weyl-polynomial-kernel': ('format', 'weyl-kernel-v1', _weyl_kernel),
    'rational-contraction': ('schema', 'rational-contraction-v1', _contraction),
    'noise-panel-selection': ('format', 'noise-panel-v1', _noise_panel),
    'pell-orbit-reduction': ('format', 'pell-orbits-v1', _pell),
    'dgla-lifting': ('format', 'dgla-lift-v1', _dgla),
    'adaptive-experiment': ('format', 'adaptive-tree-v1', _adaptive),
    'rational-obstruction-answer': ('schema', 'rational-obstruction-answer-v1', _obstruction_answer),
}

REQUIRED = ('schema', 'witness_kind', 'coefficient_domain', 'model', 'model_sha256', 'payload',
            'payload_sha256', 'hypotheses', 'scope', 'source_ids', 'producer')


@lru_cache(None)
def atlas_ids():
    a = json.loads((ROOT / 'compendium/atlas/data/atlas.json').read_text(encoding='utf-8'))
    return frozenset([r['uid'] for r in a['corpus'] + a['supplementary']] + [f['id'] for f in a['families']])


def make(kind, model, payload, hypotheses, scope, source_ids, producer, verify=True):
    env = {'schema': SCHEMA, 'witness_kind': kind, 'coefficient_domain': 'Q', 'model': model,
           'model_sha256': sha(model), 'payload': payload, 'payload_sha256': sha(payload),
           'hypotheses': list(hypotheses), 'scope': scope, 'source_ids': list(source_ids), 'producer': producer}
    if verify:
        check(env)
    return env


def check(env):
    missing = [k for k in REQUIRED if k not in env]
    if missing or env['schema'] != SCHEMA:
        raise ValueError('not a machinery-envelope-v1 object; missing ' + ', '.join(missing))
    if env['coefficient_domain'] != 'Q':
        raise ValueError('coefficient domain ' + repr(env['coefficient_domain']) + ' has no registered checker')
    kind = env['witness_kind']
    if kind not in KINDS:
        raise ValueError('unknown witness kind ' + repr(kind))
    field, value, checker = KINDS[kind]
    payload = env['payload']
    if not isinstance(payload, dict) or payload.get(field) != value:
        raise ValueError(f'payload is not a {kind} witness (expected {field}={value})')
    for f in ('field', 'coefficient_domain'):
        if f in payload and payload[f] != 'Q':
            raise ValueError('payload coefficient domain disagrees with envelope')
    if sha(env['model']) != env['model_sha256'] or sha(payload) != env['payload_sha256']:
        raise ValueError('model or payload hash mismatch')
    if not env['hypotheses'] or not isinstance(env['scope'], str) or not env['scope']:
        raise ValueError('hypotheses and scope must be declared')
    unknown = [s for s in env['source_ids'] if s not in atlas_ids()]
    if not env['source_ids'] or unknown:
        raise ValueError('source ids must be nonempty atlas uids/family ids; unknown: ' + ', '.join(unknown))
    result = checker(env['model'], payload)
    if not isinstance(result, dict) or result.get('status') != 'passed':
        raise ValueError('checker did not pass')
    return {'status': 'passed', 'witness_kind': kind, 'checker_result': result,
            'scope': env['scope'], 'hypotheses': env['hypotheses'], 'source_ids': env['source_ids']}


def load(path):
    path = Path(path)
    raw = gzip.decompress(path.read_bytes()) if path.suffix == '.gz' else path.read_bytes()
    return json.loads(raw.decode('utf-8'))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)
    c = sub.add_parser('check')
    c.add_argument('envelope', type=Path)
    sub.add_parser('kinds')
    a = ap.parse_args()
    if a.cmd == 'kinds':
        print(json.dumps({k: f'{v[0]}={v[1]}' for k, v in KINDS.items()}, indent=2))
        return
    try:
        print(json.dumps(check(load(a.envelope)), indent=2, ensure_ascii=False))
    except (ValueError, KeyError, TypeError, IndexError, ZeroDivisionError, FileNotFoundError) as e:
        print(json.dumps({'status': 'rejected', 'reason': str(e)}))
        sys.exit(2)


if __name__ == '__main__':
    main()
