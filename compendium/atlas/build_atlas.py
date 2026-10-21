from pathlib import Path
import json,html,re,hashlib,collections,unicodedata
P=Path(__file__).parent; OUT=P/'output';OUT.mkdir(exist_ok=True)
def read(p):return json.loads(Path(p).read_text())
def write(p,o):Path(p).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n')
def normalize():
 corpus=read(P/'data/source_corpus_initial_routing.json'); original={e['uid']:e for e in corpus}; chapters=[];families=[];reviews=[]
 for name in ['arithmetic','algebra','geometry','analysis','probability','computation']:
  d=P/'domains'/name
  for file,dest in [('chapters.json',chapters),('families.json',families),('classification_review.json',reviews)]:
   v=read(d/file);dest.extend(v if isinstance(v,list) else v.get(file[:-5],[]))
 grouped=collections.defaultdict(list)
 for r in reviews:grouped[r['uid']].append(r)
 assert set(grouped)==set(original)
 overrides={'2023:M001':'D14','2026:Y26-01-031':'D02','2026:Y26-01-029':'D14','2026:Y26-10-029':'D14','2026:Y26-08-901':'D15','2026:Y26-08-903':'D15'}
 merged=[]
 for uid,rs in grouped.items():
  chosen=dict(rs[0]);chosen['primary_domain']=overrides.get(uid,chosen['primary_domain'])
  chosen['secondary_domains']=sorted(set(x for r in rs for x in r.get('secondary_domains',[]))|{r['primary_domain'] for r in rs if r['primary_domain']!=chosen['primary_domain']})
  chosen['family_ids']=sorted(set(x for r in rs for x in r.get('family_ids',[])))
  chosen['reason']=' '.join(dict.fromkeys(r.get('reason','') for r in rs))
  if uid in overrides:chosen['reason']+=' Atlas editorial resolution: primary '+overrides[uid]+' follows the stated theorem and target.'
  merged.append(chosen)
 reviews=merged
 F={f['id']:f for f in families};validD={x['id'] for x in read(P/'data/taxonomy.json')['domains']}
 membership=collections.defaultdict(set)
 for f in families:
  for uid in f.get('source_uids',[]):
   assert uid in original,(f['id'],uid)
   membership[uid].add(f['id'])
 for r in reviews:
  assert r['primary_domain'] in validD
  e=original[r['uid']];e['primary_domain']=r['primary_domain'];e['secondary_domains']=[x for x in r.get('secondary_domains',[]) if x!=e['primary_domain'] and x in validD];e['classification_reason']=r.get('reason','');
  for fid in r.get('family_ids',[]):
   if fid in F:membership[r['uid']].add(fid)
  e['family_ids']=sorted(membership[r['uid']])
 # Every retained source is discoverable even if no concept-family exposition directly develops it.
 for e in corpus:e['family_ids']=sorted(membership[e['uid']])
 chapters.sort(key=lambda x:x['domain_id']);families.sort(key=lambda x:x['id'])
 supplementary=[{'uid':'2023:'+e['id'],'year':2023,'source_id':e['id'],'source_date':None,'primary_domain':'Annual synthesis','secondary_domains':[],'capabilities':[],'family_ids':[],'source':e,'classification_reason':'Additional synthesis in the original 2023 annual volume; retained as an unaltered supplementary treatment.'} for e in read(P/'source_working/2023_Mathematics_Source_Bundle/2023_Mathematics/compendium.json')['syntheses']]
 volumes=read(P/'data/source_volumes.json')
 for v in volumes:v['local_root']='source_working/'+str(v['year'])+'_Mathematics_Source_Bundle/'+str(v['year'])+'_Mathematics'
 data={'supplementary':supplementary,'introduction':read(P/'data/introduction.json'),'taxonomy':read(P/'data/taxonomy.json'),'chapters':chapters,'families':families,'corpus':corpus,'bridges':read(P/'data/bridges.json'),'labs':read(P/'labs/contracts.json'),'source_volumes':volumes,'annual_replay':read(P/'data/annual_replay.json')}
 write(P/'data/atlas.json',data);write(P/'data/classification_review.json',reviews)
 return data

def build_html(data):
 template=(P/'ui.html').read_text();blob=json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
 result=template.replace('/*__DATA__*/',blob).replace('/*__ENGINE__*/',(P/'labs/engine.js').read_text()).replace('/*__APP__*/',(P/'app.js').read_text())
 (OUT/'Mathematics_Atlas_2023_2026.html').write_text(result)

