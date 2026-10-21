from pathlib import Path
import json,re,hashlib,collections
import fitz
ROOT=Path(__file__).resolve().parent
pdf=ROOT/'output/Mathematics_Atlas_2023_2026_Report.pdf';d=fitz.open(pdf);issues=[];text='\n'.join(p.get_text() for p in d);atlas=json.loads((ROOT/'data/atlas.json').read_text())
for i,p in enumerate(d):
 for b in p.get_text('dict')['blocks']:
  if b['type']!=0:continue
  for line in b['lines']:
   for s in line['spans']:
    x0,y0,x1,y1=s['bbox']
    if x0<45 or x1>p.rect.width-45 or y0<40 or (y1>p.rect.height-55 and not s['text'].startswith('MATHEMATICS ATLAS') and not s['text'].isdigit()):issues.append({'page':i+1,'issue':'text outside body margins','text':s['text'],'bbox':s['bbox']})
 for term in ['\nNone\n','<br/>','&lt;','?e_i','?x,e_j?']:
  if term in p.get_text():issues.append({'page':i+1,'issue':'suspicious rendered literal','text':term})
for e in atlas['corpus']+atlas['supplementary']:
 if e['uid'] not in text:issues.append({'issue':'missing source index identifier','uid':e['uid']})
for f in atlas['families']:
 if f['id'] not in text:issues.append({'issue':'missing family identifier','id':f['id']})
if len(d.get_toc())<90:issues.append({'issue':'outline unexpectedly short','count':len(d.get_toc())})
r={'status':'passed' if not issues else 'failed','pages':len(d),'pdf_sha256':hashlib.sha256(pdf.read_bytes()).hexdigest(),'words':len(text.split()),'source_identifiers':1065,'family_identifiers':71,'outline_entries':len(d.get_toc()),'issues':issues};(ROOT/'data/document_audit.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n');print(json.dumps(r,ensure_ascii=False));assert not issues
