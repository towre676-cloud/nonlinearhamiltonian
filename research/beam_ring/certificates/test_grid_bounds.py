"""Exhaustive completion tests and adversarial certificate tests, stdlib only."""
from copy import deepcopy
from fractions import Fraction
from itertools import product
import json
import tempfile
from pathlib import Path
import unittest

try:
    from .grid_bounds import (CertificateError, certify, check_certificate, infer_labels,
                              make_manifest, objective_bounds, pareto_excludes, threshold_decision)
    from .check_grid_certificate import read_document
except ImportError:
    from grid_bounds import (CertificateError, certify, check_certificate, infer_labels,
                             make_manifest, objective_bounds, pareto_excludes, threshold_decision)
    from check_grid_certificate import read_document


def grid(width, height, designs=('A',), horizons=(16,)):
    cells = [f'{x},{y}' for y in range(height) for x in range(width)]
    adjacency = {c: [] for c in cells}
    for y in range(height):
        for x in range(width):
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                if 0 <= x+dx < width and 0 <= y+dy < height:
                    adjacency[f'{x},{y}'].append(f'{x+dx},{y+dy}')
    weights = {c: str((Fraction(0), Fraction(1, 2), Fraction(2), Fraction(3, 2),
                       Fraction(1, 3), Fraction(5, 4))[i % 6]) for i, c in enumerate(cells)}
    return make_manifest(cells, adjacency, weights, cells[0], list(designs), list(horizons),
                         {'example': 'finite test graph; no physical units assigned'})


def completions(labels):
    unknown = [cell for cell, value in labels.items() if value == -1]
    for assignment in product((0, 1), repeat=len(unknown)):
        yield {**labels, **dict(zip(unknown, assignment))}


def brute_objectives(manifest, labels):
    """Independent dense transitive closure, no producer/checker graph routine."""
    cells = manifest['cells']
    live = {c for c in cells if labels[c] == 1}
    reach = {(a, b): a in live and b in live and
             (a == b or b in manifest['adjacency'][a]) for a in cells for b in cells}
    for middle in cells:
        for left in cells:
            for right in cells:
                reach[(left, right)] |= reach[(left, middle)] and reach[(middle, right)]
    return (sum((Fraction(manifest['weights'][c]) for c in live), Fraction(0)),
            sum((Fraction(manifest['weights'][c]) for c in live
                 if reach[(manifest['origin'], c)]), Fraction(0)))


