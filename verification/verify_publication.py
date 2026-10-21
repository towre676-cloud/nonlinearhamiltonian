#!/usr/bin/env python3
"""Audit and replay the published mathematics collection without changing it.

Python 3.10+, standard library only. Node.js is required for atlas engine checks.
Annual suites run exactly once each, in temporary copies; the atlas is invoked
with --skip-annual, then the Hamiltonian suite once. No network or GitHub writes.
"""
from __future__ import annotations
import argparse
import collections
import concurrent.futures
import csv
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import sys
import tempfile
from urllib.parse import unquote, urlsplit
import zipfile

EXPECTED_YEARS = {2023: 114, 2024: 237, 2025: 351, 2026: 349}
ATLAS_ARCHIVE_NAME = 'Mathematics_Atlas_2023_2026_Source_Bundle.zip'
ATLAS_ARCHIVE_SIZE = 22147097
ATLAS_ARCHIVE_SHA256 = '69e639d10f90a50180dcee289d31f0a405cafb882705f1813a53c3cf56046475'
TEXT_SUFFIXES = {'.py', '.js', '.json', '.md', '.html', '.htm', '.csv', '.tsv', '.txt', '.yml', '.yaml', '.toml', '.ini', '.cfg', '.sha256'}
# Runtime paths in sealed historical receipts are portability notes, not secrets.
PATTERNS = {
    'runtime_path_note': re.compile(rb'/(?:workspace/|mnt/data/|tmp/|root/)'),
    'Library_identifier': re.compile(rb'(?:library://|library_file_id|libraryId|file_[a-fA-F0-9]{20,})'),
    'Library_helper': re.compile(rb'(?:\.library_helpers|library_(?:download|upload|file_transfer|hosted_apps)\.py)'),
    'signed_URL_or_access_token': re.compile(rb'(?:[?&](?:sig|token|X-Amz-Signature|X-Goog-Signature)=)[A-Za-z0-9%+/=_-]{12,}', re.I),
    'private_key': re.compile(rb'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),
    'credential_assignment': re.compile(rb'(?:sk-[A-Za-z0-9_-]{24,}|gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,})'),
}
# Labels are constructed without placing a literal secret-looking token in this scanner.
PRIVATE_NAMES = {'.env', 'credentials.json', 'token.json', '.DS_Store'}
EXCLUDED_DIRS = {'.git', '__pycache__', 'node_modules', '_deps'}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def canonical_hash(value) -> str:
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')).hexdigest()


def load(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))


def contained(root: Path, relative: str) -> Path:
    p = PurePosixPath(relative.replace('\\', '/'))
    if p.is_absolute() or '..' in p.parts:
        raise ValueError('Unsafe relative path')
    result = (root / Path(*p.parts)).resolve()
    if not result.is_relative_to(root.resolve()):
        raise ValueError('Path escapes package root')
    return result


class Audit:
    def __init__(self, root: Path):
        self.root = root.resolve()
        self.records = []
        self.failures = []
        self.warnings = []

    def rel(self, path: Path) -> str:
        try:
            return path.resolve().relative_to(self.root).as_posix()
        except ValueError:
            return path.name

    def check(self, condition, name, detail=None):
        record = {'check': name, 'status': 'passed' if condition else 'failed'}
        if detail is not None:
            record['details'] = detail
        self.records.append(record)
        if not condition:
            self.failures.append(name)
        return bool(condition)

    def warn(self, name, detail=None):
        self.warnings.append({'note': name, 'details': detail})

    def manifest(self, package: Path, required=True):
        manifest = package / 'MANIFEST.sha256'
        if not manifest.is_file():
            self.check(not required, 'Manifest present: ' + self.rel(package))
            return {}
        entries = {}
        errors = []
        for number, line in enumerate(manifest.read_text(encoding='utf-8').splitlines(), 1):
            if not line.strip():
                continue
            match = re.fullmatch(r'([0-9a-fA-F]{64})  (.+)', line)
            if not match:
                errors.append({'line': number, 'error': 'invalid manifest record'})
                continue
            digest, name = match.groups()
            try:
                path = contained(package, name)
                if name in entries:
                    raise ValueError('duplicate manifest path')
                entries[name] = digest.lower()
                if not path.is_file():
                    errors.append({'path': name, 'error': 'missing file'})
                elif sha256_file(path) != digest.lower():
                    errors.append({'path': name, 'error': 'digest mismatch'})
            except ValueError as e:
                errors.append({'path': name, 'error': str(e)})
        self.check(bool(entries) and not errors, 'SHA-256 manifest: ' + self.rel(package), {'files': len(entries), 'errors': errors})
        return entries


