"""Create a portable source archive, with data, checks and both reading editions."""
from pathlib import Path
from datetime import datetime,timezone
from collections import Counter
import json,shutil,hashlib,zipfile
from pypdf import PdfReader
from common import ROOT,load,collect_refs,prose_words

STEM='2024_Month_by_Month_Mathematics'
def main():
    months,entries=load();summary=json.loads((ROOT/'verification_summary.json').read_text())
    assert summary['status']=='passed',summary['failures']
    doc=json.loads((ROOT/'document_checks.json').read_text());assert doc['status']=='passed'
    stage=ROOT/'package'/'2024_Mathematics'
    if stage.exists():shutil.rmtree(stage)
    stage.mkdir(parents=True)
    for name in ['README.md','VERIFY_WINDOWS.cmd','common.py','SOURCE_SCOPE.json','verify_all.py','verification_summary.json','compendium.json','revised_questions.json','build_compendium.py','make_figures.py','verify_figures.py','figure_checks.json','check_documents.py','document_checks.json','package_results.py']:
        shutil.copy2(ROOT/name,stage/name)
    if (ROOT/'relocated_replay.json').exists():shutil.copy2(ROOT/'relocated_replay.json',stage/'relocated_replay.json')
    for name in ['independent_audit.py','independent_checks.json']:
        if (ROOT/name).exists():shutil.copy2(ROOT/name,stage/name)
    if (ROOT/'independent_review_catalog.json').exists():shutil.copy2(ROOT/'independent_review_catalog.json',stage/'independent_review_catalog.json')
    if (ROOT/'resolved_review_issues.json').exists():shutil.copy2(ROOT/'resolved_review_issues.json',stage/'resolved_review_issues.json')
    for m in months:
        folder=stage/'months'/m['key'];folder.mkdir(parents=True)
        for f in (ROOT/'months'/m['key']).iterdir():
            if f.is_file() and f.suffix in ['.json','.py','.md','.csv','.txt']:
                shutil.copy2(f,folder/f.name)
    shutil.copytree(ROOT/'figures',stage/'figures')
    for ext in ['html','pdf']:shutil.copy2(ROOT/'output'/(STEM+'.'+ext),stage/(STEM+'.'+ext))
    (stage/'requirements-build.txt').write_text('reportlab\nPillow\nmatplotlib\npypdf\n')
    meta=dict(title='2024 Mathematics, Rebuilt Month by Month',created_at=datetime.now(timezone.utc).isoformat(),developed_treatments=len(entries),prose_words=prose_words(entries),pdf_pages=len(PdfReader(ROOT/'output'/(STEM+'.pdf')).pages),months_with_dated_recovered_material=11,month_sections=12,references=len(collect_refs(entries)),verifier_programs=summary['verifier_programs'],scoped_records=summary['scoped_records'],status_counts=summary['status_counts'],month_treatment_counts={m['name']:len(m['entries']) for m in months},claim_scope='Recovered fragments only. January and March items1–80 remain explicit gaps. Expositions, finite certificates, numerical checks and literature claims retain their individual scope.')
    (stage/'RESULTS.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2))
    (ROOT/'output'/'RESULTS.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2))
    lines=[]
    for f in sorted(stage.rglob('*')):
        if f.is_file():lines.append(hashlib.sha256(f.read_bytes()).hexdigest()+'  '+f.relative_to(stage).as_posix())
    (stage/'MANIFEST.sha256').write_text('\n'.join(lines)+'\n')
    archive=ROOT/'output'/'2024_Mathematics_Source_Bundle.zip'
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for f in sorted(stage.rglob('*')):
            if f.is_file():z.write(f,f.relative_to(stage.parent))
    (ROOT/'output'/'2024_Mathematics_Source_Bundle.sha256').write_text(hashlib.sha256(archive.read_bytes()).hexdigest()+'  '+archive.name+'\n')
    print(json.dumps(dict(meta,archive_bytes=archive.stat().st_size,files=sum(f.is_file() for f in stage.rglob('*')))))

if __name__=='__main__':main()
