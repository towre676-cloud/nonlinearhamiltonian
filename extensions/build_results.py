#!/usr/bin/env python3
"""Regenerate results/: enveloped certificates for every milestone, plus RECEIPTS.json.

Each result is produced by the relevant compiler, wrapped in a machinery-envelope-v1
object (envelope.make replays it with the independent checker) and written to
results/<area>/<name>.json, gzipped deterministically when larger than 1 MB. The index
records the exact replay command, the file hash and the checker summary.

Usage: python3 -B extensions/build_results.py [--skip-slow]
"""
from __future__ import annotations
import argparse
import gzip
import hashlib
import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT = ROOT / 'results'
for sub in ('', 'observer', 'hamiltonian', 'structure', 'arithmetic'):
    sys.path.insert(0, str(HERE / sub))
import envelope                              # noqa: E402
import observer as OBS                       # noqa: E402
import panels as PAN                         # noqa: E402
import adaptive as ADA                       # noqa: E402
import weyl_groebner as WG                   # noqa: E402
import weyl_kernel as WK                     # noqa: E402
import contraction_seed as CS                # noqa: E402
import obstruction as OB                     # noqa: E402
import dgla as DG                            # noqa: E402
import pell as PE                            # noqa: E402

PRODUCER = 'towre676-cloud/nonlinearhamiltonian extensions (exact rational, Python standard library)'
index = []


def write(area, name, env, seconds):
    raw = json.dumps(env, indent=1, ensure_ascii=False).encode('utf-8') + b'\n'
    path = OUT / area / (name + '.json')
    if len(raw) > 1_000_000:
        path = path.with_suffix('.json.gz')
        raw = gzip.compress(raw, compresslevel=9, mtime=0)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(raw)
    res = envelope.check(env)['checker_result']
    rel = path.relative_to(ROOT).as_posix()
    index.append({'file': rel, 'sha256': hashlib.sha256(raw).hexdigest(), 'witness_kind': env['witness_kind'],
                  'replay': f'python3 -B extensions/envelope.py check {rel}', 'producer_seconds': round(seconds, 2),
                  'summary': {k: v for k, v in res.items() if k not in ('scope', 'nodes', 'names')}})
    print(rel, env['witness_kind'], 'passed', flush=True)


def timed(fn, *a, **k):
    t = time.time()
    r = fn(*a, **k)
    return r, time.time() - t


def observers():
    m = json.loads((HERE / 'observer/observation_example.json').read_text())
    cert, s = timed(OBS.compile_model, m)
    write('observer', 'feed_example', envelope.make(
        'observer-closure', m, cert, ['finite known rational actions', 'linear state summaries',
                                      'static initial panel measured once'],
        'all action words and all initial states of the encoded model', ['D15-F01', 'D14-F01'], PRODUCER, verify=False), s)
    eye = [[1, 0], [0, 1]]
    ill = {'dimension': 2, 'sensors': [{'name': 'x', 'row': [1, 0], 'cost': 1}, {'name': 'y/1000', 'row': [0, '1/1000'], 'cost': 1}],
           'noise': eye, 'targets': {'mode': 'explicit', 'matrices': [[[0, 1]]]}, 'contract': 'per_target',
           'gamma_squared': str(999 ** 2)}
    corr = {'dimension': 2, 'sensors': [{'name': 'x_a', 'row': [1, 0], 'cost': 1}, {'name': 'x_b', 'row': [1, 0], 'cost': 1},
                                        {'name': 'y', 'row': [0, 1], 'cost': 3}],
            'noise': [[1, '1/2', 0], ['1/2', 1, 0], [0, 0, 1]],
            'targets': {'mode': 'finite_horizon', 'actions': {'feed': [[1, 0], [1, 1]]}, 'target': [[0, 1]], 'horizon': 1},
            'contract': 'per_target', 'gamma_squared': '2'}
    for name, m in (('rank_perfect_ill_conditioned', ill), ('correlated_finite_horizon', corr)):
        (cert, _), s = timed(PAN.solve, m)
        write('observer', name, envelope.make(
            'noise-panel-selection', m, cert, ['deterministic ellipsoidal noise with declared joint matrix',
                                               'initial static panel', 'worst case over all initial states',
                                               'tie policy one_optimum'],
            'exact optimum (or infeasibility) over all subsets of the finite menu', ['D15-F01', 'D15-F03', 'D12-F04'],
            PRODUCER, verify=False), s)
    tt = {'states': ['a', 'b', 'c'], 'labels': {'a': 0, 'b': 1, 'c': 1},
          'tests': [{'name': 't1', 'cost': 1, 'outcomes': {'a': 0, 'b': 1, 'c': 1}},
                    {'name': 't2', 'cost': 2, 'outcomes': {'a': 1, 'b': 0, 'c': 1}},
                    {'name': 't4', 'cost': 4, 'outcomes': {'a': 0, 'b': 1, 'c': 2}}]}
    cert, s = timed(ADA.solve, tt)
    cert.pop('result')
    write('observer', 'target_only_decision', envelope.make(
        'adaptive-experiment', tt, cert, ['deterministic finite test table', 'positive exact costs'],
        'exact minimum worst-case cost over adaptive policies', ['D15-F04'], PRODUCER, verify=False), s)


