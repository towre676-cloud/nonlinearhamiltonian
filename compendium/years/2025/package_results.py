"""Package the source and reading editions after successful verification."""
from pathlib import Path
from datetime import datetime,timezone
import json,shutil,hashlib,zipfile
from pypdf import PdfReader
from common import ROOT,load,collect_refs,prose_words

STEM='2025_Month_by_Month_Mathematics'
def main():
    months,entries=load()
    summary=json.loads((ROOT/'verification_summary.json').read_text())
    assert summary['status']=='passed',summary.get('failures')
    doc=json.loads((ROOT/'document_checks.json').read_text())
    assert doc['status']=='passed',doc.get('issues')
    stage=ROOT/'package'/'2025_Mathematics'
    if stage.exists():shutil.rmtree(stage)
    stage.mkdir(parents=True)
    required=['README.md','VERIFY_WINDOWS.cmd','common.py','SOURCE_SCOPE.json','verify_all.py',
      'verification_summary.json','compendium.json','revised_questions.json','build_compendium.py',
      'make_figures.py','render_review.py','document_audit.py','document_checks.json','package_results.py',
      'independent_audit.py','independent_checks.json']
    optional=['relocated_replay.json','independent_review_catalog.json','resolved_review_issues.json',
              'visual_review.json']
    for name in required+optional:
        p=ROOT/name
        if p.exists():shutil.copy2(p,stage/name)
        else:assert name in optional,name
    for m in months:
        folder=stage/'months'/m['key'];folder.mkdir(parents=True)
        for p in (ROOT/'months'/m['key']).iterdir():
            if p.is_file() and p.suffix in['.json','.py','.md','.csv','.txt']:
                shutil.copy2(p,folder/p.name)
    shutil.copytree(ROOT/'figures',stage/'figures')
    for ext in['html','pdf']:shutil.copy2(ROOT/'output'/(STEM+'.'+ext),stage/(STEM+'.'+ext))
    (stage/'requirements-build.txt').write_text('reportlab\nPillow\nmatplotlib\nnumpy\npypdf\nPyMuPDF\n')
    meta=dict(title='2025 Mathematics, Rebuilt Month by Month',created_at=datetime.now(timezone.utc).isoformat(),
      developed_treatments=len(entries),prose_words=prose_words(entries),
      pdf_pages=len(PdfReader(ROOT/'output'/(STEM+'.pdf')).pages),
      months_with_dated_recovered_material=sum(bool(m['entries'])for m in months),month_sections=12,
      references=len(collect_refs(entries)),verifier_programs=summary['verifier_programs'],
      scoped_records=summary['scoped_records'],status_counts=summary['status_counts'],
      month_treatment_counts={m['name']:len(m['entries'])for m in months},
      claim_scope='Recovered fragments, not an exhaustive transcript export. Revised expositions, finite certificates, numerical examples and cited general results retain their stated scopes.')
    for path in[stage/'RESULTS.json',ROOT/'output'/'RESULTS.json']:
        path.write_text(json.dumps(meta,ensure_ascii=False,indent=2))
    lines=[]
    for p in sorted(stage.rglob('*')):
        if p.is_file():lines.append(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(stage).as_posix())
    (stage/'MANIFEST.sha256').write_text('\n'.join(lines)+'\n')
    archive=ROOT/'output'/'2025_Mathematics_Source_Bundle.zip'
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=9)as z:
        for p in sorted(stage.rglob('*')):
            if p.is_file():z.write(p,p.relative_to(stage.parent))
    (ROOT/'output'/'2025_Mathematics_Source_Bundle.sha256').write_text(hashlib.sha256(archive.read_bytes()).hexdigest()+'  '+archive.name+'\n')
    print(json.dumps(dict(meta,archive_bytes=archive.stat().st_size,files=sum(p.is_file()for p in stage.rglob('*')))))

if __name__=='__main__':main()
