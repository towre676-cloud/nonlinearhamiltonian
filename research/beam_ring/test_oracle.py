import copy
import json
from pathlib import Path
import unittest
from unittest.mock import patch
import numpy as np
import oracle
from verify_pilot import certificate_binding
from certificates.grid_bounds import certify

HERE=Path(__file__).resolve().parent


class FakeRing:
    def __init__(self):self.fail=False
    def track(self,z,nturns,**kwargs):
        if self.fail:raise RuntimeError('fixture failure')
        lost=z[0]>0
        return None,None,{'loss_map':{'islost':lost,'turn':np.zeros(len(lost),int),
                                     'elem':np.zeros(len(lost),int)}}


class OracleTests(unittest.TestCase):
    def setUp(self):
        self.protocol=json.loads((HERE/'protocol.json').read_text())

    def create(self,stage='learning'):
        with patch.object(oracle,'load_runtime',return_value=(None,np)):
            return oracle.RingOracle(self.protocol,stage=stage)

    def test_protocol_identity_and_physics_fail_closed(self):
        for mutate in [lambda p:p.update(lattice_sha256='0'*64),
                       lambda p:p['physics'].update(rf=True),
                       lambda p:p['stages']['learning']['launch_sets'][0]['coordinates'][0].append(0),
                       lambda p:p['stages']['learning']['launch_sets'][0]['coordinates'][0].__setitem__(0,float('nan'))]:
            p=copy.deepcopy(self.protocol);mutate(p)
            with self.assertRaises((ValueError,KeyError)):oracle.validated_protocol(p)

    def test_protocol_detaches_caller_mutation(self):
        instance=self.create();before=copy.deepcopy(instance.protocol)
        self.protocol['designs'][0]['strengths'][0]=1234
        self.assertEqual(instance.protocol,before)
        instance.protocol['designs'][0]['strengths'][0]=1234
        with self.assertRaises(ValueError):instance.query([(0,0,0)])

    def test_requests_atomic_cache_and_copy(self):
        instance=self.create();ring=FakeRing();instance._ring=lambda d:ring
        with self.assertRaises(ValueError):instance.query([(0,0,1),(0,0,-1)])
        self.assertEqual(instance.calls,[])
        for bad in [(0,True,1),(0,0,9999),(0,99,0)]:
            with self.assertRaises(ValueError):instance.query([bad])
        rows=instance.query([(0,0,0),(0,0,0)])
        self.assertEqual(len(instance.events),1)
        rows[0]['survived']=False
        self.assertTrue(instance.query([(0,0,0)])[0]['survived'])
        self.assertEqual(instance.ledger()['physical_points'],1)

    def test_zero_based_loss_and_stage_separation(self):
        instance=self.create();instance._ring=lambda d:FakeRing()
        grid=self.protocol['stages']['learning']['launch_sets'][0]
        launch=next(i for i,z in enumerate(grid['coordinates'])if z[0]>0)
        row=instance.query([(0,0,launch)])[0]
        self.assertFalse(row['survived']);self.assertEqual(row['survival_fraction'],0)
        self.assertEqual(self.create('validation').cache,{})

    def test_failed_calls_charged(self):
        instance=self.create();ring=FakeRing();ring.fail=True;instance._ring=lambda d:ring
        with self.assertRaises(RuntimeError):instance.query([(0,0,0)])
        self.assertEqual(instance.events,[])
        self.assertEqual(instance.failed_calls[0]['points'],1)
        self.assertGreaterEqual(instance.physical_tracking_seconds,0)

    def test_recertified_wrong_objective_rejected(self):
        path=HERE/'results/pilot/full_grid/objective_00_certificate.json'
        record=json.loads(path.read_text())
        certificate_binding(record,self.protocol,0)
        record['manifest']['weights']['cell_0000']='2'
        record['certificate']=certify(record['manifest'],record['events'])
        with self.assertRaises(ValueError):certificate_binding(record,self.protocol,0)


if __name__=='__main__':unittest.main()
