"""Build both self-contained editions from the month files; no network required."""
from pathlib import Path
from datetime import datetime,timezone
from collections import Counter
import argparse,base64,html,json,re,unicodedata
from common import ROOT,MONTHS,load,collect_refs,prose_words

OUT=ROOT/'output';OUT.mkdir(exist_ok=True)
TITLE='2026 Mathematics, Rebuilt Month by Month'
STEM='2026_Month_by_Month_Mathematics'
MONTH_NOTES={'01': 'Mechanics, vorticity geometry, discriminants, semantic quotients, resonance arithmetic and stochastic generators supply the opening questions. The developments derive explicit models and preserve the hypotheses needed for each comparison.', '02': 'Random filtrations, compatibility witnesses, ultrametric spaces, exponential categories, Hill equations and inverse-limit towers recur. Finite calculations and counterexamples make the assumptions visible.', '03': 'Lyapunov forms, resolvents, entropy, local germs and bifurcations connect operator theory to dynamics. Jet data are tested with their stated precision, and local certificates are separated from global claims.', '04': 'Graph circulation, transport and cohomology, least-squares gauges, invariant manifolds, ordered groups and exact incidence organize the month. Definitions resolve ambiguities before stronger conclusions are drawn.', '05': 'Constructive calculus, homological perturbation, quotient energy, symbolic pressure, coercivity, gauge models and symplectic reduction are developed through concrete finite and analytic examples.', '06': 'Finite Weyl systems, quadratic modules, weighted path sums, knot number fields, lattice geometry and deformation products provide exact arithmetic and algebraic test cases. Missing geometric bridges remain explicit questions.', '07': 'Spectral rigidity, jets and resolutions lead into Pauli sectors, cubic arithmetic, symmetry and observation. The entries give exact finite models where the recovered large-instance data are unavailable.', '08': 'Controlled approximation, descriptor systems, topology, deformation, finite geometry, deployment symmetries and frontier optimization become a dense program of preserving structure under approximation and reduction.', '09': 'Continuation equivalence, finite operator algebras, Hankel support, target-relative information, exact arithmetic and completeness certificates connect finite computation to provable reductions.', '10': 'The partial month through 21 October includes norm equations, exact populations, cyclotomic and E8 structures, graph arithmetic, observation quotients and shared-uncertainty decisions. Historical implementation claims remain separate from the new mathematical proofs and finite replays.'}
INTRO=['This volume rebuilds mathematics recovered from conversations dated 1 January through 21 October 2026, month by month. Each developed treatment contains a newly revised question, definitions and hypotheses, a precise result, a proof or derivation, a worked example, limits and a further mathematical problem. Related source formulas may be grouped or developed separately where they ask distinct questions.', 'All ten elapsed months have dated mathematical evidence; October is a partial month. Recovery is bounded and fragmentary, rather than an exhaustive export of every historical message. Dates are retained in UTC when available. U identifies a retrieved user-attributed topic or passage; A identifies assistant-only evidence; T identifies a topic or secondary-source fragment. U does not by itself establish that an original prompt was recovered verbatim.', 'Historical evidence and the new mathematics are separate. Revised questions, proofs and stipulated examples are authored for this volume. Exact returned source excerpts and receipt locators are retained in the searchable edition and source bundle. Missing original operators, tables, data and proof files are not reconstructed as if their historical bytes were available. Recaps explicitly concerning earlier years are excluded as new 2026 topic evidence.', 'The scope is mathematics. Classical results, new expositions, exact finite certificates, numerical examples and open conjectures are distinguished. Claims about physical devices, model-training performance or major open problems require their own evidence; the mathematical developments here do not certify such claims. Supplied programs test their stated cases and do not replace written proofs.']

