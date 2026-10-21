"""Portable retrieval-ledger checks; no historical mathematics is fabricated."""
from pathlib import Path
import json

HERE=Path(__file__).resolve().parent
entries=json.loads((HERE/'entries.json').read_text())
receipts=json.loads((HERE/'receipts.json').read_text())
report=json.loads((HERE/'report.json').read_text())
checks=[]
def check(name,condition,detail):
    assert condition,name
    checks.append(dict(id='MONTH-2024-01',name=name,status='passed',detail=detail))

check('No invented historical entries',entries==[] and report['entry_count']==0,
      'The inventory remains empty because no dated mathematical source was recovered.')
root=receipts['retrievals']
check('Four independent root retrieval calls',len(root)==4,
      'Full-month, two half-month, and unfiltered full-month queries are retained in full.')
texts=['\n'.join(c.get('text','') for c in r['result'].get('content',[]) if c.get('type')=='text') for r in root]
check('No matching source in the returned conversation results',
      all('No conversations matched the query.' in t for t in texts),
      'This audits the returned results only. It does not assert that January contained no mathematics.')
check('Coverage is explicitly a retrieval gap',report['status']=='source_gap' and report['original_user_questions_recovered']==0,
      'No theorem, historical question, original authorship or full-month completeness is inferred from failed recovery.')
out=dict(month='2024-01',status='passed',scope='retrieval ledger only; no mathematical example was available',checks=checks,count=len(checks))
(HERE/'checks.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
print(json.dumps({'month':'2024-01','checks':len(checks),'status':'passed'}))
