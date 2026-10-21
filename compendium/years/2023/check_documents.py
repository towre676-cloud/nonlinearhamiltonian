"""Structural checks for the delivered HTML/PDF; not mathematical proof checks."""
from pathlib import Path
from html.parser import HTMLParser
import json,re
from pypdf import PdfReader
P=Path(__file__).resolve().parent
class Parser(HTMLParser):
 def __init__(self):super().__init__();self.ids=[];self.links=[];self.articles=[];self.stack=[];self.errors=[]
 def handle_starttag(self,t,a):
  attrs=dict(a)
  if 'id' in attrs:self.ids.append(attrs['id'])
  if t=='a' and attrs.get('href','').startswith('#'):self.links.append(attrs['href'][1:])
  if t=='article':self.articles.append(attrs)
  if t not in ['meta','input','br','hr','link','img','area','base','embed','param','source','track','wbr']:self.stack.append(t)
 def handle_endtag(self,t):
  if not self.stack or self.stack[-1]!=t:self.errors.append([t,self.stack[-5:]])
  else:self.stack.pop()
doc=(P/'output/2023_Mathematics_Compendium.html').read_text();p=Parser();p.feed(doc)
assert not p.errors and not p.stack,(p.errors,p.stack)
assert len(p.ids)==len(set(p.ids))
assert all(x in p.ids for x in p.links)
assert len(p.articles)==128
assert sum(x.get('data-chapter')=='s' for x in p.articles)==14
assert len(re.findall('data:image/png;base64,',doc))==3
assert not re.search(r'<script[^>]+src=',doc)
pdf=PdfReader(P/'output/2023_Mathematics_Compendium.pdf')
alltext='\n'.join(x.extract_text() for x in pdf.pages)
for i in range(1,115):assert f'M{i:03d}' in alltext
for i in range(1,15):assert f'S{i:03d}' in alltext
blank=[i+1 for i,x in enumerate(pdf.pages) if len(x.extract_text().strip())<120]
assert not blank,blank
result=dict(html_articles=len(p.articles),main_entries=114,additional_entries=14,embedded_figures=3,unique_ids=True,valid_nesting=True,reference_anchors=True,external_scripts=0,pdf_pages=len(pdf.pages),pdf_blank_pages=blank,pdf_outline_present=bool(pdf.outline))
(P/'document_checks.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
