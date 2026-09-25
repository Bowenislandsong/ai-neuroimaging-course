#!/usr/bin/env python3
"""Execute our teaching notebooks in fresh Jupyter kernels; exclude upstream copies.

No scientific interpretation is certified by a passing run. Reading seminars are
human-assessed, not marked as executed. Network-tier projects
require an explicit flag. Executed copies go in ignored build/executed/ by default.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import importlib.metadata
import json
import os
from pathlib import Path
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]
# Isolate writable caches and ensure the kernel uses this exact Python environment.
CACHE = ROOT / 'build' / 'runtime'
CACHE.mkdir(parents=True, exist_ok=True)
os.environ.setdefault('MPLBACKEND', 'module://matplotlib_inline.backend_inline')
os.environ.setdefault('MPLCONFIGDIR', str(CACHE / 'matplotlib'))
os.environ.setdefault('XDG_CACHE_HOME', str(CACHE / 'cache'))
specdir = CACHE / 'jupyter' / 'kernels' / 'course-python'
specdir.mkdir(parents=True, exist_ok=True)
(specdir / 'kernel.json').write_text(json.dumps({
    'argv': [sys.executable, '-m', 'ipykernel_launcher', '-f', '{connection_file}', '--IPKernelApp.log_level=ERROR'],
    'display_name': 'Course validation Python', 'language': 'python',
}))
os.environ['JUPYTER_PATH'] = str(CACHE / 'jupyter') + os.pathsep + os.environ.get('JUPYTER_PATH', '')

import nbformat
from nbclient import NotebookClient


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--include-network', action='store_true')
    parser.add_argument('--match', default='', help='Only paths containing this text')
    parser.add_argument('--publish-offline-outputs', action='store_true', help='Update original offline notebooks with executed outputs')
    parser.add_argument('--report', default='build/validation.json')
    args = parser.parse_args()
    results = []
    for path in sorted((ROOT/'notebooks').glob('*/*.ipynb')):
        rel = str(path.relative_to(ROOT))
        if args.match and args.match not in rel:
            continue
        notebook = nbformat.read(path, as_version=4)
        nbformat.validate(notebook)
        tier = notebook.metadata.get('execution_tier', 'offline')
        row = {'path':rel, 'course_id':notebook.metadata.get('course_id'), 'tier':tier}
        if tier == 'reading':
            row['status']='skipped'; row['reason']='reading seminar; requires human assessment, not execution'
            results.append(row); print('READING',rel,flush=True); continue
        if tier != 'offline' and not args.include_network:
            row['status']='skipped'; row['reason']='requires --include-network'
            results.append(row); print('SKIP',rel,flush=True); continue
        start=time.monotonic()
        try:
            # Notebooks are ordinary Python, with no deliberate unexecuted cells.
            skipped=[i for i,c in enumerate(notebook.cells) if c.cell_type=='code' and 'skip-execution' in c.metadata.get('tags',[])]
            for i in skipped:
                notebook.cells[i].source = '# Explicitly unexecuted optional cell; see source notebook.'
            NotebookClient(notebook, timeout=240, kernel_name='course-python', resources={'metadata':{'path':str(ROOT)}}, allow_errors=False).execute()
            row.update(status='passed',code_cells=sum(c.cell_type=='code' for c in notebook.cells)-len(skipped),explicitly_skipped_cells=skipped,
                       figures=sum('image/png' in o.get('data',{}) for c in notebook.cells if c.cell_type=='code' for o in c.get('outputs',[])))
            target=ROOT/'build'/'executed'/path.relative_to(ROOT/'notebooks')
            target.parent.mkdir(parents=True,exist_ok=True); nbformat.write(notebook,target)
            if args.publish_offline_outputs and tier=='offline' and not skipped:
                # Kernel absolute interpreter paths are not part of the teaching artifact.
                notebook.metadata.kernelspec={'display_name':'Python 3','language':'python','name':'python3'}
                nbformat.write(notebook,path)
            print('PASS',rel,flush=True)
        except Exception as error:
            row.update(status='failed',error=str(error))
            print('FAIL',rel,str(error)[-1500:],flush=True)
        row['seconds']=round(time.monotonic()-start,2)
        results.append(row)
    packages=['numpy','scipy','pandas','matplotlib','scikit-learn','nibabel','nilearn','nbformat','nbclient','ipykernel']
    report={'checked_at_utc':datetime.now(timezone.utc).isoformat(), 'method':'nbclient; fresh ipykernel per notebook; source order; no allowed errors',
            'python':sys.version.split()[0], 'packages':{p:importlib.metadata.version(p) for p in packages},
            'upstream_notebooks':'Excluded; reference copies and student exercises are not certified as executed',
            'results':results}
    output=ROOT/args.report;output.parent.mkdir(parents=True,exist_ok=True);output.write_text(json.dumps(report,indent=2))
    print(json.dumps({s:sum(r['status']==s for r in results) for s in ['passed','failed','skipped']}),flush=True)
    return 1 if not results or any(r['status']=='failed' for r in results) else 0

if __name__=='__main__':
    raise SystemExit(main())
