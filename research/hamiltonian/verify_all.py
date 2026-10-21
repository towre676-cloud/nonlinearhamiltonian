#!/usr/bin/env python3
"""Replay every delivered exact verifier in temporary copies; stdlib only."""
import concurrent.futures,hashlib,json,os,shutil,subprocess,sys,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def main():
    failures=[];manifest=ROOT/'MANIFEST.sha256'
    if manifest.exists():
        for line in manifest.read_text().splitlines():
            h,n=line.split('  ',1);p=ROOT/n
            if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=h:failures.append('Manifest:'+n)
    with tempfile.TemporaryDirectory(prefix='moyal-proof-replay-') as tmp:
        tmp=Path(tmp)
        for name in ['quartic','structural','monomial','independent','context']:
            shutil.copytree(ROOT/name,tmp/name,ignore=shutil.ignore_patterns('_deps','__pycache__','scan.py'))
        for name in ['partner_lab.py','verify_cli.py']:shutil.copy2(ROOT/name,tmp/name)
        jobs=[(name,tmp/name/('verify_recovered.py' if name=='context' else 'verify.py')) for name in ['quartic','structural','monomial','independent','context']]
        jobs.append(('cubic factorization',tmp/'independent/verify_cubic.py'))
        jobs.append(('user CLI integration',tmp/'verify_cli.py'))
        def run(job):
            name,p=job;r=subprocess.run([sys.executable,'-B','-X','utf8','-S',str(p)],cwd=p.parent,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONUTF8='1'),capture_output=True,text=True,timeout=240)
            if r.returncode:failures.append(name)
            return {'suite':name,'return_code':r.returncode,'stdout':r.stdout.strip(),'stderr':r.stderr.strip()}
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:records=list(pool.map(run,jobs))
    result={'status':'passed' if not failures else 'failed','arithmetic':'exact rational/integer; standard library','suites':records,'failures':failures,'scope':'Named finite checks accompany all-degree proofs; this is not a formal proof-kernel certification or a new replay of archived global msolve receipts.'}
    print(json.dumps(result,ensure_ascii=False,indent=2));return bool(failures)
if __name__=='__main__':sys.exit(main())
