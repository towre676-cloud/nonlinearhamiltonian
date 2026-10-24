#!/usr/bin/env python3
"""Exact finite-table brackets for aperture decisions (the spec's optional checked layer).

The checker is pure exact arithmetic and needs no simulator. A label table maps
grid points to 1 (survived the horizon), 0 (lost by the horizon) or None
(unknown). Unknown labels stay unknown; nothing is imputed from a model.

* weighted bracket: for nonnegative weights, sum(w*l) over completions lies in
  [value(unknowns -> 0), value(unknowns -> 1)].
* origin-connected bracket: the weight of survivors 4-connected to the origin
  point is monotone in the labels, so the same two completions bracket it. No
  radial monotonicity is assumed.
* horizons: a loss at turn t <= T is a loss at every horizon >= T; survival to
  T says nothing about a longer horizon, so it becomes unknown there.
* Pareto exclusion: candidate A is excluded only if some B has lower bounds >=
  A's upper bounds in every objective, strictly in one. Overlapping brackets
  exclude nothing.

Run without arguments, the script checks every claim above by brute force over all completions of
random small tables. `--runtime DIR` additionally runs a staged HMBA
demonstration with Accelerator Toolbox 0.9.0, then tracks everything to the
full horizon to confirm each bracket and exclusion against the resolved table.
The demonstration candidates are illustrative sextupole scalings that do not
preserve chromaticity; they are not a tuning result.
"""
from fractions import Fraction
from itertools import product
from pathlib import Path
import argparse
import hashlib
import json
import os
import random
import sys
import time


def complete(labels, fill):
    return {k: (fill if v is None else v) for k, v in labels.items()}


def weighted(labels, weights):
    if any(w < 0 for w in weights.values()):
        raise ValueError('weights must be nonnegative')
    return sum((weights[k] for k, v in labels.items() if v == 1), Fraction(0))


def connected(labels, weights, origin):
    """Weight of survivors 4-connected to origin on an integer grid."""
    if labels.get(origin) != 1:
        return Fraction(0)
    seen = {origin}
    stack = [origin]
    while stack:
        i, j = stack.pop()
        for q in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
            if q not in seen and labels.get(q) == 1:
                seen.add(q)
                stack.append(q)
    return sum((weights[k] for k in seen), Fraction(0))


def bracket(f, labels, *args):
    return f(complete(labels, 0), *args), f(complete(labels, 1), *args)


def at_horizon(loss_turn, tracked, horizon):
    """Labels at `horizon` from points tracked to `tracked` turns.

    loss_turn[k] is the turn of loss, or None if the point survived `tracked`.
    """
    out = {}
    for k, t in loss_turn.items():
        if t is not None:
            out[k] = 0 if t < horizon else 1
        else:
            out[k] = 1 if tracked >= horizon else None
    return out


def excluded(brackets):
    """brackets[name] = [(lo, hi), ...] for objectives to maximize."""
    out = {}
    for a, ba in brackets.items():
        for b, bb in brackets.items():
            if a == b:
                continue
            ge = all(lb >= ha for (lb, _), (_, ha) in zip(bb, ba))
            gt = any(lb > ha for (lb, _), (_, ha) in zip(bb, ba))
            if ge and gt:
                out[a] = b
                break
    return out


def selftest(seed=0, trials=3000):
    rng = random.Random(seed)
    checked = 0
    for _ in range(trials):
        nx, ny = rng.randint(1, 4), rng.randint(1, 3)
        pts = [(i, j) for i in range(nx) for j in range(ny)]
        w = {p: Fraction(rng.randint(0, 5), rng.randint(1, 3)) for p in pts}
        lab = {p: rng.choice([0, 1, None]) for p in pts}
        org = rng.choice(pts)
        unk = [p for p in pts if lab[p] is None]
        bw, bc = bracket(weighted, lab, w), bracket(connected, lab, w, org)
        vals_w, vals_c = [], []
        for bits in product([0, 1], repeat=len(unk)):
            full = dict(lab)
            full.update(zip(unk, bits))
            vals_w.append(weighted(full, w))
            vals_c.append(connected(full, w, org))
            checked += 1
        # sound and attained: both endpoints are realised completions
        assert (min(vals_w), max(vals_w)) == bw
        assert (min(vals_c), max(vals_c)) == bc
        # horizons: every label decided from a shorter run is the true label
        t1, t2 = rng.randint(1, 10), rng.randint(1, 20)
        life = {p: rng.randint(0, 25) for p in pts}          # true loss turn
        seen = {p: (life[p] if life[p] < t1 else None) for p in pts}
        short = at_horizon(seen, t1, t2)
        for p in pts:
            true = 0 if life[p] < t2 else 1
            assert short[p] in (None, true)
            assert (short[p] is None) == (life[p] >= t1 and t1 < t2)
    # Pareto exclusion soundness: every completion of the excluder beats every
    # completion of the excluded one
    for _ in range(trials):
        names = 'ABC'
        br = {}
        for n in names:
            row = []
            for _ in range(2):
                lo = Fraction(rng.randint(0, 6))
                row.append((lo, lo + rng.randint(0, 3)))
            br[n] = row
        for a, b in excluded(br).items():
            for va in product(*[range(int(lo), int(hi) + 1) for lo, hi in br[a]]):
                for vb in product(*[range(int(lo), int(hi) + 1) for lo, hi in br[b]]):
                    assert all(y >= x for x, y in zip(va, vb)) and any(y > x for x, y in zip(va, vb))
    return checked


