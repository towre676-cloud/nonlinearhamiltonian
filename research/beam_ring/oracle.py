"""Source-bound finite-horizon PyAT oracle. Surrogates cannot supply truth labels."""
from pathlib import Path
import hashlib
import importlib.metadata
import json
import math
import os
import sys
import time

HERE = Path(__file__).resolve().parent
LATTICE = HERE.parent / 'beam_literature/dataset_inspection/at_hmba.mat'
LATTICE_SHA256 = '8547502b0a4612a0e145fa6033e5ba98bb13567035fed43cadef760dae385c7b'
FAMILIES = ['SD1A', 'SF2A', 'SD1B', 'SD1D', 'SF2E', 'SD1E']


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'),
                                     allow_nan=False).encode()).hexdigest()


def load_runtime(runtime=None):
    if runtime:
        sys.path.insert(0, str(Path(runtime).resolve()))
    for key in ['OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS']:
        os.environ[key] = '1'
    import at
    import numpy as np
    if at.__version__ != '0.9.0':
        raise ValueError('benchmark pins accelerator-toolbox==0.9.0')
    return at, np


def base_ring(runtime=None):
    at, np = load_runtime(runtime)
    if hashlib.sha256(LATTICE.read_bytes()).hexdigest() != LATTICE_SHA256:
        raise ValueError('lattice checksum mismatch')
    cell = at.Lattice.load(LATTICE)
    ring = (cell * int(cell.periodicity)).disable_6d(copy=True)
    if ring.periodicity != 1 or len(ring) != 3872:
        raise ValueError('one turn must cover the complete 32-cell ring')
    return ring


def set_strengths(ring, strengths):
    if len(strengths) != len(FAMILIES) or not all(math.isfinite(float(x)) for x in strengths):
        raise ValueError('six finite multipole coefficients required')
    by_family = dict(zip(FAMILIES, strengths))
    found = set()
    for element in ring:
        if element.FamName in by_family:
            values = element.PolynomB.copy()
            values[2] = by_family[element.FamName]
            element.PolynomB = values
            found.add(element.FamName)
    if found != set(FAMILIES):
        raise ValueError('nonlinear family mismatch')


def validated_protocol(protocol):
    """Detach caller state and reject unsupported or inconsistent physics metadata."""
    value=json.loads(json.dumps(protocol,allow_nan=False))
    if value.get('schema')!='public-ring-pilot-v1' or value.get('lattice_sha256')!=LATTICE_SHA256:
        raise ValueError('unsupported protocol or lattice identity')
    if value.get('full_ring_elements')!=3872 or value.get('full_ring_periodicity')!=1:
        raise ValueError('full ring convention mismatch')
    physics=value['physics']
    if physics['energy_eV']!=6e9 or any(physics[k]is not False for k in
            ['rf','radiation','space_charge','magnet_errors','mechanical_apertures_added']):
        raise ValueError('unsupported physics mode')
    if physics['loss_rule']!='PyAT native element/aperture/numerical loss checks':
        raise ValueError('unsupported loss rule')
    definition=value['control_definition']
    if definition['families']!=FAMILIES:
        raise ValueError('family order mismatch')
    baseline=definition['baseline'];basis=definition['nullspace_basis'];scale=definition['scale']
    if len(baseline)!=6 or len(basis)!=6 or any(len(row)!=4 for row in basis):
        raise ValueError('control map dimensions')
    if not all(type(x)in(int,float)and math.isfinite(x)
               for x in baseline+[scale]+[x for row in basis for x in row])or scale<=0:
        raise ValueError('finite control map required')
    ids=set()
    for design in value['designs']:
        if not isinstance(design['id'],str)or not design['id']or design['id']in ids:
            raise ValueError('unique design IDs required')
        ids.add(design['id'])
        if len(design['strengths'])!=6 or len(design['controls'])!=4:
            raise ValueError('invalid design dimensions')
        if not all(type(x)in(int,float)and math.isfinite(x)for x in design['strengths']+design['controls']):
            raise ValueError('finite design coefficients required')
        expected=[baseline[i]+scale*sum(basis[i][j]*design['controls'][j]for j in range(4))for i in range(6)]
        if any(abs(a-b)>1e-10 for a,b in zip(expected,design['strengths'])):
            raise ValueError('declared control/physical coefficient mismatch')
    if not ids:raise ValueError('nonempty design table required')
    for stage,spec in value['stages'].items():
        if stage not in ('learning','validation')or type(spec['turns'])is not int or spec['turns']<1:
            raise ValueError('unsupported stage/horizon')
        if len(spec['launch_sets'])!=2:raise ValueError('two launch objectives required')
        for grid in spec['launch_sets']:
            n=len(grid['coordinates'])
            if not n or any(len(row)!=6 or not all(type(x)in(int,float)and math.isfinite(x)
                                                  for x in row)for row in grid['coordinates']):
                raise ValueError('finite six-coordinate launches required')
            if len(grid['weights'])!=n or any(type(w)is not int or w<0 for w in grid['weights'])or sum(grid['weights'])<=0:
                raise ValueError('positive total nonnegative integer grid weights required')
            if type(grid['origin'])is not int or not 0<=grid['origin']<n or len(grid['adjacency'])!=n:
                raise ValueError('invalid origin/adjacency dimensions')
            for i,neighbors in enumerate(grid['adjacency']):
                if len(neighbors)!=len(set(neighbors))or any(type(j)is not int or not 0<=j<n or j==i
                                                           for j in neighbors):
                    raise ValueError('invalid adjacency')
                if any(i not in grid['adjacency'][j]for j in neighbors):
                    raise ValueError('adjacency must be undirected')
    if set(value['stages'])!={'learning','validation'}:raise ValueError('both stages required')
    return value


