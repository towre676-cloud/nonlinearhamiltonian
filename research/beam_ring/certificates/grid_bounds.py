"""Exact bounds for a declared finite survival table, not continuous stability.

No simulator or surrogate is trusted here. Inputs are a source-bound manifest
and explicit prefix-survival observations. Arithmetic uses Fraction only.
"""
from collections import deque
from fractions import Fraction
import hashlib
import json

MANIFEST_SCHEMA = 'finite-grid-survival-manifest-v1'
CERTIFICATE_SCHEMA = 'finite-grid-survival-certificate-v1'
PREFIX_SEMANTICS = 'deterministic-prefix-no-reinjection-v1'
OBJECTIVES = ('survival_weight', 'origin_connected_weight')


class CertificateError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise CertificateError(message)


def canonical_json(value):
    """Disallow NaN/infinity; hash exactly the JSON document, including metadata."""
    try:
        return json.dumps(value, sort_keys=True, separators=(',', ':'),
                          ensure_ascii=False, allow_nan=False).encode('utf-8')
    except (TypeError, ValueError) as exc:
        raise CertificateError('Input is not finite canonical JSON') from exc


def digest(value):
    return hashlib.sha256(canonical_json(value)).hexdigest()


def rational(value):
    """Accept integers/rational strings, never silently convert binary floats."""
    require(type(value) in (int, str, Fraction), 'Weight/bound must be an exact rational')
    try:
        result = Fraction(value)
    except (ValueError, ZeroDivisionError) as exc:
        raise CertificateError('Invalid rational') from exc
    return result


def _ids(values, name):
    require(type(values) is list and values, name+' must be a nonempty list')
    require(all(type(v) is str and v for v in values), name+' must contain nonempty strings')
    require(len(set(values)) == len(values), 'Duplicate '+name)


def validate_manifest(manifest):
    require(type(manifest) is dict, 'Manifest must be an object')
    required = {'schema', 'cells', 'adjacency', 'weights', 'origin', 'designs',
                'horizons', 'prefix_semantics', 'physics'}
    require(set(manifest) == required, 'Manifest fields/schema mismatch')
    require(manifest['schema'] == MANIFEST_SCHEMA, 'Unsupported manifest schema')
    require(manifest['prefix_semantics'] == PREFIX_SEMANTICS, 'Unsupported horizon semantics')
    for name in ('cells', 'designs'):
        _ids(manifest[name], name)
    cells = manifest['cells']
    require(manifest['origin'] in cells, 'Origin is absent from grid')
    require(type(manifest['adjacency']) is dict and set(manifest['adjacency']) == set(cells),
            'Adjacency cells mismatch')
    require(type(manifest['weights']) is dict and set(manifest['weights']) == set(cells),
            'Weight cells mismatch')
    for cell in cells:
        neighbors = manifest['adjacency'][cell]
        require(type(neighbors) is list, 'Neighbors must be a list')
        require(all(type(n) is str and n in cells and n != cell for n in neighbors),
                'Invalid adjacency endpoint/self-edge')
        require(len(neighbors) == len(set(neighbors)), 'Duplicate neighbor')
        for neighbor in neighbors:
            require(cell in manifest['adjacency'][neighbor], 'Adjacency must be undirected')
        require(rational(manifest['weights'][cell]) >= 0, 'Negative weight')
    horizons = manifest['horizons']
    require(type(horizons) is list and horizons, 'Horizons must be a nonempty list')
    require(all(type(h) is int and h > 0 for h in horizons), 'Horizons must be positive integers')
    require(horizons == sorted(set(horizons)), 'Horizons must be distinct and increasing')
    require(type(manifest['physics']) is dict, 'Physics must be an object')
    canonical_json(manifest)
    return manifest


def make_manifest(cells, adjacency, weights, origin, designs, horizons, physics=None):
    cells = list(cells)
    require(type(adjacency) is dict and set(adjacency) == set(cells), 'Adjacency cells mismatch')
    require(type(weights) is dict and set(weights) == set(cells), 'Weight cells mismatch')
    manifest = {'schema': MANIFEST_SCHEMA, 'cells': list(cells),
                'adjacency': {c: list(adjacency[c]) for c in cells},
                'weights': {c: str(rational(weights[c])) for c in cells},
                'origin': origin, 'designs': list(designs), 'horizons': list(horizons),
                'prefix_semantics': PREFIX_SEMANTICS, 'physics': {} if physics is None else physics}
    return validate_manifest(manifest)


