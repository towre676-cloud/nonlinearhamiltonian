"""Build the HTML and PDF editions from the developed entry records."""
from pathlib import Path
from collections import Counter
import argparse, html, json, re, csv, hashlib, shutil, unicodedata, base64
from datetime import datetime,timezone

P=Path(__file__).resolve().parent
OUT=P/'output';OUT.mkdir(exist_ok=True)
CHAPTERS=[('a','Arithmetic nonassociative algebra and exact wave dynamics',1,18),('b','Harmonic analysis graph invariants and arithmetic geometry',19,37),('c','Representations geometric phases and dynamical models',38,56),('d','Probability control relativity and foundations',57,77),('e','Analysis geometry and computational certificates',78,99),('f','Singularities integrable systems and quantum field mathematics',100,114)]
FIGURES={
 'S002':('gudermannian_information.png','Exact reversible observations preserve Fisher information. Finite uniform angle bins lose information in a distribution-dependent way. Curves evaluate Gaussian bin probabilities directly; they are illustrative floating-point calculations.'),
 'S011':('heat_observation_tradeoff.png','The optimal time for separating one aligned graph pair differs from the time minimizing a full-kernel inverse-error bound. The left margin has exact maximum 1/16; the right normalized bound has exact minimum e. These are distinct objectives.'),
 'S013':('gaudin_spectral_cover.png','Numerical continuation of the exact quadratic Bethe-root formula around a simple discriminant point exchanges the two root labels. This illustrates spectral-cover continuation, not KZ connection holonomy. The source script checks endpoint exchange and the polynomial residual to 1e-12.')}

def load(draft=False):
 rows=json.loads((P/'revised_rows.json').read_text())
 original={x['id']:x for x in rows};chapters=[];entries=[]
 for key,title,lo,hi in CHAPTERS:
  path=P/'chapters'/key/'entries.json'
  if not path.exists():
   if draft:continue
   raise FileNotFoundError(path)
  part=json.loads(path.read_text());ids={x['id'] for x in part};expected={f'M{i:03d}' for i in range(lo,hi+1)}
  assert ids==expected,(key,ids^expected)
  part.sort(key=lambda x:x['id'])
  for e in part:
   for k in ['id','title','status','summary','definitions','result','example','limits','extension','references']:assert k in e,(e.get('id'),k)
   for k in ['name','statement','proof']:assert isinstance(e['result'].get(k),str),(e['id'],'result',k)
   for k in ['setup','calculation','conclusion']:assert isinstance(e['example'].get(k),str),(e['id'],'example',k)
   e['original']=original[e['id']]
   e['chapter']=key
   assert all(isinstance(r.get('url'),str) and r['url'].startswith('http') for r in e['references'])
  chapters.append((key,title,part));entries.extend(part)
 synth=json.loads((P/'syntheses.json').read_text())
 for key,*_ in CHAPTERS:
  for name in ['supplemental.json','spectral_supplemental.json','jordan_supplemental.json']:
   path=P/'chapters'/key/name
   if path.exists():
    extra=json.loads(path.read_text())
    if isinstance(extra,dict):extra=[extra]
    synth.extend(extra)
 synth.sort(key=lambda e:e['id'])
 assert len({e['id'] for e in synth})==len(synth)
 if not draft:assert len(entries)==114 and len(set(e['id'] for e in entries))==114
 return rows,chapters,entries,synth

def get_checks():
 reports=[]
 for key,*_ in CHAPTERS:
  f=P/'chapters'/key/'checks.json'
  if f.exists():reports.append((key,json.loads(f.read_text())))
  f=P/'chapters'/key/'supplement_checks.json'
  if f.exists():reports.append((key+' supplement',json.loads(f.read_text())))
  for name in ['spectral_checks.json','jordan_checks.json']:
   f=P/'chapters'/key/name
   if f.exists():reports.append((key+' '+name.replace('_checks.json',''),json.loads(f.read_text())))
  for f in sorted((P/'chapters'/key).glob('independent_*_checks.json')):
   reports.append((key+' independent',json.loads(f.read_text())))
 f=P/'synthesis_checks.json'
 if f.exists():reports.append(('syntheses',json.loads(f.read_text())))
 return reports

