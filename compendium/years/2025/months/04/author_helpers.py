"""Local authoring helpers; final entries.json is self-contained."""
from pathlib import Path
import json, collections
FIELDS=('id','title','status','summary','definitions','result','example','limits','extension','references','original')
def make_entry(month,index,title,date,evidence,field,excerpt,receipt,question,summary,definitions,result,example,limits,extension,references,original_question=None,attribution_note=None,status='Developed classical result with a checked example; recovered claims corrected where needed'):
    assert date is None or date.startswith(month)
    assert evidence in ('U','A','T')
    assert original_question is None or evidence=='U'
    return dict(id=f'Y25-{month[-2:]}-{index:03}',title=title,status=status,summary=summary,definitions=definitions,result=result,example=example,limits=limits,extension=extension,references=references,original=dict(date=date,month=month,evidence=evidence,field=field,concept=title,origin='Recovered dated conversation evidence; mathematical development newly written',question=question,math=result['statement'],finish='Precise result, proof, worked example and explicit limits',kind='Revised mathematical treatment',refs=[r['url'] for r in references],source_excerpt=excerpt,retrieval_receipt=receipt,original_question=original_question,attribution_note=attribution_note or ('The dated source identifies user-authored material; the revised question and proof are new unless verbatim wording is separately provided.' if evidence=='U' else 'The historical mathematical excerpt is assistant-authored. No original user question is inferred; the revised question and worked development are new.')))
def save_entries(parent,entries):
    parent=Path(parent)
    assert len({e['id'] for e in entries})==len(entries)
    for e in entries:
        assert set(e)==set(FIELDS)
        assert set(e['result'])=={'name','statement','proof'}
        assert set(e['example'])=={'setup','calculation','conclusion'}
        assert e['original']['source_excerpt'] and e['original']['retrieval_receipt']
    parent.joinpath('entries.json').write_text(json.dumps(entries,ensure_ascii=False,indent=2)+'\n')
def assemble_receipts(parent):
    parent=Path(parent);out=[]
    for f in sorted(parent.glob('root_*.json')):
        data=json.loads(f.read_text())
        if isinstance(data,list):
            for i,r in enumerate(data):out.append(dict(receipt_file=f.name,receipt_index=i,record=r))
    parent.joinpath('receipts.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    return out
