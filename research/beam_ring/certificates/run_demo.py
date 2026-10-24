"""Build/check a synthetic finite-grid certificate and run its exhaustive tests."""
from pathlib import Path
import argparse
import hashlib
import io
import json
import unittest

try:
    from .grid_bounds import make_manifest, certify, check_certificate
except ImportError:
    from grid_bounds import make_manifest, certify, check_certificate


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=Path(__file__).with_name('results'))
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    stream = io.StringIO()
    suite = unittest.defaultTestLoader.discover(str(here), pattern='test_*.py')
    tested = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
    if not tested.wasSuccessful():
        raise RuntimeError(stream.getvalue())
    cells = [f'{x},{y}' for y in range(2) for x in range(3)]
    adjacency = {cell: [] for cell in cells}
    for y in range(2):
        for x in range(3):
            for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                if 0 <= x+dx < 3 and 0 <= y+dy < 2:
                    adjacency[f'{x},{y}'].append(f'{x+dx},{y+dy}')
    manifest = make_manifest(cells, adjacency, {c: '1' for c in cells}, '0,0',
        ['A', 'B'], [16, 64], {'provenance': 'synthetic finite-grid example only',
                               'no_physical_oracle_run': True})
    events = [dict(design='A', cell=c, horizon=64, label=1, source='synthetic-demo-v1')
              for c in cells if c != '2,1']
    events += [dict(design='B', cell=c, horizon=16, label=label, source='synthetic-demo-v1')
               for c, label in [('0,0', 1), ('1,0', 0), ('0,1', 0), ('2,1', 1)]]
    certificate = certify(manifest, events)
    check = check_certificate(manifest, events, certificate)
    args.output.mkdir(parents=True, exist_ok=True)
    for name, data in [('manifest.json', manifest), ('events.json', events),
                       ('certificate.json', certificate)]:
        (args.output/name).write_text(json.dumps(data, indent=2)+'\n')
    receipt = {'status': 'passed', 'tests_run': tested.testsRun,
               'exhaustive_partial_labelings': 3**6, 'exhaustive_completion_instances': 4**6,
               'synthetic_certificate_check': check,
               'source_sha256': {path.name: hashlib.sha256(path.read_bytes()).hexdigest()
                   for path in [here/'grid_bounds.py', here/'check_grid_certificate.py',
                                here/'test_grid_bounds.py', here/'run_demo.py']},
               'scope': 'Exact finite-table/graph semantics and supplied event consistency; no physical tracking or tenfold result.'}
    (args.output/'receipt.json').write_text(json.dumps(receipt, indent=2)+'\n')
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
