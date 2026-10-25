#!/usr/bin/env python3
"""Check saved certificates without rerunning reachable-space discovery."""
import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path

from compiler import check_certificate
from polynomial import add, evaluate, monomial, multiply, power, Q, P, scale, substitute


def require(condition, message):
    if not condition:
        raise ValueError(message)


def check(directory):
    receipt = json.loads((directory/'replay_receipt.json').read_text())
    here = Path(__file__).resolve().parent
    for name, expected in receipt['source_sha256'].items():
        require(hashlib.sha256((here/name).read_bytes()).hexdigest() == expected, 'source identity')
    for name, expected in receipt['result_sha256'].items():
        require(hashlib.sha256((directory/name).read_bytes()).hexdigest() == expected, 'result identity')
    checks = {name: check_certificate(json.loads((directory/(name+'.json')).read_text()))
              for name in ['nonzero_shear', 'zero_shear']}
    witness = json.loads((directory/'missing_information_witness.json').read_text())
    laws = [[tuple(map(Fraction, row)) for row in witness[name]] for name in ['plus', 'minus']]
    def mean(poly, law):
        return sum((weight*evaluate(poly, q, p) for q, p, weight in law), Fraction(0))
    for law in laws:
        require(all(weight > 0 for q, p, weight in law), 'positive weights')
        require(sum(row[2] for row in law) == 1, 'normalization')
    for a in range(5):
        for b in range(9-2*a):
            require(mean(monomial(a, b), laws[0]) == mean(monomial(a, b), laws[1]), 'initial moments')
    c, s, t = map(Fraction, [witness['fixed_shear'], witness['kick_time'], witness['transport_time']])
    final_p = add(P, scale(Q, -2*s))
    final_q = add(Q, scale(power(final_p, 2), t))
    physical_output = power(add(final_p, scale(power(final_q, 2), -c)), 2)
    difference = mean(physical_output, laws[0])-mean(physical_output, laws[1])
    require(difference == Fraction(witness['future_physical_second_moment_difference']) == -Fraction(10, 9),
            'future physical second moment witness')
    physical_p = add(final_p, scale(power(final_q, 2), -c))
    stats = []
    for law in laws:
        mq, mp = mean(final_q, law), mean(physical_p, law)
        a = mean(power(final_q, 2), law)-mq*mq
        b = mean(multiply(final_q, physical_p), law)-mq*mp
        z = mean(power(physical_p, 2), law)-mp*mp
        stats.append((a, b, z, a*z-b*b))
    require(stats[0][:2] == stats[1][:2], 'position variance and cross covariance')
    require(stats[0][3]-stats[1][3] == Fraction(witness['future_projected_emittance_squared_difference']),
            'future squared-emittance witness')
    return {'status': 'passed', 'families': checks, 'initial_moments_checked': 25,
            'future_physical_second_moment_difference': str(difference),
            'certificate_discovery_rerun': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--results', type=Path, default=Path(__file__).with_name('results'))
    print(json.dumps(check(parser.parse_args().results), indent=2))
