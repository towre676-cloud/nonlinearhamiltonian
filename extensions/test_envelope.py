"""C0 acceptance tests: typed envelopes reject wrong domains, swapped witness kinds and bad sources."""
import copy
import json
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
for sub in ('', 'observer', 'structure'):
    sys.path.insert(0, str(HERE / sub))
import envelope as E          # noqa: E402
import observer as OBS        # noqa: E402
import contraction_seed as CS  # noqa: E402

MODEL = json.loads((HERE / 'observer/observation_example.json').read_text())
TRI = json.loads((HERE / 'structure/triangle.json').read_text())


def obs_env():
    return E.make('observer-closure', MODEL, OBS.compile_model(MODEL), ['finite rational actions'],
                  'all words', ['D15-F01'], 'test')


class Envelopes(unittest.TestCase):
    def test_valid_envelopes_replay(self):
        self.assertEqual(E.check(obs_env())['status'], 'passed')
        env = E.make('rational-contraction', TRI, CS.build(TRI), ['finite Q complex'], 'rational cohomology',
                     ['D05-F03'], 'test')
        self.assertEqual(E.check(env)['checker_result']['cohomology_dimensions'], [1, 1])

    def rejects(self, env):
        with self.assertRaises((ValueError, KeyError, TypeError)):
            E.check(env)

    def test_rejections(self):
        good = obs_env()
        bad = copy.deepcopy(good); bad['coefficient_domain'] = 'Z'; self.rejects(bad)
        bad = copy.deepcopy(good); bad['witness_kind'] = 'rational-contraction'; self.rejects(bad)
        bad = copy.deepcopy(good); bad['witness_kind'] = 'weyl-invariant-kernel'; self.rejects(bad)
        bad = copy.deepcopy(good); bad['source_ids'] = ['D99-F99']; self.rejects(bad)
        bad = copy.deepcopy(good); bad['source_ids'] = []; self.rejects(bad)
        bad = copy.deepcopy(good); bad['hypotheses'] = []; self.rejects(bad)
        bad = copy.deepcopy(good); bad['payload']['rank'] = 1
        bad['payload_sha256'] = E.sha(bad['payload']); self.rejects(bad)
        bad = copy.deepcopy(good); bad['payload']['rank'] = 1; self.rejects(bad)       # hash mismatch
        bad = copy.deepcopy(good); bad['schema'] = 'v0'; self.rejects(bad)
        bad = copy.deepcopy(good); bad['model'] = TRI; bad['model_sha256'] = E.sha(TRI); self.rejects(bad)
        tri = copy.deepcopy(TRI); tri['field'] = 'Z'
        with self.assertRaises(ValueError):
            E.make('rational-contraction', tri, CS.build(TRI), ['x'], 'y', ['D05-F03'], 'test')


if __name__ == '__main__':
    unittest.main()
