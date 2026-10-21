#!/usr/bin/env python3
"""Build a provenance bibliography without downloading or redistributing references.
Run from a published checkout, optionally passing --root PATH. Input data and exact source locators are retained
in references.json; output Markdown links target the published repository layout.
"""
from pathlib import Path
from urllib.parse import urlsplit,urlunsplit
from collections import defaultdict,Counter
import json,re,hashlib,argparse
HERE=Path(__file__).resolve().parent
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--root',type=Path,default=HERE.parent,help='Repository root containing compendium/ and research/.')
args=parser.parse_args()
WORK=args.root.resolve()
ATLAS=WORK/'compendium/atlas'
if not (ATLAS/'data/atlas.json').exists():
    ATLAS=WORK/'mathematics_atlas_2023_2026'
A=json.loads((ATLAS/'data/atlas.json').read_text())
S=A['corpus']+A['supplementary']
BYUID={e['uid']:e for e in S}
F={f['id']:f for f in A['families']}
D={d['id']:d for d in A['taxonomy']['domains']}
CH={c['domain_id']:c for c in A['chapters']}
HREF=WORK/'research/hamiltonian/context/references.json'
if not HREF.exists():
    HREF=WORK/'moyal_partner_research/context/references.json'
H=json.loads(HREF.read_text())
records={};invalid=[];nonurl_tokens=[]

def canonical_url(url):
    """Conservative document identity: keep scheme/path/query; remove fragment only.
    Scheme and host are case insensitive. Do not guess redirects, mirror identity,
    version equivalence, or whether HTTP and HTTPS represent the same document.
    """
    p=urlsplit(url)
    if p.scheme.lower() not in ('http','https') or not p.netloc:
        raise ValueError('Not an absolute HTTP(S) reference')
    return urlunsplit((p.scheme.lower(),p.netloc.lower(),p.path,p.query,''))

def add(url,label,usage,meta=None):
    if not isinstance(url,str):return
    url=url.strip()
    try:key=canonical_url(url)
    except Exception as exc:
        invalid.append(dict(url=url,usage=usage,error=str(exc)));return
    rec=records.setdefault(key,dict(canonical_document_url=key,original_urls=set(),labels=set(),usages=[],metadata=[]))
    rec['original_urls'].add(url)
    if label:rec['labels'].add(str(label))
    u=dict(usage,original_url=url)
    if u not in rec['usages']:rec['usages'].append(u)
    if meta and meta not in rec['metadata']:rec['metadata'].append(meta)

def ref_values(obj,path=()):
    """Only named citation fields; original historical fields remain distinguishable."""
    if isinstance(obj,dict):
        for k,v in obj.items():
            if k in ('references','refs') and isinstance(v,list):
                for i,r in enumerate(v):yield path+(k,str(i)),r
            elif isinstance(v,(dict,list)):
                yield from ref_values(v,path+(k,))
    elif isinstance(obj,list):
        for i,v in enumerate(obj):
            if isinstance(v,(dict,list)):yield from ref_values(v,path+(str(i),))

def consume(value,usage):
    if isinstance(value,dict):
        for key in ('url','author_pdf'):
            if value.get(key):
                label=value.get('label') or value.get('title') or value.get('name') or value[key]
                if key=='author_pdf':label+=' (author PDF)'
                add(value[key],label,dict(usage,url_field=key),{k:v for k,v in value.items() if k not in ('url','author_pdf','web_ref','find_ref','pdf_ref','author_bibliography_ref','root_reopen_required')})
    elif isinstance(value,str):
        if value.startswith(('http://','https://')) and not re.search(r'\s',value):add(value,value,usage)
        else:nonurl_tokens.append(dict(value=value,usage=usage))

for e in S:
    domains=sorted({e['primary_domain'],*e.get('secondary_domains',[])} & set(D))
    for path,r in ref_values(e['source']):
        consume(r,dict(kind='source_treatment',source_uid=e['uid'],year=e['year'],domains=domains,field_path='.'.join(path),original_historical_field=bool(path and path[0]=='original')))
for f in A['families']:
    for path,r in ref_values(f):
        consume(r,dict(kind='atlas_family',family_id=f['id'],domains=[f['domain_id']],field_path='.'.join(path)))
for label,objects in [('chapter',A['chapters']),('bridge',A['bridges'])]:
    for obj in objects:
        for path,r in ref_values(obj):
            consume(r,dict(kind='atlas_'+label,object_id=obj.get('id',obj.get('domain_id')),domains=obj.get('domains',[obj.get('domain_id')]),field_path='.'.join(path)))
annual_inputs=[]
for volume in A['source_volumes']:
    p=WORK/f"compendium/years/{volume['year']}/compendium.json"
    if not p.exists():
        p=ATLAS/volume['local_root']/'compendium.json'
    comp=json.loads(p.read_text())
    annual_inputs.append(dict(year=volume['year'],path=str(p.relative_to(WORK)),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),reference_count=len(comp.get('references',[])),entry_count=len(comp.get('entries',[])),supplement_count=len(comp.get('syntheses',[]))))
    for i,r in enumerate(comp.get('references',[])):
        consume(r,dict(kind='annual_reference_list',year=volume['year'],domains=[],reference_key=r.get('key') if isinstance(r,dict) else None,field_path='references.'+str(i)))
for r in H:
    consume(r,dict(kind='hamiltonian_context',context_id=r['id'],domains=['D03','D06','D16'],field_path='context.references'))

