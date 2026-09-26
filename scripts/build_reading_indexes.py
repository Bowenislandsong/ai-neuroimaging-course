#!/usr/bin/env python3
"""Build paper/lesson indexes and insert original paper questions, preserving code.

Edit curriculum/papers/*_sources.json and lesson_readings.json, then run this.
The supplied notebooks' code cells and reference outputs are not regenerated.
"""
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT / 'curriculum/papers'


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')


def main():
    papers = []
    for strand in ['measurement', 'processing', 'design', 'modeling']:
        data = json.loads((PAPERS / f'{strand}_sources.json').read_text())
        for record in data if isinstance(data, list) else data['papers']:
            paper = dict(record)
            paper['guide'] = f'{strand}.md#{paper["id"].lower()}'
            paper['source_registry'] = f'{strand}_sources.json'
            papers.append(paper)
    by_id = {p['id']: p for p in papers}
    assignments = {x['notebook_id']: x for x in json.loads((PAPERS / 'lesson_readings.json').read_text())}
    groups = [
        ('00_paper_orientation', 'Paper orientation — start here'),
        ('00_foundations', 'Foundations'), ('01_processing', 'Processing'),
        ('02_design', 'Research design'), ('03_data_science', 'Data science'),
        ('04_modeling', 'Modeling'), ('05_projects', 'Projects'),
    ]
    index = []
    markdown = ['# Every class', '',
        '**Start with R00–R03 before F01.** Use the [26-week study sequence](STUDY_PLAN.md) to interleave the strands. '
        'These 83 notebooks contain 79 computational lessons/projects and four human-assessed reading seminars. '
        'The [18-paper library](papers/README.md) supplies exact readings, questions and assignments. '
        'Paper links motivate a question; they do not mean each paper implements every local method.', '',
        'Offline computational notebooks include reference outputs; P02 requires a public-data download. '
        'Reading seminars are submitted for discussion and assessment, not marked as executed. '
        '[Setup](SETUP.md) · [AI workflow](AI_WORKFLOW.md) · [Assessments](ASSESSMENT.md)', '']
    for directory, title in groups:
        markdown += [f'## {title}', '', '| ID | Class | Type | Paper questions |', '|---|---|---|---|']
        group_index = []
        for path in sorted((ROOT / 'notebooks' / directory).glob('*.ipynb')):
            notebook = json.loads(path.read_text())
            ident = notebook['metadata']['course_id']
            tier = notebook['metadata']['execution_tier']
            if tier != 'reading':
                assignment = assignments[ident]
                ids = assignment['paper_ids']
                notebook['metadata']['paper_ids'] = ids
                links = ', '.join(f'[{pid}](../../curriculum/papers/{by_id[pid]["guide"]})' for pid in ids)
                gate = ('<!-- paper-first -->\n'
                    '### Research question\n\n'
                    f'**Reading:** {links}. Review the assigned figure or result before starting the lesson.\n\n'
                    f'**Question:** {assignment["motivation_question"]}\n\n'
                    'Record a prediction, a source location, and one point you want this lesson to clarify. '
                    'Ask your AI tutor to distinguish the paper’s evidence from its interpretation.\n'
                    '<!-- /paper-first -->')
                cell = next(c for c in notebook['cells'] if c['cell_type'] == 'markdown')
                source = ''.join(cell['source']) if isinstance(cell['source'], list) else cell['source']
                source = re.sub(r'\n*<!-- paper-first -->.*?<!-- /paper-first -->\n*', '\n\n', source, flags=re.S)
                first, separator, rest = source.partition('\n')
                source = first + '\n\n' + gate + '\n\n' + rest.lstrip('\n')
                cell['source'] = source.splitlines(keepends=True)
                notebook['cells'] = [c for c in notebook['cells']
                    if c.get('metadata', {}).get('course_component') != 'paper_return']
                notebook['cells'].append({
                    'cell_type': 'markdown', 'id': f'paper-return-{ident.lower()}',
                    'metadata': {'course_component': 'paper_return'},
                    'source': ('### Return to the research question\n\n'
                        f'Revisit {links} and your initial prediction. In your '
                        '[evidence ledger](../../curriculum/coursework/EVIDENCE_LEDGER.md):\n\n'
                        '1. Cite one output or diagnostic from this lesson and explain the transformation it demonstrates.\n'
                        '2. Revise one claim or question from the paper, with a figure or section locator. '
                        'Which part of the published result remains open after this exercise?\n'
                        '3. Ask AI to propose a next check. Accept, revise or reject it with a scientific reason. '
                        'Then explain your decision aloud without reading the AI response.\n\n'
                        'Include this entry in the A2 portfolio when relevant.\n'
                    ).splitlines(keepends=True),
                })
                # Match nbformat's existing indentation without rewriting any cell values.
                path.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + '\n')
            ids = notebook['metadata'].get('paper_ids', [])
            first_cell = next(c for c in notebook['cells'] if c['cell_type'] == 'markdown')
            first_line = ''.join(first_cell['source']).splitlines()[0]
            lesson_title = re.sub(r'^#+\s*', '', first_line)
            lesson_title = re.sub(r'^(?:[A-Z]+\d+|\d+)\s*[·:—–-]\s*', '', lesson_title)
            record = {'id': ident, 'title': lesson_title, 'path': str(path.relative_to(ROOT)),
                      'execution_tier': tier, 'paper_ids': ids}
            index.append(record)
            group_index.append(record)
            paper_links = ', '.join(f'[{pid}](papers/{by_id[pid]["guide"]})' for pid in ids)
            markdown.append(f'| {ident} | [{lesson_title}](../{record["path"]}) | {tier} | {paper_links} |')
        markdown.append('')
        if directory == '00_paper_orientation':
            write_json(ROOT / 'notebooks' / directory / 'index.json', group_index)
    for paper in papers:
        paper['motivation_notebook_ids'] = [r['id'] for r in index if paper['id'] in r['paper_ids']]
    write_json(PAPERS / 'paper_registry.json', {
        'schema_version': 1,
        'verified_date_utc': '2026-09-25',
        'scope': '18 linked papers and original coursework. Six opening reads precede fundamentals. '
                 'Representative frontier selections are not a global performance ranking. '
                 'Publication and assigned manuscript versions are recorded separately. '
                 'No full paper implementation or large-model reproduction is claimed.',
        'papers': papers,
    })
    write_json(ROOT / 'curriculum/notebook_index.json', index)
    (ROOT / 'curriculum/NOTEBOOK_INDEX.md').write_text('\n'.join(markdown))
    print(f'Built {len(papers)} paper records and {len(index)} notebook entries; updated {len(assignments)} paper questions.')


if __name__ == '__main__':
    main()
