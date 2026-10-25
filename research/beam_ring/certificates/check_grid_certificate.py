"""Independent union-find / integer-sum checker for finite-grid certificates."""
from fractions import Fraction
from math import lcm
import argparse
import json
from pathlib import Path

try:
    from .grid_bounds import (CERTIFICATE_SCHEMA, OBJECTIVES, CertificateError,
                              digest, require, validate_events, validate_manifest)
except ImportError:
    from grid_bounds import (CERTIFICATE_SCHEMA, OBJECTIVES, CertificateError,
                             digest, require, validate_events, validate_manifest)


def _components(cells, adjacency, included, origin):
    """Independent algorithm: union every admissible edge, then inspect root."""
    representatives = {cell: cell for cell in cells if cell in included}
    def find(cell):
        while representatives[cell] != cell:
            representatives[cell] = representatives[representatives[cell]]
            cell = representatives[cell]
        return cell
    for cell in representatives:
        for neighbor in adjacency[cell]:
            if neighbor in representatives:
                left, right = find(cell), find(neighbor)
                if left != right:
                    representatives[right] = left
    if origin not in representatives:
        return []
    root = find(origin)
    return [cell for cell in cells if cell in representatives and find(cell) == root]


def check_certificate(manifest, events, certificate):
    validate_manifest(manifest)
    validate_events(manifest, events)
    require(type(certificate) is dict, 'Certificate must be an object')
    fields = {'schema', 'manifest_sha256', 'events_sha256', 'objectives', 'rows', 'exclusions'}
    require(set(certificate) == fields, 'Certificate fields mismatch')
    require(certificate['schema'] == CERTIFICATE_SCHEMA, 'Unsupported certificate schema')
    require(certificate['manifest_sha256'] == digest(manifest), 'Manifest hash mismatch')
    require(certificate['events_sha256'] == digest(events), 'Events hash mismatch')
    require(certificate['objectives'] == list(OBJECTIVES), 'Objective declaration mismatch')
    rows = certificate['rows']
    require(type(rows) is list, 'Rows must be a list')
    require(len(rows) == len(manifest['designs'])*len(manifest['horizons']), 'Row count mismatch')
    weights = {cell: Fraction(manifest['weights'][cell]) for cell in manifest['cells']}
    denominator = lcm(*(w.denominator for w in weights.values()))
    integer_weights = {cell: w.numerator*(denominator//w.denominator) for cell, w in weights.items()}
    def total(cells):
        return str(Fraction(sum(integer_weights[c] for c in cells), denominator))
    reconstructed = {}
    index = 0
    unresolved = 0
    for design in manifest['designs']:
        for horizon in manifest['horizons']:
            labels = []
            for cell in manifest['cells']:
                relevant = [e for e in events if e['design'] == design and e['cell'] == cell]
                lost = any(e['label'] == 0 and e['horizon'] <= horizon for e in relevant)
                survived = any(e['label'] == 1 and e['horizon'] >= horizon for e in relevant)
                require(not (lost and survived), 'Conflicting prefix-survival observations')
                labels.append(0 if lost else 1 if survived else -1)
            unresolved += labels.count(-1)
            definite = {c for c, value in zip(manifest['cells'], labels) if value == 1}
            possible = {c for c, value in zip(manifest['cells'], labels) if value != 0}
            known_component = _components(manifest['cells'], manifest['adjacency'], definite, manifest['origin'])
            possible_component = _components(manifest['cells'], manifest['adjacency'], possible, manifest['origin'])
            expected = {'design': design, 'horizon': horizon, 'labels': labels,
                'survival_weight': {'lower': total(definite), 'upper': total(possible)},
                'origin_connected_weight': {'lower': total(known_component), 'upper': total(possible_component),
                    'known_component': known_component, 'possible_component': possible_component}}
            # Exact JSON equality also rejects extra/missing fields, noncanonical rationals,
            # invented labels/components, changed horizon and row reordering.
            require(type(rows[index]) is dict and rows[index] == expected, 'Incorrect bound/label/component row')
            # Python considers True==1; explicitly reject that non-JSON-label interpretation.
            require(all(type(v) is int for v in rows[index]['labels']), 'Noninteger certificate label')
            require(type(rows[index]['horizon']) is int, 'Noninteger certificate horizon')
            reconstructed[(design, horizon)] = expected
            index += 1
    expected_exclusions = []
    for horizon in manifest['horizons']:
        for candidate in manifest['designs']:
            for dominator in manifest['designs']:
                if candidate == dominator:
                    continue
                lower = [Fraction(reconstructed[(dominator, horizon)][key]['lower']) for key in OBJECTIVES]
                upper = [Fraction(reconstructed[(candidate, horizon)][key]['upper']) for key in OBJECTIVES]
                if min(a-b for a, b in zip(lower, upper)) >= 0 and max(a-b for a, b in zip(lower, upper)) > 0:
                    expected_exclusions.append({'candidate': candidate, 'dominator': dominator, 'horizon': horizon})
    require(type(certificate['exclusions']) is list and certificate['exclusions'] == expected_exclusions,
            'Incorrect or incomplete strict Pareto exclusions')
    require(all(type(e['horizon']) is int for e in certificate['exclusions']), 'Noninteger exclusion horizon')
    return {'status': 'passed', 'manifest_sha256': digest(manifest), 'events_sha256': digest(events),
            'rows_checked': len(rows), 'strict_pareto_exclusions': len(expected_exclusions),
            'unresolved_table_entries': unresolved,
            'scope': 'Declared finite graph/weights and supplied deterministic-prefix observations only; no simulator truth or continuous stability proof.'}


def _strict_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'Duplicate JSON object key')
        result[key] = value
    return result


def read_document(path):
    def reject_constant(value):
        raise CertificateError('Nonfinite JSON constant '+value)
    return json.loads(Path(path).read_text(), object_pairs_hook=_strict_object,
                      parse_constant=reject_constant)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', type=Path, required=True)
    parser.add_argument('--events', type=Path, required=True)
    parser.add_argument('--certificate', type=Path, required=True)
    args = parser.parse_args()
    result = check_certificate(read_document(args.manifest), read_document(args.events),
                               read_document(args.certificate))
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
