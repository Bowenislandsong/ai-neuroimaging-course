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
        if n.metadata.get('execution_tier') not in {'offline','network'}:
            errors.append(f'{p.relative_to(ROOT)}: undefined execution tier')
        if not any(c.cell_type=='code' and c.source.strip() for c in n.cells):
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