def collect_refs(entries):
 refs={}
 for e in entries:
  for r in e['references']:
   url=r['url'].rstrip('/')
   if url not in refs:refs[url]=dict(key=f'R{len(refs)+1:03d}',label=r['label'],url=r['url'])
 return refs

def h(s):return html.escape(str(s),quote=True)
def paragraphs(text):return ''.join('<p>'+h(x.strip())+'</p>' for x in re.split(r'\n\s*\n',str(text)) if x.strip())
def article(e,refs,synthesis=False):
 def sec(label,text,cls=''):return '<section class="'+cls+'"><h4>'+label+'</h4>'+paragraphs(text)+'</section>'
 meta='Synthesis' if synthesis else e['original']['date']+' · '+e['original']['field']+' · historical evidence '+e['original']['evidence']
 defs=''.join(paragraphs(x) for x in e['definitions'])
 links=''
 if e.get('links'):links='<p class="crosslinks">Related entries: '+' '.join('<a href="#'+x+'">'+x+'</a>' for x in e['links'])+'</p>'
 citations=' '.join('<a href="#'+refs[r['url'].rstrip('/')]['key']+'">'+refs[r['url'].rstrip('/')]['key']+'</a>' for r in e['references'])
 figure=''
 if e['id'] in FIGURES:
  name,caption=FIGURES[e['id']];f=P/'figures'/name
  if f.exists():figure='<div class="figure"><img alt="'+h(caption)+'" src="data:image/png;base64,'+base64.b64encode(f.read_bytes()).decode()+'"><p class="citations">'+h(caption)+'</p></div>'
 return f'''<article id="{e['id']}" data-chapter="{e.get('chapter','s')}" data-search="{h(e['id']+' '+e['title'])}"><div class="meta">{h(e['id'])} · {h(meta)}</div><h3>{h(e['title'])}</h3><p class="status">{h(e['status'])}</p>{paragraphs(e['summary'])}<section><h4>Definitions and assumptions</h4>{defs}</section><section class="theorem"><h4>{h(e['result']['name'])}</h4>{paragraphs(e['result']['statement'])}</section>{sec('Derivation or proof',e['result']['proof'])}<section class="example"><h4>Worked example</h4>{paragraphs(e['example']['setup'])}{paragraphs(e['example']['calculation'])}{paragraphs(e['example']['conclusion'])}</section>{figure}{sec('Scope of the result',e['limits'])}{sec('Further development',e['extension'])}{links}<p class="citations">Mathematical references: {citations or 'The elementary calculation is supplied in full above.'}</p></article>'''