def demo(runtime, out_path, horizon, stages):
    sys.path.insert(0, str(runtime))
    os.environ['OMP_NUM_THREADS'] = '1'
    import numpy as np
    import at
    import importlib.metadata
    if at.__version__ != '0.9.0':
        raise ValueError('demo specified for accelerator-toolbox==0.9.0')
    src = Path(__file__).parent / 'dataset_inspection/at_hmba.mat'
    digest = hashlib.sha256(src.read_bytes()).hexdigest()
    if digest != '8547502b0a4612a0e145fa6033e5ba98bb13567035fed43cadef760dae385c7b':
        raise ValueError('public lattice source mismatch')
    cell0 = at.Lattice.load(src)
    # 13 x 7 grid, 2 mm by 1 mm, y >= 0 (midplane symmetry assumed by the grid)
    pts = [(i, j) for i in range(-6, 7) for j in range(7)]
    xy = {p: (Fraction(2 * p[0], 1000), Fraction(p[1], 1000)) for p in pts}
    w = {p: Fraction(2) for p in pts}                     # cell area in mm^2
    origin = (0, 0)
    deltas = [Fraction(0), Fraction(2, 100)]
    scales = {'s1.00': Fraction(1), 's0.90': Fraction(9, 10), 's1.10': Fraction(11, 10)}
    rings = {}
    for name, sc in scales.items():
        cell = cell0.deepcopy()
        for e in cell:
            if isinstance(e, at.Sextupole):
                e.PolynomB[2] *= float(sc)
        r = (cell * int(cell.periodicity)).disable_6d(copy=True)
        if r.periodicity != 1 or len(r) != len(cell) * int(cell.periodicity):
            raise ValueError('full-ring turn convention mismatch')
        rings[name] = r

    def track(ring, z, n):
        _, p, d = ring.track(np.asfortranarray(z), nturns=n, refpts=[], losses=True,
                             keep_lattice=False, omp_num_threads=1)
        lm = d['loss_map']
        return np.array(p['rout']).reshape(6, -1), np.array(lm['islost']), np.array(lm['turn'])

    def initial(dp):
        z = np.zeros((6, len(pts)), order='F')
        z[0] = [float(xy[p][0]) for p in pts]
        z[2] = [float(xy[p][1]) for p in pts]
        z[4] = float(dp)
        return z

    # state[(cand, k)]: tracked turns, loss turn per point, live coordinates
    state = {}
    ledger = {'particle_turns_tracked': 0, 'tracking_seconds': 0.0, 'checker_seconds': 0.0}

    def advance(cand, k, upto):
        st = state[(cand, k)]
        live = [i for i, p in enumerate(pts) if st['loss'][p] is None]
        n = upto - st['turns']
        if live and n > 0:
            t0 = time.perf_counter()
            z, lost, turn = track(rings[cand], st['z'][:, live], n)
            ledger['tracking_seconds'] += time.perf_counter() - t0
            ledger['particle_turns_tracked'] += int(sum((turn[m] + 1) if lost[m] else n
                                                        for m in range(len(live))))
            for m, i in enumerate(live):
                st['z'][:, i] = z[:, m]
                if lost[m]:
                    st['loss'][pts[i]] = st['turns'] + int(turn[m])
        st['turns'] = upto

    def brackets_for(cand):
        rows = []
        for k in range(len(deltas)):
            st = state[(cand, k)]
            rows.append(bracket(connected, at_horizon(st['loss'], st['turns'], horizon), w, origin))
        return rows

    for cand in scales:
        for k, dp in enumerate(deltas):
            state[(cand, k)] = {'turns': 0, 'loss': {p: None for p in pts}, 'z': initial(dp)}
    # Before the horizon no survival is decided, so every lower bound is 0 and
    # brackets alone can never exclude: an exact incumbent is needed first.
    incumbent = 's1.00'
    active = [c for c in scales if c != incumbent]
    log = []
    plan = [([incumbent], horizon)] + [(None, t) for t in stages + [horizon]]
    for who, upto in plan:
        movers = who if who is not None else list(active)
        for cand in movers:
            for k in range(len(deltas)):
                advance(cand, k, upto)
        t0 = time.perf_counter()
        br = {c: brackets_for(c) for c in scales}
        ex = {a: b for a, b in excluded(br).items() if a in active}
        ledger['checker_seconds'] += time.perf_counter() - t0
        log.append({'advanced': movers, 'to_turns': upto,
                    'brackets_mm2': {c: [[str(a), str(b)] for a, b in br[c]] for c in scales},
                    'excluded_now': ex,
                    'particle_turns_so_far': ledger['particle_turns_tracked']})
        active = [c for c in active if c not in ex]
    checked_cost = dict(ledger)
    # independent resolution: finish every candidate to the full horizon
    for cand in scales:
        for k in range(len(deltas)):
            advance(cand, k, horizon)
    truth = {c: [connected(at_horizon(state[(c, k)]['loss'], horizon, horizon), w, origin)
                 for k in range(len(deltas))] for c in scales}
    truth_weighted = {c: [weighted(at_horizon(state[(c, k)]['loss'], horizon, horizon), w)
                          for k in range(len(deltas))] for c in scales}
    for entry in log:
        for c, rows in entry['brackets_mm2'].items():
            for (lo, hi), v in zip(rows, truth[c]):
                if not Fraction(lo) <= v <= Fraction(hi):
                    raise AssertionError('bracket does not contain resolved value')
        for a, b in entry['excluded_now'].items():
            ta, tb = truth[a], truth[b]
            if not (all(y >= x for x, y in zip(ta, tb)) and any(y > x for x, y in zip(ta, tb))):
                raise AssertionError('exclusion not confirmed by resolved table')
    result = {
        'status': 'passed',
        'scope': ('exact finite-table bracket checker on a staged HMBA run; illustrative '
                  'sextupole scalings that break chromaticity correction; no tuning claim'),
        'lattice_sha256': digest, 'horizon_turns': horizon, 'stages': stages,
        'grid': {'x_mm': [-12, 12, 2], 'y_mm': [0, 6, 1], 'points': len(pts),
                 'objective': 'area (mm^2) of survivors 4-connected to (0,0)',
                 'deltas': [str(d) for d in deltas]},
        'candidates': {c: str(s) for c, s in scales.items()},
        'incumbent': 'fully resolved first; brackets alone never exclude before the horizon '
                     'because no survival is decided earlier, so every lower bound is 0',
        'stage_log': log,
        'resolved_connected_mm2': {c: [str(v) for v in truth[c]] for c in scales},
        'resolved_unconnected_count_mm2': {c: [str(v) for v in truth_weighted[c]] for c in scales},
        'all_brackets_contain_resolved_values': True,
        'all_exclusions_confirmed': True,
        'cost': {'checked_workflow': checked_cost,
                 'full_resolution_particle_turns': ledger['particle_turns_tracked'],
                 'full_resolution_tracking_seconds': ledger['tracking_seconds']},
        'physics': {'radiation': False, 'rf': False, 'space_charge': False, 'errors': False},
        'versions': {n: importlib.metadata.version(n)
                     for n in ['accelerator-toolbox', 'numpy', 'scipy']},
    }
    out_path.write_text(json.dumps(result, indent=2) + '\n')
    return result


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--runtime', type=Path, help='directory holding accelerator-toolbox 0.9.0')
    ap.add_argument('--output', type=Path,
                    default=Path(__file__).with_name('aperture_brackets_hmba.json'))
    ap.add_argument('--horizon', type=int, default=512)
    a = ap.parse_args()
    n = selftest()
    if not a.runtime:
        print(json.dumps({'status': 'passed', 'completions_checked': n,
                          'checks': ['weighted bracket sound and attained',
                                     'origin-connected bracket sound and attained',
                                     'short-horizon labels never contradict the true label',
                                     'Pareto exclusion holds for every completion']}))
        return
    print(f'selftest: {n} completions checked')
    if a.runtime:
        stages = [s for s in (16, 64, 256) if s < a.horizon]
        r = demo(a.runtime, a.output, a.horizon, stages)
        print(json.dumps({k: r[k] for k in ('resolved_connected_mm2', 'cost')}, indent=2))
        for e in r['stage_log']:
            print(e['advanced'], e['to_turns'], e['brackets_mm2'], e['excluded_now'])


if __name__ == '__main__':
    main()