def archive_audit(audit: Audit, archive: Path, annual: Path, year: int, expected_payload):
    """Check every sealed archive manifest path and its unchanged source payload."""
    if not audit.check(archive.is_file(), f'Sealed annual archive exists: {year}'):
        return
    with zipfile.ZipFile(archive) as z:
        members = {i.filename: i for i in z.infolist() if not i.is_dir()}
        manifests = [n for n in members if n.endswith('/MANIFEST.sha256') or n == 'MANIFEST.sha256']
        root_manifests = sorted(manifests, key=lambda n: (len(PurePosixPath(n).parts), n))
        if not audit.check(bool(root_manifests), f'Archive manifest present: {year}'):
            return
        manifest_name = root_manifests[0]
        prefix = manifest_name[:-len('MANIFEST.sha256')]
        unsafe = [n for n in members if PurePosixPath(n).is_absolute() or '..' in PurePosixPath(n).parts]
        errors = []
        count = 0
        for line in z.read(manifest_name).decode('utf-8').splitlines():
            if not line.strip():
                continue
            match = re.fullmatch(r'([0-9a-fA-F]{64})  (.+)', line)
            if not match:
                errors.append('invalid manifest record')
                continue
            digest, name = match.groups()
            member = prefix + name
            if member not in members or hashlib.sha256(z.read(member)).hexdigest() != digest.lower():
                errors.append(name)
            count += 1
        audit.check(not unsafe and bool(count) and not errors, f'Sealed archive manifest paths: {year}', {'files': count, 'unsafe_members': len(unsafe), 'mismatches': errors})
        payload_name = prefix + 'compendium.json'
        payload = json.loads(z.read(payload_name))
        audit.check(payload == expected_payload, f'Annual source payload equals sealed archive: {year}')
        # Public annual roots may retain extra documentation, but every original
        # manifest member must still agree byte-for-byte with the sealed source.
        mirrors = []
        for line in z.read(manifest_name).decode('utf-8').splitlines():
            if not line.strip():
                continue
            match = re.fullmatch(r'([0-9a-fA-F]{64})  (.+)', line)
            if not match:
                continue
            digest, name = match.groups()
            try:
                target = contained(annual, name)
                if not target.is_file() or sha256_file(target) != digest.lower():
                    mirrors.append(name)
            except ValueError:
                mirrors.append(name)
        audit.check(not mirrors, f'Public annual root preserves sealed files: {year}', {'mismatches': mirrors})


