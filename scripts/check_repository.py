#!/usr/bin/env python3
"""Validate core notebook structure, local teaching links and preserved source hashes."""
from pathlib import Path
import hashlib
import json
import re
import tomllib
from urllib.parse import unquote, urlsplit
import nbformat
from build_reading_indexes import (
    AGENTIC_BLOCK,
    AGENTIC_GUIDES,
    KEY_BLOCK,
    KEY_REFERENCES,
    KEY_ROLES,
    VERIFICATION,
    agentic_guide_block,
    key_reference_block,
    load_agentic_guides,
    reference_key,
)

ROOT=Path(__file__).resolve().parents[1]
errors=[]
# Absolute home directories must never reach the public repository (outputs, prose or code).
LOCAL_PATH=re.compile(r'(?<![\w.:/])(?:/usr/local/google/home|/home|/Users)/[\w.-]+/')
# Signatures of math whose parenthesized arguments were stripped; KaTeX rejects all of them.
DELIMITER=r'[()\[\]|./<>]|\\[{}|]|\\(?:[lr]?[vV]ert|[lr]angle|[lr]floor|[lr]ceil|[lr]brace|[lr]brack|backslash)(?![A-Za-z])'
BROKEN_MATH=re.compile(r'\\left(?![A-Za-z])(?!\s*(?:'+DELIMITER+r'))|\\right(?![A-Za-z])(?!\s*(?:'+DELIMITER+r'))'
                       r'|\\text\{\}|\\[bB]igg?[lr]?\s*[-+=]')
project=tomllib.loads((ROOT/'pyproject.toml').read_text())
declared={x.replace(' ','') for x in project['project']['dependencies']}
legacy={x.replace(' ','') for x in (ROOT/'requirements.txt').read_text().splitlines() if x.strip() and not x.lstrip().startswith('#')}
if declared!=legacy:errors.append('requirements.txt differs from uv project dependencies')
if not (ROOT/'uv.lock').exists():errors.append('Missing uv.lock')
ids=set()
notebooks=sorted((ROOT/'notebooks').glob('*/*.ipynb'))
texts=[]
for p in notebooks:
    try:
        n=nbformat.read(p,as_version=4);nbformat.validate(n)
        ident=n.metadata.get('course_id')
        if not ident or ident in ids:errors.append(f'{p.relative_to(ROOT)}: missing/duplicate ID {ident}')
        ids.add(ident)
        tier=n.metadata.get('execution_tier')
        if tier not in {'offline','network','reading'}:
            errors.append(f'{p.relative_to(ROOT)}: undefined execution tier')
        if tier=='reading':
            if not n.metadata.get('paper_ids') or not n.metadata.get('assessment'):
                errors.append(f'{p.relative_to(ROOT)}: reading seminar needs paper IDs and assessment')
            if any(c.cell_type=='code' for c in n.cells):
                errors.append(f'{p.relative_to(ROOT)}: reading-only seminar contains code')
        elif not any(c.cell_type=='code' and c.source.strip() for c in n.cells):
            errors.append(f'{p.relative_to(ROOT)}: no executable lesson')
        texts.append((p,'\n'.join(c.source for c in n.cells if c.cell_type=='markdown')))
        for i,c in enumerate(n.cells):
            if c.cell_type=='markdown':
                for hit in BROKEN_MATH.finditer(c.source):
                    errors.append(f'{p.relative_to(ROOT)}: cell {i}: broken math near {c.source[max(0,hit.start()-30):hit.end()+20]!r}')
            if LOCAL_PATH.search(c.source):errors.append(f'{p.relative_to(ROOT)}: cell {i}: absolute local path in source')
            for o in c.get('outputs',[]):
                if o.output_type=='error':errors.append(f'{p.relative_to(ROOT)}: saved error output')
                if o.output_type=='stream' and o.get('name')=='stderr':
                    errors.append(f'{p.relative_to(ROOT)}: cell {i}: saved stderr output (fix the warning, do not store it)')
                if LOCAL_PATH.search(json.dumps(o)):errors.append(f'{p.relative_to(ROOT)}: cell {i}: absolute local path in output')
    except Exception as e:errors.append(f'{p.relative_to(ROOT)}: {e}')
for folder in ['curriculum','course']:
    texts += [(p,p.read_text()) for p in (ROOT/folder).rglob('*.md')]