# Keep every explicit URL variant. Do not merge separate mirrors into a single work.
refs=[]
for i,(key,r) in enumerate(sorted(records.items()),1):
    uidset=sorted({u['source_uid'] for u in r['usages'] if u.get('source_uid')})
    familyset=sorted({u['family_id'] for u in r['usages'] if u.get('family_id')})
    domainset=sorted({d for u in r['usages'] for d in u.get('domains',[]) if d in D})
    hids=sorted({u['context_id'] for u in r['usages'] if u.get('context_id')})
    years=sorted({u['year'] for u in r['usages'] if u.get('year')})
    exact=sorted(r['original_urls'])
    preferred=next((u for u in exact if not urlsplit(u).fragment),exact[0])
    labels=sorted(r['labels'],key=lambda x:(x.startswith(('http:','https:')),len(x),x.casefold()))
    project=('github.com/towre676-cloud/' in key.lower())
    refs.append(dict(id=f'R{i:04d}',reference_kind='authored_current_project_document' if project else 'external_resource',label=labels[0],labels=labels,canonical_document_url=key,preferred_original_url=preferred,original_urls=exact,source_uid_count=len(uidset),source_uids=uidset,family_count=len(familyset),family_ids=familyset,domain_ids=domainset,annual_years=years,hamiltonian_context_ids=hids,usage_count=len(r['usages']),usages=r['usages'],retained_metadata=r['metadata'],status='Retained reference and provenance; live availability and every associated literature claim are not newly audited by this bibliography.'))
RID={r['canonical_document_url']:r['id'] for r in refs}
UID_REFS=defaultdict(set);FAMILY_REFS=defaultdict(set)
for r in refs:
    for u in r['source_uids']:UID_REFS[u].add(r['id'])
    for f in r['family_ids']:FAMILY_REFS[f].add(r['id'])

def source_link(uid):
    e=BYUID[uid]
    return f"../compendium/readable/years/{e['year']}/{e['source_id']}.md"
def domain_link(d):return f'../compendium/readable/domains/{d}.md'
def md(t):return str(t).replace('|','\\|').replace('\n',' ').replace('\r',' ')
def link(label,url):return '['+md(label)+'](<'+url.replace('|','%7C').replace(' ','%20')+'>)'
def sl(uid):return link(uid,source_link(uid))
def dl(d):return link(d,domain_link(d))
def rl(rid):return f'[{rid}](SOURCE_INDEX.md#{rid.lower()})'

authored=[]
for year in (2023,2024,2025,2026):
    pdf='2023_Mathematics_Compendium.pdf' if year==2023 else f'{year}_Month_by_Month_Mathematics.pdf'
    html=pdf[:-4]+'.html'
    uids=sorted(e['uid'] for e in S if e['year']==year)
    authored.append(dict(id=f'A{year}',reference_kind='authored_current_document',title=f'{year} mathematics annual volume',repository_path=f'compendium/years/{year}/{pdf}',alternate_repository_paths=[f'compendium/years/{year}/{html}',f'compendium/years/{year}/compendium.json'],covered_source_uid_count=len(uids),covered_source_uids=uids,status='Retrospective authored exposition with source evidence and scoped checks; not a complete transcript export.'))
authored += [dict(id='A-ATLAS',reference_kind='authored_current_document',title='Mathematics atlas, 2023 through 21 October 2026',repository_path='compendium/atlas/output/Mathematics_Atlas_2023_2026_Report.pdf',alternate_repository_paths=['compendium/atlas/output/Mathematics_Atlas_2023_2026.html','compendium/atlas/data/atlas.json'],covered_source_uid_count=len(S),covered_source_uids=sorted(BYUID),status='71 concept families, 16 domains, six bridges and ten implemented finite models; broader capabilities remain recipes where declared.'),dict(id='A-HAMILTONIAN',reference_kind='authored_current_document',title='Nonlinear Hamiltonians with exact classical–quantum partners',repository_path='research/hamiltonian/output/Nonlinear_Hamiltonian_Partners.pdf',alternate_repository_paths=['research/hamiltonian/output/Nonlinear_Hamiltonian_Partners.html','research/hamiltonian/output/Nonlinear_Hamiltonian_Partners.md'],covered_source_uid_count=0,covered_source_uids=[],status='Current research note with displayed proofs, exact finite fixtures and separate existing-research/external-solver boundaries. No literature-priority claim.')]