def build_html(rows,chapters,entries,synth,refs,checks):
 count=sum(len(r.get('checks',[])) for _,r in checks)
 toc=''.join(f'<a href="#chapter-{key}">{key.upper()} · {h(title)}</a>' for key,title,_ in chapters)
 index=''.join(f'<tr><td><a href="#{e["id"]}">{e["id"]}</a></td><td>{h(e["title"])}</td><td>{h(e["result"]["name"])}</td></tr>' for e in entries)
 body='<h2 id="syntheses">Connections and extended developments</h2>'+''.join(article(e,refs,True) for e in synth)
 for key,title,part in chapters:body+=f'<h2 id="chapter-{key}" class="chapter-heading">{key.upper()} · {h(title)}</h2>'+''.join(article(e,refs) for e in part)
 source_html=''.join(f'<tr id="{v["key"]}"><td>{v["key"]}</td><td><a href="{h(v["url"])}" target="_blank" rel="noopener">{h(v["label"])}</a></td></tr>' for v in refs.values())
 report_html=''
 for key,r in checks:
  for c in r.get('checks',[]):
   detail=c.get('detail','')
   if not isinstance(detail,str):detail=json.dumps(detail,ensure_ascii=False,indent=2)
   detail_html=h(detail) if len(detail)<360 else '<details><summary>Read the retained check data</summary><pre class="check-data">'+h(detail)+'</pre></details>'
   report_html+=f'<tr><td>{h(key)}</td><td>{h(c.get("id",str(c.get("ids",""))))}</td><td>{h(c.get("name",""))}</td><td>{h(c.get("status",str(c.get("passed",""))))}</td><td>{detail_html}</td></tr>'
 intro='''<p>All 114 revised questions are developed here into mathematical treatments with definitions, a stated result, a derivation or proof, a worked example, and a precise scope. Six connecting arguments organize the material into a more coherent programme. The source bundle contains portable verification scripts and their retained outputs.</p><p>The 2023 evidence remains fragmentary. U marks a recovered user question, A an assistant passage without the original user wording, and T a dated topic fragment; none supplies a complete transcript. The historical starting points and their evidence labels come from the earlier table; the mathematical treatments are newly authored expositions and calculations. Classical results and small examples are not claimed as new discoveries. A worked example does not settle every general classification or research question mentioned in its extension.</p><p><strong>Reading the proof scope.</strong> A written proof, an exhaustive finite computation and a floating-point check are different forms of evidence. Every treatment states its assumptions and limits. The verification ledger records what each script actually checks; it is not a formal proof assistant certificate. General theorems invoked from the literature remain literature dependencies.</p>'''
 doc=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>The 2023 Mathematics Compendium</title><style>
 :root{{--ink:#1c2936;--blue:#174f75;--muted:#5a6878;--line:#d5dfe7}}*{{box-sizing:border-box}}body{{margin:0;background:#eff3f6;color:var(--ink);font:16px/1.7 system-ui,Segoe UI,sans-serif}}a{{color:var(--blue);text-underline-offset:3px}}header{{background:#16344e;color:#fff;padding:54px max(26px,calc((100vw - 1180px)/2))}}header p{{max-width:960px;color:#e1ecf5;font-size:18px}}h1{{font-size:clamp(34px,4vw,54px);line-height:1.14;letter-spacing:-1.2px;margin:12px 0 24px}}.eyebrow{{font-size:12px;letter-spacing:1.5px;text-transform:uppercase;color:#b9dce9}}main{{max-width:1180px;margin:auto;padding:28px 22px 80px}}.intro{{background:white;border:1px solid var(--line);padding:24px 30px;border-radius:8px}}.stats{{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:20px 0}}.stat{{background:#fff;border:1px solid var(--line);padding:14px 20px;border-radius:6px}}.stat b{{display:block;font-size:31px;color:var(--blue)}}.stat span{{font-size:12px;color:var(--muted)}}nav{{display:grid;grid-template-columns:1fr 1fr;gap:7px 24px;padding:18px 0;font-size:14px}}.toolbar{{display:flex;gap:12px;background:#fff;padding:14px;border:1px solid var(--line);border-radius:7px;position:sticky;top:0;z-index:10;flex-wrap:wrap}}input,select,button{{font:inherit;padding:9px;border:1px solid #b8c8d5;border-radius:4px;background:white;color:var(--ink)}}input{{flex:1;min-width:240px}}button{{cursor:pointer}}.count{{font-size:13px;color:var(--muted)}}h2{{font-size:28px;line-height:1.3;margin:42px 0 20px;color:#173c59}}h3{{font-size:27px;line-height:1.25;margin:8px 0 12px;letter-spacing:-.4px}}h4{{font-size:14px;letter-spacing:.25px;color:#264b68;margin:18px 0 8px}}article{{padding:30px 34px;background:white;border:1px solid var(--line);border-radius:8px;margin:22px 0;scroll-margin-top:100px}}article p{{margin:11px 0;overflow-wrap:anywhere}}.meta{{font:12px system-ui;color:var(--muted)}}.status{{font-size:12px;color:#4b6c5d}}.theorem{{padding:2px 20px 10px;background:#eef5fa;border-left:4px solid #3b789d;margin:20px 0}}.example{{padding:2px 20px 10px;background:#f5f7f9;border-left:4px solid #c0d1df;margin:20px 0}}.citations,.crosslinks{{font-size:13px;color:var(--muted)}}.citations a,.crosslinks a{{display:inline-block;margin:0 5px 0 0}}table{{width:100%;border-collapse:collapse;font-size:13px;background:white}}th,td{{text-align:left;vertical-align:top;padding:12px;border:1px solid var(--line);overflow-wrap:anywhere}}th{{background:#e6eef5}}.table-wrap{{overflow:auto}}details{{border:1px solid var(--line);background:#fff;border-radius:6px;padding:15px 20px;margin:20px 0}}summary{{cursor:pointer;font-weight:650}}.check-data{{white-space:pre-wrap;word-break:break-word;font:11px/1.5 monospace;max-height:420px;overflow:auto}}.hidden{{display:none!important}}.figure{{background:white;padding:20px;border:1px solid var(--line);margin:20px 0}}.figure img{{width:100%;height:auto}}footer{{font-size:12px;color:var(--muted);margin-top:35px}}[id]{{scroll-margin-top:110px}}
 @media(max-width:700px){{header{{padding:34px 22px}}main{{padding:18px 12px 45px}}article{{padding:22px 20px}}h3{{font-size:23px}}.stats{{grid-template-columns:1fr 1fr}}nav{{grid-template-columns:1fr}}.toolbar{{position:static}}.intro{{padding:18px 20px}}}}
 @media print{{@page{{size:A4;margin:18mm}}body{{background:white;font-size:11px}}header{{background:white;color:black;padding:0}}header p,.eyebrow{{color:#333}}h1{{font-size:30px}}main{{padding:0;max-width:none}}.toolbar,.stats,nav,.count,details{{display:none!important}}.intro,article{{border:0;padding:0;box-shadow:none}}article{{margin:20px 0}}h2{{break-before:page;font-size:24px}}h3{{font-size:20px;break-after:avoid}}h4{{break-after:avoid}}.theorem,.example{{break-inside:avoid}}a{{color:inherit}}.hidden{{display:none!important}}}}
 </style></head><body><header><div class="eyebrow">Mathematics from the 2023 conversations · developed 20 October 2026</div><h1>The 2023 Mathematics Compendium</h1><p>114 developed treatments with worked examples and proofs, six connecting arguments, and reproducible computational checks.</p></header><main><div class="intro">{intro}</div><div class="stats"><div class="stat"><b>{len(entries)}</b><span>developed original entries</span></div><div class="stat"><b>{len(synth)}</b><span>connecting arguments and extensions</span></div><div class="stat"><b>{count}</b><span>scoped verification records</span></div><div class="stat"><b>{len(refs)}</b><span>distinct mathematical references</span></div></div><nav><a href="#syntheses">Connections and extensions</a><a href="#entry-index">Complete entry index</a>{toc}<a href="#verification">Verification ledger</a><a href="#references">References</a></nav><div class="toolbar"><input id="search" type="search" aria-label="Search treatments" placeholder="Search a question, result, formula or entry ID"><select id="chapter" aria-label="Filter chapter"><option value="">All chapters</option><option value="s">Six connecting arguments</option>{''.join('<option value="'+k+'">'+k.upper()+' · '+h(t)+'</option>' for k,t,_ in chapters)}</select><button id="reset">Reset</button><button id="print">Print visible treatments</button></div><p class="count" id="count">{len(entries)+len(synth)} treatments shown</p><details id="entry-index"><summary>Complete index of the 114 developed questions</summary><div class="table-wrap"><table><thead><tr><th>ID</th><th>Question or concept</th><th>Developed result</th></tr></thead><tbody>{index}</tbody></table></div></details>{body}<h2 id="verification">Verification ledger</h2><p>The source ZIP includes the standalone scripts and retained JSON outputs. Re-run them with Python 3 using verify_all.py. Status labels are reproduced from the individual check reports; a proof-only item is not counted as an executed numerical or exhaustive test.</p><div class="table-wrap"><table><thead><tr><th>Chapter</th><th>Entry</th><th>Check</th><th>Status</th><th>Scope and output</th></tr></thead><tbody>{report_html}</tbody></table></div><h2 id="references">Mathematical references</h2><p>References support the background theories. The new expositions and computations are not claims of novelty, and citations do not replace the explicitly stated hypotheses.</p><table><thead><tr><th>Key</th><th>Reference</th></tr></thead><tbody>{source_html}</tbody></table><footer>The retrospective is based on recovered fragments, not a complete 2023 conversation export. Each original question remains traceable by its M identifier. Computational checks and mathematical derivations have separate stated scopes.</footer></main><script>
const articles=[...document.querySelectorAll('article')];function filter(){{const q=document.getElementById('search').value.trim().toLocaleLowerCase(),c=document.getElementById('chapter').value;let count=0;for(const a of articles){{const yes=(!q||a.textContent.toLocaleLowerCase().includes(q))&&(!c||a.dataset.chapter===c);a.classList.toggle('hidden',!yes);if(yes)count++}}document.getElementById('count').textContent=count+' of '+articles.length+' treatments shown'}}document.getElementById('search').addEventListener('input',filter);document.getElementById('chapter').addEventListener('change',filter);document.getElementById('reset').addEventListener('click',()=>{{document.getElementById('search').value='';document.getElementById('chapter').value='';filter()}});document.getElementById('print').addEventListener('click',()=>window.print());
</script></body></html>'''
 path=OUT/'2023_Mathematics_Compendium.html';path.write_text(doc)
 return path

def build_pdf(chapters,entries,synth,refs,checks):
 from reportlab.pdfbase import pdfmetrics
 from reportlab.pdfbase.ttfonts import TTFont
 from reportlab.lib.styles import ParagraphStyle
 from reportlab.lib import colors
 from reportlab.lib.enums import TA_LEFT
 from reportlab.lib.pagesizes import A4
 from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,PageBreak,KeepTogether,Table,TableStyle,Image,CondPageBreak
 fontdir=Path('/usr/share/fonts/truetype/dejavu')
 for name,file in [('DV','DejaVuSans.ttf'),('DVB','DejaVuSans-Bold.ttf'),('DVI','DejaVuSans-Oblique.ttf')]:
  fontpath=fontdir/file
  if not fontpath.exists():fontpath=fontdir/'DejaVuSans.ttf'
  pdfmetrics.registerFont(TTFont(name,str(fontpath)))
 pdfmetrics.registerFontFamily('DV',normal='DV',bold='DVB',italic='DVI',boldItalic='DVB')
 styles={
 'title':ParagraphStyle('title',fontName='DVB',fontSize=32,leading=39,textColor=colors.HexColor('#173b56'),spaceAfter=25),
 'sub':ParagraphStyle('sub',fontName='DV',fontSize=14,leading=21,textColor=colors.HexColor('#53697b'),spaceAfter=18),
 'h1':ParagraphStyle('h1',fontName='DVB',fontSize=22,leading=29,textColor=colors.HexColor('#173b56'),spaceAfter=20,keepWithNext=True),
 'h2':ParagraphStyle('h2',fontName='DVB',fontSize=16,leading=22,textColor=colors.HexColor('#173b56'),spaceBefore=16,spaceAfter=12,keepWithNext=True),
 'label':ParagraphStyle('label',fontName='DVB',fontSize=9.5,leading=14,textColor=colors.HexColor('#31546c'),spaceBefore=13,spaceAfter=6,keepWithNext=True),
 'body':ParagraphStyle('body',fontName='DV',fontSize=9.6,leading=14.5,spaceAfter=9,allowWidows=0,allowOrphans=0),
 'small':ParagraphStyle('small',fontName='DV',fontSize=8,leading=12,textColor=colors.HexColor('#536576'),spaceAfter=8),
 'theorem':ParagraphStyle('theorem',fontName='DV',fontSize=9.6,leading=14.5,spaceAfter=9,leftIndent=11,rightIndent=8,borderPadding=9,backColor=colors.HexColor('#eef4f8')),
 }
 # A tiny number of unsupported glyphs are replaced explicitly, never silently.
 charmap={'\u2011':'-','\u2013':'-','\u2014':'-','\u2212':'−'}
 glyphs=pdfmetrics.getFont('DV').face.charWidths
 replacements={}
 def xml(text):
  text=str(text)
  for a,b in charmap.items():text=text.replace(a,b)
  out=[]
  for c in text:
   if ord(c)>31 and ord(c) not in glyphs:
    norm=unicodedata.normalize('NFKD',c)
    if norm!=c and all(ord(z) in glyphs for z in norm):replacements[c]=norm;out.append(norm)
    else:raise ValueError('Unsupported PDF glyph '+repr(c)+' '+hex(ord(c)))
   else:out.append(c)
  return html.escape(''.join(out)).replace('\n','<br/>')
 def para(text,sty='body'):return Paragraph(xml(text),styles[sty])
 story=[]
 def text(text,sty='body'):
  for s in re.split(r'\n\s*\n',str(text)):
   if s.strip():story.append(para(s.strip(),sty))
 def label(s):story.append(para(s,'label'))
 story.append(Spacer(1,58));story.append(para('The 2023 Mathematics Compendium','title'))
 story.append(para('114 developed mathematical treatments and '+str(len(synth))+' connecting arguments and extensions','sub'))
 text('Developed from the mathematics-only retrospective of the 2023 conversations. Prepared 20 October 2026.','small')
 story.append(Spacer(1,24))
 text('The purpose is to turn earlier questions into actual mathematics: definitions, hypotheses, explicit results, derivations, worked examples and reproducible checks. Every original M identifier is retained. The accompanying HTML edition offers search and filtering; the source archive contains the verification programs and their outputs.')
 text('The historical evidence is fragmentary. These are newly authored developments of the recovered questions, not newly discovered 2023 transcripts. Classical theorems and illustrative computations are not claimed as original discoveries. Completing a worked treatment does not settle every open extension attached to it.')
 text('Historical labels: U means a user question was recovered in the search evidence; A means an assistant passage survives without the original user wording; T means only a dated topic-level fragment is available. None indicates a complete conversation transcript.','small')
 text('A written proof, a finite exhaustive computation and a floating-point check have different scopes. The proofs below are mathematical exposition, not proof-assistant formalizations. General literature dependencies remain visible. The source ledger records each program’s actual check.')
 story.append(PageBreak());story.append(para('Contents and scope','h1'))
 text('Part S develops connecting arguments and extended results. The first six concern observable recurrences, reversible information-preserving charts, finite observation algebras, heat-kernel recovery bounds, conservative graph dynamics and Gaussian projection geometry. The additional developments supply explicit classifications and finite certificates.')
 for key,title,part in chapters:text(key.upper()+'  '+title+'  ·  '+part[0]['id']+' to '+part[-1]['id'])
 text('The complete index follows the main treatments. The source archive also contains the original revised-question table, verification records and exact certificates. The HTML edition provides direct entry links.','small')
 def entry(e,issynth=False):
  story.append(CondPageBreak(150));story.append(para(e['id']+'  '+e['title'],'h2'))
  scope=e['status'] if issynth else e['original']['date']+' · historical evidence '+e['original']['evidence']+' · '+e['status']
  text(scope,'small');text(e['summary'])
  label('Definitions and assumptions')
  for d in e['definitions']:text(d)
  label(e['result']['name']);text(e['result']['statement'],'theorem')
  label('Derivation or proof');text(e['result']['proof'])
  label('Worked example');text(e['example']['setup']);text(e['example']['calculation']);text(e['example']['conclusion'])
  if e['id'] in FIGURES:
   from PIL import Image as PILImage
   name,caption=FIGURES[e['id']];f=P/'figures'/name
   if f.exists():
    im=PILImage.open(f);width=499;height=width*im.height/im.width
    story.append(KeepTogether([Spacer(1,8),Image(str(f),width=width,height=height),para(caption,'small')]))
  label('Scope of the result');text(e['limits'])
  label('Further development');text(e['extension'])
  if e.get('links'):text('Related entries: '+', '.join(e['links']),'small')
  if e['references']:text('References: '+', '.join(refs[r['url'].rstrip('/')]['key'] for r in e['references']),'small')
 story.append(PageBreak());story.append(para('Connections and extended developments','h1'))
 for e in synth:entry(e,True)
 for key,title,part in chapters:
  story.append(PageBreak());story.append(para(key.upper()+'  '+title,'h1'))
  for e in part:entry(e)
 story.append(PageBreak());story.append(para('Complete entry index','h1'))
 for e in entries:text(e['id']+'  '+e['title'],'small')
 story.append(PageBreak());story.append(para('Verification scope','h1'))
 for key,r in checks:
  text('Chapter '+key+': '+str(len(r.get('checks',[])))+' scoped records.','label')
  for c in r.get('checks',[]):text(str(c.get('id',c.get('ids','')))+' · '+str(c.get('name',''))+' · '+str(c.get('status',c.get('passed',''))),'small')
 story.append(PageBreak());story.append(para('Mathematical references','h1'))
 for r in refs.values():
  label(r['key']+'  '+r['label'])
  story.append(Paragraph('<link href="'+html.escape(r['url'],quote=True)+'" color="#174f75">'+xml(r['url'])+'</link>',styles['small']))
 path=OUT/'2023_Mathematics_Compendium.pdf'
 def decorate(c,doc):
  c.saveState();w,h=A4;c.setStrokeColor(colors.HexColor('#d7e1e9'));c.setLineWidth(.5);c.line(48,h-35,w-48,h-35);c.setFont('DV',7.5);c.setFillColor(colors.HexColor('#536779'));c.drawString(48,h-26,'THE 2023 MATHEMATICS COMPENDIUM');c.drawRightString(w-48,25,str(doc.page));c.drawString(48,25,'Definitions · proofs · worked examples · explicit scope');c.restoreState()
 class CompendiumDoc(SimpleDocTemplate):
  def afterFlowable(self,flowable):
   if isinstance(flowable,Paragraph) and flowable.style.name in ['h1','h2']:
    title=flowable.getPlainText();key='heading-'+str(self.seq.nextf('outline'))
    self.canv.bookmarkPage(key);self.canv.addOutlineEntry(title,key,level=0 if flowable.style.name=='h1' else 1,closed=True)
 doc=CompendiumDoc(str(path),pagesize=A4,rightMargin=48,leftMargin=48,topMargin=53,bottomMargin=48,title='The 2023 Mathematics Compendium',author='Mathematical development of the user’s 2023 questions')
 doc.build(story,onFirstPage=decorate,onLaterPages=decorate)
 (OUT/'pdf_glyph_replacements.json').write_text(json.dumps(replacements,ensure_ascii=False,indent=2))
 return path

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--draft',action='store_true');ap.add_argument('--html-only',action='store_true');args=ap.parse_args()
 rows,chapters,entries,synth=load(args.draft);refs=collect_refs(synth+entries);checks=get_checks()
 htmlpath=build_html(rows,chapters,entries,synth,refs,checks)
 pdfpath=None if args.html_only else build_pdf(chapters,entries,synth,refs,checks)
 combined=dict(title='The 2023 Mathematics Compendium',historical_scope='Recovered fragments, not exhaustive transcript export',entries=entries,syntheses=synth,references=list(refs.values()),verification_reports=dict(checks))
 (P/'compendium.json').write_text(json.dumps(combined,ensure_ascii=False,indent=2))
 with (P/'coverage.csv').open('w',newline='') as f:
  w=csv.writer(f);w.writerow(['id','date','historical_evidence','title','developed_result','status','chapter']);w.writerows([e['id'],e['original']['date'],e['original']['evidence'],e['title'],e['result']['name'],e['status'],e['chapter']] for e in entries)
 print(json.dumps(dict(entries=len(entries),syntheses=len(synth),words=sum(len(json.dumps(e,ensure_ascii=False).split()) for e in entries+synth),references=len(refs),verification_records=sum(len(v.get('checks',[])) for _,v in checks),html=str(htmlpath),pdf=str(pdfpath))))

if __name__=='__main__':main()