class BoundsTests(unittest.TestCase):
    def test_every_partial_labeling_of_two_by_three_grid(self):
        manifest = grid(3, 2)
        checked_completions = 0
        for states in product((-1, 0, 1), repeat=6):
            labels = dict(zip(manifest['cells'], states))
            exact = list(brute_objectives(manifest, full) for full in completions(labels))
            checked_completions += len(exact)
            bounds = objective_bounds(manifest, labels)
            for index, key in enumerate(('survival_weight', 'origin_connected_weight')):
                self.assertEqual(Fraction(bounds[key]['lower']), min(v[index] for v in exact))
                self.assertEqual(Fraction(bounds[key]['upper']), max(v[index] for v in exact))
            events = [dict(design='A', cell=c, horizon=16, label=value)
                      for c, value in labels.items() if value != -1]
            self.assertEqual(check_certificate(manifest, events, certify(manifest, events))['status'], 'passed')
        self.assertEqual(checked_completions, 4**6)

    def test_hole_and_disconnected_island_are_not_filled(self):
        manifest = grid(3, 3)
        labels = {c: 1 for c in manifest['cells']}
        labels['1,1'] = 0
        bounds = objective_bounds(manifest, labels)
        self.assertNotIn('1,1', bounds['origin_connected_weight']['known_component'])
        line = grid(4, 1)
        labels = {'0,0': 1, '1,0': 0, '2,0': 1, '3,0': 1}
        result = objective_bounds(line, labels)
        self.assertEqual(result['origin_connected_weight']['possible_component'], ['0,0'])
        self.assertGreater(Fraction(result['survival_weight']['lower']),
                           Fraction(result['origin_connected_weight']['upper']))

    def test_unknown_bridge_retains_possible_island(self):
        manifest = grid(3, 1)
        result = objective_bounds(manifest, {'0,0': 1, '1,0': -1, '2,0': 1})
        self.assertEqual(result['origin_connected_weight']['known_component'], ['0,0'])
        self.assertEqual(result['origin_connected_weight']['possible_component'], manifest['cells'])

    def test_horizon_prefix_implications_are_one_way(self):
        manifest = grid(2, 1, horizons=(4, 16, 64))
        events = [dict(design='A', cell='0,0', horizon=4, label=1),
                  dict(design='A', cell='1,0', horizon=16, label=0)]
        labels = infer_labels(manifest, events)
        self.assertEqual(labels[('A', 4)], {'0,0': 1, '1,0': -1})
        self.assertEqual(labels[('A', 16)], {'0,0': -1, '1,0': 0})
        self.assertEqual(labels[('A', 64)], {'0,0': -1, '1,0': 0})
        later = [dict(design='A', cell='0,0', horizon=64, label=1)]
        for row in infer_labels(manifest, later).values():
            self.assertEqual(row['0,0'], 1)
        check_certificate(manifest, events, certify(manifest, events))

    def test_prefix_conflict_rejected(self):
        manifest = grid(1, 1, horizons=(4, 16))
        events = [dict(design='A', cell='0,0', horizon=4, label=0),
                  dict(design='A', cell='0,0', horizon=16, label=1)]
        with self.assertRaises(CertificateError):
            certify(manifest, events)

    def test_pareto_uses_strict_lower_upper_domination(self):
        self.assertFalse(pareto_excludes(['1', '2'], ['1', '2']))
        self.assertTrue(pareto_excludes(['1', '3'], ['1', '2']))
        self.assertFalse(pareto_excludes(['0', '3'], ['1', '2']))
        # Exhaust every pair of partial two-cell tables and every completion.
        manifest = grid(2, 1, designs=('A', 'B'))
        for left in product((-1, 0, 1), repeat=2):
            for right in product((-1, 0, 1), repeat=2):
                a = dict(zip(manifest['cells'], left))
                b = dict(zip(manifest['cells'], right))
                lower = [objective_bounds(manifest, a)[key]['lower'] for key in ('survival_weight', 'origin_connected_weight')]
                upper = [objective_bounds(manifest, b)[key]['upper'] for key in ('survival_weight', 'origin_connected_weight')]
                if pareto_excludes(lower, upper):
                    for aa in completions(a):
                        for bb in completions(b):
                            av, bv = brute_objectives(manifest, aa), brute_objectives(manifest, bb)
                            self.assertTrue(all(x >= y for x, y in zip(av, bv)))
                            self.assertTrue(any(x > y for x, y in zip(av, bv)))

    def test_certificate_exclusion_checked(self):
        manifest = grid(2, 1, designs=('good', 'bad'))
        events = [dict(design=d, cell=c, horizon=16, label=int(d == 'good'))
                  for d in manifest['designs'] for c in manifest['cells']]
        certificate = certify(manifest, events)
        self.assertEqual(certificate['exclusions'], [dict(candidate='bad', dominator='good', horizon=16)])
        check_certificate(manifest, events, certificate)
        certificate['exclusions'] = []
        with self.assertRaises(CertificateError):
            check_certificate(manifest, events, certificate)

    def test_manifest_and_event_validation(self):
        original = grid(2, 1)
        invalid = []
        for mutate in [lambda m: m['weights'].__setitem__('1,0', '-1'),
                       lambda m: m['weights'].__setitem__('1,0', 0.5),
                       lambda m: m['adjacency']['1,0'].clear(),
                       lambda m: m.__setitem__('schema', 'future-unsafe'),
                       lambda m: m.__setitem__('prefix_semantics', 'reinjection'),
                       lambda m: m['horizons'].append(16),
                       lambda m: m.__setitem__('origin', 'outside'),
                       lambda m: m['physics'].__setitem__('bad', float('nan'))]:
            manifest = deepcopy(original); mutate(manifest); invalid.append(manifest)
        for manifest in invalid:
            with self.assertRaises(CertificateError):
                certify(manifest, [])
        e = dict(design='A', cell='0,0', horizon=16, label=1)
        for events in [[e, e], [{**e, 'horizon': 17}], [{**e, 'label': 2}],
                       [{**e, 'label': True}], [{**e, 'cell': 'missing'}],
                       [{**e, 'design': 'missing'}], [{**e, 'unexpected': 1}]]:
            with self.assertRaises(CertificateError):
                certify(original, events)

    def test_tampering_fails_closed(self):
        manifest = grid(2, 1)
        events = [dict(design='A', cell='0,0', horizon=16, label=1)]
        original = certify(manifest, events)
        for mutate in [lambda c: c.__setitem__('schema', 'not-a-certificate'),
                       lambda c: c.__setitem__('events_sha256', '0'*64),
                       lambda c: c.__setitem__('manifest_sha256', '0'*64),
                       lambda c: c['rows'][0]['labels'].__setitem__(1, 1),
                       lambda c: c['rows'][0]['labels'].__setitem__(0, True),
                       lambda c: c['rows'][0]['survival_weight'].__setitem__('upper', '0'),
                       lambda c: c['rows'][0]['origin_connected_weight'].__setitem__('possible_component', ['0,0']),
                       lambda c: c['rows'][0].__setitem__('horizon', 64),
                       lambda c: c['rows'][0].__setitem__('extra', 0)]:
            certificate = deepcopy(original); mutate(certificate)
            with self.assertRaises(CertificateError):
                check_certificate(manifest, events, certificate)
        changed_events = [{**events[0], 'label': 0}]
        with self.assertRaises(CertificateError):
            check_certificate(manifest, changed_events, original)
        changed_manifest = deepcopy(manifest); changed_manifest['physics']['rf'] = True
        with self.assertRaises(CertificateError):
            check_certificate(changed_manifest, events, original)

    def test_unknown_is_not_surrogate_truth(self):
        manifest = grid(2, 1)
        events = [dict(design='A', cell='0,0', horizon=16, label=-1)]
        result = certify(manifest, events)
        self.assertEqual(result['rows'][0]['labels'], [-1, -1])
        check_certificate(manifest, events, result)

    def test_threshold_boundary_and_unresolved_case(self):
        manifest = grid(3, 1)
        bounds = objective_bounds(manifest, {'0,0': 1, '1,0': -1, '2,0': 1})
        self.assertEqual(threshold_decision(bounds, '0'), 'accept')
        self.assertEqual(threshold_decision(bounds, '5/2'), 'unresolved')
        self.assertEqual(threshold_decision(bounds, '3'), 'reject')
        with self.assertRaises(CertificateError):
            threshold_decision(bounds, 0.5)

    def test_strict_json_rejects_duplicate_keys_and_nonfinite_values(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)/'invalid.json'
            for text in ['{"a": 1, "a": 2}', '{"a": NaN}', '{"a": Infinity}']:
                path.write_text(text)
                with self.assertRaises(CertificateError):
                    read_document(path)


if __name__ == '__main__':
    unittest.main()