texts += [(p,p.read_text()) for p in ROOT.glob('*.md')]
texts += [(p,p.read_text()) for p in (ROOT/'third_party').glob('*/README.md')]
texts += [(ROOT/'third_party/README.md',(ROOT/'third_party/README.md').read_text())]
for p,s in texts:
    if p.suffix=='.md' and LOCAL_PATH.search(s):errors.append(f'{p.relative_to(ROOT)}: absolute local path')
links=0
for p,s in texts:
    s=re.sub(r'```.*?```','',s,flags=re.S)
    for destination in re.findall(r'\[[^\]]*\]\(([^\s)]+)(?:\s+"[^"]*")?\)',s):
        u=urlsplit(destination.strip('<>'))
        if u.scheme or u.netloc or not u.path:continue
        target=(p.parent/unquote(u.path)).resolve()
        links+=1
        if not target.exists():errors.append(f'{p.relative_to(ROOT)}: missing link {destination}')
# Paper records and notebook reading gates must refer to real course material.
paper_registry=ROOT/'curriculum/papers/paper_registry.json'
if paper_registry.exists():
    papers=json.loads(paper_registry.read_text())['papers']
    paper_ids={x['id'] for x in papers}
    if len(papers)!=len(paper_ids):errors.append('Duplicate paper IDs')
    for paper in papers:
        for key in ['id','title','year','status','url','fulltext_url','role','read_sections']:
            if not paper.get(key):errors.append(f'{paper.get("id")}: missing paper field {key}')
        for ident in paper.get('notebook_ids',[]):
            if ident not in ids:errors.append(f'{paper["id"]}: unknown notebook {ident}')
    for p in notebooks:
        n=nbformat.read(p,4)
        if not n.metadata.get('paper_ids'):
            errors.append(f'{p.relative_to(ROOT)}: missing paper motivation')
        for ident in n.metadata.get('paper_ids',[]):
            if ident not in paper_ids:errors.append(f'{p.relative_to(ROOT)}: unknown paper {ident}')
    index=json.loads((ROOT/'curriculum/notebook_index.json').read_text())
    if {r['id'] for r in index}!=ids or len(index)!=len(notebooks):
        errors.append('Notebook index does not match original notebook IDs')
    for record in index:
        path=ROOT/record['path']
        if not path.exists():
            errors.append(f'Notebook index: missing {record["path"]}')
            continue
        meta=nbformat.read(path,4).metadata
        if (record['id']!=meta.get('course_id') or
            record['execution_tier']!=meta.get('execution_tier') or
            record.get('paper_ids')!=meta.get('paper_ids')):
            errors.append(f'Notebook index metadata mismatch: {record["path"]}')
    # Reading guides use explicit anchors so versioned paper links remain stable.
    for p,s in texts:
        for destination in re.findall(r'\[[^\]]*\]\(([^\s)]+)(?:\s+"[^"]*")?\)',s):
            u=urlsplit(destination.strip('<>'))
            if u.scheme or u.netloc or not u.fragment:continue
            target=(p.parent/unquote(u.path)).resolve() if u.path else p
            if (target.is_file() and target.suffix=='.md' and
                (ROOT/'curriculum/papers' in target.parents or ROOT/'curriculum/coursework' in target.parents)):
                anchors=re.findall(r'<a\s+id="([^"]+)"',target.read_text())
                if unquote(u.fragment) not in anchors:
                    errors.append(f'{p.relative_to(ROOT)}: missing reading anchor {destination}')
    # Each computational lesson renders two to four verified key references (key_references.json).
    if KEY_REFERENCES.exists():
        by_id={x['id']:x for x in papers}
        lessons=json.loads(KEY_REFERENCES.read_text())['lessons']
        verified=json.loads(VERIFICATION.read_text())['references'] if VERIFICATION.exists() else {}
        entries={x['notebook_id']:x for x in lessons}
        if len(entries)!=len(lessons):errors.append('key_references.json: duplicate lesson entries')
        for pid in sorted(paper_ids-{r.get('library_id') for r in verified.values() if r.get('status')=='MATCH'}):
            errors.append(f'{pid}: library paper lacks a MATCH record; run scripts/verify_references.py')
        computational=set()
        for p in notebooks:
            n=nbformat.read(p,4);ident=n.metadata.get('course_id')
            if n.metadata.get('execution_tier')=='reading':continue
            computational.add(ident)
            entry=entries.get(ident)
            if entry is None:
                errors.append(f'{ident}: missing from key_references.json');continue
            refs=entry.get('references',[])
            if not entry.get('technique') or not entry.get('why_it_matters'):
                errors.append(f'{ident}: key references need technique and why_it_matters')
            if not 2<=len(refs)<=4:errors.append(f'{ident}: needs two to four key references')
            if not any(r.get('role') in {'foundational','standard tool'} for r in refs):
                errors.append(f'{ident}: needs a foundational or standard-tool key reference')
            if not any(int(r.get('year') or 0)>=2019 for r in refs):
                errors.append(f'{ident}: needs a key reference published in 2019 or later')
            for r in refs:
                missing=[k for k in ['role','cite','authors','year','title','venue','takeaway'] if not r.get(k)]
                if missing or r.get('role') not in KEY_ROLES or not (r.get('doi') or r.get('arxiv')):
                    errors.append(f'{ident}: malformed key reference {str(r.get("title"))[:60]!r} (missing {missing})');continue
                if r.get('registry_id') and r['registry_id'] not in paper_ids:
                    errors.append(f'{ident}: unknown registry_id {r["registry_id"]}')
                status=verified.get(reference_key(r),{}).get('status','UNVERIFIED')
                if status!='MATCH':errors.append(f'{ident}: {reference_key(r)} is {status}; run scripts/verify_references.py')
            try:expected=key_reference_block(entry,by_id)
            except (KeyError,ValueError):expected=None
            source=next(c for c in n.cells if c.cell_type=='markdown').source
            if [b.strip() for b in KEY_BLOCK.findall(source)]!=[expected]:
                errors.append(f'{ident}: first cell lacks the current key-references block; run scripts/build_reading_indexes.py')
        for ident in sorted(set(entries)-computational):
            errors.append(f'key_references.json: {ident} is not a computational notebook')
    # Every notebook renders its macOS agentic deliverable supervision block (agentic_guides.json).
    if AGENTIC_GUIDES.exists():
        agentic_guides=load_agentic_guides()
        for p in notebooks:
            n=nbformat.read(p,4);ident=n.metadata.get('course_id')
            guide=agentic_guides.get(ident)
            if guide is None:
                errors.append(f'{ident}: missing from curriculum/agentic_guides.json');continue
            for req in ('deliverable_focus','suggestive_prompt','what_to_look_for_and_trace','expected_outcome_range_and_why'):
                if not guide.get(req):
                    errors.append(f'{ident}: agentic_guides.json missing {req}')
            expected_guide=agentic_guide_block(ident,guide)
            full_md='\n\n'.join(c.source for c in n.cells if c.cell_type=='markdown')
            if [b.strip() for b in AGENTIC_BLOCK.findall(full_md)]!=[expected_guide]:
                errors.append(f'{ident}: notebook lacks the current agentic-guide block; run scripts/build_reading_indexes.py')
        for ident in sorted(set(agentic_guides)-ids):
            errors.append(f'agentic_guides.json: unknown notebook {ident}')
# Different upstream projects expose different manifest schemas; all source bytes
# remain unchanged. Metadata-only sources that were read but not copied are skipped.
records=[]
for name in ['data_science','design']:
    records += json.loads((ROOT/f'third_party/{name}/manifest.json').read_text())
records += [x for x in json.loads((ROOT/'third_party/modeling/sources_manifest.json').read_text())['sources'] if x.get('vendored')]
for x in json.loads((ROOT/'third_party/processing/PROVENANCE.json').read_text())['files']:
    records.append({'local_path':'third_party/processing/'+x['local_file'],'sha256':x['upstream_sha256']})
for record in records:
    p=ROOT/record['local_path']
    if not p.exists() or hashlib.sha256(p.read_bytes()).hexdigest()!=record['sha256']:
        errors.append(f'Upstream byte hash mismatch: {record["local_path"]}')
print(f'{len(notebooks)} original notebooks; {len(ids)} unique IDs; {links} local links; {len(records)} upstream file hashes')
if errors:
    print('\n'.join(errors));raise SystemExit(1)
print('Repository checks passed. External-link access and scientific validity are separate checks.')