def resolve_atlas_download(audit: Audit, root: Path, temporary_root: Path):
    """Accept the identical full ZIP, or strictly verify/reassemble raw parts.

    The expected original byte count and SHA-256 are fixed, not trusted solely
    from the delivery index. Reassembly never writes into the public repository.
    """
    full=root/'downloads'/ATLAS_ARCHIVE_NAME
    if full.is_file():
        valid=full.stat().st_size==ATLAS_ARCHIVE_SIZE and sha256_file(full)==ATLAS_ARCHIVE_SHA256
        audit.check(valid,'Full atlas source archive has exact delivery bytes',{'size':full.stat().st_size,'expected_size':ATLAS_ARCHIVE_SIZE,'expected_sha256':ATLAS_ARCHIVE_SHA256})
        return full if valid else None
    folder=root/'downloads/atlas-source-parts';index=folder/'parts.json'
    if not audit.check(index.is_file(),'Atlas source archive available as full ZIP or indexed raw parts'):
        return None
    try:
        data=load(index)
        valid=(data.get('filename')==ATLAS_ARCHIVE_NAME and type(data.get('size')) is int and data['size']==ATLAS_ARCHIVE_SIZE and data.get('sha256')==ATLAS_ARCHIVE_SHA256 and isinstance(data.get('parts'),list) and bool(data['parts']))
        if not audit.check(valid,'Split atlas delivery index has exact archive identity'):
            return None
        output=temporary_root/ATLAS_ARCHIVE_NAME;digest=hashlib.sha256();total=0;seen=set();details=[]
        with output.open('wb') as assembled:
            for part in data['parts']:
                name=part['filename'];size=part['size'];expected=part['sha256']
                if not isinstance(name,str) or name in seen or type(size) is not int or not 0<size<=ATLAS_ARCHIVE_SIZE or not isinstance(expected,str) or not re.fullmatch(r'[0-9a-f]{64}',expected):
                    raise ValueError('Invalid or duplicated raw-part record')
                seen.add(name);path=contained(folder,name)
                if not path.is_file() or path.stat().st_size!=size or sha256_file(path)!=expected:
                    raise ValueError('Raw-part size or SHA-256 mismatch')
                with path.open('rb') as source:
                    for chunk in iter(lambda:source.read(1024*1024),b''):
                        assembled.write(chunk);digest.update(chunk);total+=len(chunk)
                details.append({'filename':name,'size':size,'sha256':expected})
        exact=total==ATLAS_ARCHIVE_SIZE and digest.hexdigest()==ATLAS_ARCHIVE_SHA256
        audit.check(exact,'Reassembled atlas ZIP is byte-identical to full archive',{'size':total,'sha256':digest.hexdigest(),'parts':details,'destination':'temporary directory only'})
        return output if exact else None
    except (OSError,ValueError,KeyError,TypeError) as error:
        audit.check(False,'Atlas raw-part reconstruction',{'error_type':type(error).__name__,'reason':str(error)})
        return None


def delivered_archive_audit(audit: Audit, archive: Path, component: Path):
    """Validate a downloadable atlas/research bundle against its public tree."""
    if not audit.check(archive.is_file(), 'Downloadable source bundle exists: '+audit.rel(archive)):
        return
    errors=[]; count=0
    with zipfile.ZipFile(archive) as z:
        names={i.filename for i in z.infolist() if not i.is_dir()}
        manifests=sorted((n for n in names if n.endswith('/MANIFEST.sha256') or n=='MANIFEST.sha256'),key=lambda n:(len(PurePosixPath(n).parts),n))
        if not audit.check(bool(manifests), 'Download bundle has a manifest: '+archive.name):
            return
        name=manifests[0];prefix=name[:-len('MANIFEST.sha256')]
        for line in z.read(name).decode('utf-8').splitlines():
            if not line.strip():continue
            match=re.fullmatch(r'([0-9a-fA-F]{64})  (.+)',line)
            if not match:
                errors.append('invalid manifest record');continue
            digest,relative=match.groups();member=prefix+relative;count+=1
            try:
                target=contained(component,relative)
                if member not in names or hashlib.sha256(z.read(member)).hexdigest()!=digest.lower():errors.append({'path':relative,'error':'archive manifest mismatch'})
                elif not target.is_file() or sha256_file(target)!=digest.lower():errors.append({'path':relative,'error':'expanded public component differs'})
            except ValueError:
                errors.append({'path':relative,'error':'unsafe member path'})
        audit.check(bool(count) and not errors,'Download bundle matches expanded component: '+archive.name,{'files':count,'errors':errors})


