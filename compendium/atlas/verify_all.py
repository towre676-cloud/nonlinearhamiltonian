#!/usr/bin/env python3
"""Replay scoped mathematical checks without modifying the delivered package.

Python 3.10+; domain/annual checks are stdlib-only. Node is required for actual
browser-engine checks. Browser/PDF rendering checks are recorded separately.
"""
from pathlib import Path
import argparse,collections,concurrent.futures,hashlib,json,os,shutil,subprocess,sys,tempfile
ROOT=Path(__file__).resolve().parent

def load(p):return json.loads(Path(p).read_text())
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--skip-annual',action='store_true');args=ap.parse_args();failures=[]
 manifest=ROOT/'MANIFEST.sha256'
 if manifest.exists():
  for line in manifest.read_text().splitlines():
   digest,name=line.split('  ',1);p=ROOT/name
   if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=digest:failures.append('Manifest mismatch: '+name)
 atlas=load(ROOT/'data/atlas.json');corpus=atlas['corpus'];uids=[e['uid'] for e in corpus]
 assert len(uids)==len(set(uids))==1051
 assert len(atlas['supplementary'])==14 and len(atlas['families'])==71 and len(atlas['chapters'])==16
 assert collections.Counter(e['year'] for e in corpus)=={2023:114,2024:237,2025:351,2026:349}
 html=(ROOT/'output/Mathematics_Atlas_2023_2026.html').read_text();embedded=html.split('<script id="atlas-data" type="application/json">',1)[1].split('</script>',1)[0];assert json.loads(embedded)==atlas
 D={d['id'] for d in atlas['taxonomy']['domains']};F={f['id'] for f in atlas['families']}
 for e in corpus:assert e['primary_domain'] in D and set(e['family_ids'])<=F
 for f in atlas['families']:assert set(f['source_uids'])<=set(uids) and set(f['anchor_uids'])<=set(f['source_uids'])
 env=dict(os.environ,PYTHONUTF8='1',PYTHONDONTWRITEBYTECODE='1');records=[]
 with tempfile.TemporaryDirectory(prefix='atlas-verification-') as temp:
  temp=Path(temp)
  for folder in ['data','domains','labs']:shutil.copytree(ROOT/folder,temp/folder)
  for file in ['verify_labs.py']:shutil.copy2(ROOT/file,temp/file)
  from materialize_sources import extract_into
  extract_into(temp)
  for year in [2023,2024,2025,2026]:
   original=temp/'source_working'/f'{year}_Mathematics_Source_Bundle'/f'{year}_Mathematics';payload=load(original/'compendium.json');entries=payload['entries']
   actual={e['source_id']:e['source'] for e in corpus if e['year']==year}
   assert actual=={e['id']:e for e in entries},('Altered source payload',year)
   if year==2023:assert [e['source'] for e in atlas['supplementary']]==payload['syntheses']
  def run(label,path):
   p=subprocess.run([sys.executable,'-B','-X','utf8','-S',str(path)],cwd=path.parent,env=env,capture_output=True,text=True,timeout=240)
   result={'label':label,'return_code':p.returncode,'stdout':p.stdout.strip(),'stderr':p.stderr.strip()}
   if p.returncode:failures.append(label)
   return result
  jobs=[('domain:'+name,temp/'domains'/name/'verify.py') for name in ['arithmetic','algebra','geometry','analysis','probability','computation']]
  if not args.skip_annual:jobs += [('annual:'+str(y),temp/'source_working'/f'{y}_Mathematics_Source_Bundle'/f'{y}_Mathematics'/'verify_all.py') for y in [2023,2024,2025,2026]]
  # Independent read-only processes operate on disjoint domain/source trees.
  with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
   records=list(pool.map(lambda t:run(*t),jobs))
  if shutil.which('node'):
   records.append(run('independent browser-engine fixtures',temp/'verify_labs.py'))
   p=subprocess.run(['node',str(temp/'labs/test_engine.js')],capture_output=True,text=True,cwd=temp)
   records.append({'label':'engine regression checks','return_code':p.returncode,'stdout':p.stdout.strip(),'stderr':p.stderr.strip()})
   if p.returncode:failures.append('engine regression checks')
  else:records.append({'label':'browser-engine fixtures','status':'not run: Node unavailable'})
 result={'status':'passed' if not failures else 'failed','main_treatments':1051,'supplementary_treatments':14,'concept_families':71,'domains':16,'source_payloads_unchanged':True,'annual_suites_replayed':not args.skip_annual,'records':records,'failures':failures}
 print(json.dumps(result,ensure_ascii=False,indent=2));return bool(failures)
if __name__=='__main__':sys.exit(main())
