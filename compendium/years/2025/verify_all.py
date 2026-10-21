"""Replay supplied mathematical programs offline, then validate the source schema."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from collections import Counter
import subprocess,sys,json,hashlib,os
from common import ROOT,load

def run(path):
    env=dict(os.environ,PYTHONUTF8='1')
    result=subprocess.run([sys.executable,'-S',str(path)],cwd=path.parent,capture_output=True,text=True,encoding='utf-8',env=env)
    return dict(program=path.relative_to(ROOT).as_posix(),return_code=result.returncode,stdout=result.stdout.strip(),stderr=result.stderr.strip())

def main():
    for month in range(1,13):
        for name in ['entries.json','verify.py','checks.json','report.json']:
            assert (ROOT/'months'/f'{month:02d}'/name).is_file(),('Required monthly deliverable missing',month,name)
    paths=sorted((ROOT/'months').glob('*/verify.py'))
    paths+=sorted((ROOT/'months').glob('*/catalog_verify.py'))
    paths+=sorted((ROOT/'months').glob('*/independent_*.py'))
    if (ROOT/'verify_figures.py').exists():paths.append(ROOT/'verify_figures.py')
    if (ROOT/'independent_audit.py').exists():paths.append(ROOT/'independent_audit.py')
    with ThreadPoolExecutor(max_workers=6) as pool: results=list(pool.map(run,paths))
    failures=[r for r in results if r['return_code']]
    months,entries=load()
    records=[]; counts=Counter();seen_checks=set();duplicates=0
    report_paths=sorted((ROOT/'months').glob('*/*checks.json'))
    if (ROOT/'figure_checks.json').exists():report_paths.append(ROOT/'figure_checks.json')
    if (ROOT/'independent_checks.json').exists():report_paths.append(ROOT/'independent_checks.json')
    for path in report_paths:
        report=json.loads(path.read_text())
        checks=report.get('checks',[]) if isinstance(report,dict) else report
        if not isinstance(checks,list):continue
        added=0
        for c in checks:
            if 'status' in c: status=str(c['status']).lower()
            elif 'passed' in c:status='passed' if c['passed'] else 'failed'
            else:status='unspecified'
            if status in ['failed','fail','false','error']:failures.append(dict(report=path.relative_to(ROOT).as_posix(),check=c))
            month=path.parent.name if path.parent.parent.name=='months' else 'root'
            key=(month,json.dumps(c.get('id',c.get('ids','')),sort_keys=True),c.get('name',c.get('check','Check')))
            if key in seen_checks:duplicates+=1;continue
            seen_checks.add(key);counts[status]+=1;added+=1
        records.append(dict(report=path.relative_to(ROOT).as_posix(),records=added,raw_records=len(checks),sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
    summary=dict(status='passed' if not failures else 'failed',developed_entries=len(entries),months_represented=12,months_with_recovered_entries=sum(bool(m['entries']) for m in months),verifier_programs=len(paths),scoped_records=sum(r['records'] for r in records),duplicate_records_omitted=duplicates,status_counts=dict(counts),results=results,reports=records,failures=failures,scope='Finite examples, exact certificates and numerical checks only; written proofs and cited general results have their own stated scope. Retrieval/schema checks are separated in the individual ledger.')
    (ROOT/'verification_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2))
    print(json.dumps({k:summary[k] for k in ['status','developed_entries','verifier_programs','scoped_records','status_counts','failures']},ensure_ascii=False))
    if failures:sys.exit(1)

if __name__=='__main__':main()
