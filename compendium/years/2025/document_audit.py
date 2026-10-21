"""Audit provenance and delivered-document structure; no general proof claim."""
from pathlib import Path
from collections import Counter
import json,re,hashlib
from common import ROOT,load,prose_words

def result_text(result):
    messages=result.get('structuredContent',{}).get('messages',[])
    if messages:return '\n'.join(m.get('content','')for m in messages)
    return '\n'.join(c.get('text','')for c in result.get('content',[])if c.get('type')=='text')

def main():
    months,entries=load();issues=[];rows=[]
    for m in months:
        folder=ROOT/'months'/m['key'];texts={}
        for p in folder.glob('root*.json'):
            data=json.loads(p.read_text())
            if isinstance(data,list):texts[p.name]=[result_text(r.get('result',{}))for r in data]
        for e in m['entries']:
            original=e['original'];excerpt=original['source_excerpt'];locator=original['retrieval_receipt']
            filename=re.search(r'(root_[a-z_]+\.json|receipts\.json)',locator)
            record=re.search(r'record\s*(\d+)',locator)
            matching_files=[]
            for name,values in texts.items():
                for i,t in enumerate(values):
                    if excerpt in t:matching_files.append((name,i))
            literal=bool(matching_files)
            locator_match=bool(filename and record and(filename.group(1),int(record.group(1)))in matching_files)
            if not literal:issues.append(dict(id=e['id'],issue='Source excerpt is not literal returned evidence'))
            if not locator_match:issues.append(dict(id=e['id'],issue='Receipt locator does not identify the literal source match',locator=locator,matches=matching_files))
            source_role=re.search(r'\b([UA])@(2025-\d\d-\d\d)',excerpt)
            role_match=not source_role or original['evidence']==source_role.group(1)
            role_exception=None
            if (source_role and source_role.group(1)=='U' and original['evidence']=='A'
                    and 'assistant-generated' in excerpt and original.get('source_role_exception')):
                role_match=True
                role_exception=original['source_role_exception']
            date_match=not source_role or original.get('date','').startswith(source_role.group(2))
            if not role_match:issues.append(dict(id=e['id'],issue='Evidence author label differs from source'))
            if not date_match:issues.append(dict(id=e['id'],issue='Entry date differs from source date'))
            if original.get('original_question')is not None:issues.append(dict(id=e['id'],issue='Verbatim question needs manual supporting-source review'))
            rows.append(dict(id=e['id'],literal_source_match=literal,receipt_locator_match=locator_match,
                             author_match=role_match,documented_author_exception=role_exception,
                             date_match=date_match,source_matches=matching_files))
    html_path=ROOT/'output'/'2025_Month_by_Month_Mathematics.html'
    if html_path.exists():
        text=html_path.read_text();ids=re.findall(r'<article id="([^"]+)"',text)
        if Counter(ids)!=Counter(e['id']for e in entries):issues.append(dict(issue='HTML entry identifiers differ from current source'))
        if any(x in text for x in['2024 Mathematics','January source gap','eleven recovered months']):issues.append(dict(issue='Stale previous-year text'))
    pdf_path=ROOT/'output'/'2025_Month_by_Month_Mathematics.pdf';pdf_data={}
    if pdf_path.exists():
        import fitz
        d=fitz.open(pdf_path);alltext='\n'.join(p.get_text()for p in d)
        missing=[e['id']for e in entries if e['id']not in alltext]
        if missing:issues.append(dict(issue='PDF missing entry identifiers',ids=missing))
        geometry=[];blank=[]
        for n,p in enumerate(d,1):
            text=p.get_text()
            if len(text.strip())<100:blank.append(n)
            for block in p.get_text('blocks'):
                if len(block)>4 and str(block[4]).strip():
                    x0,y0,x1,y1=block[:4]
                    if x0<35 or x1>p.rect.width-35 or y0<8 or y1>p.rect.height-8:
                        geometry.append(dict(page=n,bounds=[x0,y0,x1,y1],sample=str(block[4])[:100]))
        if blank:issues.append(dict(issue='Near-empty PDF pages',pages=blank))
        if geometry:issues.append(dict(issue='PDF text outside expected safe geometry',blocks=geometry))
        pdf_data=dict(pages=len(d),blank_pages=blank,geometry_issues=len(geometry),missing_ids=missing)
    report=dict(status='passed'if not issues else'failed',treatments=len(entries),
                prose_words=prose_words(entries),months={m['name']:len(m['entries'])for m in months},
                evidence=dict(Counter(e['original']['evidence']for e in entries)),
                source_rows=rows,issues=issues,pdf=pdf_data,
                scope='Schema, exact source attribution, document completeness and page geometry only. This is not automated verification of every written mathematical proof.')
    (ROOT/'document_checks.json').write_text(json.dumps(report,indent=2))
    print(json.dumps({k:report[k]for k in['status','treatments','prose_words','issues','pdf']}))
    if issues:raise SystemExit(1)

if __name__=='__main__':main()
