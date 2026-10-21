import json,re,pathlib
P=pathlib.Path(__file__).resolve().parent
E=json.loads((P/'entries.json').read_text())
receipts=[];lines=[]
for fn in ('root_receipts.json','root_followups.json','root_details.json'):
 data=json.loads((P/fn).read_text());receipts.append({'file':fn,'records':len(data)})
 for i,r in enumerate(data):
  for m in r.get('result',r).get('structuredContent',{}).get('messages',[]):
   for line in m.get('content','').splitlines():
    if re.search(r'[UAT]@2024-11-',line):lines.append((fn,i,line))
coverage=[
('2024-11-01 to 2024-11-03','Compound growth, accounting, resource totals, wave-power units, hypothetical efficiency percentages',[1,2]),
('2024-11-01','Partial Euler products, prime-factor perturbation, critical-line convergence error',[4]),
('2024-11-03','Harmonic-oscillator finite differences and unsupported spectral zero matching',[3]),
('2024-11-04','Unified operator/function, finite supersymmetry, Fourier duality, trace-like claims, categorical typing',[5]),
('2024-11-04','BSD rank and spectral multiplicity; arithmetic zeros, primes, spectral-statistics limits',[6,4,5]),
('2024-11-04','KMS and Laplace transforms; unconfined hydrogen partition-function obstruction',[7]),
('2024-11-12','Wavelengths, photon/charge/energy dimensions, Faraday/Tafel correction, simulation model versus discretization error',[8]),
('2024-11-15 to 2024-11-16','Maximal properties, suprema, Chevalley images, rational-function domains, projective compactness',[9]),
('2024-11-16','Higher-dimensional polytopes and geometry: slices, projection fibers, hidden-dimension inference',[11]),
('2024-11-15','Temperley–Lieb/affine quotient conventions',[12]),
('2024-11-15 to 2024-11-16','Finite-support homoclinic sequences and conditions needed for an actual horseshoe',[13]),
('2024-11-15','Cylindrical Gaussian extension, Sazonov scope, trace-class covariance and tightness',[14]),
('2024-11-15','Bratteli diagram branching/path counts and probability-data distinction',[15]),
('2024-11-16','AGCP/SEACC labels, invariant subspaces, Grassmannian charts, fields and bit complexity',[16]),
('2024-11-19','Brauer height-zero theorem, exact arXiv version, elementary character-height example',[17]),
('2024-11-19','Representation/fluid analogy: legitimate equivariant reduction and separate PDE energy model',[10,20]),
('2024-11-20','Harper norm/flux/energy symmetries, rational branches and touching bands',[18]),
('2024-11-20','IDS/Wannier Diophantine relation, label ambiguity and topological hypotheses',[19]),
('2024-11-21 to 2024-11-25','Land-allocation overcount, yearly versus cycle totals, per-person/aggregate units, weekly percentage denominator',[1]),
('2024-11-30','Frenet/Beta frames, Darboux vector, curved connection conventions',[21]),
('2024-11-30','Pontryagin/Chern curvature forms and boundary variation',[22]),
('2024-11-30','Twisted boundary phases and operator domains',[23]),
('2024-11-30','Schmidt, superselection, finite error-correction scope',[24]),
('2024-11-30','Weak formulations, coercivity, Lax–Milgram and Sobolev-space example',[25]),
('2024-11-30','RG beta flow, scale normalization and finite/formal proof limits',[26])]
def ids(ns):return [f'Y24-11-{n:03d}' for n in ns]
report={'month':'2024-11','status':'Developed all sufficiently specified mathematical topic groups in the recovered evidence; archive coverage remains retrieval-limited','entries':len(E),'receipt_files':receipts,'retrieved_dated_evidence_lines':len(lines),'distinct_dated_source_lines':len(set(x[2] for x in lines)),'coverage':[dict(date=d,topics=t,entries=ids(ns)) for d,t,ns in coverage],
'gaps':[
 'Retrieval receipts are summaries and sometimes truncated; complete original conversations and original user wording were not recovered. Every original_question remains null.',
 'The named FB-SURD/BS-rank scale, AGCP/SEACC classes, and logistics percentages had no adequate definitions or reproducible datasets. Precise bounded replacement models are developed; no theorem about the undefined frameworks is claimed.',
 'The geometric-Langlands fragment names categories but does not specify the curve, group, stacks, functor, or exact theorem. Entry005 supplies a typed finite duality example and records this missing structure.',
 'The affine Temperley–Lieb presentation was unspecified; entry012 proves the universal quotient criterion and finite relations without choosing an unsupported affine convention.',
 'The broad Nov30 catalogue names Gelfond–Schneider, q-numbers, Hilbert problems, and additional open physics problems without a recovered concrete question or definition. These fragments are recorded as fragments, not expanded into invented historical work.',
 'Hypersonic/VTOL technical design parameters, commercial/agricultural instructions, and nutritional prescriptions are outside the mathematics-only scope. Only coherent abstract arithmetic or PDE principles are retained.',
 'No numerical list, spectral analogy, or zero-spacing observation is promoted to an RH, BSD, Langlands, P-versus-NP, or interacting-continuum-QFT proof.'
],
'corrections':['Wrong-sign/coarse-grid spectral list rejected by positivity and Gershgorin bounds.','Ordinary critical-line partial Euler products do not inherit the absolute Euler-product theorem.','Land allocations total74500, not70000; aggregate and per-recipient energy totals differ by1000.','Harper Q branches can touch; a rational label fixes a Hall integer only moduloQ without further conventions.','Cylindrical consistency alone does not give an ell2-valued Gaussian.'],
'verification':{'script':'verify.py','ledger':'checks.json','passed':27,'total':27,'scope':'Exact rational/integer finite examples plus selected floating-point convention checks; written proofs supply the general statements.'},
'word_count_main_fields':sum(len(' '.join([e['summary'],*e['definitions'],*e['result'].values(),*e['example'].values(),e['limits'],e['extension']]).split()) for e in E),
'primary_source_checks':['https://arxiv.org/abs/2209.04736v2','https://annals.math.princeton.edu/2024/200-2/p04','https://epubs.siam.org/doi/abs/10.1137/1103018','https://dlmf.nist.gov/18.3','https://doi.org/10.1103/PhysRevLett.49.405'],
'attribution_policy':'U/A/T labels refer to dated historical evidence. Revised questions, proofs and examples are newly authored; no original prompt or new discovery is inferred.'}
(P/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