def esc(s):return html.escape(str(s),quote=True)
SYNTHESIS=['The strongest common question is: which distinctions must survive a reduction so that the intended mathematical question remains answerable? In finite-dimensional linear observation, a target Gx is determined by Hx exactly when ker H⊆ker G. The factor L defined by L(Hx)=Gx is well-defined under this condition, so G=LH; conversely that factorization immediately gives the kernel inclusion. For dynamics x′=Ax, an autonomous observed state additionally requires ker H to be A-invariant. These elementary criteria connect the year’s semantic quotients, operator reductions, finite-state continuation, target-relative information and October observation design.', 'The noisy version asks for a quantitative ambiguity bound rather than exact identification. For an admissible class M and noise level δ, compare the possible targets of x,z∈M satisfying ||H(x−z)||≤2δ. A small target diameter can justify a decision even when the full state is poorly determined. August’s approximation theorem controls one reconstruction by bias plus noise amplification; its polynomial and logarithmic rates are proved together with two-point lower bounds. In the severe case, a log-log safety margin matters: choosing the leading cutoff scale too aggressively can leave unit noise amplification. This makes approximation, information and the cost of a decision part of one explicit mathematical problem.', 'The graph example shows why changing the observation changes the answer. Two recovered seven-vertex graphs agree in all128 binary size-and-energy counts. Their first integer-height separation has total height3, with exact difference q³(1−q)(1−q³)²(1−q⁴)². It is11025/262144 atq=1/2. Thus a complete finite census for one observation can still discard a distinction visible to a richer observation. The independent certificate in this edition enumerates both the binary populations and the required weak compositions.', 'The arithmetic develops equally concrete positive results. The corrected degree φ(1680)=384 gives48 primitive conductor1680 phases above each of the8 primitive conductor30 phases. An exact Bernoulli-polynomial sum also reproduces the October phase-log integral coefficient955/867. Such identities provide real arithmetic structure, while an E8 lattice comparison, a monodromy closure, a large counting implementation or an accepted-output state decoder still requires its own specified map and proof. The most fruitful continuation is to choose one target, state exactly what observations determine it, and optimize the least additional information required to settle it.', 'A particularly strong new certificate concerns the recovered FreeLIP recurrence xᵢ₊₁=Axᵢ modulo(2^107−1), observed through26-bit raw words. Equality of five selected outputs forces a vector into a known integer lattice and a small coordinate box. For all126five-position subsets of nine steps, the checked lattice basis and its rational inverse force every integer coefficient to have absolute value below3/8, hence to be zero. This proves all-state uniqueness, not only successful sample decoding. The resulting exact decoder gives one-error correction from seven words and two-error correction from nine, with optimal length proved by puncturing. Rejection-sampled accepted outputs require a separate result.']

def paras(text):return ''.join('<p>'+esc(x.strip())+'</p>' for x in re.split(r'\n\s*\n',str(text)) if x.strip())
def refs_for(e,refs):return [refs[r['url'].rstrip('/')]['key'] for r in e['references']]
def ledger():
    data=[]
    for path in sorted((ROOT/'months').glob('*/*checks.json')):
        r=json.loads(path.read_text())
        checks=r.get('checks',[]) if isinstance(r,dict) else r
        if isinstance(checks,list):
            data.extend(dict(c,month=path.parent.name,report=path.name) for c in checks)
    path=ROOT/'figure_checks.json'
    if path.exists():
        data.extend(dict(c,month='Illustrations',report=path.name) for c in json.loads(path.read_text()).get('checks',[]))
    path=ROOT/'independent_checks.json'
    if path.exists():
        data.extend(dict(c,month='Independent audit',report=path.name) for c in json.loads(path.read_text()).get('checks',[]))
    path=ROOT/'freelip_checks.json'
    if path.exists():data.extend(dict(c,month='Independent audit',report=path.name)for c in json.loads(path.read_text()).get('checks',[]))
    unique=[];seen=set()
    for c in data:
        key=(c['month'],json.dumps(c.get('id',c.get('ids','')),sort_keys=True),c.get('name',c.get('check','Check')))
        if key not in seen:seen.add(key);unique.append(c)
    return unique
def check_status(c):
    return str(c.get('status','passed' if c.get('passed') else 'unspecified'))
def overview_status(m):
    return 'Source gap: no dated fragment recovered' if not m['entries'] else 'Dated fragments recovered; complete transcript unavailable'