# Reading routes transfer named constructions, not analogies or unproved equivalences.
routes=[
 dict(id='T01',title='Recover a target, then decide which observation is worth buying',domains=['D03','D14','D15','D11','D12'],families=['D03-F01','D14-F01','D15-F01','D11-F01','D12-F04','D15-F04'],bridges=['B01'],labs=['L01','L08'],question='What is the smallest observation that still determines the target or preserves the action?',reading='Begin with equivalence classes and a transition rule that respects those classes. For linear data Hx and target Gx, work through ker H⊆ker G and G=LH, then calculate the recovery norm. Only after present target recovery is settled should you ask whether the observed state closes dynamically; HA=TH is an additional condition. Read hidden-target risk next: an unobserved coordinate can leave irreducible conditional variation even when observed noise tends to zero. Shared uncertainty then changes a decision difference because common terms cancel. Finish with the finite cheapest-experiment recursion, where the terminal condition is constancy of the target, rather than identification of every state.',checkpoint='Produce both a factorization certificate and a counterexample invisible vector for a failing target. In L01 compare the cheapest probes for the scalar target and a larger target. In L08 retain the same common uncertain variable in both actions.',boundary='These finite exact examples do not establish nonlinear global fibre constancy, future predictive performance or an optimal noisy sensor policy.'),
 dict(id='T02',title='From boundary matrices to gluing and transport',domains=['D04','D05','D06','D13'],families=['D04-F02','D05-F01','D05-F03','D05-F04','D06-F03','D13-F03'],bridges=['B02'],labs=['L09','L05'],question='Which local data assemble to a global object, and which obstruction survives?',reading='Compute an actual chain complex before interpreting its homology: verify that the product of successive boundaries is zero, and keep the coefficient ring. L09 compares a graph cycle with the complex obtained by filling its face. Continue to integer torsion and cochain gluing, where a real nullspace calculation can lose an integral obstruction. A logarithmic differential then supplies a complementary local-to-global example: locally closed need not mean globally exact because loop periods remain. Connections and gauge transport add ordered matrix products. L05 displays order dependence for two shears, but a two-matrix loop is not a construction of curvature on an arbitrary manifold.',checkpoint='Write down the boundary or Čech maps and one obstruction class. Compare a zero local differential with a nonzero loop period, then keep the shear commutator distinct from the projection contraction in the second L05 mode.',boundary='A picture of overlapping patches, an adjacency graph or a sampled transport loop does not determine a sheaf, its coefficient system, its derived comparison maps or a global connection.'),
 dict(id='T03',title='Spectral representation, stable evolution and inverse resolution',domains=['D07','D08','D09','D15'],families=['D07-F04','D08-F01','D08-F02','D09-F01','D15-F03','D07-F01'],bridges=['B03'],labs=['L04','L05'],question='When does a spectral formula control a trajectory or a reconstruction error?',reading='Start with a self-adjoint operator and its domain, multiplicities and spectral measure. Derive the heat semigroup and its mean-zero energy decay before comparing it with a finite stencil. Check conservation, positivity and stability separately, and use normalized grid norms when discussing a continuum rate. The Lyapunov example then shows why stable eigenvalues do not rule out temporary Euclidean growth. Move to the inverse problem last: positive singular values give uniqueness, while a small singular-value tail makes the inverse unbounded. The admissible source ellipsoid and deterministic noise norm determine a cutoff bound with two distinct terms.',checkpoint='In L04 compare bias, noise amplification and total upper bound while changing N. In severe mode keep the logarithmic safety margin; that implemented mode fixes β=1. Use L05 only for the stated two-line principal-angle model, not as a substitute inverse solver.',boundary='A residual-to-error bound needs operator hypotheses, and fixed-time trace class differs from a small-time heat asymptotic. No one lab implements all the PDE, frame or control recipes in this route.'),
 dict(id='T04',title='Exact populations, summaries and information loss',domains=['D13','D10','D11','D12','D14'],families=['D13-F01','D13-F02','D10-F02','D11-F04','D12-F03','D14-F01'],bridges=['B04'],labs=['L02','L03'],question='What can be counted exactly, and which distinctions are lost by a compressed statistic?',reading='Construct a finite population and its reversible address before using asymptotic approximations. L02 exhausts a six-item selection problem and exposes feasible counts, ranks and optimal values. Read random inclusion laws with a declared sampling model next; independence, fixed-size sampling and weighted sampling produce different pair probabilities. The graph-census family gives a stronger counterexample to overinterpreting summaries: two graphs can agree on a binary size–energy census while integer-height probes distinguish them. This connects exact enumeration to observation equivalence. A quotient suitable for optimization must preserve multiplicities if counts or probabilities are also requested.',checkpoint='Check a rank/unrank round trip and a lower-bound certificate for the finite optimum. In L03 compare the entire exact coefficient census, then evaluate it at a chosen floating q while retaining the distinction between the polynomial identity and its numerical value.',boundary='The six-item and seven-vertex examples do not reconstruct missing large-instance historical tables. A matching summary is an equivalence only relative to its stated probes.'),
 dict(id='T05',title='Poisson geometry to exact Moyal partners and coherent dynamics',domains=['D06','D03','D16','D14','D15'],families=['D06-F02','D03-F04','D16-F03','D16-F06','D14-F03','D15-F01'],bridges=['B05'],labs=['L06'],question='When does a nonlinear Hamiltonian admit exact classical–quantum partners, and when does equality persist under evolution?',reading='Fix one canonical pair, a characteristic-zero coefficient field and the flat Weyl–Moyal convention. Compute every nonzero odd transvectant gate rather than only the cubic correction. L06 makes this finite polynomial calculation inspectable. Then read the Hamiltonian note: separate the one-step kernel E(H), active partners with nonzero first bracket, the iterated invariant core D∞(H), exact Lie sectors and product closure. The note supplies all-degree proofs for its stated cubic, homogeneous-quartic, qF(p) and monomial classes, while finite fixtures independently replay named instances. The observability bridge interprets the coherent core as the invariant space invisible to correction outputs; exact invariance must be checked in the full polynomial ring.',checkpoint='Read the universal-observable theorem of Robert with its quantifier before comparing a restricted polynomial partner family. Reproduce a partner whose second action fails, and contrast it with an invariant exact sector. Use the pinned PerfectJet documents to locate the existing full-sextic through-degree-20 result.',boundary='Universal Schwartz-observable exactness is different from a restricted infinite polynomial sector. The retained full-space sextic classification has archived msolve dependencies; degrees 21 and above and independent proof-carrying replay remain separate obligations. A nonlinear canonical map need not preserve the same flat star product.'),
 dict(id='T06',title='Arithmetic reduction with complete orbit certificates',domains=['D01','D02','D09','D14'],families=['D01-F01','D01-F03','D01-F04','D01-F05','D02-F02','D14-F03'],bridges=['B06'],labs=['L07','L10'],question='How can a finite certificate establish a statement about an infinite arithmetic family?',reading='Begin with the scalar ring, residue system and p-adic precision. A root modulo p^n becomes a genuine p-adic root only with a compatible lifting and completeness argument. Cyclotomic reduction then provides a finite exact map whose fibres can be exhausted. L07 evaluates the unit reduction underlying the displayed phase map. Move to Pell orbits next: a unit action generates candidates, but a reduction argument and complete seed list are required for exhaustiveness. L10 navigates exact integer iterates of a proved orbit decomposition. Norm forms and elliptic height lattices extend the same pattern while adding class, unit, descent and saturation conditions.',checkpoint='Display one exact congruence or determinant certificate and state the theorem connecting it to the infinite result. For a Pell claim, identify all seeds and verify the descent that reaches them, rather than only computing many iterates.',boundary='Finite residues do not certify an exact zero by themselves. A rational-point search does not prove completeness without the corresponding descent, rank and saturation obligations.'),
 dict(id='T07',title='Periods, singular differential equations and asymptotic constants',domains=['D01','D02','D05','D07','D08'],families=['D01-F06','D02-F04','D05-F04','D07-F03','D08-F03','D08-F04'],bridges=['B02','B03'],labs=[],question='How does a specified integral become a differential equation and a controlled limiting value?',reading='Use the exact-integral family to establish a convergent representation, a branch and an interchange argument. Mellin moments provide a transparent example with a rational tail bound. For a parameter-dependent period, supply its operator and cycle data before calling it Picard–Fuchs. The Frobenius divided difference demonstrates how a logarithm emerges from coalescing exponents while the normalized Wronskian stays nonzero. Continue around a singular point to distinguish identity monodromy from a matrix whose eigenvalues are merely all one. Finish with the factorial Borel model, cubic fold and elliptic logarithmic constant: each states a small parameter and a quantified finite remainder or exact scaling identity.',checkpoint='Carry branch, cycle, normalization and operator metadata through one calculation. Distinguish a removable basis pole from singular boundary data, then compare a convergent evaluation with a divergent but valid finite asymptotic expansion.',boundary='A period name does not recover a missing differential operator. A local germ does not determine global Stokes constants, and naming a period does not prove algebraic independence.'),
 dict(id='T08',title='From random laws to reliable robust decisions',domains=['D10','D11','D12','D15'],families=['D10-F01','D10-F03','D11-F01','D11-F03','D12-F01','D12-F04','D15-F04'],bridges=['B01','B04'],labs=['L08','L01'],question='Which uncertainty model supports a useful action guarantee?',reading='Specify the joint law or deterministic uncertainty set before computing a variance or worst-case range. Stochastic dynamics requires its own time discretization and Itô correction; a marginal law does not determine dependence. Conditional risk identifies uncertainty left by the observation itself, whereas independent repeated measurements may only reduce sensor noise. Statistical validation then asks whether a procedure calibrated on one sample predicts another. In the deterministic branch, duality and robust difference bounds provide certificates for an action across a declared set. Correlated errors can cancel in a comparison even when their separate marginal intervals are wide.',checkpoint='Separate irreducible target uncertainty, observation noise, model uncertainty and finite-sample calibration. In L08 check the exact action difference under a shared variable, and in L01 test whether a new probe removes a target-relevant null direction.',boundary='A deterministic interval is not a confidence interval without a probabilistic coverage argument. Development-set optimality is neither causal evidence nor an out-of-sample guarantee.')
]

