#!/usr/bin/env python3
"""Verify every lesson key reference and library paper against Crossref, OpenAlex and arXiv.

Requires network access; run it after editing curriculum/papers/key_references.json:

    uv run --locked python scripts/verify_references.py

For each unique DOI the script compares the recorded title, year and first author with
Crossref, records OpenAlex and Crossref citation counts, and writes
curriculum/papers/reference_verification.json. arXiv identifiers are checked against the
arXiv API. The offline repository check then requires a MATCH record for every reference.
Citation counts change daily; the file records when they were retrieved.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import difflib
import html
import json
from pathlib import Path
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

from build_reading_indexes import KEY_REFERENCES, reference_key

ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT / 'curriculum/papers'
OUTPUT = PAPERS / 'reference_verification.json'
CONTACT = 'bowenislandsong@gmail.com'
USER_AGENT = f'ai-neuroimaging-course-reference-check/1.0 (mailto:{CONTACT})'


def fetch(url: str, params: dict | None = None, attempts: int = 4) -> bytes | None:
    if params:
        url = url + '?' + urllib.parse.urlencode(params)
    for attempt in range(attempts):
        try:
            request = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
            with urllib.request.urlopen(request, timeout=30) as response:
                return response.read()
        except urllib.error.HTTPError as error:
            if error.code == 404:
                return None
            time.sleep(2 + 2 * attempt)
        except (urllib.error.URLError, TimeoutError):
            time.sleep(2 + 2 * attempt)
    return None


def words(text: str) -> list[str]:
    text = html.unescape(re.sub(r'<[^>]+>', ' ', text or ''))
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode()
    return re.sub(r'[^a-z0-9 ]', ' ', text.lower()).split()


def similarity(a: str, b: str) -> float:
    return round(difflib.SequenceMatcher(None, ' '.join(words(a)), ' '.join(words(b))).ratio(), 3)


def crossref(doi: str) -> dict | None:
    raw = fetch(f'https://api.crossref.org/works/{urllib.parse.quote(doi)}', {'mailto': CONTACT})
    if raw is None:
        return None
    message = json.loads(raw)['message']
    year = None
    for field in ('published-print', 'published-online', 'issued', 'created'):
        parts = (message.get(field) or {}).get('date-parts') or [[None]]
        if parts and parts[0] and parts[0][0]:
            year = parts[0][0]
            break
    authors = message.get('author') or []
    return {
        'title': ' '.join(message.get('title') or ['']),
        'year': year,
        'first_author_family': (authors[0].get('family') or authors[0].get('name')) if authors else None,
        'author_count': len(authors),
        'author_families': [a.get('family') or a.get('name') for a in authors[:3]],
        'venue': ' '.join(message.get('container-title') or ['']) or message.get('publisher'),
        'type': message.get('type'),
        'crossref_cited_by': message.get('is-referenced-by-count'),
    }


def openalex(doi: str) -> dict | None:
    raw = fetch(f'https://api.openalex.org/works/doi:{urllib.parse.quote(doi)}', {'mailto': CONTACT})
    if raw is None:
        return None
    work = json.loads(raw)
    return {'openalex_id': work.get('id'), 'openalex_cited_by': work.get('cited_by_count')}


def arxiv(identifier: str) -> dict | None:
    raw = fetch('https://export.arxiv.org/api/query', {'id_list': identifier})
    if raw is None:
        return None
    ns = {'a': 'http://www.w3.org/2005/Atom'}
    entry = ET.fromstring(raw).find('a:entry', ns)
    if entry is None or entry.find('a:title', ns) is None or entry.find('a:published', ns) is None:
        return None
    names = [a.find('a:name', ns).text for a in entry.findall('a:author', ns)]
    return {'title': ' '.join(entry.find('a:title', ns).text.split()),
            'year': int(entry.find('a:published', ns).text[:4]),
            'first_author_family': names[0].split()[-1] if names else None,
            'author_count': len(names), 'author_families': [n.split()[-1] for n in names[:3]]}


def family_matches(expected: str, found: str | None) -> bool:
    if not expected or not found:
        return True
    return words(found)[:1] == words(expected)[:1] or ' '.join(words(found)) in ' '.join(words(expected))


def collect() -> dict[str, dict]:
    refs: dict[str, dict] = {}
    data = json.loads(KEY_REFERENCES.read_text())
    for lesson in data['lessons']:
        for ref in lesson['references']:
            record = refs.setdefault(reference_key(ref), {'reference': ref, 'lessons': []})
            record['lessons'].append(lesson['notebook_id'])
    for paper in json.loads((PAPERS / 'paper_registry.json').read_text())['papers']:
        doi = paper.get('doi') or ''
        match = re.match(r'10\.48550/arXiv\.(.+)', doi, re.I)
        ref = {'title': paper['title'], 'year': paper['year'], 'registry_id': paper['id']}
        ref.update({'arxiv': match.group(1)} if match else {'doi': doi})
        refs.setdefault(reference_key(ref), {'reference': ref, 'lessons': []})['library'] = paper['id']
    return refs


def verify(ref: dict) -> dict:
    result: dict = {}
    if ref.get('doi'):
        found = crossref(ref['doi'])
        if found is None:
            return {'status': 'DOI_NOT_FOUND'}
        result.update(found)
        result.update(openalex(ref['doi']) or {})
    elif ref.get('arxiv'):
        found = arxiv(re.sub(r'v\d+$', '', ref['arxiv']))
        if found is None:
            return {'status': 'ARXIV_NOT_FOUND'}
        result.update(found)
    else:
        return {'status': 'URL_ONLY'}
    result['title_similarity'] = similarity(ref.get('title', ''), found['title'])
    problems = []
    if result['title_similarity'] < 0.85:
        problems.append('title')
    if ref.get('year') and found.get('year') and abs(int(ref['year']) - int(found['year'])) > 1:
        problems.append('year')
    first = (ref.get('authors') or '').split(',')[0].strip()
    if first and not family_matches(first, found.get('first_author_family')):
        problems.append('first_author')
    result['status'] = 'MATCH' if not problems else 'MISMATCH'
    if problems:
        result['problems'] = problems
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--output', default=str(OUTPUT))
    args = parser.parse_args()
    refs = collect()
    records = {}
    for index, (key, item) in enumerate(sorted(refs.items()), 1):
        outcome = verify(item['reference'])
        outcome['lessons'] = sorted(set(item['lessons']))
        if item.get('library'):
            outcome['library_id'] = item['library']
        records[key] = outcome
        print(f"[{index}/{len(refs)}] {outcome['status']:<15} {key} :: {item['reference'].get('title', '')[:70]}", flush=True)
        time.sleep(0.2)
    summary = {status: sum(r['status'] == status for r in records.values())
               for status in sorted({r['status'] for r in records.values()})}
    report = {
        'checked_at_utc': datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        'method': 'Crossref works API (title similarity >= 0.85, year within 1, first-author family name); '
                  'OpenAlex and Crossref citation counts; arXiv API for preprints.',
        'summary': summary,
        'references': records,
    }
    Path(args.output).write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps(summary))
    return 0 if set(summary) <= {'MATCH'} else 1


if __name__ == '__main__':
    sys.exit(main())