def privacy_scan(audit: Audit, archives=True, extra_archives=()):
    findings = []
    scanned = 0
    archive_seen = set()

    def scan_bytes(label, data, historical=False):
        nonlocal scanned
        scanned += 1
        for kind, pattern in PATTERNS.items():
            count = sum(1 for _ in pattern.finditer(data))
            if count:
                findings.append({'path': label, 'category': kind, 'matches': count, 'classification': 'note' if kind == 'runtime_path_note' else 'review', 'historical': historical})

    def scan_zip(label, data, depth=0):
        # Sources are repeated in downloads and atlas archives. The same sealed
        # ZIP is scanned once by content, while all its manifest paths are checked.
        digest = hashlib.sha256(data).digest()
        if digest in archive_seen:
            return
        archive_seen.add(digest)
        try:
            with zipfile.ZipFile(io.BytesIO(data)) as z:
                for i in z.infolist():
                    if i.is_dir():
                        continue
                    p = PurePosixPath(i.filename)
                    child = label + '!' + i.filename
                    if p.name in PRIVATE_NAMES or '.library_helpers' in i.filename:
                        findings.append({'path': child, 'category': 'private_or_helper_file', 'classification': 'review', 'historical': True})
                    if p.suffix.lower() in TEXT_SUFFIXES:
                        scan_bytes(child, z.read(i), historical=True)
                    elif depth < 2 and p.suffix.lower() == '.zip':
                        scan_zip(child, z.read(i), depth + 1)
        except zipfile.BadZipFile:
            audit.check(False, 'ZIP readable: ' + label)

    for base, dirs, names in os.walk(audit.root):
        dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]
        for name in names:
            path = Path(base) / name
            rel = audit.rel(path)
            if name in PRIVATE_NAMES or '.library_helpers' in rel:
                findings.append({'path': rel, 'category': 'private_or_helper_file', 'classification': 'review', 'historical': False})
            if path.is_symlink():
                audit.check(path.resolve().is_relative_to(audit.root), 'Symlink remains inside repository: ' + rel)
            if path.suffix.lower() in TEXT_SUFFIXES:
                # The scanner necessarily contains pattern names; its source and
                # emitted reports are not data disclosures and are excluded.
                if path.resolve() == Path(__file__).resolve() or (path.parent.name == 'verification' and name.endswith(('_results.json', '_audit.json'))):
                    continue
                scan_bytes(rel, path.read_bytes(), historical=rel.startswith(('compendium/', 'research/')))
            elif archives and path.suffix.lower() == '.zip':
                scan_zip(rel, path.read_bytes())
    if archives:
        for label,path in extra_archives:
            scan_zip(label,path.read_bytes())
    critical = [f for f in findings if f['classification'] == 'review']
    audit.check(not critical, 'No Library identifiers/helpers or credential material in public payload', {'text_members_scanned': scanned, 'review_findings': critical})
    notes = [f for f in findings if f['classification'] == 'note']
    if notes:
        audit.warn('Nonsecret historical runtime paths remain; they are not portability guarantees or credentials.', notes)
    return findings