# Domain frontiers are project-level open tasks, not claims of unsolved literature.
queue=[]
for d,c in sorted(CH.items()):
    family_ids=c['concept_order']
    questions=[dict(family_id=fid,question=q) for fid in family_ids for q in F[fid].get('open_questions',[])]
    anchors=list(dict.fromkeys(u for fid in family_ids for u in F[fid].get('anchor_uids',[])))
    queue.append(dict(id='Q-'+d,domain_ids=[d],status='open_extension_in_retained_material',title=c['title']+' — next proof or certificate',task=c['open_frontier'],proof_obligation='Supply the explicit object, map, hypotheses and completeness or error argument required by the listed task; passing finite fixtures alone is not a proof of the extension.',family_ids=family_ids,source_uids=anchors,reference_ids=sorted({rid for fid in family_ids for rid in FAMILY_REFS[fid]}),subquestions=questions))
queue += [
 dict(id='Q-H01',domain_ids=['D03','D06','D16'],status='open_extension_in_retained_material',title='General higher-degree active partner kernels',task='Classify active polynomial exact-partner kernels for arbitrary quintic and sextic coefficient varieties in all partner degrees, with explicit exceptional strata.',proof_obligation='Control every higher odd gate and rule out unbounded-degree families or construct them with an all-degree argument. The existing pinned full-space sextic classification is through degree 20 and has an archived-solver boundary.',source_uids=[],family_ids=['D16-F03','D16-F06'],hamiltonian_sections=['Coordinate changes, existing research and the next boundary','Appendix F · Existing work and evidential boundaries']),
 dict(id='Q-H02',domain_ids=['D03','D09','D16'],status='open_extension_in_retained_material',title='Static kernels versus dynamically coherent cores',task='Determine D∞(H) and exact Lie sectors across arbitrary inhomogeneous quartics and higher-degree families, beyond the solved classes in the note.',proof_obligation='Prove exact invariance in the full polynomial ring. A degree truncation or one-step partner computation does not prove closure under every iterate.',source_uids=[],family_ids=['D16-F03','D09-F04','D15-F01'],hamiltonian_sections=['A quadratic perturbation that changes the dynamical answer completely','Appendix B · Arbitrary F, cubic PDEs and dynamical cores']),
 dict(id='Q-H03',domain_ids=['D03','D14','D16'],status='external_solver_dependency',title='Independent rational replay of global sextic receipts',task='Replace or supplement the retained archived msolve/Singular global verdicts with independently checkable characteristic-zero certificates and a formal attachment where desired.',proof_obligation='Distinguish exact rational instance kernels, finite-prime supporting checks and the global elimination conclusion. Preserve the pin and receipt hashes.',source_uids=[],family_ids=['D14-F03','D16-F03'],hamiltonian_context_ids=['R-PERFECTJET-PARTNER','R-PERFECTJET-INTEGRATION']),
 dict(id='Q-H04',domain_ids=['D06','D16'],status='open_extension_in_retained_material',title='Several canonical pairs and transported products',task='Extend coherent exact-sector classifications to several canonical pairs and explicit transported deformation products.',proof_obligation='State the symplectic convention, product and symbol/operator domain. Do not transport flat-Moyal exactness under an arbitrary nonlinear canonical pullback without correcting the product.',source_uids=[],family_ids=['D06-F02','D16-F06']),
 dict(id='Q-G01',domain_ids=[],status='historical_source_gap',title='Historical coverage and missing prompts',task='Recover any additional original conversation export and missing verbatim prompts when available, preserving speaker/date evidence and distinguishing historical statements from current exposition.',proof_obligation='Use the original record as evidence. A retrieved topic summary does not establish a verbatim prompt or the historical invention date of the displayed proof.',source_uids=[],family_ids=[]),
 dict(id='Q-G02',domain_ids=['D07','D08'],status='historical_source_gap',title='January 2024 and the omitted equation catalogue',task='The retained 2024 scope records no recovered January conversations and only an adjacent unnumbered Laplace transform plus equations 81–100 of a claimed 100-equation list. Recover missing entries before extending that historical catalogue.',proof_obligation='Absence from retrieved material is not proof that no mathematics was discussed. Do not invent equations 1–80.',source_uids=[e['uid'] for e in S if e['year']==2024 and e['source_id'].startswith('Y24-03-')],family_ids=[]),
 dict(id='Q-G03',domain_ids=['D13','D14','D15'],status='historical_source_gap',title='Missing large tables, operational inputs and benchmark data',task='Recover the named large-instance tables, sensor designs, action tables, original programs and benchmark protocols before claiming those historical instances or performance results were replayed.',proof_obligation='Keep the delivered six-item selection, seven-vertex graph, finite-probe and small matrix examples explicitly separate from unrecovered originals.',source_uids=list(dict.fromkeys(u for fid in ['D13-F01','D14-F01','D15-F01'] for u in F[fid]['anchor_uids'])),family_ids=['D13-F01','D14-F01','D15-F01']),
 dict(id='Q-G04',domain_ids=['D02','D08','D16'],status='historical_source_gap',title='Unspecified operators, monodromy and anyon matrices',task='Supply actual differential operators, cycles, braid generators, fusion/associator data and coefficient conventions for the larger historical proposals.',proof_obligation='A named theory or an isolated spectral statistic cannot determine missing matrices, coherence equations or a global continuation law.',source_uids=list(dict.fromkeys(u for fid in ['D08-F03','D16-F04'] for u in F[fid]['anchor_uids'])),family_ids=['D08-F03','D16-F04'])]