def validate_events(manifest, events):
    validate_manifest(manifest)
    require(type(events) is list, 'Events must be a list')
    seen = set()
    for event in events:
        require(type(event) is dict, 'Event must be an object')
        require(set(event) in ({'design', 'cell', 'horizon', 'label'},
                               {'design', 'cell', 'horizon', 'label', 'source'}),
                'Event fields mismatch')
        require(event['design'] in manifest['designs'], 'Unknown design')
        require(event['cell'] in manifest['cells'], 'Unknown cell')
        require(type(event['horizon']) is int and event['horizon'] in manifest['horizons'],
                'Undeclared horizon')
        require(type(event['label']) is int and event['label'] in (-1, 0, 1), 'Invalid label')
        if 'source' in event:
            require(type(event['source']) is str and event['source'], 'Invalid source identity')
        key = (event['design'], event['cell'], event['horizon'])
        require(key not in seen, 'Duplicate observation key (even identical duplicates are rejected)')
        seen.add(key)
    canonical_json(events)
    return events


def infer_labels(manifest, events):
    validate_events(manifest, events)
    table = {(d, h): {c: -1 for c in manifest['cells']}
             for d in manifest['designs'] for h in manifest['horizons']}
    for event in events:
        if event['label'] == -1:
            continue
        for horizon in manifest['horizons']:
            implied = ((event['label'] == 0 and horizon >= event['horizon']) or
                       (event['label'] == 1 and horizon <= event['horizon']))
            if implied:
                row = table[(event['design'], horizon)]
                current = row[event['cell']]
                require(current in (-1, event['label']), 'Conflicting prefix-survival observations')
                row[event['cell']] = event['label']
    return table


def _component(manifest, admissible):
    root = manifest['origin']
    if root not in admissible:
        return set()
    reached = {root}
    queue = deque([root])
    while queue:
        for neighbor in manifest['adjacency'][queue.popleft()]:
            if neighbor in admissible and neighbor not in reached:
                reached.add(neighbor)
                queue.append(neighbor)
    return reached


def objective_bounds(manifest, labels):
    validate_manifest(manifest)
    require(type(labels) is dict and set(labels) == set(manifest['cells']), 'Label cells mismatch')
    require(all(type(v) is int and v in (-1, 0, 1) for v in labels.values()), 'Invalid table label')
    weights = {c: rational(w) for c, w in manifest['weights'].items()}
    definite = {c for c, v in labels.items() if v == 1}
    possible = {c for c, v in labels.items() if v != 0}
    lower_component = _component(manifest, definite)
    upper_component = _component(manifest, possible)
    def total(cells):
        return str(sum((weights[c] for c in cells), Fraction(0)))
    return {'survival_weight': {'lower': total(definite), 'upper': total(possible)},
            'origin_connected_weight': {'lower': total(lower_component), 'upper': total(upper_component),
                'known_component': [c for c in manifest['cells'] if c in lower_component],
                'possible_component': [c for c in manifest['cells'] if c in upper_component]}}


def pareto_excludes(dominator_lower, candidate_upper):
    require(len(dominator_lower) == len(candidate_upper) and len(dominator_lower) > 0,
            'Objective dimensions mismatch')
    lower = [rational(x) for x in dominator_lower]
    upper = [rational(x) for x in candidate_upper]
    return all(a >= b for a, b in zip(lower, upper)) and any(a > b for a, b in zip(lower, upper))


def threshold_decision(bounds, threshold, objective='origin_connected_weight'):
    """Decide a declared finite-grid score>=threshold, retaining unresolved cases."""
    require(objective in OBJECTIVES, 'Unknown objective')
    require(type(bounds) is dict and objective in bounds, 'Missing objective bounds')
    lower = rational(bounds[objective]['lower'])
    upper = rational(bounds[objective]['upper'])
    target = rational(threshold)
    require(lower <= upper, 'Inverted bounds')
    if lower >= target:
        return 'accept'
    if upper < target:
        return 'reject'
    return 'unresolved'


def certify(manifest, events):
    table = infer_labels(manifest, events)
    rows = []
    lookup = {}
    for design in manifest['designs']:
        for horizon in manifest['horizons']:
            labels = table[(design, horizon)]
            bounds = objective_bounds(manifest, labels)
            row = {'design': design, 'horizon': horizon,
                   'labels': [labels[c] for c in manifest['cells']], **bounds}
            rows.append(row)
            lookup[(design, horizon)] = row
    exclusions = []
    for horizon in manifest['horizons']:
        for candidate in manifest['designs']:
            for dominator in manifest['designs']:
                if dominator == candidate:
                    continue
                lower = [lookup[(dominator, horizon)][o]['lower'] for o in OBJECTIVES]
                upper = [lookup[(candidate, horizon)][o]['upper'] for o in OBJECTIVES]
                if pareto_excludes(lower, upper):
                    exclusions.append({'candidate': candidate, 'dominator': dominator, 'horizon': horizon})
    return {'schema': CERTIFICATE_SCHEMA, 'manifest_sha256': digest(manifest),
            'events_sha256': digest(events), 'objectives': list(OBJECTIVES),
            'rows': rows, 'exclusions': exclusions}


def check_certificate(manifest, events, certificate):
    # Separate union-find checker, with independent horizon reconstruction.
    try:
        from .check_grid_certificate import check_certificate as checker
    except ImportError:
        from check_grid_certificate import check_certificate as checker
    return checker(manifest, events, certificate)
