"""Rebuild source receipts and coverage reports without changing root evidence."""
from pathlib import Path
from collections import Counter
import json,re
HERE=Path(__file__).resolve().parent
entries=json.loads((HERE/'entries.json').read_text())
receipts=[]
for path in sorted(HERE.glob('root*.json')):
 raw=json.loads(path.read_text())
 if not isinstance(raw,list):continue
 for i,record in enumerate(raw):receipts.append({'source_file':path.name,'source_record':i,'query':record.get('query',record.get('request')),'result':record['result']})
(HERE/'receipts.json').write_text(json.dumps(receipts,ensure_ascii=False,indent=2)+'\n')
for e in entries:
 o=e['original'];name,idx=o['retrieval_receipt'].rsplit(' record ',1)
 record=json.loads((HERE/name).read_text())[int(idx)]
 text='\n'.join(c['text'] for c in record['result']['content'] if c.get('type')=='text')
 assert o['source_excerpt'] in text,(e['id'],'source line absent')
 assert o['date'] in o['source_excerpt'],(e['id'],'date mismatch')
 role=re.search(r'\b([UA])@',o['source_excerpt'])
 assert role and role.group(1)==o['evidence'],(e['id'],'role mismatch')
 assert o['original_question'] is None
 assert o['month']=='2026-'+HERE.name
 assert not any(x in o['source_excerpt'] for x in ['retrospective must','mustrecover'])
checks=json.loads((HERE/'checks.json').read_text())['checks']
common=[
 'Recovery is bounded and fragmentary, not an exhaustive archive export. Four recorded source passes do not prove that omitted days had no mathematics.',
 'The exact source line supplies attribution and date. Original questions remain null; all revised questions, proofs and worked examples are newly authored.',
 'Root performed historical retrieval because child Personal Context was unavailable earlier. The saved complete root query/result records are the evidence; no child failure is treated as historical absence.',
 'Prior assistant numerical results, physical performance, security exponents and sweeping framework claims are not inherited as demonstrated results.',
 'General background theorems are either derived with hypotheses in prose or explicitly cited. The check program verifies finite examples and stated numerical identities, not all general theorems.'
]
jan=[
 'The multiplication table for M29, a complete F7 witness, discrete-log lattice decoder and exact logged transition system were not recovered. General finite-algebra models are clearly new developments.',
 'Yoccoz/Branner–Hubbard moduli, Ecalle–Voronin invariants, hyperoperators and some quantum or automorphic names occur as topic labels without defining constructions. No missing classification theorem is invented.',
 'The actual Eisenstein scattering determinant, spectral measure and claimed fitted intercept calculations were not supplied. Finite Gibbs/partition calculations do not certify those experiments.',
 'The actual chi–theta governor, singular diffusion schedule and full causal jump-diffusion coefficients were not recovered. Explicit solvable benchmark dynamics are substituted transparently.',
 'The thin-shell source does not define every physical unit or boundary condition. The corrected selector is a newly defined dimensional model, not an engineering validation.',
 'The root-authored January catalog_entries.json separately develops the late-January equation archive. Its ten entries and checks are not counted in this base report.',
 'January30 names broad Langlands/GKZ/microlocal topics but supplies no full operator, curve, functor or certified data. The Selmer, Cech and CM examples are specified new mathematical models rather than reconstructed historical computations.'
]
feb=[
 'The original complete PT-coupler equations were not recovered. A newly specified balanced coupler and standard Mathieu equation are independently derived, with historical sign errors corrected.',
 'No complete exponential category, mixed-Ext vanishing theorem or category equivalence was supplied. The elliptic-curve and semisimple examples have separate explicit hypotheses.',
 'THSC legality, conical equivalence, Delzant integrality and secretless factorization claims lack full original proofs. Concrete finite spectral collisions, cone scaling and observation-fiber theorems give scoped replacements.',
 'The purported Heisenberg tower bonding maps were conditional. The doubling-tower lim1 is proved algebraically, while contraction is kept distinct from exact Mittag–Leffler image stabilization.',
 'Historical optimizer metrics, hardware attenuation claims, FAR exponents and alleged external-table ingestion are unverified claims; no experiments or datasets are fabricated.',
 'The sixth-order recurrence lacks initial data and parameter semantics. The Fibonacci and Jacobi transfer models are explicit, while no missing unique recurrence sequence is invented.',
 'The symmetry-indicator example is a new integer-lattice certificate, not an asserted crystallographic table. Actual external representations, compatibility, induction and anomaly maps require independent data.',
 'A broad February10 equation/domain catalog supplies names rather than separate complete research questions. The scalar-domain entry develops its core algebraic distinction; common elementary labels are not inflated into unrelated filler.'
]
words=[len(' '.join([e['summary'],*e['definitions'],*e['result'].values(),*e['example'].values(),e['limits'],e['extension']]).split()) for e in entries]
report={'month':'2026-'+HERE.name,'item_count':len(entries),'ids':[e['id'] for e in entries],
 'historical_dates':sorted({e['original']['date'] for e in entries}),
 'evidence_counts':dict(Counter(e['original']['evidence'] for e in entries)),
 'receipt_count':len(receipts),'source_files':sorted({r['source_file'] for r in receipts}),
 'coverage':'Broad full-month recovery, two targeted followup passes and a final early/late-window sweep. Distinct recoverable mathematical clusters receive substantial explicit developments, with source gaps retained.',
 'gaps':common+(jan if HERE.name=='01' else feb),
 'check_count':len(checks),'checks_passed':sum(x['status']=='passed' for x in checks),'checks_failed':sum(x['status']!='passed' for x in checks),
 'development_words':sum(words),'entry_word_range':[min(words),max(words)],
 'verification_scope':'Portable stdlib-only finite exact certificates and declared numerical checks, with the scope of cited general theorems identified in every relevant check.',
 'provenance_check':'Every exact source excerpt occurs in its actual cited record, carries the assigned date and matching U/A role, and is a mathematical topic passage rather than a retrieval query or format-only constraint.',
 'artifact_owner':'Root integrates common artifacts and persists final deliverables.'}
(HERE/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(report['month'],len(entries),'entries',len(receipts),'source receipts',report['checks_passed'],'checks passed; provenance passed')