HAMILTONIANS = [
    ('q3', 'q^3', False), ('qp3', 'q*p^3', False), ('qp3_plus_q2', 'q*p^3+q^2', False),
    ('qp3_plus_p2', 'q*p^3+p^2', False), ('qp3_plus_q2_plus_p2', 'q*p^3+q^2+p^2', True),
    ('q3p3', 'q^3*p^3', False), ('q2p2', 'q^2*p^2', False), ('q2p3', 'q^2*p^3', False), ('p3_plus_q2', 'p^3+q^2', False),
]


def hamiltonians(skip_slow):
    for name, h, slow in HAMILTONIANS:
        if slow and skip_slow:
            continue
        H = WG.parse_poly(h)
        (meta, receipt), s1 = timed(WG.discover, H, max_steps=400000, max_generators=100)
        (kmeta, kobj), s2 = timed(WK.classify, receipt)
        model = receipt['hamiltonian']
        write('hamiltonian', name, envelope.make(
            'weyl-polynomial-kernel', model, kobj,
            ['flat Weyl-Moyal convention, one canonical pair', 'D = {H,.}, C_k = T_k(H,.) for odd k >= 3',
             'coefficients in Q'],
            'full dynamic exact core in all polynomial degrees', ['D16-F03', 'D06-F02'], PRODUCER, verify=False), s1 + s2)


SIX_PARAMETER = [('six_a1_b2_c3_e1', '1', '2', '3', '0', '1', '0'), ('six_a_minus2_b_half_d5', '-2', '1/2', '0', '5', '0', '0'),
                 ('six_a0_b2_c3_d1_e1', '0', '2', '3', '1', '1', '0'), ('six_a0_c_minus1_e7_f4', '0', '0', '-1', '0', '7', '4')]


def top_reductions():
    import top_reduction as TR
    for name, *coef in SIX_PARAMETER:
        a, b, c, d, e, f = (WG.F(x) for x in coef)
        H = WG.W.tidy({(1, 3): WG.F(1), (2, 0): a, (1, 1): b, (0, 2): c, (1, 0): d, (0, 1): e, (0, 0): f})
        (meta, cert), s = timed(TR.reduce, H, (3, 1))
        write('hamiltonian', name, envelope.make(
            'weyl-top-reduction', cert['hamiltonian'], cert,
            ['weight (3,1); top part qp^3 + a q^2', 'top-weight reduction lemma (DYNAMIC_CORE_RESULTS.md 3b)',
             'coefficients in Q'],
            'full dynamic exact core in all polynomial degrees', ['D16-F03', 'D06-F02'], PRODUCER, verify=False), s)