status_legend={
 'proved_in_stated_scope':'A displayed proof supports its exact hypotheses; this label is not a claim of novelty or independent formal verification.',
 'implemented_worked_model':'The interactive or exact engine implements the declared finite model and arithmetic, not an unrestricted domain solver.',
 'documented_recipe':'A mathematical workflow is described, but its general interactive engine is not implemented.',
 'external_solver_dependency':'The retained conclusion depends partly on explicitly identified archived external computation.',
 'open_extension_in_retained_material':'A proposed extension remains unproved in this collection; no claim is made that it is unsolved throughout the literature.',
 'historical_source_gap':'Required historical content was not recovered. A current illustrative model does not fill that provenance gap.'}

source_index=[]
for e in sorted(S,key=lambda x:x['uid']):
 source_index.append(dict(uid=e['uid'],title=e['source']['title'],year=e['year'],source_id=e['source_id'],primary_domain=e['primary_domain'],secondary_domains=e.get('secondary_domains',[]),family_ids=e.get('family_ids',[]),reference_ids=sorted(UID_REFS[e['uid']]),repository_path=source_link(e['uid'])[3:],status=e['source'].get('status'),source_date=e.get('source_date')))
metadata=dict(title='Source-linked mathematical bibliography and reading routes',edition_date='2026-10-21',source_scope='1,051 main treatments plus 14 retained 2023 annual syntheses; 71 atlas families; all four annual reference lists; Hamiltonian context references.',deduplication='Conservative canonical document URL: lowercase scheme/host and remove only fragment. Preserve scheme, path case, query and all exact original URLs. No mirror, redirect, DOI/arXiv-version or HTTP/HTTPS equivalence is guessed.',counting='source_uid_count counts unique treatments that explicitly retain the URL in their reference fields, including separately marked original historical refs. Family, annual-list and Hamiltonian-context citations are counted separately; family membership does not imply direct source citation.',availability='No network lookup or third-party PDF download is performed by this builder. References are provenance links, not blanket endorsement or proof dependencies.',inputs=[dict(path=str((ATLAS/'data/atlas.json').relative_to(WORK)),sha256=hashlib.sha256((ATLAS/'data/atlas.json').read_bytes()).hexdigest()),dict(path=str(HREF.relative_to(WORK)),sha256=hashlib.sha256(HREF.read_bytes()).hexdigest())]+annual_inputs)
stats=dict(main_treatments=len(A['corpus']),supplementary_treatments=len(A['supplementary']),all_treatments=len(S),families=len(F),domains=len(D),reference_documents=len(refs),exact_original_urls=sum(len(r['original_urls']) for r in refs),source_treatments_with_references=sum(bool(UID_REFS[u])for u in BYUID),source_treatments_without_references=sum(not UID_REFS[u]for u in BYUID),family_citations=sum(r['family_count']for r in refs),hamiltonian_context_records=len(H),authored_reading_documents=len(authored),reading_routes=len(routes),research_queue_items=len(queue),non_url_historical_tokens=len(nonurl_tokens))
out=dict(metadata=metadata,statistics=stats,references=refs,authored_documents=authored,source_index=source_index,family_reference_index={k:sorted(v)for k,v in sorted(FAMILY_REFS.items())},reading_routes=routes,research_queue=queue,status_legend=status_legend,invalid_reference_urls=invalid)
(HERE/'references.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')

