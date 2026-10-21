"""Replace authoring shorthand by literal retrieved result bullets, never queries."""
from pathlib import Path
import json,re
P=Path(__file__).resolve().parent

def apply(parent):
 parent=Path(parent);es=json.loads((parent/'entries.json').read_text());sources=[]
 for fn in ['root_receipts.json','root_followups.json','root_coverage.json']:
  f=parent/fn
  if not f.exists():continue
  for i,record in enumerate(json.loads(f.read_text())):
   result=record['result']
   texts=[c['text'] for c in result.get('content',[]) if c.get('type')=='text']
   for text in texts:
    # Each bullet includes all literal continuation lines up to the next bullet or section.
    starts=[m.start() for m in re.finditer(r'(?m)^- \[',text)]
    if not starts:
     starts=[m.start() for m in re.finditer(r'(?m)^\[PRIOR_ASSISTANT_OUTPUT\]',text)]
    for k,start in enumerate(starts):
     end=starts[k+1] if k+1<len(starts) else len(text)
     bullet=text[start:end].split('\n\n[gmail]')[0].split('\n\n[files]')[0].split('\n\n<assistant_usage_note>')[0].strip()
     sources.append((fn,i,bullet,text))
 for e in es:
  o=e['original'];date=o['date'];role=o['evidence']
  matches=[s for s in sources if f'{role}@{date}' in s[2]]
  if not matches:
   raise ValueError((e['id'],date,role,'no literal source bullet'))
  # Prefer a source with the specific locator file if available, then the broad source.
  requested=o['retrieval_receipt'].split()[0]
  matches.sort(key=lambda s:(s[0]!=requested,s[0]!='root_receipts.json',len(s[2])))
  fn,i,bullet,raw=matches[0]
  assert bullet in raw
  o['source_excerpt']=bullet
  o['retrieval_receipt']=f'{fn} record {i}'
  o['attribution_note']+=' The source_excerpt is a literal retrieved result bullet (including any original truncation), not a reconstructed transcript. It may summarize historical content; no verbatim original question is inferred.'
 parent.joinpath('entries.json').write_text(json.dumps(es,ensure_ascii=False,indent=2)+'\n')
 return len(es)
if __name__=='__main__':print(apply(P),'literal source excerpts matched')