def structure():
    tri = json.loads((HERE / 'structure/triangle.json').read_text())
    for name, b in (('triangle_primitive', [1, 2, -3]), ('triangle_obstruction', [1, 2, -2])):
        ans, s = timed(OB.solve, tri, 1, b)
        write('structure', name, envelope.make(
            'rational-obstruction-answer', tri, ans, ['finite cochain complex over Q'],
            'rational cohomology only; no integral torsion statement', ['D05-F03', 'D05-F01'], PRODUCER, verify=False), s)
    toy = {'schema': 'dgla-v1', 'field': 'Q',
           'basis': [{'degree': 1, 'name': 'e1'}, {'degree': 1, 'name': 'e2'}, {'degree': 2, 'name': 'f'}],
           'differential': [[0, 0, 0]] * 3, 'bracket': [[0, 1, [[2, 1]]]]}
    heis = DG.lie_deformation_dgla(3, {(0, 1): {2: 1}})
    cases = [('dgla_toy_obstructed', toy, [1, 1, 0], 3),
             ('heisenberg_order2_obstruction', heis, DG.two_cochain(3, {(0, 1): {0: 1}, (0, 2): {1: 1}}, heis), 3),
             ('heisenberg_order3_jet_obstruction', heis, DG.two_cochain(3, {(0, 1): {1: 1}, (1, 2): {2: 1}}, heis), 4),
             ('heisenberg_lift_order4', heis, DG.two_cochain(3, {(0, 2): {2: 1}}, heis), 4)]
    for name, m, x1, order in cases:
        cert, s = timed(DG.lift, m, [str(c) for c in x1], order)
        cert.pop('result')
        write('structure', name, envelope.make(
            'dgla-lifting', m, cert, ['finite DGLA over Q given by structure constants', 'truncation as declared'],
            'formal Maurer-Cartan lifting to the declared order; no convergence or moduli claim',
            ['D04-F03', 'D16-F06'], PRODUCER, verify=False), s)


def arithmetic():
    fx = json.loads((HERE / 'structure/arithmetic_future_fixtures.json').read_text())['cases']
    models = [{'D': c['D'], 'N': c['N'], 'unit': c['unit'], 'height': c['height_bound'],
               'filter': {'modulus': 3, 'accept': [[x, 0] for x in range(3)]}} for c in fx]
    models.append({'D': 2, 'N': -7, 'unit': [17, 12], 'height': 10 ** 30})
    models.append({'D': 13, 'N': -3, 'unit': 'fundamental', 'height': 10 ** 40})
    for m in models:
        cert, s = timed(PE.compile_model, m)
        cert.pop('result')
        u = 'fundamental' if m['unit'] == 'fundamental' else f"{m['unit'][0]}_{m['unit'][1]}"
        name = f"pell_D{m['D']}_N{m['N']}_unit{u}".replace('-', 'm')
        write('arithmetic', name, envelope.make(
            'pell-orbit-reduction', m, cert, ['declared order Z[sqrt D], integer coordinates',
                                              'supplied unit, not necessarily fundamental'],
            'complete orbit classification under the supplied unit; exact filtered height counts',
            ['D01-F04', '2024:Y24-03-024'], PRODUCER, verify=False), s)


def integer_and_units():
    import smith as SM
    import units as UN
    for name, m, cocycles in (
            ('rp2_integral_cohomology', {'field': 'Z', 'dimensions': [1, 1, 1], 'differentials': [[[0]], [[2]]]}, [(2, [1])]),
            ('klein_bottle_torsion_witness', {'field': 'Z', 'dimensions': [1, 2, 1], 'differentials': [[[0], [0]], [[2, 0]]]},
             [(2, [1]), (2, [2])]),
            ('times_two_rational_vs_integral', {'field': 'Z', 'dimensions': [1, 1], 'differentials': [[[2]]]}, [(1, [1])])):
        cert, s = timed(SM.build, m, cocycles)
        cert.pop('result')
        write('structure', name, envelope.make(
            'integer-cohomology', m, cert, ['finite cochain complex over Z'],
            'integral cohomology (rank and torsion) with integer coboundary decisions', ['D05-F01', 'D05-F03'],
            PRODUCER, verify=False), s)
    for D in (2, 61, 991):
        (cert, model), s = timed(UN.fundamental, D)
        cert.pop('result')
        write('arithmetic', f'fundamental_unit_D{D}', envelope.make(
            'fundamental-unit', model, cert, ['order Z[sqrt D]', 'Legendre convergent criterion'],
            'unit group of Z[sqrt D]; not the maximal order', ['D01-F04'], PRODUCER, verify=False), s)


def quartic_theorem():
    import quartic_uniform as QU
    cert, s = timed(QU.build, 12)
    cert.pop('result')
    write('hamiltonian', 'quartic_all_degrees_theorem', envelope.make(
        'quartic-uniform', {'family': cert['family']}, cert,
        ['binary quartics with four distinct roots, normal form q^4 + l q^2 p^2 + p^4 over Qbar',
         'GL2 covariance of the transvectants; D_inf graded for homogeneous H'],
        'D_inf(H) = span{1, H} in all degrees for every quartic with distinct roots', ['D16-F03', 'D06-F02'],
        PRODUCER, verify=False), s)


BINARY_MONOMIALS = [('quintic_q5', 'q^5'), ('quintic_q4p', 'q^4*p'), ('sextic_q6', 'q^6'), ('sextic_q5p', 'q^5*p'),
                    ('sextic_q4p2', 'q^4*p^2')]


