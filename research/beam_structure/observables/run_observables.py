#!/usr/bin/env python3
"""Build exact observable certificates and replay their small algebraic examples."""
import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import subprocess
import sys

from compiler import (check_certificate, compile_family, finite_word_pullback,
                      first_missing_image, hidden_cloud_witness, physical_outputs,
                      quadratic_backbone, residual_observable_bound, shared_backbone)
from polynomial import (P, Q, add, encode, monomial, power, scale)


HERE = Path(__file__).resolve().parent


def write(path, data):
    path.write_text(json.dumps(data, indent=2)+'\n')


def build(output):
    output.mkdir(parents=True, exist_ok=True)
    families = {}
    for name, shear in [('nonzero_shear', F(1)), ('zero_shear', F(0))]:
        certificate = compile_family(shear)
        checked = check_certificate(certificate)
        write(output/(name+'.json'), certificate)
        families[name] = checked
    write(output/'missing_information_witness.json', hidden_cloud_witness())
    certificate = compile_family()
    failures = {'quadrupole': first_missing_image(certificate, power(Q, 2)),
                'physical_p2': first_missing_image(certificate, physical_outputs(1)['p2'])}
    if any(row['closed'] for row in failures.values()):
        raise ValueError('expected finite-module obstruction absent')
    write(output/'control_obstructions.json', failures)
    backbones = [quadratic_backbone(2, 3, 4, 2), quadratic_backbone(2, 3, 4, F(15, 7))]
    delta = F(backbones[1]['delta'])
    defect, bound = residual_observable_bound(power(P, 2), delta, F(1, 2), F(2, 3))
    write(output/'backbone_routes.json', {'examples': backbones,
        'shared_route': shared_backbone([(2, 3, 4, 2), (3, 1, 6, 4), (0, 1, 0, 0)], 1),
        'mismatched_shear': shared_backbone([(2, 3, 4, 2)], 2),
        'conditional_p2_defect': encode(defect), 'conditional_p2_defect_bound': str(bound),
        'assumed_adapted_rectangle': {'Q_radius': '1/2', 'P_radius': '2/3'},
        'support_enclosure_verified': False,
        'scope': 'Algebraic reduction and a conditional local generator bound; no trajectory enclosure.'})
    maps = [(add(Q, scale(power(P, 2), F(1, 5))), P),
            (Q, add(P, monomial(0, 0, F(-2, 7)))),
            (scale(Q, F(3, 2)), scale(P, F(2, 3))),
            (add(Q, scale(power(P, 2), F(-2, 9))), P)]
    base = finite_word_pullback(physical_outputs(F(2, 3)), maps)
    extended = finite_word_pullback(physical_outputs(F(2, 3)),
        maps+[(Q, add(P, scale(Q, F(-1, 3))))]+maps)
    write(output/'finite_word_summaries.json', {'closed_family': base, 'extra_quadrupole_word': extended})
    tests = subprocess.run([sys.executable, '-B', '-S', '-m', 'unittest', 'discover',
        '-s', str(HERE), '-p', 'test_*.py'], capture_output=True, text=True)
    if tests.returncode:
        raise ValueError(tests.stdout+tests.stderr)
    receipt = {'status': 'passed', 'arithmetic': 'stdlib Fraction; exact rational arithmetic',
        'families': families, 'unit_tests': 10, 'unit_test_exit_code': tests.returncode,
        'finite_word_monomial_counts': {'closed': base['monomial_count'],
                                      'extra_quadrupole': extended['monomial_count']},
        'positive_probability_hidden_readout_difference': '-10/9',
        'all_degree_results': ['minimal dimension25 for fixed nonzero shear',
            'minimal dimension9 for zero shear', 'quadrupole control infinite common closure',
            'physical p2 control infinite common closure when shear is nonzero'],
        'all_degree_basis': 'Explicit proofs in THEOREMS.md; finite replays check implementations.',
        'source_sha256': {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                          for p in sorted(HERE.glob('*.py'))},
        'result_sha256': {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                         for p in sorted(output.glob('*.json')) if p.name != 'replay_receipt.json'},
        'tenfold_gain_established': False,
        'scope': 'Prescribed classical polynomial model only. No physical beam-transfer validation, space-charge closure or quantum-exactness inference.'}
    write(output/'replay_receipt.json', receipt)
    return receipt


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=HERE/'results')
    args = parser.parse_args()
    print(json.dumps(build(args.output), indent=2))