def question_rows(part):
    return ''.join('<tr data-row-month="'+e['month_key']+'"><td><a href="#'+e['id']+'">'+e['id']+'</a><br>'+esc((e['original'].get('date') or 'Date unavailable')[:10])+' · '+e['original']['evidence']+'</td><td><strong>'+esc(e['title'])+'</strong><br><span class="small">'+esc(e['original'].get('field','Mathematics'))+'</span></td><td>'+esc(e['original']['question'])+'</td><td><strong>'+esc(e['result']['name'])+'</strong><br>'+esc(e['result']['statement'])+'</td></tr>' for e in part)
def article(e,refs):
    o=e['original']
    source='<details><summary>Recovered source and attribution</summary>'+paras(o.get('source_excerpt',''))+paras(o.get('attribution_note',''))+'<p class="small">Source receipt: '+esc(o['retrieval_receipt'])+'. Original user question: '+esc(o.get('original_question') or 'not recovered verbatim')+'</p></details>'
    body=f'<article id="{e["id"]}" data-month="{e["month_key"]}"><p class="meta">{e["id"]} · {esc(o.get("date") or "Date unavailable")} · historical evidence {o["evidence"]}</p><h3>{esc(e["title"])}</h3><p class="status">{esc(e["status"])}</p>{source}<section class="question"><h4>Revised question</h4>{paras(o["question"])}</section>{paras(e["summary"])}<h4>Definitions and assumptions</h4>'
    body+=''.join(paras(d) for d in e['definitions'])
    body+='<section class="theorem"><h4>'+esc(e['result']['name'])+'</h4>'+paras(e['result']['statement'])+'</section><h4>Derivation or proof</h4>'+paras(e['result']['proof'])
    body+='<section class="example"><h4>Worked example</h4>'+''.join(paras(e['example'][k]) for k in ['setup','calculation','conclusion'])+'</section><h4>Scope</h4>'+paras(e['limits'])+'<h4>Further development</h4>'+paras(e['extension'])
    if e['references']:body+='<p class="small">Mathematical references: '+' '.join('<a href="#'+k+'">'+k+'</a>' for k in refs_for(e,refs))+'</p>'
    body+='</article>'
    return body

