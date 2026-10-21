"""Stage a complete portable source bundle and create its ZIP."""
from pathlib import Path
import json,shutil,zipfile,hashlib
from datetime import datetime
from zoneinfo import ZoneInfo
from pypdf import PdfReader

P=Path(__file__).resolve().parent
stage=P/'package'/'2023_Mathematics'
if stage.exists():shutil.rmtree(stage)
stage.mkdir(parents=True)
root_files=['README.md','VERIFY_WINDOWS.cmd','verify_all.py','verify_syntheses.py','syntheses.py','syntheses.json','synthesis_checks.json','revised_rows.json','original_2023_table.html','compendium.json','coverage.csv','verification_summary.json','build_compendium.py','make_figures.py','check_documents.py','document_checks.json','package_results.py','relocated_replay.json']
for name in root_files:shutil.copy2(P/name,stage/name)
for name in ['2023_Mathematics_Compendium.html','2023_Mathematics_Compendium.pdf']:shutil.copy2(P/'output'/name,stage/name)
for key in 'abcdef':
 target=stage/'chapters'/key;target.mkdir(parents=True)
 for f in (P/'chapters'/key).iterdir():
  if f.is_file() and f.suffix in ['.py','.json','.md','.csv','.txt']:shutil.copy2(f,target/f.name)
shutil.copytree(P/'figures',stage/'figures')
(stage/'requirements-build.txt').write_text('reportlab\nPillow\nmatplotlib\npypdf\n')
r=json.loads((P/'compendium.json').read_text())
def words(e):return sum(len(s.split()) for s in [e['summary'],*e['definitions'],*e['result'].values(),*e['example'].values(),e['limits'],e['extension']])
summary=json.loads((P/'verification_summary.json').read_text())
meta=dict(title='The 2023 Mathematics Compendium',built_at=datetime.now(ZoneInfo('America/New_York')).isoformat(),main_treatments=len(r['entries']),additional_treatments=len(r['syntheses']),prose_words=sum(map(words,r['entries']+r['syntheses'])),pdf_pages=len(PdfReader(P/'output/2023_Mathematics_Compendium.pdf').pages),mathematical_references=len(r['references']),verifier_programs=summary['verifier_programs'],verification_status=summary['status'],scoped_records=summary['scoped_records'],status_counts=summary['status_counts'],claim_scope='Developed proofs and worked examples for recovered questions; no claim of exhaustive transcript recovery or mathematical novelty. See each treatment for hypotheses and limits.')
(stage/'RESULTS.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2))
(P/'output'/'RESULTS.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2))
def seal():
 lines=[]
 for f in sorted(stage.rglob('*')):
  if f.is_file() and f.name!='MANIFEST.sha256':lines.append(hashlib.sha256(f.read_bytes()).hexdigest()+'  '+f.relative_to(stage).as_posix())
 (stage/'MANIFEST.sha256').write_text('\n'.join(lines)+'\n')
seal()
archive=P/'output/2023_Mathematics_Source_Bundle.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for f in sorted(stage.rglob('*')):
  if f.is_file():z.write(f,f.relative_to(stage.parent))
(P/'output/2023_Mathematics_Source_Bundle.sha256').write_text(hashlib.sha256(archive.read_bytes()).hexdigest()+'  '+archive.name+'\n')
print(json.dumps(dict(meta,archive=str(archive),archive_bytes=archive.stat().st_size,files=sum(f.is_file() for f in stage.rglob('*')))))
