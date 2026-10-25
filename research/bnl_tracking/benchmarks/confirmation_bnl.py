"""Independent frozen confirmation. Run only after the exploratory audit completes."""
from pathlib import Path
from datetime import datetime,timezone
import os,sys,json,time,hashlib,importlib.util
for key in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS']:os.environ[key]='1'
import qualification_bnl as q
import numpy as np
BASE=Path(__file__).resolve().parent
OUT=BASE/'confirmation'
LAB=Path('/workspace/scratch/9c6a3d2e42ab/bnl_acceleration_lab')
METHODS=[('native2',2,None,3),('native4',4,None,3),('native10',10,None,3),('native20',20,None,1),('native40',40,None,1),('native80',80,None,1),('fused10',10,None,3),('fused2',10,2,3),('fused4',10,4,3),('analytic10',10,10,3),('analytic2',10,2,3),('analytic4',10,4,3),('fused40_s10',40,10,3),('fused40_s2',40,2,3),('fused40_s4',40,4,3)]

def main():
 if OUT.exists():raise FileExistsError('Confirmation is immutable; refuse existing output')
 OUT.mkdir()
 rng=np.random.default_rng(20261024);z=np.zeros((6,64),order='F')
 z[0,:16]=rng.uniform(-.00025,.00025,16);z[2,:16]=rng.uniform(-.0000625,.0000625,16)
 z[0,16:]=rng.uniform(-.008,.008,48);z[2,16:]=rng.uniform(0,.002,48)
 paths=[Path(__file__),BASE/'qualification_bnl.py',LAB/'compiler.py',LAB/'compiler_fused.py',LAB/'FixedDeltaBlockPass.c',LAB/'build_fused.py',LAB/'fused_build_receipt.json',LAB/'plugin_build_timing.json']
 snapshots=OUT/'source_snapshot';snapshots.mkdir()
 hashes={}
 for path in paths:
  data=path.read_bytes();hashes[str(path)]=q.digest_bytes(data);(snapshots/path.name).write_bytes(data)
 protocol={'schema':'bnl-independent-confirmation-v1','frozen_utc':datetime.now(timezone.utc).isoformat(),'seed':20261024,'turns':256,'launches':z.tolist(),'core_indices':list(range(16)),
 'source_sha256':q.digest_bytes(q.SOURCE.read_bytes()),'source_path':str(q.SOURCE),'source_hashes':hashes,
 'methods':[{'id':n,'native_steps':s,'sext_steps':ss,'repeats':r}for n,s,ss,r in METHODS],
 'gate':{'label_errors_allowed_where_native40_and80_agree':0,'core_position_max_abs_m':1e-6,'core_momentum_max_abs_normalized':1e-6},
 'physics':'3GeV fixed delta0, RF/radiation/errors/collective effects off; imported old BNL public CB65pm demo; transverse readout only.',
 'policy':'No algorithm or threshold retuning. Sequential methods. Source hashes checked before and after. Native2/4 and built-in analytic QuadLinearPass/BendLinearPass withsext2/4/10 are mandatory competitors. Fused40_s2/s4/s10 preserve40-step linear bodies. Construction, warmup, fallback and plugin build cost retained separately.'}
 q.write_json(OUT/'protocol.json',protocol)
 module_path=LAB/'compiler_fused.py';sys.path.insert(0,str(LAB))
 spec=importlib.util.spec_from_file_location('bnl_fused_confirmation',module_path);module=importlib.util.module_from_spec(spec);sys.modules['bnl_fused_confirmation']=module;spec.loader.exec_module(module)
 results=[]
 for name,steps,sext,repeats in METHODS:
  folder=OUT/name;folder.mkdir();start=time.perf_counter();native=q.load_source(steps);
  if name.startswith('analytic'):
   for element in native:
    if isinstance(element,q.at.Quadrupole):element.PassMethod='QuadLinearPass'
    elif isinstance(element,q.at.Dipole):element.PassMethod='BendLinearPass'
    elif isinstance(element,q.at.Sextupole):element.NumIntSteps=sext
  native_seconds=time.perf_counter()-start
  receipt=None;compile_seconds=0.;r=native
  if name.startswith('fused'):
   start=time.perf_counter();r,receipt=module.compile_ring(native,dp=0,sext_steps=sext,guards=True);compile_seconds=time.perf_counter()-start
   q.write_json(folder/'compiler_receipt.json',receipt)
  _,warm=q.track(r,np.zeros((6,1),order='F'),1)
  times=[];fallback=[];first=None
  for rep in range(repeats):
   if receipt is None:
    data,elapsed=q.track(native,z,256);cost={'seconds':elapsed,'fallback_particles':0}
   else:
    rout,loss,cost=module.track_with_fallback(native,r,receipt,z.copy(order='F'),256)
    data={'rout':np.array(rout),'islost':np.array(loss['islost']),'turn':np.array(loss['turn']),'elem':np.array(loss['elem'])};elapsed=cost['seconds']
   np.savez_compressed(folder/f'run_{rep}.npz',**data);q.write_json(folder/f'cost_{rep}.json',cost)
   if first is None:first=data
   else:
    assert np.array_equal(first['islost'],data['islost'])
    assert np.allclose(first['rout'],data['rout'],rtol=0,atol=0,equal_nan=True)
   times.append(elapsed);fallback.append(cost['fallback_particles'])
  result={'method':name,'native_steps':steps,'sext_steps':sext,'elements':len(r),'native_construction_seconds':native_seconds,'compile_seconds':compile_seconds,'warmup_seconds':warm,'tracking_seconds':times,'fallback_counts':fallback,'median_tracking_seconds':float(np.median(times)),'survivors':int((~first['islost']).sum())}
  q.write_json(folder/'result.json',result);results.append(result)
  print(json.dumps(result),flush=True)
 for path in paths:assert q.digest_bytes(path.read_bytes())==hashes[str(path)]
 q.write_json(OUT/'raw_summary.json',{'status':'completed','results':results,'source_hashes_unchanged':True})
 audit(protocol,results)