def build_html(months,entries,refs,checks):
    counts=Counter(e['original']['evidence'] for e in entries)
    coverage=''.join('<tr><td><a href="#month-'+m['key']+'">'+m['name']+'</a></td><td>'+str(len(m['entries']))+'</td><td>'+str(m['evidence_counts'].get('U',0))+' / '+str(m['evidence_counts'].get('A',0))+' / '+str(m['evidence_counts'].get('T',0))+'</td><td>'+str(m['retrieval_calls'])+'</td><td>'+overview_status(m)+'</td></tr>' for m in months)
    sections=''
    for m in months:
        sections+='<section class="month-section" id="month-'+m['key']+'"><h2>'+m['name']+' 2026</h2><p class="month-summary">'+overview_status(m)+'. '+str(len(m['entries']))+' developed treatments.</p>'+paras(MONTH_NOTES[m['key']])
        if m['entries']:
            sections+='<details class="month-table"><summary>Revised questions and developed results for '+m['name']+'</summary><div class="scroll"><table><thead><tr><th>ID · source date</th><th>Concept and field</th><th>Revised question</th><th>Result and mathematical core</th></tr></thead><tbody>'+question_rows(m['entries'])+'</tbody></table></div></details>'
            sections+=''.join(article(e,refs) for e in m['entries'])
        else:sections+='<div class="gap"><p>No source-supported treatment is available for this section. Search coverage does not establish historical absence.</p></div>'
        sections+='</section>'
    checkrows=''
    for c in checks:
        detail=c.get('detail',c.get('details',c.get('scope','')))
        if not isinstance(detail,str):detail=json.dumps(detail,ensure_ascii=False)
        checkrows+='<tr><td>'+c['month']+'</td><td>'+esc(c.get('id',c.get('ids','')) )+'</td><td>'+esc(c.get('name',c.get('check','Check')))+'</td><td>'+esc(check_status(c))+'</td><td>'+esc(detail)+'</td></tr>'
    references=''.join('<tr id="'+r['key']+'"><td>'+r['key']+'</td><td><a href="'+esc(r['url'])+'" target="_blank" rel="noopener">'+esc(r['label'])+'</a><br><span class="small">'+esc(r['url'])+'</span></td></tr>' for r in refs.values())
    figures=''
    figmeta=ROOT/'figures'/'figures.json'
    if figmeta.exists():
        for f in json.loads(figmeta.read_text()):
            p=ROOT/'figures'/f['file']
            figures+='<figure><img alt="'+esc(f['caption'])+'" src="data:image/png;base64,'+base64.b64encode(p.read_bytes()).decode()+'"><figcaption>'+esc(f['caption'])+'</figcaption></figure>'
    nav=''.join('<a href="#month-'+m['key']+'">'+m['name']+' <span>'+str(len(m['entries']))+'</span></a>' for m in months)
    doc='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'''+TITLE+'''</title><style>
:root{--ink:#1e2d39;--blue:#23536f;--muted:#5f7180;--line:#d7e1e7}*{box-sizing:border-box}body{margin:0;background:#eff3f5;color:var(--ink);font:16px/1.72 system-ui,Segoe UI,sans-serif}a{color:var(--blue);text-underline-offset:3px}header{padding:55px max(24px,calc((100vw - 1240px)/2));background:#15384d;color:white}header p{max-width:1000px;font-size:19px;color:#dceaf0}h1{font-size:clamp(34px,4.6vw,58px);line-height:1.12;letter-spacing:-1.2px;max-width:1100px}.eyebrow{font-size:12px;letter-spacing:1.6px;text-transform:uppercase;color:#bbdbe7}main{max-width:1240px;margin:auto;padding:25px 22px 70px}.intro,article,.gap{padding:24px 30px;background:white;border:1px solid var(--line);border-radius:7px}.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:18px 0}.stats div{background:white;border:1px solid var(--line);padding:14px 20px;border-radius:6px}.stats b{display:block;font-size:30px;color:var(--blue)}.stats span{font-size:12px;color:var(--muted)}nav{display:grid;grid-template-columns:repeat(4,1fr);gap:8px 20px;margin:22px 0}nav a{padding:4px 0}nav span{font-size:12px;color:var(--muted);margin-left:6px}.toolbar{display:flex;flex-wrap:wrap;gap:10px;position:sticky;top:0;background:white;border:1px solid var(--line);padding:13px;z-index:5;border-radius:6px}input,select,button{font:inherit;padding:9px;border:1px solid #b7c9d4;background:white;color:var(--ink);border-radius:4px}input{flex:1;min-width:230px}button{cursor:pointer}.small,.meta,figcaption{font-size:12px;color:var(--muted)}h2{font-size:31px;color:#204a63;margin:43px 0 16px}h3{font-size:26px;line-height:1.25;margin:8px 0 13px;letter-spacing:-.4px}h4{font-size:14px;color:#315a73;margin:20px 0 7px}article{margin:22px 0}article p{overflow-wrap:anywhere}.meta{margin:0}.status{font-size:12px;color:#426a60}.question{border-bottom:1px solid var(--line);padding-bottom:7px}.theorem{background:#edf5fa;border-left:4px solid #367ca0;padding:1px 20px 8px;margin:20px 0}.example{background:#f5f7f8;border-left:4px solid #bfd0db;padding:1px 20px 8px;margin:20px 0}details{background:white;border:1px solid var(--line);padding:14px 18px;border-radius:5px;margin:15px 0}summary{font-size:14px;font-weight:650;cursor:pointer}.scroll{overflow:auto;margin-top:15px}table{width:100%;border-collapse:collapse;background:white;font-size:12px;line-height:1.6}td,th{padding:10px 12px;border:1px solid var(--line);vertical-align:top;text-align:left;overflow-wrap:anywhere}th{background:#e5eef3}figure{background:white;padding:22px;border:1px solid var(--line);margin:24px 0}figure img{width:100%;height:auto}figcaption{padding-top:10px}.hidden{display:none!important}[id]{scroll-margin-top:100px}footer{font-size:12px;color:var(--muted);margin-top:35px}
@media(max-width:750px){header{padding:32px 22px}main{padding:18px 12px}.stats{grid-template-columns:1fr 1fr}nav{grid-template-columns:1fr 1fr}article,.intro{padding:20px}h3{font-size:23px}.toolbar{position:static}}
@media print{@page{size:A4;margin:18mm}body{background:white;font-size:11px}header{background:white;color:black;padding:0}header p,.eyebrow{color:#333}h1{font-size:30px}main{max-width:none;padding:0}.toolbar,nav,.stats,details,.small#visible-count{display:none!important}article,.intro{border:0;padding:0}h2{break-before:page;font-size:24px}h3{font-size:19px;break-after:avoid}h4{break-after:avoid}.hidden{display:none!important}}
</style></head><body><header><div class="eyebrow">Mathematics recovered from January–21 October 2026</div><h1>'''+TITLE+'''</h1><p>Revised questions, precise statements, proofs, examples and reproducible checks, organized by source month.</p></header><main><div class="intro">'''+''.join(paras(x) for x in INTRO)+'''</div><section class="intro"><h2>The mathematical thread</h2>'''+''.join(paras(x)for x in SYNTHESIS)+'''</section><div class="stats"><div><b>'''+str(len(entries))+'''</b><span>developed treatments</span></div><div><b>10</b><span>month sections with recovered material</span></div><div><b>'''+str(prose_words(entries))+'''</b><span>words of mathematical development</span></div><div><b>'''+str(len(refs))+'''</b><span>distinct mathematical references</span></div></div><h2 id="coverage">Month-by-month source coverage</h2><p class="small">U / A / T count treatments by evidence label, not conversations. Search calls do not measure transcript completeness.</p><div class="scroll"><table><thead><tr><th>Month</th><th>Treatments</th><th>U / A / T</th><th>Recovery calls</th><th>Historical coverage</th></tr></thead><tbody>'''+coverage+'''</tbody></table></div><nav>'''+nav+'''<a href="#complete-table">Complete revised-question table</a><a href="#verification">Verification ledger</a><a href="#references">References</a></nav><div class="toolbar"><input id="search" type="search" aria-label="Search all mathematical treatments" placeholder="Search a formula, concept, question or entry ID"><select id="month-filter" aria-label="Filter month"><option value="">All months</option>'''+''.join('<option value="'+m['key']+'">'+m['name']+'</option>' for m in months)+'''</select><button id="reset">Reset</button><button id="print">Print visible treatments</button></div><p class="small" id="visible-count">'''+str(len(entries))+''' treatments shown</p>'''+sections+'''<h2 id="complete-table">Complete revised-question table</h2><details><summary>Open all revised questions and developed results</summary><div class="scroll"><table><thead><tr><th>ID · source date</th><th>Concept and field</th><th>Revised question</th><th>Result and mathematical core</th></tr></thead><tbody>'''+question_rows(entries)+'''</tbody></table></div></details>'''+('<h2>Calculated illustrations</h2>'+figures if figures else '')+'''<h2 id="verification">Verification ledger</h2><p>The source package replays the supplied scripts offline with Python 3.10 or newer. This ledger includes provenance/schema checks as well as exact and numerical mathematical examples. Its records do not replace the written proofs or the cited literature. Each script states what it tests.</p><div class="scroll"><table><thead><tr><th>Month</th><th>Entry</th><th>Check</th><th>Status</th><th>Scope and retained output</th></tr></thead><tbody>'''+checkrows+'''</tbody></table></div><h2 id="references">Mathematical references</h2><p>These sources support the mathematical background and stated literature dependencies. A citation does not validate an unspecified bridge to an application.</p><table><thead><tr><th>Key</th><th>Reference</th></tr></thead><tbody>'''+references+'''</tbody></table><footer>The source bundle retains entry data, coverage reports and the mathematical verification programs. Newly written questions are reconstructions; unavailable original prompts remain unavailable.</footer></main><script>
const articles=[...document.querySelectorAll('article')];
function filter(){let q=document.getElementById('search').value.trim().toLocaleLowerCase(),m=document.getElementById('month-filter').value,n=0;for(let a of articles){let yes=(!q||a.textContent.toLocaleLowerCase().includes(q))&&(!m||a.dataset.month===m);a.classList.toggle('hidden',!yes);if(yes)n++}for(let s of document.querySelectorAll('.month-section')){let own=[...s.querySelectorAll('article')],show=(!m||s.id==='month-'+m)&&(!own.length?!q:own.some(x=>!x.classList.contains('hidden')));s.classList.toggle('hidden',!show)}for(let row of document.querySelectorAll('tr[data-row-month]')){let yes=(!m||row.dataset.rowMonth===m)&&(!q||row.textContent.toLocaleLowerCase().includes(q));row.classList.toggle('hidden',!yes)}document.getElementById('visible-count').textContent=n+' of '+articles.length+' treatments shown'}
document.getElementById('search').addEventListener('input',filter);document.getElementById('month-filter').addEventListener('change',filter);document.getElementById('reset').addEventListener('click',()=>{document.getElementById('search').value='';document.getElementById('month-filter').value='';filter()});document.getElementById('print').addEventListener('click',()=>window.print());
</script></body></html>'''
    path=OUT/(STEM+'.html');path.write_text(doc,encoding='utf-8');return path

