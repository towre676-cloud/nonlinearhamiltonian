from pathlib import Path
from collections import Counter
import json

HERE=Path(__file__).resolve().parent
entries=json.loads((HERE/'entries.json').read_text())
receipts=[]
for name in ('root_receipts.json','root_followups.json','root_details.json'):
    p=HERE/name
    for i,r in enumerate(json.loads(p.read_text())):
        receipts.append({'receipt_id':f'{name}[{i}]','source_file':name,'raw':r})
(HERE/'receipts.json').write_text(json.dumps({'month':'2024-05','receipts':receipts,'child_errors_file':'child_errors.json','note':'Raw root queries/results are preserved without rewriting; child capability errors are not historical evidence.'},ensure_ascii=False,indent=2)+'\n')
wordcounts={e['id']:len(' '.join([e['summary'],*e['definitions'],*e['result'].values(),*e['example'].values(),e['limits'],e['extension']]).split()) for e in entries}
report={
 'month':'2024-05','entries':len(entries),'entry_ids':[e['id'] for e in entries],
 'evidence_counts':dict(Counter(e['original']['evidence'] for e in entries)),
 'recovered_dates':sorted({e['original']['date'] for e in entries if e['original']['date']}),
 'substantive_word_counts':wordcounts,'substantive_words':sum(wordcounts.values()),
 'raw_root_receipts':len(receipts),
 'historical_attribution':'All developed subjects are recovered assistant passages, not user-authored prompts. Dates are supported by timestamped excerpts. Every revised question and worked development is new editorial mathematics.',
 'coverage':'Finite mixtures/kernels, winding, variational calculus, graded brackets, finite-field and symmetric-power zeta counting, local L-factors, Schrödinger continuity, nonlinear wave conservation, finite Gaussian/Grassmann integrals, generating-function response and dimensional nonidentification, categorical intertwiners, coupled equilibria, SDE covariance and stochastic-kernel/topology distinctions.',
 'source_gaps':[
  'The searches do not certify a complete archive. Other May mathematics may exist but was not recovered.',
  'The May13 game/AI and database outline was truncated and supplied no equations; no specific game-theoretic historical claim or invented original problem is extracted from that outline.',
  'The May24/25 speculative frameworks did not define a complete motive, full graded neural algebra, QCD construction, loop-gravity Hamiltonian, AdS/CFT dictionary or eleven-dimensional interacting theory. The entries explicitly develop tractable mathematical components and do not claim those theories are constructed.',
  'One May1–15 follow-up returned an access disclaimer despite successful dated May6 retrieval elsewhere. It is retained as raw output, not treated as evidence that May6 mathematics was absent.',
  'No verbatim original user mathematical prompts were returned. original_question is null throughout.'
 ],
 'checks':'verify.py uses only Python stdlib, writes checks.json beside itself and distinguishes exact finite identities from bounded numerical samples and general written proofs.'
}
(HERE/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'entries':len(entries),'words':sum(wordcounts.values()),'receipts':len(receipts)}))