def audit(protocol,results):
 r40=np.load(OUT/'native40/run_0.npz');r80=np.load(OUT/'native80/run_0.npz');agree=r40['islost']==r80['islost'];core=np.array(protocol['core_indices']);rows=[]
 for result in results:
  name=result['method'];d=np.load(OUT/name/'run_0.npz');errors=np.flatnonzero(agree&(d['islost']!=r80['islost']))
  valid=not np.any(d['islost'][core])and not np.any(r80['islost'][core])
  position=float(np.max(abs(d['rout'][[0,2]][:,core]-r80['rout'][[0,2]][:,core])))if valid else None
  momentum=float(np.max(abs(d['rout'][[1,3]][:,core]-r80['rout'][[1,3]][:,core])))if valid else None
  qualified=valid and not len(errors)and position<=1e-6 and momentum<=1e-6
  row={**result,'qualified':bool(qualified),'label_error_indices':errors.tolist(),'core_position_max_abs_m':position,'core_momentum_max_abs_normalized':momentum,
       'construction_and_warmup_seconds':result['native_construction_seconds']+result['compile_seconds']+result['warmup_seconds']}
  row['first_workload_seconds']=row['median_tracking_seconds']+row['construction_and_warmup_seconds'];rows.append(row)
 build_timing=json.loads((LAB/'plugin_build_timing.json').read_text())
 build_seconds=build_timing.get('seconds',build_timing.get('elapsed_seconds',build_timing.get('build_seconds')))
 if build_seconds is None:raise ValueError('Build time missing')
 for row in rows:
  row['plugin_build_seconds_charged']=build_seconds if row['method'].startswith('fused')else 0.
  row['first_workload_seconds']+=row['plugin_build_seconds_charged']
 qualified_native=[r for r in rows if r['qualified']and r['method'].startswith(('native','analytic'))]
 best=min(qualified_native,key=lambda r:r['first_workload_seconds'])if qualified_native else None
 refcost=sum(sum(r['tracking_seconds'])+r['construction_and_warmup_seconds']for r in rows if r['method']in ['native40','native80'])
 build=json.loads((LAB/'fused_build_receipt.json').read_text());build_seconds=float(build_seconds)
 for row in rows:
  row['gain_vs_fastest_qualified_native_first_workload']=None if best is None else best['first_workload_seconds']/row['first_workload_seconds']
  saving=None if best is None else best['median_tracking_seconds']-row['median_tracking_seconds']
  row['conditional_break_even_fresh_workloads']=None if saving is None or saving<=0 else (refcost+row['construction_and_warmup_seconds'])/saving
 report={'status':'passed_audit','protocol_sha256':q.digest_bytes((OUT/'protocol.json').read_bytes()),'reference_agreement_points':int(agree.sum()),'reference_unresolved_indices':np.flatnonzero(~agree).tolist(),'reference_generation_seconds':refcost,'plugin_build_receipt':build,'plugin_build_seconds':build_seconds,'plugin_build_timing_receipt':build_timing,'fastest_qualified_native':None if best is None else best['method'],'results':rows,
 'scope':'One independent frozen public-model confirmation. No operational machine/6D/collective claim. Timing repeats are not distinct industrial tasks; break-even is conditional and cache-equivalent repeated queries do not establish amortization. Plugin build and reference generation are separate charges.',
 'industrial_tenfold_established':False}
 q.write_json(OUT/'confirmation_audit.json',report)
 print('AUDIT',json.dumps({'reference_agreement_points':int(agree.sum()),'reference_unresolved_indices':np.flatnonzero(~agree).tolist(),'fastest_qualified_native':report['fastest_qualified_native'],'qualification':[{'method':r['method'],'qualified':r['qualified'],'errors':r['label_error_indices'],'gain':r['gain_vs_fastest_qualified_native_first_workload']}for r in rows]}),flush=True)

if __name__=='__main__':main()
