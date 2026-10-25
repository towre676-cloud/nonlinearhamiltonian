"""Replay the exact component and compact physical diagnostics; no new PIC."""
from pathlib import Path
import argparse,hashlib,io,json,unittest


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    here=Path(__file__).resolve().parent
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--exact-only',action='store_true')
    args=parser.parse_args()
    suite=unittest.TestLoader().discover(str(here),pattern='test_*.py')
    log=io.StringIO();out=unittest.TextTestRunner(stream=log,verbosity=1).run(suite)
    if not out.wasSuccessful():
        raise ValueError(log.getvalue())
    report={'status':'passed','exact_unittest_cases':out.testsRun,
            'random_scalar_clouds':240,'random_vector_clouds':90,
            'arithmetic':'Python arbitrary precision integers/Fraction',
            'test_failures':len(out.failures),'test_errors':len(out.errors),
            'physical_replay':None,'new_particle_solver_calls':0,
            'conditional_predictor_force_premises_verified':False,
            'industrial_speedup_established':False}
    if not args.exact_only:
        from physical_diagnostics import diagnose
        source=here/'physical_inputs.json';data=json.loads(source.read_text())
        saved=json.loads((here/'physical_receipt.json').read_text())
        if hashlib.sha256(source.read_bytes()).hexdigest()!=saved['input_sha256']:
            raise ValueError('physical input source mismatch')
        rows=[diagnose(row)for row in data['rows']]
        if len(rows)!=63 or len(saved['rows'])!=63 or len({row['case_id']for row in rows})!=63 or any(not p['norm_bound_numerically_satisfied']for row in rows for p in row['planes']):
            raise ValueError('physical diagnostic replay failed')
        for old,new in zip(saved['rows'],rows):
            if old['case_id']!=new['case_id']:
                raise ValueError('case order mismatch')
            for op,np in zip(old['planes'],new['planes']):
                for key in ['own_plane_residual_force_variance_per_m2','signed_ug_per_m','emittance_before_m','emittance_after_m']:
                    if abs(op[key]-np[key])>1e-11*max(abs(op[key]),abs(np[key]),1e-30):
                        raise ValueError('stored/recomputed numeric result mismatch')
        report['physical_replay']={'input_sha256':saved['input_sha256'],'cases':63,'plane_kicks':126,
                                   'scope':'Retrospective numeric diagnostics; no physical enclosure or predictive coverage.'}
    files=[p for p in here.iterdir()if p.suffix in ['.py','.md']or p.name=='physical_inputs.json']
    report['source_sha256']={p.name:hashlib.sha256(p.read_bytes()).hexdigest()for p in sorted(files)}
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k]for k in ['status','exact_unittest_cases','physical_replay','new_particle_solver_calls']},indent=2))


if __name__=='__main__':main()
