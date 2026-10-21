"""Rebuild the month report and preserve raw retrieval records without reinterpretation."""
from pathlib import Path
from collections import Counter
import json,subprocess,sys,tempfile,shutil
from author_helpers import substantive_words
H=Path(__file__).resolve().parent
E=json.loads((H/'entries.json').read_text())
C=json.loads((H/'checks.json').read_text())['checks']
receipts=[]
for path in sorted(H.glob('root*.json')):
    records=json.loads(path.read_text())
    for i,record in enumerate(records):
        receipts.append({'receipt_file':path.name,'record':i,'raw':record})
(H/'receipts.json').write_text(json.dumps(receipts,ensure_ascii=False,indent=2)+'\n')
for e in E:
    o=e['original'];filename,_,index=o['retrieval_receipt'].partition(' record ')
    raw=json.loads((H/filename).read_text())[int(index)]
    text='\n'.join(b.get('text','') for b in raw.get('result',{}).get('content',[]))
    assert o['source_excerpt'] in text,e['id']
    assert o['evidence']+'@'+o['date'] in o['source_excerpt'],e['id']
    assert o['original_question'] is None
with tempfile.TemporaryDirectory() as td:
    P=Path(td)
    for fn in ('verify.py','entries.json'):shutil.copyfile(H/fn,P/fn)
    subprocess.run([sys.executable,str(P/'verify.py')],cwd='/',check=True,capture_output=True)
    portable=json.loads((P/'checks.json').read_text())
    assert all(c['status']=='pass' for c in portable['checks'])
words={e['id']:substantive_words(e) for e in E}
report={
 'month':'2026-09','status':'recovered_fragments_substantially_developed',
 'entry_count':len(E),'evidence_counts':dict(Counter(e['original']['evidence'] for e in E)),
 'source_dates':sorted({e['original']['date'] for e in E}),
 'original_questions_recovered':0,
 'coverage':'Root month-wide retrieval, separate date-window coverage and topic-specific followups. Distinct mathematically meaningful recovered clusters are developed. The returned material consists of dated retrieval summaries and fragments rather than a complete transcript archive. No unrecovered date is treated as proof that no mathematics occurred.',
 'source_gaps':['Full historical transition tables, TTL separator tensors, large intertwiners, support matrices, M22 networks and finite-group census certificates were not returned; small exact models are newly declared examples.','Raw throughput and WIND data were not recovered, so historical timing, prediction accuracy and empirical superiority are not certified.','The asserted general perfect-power classification, complete Thue/cubic census and RH-dependent Schatten thresholds are not adopted as established. Precise tractable subfamilies and conditional analytic scopes replace unsupported global conclusions.','Retrospective query echoes, retrieval-limit statements and a retrieved 2025 file fragment are excluded as original September 2026 mathematics.'],
 'new_work_boundary':'Every revised question, proof, worked calculation and extension is newly authored. U and A identify the actual role in the exact returned source bullet, not authorship of the revised mathematics. General results are proved in text under stated hypotheses; finite/numerical checks corroborate the specified examples and do not substitute for those proofs.',
 'notable_corrections':['For c*n to be a dth power, n=a*t^d where a complements prime valuations of c modulo d; for squares this is the squarefree part of c. The formula n=c*w^2 requires c squarefree or an equivalent restricted parameter convention.','A modular zero-Hom rank proves the rational conclusion only when full column rank is actually certified; exceptional primes can gain solutions.','First-order invisibility does not establish finite-amplitude target constancy on a nonlinear observation fiber.','A simple point certificate on a Mordell curve does not establish the completeness of a curve or Thue census.'],
 'verification':{'script':'verify.py','checks':'checks.json','passed':sum(c['status']=='pass' for c in C),'failed':sum(c['status']=='fail' for c in C),'scope':'35 exact finite/integer/rational/matrix/finite-field checks or explicitly identified numerical corroborations; theorem scope remains in the written proofs.','portability':'A clean temporary copy containing only verify.py and entries.json was run from / and wrote passing checks.json beside its own script.','literal_provenance_audit':'All35 source excerpts occur literally in their specified root receipt/record; all evidence roles and dates match the exact source bullet.'},
 'body_words':words,'total_body_words':sum(words.values()),'min_body_words':min(words.values()),'max_body_words':max(words.values()),
 'receipt_files':[p.name for p in sorted(H.glob('root*.json'))]+['receipts.json'],
 'coverage_topics':[e['title'] for e in E]
}
(H/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'entries':len(E),'words':sum(words.values()),'checks':len(C),'receipt_records':len(receipts),'literal_sources':'all pass','portable':'pass'}))
