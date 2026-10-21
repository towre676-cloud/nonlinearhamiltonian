"""Structural edition checks; visual PDF inspection remains a separate step."""
from pathlib import Path
from html.parser import HTMLParser
from pypdf import PdfReader
import re,json
from common import ROOT
STEM='2024_Month_by_Month_Mathematics'
class Parser(HTMLParser):
    def __init__(self):
        super().__init__();self.ids=[];self.links=[];self.articles=[];self.errors=[];self.stack=[]
    def handle_starttag(self,t,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.append(a['id'])
        if t=='a' and a.get('href','').startswith('#'):self.links.append(a['href'][1:])
        if t=='article':self.articles.append(a)
        if t not in ['meta','input','br','hr','link','img','area','base','embed','param','source','track','wbr']:self.stack.append(t)
    def handle_endtag(self,t):
        if not self.stack or self.stack[-1]!=t:self.errors.append([t,self.stack[-5:]])
        else:self.stack.pop()
data=json.loads((ROOT/'compendium.json').read_text())
doc=(ROOT/'output'/(STEM+'.html')).read_text();parser=Parser();parser.feed(doc)
assert not parser.errors and not parser.stack,(parser.errors,parser.stack)
assert len(parser.ids)==len(set(parser.ids))
assert all(x in parser.ids for x in parser.links)
assert len(parser.articles)==len(data['entries'])
assert len(set(x['id'] for x in parser.articles))==len(data['entries'])
assert sum('id="month-'+f'{i:02d}'+'"' in doc for i in range(1,13))==12
assert not re.search(r'<script[^>]+src=',doc)
assert doc.count('data:image/png;base64,')==3
pdf=PdfReader(ROOT/'output'/(STEM+'.pdf'));texts=[p.extract_text() for p in pdf.pages];alltext='\n'.join(texts)
for e in data['entries']:assert e['id'] in alltext,e['id']
for name in ['January','February','March','April','May','June','July','August','September','October','November','December']:assert name+' 2024' in alltext,name
blank=[i+1 for i,t in enumerate(texts) if len(t.strip())<110]
assert not blank,blank
assert pdf.outline
assert 'source gap' in alltext.lower()
assert not any(s in alltext for s in ['PLACEHOLDER','TODO: write','turn0search'])
result=dict(status='passed',treatments=len(data['entries']),month_sections=12,embedded_figures=3,pdf_pages=len(pdf.pages),unique_ids=True,html_nesting=True,internal_anchors=True,pdf_all_entry_ids=True,pdf_blank_pages=blank,pdf_outline=True,source_gap_visible=True)
(ROOT/'document_checks.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
