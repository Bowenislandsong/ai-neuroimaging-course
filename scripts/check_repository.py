#!/usr/bin/env python3
"""Validate core notebook structure, local teaching links and preserved source hashes."""
from pathlib import Path
import hashlib
import json
import re
from urllib.parse import unquote, urlsplit
import nbformat

ROOT=Path(__file__).resolve().parents[1]
errors=[]
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
        for c in n.cells:
            for o in c.get('outputs',[]):
                if o.output_type=='error':errors.append(f'{p.relative_to(ROOT)}: saved error output')
    except Exception as e:errors.append(f'{p.relative_to(ROOT)}: {e}')
for folder in ['curriculum','course']:
    texts += [(p,p.read_text()) for p in (ROOT/folder).rglob('*.md')]
texts += [(p,p.read_text()) for p in ROOT.glob('*.md')]
texts += [(p,p.read_text()) for p in (ROOT/'third_party').glob('*/README.md')]
texts += [(ROOT/'third_party/README.md',(ROOT/'third_party/README.md').read_text())]
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
