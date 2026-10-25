"""Portable offline check of stored BNL confirmation/backcheck arrays and gates."""
from pathlib import Path
import argparse,hashlib,json
import numpy as np


def require(value,message):
 if not value:raise ValueError(message)

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def load_arrays(path):
 with np.load(path,allow_pickle=False)as f:return {k:f[k]for k in f.files}

def inspect_gate(data,ref40,ref80,core):
 agree=ref40['islost']==ref80['islost'];core=np.array(core)
 require(data['rout'].shape==ref80['rout'].shape,'state shape')
 errors=np.flatnonzero(agree&(data['islost']!=ref80['islost'])).tolist()
 valid=not np.any(data['islost'][core])and not np.any(ref80['islost'][core])
 position=float(np.max(abs(data['rout'][[0,2]][:,core]-ref80['rout'][[0,2]][:,core])))if valid else None
 momentum=float(np.max(abs(data['rout'][[1,3]][:,core]-ref80['rout'][[1,3]][:,core])))if valid else None
 gate=bool(valid and not errors and position<=1e-6 and momentum<=1e-6)
 return gate,errors,position,momentum,np.flatnonzero(~agree).tolist()

def audit(root,name,report_name,reference_paths):
 folder=root/name;protocol=json.loads((folder/'protocol.json').read_text());report=json.loads((folder/report_name).read_text())
 require(report['protocol_sha256']==sha(folder/'protocol.json'),'protocol hash')
 for original,expected in protocol['source_hashes'].items():
  snapshot=folder/'source_snapshot'/Path(original).name
  require(sha(snapshot)==expected,'executed source snapshot '+str(snapshot))
 ref40,ref80=[load_arrays(root/path)for path in reference_paths]
 if name=='backcheck':
  for original,expected in protocol['reference_files'].items():
   method=Path(original).parent.name
   require(sha(root/'qualification'/method/'heldout_0.npz')==expected,'backcheck reference hash')
 rows=[]
 for row in report['results']:
  method=row['method'];path=folder/method/'run_0.npz';data=load_arrays(path)
  gate,errors,pos,mom,unresolved=inspect_gate(data,ref40,ref80,protocol['core_indices'])
  require(gate==row['qualified']and errors==row['label_error_indices'],'qualification result '+method)
  require(pos==row['core_position_max_abs_m']and mom==row['core_momentum_max_abs_normalized'],'core residual '+method)
  require(unresolved==report['reference_unresolved_indices'],'unresolved labels')
  cost=[];fallback=[];rep=0
  while(folder/method/f'run_{rep}.npz').exists():
   other=load_arrays(folder/method/f'run_{rep}.npz')
   require(np.array_equal(data['islost'],other['islost']),'repeat survival '+method)
   require(np.allclose(data['rout'],other['rout'],rtol=0,atol=0,equal_nan=True),'repeat state '+method)
   receipt=json.loads((folder/method/f'cost_{rep}.json').read_text())
   require(np.isfinite(receipt['seconds'])and receipt['seconds']>=0,'positive tracking timer')
   cost.append(receipt['seconds']);fallback.append(receipt['fallback_particles']);rep+=1
  require(cost==row['tracking_seconds'],'timing receipts '+method)
  require(fallback==row['fallback_counts'],'fallback accounting '+method)
  require(float(np.median(cost))==row['median_tracking_seconds'],'median arithmetic '+method)
  first=row['median_tracking_seconds']+row['native_construction_seconds']+row.get('compile_seconds',row.get('compilation_seconds',0))+row['warmup_seconds']+row['plugin_build_seconds_charged']
  require(abs(first-row['first_workload_seconds'])<1e-12,'first workload cost '+method)
  rows.append({'method':method,'qualified':gate,'label_error_indices':errors,'core_position_max_abs_m':pos,'core_momentum_max_abs_normalized':mom,'first_workload_seconds':first})
 return {'campaign':name,'status':'passed','methods':rows,'reference_unresolved_indices':report['reference_unresolved_indices']}

def audit_diagnostics(root):
 folder=root/'boundary_diagnostics';protocol=json.loads((folder/'protocol.json').read_text());report=json.loads((folder/'diagnostic_audit.json').read_text())
 for name,key in [('diagnose_boundaries.py','script_sha256'),('qualification_bnl.py','helper_sha256')]:
  require(sha(folder/'source_snapshot'/name)==protocol[key],'diagnostic executed source')
 reference40=load_arrays(root/'qualification/native40/heldout_0.npz');reference80=load_arrays(root/'qualification/native80/heldout_0.npz');rows=[]
 for row in report['additional_backcheck']:
  data=load_arrays(folder/row['method']/'run_0.npz')
  gate,errors,pos,mom,unresolved=inspect_gate(data,reference40,reference80,list(range(32)))
  require(gate==row['qualified']and errors==row['label_error_indices'],'additional comparator gate')
  require(pos==row['core_position_max_abs_m']and mom==row['core_momentum_max_abs_normalized'],'additional comparator core')
  require(abs(row['first_workload_seconds']-sum([row['median_tracking_seconds'],row['native_construction_seconds'],row['warmup_seconds']]))<1e-12,'additional comparator cost')
  rows.append({'method':row['method'],'qualified':gate,'first_workload_seconds':row['first_workload_seconds']})
 point_rows=json.loads((folder/'point_diagnostics.json').read_text())['results']
 require(point_rows==report['point_diagnostics'],'diagnostic label record agreement')
 return {'campaign':'post_selection_boundary_diagnostics','status':'passed','methods':rows,'point_label_records':len(point_rows),'physical_convergence_asserted':False}

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--data-root',type=Path,default=Path(__file__).resolve().parent);p.add_argument('--output',type=Path,required=True);args=p.parse_args()
 results=[audit(args.data_root,'confirmation','confirmation_audit.json',['confirmation/native40/run_0.npz','confirmation/native80/run_0.npz'])]
 if(args.data_root/'backcheck/backcheck_audit.json').exists():results.append(audit(args.data_root,'backcheck','backcheck_audit.json',['qualification/native40/heldout_0.npz','qualification/native80/heldout_0.npz']))
 if(args.data_root/'boundary_diagnostics/diagnostic_audit.json').exists():results.append(audit_diagnostics(args.data_root))
 report={'status':'passed','campaigns':results,'new_tracking':False,'scope':'Source snapshot, stored numerical-array, gate and cost arithmetic checks. No independent proof of simulator truth or industrial gain.'}
 args.output.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'status':'passed','campaigns':len(results),'new_tracking':False}))

if __name__=='__main__':main()
