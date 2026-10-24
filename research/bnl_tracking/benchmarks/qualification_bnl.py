"""Frozen BNL-model qualification. Reference disagreement stays unresolved."""
from pathlib import Path
import sys,time,json,hashlib,os,importlib.util
from datetime import datetime,timezone
for k in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='1'
sys.path.insert(0,'/workspace/scratch/9c6a3d2e42ab/beam_literature_runtime')
import at,numpy as np
BASE=Path(__file__).resolve().parent
SOURCE=Path('/workspace/scratch/9c6a3d2e42ab/bnl_fit/demo/nsls2cb65pm.lte')
COMPILER=Path('/workspace/scratch/9c6a3d2e42ab/bnl_acceleration_lab/compiler.py')
OUT=BASE/'qualification'
METHODS=[('native10',10,None),('native20',20,None),('native40',40,None),('native80',80,None),('compressed10',10,None),('compressed2',10,2),('compressed4',10,4),('native2',2,None),('native4',4,None)]

def digest_bytes(data):return hashlib.sha256(data).hexdigest()
def write_json(path,value):path.write_text(json.dumps(value,indent=2,allow_nan=False)+'\n')
def load_source(steps):
 r=at.load_elegant(SOURCE,energy=3e9).disable_6d(copy=True)
 for e in r:
  if hasattr(e,'NumIntSteps'):e.NumIntSteps=steps
 return r

def track(r,z,turns):
 start=time.perf_counter()
 _,p,d=r.track(z.copy(order='F'),nturns=turns,refpts=[],losses=True,keep_lattice=False,omp_num_threads=1)
 elapsed=time.perf_counter()-start;l=d['loss_map']
 return {'rout':np.array(p['rout']),'islost':np.array(l['islost']),'turn':np.array(l['turn']),'elem':np.array(l['elem'])},elapsed

def create_protocol():
 rng=np.random.default_rng(20261023)
 cal=np.zeros((6,64),order='F');cal[0]=np.repeat(np.linspace(-.008,.008,8),8);cal[2]=np.tile(np.linspace(0,.002,8),8)
 held=np.zeros((6,128),order='F');held[0,:32]=rng.uniform(-.00025,.00025,32);held[2,:32]=rng.uniform(-.0000625,.0000625,32)
 held[0,32:]=rng.uniform(-.008,.008,96);held[2,32:]=rng.uniform(0,.002,96)
 protocol={'schema':'bnl-fixed-energy-qualification-v1','frozen_utc':datetime.now(timezone.utc).isoformat(),
 'source':str(SOURCE),'source_sha256':digest_bytes(SOURCE.read_bytes()),'energy_eV':3e9,'seed':20261023,
 'physics':{'RF':False,'radiation':False,'space_charge':False,'errors':False,'additional_mechanical_apertures':False,'delta':0.0},
 'compiler_path':str(COMPILER),'compiler_contract':'compile_ring(ring,dp=0,sext_steps=None,guards=True) returns ring and stats; native fallback for uncertain guard losses.',
 'calibration':{'turns':128,'launches':cal.tolist()},'heldout':{'turns':512,'core_indices':list(range(32)),'launches':held.tolist()},
 'methods':[{'id':n,'native_steps':s,'compressed_sext_steps':ss,'repeats':1 if n in ('native40','native80')else 2}for n,s,ss in METHODS],
 'gate':{'labels':'Zero candidate disagreements where native40 and native80 agree; all reference disagreements retained unresolved.',
         'core_position_max_abs_m':1e-6,'core_momentum_max_abs_normalized':1e-6,
         'readout':'First4coordinates only; no longitudinal-path equivalence.'},
 'cost':'Measure native construction, compiler construction, warmup, tracking, and fallback; qualification reference generation separate; report amortization break-even.'}
 return protocol