def binary_forms():
    """Quintic and sextic classification: monomial cores and static finiteness at a simple root.
    The static producer uses sympy (only here); the checkers use the standard library."""
    import binary_static as BS
    for name, h in BINARY_MONOMIALS:
        H = WG.parse_poly(h)
        (meta, receipt), s1 = timed(WG.discover, H, max_steps=400000, max_generators=100)
        (kmeta, kobj), s2 = timed(WK.classify, receipt)
        write('hamiltonian', name, envelope.make(
            'weyl-polynomial-kernel', receipt['hamiltonian'], kobj,
            ['flat Weyl-Moyal convention, one canonical pair', 'D = {H,.}, C_k = T_k(H,.) for odd k >= 3',
             'coefficients in Q'],
            'full dynamic exact core in all polynomial degrees (monomial root class of the quintic/sextic '
            'classification)', ['D16-F03', 'D06-F02'], PRODUCER, verify=False), s1 + s2)
    for d in (5, 6):
        cert, s = timed(BS.build, d)
        cert.pop('result')
        write('hamiltonian', f'binary_static_d{d}', envelope.make(
            'binary-static', {'degree': d}, cert,
            [f'binary forms of degree {d} over an algebraically closed field of characteristic zero with a simple root',
             'local normal form at the simple root; static top lemma for q^(d-1) p'],
            f'E_n(H) = 0 for n >= N0 unless H has type ({d - 1},1) or ({d - 2},1,1)', ['D16-F03', 'D06-F02'],
            PRODUCER + '; elimination trees searched with sympy', verify=False), s)


RIGIDITY_EXAMPLES = [
    ('rigidity_septic_squarefree_perturbed', {(7, 0): 1, (0, 7): 1, (1, 6): -1, (3, 2): 5, (2, 1): -3, (0, 1): 1}),
    ('rigidity_octic_4211_perturbed', {(4, 4): 1, (3, 5): -1, (2, 6): -1, (1, 7): 1, (5, 1): 2, (0, 2): 1}),
    ('rigidity_sextic_3111_perturbed', {(5, 1): 1, (3, 3): -1, (2, 2): 7, (1, 0): 1}),
    ('rigidity_octic_squarefree', {(8, 0): 1, (0, 8): 1, (4, 4): 3}),
    ('rigidity_q5p3_monomial', {(5, 3): 1}),
]


def rigidity():
    import check_monomial_theorem as MT
    import check_root_rigidity as RR
    cert, s = timed(lambda: {'format': MT.FORMAT, 'identities': sorted(MT.identities())})
    write('hamiltonian', 'monomial_theorem', envelope.make(
        'monomial-theorem', {'family': 'q^a p^b, a >= b, a + b >= 3'}, cert,
        ['characteristic zero', 'ray analysis of the T_3 gate along D-orbits of monomials'],
        'D_inf(q^a p^b) in all degrees for all exponents', ['D16-F03', 'D06-F02'], PRODUCER, verify=False), s)
    import check_simple_root as SRC
    cert, s = timed(SRC.build, 40)
    cert.pop('result')
    write('hamiltonian', 'simple_root_rigidity', envelope.make(
        'simple-root-rigidity', {'family': 'binary forms with a simple root, every degree d >= 3'}, cert,
        ['characteristic zero', 'weight induction at a simple root with T_3 and one bracket'],
        'S_n(H) = 0 for n >= N0(d) unless H = c l^(d-1) m; N0 tabulated for d <= 40', ['D16-F03', 'D06-F02'],
        PRODUCER, verify=False), s)
    for name, h in RIGIDITY_EXAMPLES:
        H = {k: WG.F(v) for k, v in h.items()}
        c, s = timed(RR.certify, H)
        c.pop('result')
        write('hamiltonian', name, envelope.make(
            'root-rigidity', c['hamiltonian'], c,
            ['root type of the top homogeneous part over Qbar via a verified square-free decomposition',
             'routes of DYNAMIC_CORE_RESULTS.md section 5'],
            'D_inf(H) when a proved route applies; otherwise reported open', ['D16-F03', 'D06-F02'], PRODUCER,
            verify=False), s)


BINOMIALS = [('binomial_qp2_plus_q2', 'q*p^2+q^2'), ('binomial_qp4_plus_q2', 'q*p^4+q^2'),
             ('binomial_q4_plus_p2', 'q^4+p^2'), ('binomial_q5_plus_p2', 'q^5+p^2')]
