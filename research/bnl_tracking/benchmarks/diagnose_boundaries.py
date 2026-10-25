"""Post-selection boundary diagnostics and prospectively declared extra comparators."""
from pathlib import Path
from datetime import datetime,timezone
import json,time,hashlib,sys
import qualification_bnl as q
import numpy as np
HERE=Path(__file__).resolve().parent
OUT=HERE/'boundary_diagnostics'

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def analytic(steps):
 r=q.load_source(10)
 for e in r:
  if isinstance(e,q.at.Quadrupole):e.PassMethod='QuadLinearPass'
  elif isinstance(e,q.at.Dipole):e.PassMethod='BendLinearPass'
  elif isinstance(e,q.at.Sextupole):e.NumIntSteps=steps
 return r

def main():
 if OUT.exists():raise FileExistsError('Keep diagnostics immutable')
 OUT.mkdir()
 old=json.loads((HERE/'qualification/protocol.json').read_text());confirmation=json.loads((HERE/'confirmation/protocol.json').read_text())
 points=[{'name':'backcheck_point41','index':41,'turns':512,'initial':np.array(old['heldout']['launches'])[:,41].tolist()},
         {'name':'confirmation_point48','index':48,'turns':256,'initial':np.array(confirmation['launches'])[:,48].tolist()}]
 protocol={'schema':'bnl-post-selection-boundary-diagnostics-v1','frozen_utc':datetime.now(timezone.utc).isoformat(),'post_selection':True,'points':points,
 'diagnostic_methods':['native40','native80','native160','native320','analytic20','analytic40'],
 'full128_backcheck_addendum':[{'method':'analytic20','repeats':1},{'method':'analytic40','repeats':1}],
 'full_backcheck_gate':'Unchanged: zero errors on native40/80 consensus labels; corepos<=1um andmomentum<=1urad. Newreferences are diagnostics, not substituted retrospectively.',
 'source_sha256':sha(q.SOURCE),'script_sha256':sha(Path(__file__)),'helper_sha256':sha(HERE/'qualification_bnl.py'),
 'scope':'Post-selection diagnostic and declared extension; no independentconfirmation or performanceheadline.'}
 q.write_json(OUT/'protocol.json',protocol)
 snapshot=OUT/'source_snapshot';snapshot.mkdir()
 for f in [Path(__file__),HERE/'qualification_bnl.py']:(snapshot/f.name).write_bytes(f.read_bytes())
 diagnostics=[]
 for name in protocol['diagnostic_methods']:
  steps=int(name.replace('native','').replace('analytic',''));r=analytic(steps)if name.startswith('analytic')else q.load_source(steps)
  for point in points:
   data,elapsed=q.track(r,np.array(point['initial'],dtype=float).reshape(6,1,order='F'),point['turns'])
   row={'method':name,'point':point['name'],'turns':point['turns'],'lost':bool(data['islost'][0]),'loss_turn':int(data['turn'][0])if data['islost'][0]else None,'loss_element':int(data['elem'][0])if data['islost'][0]else None,'seconds':elapsed}
   diagnostics.append(row);print(json.dumps(row),flush=True)
 q.write_json(OUT/'point_diagnostics.json',{'post_selection':True,'results':diagnostics})
 z=np.array(old['heldout']['launches'],order='F');r40=np.load(HERE/'qualification/native40/heldout_0.npz');r80=np.load(HERE/'qualification/native80/heldout_0.npz');agree=r40['islost']==r80['islost'];core=np.arange(32);rows=[]
 for steps in [20,40]:
  name=f'analytic{steps}';folder=OUT/name;folder.mkdir();start=time.perf_counter();r=analytic(steps);construction=time.perf_counter()-start;_,warm=q.track(r,np.zeros((6,1),order='F'),1)
  data,elapsed=q.track(r,z,512);np.savez_compressed(folder/'run_0.npz',**data)
  errors=np.flatnonzero(agree&(data['islost']!=r80['islost'])).tolist();valid=not np.any(data['islost'][core])and not np.any(r80['islost'][core])
  pos=float(np.max(abs(data['rout'][[0,2]][:,core]-r80['rout'][[0,2]][:,core])))if valid else None
  mom=float(np.max(abs(data['rout'][[1,3]][:,core]-r80['rout'][[1,3]][:,core])))if valid else None
  passed=bool(valid and not errors and pos<=1e-6 and mom<=1e-6)
  row={'method':name,'qualified':passed,'label_error_indices':errors,'core_position_max_abs_m':pos,'core_momentum_max_abs_normalized':mom,'tracking_seconds':[elapsed],'median_tracking_seconds':elapsed,'native_construction_seconds':construction,'warmup_seconds':warm,'first_workload_seconds':elapsed+construction+warm,'fallback_counts':[0],'survivors':int((~data['islost']).sum()),'post_selection':True,'repeats':1}
  q.write_json(folder/'result.json',row);rows.append(row);print('FULL',json.dumps(row),flush=True)
 require_sources=sha(Path(__file__))==protocol['script_sha256']and sha(HERE/'qualification_bnl.py')==protocol['helper_sha256'];assert require_sources
 candidate=json.loads((HERE/'backcheck/fused40_s4/result.json').read_text());eligible=[r for r in rows if r['qualified']];best=min(eligible,key=lambda r:r['first_workload_seconds'])if eligible else None
 report={'status':'passed_audit','post_selection':True,'sources_unchanged':True,'point_diagnostics':diagnostics,'additional_backcheck':rows,'best_qualified_additional_ordinary':None if best is None else best['method'],'qualified_first_workload_gain':None if best is None or not candidate['qualified']else best['first_workload_seconds']/candidate['first_workload_seconds'],'scope':'Post-selection diagnostic and comparator extension; does not revise originalconsensus labels/gates or become independentconfirmation.'}
 q.write_json(OUT/'diagnostic_audit.json',report)

if __name__=='__main__':main()
