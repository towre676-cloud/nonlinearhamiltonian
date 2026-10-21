"""Render all final PDF pages into indexed contact sheets for visual review."""
from pathlib import Path
import hashlib,json,math
import fitz
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parent
PDF=ROOT/'output'/'2025_Month_by_Month_Mathematics.pdf'
OUT=ROOT/'tmp'/'visual';OUT.mkdir(parents=True,exist_ok=True)
d=fitz.open(PDF);sheets=[];pages=[]
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',15)
for start in range(0,len(d),12):
    sheet=Image.new('RGB',(1040,1128),'#dbe3e8');draw=ImageDraw.Draw(sheet)
    for j,n in enumerate(range(start,min(start+12,len(d)))):
        page=d[n];pix=page.get_pixmap(matrix=fitz.Matrix(.39,.39),alpha=False)
        im=Image.frombytes('RGB',[pix.width,pix.height],pix.samples)
        x=(j%4)*260+(260-im.width)//2;y=(j//4)*376+31
        sheet.paste(im,(x,y));draw.text((j%4*260+14,j//4*376+6),f'Page{n+1}',fill='#243a48',font=font)
        pages.append(dict(page=n+1,text_sha256=hashlib.sha256(page.get_text().encode()).hexdigest()))
    target=OUT/f'contact-{start+1:03}-{min(start+12,len(d)):03}.jpg'
    sheet.save(target,quality=88)
    sheets.append(dict(start=start+1,end=min(start+12,len(d)),file=str(target.resolve())))
chunk=math.ceil(len(d)/36)*12
groups=[]
for start in range(1,len(d)+1,chunk):
    end=min(start+chunk-1,len(d));selected=sorted(set([start,min(start+3,end),(start+end)//2,max(start,end-3),end]))
    full=[]
    for n in selected:
        target=OUT/f'full-{n:03}.png';d[n-1].get_pixmap(matrix=fitz.Matrix(1.1,1.1),alpha=False).save(target)
        full.append(str(target.resolve()))
    groups.append(dict(start=start,end=end,sheets=[s['file']for s in sheets if start<=s['start']<=end],full=full))
manifest=dict(pdf_sha256=hashlib.sha256(PDF.read_bytes()).hexdigest(),pages=len(d),groups=groups,sheets=sheets,page_text=pages)
(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2))
print(json.dumps(dict(pages=len(d),contacts=len(sheets),groups=[dict(start=g['start'],end=g['end'],sheets=len(g['sheets']))for g in groups])))
