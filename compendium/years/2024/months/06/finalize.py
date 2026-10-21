from pathlib import Path
from collections import Counter
import json

HERE=Path(__file__).resolve().parent
entries=json.loads((HERE/'entries.json').read_text())
receipts=[]
for name in ('root_receipts.json','root_followups.json','root_specifics.json'):
    p=HERE/name
    for i,r in enumerate(json.loads(p.read_text())):
        receipts.append({'receipt_id':f'{name}[{i}]','source_file':name,'raw':r})
(HERE/'receipts.json').write_text(json.dumps({'month':'2024-06','receipts':receipts,'child_errors_file':'child_errors.json','note':'Raw root queries/results are preserved without rewriting; child capability errors are not historical evidence.'},ensure_ascii=False,indent=2)+'\n')
wordcounts={e['id']:len(' '.join([e['summary'],*e['definitions'],*e['result'].values(),*e['example'].values(),e['limits'],e['extension']]).split()) for e in entries}
report={
 'month':'2024-06','entries':len(entries),'entry_ids':[e['id'] for e in entries],
 'evidence_counts':dict(Counter(e['original']['evidence'] for e in entries)),
 'recovered_dates':sorted({e['original']['date'] for e in entries if e['original']['date']}),
 'undated_topic_ids':[e['id'] for e in entries if e['original']['date'] is None],
 'substantive_word_counts':wordcounts,'substantive_words':sum(wordcounts.values()),
 'raw_root_receipts':len(receipts),
 'historical_attribution':'U identifies recovered user subject matter, not authorship of the assistant formulas summarized nearby. A is assistant-only mathematics. T is an undated mathematical document fragment. All revised questions, proofs and example choices are newly authored; no unrecovered original prompt is quoted.',
 'coverage':'Number-system distinctions; Lie closure/periodicity; symplectic flows/Casimirs; rational coordinates/dimension; e and affine shape equivalence; circle coordinate rings; corrected quartic Galois classification; weight-normalized Hecke operators; Čech gluing obstruction; formal braid matrix; trefoil bracket; hyperbolic metric; Virasoro cocycle; spheres/surfaces/triangles fundamental groups; forms/Hodge/Stokes; density/implicit surfaces; SPD/CG; toroidal graph/surface/Morse distinctions; probability renormalization; skew tensors and gauge patches; finite Gibbs/Metropolis; qubit gradients; Bell Lindblad dephasing; additive identifiability.',
 'repairs':[
  'The quartic x^4−2x^2+9 has roots ±(sqrt2+i), ±(sqrt2−i), splitting field Q(sqrt2,i), and Galois group V4, not D4.',
  'Canonical nondegenerate symplectic Casimirs are constant on connected domains; a conserved oscillator Hamiltonian is not a Casimir.',
  'For weight4 level1, T2 uses a_(2n)+8a_(n/2), with the second term zero for odd n; it does not use a_(2n)+2a_n.',
  'A defined Čech complex supplies a concrete closed-not-exact obstruction; sheaf compatible-section gluing itself is not contradicted.',
  'The quantum weight-update heuristic need not descend the stated loss; an explicit qubit counterexample and exact gradient replace that claim.',
  'Gyre additive corrections supply no defined physical mechanism or identifiable decomposition without additional independent data.'
 ],
 'source_gaps':[
  'The searches do not certify a complete archive. Topics not returned are not evidence that no mathematics occurred on those dates.',
  'The full mathematical document requested June7, including its original date and complete Tonnetz formula, was not recovered. Y24-06-018 keeps date null and evidence T; its triangulation is a clearly new toy example.',
  'The scaling recurrence was truncated. The normalized-sum renormalization map is an explicit new replacement example, not a reconstruction of that recurrence.',
  'The June7 distributed-model framework catalogue had no unified equations. A two-spin finite Gibbs example develops one named framework; CFD, chaos, spin-glass thermodynamic limits and turbulence are not claimed reconstructed.',
  'The June30 nonlinear-gravity fragment and gyre definitions remained incomplete. No invented field equations or predictive physics are supplied.',
  'The number-system catalogue did not return definitions of every listed hyperreal, surreal, ordinal or nonassociative system; selected exact constructions distinguish their types without falsely merging them into an inclusion chain.',
  'No verbatim full original user mathematical prompt was returned. original_question remains null throughout.'
 ],
 'checks':'verify.py is portable and stdlib-only. It includes a formal Laurent-polynomial braid certificate, exact finite-field/field-basis checks, exact CG, F2 boundary ranks, finite detailed balance and rational channel states. Bounded numerical checks are explicitly distinguished from general proofs.'
}
(HERE/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'entries':len(entries),'words':sum(wordcounts.values()),'receipts':len(receipts)}))
