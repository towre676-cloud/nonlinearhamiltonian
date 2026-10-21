#!/usr/bin/env python3
"""Adversarial bridge checks using the existing independent star exponential."""
from fractions import Fraction as F
import importlib.util
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('baseline_star_engine', root / 'research/hamiltonian/independent/engine.py')
e = importlib.util.module_from_spec(spec)
spec.loader.exec_module(e)
H, G = e.monomial(3, 3), e.monomial(2, 19)
bracket = e.moyal(H, G)
assert 2 not in bracket
assert bracket == {0: {(4, 21): F(51)}, 4: {(0, 17): F(8721, 4)}}
H, G = e.monomial(1, 3), e.monomial(2, 0)
assert e.defects(H, G) == {}
assert e.defects(H, e.poisson(H, G)) == {2: {(0, 2): F(18)}}
for r in range(6):
    assert e.moyal(H, e.monomial(3*r+2, r)) == {0: {(3*r+2, r+2): F(-8*r-6)}}
print(json.dumps({'status': 'passed', 'checks': 8,
                  'cases': ['third correction zero but fifth nonzero', 'exact first partner leaves the dynamic core',
                            'six favorite-identity calibration instances'],
                  'scope': 'Exact finite adversarial calculations; all-degree favorite identity has a separate source proof.'}, indent=2))