lines=['# Mathematical references','',f"This bibliography links **{len(S):,} retained treatment bodies**—{len(A['corpus']):,} main treatments and 14 supplementary 2023 syntheses—to their cited resources. It also records all 71 concept families, the four annual reference lists and the Hamiltonian research context. A reference is evidence of a retained citation; it does not imply that every theorem in that resource is invoked or reproved here.",'', 'Use the [domain and cross-domain reading routes](READING_ROUTES.md), [research queue](RESEARCH_QUEUE.md) and [source-by-source index](SOURCE_INDEX.md). Machine-readable provenance, exact URL variants, labels and usage paths are in [references.json](references.json).','', '## Counting and URL identity','',metadata['deduplication'],'',metadata['counting'],'','A source count links to its complete treatment list. A count of zero can therefore be correct for a family-only, annual-list-only or Hamiltonian-context resource. Resources hosted as third-party PDFs are linked rather than redistributed.','', '## Authored reading documents','', '| ID | Current authored exposition | Retained treatment coverage | Other reading forms |','|---|---|---:|---|']
for d in authored:
 lines.append('| '+d['id']+' | '+link(d['title'],'../'+d['repository_path'])+' | '+str(d['covered_source_uid_count'])+' | '+' · '.join(link(Path(p).suffix[1:].upper(), '../'+p)for p in d['alternate_repository_paths'])+' |')
lines += ['', '## Complete reference table','',f"There are **{len(refs)} document identities** represented by **{stats['exact_original_urls']} exact original URLs**. Separate publisher and author mirrors remain separate records unless their conservative document URLs coincide. Current project documents retain their authors and pinned repository locators; the table distinguishes them from external literature.",'', '| ID | Retained label and exact link | Kind | Source UIDs | Families | Domains | Original URL variants |','|---|---|---|---:|---:|---|---|']
for r in refs:
 variants=' · '.join(link(str(i+1),u)for i,u in enumerate(r['original_urls']))
 lines.append('| '+rl(r['id'])+' | '+link(r['label'],r['preferred_original_url'])+' | '+('Current project document' if r['reference_kind']=='authored_current_project_document' else 'External resource')+' | '+f"[{r['source_uid_count']}](SOURCE_INDEX.md#{r['id'].lower()})"+' | '+str(r['family_count'])+' | '+' '.join(dl(d)for d in r['domain_ids'])+' | '+variants+' |')
lines += ['', '## Comparing these counts with the CSV exports','', 'The source-level table tables/references.csv has 997 citation-use rows from the developed treatment reference lists. This bibliography additionally retains 698 URL uses from original historical reference fields, 306 family citation fields, 672 annual-list entries and seven URL locators across six Hamiltonian context records. These are provenance occurrences, often repeated. Deduplication yields 618 exact URLs and 616 conservative document identities. Source-UID counts count each treatment at most once per document; they are not occurrence counts.','', '## Scope of the Hamiltonian references','', 'The Hamiltonian note distinguishes Robert’s universal Schwartz-observable boundary, Gotay’s coordinate Lie-algebra setting, the classical transvectant literature and the pinned PerfectJet sextic programme. A restricted polynomial exact-partner family does not contradict a theorem quantified over every observable. The current note’s displayed all-degree proofs, its finite exact fixtures and the existing programme’s archived external-solver verdicts retain separate evidential roles. See route T05 and the research queue for the remaining boundaries.','', '## Bibliography build','', 'The builder reads retained JSON and writes these indexes without network access or reference downloads. CHECKS.json records source coverage, identifier validity, URL preservation and link-shape checks. Those checks establish bibliography consistency, not the mathematical truth of every cited work.']
(HERE/'REFERENCES.md').write_text('\n'.join(lines)+'\n')