TWO_ROOT_EXAMPLES = [
    ('tworoot_unequal_normal_form', {(3, 2): 1, (2, 1): 1, (1, 0): 2, (1, 1): -1}),
    ('tworoot_unequal_generic', {(3, 2): 1, (0, 1): 1}),
    ('tworoot_near_affine', {(1, 4): 1, (1, 2): 3, (0, 3): -1, (0, 1): 1}),
    ('tworoot_near_q2_family', {(1, 4): 1, (2, 0): 2, (1, 2): 1, (0, 3): 5}),
    ('tworoot_pure_strip', {(4, 0): 1, (2, 0): 1, (1, 1): 3, (0, 1): -1}),
    ('tworoot_pure_p2_family', {(5, 0): 1, (0, 2): 1, (1, 1): 2, (3, 0): -1}),
    ('tworoot_balanced_KG', {(2, 2): 1, (2, 1): 2, (2, 0): 1, (1, 1): 3, (1, 0): 3}),
    ('tworoot_balanced_box', {(3, 3): 1, (2, 1): 1, (1, 1): -2}),
]


def two_root():
    import check_two_root as TRC
    import check_balanced as CBL
    cert, s0 = timed(lambda: {'format': CBL.FORMAT, 'identities': sorted(CBL.check()['identities'])})
    write('hamiltonian', 'balanced_top_theorem', envelope.make(
        'balanced-top', {'family': 'c Q^mu + lower-order terms'}, cert,
        ['characteristic zero', 'weight induction on off-diagonal parts with T_3 and the top of {H, G}'],
        'D_inf = K[G] if H in K[G], else span{1, H}', ['D16-F03', 'D06-F02'], PRODUCER, verify=False), s0)
    for name, h in BINOMIALS:
        H = WG.parse_poly(h)
        (meta, receipt), s1 = timed(WG.discover, H, max_steps=400000, max_generators=100)
        (kmeta, kobj), s2 = timed(WK.classify, receipt)
        write('hamiltonian', name, envelope.make(
            'weyl-polynomial-kernel', receipt['hamiltonian'], kobj,
            ['flat Weyl-Moyal convention, one canonical pair', 'D = {H,.}, C_k = T_k(H,.) for odd k >= 3',
             'coefficients in Q'],
            'full dynamic exact core in all polynomial degrees (binomial top of DYNAMIC_CORE_RESULTS.md section 6)',
            ['D16-F03', 'D06-F02'], PRODUCER, verify=False), s1 + s2)
    for name, h in TWO_ROOT_EXAMPLES:
        c, s = timed(TRC.certify, {k: WG.F(v) for k, v in h.items()})
        c.pop('result')
        write('hamiltonian', name, envelope.make(
            'two-root-perturbation', c['hamiltonian'], c,
            ['top homogeneous part with at most two roots', 'criteria of DYNAMIC_CORE_RESULTS.md section 6'],
            'D_inf(H) when a proved criterion applies; otherwise reported as conjectural', ['D16-F03', 'D06-F02'],
            PRODUCER, verify=False), s)


SECTIONS = {'observer': lambda a: observers(), 'structure': lambda a: structure(), 'arithmetic': lambda a: arithmetic(),
            'hamiltonian': lambda a: hamiltonians(a.skip_slow), 'top': lambda a: top_reductions(),
            'integer': lambda a: integer_and_units(), 'quartic': lambda a: quartic_theorem(),
            'binary': lambda a: binary_forms(), 'rigidity': lambda a: rigidity(),
            'tworoot': lambda a: two_root()}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--skip-slow', action='store_true')
    ap.add_argument('--only', nargs='*', choices=sorted(SECTIONS), help='regenerate only these sections')
    a = ap.parse_args()
    for name in (a.only or SECTIONS):
        SECTIONS[name](a)
    idx_path = OUT / 'RECEIPTS.json'
    old = {r['file']: r for r in json.loads(idx_path.read_text())['results']} if idx_path.exists() else {}
    merged = {**old, **{r['file']: r for r in index}}
    idx_path.write_text(json.dumps({'schema': 'machinery-results-v1', 'results': [merged[k] for k in sorted(merged)]},
                                   indent=1) + '\n')
    print(json.dumps({'status': 'written', 'results': len(merged)}))


if __name__ == '__main__':
    main()