class RingOracle:
    """One cache per method/stage; every newly simulated point has a cost event.

    launch_sets is a list of grids, each with six-coordinate absolute launches.
    All points start at the ring entrance. These are declared finite-grid scores,
    not continuous dynamic aperture or longitudinally resolved momentum aperture.
    """
    def __init__(self, protocol, *, stage='learning', runtime=None):
        self.at, self.np = load_runtime(runtime)
        self.protocol = validated_protocol(protocol)
        self.protocol_sha256 = digest(self.protocol)
        self.stage = stage
        self.stage_spec = self.protocol['stages'][stage]
        self.turns = self.stage_spec['turns']
        if type(self.turns) is not int or self.turns < 1:
            raise ValueError('positive integer turn horizon required')
        self.events = []
        self.calls = []
        self.failed_calls = []
        self.cache = {}
        self.rings = {}
        self.construction_seconds = 0.0
        self.physical_tracking_seconds = 0.0

    def _ring(self, design):
        if design not in self.rings:
            start = time.perf_counter()
            ring = base_ring()
            set_strengths(ring, self.protocol['designs'][design]['strengths'])
            self.rings[design] = ring
            self.construction_seconds += time.perf_counter() - start
        return self.rings[design]

    def query(self, requests, *, purpose='acquisition'):
        # Validate the entire request before touching the simulator.
        if digest(self.protocol)!=self.protocol_sha256:
            raise ValueError('protocol changed after oracle construction')
        checked = []
        for item in requests:
            if len(item) != 3 or any(type(i) is not int for i in item):
                raise ValueError('request must be integer (objective, design, launch)')
            objective, design, launch = item
            if not 0 <= design < len(self.protocol['designs']):
                raise ValueError('unknown design')
            if not 0 <= objective < len(self.stage_spec['launch_sets']):
                raise ValueError('unknown objective')
            grid = self.stage_spec['launch_sets'][objective]
            if not 0 <= launch < len(grid['coordinates']):
                raise ValueError('unknown launch')
            checked.append(tuple(item))
        fresh = list(dict.fromkeys(k for k in checked if k not in self.cache))
        by_design = {}
        for key in fresh:
            by_design.setdefault(key[1], []).append(key)
        for design, keys in by_design.items():
            ring = self._ring(design)
            initial = self.np.asfortranarray(self.np.array([
                self.stage_spec['launch_sets'][o]['coordinates'][l] for o, d, l in keys
            ], dtype=float).T)
            start = time.perf_counter()
            # keep_lattice=False avoids the global AT cache reusing another design.
            try:
                _, _, diagnostics = ring.track(initial, nturns=self.turns, refpts=[],
                                                losses=True, omp_num_threads=1,
                                                keep_lattice=False)
            except Exception as exc:
                elapsed=time.perf_counter()-start
                self.physical_tracking_seconds+=elapsed
                self.failed_calls.append({'design':design,'points':len(keys),'seconds':elapsed,
                                          'purpose':purpose,'stage':self.stage,
                                          'exception':type(exc).__name__})
                raise
            elapsed = time.perf_counter() - start
            self.physical_tracking_seconds += elapsed
            loss = diagnostics['loss_map']
            self.calls.append({'design': design, 'points': len(keys), 'seconds': elapsed,
                               'purpose': purpose, 'stage': self.stage})
            for j, (objective, _, launch) in enumerate(keys):
                lost = bool(loss['islost'][j])
                turn = int(loss['turn'][j]) if lost else self.turns
                element = int(loss['elem'][j]) if lost else None
                if not 0 <= turn <= self.turns or (lost and turn==self.turns):
                    raise ValueError('invalid simulator loss horizon')
                value = turn / self.turns if lost else 1.0
                event = {'objective': objective, 'design': design, 'launch': launch,
                         'survived': not lost, 'completed_turns': turn,
                         'loss_element_zero_based': element,
                         'survival_fraction': value, 'turns': self.turns,
                         'stage': self.stage, 'purpose': purpose,
                         'protocol_sha256': self.protocol_sha256}
                self.cache[(objective, design, launch)] = event
                self.events.append(event)
        return [self.cache[key].copy() for key in checked]

    def ledger(self):
        return {'stage': self.stage, 'turns': self.turns,
                'physical_points': len(self.events), 'batched_tracking_calls': len(self.calls),
                'attempted_physical_points':sum(c['points']for c in self.calls+self.failed_calls),
                'construction_seconds': self.construction_seconds,
                'tracking_seconds': self.physical_tracking_seconds,
                'completed_particle_turns': sum(e['completed_turns'] for e in self.events),
                'calls': self.calls,'failed_calls':self.failed_calls}


def connected_fraction(labels, grid):
    if len(labels) != len(grid['coordinates']):
        raise ValueError('label/grid size mismatch')
    origin = grid['origin']
    if not labels[origin]:
        return 0.0
    seen = {origin}
    pending = [origin]
    while pending:
        for node in grid['adjacency'][pending.pop()]:
            if node not in seen and labels[node]:
                seen.add(node)
                pending.append(node)
    return sum(grid['weights'][i] for i in seen) / sum(grid['weights'])