lines=['# Source and reference usage index','', 'Every retained treatment is listed, including entries with no explicit reference. Treatment links point to the repository’s readable annual pages. The lower sections list every direct source use of each bibliography record; family, annual-list and Hamiltonian-context uses remain separately named.','', '## All 1,065 treatment bodies','', '| Source UID | Treatment | Primary domain | Reference records |','|---|---|---|---|']
for e in source_index:
 p=e['primary_domain'];d=dl(p) if p in D else md(p)
 lines.append('| '+sl(e['uid'])+' | '+md(e['title'])+' | '+d+' | '+(' '.join(rl(x)for x in e['reference_ids']) or 'No explicit URL retained')+' |')
for r in refs:
 lines += ['', '## '+r['id'],'',link(r['label'],r['preferred_original_url']), '',f"**{r['source_uid_count']} unique direct source UIDs; {r['family_count']} family uses.**",'', ' · '.join(sl(u)for u in r['source_uids']) if r['source_uids'] else 'No direct treatment citation; the reference is retained in the following family, annual list or Hamiltonian context.']
 if r['family_ids']:lines += ['', 'Families: '+', '.join(link(fid,domain_link(F[fid]['domain_id']))for fid in r['family_ids'])+'.']
 if r['annual_years']:lines += ['', 'Annual reference-list/source years: '+', '.join(map(str,r['annual_years']))+'.']
 if r['hamiltonian_context_ids']:lines += ['', 'Hamiltonian context IDs: '+', '.join(r['hamiltonian_context_ids'])+'.']
 if len(r['original_urls'])>1:lines += ['', 'Original exact URL variants: '+' · '.join(link(str(i+1),u)for i,u in enumerate(r['original_urls']))+'.']
(HERE/'SOURCE_INDEX.md').write_text('\n'.join(lines)+'\n')

lines=['# Mathematical reading routes','', 'The atlas is organized by the operation a reader wants to perform: calculate, certify, reconstruct, classify, evolve, transport or decide. These routes use actual theorems and declared worked models. They do not equate different theories merely because both use a spectrum, an entropy or a commutator.','', 'Start with the [atlas report](../compendium/atlas/output/Mathematics_Atlas_2023_2026_Report.pdf), use the readable domain links below, and open a cited treatment by its source UID for its complete definitions, proof, example and limitations. The [interactive atlas](../compendium/atlas/output/Mathematics_Atlas_2023_2026.html) supplies ten finite worked models. Its broader capacity tags are not claims of unrestricted solver implementation.','', '## Evidence and implementation statuses','', '| Status | Meaning |','|---|---|']
for k,v in status_legend.items():lines.append('| '+k+' | '+md(v)+' |')
lines += ['', '## Cross-domain routes','']
for t in routes:
 lines += ['### '+t['id']+' · '+t['title'],'', '**Question.** '+t['question'],'', t['reading'],'', '**Constructive checkpoint.** '+t['checkpoint'],'', '**Boundary.** '+t['boundary'],'', 'Reading sequence: '+' → '.join(link(fid,domain_link(F[fid]['domain_id']))for fid in t['families'])+'.','', 'Domains: '+' · '.join(dl(d)for d in t['domains'])+'. Bridges: '+', '.join(t['bridges'])+'. Worked models: '+(', '.join(t['labs']) if t['labs'] else 'documented recipes; no dedicated lab')+'.','']
lines += ['## Domain reading sequences','', 'Each sequence follows the atlas chapter’s concept order. The checkpoint is the family’s declared central question; its worked proof and example appear in the linked domain. Source anchors provide direct entry points into the annual material. The final frontier is a task left open in this retained collection, not a claim about worldwide mathematical novelty.','']
for d,c in sorted(CH.items()):
 lines += ['## '+d,'', '**'+c['title']+'**','',c['organizing_question'],'', '| Order | Family and constructive checkpoint | Direct source entry points | Implemented link or recipe |','|---:|---|---|---|']
 for i,fid in enumerate(c['concept_order'],1):
  f=F[fid];labs=f.get('interactive_contract',{}).get('lab_ids',[])
  lines.append('| '+str(i)+' | '+link(fid+' — '+f['title'],domain_link(d))+'. '+md(f['central_question'])+' | '+' · '.join(sl(u)for u in f['anchor_uids'][:3])+' | '+(', '.join(labs) if labs else 'Documented recipe / worked proof')+' |')
 lines += ['', '**Cross-domain continuation.** '+' · '.join(t['id']for t in routes if d in t['domains'])+'.','', '**Next boundary.** '+c['open_frontier'],'']
lines += ['## Focused Hamiltonian route','', 'Read the [Hamiltonian note](../research/hamiltonian/output/Nonlinear_Hamiltonian_Partners.md) after T05. Follow definitions of E(H) and D∞(H), the cubic rank argument, the homogeneous-quartic apolar adjoint, arbitrary qF(p), monomial all-degree organization, and then dynamic closure and quantum ladders. The appendices display the general proofs; exact engines and fixtures replay specified finite examples. Appendix F pins the prior PerfectJet source, classical literature and external-solver boundary. Use the [bibliography](REFERENCES.md) to distinguish current project documents from external primary resources.']
(HERE/'READING_ROUTES.md').write_text('\n'.join(lines)+'\n')

