"""Post-selection longer-horizon backcheck; not an independent confirmation."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,os,sys,json,time,hashlib,importlib.util
for key in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS']:os.environ[key]='1'
import qualification_bnl as q
import numpy as np
HERE=Path(__file__).resolve().parent

def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--source',type=Path,default=q.SOURCE)
 p.add_argument('--compiler-dir',type=Path,default=Path('/workspace/scratch/9c6a3d2e42ab/bnl_acceleration_lab'))
 p.add_argument('--reference-dir',type=Path,default=HERE/'qualification')
 p.add_argument('--output',type=Path,default=HERE/'backcheck')
 args=p.parse_args();q.SOURCE=args.source;out=args.output
 if out.exists():raise FileExistsError('Backcheck output is immutable')
 out.mkdir();lab=args.compiler_dir
 original=json.loads((args.reference_dir/'protocol.json').read_text());z=np.array(original['heldout']['launches'],order='F')
 assert z.shape==(6,128)
 source_paths=[Path(__file__),HERE/'qualification_bnl.py',lab/'compiler.py',lab/'compiler_fused.py',lab/'FixedDeltaBlockPass.c',lab/'build_fused.py',lab/'fused_build_receipt.json',lab/'plugin_build_timing.json']
 sources={str(path):q.digest_bytes(path.read_bytes())for path in source_paths};snapshot=out/'source_snapshot';snapshot.mkdir()
 for path in source_paths:(snapshot/path.name).write_bytes(path.read_bytes())
 reference_paths={str(args.reference_dir/name/'heldout_0.npz'):q.digest_bytes((args.reference_dir/name/'heldout_0.npz').read_bytes())for name in ['native40','native80']}
 protocol={'schema':'bnl-post-selection-backcheck-v1','frozen_utc':datetime.now(timezone.utc).isoformat(),'post_selection':True,'not_independent_confirmation':True,
 'selection_source':'Previously completed64pointseed20261024confirmation; this backcheck reuses original128point qualification launches.',
 'source_sha256':q.digest_bytes(args.source.read_bytes()),'launches':z.tolist(),'turns':512,'core_indices':list(range(32)),
 'methods':[{'id':'analytic10','repeats':3},{'id':'fused40_s4','repeats':3}],
 'gate':{'label_errors_allowed_where_native40and80_agree':0,'core_position_max_abs_m':1e-6,'core_momentum_max_abs_normalized':1e-6},
 'reference_files':reference_paths,'source_hashes':sources,'physics':'Fixed delta0/noRF/no radiation/noerrors/no collective physics; first4coordinates only.'}
 q.write_json(out/'protocol.json',protocol)
 sys.path.insert(0,str(lab));spec=importlib.util.spec_from_file_location('bnl_fused_backcheck',lab/'compiler_fused.py');module=importlib.util.module_from_spec(spec);sys.modules['bnl_fused_backcheck']=module;spec.loader.exec_module(module)
 build=json.loads((lab/'plugin_build_timing.json').read_text())['build_seconds'];rows=[]
 ref40=np.load(args.reference_dir/'native40/heldout_0.npz');ref80=np.load(args.reference_dir/'native80/heldout_0.npz');agree=ref40['islost']==ref80['islost'];core=np.array(protocol['core_indices'])
 for name in ['analytic10','fused40_s4']:
  folder=out/name;folder.mkdir();started=time.perf_counter();native=q.load_source(10 if name=='analytic10'else 40)
  if name=='analytic10':
   for e in native:
    if isinstance(e,q.at.Quadrupole):e.PassMethod='QuadLinearPass'
    elif isinstance(e,q.at.Dipole):e.PassMethod='BendLinearPass'
    elif isinstance(e,q.at.Sextupole):e.NumIntSteps=10
  construction=time.perf_counter()-started;r=native;receipt=None;compilation=0
  if name=='fused40_s4':
   started=time.perf_counter();r,receipt=module.compile_ring(native,dp=0,sext_steps=4,guards=True);compilation=time.perf_counter()-started;q.write_json(folder/'compiler_receipt.json',receipt)
  _,warm=q.track(r,np.zeros((6,1),order='F'),1);times=[];fallback=[];first=None
  for repeat in range(3):
   if receipt is None:data,elapsed=q.track(native,z,512);cost={'seconds':elapsed,'fallback_particles':0}
   else:
    rout,loss,cost=module.track_with_fallback(native,r,receipt,z.copy(order='F'),512);elapsed=cost['seconds'];data={'rout':np.array(rout),'islost':np.array(loss['islost']),'turn':np.array(loss['turn']),'elem':np.array(loss['elem'])}
   np.savez_compressed(folder/f'run_{repeat}.npz',**data);q.write_json(folder/f'cost_{repeat}.json',cost);times.append(elapsed);fallback.append(cost['fallback_particles'])
   if first is None:first=data
   else:assert np.array_equal(first['islost'],data['islost'])and np.allclose(first['rout'],data['rout'],rtol=0,atol=0,equal_nan=True)
  valid=not np.any(first['islost'][core])and not np.any(ref80['islost'][core]);errors=np.flatnonzero(agree&(first['islost']!=ref80['islost']))
  position=float(np.max(abs(first['rout'][[0,2]][:,core]-ref80['rout'][[0,2]][:,core])))if valid else None
  momentum=float(np.max(abs(first['rout'][[1,3]][:,core]-ref80['rout'][[1,3]][:,core])))if valid else None
  qualified=valid and not len(errors)and position<=1e-6 and momentum<=1e-6
  first_cost=float(np.median(times))+construction+compilation+warm+(build if name=='fused40_s4'else 0.)
  row={'method':name,'qualified':bool(qualified),'tracking_seconds':times,'median_tracking_seconds':float(np.median(times)),'native_construction_seconds':construction,'compilation_seconds':compilation,'warmup_seconds':warm,'plugin_build_seconds_charged':build if name=='fused40_s4'else 0.,'first_workload_seconds':first_cost,'fallback_counts':fallback,'label_error_indices':errors.tolist(),'core_position_max_abs_m':position,'core_momentum_max_abs_normalized':momentum,'survivors':int((~first['islost']).sum())}
  q.write_json(folder/'result.json',row);rows.append(row);print(json.dumps(row),flush=True)
 for path,sha in sources.items():assert q.digest_bytes(Path(path).read_bytes())==sha
 for path,sha in reference_paths.items():assert q.digest_bytes(Path(path).read_bytes())==sha
 baseline,candidate=rows
 report={'status':'passed_audit','post_selection':True,'not_independent_confirmation':True,'protocol_sha256':q.digest_bytes((out/'protocol.json').read_bytes()),'reference_agreement_points':int(agree.sum()),'reference_unresolved_indices':np.flatnonzero(~agree).tolist(),'sources_unchanged':True,'results':rows,
 'qualified_gain_first_workload':baseline['first_workload_seconds']/candidate['first_workload_seconds']if baseline['qualified']and candidate['qualified']else None,
 'qualified_gain_tracking':baseline['median_tracking_seconds']/candidate['median_tracking_seconds']if baseline['qualified']and candidate['qualified']else None,
 'scope':'Post-selection backcheck against already generated high-resolution reference, not new independent validation. Referencegeneration,installation,coldstartup/reportserialization excluded from first-workload timing; build andfallback charged. No industrialtenfold claim.'}
 q.write_json(out/'backcheck_audit.json',report);print('AUDIT',json.dumps(report),flush=True)

if __name__=='__main__':main()
