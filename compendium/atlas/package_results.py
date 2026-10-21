from pathlib import Path
import hashlib,json,zipfile
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'output/Mathematics_Atlas_2023_2026_Source_Bundle.zip'
selected=[]
rootnames=['README.md','RESULTS.json','verify_all.py','verify_labs.py','materialize_sources.py','build_atlas.py','make_synthesis.py','document_audit.py','render_review.py','test_interface.js','test_catalogue.js','ui.html','app.js','package_results.py']
selected += [ROOT/n for n in rootnames]
selected += [p for p in (ROOT/'data').glob('*.json') if p.name!='initial_catalog_index.json']
selected += list((ROOT/'labs').glob('*'))
for d in (ROOT/'domains').iterdir():
 selected += [p for p in d.iterdir() if p.is_file() and (p.suffix=='.json' or p.name=='verify.py') and p.name!='initial_index.json']
selected += list((ROOT/'sources').glob('*.zip'))
selected += [ROOT/'output/Mathematics_Atlas_2023_2026.html',ROOT/'output/Mathematics_Atlas_2023_2026_Report.pdf']
selected=sorted(set(selected));assert all(p.is_file() for p in selected)
manifest=''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(ROOT).as_posix()+'\n' for p in selected)
(ROOT/'MANIFEST.sha256').write_text(manifest)
with zipfile.ZipFile(OUT,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for p in selected+[ROOT/'MANIFEST.sha256']:z.write(p,'Mathematics_Atlas_2023_2026/'+p.relative_to(ROOT).as_posix())
print(json.dumps({'files':len(selected)+1,'zip':str(OUT),'bytes':OUT.stat().st_size,'sha256':hashlib.sha256(OUT.read_bytes()).hexdigest()}))