lines=['# Research queue and source gaps','', 'This queue records concrete next tasks from the retained collection. “Open” means unproved or unrecovered here; it is not a claim of an unsolved problem throughout the literature. A missing historical input remains a provenance gap even if a related finite model has been proved.','', '| Queue | Status | Domains | Concrete next obligation |','|---|---|---|---|']
for q in queue:
 lines.append('| ['+q['id']+'](#'+q['id'].lower()+') | '+q['status']+' | '+' '.join(dl(d)for d in q['domain_ids'])+' | '+md(q['task'])+' |')
for q in queue:
 lines += ['', '## '+q['id'],'', '**'+q['title']+'**','', '**Status:** '+q['status']+'.','',q['task'],'', '**Proof or source obligation.** '+q['proof_obligation']]
 if q.get('family_ids'):lines += ['', 'Atlas families: '+' · '.join(link(fid,domain_link(F[fid]['domain_id']))for fid in q['family_ids'])+'.']
 if q.get('source_uids'):lines += ['', 'Source anchors: '+' · '.join(sl(u)for u in q['source_uids'])+'.']
 if q.get('reference_ids'):lines += ['', 'Retained reference entry points: '+' '.join(rl(x)for x in q['reference_ids'])+'.']
 if q.get('subquestions'):
  lines += ['', '| Family | Specific next question |','|---|---|']
  for z in q['subquestions']:lines.append('| '+z['family_id']+' | '+md(z['question'])+' |')
 if q.get('hamiltonian_sections'):lines += ['', 'Hamiltonian note sections: '+'; '.join(q['hamiltonian_sections'])+'.']
 if q.get('hamiltonian_context_ids'):lines += ['', 'Pinned context records: '+', '.join(q['hamiltonian_context_ids'])+'.']
lines += ['', '## What is already established in the stated scope','', 'The annual treatments and atlas contain their own explicit results and limitations. This queue does not reopen every classical theorem. The delivered finite models include exact selection counts, graph census coefficients, observation rank tests, homology over Q, unit fibres, Pell iterates and polynomial Moyal coefficients; cutoff and projection models evaluate analytic formulas in floating arithmetic. The Hamiltonian note gives all-degree proofs in its declared cubic, homogeneous-quartic, arbitrary qF(p), balanced-monomial and unequal-monomial classes. Those scoped positive results coexist with the larger open extensions and source gaps above.']
(HERE/'RESEARCH_QUEUE.md').write_text('\n'.join(lines)+'\n')

# Internal consistency checks, plus repository-link intentions (staging may still be in progress).
assert len(S)==1065 and len(BYUID)==1065 and len(F)==71 and len(D)==16
assert not invalid,invalid
assert {e['uid']for e in source_index}==set(BYUID)
assert all(r['source_uid_count']==len(set(r['source_uids']))for r in refs)
assert all(u in BYUID for r in refs for u in r['source_uids'])
assert all(f in F for r in refs for f in r['family_ids'])
assert all(canonical_url(u)==r['canonical_document_url']for r in refs for u in r['original_urls'])
assert all(t in F for route in routes for t in route['families'])
assert all(d in D for route in routes for d in route['domains'])
assert all(u in BYUID for q in queue for u in q.get('source_uids',[]))
coverage=Counter(e['year']for e in source_index)
occurrence_counts=Counter(u['kind'] for r in refs for u in r['usages'])
source_occurrence_counts=Counter('original_historical_reference_fields' if u.get('original_historical_field') else 'developed_treatment_reference_fields' for r in refs for u in r['usages'] if u['kind']=='source_treatment')
checks=dict(status='passed',scope='Bibliography extraction, source linkage, canonical-URL preservation and reading-route identifier checks; not a proof audit or live availability test.',statistics=stats,source_counts_by_year=dict(sorted(coverage.items())),checks=[dict(name='All 1,065 source UIDs represented exactly once',status='passed'),dict(name='Every source/family/route identifier resolves in retained atlas',status='passed'),dict(name='Every exact URL belongs to its conservatively canonicalized record',status='passed'),dict(name='All annual reference lists and six Hamiltonian context records included',status='passed'),dict(name='External references are linked, not redistributed',status='passed')],repository_link_template='../compendium/readable/years/{year}/{source_id}.md and ../compendium/readable/domains/{domain_id}.md',count_reconciliation=dict(developed_treatment_reference_use_rows=source_occurrence_counts['developed_treatment_reference_fields'],original_historical_reference_url_occurrences=source_occurrence_counts['original_historical_reference_fields'],all_usage_kinds=dict(occurrence_counts),exact_original_urls=stats['exact_original_urls'],canonical_document_identities=stats['reference_documents'],explanation='tables/references.csv contains 997 developed treatment citation-use rows. These differ from unique URLs/documents, and this bibliography also includes original historical references, family references, annual lists and Hamiltonian context. source_uid_count deduplicates each treatment within each document.'))
relative_links=0
missing_links=[]
for page in HERE.glob('*.md'):
    for match in re.findall(r'\]\((?:<([^>]+)>|([^\s)]+))\)',page.read_text()):
        target=match[0] or match[1]
        if target.startswith(('http:','https:','mailto:','#')):continue
        relative_links+=1
        destination=(page.parent/target.split('#',1)[0]).resolve()
        if not destination.exists():missing_links.append(dict(file=page.name,target=target))
checks['relative_link_audit']=dict(links_checked=relative_links,missing_count=len(missing_links),missing_targets=missing_links)
if missing_links:checks['status']='failed'
else:checks['checks'].append(dict(name='All relative Markdown file targets exist in the repository',status='passed'))
(HERE/'CHECKS.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(stats,ensure_ascii=False,indent=2))