def main():
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--phase',choices=['native','compiled','fused','audit'],required=True);args=p.parse_args()
 if not OUT.exists():
  OUT.mkdir();write_json(OUT/'protocol.json',create_protocol())
 protocol=json.loads((OUT/'protocol.json').read_text())
 require_sha=digest_bytes(SOURCE.read_bytes());assert require_sha==protocol['source_sha256']
 methods=[m for m in protocol['methods']if (not m['id'].startswith('compressed'))==(args.phase=='native')]
 if args.phase=='fused':methods=json.loads((OUT/'protocol_addendum_fused.json').read_text())['variants']
 if args.phase=='audit':return audit(protocol)
 for method in methods:
  name=method['id'];destination=OUT/name
  if destination.exists():raise FileExistsError(name+' already exists; retain outputs')
  destination.mkdir();started=time.perf_counter();r=load_source(method['native_steps']);native_construction=time.perf_counter()-started
  compiler_stats=None;compiler_seconds=0
  if name.startswith(('compressed','fused')):
   compiler_path=COMPILER.with_name('compiler_fused.py')if name.startswith('fused')else COMPILER
   if not compiler_path.exists():raise FileNotFoundError('Compiler not ready')
   source_hash=digest_bytes(compiler_path.read_bytes());sys.path.insert(0,str(compiler_path.parent))
   spec=importlib.util.spec_from_file_location('bnl_compiler',compiler_path);module=importlib.util.module_from_spec(spec);sys.modules['bnl_compiler']=module;spec.loader.exec_module(module)
   native=r;started=time.perf_counter();r,compiler_stats=module.compile_ring(r,dp=0,sext_steps=method['compressed_sext_steps'],guards=True);compiler_seconds=time.perf_counter()-started
   write_json(destination/'compiler_receipt.json',compiler_stats)
  else:source_hash=None
  _,warmup=track(r,np.zeros((6,1),order='F'),1)
  result={'method':name,'elements':len(r),'native_construction_seconds':native_construction,'compiler_seconds':compiler_seconds,
          'compiler_sha256':source_hash,'compiler_stats':None if compiler_stats is None else {k:v for k,v in compiler_stats.items()if k not in ['blocks','native_index_map']},'warmup_seconds':warmup,'scenarios':{}}
  for scenario in ['calibration','heldout']:
   z=np.array(protocol[scenario]['launches'],order='F');times=[];runs=[]
   for rep in range(method['repeats']):
    if name.startswith(('compressed','fused')):
     rout,loss,cost=module.track_with_fallback(native,r,compiler_stats,z.copy(order='F'),protocol[scenario]['turns'])
     data={'rout':np.array(rout),'islost':np.array(loss['islost']),'turn':np.array(loss['turn']),'elem':np.array(loss['elem'])}
     elapsed=cost['seconds']
    else:data,elapsed=track(r,z,protocol[scenario]['turns']);cost={'fallback_particles':0,'guard_uncertain_indices':[]}
    times.append(elapsed);runs.append(data)
    write_json(destination/f'{scenario}_{rep}_cost.json',cost)
    np.savez_compressed(destination/f'{scenario}_{rep}.npz',**data)
   for data in runs[1:]:
    assert np.array_equal(data['islost'],runs[0]['islost'])
    assert np.allclose(data['rout'],runs[0]['rout'],rtol=0,atol=0,equal_nan=True)
   result['scenarios'][scenario]={'seconds':times,'median_seconds':float(np.median(times)),
          'survivors':int(np.sum(~runs[0]['islost'])),'lost':int(np.sum(runs[0]['islost']))}
   write_json(destination/'result.json',result)
   print(json.dumps({'method':name,'scenario':scenario,**result['scenarios'][scenario]}),flush=True)
  write_json(destination/'result.json',result)

