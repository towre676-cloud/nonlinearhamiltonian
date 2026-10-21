from pathlib import Path
import json

HERE=Path(__file__).resolve().parent

def recovered_source(date,needle,evidence):
    """Return a literal dated source line, never a guessed fallback."""
    for path in sorted(HERE.glob('root*.json')):
        records=json.loads(path.read_text())
        for index,record in enumerate(records):
            for block in record.get('result',{}).get('content',[]):
                for line in block.get('text','').splitlines():
                    role_ok=evidence=='T' or evidence+'@'+date in line
                    if role_ok and date in line and needle.lower() in line.lower():
                        return line,f'{path.name} record {index}'
    raise ValueError(f'No exact {evidence} source for {date}: {needle}')

def entry(number,date,needle,evidence,field,title,question,summary,definitions,
          statement,proof,setup,calculation,conclusion,limits,extension,references=()):
    excerpt,receipt=recovered_source(date,needle,evidence)
    return {
        'id':f'Y26-09-{number:03d}',
        'title':title,
        'status':'Classical mathematics with newly authored derivation or explicitly defined worked model',
        'summary':summary,
        'definitions':definitions,
        'result':{'name':title,'statement':statement,'proof':proof},
        'example':{'setup':setup,'calculation':calculation,'conclusion':conclusion},
        'limits':limits,
        'extension':extension,
        'references':[{'label':label,'url':url} for label,url in references],
        'original':{
            'date':date,'month':'2026-09','evidence':evidence,
            'field':field,'concept':title,'origin':'Recovered dated mathematical passage',
            'question':question,'math':statement,'finish':'Actual proof and worked example, with stated scope and extension',
            'kind':'Revised mathematical treatment','refs':[url for _,url in references],
            'source_excerpt':excerpt,'retrieval_receipt':receipt,'original_question':None,
            'attribution_note':'This is the literal returned retrieval bullet, which may summarize rather than transcribe the historical exchange. U identifies user subject matter and does not attribute nearby assistant formulas to the user; A identifies assistant output; T identifies other source material. All revised formulations and worked mathematics are newly authored.'
        }
    }

def substantive_words(e):
    return len(' '.join([e['summary'],*e['definitions'],*e['result'].values(),
        *e['example'].values(),e['limits'],e['extension']]).split())

def write_entries(entries):
    ids=[e['id'] for e in entries]
    assert len(set(ids))==len(ids)
    for e in entries:
        assert substantive_words(e)>=290,(e['id'],substantive_words(e))
    (HERE/'entries.json').write_text(json.dumps(entries,ensure_ascii=False,indent=2)+'\n')
    print(len(entries),'entries',sum(map(substantive_words,entries)),'substantive words')