def build_pdf(data):
 from reportlab.platypus import SimpleDocTemplate,BaseDocTemplate,PageTemplate,Frame,Paragraph,Spacer,PageBreak,LongTable,TableStyle,KeepTogether
 from reportlab.platypus.tableofcontents import TableOfContents
 from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
 from reportlab.lib import colors
 from reportlab.pdfbase import pdfmetrics
 from reportlab.pdfbase.ttfonts import TTFont
 from reportlab.lib.enums import TA_LEFT
 font='/usr/share/fonts/truetype/dejavu/';pdfmetrics.registerFont(TTFont('Atlas',font+'DejaVuSans.ttf'));pdfmetrics.registerFont(TTFont('AtlasBold',font+'DejaVuSans-Bold.ttf'));pdfmetrics.registerFont(TTFont('AtlasItalic',font+'DejaVuSans.ttf'));pdfmetrics.registerFontFamily('Atlas',normal='Atlas',bold='AtlasBold',italic='AtlasItalic',boldItalic='AtlasBold')
 styles=getSampleStyleSheet();styles.add(ParagraphStyle(name='BodyAtlas',fontName='Atlas',fontSize=9.3,leading=14.4,spaceAfter=8,textColor=colors.HexColor('#182c34'),splitLongWords=True));styles.add(ParagraphStyle(name='SmallAtlas',parent=styles['BodyAtlas'],fontSize=7.6,leading=10.8,spaceAfter=5));styles.add(ParagraphStyle(name='H1Atlas',parent=styles['BodyAtlas'],fontName='AtlasBold',fontSize=23,leading=29,spaceBefore=8,spaceAfter=18,keepWithNext=True));styles.add(ParagraphStyle(name='H2Atlas',parent=styles['BodyAtlas'],fontName='AtlasBold',fontSize=15,leading=20,spaceBefore=16,spaceAfter=10,keepWithNext=True));styles.add(ParagraphStyle(name='H3Atlas',parent=styles['BodyAtlas'],fontName='AtlasBold',fontSize=10.5,leading=15,spaceBefore=10,spaceAfter=6,keepWithNext=True));styles.add(ParagraphStyle(name='KickerAtlas',parent=styles['BodyAtlas'],fontSize=9,leading=13,textColor=colors.HexColor('#007b78'),spaceAfter=8))
 styles.add(ParagraphStyle(name='CoverAtlas',parent=styles['H1Atlas'],fontSize=36,leading=43,spaceAfter=28));styles.add(ParagraphStyle(name='RefAtlas',parent=styles['SmallAtlas'],fontSize=7.3,leading=9.8,spaceAfter=2))
 styles.add(ParagraphStyle(name='TOCAtlas',parent=styles['BodyAtlas'],fontSize=9,leading=14,leftIndent=10,firstLineIndent=-10,spaceBefore=2,spaceAfter=2))
 # Only substitute characters the embedded font cannot draw; preserve actual mathematics whenever available.
 coverage=pdfmetrics.getFont('Atlas').face.charToGlyph
 replacements={'𝔽':'F','ℏ':'ℏ','𝕏':'X','ℂ':'C','ℚ':'Q','ℝ':'R','ℤ':'Z','𝒪':'O','𝓞':'O','𝒞':'C','𝔤':'g','𝔥':'h','𝑥':'x','𝑦':'y','𝟙':'1'}
 def clean(t):
  t=str(t)
  for a,b in replacements.items():t=t.replace(a,b)
  return ''.join(c if ord(c) in coverage or c in '\n\t' else unicodedata.normalize('NFKD',c) if all(ord(z) in coverage for z in unicodedata.normalize('NFKD',c)) else '?' for c in t)
 def esc(t):return html.escape(clean(t)).replace('\n','<br/>')
 story=[]
 def para(t,style='BodyAtlas'):
  if t is None:return
  if isinstance(t,list):
   for x in t:para(x,style)
   return
  if isinstance(t,dict):
   for k,v in t.items():para(str(k).replace('_',' ').capitalize()+': '+str(v),style)
   return
  for block in str(t).split('\n\n'):
   if block.strip():story.append(Paragraph(esc(block.strip()),styles[style]))
 def h(t,level=2,key=None):
  p=Paragraph(esc(t),styles['H'+str(level)+'Atlas']);p._atlas_heading=(level,str(t),key or re.sub(r'\W+','-',str(t))[:80]);story.append(p)
 def section(label,text):
  start=len(story);h(label,3);para(text)
  if label=='Core objects':
   chunk=story[start:];del story[start:];story.append(KeepTogether(chunk))
 def table(rows,widths):
  formatted=[[Paragraph(esc(c),styles['SmallAtlas']) for c in row] for row in rows];t=LongTable(formatted,colWidths=widths,repeatRows=1,hAlign='LEFT');t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#deeeea')),('VALIGN',(0,0),(-1,-1),'TOP'),('LINEBELOW',(0,0),(-1,0),.5,colors.HexColor('#88aaa5')),('LINEBELOW',(0,1),(-1,-1),.2,colors.HexColor('#dbe3e1')),('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]));story.append(t);story.append(Spacer(1,10))
 W,H=595.276,841.89;left=49;right=49;usable=W-left-right
 class Doc(BaseDocTemplate):
  def afterFlowable(self,flow):
   if hasattr(flow,'_atlas_heading') and flow._atlas_heading[0]<=2:
    level,title,key=flow._atlas_heading;self.canv.bookmarkPage(key);self.canv.addOutlineEntry(title,key,level=level-1,closed=level>1)
    if level==1:self.notify('TOCEntry',(0,title,self.page,key))
 def footer(c,d):
  c.setStrokeColor(colors.HexColor('#a9c5bf'));c.line(left,43,W-right,43);c.setFont('Atlas',7);c.setFillColor(colors.HexColor('#51676e'));c.drawString(left,31,'MATHEMATICS ATLAS  |  2023–21 OCTOBER 2026');c.drawRightString(W-right,31,str(d.page))
 doc=Doc(str(OUT/'Mathematics_Atlas_2023_2026_Report.pdf'),pagesize=(W,H),leftMargin=left,rightMargin=right,topMargin=48,bottomMargin=59,title='Mathematics Atlas 2023–2026',author='Mathematics synthesis',allowSplitting=True)
 doc.addPageTemplates([PageTemplate(id='Main',frames=[Frame(left,59,usable,H-107,id='body',leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0)],onPage=footer)])
 para('A FOUR-YEAR MATHEMATICS SYNTHESIS','KickerAtlas');story.append(Spacer(1,45));para('Mathematics\nAtlas','CoverAtlas');para('2023–21 October 2026','H2Atlas');para(data['introduction']['subtitle']);story.append(Spacer(1,25));para(f"1,051 retained treatments · 16 domains · {len(data['families'])} concept families · 10 working models",'H3Atlas');para('Definitions. Theorems. Proofs. Exact examples. Limits. Cross-domain bridges.');story.append(Spacer(1,30));para(data['introduction']['scope']);para('The self-contained interactive companion includes the full source-treatment text, search and filters, and parameterized mathematical labs. The portable bundle retains all four annual source volumes and replayable checks.','SmallAtlas');story.append(PageBreak())
 h('Contents and reading map',1,'contents');toc=TableOfContents();toc.levelStyles=[styles['TOCAtlas']];story.append(toc);story.append(PageBreak())
 h('Scope, method and central argument',1,'scope')
 for label,k in [('Source boundary','scope'),('Editorial method','method'),('The central argument','argument'),('Interactive capacities','interactivity'),('How to read the atlas','reading'),('What has been checked','verification')]:section(label,data['introduction'][k])
 table([['Source year','Treatments','Original verifier programs','Scoped records']]+[[str(x['year']),str(x['entries']),str(json.loads(r['stdout'])['verifier_programs']),str(json.loads(r['stdout'])['scoped_records'])] for x,r in zip(data['source_volumes'],data['annual_replay'])],[70,90,160,usable-320])
 h('The domain map',1,'domain-map');counts=collections.Counter(e['primary_domain'] for e in data['corpus']);table([['Domain','Primary treatments','Concept families']]+[[d['id']+' · '+d['title'],str(counts[d['id']]),str(sum(f['domain_id']==d['id'] for f in data['families']))] for d in data['taxonomy']['domains']],[usable-150,75,75]);para('Primary counts are editorial placements after a complete routing review. Secondary domains and family membership preserve overlap. A retained treatment may have no expanded family of its own; it remains fully available in the catalogue.','SmallAtlas')
 for chapter in data['chapters']:
  did=chapter['domain_id'];story.append(PageBreak());h(did+' · '+chapter['title'],1,did);section('Organizing question',chapter.get('organizing_question',''));para(chapter.get('overview',''));section('Core objects',chapter.get('core_objects',[]));section('Open frontier',chapter.get('open_frontier',''))
  order=chapter.get('concept_order',[]);fs=[f for f in data['families'] if f['domain_id']==did];fs.sort(key=lambda f:order.index(f['id']) if f['id'] in order else 999)
  for f in fs:
   h(f['id']+' · '+f['title'],2,f['id']);para(f.get('central_question',''),'KickerAtlas');para(f.get('synopsis',''));section('Definitions',f.get('definitions',[]));theorem=f.get('theorem',{});section('Theorem and hypotheses',theorem.get('statement',''));section('Proof',theorem.get('proof',''));ex=f.get('worked_example',{});section('Worked example',ex.get('setup',''));para(ex.get('calculation',''));para(ex.get('meaning',ex.get('conclusion','')))
   section('Continuity across the source years',[str(x.get('year',''))+' — '+str(x.get('narrative',''))+' Sources: '+', '.join(x.get('evidence_uids',[])) for x in f.get('progression',[])])
   section('Connections',[x.get('target_domain','')+' — '+x.get('relation','')+'. '+x.get('mathematical_bridge','')+' '+x.get('scope','') for x in f.get('connections',[])])
   section('Capacity and interactive scope',f.get('interactive_contract',{}));section('Limits',f.get('limits',''));section('Next questions',f.get('open_questions',[]));para('Source anchors: '+', '.join(f.get('anchor_uids',f.get('source_uids',[]))),'SmallAtlas')
   refs=f.get('references',[])
   for r in refs:
    if isinstance(r,dict):para(r.get('label','Reference')+' — '+r.get('url',''),'RefAtlas')
 story.append(PageBreak());h('Six cross-domain bridges',1,'bridges');para('Each bridge states what is actually transported between domains. Its scope distinguishes a theorem in a named model from a shared formal pattern or an open programme.')
 for b in data['bridges']:
  h(b['id']+' · '+b['title'],2,b['id']);para(b['kind']+' · '+', '.join(b['domains']),'KickerAtlas');para(b['question']);para(b['text']);para('Working models: '+', '.join(b['labs']),'SmallAtlas')
 story.append(PageBreak());h('Interactive capacity contracts',1,'capacities');para(data['introduction']['interactivity']);table([['Capacity','Implemented worked-model links']]+[[c['id']+' · '+c['title'],', '.join(l['id'] for l in data['labs'] if c['id'] in l['capabilities']) or 'Conceptual recipes in the chapters; no general solver'] for c in data['taxonomy']['capabilities']],[usable*.58,usable*.42])
 for l in data['labs']:
  start=len(story)
  h(l['id']+' · '+l['title'],2,l['id']);section('Arithmetic',l['arithmetic']);section('Inputs',[x['label'] for x in l['inputs']]);section('Limits',l['limits']);para('Domains: '+', '.join(l['domains'])+' · Capacities: '+', '.join(l['capabilities']),'SmallAtlas');chunk=story[start:];del story[start:];story.append(KeepTogether(chunk))
 story.append(PageBreak());h('Complete treatment index',1,'catalogue');para('Every retained treatment is indexed below by stable year-prefixed identifier and revised domain. The interactive companion contains the complete definitions, theorem, proof, example, limits, extension, original question and references of each treatment. Titles are revised annual-volume titles, not verbatim historical conversation titles. Source evidence codes remain as originally recorded and are not reinterpreted as confidence scores.')
 rows=[['Source identifier / date','Revised treatment','Domain']]
 for e in data['corpus']:rows.append([e['uid']+'\n'+str(e['source_date'] or 'Date unavailable'),e['source']['title'],e['primary_domain']])
 table(rows,[112,usable-157,45]);h('Additional 2023 annual syntheses',2,'additional-2023');para('Fourteen additional synthesis treatments from the 2023 volume are preserved separately from the 1,051 main-treatment count. Their complete original revised text is available in the interactive companion and source bundle.');table([['Identifier','Synthesis']]+[[e['uid'],e['source']['title']] for e in data['supplementary']],[112,usable-112]);story.append(PageBreak());h('Verification and reproducibility',1,'verification');para(data['introduction']['verification']);para('The portable bundle includes normalized data, full immutable source payloads, domain verifier scripts, the exact lab engine, independent fixtures, interface tests, builders and the four annual source ZIPs. Verification results name their scope. Rebuilding the PDF needs ReportLab and DejaVu fonts; the mathematical domain checks use the Python standard library. Running the HTML companion needs only a modern browser and no network connection.');para('The catalogue preserves original annual treatment payloads byte-for-byte at the JSON value level. Classification, grouping, navigation and newly authored bridges are additional atlas data. Source hashes and a portable package manifest make accidental changes detectable. Historical gaps—such as unrecovered large-instance tables or actual braid generators—remain gaps, even when a related finite model can be demonstrated.');para('New computations and conceptual refinements belong to this atlas edition. They are not backdated to the conversation dates. The report does not claim that numerical spot checks constitute formal verification of all prose proofs.')
 doc.multiBuild(story)
 print('PDF built',len(data['families']),'families',len(data['corpus']),'treatments')
if __name__=='__main__':
 import argparse
 ap=argparse.ArgumentParser();ap.add_argument('--html-only',action='store_true');ap.add_argument('--from-data',action='store_true');a=ap.parse_args();data=read(P/'data/atlas.json') if a.from_data else normalize();build_html(data)
 if not a.html_only:build_pdf(data)
