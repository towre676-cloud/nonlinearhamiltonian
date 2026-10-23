#!/usr/bin/env python3
"""Run the contraction seed's independent tests and emit a structured receipt."""
import io
import json
from pathlib import Path
import sys
import unittest

here = Path(__file__).resolve().parent
sys.path.insert(0, str(here))
suite = unittest.defaultTestLoader.discover(str(here), pattern='test_contraction_seed.py')
stream = io.StringIO()
result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
print(json.dumps({'status': 'passed' if result.wasSuccessful() else 'failed',
                  'test_groups': result.testsRun, 'failures': len(result.failures),
                  'errors': len(result.errors), 'details': stream.getvalue(),
                  'scope': 'Finite rational complexes, exact contraction identities, primitives and obstruction witnesses.'}, indent=2))
raise SystemExit(0 if result.wasSuccessful() else 1)