def build_pdf(months,entries,refs,checks):
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.lib import colors
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,PageBreak,Table,TableStyle,CondPageBreak,KeepTogether,Image
    for name,file in [('DV','DejaVuSans.ttf'),('DVB','DejaVuSans-Bold.ttf')]:
        pdfmetrics.registerFont(TTFont(name,'/usr/share/fonts/truetype/dejavu/'+file))
    pdfmetrics.registerFontFamily('DV',normal='DV',bold='DVB',italic='DV',boldItalic='DVB')
    ink=colors.HexColor('#1c2d39');blue=colors.HexColor('#214f6b');muted=colors.HexColor('#5c7180')
    styles={
      'title':ParagraphStyle('title',fontName='DVB',fontSize=32,leading=40,textColor=blue,spaceAfter=24),
      'sub':ParagraphStyle('sub',fontName='DV',fontSize=14,leading=21,textColor=muted,spaceAfter=20),
      'h1':ParagraphStyle('h1',fontName='DVB',fontSize=24,leading=31,textColor=blue,spaceAfter=20,keepWithNext=True),
      'h2':ParagraphStyle('h2',fontName='DVB',fontSize=16,leading=22,textColor=blue,spaceBefore=16,spaceAfter=11,keepWithNext=True),
      'label':ParagraphStyle('label',fontName='DVB',fontSize=9.4,leading=14,textColor=blue,spaceBefore=12,spaceAfter=5,keepWithNext=True),
      'body':ParagraphStyle('body',fontName='DV',fontSize=9.5,leading=14.4,textColor=ink,spaceAfter=9,allowWidows=0,allowOrphans=0),
      'small':ParagraphStyle('small',fontName='DV',fontSize=7.8,leading=11.6,textColor=muted,spaceAfter=8),
      'cell':ParagraphStyle('cell',fontName='DV',fontSize=7.3,leading=10.6,textColor=ink),
      'theorem':ParagraphStyle('theorem',fontName='DV',fontSize=9.5,leading=14.4,textColor=ink,spaceAfter=10,leftIndent=10,rightIndent=8,borderPadding=8,backColor=colors.HexColor('#edf4f8'))
    }
    glyphs=pdfmetrics.getFont('DV').face.charWidths; replacements={}
    def xml(value):
        value=str(value).replace('\u2011','-').replace('\u2013','-').replace('\u2014','-')
        for c,rep in {'〈':'⟨','〉':'⟩'}.items():
            if c in value:replacements[c]=rep;value=value.replace(c,rep)
        chars=[]
        for c in value:
            if ord(c)>31 and ord(c) not in glyphs:
                norm=unicodedata.normalize('NFKD',c)
                if norm!=c and all(ord(x) in glyphs for x in norm):replacements[c]=norm;chars.append(norm)
                else:raise ValueError('Unsupported PDF glyph '+repr(c)+' '+hex(ord(c)))
            else:chars.append(c)
        return html.escape(''.join(chars)).replace('\n','<br/>')
    def para(s,style='body'):return Paragraph(xml(s),styles[style])
    story=[]
    def text(s,style='body'):
        for t in re.split(r'\n\s*\n',str(s)):
            if t.strip():story.append(para(t.strip(),style))
    def label(s):text(s,'label')
    def table(rows,widths):
        t=Table([[para(c,'cell') for c in row] for row in rows],colWidths=widths,repeatRows=1,hAlign='LEFT')
        t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e5eef4')),('GRID',(0,0),(-1,-1),.4,colors.HexColor('#cedbe3')),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7)]))
        story.append(t)
    story.append(Spacer(1,52));text(TITLE,'title');text(str(len(entries))+' developed treatments from ten elapsed months, through 21 October 2026.','sub')
    text('Mathematics-only retrospective · prepared 21 October 2026','small')
    for s in INTRO:text(s)
    story.append(PageBreak());text('The mathematical thread','h1')
    for s in SYNTHESIS:text(s)
    text('The searchable HTML edition provides complete question tables, month filtering and the full source summaries. The accompanying ZIP contains machine-readable entries and offline replay programs.','small')
    story.append(PageBreak());text('Month-by-month coverage','h1')
    table([['Month','Treatments','U / A / T','Source coverage']]+[[m['name'],str(len(m['entries'])),' / '.join(str(m['evidence_counts'].get(k,0)) for k in ['U','A','T']),overview_status(m)] for m in months],[74,62,68,295])
    story.append(Spacer(1,15));text('The counts measure developed treatments, not conversations. Related source formulas can be grouped in one treatment. Different treatments may develop distinct aspects of the same conversation. Source dates are not newly assigned publication dates.','small')
    text('How to read the edition','label');text('Each month begins with a revised-question table. The complete developments follow it in source-date order. The PDF outline links months and treatment identifiers. A is assistant-only evidence; U is user-attributed recovered content rather than a promise of exact original wording. The new mathematical question is always separate from the recovered starting point.')
    for m in months:
        story.append(PageBreak());text(m['name']+' 2026','h1')
        text(overview_status(m)+'. '+str(len(m['entries']))+' developed treatments.','small')
        text(MONTH_NOTES[m['key']])
        if not m['entries']:
            text('No dated mathematical fragment was recovered for this section. Its historical coverage remains open.')
            continue
        table([['ID · date','Concept and revised question','Result and mathematical core']]+[[e['id']+'\n'+str(e['original'].get('date') or 'date unavailable')[:10]+' · '+e['original']['evidence'],e['title']+'\n'+e['original']['question'],e['result']['name']+'\n'+e['original'].get('math','')] for e in m['entries']],[99,230,170])
        story.append(Spacer(1,15))
        for e in m['entries']:
            o=e['original'];story.append(CondPageBreak(160));text(e['id']+'  '+e['title'],'h2')
            text(str(o.get('date') or 'Date unavailable')+' · historical evidence '+o['evidence']+' · '+e['status'],'small')
            label('Recovered starting point');text(o.get('origin',o.get('source_excerpt','')),'small')
            label('Revised question');text(o['question'])
            text(e['summary']);label('Definitions and assumptions')
            for d in e['definitions']:text(d)
            label(e['result']['name']);text(e['result']['statement'],'theorem')
            label('Derivation or proof');text(e['result']['proof'])
            label('Worked example')
            for k in ['setup','calculation','conclusion']:text(e['example'][k])
            label('Scope');text(e['limits']);label('Further development');text(e['extension'])
            text('Source receipt: months/'+m['key']+'/'+o['retrieval_receipt']+'.'+(' Mathematical references: '+', '.join(refs_for(e,refs))+'.' if e['references'] else ''),'small')
    figmeta=ROOT/'figures'/'figures.json'
    if figmeta.exists():
        from PIL import Image as PILImage
        story.append(PageBreak());text('Calculated illustrations','h1')
        for f in json.loads(figmeta.read_text()):
            p=ROOT/'figures'/f['file'];im=PILImage.open(p);height=499*im.height/im.width
            story.append(KeepTogether([Image(str(p),width=499,height=height),para(f['caption'],'small'),Spacer(1,15)]))
    story.append(PageBreak());text('Verification ledger and scope','h1')
    text('The supplied programs replay exact finite calculations and scoped numerical examples. The ledger also includes source/schema checks, which are not mathematical theorem checks. Written proofs and general literature results retain the scopes stated in their treatments. The full retained details are in the HTML edition and JSON reports.')
    for m in months:
        label(m['name'])
        for c in checks:
            if c['month']==m['key']:text(str(c.get('id',c.get('ids','')))+' · '+str(c.get('name',c.get('check','Check')))+' · '+check_status(c),'small')
    label('Calculated illustrations')
    for c in checks:
        if c['month']=='Illustrations':text(str(c.get('name',''))+' · '+check_status(c),'small')
    label('Independent exact audit')
    for c in checks:
        if c['month']=='Independent audit':text(str(c.get('name',''))+' · '+check_status(c),'small')
    story.append(PageBreak());text('Mathematical references','h1')
    for r in refs.values():
        label(r['key']+'  '+r['label'])
        story.append(Paragraph('<link href="'+html.escape(r['url'],quote=True)+'" color="#23536f">'+xml(r['url'])+'</link>',styles['small']))
    path=OUT/(STEM+'.pdf')
    working_path=OUT/(STEM+'.building.pdf')
    class Doc(SimpleDocTemplate):
        def afterFlowable(self,flowable):
            if isinstance(flowable,Paragraph) and flowable.style.name in ['h1','h2']:
                key='heading-'+str(self.seq.nextf('outline'));self.canv.bookmarkPage(key)
                self.canv.addOutlineEntry(flowable.getPlainText(),key,level=0 if flowable.style.name=='h1' else 1,closed=True)
    def decorate(c,d):
        c.saveState();w,h=A4;c.setStrokeColor(colors.HexColor('#d5e1e8'));c.setLineWidth(.5);c.line(48,h-35,w-48,h-35);c.setFont('DV',7.2);c.setFillColor(muted);c.drawString(48,h-26,'2026 MATHEMATICS, REBUILT MONTH BY MONTH');c.drawString(48,25,'Revised questions · proofs · examples · explicit source coverage');c.drawRightString(w-48,25,str(d.page));c.restoreState()
    doc=Doc(str(working_path),pagesize=A4,leftMargin=48,rightMargin=48,topMargin=53,bottomMargin=48,title=TITLE,author='Mathematical development of the recovered 2026 conversations')
    doc.build(story,onFirstPage=decorate,onLaterPages=decorate)
    assert working_path.stat().st_size>10000
    working_path.replace(path)
    (OUT/'glyph_normalizations.json').write_text(json.dumps(replacements,ensure_ascii=False,indent=2))
    return path

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--draft',action='store_true');parser.add_argument('--html-only',action='store_true');args=parser.parse_args()
    months,entries=load(args.draft);refs=collect_refs(entries);checks=ledger()
    for m in months:m['editorial_overview']=MONTH_NOTES[m['key']]
    integrated=dict(title=TITLE,created_at=datetime.now(timezone.utc).isoformat(),scope=json.loads((ROOT/'SOURCE_SCOPE.json').read_text()),months=months,entries=entries,references=list(refs.values()),checks=checks)
    (ROOT/'compendium.json').write_text(json.dumps(integrated,ensure_ascii=False,indent=2))
    rows=[dict(id=e['id'],month=e['original']['month'],source_date=e['original'].get('date'),evidence=e['original']['evidence'],concept=e['title'],field=e['original']['field'],historical_origin=e['original'].get('origin'),original_question=e['original'].get('original_question'),revised_question=e['original']['question'],mathematical_core=e['original'].get('math'),result=e['result']['name'],developed_statement=e['result']['statement'],further_development=e['extension'],source_receipt=e['original']['retrieval_receipt']) for e in entries]
    (ROOT/'revised_questions.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
    h=build_html(months,entries,refs,checks);p=None if args.html_only else build_pdf(months,entries,refs,checks)
    print(json.dumps(dict(treatments=len(entries),prose_words=prose_words(entries),references=len(refs),ledger_records=len(checks),html=str(h),pdf=str(p) if p else None)))

if __name__=='__main__':main()
