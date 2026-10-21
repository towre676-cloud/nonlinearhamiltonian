import json,re,pathlib
P=pathlib.Path(__file__).resolve().parent;E=json.loads((P/'entries.json').read_text());receipts=[];lines=[]
for fn in ('root_receipts.json','root_followups.json','root_details.json'):
 data=json.loads((P/fn).read_text());receipts.append({'file':fn,'records':len(data)})
 for i,r in enumerate(data):
  for m in r.get('result',r).get('structuredContent',{}).get('messages',[]):
   for line in m.get('content','').splitlines():
    if re.search(r'[UAT]@2024-12-',line):lines.append((fn,i,line))
coverage=[
('2024-12-01','Sphere eversion/immersion distinction, Boy/Morin topology and Willmore normalization',[1]),
('2024-12-01','TT gauge and polarization dimension',[2]),
('2024-12-01','Trace anomaly, scale derivative and the actual cited lattice-QCD source',[3]),
('2024-12-01','Quiddity failures, transfer matrices, continuants and generating functions',[4]),
('2024-12-01','Jordan code, nullity chains, matrix example, symmetry commutation and numerical instability',[5]),
('2024-12-01','Stinespring and a complete finite positive channel dilation',[37]),
('2024-12-03','Wave-tensor bundle typing, curvature integrability and determinant-factorization tautology',[6]),
('2024-12-03','Projector spectrum versus dissipative generator and nonnormal growth',[7]),
('2024-12-03 to 2024-12-08','Characters, mock-series domains, unit-circle evaluation, formal measure and modular-series scope',[8,20]),
('2024-12-05','Energy-rate arithmetic corrected by10^6 and a non-operational one-dimensional barrier exponent',[9]),
('2024-12-12','Laguerre/spherical basis, radial weight, normalization and torus-domain mismatch',[10]),
('2024-12-12','1597-mode sum and exact phase-feedback objective; orthogonality makes the integrated gradient zero',[11]),
('2024-12-13','Traveling/serpenoid waves, Laurent operator symbol and layered-field type errors',[12]),
('2024-12-13','Modal neural weights, correct chain rule, interference XOR and nonlinear readout',[13]),
('2024-12-14','Heat kernels, Minakshisundaram–Pleijel zeta, zero modes, compactness and hydrogen obstruction',[14]),
('2024-12-14','Lie superalgebra coefficients, parity, Jacobi, square-zero differential and deformation obstructions',[15]),
('2024-12-15','Six-point zero statistics, fitted Hermitian mass matrices and sample/ensemble distinction',[16]),
('2024-12-16','SU2 exponential, exponentially changing angles, chord-distance failure and area-sequence asymptotic',[17]),
('2024-12-16','Galois versus Langlands and an exact local quadratic splitting example',[18]),
('2024-12-17','S4 conjugacy classes, full character table, V4 quotient and resolvent interpretation',[19]),
('2024-12-17','E2,24,eta derivative,quasimodularity,j(i)=1728 and limits of RH/physical inference',[20]),
('2024-12-17','Frequency-to-note mapping corrected through ratios and cents',[21]),
('2024-12-17','A2 Cartan/root data,crystallographic restriction,E8/rank/dimension audit and unsupported mineral counts',[22]),
('2024-12-17','Abstract simplicial topology: clique dimension versus genuine fifth homology',[23]),
('2024-12-17','Running-coupling factor-of-two convention',[36]),
('2024-12-18','P30 explicit coordinates and integer coefficients: exact polynomial and rational-interval rejection',[24]),
('2024-12-18','Mordell–Weil rank/torsion,canonical heights and a proved rational two-torsion calculation',[25]),
('2024-12-19','Height pairings and a precisely defined finite-set width',[26]),
('2024-12-18','Mineral-symmetry model abstractions: Landau parity/coexistence and two-band Bloch spectrum',[27]),
('2024-12-26','Exact enhanced Hamiltonian form,Hermiticity,finite evolution and spin-exchange spectrum',[28]),
('2024-12-26','GHZ coherence,dephasing and ideal quantum-Zeno scope',[29]),
('2024-12-26','A2 cluster mutation and pentagon Laurent sequence',[30]),
('2024-12-26','Quiver Grassmannian incidence and Euler characteristic',[31]),
('2024-12-26','F1 counting heuristic,Krasner hyperfield and multiplicative-inverse type distinction',[32]),
('2024-12-26','Combinatorial flag varieties,Tits-style incidence,Plucker equation and support specialization',[33]),
('2024-12-31','MPPF braid/Reidemeister/modular-category claims: exact S/T datum and framing conventions',[34]),
('2024-12-31','Toric-code baseline,stabilizers,logical loops and distance versus unrestricted protection',[35])]
report={'month':'2024-12','status':'All sufficiently specified recovered mathematical topic groups developed; unrecovered or nonmathematical claims explicitly delimited','entries':len(E),'receipt_files':receipts,'retrieved_dated_evidence_lines':len(lines),'distinct_dated_source_lines':len(set(x[2] for x in lines)),'coverage':[dict(date=d,topics=t,entries=[f'Y24-12-{n:03d}' for n in ns]) for d,t,ns in coverage],
'gaps':[
 'The receipts are retrieved summaries with truncations, not a full message export. Exact original user questions were not recovered and remain null.',
 'The unsupported Dec5 biological/device allegations are excluded. Dec6 person-lifting and Dec8 medical-stimulation designs are not developed; only independently meaningful abstract mathematical ingredients are retained without engineering or clinical instructions.',
 'The Dec17 brain/quantum/Galois narrative is unsupported. Entry023 develops only abstract simplicial topology and makes no physical attribution.',
 'No actual knot-to-particle map, independent mass matrix, mineral Galois polynomial, mineral-count dataset, or Mordell–Weil-to-space-group morphism was recovered. Their proposed consequences are not asserted.',
 'The exact P30 coordinates and coefficients were recovered as historical assistant output. They fail both exact certificates; no valid rational point, rank, or torsion claim follows.',
 'The proposed MPPF carrier Hamiltonian,anyon data,noise model,and protection theorem were not recovered. Entries034–035 supply established finite categorical/code baselines and identify the missing proof obligations.',
 'The Dec26 Hamiltonian was recovered symbolically but not with numerical operators or coefficients; no material spectrum or simultaneous hyperfield-state implementation is inferred.',
 'General sphere eversion,modular transformation,canonical-height,and spectral-geometry theorems are cited where used; elementary finite examples and stated algebraic consequences are proved here. No novelty or continuum-QFT construction is claimed.'
],
'corrections':['The three historical polygon quiddities fail their incidence sums.','The recovered P30 point is exactly false, not merely numerically inaccurate.','The historical energy-rate power is1.12953452697mW, not1.13kW.','Orthogonal global modes have phase-independent integrated energy, so the proposed phase-gradient feedback vanishes.','Bare Laguerre polynomials are not L2 radial waves; spherical harmonics are not automatically orthogonal on a torus.','A general exponentially weighted distance need not satisfy the triangle inequality.','The one-loop coupling needs4pi over beta0 log(mu^2/Lambda^2) under the stated log-mu beta convention.','A high-dimensional simplex is contractible; dimension alone is not a cavity.'],
'verification':{'script':'verify.py','ledger':'checks.json','passed':38,'total':38,'scope':'Exact finite/integer/rational certificates,independently assembled stabilizer/homology matrices,and selected numerical convention checks. General statements are proved in the entry text.'},
'word_count_main_fields':sum(len(' '.join([e['summary'],*e['definitions'],*e['result'].values(),*e['example'].values(),e['limits'],e['extension']]).split()) for e in E),
'primary_source_checks':['https://doi.org/10.1103/PhysRevD.109.094504','https://dlmf.nist.gov/18.3','https://dlmf.nist.gov/14.30','https://arxiv.org/abs/math/0104151','https://arxiv.org/abs/0807.4834','https://arxiv.org/abs/quant-ph/9707021','https://doi.org/10.2307/3615344'],
'attribution_policy':'Dated source attribution is preserved. Every revised prompt and worked construction is newly authored. User,assistant and retrieved-file statements are not silently interchanged.'}
(P/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