def audit(protocol):
 reference40=np.load(OUT/'native40/heldout_0.npz');reference80=np.load(OUT/'native80/heldout_0.npz')
 agree=reference40['islost']==reference80['islost'];core=np.array(protocol['heldout']['core_indices'])
 rows=[]
 for method in protocol['methods']+json.loads((OUT/'protocol_addendum_fused.json').read_text())['variants']:
  name=method['id'];folder=OUT/name
  if not(folder/'result.json').exists():continue
  result=json.loads((folder/'result.json').read_text());data=np.load(folder/'heldout_0.npz')
  disagreements=np.flatnonzero(agree&(data['islost']!=reference80['islost']))
  core_valid=not np.any(data['islost'][core])and not np.any(reference80['islost'][core])
  if core_valid:
   position=float(np.max(abs(data['rout'][[0,2]][:,core]-reference80['rout'][[0,2]][:,core])))
   momentum=float(np.max(abs(data['rout'][[1,3]][:,core]-reference80['rout'][[1,3]][:,core])))
  else:position=None;momentum=None
  gate=core_valid and len(disagreements)==0 and position<=1e-6 and momentum<=1e-6
  fallback=[]
  for rep in range(method['repeats']):
   cost_path=folder/f'heldout_{rep}_cost.json'
   if cost_path.exists():fallback.append(json.loads(cost_path.read_text())['fallback_particles'])
   elif name.startswith('native'):fallback.append(0)
   else:raise FileNotFoundError(cost_path)
  propagation=result['scenarios']['heldout']['median_seconds']
  construction=result['native_construction_seconds']+result['compiler_seconds']+result['warmup_seconds']
  rows.append({'method':name,'qualified':bool(gate),'label_errors_on_reference_agreement':disagreements.tolist(),
    'core_position_max_abs_m':position,'core_momentum_max_abs_normalized':momentum,
    'reference_unresolved_indices':np.flatnonzero(~agree).tolist(),'reference_agreement_points':int(agree.sum()),
    'heldout_seconds':result['scenarios']['heldout']['seconds'],'median_tracking_with_fallback_seconds':propagation,
    'construction_and_warmup_seconds':construction,'one_workload_seconds':propagation+construction,
    'fallback_particles_each_repeat':fallback,'compiled_elements':result['elements'],
    'scope':'Frozen finite test only; unresolved reference labels retained. No uniform phase-space or operational machine guarantee.'})
 qualification_cost=sum(json.loads((OUT/name/'result.json').read_text())['native_construction_seconds']+
     sum(sum(v['seconds'])for v in json.loads((OUT/name/'result.json').read_text())['scenarios'].values())
     for name in ['native40','native80'])
 qualified=[row for row in rows if row['qualified']and row['method'].startswith('native')]
 best_native=min(qualified,key=lambda row:row['one_workload_seconds'])if qualified else None
 for row in rows:
  row['gain_vs_fastest_qualified_native_one_workload']=None if best_native is None else best_native['one_workload_seconds']/row['one_workload_seconds']
  saving=None if best_native is None else best_native['median_tracking_with_fallback_seconds']-row['median_tracking_with_fallback_seconds']
  row['conditional_qualification_amortization_workloads']=None if saving is None or saving<=0 else (qualification_cost+row['construction_and_warmup_seconds'])/saving
 report={'status':'passed_audit','protocol_sha256':digest_bytes((OUT/'protocol.json').read_bytes()),
    'addendum_sha256':digest_bytes((OUT/'protocol_addendum_fused.json').read_bytes()),
    'reference_agreement_points':int(agree.sum()),'reference_unresolved_indices':np.flatnonzero(~agree).tolist(),
    'qualification_reference_generation_seconds':qualification_cost,'fastest_qualified_native':None if best_native is None else best_native['method'],
    'results':rows,'timing_warning':'Native references and candidates were run on shared host concurrently. Timing-only refresh is required before a headline performance ratio.',
    'amortization_warning':'Conditional arithmetic only. Timing repetitions are not new industrial tasks; cache-equivalent repeated queries do not establish amortization.',
    'industrial_tenfold_established':False}
 write_json(OUT/'qualification_audit.json',report)
 for row in rows:print(json.dumps(row),flush=True)
 print('REFERENCE',int(agree.sum()),'agreed',len(np.flatnonzero(~agree)),'unresolved',flush=True)

if __name__=='__main__':main()
