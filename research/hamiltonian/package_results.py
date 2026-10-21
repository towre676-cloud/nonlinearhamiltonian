from pathlib import Path
import hashlib,json,zipfile
ROOT=Path(__file__).resolve().parent
out=ROOT/'output/Nonlinear_Hamiltonian_Partners_Source_Bundle.zip'
rootfiles=['README.md','RESULTS.json','overview.md','partner_lab.py','verify_all.py','verify_cli.py','cli_checks.json','browser_checks.json','document_audit.json','make_browser_fixtures.py','test_browser.js','lab.js','lab_fragment.html','build_note.js','render_review.py','package_results.py']
files=[ROOT/n for n in rootfiles]
for folder in ['quartic','structural','monomial','independent','context']:
 for p in (ROOT/folder).rglob('*'):
  if p.is_file() and p.suffix in ['.py','.md','.json'] and '_deps' not in p.parts and '__pycache__' not in p.parts and p.name!='scan.py':files.append(p)
files += [ROOT/'output'/('Nonlinear_Hamiltonian_Partners'+ext) for ext in ['.pdf','.html','.md']]
files=sorted(set(files));assert all(p.is_file() for p in files)
manifest=''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(ROOT).as_posix()+'\n' for p in files)
(ROOT/'MANIFEST.sha256').write_text(manifest)
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for p in files+[ROOT/'MANIFEST.sha256']:z.write(p,'Nonlinear_Hamiltonian_Partners/'+p.relative_to(ROOT).as_posix())
print(json.dumps({'files':len(files)+1,'bytes':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest()}))
