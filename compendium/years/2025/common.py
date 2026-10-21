"""Shared data loading and scope checks for the 2025 mathematics editions."""
from pathlib import Path
from collections import Counter
import json

ROOT = Path(__file__).resolve().parent
MONTHS = ['January','February','March','April','May','June','July','August','September','October','November','December']
REQUIRED = ['id','title','status','summary','definitions','result','example','limits','extension','references','original']

def month_entries(folder):
    entries = []
    for name in ['entries.json','catalog_entries.json']:
        path = folder/name
        if path.exists():
            part = json.loads(path.read_text(encoding='utf-8'))
            if isinstance(part,dict):
                part = part.get('entries',[part])
            entries.extend(part)
    return sorted(entries,key=lambda x:(x['original'].get('date') or '9999',x['id']))

def load(draft=False):
    months=[]; entries=[]; seen=set()
    for i,name in enumerate(MONTHS,1):
        key=f'{i:02d}'; folder=ROOT/'months'/key
        if not (folder/'entries.json').exists() and not draft:
            raise FileNotFoundError(folder/'entries.json')
        part=month_entries(folder)
        report_path=folder/'report.json'
        report=json.loads(report_path.read_text()) if report_path.exists() else {}
        catalog_path=folder/'catalog_report.json'
        catalog_report=json.loads(catalog_path.read_text()) if catalog_path.exists() else None
        for e in part:
            assert all(k in e for k in REQUIRED),(e.get('id'),'missing field')
            assert e['id'].startswith('Y25-'+key+'-'),e['id']
            assert e['id'] not in seen,('duplicate',e['id'])
            seen.add(e['id'])
            for k in ['name','statement','proof']:
                assert isinstance(e['result'].get(k),str) and e['result'][k].strip(),(e['id'],'result',k)
            for k in ['setup','calculation','conclusion']:
                assert isinstance(e['example'].get(k),str) and e['example'][k].strip(),(e['id'],'example',k)
            assert isinstance(e['definitions'],list) and e['definitions'],e['id']
            original=e['original']
            assert original.get('evidence') in ['U','A','T'],(e['id'],'evidence')
            assert original.get('month')==f'2025-{key}',(e['id'],'month')
            assert original.get('source_excerpt') and original.get('retrieval_receipt'),(e['id'],'source')
            assert not original.get('date') or str(original['date']).startswith(f'2025-{key}'),(e['id'],'date')
            if original['evidence']=='A':
                assert original.get('original_question') is None,(e['id'],'assistant evidence assigned a user prompt')
            for ref in e['references']:
                assert ref.get('label') and ref.get('url','').startswith(('https://','http://')),(e['id'],'reference')
            e['month_key']=key
        counts=dict(Counter(e['original']['evidence'] for e in part))
        receipts=[]
        for path in sorted(folder.glob('root_*.json')):
            data=json.loads(path.read_text())
            if isinstance(data,list): receipts.extend(data)
        months.append(dict(key=key,name=name,entries=part,report=report,catalog_report=catalog_report,combined_treatment_count=len(part),evidence_counts=counts,retrieval_calls=len(receipts)))
        entries.extend(part)
    return months,entries

def collect_refs(entries):
    refs={}
    for e in entries:
        for r in e['references']:
            url=r['url'].rstrip('/')
            if url not in refs:
                refs[url]=dict(key=f'R{len(refs)+1:03d}',label=r['label'],url=r['url'])
    return refs

def prose_words(entries):
    total=0
    for e in entries:
        texts=[e['summary'],*e['definitions'],*e['result'].values(),*e['example'].values(),e['limits'],e['extension']]
        total+=sum(len(str(x).split()) for x in texts)
    return total