def coverage(audit: Audit, atlas, table: Path):
    corpus = atlas.get('corpus', [])
    supplementary = atlas.get('supplementary', [])
    entries = corpus + supplementary
    expected = {e['uid']: e for e in entries}
    audit.check(len(corpus) == 1051 and len({e['uid'] for e in corpus}) == 1051, 'Atlas contains 1,051 unique main treatments')
    audit.check(len(supplementary) == 14 and len(expected) == 1065, 'Atlas retains fourteen distinct supplementary treatments')
    audit.check(dict(collections.Counter(e['year'] for e in corpus)) == EXPECTED_YEARS, 'Atlas annual main-treatment coverage')
    if not audit.check(table.is_file(), 'Root treatment table exists'):
        return
    with table.open(encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        columns = set(reader.fieldnames or [])
        rows = list(reader)
    if not audit.check({'uid', 'kind', 'source_payload_sha256'} <= columns, 'Treatment table has identity, kind and canonical source-hash columns'):
        return
    ids = [r['uid'] for r in rows]
    audit.check(len(ids) == len(set(ids)) == 1065 and set(ids) == set(expected), 'Treatment table covers exactly all 1,065 source bodies', {'rows': len(ids), 'missing': sorted(set(expected)-set(ids)), 'unexpected': sorted(set(ids)-set(expected))})
    mismatches = []
    for row in rows:
        e = expected.get(row['uid'])
        if not e:
            continue
        if row['source_payload_sha256'].lower() != canonical_hash(e['source']):
            mismatches.append({'uid': row['uid'], 'column': 'source_payload_sha256'})
        for col, value in [('year', str(e['year'])), ('source_id', e['source_id']), ('title', e['source']['title'])]:
            if col in columns and row[col] != value:
                mismatches.append({'uid': row['uid'], 'column': col})
    audit.check(not mismatches, 'Root table identities and full source hashes match atlas', {'mismatches': mismatches})
    audit.check(len({r['kind'] for r in rows if r['uid'] in {e['uid'] for e in supplementary}}) == 1 and all(r['kind'] for r in rows), 'Table marks supplementary bodies separately', {'kind_counts': dict(collections.Counter(r['kind'] for r in rows))})
    main_kinds = {r['kind'] for r in rows if r['uid'] in {e['uid'] for e in corpus}}
    supplement_kinds = {r['kind'] for r in rows if r['uid'] in {e['uid'] for e in supplementary}}
    audit.check(not main_kinds & supplement_kinds, 'Main and supplementary table kinds are disjoint')


def documentation_links(audit: Audit, components):
    # Root navigation is new publication material. Do not reinterpret all old
    # relative links in immutable annual narrative files as root navigation.
    docs = [audit.root / 'README.md']
    for folder in ['discussions', 'tables', 'verification', 'papers', 'docs', 'bibliography', 'downloads']:
        p = audit.root / folder
        if p.is_dir():
            docs += list(p.rglob('*.md'))
    github_paper=audit.root/'research/hamiltonian/GITHUB_RESEARCH.md'
    if github_paper.is_file():docs.append(github_paper)
    local_targets = set()
    broken = []
    for p in docs:
        if not p.is_file():
            continue
        text = p.read_text(encoding='utf-8')
        for raw in re.findall(r'\]\(([^)]+)\)', text):
            target = raw.strip().split(' "', 1)[0].strip('<>')
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            path = (p.parent / unquote(parsed.path)).resolve()
            if not path.is_relative_to(audit.root) or not path.exists():
                broken.append({'document': audit.rel(p), 'target': target})
            else:
                local_targets.add(path)
    audit.check(not broken, 'Publication navigation links resolve locally', {'documents_checked': len(docs), 'broken_links': broken})
    pdfs = sorted({p.resolve() for component in components for p in component.rglob('*.pdf')})
    bad_headers=[]
    for path in pdfs:
        with path.open('rb') as f:
            if f.read(5)!=b'%PDF-':bad_headers.append(audit.rel(path))
    audit.check(not bad_headers,'Delivered PDF files have PDF headers',{'invalid_headers':bad_headers})
    missing = [audit.rel(p) for p in pdfs if p not in local_targets]
    audit.check(len(pdfs) >= 6 and not missing, 'Every delivered paper/PDF has a publication navigation link', {'pdfs': len(pdfs), 'unlinked_pdfs': missing})


def replay_suite(label, package: Path, args, timeout, copy_first=False):
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONUTF8='1')
    env.pop('PYTHONPATH', None)
    def run(target):
        proc = subprocess.run([sys.executable, '-B', '-X', 'utf8', '-S', str(target/'verify_all.py'), *args], cwd=target, env=env, capture_output=True, text=True, encoding='utf-8', timeout=timeout)
        parsed = None
        try:
            parsed = json.loads(proc.stdout)
        except json.JSONDecodeError:
            pass
        return {'suite': label, 'return_code': proc.returncode, 'command': ['python3', '-B', '-X', 'utf8', '-S', 'verify_all.py', *args], 'result': parsed, 'stdout': proc.stdout if parsed is None else None, 'stderr': proc.stderr}
    try:
        if copy_first:
            with tempfile.TemporaryDirectory(prefix='publication-annual-') as tmp:
                target = Path(tmp)/'annual'
                shutil.copytree(package, target, ignore=shutil.ignore_patterns('__pycache__', '.git'))
                return run(target)
        return run(package)
    except subprocess.TimeoutExpired:
        return {'suite': label, 'return_code': 124, 'error': 'suite timeout'}
    except Exception as e:
        return {'suite': label, 'return_code': 1, 'error': type(e).__name__ + ': ' + str(e)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--table', default='tables/treatments.csv', help='Repository-relative canonical coverage table')
    parser.add_argument('--audit-only', action='store_true', help='Do not execute mathematical suites; report this limitation explicitly')
    parser.add_argument('--output', type=Path, help='Optional report path; the default prints JSON without writing files')
    parser.add_argument('--timeout', type=int, default=1200, help='Seconds allowed per top-level suite')
    parser.add_argument('--annual-workers', type=int, default=2, choices=range(1,5), help='Annual runners already parallelize internally')
    parser.add_argument('--skip-archive-privacy-scan', action='store_true', help='Faster local audit; nested ZIP disclosures then remain unreviewed')
    args = parser.parse_args()
    if sys.version_info < (3,10):
        parser.error('Python 3.10 or later is required')
    root = args.root.resolve()
    audit = Audit(root)
    annuals = {y: root/'compendium/years'/str(y) for y in EXPECTED_YEARS}
    atlas_root = root/'compendium/atlas'
    hamiltonian = root/'research/hamiltonian'
    payloads = {}
    components = list(annuals.values()) + [atlas_root, hamiltonian]
    # Manifest verification always precedes running programs that may produce
    # fresh reports. Annual programs run only in disposable copies below.
    for component in components:
        audit.check((component/'verify_all.py').is_file(), 'Suite runner present: '+audit.rel(component))
        audit.manifest(component)
    if (root/'MANIFEST.sha256').exists():
        audit.manifest(root)
    else:
        audit.warn('No repository-wide manifest; component manifests are still mandatory.')
    for year, path in annuals.items():
        if not audit.check((path/'compendium.json').is_file(), f'Annual payload present: {year}'):
            continue
        payload = load(path/'compendium.json'); payloads[year] = payload
        ids = [e['id'] for e in payload['entries']]
        audit.check(len(ids) == len(set(ids)) == EXPECTED_YEARS[year], f'Annual payload coverage: {year}', {'main_treatments': len(ids)})
        archive_audit(audit, atlas_root/'sources'/f'{year}_Mathematics_Source_Bundle.zip', path, year, payload)
    for year in EXPECTED_YEARS:
        sealed=atlas_root/'sources'/f'{year}_Mathematics_Source_Bundle.zip'
        download=root/'downloads'/sealed.name
        audit.check(download.is_file() and sealed.is_file() and sha256_file(download)==sha256_file(sealed),f'Annual download equals atlas source archive: {year}')
    atlas_delivery_temporary=tempfile.TemporaryDirectory(prefix='publication-atlas-delivery-')
    atlas_download=resolve_atlas_download(audit,root,Path(atlas_delivery_temporary.name))
    if atlas_download is not None:delivered_archive_audit(audit,atlas_download,atlas_root)
    delivered_archive_audit(audit,root/'downloads/Nonlinear_Hamiltonian_Partners_Source_Bundle.zip',hamiltonian)
    atlas = None
    atlas_path = atlas_root/'data/atlas.json'
    if audit.check(atlas_path.is_file(), 'Integrated atlas payload present'):
        atlas = load(atlas_path)
        coverage(audit, atlas, contained(root, args.table))
        for year, payload in payloads.items():
            observed = {e['source_id']: e['source'] for e in atlas['corpus'] if e['year'] == year}
            audit.check(observed == {e['id']: e for e in payload['entries']}, f'Atlas preserves complete annual treatment bodies: {year}')
        if 2023 in payloads:
            audit.check([e['source'] for e in atlas['supplementary']] == payloads[2023]['syntheses'], 'Atlas preserves all fourteen annual synthesis bodies')
        volumes = {v['year']: v for v in atlas.get('source_volumes', [])}
        for year, path in annuals.items():
            if year in volumes and year in payloads:
                audit.check(sha256_file(path/'compendium.json') == volumes[year]['compendium_sha256'], f'Annual payload hash agrees with atlas provenance: {year}')
    redactions=root/'verification/publication_redactions.json'
    if redactions.exists():
        record=load(redactions)
        for name,item in record.get('archives',{}).items():
            for relative in item.get('public_locations',[]):
                is_atlas_delivery=(relative=='downloads/'+ATLAS_ARCHIVE_NAME or item.get('reassembled_filename')=='downloads/'+ATLAS_ARCHIVE_NAME)
                path=atlas_download if is_atlas_delivery else contained(root,relative)
                audit.check(path is not None and path.is_file() and sha256_file(path)==item['public_derivative_sha256'],'Documented public-derivative hash: '+relative)
        for relative,digest in record.get('canonical_mathematical_payloads_unchanged',{}).items():
            path=contained(root,relative)
            audit.check(path.is_file() and sha256_file(path)==digest,'Documented unchanged mathematical payload: '+relative)
        audit.check(record.get('occurrences_redacted')==2 and record.get('identifier_values_recorded') is False,'Redaction provenance records counts without identifier values')
    documentation_links(audit, components)
    extra_archives=[('downloads/atlas-source-parts (reassembled atlas ZIP)',atlas_download)] if atlas_download is not None else []
    privacy = privacy_scan(audit, archives=not args.skip_archive_privacy_scan,extra_archives=extra_archives)
    if args.skip_archive_privacy_scan:
        audit.warn('Nested ZIP privacy scan was explicitly omitted; archive manifests and source equality were still checked.')
    replay = []
    if not args.audit_only:
        audit.check(shutil.which('node') is not None, 'Node.js available for actual atlas engine replay')
        # Four annual top-level runners, each once. The atlas is then forbidden
        # from launching those four runners again via its --skip-annual flag.
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.annual_workers) as pool:
            replay = list(pool.map(lambda item: replay_suite('annual:'+str(item[0]), item[1], [], args.timeout, True), annuals.items()))
        replay.append(replay_suite('atlas:integration-domains-labs', atlas_root, ['--skip-annual'], args.timeout))
        replay.append(replay_suite('Hamiltonian:newest-delivered-bundle', hamiltonian, [], args.timeout))
        for r in replay:
            result_status = (r.get('result') or {}).get('status')
            audit.check(r['return_code'] == 0 and result_status in ('passed','pass'), 'Mathematical suite: '+r['suite'], {'return_code': r['return_code'], 'result_status': result_status})
        by_label = collections.Counter(r['suite'] for r in replay)
        audit.check(all(by_label['annual:'+str(y)] == 1 for y in EXPECTED_YEARS) and len(replay) == 6, 'Each annual runner once, atlas once with --skip-annual, Hamiltonian once')
    result = {
        'status': 'passed' if not audit.failures else 'failed',
        'mode': 'audit-only; no mathematical suites replayed' if args.audit_only else 'full audit and six top-level suite runs',
        'counts': {'main_treatments':1051,'supplementary_treatments':14,'source_bodies':1065,'annual_volumes':4},
        'checks': audit.records, 'failures': audit.failures, 'warnings': audit.warnings,
        'replay': replay,
        'privacy_scope': {'nested_archives_scanned':not args.skip_archive_privacy_scan,'findings':privacy,'note':'Findings expose paths and categories, never matched credential or identifier values. Nonsecret historical runtime paths are notes.'},
        'claim_scope': 'Integrity and source coverage plus the scoped finite/exact/numerical checks implemented by the delivered suites. This is not fresh historical transcript retrieval, formal proof-kernel certification of all prose, or a rerun of absent historical research inputs.'
    }
    rendered = json.dumps(result, ensure_ascii=False, indent=2)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(rendered,encoding='utf-8')
    print(rendered,end='')
    atlas_delivery_temporary.cleanup()
    return 0 if not audit.failures else 1


if __name__ == '__main__':
    raise SystemExit(main())
