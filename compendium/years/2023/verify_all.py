"""Replay every supplied mathematical verifier using Python's standard library.

Run from any directory: python /path/to/verify_all.py
"""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import subprocess,sys,json,collections,hashlib

ROOT=Path(__file__).resolve().parent
JOBS=[]
for key in 'abcdef':
 for script,report in [('verify.py','checks.json'),('supplement_verify.py','supplement_checks.json'),('spectral_verify.py','spectral_checks.json'),('jordan_verify.py','jordan_checks.json')]:
  path=ROOT/'chapters'/key/script
  if path.exists():JOBS.append((key+'/'+script,path,path.with_name(report)))
 for path in (ROOT/'chapters'/key).glob('independent_*.py'):
  report=path.with_name(path.stem+'_checks.json')
  JOBS.append((key+'/'+path.name,path,report))
JOBS.append(('syntheses',ROOT/'verify_syntheses.py',ROOT/'synthesis_checks.json'))

def run(job):
 label,script,report=job
 p=subprocess.run([sys.executable,str(script)],cwd=script.parent,text=True,capture_output=True,timeout=180)
 result=dict(verifier=label,return_code=p.returncode,stdout=p.stdout.strip(),stderr=p.stderr.strip())
 if p.returncode:return result
 data=json.loads(report.read_text());records=data.get('checks',[])
 result['records']=len(records)
 result['status_counts']=dict(collections.Counter(str(c.get('status',c.get('passed','unspecified'))) for c in records))
 result['record_digest']=hashlib.sha256(report.read_bytes()).hexdigest()
 result['report']=str(report.relative_to(ROOT))
 return result

def main():
 with ThreadPoolExecutor(max_workers=6) as pool:results=list(pool.map(run,JOBS))
 failed=[x for x in results if x['return_code']]
 totals=collections.Counter()
 for r in results:totals.update(r.get('status_counts',{}))
 for key,count in totals.items():
  if key.lower() in ['fail','failed','error','false'] and count:failed.append({'status':key,'count':count})
 coverage=json.loads((ROOT/'revised_rows.json').read_text());seen=[]
 for path in (ROOT/'chapters').glob('*/entries.json'):seen.extend(x['id'] for x in json.loads(path.read_text()))
 expected={x['id'] for x in coverage}
 assert len(seen)==len(set(seen))==114 and set(seen)==expected,'Missing or duplicated developed entry'
 result=dict(status='passed' if not failed else 'failed',developed_entries=114,verifier_programs=len(results),scoped_records=sum(x.get('records',0) for x in results),status_counts=dict(totals),failures=failed,results=results,scope='This runner replays finite, exact and numerical examples. Written proofs and literature dependencies retain the scopes stated in the compendium. Proof-only records are not executable confirmations.')
 (ROOT/'verification_summary.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
 print(json.dumps({k:v for k,v in result.items() if k not in ['results','scope']},ensure_ascii=False))
 if failed:sys.exit(1)

if __name__=='__main__':main()
